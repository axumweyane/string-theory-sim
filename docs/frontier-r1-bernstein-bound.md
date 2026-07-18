# Frontier round 1 — NEAR-MISS: a Bernstein bound on dimension flow

## Collision
Spectral dimension flow (quantum-gravity diffusion) x complete monotonicity /
non-equilibrium thermodynamics. Motivated by our own death log: the innovation session
measured a d_s overshoot with no governing principle.

## Imported structure (Cross-Specialist)
Bernstein-Widder: P(sigma) with positive spectral measure is completely monotone —
the return probability is a Laplace transform, not just data.

## Claim (Physicist, derivation-backed)
With <.>_s the e^{-s l} spectral average: d_s = 2 s <l>_s, and
  **d(d_s)/dln(s) = d_s - 2 s^2 Var_s(l)  <=  d_s.**
Dimension can FALL arbitrarily fast but can RISE at most one e-fold per e-fold
(d_s(s2) <= d_s(s1) * s2/s1). LOAD-BEARING: positivity of the MEASURE — positivity of
P(sigma) alone is insufficient.

## Evidence (simulations/round_frontier-live-r1.py)
- Identity residual: 1.1e-7 (finite-difference limited), across a 4D torus, the
  overshoot hierarchy geometry, and a random 200-atom positive measure
- Bound margin >= +8e-4 everywhere on all positive-measure cases (incl. the overshoot)
- Adversarial SIGNED measure with P > 0 everywhere: violates the bound by 0.80 —
  the positivity dependency is sharp
- Plot: simulations/outputs/frontier_r1_bernstein_bound.png

## Falsifiable prediction
Any diffusion-based dimension-flow curve (CDT, asymptotic safety, causal sets) must obey
slope <= d_s in log diffusion time; an observed super-linear rise is a smoking gun for a
non-positive (interference-type / Lorentzian) diffusion kernel. Checkable against
published d_s(sigma) curves today.

## Scorecard
closure 9 | artifact-resistance 9 | prediction-novelty 6 | **literature-gap 5** | genuineness 7
-> NEAR-MISS (killed conservatively on literature gap: two searches in both fields'
vocabularies found no explicit statement, but the derivation is elementary — variance
positivity — so folklore status in heat-kernel analysis is plausible).

## For a domain expert (one afternoon)
Is "the log-derivative of sigma <lambda>_sigma is bounded by itself, giving a universal
rise-limit and rise/fall asymmetry for spectral dimension, violated exactly by signed
spectral measures" stated anywhere in the heat-kernel / subordination / QG-dimension
literature? If not, it is a small clean publishable remark.

Math is not physics: expert review required; no claim about reality is made.
