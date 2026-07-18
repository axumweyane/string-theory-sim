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

from agents import analyst, cross_specialist, engineer, orchestrator, physicist
from agents import validator as validator_agent
from utils import llm
from utils.problems import DEEP_VARIATIONS, INNOVATION_CHALLENGES, PROBLEMS, SEED_COLLISIONS
from utils.runner import run_simulation
from utils.transcript import Transcript

MAX_ROUNDS = 5  # default; deep mode raises it (hard safety stop, not a target)
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
    memo: dict
    round: int


def node_propose(state: DebateState) -> dict:
    print("[physicist] proposing model...")
    proposal = physicist.propose(state["problem"], state["transcript"])
    print(f"  -> {proposal['model_name']}")
    return {"proposal": proposal, "round": 1}


def node_build(state: DebateState) -> dict:
    print(f"[engineer] round {state['round']}: implementing + running simulation...")
    built = engineer.build(state["proposal"], state.get("run_result"), state["transcript"])
    result = run_simulation(built["code"], f"{state['slug']}-r{state['round']}")
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
    return {"memo": memo}


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


def run_phase2(hypothesis: str, slug: str) -> dict:
    """Novelty check -> (if novel/uncertain) design test -> run -> validate -> memo.

    Returns {"status": "known", "memo": path} or
            {"status": "tested", "outcome", "confidence", "memo": path}.
    """
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
        return {"status": "known", "memo": str(path)}

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
    return {"status": "tested", "outcome": memo["outcome"], "confidence": memo["confidence"], "memo": str(path)}


def run_debate(problem: str, slug: str) -> dict:
    transcript = Transcript(slug)
    print(f"=== debate start slug={slug} (round cap {MAX_ROUNDS}) ===")
    graph = build_graph()
    final = graph.invoke(
        {"problem": problem, "slug": slug, "transcript": transcript},
        {"recursion_limit": 8 * MAX_ROUNDS + 20},
    )
    print(f"=== debate end: {final['resolution']['decision']} — transcript: {transcript.path} ===")
    return final


def run_deep(variations=DEEP_VARIATIONS, summary_slug="deep-research-summary",
             headline="Deep open-ended research") -> int:
    """Iterate a variation/challenge queue until a novel candidate survives its
    falsifiable test, or the queue is exhausted. Known results are logged with
    citations and the agents move ON."""
    stats = {"explored": 0, "accepted": 0, "deadlocked": 0, "hypotheses": 0, "known": 0, "tested": []}
    survivor = None

    for var in variations:
        print(f"\n########## target {stats['explored'] + 1}/{len(variations)}: {var['name']} ##########")
        stats["explored"] += 1
        final = run_debate(var["text"], var["slug"])
        if final["resolution"]["decision"] != "accept":
            stats["deadlocked"] += 1
            print("[deep] no accepted result for this variation — moving on")
            continue
        stats["accepted"] += 1

        for h in final.get("memo", {}).get("candidate_hypotheses", []):
            stats["hypotheses"] += 1
            print(f"\n[deep] Phase 2 on candidate: {h['statement']}")
            r = run_phase2(h["statement"], var["slug"])
            if r["status"] == "known":
                stats["known"] += 1
                continue
            stats["tested"].append({"hypothesis": h["statement"], **r})
            if r["outcome"] == "supported":
                survivor = {"variation": var["name"], "hypothesis": h["statement"], **r}
                break
        if survivor:
            break

    lines = [
        f"# {headline} — run summary",
        "",
        f"- targets explored: {stats['explored']}/{len(variations)}",
        f"- debates accepted: {stats['accepted']}  |  deadlocked/escalated: {stats['deadlocked']}",
        f"- candidate hypotheses raised: {stats['hypotheses']}",
        f"- already known (cited, moved on): {stats['known']}",
        f"- novel candidates tested: {len(stats['tested'])}",
    ]
    if survivor:
        lines += [
            "",
            "## Novel candidate SURVIVED its falsifiable test",
            f"- variation: {survivor['variation']}",
            f"- hypothesis: {survivor['hypothesis']}",
            f"- outcome: {survivor['outcome']} (confidence: {survivor['confidence']})",
            f"- memo: {survivor['memo']}",
            "",
            "A surviving mathematical result is promising math, NOT a discovery about the "
            "universe — experimental validation is still required for any claim about reality.",
        ]
    else:
        lines += ["", "## No novel candidate survived — target space exhausted",
                  "Everything surfaced was already in the literature or failed its test. "
                  "That is the normal outcome of honest research."]
    summary = "\n".join(lines) + "\n"
    path = _write_memo(summary_slug, summary)
    print(f"\n{summary}\nsummary written to {path}")
    return 0


