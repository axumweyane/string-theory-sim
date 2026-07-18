"""Single choke point for all model calls.

Model mix per the framework doc: Opus for deep reasoning + debate roles,
Sonnet for code + pattern work. System prompts are sent with a cache
breakpoint so repeated turns reuse the prefix.

Set MOCK_LLM=1 to run the whole loop offline with canned responses.
"""
import json
import os

OPUS = "claude-opus-4-8"
SONNET = "claude-sonnet-5"

MODEL_FOR_ROLE = {
    "physicist": OPUS,
    "validator": OPUS,
    "orchestrator": OPUS,
    "cross_specialist": OPUS,
    "engineer": SONNET,
    "analyst": SONNET,
}

_client = None


def complete(role: str, phase: str, system: str, payload: dict, schema: dict) -> dict:
    if os.environ.get("MOCK_LLM") == "1":
        from utils import mock

        return mock.respond(role, phase, payload)

    global _client
    if _client is None:
        import anthropic

        _client = anthropic.Anthropic()

    resp = _client.messages.create(
        model=MODEL_FOR_ROLE[role],
        max_tokens=16000,
        thinking={"type": "adaptive"},
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": json.dumps(payload, indent=2)}],
        output_config={"format": {"type": "json_schema", "schema": schema}},
    )
    if resp.stop_reason == "refusal":
        raise RuntimeError(f"{role}/{phase} was refused: {resp.stop_details}")
    text = next(b.text for b in resp.content if b.type == "text")
    return json.loads(text)


def web_research(query: str, max_uses: int = 8) -> dict:
    """Literature search via the server-side web_search tool.

    Returns {"findings": <text>, "sources": [{"title", "url"}, ...]}.
    Handles pause_turn (server-tool iteration limit) by resuming the turn.
    """
    if os.environ.get("MOCK_LLM") == "1":
        from utils import mock

        return mock.web_research(query)

    global _client
    if _client is None:
        import anthropic

        _client = anthropic.Anthropic()

    prompt = (
        "Search the physics literature (arXiv, journals, textbooks) for prior work on the "
        "following candidate result, then summarize what exists and how closely it matches:\n\n"
        f"{query}"
    )
    messages = [{"role": "user", "content": prompt}]
    for _ in range(5):
        resp = _client.messages.create(
            model=SONNET,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": max_uses}],
            messages=messages,
        )
        if resp.stop_reason != "pause_turn":
            break
        messages = [messages[0], {"role": "assistant", "content": resp.content}]

    findings = "".join(b.text for b in resp.content if b.type == "text")
    sources = []
    for b in resp.content:
        if b.type == "web_search_tool_result" and isinstance(b.content, list):
            for item in b.content:
                if getattr(item, "type", None) == "web_search_result":
                    sources.append({"title": item.title, "url": item.url})
    return {"findings": findings, "sources": sources}
