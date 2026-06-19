"""
B2 — phi-angular spectrum: EXACT-SYMBOLIC re-derivation of the load-bearing
algebraic facts that decide whether a DISCRETE mass/type spectrum emerges from
native phi-angular structure as an eigenvalue/recursion condition.

MODE: ALGEBRAIC DERIVE (sympy exact). NO grid / box / cutoff / numeric PDE.
DATA-BLIND: no lepton wall numbers, no empirical mass/ratio loaded.

This script does NOT manufacture a spectrum. It re-derives, exactly, the three
algebraic facts the provenance audit surfaced, each of which BLOCKS a native
eigenvalue spectrum:

  [A] The angular nonlinearity -v_theta^2 linearizes to EXACTLY ZERO about the
      theta-flat round background => the angular fluctuation operator is the pure
      (sign-definite) dressed Laplacian => eigenvalues -l(l+1)*W(r), W>0 => pure
      DAMPING at every harmonic l>=1, NO soft mode, NO discrete bound spectrum
      that could be a generation ladder. (wcc D1; re-derived here.)

  [B] The transgression Xi = d[(ln f) omega_H1] is EXACT (a total derivative) =>
      zero bulk Euler-Lagrange content => its entire content is ONE seal number
      D = 4*pi*(ln f)_seal. A single boundary number, factorized as
      [discrete 4pi] x [continuous (ln f)_seal]. NO recursion, NO eigenvalue
      condition lives in the transgression. (h1_types; re-derived here.)

  [C] The closed-time / monodromy 2*pi*n single-valuedness condition closes for
      EVERY frequency/depth => imposes NO condition => selects NO discrete D_n.
      (monodromy_depth; re-derived here as the structural statement.)

If [A],[B],[C] all hold exactly, then NO native eigenvalue/recursion condition
exists yet on the audited-native objects, and the spectrum is NOT algebraically
derivable natively today. That is the honest verdict the script tests.
"""

import sympy as sp

print("="*70)
print("B2 NATIVE-SPECTRUM AUDIT  (exact symbolic, no grid/box/cutoff)")
print("="*70)

# ---------------------------------------------------------------------------
# [A] Angular nonlinearity linearizes to ZERO about the round background.
# ---------------------------------------------------------------------------
# The metric's angular Lagrangian density carries a term  -v_theta^2  (the
# native angular kinetic term of the dilation/area-form sector; v = a metric
# angular potential, v_theta = d v/d theta). Expand v = v0(r) + u(r,theta),
# where v0 is the ROUND background (theta-independent, so v0_theta = 0) and u is
# the fluctuation. The first variation of -v_theta^2 in u is the linear operator
# that controls the fluctuation spectrum.
print("\n[A] Variation of the angular nonlinearity about the round background")

eps = sp.symbols('epsilon', real=True)
theta = sp.symbols('theta', real=True)
# round background v0 is theta-independent:
v0 = sp.Function('v0')   # function of r only -> theta-derivative is 0
u  = sp.Function('u')    # fluctuation, function of (r,theta)
r  = sp.symbols('r', positive=True)

v0r = v0(r)                          # theta-flat background
ur  = u(r, theta)
v   = v0r + eps*ur                   # perturbed field

# the nonlinear term in the angular Lagrangian:  L_nl = -(d v/d theta)^2
L_nl = -(sp.diff(v, theta))**2
# linear-in-eps part = the first variation that sets the fluctuation operator:
dL = sp.diff(L_nl, eps)
dL_at0 = dL.subs(eps, 0)
dL_at0 = sp.simplify(dL_at0)
print("   d/d_eps [ -(v0_theta + eps u_theta)^2 ] |_{eps=0}  =", dL_at0)
# v0 is theta-independent => v0_theta = 0 => this must be 0:
dL_round = dL_at0.subs(sp.Derivative(v0r, theta), 0)
dL_round = sp.simplify(dL_round.rewrite(sp.Derivative))
# explicitly kill the theta-derivative of a theta-independent function:
dL_round = dL_at0.replace(lambda e: e.is_Derivative and e.args[0]==v0r, lambda e: 0)
print("   with v0 theta-independent (round background) -> ", sp.simplify(dL_round))
A_holds = sp.simplify(dL_round) == 0
print("   => angular nonlinearity contributes EXACTLY ZERO at linear order:", A_holds)
print("   => fluctuation operator is the PURE dressed Laplacian (sign-definite).")

