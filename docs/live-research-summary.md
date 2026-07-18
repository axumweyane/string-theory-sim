# Live open-ended research session — summary (2026-07-18)

All five roles were run live in-session (no SDK agents): real computation through
utils/runner.py, real literature searches, one memo per target. Debates ran with no round
cap; each closed on a derivation-backed conclusion.

## Scorecard

| # | Target | Result | Novelty verdict | Confidence in the math |
|---|--------|--------|-----------------|------------------------|
| 1 | S^1 spectrum + self-dual point | 9 massless at R=1 (SU(2)xSU(2) pattern), T-duality exact, cutoff-stable | **KNOWN** — arXiv:1510.07644, hep-th/9509171 | high |
| 2 | T^2 moduli (tau, rho) | Dualities exact; enhancement ladder 3 / 25 / 49 on tau=rho locus; one prediction corrected mid-debate (single chiral SU(2) on generic locus) | **KNOWN** — arXiv:2010.14450, hep-th/9509171, 1704.04427 | high |
| 3 | Wilson-line deformation | Charged states lifted, neutral winding scalars survive (count 3); extra massless scalars at half-holonomy via (2a-1)^2 arithmetic; exact a -> a+1 periodicity | **KNOWN** — arXiv:1805.11128, hep-th/0305085 | high |
| 4 | Asymmetric shift orbifold | Consistent iff R^2 integer (vs symmetric shift: all R); frac class = delta.delta/2; 9/9 massless survive at R=1 | **KNOWN** — NSV (CERN CDS 211766), arXiv:2502.18453, 2604.19634 | high |

## Bottom line
- Targets explored: **4/4** (list exhausted)
- Already known: **4** (all with citations)
- Genuinely novel candidates surviving a literature check: **0** — nothing reached the
  falsifiable-test stage, because every surfaced pattern was located in the literature first
- The debates produced three real mid-round corrections (T2 locus counting, Wilson-line
  neutral-state survival, Wilson-line half-holonomy scalars), each resolved by
  evidence > derivation > heuristic

"High confidence" above refers to the **mathematics of the free-string models** — the
computations reproduce known structures at machine precision. None of this is evidence about
physical reality: these are properties of a mathematical model, and experimental validation
would be required for any claim about the universe. Finding only known physics across four
textbook-adjacent targets is the expected, honest outcome; genuinely new results live further
from charted territory than a four-stop tour can reach.

## Artifacts
- Memos: docs/live-{s1-spectrum, t2-moduli, wilson-line, asym-orbifold}.md
- Plots: simulations/outputs/live_{s1_spectrum, t2_moduli, wilson_line, asym_orbifold}.png
- Run code: simulations/round_live-{s1, t2, wilson, orbifold}.py
- Transcript: debates/live-session-20260718.json
