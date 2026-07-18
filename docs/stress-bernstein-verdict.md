# Bernstein bound — stress-test verdict: DEAD (scooped at the level of mathematics)

One claim, four attacks, run live 2026-07-18. Code: simulations/round_stress-bernstein.py;
plot: simulations/outputs/stress_bernstein.png.

## The one-paragraph verdict (the deliverable)
The bound d(d_s)/dln(sigma) <= d_s is exactly the statement that ln P(sigma) is CONVEX in
sigma — and log-convexity of the Laplace transform of a positive measure is classical
analysis with a two-line Cauchy-Schwarz proof: P((s+t)/2) = int e^{-s l/2} e^{-t l/2} dmu
<= sqrt(P(s) P(t)). It is a textbook property of completely monotone functions (Widder 1941;
the Bernstein-functions literature — see the CM digest, arXiv:1211.0900; log-convex-function
references list Laplace transforms as the canonical example). On the physics side, the
conceptual arena — positivity of quantum-corrected diffusion kernels in spectral-dimension
studies — is also already charted: Calcagni et al. explicitly discuss negative-probability
kernels and engineer positive-semidefinite diffusion equations for asymptotic safety,
Horava-Lifshitz and LQG (arXiv:1408.0199, arXiv:1909.12207). Our inequality is therefore a
corollary of known mathematics inside a known discussion, not a new result. SCOOPED.

## What the four attacks established before the death
1. **Unbreakable in the positive class** (as a theorem must be): min margin >= 0 on gapped,
   continuum+atoms, heavy-tail, exact level-6 Sierpinski gasket, and Horava z=3 kernels;
   2000-sample adversarial search inside the positive class: max violation 9e-9 (numerical
   zero). Signedness is exactly the only way to break it.
2. **Not vacuous**: saturation (slope/d_s -> 1) is physical — any gapped kernel saturates in
   its exponential IR regime (measured 0.9994; Sierpinski exactly 1.0); a single mode
   saturates identically.
3. **Genuinely tested by real data**: the published CDT fit d_s = 4.02 - 119/(54+sigma)
   RISES, so the rise bound is exercised: max sigma d_s'/d_s = 0.196 — passes with 5x slack.
   Precise test statement: for any d_s from a genuine positive-kernel return probability,
   sigma d_s'/d_s <= 1 at every sigma; violation certifies negative spectral weight.
4. **Literature (the decisive axis)**: searched in the correct vocabulary this time
   (log-convexity, CM functions, heat trace) — the math is standard; the physics arena is
   active. Last run's literature-gap score of 5 was still too generous; true value ~2.

## Final scorecard
closure 10 (now carries a 2-line proof) | artifact-resistance 9 | non-vacuousness 7 |
prediction sharpness 8 | **literature gap 2 -> DEAD**

## Lesson for the failure map
The conservative instinct was right and still not conservative enough: an elementary
derivation (variance positivity = Cauchy-Schwarz) is almost always a known theorem wearing
new clothes. The stress protocol's requirement to search the OTHER field's vocabulary
(log-convexity, not "spectral dimension monotonicity") is what found the scoop in one
query. Residual value: a pedagogical remark connecting log-convexity to the d_s rise rate
might merit one sentence in a review — comment-level, not result-level.

Math is not physics; and in this case the math wasn't new either. Case closed.
