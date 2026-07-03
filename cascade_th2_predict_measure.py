"""th2: assembled second-order theta_0 prediction vs direct measurement, per rung.
theta_0(N,Z,fam) = z*_eff(gamma) [self-consistent bottom system]
                 + Sum P        [exact frozen-Phi quadrature along leading flux law]
Analytic cross-check: Sum P ~ kappa_E * Z(1-xc)^2/(3 Theta) + (N+1) pi (3 c3h/2) dh,
kappa_E = 2 + 15 c3h^2/16 - 3 c3h/2 + 3 c4h/4  (CAS, th2_cas_kappa.py).
Inputs: banked d*/a* pins (rung identity), family U (CHOSE, banked), x_c (pin). NO FITS.
"""
import json, sys
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, make_risefall_slice
from cascade_stageC_lib import make_A2_slice, make_A3_slice

XC = 1.0/1101.0
BASE = "/home/udt-admin/udt_mass_codex/"
SHOTS = [0]

# ---------------- family symbolic constants (exact at given param)
rho = sp.Symbol('rho', positive=True)
def fam_constants(kind, par):
    if kind.startswith("A1m"):
        m = float(kind[3:]); Uexpr = 2*rho**m*sp.exp(-par*(rho**2-1))
    elif kind == "A2k3":
        Uexpr = 2*rho**2*sp.exp(-par*(rho**3-1))
    elif kind == "A3":
        Uexpr = 2*rho**2*(1+par)/(1+par*rho**4)
    ders = [float(sp.diff(Uexpr, rho, n).subs(rho, 1)) for n in (1,2,3,4)]
    dt = ders[0]/4.0; s1 = -ders[1]/4.0
    c3h = ders[2]/(12.0*s1); c4h = ders[3]/(48.0*s1)
    return dt, s1, c3h, c4h

def make_slice(kind, par):
    if kind.startswith("A1m"): return make_risefall_slice(par, m=float(kind[3:]))
    if kind == "A2k3": return make_A2_slice(par, k=3.0)
    if kind == "A3":  return make_A3_slice(par)

# ---------------- bottom system: z*_eff(gamma), z_c_eff(gamma)
def bottom(gamma, zmax=120.0):
    f = lambda z, y: [y[1], y[3]*y[1]-y[0]+1.0, y[3], gamma*np.exp(-2*y[2])*y[1]**2-y[3]**2]
    s = solve_ivp(f, (0.0, zmax), [0.,0.,0.,0.], rtol=1e-11, atol=1e-13, dense_output=True)
    zz = np.linspace(1e-3, zmax, 300001)
    vz = s.sol(zz)[1]
    idx = np.where(np.sign(vz[:-1])*np.sign(vz[1:]) < 0)[0]
    nodes = np.array([brentq(lambda z: s.sol(z)[1], zz[i], zz[i+1], xtol=1e-12) for i in idx])
    lad = np.mod(nodes, np.pi)
    mask = zz > 0.75*zmax
    psi = s.sol(zz[mask])[2]
    zc_eff = float(np.sqrt(np.mean(zz[mask]**2/np.exp(psi))))
    # ladder convergence: mid-window vs late-window
    mid = lad[(nodes>20)&(nodes<32)]
    return float(np.mean(lad[-6:])), zc_eff, float(np.mean(mid)) if len(mid) else np.nan, nodes[0]

# ---------------- exact per-cycle quadrature (as th2_nodewise)
x_g, w_g = np.polynomial.legendre.leggauss(240)
TH, TW = 0.5*np.pi*x_g, 0.5*np.pi*w_g
from scipy.optimize import minimize_scalar
def P_excess(Phi, Z, U, s1):
    Wf = lambda rr_: Phi*Phi/(2.0*Z*rr_*rr_) + U(rr_) - 2.0
    mres = minimize_scalar(lambda rr_: -Wf(rr_), bounds=(0.3, 3.0), method='bounded')
    r0 = mres.x
    if Wf(r0) <= 0: return 0.0
    lo, hi = r0, r0
    while Wf(lo) > 0 and lo > 0.15: lo -= 0.02
    while Wf(hi) > 0 and hi < 6.0: hi += 0.02
    rm = brentq(Wf, lo, r0, xtol=1e-14); rp = brentq(Wf, r0, hi, xtol=1e-14)
    c, A = 0.5*(rp+rm), 0.5*(rp-rm)
    rt = c + A*np.sin(TH)
    h = Wf(rt)/(A*A*np.cos(TH)**2)
    Qt = s1 + Phi*Phi/(4.0*Z*rt**4)
    return float(np.sum(np.sqrt(2.0*Qt/h)*TW) - np.pi)

