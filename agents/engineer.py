from agents.base import call


def build(proposal: dict, previous_result: dict | None = None, transcript=None) -> dict:
    payload = {"task": "build", "proposal": proposal}
    if previous_result:
        payload["previous_run"] = previous_result
    return call("engineer", "build", payload, transcript)
