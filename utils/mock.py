"""Canned agent responses for MOCK_LLM=1 — verifies the full loop offline.

The engineer's canned code is a real RK4 two-body simulation checked against
the analytic Kepler period, so the mock run exercises the sandbox runner,
metric parsing, plotting, and memo writing exactly like a live run.
"""

_TWO_BODY_CODE = '''\
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Two-body gravity, reduced to a one-body problem about the barycenter.
G, M, m = 1.0, 1.0, 1e-3
mu = G * (M + m)
a_sma = 1.0                     # semi-major axis
e = 0.3                         # eccentricity
T_analytic = 2 * np.pi * np.sqrt(a_sma**3 / mu)

# start at perihelion
r0 = a_sma * (1 - e)
v0 = np.sqrt(mu * (2 / r0 - 1 / a_sma))
state = np.array([r0, 0.0, 0.0, v0])

def deriv(s):
    x, y, vx, vy = s
    r3 = (x * x + y * y) ** 1.5
    return np.array([vx, vy, -mu * x / r3, -mu * y / r3])

def energy(s):
    x, y, vx, vy = s
    return 0.5 * (vx * vx + vy * vy) - mu / np.hypot(x, y)

dt = T_analytic / 20000
n_steps = int(2.5 * T_analytic / dt)
traj = np.empty((n_steps, 4))
E0 = energy(state)
crossings = []
prev_y = state[1]

for i in range(n_steps):
    k1 = deriv(state)
    k2 = deriv(state + 0.5 * dt * k1)
    k3 = deriv(state + 0.5 * dt * k2)
    k4 = deriv(state + dt * k3)
    state = state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    traj[i] = state
    if prev_y < 0 <= state[1] and state[0] > 0:   # upward x-axis crossing
        crossings.append(i * dt)
    prev_y = state[1]

T_measured = crossings[0] if crossings else float("nan")
energy_drift = abs((energy(state) - E0) / E0)
period_error = abs(T_measured - T_analytic) / T_analytic

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
ax1.plot(traj[:, 0], traj[:, 1], lw=0.8)
ax1.plot(0, 0, "k*", ms=12)
ax1.set_aspect("equal")
ax1.set_title(f"Two-body orbit (e={e})")
t = np.arange(n_steps) * dt
E = 0.5 * (traj[:, 2] ** 2 + traj[:, 3] ** 2) - mu / np.hypot(traj[:, 0], traj[:, 1])
ax2.plot(t / T_analytic, (E - E0) / abs(E0))
ax2.set_xlabel("t / T")
ax2.set_title("Relative energy error")
fig.tight_layout()
fig.savefig("outputs/round_1.png", dpi=120)

print("RESULT_JSON: " + json.dumps({
    "period_analytic": T_analytic,
    "period_measured": T_measured,
    "period_error": period_error,
    "energy_drift": energy_drift,
}))
'''

_PROPOSAL = {
    "model_name": "Newtonian two-body problem (barycentric reduction)",
    "equations": [
        "r'' = -G(M+m) r / |r|^3",
        "T = 2*pi*sqrt(a^3 / (G(M+m)))  (Kepler III)",
        "E = v^2/2 - mu/|r| = -mu/(2a)  (conserved)",
    ],
    "assumptions": [
        "Point masses, no radiation or drag",
        "Non-relativistic regime (v << c)",
        "Reduced one-body form about the barycenter is exact for two bodies",
    ],
    "predicted_behavior": [
        "Closed elliptical orbit with eccentricity e = 0.3",
        "Measured period matches Kepler III within 1e-4 relative error",
        "Relative energy drift below 1e-6 over 2.5 periods with RK4",
    ],
    "rationale": "Two-body gravity has an exact analytic solution, giving hard "
    "ground truth to validate the simulation pipeline before scaling to systems "
    "without closed-form answers.",
}


def respond(role: str, phase: str, payload: dict) -> dict:
    if phase == "propose":
        return _PROPOSAL
    if phase == "build":
        return {
            "code": _TWO_BODY_CODE,
            "how_it_maps_to_theory": "RK4 integration of the reduced one-body "
            "ODE; period measured via upward x-axis crossings at perihelion side; "
            "energy drift computed against the initial Hamiltonian.",
            "expected_metrics": ["period_analytic", "period_measured", "period_error", "energy_drift"],
        }
    if phase == "attack_validator":
        metrics = (payload.get("run_result") or {}).get("metrics") or {}
        pe, ed = metrics.get("period_error", 1), metrics.get("energy_drift", 1)
        ok = pe < 1e-4 and ed < 1e-6
        return {
            "verdict": "pass" if ok else "fail",
            "issues": []
            if ok
            else [
                {
                    "claim": "Simulation matches analytic predictions",
                    "reason": f"period_error={pe:.2e}, energy_drift={ed:.2e} exceed stated bounds",
                    "severity": "blocking",
                }
            ],
            "summary": "Measured period and energy conservation checked against Kepler III bounds.",
        }
    if phase == "attack_analyst":
        return {
            "verdict": "pass",
            "issues": [
                {
                    "claim": "RK4 with fixed dt is sufficient for all regimes",
                    "reason": "High-eccentricity orbits will need adaptive stepping or a symplectic integrator",
                    "severity": "minor",
                }
            ],
            "summary": "No blocking issues; flagged integrator choice as a future limitation.",
        }
    if phase == "rebut":
        return {
            "responses": [
                {
                    "issue": "RK4 with fixed dt is sufficient for all regimes",
                    "stance": "accept",
                    "reason": "Valid for e=0.3 here; noted as constraint before scaling to e>0.9.",
                }
            ],
            "revised": False,
            "revision": None,
        }
    if phase == "resolve":
        verdicts = [a.get("verdict") for a in payload.get("attacks", [])]
        accept = all(v == "pass" for v in verdicts) and verdicts
        return {
            "decision": "accept" if accept else "continue",
            "applied_rule": "evidence > derivation > heuristic",
            "reasoning": "Simulation evidence matches analytic derivation; no blocking issues remain."
            if accept
            else "Blocking issues unresolved; another round required.",
            "memo_markdown": None,
        }
    if phase == "analyze":
        metrics = (payload.get("run_result") or {}).get("metrics") or {}
        return {
            "title": "Two-body gravity: pipeline validation",
            "patterns": [
                f"Period error {metrics.get('period_error', float('nan')):.2e} vs Kepler III",
                f"Energy drift {metrics.get('energy_drift', float('nan')):.2e} over 2.5 periods",
            ],
            "next_directions": [
                "Harmonic oscillator (analytic ground truth, different force law)",
                "Symplectic integrator comparison at high eccentricity",
                "Then: compactified extra-dimension toy models (Kaluza-Klein spectra)",
            ],
            "memo_markdown": (
                "# Two-body gravity: pipeline validation\n\n"
                "## Accepted model\n"
                "Newtonian two-body problem in barycentric reduction, RK4 integrated.\n\n"
                "## Evidence\n"
                f"- period_error: {metrics.get('period_error', 'n/a')}\n"
                f"- energy_drift: {metrics.get('energy_drift', 'n/a')}\n\n"
                "## Debate outcome\n"
                "Validator passed both quantitative predictions. Analyst flagged fixed-step "
                "RK4 as a limitation for high-eccentricity work; physicist accepted the "
                "constraint. Orchestrator resolved on evidence.\n\n"
                "## Next\n"
                "Harmonic oscillator, then integrator study, then higher-dimensional toys.\n"
            ),
        }
    raise ValueError(f"no mock for phase {phase!r}")
