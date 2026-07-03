"""th2: node-wise phase decomposition of a rung + exact per-half-cycle quadrature prediction.

NEW-THIS-DERIVATION (exact reformulation, verified numerically here):
  H_tot = 0 (solver-exact)  =>  rho'^2 = (e^{2phi}/2) W(rho, Phi),
      W(rho,Phi) = Phi^2/(2 Z rho^2) + U(rho) - 2
  => rho'-nodes are EXACTLY the roots of W (Theorem B = seal is a turning point).
  In dtau = e^phi dr the half-cycle nominal phase (Theta-measure) is EXACTLY
      DTheta_half = int_{rho-}^{rho+} sqrt(2 Q(rho,Phi)) / sqrt(W(rho,Phi)) drho
  (frozen-Phi adiabatic; intra-cycle Phi-drift = flagged higher order),
  with Q(rho,Phi) = |s1| + Phi^2/(4 Z rho^4)  [the exact measurement Q].
  This contains ALL orders of: U''' / U'''' anharmonicity, rho^-2 backreaction,
  and the offset (asymmetric hump) -- task contributions 1+2+3 unified.
Per-half-cycle excess P(Phi) = DTheta_half - pi.  theta_0 = launch + sum P.
"""
import json, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, make_risefall_slice

XC = 1.0/1101.0

def gauss_theta(n=240):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.25*np.pi*(x+1.0)*2.0 - 0.5*np.pi, w*0.5*np.pi   # theta in (-pi/2, pi/2)
TH, TW = gauss_theta()

def P_excess(Phi, Z, U, s1_abs, rho_lo, rho_hi):
    """Exact frozen-Phi half-cycle phase minus pi. rho_lo/rho_hi: bracket guesses around roots."""
    Wf = lambda rho: Phi*Phi/(2.0*Z*rho*rho) + U(rho) - 2.0
    # bracket the two roots of W around the hump top
    # hump top:
    from scipy.optimize import minimize_scalar
    m = minimize_scalar(lambda rho: -Wf(rho), bounds=(rho_lo, rho_hi), method='bounded')
    r0 = m.x
    if Wf(r0) <= 0:  return np.nan, (np.nan, np.nan)
    # expand outward for sign change
    lo = r0
    step = max(1e-4, 0.1*(r0-rho_lo))
    while Wf(lo) > 0 and lo > rho_lo*0.5: lo -= step
    hi = r0
    step = max(1e-4, 0.1*(rho_hi-r0))
    while Wf(hi) > 0 and hi < rho_hi*2.0: hi += step
    rm = brentq(Wf, lo, r0, xtol=1e-14)
    rp = brentq(Wf, r0, hi, xtol=1e-14)
    c, A = 0.5*(rp+rm), 0.5*(rp-rm)
    rho_t = c + A*np.sin(TH)
    W_t = Wf(rho_t)
    h = W_t/(A*A*np.cos(TH)**2)          # smooth positive on open interval
    Q_t = s1_abs + Phi*Phi/(4.0*Z*rho_t**4)
    F = np.sqrt(2.0*Q_t/h)
    return float(np.sum(F*TW) - np.pi), (rm, rp)

