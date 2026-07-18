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


# Closed bosonic string on S^1, alpha'=1: real spectrum code so the mock run
# exercises the 3D-projection contract and the self-dual-radius physics.
_STRING_CODE = '''\
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Closed bosonic string, one dimension on S^1 of radius R, alpha' = 1.
# M^2 = (n/R)^2 + (w R)^2 + 2 (N + Nt - 2),  level matching N - Nt = n w.
NMAX, LMAX = 3, 3
EPS = 1e-9

def spectrum(R):
    out = []
    for n in range(-NMAX, NMAX + 1):
        for w in range(-NMAX, NMAX + 1):
            for N in range(LMAX + 1):
                for Nt in range(LMAX + 1):
                    if N - Nt != n * w:
                        continue
                    m2 = (n / R) ** 2 + (w * R) ** 2 + 2 * (N + Nt - 2)
                    out.append((n, w, N, Nt, m2))
    return out

def masses(R):
    return sorted(round(s[-1], 9) for s in spectrum(R))

# T-duality: spectrum at R must equal spectrum at 1/R (n <-> w swap is a relabeling).
R = 1.7
t_dev = max(abs(a - b) for a, b in zip(masses(R), masses(1.0 / R)))

massless_generic = sum(1 for s in spectrum(R) if abs(s[-1]) < EPS)
massless_selfdual = sum(1 for s in spectrum(1.0) if abs(s[-1]) < EPS)

# 3D projection of the higher-dimensional mode lattice: min M^2 over oscillator
# levels, plotted over the (n, w) charge lattice at the self-dual radius.
# Preserved invariants: M^2 values and the n <-> w exchange symmetry at R=1.
fig = plt.figure(figsize=(11, 5))
ax1 = fig.add_subplot(121, projection="3d")
grid = {}
for n, w, N, Nt, m2 in spectrum(1.0):
    key = (n, w)
    grid[key] = min(grid.get(key, np.inf), m2)
ns, ws, m2s = zip(*[(k[0], k[1], v) for k, v in grid.items()])
sc = ax1.scatter(ns, ws, m2s, c=m2s, cmap="viridis", s=45)
ax1.set_xlabel("n (KK momentum)"); ax1.set_ylabel("w (winding)"); ax1.set_zlabel("min $M^2$")
ax1.set_title("Mode lattice at self-dual R=1")
fig.colorbar(sc, ax=ax1, shrink=0.6)

ax2 = fig.add_subplot(122)
Rs = np.linspace(0.5, 2.0, 301)
counts = [sum(1 for s in spectrum(float(r)) if abs(s[-1]) < 1e-6) for r in Rs]
ax2.plot(Rs, counts)
ax2.set_xlabel("R"); ax2.set_ylabel("# massless states")
ax2.set_title("Massless spectrum vs radius")
fig.tight_layout()
fig.savefig("outputs/{outname}.png", dpi=120)

print("RESULT_JSON: " + json.dumps({
    "t_duality_max_dev": t_dev,
    "massless_generic": massless_generic,
    "massless_selfdual": massless_selfdual,
}))
'''

_STRING_TEST_CODE = '''\
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

NMAX, LMAX, EPS = 3, 3, 1e-6

def count0(R):
    c = 0
    for n in range(-NMAX, NMAX + 1):
        for w in range(-NMAX, NMAX + 1):
            for N in range(LMAX + 1):
                for Nt in range(LMAX + 1):
                    if N - Nt != n * w:
                        continue
                    m2 = (n / R) ** 2 + (w * R) ** 2 + 2 * (N + Nt - 2)
                    if abs(m2) < EPS:
                        c += 1
    return c

# grid symmetric under R -> 1/R and containing R=1 exactly
logs = np.linspace(-0.6, 0.6, 241)
Rs = np.exp(logs)
counts = np.array([count0(float(r)) for r in Rs])
peak_R = float(Rs[int(np.argmax(counts))])
t_sym_dev = int(np.max(np.abs(counts - counts[::-1])))
baseline = int(counts[0])

fig = plt.figure(figsize=(6.5, 5))
ax = fig.add_subplot(111, projection="3d")
ax.plot(Rs, np.zeros_like(Rs), counts, lw=1.5)
ax.scatter([peak_R], [0], [counts.max()], color="crimson", s=60)
ax.set_xlabel("R"); ax.set_ylabel(""); ax.set_zlabel("# massless states")
ax.set_title("Massless-count localization at self-dual R")
fig.tight_layout()
fig.savefig("outputs/phase2_test.png", dpi=120)

print("RESULT_JSON: " + json.dumps({
    "peak_R": peak_R,
    "peak_count": int(counts.max()),
    "baseline_count": baseline,
    "t_duality_sym_dev": t_sym_dev,
}))
'''

