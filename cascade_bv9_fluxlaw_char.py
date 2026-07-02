"""bv9_fluxlaw_char.py -- characterize the Phi^2/(e^phi - x_c) ratio along the banked rung:
instantaneous vs at-rho'-nodes vs cycle-averaged; where the deviations live (ramp vs tail).
One additional IVP shot (dense).
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, make_risefall_slice

Z, M, ASTAR = 8.0, 3.0, 1.4941244349
XC = np.exp(PHI_C)
S1 = (8*ASTAR**2 - 8*ASTAR*M - 4*ASTAR + 2*M*M - 2*M)/4.0
U, Up, _ = make_risefall_slice(ASTAR, m=M)

seal = lambda r, y, *a: y[0]
seal.terminal, seal.direction = True, +1
sol = solve_ivp(rhs, (0.0, 5.0e3), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                method="LSODA", rtol=1e-11, atol=1e-13, dense_output=True, events=[seal])
r_s = float(sol.t_events[0][0])
rr = np.linspace(0.0, r_s, 400001)
phi, phip, rho, rhop = sol.sol(rr)
q = Z*sol.y_events[0][0][2]**2*sol.y_events[0][0][1]

Qfull = (Z/4.0)*phip**2 - S1
kfull = np.exp(phi)*np.sqrt(Qfull)
zeta = np.concatenate([[0.0], np.cumsum(0.5*(kfull[1:]+kfull[:-1])*np.diff(rr))])
Theta = zeta[-1]

Phi = Z*rho**2*phip
x = np.exp(phi)
ratio = np.where(x-XC > 0, Phi**2/(x-XC), np.nan)

# C from q (the D3 route): q = 2 C sqrt(Z) |s1|^{1/4} sqrt(1-xc)
C_q = q/(2*np.sqrt(Z)*(-S1)**0.25*np.sqrt(1-XC))
const_pred = 4*Z*C_q**2*np.sqrt(-S1)
print(f"q = {q:.8f};  C(from q) = {C_q:.6f};  predicted flux-law const 4ZC^2 sqrt|s1| = {const_pred:.6f}")
print(f"ratio at seal = q^2/(1-x_c) = {q*q/(1-XC):.6f} (same thing, tautology check)")
Th_pred = np.sqrt(Z)*(-S1)**0.25*np.sqrt(1-XC)/C_q
print(f"D2 with C(q): Theta_pred = {Th_pred/np.pi:.4f} pi vs measured {Theta/np.pi:.4f} pi "
      f"({100*(Th_pred/Theta-1):+.2f}%)")

# rho'-nodes
s = np.sign(rhop)
idx = np.nonzero(s[1:]*s[:-1] < 0)[0]
idx = [i for i in idx if zeta[i] > 1e-3]
print("\nratio at rho'-nodes (and seal), normalized by predicted const:")
for i in idx:
    print(f"  zeta = {zeta[i]/np.pi:7.4f} pi   ratio = {ratio[i]:.6f}   ratio/pred = {ratio[i]/const_pred:.4f}")
print(f"  zeta = {Theta/np.pi:7.4f} pi   ratio = {q*q/(1-XC):.6f}   ratio/pred = {(q*q/(1-XC))/const_pred:.4f}  [seal]")

# cycle-averaged ratio: average Phi^2 and (e^phi - xc) over each pi-window in zeta
print("\ncycle-window (pi-bins in zeta) <Phi^2>/<e^phi - x_c>, /pred:")
edges = np.arange(0.0, Theta + 1e-9, np.pi)
for j in range(len(edges)-1):
    m_ = (zeta >= edges[j]) & (zeta < edges[j+1])
    if m_.sum() < 10: continue
    num = np.trapezoid(Phi[m_]**2, zeta[m_])
    den = np.trapezoid(x[m_]-XC, zeta[m_])
    print(f"  bin [{edges[j]/np.pi:.0f},{edges[j+1]/np.pi:.0f}]pi: <ratio> = {num/den:.6f}  /pred = {num/den/const_pred:.4f}")

# where are the instantaneous extremes? report ratio stats vs zeta quartile
print("\ninstantaneous ratio stats by zeta quartile:")
for j in range(4):
    m_ = (zeta >= Theta*j/4) & (zeta < Theta*(j+1)/4) & np.isfinite(ratio)
    rq = ratio[m_]
    print(f"  zeta in [{j}/4,{(j+1)/4}] Theta: min = {rq.min():.4f} max = {rq.max():.4f} "
          f"mean = {rq.mean():.4f}")

# linear fit Phi^2 vs (x - xc), r-uniform and zeta-uniform
A = np.vstack([x-XC, np.ones_like(x)]).T
coef, res, *_ = np.linalg.lstsq(A, Phi**2, rcond=None)
print(f"\nlstsq (r-uniform samples): slope = {coef[0]:.6f} (pred {const_pred:.6f}), intercept = {coef[1]:.2e}")
print("\nSHOT LEDGER: 1 IVP shot this script (cumulative 3)")
