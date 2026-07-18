# Innovation debate 1 — is D=26 actually forced?

## Heresy
The bosonic string's critical dimension is a convention, not a necessity.

## Evidence (simulations/round_innov-critdim.py)
- Regulator independence: zeta(-1) vs smooth-cutoff extrapolation of "sum n" agree to **5.8e-12** — the -1/12 is not a scheme artifact
- Lorentz anomaly Delta_m = m(26-D)/12 + (1/m)[(D-26)/12 + 2(1-a)] with a=(D-2)/24:
  **exactly 0 for all m at D=26**; at D=4, Delta_1 = 1.83 and level-1 vector has
  alpha'M^2 = 0.917 with 2 polarizations where a massive vector needs 3
- Two independent conditions (a=1 and the m-coefficient) both solve to D=26
- Steelman table: Liouville background charge Q^2 = (26-D)/6 rebalances the anomaly at any D
- Plot: simulations/outputs/innov_critical_dimension.png

## Frontier map
1. **Why the heresy died:** quantified Lorentz anomaly at D != 26; regulator-independent.
2. **What saves the orthodoxy:** nothing sacred about 26 — the real requirement is total
   conformal anomaly cancellation; D=26 is its flat-background/constant-dilaton case.
   Relax that and non-critical (linear-dilaton/Liouville) strings exist at any D. (KNOWN:
   [Non-critical string theory](https://en.wikipedia.org/wiki/Non-critical_string_theory),
   [arXiv:hep-th/0006043](https://arxiv.org/pdf/hep-th/0006043))
3. **Frontier:** controlled supercritical / time-dependent non-critical backgrounds above D=2.

Mathematical result only; experimental validation required for any claim about reality.