FRONTIER_THRESHOLDS = {"mathematical_closure": 6, "artifact_resistance": 7,
                       "prediction_novelty": 7, "literature_gap": 6, "cross_field_genuineness": 6}


def run_frontier(max_rounds: int = 40) -> int:
    """Hunt for novelty at field collisions: collide -> propose -> build -> attack
    -> literature check -> scorecard. Deaths are logged; the failure map is the
    product even with zero survivors."""
    transcript = Transcript("frontier")
    deaths, near_misses = [], []

    for rnd in range(1, max_rounds + 1):
        print(f"\n########## frontier round {rnd}/{max_rounds} ##########")
        collision = orchestrator.collide(rnd, SEED_COLLISIONS, deaths, transcript)
        print(f"[orchestrator] collide: {collision['field_a']}  x  {collision['field_b']}")
        print(f"  bridge: {collision['bridge_question']}")

        bridge = cross_specialist.bridge(collision, transcript)
        print(f"[cross-specialist] import: {bridge['imported_structure']}")

        proposal = physicist.propose(
            f"Frontier collision. Field A: {collision['field_a']}. Field B: {collision['field_b']}. "
            f"Bridge question: {collision['bridge_question']}. Imported structure from Field B: "
            f"{bridge['imported_structure']} — {bridge['what_it_constrains']}. Computable test: "
            f"{bridge['computable_test']}. Build the joint mechanism.",
            transcript,
        )
        print(f"[physicist+cross-specialist] proposal: {proposal['model_name']}")

        built = engineer.build(proposal, None, transcript)
        result = run_simulation(built["code"], f"frontier-r{rnd}")
        transcript.log("harness", "run", {k: v for k, v in result.items() if k != "stdout"})
        print(f"[engineer] ok={result['ok']} metrics={result['metrics']}")

        attack = validator_agent.attack(proposal, built, result, transcript)
        print(f"[validator] {attack['verdict']}")
        if attack["verdict"] == "fail" or not result["ok"]:
            death = {"round": rnd, "collision": collision["bridge_question"],
                     "killed_by": "validator" if result["ok"] else "runtime",
                     "why": attack["summary"]}
            deaths.append(death)
            print(f"  -> DEAD ({death['killed_by']}): {death['why'][:120]}")
            continue

        research = llm.web_research(f"{proposal['model_name']}: {proposal['rationale']}")
        transcript.log("analyst", "web_search", research)
        novelty = analyst.novelty(proposal["model_name"] + " — " + proposal["rationale"], research, transcript)
        print(f"[analyst] novelty: {novelty['status']}")

        card = orchestrator.scorecard(collision, proposal, result, attack, novelty, transcript)
        axes = {k: card[k] for k in FRONTIER_THRESHOLDS}
        passed = all(card[k] >= v for k, v in FRONTIER_THRESHOLDS.items())
        print(f"[orchestrator] scorecard {axes} -> {card['verdict']}")

        if card["verdict"] == "survivor" and passed:
            memo = (f"# FRONTIER SURVIVOR (round {rnd})\n\n**Do not announce — hand to a domain "
                    f"expert first.**\n\n## Collision\n{collision['field_a']} x {collision['field_b']}\n\n"
                    f"## Mechanism\n{proposal['model_name']}\n\nEquations: {proposal['equations']}\n\n"
                    f"## Scorecard\n{axes}\n\n## Reasoning\n{card['reasoning']}\n\n"
                    f"Math is not physics: this is a promising mathematical claim requiring expert "
                    f"review and, ultimately, experiment — not a discovery.\n")
            path = _write_memo(f"frontier-survivor-r{rnd}", memo)
            print(f"SURVIVOR — memo: {path}")
            return 0
        if card["verdict"] == "near_miss":
            near_misses.append({"round": rnd, "claim": proposal["model_name"], "axes": axes,
                                "why_near": card["reasoning"]})
        deaths.append({"round": rnd, "collision": collision["bridge_question"],
                       "killed_by": "scorecard", "why": card["reasoning"]})

    lines = ["# Frontier run — dependency map (no survivor)", "",
             f"- rounds: {len(deaths)}; near-misses: {len(near_misses)}", "", "## Deaths"]
    lines += [f"- r{d['round']} [{d['killed_by']}] {d['collision']}: {d['why']}" for d in deaths]
    if near_misses:
        lines += ["", "## Near-misses (worth a human expert's second look)"]
        lines += [f"- r{m['round']} {m['claim']} — {m['axes']}: {m['why_near']}" for m in near_misses]
    lines += ["", "Math is not physics; every claim above requires expert review."]
    path = _write_memo("frontier-dependency-map", "\n".join(lines) + "\n")
    print(f"\nno survivor — dependency map: {path}")
    return 0


