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
from utils import llm
from utils.problems import PROBLEMS
from utils.runner import run_simulation
from utils.transcript import Transcript

MAX_ROUNDS = 5
DOCS_DIR = Path(__file__).resolve().parent / "docs"


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
    for a in result.get("artifacts", []):
        print(f"  artifact: {a}")
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
    for h in memo.get("candidate_hypotheses", []):
        print(f"  candidate hypothesis: {h['statement']}")
        print(f'    -> Phase 2: python main.py --phase2 "{h["statement"]}"')
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


def run_phase2(hypothesis: str, slug: str) -> int:
    """Novelty check -> (if novel/uncertain) design test -> run -> validate -> memo."""
    transcript = Transcript(f"{slug}-phase2")
    print(f"=== phase 2: novelty check & test ===\nhypothesis: {hypothesis}")

    print("[analyst] searching literature (web_search)...")
    research = llm.web_research(hypothesis)
    transcript.log("analyst", "web_search", research)
    verdict = analyst.novelty(hypothesis, research, transcript)
    print(f"  -> novelty: {verdict['status']}")

    if verdict["status"] == "known":
        cites = "\n".join(f"- [{c['title']}]({c['url']})" for c in verdict["citations"]) or "- (none provided)"
        memo_md = (
            f"# Novelty check: already known\n\n## Hypothesis\n{hypothesis}\n\n"
            f"## Verdict\nAlready in the literature.\n\n{verdict['summary']}\n\n"
            f"## Citations\n{cites}\n\n## Reasoning\n{verdict['reasoning']}\n"
        )
        path = _write_memo(f"{slug}-phase2-known", memo_md)
        print(f"[analyst] already known — logged with citations: {path}")
        return 0

    print("[physicist] designing test...")
    test = physicist.design_test(hypothesis, verdict, transcript)
    print(f"  -> {test['model_name']}")

    print("[engineer] implementing + running test...")
    built = engineer.build(test, None, transcript)
    result = run_simulation(built["code"], round_no="p2")
    transcript.log("harness", "run", {k: v for k, v in result.items() if k != "stdout"})
    print(f"  -> ok={result['ok']} metrics={result['metrics']}")
    for a in result.get("artifacts", []):
        print(f"  artifact: {a}")

    print("[validator] judging result...")
    attack = validator_agent.attack(test, built, result, transcript)
    print(f"  -> verdict: {attack['verdict']}")

    print("[analyst] writing phase-2 memo...")
    memo = analyst.phase2_memo(hypothesis, verdict, test, result, attack, transcript)
    path = _write_memo(f"{slug}-phase2", memo["memo_markdown"])
    print(f"  -> outcome: {memo['outcome']} (confidence: {memo['confidence']})")
    print(f"=== phase 2 end — memo: {path}, transcript: {transcript.path} ===")
    return 0


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Adversarial multi-agent physics simulation panel")
    parser.add_argument("--task", choices=sorted(PROBLEMS), default="string-modes",
                        help="named problem preset (default: string-modes)")
    parser.add_argument("--problem", default=None, help="free-form problem text (overrides --task)")
    parser.add_argument("--slug", default=None)
    parser.add_argument("--phase2", metavar="HYPOTHESIS", default=None,
                        help="run Phase 2 novelty-check and test on the given hypothesis")
    args = parser.parse_args()

    preset = PROBLEMS[args.task]
    problem = args.problem or preset["text"]
    slug = re.sub(r"[^a-z0-9-]", "-", (args.slug or preset["slug"]).lower())
    mode = "MOCK" if os.environ.get("MOCK_LLM") == "1" else "LIVE"

    if args.phase2:
        return run_phase2(args.phase2, slug)

    transcript = Transcript(slug)
    print(f"=== debate start [{mode}] slug={slug} ===")
    graph = build_graph()
    final = graph.invoke(
        {"problem": problem, "slug": slug, "transcript": transcript},
        {"recursion_limit": 60},
    )
    print(f"=== debate end: {final['resolution']['decision']} — transcript: {transcript.path} ===")
    return 0 if final["resolution"]["decision"] == "accept" else 1


if __name__ == "__main__":
    sys.exit(main())
