"""bv9_reshoot.py -- D5(c): re-shoot the banked stageB rung (A1/risefall m=3, Z=8, N=8,
a* = 1.4941244349) and measure, with own code:
  (1) node spacings of rho' in the phase coordinate zeta = int k dr (vs pi)
  (2) theta0 = Theta - (N+1)pi directly from the trajectory
  (3) Phi^2/(e^phi - x_c) constancy along the run
Shot ledger printed. Single process, CPU, bounded.
"""
import sys
import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from cell_solver_universe_T3 import rhs, PHI_C, make_risefall_slice

SHOTS = 0
Z, M, ASTAR = 8.0, 3.0, 1.4941244349
XC = np.exp(PHI_C)                     # = 1/1101
S1 = (8*ASTAR**2 - 8*ASTAR*M - 4*ASTAR + 2*M*M - 2*M)/4.0   # own formula (sympy-verified)
print(f"a* = {ASTAR}, s~1(a*) = {S1:+.6f}  (|s1| = {-S1:.6f})")

U, Up, lab = make_risefall_slice(ASTAR, m=M)

def shoot(rtol, atol):
    global SHOTS
    SHOTS += 1
    seal = lambda r, y, *a: y[0]
    seal.terminal, seal.direction = True, +1
    sol = solve_ivp(rhs, (0.0, 5.0e3), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up),
                    method="LSODA", rtol=rtol, atol=atol, dense_output=True,
                    events=[seal], max_step=np.inf)
    return sol

sol = shoot(1e-11, 1e-13)
r_s = float(sol.t_events[0][0])
phi_s, phip_s, rho_s, rhop_s = sol.y_events[0][0]
q = Z*rho_s**2*phip_s
print(f"re-shot: r_s={r_s:.4f}  rho_s={rho_s:.8f}  q={q:.8f}  rhop_s={rhop_s:+.2e}")
print(f"banked : r_s=1253.08   rho_s=1.092026    q=0.942356")

# dense sampling
rr = np.linspace(0.0, r_s, 400001)
phi, phip, rho, rhop = sol.sol(rr)
e2p = np.exp(2.0*phi)

# --- phase coordinate: k^2 = e^{2phi} Q, Q = (Z/4)phi'^2 + |s1| (full Q) ---
Qfull = (Z/4.0)*phip**2 - S1
kfull = np.exp(phi)*np.sqrt(Qfull)
zeta = np.concatenate([[0.0], np.cumsum(0.5*(kfull[1:]+kfull[:-1])*np.diff(rr))])
Theta = zeta[-1]
# also with Q ~= |s1| only (the D2 bookkeeping)
k0 = np.exp(phi)*np.sqrt(-S1)
zeta0 = np.concatenate([[0.0], np.cumsum(0.5*(k0[1:]+k0[:-1])*np.diff(rr))])
Theta0 = zeta0[-1]
print(f"\nTheta (full Q)   = {Theta:.6f} = {Theta/np.pi:.6f} pi -> theta0 = {(Theta-9*np.pi)/np.pi:+.4f} pi")
print(f"Theta (Q=|s1|)   = {Theta0:.6f} = {Theta0/np.pi:.6f} pi -> theta0 = {(Theta0-9*np.pi)/np.pi:+.4f} pi")
print(f"D2 closed form sqrt(Z)|s1|^{{1/4}}sqrt(1-xc)/C: needs C -- not directly measurable; skip")

# --- rho' interior nodes in zeta ---
s = np.sign(rhop)
idx = np.nonzero(s[1:]*s[:-1] < 0)[0]
# refine by linear interpolation in zeta
znodes = []
for i in idx:
    z1, z2, f1, f2 = zeta[i], zeta[i+1], rhop[i], rhop[i+1]
    znodes.append(z1 - f1*(z2-z1)/(f2-f1))
