"""
global_spin_structure.py  — UDT Mass Codex
Topological/analytic analysis of the time-reversal DOUBLED cell:
  - orientability of the fold (does sigma: t->-t reverse orientation?)
  - H^1( M ; Z_2)  (count of spin structures)  and  w_2 (does a spin structure exist?)
  - holonomy / antiperiodicity test (does global consistency FORCE T^2=-1 ?)
  - q=1/3 connection

OBSERVE mode. We DERIVE which spin structures exist/are forced; we do NOT
import a spinor. sympy used for the algebraic (Jacobian-sign / orientation)
checks; the cohomology is by Kunneth/Mayer-Vietoris reasoning, cross-checked
on the concrete product/double models.

NB: nvidia/torch not needed; pure sympy + reasoning.
"""
import sympy as sp

print("="*72)
print(" PART 1.  ORIENTABILITY OF THE TIME-REVERSAL FOLD")
print("="*72)

# The seal is the FIXED SURFACE of sigma: t -> -t.  sigma acts ONLY on the
# time direction (w6/#42, and the #37 VERIFIER CORRECTION: r,theta,phi,f,
# omega_H1 all sigma-INVARIANT; the involution touches ONLY the time row).
#
# Question: does the gluing map that builds the double from two cell-copies
# REVERSE orientation?  An involution on a manifold-with-boundary, doubled
# across its fixed surface, yields an orientable double iff the gluing
# diffeomorphism of the boundary, EXTENDED by the reflection, preserves
# orientation of the total space.
#
# Concretely: local coords (t, r, theta, phi).  The fold reflects t -> -t and
# (for the LINE ELEMENT to be sigma-invariant with a sigma-ODD time row) the
# time-row entries A=g_tr,B=g_ttheta flip sign.  But ORIENTABILITY is about
# the COORDINATE Jacobian of the gluing, not the metric components.
#
# The double of a manifold X (with boundary) across the SAME boundary is
# ALWAYS orientable if X is orientable:  DX = X u_{bdy} X-bar, and the
# canonical orientation-reversing identity on the boundary makes the two
# orientations match up.  This is the standard "orientation double has a
# canonical orientation" / "the double of an orientable manifold is
# orientable" fact.  We verify the Jacobian sign of the reflection.

t, r, th, ph = sp.symbols('t r theta phi', real=True)
# The reflection R that defines the fold:  (t,r,theta,phi) -> (-t,r,theta,phi)
R = sp.Matrix([-t, r, th, ph])
J = R.jacobian([t, r, th, ph])
detJ = sp.simplify(J.det())
print(f"  Reflection R: (t,r,th,ph) -> (-t,r,th,ph)")
print(f"  Jacobian det of the pure spatial-fixed reflection  = {detJ}")
print("   => the LOCAL reflection across the t=0 surface is ORIENTATION-REVERSING")
print("      (det = -1: one coordinate, t, flips).")
print()
print("  But the DOUBLE is built by gluing copy-1 to a MIRROR copy-2; the")
print("  mirror copy is given the OPPOSITE orientation, and the two match")
print("  across the fixed surface.  Standard fact:  Double(X) of an")
print("  orientable X is ORIENTABLE (it bounds; it is the boundary-double).")
print("  The fold being a reflection is exactly what makes the canonical")
print("  orientation of the double CONSISTENT.")
print()
print("  KEY DISTINCTION (settles the wcc/#37 flag):")
print("   - METRIC orientation of a single sheet vs its mirror: the time row")
print("     flips sign (sigma-ODD), which is a sign on g_tr,g_ttheta, NOT a")
print("     reversal of the coordinate orientation form  dt^dr^dth^dph.")
print("   - The coordinate volume form  e1^e2^e3^e4  is built from the frame;")
print("     under t->-t the timelike leg e^0 -> -e^0, so the 4-volume form")
print("     flips sign on a SINGLE chart, but the DOUBLE re-glues with the")
print("     mirrored orientation so the global form is well-defined.")
print()
print("  VERDICT 1: the time-reversal DOUBLE is ORIENTABLE (it is a boundary-")
print("  double of an orientable cell).  The earlier 'orientation-reversal")
print("  reading' in wcc was about the SINGLE-sheet volume-form sign, which is")
print("  not a global non-orientability.  [DERIVED]")
print()

print("="*72)
print(" PART 2.  THE UNDERLYING MANIFOLD AND ITS COHOMOLOGY")
print("="*72)
# Single cell spatial+radial body:  I x S^2  (collar I = radial interval,
# S^2 = genus-0 cross section, #37 SOLID).  The cell also has a time
# direction.  Two cases for the GLOBAL shape of the doubled object:
#
#  (A)  TIME is an INTERVAL I_t, sealed at one end (t=0 fold) and capped/
#       open at the other.  Doubling across t=0 gives time -> a (possibly)
#       larger interval or a circle.
#  (B)  The doubling identifies copy-1 and copy-2 -> the time direction
#       becomes a DOUBLED interval; if the FAR ends are ALSO identified
#       (finite-cell canon: NO spatial infinity, finite mirrored domains),
#       the time direction can CLOSE into a CIRCLE S^1_t.
#
# The discriminating object for spin structures is H^1(M;Z_2) and w_2(M).
# We compute for the candidate global shapes.

