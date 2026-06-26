"""
Thin wrapper around the Anthropic API.

Set your key in the environment:  export ANTHROPIC_API_KEY=sk-ant-...
Or put it in a .env file (see .env.example) — loaded automatically if python-dotenv
is installed.

Default model is configurable via COUNTERDRAFT_MODEL. We default to a Sonnet-class
model for cost/quality balance on contract analysis.
"""

import os
import json

DEFAULT_MODEL = os.environ.get("COUNTERDRAFT_MODEL", "claude-sonnet-4-6")


def _load_dotenv():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass


def have_key() -> bool:
    _load_dotenv()
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def complete(system: str, user: str, max_tokens: int = 4000,
             model: str | None = None, temperature: float = 0.2) -> str:
    """Single-turn completion. Returns the text of the model's reply."""
    _load_dotenv()
    try:
        import anthropic
    except ImportError as e:
        raise ImportError("anthropic not installed. Run: pip install anthropic") from e

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    resp = client.messages.create(
        model=model or DEFAULT_MODEL,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in resp.content if block.type == "text")


def complete_json(system: str, user: str, **kw) -> dict:
    """Completion that must return JSON. Strips code fences and parses."""
    raw = complete(system, user, **kw)
    return _parse_json(raw)


def _parse_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        # strip ```json ... ``` fences
        raw = raw.split("```", 2)[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip().rstrip("`").strip()
    # find first { and last }
    start, end = raw.find("{"), raw.rfind("}")
    if start != -1 and end != -1:
        raw = raw[start:end + 1]
    return json.loads(raw)
