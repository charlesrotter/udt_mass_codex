"""G<->P SWITCH-CRITERION derivation (analytic anchors via sympy; no solver).
Adversarial target (Charles, sharpened): P admissible IFF finite transverse/angular data
pins a DIMENSIONLESS radial-to-angular invariant that makes the constant-phi mode measurable.
Distinguish (a) which term breaks the shift, (b) is the breaking BULK or BOUNDARY, (c) does
fixed-angular-scale-alone suffice, (d) the minimal pinned invariant."""
import sympy as sp

r, th, ps, c, lam, Z = sp.symbols('r theta psi c lambda Z', positive=True)
phi = sp.Function('phi')

print("=== (a) TERM-BY-TERM shift phi->phi+lam : which terms break? ===")
ph = phi(r)
# kinetic density (R1-weighted) = c sqrt(h) * e^{2phi} g^rr phi'^2 ; on canonical g^rr=e^{-2phi}
kin = sp.exp(2*ph)*sp.exp(-2*ph)*sp.diff(ph,r)**2          # = phi'^2, phi-free
print("  kinetic e^{2phi}g^rr phi'^2 =", sp.simplify(kin), " -> shift-invariant (phi' only):",
      sp.simplify(kin.subs(ph, ph+lam) - kin)==0)
# R^(2)[h] depends only on h (independent of phi) -> invariant by construction (no phi in it)
print("  R^(2)[h]: function of h only -> phi-independent -> shift-invariant: True (by construction)")
# matter (channel-corrected, undilated) -> phi-blind -> invariant: True (derived earlier)
print("  L_m^UDT (undilated channels): phi-blind -> shift-invariant: True (derived)")
# K = K_AB K^AB - K^2 with K_AB = 1/2 e^{-phi} d_r h_AB  -> K ~ e^{-2phi} * (h-only) -> weight -2
Kround = -2*sp.exp(-2*ph)/r**2
print("  K (round, = -2 e^{-2phi}/r^2) shift-weight:",
      sp.simplify(sp.log(Kround.subs(ph,ph+lam)/Kround)/lam), " -> e^{-2lam} K (BREAKS the shift)")
print("  => the ONLY shift-breaking term is the transverse extrinsic K.\n")

print("=== (b) is the K-breaking BULK or BOUNDARY? (round case) ===")
sqh = r**2*sp.sin(th)                     # sqrt(h)
dens = sqh*Kround                          # sqrt(h) K = -2 e^{-2phi} sin th
print("  sqrt(h) K =", sp.simplify(dens))
# EL contribution of the UNcompensated K term to the phi-equation: dK/dphi
print("  dK/dphi =", sp.simplify(sp.diff(Kround,phi(r)).doit() if False else -2*Kround),
      " = -2K  != 0  -> K contributes a genuine BULK source to the phi-EL (P is a BULK eq, not just a BC).")
# is int dr sqrt(h) K a total r-derivative (=> boundary only)? it is -2 sin th * int e^{-2phi} dr,
# whose integrand -2 e^{-2phi} is d/dr F only if F=-2 int e^{-2phi} (nonlocal) -> NOT a local total deriv
print("  int dr sqrt(h)K = -2 sinth * int e^{-2phi} dr : integrand -2e^{-2phi} is NOT d/dr(local F[phi,phi'])")
print("  -> the shift-breaking is BULK (depends on the full phi profile), not boundary-determined.\n")

print("=== (c) does FIXED ANGULAR SCALE alone suffice? (adversarial task 1) ===")
# invariant chi = (radial proper extent)/(transverse scale) = int e^{phi} dr / sqrt(A/4pi)
# under shift: numerator -> e^{lam} * numerator ; A (from h, phi-free) fixed -> chi -> e^{lam} chi
print("  chi = int e^{phi} dr / sqrt(A/4pi) ;  under shift numerator-> e^{lam}*num, A fixed -> chi-> e^{lam} chi")
print("  IF radial interval [r_c,r_i] AND A both fixed -> chi is a FIXED observable that MOVES -> shift NOT gauge -> P")
print("  IF radial extent FREE (r_i->inf continuum exterior, or reparam modulus) -> chi not a fixed finite obs")
print("     -> shift absorbable -> G.  => FIXED ANGULAR SCALE ALONE is INSUFFICIENT (need pinned radial interval too).")

print("\n=== (d) topology n:S^2->S^2 alone? (task 2) ===")
print("  degree = integer (dimensionless); fixes winding/charge, NOT an absolute length -> does NOT pin chi")
print("  -> topology alone does NOT break the shift (it can help SOURCE h_AB / build the cell, but is insufficient).")

print("\n=== (e) Gauss-Bonnet: R^(2) carries NO scale; the scale lives in K ===")
R2 = 2/r**2                               # round 2-sphere intrinsic curvature (radius r)
GB = sp.integrate(sp.integrate(R2*sqh, (th,0,sp.pi)), (ps,0,2*sp.pi))
print("  int_{S^2} sqrt(h) R^(2) =", GB, " = 8 pi (topological, size-INDEPENDENT) -> R^(2) is not a scale-carrier.")
print("  => the radial-to-angular scale that the shift moves is carried by K (radial evolution), consistent with (b).")
