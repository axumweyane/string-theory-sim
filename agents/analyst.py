from agents.base import call


def attack(proposal: dict, build: dict, run_result: dict, transcript=None) -> dict:
    return call(
        "analyst",
        "attack_analyst",
        {"task": "attack", "proposal": proposal, "build": build, "run_result": run_result},
        transcript,
    )


def analyze(proposal: dict, run_result: dict, debate_tail: list[dict], transcript=None) -> dict:
    return call(
        "analyst",
        "analyze",
        {"task": "analyze", "proposal": proposal, "run_result": run_result, "debate": debate_tail},
        transcript,
    )
