#!/usr/bin/env python3
"""Step-3 exact symbolic checks (sympy, CPU). NO data files touched (F-DATA clean).
Metric (law-set S reduced form, step-2 ground): ds^2 = -e^{-2phi} c^2 dt^2 + e^{2phi} dr^2 + rho^2 dOmega.
Static redshift readout (canon C-2026-07-02-1 form): 1+z = e^{phi_emit - phi_obs}.
Flux identity (step-2, exact): Phi := Z rho^2 phi',  Phi' = 4 e^{-2phi} rho'^2.
"""
import sympy as sp

PASS = []
def check(name, ok):
    PASS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")

t, d, s, Z, rho_c, phi_c, a, a3, alpha, X, r, m, u = sp.symbols(
    't d s Z rho_c phi_c a a_3 alpha X r m u', positive=True)

# ---------- C1: core-seat expansion (generic even-fold member: rho' = a t + a3/2 t^2, t = r - r_c)
# Solve the flux identity perturbatively to O(t^6); phi enters RHS only at higher order (iterate once).
rp = a*t + sp.Rational(1,2)*a3*t**2                      # rho'(t), a = rho''(r_c) generic
rho = rho_c + sp.integrate(rp, t)
phi0 = phi_c                                              # zeroth iterate
Phi = sp.integrate(4*sp.exp(-2*phi0)*rp**2, t)            # Phi(t) to leading orders (Phi(0)=0, even-core pin)
phip = sp.expand(Phi/(Z*rho**2)).series(t, 0, 6).removeO()
phi_of_t = phi_c + sp.integrate(phip, t)
dphi = sp.expand(phi_of_t - phi_c)
lead4 = dphi.coeff(t, 4)
check("C1a core-seat: phi-phi_c leading term is t^4 (t^1..t^3 coefficients vanish)",
      all(sp.simplify(dphi.coeff(t, k)) == 0 for k in (1, 2, 3)))
check("C1b core-seat quartic coefficient = a^2 e^{-2phi_c}/(3 Z rho_c^2)",
      sp.simplify(lead4 - a**2*sp.exp(-2*phi_c)/(3*Z*rho_c**2)) == 0)
# z(t) = e^{phi-phi_c} - 1 -> leading = dphi leading. Proper distance d = int e^phi dt = e^{phi_c} t (1+O(t^4)).
z_t = sp.series(sp.exp(dphi) - 1, t, 0, 5).removeO()
d_t = sp.series(sp.integrate(sp.exp(phi_of_t), t), t, 0, 5).removeO()
t_of_d = sp.series(sp.solve(sp.Eq(d, sp.exp(phi_c)*t), t)[0], d, 0, 2)  # leading inversion t = e^{-phi_c} d
z_d_lead = sp.simplify(lead4 * (sp.exp(-phi_c)*d)**4)
check("C1c z(d) leading = [rho''(r_c)^2 e^{-6phi_c}/(3 Z rho_c^2)] d^4",
      sp.simplify(z_d_lead - a**2*sp.exp(-6*phi_c)/(3*Z*rho_c**2)*d**4) == 0)
# Areal-excess form: rho - rho_c = (a/2) t^2 + O(t^3)  =>  t^4 = (2(rho-rho_c)/a)^2 (leading)
drho = sp.symbols('Delta_rho', positive=True)   # rho - rho_c
z_areal = sp.simplify(lead4 * ((2*drho/a))**2)  # substitute t^4 -> (2 drho/a)^2
check("C1d z leading in areal excess: z = [4 e^{-2phi_c}/(3 Z rho_c^2)] (rho-rho_c)^2 (QUADRATIC, never linear)",
      sp.simplify(z_areal - 4*sp.exp(-2*phi_c)/(3*Z*rho_c**2)*drho**2) == 0)

# ---------- C2: general activation order rho' ~ a t^alpha  => onset order 2*alpha + 2 >= 4
Phi_g = sp.integrate(4*sp.exp(-2*phi_c)*(a*t**alpha)**2, t)     # = 4 a^2 e^{-2phi_c} t^{2a+1}/(2a+1)
phi_g = phi_c + sp.integrate(Phi_g/(Z*rho_c**2), t)
lead_g = sp.simplify(phi_g - phi_c)
check("C2 general onset: phi-phi_c = 4 a^2 e^{-2phi_c} t^{2alpha+2} / ((2alpha+1)(2alpha+2) Z rho_c^2)",
      sp.simplify(lead_g - 4*a**2*sp.exp(-2*phi_c)*t**(2*alpha+2)/((2*alpha+1)*(2*alpha+2)*Z*rho_c**2)) == 0)

# ---------- C3: off-core seat, phi = phi_0 + p1 s + p2 s^2 (s = r - r_obs; p1 = phi'(r_obs) != 0)
phi_0, p1, p2 = sp.symbols('phi_0 p_1 p_2')
phi_off = phi_0 + p1*s + p2*s**2
z_s = sp.series(sp.exp(phi_off - phi_0) - 1, s, 0, 3).removeO()
# proper distance outward: d(s) = int_0^s e^{phi} = A1 s + A2 s^2 + O(s^3); exact series reversion:
d_full = sp.integrate(sp.exp(phi_off - phi_0), (s, 0, s)) * sp.exp(phi_0)
d_ser = sp.series(d_full, s, 0, 3).removeO()
A1, A2 = d_ser.coeff(s, 1), d_ser.coeff(s, 2)
s_ser = sp.expand((1/A1)*d - (A2/A1**3)*d**2)           # reversion to O(d^2)
check("C3-rev reversion valid: d(s(d)) = d + O(d^3)",
      sp.simplify(sp.series(d_ser.subs(s, s_ser), d, 0, 3).removeO() - d) == 0)