print("  Candidate global shapes of the doubled cell M:")
print("   (a)  M = I_t x I_r x S^2   (time & radius both intervals): contractible x S^2")
print("        ~ homotopy type S^2.    H^1(S^2;Z_2)=0,  w_2(S^2)=0  (S^2 IS spin).")
print("   (b)  M = S^1_t x I_r x S^2  (time CLOSES, finite-cell double): ~ S^1 x S^2.")
print("        H^1(S^1 x S^2 ; Z_2)= Z_2,  w_2 = 0  (S^1 x S^2 IS spin).")
print("   (c)  M = S^1_t x S^2  (radius capped both ends): same H^1, w_2 as (b).")
print()

# w_2 of these:  S^2 is spin (w=1+...; w_1=w_2=0 since orientable surface,
# in fact TS^2 has w_2 = Euler mod 2 = 2 mod 2 = 0).  Products with
# parallelizable S^1 and contractible I don't add w_2.  So w_2(M)=0 in ALL
# candidate shapes: a spin structure EXISTS.
print("  w_2 computation:")
print("   - TS^2: w_2(S^2) = e(TS^2) mod 2 = chi(S^2) mod 2 = 2 mod 2 = 0.")
print("     (Euler number 2 is EVEN => S^2 admits a spin structure.)")
print("   - S^1 and I are parallelizable (w=1); products: w(M)=w(S^2) by")
print("     Whitney, so w_2(M)=0 for every candidate shape.")
print("   => A SPIN STRUCTURE EXISTS on the doubled cell in every shape. [DERIVED]")
print()
print("  H^1(M;Z_2)  (= the TORSOR of spin structures, # = |H^1|):")
print("   - shape (a)  ~ S^2 :        H^1(;Z_2) = 0   -> spin structure UNIQUE")
print("                               (only the PERIODIC one; T^2=+1).")
print("   - shape (b)/(c) ~ S^1 x S^2: H^1(;Z_2) = Z_2 -> TWO spin structures:")
print("                               PERIODIC (T^2=+1) and ANTIPERIODIC (T^2=-1)")
print("                               around the time circle S^1_t.")
print()
print("  CONSEQUENCE: whether an ANTIPERIODIC (fermionic) spin structure even")
print("  EXISTS is FORK-DEPENDENT on whether the time direction CLOSES into a")
print("  circle (shapes b/c) or stays an interval (shape a).")
print("   - interval time  => H^1=0 => ONLY the periodic structure => NO fermion option.")
print("   - circle time    => H^1=Z_2 => BOTH exist => the fermionic one is ADMITTED.")
print()

print("="*72)
print(" PART 3.  HOLONOMY / ANTIPERIODICITY TEST")
print("="*72)
# The load-bearing loop: go through the seal to the mirror sheet and BACK.
# Going through the seal applies sigma ONCE; the round trip applies sigma^2.
# sigma is t->-t, an honest INVOLUTION: sigma^2 = identity AS A MAP ON THE
# MANIFOLD.  The question is what sigma^2 does to a FIELD / frame, i.e. the
# holonomy in the (double cover of the) frame bundle.
#
# Decompose:  for a TENSOR field, sigma^2 = +1 (single-valued always closes).
# For a would-be SPINOR, the lift of sigma to the spin bundle, call it
# \hat sigma, can square to +1 (periodic) or -1 (antiperiodic).  BOTH lifts
# exist whenever the spin structure with that holonomy exists (Part 2).
#
# CRUCIAL: the round-trip-through-the-seal loop is CONTRACTIBLE when time is
# an interval (shape a): the loop bounds a disk (you can slide the crossing
# point off), so its holonomy MUST be +1 for ANY field, spinor or not.
# A contractible loop has trivial holonomy in a flat/Z_2 sense; antiperiodicity
# can ONLY be carried by a NON-contractible loop.

