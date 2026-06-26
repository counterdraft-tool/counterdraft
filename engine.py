# -*- coding: utf-8 -*-
"""Counterdraft pipeline: text -> classify -> audit (JSON) -> counter-letter.
Jurisdiction-aware: jurisdiction='us' (default) or 'ua' (Ukraine, CKU)."""

import json

import prompts, llm
from taxonomy import contract_types
from mock import MOCK_AUDIT, MOCK_LETTER, MOCK_AUDIT_UA, MOCK_LETTER_UA


def classify(text, jurisdiction="us", **kw):
    out = llm.complete_json(prompts.classify_system(jurisdiction), text[:6000],
                            max_tokens=200, **kw)
    types = contract_types(jurisdiction)
    ct = out.get("contract_type", "other")
    if ct not in types and ct != "other":
        ct = "other"
    out["contract_type"] = ct
    return out


def audit(text, contract_type, jurisdiction="us", **kw):
    system = prompts.audit_system(contract_type, jurisdiction)
    user = prompts.AUDIT_USER_TEMPLATE.format(contract_text=text)
    return llm.complete_json(system, user, max_tokens=4000, **kw)


def counter_letter(audit_json, jurisdiction="us", **kw):
    user = prompts.COUNTER_USER_TEMPLATE.format(
        audit_json=json.dumps(audit_json, ensure_ascii=False, indent=2))
    return llm.complete(prompts.counter_system(jurisdiction), user, max_tokens=1500, **kw)


def _default_type(jurisdiction):
    return "ua_supply" if jurisdiction == "ua" else "vendor_msa"


def run(text, contract_type=None, jurisdiction="us", force_mock=False, model=None):
    if force_mock or not llm.have_key():
        if jurisdiction == "ua":
            a, letter, ct = MOCK_AUDIT_UA, MOCK_LETTER_UA, "ua_services"
        else:
            a, letter, ct = MOCK_AUDIT, MOCK_LETTER, "vendor_msa"
        return {
            "jurisdiction": jurisdiction, "contract_type": ct,
            "classify": {"contract_type": ct, "confidence": 0.95,
                         "label": contract_types(jurisdiction).get(ct, ct)},
            "audit": a, "letter": letter, "mocked": True,
        }

    kw = {"model": model} if model else {}
    if contract_type is None:
        cls = classify(text, jurisdiction, **kw)
        contract_type = cls["contract_type"]
        if contract_type == "other":
            contract_type = _default_type(jurisdiction)
    else:
        cls = {"contract_type": contract_type, "confidence": 1.0,
               "label": contract_types(jurisdiction).get(contract_type, contract_type)}

    a = audit(text, contract_type, jurisdiction, **kw)
    letter = counter_letter(a, jurisdiction, **kw)
    return {
        "jurisdiction": jurisdiction, "contract_type": contract_type,
        "classify": cls, "audit": a, "letter": letter, "mocked": False,
    }
