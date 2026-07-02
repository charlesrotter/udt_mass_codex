"""LEMMA D — final table: FULLY-DERIVED predictions vs banked, N=5..11, all 6 combos.

Inputs per row: Z, N, x_c = 1/1101, |s1| (family stuck value; s1(d*)-s1(0) = O(d) ~ 0.2%
TRUNC-flagged). NO banked outputs are used in the prediction chain:
    z_c   = Theta sqrt(x_c)                       (self-consistent, iterated)
    z*    = universal mixture phase from the bottom ODE   [DERIVED, leading order]
    Theta = (N+1) pi + z*                         (node quantization; counting offset -> theta_0
                                                   residual is the KNOWN GAP, O(a^2 Theta))
    q     = 2 Z sqrt|s1| (1 - x_c) / Theta        (flux budget)
    a     = sqrt(Z (1-x_c)) (|s1|/Q_s)^{1/4} / Theta   (Q_s iterated via phi'_s = q/(Z rho_s^2))
    F     = sqrt(alpha^2 + beta^2)                (launch factor)
    dt*   = |s1| sqrt(Z) sqrt(1-x_c) (|s1|/Qs)^{1/4} / (F Theta z_s)  -> d* prediction
    rho_s = 1 + sign(dt)(-1)^N a + u_p            (parity law banked/derived)
Also: 1 extra shot to measure the (A,B) mixture on c2 Z=1 N=8 (beta-contamination check).
"""
import json
import sys
import numpy as np
from scipy.integrate import solve_ivp

BASE = "/home/udt-admin/udt_mass_codex/"
XC = 1.0/1101.0

# family: (Z, |s1| at stuck, dt(d), file, param->d inversion factor dt = c_dt * d)
FAM = {
    "c1_A1m2_Z8":     (8.0, 2.0, 1.0,  "cascade_stageC_c1_A1m2_Z8.json"),
    "c3_A2k3_Z8":     (8.0, 3.0, 1.0,  "cascade_stageC_c3_A2k3_Z8.json"),
    "c4_A3_Z8":       (8.0, 2.0, 0.5,  "cascade_stageC_c4_A3_Z8.json"),   # dt ~ d/2 + O(d^2)
    "c5_A1m4_Z8":     (8.0, 4.0, 2.0,  "cascade_stageC_c5_A1m4_Z8.json"),
    "stageB_A1m3_Z8": (8.0, 3.0, 1.5,  "cascade_stageB_rungs.json"),
    "c2_A1m3_Z1":     (1.0, 3.0, 1.5,  "cascade_stageC_c2_A1m3_Z1.json"),
}

def inject(z_c, zeta_max=60.0):
    def f(z, y):
        g, gp = y
        return [gp, 2*z/(z*z + z_c*z_c)*gp - g]
    s = solve_ivp(f, (0.0, zeta_max), [-1.0, 0.0], rtol=1e-11, atol=1e-13)
    z = zeta_max
    g, gp = s.y[:, -1]
    uJ, uY = np.sin(z) - z*np.cos(z), np.cos(z) + z*np.sin(z)
    uJp, uYp = z*np.sin(z), z*np.cos(z)
    W = uJ*uYp - uY*uJp
    return (g*uYp - gp*uY)/W, (gp*uJ - g*uJp)/W

def predict(Z, s1, N):
    Theta = (N+1)*np.pi
    for _ in range(4):                       # self-consistency iteration (converges fast)
        z_c = Theta*np.sqrt(XC)
        al, be = inject(z_c)
        zstar = np.mod(np.arctan2(-be, al), np.pi)
        Theta = (N+1)*np.pi + zstar
    q = 2*Z*np.sqrt(s1)*(1-XC)/Theta
    a = np.sqrt(Z*(1-XC))/Theta              # first pass, then Qs correction
    for _ in range(3):
        rho_s = 1.0 + a if N % 2 == 0 else 1.0 - a   # sign(dt)>0 branch (below-stuck families)
        phps = q/(Z*rho_s**2)
        Qs = s1 + 0.25*Z*phps**2
        a = np.sqrt(Z*(1-XC))*(s1/Qs)**0.25/Theta
    F = np.hypot(al, be)
    dts = s1*np.sqrt(Z*(1-XC))*(s1/Qs)**0.25/(F*Theta*Theta)   # z_s ~ Theta
    up = (dts - 0.25*Z*phps**2)/Qs
    rho_s = 1.0 + ((+1 if N % 2 == 0 else -1)*a + up)
    return dict(Theta=Theta, zstar=zstar, q=q, a=a, F=F, dts=dts, rho_s=rho_s, z_c=z_c)