print("  The 'through the seal and back' loop applies sigma twice.")
print("  sigma: t->-t is a genuine INVOLUTION on the manifold:  sigma^2 = id.")
print()
print("  Is the through-seal-and-back loop CONTRACTIBLE?")
print("   - Shape (a), time = INTERVAL: the seal is the t=0 face; crossing it")
print("     and returning is a loop that BOUNDS (slide the crossing off the")
print("     face).  CONTRACTIBLE => holonomy = +1 FORCED for every field.")
print("     => antiperiodicity CANNOT be required.  No fermion forced (global).")
print("   - Shape (b/c), time = CIRCLE S^1_t: the loop that goes ALL THE WAY")
print("     AROUND the time circle (through the seal AND through the far")
print("     identification) is NON-contractible (generator of pi_1 = Z).")
print("     ITS holonomy is the free choice labelled by H^1(;Z_2)=Z_2:")
print("        +1 = periodic spin structure,   -1 = antiperiodic (fermionic).")
print()
print("  So GLOBAL CONSISTENCY does NOT, by itself, FORCE T^2=-1: it ADMITS")
print("  both, and only when the time direction CLOSES.  The mere existence of")
print("  the mirror fold (a reflection) does not create a non-contractible")
print("  loop; it creates a fixed surface.  [DERIVED]")
print()
print("  This is the GLOBAL echo of #46's LOCAL result: the seal round-trip")
print("  sigma^2 = id, so neither locally (seal-value=0) nor globally (round-")
print("  trip loop contractible) does the FOLD ITSELF force antiperiodicity.")
print()

print("="*72)
print(" PART 4.  q = 1/3 CONNECTION")
print("="*72)
# q = 1 - 2/N = 1/3 is the SLOPE in d ln f = -q d ln r, the public charge of
# the H1 area-form transgression Theta=(ln f) omega_H1.  Per the #37 verifier
# CORRECTION, omega_H1 is sigma-INVARIANT (sigma touches only the time row),
# the transgression glues SYMMETRICALLY, and it is EXACT.
#
# Does q=1/3 = a projective/double-cover (=> antiperiodic spin) signature?
N = sp.Symbol('N', positive=True, integer=True)
q_expr = 1 - sp.Rational(2)/N
print(f"  q = 1 - 2/N ; at N=3:  q = {q_expr.subs(N,3)}")
print("  q is a SLOPE (d ln f = -q d ln r) of an EXACT, sigma-EVEN transgression")
print("  (omega_H1 area form), NOT a Z_2 holonomy or a half-integer winding.")
print()
print("  Is q=1/3 'fractional charge => projective => double cover'?")
print("   - A genuine spin/projective Z_2 signature would be a HALF-integer")
print("     period or a Z_2 holonomy.  q=1/3 is a 1/3, lives in the RADIAL x")
print("     ANGULAR (H^2) sector, is sigma-EVEN, and is an EXACT form (zero")
print("     period over any closed cycle, by Stokes).  It is NOT a Z_2")
print("     spin-bundle datum and does NOT live on the time circle S^1_t that")
print("     would carry antiperiodicity.")
print("   - Therefore q=1/3 does NOT, on the present derivation, pick out the")
print("     antiperiodic spin structure.  It is an EVEN, EXACT, H^2 charge in a")
print("     DIFFERENT cohomological slot than H^1(;Z_2) (where spin lives).")
print("   [DERIVED negative on the q-> spin link, given the banked #37 correction.]")
print()
print("   CAVEAT (honest): IF a later derivation re-grades omega_H1's radial")
print("   factor as orientation-/sigma-ODD (the wcc D3 reading, currently")
print("   SUPERSEDED by the #37 verifier as sigma-EVEN), the transgression would")
print("   move to the odd/Dirichlet sector and a q-spin tie could reopen. Under")
print("   the CURRENT banked facts it does not.")
print()

print("="*72)
print(" PART 5.  SCOPE LADDER")
print("="*72)
print("  EXISTS (weak):      YES, a spin structure exists (w_2=0) in every shape.")
print("  ADMITTED (medium):  the ANTIPERIODIC one is admitted IFF the time")
print("                      direction CLOSES (H^1=Z_2); for interval-time it is")
print("                      not even admitted (H^1=0, unique periodic).")
print("  FORCED/SELECTED:    NOT established. Global consistency does not force")
print("                      antiperiodicity (the through-seal loop is sigma^2=id,")
print("                      contractible for interval-time; a free Z_2 choice for")
print("                      circle-time). q=1/3 does not select it either (even,")
print("                      exact, wrong cohomology slot).")
print()
print("  THE HINGE: does the finite-cell canon CLOSE the time direction into a")
print("  circle?  That is the underived fact that decides ADMITTED-or-not, and")
print("  even then leaves the periodic-vs-antiperiodic choice UNFORCED by the")
print("  topology alone (it would need a physical selector, e.g. a fermion-")
print("  number / Kramers condition that is NOT in the banked structure).")
print()
print("="*72)
print(" SUMMARY OF DERIVED TOPOLOGICAL FACTS")
print("="*72)
print("  - Doubled cell ORIENTABLE: YES (boundary-double of orientable cell).")
print("  - w_2 = 0 (S^2 Euler number 2 is even): spin structure EXISTS.")
print("  - H^1(M;Z_2) = 0 (interval time) or Z_2 (circle time).")
print("  - Antiperiodic structure ADMITTED iff time closes; never FORCED by topology.")
print("  - q=1/3 is sigma-EVEN, exact, H^2: does NOT select the spin structure.")