z_d_off = sp.series(sp.expand(z_s.subs(s, s_ser)), d, 0, 3).removeO()
check("C3a off-core outward: z(d) = p1 e^{-phi_0} d + p2 e^{-2phi_0} d^2 + O(d^3)",
      sp.simplify(z_d_off.coeff(d,1) - p1*sp.exp(-phi_0)) == 0 and
      sp.simplify(z_d_off.coeff(d,2) - p2*sp.exp(-2*phi_0)) == 0)
# inward: source at s = -sigma (sigma > 0), same proper distance d = int_{-sigma}^0 e^{phi}
sig = sp.symbols('sigma', positive=True)
d_in_full = -sp.integrate(sp.exp(phi_off - phi_0), (s, 0, s)).subs(s, -sig) * sp.exp(phi_0)
d_in_ser = sp.series(d_in_full, sig, 0, 3).removeO()
B1, B2 = d_in_ser.coeff(sig, 1), d_in_ser.coeff(sig, 2)
sig_ser = sp.expand((1/B1)*d - (B2/B1**3)*d**2)
z_d_in = sp.series(sp.expand(z_s.subs(s, -sig).subs(sig, sig_ser)), d, 0, 3).removeO()
dipole = sp.simplify((z_d_off - z_d_in)/2)
monopole = sp.simplify((z_d_off + z_d_in)/2)
check("C3b anisotropy exact: dipole = p1 e^{-phi_0} d (leading), monopole = p2 e^{-2phi_0} d^2 (quadratic)",
      sp.simplify(dipole.coeff(d,1) - p1*sp.exp(-phi_0)) == 0 and sp.simplify(dipole.coeff(d,2)) == 0 and
      sp.simplify(monopole.coeff(d,1)) == 0 and sp.simplify(monopole.coeff(d,2) - p2*sp.exp(-2*phi_0)) == 0)

# ---------- C4: WR-L chart-level z(z+2) reproduction (banked Etherington d_L = (1+z)^2 r, D_A = r)
zL = (1 - r/X)**sp.Rational(-1,2) - 1          # 1+z = e^{phi_L}, phi_L = -(1/2)ln(1-r/X), observer phi(0)=0
dL = (1 + zL)**2 * r
check("C4 chart-level: d_L/X - z(z+2) == 0 exactly", sp.simplify(dL/X - zL*(zL+2)) == 0)
# and the seat slope: z = -1 + sqrt(1 + d_L/X) => dz/d(d_L)|_0 = 1/(2X) != 0
zofdL = -1 + sp.sqrt(1 + d/X)
check("C4b z(z+2) forces dz/dd_L|_0 = 1/(2X) != 0 (linear seat onset)",
      sp.simplify(sp.diff(zofdL, d).subs(d, 0) - 1/(2*X)) == 0)

# ---------- C5: S-embedding of L: the flux-identity quadratic (step-2 SIII) and rho = r NOT a solution
quad = 4*(m/X)*u**2 - (Z/m)*u - Z/(2*m**2)      # exact reduction for phi = phi_L (step-2 C6a)
res_rho_eq_r = sp.simplify(quad.subs({u: 1/r, m: X - r}))
num = sp.simplify(sp.numer(sp.together(res_rho_eq_r)))
check("C5 rho = r is NOT an S-solution under phi_L: residual numerator not identically 0",
      sp.expand(num) != 0)

# ---------- C6: u_+ bounded and positive at r=0 (m=X)  => rho(0) > 0 forced (no areal center in S)
disc = sp.simplify((Z/m)**2 + 4*4*(m/X)*Z/(2*m**2))
u_plus_0 = sp.simplify(((Z/m) + sp.sqrt(Z**2/m**2 + 8*Z/(m*X)))/(8*m/X)).subs(m, X)
check("C6 u_+(r=0) = (Z + sqrt(Z^2+8Z))/(8X): finite and > 0 for Z>0",
      sp.simplify(u_plus_0 - (Z + sp.sqrt(Z**2 + 8*Z))/(8*X)) == 0)

# ---------- C7: c_eff ratio identity (canon C-2026-08-06-1): e^{-2 dphi} = (1+z)^{-2} given 1+z = e^{dphi}
dphi_s = sp.symbols('dphi')
check("C7 c_eff ratio: e^{-2 dphi} == (1+z)^{-2} under 1+z = e^{dphi}",
      sp.simplify(sp.exp(-2*dphi_s) - (sp.exp(dphi_s))**(-2)) == 0)

n_fail = sum(1 for _, ok in PASS if not ok)
print(f"\n{len(PASS) - n_fail}/{len(PASS)} PASS")
raise SystemExit(1 if n_fail else 0)
