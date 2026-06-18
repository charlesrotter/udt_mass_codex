"""
verify_relrederiv_reciprocity_deep.py
Deep attack on B/P8: is there an INTERNAL (non-SR-import) principle that forces
the INVERSE pairing g_tt*g_rr=-c^2, or is inverse-vs-equal genuinely a free choice?
Test candidate internal principles that could promote P8 from 'assumed analog' to
'derived', OR confirm it is irreducibly a choice.
"""
import sympy as sp
phi=sp.symbols('phi',real=True); c=sp.symbols('c',positive=True)
A=sp.exp(-2*phi)            # -g_tt/c^2, from Part 1a (this is forced)
print("Given (forced by R1+R2): -g_tt/c^2 = A = exp(-2 phi).  g_rr = B = ? (to be tied by R3)")
print()

print("CANDIDATE 1: 'local light speed is c' (null cone normalization).")
print("  Radial null: -g_tt dt^2 = g_rr dr^2 => (dr/dt)^2 = -g_tt/g_rr = c^2 A / B.")
print("  Demanding coordinate light speed = c forces B = A (NOT 1/A). This gives the EQUAL")
print("  reading, contradicting B=1/A. So 'light speed=c in these coords' does NOT yield the tie;")
print("  it yields the opposite. => the tie is NOT a light-cone normalization. (Note: coordinate")
print("  light speed is gauge anyway.)")
print()

print("CANDIDATE 2: 'proper radial distance dilation is reciprocal to clock rate' (the doc's P8).")
print("  f=sqrt(-g_tt/c^2)=sqrt(A); ruler h=sqrt(B). f*h=1 => B=1/A. This is the doc reading.")
B_doc=1/A
print("  => B=",sp.simplify(B_doc)," ; g_tt*g_rr=",sp.simplify(-A*c**2*B_doc))
print()

print("CANDIDATE 3: 'determinant / 2-volume in the t-r plane preserved' (area-form).")
print("  sqrt(-g_tt*g_rr)=const => -g_tt g_rr = const = c^2 => g_tt g_rr=-c^2 => B=1/A. SAME as P8.")
print("  This is an ALTERNATIVE internal route to B=1/A: the t-r area element c*dt*dr is")
print("  phi-INDEPENDENT. But is 'preserve the t-r area' itself forced? No -- it is equivalent")
print("  to P8, not more fundamental. It just renames the assumption.")
print()

print("CANDIDATE 4: physical symmetry 'neither position preferred' as an INVOLUTION.")
print("  Demand the position-swap map (phi -> -phi about the midpoint) be an isometry of the")
print("  t-r block. Under phi->-phi: g_tt=-c^2 A(phi) -> -c^2 A(-phi); for the t-r block to map")
print("  to itself with t<->(length) swapped, need g_rr(phi)=(-g_tt(phi)/c^2)^{-1}? Test:")
# swap symmetry: require the 2-metric diag(-c^2 A, B) be invariant under phi->-phi AND t<->r-roles
A_swap=A.subs(phi,-phi)
print("   A(-phi)=",sp.simplify(A_swap)," ; if B(phi)=A(-phi) then B=",sp.simplify(A_swap),
      " => g_tt*g_rr=",sp.simplify(-A*c**2*A_swap))
print("   This ALSO yields B=1/A (since A(-phi)=exp(2phi)=1/A). Interesting: the phi->-phi")
print("   symmetry route gives B=1/A TOO -- but ONLY because A is exponential (A(-phi)=1/A(phi)).")
print("   So GIVEN the exponential law, 'mirror symmetry phi<->-phi between the two positions'")
print("   is EQUIVALENT to the inverse pairing. This is the closest to an internal justification:")
print("   'neither preferred' = invariance under swapping the two positions = phi->-phi, which")
print("   for the (already forced) exponential A forces B=A(-phi)=1/A.")
print()

print("ASSESSMENT of whether P8 can be promoted to DERIVED:")
print(" - Candidates 2,3,4 ALL yield B=1/A and are mutually equivalent GIVEN the exp law.")
print(" - Candidate 1 (light-speed=c) yields B=A instead, and is gauge -> rejected as the meaning.")
print(" - The phi->-phi swap (Cand 4) is the most defensible reading of 'neither position")
print("   preferred': it is a genuine symmetry statement, and combined with the FORCED exp law")
print("   it forces B=1/A WITHOUT importing the SR length-contraction value -- only using")
print("   exp(-x)=1/exp(x). This WEAKENS the 'P8 is a free analog choice' worry: there is an")
print("   internal symmetry reading that lands on the same tie.")
print(" - BUT it still requires CHOOSING that the swap acts as t-rate <-> radial-length")
print("   (i.e. that g_rr is the conjugate slot). A reading where the swap acts within the")
print("   time slot alone is vacuous; a reading tying time to a TRANSVERSE slot would tie g_thth.")
print("   So the SLOT identification (P8 part ii) remains a choice; the INVERSE vs EQUAL part")
print("   (P8 part i) is essentially forced once the exp law + swap symmetry are in hand.")
print()
print(" NET: P8 is PARTLY reducible (inverse-not-equal follows from exp+swap-symmetry), but the")
print(" component-slot identification (radial=conjugate) is irreducibly a choice. Doc's tagging of")
print(" P8 as ASSUMED(named) is therefore CORRECT and arguably slightly conservative.")
print()

print("CROSS-CHECK: does the EQUAL reading (B=A) even give a constant g_tt*g_rr?")
B_eq=A
print("  EQ: g_tt*g_rr=",sp.simplify(-A*c**2*B_eq)," -> NOT constant (depends on phi).")
print("  So 'B=A' fails to produce any phi-independent structural identity at all; the only")
print("  reading yielding a clean constant tie -c^2 is the inverse one. This is a mild INTERNAL")
print("  argument FOR the inverse reading: only it yields a phi-independent invariant. CONFIRMS")
print("  the doc's choice is the natural one, though 'natural' != 'forced by relativity alone'.")
