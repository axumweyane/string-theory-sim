import json

from utils.schema import SCHEMAS

EXPECTED_PHASES = {
    "propose", "build", "attack_validator", "attack_analyst", "rebut", "resolve", "analyze",
    "novelty", "design_test", "phase2_memo",
}


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


def test_viz_mock_responses_fit_schemas():
    from utils import mock

    payload = {
        "problem": "project string vibration into 3D with an animation and rotating camera",
        "attacks": [{"verdict": "pass"}],
        "run_result": {
            "metrics": {
                "energy_rel_drift": 1e-15, "closure_error": 1e-16,
                "node_count": 6, "expected_nodes": 6, "n_frames": 72,
            }
        },
    }
    for phase in ("propose", "build", "attack_validator", "attack_analyst", "rebut", "resolve", "analyze"):
        out = mock.respond("any", phase, payload)
        assert set(out) == set(SCHEMAS[phase]["properties"]), phase


def test_string_mock_responses_fit_schemas():
    from utils import mock

    payload = {
        "problem": "closed string compactified on a circle, winding modes",
        "hypothesis": "massless-state count jumps at the self-dual radius",
        "proposal": {"rationale": "design_test: localization scan"},
        "attacks": [{"verdict": "pass"}],
        "run_result": {"metrics": {"t_duality_max_dev": 0.0, "massless_generic": 1, "massless_selfdual": 9}},
    }
    for phase, schema in SCHEMAS.items():
        out = mock.respond("any", phase, payload)
        assert set(out) == set(schema["properties"]), phase
