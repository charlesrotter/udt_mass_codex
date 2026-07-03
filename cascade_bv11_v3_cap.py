"""bv11 V3: the band cap. CAS re-derivation + numeric T_max + trajectory attack."""
import numpy as np
import sympy as sp

# ---------------------------------------------------------------- CAS: orbit identities
r = sp.symbols("r")
Zs = sp.symbols("Z", positive=True)
phi = sp.Function("phi")(r)
rho = sp.Function("rho")(r)
Uf = sp.Function("U")
# EOMs (from cell_solver_universe_T3.rhs):
phipp = 4*sp.diff(rho, r)**2/(sp.exp(2*phi)*Zs*rho**2) - 2*sp.diff(phi, r)*sp.diff(rho, r)/rho
rhopp = 2*sp.diff(phi, r)*sp.diff(rho, r) - sp.Rational(1, 4)*Zs*rho*sp.exp(2*phi)*sp.diff(phi, r)**2 \
        + sp.Rational(1, 4)*sp.exp(2*phi)*Uf(rho).diff(rho)

Phi = Zs*rho**2*sp.diff(phi, r)
W = Phi**2/(2*Zs*rho**2) + Uf(rho) - 2
H = sp.Rational(1, 2)*Zs*rho**2*sp.diff(phi, r)**2 - 2*sp.exp(-2*phi)*sp.diff(rho, r)**2 - 2 + Uf(rho)

# (a) W - 2 e^{-2phi} rho'^2 == H  (so on H=0: rho'^2 = e^{2phi} W / 2)
chk_a = sp.simplify(W - 2*sp.exp(-2*phi)*sp.diff(rho, r)**2 - H)
# (b) Phi' == 4 e^{-2phi} rho'^2 after substituting the phi EOM
Phip = sp.diff(Phi, r).subs(sp.Derivative(phi, r, 2), phipp)
chk_b = sp.simplify(Phip - 4*sp.exp(-2*phi)*sp.diff(rho, r)**2)
print("CAS (a) W - 2e^{-2phi}rho'^2 - H = 0 ?", chk_a == 0)
print("CAS (b) Phi' - 4e^{-2phi}rho'^2 = 0 (phi-EOM substituted)?", chk_b == 0)
print("   => on the H=0 orbit: Phi' = 2W  and  W = 2e^{-2phi}rho'^2 >= 0 IDENTICALLY")
# (c) Lemma 1: W=0, Phi^2>0 -> U = 2 - Phi^2/(2 Z rho^2) < 2  (immediate; record)
print("CAS (c) Lemma 1: W=0 => U = 2 - Phi^2/(2 Z rho^2) < 2 when Phi^2>0 : holds by (a)")
# (d) rho'' at a seal (phi=0, rho'=0): rho''_s = (U'(rho_s) - q^2/(Z rho_s^3))/4
rhopp_seal = rhopp.subs({sp.Derivative(rho, r): 0, phi: 0})
q_ = sp.symbols("q")
rhopp_seal = rhopp_seal.subs(sp.Derivative(phi, r), q_/(Zs*rho**2))
chk_d = sp.simplify(rhopp_seal - (Uf(rho).diff(rho) - q_**2/(Zs*rho**3))/4)
print("CAS (d) rho''_seal = [U'(rho_s) - q^2/(Z rho_s^3)]/4 ?", chk_d == 0)
print("   with q^2 = 2Z rho_s^2 (2-U_s):  rho''_s > 0  <=>  rho_s U'(rho_s) > 2(2-U(rho_s))")
print("   i.e. the BAND CONDITION == approach-from-above (one-sided local min), EXACTLY.")

# ---------------------------------------------------------------- numeric T_max
Zn, m = 8.0, 3.0
def U(rh, a):  return 2.0*rh**m*np.exp(-a*(rh*rh-1.0))
def Up(rh, a): return U(rh, a)*(m/rh - 2.0*a*rh)
def T(rh, a):  return 2.0*Zn*rh*rh*(2.0-U(rh, a))

