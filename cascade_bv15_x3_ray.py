"""bv15 X3: nonlinear ray S[bg + eps*mode] - S[bg] on B00.

Configuration at ray parameter eps:
  inner endpoint a(eps) = eps*alpha   (inner fold shift; no essential constraint there)
  outer endpoint b(eps):
     EXACT handling:   b solves phi(b) + eps*u_ext(b) = 0 (root-found per eps, tol 1e-13)
     FIRST-ORDER-only: b = r_s + eps*beta
  fields: phi_eps = phi + eps*u_ext, rho_eps = rho + eps*v_ext on [a, b].
Extensions (stated): background by the ODE dense solution (valid to r_s+1.3; even reflection
for r<0); mode u,v by cubic spline on [0, r_s], LINEAR extension past r_s with the end slope,
EVEN extension for r<0. Mode = the MC1 deflated negative-branch eigenvector at M=51200,
normalized x^T M_MC1 x = 1 (lambda_defl(51200) = the comparison lambda).
Action: S = int L dr, L = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2 - U(rho).
Quadrature: composite Simpson, N=2^19 intervals (error checked by N-doubling).
"""
import numpy as np, json, os, sys
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
import bv15_asm as asm
from bv15_x2_anatomy import defl_solve

SCR = os.path.dirname(os.path.abspath(__file__))
NQ = 2**19


def get_mode(info, sol, M):
    Q, idx = asm.assemble_Q(info, sol, M)
    Mm = asm.mass(info, idx, "MC1")
    t = asm.translation(idx)
    perm = asm.order_interleave(idx)
    w, Y, gam, _ = defl_solve(Q, Mm, t, perm)
    j = int(np.argmin(w))                       # negative branch (verified negative at 51200)
    lam = float(w[j])
    x = Y[:, j] / np.sqrt(Y[:, j] @ (Mm @ Y[:, j]))
    al, be = x[idx["ia"]], x[idx["ib"]]
    rn = idx["rn"]
    un = np.concatenate([x[idx["iu"]], [-info["phip_s"] * be]])
    vn = x[idx["iv"]]
    # sign convention: make alpha > 0
    if al < 0:
        x = -x; al, be, un, vn = -al, -be, -un, -vn
    us = CubicSpline(rn, un)
    vs = CubicSpline(rn, vn)
    return lam, float(al), float(be), us, vs, rn[-1]


def field_evals(sol, r_s, us, vs, r):
    """Background + mode at points r (with stated extensions). Returns phi,phip,rho,rhop,u,v."""
    r = np.asarray(r)
    ra = np.abs(r)                              # even reflection for r<0
    y = sol.sol(ra)
    phi, phip, rho, rhop = y
    sgn = np.where(r < 0, -1.0, 1.0)
    phip = phip * sgn; rhop = rhop * sgn
    inside = ra <= r_s
    u = np.where(inside, us(np.minimum(ra, r_s)), 0.0)
    v = np.where(inside, vs(np.minimum(ra, r_s)), 0.0)
    if np.any(~inside):
        ro = ra[~inside]
        u_end, up_end = us(r_s), us(r_s, 1)
        v_end, vp_end = vs(r_s), vs(r_s, 1)
        u = np.array(u); v = np.array(v)
        u[~inside] = u_end + up_end * (ro - r_s)
        v[~inside] = v_end + vp_end * (ro - r_s)
    up = np.where(inside, us(np.minimum(ra, r_s), 1), us(r_s, 1)) * sgn
    vp = np.where(inside, vs(np.minimum(ra, r_s), 1), vs(r_s, 1)) * sgn
    return phi, phip, rho, rhop, u, up, v, vp


def _simpson_piece(info, sol, us, vs, r_s, eps, a, b, U, n):
    if b <= a:
        return 0.0
    n = max(8, int(np.ceil(n / 2.0)) * 2)
    r = np.linspace(a, b, n + 1)
    phi, phip, rho, rhop, u, up, v, vp = field_evals(sol, r_s, us, vs, r)
    P = phi + eps * u; Pp = phip + eps * up
    R = rho + eps * v; Rp = rhop + eps * vp
    L = 0.5 * info["Z"] * R**2 * Pp**2 - 2.0 * np.exp(-2.0 * P) * Rp**2 + 2.0 - U(R)
    h = (b - a) / n
    w = np.ones(n + 1); w[1:-1:2] = 4.0; w[2:-1:2] = 2.0
    return float(h / 3.0 * np.sum(w * L))