znodes = np.array(znodes)
# drop any node from the r~0 region where rhop ~ 0 numerically (inner fold has rho'=0)
znodes = znodes[znodes > 1e-3]
print(f"\ninterior rho'-nodes found: {len(znodes)} (banked N_rhop = 8)")
print("zeta_nodes/pi :", " ".join(f"{z/np.pi:.4f}" for z in znodes))
sp_ = np.diff(znodes)
print("spacings/pi   :", " ".join(f"{d/np.pi:.4f}" for d in sp_))
if len(sp_):
    print(f"spacing stats: mean = {sp_.mean()/np.pi:.5f} pi, min = {sp_.min()/np.pi:.5f}, max = {sp_.max()/np.pi:.5f}")
# distance from last node to the seal in zeta (u'(r_s)=0 is itself a node -> spacing to seal)
print(f"last node -> seal: {(Theta-znodes[-1])/np.pi:.4f} pi (seal is an exact rho'=0)")

# theta0 read from node ladder: seal node at Theta; if nodes at ~ n pi + const...
# also delta = rho - 1 interior zeros in zeta (N_delta = 8 banked)
sd = np.sign(rho-1.0)
idxd = np.nonzero(sd[1:]*sd[:-1] < 0)[0]
zd = []
for i in idxd:
    z1, z2, f1, f2 = zeta[i], zeta[i+1], rho[i]-1.0, rho[i+1]-1.0
    zd.append(z1 - f1*(z2-z1)/(f2-f1))
zd = np.array(zd)
print(f"\ninterior (rho-1)-zeros: {len(zd)}")
print("zeta_zeros/pi :", " ".join(f"{z/np.pi:.4f}" for z in zd))
if len(zd) > 1:
    print("spacings/pi   :", " ".join(f"{d/np.pi:.4f}" for d in np.diff(zd)))

# --- flux law constancy: Phi^2/(e^phi - x_c) ---
Phi = Z*rho**2*phip
ratio = Phi**2/(np.exp(phi) - XC)
# exclude the first tiny stretch where both -> 0 (0/0) : start where e^phi - x_c > 0.02*x_c
mask = (np.exp(phi) - XC) > 0.02*XC
rat = ratio[mask]
print(f"\nPhi^2/(e^phi - x_c): mean = {rat.mean():.6f}")
print(f"  min = {rat.min():.6f} ({100*(rat.min()/rat.mean()-1):+.2f}%), "
      f"max = {rat.max():.6f} ({100*(rat.max()/rat.mean()-1):+.2f}%)")
# percentiles to characterize (not filter)
for p in (1, 5, 25, 50, 75, 95, 99):
    print(f"  p{p:02d} = {np.percentile(rat, p):.6f}")
# the D1 prediction: ratio = 4 Z C^2 sqrt|s1| = const; implied C:
C_impl = np.sqrt(rat.mean()/(4*Z*np.sqrt(-S1)))
print(f"implied C = {C_impl:.6f}")
# cross-check D2: Theta_pred = sqrt(Z)|s1|^{1/4} sqrt(1-xc)/C
Th_pred = np.sqrt(Z)*(-S1)**0.25*np.sqrt(1-XC)/C_impl
print(f"D2 with implied C: Theta_pred = {Th_pred:.4f} = {Th_pred/np.pi:.4f} pi (measured {Theta/np.pi:.4f} pi)")
# a_seal check: banked |rho_s - 1| vs R2 with measured Theta
Qs = (Z/4.0)*(q/(Z*rho_s**2))**2 - S1
a_R2 = np.sqrt(Z*(1-XC))*((-S1)/Qs)**0.25/Theta
a_R1 = q/(2*np.sqrt(Z*(1-XC))*((-S1)*Qs)**0.25)
print(f"\nR1 a_seal = {a_R1:.6f}; R2 a_seal (measured Theta) = {a_R2:.6f}; banked |rho_s-1| = {abs(rho_s-1):.6f}")

# convergence spot-check: one more shot at looser tol
sol2 = shoot(1e-9, 1e-11)
r_s2 = float(sol2.t_events[0][0])
_, phip_s2, rho_s2, _ = sol2.y_events[0][0]
print(f"\n[tol check rtol=1e-9] r_s={r_s2:.4f} rho_s={rho_s2:.8f} q={Z*rho_s2**2*phip_s2:.8f}")
print(f"\nSHOT LEDGER: {SHOTS} IVP shots")
