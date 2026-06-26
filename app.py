# -*- coding: utf-8 -*-
"""Counterdraft web app: serves the site + a real /api/audit endpoint.

Run locally:   uvicorn app:app --reload
Deploy:        uvicorn app:app --host 0.0.0.0 --port $PORT
Set ANTHROPIC_API_KEY in the environment for real audits (otherwise demo output).
"""
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import engine

app = FastAPI(title="Counterdraft")

STATIC_DIR = os.path.dirname(os.path.abspath(__file__))


class AuditReq(BaseModel):
    text: str = ""
    jurisdiction: str = "us"


@app.get("/api/health")
def health():
    return {"ok": True, "ai_configured": engine.llm.have_key()}


@app.post("/api/audit")
def api_audit(req: AuditReq):
    text = (req.text or "").strip()
    if len(text) < 40:
        return JSONResponse(
            {"error": "Please paste a longer contract (at least a few clauses)."},
            status_code=400)
    if req.jurisdiction not in ("us", "ua"):
        req.jurisdiction = "us"
    try:
        result = engine.run(text, jurisdiction=req.jurisdiction)
        return result
    except Exception as e:
        return JSONResponse({"error": "Audit failed: %s" % e}, status_code=500)


# serve static site (index.html at /, app.html at /app.html, logos, etc.)
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
