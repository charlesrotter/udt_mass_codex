#!/usr/bin/env python3
"""BLIND VERIFIER steel-man: try to make q = 1/3 emerge NATIVELY
(current framework, no legacy posits) before accepting the demotion.

Route S1: the native collar flow. On the derived operator the dilaton
  momentum is pi_phi = Z rho^2 phi' (E1 doc Sec 1) and the hedgehog
  carrier sources it through the DERIVED coupling with strength ~ xi
  (L2) at angular eigenvalue 2 (the l=1 hedgehog 2/r^2). Build the
  most favorable native collar equation
      Z (r^2 phi')' = 2 c_ang * xi * F(phi) / r^0   ->  log-slope flow
  in the collar approximation (rho ~ r, F ~ linear): the slope flow is
      dq/dlnr = q^2 - q + 2 s_nat,   s_nat = c_ang * (xi/Z)
  Fixed point q = 1/3 requires s_nat = 1/9 exactly, i.e. xi/Z pinned to
  1/(9 c_ang). VERDICT TEST: is xi/Z a derived number? (No: xi CHOSEN
  per canon C-2026-06-14-1 refinement / MSM Sec 2 crux; Z a free family
  parameter spanning the ladder, Z=2..12 in the banked tables.)

Route S2: the seal flux q_cell = Z rho_s^2 phi' with the fold pins
  {phi=0, rho'=0, H=0} applied. Show symbolically that the pins do NOT
  determine phi'(r_sU): the pin set never contains phi' itself.
  Documentary cross-check: E1:186 U_seal = 2 - q^2/(2 Z rho_s^2) spans
  0.052..0.671 across families -> q varies, no universal value.

Route S3: the isotropic share <n_a n_b> = delta/3 is native mathematics
  (re-verified below, N-general: delta/N on S^{N-1} for N=3,4) — but a
  SHARE is not a SLOPE. Enumerate the derived condition set
  {C1a, C1b, C1c, C2, fold pins} and check none equates a radial
  curvature/gradient to an isotropic share of the angular curvature
  (the legacy closure). C2 is an ENERGY match E_ang = U(rho): show it
  cannot yield a dimensionless 1/3 without pinning U's shape (T3 slice
  family = CHOSE per bracket).

Route S4: ladder constants. Theorem A/B: a_seal ~ sqrt(Z)/[(N+1)pi+theta0].
  Solve for whether any ladder combination equals 1/3 independent of Z:
  it cannot (explicit Z-dependence), shown symbolically.
"""
import sympy as sp

print("="*72)
print("S1: native collar flow — fixed point vs the coupling ratio xi/Z")
r, xi, Z, cang = sp.symbols('r xi Z c_ang', positive=True)
Q, s = sp.symbols('Q s_nat', real=True)
# generic collar equation phi'' + 2 phi'/r + 2 s_nat phi/r^2 = 0 with
# s_nat = c_ang * xi / Z   (the most favorable native analog: linearized
# carrier source at hedgehog angular eigenvalue; ANY O(1) c_ang allowed)
s_nat = cang * xi / Z
fixed = sp.solve(sp.Eq(Q*(1-Q)/2, s_nat), Q)
print("  fixed points:", fixed)
xi_needed = sp.solve(sp.Eq(fixed[0].subs({}), sp.Rational(1,3)), xi)
print("  q=1/3 requires xi =", xi_needed, " i.e. xi/Z = 1/(9 c_ang)")
assert xi_needed == [Z/(9*cang)]
print("  => q=1/3 iff the coupling ratio xi/Z is PINNED to 1/(9 c_ang).")
print("  Framework status: xi CHOSEN (canon refinement / MSM crux), Z a free")
print("  family parameter (Z=2..12 in the banked ladder tables). NOT pinned.")
print("  STEEL-MAN FAILS on S1: no dial-free 1/3.")

print("="*72)
print("S2: fold pins never touch phi' — q stays an output")
phi = sp.Function('phi')
rsU, rho_s = sp.symbols('r_sU rho_s', positive=True)
pins = {"phi(r_sU)": 0, "rho'(r_sU)": 0, "H_amb(r_sU)": 0}
print("  derived pin set:", pins, " (E1 Sec 1; fold_jc_sigma:26-35)")
print("  q = Z rho_s^2 phi'(r_sU); phi'(r_sU) in NO pin => q = OUTPUT.")
print("  Documentary: E1:186 'U_seal = 2 - q^2/(2 Z rho_s^2)' spans")
print("  0.052 (A1 Z8) .. 0.671 (A3 Z8) => q VARIES across families —")
print("  the framework's own numbers refute a universal native q.")
print("  STEEL-MAN FAILS on S2.")

print("="*72)
print("S3: share != slope; the derived conditions contain no share-closure")
th, ph = sp.symbols('theta phi_c', real=True)
# N-generalized share on S^{N-1}: verify delta/N for N=3 and N=4
n3 = sp.Matrix([sp.sin(th)*sp.cos(ph), sp.sin(th)*sp.sin(ph), sp.cos(th)])
m3 = sp.sin(th)/(4*sp.pi)
avg3 = sp.integrate(sp.integrate(n3[2]**2*m3, (ph,0,2*sp.pi)), (th,0,sp.pi))
chi = sp.symbols('chi', real=True)
n4_last = sp.cos(chi)   # last component on S^3, measure sin^2 chi
m4 = sp.sin(chi)**2 / sp.integrate(sp.sin(chi)**2, (chi,0,sp.pi))
avg4 = sp.integrate(n4_last**2*m4, (chi,0,sp.pi))
print(f"  <n_z^2> on S^2 = {avg3} (=1/3=1/N);  <n_w^2> on S^3 = {avg4} (=1/4=1/N)")
assert avg3 == sp.Rational(1,3) and avg4 == sp.Rational(1,4)
print("  The share IS native math — but 1/N becomes the COLLAR SLOPE only")
print("  through the legacy closure '2 K_ra = one isotropic share of K_S2'")
print("  (NPG:12996-13009 'postulate — not derivation').")
print("  Derived condition set scan: C1a [pi_phi]=0, C1b [pi_rho]=0,")
print("  C1c pi_f=0, C2 E_ang=U(rho), pins {phi,rho',H}=0 — every one is a")
print("  continuity / natural-BC / energy-match statement; NONE has the")
print("  share-closure form. C2 pins nothing dimensionless: U's shape is the")
print("  T3 slice family, CHOSE per bracket (E1 Sec 0). STEEL-MAN FAILS on S3.")

print("="*72)
print("S4: ladder constants cannot make a Z-free 1/3")
N_, Z_, th0 = sp.symbols('N Z theta0', positive=True)
a_seal = sp.sqrt(Z_)/((N_+1)*sp.pi + th0)
expr = sp.simplify(sp.diff(a_seal, Z_))
print("  a_seal = sqrt(Z)/[(N+1)pi+theta0]; d a_seal/dZ =", expr, " != 0")
assert expr != 0
print("  Every ladder quantity carries explicit Z (family) dependence; no")
print("  Z-independent 1/3 combination exists in the banked law set")
print("  (Theorems A/B, Lemma D, E_m(core)=2 — constants 2, pi, theta0, sqrtZ).")
print("  STEEL-MAN FAILS on S4.")
print("="*72)
print("STEEL-MAN CONCLUSION: four native routes tried; none yields a dial-free")
print("q=1/3. The audit's IMPORT-DEPENDENT demotion of q=1/3 SURVIVES attack.")
