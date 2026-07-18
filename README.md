# string-theory-sim

Adversarial multi-agent physics simulation framework. Five AI agents — Physicist, Engineer, Validator, Analyst, Orchestrator — argue like a research panel: theory is proposed, implemented as a real simulation, attacked, defended, and only accepted when the evidence survives. Starts with 2-body gravity (analytic ground truth), designed to scale toward harmonic oscillators and higher-dimensional (string-theory) mathematics.

**Honest scope:** this explores/validates mathematics and generates hypotheses. It does not prove string theory.

## Architecture

```
propose (Physicist, Opus) ──▶ build+run (Engineer, Sonnet) ──▶ attack (Validator+Analyst)
       ▲                                                              │
       └── revision ◀── rebut (Physicist) ◀───────────────────────────┘
                              │
                        resolve (Orchestrator, Opus)
                    accept ─▶ research memo (docs/)
                    continue ─▶ next round (max 5)
                    escalate ─▶ memo for human decision (docs/)
```

- **LangGraph** state machine (`main.py`), Anthropic SDK for all model calls (`utils/llm.py`).
- Agents exchange **structured JSON** only (schemas in `utils/schema.py`, enforced server-side via `output_config.format`).
- System prompts (`prompts/*.md`) sent once per call with a cache breakpoint.
- Engineer's code is executed in a subprocess (`utils/runner.py`); it must emit `RESULT_JSON: {...}` metrics and save plots to `simulations/outputs/`.
- Every event is persisted to `debates/<timestamp>_<slug>.json` (`utils/transcript.py`) — shared memory + reproducibility.
- Models: `claude-opus-4-8` for Physicist/Validator/Orchestrator, `claude-sonnet-5` for Engineer/Analyst.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add ANTHROPIC_API_KEY (or `ant auth login`)
```

## Run — Phase 1 (explore & propose)

```bash
# string-theory vibration modes (default task): closed string on S^1, KK + winding
# spectrum, T-duality checks, 3D projection plot, candidate hypotheses flagged
python main.py

# pipeline-validation task (2-body gravity, analytic ground truth)
python main.py --task two-body

# 3D visualization task: PNG stills from several camera angles + an MP4 (GIF
# fallback) of the string oscillating with a rotating camera; colour encodes the
# compressed compact dimension; projection invariants (energy, closure, node
# count) are verified per frame by the Validator
python main.py --task string-viz

# free-form problem
python main.py --slug harmonic-oscillator --problem "Model the 1D simple harmonic oscillator..."

# offline smoke test — canned agents, real simulations + plots + memos, no API key
MOCK_LLM=1 python main.py
```

Outputs: 3D projection plot(s) in `simulations/outputs/`, research memo (with any candidate hypotheses) in `docs/`, full debate transcript in `debates/`. Exit code 0 = accepted, 1 = escalated to you.

## Run — Phase 2 (novelty check & test)

When a Phase-1 memo flags a candidate hypothesis, the run prints the exact Phase-2 command:

```bash
python main.py --phase2 "the hypothesis statement"
```

Pipeline: literature search via the Anthropic `web_search` server tool → Analyst novelty verdict (`known` requires citations) → if **known**: logged to `docs/*-phase2-known.md` with sources → if **novel/uncertain**: Physicist designs a falsifiable test, Engineer implements and runs it, Validator judges, Analyst writes `docs/*-phase2.md` with the outcome and an **honest confidence level**.

**The one rule:** a correct equation or clean plot is *not* a discovery about the universe. Every Phase-2 memo states explicitly that experimental validation is still required — trust the confidence line, not the excitement of a result. Likewise every visualization memo states that a 3D projection is a compression of the mathematics — a shadow of the higher-dimensional object, not the object, and not evidence the dimensions physically exist.

## Run — Deep open-ended research mode

```bash
python main.py --deep              # this one takes real time and real tokens
python main.py --deep --max-rounds 60   # override the hard safety stop (default 40)
```

No 5-round cap — each debate runs until genuine consensus (Validator-confirmed with a derivation), a true deadlock (memo + move on), or the safety stop. Every proposal is simulated immediately in the sandbox; nothing is argued in the abstract. The driver walks a target space of **beyond-textbook variations** (`utils/problems.py: DEEP_VARIATIONS` — T² with complex/Kähler moduli, Wilson-line deformations, asymmetric shift orbifolds) and feeds every candidate hypothesis into the Phase-2 pipeline. **Novelty is the only success condition**: known results are logged with citations and the panel moves on; the run ends when a novel candidate survives its falsifiable test or the target space is exhausted. An end-of-run summary (also written to `docs/deep-research-summary.md`) reports variations explored, known vs tested counts, and whether anything survived.

Honest expectation: most of what the panel surfaces will already exist — that is the normal outcome of real research, and the summary says so.

## Run — Deep innovation mode (assumption-breaking)

```bash
python main.py --deep-innovation
```

Instead of building on the standard assumptions, the panel attacks them (`utils/problems.py: INNOVATION_CHALLENGES`): **is D=26 actually forced** (light-cone anomaly computed at D∈{4,10,26}, zeta vs cutoff regularization, Liouville steelman); **is dimension emergent** (running spectral dimension from real random-walk ensembles vs a fixed-D control); **what if an extra dimension is timelike** (tachyon tower, growth rates, ghost norms — computed, not recited); **do we need compactification at all** (warped infinite dimension: numerical graviton zero mode + KK continuum). Rules of engagement: heresies get steelmanned, not strawmanned; a computation contradicting a textbook triggers an independent re-derivation of the textbook claim rather than auto-rejection; and every memo must state *why* the alternative failed or survived, *which* assumption rescues the orthodox picture, and *where* the nearest genuinely unsettled question is. Realistic expectation: most alternatives collapse under scrutiny — the dependency map of what saves string theory is the deliverable.

```bash
pytest   # unit tests for schemas, mocks, runner, transcript
```

## Scaling to harder physics

1. Verify the loop on 2-body gravity (`--task two-body`), then the S^1 string spectrum (default).
2. Cutoff-independence checks on any spectrum-counting result.
3. T^2 compactification with complex/Kähler moduli, then orbifolds — the first step toward genuinely curved Calabi-Yau spectra and exotic topologies.
4. New targets go in `utils/problems.py`; the panel machinery is unchanged.

## Push to GitHub

```bash
gh repo create axumweyane/string-theory-sim --private --source . --push
# or manually:
git remote add origin git@github.com:axumweyane/string-theory-sim.git
git push -u origin main
```
