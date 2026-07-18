import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Wilson-line deformation as the off-diagonal torus modulus (alpha'=1):
# vielbein e = [[R1, a],[0, R2]] -> G = e^T e, B = 0.
# a = Wilson line of the circle-2 graviphoton along circle 1.
EPS = 1e-8
R1, R2 = 1.0, 1.55
Q = 4
_r = np.arange(-Q, Q + 1)
CH = np.array(np.meshgrid(_r, _r, _r, _r, indexing="ij")).reshape(4, -1).T
N_, W_ = CH[:, :2].astype(float), CH[:, 2:].astype(float)
DOT = np.einsum("ij,ij->i", N_, W_)


def pLpR2(a):
    e = np.array([[R1, a], [0.0, R2]])
    G = e.T @ e
    Gi = np.linalg.inv(G)
    vp = N_ + W_ @ G.T
    vm = N_ - W_ @ G.T
    pL2 = 0.5 * np.einsum("ij,jk,ik->i", vp, Gi, vp)
    pR2 = 0.5 * np.einsum("ij,jk,ik->i", vm, Gi, vm)
    return pL2, pR2


def massless_count(a):
    pL2, pR2 = pLpR2(a)
    S = 2.0 - 0.5 * (pL2 + pR2)
    ok = (np.abs(S - np.round(S)) < EPS) & (np.round(S) >= np.abs(DOT)) \
         & (np.abs(np.mod(np.round(S) - DOT, 2)) < EPS)
    return int(np.sum(ok))


def low_spectrum(a, m2max=5.5):
    pL2, pR2 = pLpR2(a)
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


# level-matching identity under the deformation (derivation check)
lm_dev = 0.0
for a in (0.0, 0.23, 0.5, 0.81, 1.0):
    pL2, pR2 = pLpR2(a)
    lm_dev = max(lm_dev, float(np.max(np.abs(0.5 * (pL2 - pR2) - DOT))))

# P1/P2/P4: counts at key Wilson-line values
c0, c_small, c_half, c_one = massless_count(0.0), massless_count(0.05), massless_count(0.5), massless_count(1.0)

# P3: exact periodicity a -> a + R1 at a generic a
K = 60
period_dev = float(np.max(np.abs(low_spectrum(0.37)[:K] - low_spectrum(1.37)[:K])))

# scan: count + level flow vs a
avals = np.linspace(0.0, 1.2, 241)
counts = [massless_count(float(a)) for a in avals]
flow = np.array([low_spectrum(float(a), 4.4)[:12] for a in avals])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
ax1.plot(avals, counts)
ax1.set_xlabel("Wilson line a"); ax1.set_ylabel("# massless states")
ax1.set_title(f"Enhancement breaking/restoration (R1=1, R2={R2})")
for k in range(flow.shape[1]):
    ax2.plot(avals, flow[:, k], lw=0.8)
ax2.set_xlabel("Wilson line a"); ax2.set_ylabel("$M^2$")
ax2.set_title("Low-lying level flow vs a")
fig.tight_layout()
fig.savefig("outputs/live_wilson_line.png", dpi=120)

restored_at = [float(avals[i]) for i in range(len(avals)) if counts[i] == c0]
print("RESTORED_AT:", restored_at)
print("RESULT_JSON: " + json.dumps({
    "lm_identity_dev": lm_dev,
    "massless_a0": c0,
    "massless_a005": c_small,
    "massless_a05": c_half,
    "massless_a1": c_one,
    "periodicity_dev_K60": period_dev,
}))
