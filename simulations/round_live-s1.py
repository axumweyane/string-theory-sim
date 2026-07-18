import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Closed bosonic string on S^1, alpha'=1.
# M^2 = (n/R)^2 + (w R)^2 + 2 (N + Nt - 2), level matching N - Nt = n w.
EPS = 1e-8

def spectrum(R, nmax, lmax):
    out = []
    for n in range(-nmax, nmax + 1):
        for w in range(-nmax, nmax + 1):
            for N in range(lmax + 1):
                for Nt in range(lmax + 1):
                    if N - Nt != n * w:
                        continue
                    out.append((n, w, N, Nt, (n / R) ** 2 + (w * R) ** 2 + 2 * (N + Nt - 2)))
    return out

def masses(R, nmax=3, lmax=3):
    return sorted(round(s[-1], 9) for s in spectrum(R, nmax, lmax))

def massless(R, nmax=3, lmax=3):
    return sum(1 for s in spectrum(R, nmax, lmax) if abs(s[-1]) < EPS)

# P1: T-duality at several radii
t_dev = 0.0
for R in (1.3, 1.7, 2.4, 3.1):
    a, b = masses(R), masses(1.0 / R)
    assert len(a) == len(b)
    t_dev = max(t_dev, max(abs(x - y) for x, y in zip(a, b)))

# P2, P3
m_generic = massless(1.7)
m_selfdual = massless(1.0)

# P4: cutoff independence of the massless counts (3 -> 5)
cutoff_stable = int(massless(1.7, 5, 5) == m_generic and massless(1.0, 5, 5) == m_selfdual)

# The self-dual extra states, listed explicitly for the validator
extra = sorted(s[:4] for s in spectrum(1.0, 3, 3) if abs(s[-1]) < EPS)

# plot: massless count vs R, and low-lying level flow M^2(R)
Rs = np.linspace(0.5, 2.0, 301)
counts = [massless(float(r)) for r in Rs]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
ax1.plot(Rs, counts)
ax1.set_xlabel("R"); ax1.set_ylabel("# massless (n,w,N,Nt) combos")
ax1.set_title("Massless count vs radius (jump at self-dual R=1)")
flow = np.array([[m for m in masses(float(r)) if m < 6.05][:14] for r in Rs])
for k in range(flow.shape[1]):
    ax2.plot(Rs, flow[:, k], lw=0.8)
ax2.set_xlabel("R"); ax2.set_ylabel("$M^2$")
ax2.set_title("Low-lying level flow")
fig.tight_layout()
fig.savefig("outputs/live_s1_spectrum.png", dpi=120)

print("EXTRA_MASSLESS_AT_SELFDUAL:", extra)
print("RESULT_JSON: " + json.dumps({
    "t_duality_max_dev": t_dev,
    "massless_generic": m_generic,
    "massless_selfdual": m_selfdual,
    "cutoff_stable_3_to_5": cutoff_stable,
}))
