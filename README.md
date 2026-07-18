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

## Run

```bash
# offline smoke test — canned agents, real simulation + plot + memo, no API key needed
MOCK_LLM=1 python main.py

# the real thing
python main.py

# a different problem
python main.py --slug harmonic-oscillator \
  --problem "Model the 1D simple harmonic oscillator; analytic ground truth is x(t)=A cos(wt+phi) and energy conservation; give quantitative predictions a simulation must reproduce."
```

Outputs: plot(s) in `simulations/outputs/`, research memo in `docs/`, full debate transcript in `debates/`. Exit code 0 = accepted, 1 = escalated to you.

```bash
pytest   # unit tests for schemas, runner, transcript
```

## Scaling to harder physics

1. Verify 2-body gravity end-to-end (`python main.py`).
2. Harmonic oscillator (`--slug harmonic-oscillator`, prompt above).
3. Coupled oscillators / wave equation — first problems without trivial closed forms.
4. Kaluza-Klein toy models: compactified extra dimension, KK mode spectra — the on-ramp to string-theory mathematics. Give the Physicist the target in `--problem`; the panel machinery is unchanged.

## Push to GitHub

```bash
gh repo create axumweyane/string-theory-sim --private --source . --push
# or manually:
git remote add origin git@github.com:axumweyane/string-theory-sim.git
git push -u origin main
```
