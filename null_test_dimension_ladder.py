"""Null test / look-elsewhere audit of the dimension-ladder selector claims.

Targets the exact-rational matches celebrated in
`particle_spectrum_native_geometry.md` (sections 6-7, 15, 27-28, 38, 40-43)
and mirrored in `legacy_hadron_survivor_filter.md`.

This audit does NOT re-derive the operator algebra (that is done in
`native_h1_operator_algebra.py`, `native_commutator_kernel_image_split.py`,
etc.). It asks the statistical/structural question the legacy audit asked of
the (rational)*pi^k mass fits (the da_reaudit_s2_labels.py dense-family
methodology, applied per audit #7 "potential for different models"):

    How much INDEPENDENT evidential weight do the exact rational matches
    carry, once (a) arithmetic dependence between the matched constants,
    (b) forcing by already-banked facts, and (c) naming freedom in a
    small-rational universe are accounted for?

Tests:
  A. Dependence collapse + lock census for the five pre-spectrum matches.
  B. Generalized-N classification of later celebrated identities
     (FORCED / N=3-specific / not-N=3-specific).
  C. Naming multiplicity of headline values in an explicit ladder grammar.
  D. Expressibility coverage of small rationals (the chance level for an
     exact match).
  E. Residual-ledger look-elsewhere (channel residual lattice coverage).
  F. Integer fingerprint coverage 1..200 (context for 36/63/84/108/180).

New file; alters nothing existing. Run: python3 null_test_dimension_ladder.py
"""

from fractions import Fraction as Fr
from math import comb
import sympy as sp


# ----------------------------------------------------------------------
# Shared structures
# ----------------------------------------------------------------------

# The N=3 ladder atoms, each with its native meaning in the spectrum doc.
LADDER_ATOMS = {
    1: "trace / Lambda^0",
    3: "H1, A3, Lambda^2 A3",
    5: "S5",
    8: "T8, trace^T8 block",
    9: "End(H1)",
    10: "Lambda^2 S5",
    15: "A3 tensor S5",
    28: "Lambda^2 T8",
    36: "Lambda^2 End(H1)",
    56: "Lambda^3 T8",
    84: "Lambda^3 End(H1)",
    126: "Lambda^4 End(H1)",
}

# Native boundary/readout instruments (values at q=1/3, N=3), as named in
# particle_spectrum_native_geometry.md sections 36-43. NOTE: 2/9 (the
# trace-kernel load) is deliberately EXCLUDED -- it is one of the matched
# residual values, so including it as an instrument would be circular; its
# claimed native names are level-2 products (q * W(T8)).
INSTRUMENTS = {
    Fr(1, 36): "eta/2 (one-sided H1 transfer, domain unit)",
    Fr(1, 18): "eta (H1 projected unit)",
    Fr(1, 12): "S_C1/R (image unit)",
    Fr(1, 9): "s (End(H1) ninth unit)",
    Fr(1, 6): "q/2 (C1 boundary momentum)",
    Fr(1, 4): "W(A3)",
    Fr(5, 12): "W(S5)",
    Fr(1, 3): "q",
    Fr(2, 3): "W(T8)",
    Fr(1, 1): "full normalized unit",
}


def header(title):
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


# ----------------------------------------------------------------------
# TEST A: dependence collapse and lock census
# ----------------------------------------------------------------------

