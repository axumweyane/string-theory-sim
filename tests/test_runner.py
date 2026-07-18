from utils.runner import run_simulation

OK_CODE = 'import json\nprint("RESULT_JSON: " + json.dumps({"x": 1.5}))\n'
BAD_CODE = "raise RuntimeError('boom')\n"
NO_METRICS = 'print("hello")\n'


def test_parses_result_json():
    r = run_simulation(OK_CODE, round_no=901)
    assert r["ok"] and r["metrics"] == {"x": 1.5}


def test_failing_code_reported():
    r = run_simulation(BAD_CODE, round_no=902)
    assert not r["ok"] and r["returncode"] != 0 and "boom" in r["stderr"]


def test_missing_metrics_is_not_ok():
    r = run_simulation(NO_METRICS, round_no=903)
    assert not r["ok"] and r["metrics"] is None and r["returncode"] == 0
