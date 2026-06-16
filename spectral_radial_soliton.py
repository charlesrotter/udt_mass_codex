#!/usr/bin/env python3
"""
spectral_radial_soliton.py -- STAGE A: the SPECTRAL radial coupled Einstein+L2+L4
soliton solver (Chebyshev pseudospectral), the validation gate against the
corrected #56 round soliton.

Driver: Claude (Opus 4.8, 1M).  2026-06-16.  OBSERVE mode.  DATA-BLIND.

WHY THIS FIRST (the #58 cure, measured): #58 (nonlinear_gapcloser) hit a WALL --
its 2-D FD Theta Euler-Lagrange carried a ~0.2 inner-body TRUNCATION residual on
the round profile, which forced the matter FROZEN (w_matter=0), so MATTER could
never deform and matter-shaped catalog types were never probed.  The diagnosis:
FD on the steep core profile + 1/r^2 amplification.  The cure is SPECTRAL: the
Chebyshev derivative is exact-on-polynomials, so the SAME Theta-EL evaluated
spectrally has NO inner-body floor.  Stage A proves this in 1-D (clean spectral
Theta-EL, exponential convergence) before lifting to 2-D where the matter is free.

THE SYSTEM (identical PHYSICS to radial_Bfree_soliton.py / #56; B=1/A FREE):
  ds^2 = -e^{2a(r)} dt^2 + e^{2b(r)} dr^2 + r^2 dOmega^2,  a,b INDEPENDENT.
  Matter = unit-S^3 hedgehog, winding m=1, profile Theta(r).
  Mixed Einstein (verified, verify_indep_einstein / #56):
    G^t_t   = e^{-2b}(-2 r b' - e^{2b} + 1)/r^2
    G^r_r   = e^{-2b}( 2 r a' - e^{2b} + 1)/r^2
    G^th_th = e^{-2b}(r a'^2 - r a'b' + r a'' + a' - b')/r
  Mixed stress (X=e^{-2b}Th'^2, Y=sin^2Th/r^2):
    rho = (xi/2)(X+2Y)+(kap/2)(2XY+Y^2);  p_r = (xi/2)(X-2Y)+(kap/2)(2XY-Y^2)
    p_T = (kap/2)Y^2 - (xi/2)X
  EOS p_r+rho = X(xi+2 kap Y) >= 0 (no exotic matter).

THE SPECTRAL SOLVE (the new solver; PHYSICS reused):
  Unknowns on the CGL grid: a(r) (N+1), b(r) (N+1), Theta(r) (N+1).
  Residual system (the SAME native equations, NOT B=1/A):
    R_b   = (t,t):   G^t_t - kap8*(-rho) = 0            (gives b)
    R_a   = (r,r):   G^r_r - kap8*( p_r) = 0            (gives a)
    R_Th  = Theta-EL (unit S^3 Euler-Lagrange) = 0      (gives Theta, MATTER FREE)
  + boundary conditions (regularity + seal):
    a(seal)=0  (phi=-a, phi(seal)=0; an additive gauge on a)
    Theta(core)=m*pi, Theta(seal)=0  (winding BC)
    b: m_core dial enters via the integrated (t,t); b at core set by the depth dial
       through e^{-2b(core)} = e^{2p} convention (m_core = rc(1-e^{2p})).
  Solved by collocation Newton (dense Jacobian by autodiff-free finite-difference
  perturbation; the SAME native residual, no linearization-as-result -- Newton's
  local linear step is the solver, exactly as the FD #56 used a banded Newton).

  (th,th) is a BIANCHI CONSISTENCY CHECK, NOT imposed -- same as #56.

CATEGORY-A PROOF (delivered numerically in the results doc):
  (i) recovers #56: M_MS=0.281, b0,a0 match; (ii) basis-invariant: matches the FD
  #56 to FD accuracy; (iii) EXPONENTIAL convergence in N (the spectral signature),
  AND the Theta-EL residual reaches machine zero in the inner body (the #58 cure).

PRINCIPLE 2: full nonlinear; spectral derivative = sanctioned exact-on-poly
function-replacement; no linearization kept as a result.
"""
import numpy as np
import math
from spectral_cheb import cheb_interval, clenshaw_curtis_weights

PI = math.pi


# ---------------------------------------------------------------------------
# Matter stress pieces (mixed), unit-S^3 hedgehog.  Thp = dTheta/dr.
# ---------------------------------------------------------------------------
def stress(r, Th, Thp, b, xi, kap):
    X = np.exp(-2.0 * b) * Thp**2
    Y = np.sin(Th)**2 / r**2
    rho = (xi/2)*(X + 2*Y) + (kap/2)*(2*X*Y + Y**2)
    pr = (xi/2)*(X - 2*Y) + (kap/2)*(2*X*Y - Y**2)
    pT = (kap/2)*Y**2 - (xi/2)*X
    return X, Y, rho, pr, pT


