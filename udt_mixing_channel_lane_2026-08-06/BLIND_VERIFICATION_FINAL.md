# BLIND VERIFICATION FINAL — the two surviving mu claims, attacked by NEW routes

Blind adversarial verifier, 2026-08-06, branch grok. Fresh sympy; NO lane code imported.
Scripts (scratchpad, uncommitted): `bvf_claim1.py`, `bvf_claim2.py`. NOT committed.
Routes deliberately DISJOINT from the prior reviews: R1 used O(1,2) endpoint-frame attacks +
charpoly conjugation-invariance; R2 used symbolic-k Hessian at a fixed numeric instance. This pass
uses (1a) causal eigenvector labeling (eigenvalue-ordering ambiguity), (1b) exact spectral matching
C(r,s,mu) vs diag-reciprocal C(r',s',0) via the three symmetric invariants (assignment-free), and
(2) an independent leg-ratio parametrization (a_i,s_i; a1a2a3=s1s2s3=1) with order-by-order
charpoly perturbation and a form-dependency rank argument — none used before.

## CLAIM 1 — mu is a non-gauge invariant (the reciprocal-lock defect)

**Rebuilt from scratch and confirmed:** Trace = r²+1/r²+s²−mu², Inv2 = 1+r²s²+s²/r²−mu²r²,
Det = s² — all three doc values exact. lambda_time = 1/r² leaves block-charpoly residual mu²/r²,
so **lambda_time·lambda_radial = 1 iff mu = 0 (slot-1 labeling) is EXACT** — reconfirmed.
(Transcription nit, no downstream effect: doc line 27's factored charpoly writes the quadratic
constant as s²; the block det is s²/r². The doc's trace/Inv2/det and the stratum condition line 41
all use the correct value, so nothing rides on the typo.)

**(1a) Eigenvalue-ordering ambiguity.** The timelike label IS invariantly defined on the hyperbolic
stratum: the eta-self-adjoint block has one eta-timelike and one eta-spacelike eigenvector whenever
its eigenvalues are real and distinct (verified at generic instances; e.g. r=1/2, s=3, mu=1/2 gives
lam_time = 51/8−3√33/8 with eta-norm < 0). The "radial" label among the TWO spacelike eigenvalues is
NOT fixed by the spectrum alone — the only two pairings are:
  lambda_time · r² = 1  ⟺  mu = 0   (exact),
  lambda_time · lambda_blockspace = block-det = s²/r² = 1  ⟺  s = r  (mu-independent!).
So generically (s ≠ r) NO labeling choice fakes the reciprocal lock: the iff is ORDERING-ROBUST.
The ambiguity has teeth only on s = r — exactly the locus found independently by route (1b).

