"""Debate transcript: shared memory on disk, one JSON file per debate.

Persisted after every event so a crashed run leaves a full record, and so
agents can be fed the transcript instead of re-sending full chat history.
"""
import json
import time
from pathlib import Path

DEBATES_DIR = Path(__file__).resolve().parent.parent / "debates"


class Transcript:
    def __init__(self, slug: str):
        DEBATES_DIR.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        self.path = DEBATES_DIR / f"{stamp}_{slug}.json"
        self.events: list[dict] = []

    def log(self, role: str, phase: str, content: dict) -> None:
        self.events.append(
            {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "role": role, "phase": phase, "content": content}
        )
        self.path.write_text(json.dumps(self.events, indent=2))

    def tail(self, n: int = 12) -> list[dict]:
        return self.events[-n:]