def test_a():
    header("TEST A: dependence collapse + lock census (5 claimed matches)")

    q, N = sp.symbols("q N", positive=True)

    # Branch formulas as stated in the docs:
    #   flow fixed point:  s = (q - q^2)/2     (dq/dt = q^2 - q + 2s = 0)
    #   boundary momentum: DeltaPi/R = q/2
    #   H1 projection:     eta = (q/2)/N,  eta/2 = (q/2)/(2N)
    s_fp = (q - q**2) / 2
    eta = (q / 2) / N
    eta2 = eta / 2
    dim_h1 = N
    dim_end = N**2
    dim_l2 = N**2 * (N**2 - 1) / 2  # C(N^2, 2)

    print("""
The five claimed matches (spectrum doc section 6):
    M1: q          = 1/dim H1            = 1/N
    M2: s          = 1/dim End(H1)       = 1/N^2
    M3: DeltaPi/R  = 1/(2 dim H1)        = 1/(2N)
    M4: eta        = 2/dim L2End(H1)     = 4/(N^2(N^2-1))
    M5: eta/2      = 1/dim L2End(H1)     = 2/(N^2(N^2-1))
""")

    # M3 is equivalent to M1 (DeltaPi/R := q/2 by definition).
    m3_equiv_m1 = sp.simplify(
        sp.Eq(q / 2, 1 / (2 * dim_h1)).lhs - sp.Eq(q / 2, 1 / (2 * dim_h1)).rhs
        - (q - 1 / dim_h1) / 2
    ) == 0
    print(f"M3 <=> M1 (pure arithmetic, since DeltaPi/R := q/2): {m3_equiv_m1}")

    # M5 is equivalent to M4 (eta/2 is half of eta by definition).
    print("M5 <=> M4 (pure arithmetic, since eta/2 := eta/2): True")

    # LOCK-FLOW: substitute the primary identification q = 1/N into the flow
    # fixed-point source and require M2.
    lhs = s_fp.subs(q, 1 / N)
    sols_flow = sp.solve(sp.Eq(lhs, 1 / dim_end), N)
    print(f"\nLOCK-FLOW: [s = (q-q^2)/2 with q=1/N] == 1/N^2  ->  N in {sols_flow}")
    print("    i.e. (N-1)/(2N^2) = 1/N^2  <=>  N = 3.  Unique positive solution.")

    # Equivalent reading: with the H1 source s = 1/N^2, the flow fixed point
    # q = (1 - sqrt(1-8/N^2))/2 equals 1/N only at N = 3.
    qfix = (1 - sp.sqrt(1 - 8 / N**2)) / 2
    sols_flow2 = sp.solve(sp.Eq(qfix, 1 / N), N)
    print(f"    equivalent: flow root equals 1/N  ->  N in {sols_flow2}")

    # LOCK-2F: with q = 1/N, require M4/M5.
    sols_2f = sp.solve(sp.Eq(eta2.subs(q, 1 / N), 1 / dim_l2), N)
    print(f"\nLOCK-2F: eta/2 = 1/(4N^2) == 1/C(N^2,2)  ->  N in {sols_2f}")
    print("    i.e. C(N^2,2) = 4N^2  <=>  N^2 - 1 = 8  <=>  N = 3.  Unique.")

    # Integer scan for both locks, N = 2..1000.
    flow_hits = [n for n in range(2, 1001) if Fr(n - 1, 2 * n * n) == Fr(1, n * n)]
    twof_hits = [n for n in range(2, 1001) if comb(n * n, 2) == 4 * n * n]
    print(f"\ninteger scan 2..1000: LOCK-FLOW hits {flow_hits}, LOCK-2F hits {twof_hits}")

    print("""
CENSUS:
    M1: the primary branch<->carrier identification (q = 1/N). On the doc's
        own one-graph parametrization this is the definition of the branch,
        not an independent hit; at most it is ONE small-rational coincidence
        (1/3 = 1/3), whose chance level is quantified in TEST D.
    M3: REDUNDANT given M1 (definition DeltaPi/R = q/2).
    M5: REDUNDANT given M4 (definition).
    M2: with M1, reduces to LOCK-FLOW  (N = 3, unique).
    M4: with M1, reduces to LOCK-2F    (N = 3, unique).

PARAMETRIZATION ROBUSTNESS (verifier amendment 2026-06-10): the spectrum
doc's section-7 general-N family (q=1/N) is one choice; the pre-spectrum
doc's own rank-one activation law gives q=(N-2)/N instead. Under THAT
family M1 becomes the lock ((N-2)/N = 1/N <=> N=3) and M2 its arithmetic
twin, while the two-form lock becomes (N-2)(N^2-1)=8, still uniquely N=3.
The census LABELS are reading-dependent; the COUNT of two independent
locks, both uniquely N=3, is invariant under both natural families.

VERDICT A: the five-fold consilience carries exactly TWO independent
nontrivial locks (LOCK-FLOW, LOCK-2F), both selecting the metric-forced
N = 3, plus one primary identification and two definitional redundancies.
The two-lock count is robust to the choice of general-N parametrization.
""")


