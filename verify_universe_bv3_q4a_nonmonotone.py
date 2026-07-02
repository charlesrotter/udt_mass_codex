"""bv3_q4a_nonmonotone.py — Q4(a): demonstrate a non-monotone rho on an admissible solution.
Potential-only phi-blind matter U(rho) = 2 + beta(rho-rho_c) - gamma(rho-rho_c)^2 with beta<0:
sigma = (e^{2phi}/4)U'(rho) is negative at the core (rho dips) then positive (recovers).
D3-banked: potential-only L_m realizes essentially any smooth sigma -> such matter is admissible.
Check: interior rho_min < min(rho_c, rho_s); Q4 bounds still hold with the TRUE interval minimum.
"""
import numpy as np
from scipy.integrate import solve_ivp

Z = 8.0; rho_c = 1.0; phi_c = -np.log(3.0)
beta, gamma = -1.0, 5.0
def U(rho):  return 2.0 + beta*(rho-rho_c) - gamma*(rho-rho_c)**2
def Up(rho): return beta - 2*gamma*(rho-rho_c)

def rhs(r, y):
    phi, rho, phip, rhop = y
    phipp = 4*np.exp(-2*phi)*rhop**2/(Z*rho**2) - 2*phip*rhop/rho
    rhopp = 2*phip*rhop - (Z/4)*rho*np.exp(2*phi)*phip**2 + (np.exp(2*phi)/4)*Up(rho)
    return [phip, rhop, phipp, rhopp]

def phi_zero(r, y): return y[0]
phi_zero.terminal = True; phi_zero.direction = 1
def rho_zero(r, y): return y[1]
rho_zero.terminal = True; rho_zero.direction = -1

s = solve_ivp(rhs, (1e-9, 4000.0), [phi_c, rho_c, 0.0, 0.0], events=[phi_zero, rho_zero],
              rtol=1e-12, atol=1e-14, dense_output=True, max_step=0.2)
if not s.t_events[0].size:
    print("phi never hit 0 (rho collapse or range end):", s.t_events[1], s.t[-1]); raise SystemExit
rs = s.t_events[0][0]
rr = np.linspace(s.t[0], rs, 40001); phi, rho, phip, rhop = s.sol(rr)
phis, rhos, phips, rhops = s.sol(rs)
q = Z*rhos**2*phips
Htot = 0.5*Z*rho**2*phip**2 - 2*np.exp(-2*phi)*rhop**2 - 2 + U(rho)
i_min = np.argmin(rho); rho_min = rho[i_min]
Iinv = np.trapezoid(1.0/rho**2, rr); Dphi = phis - phi_c
print(f"r_s={rs:.6f} rho_s={rhos:.6f} rho'_s={rhops:.6f} q={q:.6f}  maxH={np.max(np.abs(Htot)):.2e}")
print(f"rho_min={rho_min:.6f} at r={rr[i_min]:.4f} (interior? {0 < i_min < len(rr)-1});"
      f" rho_c={rho_c}, rho_s={rhos:.4f} -> rho_min < min(endpoints)? {rho_min < min(rho_c, rhos)-1e-9}")
print(f"monotone rho? {np.all(np.diff(rho) >= -1e-14)}")
print(f"Q4 exact:  Dphi={Dphi:.6f} <= (q/Z)Iinv={(q/Z)*Iinv:.6f}: {Dphi <= (q/Z)*Iinv}")
print(f"Q4 lower:  q={q:.6f} >= Z Dphi/Iinv={Z*Dphi/Iinv:.6f}: {q >= Z*Dphi/Iinv}")
print(f"Q4 rho_min form (true interval min): q >= Z Dphi rho_min^2/(r_s-r_c)="
      f"{Z*Dphi*rho_min**2/(rs-rr[0]):.6f}: {q >= Z*Dphi*rho_min**2/(rs-rr[0])}")
print(f"m at interior rho-min: 2m/rho = {(1-(1-2*((rho[i_min]/2)*(1-np.exp(-2*phi[i_min])*rhop[i_min]**2))/rho[i_min])):.8f} (expect 1: marginal sphere)")
Phi = Z*rho**2*phip
print(f"Phi monotone in [0,q]? min={np.min(Phi):.2e} max-q={np.max(Phi)-q:.2e} mono={np.all(np.diff(Phi)>=-1e-10)}")
