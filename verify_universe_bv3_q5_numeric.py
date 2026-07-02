"""bv3_q5_numeric.py — BV3 numeric spot-check (Q5) of Q1-Q4 identities/inequalities.
Toy phi-blind matter: potential-only L_m = -U(rho), U(rho) = 2 rho^2 / rho_c^2
  => H_m = +U(rho); H_m(core) = 2 exactly (Q3 core closure), so H_tot == 0 along the orbit.
  sigma-source (banked D3 form): rho'' gains + (e^{2phi}/4) U'(rho).
Integrate from core pins (phi'=rho'=0, phi_c=-ln 3, rho_c=1) to the phi=0 crossing = r_s
(rho'_s GENERAL there — tests the general-edge Q2). CPU, bounded.
"""
import numpy as np
from scipy.integrate import solve_ivp

Z = 8.0
rho_c = 1.0
phi_c = -np.log(3.0)       # Delta_phi = ln 3 (toy anchor)

def U(rho):  return 2.0*rho**2/rho_c**2
def Up(rho): return 4.0*rho/rho_c**2

def rhs(r, y):
    phi, rho, phip, rhop = y
    e2m = np.exp(-2*phi)
    phipp = 4*e2m*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
    rhopp = 2*phip*rhop - (Z/4)*rho*np.exp(2*phi)*phip**2 + (np.exp(2*phi)/4)*Up(rho)
    return [phip, rhop, phipp, rhopp]

def phi_zero(r, y): return y[0]
phi_zero.terminal = True; phi_zero.direction = 1

def run(phi_c, rho_c, r0=1e-9, rmax=2000.0):
    y0 = [phi_c, rho_c, 0.0, 0.0]
    s = solve_ivp(rhs, (r0, rmax), y0, events=phi_zero, rtol=1e-12, atol=1e-14,
                  dense_output=True, max_step=0.5)
    assert s.t_events[0].size, "phi never reached 0"
    rs = s.t_events[0][0]
    return s, rs

s, rs = run(phi_c, rho_c)
rr = np.linspace(s.t[0], rs, 20001)
Y = s.sol(rr)
phi, rho, phip, rhop = Y
phis, rhos, phips, rhops = s.sol(rs)

Hgeo = 0.5*Z*rho**2*phip**2 - 2*np.exp(-2*phi)*rhop**2 - 2.0
Hm   = U(rho)
Htot = Hgeo + Hm
print(f"r_s = {rs:.8f}, rho_s = {rhos:.8f}, rho'_s = {rhops:.8f}, phi_s = {phis:.2e}")
print(f"H_tot drift: max|H_tot| = {np.max(np.abs(Htot)):.3e}  (should be ~0; H_m(core)=2 exact)")

# Q1: MS mass identities
m = (rho/2.0)*(1 - np.exp(-2*phi)*rhop**2)
lhs = 1 - 2*m/rho
rhs_ = np.exp(-2*phi)*rhop**2
print(f"Q1 residual max|1-2m/rho - e^(-2phi)rho'^2| = {np.max(np.abs(lhs-rhs_)):.3e}")
# Phi' = 4(1-2m/rho): check Phi(rs) - Phi(rc) = 4 int (1-2m/rho) dr
Phi = Z*rho**2*phip
q = Z*rhos**2*phips
I_flux = np.trapz(4*(1-2*m/rho), rr)
print(f"Q1 q = {q:.8f};  4 int(1-2m/rho)dr = {I_flux:.8f};  rel.residual = {abs(q-I_flux)/abs(q):.2e}")
print(f"Q1 m(core) = {m[0]:.8f} (expect rho_c/2 = {rho_c/2});  m(seal) = {m[-1]:.8f} "
      f"(expect (rho_s/2)(1-rho'_s^2) = {(rhos/2)*(1-rhops**2):.8f})")
print(f"Q1 2m<rho interior: min over rho'!=0 of (1-2m/rho) = {np.min((1-2*m/rho)[1:]):.3e} (>0?)"
      f"  at core: 1-2m/rho = {(1-2*m[0]/rho[0]):.3e} (=0, marginal)")