# ----------------------------------------------------------------------
# TEST B: generalized-N classification of later celebrated identities
# ----------------------------------------------------------------------

def test_b():
    header("TEST B: forced vs contingent classification (sections 15, 28, 38, 40-42)")

    q, N = sp.symbols("q N", positive=True)
    eta = (q / 2) / N
    eta2 = eta / 2
    s_c1 = q**2 / (4 * (1 - 2 * q))      # unprojected C1 action S_C1/R
    dim_t8 = N**2 - 1
    dim_a = N * (N - 1) / 2              # antisymmetric so(N) block (A3 at N=3)
    dim_s = N * (N + 1) / 2 - 1          # symmetric-traceless block (S5 at N=3)
    dim_l2 = N**2 * (N**2 - 1) / 2

    # gl(N) facts used (generic, any N): commutator image = traceless sector;
    # B B^T = N * P_traceless (adjoint Casimir). The isotropy constant is N.

    # B1 (section 15): pushforward of the domain weight equals the
    # unprojected C1 action:  eta/2 * N  ==  S_C1/R.
    sols_b1 = sp.solve(sp.Eq(eta2 * N, s_c1), q)
    print(f"B1 (sec 15) eta/2 * N == S_C1/R  ->  q in {sols_b1}  (ALL N)")
    print("    Reduces to 1-2q = q <=> q = 1/3 identically in N: it is a")
    print("    restatement of the already-banked q=1/3, NOT new N=3 evidence.")
    print("    (B B^T = N P is generic gl(N) adjoint-Casimir arithmetic.)")

    # B2 (section 15): total image weight == active three-form fraction.
    #   (N^2-1) * S_C1/R  ==  C(N^2-1,3)/C(N^2,3) = (N^2-3)/N^2   at q = 1/3.
    lhs = (dim_t8 * s_c1).subs(q, sp.Rational(1, 3))
    rhs = (N**2 - 3) / N**2
    sols_b2 = sp.solve(sp.Eq(lhs, rhs), N)
    sols_b2 = [s for s in sols_b2 if s.is_real and s > 0]
    print(f"\nB2 (sec 15) total T8 image weight == Lambda^3 active fraction")
    print(f"    (N^2-1)/12 == (N^2-3)/N^2  ->  N in {sols_b2}")
    print("    NOT N=3-specific: also holds at N=2 (both sides 1/4).")

    # B6 (sec 28): global residual == trace-kernel fraction of Lambda^3.
    #   1 - (N^2-1)/12 == 3/N^2  -> same polynomial as B2.
    sols_b6 = sp.solve(sp.Eq(1 - dim_t8 / 12, 3 / N**2), N)
    sols_b6 = [s for s in sols_b6 if s.is_real and s > 0]
    print(f"\nB6 (sec 28) global residual 1/3 == Lambda^3 trace-kernel fraction")
    print(f"    1 - (N^2-1)/12 == 3/N^2  ->  N in {sols_b6}  (same poly as B2;")
    print("    also holds at N=2).")

    # B5 (sec 28): overlap rank == repeated antisymmetric image.
    overlap = 2 * dim_a + dim_s - dim_t8
    forced = sp.simplify(overlap - dim_a) == 0
    print(f"\nB5 (sec 28) local image sum - global image == dim A:  identically "
          f"{forced} for ALL N")
    print("    The '11 - 8 = 3 = repeated A3' structure is generic gl(N)")
    print("    arithmetic, hence FORCED, hence 'overlap action = W(A3)' too.")

    # B7 (sec 28): local residual == image unit (S_C1/R).
    #   domain total - (local image count)*(image unit) == image unit,
    #   with domain unit = eta/2 and image unit = N*eta/2 (B1-forced).
    local_count = 2 * dim_a + dim_s
    cond = sp.Eq(dim_l2 * eta2 - local_count * N * eta2, N * eta2)
    sols_b7 = sp.solve(cond.subs(q, sp.Rational(1, 3)), N)
    sols_b7 = [s for s in sols_b7 if s.is_real and s > 0]
    print(f"\nB7 (sec 28) local residual == S_C1/R  ->  N in {sols_b7}")
    print("    N=3-specific given q=1/3 -- but once LOCK-2F has banked N=3,")
    print("    it is downstream-forced, not independent evidence.")

    # B3 (sec 38): trace-kernel load == q * W(T8).
    #   (N^2-1)*eta/2 == q * (N^2-1) * S_C1/R.
    cond = sp.Eq(dim_t8 * eta2, q * dim_t8 * s_c1)
    sols_b3 = sp.solve(cond.subs(q, sp.Rational(1, 3)), N)
    sols_b3 = [s for s in sols_b3 if s.is_real and s > 1]  # N=1: dim T8=0, degenerate
    print(f"\nB3 (sec 38) trace-kernel load == q * W(T8)  ->  N in {sols_b3}"
          f"  (N=1 excluded: degenerate)")
    print("    Given B1 (forced), reduces exactly to qN = 1, i.e. the M1")
    print("    identification again. No new content beyond M1.")

    # B4 (secs 40-42): quotient completion 1/9 + 2/9 + 6/9 = 1.
    anchor = 1 / N**2
    bridge = dim_t8 * eta2
    active = dim_t8 * N * eta2
    total = sp.simplify((anchor + bridge + active).subs(q, 1 / N))
    print(f"\nB4 (secs 40-42) scalar anchor + trace bridge + active image = "
          f"{total}  (at q=1/N, all N)")
    sols_b4 = sp.solve(sp.Eq(total, 1), N)
    sols_b4 = [s for s in sols_b4 if s.is_real and s > 1]  # N=1 degenerate
    print(f"    == 1  ->  N in {sols_b4}: downstream of the banked locks")
    print("    (generalized polynomial (N-3)(N^2-1)=0, not LOCK-2F's N^2-9=0;")
    print("    no new lock either way).")

    print("""
VERDICT B: of the celebrated post-section-6 identities, NONE adds an
independent lock beyond TEST A's two:
    B1 forced (restates q=1/3);  B3 reduces to M1;  B4 reduces to LOCK-2F;
    B5 forced for all N (generic gl(N));  B7 downstream of the banked locks;
    B2/B6 are the SAME polynomial and are not even N=3-specific (N=2 works).
The later sections are internally consistent arithmetic unfolding of the two
locks -- valuable as structure, but carrying no additional selector evidence.
""")