for label, a in (("fundamental a*(mine)", 1.5099953390),
                 ("claimed-a 1.51", 1.51),
                 ("below N=1 a*", 1.4903071093405713)):
    rh = np.linspace(1e-6, 1.0-1e-9, 2000001)
    Tv = T(rh, a)
    band = rh*Up(rh, a) > 2.0*(2.0-U(rh, a))          # == T'(rho)<0 region
    iT = np.argmax(Tv)
    Tmax_all = Tv[iT]
    Tmax_band = np.max(Tv[band]) if band.any() else np.nan
    # band edges
    edges = rh[np.where(np.diff(band.astype(int)) != 0)[0]]
    print(f"\n[{label}] a={a}")
    print(f"  max T over (0,1)     = {Tmax_all:.6f} at rho={rh[iT]:.6f}")
    print(f"  max T over band      = {Tmax_band:.6f}   band edges(rho): {edges}")
    print(f"  q_cap = sqrt(T_max)  = {np.sqrt(Tmax_band):.6f}")

qf, qb = 2.2090567868962654, 2.1916694402365264
Tf = np.sqrt(np.max(np.where(np.linspace(1e-6,1-1e-9,2000001)*Up(np.linspace(1e-6,1-1e-9,2000001),1.5099953390)>2*(2-U(np.linspace(1e-6,1-1e-9,2000001),1.5099953390)), T(np.linspace(1e-6,1-1e-9,2000001),1.5099953390), -np.inf)))
Tb = np.sqrt(np.max(np.where(np.linspace(1e-6,1-1e-9,2000001)*Up(np.linspace(1e-6,1-1e-9,2000001),1.4903071093405713)>2*(2-U(np.linspace(1e-6,1-1e-9,2000001),1.4903071093405713)), T(np.linspace(1e-6,1-1e-9,2000001),1.4903071093405713), -np.inf)))
print(f"\nfundamental: q={qf:.4f}  cap={Tf:.4f}  q/cap = {qf/Tf:.4f}")
print(f"below N=1  : q={qb:.4f}  cap={Tb:.4f}  q/cap = {qb/Tb:.4f}")

# ---------------------------------------------------------------- trajectory attack
d = np.load("bv11_fundamental_traj.npz")
rr, ph, php, rho_t, rhop_t = d["rr"], d["phi"], d["phip"], d["rho"], d["rhop"]
a_star = float(d["astar"])
Phi_t = Zn*rho_t**2*php
W_t = Phi_t**2/(2*Zn*rho_t**2) + U(rho_t, a_star) - 2.0
res = W_t - 2.0*np.exp(-2*ph)*rhop_t**2
print(f"\n[trajectory, N=0 fundamental] max|W - 2e^(-2phi)rho'^2| = {np.max(np.abs(res)):.2e}")
print(f"  Phi monotone nondecreasing? {bool(np.all(np.diff(Phi_t) > -1e-12))}"
      f"   Phi range [{Phi_t.min():.3e}, {Phi_t.max():.4f}]")
print(f"  min W on trajectory = {W_t.min():.3e}  (claim: W>=0)")
rs, qs = rho_t[-1], Phi_t[-1]
bandval = rs*Up(rs, a_star) - 2.0*(2.0-U(rs, a_star))
print(f"  seal rho_s={rs:.6f}: rho_s U' - 2(2-U) = {bandval:+.4f}  (>0 => in band)")
print(f"  q^2 = {qs*qs:.6f} vs T(rho_s) = {T(rs, a_star):.6f}  (exact seal identity)")
# below N=1 band membership from banked numbers
ab, rsb = 1.4903071093405713, 0.6426014077682966
print(f"[below N=1, banked rho_s={rsb}] rho_s U' - 2(2-U) = "
      f"{rsb*Up(rsb, ab) - 2*(2-U(rsb, ab)):+.4f}  (>0 => in band)")
print(f"  q^2 banked = {qb*qb:.6f} vs T(rho_s) = {T(rsb, ab):.6f}")
