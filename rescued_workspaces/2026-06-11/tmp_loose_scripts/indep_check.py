"""Independent verification of native_sector_weight_spectral_probe.py eigenvalues.

Methods deliberately different from the script's control-volume FV eigensolver:
  A) analytic Bessel solution for Lambda=0 power-law cells
  B) shooting method (solve_ivp + brentq) in x = ln r
  C) uniform-in-r second-order FD with exact boundary-node Dirichlet,
     Richardson extrapolated
"""
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import jv

XSPAN = 12.0

# ---------- A) analytic: q power law, Lambda=0, Dirichlet ----------
# -(r^{2-q} R')' = w^2 r^{2+q} R  on (0,1], regular at 0, R(1)=0
# regular solution R = r^{(q-1)/2} J_nu( w r^{1+q}/(1+q) ), nu=(1-q)/(2(1+q))
# (positive order gives R ~ const, flux -> 0). Dirichlet: J_nu(w/(1+q))=0.
def analytic_lam0(q, n=1):
    nu = (1.0 - q) / (2.0 * (1.0 + q))
    # find nth zero of J_nu
    zeros = []
    z = 0.1
    step = 0.05
    prev = jv(nu, z)
    while len(zeros) < n:
        z2 = z + step
        cur = jv(nu, z2)
        if prev * cur < 0:
            zeros.append(brentq(lambda t: jv(nu, t), z, z2, xtol=1e-14))
        z, prev = z2, cur
    return (1.0 + q) * zeros[n - 1]

# ---------- B) shooting in x = ln r ----------
# R_xx + (1-q) R_x + (w^2 e^{(2+2q)x} - Lam e^{q x}) R = 0
# x in [-XSPAN, 0]; inner zero flux: R(-XSPAN)=1, R_x(-XSPAN)=0
def shoot_residual(w, q, lam, bc, xspan=XSPAN):
    def rhs(x, y):
        R, Rx = y
        return [Rx, -(1.0 - q) * Rx - (w * w * math.exp((2.0 + 2.0 * q) * x)
                                       - lam * math.exp(q * x)) * R]
    sol = solve_ivp(rhs, (-xspan, 0.0), [1.0, 0.0], rtol=1e-11, atol=1e-13,
                    dense_output=False, max_step=0.05)
    R, Rx = sol.y[0][-1], sol.y[1][-1]
    return R if bc == "dirichlet" else Rx

def shoot_eigs(q, lam, bc, wmax, nwant=4, xspan=XSPAN):
    ws = np.linspace(0.05, wmax, 400)
    vals = [shoot_residual(w, q, lam, bc, xspan) for w in ws]
    eigs = []
    for i in range(len(ws) - 1):
        if vals[i] * vals[i + 1] < 0:
            eigs.append(brentq(shoot_residual, ws[i], ws[i + 1],
                               args=(q, lam, bc, xspan), xtol=1e-12, rtol=1e-13))
            if len(eigs) >= nwant:
                break
    return eigs

# ---------- C) uniform-in-r FD, Richardson ----------
# -(r^2 f R')' + Lam R = w^2 (r^2/f) R, f = r^{-q} (R_cell=1)
def fd_uniform_r(q, lam, bc, ngrid, rmin=math.exp(-XSPAN)):
    from scipy.sparse import diags
    from scipy.sparse.linalg import eigsh
    r = np.linspace(rmin, 1.0, ngrid)
    h = r[1] - r[0]
    rh = 0.5 * (r[:-1] + r[1:])
    p = rh ** (2.0 - q)
    n = ngrid
    left = np.zeros(n); right = np.zeros(n)
    left[1:] = p; right[:-1] = p
    vol = np.full(n, h); vol[0] = 0.5 * h; vol[-1] = 0.5 * h
    if bc == "dirichlet":
        m = n - 1
        vold = np.full(m, h); vold[0] = 0.5 * h
        main = (left[:m] + right[:m]) / h + lam * vold
        A = diags([-p[:m - 1] / h, main, -p[:m - 1] / h], [-1, 0, 1], format="csr")
        B = diags((r[:m] ** (2.0 + q)) * vold, 0, format="csr")
    else:
        right[-1] = 0.0
        main = (left + right) / h + lam * vol
        A = diags([-p / h, main, -p / h], [-1, 0, 1], format="csr")
        B = diags((r ** (2.0 + q)) * vol, 0, format="csr")
    vals = eigsh(A, M=B, k=1, sigma=-1e-6, which="LM", return_eigenvectors=False)
    return math.sqrt(max(vals[0], 0.0))

