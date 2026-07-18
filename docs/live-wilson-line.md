# Live debate 3 — Wilson-line deformation of the S^1 spectrum

## Model (Physicist)
Wilson line of the circle-2 graviphoton along circle 1, as the off-diagonal torus modulus:
vielbein e = [[R1, a],[0, R2]], G = e^T e, B = 0, with R1 = 1 (self-dual), R2 = 1.55 (generic).
Narain spectrum as in debate 2 (formulas already validated there).

## Evidence (Engineer — simulations/round_live-wilson.py)
- Level-matching identity across a in {0, .23, .5, .81, 1}: max dev **2.1e-14**
- Massless counts: a=0 -> **9**; a=0.05 -> **3**; a=0.5 -> **5**; a=1 -> **9**
- Exact periodicity a -> a+1 (integer basis change e2 -> e2+e1): 60-level dev **8.9e-16**
- Restoration on the scan grid only at integer a
- Plot: simulations/outputs/live_wilson_line.png (count vs a; level flow with crossings)

## The debate (two predictions corrected by evidence)
1. Physicist predicted count 1 at small a. Measured 3. State identification: the survivors are
   (0,0,±2,0) — circle-1 winding-2 scalars with zero graviphoton charge (n2=w2=0). A Wilson line
   lifts only charged states (adjoint-Higgs pattern), and M^2 = 4 G11 - 4 = 4 R1^2 - 4 is
   a-independent. Correct generic count: 3.
2. The unpredicted count-5 point at a = 1/2: states (±2,±1,0,0) with
   n^T G^{-1} n = ((2a-1)^2 + 4 R2^2)/R2^2 = 4 exactly at a = 1/2 -> two extra massless
   **scalars** (S=0), not gauge bosons; no chiral (2,0) solution exists at generic R2, so no
   vector enhancement away from integer a. Both revisions derivation-backed; accepted under
   evidence > heuristic.

## Novelty check (Analyst — live web search)
**KNOWN.** Wilson-line "enhancement-breaking", survival of holonomy-neutral states, and extra
massless states at special (R, Wilson line) values are standard:
- [A new twist on heterotic string compactifications, arXiv:1805.11128](https://arxiv.org/pdf/1805.11128)
- [Wilson lines corrections to gauge couplings, arXiv:hep-th/0305085](https://arxiv.org/pdf/hep-th/0305085)
- [nLab: enhanced gauge symmetry](https://ncatlab.org/nlab/show/enhanced+gauge+symmetry)

## Honest scope
Mathematical result about the deformed free spectrum. Not a claim about physical reality;
experimental validation would be required for any such claim.
