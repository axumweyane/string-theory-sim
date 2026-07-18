# Deep innovation (assumption-breaking) research — live session summary (2026-07-18)

All five roles run live in-session: real computation via utils/runner.py, real literature
searches, no round cap. Novelty was the success condition; the dependency map is the yield.

## Scorecard

| # | Heresy | Fate of the heresy | Novelty | Confidence in the math |
|---|--------|--------------------|---------|------------------------|
| 1 | D=26 is a convention | **Refuted by computation** — regulator-independent -1/12; Lorentz anomaly vanishes only at D=26 (two independent conditions) | Escape route (Liouville) KNOWN | high |
| 2 | Dimension is emergent | **Survives as a concept** — d_s runs 2.29 -> 4.02 in a real diffusion computation; but our toy smuggles in the "4" | KNOWN (CDT, AJL 2005) | high |
| 3 | Extra time dimension | **Refuted (naive form)** — divergent tachyon tower (2N), unbounded growth rates, derived ghost sign | Escape route (2T-physics) KNOWN | high |
| 4 | No compactification needed | **SURVIVED its falsifiable test** — localized graviton, gapless continuum, r^-2 corrections, all confirmed numerically | KNOWN (RS2, 1999) | high |

## Bottom line
- Heresies explored: **4/4**. Refuted by computation: 2. Survived as concept/mechanism: 2.
- Genuinely novel: **0** — even the surviving alternative (gravity without compactification)
  was published in 1999 under the literal title "An Alternative to Compactification."
- The real deliverable is the dependency map: **D=26 hangs on flat background + constant
  dilaton** (relax -> non-critical strings); **one time hangs on unitarity + bounded
  Hamiltonian** (gauge it away -> 2T-physics, which returns effectively one time);
  **compactification hangs on wanting unwarped bulk geometry** (warp it -> RS2);
  and **fixed dimensionality is a choice of observable** (diffusion sees a running one).
- Debates included two real validator catches (a finite-size artifact that would have faked
  an emergent-dimension signal, and an honest overshoot report) — the adversarial loop did
  its job on our own code, which is the point.

None of this is evidence about physical reality. These are properties of mathematical
models; experimental validation would be required for any claim about the universe.

## Artifacts
- Memos: docs/innov-{critical-dimension, emergent-dimension, timelike-dimension, no-compactification}.md
- Plots: simulations/outputs/innov_*.png
- Run code: simulations/round_innov-*.py
- Transcript: debates/live-innovation-20260718.json
