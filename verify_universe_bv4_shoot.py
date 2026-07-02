"""bv4_shoot.py -- BLIND-VERIFIER independent shooter for the universe-cell 1-D problem.

Built from banked equations only:
  phi'' = 4 e^{-2phi} rho'^2/(Z rho^2) - 2 phi' rho'/rho
  rho'' = 2 phi' rho' - (Z/4) rho e^{2phi} phi'^2 + (e^{2phi}/4) U'(rho)
IC (even fold + anchor): phi(0)=-ln(1101), phi'(0)=0, rho(0)=rho_c, rho'(0)=0.
Target (odd fold): rho'(r_s)=0 at FIRST phi=0 upcrossing.
H = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 + U(rho) == const (=0 iff U(rho_c)=2).

Integrator: scipy DOP853 (NOT LSODA), with Radau and hand-rolled RK4 cross-checks.
"""
import numpy as np
from scipy.integrate import solve_ivp

PHI_C = -np.log(1101.0)

# ---------------- slice families (definitions extracted from cell_solver_universe_T3.py) ---
def make_power_slice(n, rho_c=1.0):
    def U(rho):  return 2.0 * (rho / rho_c) ** n
    def Up(rho): return 2.0 * n * rho ** (n - 1.0) / rho_c ** n
    return U, Up, f"power n={n:+.4f}"

def make_risefall_slice(a, m=2.0, rho_c=1.0):
    def U(rho):
        x = rho / rho_c
        return 2.0 * x ** m * np.exp(-a * (x * x - 1.0))
    def Up(rho):
        x = rho / rho_c
        return (2.0 * x ** m * np.exp(-a * (x * x - 1.0))) * (m / x - 2.0 * a * x) / rho_c
    return U, Up, f"risefall m={m} a={a:+.6f}"

# ---------------- my RHS -------------------------------------------------------------------
def rhs(r, y, Z, Up):
    phi, phip, rho, rhop = y
    e2 = np.exp(2.0 * phi)
    phipp = 4.0 * rhop * rhop / (e2 * Z * rho * rho) - 2.0 * phip * rhop / rho
    rhopp = 2.0 * phip * rhop - 0.25 * Z * rho * e2 * phip * phip + 0.25 * e2 * Up(rho)
    return (phip, phipp, rhop, rhopp)

def Hfun(y, Z, U):
    phi, phip, rho, rhop = y
    return 0.5 * Z * rho * rho * phip * phip - 2.0 * np.exp(-2.0 * phi) * rhop * rhop \
           - 2.0 + U(rho)

# ---------------- shooter ------------------------------------------------------------------
def shoot(U, Up, Z, rho_c=1.0, phi_c=PHI_C, r_max=5000.0, rtol=1e-11, atol=1e-13,
          method='DOP853'):
    """Integrate from the even fold; stop at first phi=0 UPcrossing or rho collapse/blowup.
    Returns dict: status in {'seal','collapse','blowup','rmax'}, r_s, y_s, miss=rho'(r_s),
    Hdrift = max |H - H0| over ~400 dense samples."""
    y0 = [phi_c, 0.0, rho_c, 0.0]

    def ev_phi0(r, y, *a):  return y[0]
    ev_phi0.terminal, ev_phi0.direction = True, +1.0
    def ev_coll(r, y, *a):  return y[2] - 1e-8 * rho_c
    ev_coll.terminal, ev_coll.direction = True, -1.0
    def ev_blow(r, y, *a):  return y[2] - 1e6 * rho_c
    ev_blow.terminal, ev_blow.direction = True, +1.0

    sol = solve_ivp(rhs, (0.0, r_max), y0, args=(Z, Up), method=method,
                    rtol=rtol, atol=atol, dense_output=True,
                    events=(ev_phi0, ev_coll, ev_blow))
    # H drift over dense samples
    rr = np.linspace(0.0, sol.t[-1], 401)
    H0 = Hfun(np.asarray(y0), Z, U)
    Hd = max(abs(Hfun(sol.sol(r), Z, U) - H0) for r in rr)
    out = dict(Hdrift=Hd, H0=H0, r_end=sol.t[-1], y_end=sol.y[:, -1], sol=sol)
    if sol.t_events[0].size:
        rs = sol.t_events[0][0]; ys = sol.y_events[0][0]
        out.update(status='seal', r_s=rs, y_s=ys, miss=ys[3])
    elif sol.t_events[1].size:
        out.update(status='collapse', r_s=sol.t_events[1][0], y_s=sol.y_events[1][0],
                   miss=np.nan)
    elif sol.t_events[2].size:
        out.update(status='blowup', r_s=sol.t_events[2][0], y_s=sol.y_events[2][0],
                   miss=np.nan)
    else:
        out.update(status='rmax', r_s=np.nan, y_s=sol.y[:, -1], miss=np.nan)
    return out

# ---------------- hand-rolled fixed-step RK4 (fully independent spot check) ---------------
def rk4_shoot(U, Up, Z, rho_c=1.0, phi_c=PHI_C, r_max=5000.0, h=0.01):
    y = np.array([phi_c, 0.0, rho_c, 0.0])
    f = lambda r, y: np.asarray(rhs(r, y, Z, Up))
    r = 0.0
    while r < r_max:
        yprev, rprev = y.copy(), r
        k1 = f(r, y); k2 = f(r + h/2, y + h/2*k1)
        k3 = f(r + h/2, y + h/2*k2); k4 = f(r + h, y + h*k3)
        y = y + (h/6)*(k1 + 2*k2 + 2*k3 + k4); r += h
        if y[2] < 1e-8:
            return dict(status='collapse', r_s=r, y_s=y, miss=np.nan)
        if yprev[0] < 0.0 <= y[0]:
            # bisect the crossing on the RK4 step for the seal state
            a, b, ya = rprev, r, yprev
            for _ in range(60):
                m = 0.5*(a+b); hm = m - a
                k1 = f(a, ya); k2 = f(a+hm/2, ya+hm/2*k1)
                k3 = f(a+hm/2, ya+hm/2*k2); k4 = f(a+hm, ya+hm*k3)
                ym = ya + (hm/6)*(k1+2*k2+2*k3+k4)
                if ym[0] < 0.0: a, ya = m, ym
                else: b = m
            return dict(status='seal', r_s=a, y_s=ya, miss=ya[3],
                        Hdrift=abs(Hfun(ya, Z, U) - Hfun(np.array([phi_c,0,rho_c,0]), Z, U)))
    return dict(status='rmax', r_s=np.nan, y_s=y, miss=np.nan)