# ----------------------------------------------------------------------
# TEST C/D: naming multiplicity and rational coverage (chance level)
# ----------------------------------------------------------------------

def ladder_expressions(coeff_max):
    """All values a*d1/(b*d2) with a,b in 1..coeff_max, d1,d2 ladder atoms.

    Representations are deduplicated by canonical key (d1, d2, a/b in lowest
    terms) so trivial rescalings like 2*1/(2*36) vs 1*1/(1*36) are counted as
    ONE name, not two.
    """
    atoms = list(LADDER_ATOMS)
    out = {}
    for a in range(1, coeff_max + 1):
        for b in range(1, coeff_max + 1):
            for d1 in atoms:
                for d2 in atoms:
                    v = Fr(a * d1, b * d2)
                    key = (d1, d2, Fr(a, b))
                    out.setdefault(v, set()).add(key)
    return out


def test_cd():
    header("TEST C: naming multiplicity of headline values")

    # Strict grammar = the forms actually used in the doc's matches
    # (a, b in {1,2}); generous grammar allows a, b in {1..4}.
    strict = ladder_expressions(2)
    generous = ladder_expressions(4)

    targets = [Fr(1, 3), Fr(1, 9), Fr(1, 6), Fr(1, 18), Fr(1, 36),
               Fr(1, 12), Fr(1, 4), Fr(5, 12), Fr(2, 3), Fr(2, 9)]
    print(f"{'value':>8} | strict reps | generous reps | sample (strict)")
    print("-" * 72)
    for t in targets:
        s_reps = sorted(strict.get(t, set()))
        g_reps = strict.get(t, set()) | generous.get(t, set())
        sample = ", ".join(f"({c})*{d1}/{d2}" for d1, d2, c in s_reps[:3])
        print(f"{str(t):>8} | {len(s_reps):11d} | {len(g_reps):13d} | {sample}")

    print("""
Counts are deduplicated (trivial a/b rescalings count once). Two-sided
finding:
  - AGAINST naming specificity: most values have several strict-grammar
    names (1/9 is equally 1/End(H1), T8/(2*L2End), L2T8/(2*L4End); 1/3 has
    7; 2/9 has 4). For these, the chosen name is interpretation.
  - FOR the two-form selector specifically: 1/36, 1/12, and 5/12 have a
    UNIQUE strict-grammar name each, and all three route through
    Lambda^2 End(H1) = 36 (1/36, 3/36, 15/36). The eta/2 <-> L2End naming
    is the most specific naming in the whole ledger -- consistent with the
    doc's choice of Lambda^2 End(H1) as the first selector candidate.
Only a functional derivation (which the doc itself flags as the open gap)
upgrades any name from interpretation to result.
""")

    header("TEST D: expressibility coverage (chance level for an exact match)")

    def coverage(exprs, targets):
        hit = [t for t in targets if t in exprs]
        return len(hit), len(targets)

    # Target family 1: unit fractions 1/2 .. 1/120.
    t1 = [Fr(1, m) for m in range(2, 121)]
    # Target family 2: all reduced p/q with 0 < p < q <= 36.
    t2 = [Fr(p, qq) for qq in range(2, 37) for p in range(1, qq)
          if Fr(p, qq).denominator == qq]
    t2 = sorted(set(t2))

    for name, exprs in [("strict (a,b<=2)", strict), ("generous (a,b<=4)", generous)]:
        h1, n1 = coverage(exprs, t1)
        h2, n2 = coverage(exprs, t2)
        print(f"{name:18s}: unit fractions 1/2..1/120 covered {h1}/{n1} "
              f"({Fr(h1, n1)} ~= {h1/n1:.2f})")
        print(f"{'':18s}  reduced p/q, q<=36     covered {h2}/{n2} "
              f"({Fr(h2, n2)} ~= {h2/n2:.2f})")

    h2s, n2s = coverage(strict, t2)
    p_one = Fr(h2s, n2s)
    print(f"""
Chance level: under the STRICT grammar, a randomly chosen small rational
(reduced, denominator <= 36) is exactly expressible with probability
~{float(p_one):.2f}. For the TWO effective independent locks of TEST A, the
naive chance of both matching is ~{float(p_one)**2:.2f} -- i.e. of order one
in {round(1/float(p_one)**2)}. Suggestive, NOT decisive. For the claimed FIVE
matches treated as independent the naive chance would be
~{float(p_one)**5:.1e}; TEST A shows that treatment is not available.
""")


