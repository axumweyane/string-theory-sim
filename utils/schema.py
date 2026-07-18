"""JSON schemas for structured agent outputs.

Every agent reply is forced through one of these via the API's
output_config.format json_schema, so downstream code never parses prose.
"""


def _obj(properties: dict, required: list[str] | None = None) -> dict:
    return {
        "type": "object",
        "properties": properties,
        "required": required if required is not None else list(properties),
        "additionalProperties": False,
    }


_ISSUE = _obj(
    {
        "claim": {"type": "string", "description": "The specific claim being challenged"},
        "reason": {"type": "string", "description": "Logical reason the claim may be wrong"},
        "severity": {"type": "string", "enum": ["blocking", "major", "minor"]},
    }
)

PROPOSE = _obj(
    {
        "model_name": {"type": "string"},
        "equations": {"type": "array", "items": {"type": "string"}},
        "assumptions": {"type": "array", "items": {"type": "string"}},
        "predicted_behavior": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Concrete, checkable predictions the simulation must reproduce",
        },
        "rationale": {"type": "string"},
    }
)

BUILD = _obj(
    {
        "code": {"type": "string", "description": "Complete runnable Python module"},
        "how_it_maps_to_theory": {"type": "string"},
        "expected_metrics": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Names of metrics emitted in the RESULT_JSON line",
        },
    }
)

ATTACK = _obj(
    {
        "verdict": {"type": "string", "enum": ["pass", "fail"]},
        "issues": {"type": "array", "items": _ISSUE},
        "summary": {"type": "string"},
    }
)

REBUT = _obj(
    {
        "responses": {
            "type": "array",
            "items": _obj(
                {
                    "issue": {"type": "string"},
                    "stance": {"type": "string", "enum": ["accept", "reject"]},
                    "reason": {"type": "string"},
                }
            ),
        },
        "revised": {
            "type": "boolean",
            "description": "True if the proposal below supersedes the previous one",
        },
        "revision": {
            "anyOf": [PROPOSE, {"type": "null"}],
            "description": "Full revised proposal when revised is true, else null",
        },
    }
)

RESOLVE = _obj(
    {
        "decision": {"type": "string", "enum": ["accept", "continue", "escalate"]},
        "applied_rule": {
            "type": "string",
            "description": "Priority rule used on deadlock: evidence > derivation > heuristic",
        },
        "reasoning": {"type": "string"},
        "memo_markdown": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": "Escalation memo summarizing both sides; null unless decision is escalate",
        },
    }
)

_HYPOTHESIS = _obj(
    {
        "statement": {"type": "string", "description": "The candidate result, stated precisely"},
        "argument": {"type": "string", "description": "The logical/numerical argument behind it"},
        "novelty_rationale": {"type": "string", "description": "Why this might be new (or where it likely already exists)"},
    }
)

ANALYZE = _obj(
    {
        "title": {"type": "string"},
        "patterns": {"type": "array", "items": {"type": "string"}},
        "candidate_hypotheses": {
            "type": "array",
            "items": _HYPOTHESIS,
            "description": "Results that look potentially novel — empty list if nothing qualifies",
        },
        "next_directions": {"type": "array", "items": {"type": "string"}},
        "memo_markdown": {"type": "string", "description": "Full research memo in Markdown"},
    }
)

NOVELTY = _obj(
    {
        "status": {"type": "string", "enum": ["known", "novel", "uncertain"]},
        "summary": {"type": "string", "description": "What the literature search found"},
        "citations": {
            "type": "array",
            "items": _obj({"title": {"type": "string"}, "url": {"type": "string"}}),
        },
        "reasoning": {"type": "string"},
    }
)

PHASE2_MEMO = _obj(
    {
        "title": {"type": "string"},
        "hypothesis": {"type": "string"},
        "outcome": {"type": "string", "enum": ["supported", "refuted", "inconclusive"]},
        "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        "memo_markdown": {
            "type": "string",
            "description": "Memo: hypothesis, novelty-check result, test, outcome, honest confidence, "
            "and an explicit statement that experimental validation is still required",
        },
    }
)

SCHEMAS = {
    "propose": PROPOSE,
    "build": BUILD,
    "attack_validator": ATTACK,
    "attack_analyst": ATTACK,
    "rebut": REBUT,
    "resolve": RESOLVE,
    "analyze": ANALYZE,
    "novelty": NOVELTY,
    "design_test": PROPOSE,  # a Phase-2 test is proposal-shaped: equations, assumptions, checkable predictions
    "phase2_memo": PHASE2_MEMO,
}