# Q2: general-edge budget  H_m(core) - H_m(seal) = q^2/(2 Z rho_s^2) - 2 rho'_s^2
lhs2 = U(rho_c) - U(rhos)
rhs2 = q**2/(2*Z*rhos**2) - 2*rhops**2
print(f"Q2 H_mc-H_ms = {lhs2:.8f};  q^2/(2Z rho_s^2) - 2 rho'_s^2 = {rhs2:.8f};  residual = {lhs2-rhs2:.2e}")

# Q3: H_m(seal) = 2 + 2 rho'_s^2 - q^2/(2 Z rho_s^2)  (under H_tot==0)
Hms_pred = 2 + 2*rhops**2 - q**2/(2*Z*rhos**2)
print(f"Q3 H_m(seal) actual = {U(rhos):.8f};  predicted = {Hms_pred:.8f};  residual = {U(rhos)-Hms_pred:.2e}")
qmax = 2*np.sqrt(Z*(1+rhops**2))*rhos
print(f"Q3 q = {q:.6f} <= q_max = 2 rho_s sqrt(Z(1+rho'_s^2)) = {qmax:.6f}:  {q <= qmax}")

# Q4: Delta_phi <= (q/Z) int dr/rho^2  and  q >= Z Dphi / int dr/rho^2 ; weaker rho_min form
Dphi = phis - phi_c
Iinv = np.trapz(1.0/rho**2, rr)
ub = (q/Z)*Iinv
rho_min = np.min(rho)
print(f"Q4 Delta_phi = {Dphi:.6f} <= (q/Z) int dr/rho^2 = {ub:.6f}:  {Dphi <= ub}")
print(f"Q4 q = {q:.6f} >= Z Dphi / int = {Z*Dphi/Iinv:.6f}:  {q >= Z*Dphi/Iinv}")
print(f"Q4 weaker: q >= Z Dphi rho_min^2/(r_s-r_c) = {Z*Dphi*rho_min**2/(rs-rr[0]):.6f}:  "
      f"{q >= Z*Dphi*rho_min**2/(rs-rr[0])}   (rho_min={rho_min:.6f}, rho_c={rho_c}, monotone rho? "
      f"{np.all(np.diff(rho)>=-1e-14)})")
print(f"Q4 Phi in [0,q]? min Phi = {np.min(Phi):.3e}, max Phi - q = {np.max(Phi)-q:.3e}, monotone? "
      f"{np.all(np.diff(Phi)>=-1e-10)}")

# Q4b numeric homothety: lambda=2 => rho_c->2, r->2r, U_lam(rho)=U(rho/lam) (so H_m(core)=2 kept)
lam = 2.0
def U2(rho):  return U(rho/lam)
def Up2(rho): return Up(rho/lam)/lam
def rhs2f(r, y):
    phi, rho, phip, rhop = y
    e2m = np.exp(-2*phi)
    phipp = 4*e2m*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
    rhopp = 2*phip*rhop - (Z/4)*rho*np.exp(2*phi)*phip**2 + (np.exp(2*phi)/4)*Up2(rho)
    return [phip, rhop, phipp, rhopp]
s2 = solve_ivp(rhs2f, (1e-9, 4000.0), [phi_c, lam*rho_c, 0.0, 0.0], events=phi_zero,
               rtol=1e-12, atol=1e-14, dense_output=True, max_step=0.5)
rs2 = s2.t_events[0][0]
p2s = s2.sol(rs2)
q2 = Z*p2s[1]**2*p2s[2]
rr2 = np.linspace(s2.t[0], rs2, 20001); Y2 = s2.sol(rr2)
Iinv2 = np.trapz(1.0/Y2[1]**2, rr2)
print(f"\nQ4b homothety lam=2: r_s2/r_s = {rs2/rs:.8f} (expect 2), q2/q = {q2/q:.8f} (expect 2), "
      f"Iinv2/Iinv = {Iinv2/Iinv:.8f} (expect 0.5)")
print(f"Q4b window-condition invariant rho_s*Iinv: base = {rhos*Iinv:.8f}, scaled = {p2s[1]*Iinv2:.8f}")