_STRING_PROPOSAL = {
    "model_name": "Closed bosonic string on R^24,1 x S^1 (flat-torus compactification)",
    "equations": [
        "M^2 = (n/R)^2 + (w R)^2 + 2 (N + Ntilde - 2)   [alpha' = 1]",
        "Level matching: N - Ntilde = n w",
        "T-duality: spectrum(R) = spectrum(1/R) under n <-> w",
    ],
    "assumptions": [
        "Free bosonic string spectrum (26D critical), no interactions",
        "Flat background; single dimension compactified on S^1 of radius R",
        "Oscillator and charge lattice truncated for numerics (|n|,|w| <= 3, N,Ntilde <= 3)",
        "State counts ignore polarization multiplicity",
    ],
    "predicted_behavior": [
        "T-duality: max spectrum deviation between R and 1/R below 1e-9",
        "Exactly one massless (n,w,N,Ntilde) combination at generic R (n=w=0, N=Ntilde=1)",
        "Additional massless states appear at the self-dual radius R=1 (enhanced gauge symmetry)",
    ],
    "rationale": "The S^1 (trivial Calabi-Yau) compactification has an exact spectrum, "
    "giving hard ground truth for the KK/winding machinery before exotic topologies.",
}


_STRING_KEYWORDS = ("string", "compactif", "winding", "duality", "self-dual", "kaluza")


def _is_string_task(payload: dict) -> bool:
    import json as _json

    blob = _json.dumps(payload).lower()
    return any(k in blob for k in _STRING_KEYWORDS)


def respond(role: str, phase: str, payload: dict) -> dict:
    if phase in ("novelty", "design_test", "phase2_memo") or _is_string_task(payload):
        out = _respond_string(role, phase, payload)
        if out is not None:
            return out
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
            "candidate_hypotheses": [],
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


def web_research(query: str) -> dict:
    if "self-dual" in query.lower() or "enhanced" in query.lower():
        return {
            "findings": "Enhanced gauge symmetry at the self-dual radius R = sqrt(alpha') is a "
            "textbook result of bosonic string compactification: extra massless vectors at R=1 "
            "assemble into SU(2) x SU(2). Covered in Polchinski Vol. 1 ch. 8 and reviews of "
            "T-duality (Giveon-Porrati-Rabinovici).",
            "sources": [
                {"title": "Polchinski, String Theory Vol. 1, ch. 8", "url": "https://doi.org/10.1017/CBO9780511816079"},
                {"title": "Giveon, Porrati, Rabinovici — Target space duality in string theory", "url": "https://arxiv.org/abs/hep-th/9401139"},
            ],
        }
    return {
        "findings": "No close match found in the mock literature index for this exact statement.",
        "sources": [],
    }


