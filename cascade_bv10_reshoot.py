"""bv10_reshoot.py -- direct theta0 measurement on re-shot rungs (my own pipeline).
Shots: stageB Z8 m3 N=8; c5 Z8 m4 N=8; c1 Z8 m2 N=8; stageB Z8 m3 N=22.  (4 IVP shots)
For each: Theta = int e^phi sqrt((Z/4)phi'^2 - s1) dr;  theta0 = Theta - (N+1)pi;
W(node) residuals; per-node-interval phase excesses (handover probe).
"""
import sys
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import make_risefall_slice
from cascade_stageC_lib import shoot_g
import sympy as sp

XC = 1.0/1101.0
SHOTS = 0

def U_derivs_m(m, a):
    """Exact U-derivatives at rho=1 for U = 2 rho^m exp(-a(rho^2-1)) via sympy."""
    rho = sp.symbols('rho', positive=True)
    U = 2*rho**m*sp.exp(-a*(rho**2 - 1))
    d = [float(sp.diff(U, rho, k).subs(rho, 1)) for k in range(5)]
    return d  # [U, U', U'', U''', U'''']

def measure(Z, m, d_star, label, npts=800001):
    global SHOTS
    a = (m/2.0)*(1.0 - d_star)
    U, Up, _ = make_risefall_slice(a, m=float(m))
    o = shoot_g(Z, Up)                     # 1 IVP shot
    SHOTS += 1
    assert o["status"] == "seal", o["status"]
    r_s = o["r_s"]
    rr = np.linspace(0.0, r_s, npts)
    phi, phip, rho, rhop = o["sol"].sol(rr)
    dU = U_derivs_m(m, a)
    s1 = dU[2]/4.0                          # < 0
    dt = dU[1]/4.0
    c3 = dU[3]/(12.0*abs(s1))
    c4 = dU[4]/(48.0*abs(s1))
    Q = (Z/4.0)*phip**2 - s1
    k = np.exp(phi)*np.sqrt(Q)
    Theta = np.trapezoid(k, rr)
    # cumulative phase for per-interval excess
    cumTheta = np.concatenate([[0.0], np.cumsum(0.5*(k[1:]+k[:-1])*np.diff(rr))])
    # interior rho'-nodes: sign changes with graded floor
    s = rhop[1:-1]
    fl = 0.01*np.max(np.abs(s))
    mask = np.abs(s) > fl
    sgn = np.sign(s[mask]); idx = np.where(mask)[0]
    changes = [(idx[i], idx[i+1]) for i in range(len(sgn)-1) if sgn[i]*sgn[i+1] < 0]
    nodes_r, nodes_T, nodes_rho, nodes_W = [], [], [], []
    Phi_ = Z*rho**2*phip
    for i0, i1 in changes:
        # refine node by linear interp on rhop between grid points
        j0, j1 = i0+1, i1+1
        # bisect on dense sol
        aa, bb = rr[j0], rr[j1]
        fa = o["sol"].sol(aa)[3]
        for _ in range(60):
            mm = 0.5*(aa+bb); fm = o["sol"].sol(mm)[3]
            if fa*fm <= 0: bb = mm
            else: aa, fa = mm, fa*0+fm
        rn = 0.5*(aa+bb)
        ph, php, rh, rhp = o["sol"].sol(rn)
        PHI = Z*rh**2*php
        Wn = PHI**2/(2.0*Z*rh**2) + U(rh) - 2.0
        Tn = np.interp(rn, rr, cumTheta)
        nodes_r.append(rn); nodes_T.append(Tn); nodes_rho.append(rh); nodes_W.append(Wn)
    N = len(nodes_r)
    theta0 = Theta - (N+1)*np.pi
    print(f"=== {label}: Z={Z} m={m} d*={d_star:.9f} a*={a:.9f} ===")
    print(f"  s1={s1:.6f} dt={dt:.6e} c3={c3:.6f} c4={c4:.6f}")
    print(f"  r_s={r_s:.4f} rho_s={o['rho_s']:.6f} (banked cross-check)")
    print(f"  N(interior rho'-nodes)={N}   Theta={Theta:.6f} = {Theta/np.pi:.6f} pi")
    print(f"  theta0 = {theta0/np.pi:+.5f} pi")
    print(f"  max|W(node)| = {np.max(np.abs(nodes_W)):.3e}   (== H-drift tautology check)")
    # per-interval excesses (including seal as final node)
    nodes_T_full = nodes_T + [Theta]
    exc = np.diff([0.0]+nodes_T_full) - np.pi   # first = launch-to-first-node
    print(f"  per-interval (node-to-node) phase excess / pi:")
    print("   ", np.round(np.array(exc)/np.pi, 5))
    # E_n at each node from flux law position: E = Phi^2/(4 Z |s1|) measured directly
    En = []
    for rn in nodes_r:
        ph, php, rh, rhp = o["sol"].sol(rn)
        PHI = Z*rh**2*php
        En.append(PHI**2/(4.0*Z*abs(s1)))
    print(f"  E_n at nodes: ", np.round(np.array(En), 6))
    return dict(label=label, Z=Z, m=m, d=d_star, a=a, s1=s1, dt=dt, c3=c3, c4=c4,
                N=N, Theta=Theta, theta0=theta0, exc=exc, En=En, r_s=r_s)

if __name__ == "__main__":
    res = []
    res.append(measure(8.0, 3, 0.003917043, "stageB Z8 m3 N=8"))
    res.append(measure(8.0, 4, 0.003914956, "c5 Z8 m4 N=8"))
    res.append(measure(8.0, 2, 0.003919133, "c1 Z8 m2 N=8"))
    res.append(measure(8.0, 3, 0.002128889, "stageB Z8 m3 N=22", npts=1600001))
    print(f"\nTOTAL IVP SHOTS: {SHOTS}")
    np.save("bv10_reshoot_results.npy", res, allow_pickle=True)
