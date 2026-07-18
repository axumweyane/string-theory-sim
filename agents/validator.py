from agents.base import call


def attack(proposal: dict, build: dict, run_result: dict, transcript=None) -> dict:
    return call(
        "validator",
        "attack_validator",
        {"task": "attack", "proposal": proposal, "build": build, "run_result": run_result},
        transcript,
    )
