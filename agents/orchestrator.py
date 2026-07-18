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


def collide(round_no: int, seed_collisions: list, deaths: list, transcript=None) -> dict:
    return call(
        "orchestrator",
        "collide",
        {"task": "collide", "round": round_no, "seed_collisions": seed_collisions,
         "prior_deaths": deaths[-10:]},
        transcript,
    )


def scorecard(collision: dict, proposal: dict, run_result: dict, attack: dict, novelty: dict, transcript=None) -> dict:
    return call(
        "orchestrator",
        "scorecard",
        {"task": "scorecard", "collision": collision, "proposal": proposal,
         "run_result": run_result, "validator_attack": attack, "novelty_check": novelty,
         "kill_thresholds": {"mathematical_closure": 6, "artifact_resistance": 7,
                             "prediction_novelty": 7, "literature_gap": 6,
                             "cross_field_genuineness": 6}},
        transcript,
    )