def sumP_quad(Z, U, s1, Theta, n_t=48):
    """int P dn over the slow flow: x = xc + t^2, t in (0, sqrt(1-xc));
       Phi(x) = 2 Z sqrt(s1) sqrt((1-xc)(x-xc))/Theta ; dn = Z sqrt(Qbar)/(pi Phi) dx."""
    tmax = np.sqrt(1.0-XC)
    xt, wt = np.polynomial.legendre.leggauss(n_t)
    t = 0.5*tmax*(xt+1.0); wts = 0.5*tmax*wt
    tot = 0.0
    for ti, wi in zip(t, wts):
        Phi = 2.0*Z*np.sqrt(s1)*np.sqrt(1.0-XC)*ti/Theta
        Qb = s1 + Phi*Phi/(4.0*Z)
        dn_dx = Z*np.sqrt(Qb)/(np.pi*Phi)
        tot += P_excess(Phi, Z, U, s1)*dn_dx*2.0*ti*wi
    return tot   # radians: sum P = int P(Phi) dn  (dn = half-cycle count measure)

def measure(Z, kind, par, N):
    U, Up, lab = make_slice(kind, par)
    seal = lambda r, y, *a: y[0]; seal.terminal, seal.direction = True, +1
    sol = solve_ivp(rhs, (0.0, 5.0e7), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                    method="LSODA", rtol=1e-10, atol=1e-12, events=[seal], dense_output=True)
    SHOTS[0] += 1
    r_s = sol.t_events[0][0]
    rr = np.linspace(0.0, r_s, 400001)
    phi, phip, rho_, rhop = sol.sol(rr)
    _, s1, _, _ = None, None, None, None
    return sol, r_s, rr, phi, phip, rho_, rhop

RUNGS = []
sb = json.load(open(BASE+"cascade_stageB_rungs.json"))
for N in (8, 10, 13, 14, 18, 22):
    a_star = [r['a_star'] for r in sb['rungs'] if r['N_delta'] == N][0]
    RUNGS.append(dict(tag=f"B_m3_Z8_N{N}", Z=8.0, kind="A1m3", par=a_star, N=N))
for cf, kind, Z, stuck in (("c2_A1m3_Z1","A1m3",1.0,1.5), ("c1_A1m2_Z8","A1m2",8.0,1.0),
                           ("c5_A1m4_Z8","A1m4",8.0,2.0), ("c3_A2k3_Z8","A2k3",8.0,2.0/3.0),
                           ("c4_A3_Z8","A3",8.0,1.0)):
    d = json.load(open(BASE+f"cascade_stageC_{cf}.json"))
    ds = [r['d_star'] for r in d['rungs'] if r['N_delta'] == 8][0]
    RUNGS.append(dict(tag=f"{cf}_N8", Z=Z, kind=kind, par=stuck*(1.0-ds), N=8))

print(f"{'rung':>18}{'gamma':>8}{'z*eff/pi':>10}{'SP_q/pi':>9}{'SP_an/pi':>10}"
      f"{'th0_pred/pi':>12}{'th0_meas/pi':>12}{'diff/pi':>9}{'zc_eff':>8}{'zc_req':>8}")
results = []
for R in RUNGS:
    Z, kind, par, N = R['Z'], R['kind'], R['par'], R['N']
    dt, s1, c3h, c4h = fam_constants(kind, par)
    gamma = 4.0*dt*dt/(Z*s1*s1*XC*XC)
    zstar, zc_eff, zstar_mid, first = bottom(gamma)
    U, Upf, lab = make_slice(kind, par)
    kappaE = 2.0 + 15.0*c3h*c3h/16.0 - 1.5*c3h + 0.75*c4h
    # self-consistent Theta
    th0 = zstar
    for _ in range(4):
        Theta = (N+1)*np.pi + th0
        SP_q = sumP_quad(Z, U, s1, Theta)
        SP_an = kappaE*Z*(1.0-XC)**2/(3.0*Theta) + (N+1)*np.pi*1.5*c3h*(dt/s1)
        th0 = zstar + SP_q
    # measure
    sol, r_s, rr, phi, phip, rho_, rhop = measure(Z, kind, par, N)
    Q = s1 + 0.25*Z*phip**2
    Theta_m = np.trapezoid(np.exp(phi)*np.sqrt(Q), rr)
    th0_m = Theta_m - (N+1)*np.pi
    zc_req = Theta_m*np.sqrt(XC)/np.sqrt(1.0-XC)
    print(f"{R['tag']:>18}{gamma:>8.3f}{zstar/np.pi:>10.4f}{SP_q/np.pi:>9.4f}{SP_an/np.pi:>10.4f}"
          f"{th0/np.pi:>12.4f}{th0_m/np.pi:>12.4f}{(th0-th0_m)/np.pi:>9.4f}{zc_eff:>8.4f}{zc_req:>8.4f}")
    results.append(dict(R, gamma=gamma, zstar=zstar, SP_q=SP_q, SP_an=SP_an,
                        th0_pred=th0, th0_meas=th0_m, kappaE=kappaE, dt=dt, s1=s1,
                        c3h=c3h, c4h=c4h, zc_eff=zc_eff, zc_req=zc_req, rho_s=float(rho_[-1])))
print(f"shots: {SHOTS[0]}")
json.dump(results, open("th2_results.json","w"), indent=1, default=float)
