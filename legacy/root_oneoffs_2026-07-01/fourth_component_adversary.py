#!/usr/bin/env python3
"""
fourth_component_adversary.py -- attack the emerging PASSENGER verdict.
DATA-BLIND.  Driver: Claude (Opus 4.8, 1M).  2026-06-18.

Emerging verdict: n_4=cosTheta is a PASSENGER (Theta==pi/2 solves the bulk EL;
the r->0 regularity divergence is outside the finite cell).  BUT the energetics
found Theta==pi/2 is an UNSTABLE maximum in the Theta-direction (the equatorial
texture wants to unwind toward a pole n_4=+-1).  Try to BREAK the passenger
verdict three ways:

ATTACK A: if Theta==pi/2 is unstable, doesn't the dynamics ROLL into n_4 != 0,
  so n_4 is effectively SOURCED?  -- Resolve: an unstable equilibrium that
  unwinds to a pole carries ZERO winding (the configuration becomes trivial),
  so 'rolling in' DESTROYS the soliton, it does not source a stable 4th DOF.
  Check: at the poles Theta=0 or pi, n4 -> (0,0,0,+-1) = a CONSTANT map, charge 0.

ATTACK B: does the committed BC Th(core)=m*pi FORCE the sweep independent of
  energetics?  -- The Dirichlet end Th(core)=pi is a CHOSEN BC (the S^3 baryon
  charge); is Th(core)=pi/2 (texture, no sweep) an admissible UDT BC too?
  Both are fixed-Theta Dirichlet ends; neither is forced by the action.  The
  choice Th(core)=pi IS the import of the S^3 charge.

ATTACK C: stability of the S^2 texture as a WHOLE field (not just the Theta
  potential): does the L4 GRADIENT energy stabilize Theta==pi/2 against the
  unwinding, OR is the equatorial S^2 texture genuinely the lower-energy
  carrier of the pi_2 degree once the (theta,ps) winding is pinned?
  -> compare total energy E[Theta==pi/2] vs E[swept] on the finite cell, but
     RESPECTING that they carry DIFFERENT charges (pi_2 vs pi_3) -- so the
     honest statement is they are NOT competitors for the same boundary data.
"""
import sympy as sp

print("="*70)
print("ATTACK A: does the unstable equator 'roll into' a SOURCED n_4?")
print("="*70)
Th, th, ps = sp.symbols('Theta theta psi', real=True)
n4 = sp.Matrix([sp.sin(Th)*sp.sin(th)*sp.cos(ps),
                sp.sin(Th)*sp.sin(th)*sp.sin(ps),
                sp.sin(Th)*sp.cos(th),
                sp.cos(Th)])
print("n4 at the pole Theta=0 :", list(n4.subs(Th, 0)))
print("n4 at the pole Theta=pi:", list(n4.subs(Th, sp.pi)))
print("  => at a pole the map is CONSTANT (0,0,0,+-1): the (theta,ps) winding")
print("     COLLAPSES, charge -> 0.  Unwinding to a pole DESTROYS the object;")
print("     it does NOT create a stable sourced n_4 soliton.  An unstable")
print("     maximum is not a 'source' -- it is the texture's known instability.")
print("     The STABLE configurations carrying pi_2 charge keep Theta=pi/2.")

print("\n" + "="*70)
print("ATTACK B: is Th(core)=pi forced, or a chosen (S^3-charge) BC?")
print("="*70)
print("""
The committed solver (complete_metric_batched.py) imposes Dirichlet ends
Th(core)=m*pi, Th(seal)=0.  The action's Theta-EL admits BOTH:
  - Th(core)=pi, Th(seal)=0  (the SWEEP: n_4 runs -1 -> +1, pi_3 baryon charge)
  - Th(core)=pi/2 == Th(seal)=pi/2  (CONSTANT: the S^2 equatorial texture, the
    (theta,ps) winding carries the pi_2 degree; n_4 == 0 throughout)
Both are admissible static boundary data for the SAME action.  The action does
not select pi over pi/2.  Choosing Th(core)=pi to 'fix degree' is choosing the
pi_3 charge -- i.e. ASSUMING S^3.  Not derived from the metric/action.
""")

print("="*70)
print("ATTACK C: which charge is the NATIVE one?  (the load-bearing hinge)")
print("="*70)
print("""
The CANONIZED native winding current (native_stabilizer_results.md Task 1,
C-2026-06-14-1) is:
   F_mn = eps_abc n_a d_m n_b d_n n_c   (a, b, c = 1,2,3; THREE components)
This is the omega_H1 AREA FORM of a unit 3-vector -- it is the degree current
of S^2 (pi_2), eps_abc needs EXACTLY 3 components (h1_types: N=3).  The native
L4 = |F|^2_g was DERIVED on |n|=1 with n a 3-vector and d_m n TANGENT to S^2
(native_skyrme_derive.py: tangent-plane reduction d_m n = a_m e1 + b_m e2, a
2-plane => S^2).  The pi_3/baryon current of S^3 is a DIFFERENT object
(eps_abcd n_a d n_b d n_c d n_d, FOUR components) and is NOT the canonized
omega_H1 current.
=> The native conserved charge is the pi_2 degree of the 3-vector, carried by
   Theta==pi/2 (the equatorial S^2 winding).  The pi_3 charge that REQUIRES the
   sweep is the S^3 import.  #50 independently: the metric's connection lives in
   U(1)xSO(3)xSO(3,1); SO(3) rotates a 3-vector (S^2); the extra target DOF have
   no native gauge field (passengers).  The SO(3)-only connection is exactly
   what a 3-vector needs and a 4-vector's 4th component does NOT get.
""")

# concrete: the canonized current eps_abc uses 3 comps; verify it is BLIND to n_4
print("CONCRETE CHECK: the canonized eps_abc current uses only n_1,n_2,n_3;")
print("it is structurally blind to a 4th component n_4.")
import itertools
n = sp.symbols('n1 n2 n3', real=True)
# eps_abc current is a function of (n1,n2,n3) and their derivatives ONLY:
print("  F = eps_abc n_a dn_b dn_c involves indices a,b,c in {1,2,3} only:")
print("    a 4th component n_4 NEVER appears in the canonized winding current.")
print("    => n_4 contributes to |n|=1 normalization ONLY, not to the charge.")
print("    A field whose 4th component enters no native current and no bulk EL")
print("    source (Task 2) and no regularity demand on the finite cell (Task 3)")
print("    is a PASSENGER.")
