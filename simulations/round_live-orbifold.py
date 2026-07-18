import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Asymmetric shift orbifold of S^1 (alpha'=1): g: X_L -> X_L + pi R.
# Phase on |n,w>: exp(2 pi i (n/2 + w R^2/2)); twisted charges (n + R^2/2, w + 1/2).
# Shift orbifolds do not twist oscillators -> consistency is lattice arithmetic.
EPS = 1e-9
Q = 6
ns, ws = np.meshgrid(np.arange(-Q, Q + 1), np.arange(-Q, Q + 1), indexing="ij")
ns, ws = ns.ravel(), ws.ravel()


def class_spread(b, a=0.5):
    """Max circular spread of frac((n+b)(w+a)) within (n%2, w%2) classes.
    0 => an order-2 projection can level-match the twisted sector (necessary cond.)."""
    f = np.mod((ns + b) * (ws + a), 1.0)
    worst = 0.0
    for pn in (0, 1):
        for pw in (0, 1):
            sel = f[(ns % 2 == pn) & (ws % 2 == pw)]
            d = np.abs(sel - sel[0])
            worst = max(worst, float(np.max(np.minimum(d, 1.0 - d))))
    return worst


# P2: scan R^2 — asymmetric (b = R^2/2) vs symmetric geometric shift (b = 0)
R2s = np.linspace(0.6, 4.4, 191)
asym = np.array([class_spread(r2 / 2.0) for r2 in R2s])
sym = np.array([class_spread(0.0) for _ in R2s])
int_points = {int(k): class_spread(k / 2.0) for k in (1, 2, 3, 4)}

# frac class present at integer R^2 must equal delta.delta/2 = R^2/4 mod 1
class_reps = {}
for k in (1, 2):
    f = np.mod((ns + k / 2.0) * (ws + 0.5), 1.0)
    class_reps[k] = sorted(set(np.round(f, 9)))

# P3 at R = 1: untwisted projection keeps (-1)^(n+w) = +1
def s1_massless(R):
    out = []
    for n in range(-3, 4):
        for w in range(-3, 4):
            for N in range(4):
                for Nt in range(4):
                    if N - Nt != n * w:
                        continue
                    if abs((n / R) ** 2 + (w * R) ** 2 + 2 * (N + Nt - 2)) < 1e-8:
                        out.append((n, w, N, Nt))
    return out

kept = [s for s in s1_massless(1.0) if (s[0] + s[1]) % 2 == 0]
total = s1_massless(1.0)

# twisted-sector minimal |M^2| at R=1 (charges n+1/2, w+1/2; no oscillator twist)
tw_m2 = []
for n in range(-4, 5):
    for w in range(-4, 5):
        pl2 = 0.5 * ((n + 0.5) + (w + 0.5)) ** 2
        pr2 = 0.5 * ((n + 0.5) - (w + 0.5)) ** 2
        d = pl2 - pr2  # = 2(n+1/2)(w+1/2), frac class 1/4 handled by twisted vacuum phase
        for S in range(0, 6):
            tw_m2.append(pl2 + pr2 + 2 * (S - 2))
min_tw = float(min(abs(m) for m in tw_m2))

fig, ax = plt.subplots(figsize=(7.5, 4.6))
ax.plot(R2s, asym, label="asymmetric shift (X_L only)")
ax.plot(R2s, sym, "--", label="symmetric geometric shift")
for k in (1, 2, 3, 4):
    ax.axvline(k, color="gray", lw=0.5, alpha=0.5)
ax.plot(list(int_points), [int_points[k] for k in int_points], "ro", label="integer $R^2$")
ax.set_xlabel("$R^2$"); ax.set_ylabel("level-matchability violation (class spread)")
ax.set_title("Asymmetric shift orbifold: consistent only at integer $R^2$")
ax.legend()
fig.tight_layout()
fig.savefig("outputs/live_asym_orbifold.png", dpi=120)

print("CLASS_FRACS R^2=1:", class_reps[1], " R^2=2:", class_reps[2])
print("RESULT_JSON: " + json.dumps({
    "asym_spread_generic_max": float(asym.max()),
    "asym_spread_generic_min_offint": float(min(a for r2, a in zip(R2s, asym) if abs(r2 - round(r2)) > 0.05)),
    "asym_spread_at_int_R2": max(int_points.values()),
    "sym_spread_all_R": float(sym.max()),
    "untwisted_massless_kept_R1": len(kept),
    "untwisted_massless_total_R1": len(total),
    "twisted_min_absM2_R1": min_tw,
}))
