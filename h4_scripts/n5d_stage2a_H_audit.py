"""Part B: off-round H / transversality audit (pi2 tile).  Construct the autonomous radial Lagrangian
L_gs = L_vac + L_shear (geometric+shear sector), derive its EL eqs, form the Beltrami H, verify
dH/dr=0 on-shell symbolically, and confirm round-limit -> base vacuum H.  Matter moments handled by
structure + round-limit (full moment-integral conservation flagged as residual)."""
import sympy as sp

r = sp.symbols('r')
Z, K = sp.symbols('Z K', positive=True)          # Z_phi ; K = geometric shear-kinetic constant (=2c/5)
phi = sp.Function('phi')(r); rho = sp.Function('rho')(r); a2 = sp.Function('a2')(r)
ph1 = sp.diff(phi, r); rh1 = sp.diff(rho, r); a1 = sp.diff(a2, r)
e2m = sp.exp(-2*phi)

# --- radial Lagrangian (autonomous: no explicit r) ---
# L_vac reverse-engineered so Beltrami H = (Z/2)rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - 2 (the base vacuum H)
L_vac = sp.Rational(1,2)*Z*rho**2*ph1**2 - 2*e2m*rh1**2 + 2
# shear kinetic (P2-projected): L_shear = -(K/2) e^{-2phi} rho^2 a2'^2  (EL => the E_s_geom operator)
L_shear = -sp.Rational(1,2)*K*e2m*rho**2*a1**2
L = L_vac + L_shear

def EL(Lag, q):
    return sp.diff(Lag, q) - sp.diff(sp.diff(Lag, sp.diff(q, r)), r)

ELphi = sp.simplify(EL(L, phi)); ELrho = sp.simplify(EL(L, rho)); ELa2 = sp.simplify(EL(L, a2))
print("=== EL equations from L_gs (solve for phi'', rho'', a2'') ===")
ph2 = sp.symbols('phipp'); rh2 = sp.symbols('rhopp'); a2pp = sp.symbols('a2pp')
sub2 = {sp.diff(phi,r,2):ph2, sp.diff(rho,r,2):rh2, sp.diff(a2,r,2):a2pp}
phi_eom = sp.solve(ELphi.subs(sub2), ph2)[0]
rho_eom = sp.solve(ELrho.subs(sub2), rh2)[0]
a2_eom  = sp.solve(ELa2.subs(sub2), a2pp)[0]
print("phi'' =", sp.simplify(phi_eom))
print("rho'' =", sp.simplify(rho_eom))
print("a2''  =", sp.simplify(a2_eom))

# --- base off-round checks ---
print("\n=== round-limit / base recovery ===")
phi_base = 4*e2m*rh1**2/(Z*rho**2) - 2*ph1*rh1/rho
print("  phi'' - [base + a2 correction]  (a2=0):",
      sp.simplify((phi_eom - phi_base).subs({a2:0, a1:0})))
print("  phi'' off-round has the +a2'^2 term:  phi''-phi_base =",
      sp.simplify(phi_eom - phi_base))
rho_base = 2*ph1*rh1 - sp.Rational(1,4)*Z*rho*sp.exp(2*phi)*ph1**2
print("  rho'' - base_vac (a2=0):", sp.simplify((rho_eom - rho_base).subs({a2:0, a1:0})))

# --- Beltrami H and dH/dr=0 ---
H = sp.simplify(ph1*sp.diff(L,ph1) + rh1*sp.diff(L,rh1) + a1*sp.diff(L,a1) - L)
print("\n=== Beltrami H_gs ===")
print("H_gs =", H)
print("H_gs at a2'=0 (round) =", sp.simplify(H.subs({a1:0})), " (expect base vacuum H)")

dH = sp.diff(H, r)
# substitute the EL second-derivatives on-shell
dH_onshell = dH.subs({sp.diff(phi,r,2):phi_eom.subs(sub2, simultaneous=True) if False else 0})
# cleaner: replace phi'',rho'',a2'' by their EOMs
dH2 = dH.subs({sp.diff(phi,r,2): phi_eom, sp.diff(rho,r,2): rho_eom, sp.diff(a2,r,2): a2_eom})
print("\n=== dH/dr on-shell (expect 0) ===")
print("dH/dr =", sp.simplify(dH2))

print("\n=== Hseal row for Stage-2b ===")
print("H(r) = (Z/2)rho^2 phi'^2 - 2 e^{-2phi} rho'^2 - (K/2) e^{-2phi} rho^2 a2'^2 - 2")
print("       - (xi/2)rho^2 I_r + (xi/2)(I_th^s + N^2 I_s^s) - (kap N^2/2) I_4r^s + (kap N^2/2) I_4th^s/rho^2")
print("  (matter moments = off-round e^{+-s} versions; -> base at s=0).  Hseal: H(r_s)=0.")
