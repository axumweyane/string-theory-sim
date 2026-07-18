from agents.base import call


def propose(problem: str, transcript=None) -> dict:
    return call("physicist", "propose", {"task": "propose", "problem": problem}, transcript)


def design_test(hypothesis: str, novelty: dict, transcript=None) -> dict:
    return call(
        "physicist",
        "design_test",
        {
            "task": "design_test",
            "instruction": "Design a concrete, falsifiable numerical test of this hypothesis: "
            "specific calculation, quantitative predicted outcomes with tolerances that would "
            "support or refute it.",
            "hypothesis": hypothesis,
            "novelty_check": novelty,
        },
        transcript,
    )


def rebut(proposal: dict, attacks: list[dict], run_result: dict, transcript=None) -> dict:
    return call(
        "physicist",
        "rebut",
        {"task": "rebut", "proposal": proposal, "attacks": attacks, "run_result": run_result},
        transcript,
    )
