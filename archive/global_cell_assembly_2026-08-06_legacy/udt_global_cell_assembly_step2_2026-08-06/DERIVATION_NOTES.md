# Step-2 derivation notes — survivor-closure admissibility (LEAD / UNBANKED)

Date: 2026-08-06. Contract: `PREREGISTRATION.md` (frozen; obeyed). Status of every line:
LEAD / UNBANKED until the two adversarial reviews land. Nothing committed by this agent.

**Standing caveat (travels verbatim on EVERY claim below, per Step-1 amendment 3):**
"S (the 2026-07-01 law-set + phi-blind sources) is UNFORCED (08-06 free-data inference) but
the unique banked candidate; conditional robust across Routes A/B." All results are further
scoped: round-static Branch-P reduction, ratio level, Route-A orientation primary (Route-B
carried structurally via the regrade's C6), no G18 ruling, no mass/discreteness content.

## §0 Ground (cited at source; nothing imported as code)

- Law-set S at source (`udt_two_mirror_rigidity_regrade_2026-08-06/REGRADE_REPORT.md` R1):
  reduced Lagrangian L = (Z/2)ρ²φ'² − 2e^{−2φ}ρ'² + 2 on ds² = −e^{−2φ}c²dt² + e^{2φ}dr²
  + ρ²dΩ; arbitrary φ-blind source S(r) in the ρ-equation ONLY (the φ-EL is unsourced —
  φ-blindness means ∂L_m/∂φ = 0). EOM forms cross-checked against `cell_solver_round.py`
  (vacuum P): φ'' = 4e^{−2φ}ρ'²/(Zρ²) − 2φ'ρ'/ρ; ρ'' = 2φ'ρ' − (Z/4)ρe^{2φ}φ'².
  [step2_checks.py C1a/C1b PASS]
- Flux identity (the load-bearing object): with Φ := Zρ²φ', the φ-EL IS
  **Φ' = 4e^{−2φ}ρ'² ≥ 0** — exact, source-blind, ρ''-free. [C2 PASS]
- Shift/Z-rescale (ratio-level) lemma, verified: (φ,ρ) solves at Z ⇒ (φ−c, ρ) solves at
  Ze^{2c}; Δφ invariant. The φ(r_s)=0 canon convention (C-2026-07-02-1) is absorbable; the
  invariant content is Δφ = ln(1101). [C3a/C3b PASS]
- Cell geometry (source docs): inner end = the even-fold core at r_c with ρ_c > 0
  (`universe_cell_fold_jc_sigma_results.md`: stationarity alone pins φ'(r_c)=ρ'(r_c)=0;
  φ_c, ρ_c free). Banked center facts CITED, not re-derived: center-regular vacuum EMPTY,
  matter required (R1a center obstruction; the round solver's finite-core note). One-line
  LEAD sharpening (unbanked, follows from source-blindness of the flux identity): since
  φ-blind sources never enter the φ-EL, the R1a-type center exclusion is source-independent
  within S — the finite core is forced for ALL φ-blind matter, not just vacuum. (Offered to
  review; nothing below depends on it — the even-fold core is the source-doc geometry.)
- Fork-1 at source VERIFIED (`universe_cell_vacuum_impossibility_results.md`:148-156): the
  odd fold is the UNIQUE in-reduction survivor; its shape claim there ("Φ grows monotonically
  outward to nonzero seal flux q") is PONDER-tagged at source — DERIVED exactly below, not
  assumed. "Single-dip" appears nowhere verbatim in the source docs; the precise derived form
  is the flat-then-strictly-rising φ of §I.3 (a single dip at the core on the quotient
  doubling). Step-1's escape reading for both survivors is thereby checked, not cited.
- Generic glue at source (`udt_p4_seam_closure_derivation_2026-07-30/AUDIT_REPORT.md` +
  EXACT_DERIVATION §K6c): jump ΔΠ = q/2; well-posed iff a seam functional B with
  B'(ρ_s) = q/2 is added; B is the 07-18 OPEN object (free); flux-carrying (q ≠ 0 allowed).

## §I Closure (I): the ODD FOLD (outer, r_s: φ(r_s)=0, ρ'(r_s)=0, φ' free; inner even fold)

### §I.0 The monotone spine (exact; used by every item below)
Even-fold inner pin φ'(r_c)=0 ⇒ Φ(r_c)=0. Flux identity ⇒ Φ non-decreasing ⇒ Φ ≥ 0 on
[r_c, r_s] ⇒ sign(φ') = sign(Z) pointwise (ρ² > 0). The anchor Δφ = ln(1101) > 0 needs
φ' > 0 somewhere ⇒ **Z > 0 is FORCED by the anchor** (within S, Route-A orientation; under
the regrade's C7 flipped convention the mirrored statement holds; under Route B the monotone
object is Φ_B = Zρ²φ' + 4ρρ' per regrade C6 — see §IV caveat 5). Henceforth Z > 0.
Corollary: Φ non-decreasing with Φ(r_c)=0 ⇒ once Φ > 0 it stays > 0; Φ(r) = 0 iff ρ' ≡ 0
on [r_c, r]. So φ' = 0 exactly on an initial segment [r_c, r*] (r* := sup{r : ρ'≡0 on
[r_c,r]}, possibly r* = r_c) and φ' > 0 strictly on (r*, r_s]. **φ is flat-then-strictly-
rising** — no interior extrema, no plateaus after activation. q := Φ(r_s) = ∫ 4e^{−2φ}ρ'²
≥ 0, and q = 0 ⇔ ρ' ≡ 0 ⇔ φ' ≡ 0 ⇔ Δφ = 0. The anchor therefore FORCES q > 0 and ρ' ≢ 0.

### §I.1 Q2a anchor-carrying: YES — exact existence (IVT construction) + one witness shoot
Construction (exact, conditional on S). Fix Z > 0, r_c = 0, r_s = L, ρ_c > 0. Family
ρ_ε(r) = ρ_c(1 + ε s(r)), s(r) = sin²(πr/2L): s'(0) = s'(L) = 0 (both fold ρ-pins met),
s' > 0 on (0, L) (ρ_ε injective in the interior — used in §I.2 for σ-realizability).
Solve the φ-IVP of the flux identity from φ(0) = −ln(1101), φ'(0) = 0 (even-fold pin).
(a) Global existence on [0, L]: φ' = Φ/(Zρ²) ≥ 0 ⇒ φ ≥ −ln(1101) ⇒ e^{−2φ} ≤ 1101², so
    Φ ≤ 4·1101²∫ρ'² < ∞ and φ' is bounded — no blow-up. Exact.
(b) D(ε) := Δφ(ε) = φ_ε(L) + ln(1101). D(0) = 0 (ρ' ≡ 0 ⇒ Φ ≡ 0 ⇒ φ' ≡ 0). D is
    continuous in ε (smooth dependence of bounded ODE solutions on parameters; standard).
(c) D(ε) → ∞: suppose φ ≤ 0 throughout (else D > ln(1101) already); then e^{−2φ} ≥ 1 and
    Cauchy–Schwarz gives Φ(r) ≥ 4(ρ(r)−ρ_c)²/r. Where ρ ≥ 2ρ_c, (ρ−ρ_c)²/ρ² ≥ 1/4, so
    φ' ≥ 1/(Zr) there. With sin x ≥ (2/π)x on [0, π/2], s(r) ≥ (r/L)², so ρ = 2ρ_c is
    reached by r₁ ≤ L/√ε. Hence D(ε) ≥ (1/Z)ln(L/r₁) ≥ (ln ε)/(2Z) → ∞ — contradiction
    for ε > e^{2Z ln(1101)}. So D(ε̄) > ln(1101) at some finite ε̄. Exact.
(d) IVT: ∃ ε* ∈ (0, ε̄) with D(ε*) = ln(1101) exactly. At ε*: φ(L) = 0 (the canon
    convention lands automatically), φ'(0) = 0, ρ'(0) = ρ'(L) = 0, ρ > 0, q = Φ(L) > 0
    with φ'(r_s) = q/(Zρ_s²) free-and-output — ALL odd-fold + even-fold pins met, anchor
    carried. The source σ is DEFINED from the ρ-equation residual (§I.2). ∎ (within S)
WITNESS (the one allowed bounded CPU shoot; labeled witness, not theorem): Z = 8, L = 1,
ρ_c = 1: ε* ≈ 0.011032, q ≈ 73.69, |φ(r_s)| < 1e−9. [C7 PASS] (Note the depth
amplification e^{−2φ} ≈ 1101² at the core: a ~1% areal-radius modulation suffices.)
Step-1's fork-1 escape claim is thereby VERIFIED as an existence fact, not assumed.

### §I.2 Q2b the admitted class, exactly
𝒜_fold = { data (r_c < r_s; ρ ∈ C²([r_c,r_s]), ρ > 0, ρ'(r_c) = ρ'(r_s) = 0, ρ' ≢ 0;
Z > 0) satisfying ONE scalar condition D[ρ, Z] = ln(1101) }, where D[ρ, Z] := Δφ of the
unique φ-IVP solution from (φ(r_c) = −ln(1101), φ'(r_c) = 0). SLAVED (outputs, not free):
- φ: fully determined by ρ (and Z) via the unsourced φ-EL — one function's worth REMOVED
  by φ-blindness; source freedom cannot restore it (the φ-EL cannot be sourced within S).
- σ: the φ-blind source is read off as the ρ-equation residual of the chosen (φ, ρ) — one
  output function. Realizability: as a prescribed φ-blind S(r) it is EXACTLY the class the
  Step-1 rigidity was proven against (apples-to-apples). As an autonomous L_m: D3
  (`universe_cell_fold_jc_sigma_results.md`) realizes essentially any smooth σ along
  injective-ρ segments — our witness ρ is interior-injective; the two endpoint ρ'=0 points
  are D3's own flagged scope edge (matter kinetics enlarge the class; not settled here).
- q = Φ(r_s) > 0: an OUTPUT (fold-doc "q is an output" verified); E(r_s) = q²/(2Zρ_s²)
  forced (cited); the budget/transversality relations ride EXTRA postures (cited, unused).
- φ_c = −ln(1101), φ(r_s) = 0: the anchor + canon convention (shift/Z-rescale absorbable).
SIZE: one free function (ρ) + three constants (L = r_s − r_c, ρ_c, Z) − one scalar (the
anchor) − r-translation redundancy. A function's worth, codimension 1 in its own data.

### §I.3 Q2c constrain-or-admit-all: **S2-CONSTRAINS (proper subclass; exact cuts named)**
Relative to kinematically-free profile data (free pairs (φ, ρ), free q):
CUT-1 (from S itself, shared by any closure): φ is SLAVED to ρ — the flux identity is a
  hard functional cut that φ-blind source freedom can never relax. NOT "admits all via
  source freedom": source freedom buys every regular ρ, but no (φ, ρ) pair off the φ-EL.
CUT-2 (S + inner even fold): sign(φ') = sign(Z) pointwise — φ monotone; anchor sign forces
  Z > 0; Δφ < 0 data (e.g. the anchor with reversed sign) is INADMISSIBLE.
CUT-3 (S + inner even fold): φ flat-then-strictly-rising (§I.0) — the precise, now-derived
  form of the source docs' PONDER-tagged shape claim (single dip at the core on doubling).
CUT-4 (the odd fold's OWN cuts): ρ'(r_s) = 0 (a pointwise cut on ρ; excludes all profiles
  with seam areal drift — via the flux identity it also forces Φ'(r_s) = 0, seam-critical
  flux); and the interlock: q is NOT a free closure datum — the seam flux is fully
  determined by the interior profile (q = ∫ 4e^{−2φ}ρ'²), with q > 0 forced by the anchor.
Honest attribution (F-STEER): most constraining power lives in S + the inner fold (CUT-1..3);
the odd fold's marginal cut is CUT-4. But the closure↔profile interlock the spine asks
about is REAL and exact: the fold's seam data (q, E(r_s)) is slaved to the bulk profile.

### §I.4 Q2d L-lead placement: **OUTSIDE 𝒜_fold** (three independent exact violations)
φ_L = −(1/2)ln(1 − r/X) (A = 1 − r/X):
(i) φ_L'(r_c) = 1/(2(X − r_c)) ≠ 0 — violates the inner even-fold φ-pin for every finite
    r_c < X. (ii) The flux identity with φ = φ_L forbids ρ'(r₀) = 0 at ANY point: the
    residual there is Zρ²/(2(X − r₀)²) ≠ 0 [C5 PASS] — so BOTH ρ-pins (ρ'(r_c) = 0,
    ρ'(r_s) = 0) are unsatisfiable by any ρ. (iii) = (ii) at the seam independently.
The violations vanish only as X → ∞ (canon-blocked: no spatial infinity). See §III for the
bulk-level placement (inside-in-bulk), which sharpens "outside" to "boundary-excluded".

## §II Closure (II): GENERIC GLUE (outer, r_s: ΔΠ = q/2, B'(ρ_s) = q/2, flux-carrying)

Cell geometry unchanged (inner = even-fold core; the glue replaces only the OUTER closure).
Seam content at source (K6c, cited §0): the interior-side momentum jump ΔΠ = q/2 is
absorbed by a seam functional B with B'(ρ_s) = q/2; B is FREE (the 07-18 OPEN object);
q = Zρ²φ'(r_s) is carried (flux-carrying), not pinned; φ(r_s), ρ(r_s), ρ'(r_s) NOT pinned.

### §II.1 Q2a anchor-carrying: YES — the §I.1 witness carries verbatim
The §I.1 construction satisfies strictly more than the glue requires (it happens to have
ρ'(r_s) = 0, which the glue does not ask). At ε*: q = Φ(r_s) > 0; choose B(ρ) = (q/2)ρ
(B'(ρ_s) = q/2 exactly; B free, so this is a choice OF the closure, not a constraint ON
the profile). All glue conditions met; anchor carried. Beyond the witness, ANY member of
the §II.2 class works — existence is generic here, not tuned. ∎ (within S)

### §II.2 Q2b the admitted class, exactly
𝒜_glue = { (r_c < r_s; ρ ∈ C², ρ > 0, ρ'(r_c) = 0, ρ' ≢ 0; Z > 0) : D[ρ, Z] = ln(1101) }
— i.e. the §I.2 class with the seam ρ-pin DROPPED — together with the seam data
(q; B), where q = Φ(r_s) is an OUTPUT (slaved to the profile, one-directional: profile ⇒
seam charge, nothing back) and B is one free function of ρ constrained only by the single
point-condition B'(ρ_s) = q/2 (always solvable for any (q, ρ_s): B is free).
SIZE: one free function (ρ) + three constants − one scalar (anchor), PLUS one free
function's worth of closure data (B mod its 1-point condition) that never touches the
profile. Exact inclusion: 𝒜_fold = 𝒜_glue ∩ {ρ'(r_s) = 0} (with φ(r_s) = 0 the shared
ratio-level convention) — the fold class is a proper (codim-1 boundary-pin) subclass.

### §II.3 Q2c constrain-or-admit-all: **S2-ADMITS-ALL at the closure↔profile level**
The glue closure imposes NO pointwise or functional cut on the interior profile: every
profile admitted by {S + inner even fold + regularity + anchor} passes the glue, because
B's freedom absorbs any (q, ρ_s) via the always-solvable one-point condition. The ONLY
cuts on the profile are the closure-independent CUT-1..3 of §I.3 (φ slaved to ρ; monotone;
Z > 0 forced; flat-then-rising). Two precision notes (first-class per prereg, F-STEER —
this is the anti-spine cell and it is reported plainly):
(a) "Freedoms independent" holds in the direction that matters (closure constrains profile:
    nothing), but NOT conversely: the profile fully DETERMINES the required seam charge
    q = ∫ 4e^{−2φ}ρ'² — a one-way slaving, not an interlock.
(b) The glue does constrain the ACTION content (a seam functional B must EXIST — K6c
    well-posedness; B ≡ 0 would force q = 0 and re-enter Step-1's dead φ'=0-both-ends
    class, per the Step-1 amendment). That is a cut on the boundary action, not on the
    profile; Q2c is a profile question, so the landed class is ADMITS-ALL.

### §II.4 Q2d L-lead placement: **OUTSIDE 𝒜_glue — but only via the INNER end**
The glue seam imposes nothing, and the L-lead is bulk-realizable (§III); the exclusion is
entirely the inner even-fold pins: φ_L'(r_c) ≠ 0 (§I.4(i)) and ρ'(r_c) = 0 unsatisfiable
(§I.4(ii)). If the inner end were relaxed to a free/finite-core datum (the fold-doc's
"different class", NOT the source-doc universe-cell geometry — a fork, not a finding), the
L-lead would sit INSIDE the glue-closed bulk class. As posed on the source-doc cell:
OUTSIDE, by the inner closure alone.

## §III The L-lead in the BULK of S (characterization supporting Q2d; no closure)

With φ = φ_L, the flux identity reduces exactly to a quadratic in u = ρ'/ρ (m := X − r):
4(m/X)u² − (Z/m)u − Z/(2m²) = 0, discriminant Z²/m² + 8Z/(mX) > 0 for Z > 0, root product
−ZX/(8m³) < 0 [C6a/C6b PASS]: two real roots of opposite sign, NEITHER zero — so ρ' never
vanishes, and ρ₊ = ρ_c exp(∫u₊) > 0 exists on any compact [r_c, r_s] ⊂ (0, X) by exact
quadrature [C6c PASS]. Hence (φ_L, ρ₊, σ slaved) IS an exact S-solution in the bulk, and
Δφ_L = (1/2)ln((X−r_c)/(X−r_s)) carries ln(1101) iff (X−r_c)/(X−r_s) = 1101². PLACEMENT:
**inside the bulk solution set of S; excluded from BOTH admitted classes exactly and only
by the end/closure conditions** (every violated condition is an endpoint pin; ρ' ≠ 0
everywhere is the single bulk fact driving all of them). Owner record favored "inside"
(F-STEER): the honest verdict is outside-as-posed, boundary-excluded-not-bulk-excluded,
with the only rescue limits (X → ∞; free-core inner end) respectively canon-blocked and
outside the source-doc geometry. For Z < 0 the discriminant can turn negative (φ_L then
bulk-unrealizable) — moot, since §I.0 forces Z > 0 under the anchor.

## §IV Landed table + caveats

| Closure | Q2a anchor | Q2b class | Q2c verdict | Q2d L-lead |
|---|---|---|---|---|
| Odd fold | YES (exact IVT + witness) | 1 function (ρ), codim-1 anchor cut; φ, σ, q slaved | **S2-CONSTRAINS** (CUT-1..4; interlock: seam data slaved to bulk) | OUTSIDE (3 exact violations) |
| Generic glue | YES (same witness; generic) | 𝒜_fold's superclass (seam ρ-pin dropped) + free B (1-pt condition) | **S2-ADMITS-ALL** (closure adds no profile cut; one-way q-slaving; B-existence = action-level only) | OUTSIDE via inner end only; bulk-inside |

Overall: **S2-MIXED** (per-closure, as the prereg anticipated). Single load-bearing step,
per closure: (I) the monotone spine §I.0 (Φ(r_c) = 0 + Φ' ≥ 0), which yields every cut AND
the existence mechanism; (II) the freeness of B (K6c), which single-handedly lands
ADMITS-ALL — reviews should attack §I.1(c)'s growth bound and B's at-source freeness first.

Caveats (each travels with every claim):
1. The verbatim S-caveat of the header; everything is conditional on S and ratio-level.
2. Inner end = even-fold core is the SOURCE-DOC geometry (cited), itself a closure CHOSE
   (OC2 germ freedom); Q2c cuts 2–3 ride on it; a free-core inner end relaxes them to
   "Φ non-decreasing" only. No inner-closure ruling is made here.
3. σ-realizability: exact in the prescribed-S(r) class (the Step-1 comparison class);
   autonomous-L_m realization at the two ρ'=0 endpoints is D3's open scope edge.
4. Orientation: Route-A sign; the C7-flipped convention mirrors all signs (same squeezes).
5. Route B (structural, cited regrade C6, Z=8 tension OWED at source): the monotone object
   becomes Φ_B = Zρ²φ' + 4ρρ'; both fold ends still zero it (ρ' = φ' = 0 there), and the
   even-fold inner still gives Φ_B(r_c) = 0, Φ_B ≥ 0 ⇒ φ + (4/Z)ln ρ non-decreasing — the
   monotone CUT survives in modified form; the Q2a existence argument was NOT re-derived
   under Route B here (flagged, bounded scope).
6. No G18 ruling; no closure adopted; no mass/spectrum content (F-TARGET clean).
7. Checks: `step2_checks.py`, 10/10 PASS, exit 0 (sympy exact + the ONE bounded witness
   shoot C7, labeled witness-not-theorem). LEAD / UNBANKED pending the two reviews.

## CONSOLIDATED (2026-08-06, both reviews in): S2-MIXED SUSTAINED — AMENDED (no cell overturned)

Files: ADVERSARIAL_REVIEW_1_algebra.md (SUSTAINED; independent recomputes incl. own-method witness
shoot, all digits match + a second witness family), ADVERSARIAL_REVIEW_2_classification.md
(SUSTAINED-AMENDED; geometry-consistency adjudicated NO-STRADDLE).

**FINAL AMENDED TABLE (conditional on S = the unforced-but-unique-banked 07-01 law-set + phi-blind
sources; round-static Branch-P; ratio level; Route-A orientation, even-core inner end):**

- **ODD FOLD = S2-CONSTRAINS (thin, honestly attributed):** the closure's OWN marginal cut is the
  seam rho-pin rho'(r_s)=0 (codim-1; the fold's source-derived property — rho even => rho' odd;
  q, E_s slaved, q>0 anchor-forced => Phi'(r_s)=0). The heavier cuts — phi slaved to rho (NO
  phi-blind source can touch the phi-EL, proven symbolically); phi monotone flat-then-rising;
  anchor forces Z>0 — are S + inner-core cuts shared by every closure. ROUTE-B RIDER: pointwise
  monotonicity and anchor-forced Z>0 are Route-A results; under Route B, Z>0 is law-forced (Z=8),
  monotonicity not re-derived.
- **GENERIC GLUE = S2-ADMITS-ALL (B-UNFIXED reading; FLIP RIDER):** B'(rho_s)=q/2 is one-point
  solvable for any (q,rho_s) — no hidden cut. BUT this is the B-unfixed reading: any FIXED/derived
  seam functional B imposes the codim-1 cut q=2B'(rho_s) and FLIPS the cell to CONSTRAINS. This
  rider travels with the table; Step 3+ may not lean on ADMITS-ALL after any B derivation.
- **L-lead placement:** OUTSIDE the fold class — at BOTH ends independently (phi_L' != 0 everywhere
  kills the inner core pin; the seam residual Z rho^2/(2(X-r)^2) != 0 kills the fold's own rho-pin;
  honest count: 2 independent facts). BULK-INSIDE the glue class (exact quadrature, two real
  nonzero roots; Z<0 can close it). Rescue limits canon-blocked (verified at citations).
- **Anchor-carrying existence:** BOTH survivors carry the anchor (constructive IVT + two independent
  witness families; eps* ~ 0.011, q ~ 73.7, digits matched by an own-method re-shoot).
- **Geometry consistency (R2 item 2): NO row-1 straddle** — row 1 kills the both-ends conjunction;
  Step 2 imposes phi'=0 at one end only; the finite core (rho_c>0) is a different class from the
  killed regular center; the witness proves the class non-empty. The fold excludes L on its OWN
  seam pin, not merely via the inner-end choice (that inner-end-only reading is true only of glue).
- **Correction (safe direction):** the "finite core forced" sharpening is ALREADY BANKED (07-02
  R2, blind-verified) — re-cited as banked, not a new lead. Z>0-forced is exact, carries
  Route-A + even-core tags wherever quoted.

**SPINE READING (scoped):** within S the closure<->profile interlock is REAL but THIN (one codim-1
cut per closure at most vs the shared S-cuts); and the observed L-lead sits INSIDE the glue
universe's bulk but OUTSIDE the fold universe's class — making Step 3 (anchor/profile
discrimination) substantive, not formal. No G18 ruling here; no mass content. Same-session review
caveat travels; external bar owed for any hard bank.

## ANCHOR RE-SCOPE (2026-08-06, Charles-directed)

All Step-2 verdicts are RE-SCOPED to the anchor **"some Delta phi > 0"** (sign fixed): Q2a existence
is generic in the target (the IVT construction works for any positive span); Z>0-forced rides the
sign only; the admitted-class cuts and the L-placement facts are value-independent. The specific
value ln(1101) = the standard CMB last-scattering interpretation — a legacy import, now a separate
flagged premise (canon C-2026-07-02-1 under provenance audit). Only the witness NUMBERS (eps*, q)
and the 1101^{2Z} threshold are value-conditional.
