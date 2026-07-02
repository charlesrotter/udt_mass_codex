"""bv9_reshoot_Z1.py -- direct theta0 measurement for Z=1 (c2 = A1 m=3, N=8 rung,
p* = 1.4979093504148864). Claim to test: measured theta0 ~ 0.25 pi.
One IVP shot.
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, make_risefall_slice

Z, M, ASTAR = 1.0, 3.0, 1.4979093504148864
XC = np.exp(PHI_C)
S1 = (8*ASTAR**2 - 8*ASTAR*M - 4*ASTAR + 2*M*M - 2*M)/4.0
print(f"Z=1, a* = {ASTAR}, s~1(a*) = {S1:+.6f}")
U, Up, _ = make_risefall_slice(ASTAR, m=M)

seal = lambda r, y, *a: y[0]
seal.terminal, seal.direction = True, +1
sol = solve_ivp(rhs, (0.0, 5.0e3), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                method="LSODA", rtol=1e-11, atol=1e-13, dense_output=True, events=[seal])
r_s = float(sol.t_events[0][0])
phi_s, phip_s, rho_s, rhop_s = sol.y_events[0][0]
q = Z*rho_s**2*phip_s
print(f"re-shot: r_s={r_s:.4f}  rho_s={rho_s:.8f}  q={q:.8f}  (banked 1244.05, 1.03445802, 0.12010281)")

rr = np.linspace(0.0, r_s, 400001)
phi, phip, rho, rhop = sol.sol(rr)
Qfull = (Z/4.0)*phip**2 - S1
kfull = np.exp(phi)*np.sqrt(Qfull)
zeta = np.concatenate([[0.0], np.cumsum(0.5*(kfull[1:]+kfull[:-1])*np.diff(rr))])
Theta = zeta[-1]
k0 = np.exp(phi)*np.sqrt(-S1)
Theta0 = np.trapezoid(k0, rr)
print(f"Theta (full Q) = {Theta/np.pi:.6f} pi -> theta0 = {(Theta-9*np.pi)/np.pi:+.4f} pi")
print(f"Theta (Q=|s1|) = {Theta0/np.pi:.6f} pi -> theta0 = {(Theta0-9*np.pi)/np.pi:+.4f} pi")

# nodes
s = np.sign(rhop)
idx = [i for i in np.nonzero(s[1:]*s[:-1] < 0)[0] if zeta[i] > 1e-3]
zn = np.array([zeta[i] - rhop[i]*(zeta[i+1]-zeta[i])/(rhop[i+1]-rhop[i]) for i in idx])
print(f"rho'-nodes: {len(zn)};  zeta/pi:", " ".join(f"{z/np.pi:.4f}" for z in zn))
print("spacings/pi:", " ".join(f"{d/np.pi:.4f}" for d in np.diff(zn)),
      f"| last->seal: {(Theta-zn[-1])/np.pi:.4f} pi")

# flux-law at nodes
Phi = Z*rho**2*phip
x = np.exp(phi)
C_q = q/(2*np.sqrt(Z)*(-S1)**0.25*np.sqrt(1-XC))
const_pred = 4*Z*C_q**2*np.sqrt(-S1)
print(f"\nC(from q) = {C_q:.6f}; pred const = {const_pred:.6f}")
for i in idx:
    print(f"  node zeta={zeta[i]/np.pi:7.4f} pi  ratio/pred = {(Phi[i]**2/(x[i]-XC))/const_pred:.4f}")
Th_pred = np.sqrt(Z)*(-S1)**0.25*np.sqrt(1-XC)/C_q
print(f"D2 with C(q): Theta_pred = {Th_pred/np.pi:.4f} pi vs measured {Theta/np.pi:.4f} pi "
      f"({100*(Th_pred/Theta-1):+.2f}%)")
# R2 with measured Theta
Qs = (Z/4.0)*(q/(Z*rho_s**2))**2 - S1
a_R2 = np.sqrt(Z*(1-XC))*((-S1)/Qs)**0.25/Theta
print(f"R2 a_seal (measured Theta) = {a_R2:.6f}; banked |rho_s-1| = {abs(rho_s-1):.6f} "
      f"({100*(a_R2/abs(rho_s-1)-1):+.2f}%)")
print("\nSHOT LEDGER: 1 IVP shot this script (cumulative 4)")
