"""Shared plumbing: load each agent's system prompt once, call the model with
a structured-output schema, log everything to the debate transcript."""
import functools
from pathlib import Path

from utils import llm
from utils.schema import SCHEMAS

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


@functools.lru_cache(maxsize=None)
def system_prompt(role: str) -> str:
    return (PROMPTS_DIR / f"{role}.md").read_text()


def call(role: str, phase: str, payload: dict, transcript=None) -> dict:
    result = llm.complete(role, phase, system_prompt(role), payload, SCHEMAS[phase])
    if transcript is not None:
        transcript.log(role, phase, result)
    return result