def _respond_string(role: str, phase: str, payload: dict):
    """String-task canned responses; returns None to fall through to shared phases."""
    metrics = (payload.get("run_result") or {}).get("metrics") or {}
    if phase == "propose":
        return _STRING_PROPOSAL
    if phase == "build":
        if "design_test:" in str(payload.get("proposal", {}).get("rationale", "")):
            return {
                "code": _STRING_TEST_CODE,
                "how_it_maps_to_theory": "Scans count0(R) over a fine grid including R=1 exactly; "
                "peak location tests localization, and count0(R) vs count0(1/R) tests T-duality.",
                "expected_metrics": ["peak_R", "peak_count", "baseline_count", "t_duality_sym_dev"],
            }
        return {
            "code": _STRING_CODE.replace("{outname}", "round_1"),
            "how_it_maps_to_theory": "Direct enumeration of the (n, w, N, Ntilde) lattice under "
            "level matching; T-duality checked as multiset equality of M^2 values; 3D scatter "
            "projects the charge lattice + mass axis, preserving M^2 and the n<->w symmetry.",
            "expected_metrics": ["t_duality_max_dev", "massless_generic", "massless_selfdual"],
        }
    if phase == "attack_validator":
        if "peak_R" in metrics:
            ok = (
                abs(metrics.get("peak_R", 0) - 1.0) < 1e-12
                and metrics.get("baseline_count") == 1
                and metrics.get("t_duality_sym_dev", 1) == 0
                and metrics.get("peak_count", 0) > 1
            )
            return {
                "verdict": "pass" if ok else "fail",
                "issues": []
                if ok
                else [
                    {
                        "claim": "Enhancement is localized at R=1",
                        "reason": f"metrics={metrics}",
                        "severity": "blocking",
                    }
                ],
                "summary": "Checked peak location, baseline count, and R->1/R symmetry of count0.",
            }
        td = metrics.get("t_duality_max_dev", 1)
        mg = metrics.get("massless_generic", 0)
        ms = metrics.get("massless_selfdual", 0)
        ok = td < 1e-9 and mg == 1 and ms > mg
        return {
            "verdict": "pass" if ok else "fail",
            "issues": []
            if ok
            else [
                {
                    "claim": "Spectrum matches stated predictions",
                    "reason": f"t_duality_max_dev={td}, massless_generic={mg}, massless_selfdual={ms}",
                    "severity": "blocking",
                }
            ],
            "summary": "Checked T-duality invariance, generic massless sector, and self-dual enhancement.",
        }
    if phase == "attack_analyst":
        return {
            "verdict": "pass",
            "issues": [
                {
                    "claim": "Truncated lattice (|n|,|w|<=3) represents the full spectrum",
                    "reason": "Enhancement counting at R=1 could miss states just outside the cutoff; needs a cutoff-independence check before exotic topologies",
                    "severity": "minor",
                }
            ],
            "summary": "Result is standard-consistent; flagged truncation as a scaling risk.",
        }
    if phase == "rebut":
        return {
            "responses": [
                {
                    "issue": "Truncated lattice represents the full spectrum",
                    "stance": "accept",
                    "reason": "Massless states at R=1 all sit within |n|,|w|<=2; cutoff at 3 is safe here, re-check when topology changes.",
                }
            ],
            "revised": False,
            "revision": None,
        }
    if phase == "analyze":
        return {
            "title": "Closed string on S^1: KK/winding spectrum validation",
            "patterns": [
                f"T-duality max deviation {metrics.get('t_duality_max_dev', 'n/a')}",
                f"Massless states: {metrics.get('massless_generic', 'n/a')} generic vs {metrics.get('massless_selfdual', 'n/a')} at R=1",
            ],
            "candidate_hypotheses": [
                {
                    "statement": "The massless-state count jumps discontinuously at the self-dual radius R=1 (enhanced symmetry point)",
                    "argument": "Numerical spectrum shows extra M^2=0 states exactly at R=1 from (n,w)=(±1,±1) and (±2,0)/(0,±2) combinations satisfying level matching.",
                    "novelty_rationale": "Needs a literature check — symmetry enhancement at special radii is likely known in the T-duality literature.",
                }
            ],
            "next_directions": [
                "Cutoff-independence check on the enhancement count",
                "T^2 compactification with complex/Kähler moduli",
                "Then orbifolds — first step toward genuinely curved Calabi-Yau spectra",
            ],
            "memo_markdown": (
                "# Closed string on S^1: KK/winding spectrum validation\n\n"
                "## Accepted model\nClosed bosonic string, one dimension on S^1 (alpha'=1); "
                "M^2 = (n/R)^2 + (wR)^2 + 2(N+Ntilde-2), level matching N-Ntilde=nw.\n\n"
                "## Evidence\n"
                f"- t_duality_max_dev: {metrics.get('t_duality_max_dev', 'n/a')}\n"
                f"- massless_generic: {metrics.get('massless_generic', 'n/a')}\n"
                f"- massless_selfdual: {metrics.get('massless_selfdual', 'n/a')}\n\n"
                "## Candidate hypothesis (needs Phase-2 novelty check)\n"
                "Discontinuous massless-count jump at the self-dual radius R=1.\n\n"
                "## Honest scope\nMathematical result only — experimental validation would still be "
                "required for any physical claim.\n"
            ),
        }
    if phase == "novelty":
        hyp = str(payload.get("hypothesis", ""))
        research = web_research(hyp)
        if research["sources"]:
            return {
                "status": "known",
                "summary": research["findings"],
                "citations": research["sources"],
                "reasoning": "Direct textbook match: enhanced gauge symmetry at the self-dual radius.",
            }
        return {
            "status": "novel",
            "summary": "No close match surfaced in the search.",
            "citations": [],
            "reasoning": "Mock index found nothing matching; treat as candidate-novel and test.",
        }
    if phase == "design_test":
        return {
            "model_name": "Test: localization of spectrum enhancement at R=1",
            "equations": [
                "M^2(n,w,N,Ntilde;R) = (n/R)^2 + (w R)^2 + 2(N + Ntilde - 2)",
                "count0(R) = #{states : |M^2| < eps}",
            ],
            "assumptions": [
                "Same truncated lattice as Phase 1 (|n|,|w| <= 3, N,Ntilde <= 3)",
                "eps = 1e-6 massless threshold",
            ],
            "predicted_behavior": [
                "count0(R) attains its maximum exactly at R=1 on a fine radius grid",
                "count0 is symmetric under R -> 1/R (T-duality) to machine precision",
                "generic-R baseline count is 1",
            ],
            "rationale": "design_test: if the enhancement is a genuine self-dual-point effect, the "
            "massless count must peak exactly at R=1 and respect T-duality; a peak elsewhere or "
            "asymmetry refutes the hypothesis.",
        }
    if phase == "phase2_memo":
        return {
            "title": "Phase 2: self-dual enhancement localization test",
            "hypothesis": str(payload.get("hypothesis", "")),
            "outcome": "supported",
            "confidence": "medium",
            "memo_markdown": (
                "# Phase 2 memo: spectrum enhancement at the self-dual radius\n\n"
                f"## Hypothesis\n{payload.get('hypothesis', '')}\n\n"
                "## Novelty check\nSee attached search summary and citations.\n\n"
                "## Test\nMassless-count scan over a fine R grid with T-duality symmetry check.\n\n"
                "## Outcome\nSupported: count peaks exactly at R=1 and the spectrum is R->1/R "
                "symmetric to machine precision.\n\n"
                "## Honest confidence: medium\nTruncated lattice; single compactification. "
                "This is a mathematical result about the model — **experimental validation would "
                "still be required for any claim about physical reality.**\n"
            ),
        }
    return None
