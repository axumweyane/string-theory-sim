"""Debate driver: propose -> build -> attack -> rebut -> resolve -> iterate.

LangGraph state machine per the framework blueprint. Run:
    python main.py                          # 2-body gravity, live API
    MOCK_LLM=1 python main.py               # offline smoke test, canned agents
    python main.py --problem "..." --slug harmonic-oscillator
"""
import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from agents import analyst, engineer, orchestrator, physicist
from agents import validator as validator_agent
from utils.runner import run_simulation
from utils.transcript import Transcript

MAX_ROUNDS = 5
DOCS_DIR = Path(__file__).resolve().parent / "docs"

DEFAULT_PROBLEM = (
    "Model the gravitational two-body problem (a small mass orbiting a large one). "
    "Provide the governing equations, an analytic ground truth (Kepler's third law and "
    "energy conservation), and quantitative predictions a numerical simulation must "
    "reproduce. This validates the panel's pipeline before scaling to harmonic "
    "oscillators and then higher-dimensional (string-theory) mathematics."
)


class DebateState(TypedDict, total=False):
    problem: str
    slug: str
    transcript: Any
    proposal: dict
    build: dict
    run_result: dict
    attacks: list
    rebuttal: dict
    resolution: dict
    round: int


def node_propose(state: DebateState) -> dict:
    print("[physicist] proposing model...")
    proposal = physicist.propose(state["problem"], state["transcript"])
    print(f"  -> {proposal['model_name']}")
    return {"proposal": proposal, "round": 1}


def node_build(state: DebateState) -> dict:
    print(f"[engineer] round {state['round']}: implementing + running simulation...")
    built = engineer.build(state["proposal"], state.get("run_result"), state["transcript"])
    result = run_simulation(built["code"], state["round"])
    state["transcript"].log("harness", "run", {k: v for k, v in result.items() if k != "stdout"})
    print(f"  -> ok={result['ok']} metrics={result['metrics']}")
    return {"build": built, "run_result": result}


def node_attack(state: DebateState) -> dict:
    print("[validator+analyst] attacking...")
    a1 = validator_agent.attack(state["proposal"], state["build"], state["run_result"], state["transcript"])
    a2 = analyst.attack(state["proposal"], state["build"], state["run_result"], state["transcript"])
    print(f"  -> validator: {a1['verdict']}, analyst: {a2['verdict']}")
    return {"attacks": [a1, a2]}


def node_rebut(state: DebateState) -> dict:
    print("[physicist] rebutting...")
    rebuttal = physicist.rebut(state["proposal"], state["attacks"], state["run_result"], state["transcript"])
    out: dict = {"rebuttal": rebuttal}
    if rebuttal.get("revised") and rebuttal.get("revision"):
        print("  -> proposal revised")
        out["proposal"] = rebuttal["revision"]
    return out


def node_resolve(state: DebateState) -> dict:
    print("[orchestrator] resolving...")
    res = orchestrator.resolve(
        state["proposal"], state["attacks"], state["rebuttal"], state["run_result"],
        state["round"], MAX_ROUNDS, state["transcript"],
    )
    print(f"  -> decision: {res['decision']} ({res['applied_rule']})")
    return {"resolution": res, "round": state["round"] + 1}


def node_analyze(state: DebateState) -> dict:
    print("[analyst] writing research memo...")
    memo = analyst.analyze(state["proposal"], state["run_result"], state["transcript"].tail(), state["transcript"])
    path = _write_memo(state["slug"], memo["memo_markdown"])
    print(f"  -> {path}")
    return {}


def node_escalate(state: DebateState) -> dict:
    memo = state["resolution"].get("memo_markdown") or "Escalated without memo — inspect the debate transcript."
    path = _write_memo(f"{state['slug']}-ESCALATION", memo)
    print(f"[orchestrator] ESCALATED to human — memo at {path}")
    return {}


def _write_memo(slug: str, markdown: str) -> Path:
    DOCS_DIR.mkdir(exist_ok=True)
    path = DOCS_DIR / f"{slug}.md"
    path.write_text(markdown)
    return path


def route_after_resolve(state: DebateState) -> str:
    decision = state["resolution"]["decision"]
    if decision == "accept":
        return "analyze"
    if decision == "continue" and state["round"] <= MAX_ROUNDS:
        return "build"
    return "escalate"


def build_graph():
    g = StateGraph(DebateState)
    g.add_node("propose", node_propose)
    g.add_node("build", node_build)
    g.add_node("attack", node_attack)
    g.add_node("rebut", node_rebut)
    g.add_node("resolve", node_resolve)
    g.add_node("analyze", node_analyze)
    g.add_node("escalate", node_escalate)
    g.set_entry_point("propose")
    g.add_edge("propose", "build")
    g.add_edge("build", "attack")
    g.add_edge("attack", "rebut")
    g.add_edge("rebut", "resolve")
    g.add_conditional_edges("resolve", route_after_resolve, {"analyze": "analyze", "build": "build", "escalate": "escalate"})
    g.add_edge("analyze", END)
    g.add_edge("escalate", END)
    return g.compile()


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Adversarial multi-agent physics simulation panel")
    parser.add_argument("--problem", default=DEFAULT_PROBLEM)
    parser.add_argument("--slug", default="two-body-gravity")
    args = parser.parse_args()

    slug = re.sub(r"[^a-z0-9-]", "-", args.slug.lower())
    transcript = Transcript(slug)
    mode = "MOCK" if os.environ.get("MOCK_LLM") == "1" else "LIVE"
    print(f"=== debate start [{mode}] slug={slug} ===")

    graph = build_graph()
    final = graph.invoke(
        {"problem": args.problem, "slug": slug, "transcript": transcript},
        {"recursion_limit": 60},
    )

    print(f"=== debate end: {final['resolution']['decision']} — transcript: {transcript.path} ===")
    return 0 if final["resolution"]["decision"] == "accept" else 1


if __name__ == "__main__":
    sys.exit(main())
