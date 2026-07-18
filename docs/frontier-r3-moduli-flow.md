# Frontier round 3 — DEAD (validator/artifact): optimization x moduli landscapes

Claim attempted: enhanced-symmetry points are attractors of gradient flow on a
free-energy-like landscape F = sum exp(-M^2) over Narain T^2 moduli.

Killed by the Validator (simulations/round_frontier-live-r3.py): all 30/30 trajectories
ran to the domain boundary — F rewards light KK towers, so the flow measures
DECOMPACTIFICATION, and F at a generic point (394) exceeds F at tau=rho=i (335): the
symmetry point is not even a local maximum of this functional. The seductive "97% of
endpoints on the tau=rho locus" was a clipping artifact (trajectories pinned to the same
boundary corner). The load-bearing assumption (boundedness of the landscape) was named in
advance and it failed.

Failure-map lesson: the basin-of-attraction question on moduli space is ill-posed until
the functional is a genuine bounded modular-invariant free energy (or carries a volume
constraint). Without that, "optimization on moduli space" rediscovers runaway
decompactification, not symmetry selection.
