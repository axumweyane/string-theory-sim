from agents.base import call


def attack(proposal: dict, build: dict, run_result: dict, transcript=None) -> dict:
    return call(
        "analyst",
        "attack_analyst",
        {"task": "attack", "proposal": proposal, "build": build, "run_result": run_result},
        transcript,
    )


def novelty(hypothesis: str, research: dict, transcript=None) -> dict:
    return call(
        "analyst",
        "novelty",
        {
            "task": "novelty",
            "hypothesis": hypothesis,
            "literature_findings": research["findings"],
            "sources": research["sources"],
        },
        transcript,
    )


def phase2_memo(hypothesis: str, novelty_verdict: dict, test: dict, run_result: dict, attack: dict, transcript=None) -> dict:
    return call(
        "analyst",
        "phase2_memo",
        {
            "task": "phase2_memo",
            "hypothesis": hypothesis,
            "novelty_check": novelty_verdict,
            "test_design": test,
            "run_result": run_result,
            "validator_attack": attack,
        },
        transcript,
    )


def analyze(proposal: dict, run_result: dict, debate_tail: list[dict], transcript=None) -> dict:
    return call(
        "analyst",
        "analyze",
        {"task": "analyze", "proposal": proposal, "run_result": run_result, "debate": debate_tail},
        transcript,
    )