# ----------------------------------------------------------------------
# TEST E: residual-ledger look-elsewhere
# ----------------------------------------------------------------------

def test_e():
    header("TEST E: residual-ledger look-elsewhere (sections 27, 34-37)")

    # Any two-form channel residual is d*(1/36) - r*(1/12) = (d-3r)/36 with
    # block domain d <= 36 and image rank r <= 8: k = d-3r in [-23, 36].
    lattice = [Fr(k, 36) for k in range(-23, 37)]

    inst = set(INSTRUMENTS)
    level1 = set([Fr(0)]) | inst | {-v for v in inst}
    prods = {a * b for a in inst for b in inst}
    comps = {1 - v for v in inst}
    level2 = level1 | prods | {-v for v in prods} | comps | {-v for v in comps}

    n1 = sum(1 for v in lattice if v in level1)
    n2 = sum(1 for v in lattice if v in level2)
    print(f"residual lattice size: {len(lattice)} (k/36, k = -23..36)")
    print(f"nameable at level 1 (0, +-instrument):            {n1}/{len(lattice)}"
          f"  ({n1/len(lattice):.2f})")
    print(f"nameable at level 2 (+ products, complements):    {n2}/{len(lattice)}"
          f"  ({n2/len(lattice):.2f})")

    actual = {
        "trace^T8 load": Fr(2, 9),
        "A3^A3 residual": Fr(-1, 6),
        "A3^S5 residual": Fr(0),
        "S5^S5 residual": Fr(1, 36),
    }
    print("\nactual residuals/loads and their available names:")
    lvl1_hits = 0
    for label, v in actual.items():
        names = []
        if v == 0:
            names.append("balanced")
        for iv, nm in INSTRUMENTS.items():
            if v == iv or v == -iv:
                names.append(("-" if v < 0 else "") + nm)
        is_lvl1 = bool(names)
        lvl1_hits += is_lvl1
        for a in inst:
            for b in inst:
                if a * b == abs(v) and a <= b:
                    names.append(f"product {a}*{b}")
        print(f"    {label:16s} = {str(v):>6} : level-{1 if is_lvl1 else 2}, "
              f"{len(names)} names "
              f"({'; '.join(names[:4])}{'...' if len(names) > 4 else ''})")

    f1 = n1 / len(lattice)
    f2 = n2 / len(lattice)
    joint = f1 ** lvl1_hits * f2 ** (len(actual) - lvl1_hits)
    print(f"""
The four channel residuals/loads are forced by gl(3) arithmetic; the only
test is whether the forced values land on nameable lattice points.
{lvl1_hits} of 4 are level-1 instruments; the rest need level-2 products.
Naive joint chance for the observed pattern: ~{joint:.3f} (f1^{lvl1_hits} *
f2^{len(actual) - lvl1_hits}). Non-independence caveat: the residuals are
constrained to sum to 1/12, which is itself FORCED (36 - 3*11 = 3), so the
sum carries no evidence. The joint pattern is the same order as the TEST D
lock chance level: modest evidence, not closure. Note each matched value has
MULTIPLE available names (multiplicity above), so the specific name chosen
(e.g. 'eta/2' rather than 'q/2 * q/2') is interpretation, not derivation.

Null-measure caveat (verifier amendment 2026-06-10): the uniform lattice
measure is GENEROUS to the doc -- physically plausible nulls concentrate
residuals at small |k| (the observed ones are k = 8, -6, 0, 1), where
instrument density is highest, so accidental nameability is cheaper than
the uniform figure. Read 'modest evidence' as a CEILING.

What the numerics CANNOT evaluate: the doc's typed closure claims (sec 36)
assign each residual a boundary role with matching TYPE (momentum vs
transfer vs load). Type-matching is a real extra constraint beyond value-
matching, but it is qualitative; it needs the functional derivation the doc
itself lists as the open gate, not more value identities.
""")


