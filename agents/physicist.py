from agents.base import call


def propose(problem: str, transcript=None) -> dict:
    return call("physicist", "propose", {"task": "propose", "problem": problem}, transcript)


def rebut(proposal: dict, attacks: list[dict], run_result: dict, transcript=None) -> dict:
    return call(
        "physicist",
        "rebut",
        {"task": "rebut", "proposal": proposal, "attacks": attacks, "run_result": run_result},
        transcript,
    )
