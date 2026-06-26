# -*- coding: utf-8 -*-
"""Counterdraft web app: site + /api/audit gated by LemonSqueezy license keys.

Flow: customer pays on LemonSqueezy -> gets a license key -> enters key + contract
on /app.html -> backend "activates" one slot of the key (1 slot = 1 audit) -> runs
the AI audit. Single audit product = activation limit 1; Starter/Pro = higher.

No database, no accounts. License validation is done via LemonSqueezy's public
license endpoints (keyed by the license itself, no API token required).
"""
import os
import json
import uuid
import urllib.request
import urllib.parse
import urllib.error

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import engine

app = FastAPI(title="Counterdraft")
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))
LS_BASE = "https://api.lemonsqueezy.com/v1/licenses"
# Set to "1" in Render env to bypass license check (for your own testing only).
BYPASS = os.environ.get("COUNTERDRAFT_BYPASS_LICENSE") == "1"


class AuditReq(BaseModel):
    text: str = ""
    jurisdiction: str = "us"
    license_key: str = ""


def _ls_post(path, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        LS_BASE + path, data=body,
        headers={"Accept": "application/json",
                 "Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode()), None
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode()), None
        except Exception:
            return None, "License service error (%s)." % e.code
    except Exception as e:
        return None, "Could not reach license service: %s" % e


def consume_license(key):
    """Activate one slot of the key. Returns (ok, message)."""
    key = (key or "").strip()
    if not key:
        return False, "A license key is required. Buy an audit to get one."
    data, err = _ls_post("/activate", {
        "license_key": key,
        "instance_name": "counterdraft-" + uuid.uuid4().hex[:12],
    })
    if err:
        return False, err
    if not data or not data.get("activated"):
        return False, (data or {}).get("error") or \
            "This license key is invalid or has reached its audit limit."
    lk = data.get("license_key", {})
    if lk.get("status") in ("expired", "disabled"):
        return False, "This license key is %s." % lk.get("status")
    return True, None


@app.get("/api/health")
def health():
    return {"ok": True, "ai_configured": engine.llm.have_key(),
            "license_gate": (not BYPASS)}


@app.post("/api/audit")
def api_audit(req: AuditReq):
    text = (req.text or "").strip()
    if len(text) < 40:
        return JSONResponse(
            {"error": "Please paste a longer contract (at least a few clauses)."},
            status_code=400)

    if not BYPASS:
        ok, msg = consume_license(req.license_key)
        if not ok:
            return JSONResponse({"error": msg, "need_license": True}, status_code=402)

    juris = req.jurisdiction if req.jurisdiction in ("us", "ua") else "us"
    try:
        return engine.run(text, jurisdiction=juris)
    except Exception as e:
        return JSONResponse({"error": "Audit failed: %s" % e}, status_code=500)


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
