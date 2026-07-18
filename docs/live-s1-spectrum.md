# Live debate 1 — closed string on S^1: spectrum and the self-dual point

**Panel:** all five roles run live (in-session), real computation + real literature search.

## Model (Physicist)
Closed bosonic string, one dimension on S^1, alpha'=1: M^2 = (n/R)^2 + (wR)^2 + 2(N+Nt-2),
level matching N-Nt = nw. Assumptions: free spectrum, flat background, truncated lattice
(|n|,|w| <= 3, levels <= 3; cross-checked at 5), state counting ignores polarization.

## Evidence (Engineer — simulations/round_live-s1.py)
- T-duality R -> 1/R spectrum deviation: **0.0** across R in {1.3, 1.7, 2.4, 3.1}
- Massless (n,w,N,Nt) combos: **1** at generic R (1.7), **9** at R = 1
- Cutoff independence 3 -> 5: **stable**
- Extra self-dual states: (0,0,1,1); (±1,±1) with one oscillator (level matching nw = ±1);
  (±2,0),(0,±2) with N=Nt=0 (M^2 = 4 - 4 = 0)
- Plot: simulations/outputs/live_s1_spectrum.png (massless count vs R; low-lying level flow)

## Attack & resolution (Validator, Orchestrator)
Dimensional analysis passes; the 9 states decompose exactly as the SU(2)_L x SU(2)_R
current-algebra pattern (p_L^2 = 2, p_R^2 = 0 and mirror, plus charged scalars), so the
enhancement is structural, not numerical. No blocking issues. **Accepted** on
evidence + derivation.

## Novelty check (Analyst — live web search)
**KNOWN.** Enhancement to SU(2) x SU(2) at the self-dual radius, with six gauge fields and
nine scalars in the bi-fundamental, is textbook material:
- [Enhanced gauge symmetry and winding modes in Double Field Theory, arXiv:1510.07644](https://arxiv.org/abs/1510.07644)
- [Symmetry breaking at enhanced symmetry points, arXiv:hep-th/9509171](https://arxiv.org/pdf/hep-th/9509171)

Logged as known; the panel moves on.

## Honest scope
This is a mathematical result about the free-string spectrum. It is not evidence about
physical reality; experimental validation would be required for any such claim.
