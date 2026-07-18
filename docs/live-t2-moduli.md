# Live debate 2 — T^2 with complex/Kahler moduli: dualities and enhancement loci

## Model (Physicist)
Narain form of the closed bosonic string on T^2 (alpha'=1): G = (rho2/tau2)[[1,tau1],[tau1,|tau|^2]],
B12 = rho1; v_pm = n + (B pm G) w; p_{L,R}^2 = (1/2) v^T G^{-1} v; M^2 = pL^2 + pR^2 + 2(N+Nt-2),
level matching N - Nt = n.w. Charge box |q| <= 4; oscillator levels enumerated exactly (no cutoff).

## Evidence (Engineer — simulations/round_live-t2.py)
- Level-matching identity (pL^2 - pR^2)/2 = n.w at 5 random moduli: max dev **2.1e-14**
- 60 lowest levels invariant under tau->tau+1, tau->-1/tau, rho->rho+1, rho->-1/rho, tau<->rho: **2.2e-15**
- Massless counts: generic (tau,rho) **1**; tau=rho generic **3**; tau=rho=i **25**; tau=rho=e^{i pi/3} **49**
- Heatmap over tau=rho=x+iy peaks exactly at (0,1); SU(3) points are measure-zero (need exact evaluation)
- Plot: simulations/outputs/live_t2_moduli.png

## The debate (one real correction)
Physicist predicted 9 on the generic tau=rho locus from a symmetric (1+r)^2 root-count heuristic.
Measured: 3. Validator demanded the chirality structure; direct enumeration showed the extra states
are ±(1,0,-1,0) with (pL^2,pR^2) = (0,2) — a **single chiral SU(2)** (2 roots, one chirality).
Physicist's revision (accepted): count = (1+r_L)(1+r_R); v_+ = 0 for that charge holds identically
on tau=rho since rho2/tau2 = 1 and tau1 rho2/tau2 - rho1 = 0. Then 25 = (1+4)^2 and 49 = (1+6)^2
follow for the symmetric points. Resolution rule applied: evidence > heuristic.

## Novelty check (Analyst — live web search)
**KNOWN.** The T=U -> SU(2); T=U=i -> SU(2)xSU(2); T=U=e^{i pi/3} -> SU(3) ladder is standard:
- [Torus Bundles, Automorphisms and T-Duality, arXiv:2010.14450](https://arxiv.org/abs/2010.14450)
- [Symmetry breaking at enhanced symmetry points, arXiv:hep-th/9509171](https://arxiv.org/pdf/hep-th/9509171)
- [Gauge symmetry enhancing-breaking from a Double Field Theory perspective, arXiv:1704.04427](https://arxiv.org/pdf/1704.04427)

## Honest scope
Mathematical result about the free spectrum on T^2. Not a claim about physical reality;
experimental validation would be required for any such claim.
