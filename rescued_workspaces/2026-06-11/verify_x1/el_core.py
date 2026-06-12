"""Blind verifier core: independent integrator for the reduced EL system.

System (per-solid-angle ell<=1 class), re-derived by me:
   (y^2 F')' = 2 P_F = -H(kappa),   H = L/(2k) - 1
   (y^2 a')' = 2 P_a,               P_a = sqrt(3)[L(1+k^2)-2k]/(8k^2)
   kappa = sqrt(3) a / F,  L = ln((1+k)/(1-k))

In t = ln(1/y) (interior of unit interface sphere, t >= 0, autonomous):
   F_tt = F_t - H(kappa)
   a_tt = a_t + 2 P_a(kappa)
Interface jet (momentum-only class): F(0)=1, F_t(0)=gamma, a(0)=0, a_t(0)=c.
(Check: a_t = da/dt = -y da/dy; a'(1) = -c  =>  a_t(0)=c.  F'(1) = -gamma => F_t(0)=gamma.)
"""
import numpy as np
from scipy.integrate import solve_ivp

SQ3 = np.sqrt(3.0)

def H_of_k(k):
    k = np.asarray(k, dtype=float)
    out = np.empty_like(k)
    small = np.abs(k) < 1e-4
    ks = k[small]
    out[small] = ks**2/3 + ks**4/5 + ks**6/7
    kb = k[~small]
    L = np.log((1+kb)/(1-kb))
    out[~small] = L/(2*kb) - 1
    return out

def Pa_of_k(k):
    k = np.asarray(k, dtype=float)
    out = np.empty_like(k)
    small = np.abs(k) < 1e-4
    ks = k[small]
    out[small] = SQ3*(ks/3 + 2*ks**3/15 + 3*ks**5/35)
    kb = k[~small]
    L = np.log((1+kb)/(1-kb))
    out[~small] = SQ3*(L*(1+kb**2) - 2*kb)/(8*kb**2)
    return out

def rhs(t, u):
    F, Ft, A, At = u
    k = SQ3*A/F
    if k >= 1.0:
        k = 1.0 - 1e-15
    if k <= -1.0:
        k = -1.0 + 1e-15
    H = float(H_of_k(np.array([k])))
    Pa = float(Pa_of_k(np.array([k])))
    return [Ft, Ft - H, At, At + 2*Pa]

KSEAL = 1.0 - 1e-9

def ev_seal(t, u):
    return SQ3*u[2]/u[0] - KSEAL
ev_seal.terminal = True
ev_seal.direction = 1

def ev_Fzero(t, u):
    return u[0] - 1e-12
ev_Fzero.terminal = True
ev_Fzero.direction = -1

def run_flow(gamma, c, Tmax=60.0, rtol=1e-11, atol=1e-13, dense=False,
             F0=1.0, a0=0.0, t_eval=None):
    u0 = [F0, gamma, a0, c]
    sol = solve_ivp(rhs, (0.0, Tmax), u0, method='LSODA',
                    events=[ev_seal, ev_Fzero], rtol=rtol, atol=atol,
                    dense_output=dense, t_eval=t_eval, max_step=1.0)
    sealed = len(sol.t_events[0]) > 0
    return sol, sealed

def classify(gamma, c, Tmax=60.0):
    """Return 'TERM' (kappa->1 at finite t) or 'SAT' (rides to Tmax)."""
    sol, sealed = run_flow(gamma, c, Tmax=Tmax)
    if sealed:
        return 'TERM', sol
    return 'SAT', sol

def threshold(gamma, clo, chi, tol_rel=2e-6, Tmax=60.0, verbose=False):
    """Bisect on c.  Requires classify(clo)=SAT, classify(chi)=TERM."""
    klo, _ = classify(gamma, clo, Tmax); khi, _ = classify(gamma, chi, Tmax)
    assert klo == 'SAT' and khi == 'TERM', (klo, khi, gamma, clo, chi)
    while (chi - clo) > tol_rel*chi:
        cm = 0.5*(clo + chi)
        km, _ = classify(gamma, cm, Tmax)
        if km == 'TERM':
            chi = cm
        else:
            clo = cm
        if verbose:
            print(f"  [{clo:.8f}, {chi:.8f}] {km}")
    return 0.5*(clo + chi)