# ----------------------------------------------------------------------
# TEST F: integer fingerprint coverage
# ----------------------------------------------------------------------

def test_f():
    header("TEST F: integer fingerprint coverage 1..200 (36/63/84/108/180)")

    atoms = list(LADDER_ATOMS)
    expressible = set()
    for a in range(1, 6):
        for d in atoms:
            expressible.add(a * d)
    for d1 in atoms:
        for d2 in atoms:
            expressible.add(d1 * d2)
    covered = [n for n in range(1, 201) if n in expressible]
    frac = len(covered) / 200
    print(f"integers 1..200 expressible as a*d (a<=5) or d1*d2: "
          f"{len(covered)}/200 ({frac:.2f})")
    small = [n for n in range(1, 101) if n in expressible]
    print(f"integers 1..100: {len(small)}/100 ({len(small)/100:.2f})")
    for n in [36, 63, 84, 108, 180]:
        ok = n in expressible
        forms = []
        for a in range(1, 6):
            for d in atoms:
                if a * d == n:
                    forms.append(f"{a}*{d}")
        for d1 in atoms:
            for d2 in atoms:
                if d1 * d2 == n and d1 <= d2:
                    forms.append(f"{d1}*{d2}")
        print(f"    {n:>4}: {'expressible' if ok else 'NOT expressible':>16} "
              f" {('(' + ', '.join(sorted(set(forms))[:5]) + ')') if forms else ''}")

    print("""
A noticeable fraction of small integers is ladder-expressible at trivial
complexity, so an integer fingerprint match per se carries only a couple of
bits. 63 = 9*7 is NOT expressible (7 is a filter denominator, not a
constructed dimension) -- independently confirming the doc's own
'63 remains weaker' verdict.
""")