# ---------------------------------------------------------------------------
# Mixed Einstein residuals on (a,b,Theta).  D = d/dr (spectral matrix).
# ---------------------------------------------------------------------------
def einstein_pieces(r, a, b, Th, D, xi, kap):
    ap = D @ a
    bp = D @ b
    app = D @ (D @ a)
    Thp = D @ Th
    e2b = np.exp(2.0 * b)
    em2b = np.exp(-2.0 * b)
    Gtt = em2b * (-2*r*bp - e2b + 1) / r**2
    Grr = em2b * (2*r*ap - e2b + 1) / r**2
    Gthth = em2b * (r*ap**2 - r*ap*bp + r*app + ap - bp) / r
    X, Y, rho, pr, pT = stress(r, Th, Thp, b, xi, kap)
    return dict(Gtt=Gtt, Grr=Grr, Gthth=Gthth, rho=rho, pr=pr, pT=pT,
                ap=ap, bp=bp, app=app, Thp=Thp, X=X, Y=Y)


# ---------------------------------------------------------------------------
# Theta Euler-Lagrange residual (unit-S^3), the SAME EL as radial_Bfree_soliton
# (theta_ddot_freed), here as a residual R_Th = Thpp - rhs(Theta,...).
# ---------------------------------------------------------------------------
def theta_el_residual(r, a, b, Th, D, xi, kap):
    ap = D @ a
    bp = D @ b
    Thp = D @ Th
    Thpp = D @ Thp
    s = np.sin(Th)
    e2b = np.exp(2.0 * b)
    num = (-2*kap*r**2*s**2*Thp*ap + 2*kap*r**2*s**2*Thp*bp
           - kap*r**2*np.sin(2*Th)*Thp**2 + 2*kap*e2b*s**3*np.cos(Th)
           - r**4*xi*Thp*ap + r**4*xi*Thp*bp - 2*r**3*xi*Thp
           + r**2*xi*e2b*np.sin(2*Th))
    den = r**2*(2*kap*s**2 + r**2*xi)
    rhs = num / den
    return Thpp - rhs


# ---------------------------------------------------------------------------
# FULL coupled residual vector F(u), u = [a; b; Th], length 3(N+1).
# Interior collocation equations + boundary rows.
#  R_b at interior nodes = (t,t) residual;        b core row: e^{-2b}=e^{2p} (dial)
#  R_a at interior nodes = (r,r) residual;        a seal row: a(seal)=0
#  R_Th at interior nodes = Theta-EL residual;    Th core/seal rows: winding BC
# Index convention: r[0]=core, r[-1]=seal.
# ---------------------------------------------------------------------------
def residual(u, r, D, xi, kap, p, kap8, m=1):
    Np = r.size
    a = u[0:Np]
    b = u[Np:2*Np]
    Th = u[2*Np:3*Np]
    E = einstein_pieces(r, a, b, Th, D, xi, kap)
    Rb = E['Gtt'] - kap8*(-E['rho'])      # (t,t)
    Ra = E['Grr'] - kap8*(E['pr'])        # (r,r)
    RT = theta_el_residual(r, a, b, Th, D, xi, kap)

    F = np.empty(3*Np)
    # --- b block: interior (t,t); core BC fixes b(core) by depth dial ---
    Fb = Rb.copy()
    # depth dial: m_core = rc*(1-e^{2p}); e^{-2b(core)} = 1 - m_core/rc = e^{2p}
    # => b(core) = -p.  This is the SAME deep-neg core dial convention as #56.
    Fb[0] = b[0] - (-p)
    # --- a block: interior (r,r); seal BC a(seal)=0 ---
    Fa = Ra.copy()
    Fa[-1] = a[-1] - 0.0
    # --- Th block: interior EL; core Th=m*pi, seal Th=0 ---
    FT = RT.copy()
    FT[0] = Th[0] - m*PI
    FT[-1] = Th[-1] - 0.0

    F[0:Np] = Fa
    F[Np:2*Np] = Fb
    F[2*Np:3*Np] = FT
    return F


def jacobian_fd(u, r, D, xi, kap, p, kap8, m=1, eps=1e-7):
    """Dense Jacobian of F by finite-difference perturbation (the solver's local
    linear step; NOT a physics linearization).  Coupled full 3(N+1)x3(N+1)."""
    n = u.size
    F0 = residual(u, r, D, xi, kap, p, kap8, m=m)
    J = np.empty((n, n))
    for j in range(n):
        du = np.zeros(n)
        h = eps * (1.0 + abs(u[j]))
        du[j] = h
        Fp = residual(u + du, r, D, xi, kap, p, kap8, m=m)
        J[:, j] = (Fp - F0) / h
    return J, F0