def action(info, sol, us, vs, r_s, eps, a, b, U):
    """Piecewise Simpson of L[phi+eps u, rho+eps v] over [a,b]; exact breakpoints at the
    r=0 reflection kink and the r_s mode-extension kink; interior piece always [max(a,0),
    min(b,r_s)] with NQ intervals (matches the S0 grid when a<=0<=r_s<=b)."""
    S = 0.0
    lo, hi = max(a, 0.0), min(b, r_s)
    S += _simpson_piece(info, sol, us, vs, r_s, eps, lo, hi, U, NQ)
    if a < 0.0:
        S += _simpson_piece(info, sol, us, vs, r_s, eps, a, 0.0, U, 8192)
    if b > r_s:
        S += _simpson_piece(info, sol, us, vs, r_s, eps, r_s, b, U, 8192)
    return S


def phi_eps_at(sol, r_s, us, vs, eps, b):
    phi = sol.sol(b)[0]
    if b <= r_s:
        u = us(b)
    else:
        u = us(r_s) + us(r_s, 1) * (b - r_s)
    return phi + eps * u


if __name__ == "__main__":
    info, sol = asm.load_bg("B00")
    U, _, _ = asm.makeU(info["a"], info["m"])
    lam, al, be, us, vs, r_s = get_mode(info, sol, 51200)
    print(f"mode: lam(51200)={lam:+.5e} alpha={al:+.5f} beta={be:+.5f} "
          f"u(rs)={float(us(r_s)):+.5f} v(rs)={float(vs(r_s)):+.5f}")
    S0 = action(info, sol, us, vs, r_s, 0.0, 0.0, r_s, U)
    print(f"S0 = {S0:.10f}")
    eps_list = [0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.18, 0.25, 0.30, 0.35]
    eps_list = sorted([-e for e in eps_list] + eps_list)
    rows = []
    for eps in eps_list:
        a = eps * al
        b1 = r_s + eps * be                              # first-order-only
        f = lambda bb: phi_eps_at(sol, r_s, us, vs, eps, bb)
        lo, hi = b1 - 0.3, b1 + 0.3
        bex = brentq(f, lo, hi, xtol=1e-13, rtol=8.9e-16)
        dS_ex = action(info, sol, us, vs, r_s, eps, a, bex, U) - S0
        dS_fo = action(info, sol, us, vs, r_s, eps, a, b1, U) - S0
        rows.append(dict(eps=eps, a=a, b_fo=b1, b_ex=bex,
                         phi_res_fo=float(f(b1)), dS_ex=dS_ex, dS_fo=dS_fo))
        print(f"eps={eps:+.3f} a={a:+.4f} b_ex-rs={bex-r_s:+.6f} b_fo-rs={b1-r_s:+.6f} "
              f"dS_ex={dS_ex:+.6e} dS_fo={dS_fo:+.6e}")
        sys.stdout.flush()
    # fits
    def fit(rows, key, kmax, esub=None):
        e = np.array([r["eps"] for r in rows if esub is None or abs(r["eps"]) <= esub])
        y = np.array([r[key] for r in rows if esub is None or abs(r["eps"]) <= esub])
        A = np.vstack([e**k for k in range(1, kmax + 1)]).T
        c, *_ = np.linalg.lstsq(A, y, rcond=None)
        return c
    for esub in (0.05, 0.12, None):
        cex = fit(rows, "dS_ex", 4 if esub else 5, esub)
        cfo = fit(rows, "dS_fo", 4 if esub else 5, esub)
        print(f"[fit |eps|<={esub}] exact: c1={cex[0]:+.3e} c2={cex[1]:+.6e} c3={cex[2]:+.3e}")
        print(f"[fit |eps|<={esub}] f-ord: c1={cfo[0]:+.3e} c2={cfo[1]:+.6e} c3={cfo[2]:+.3e}")
        print(f"   c2_ex/lam={cex[1]/lam:+.4f}  2*c2_ex/lam={2*cex[1]/lam:+.4f}  "
              f"leak c2_fo-c2_ex={cfo[1]-cex[1]:+.4e}")
    json.dump(dict(lam=lam, alpha=al, beta=be, S0=S0, rows=rows),
              open(os.path.join(SCR, "bv15_x3_ray.json"), "w"), indent=1)
