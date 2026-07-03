"""tw_reshoot.py -- 4 bounded re-shoots at BANKED rung parameters (N=8,9 x below/above):
direct measurement of Theta, theta0, node ladder, ramp fraction, seal data, per side.
Adjudicates the theta0-odd twin flip (off-channel) vs the closure-implied sign.
Shots: 4 (single process, CPU, bounded).
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.optimize import brentq
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, make_risefall_slice

M, Z = 3.0, 8.0
XC = 1.0/1101.0

cases = [
    ("B_N8", 1.4941244349239216, 8),
    ("A_N8", 1.50587703866,      8),
    ("B_N9", 1.4944556048040025, 9),
    ("A_N9", 1.50556166549,      9),
]

for tag, a_param, N in cases:
    U, Up, lab = make_risefall_slice(a_param, m=M)
    seal = lambda r, y, *aa: y[0]
    seal.terminal, seal.direction = True, +1
    sol = solve_ivp(rhs, (0.0, 5.0e7), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                    method="LSODA", rtol=1e-10, atol=1e-12, events=[seal], dense_output=True)
    if not sol.t_events[0].size:
        print(f"{tag}: NO SEAL (status {sol.status})"); continue
    r_s = sol.t_events[0][0]
    rr = np.linspace(0.0, r_s, 800001)
    phi, phip, rho, rhop = sol.sol(rr)
    dt = Up(1.0)/4.0
    g1, gp1 = M - 2*a_param, -M - 2*a_param
    s1_abs = -0.5*(g1*g1 + gp1)
    Q = s1_abs + 0.25*Z*phip**2
    k = np.exp(phi)*np.sqrt(Q)
    zeta = np.concatenate([[0.0], cumulative_trapezoid(k, rr)])
    Theta = zeta[-1]
    theta0 = Theta/np.pi - (N + 1)
    L = float(np.trapezoid(np.exp(phi), rr))
    q = Z*rho[-1]**2*phip[-1]
    # rho'-nodes and their phase positions
    sgn = np.sign(rhop)
    idx = np.where(sgn[:-1]*sgn[1:] < 0)[0]
    nodes = np.array([brentq(lambda r: sol.sol(r)[3], rr[i], rr[i+1], xtol=1e-13*r_s) for i in idx])
    node_phase = np.interp(nodes, rr, zeta)/np.pi
    gaps = np.diff(np.concatenate([node_phase, [Theta/np.pi]]))
    # ramp end ~ first node; ramp fraction of L
    if nodes.size:
        i_ramp = np.searchsorted(rr, nodes[0])
        L_ramp = float(np.trapezoid(np.exp(phi[:i_ramp]), rr[:i_ramp]))
    else:
        L_ramp = np.nan
    print(f"{tag}: a={a_param:.10f} dt={dt:+.7e} |s1|={s1_abs:.6f}")
    print(f"   r_s={r_s:.3f} rho_s={rho[-1]:.7f} q={q:.7f} L={L:.5f} (banked-side check)")
    print(f"   Theta={Theta:.6f} = {Theta/np.pi:.6f} pi ; theta0={theta0:+.6f} pi ; nodes={len(nodes)}")
    print(f"   first-node phase={node_phase[0] if nodes.size else np.nan:.4f} pi ; "
          f"L_ramp={L_ramp:.4f} ({100*L_ramp/L:.2f}% of L)")
    print(f"   node-gap ladder (pi units, last 6): {np.array2string(gaps[-6:], precision=4)}")
    print(f"   off-term prediction this side: (N+1)*1.5*chat3*dt/|s1| = "
          f"{(N+1)*1.5*((16*dt**3+24*dt**2-24*dt*M+4*M)/(12*s1_abs))*dt/s1_abs:+.6f} pi")
    print()