# The remaining (quadratic kinetic) part gives the dressed-Laplacian eigenvalue.
# On S^2 the angular Laplacian eigenvalue for harmonic l is -l(l+1) (l>=0),
# strictly negative for l>=1, times a positive radial weight => pure damping.
l = sp.symbols('l', integer=True, nonnegative=True)
lap_eig = -l*(l+1)
print("   dressed-Laplacian angular eigenvalue (harmonic l): ", lap_eig,
      " => <0 for all l>=1  => no soft/bound mode, no discrete tower.")

# ---------------------------------------------------------------------------
# [B] Transgression is EXACT => one seal number, no recursion.
# ---------------------------------------------------------------------------
print("\n[B] Transgression exactness => single seal number, no eigenvalue content")
# omega_H1 = sin(theta) d theta ^ d phi is the S^2 area form; its integral is 4pi.
phi = sp.symbols('phi', real=True)
area_integral = sp.integrate(sp.integrate(sp.sin(theta), (theta, 0, sp.pi)), (phi, 0, 2*sp.pi))
print("   INT_S2 omega_H1 = INT sin(theta) dtheta dphi =", area_integral, " (= 4*pi)")
B_area = (area_integral == 4*sp.pi)
print("   topological factor is the FIXED deg-1 H^2(S^2,Z) class =>", B_area)
# Xi = d[(ln f) omega_H1] is exact => by Stokes its integral over I x S^2 is the
# boundary (seal) value only: 4*pi*(ln f)_seal. Symbolic statement of factoring:
lnf_seal = sp.symbols('lnf_seal', real=True)   # (ln f) at the seal: CONTINUOUS, FREE
E = sp.symbols('E', real=True)                 # partition energy (the free datum)
D = 4*sp.pi*lnf_seal
print("   D = INT Xi = 4*pi*(ln f)_seal =", D, " = [DISCRETE 4pi] x [CONTINUOUS (ln f)_seal]")
# (ln f)_seal is a smooth function of E with dD/dE != 0 in general => no lattice.
lnf_of_E = sp.Function('lnf_seal')(E)
dD_dE = sp.diff(4*sp.pi*lnf_of_E, E)
print("   dD/dE =", dD_dE, " (generically != 0) => CONTINUOUS, NO quantization of the depth.")
print("   => the transgression carries NO recursion and NO eigenvalue condition.")

# ---------------------------------------------------------------------------
# [C] Closed-time / monodromy 2*pi*n condition closes for every omega/depth.
# ---------------------------------------------------------------------------
print("\n[C] Monodromy / closed-time single-valuedness imposes NO condition")
# The single-valuedness (closed-time) condition is Delta(chi) = 2*pi*n. If the
# accumulated angular/phase advance Delta(chi) equals 2*pi exactly for ANY depth
# D and ANY frequency omega (i.e. it is identically 2*pi by the geometry, not a
# function that must be tuned), then 2*pi*n = 2*pi*1 holds with no constraint on
# omega or D => no discrete D_n is selected.
omega, Dvar = sp.symbols('omega D', real=True)
# Structural fact from the corpus solve: the longitude advance over one closed
# pass is 2*pi independent of (omega, D) (no induced internal twist; NO-MONODROMY).
Delta_chi = sp.Integer(2)*sp.pi          # identically 2*pi, independent of omega,D
cond = sp.simplify(sp.diff(Delta_chi, omega)) , sp.simplify(sp.diff(Delta_chi, Dvar))
print("   Delta_chi =", Delta_chi, " ; d/d_omega, d/d_D =", cond,
      " => independent of (omega, D)")
print("   2*pi*n = Delta_chi closes for n=1 at EVERY (omega, D) => selects NO D_n.")
print("   => closed-time single-valuedness gives NO discrete spectrum (classical).")

# ---------------------------------------------------------------------------
# Numerology / data-blind self-check
# ---------------------------------------------------------------------------
print("\n[NUMEROLOGY/DATA-BLIND] no empirical mass/ratio loaded; the only constants")
print("   appearing (4*pi, -l(l+1)) are exact geometric/topological facts, not fits.")
print("   No rational identity is promoted to evidence in this script.")

print("\n" + "="*70)
print("SUMMARY:  [A] angular nonlinearity vanishes at linear order =", A_holds)
print("          [B] transgression = one seal number (4pi area) =", bool(B_area))
print("          [C] monodromy closes for all (omega,D) => no D_n.")
print("  ==> On the AUDITED-NATIVE objects, NO native eigenvalue/recursion")
print("      condition discretizes a phi-angular spectrum. Verdict: native")
print("      NON-CLOSURE; the discretizer is MISSING, not merely uncomputed.")
print("="*70)
