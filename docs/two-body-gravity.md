# Two-body gravity: pipeline validation

## Accepted model
Newtonian two-body problem in barycentric reduction, RK4 integrated.

## Evidence
- period_error: 0.0
- energy_drift: 2.66187338571466e-15

## Debate outcome
Validator passed both quantitative predictions. Analyst flagged fixed-step RK4 as a limitation for high-eccentricity work; physicist accepted the constraint. Orchestrator resolved on evidence.

## Next
Harmonic oscillator, then integrator study, then higher-dimensional toys.