**(1b) Reparametrization / absorption test (the polar-decomposition attack).** Can the mu≠0 strain
spectrum equal some diag-reciprocal spectrum {1/r'², r'², s'²}? Assignment-free exact answer via the
three invariants: Det forces s' = s; then Trace and Inv2 force
    **mu²·(r−s)(r+s)/s² = 0.**
- **Generic (s ≠ r): NO absorption — CONFIRMED-DEFECT.** The mu≠0 spectrum cannot be produced by any
  mixing-free reciprocal strain; (r,s,mu) is NOT over-parametrized; mu is an independent invariant.
- **EXACT CARVE-OUT (new; missed by both prior reviews): on s = r, mu IS absorbable.** Explicit
  witness, arrow level, all exact: r = s = 1/2, mu = √7/2 ≠ 0 gives spectrum {2, 1/2, 1/4}
  (lam_time = 2, causally verified); with r'² = 1/lam_time = 1/2, s' = s, I constructed L_p, L_q with
  L^T·eta·L = eta EXACTLY (both) and **A_mu = L_q · A_diag(r',s',0) · L_p⁻¹ exactly** — an eta-
  orthogonal endpoint-frame pair that REMOVES mu, trading it into r → r'. R1's blanket "no O(1,2)
  frame pair removes mu" is therefore FALSE on s = r (R1 proved charpoly invariance, which is true,
  but charpoly-contains-mu does not preclude trading mu into r'; on s=r the trade is exact).
  Window: absorption exists iff |mu| < |1/r − r| (the inner hyperbolic window). At the boundary the
  block is a Jordan cell (verified non-diagonalizable) — no absorption; in the outer window
  mu > 1/r+s both block eigenvalues are negative (verified) — no positive diagonal spectrum matches.
- Structural reading: s = r is where the mu=0 reference strain has a DEGENERATE spacelike pair
  {r², s²=r²}; the absorption relabels which spacelike eigenvalue is "radial" vs "screen" (in the
  witness, the reciprocal partner of lam_time is a mixing-block eigenvalue and the original slot-1 r²
  becomes the screen). It exists precisely because O(1,2) contains radial↔screen rotations. If the
  physical endpoint group is instead restricted to screen-split-preserving frames, mu is non-gauge
  everywhere — but that is a SMALLER group than the one R1's gate proof used; the record cannot have
  it both ways, so the scope must be carried.

**Claim 1 verdict: CONFIRMED-DEFECT, generically — with a mandatory scope line.** mu is a genuine
non-gauge invariant and exactly the reciprocal-lock defect for s ≠ r (measure-zero exception). On the
coincidence locus s = r (screen ratio = radial ratio), with |mu| < |1/r − r|, mu is PURE GAUGE under
the same O(1,2) endpoint group the gate proof used: the strain is exactly a mixing-free reciprocal
strain in another orthonormal frame. Any future use of mu as a recorded invariant must carry
"s ≠ r" (or a justified restriction of the frame group) as scope.

## CLAIM 2 — COUPLING-INERT (the k-absorption, rank-1 structure)

Independent parametrization: legs carry ratio variables (a_i, s_i), i=1..3, with loop constraints
a1a2a3 = 1 = s1s2s3 (no potentials used); coboundary mixing m(p,q) = a·k_q − s·k_p scaled by t;
timelike eigenvalue obtained by order-by-order charpoly perturbation anchored at a² (branch-free;
independently reproduces lam = a²(1 − m²/(a²−s²)) + O(m⁴), i.e. leg depth −log a + m²/(2(a²−s²))).
Fully SYMBOLIC in the profile (stronger than both prior reviews, which fixed numeric profiles):
- O(t⁰) = 0 and O(t¹) = 0 exactly (closure for ALL profiles at k=0 — telescoping, confirmed).
- Hessian of o2 in (kP,kQ,kR): det = 0 and ALL nine 2×2 minors = 0 symbolically; H[0,0] ≠ 0
  generically ⟹ **rank exactly 1 for EVERY generic profile** — not just at R2's instance.
- Exact factorization: o2 = −(linear form in k)² / (2(s1²−a1²)(s2²−a2²)(s1²s2²−a1²a2²)·sign-carrying
  denominator) — precisely the o2 = C(profile)·l(k)² structure. solve(o2=0, kP) returns exactly ONE
  solution (rank-1 square), k=0 gives o2=0 identically, and dC/da1 ≠ 0 (profile enters ONLY as
  amplitude). Closure is a condition on k ALONE ⟹ phi unconstrained ⟹ COUPLING-INERT.
- Independent structural reason found for the rank collapse (new): the three mixing forms
  l1=(−s1,a1,0), l2=(0,−s2,a2), l3=(a3,0,−s3) satisfy det = a1a2a3 − s1s2s3 = 0 (dependency forced by
  the loop constraints), and the residual 2×2 weight determinant w1w2 + w1w3β² + w2w3α² simplifies to
  0 EXACTLY. Rank 1 is an identity of the loop constraints, not numerical luck.
- Excluded loci (poles of C, both visible in the factorization): a_i = s_i per leg and a1a2 = s1s2
  (level crossings, the a²=s² coalescence R1 flagged). Distinct from claim 1's s=r locus.

**Claim 2 verdict: CONFIRMED — COUPLING-INERT stands, now with a fully symbolic all-profile proof.**

## OVERALL

- Claim 1: **CONFIRMED-DEFECT (generic)** + NARROW exact carve-out: mu is gauge on s=r,
  |mu| < |1/r−r|, under the full O(1,2) endpoint group. Scope line is mandatory in the record.
- Claim 2: **CONFIRMED** (strengthened to symbolic generality).
- **PASS** for leaning on mu as a recorded invariant, conditional on the record carrying the s ≠ r
  scope (or an explicit, justified restriction of the endpoint frame group to screen-split-
  preserving frames, which would close the carve-out but shrinks the group below what the banked
  gate proof exercised). Doc nit: line 27 factored-charpoly constant term (s² should be s²/r²).
