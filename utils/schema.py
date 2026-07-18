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

ANALYZE = _obj(
    {
        "title": {"type": "string"},
        "patterns": {"type": "array", "items": {"type": "string"}},
        "next_directions": {"type": "array", "items": {"type": "string"}},
        "memo_markdown": {"type": "string", "description": "Full research memo in Markdown"},
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
}