print("=" * 122)
print("FULLY-DERIVED predictions (inputs: Z, N, x_c, family |s1| only)  vs  BANKED  —  N=5..11")
print("=" * 122)
print(f"{'combo':<16}{'N':>3}{'q_pred':>9}{'q_bank':>9}{'dq%':>7}"
      f"{'|rho_s-1|_pred':>15}{'|rho_s-1|_bank':>15}{'da%':>7}{'d*_pred':>11}{'d*_bank':>11}{'dd%':>7}")
for combo, (Z, s1, c_dt, f) in FAM.items():
    data = json.load(open(BASE + f))
    for r in data["rungs"]:
        N = r["N_delta"]
        if not (5 <= N <= 11):
            continue
        p = predict(Z, s1, N)
        d_pred = p["dts"]/c_dt
        dq = (p["q"]/r["q"] - 1)*100
        da = (abs(p["rho_s"]-1)/abs(r["rho_s"]-1) - 1)*100
        dd = (d_pred/r["d_star"] - 1)*100
        print(f"{combo:<16}{N:>3}{p['q']:>9.4f}{r['q']:>9.4f}{dq:>7.1f}"
              f"{abs(p['rho_s']-1):>15.5f}{abs(r['rho_s']-1):>15.5f}{da:>7.1f}"
              f"{d_pred:>11.3e}{r['d_star']:>11.3e}{dd:>7.1f}")
    print("-" * 122)

# headline number
p = predict(8.0, 3.0, 8)
print(f"\nHEADLINE: N=8, Z=8: derived |rho_s-1| = {abs(p['rho_s']-1):.4f}  (banked 0.0920);"
      f"  Theta = {p['Theta']/np.pi:.4f} pi;  z* = {p['zstar']/np.pi:.4f} pi (universal);  F = {p['F']:.3f}")
p1 = predict(1.0, 3.0, 8)
print(f"          N=8, Z=1: derived |rho_s-1| = {abs(p1['rho_s']-1):.4f}  (banked 0.0345);"
      f"  ratio pred {abs(p1['rho_s']-1)/abs(p['rho_s']-1):.4f} vs banked {0.034458/0.092026:.4f}")

# ---- 1 shot: measure the (A,B) mixture on c2 Z=1 N=8 (is the beta contamination Z-dependent?)
print("\nMixture measurement, c2 Z=1 N=8 (1 shot):")
sys.path.insert(0, BASE)
from cell_solver_universe_T3 import rhs, PHI_C, make_risefall_slice
Z, m = 1.0, 3.0
U, Up, _ = make_risefall_slice(1.5*(1.0 - 1.393766e-3), m=m)
seal = lambda rr, y, *a: y[0]; seal.terminal, seal.direction = True, +1
sol = solve_ivp(rhs, (0.0, 5e7), [PHI_C, 0.0, 1.0, 0.0], args=(Z, Up), method="LSODA",
                rtol=1e-10, atol=1e-12, events=[seal], dense_output=True)
r_s = sol.t_events[0][0]
rr = np.linspace(0.0, r_s, 400001)
phi, phip, rho, rhop = sol.sol(rr)
h = 1e-6
dt = Up(1.0)/4.0
s1 = -(Up(1.0+h)-Up(1.0-h))/(2*h)/4.0
Q = 0.25*Z*phip**2 + s1
Theta = np.trapezoid(np.exp(phi)*np.sqrt(Q), rr)
C = np.sqrt(Z)*s1**0.25*np.sqrt(1-XC)/Theta
kappa = C*s1**0.25/np.sqrt(Z)
zg = np.sqrt(s1)/kappa*np.exp(phi/2.0)
osc = rho - 1.0 - (dt - 0.25*Z*phip**2)/Q
uJ, uY = np.sin(zg) - zg*np.cos(zg), np.cos(zg) + zg*np.sin(zg)
i0 = np.argmin(np.abs(zg - 0.55*zg[-1])); i1 = i0 + 400
A, B = np.linalg.solve(np.array([[uJ[i0], uY[i0]], [uJ[i1], uY[i1]]]), [osc[i0], osc[i1]])
al, be = inject(Theta*np.sqrt(XC))
print(f"    measured (A,B)*|s1|/dt = ({A*s1/dt:.4f}, {B*s1/dt:.4f});"
      f"  universal prediction = ({al:.4f}, {be:.4f})")
print(f"    F: measured {np.hypot(A, B)*s1/dt:.4f} vs predicted {np.hypot(al, be):.4f};"
      f"  Theta_meas = {Theta/np.pi:.4f} pi vs derived {(9*np.pi+np.mod(np.arctan2(-be,al),np.pi))/np.pi:.4f} pi")