def seed(r, p, m=1, xi=1.0, kap=1.0):
    """Physically motivated seed: a,b from the deep-neg log background, Theta the
    tanh hedgehog (same seed family as #56)."""
    L = math.sqrt(kap/xi)
    rc = r[0]
    b = p * np.log(r / r[-1])          # b(seal)=0, b(core)=p*log(rc/ri)<0... adjust
    # we want b(core)=-p (the dial). Use a simple monotone seed honoring both ends:
    b = -p * (1.0 - (r - rc) / (r[-1] - rc))   # b(core)=-p, b(seal)=0
    a = -b.copy()                               # B=1/A seed (a=-b), freed by solve
    Th = (m*PI) * 0.5 * (1 - np.tanh((r - (rc + 2*L)) / (0.8*L)))
    Th[0] = m*PI
    Th[-1] = 0.0
    return np.concatenate([a, b, Th])


def solve(N, rc=0.05, cell=14.0, p=0.4, kap8=0.05, xi=1.0, kap=1.0, m=1,
          u0=None, maxit=60, tol=1e-11, verbose=False, lm0=1e-10):
    ri = rc + cell
    r, D = cheb_interval(N, rc, ri)
    u = seed(r, p, m=m, xi=xi, kap=kap) if u0 is None else u0.copy()
    lam = lm0
    Fnorm_prev = None
    for it in range(maxit):
        J, F = jacobian_fd(u, r, D, xi, kap, p, kap8, m=m)
        Fnorm = np.max(np.abs(F))
        if verbose and (it % 5 == 0 or it == maxit-1):
            print(f"  [newt] it={it:3d} |F|={Fnorm:.3e} lam={lam:.1e}")
        if Fnorm < tol:
            break
        # Levenberg-Marquardt damped Newton with monotone acceptance
        n = u.size
        accepted = False
        for _try in range(8):
            A = J.T @ J + lam * np.eye(n)
            du = np.linalg.solve(A, -(J.T @ F))
            u_new = u + du
            F_new = residual(u_new, r, D, xi, kap, p, kap8, m=m)
            if np.max(np.abs(F_new)) < Fnorm:
                u = u_new
                lam = max(lam * 0.4, 1e-14)
                accepted = True
                break
            lam *= 4.0
        if not accepted:
            # pure Newton fallback (well-conditioned near solution)
            du = np.linalg.solve(J + 1e-12*np.eye(n), -F)
            u = u + du
        Fnorm_prev = Fnorm

    Np = r.size
    a = u[0:Np]; b = u[Np:2*Np]; Th = u[2*Np:3*Np]
    E = einstein_pieces(r, a, b, Th, D, xi, kap)
    # M_MS = integrated source mass to the seal: m' = kap8 r^2 rho; m_core+integral
    w = clenshaw_curtis_weights(N, rc, ri)
    m_src = np.cumsum(0.5*(kap8*r[1:]**2*E['rho'][1:] + kap8*r[:-1]**2*E['rho'][:-1])*(r[1:]-r[:-1]))
    m_src = np.concatenate([[0.0], m_src])
    M_MS = m_src[-1]   # the source mass integrated across the cell (= #56 def: m_areal(seal)-m_core... )
    # #56 reports M_MS = m_areal(seal) - m_core = m_src(seal). matches.
    res_tt = E['Gtt'] - kap8*(-E['rho'])
    res_rr = E['Grr'] - kap8*(E['pr'])
    res_thth = E['Gthth'] - kap8*(E['pT'])
    rT = theta_el_residual(r, a, b, Th, D, xi, kap)
    return dict(r=r, D=D, a=a, b=b, Th=Th, phi=-a, M_MS=M_MS,
                res_tt=res_tt, res_rr=res_rr, res_thth=res_thth, res_thetaEL=rT,
                Fnorm=np.max(np.abs(residual(u, r, D, xi, kap, p, kap8, m=m))),
                E=E, u=u, m_src=m_src)


if __name__ == "__main__":
    xi = kap = 1.0
    print("=== STAGE A: spectral radial coupled soliton (B=1/A FREE) ===")
    print("Convergence under basis refinement N (the spectral signature):")
    print(f"{'N':>4} {'M_MS':>10} {'|F|':>11} {'max|res_tt|':>12} "
          f"{'max|res_rr|':>12} {'max|EL|(body)':>13} {'a0':>9} {'b0':>9}")
    prev = None
    for N in [32, 48, 64, 96, 128]:
        out = solve(N, p=0.4, kap8=0.05, maxit=80, verbose=False)
        r = out['r']
        # body mask: exclude the very innermost/outermost collocation nodes
        body = (r > 0.5) & (r < r[-1]-0.5)
        elbody = np.max(np.abs(out['res_thetaEL'][body]))
        print(f"{N:>4} {out['M_MS']:>10.6f} {out['Fnorm']:>11.2e} "
              f"{np.max(np.abs(out['res_tt'][body])):>12.2e} "
              f"{np.max(np.abs(out['res_rr'][body])):>12.2e} "
              f"{elbody:>13.2e} {out['a'][0]:>9.4f} {out['b'][0]:>9.4f}")