def analyze(tag, Z, m, a_param, N, npts=800001):
    U, Up, lab = make_risefall_slice(a_param, m=m)
    seal = lambda r, y, *a: y[0]; seal.terminal, seal.direction = True, +1
    sol = solve_ivp(rhs, (0.0, 5.0e7), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                    method="LSODA", rtol=1e-10, atol=1e-12, events=[seal], dense_output=True)
    r_s = sol.t_events[0][0]
    rr = np.linspace(0.0, r_s, npts)
    phi, phip, rho, rhop = sol.sol(rr)
    g1, gp1 = m - 2*a_param, -m - 2*a_param
    s1_abs = -0.5*(g1*g1 + gp1)          # = -U''(1)/4, U''(1)=2(g^2+g')
    dt = Up(1.0)/4.0
    Q = s1_abs + 0.25*Z*phip**2
    k = np.exp(phi)*np.sqrt(Q)
    from scipy.integrate import cumulative_trapezoid
    zeta = np.concatenate([[0.0], cumulative_trapezoid(k, rr)])
    Theta = zeta[-1]
    theta0 = Theta/np.pi - (N+1)
    Phi_arr = Z*rho**2*phip
    print(f"===== {tag}: {lab} Z={Z} N={N}: r_s={r_s:.2f} rho_s={rho[-1]:.6f} "
          f"|s1|={s1_abs:.6f} dt={dt:.6e}")
    print(f"  Theta = {Theta/np.pi:.4f} pi ; theta0 = {theta0:.4f} pi")
    # ---- rho'-nodes (roots of rhop), refined
    sgn = np.sign(rhop)
    idx = np.where(sgn[:-1]*sgn[1:] < 0)[0]
    nodes = [brentq(lambda r: sol.sol(r)[3], rr[i], rr[i+1], xtol=1e-13*r_s) for i in idx]
    nodes = np.array(nodes)
    print(f"  n_nodes(interior)={len(nodes)}  + seal (rho'_s={rhop[-1]:.2e})")
    zeta_i = np.interp(nodes, rr, zeta)
    zeta_all = np.concatenate([zeta_i, [Theta]])
    r_all = np.concatenate([nodes, [r_s]])
    yA = sol.sol(r_all)
    Phi_n = Z*yA[2]**2*yA[1]
    rho_n = yA[2]
    # W at nodes must vanish (H=0 check)
    Wn = Phi_n**2/(2*Z*rho_n**2) + U(rho_n) - 2.0
    print(f"  H=0 check: max|W(node)| = {np.max(np.abs(Wn)):.2e}")
    print(f"  launch: zeta(first node) = {zeta_all[0]/np.pi:.4f} pi")
    print(f"  {'i':>3}{'dTheta/pi -1':>14}{'P_pred/pi':>12}{'Phi_mid':>10}{'a_orb':>9}{'rho- rho+':>20}")
    Psum = 0.0
    for i in range(len(zeta_all)-1):
        dTh = zeta_all[i+1]-zeta_all[i]
        zm = 0.5*(zeta_all[i]+zeta_all[i+1])
        r_mid = np.interp(zm, zeta, rr)
        ym = sol.sol(r_mid)
        Phi_mid = Z*ym[2]**2*ym[1]
        P, (rm_, rp_) = P_excess(Phi_mid, Z, U, s1_abs, 0.3, 3.0)
        Psum += P
        print(f"  {i:>3}{dTh/np.pi-1:>14.5f}{P/np.pi:>12.5f}{Phi_mid:>10.5f}{(rp_-rm_)/2:>9.5f}"
              f"   [{rm_:.5f},{rp_:.5f}]")
    launch = zeta_all[0] - len(nodes)*0.0  # raw
    resid = theta0*np.pi - (zeta_all[0] - np.pi*1.0) - Psum   # if first node ~ launch+1pi ladder
    print(f"  SUM P_pred = {Psum/np.pi:.4f} pi ; measured sum excess = {(Theta-zeta_all[0])/np.pi-(len(zeta_all)-1):.4f} pi")
    print(f"  decomposition: theta0 = [zeta_first - pi] + sum(dTheta-pi) = "
          f"{(zeta_all[0]/np.pi-1):.4f} + {(Theta-zeta_all[0])/np.pi-(len(zeta_all)-1):.4f} "
          f"= {theta0:.4f} (check)")
    return dict(theta0=theta0, zeta_first=zeta_all[0], Theta=Theta, N=N)

if __name__ == "__main__":
    d = json.load(open('/home/udt-admin/udt_mass_codex/cascade_stageB_rungs.json'))
    a8 = [r['a_star'] for r in d['rungs'] if r['N_delta'] == 8][0]
    analyze("stageB N=8", Z=8.0, m=3.0, a_param=a8, N=8)
