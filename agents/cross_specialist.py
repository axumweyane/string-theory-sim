from agents.base import call


def bridge(collision: dict, transcript=None) -> dict:
    return call("cross_specialist", "bridge", {"task": "bridge", "collision": collision}, transcript)
