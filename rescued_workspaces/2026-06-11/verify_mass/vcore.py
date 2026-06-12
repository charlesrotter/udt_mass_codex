"""BLIND VERIFIER core engine — written from scratch from the pinned
conventions (sealed_cavity_s1_results.md + audit_core.py docstring).
Independent choices: own harmonics/quadrature (GL N=3200 default),
own closed-form f_min (cubic derivative roots), own event handling,
action/momentum-transfer integrals carried INSIDE the ODE as quadrature
states (not post-hoc Simpson), tighter tolerances (rtol 1e-12).

Conventions pinned:
  f(t,u) = sum_l X_l(t) Y_l(u), Y orthonormal in (1/2)Int_{-1}^1 du
  t = ln(1/y); A = Int e^{-t}[(1/4) sum X_t^2 + P] dt
  P = (1/8) Int_{-1}^1 (1-u^2) f_u^2 / f du
  EL: X_tt - X_t = 2 P_X ; p_l = e^{-t} X_t / 2
  weld jet X=(1,0,0,0), X_t=(gamma,-c,0,0)
  ABSOLUTE f_min classifier, stop at f_min = fstop
  t_seal* = t_stop + mu/|mu_t| (linear layer extrapolation)
  D = (1/2) ln F_seal ; M0 = (y/2)(1-F); m_pole = (y/2)(1-f(u=1))
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

S3, S5, S7 = np.sqrt(3.0), np.sqrt(5.0), np.sqrt(7.0)
Y1P = np.array([1.0, S3, S5, S7])              # Y_l(u=+1)
Y1PP = np.array([0.0, S3, 3.0*S5, 6.0*S7])     # Y_l'(u=+1)

class Quad:
    def __init__(self, n=3200):
        x, w = np.polynomial.legendre.leggauss(n)
        self.u, self.w = x, w
        self.Y = np.vstack([np.ones_like(x), S3*x, (S5/2)*(3*x*x - 1),
                            (S7/2)*(5*x**3 - 3*x)])           # (4,n)
        self.Yp = np.vstack([np.zeros_like(x), S3*np.ones_like(x),
                             3*S5*x, (S7/2)*(15*x*x - 3)])
        self.one_m_u2 = 1.0 - x*x

def P_and_grad(X, q):
    f = X @ q.Y                      # (n,)
    fu = X @ q.Yp
    base = q.one_m_u2 * q.w / 8.0
    P = np.dot(base, fu*fu/f)
    gP = q.Yp @ (base * 2*fu/f) - q.Y @ (base * fu*fu/(f*f))
    return P, gP

def fmin_closed(X):
    """min over u in [-1,1] of cubic f(u); closed-form critical points."""
    # f_u = S3 X1 + 3 S5 X2 u + (S7/2)(15 u^2 - 3) X3
    a = 7.5*S7*X[3]; b = 3.0*S5*X[2]; c = S3*X[1] - 1.5*S7*X[3]
    cands = [-1.0, 1.0]
    if abs(a) > 1e-300:
        disc = b*b - 4*a*c
        if disc >= 0.0:
            sq = np.sqrt(disc)
            for r in ((-b+sq)/(2*a), (-b-sq)/(2*a)):
                if -1.0 < r < 1.0:
                    cands.append(r)
    elif abs(b) > 1e-300:
        r = -c/b
        if -1.0 < r < 1.0:
            cands.append(r)
    def fval(u):
        return (X[0] + S3*X[1]*u + (S5/2)*X[2]*(3*u*u-1)
                + (S7/2)*X[3]*(5*u**3-3*u))
    vals = [fval(u) for u in cands]
    i = int(np.argmin(vals))
    return vals[i], cands[i]

def rhs_full(t, z, q):
    """state: X(4), Xt(4), Akin_l(4), Apot, dp_l(4) = 17 components."""
    X, Xt = z[0:4], z[4:8]
    P, gP = P_and_grad(X, q)
    e = np.exp(-t)
    dz = np.empty(17)
    dz[0:4] = Xt
    dz[4:8] = Xt + 2.0*gP
    dz[8:12] = e*0.25*Xt*Xt
    dz[12] = e*P
    dz[13:17] = e*gP
    return dz

def run_flow(gamma, c, fstop=0.002, q=None, Tmax=120.0, rtol=1e-12,
             atol=1e-14, max_step=0.04):
    if q is None:
        q = QDEF
    z0 = np.zeros(17); z0[0] = 1.0; z0[4] = gamma; z0[5] = -c
    def ev(t, z, *a):
        return fmin_closed(z[0:4])[0] - fstop
    ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs_full, (0.0, Tmax), z0, args=(q,), method='DOP853',
                    rtol=rtol, atol=atol, events=ev, dense_output=True,
                    max_step=max_step)
    sealed = len(sol.t_events[0]) > 0
    return sol, sealed

def seal_only_run(gamma, c, fstop, Tmax=120.0, q=None):
    """cheap classifier run (no quadrature states) for c* bisection."""
    if q is None:
        q = QCHEAP
    z0 = np.zeros(8); z0[0] = 1.0; z0[4] = gamma; z0[5] = -c
    def rhs(t, z):
        X, Xt = z[0:4], z[4:8]
        _, gP = P_and_grad(X, q)
        return np.concatenate([Xt, Xt + 2.0*gP])
    def ev(t, z):
        return fmin_closed(z[0:4])[0] - fstop
    ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs, (0.0, Tmax), z0, method='DOP853', rtol=1e-11,
                    atol=1e-13, events=ev, max_step=0.05)
    return len(sol.t_events[0]) > 0

def cstar(gamma, lo, hi, fstop=0.02, xtol=1e-9):
    g = lambda c: 1.0 if seal_only_run(gamma, c, fstop) else -1.0
    assert g(lo) < 0 and g(hi) > 0
    return brentq(g, lo, hi, xtol=xtol)

def measure(gamma, c, fstop=0.002, q=None, label=""):
    sol, sealed = run_flow(gamma, c, fstop=fstop, q=q)
    assert sealed, f"{label}: did not seal"
    t_stop = sol.t_events[0][0]
    z = sol.y_events[0][0]
    X, Xt = z[0:4], z[4:8]
    mu, umin = fmin_closed(X)
    mu_t = float(Xt @ Y1P) if umin > 0.999 else np.nan  # envelope: df_min/dt
    t_seal = t_stop + mu/abs(mu_t)
    y_seal = np.exp(-t_seal)
    ys = np.exp(-t_stop)
    A_kin_l = z[8:12]; A_pot = z[12]; A_tot = A_kin_l.sum() + A_pot
    dp_int = z[13:17]
    p_stop = 0.5*ys*Xt
    p_weld = np.array([gamma/2, -c/2, 0.0, 0.0])
    dp_dir = p_stop - p_weld
    F_seal = X[0]; D = 0.5*np.log(F_seal)
    M0_seal = 0.5*ys*(1.0 - F_seal)
    fpole = float(X @ Y1P)
    m_pole = 0.5*ys*(1.0 - fpole)
    fu_pole = float(X @ Y1PP)
    fK_lim = 2.0*fu_pole**2/ys**4
    qq = q if q is not None else QDEF
    P_stop, _ = P_and_grad(X, qq)
    E_seal = 0.25*(Xt*Xt).sum() - P_stop
    E0 = 0.25*(gamma*gamma + c*c)
    # virial: A =? [ (1/2) X.p ]_0^stop + (1/2) Int e^-t P
    bnd_stop = 0.5*float(X @ p_stop)
    bnd_weld = 0.5*(1.0*gamma/2)
    A_vir = (bnd_stop - bnd_weld) + 0.5*A_pot
    return dict(label=label, gamma=gamma, c=c, fstop=fstop, sol=sol,
                t_stop=t_stop, t_seal=t_seal, y_seal=y_seal, mu=mu,
                mu_t=mu_t, umin=umin, A_tot=A_tot, A_kin=A_kin_l.sum(),
                A_pot=A_pot, A_kin_l=A_kin_l, dp_int=dp_int,
                dp_dir=dp_dir, p_weld=p_weld, p_seal=p_stop,
                F_seal=F_seal, D=D, M0_seal=M0_seal, m_pole_seal=m_pole,
                fK_lim=fK_lim, E0=E0, E_seal=E_seal, A_vir=A_vir,
                bnd_weld=bnd_weld)

QDEF = Quad(3200)
QCHEAP = Quad(900)
QHI = Quad(6400)
