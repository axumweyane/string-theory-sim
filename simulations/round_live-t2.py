import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Closed bosonic string on T^2, alpha'=1, Narain form.
# G = (rho2/tau2) [[1, tau1],[tau1, |tau|^2]], B12 = rho1
# v_pm = n + (B pm G) w ; p_{L,R}^2 = (1/2) v_pm^T G^{-1} v_pm
# M^2 = pL^2 + pR^2 + 2(N + Nt - 2), level matching N - Nt = n.w
EPS = 1e-8
Q = 4  # charge box

_r = np.arange(-Q, Q + 1)
CH = np.array(np.meshgrid(_r, _r, _r, _r, indexing="ij")).reshape(4, -1).T  # (n1,n2,w1,w2)
N_, W_ = CH[:, :2].astype(float), CH[:, 2:].astype(float)
DOT = np.einsum("ij,ij->i", N_, W_)  # n.w


def pLpR2(tau, rho):
    t1, t2 = tau.real, tau.imag
    r1, r2 = rho.real, rho.imag
    G = (r2 / t2) * np.array([[1.0, t1], [t1, abs(tau) ** 2]])
    B = np.array([[0.0, r1], [-r1, 0.0]])
    Gi = np.linalg.inv(G)
    vp = N_ + W_ @ (B + G).T
    vm = N_ + W_ @ (B - G).T
    pL2 = 0.5 * np.einsum("ij,jk,ik->i", vp, Gi, vp)
    pR2 = 0.5 * np.einsum("ij,jk,ik->i", vm, Gi, vm)
    return pL2, pR2


def low_spectrum(tau, rho, m2max=5.5):
    """All level-matched M^2 < m2max. Oscillator sum S = N+Nt >= |n.w|, S == n.w mod 2
    (exact enumeration, no level cutoff)."""
    pL2, pR2 = pLpR2(tau, rho)
    base = pL2 + pR2
    out = []
    for b, d in zip(base, DOT):
        S = abs(int(round(d)))
        while True:
            m2 = b + 2 * (S - 2)
            if m2 >= m2max:
                break
            out.append(m2)
            S += 2
    return np.sort(np.array(out))


def massless_count(tau, rho):
    pL2, pR2 = pLpR2(tau, rho)
    S = 2.0 - 0.5 * (pL2 + pR2)          # required N + Nt
    ok = (np.abs(S - np.round(S)) < EPS) & (np.round(S) >= np.abs(DOT)) \
         & (np.abs(np.mod(np.round(S) - DOT, 2)) < EPS)
    return int(np.sum(ok))


# P1: level-matching identity at random moduli (derivation check)
rng = np.random.default_rng(7)
lm_dev = 0.0
for _ in range(5):
    tau = complex(rng.uniform(-1, 1), rng.uniform(0.6, 2.0))
    rho = complex(rng.uniform(-1, 1), rng.uniform(0.6, 2.0))
    pL2, pR2 = pLpR2(tau, rho)
    lm_dev = max(lm_dev, float(np.max(np.abs(0.5 * (pL2 - pR2) - DOT))))

# P2: duality invariance of the K lowest levels at a generic point
tau0, rho0 = 0.31 + 1.27j, 0.63 + 1.94j
K = 60
ref = low_spectrum(tau0, rho0)[:K]
duality_dev = 0.0
for tt, rr in [(tau0 + 1, rho0), (-1 / tau0, rho0), (tau0, rho0 + 1), (tau0, -1 / rho0), (rho0, tau0)]:
    duality_dev = max(duality_dev, float(np.max(np.abs(low_spectrum(tt, rr)[:K] - ref))))

# P3: massless counts
c_generic = massless_count(tau0, rho0)
c_locus = massless_count(0.4 + 1.3j, 0.4 + 1.3j)
c_su2su2 = massless_count(1j, 1j)
w3 = np.exp(1j * np.pi / 3)
c_su3 = massless_count(w3, w3)

# P4: heatmap over the tau = rho = x + iy patch
xs, ys = np.linspace(-0.65, 0.65, 53), np.linspace(0.55, 1.45, 37)
H = np.array([[massless_count(complex(x, y), complex(x, y)) for x in xs] for y in ys])
peaks = [(float(xs[j]), float(ys[i])) for i, j in zip(*np.where(H == H.max()))]

fig, ax = plt.subplots(figsize=(7.5, 5))
im = ax.pcolormesh(xs, ys, H, shading="nearest", cmap="magma")
ax.plot([0], [1], "c+", ms=14, mew=2, label="tau=rho=i (SU(2)^2)")
ax.plot([0.5, -0.5], [np.sqrt(3) / 2] * 2, "wx", ms=10, mew=2, label="tau=rho=exp(i pi/3) (SU(3))")
ax.set_xlabel("x = Re tau = Re rho"); ax.set_ylabel("y = Im tau = Im rho")
ax.set_title("Massless count on the tau = rho locus")
ax.legend(loc="upper right", fontsize=8)
fig.colorbar(im, ax=ax, label="# massless states")
fig.tight_layout()
fig.savefig("outputs/live_t2_moduli.png", dpi=120)

print("HEATMAP_MAX:", int(H.max()), "at", peaks)
print("RESULT_JSON: " + json.dumps({
    "lm_identity_dev": lm_dev,
    "duality_dev_K60": duality_dev,
    "massless_generic": c_generic,
    "massless_locus_generic": c_locus,
    "massless_tau_rho_i": c_su2su2,
    "massless_tau_rho_w3": c_su3,
}))
