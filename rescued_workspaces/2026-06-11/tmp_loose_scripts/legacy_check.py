"""Reimplement legacy ghost-node scheme of native_cell_spectrum.py verbatim
and check (1) absolute accuracy cap, (2) whether EXP2/EXP3 ratio verdicts change."""
import math
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

def legacy_spectrum(q, lam, ngrid, bc, rmin=math.exp(-12.0), modes=1):
    # f(r) = r^{-q}, R_cell = 1 (matches f_func of legacy with this background)
    r = np.linspace(rmin, 1.0, ngrid)
    h = r[1] - r[0]
    r_half = 0.5 * (r[:-1] + r[1:])
    p_half = r_half * r_half * r_half ** (-q)
    left = np.zeros(ngrid); right = np.zeros(ngrid)
    left[1:] = p_half; right[:-1] = p_half
    if bc == "dirichlet":
        right[-1] = 1.0  # rmax^2 f(rmax) = 1 (ghost node R=0 at rmax+h)
    else:
        right[-1] = 0.0
    main = (left + right) / (h * h) + lam
    lower = -left[1:] / (h * h)
    upper = -right[:-1] / (h * h)
    weight = r * r / r ** (-q)
    A = diags([lower, main, upper], [-1, 0, 1], format="csr")
    B = diags(weight, 0, format="csr")
    vals = eigsh(A, M=B, k=modes, sigma=1e-8, which="LM", return_eigenvectors=False)
    return np.sqrt(np.maximum(np.sort(vals), 0.0))

def digits(a, b):
    return -math.log10(max(abs(a - b) / max(abs(a), abs(b)), 1e-16))

TRUE = {  # from shooting (converged to ~1e-11)
    ("dir", 1/3, 2.0): 5.03280440,
}

print("== legacy absolute accuracy, q=1/3 Lam=2 dirichlet (truth 5.03280440 from shooting) ==")
for n in (1800, 3600, 7200, 14400):
    w = legacy_spectrum(1/3, 2.0, n, "dirichlet")[0]
    print(f"  ngrid={n:6d}: w1={w:.8f}  digits vs truth={digits(w, 5.03280440):.2f}")

print()
print("== legacy ratios, EXP2 (Lam=2, q backgrounds) and EXP3 (q=1/3, Lam_eff) ==")
QS = {"common": 1/3, "A3": math.sqrt(2)-1, "S5": (2*math.sqrt(10)-5)/3,
      "T8": (2*math.sqrt(22)-8)/3}
W = {"common": 1/12, "A3": 0.25, "S5": 5/12, "T8": 2/3}
NG = 3600
for bc in ("dirichlet", "flux"):
    w1 = {k: legacy_spectrum(qv, 2.0, NG, bc)[0] for k, qv in QS.items()}
    print(f" EXP2 {bc}:")
    for name in ("A3", "S5", "T8"):
        r_obs = w1[name] / w1["common"]
        best = min(
            ("W", W[name]/W["common"]), ("expW", math.exp(W[name]-W["common"])),
            ("sqrtW", math.sqrt(W[name]/W["common"])),
            key=lambda c: abs(r_obs / c[1] - 1.0))
        print(f"   {name}/common ratio={r_obs:.8f}  best cand {best[0]}={best[1]:.6f} "
              f"dev={abs(r_obs/best[1]-1):.3e}  -> {'HIT' if abs(r_obs/best[1]-1)<=1e-3 else 'no relation'}")
    for name in ("S5", "T8"):
        r_obs = w1[name] / w1["A3"]
        best = min(
            ("W", W[name]/W["A3"]), ("expW", math.exp(W[name]-W["A3"])),
            ("sqrtW", math.sqrt(W[name]/W["A3"])),
            key=lambda c: abs(r_obs / c[1] - 1.0))
        print(f"   {name}/A3     ratio={r_obs:.8f}  best cand {best[0]}={best[1]:.6f} "
              f"dev={abs(r_obs/best[1]-1):.3e}  -> {'HIT' if abs(r_obs/best[1]-1)<=1e-3 else 'no relation'}")

for bc in ("dirichlet", "flux"):
    w3 = {tr: legacy_spectrum(1/3, 2.0*tr, NG, bc)[0] for tr in (1, 3, 5, 8)}
    print(f" EXP3 {bc}:")
    for name, tr in (("S5", 5), ("T8", 8)):
        r_obs = w3[tr] / w3[3]
        best = min(
            ("W", W[name]/W["A3"]), ("expW", math.exp(W[name]-W["A3"])),
            ("sqrtW", math.sqrt(W[name]/W["A3"])),
            key=lambda c: abs(r_obs / c[1] - 1.0))
        print(f"   Tr{tr}/Tr3 ratio={r_obs:.8f}  best cand {best[0]}={best[1]:.6f} "
              f"dev={abs(r_obs/best[1]-1):.3e}  -> {'HIT' if abs(r_obs/best[1]-1)<=1e-3 else 'no relation'}")
    for name, tr in (("A3", 3), ("S5", 5), ("T8", 8)):
        r_obs = w3[tr] / w3[1]
        best = min(
            ("W", W[name]/W["common"]), ("expW", math.exp(W[name]-W["common"])),
            ("sqrtW", math.sqrt(W[name]/W["common"])),
            key=lambda c: abs(r_obs / c[1] - 1.0))
        print(f"   Tr{tr}/bare ratio={r_obs:.8f}  best cand {best[0]}={best[1]:.6f} "
              f"dev={abs(r_obs/best[1]-1):.3e}  -> {'HIT' if abs(r_obs/best[1]-1)<=1e-3 else 'no relation'}")