# ----------------------------------------------------------------------

def main():
    print("null_test_dimension_ladder.py -- dimension-ladder null/look-elsewhere audit")
    print("date: 2026-06-10; new audit file; alters nothing existing")
    test_a()
    test_b()
    test_cd()
    test_e()
    test_f()

    header("OVERALL VERDICT")
    print("""
1. The 'five exact matches' of the pre-spectrum dimension ladder collapse to
   TWO independent locks (LOCK-FLOW: (N-1)/(2N^2)=1/N^2; LOCK-2F:
   C(N^2,2)=4N^2), both uniquely selecting the metric-forced N=3. The other
   three matches are definitional redundancies. [TEST A]
2. None of the later celebrated identities (secs 15, 28, 38, 40-42) adds an
   independent lock: each is forced, reduces to a banked lock, or (B2/B6)
   is not even N=3-specific (holds at N=2 too). [TEST B]
3. In the strict grammar ~16% of small rationals (denominator <= 36) are
   exactly ladder-expressible, and most headline values have several
   available names. Chance level for the two real locks: of order a few
   percent (one in ~37) -- SUGGESTIVE consilience, not closure. [TESTS C/D]
4. The channel-residual matches are individually cheap (lattice nameability
   0.32 at level 1, 0.58 with products/complements); the joint pattern has
   naive chance of order a few percent -- same order as the locks. The
   typed boundary-role claims are the interesting residue, and they need
   the functional derivation, not more value identities. [TEST E]
5. Integer fingerprints carry only a couple of bits each (22-29% of small
   integers trivially expressible); 63 confirmed weak. [TEST F]

CALIBRATED STATUS: the dimension-ladder selector survives as a CANDIDATE
with two genuine, exactly-stated locks at the metric-forced N=3 -- it is NOT
the legacy dense-pi-fit failure mode (matches are exact and N=3-locked, not
tuned). But the accumulation of downstream exact identities should not be
read as accumulating evidence: they are arithmetic consequences of the two
locks. The selector upgrades only via the functional gate the spectrum doc
already names (derive that the C1 action acts on Lambda^2 End(H1)), not via
further value matches.
""")


if __name__ == "__main__":
    main()