def main():
    print("== A) analytic Bessel, Lambda=0, Dirichlet ==")
    for q, claimed in [(1.0 / 3.0, [3.7078483, 7.8748315, 12.056417, 16.241554]),
                       (0.0, [math.pi, 2 * math.pi, 3 * math.pi, 4 * math.pi])]:
        for n in range(1, 5):
            w = analytic_lam0(q, n)
            print(f"  q={q:.6f} n={n}: analytic={w:.8f}  claimed={claimed[n-1]:.8f}"
                  f"  rel.dev={abs(w/claimed[n-1]-1):.2e}")

    print("\n== B) shooting in x ==")
    cases = [
        ("q=1/3 Lam=0 dir", 1/3, 0.0, "dirichlet", 18.0, 3.7078483),
        ("q=1/3 Lam=2 dir", 1/3, 2.0, "dirichlet", 18.0, 5.0328001),
        ("q=sqrt2-1 Lam=2 dir", math.sqrt(2)-1, 2.0, "dirichlet", 19.0, 5.1650086),
        ("flat q=0 Lam=0 dir", 0.0, 0.0, "dirichlet", 13.5, math.pi),
        ("q=1/3 Lam=6 flux", 1/3, 6.0, "flux", 17.5, 3.49418),
        ("q=1/3 Lam=16 flux", 1/3, 16.0, "flux", 19.5, 5.295801),
        ("q=1/3 Lam=2 flux", 1/3, 2.0, "flux", 16.0, 2.2024467),
        ("q=A3 Lam=2 flux", math.sqrt(2)-1, 2.0, "flux", 16.0, 2.2326216),
    ]
    shoot = {}
    for label, q, lam, bc, wmax, claimed in cases:
        eigs = shoot_eigs(q, lam, bc, wmax, nwant=4)
        w1 = eigs[0]
        shoot[label] = w1
        print(f"  {label}: w1={w1:.8f}  claimed={claimed:.8f}"
              f"  rel.dev={abs(w1/claimed-1):.2e}   (modes: "
              + " ".join(f"{e:.6f}" for e in eigs) + ")")

    print("\n  EXP3 isolated-hit ratio (shooting, flux): "
          f"w1(Lam=16)/w1(Lam=6) = {shoot['q=1/3 Lam=16 flux']/shoot['q=1/3 Lam=6 flux']:.10f}"
          f"  vs exp(5/12)={math.exp(5/12):.10f}"
          f"  dev={abs(shoot['q=1/3 Lam=16 flux']/shoot['q=1/3 Lam=6 flux']/math.exp(5/12)-1):.3e}")
    print("  EXP2 A3/common flux ratio (shooting): "
          f"{shoot['q=A3 Lam=2 flux']/shoot['q=1/3 Lam=2 flux']:.8f} (script: 1.01370065)")

    print("\n== C) uniform-in-r FD + Richardson, q=1/3 Lam=2 dirichlet ==")
    w_a = fd_uniform_r(1/3, 2.0, "dirichlet", 40000)
    w_b = fd_uniform_r(1/3, 2.0, "dirichlet", 80000)
    w_rich = (4 * w_b - w_a) / 3.0
    print(f"  n=40000: {w_a:.8f}  n=80000: {w_b:.8f}  Richardson: {w_rich:.8f}"
          f"  claimed 5.0328001  dev={abs(w_rich/5.0328001-1):.2e}")

if __name__ == "__main__":
    main()
