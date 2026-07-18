# Live debate 4 — asymmetric shift orbifold of S^1

## Model (Physicist)
Orbifold by the pure left-mover half-shift g: X_L -> X_L + pi R (alpha'=1). g acts on |n,w>
with phase exp(2 pi i (n/2 + w R^2/2)); twisted charges (n + R^2/2, w + 1/2). Shift orbifolds
do not twist oscillators, so consistency is pure lattice arithmetic.

## Evidence (Engineer — simulations/round_live-orbifold.py)
- Level-matchability metric (frac((n+b)(w+a)) spread within (n,w)-parity classes — a
  necessary condition, since an order-2 projection acts only through charge parities):
  **exactly 0 at integer R^2**, >= 0.36 at every off-integer point (max 0.5)
- Symmetric geometric shift control (b=0): metric 0 at **all** R — the asymmetry is what
  imposes the special radii
- Surviving twisted frac class contains delta.delta/2 = R^2/4: {1/4,3/4} at R^2=1,
  {0,1/2} at R^2=2 — the modular bookkeeping comes out right
- At R=1: untwisted projection (-1)^(n+w) keeps **9/9** massless states (all have n+w even)
  while halving the massive charged tower; twisted sector min |M^2| = **0.5** (no new massless)
- Plot: simulations/outputs/live_asym_orbifold.png

## Attack & resolution (Validator, Orchestrator)
Metric legitimacy established (necessary condition, exact rational arithmetic, box-independent);
symmetric control rules out a trivially-zero metric. All physicist predictions confirmed.
**Accepted** on evidence + derivation.

## Novelty check (Analyst — live web search)
**KNOWN.** This is the Narain–Sarmadi–Vafa consistency story for asymmetric (shift) orbifolds —
Z_2 shifts delta = (p_L,p_R)/2, vacuum-energy p^2/8 bookkeeping, special-lattice requirements:
- [Narain, Sarmadi, Vafa — Asymmetric orbifolds (CERN CDS)](https://cds.cern.ch/record/211766)
- [Shift orbifolds, decompactification limits, and lattices, arXiv:2502.18453](https://arxiv.org/pdf/2502.18453)
- [Dai-Freed anomalies and level matching in heterotic asymmetric orbifolds, arXiv:2604.19634](https://arxiv.org/pdf/2604.19634)

"Consistent iff R^2 integer" for the pure-left half-shift is a special case of the standard
shift condition. Logged as known.

## Honest scope
Mathematical consistency analysis of a free-string orbifold. Not a claim about physical
reality; experimental validation would be required for any such claim.
