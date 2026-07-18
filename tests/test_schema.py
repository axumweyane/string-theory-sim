import json

from utils.schema import SCHEMAS

EXPECTED_PHASES = {"propose", "build", "attack_validator", "attack_analyst", "rebut", "resolve", "analyze"}


def test_all_phases_present():
    assert set(SCHEMAS) == EXPECTED_PHASES


def test_schemas_are_strict_objects():
    for name, schema in SCHEMAS.items():
        assert schema["type"] == "object", name
        assert schema["additionalProperties"] is False, name
        assert set(schema["required"]) <= set(schema["properties"]), name
        json.dumps(schema)  # serializable


def test_mock_responses_fit_schemas():
    from utils import mock

    payload = {"attacks": [{"verdict": "pass"}], "run_result": {"metrics": {"period_error": 1e-6, "energy_drift": 1e-9}}}
    for phase, schema in SCHEMAS.items():
        out = mock.respond("any", phase, payload)
        assert set(out) == set(schema["properties"]), phase