def main() -> int:
    load_dotenv()
    global MAX_ROUNDS
    parser = argparse.ArgumentParser(description="Adversarial multi-agent physics simulation panel")
    parser.add_argument("--task", choices=sorted(PROBLEMS), default="string-modes",
                        help="named problem preset (default: string-modes)")
    parser.add_argument("--problem", default=None, help="free-form problem text (overrides --task)")
    parser.add_argument("--slug", default=None)
    parser.add_argument("--phase2", metavar="HYPOTHESIS", default=None,
                        help="run Phase 2 novelty-check and test on the given hypothesis")
    parser.add_argument("--deep", action="store_true",
                        help="deep open-ended research over the variation queue; novelty is the success condition")
    parser.add_argument("--frontier", action="store_true",
                        help="frontier novelty hunt: collide two fields per round, score candidates "
                        "on 5 axes, log every death; 40-round safety stop")
    parser.add_argument("--deep-innovation", action="store_true",
                        help="assumption-breaking mode: challenge the foundations (critical dimension, "
                        "compactification, fundamental dimensionality) with falsifiable computations")
    parser.add_argument("--max-rounds", type=int, default=None,
                        help="debate round cap (default: 5; deep modes: 40 hard safety stop)")
    args = parser.parse_args()

    MAX_ROUNDS = args.max_rounds or (40 if (args.deep or args.deep_innovation or args.frontier) else 5)
    mode = "MOCK" if os.environ.get("MOCK_LLM") == "1" else "LIVE"
    print(f"[mode: {mode}]")

    if args.frontier:
        return run_frontier(MAX_ROUNDS)
    if args.deep_innovation:
        return run_deep(INNOVATION_CHALLENGES, "innovation-research-summary",
                        "Deep innovation (assumption-breaking) research")
    if args.deep:
        return run_deep()

    preset = PROBLEMS[args.task]
    problem = args.problem or preset["text"]
    slug = re.sub(r"[^a-z0-9-]", "-", (args.slug or preset["slug"]).lower())

    if args.phase2:
        run_phase2(args.phase2, slug)
        return 0

    final = run_debate(problem, slug)
    return 0 if final["resolution"]["decision"] == "accept" else 1


if __name__ == "__main__":
    sys.exit(main())
