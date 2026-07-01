#!/usr/bin/env python3
"""
particles_verifier_test_b.py  — BLIND ADVERSARIAL VERIFIER (shares no machinery
with the arm). Refutation target: particles_types_results.md claims 1 (three
generations = odd sectors {3,5,7}) and 2 (depths 5,7 = sector dims).

TEST-B classifier per dimension_ladder_null_audit.md:
  (a) does the selection rule GENERALIZE / is it N-specific?
  (b) how many equally-simple slicings of a dim-9 (or 1+3+5) object yield
      "3 of something"?  -> coincidence-classifier cost.
  (c) is the "7" native to End(H1) as an SO(3) irrep, or imported?
"""
import math, itertools

def out(*a): print(" ".join(str(x) for x in a))

out("="*72)
out("CLAIM 1 — is {3,5,7} = three generations PRINCIPLED or a classifier hit?")
out("="*72)

# ---- FACT 1: the actually-banked SO(3) content of End(H1) (spectrum doc) -----
# End(H1) = 1 + 8, and 8 = 3 + 5.  The banked SO(3) irreps are {1,3,5}.
banked_irreps = [1,3,5]
out("\n[banked, spectrum doc lines 71-86] End(H1)=1+8, 8=3+5 -> SO(3) irreps:",
    banked_irreps)
out("  -> traceless part is 8-dim = A3(3)+S5(5). There is NO room for a 7.")
out("  -> dim of the spin-3 SO(3) irrep (2L+1=7) does NOT appear in End(H1).")

# ---- FACT 2: what the spectrum doc actually says the 7 is -----
out("\n[banked, spectrum doc lines 366-380] the native '7' is:")
out("   *Lambda^2 End(H1) = Lambda^7 End(H1)  -> 7 is a GRADE INDEX (9-2=7),")
out("   the Hodge-COMPLEMENT grade of the two-form sector.")
out("   dim Lambda^7 End(H1) =", math.comb(9,7), " (NOT 7).")
out("   So 'L7 dim 7' conflates an exterior GRADE INDEX with an SO(3) DIMENSION.")
out("   The object of dimension 7 (spin-3 irrep) is NOT present; only the")
out("   number 7 appears, as an index. CONCLUSION: the 7 is IMPORTED.")

# ---- FACT 3: count the equally-simple slicings that yield 'three of something'
out("\n[coincidence-classifier] enumerate simple slicings -> how many give 3?")
# A dim-9 alphabet 1+3+5 (and trace/whole). Enumerate 'natural' subset rules.
pieces = {'trace':1, 'A3':3, 'S5':5}     # banked irreps
full = 9
candidate_rules = []

# Rule family A: pick which irreps among {trace,A3,S5} count as 'generations'
for r in range(0, len(pieces)+1):
    for combo in itertools.combinations(pieces, r):
        candidate_rules.append(("subset of banked irreps", combo, len(combo)))

# Rule family B: odd numbers up to a cap, with various exclusions
def odd_upto(cap): return [k for k in range(1,cap+1) if k%2==1]
for cap in (5,7,9,11):
    odds = odd_upto(cap)
    candidate_rules.append((f"odd<= {cap}", tuple(odds), len(odds)))
    candidate_rules.append((f"odd<= {cap} drop 1", tuple(o for o in odds if o!=1), len(odds)-1))
    candidate_rules.append((f"odd<= {cap} drop 1&top", tuple(o for o in odds if o!=1 and o!=cap), len([o for o in odds if o!=1 and o!=cap])))
    candidate_rules.append((f"odd<= {cap} drop top", tuple(o for o in odds if o!=cap), len(odds)-1))

# count how many rules yield exactly 3 elements
three_hits = [r for r in candidate_rules if r[2]==3]
out(f"  total simple slicing rules enumerated: {len(candidate_rules)}")
out(f"  rules yielding exactly THREE pieces: {len(three_hits)}")
for r in three_hits:
    out("     ->", r[0], r[1])

out("""
  The arm's rule is "odds <=9, drop 1 (trace) AND 9 (whole)" = {3,5,7}.
  But "odds<=9 drop 1" = {3,5,7,9} (FOUR). To get three you ALSO drop 9.
  Equally-simple rules that ALSO yield three:
    - {trace,A3,S5} (the BANKED content, NO import) = THREE already!
    - odds<=7 drop 1 = {3,5,7}
    - odds<=9 drop top = {1,3,5,7}? no that's four ... etc.
  i.e. the BANKED 1+3+5 already gives 'three pieces' (trace,A3,S5) with NO
  Hodge import. The arm instead DROPS the trace, DROPS the whole, and IMPORTS
  a 7 to land on {3,5,7}. That is two exclusions + one import to reach a count
  the banked object already supplied differently.
""")

out("[N-specificity] does the rule generalize? the closure formula N+2(d-1):")
for N in (2,3,4,5):
    odds = [N + 2*(d-1) for d in range(1,5)]
    out(f"   N={N}: N+2(d-1) for d=1..4 = {odds}")
out("   -> 'three generations' is NOT forced by N=3; the count 3 came from")
out("      hand-stopping the cascade at d=3, not from the alphabet closing.")

out("\n"+"="*72)
out("CLAIM 2 — depths 5,7 = sector dims, or RE-LABELED closure counts?")
out("="*72)
out("[git] N_M1=5, N_E1=7 are HARDCODED in native_lepton_ratio_diagnostic_lane.py")
out("      since commit 691e04a (Initial snapshot) — NO derivation there.")
out("[contract 26fc757] gave them rationale n_close = 3 + 2(d-1):")
for d in (1,2,3):
    out(f"      d={d}: 3+2(d-1) = {3+2*(d-1)}")
out("[native_closure_constraint_count.py] n_close(d)=N+2(d-1), N=3:")
out("      this is a BOUNDARY-CLOSURE-CONSTRAINT count, NOT an SO(3) dimension.")
out("""
  So 5 and 7 already had a DIFFERENT 'derivation' (closure-constraint count
  N+2(d-1)) when frozen. The arm now re-labels the SAME 5,7 as 'dim S5, dim L7'.
  Both stories produce {3,5,7,...} because N+2(d-1) with N=3 IS the odd
  arithmetic progression — the same sequence the SO(3) tower 2L+1 produces.
  'Depth = sector dimension' is therefore NOT a derivation that the transfer
  depth EQUALS the irrep dimension; it is a coincidence that two different
  countings of the same odd progression both pass through 5 and 7.
  RETROFIT CONFIRMED: 5,7 were independently frozen; the new label re-describes.
""")
