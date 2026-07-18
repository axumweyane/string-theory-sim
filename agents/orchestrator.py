from agents.base import call


def resolve(proposal: dict, attacks: list[dict], rebuttal: dict, run_result: dict, round_no: int, max_rounds: int, transcript=None) -> dict:
    return call(
        "orchestrator",
        "resolve",
        {
            "task": "resolve",
            "round": round_no,
            "max_rounds": max_rounds,
            "proposal": proposal,
            "attacks": attacks,
            "rebuttal": rebuttal,
            "run_result": run_result,
        },
        transcript,
    )
