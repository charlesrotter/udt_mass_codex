# BLIND VERIFIER REPORT — P4 doorway study (compact-field registration test)

Verifier: blind adversarial verifier, same-session-spawned (Claude agent; NOT a hosted
external model — caveat travels). Date: 2026-07-31. Zero prior context; contract =
`PREREGISTRATION.md` @ fd2b890 (verified contract-first in git: that commit contains ONLY
the preregistration + a LIVE.md line, committed before all derivation artifacts, which are
still uncommitted working-tree files at verification time).

## Duty 0 — RERUN

- `python3 derive_doorway_study.py`: exit 0, runtime < 1 s CPU, single process.
- Stdout BYTE-IDENTICAL to banked `DERIVATION_STDOUT.txt` (diff empty).
- Counts: 33 checks = 29 SUBSTANTIVE + 4 GUARD, 0 failures — matches the claim.
- Split audit: pending (see below).
- Forbidden-content greps: pending.

(Report built incrementally; findings appended per duty.)

## Duty 0 — completed

- Split audit: 4 GUARDS = C1c (citation: registered fields real), C2b (verdict assembly
  riding the CITED period-gate cycle census + recomputed C1d), TD3d (typed, conditional,
  F-S7 travels), TD4_three_layer_verdict (summary). All four are honestly non-computational;
  every load-bearing computation sits in a SUBSTANTIVE row. Split honest.
- Purity: no floats/randomness/numeric solvers/GPU in `derive_doorway_study.py` (grep clean).
- Forbidden content: REGISTERED-POSIT tag present in ALL five artifacts wherever C5's
  registration is stated (ledger 3x, EXACT_DERIVATION 5x, stdout 2x, JSON 3x, decision
  surface 1x). No un-negated adoption language anywhere. Hopfion/carrier appears only in
  F-D4 disclaimers and the one-way TD-4 comparison. Clean.

## Duties 1–8 — independent re-derivation (`VERIFIER_INDEPENDENT_CHECK.py`, 43 checks, exit 0)

All groups PASS on my own routes (not copies): G1 Chern via Stokes on two charts AND direct
integration (−4π both); potentials (cosθ∓1)dφ verified as σ₃−dψ_{N/S} with ψ_N=ψ+φ,
ψ_S=ψ−φ; transition ψ_N−ψ_S=2φ winding 4π/4π=1. G2 census: independent TSV parse, 104 rows,
all dets recomputed, all |det|=1, banked column matches. G3 arc-confinement kill. G4 the
full Route-B K₄ instantiated as 4×4 matrices — screen blocks {I,−I,diag(−1,1),diag(1,−1)};
exactly TWO lie in SO(2) (the 2-torsion {±I}); triangular generators real-spectrum/nilpotent;
dressing dsolve θ≡0 reproduced (matches Route D §1.5 verbatim in the banked record). G5 E08
associativity + no-torsion on my own symbols; E07 point kernel. G6 periodicity rule (incl. a
compound entry cos2θ+3sinθ); co-translation defect with MY witness x³ (residual −s³) AND
their −s² reproduced — the rule form matches Route D R3's banked exclusion (∫₀ˣ m du,
residual s³/3 there) exactly. G7 two-sided-law associativity WITH the U(1) slot on fresh
generic blocks; blocks untouched; unitarity. G8 crease 2-torsion by fundamental-domain sweep
{0,π}; J05 IBP on non-polynomial witnesses (sin x, cos 2x, x²+3x); F-D5 lattice-vs-point.
G9 TD-3: N=2 telescoping re-derivation — increment = c₁L₁+c₂L₂+J₁+J₂ exactly; the 2π enters
ONLY through e^{iΔ}=1 on the registered target (genuine, not inserted); real-target contrast
= single hyperplane (banked form); ℤ-indexed family; slopes absorb any (L,n) — the
no-unconditional-cut claim is REAL freedom, correctly scoped, with J05 named as the coupling
seat. Hom(D∞,ℤ)=0; torsion revival both directions (2P=0⇒P=0 over ℝ; z²=1⇒{±1} over U(1)).
G10 π₂(S¹)=0 (lift + null-homotopy endpoints); σ₁²+σ₂² = dθ²+sin²θdφ², ψ-independent;
equatorial |n|=1.

## Duty 9 — falsifier hunts

- F-D3 (FIRST): stamps present — standing block in EXACT_DERIVATION §stamps; per-row stamps
  column in the ledger (posture/census/completion/arena carried; TD3 rows cycle-stamped;
  ε_θ conditionality stamped on the crease datum). No unstamped claim found.
- F-D1: the four failures carry exact obstruction forms of comparable depth to the C5 pass
  (Chern class; cap kill; spent-as-gauge with the chart-intersection computation; group-level
  real-spectrum/solvable). Dismissed-promotion hunt: (a) the fiber phase restricted to the 1D
  cell WOULD trivialize — the record correctly routes this to C5 ("promotion = adding a
  field") rather than suppressing it; (b) C3 promotion via unfixing chart/anchor is typed as
  a footing change, consistent with E02/Route D being THE banked registration. No suppressed
  promotion path within the banked footing found.
- F-D2: every legality re-derived by me from the banked rules; none asserted. Requirement-
  for-requirement vs Route D's grade (class/orbits/quotient/cocycle/alphabet/response-typing):
  coherence=C5a (lift-independence), cocycle=C5c, alphabet=C5a/C5b, slots=C5e, parity=C5d;
  the ORBITS/QUOTIENT leg has no banked action on θ other than K₄/parity (covered by C5d) —
  arguably vacuous, see Observation O2. The frozen contract's TD-2 list is exactly the five
  run. No waiver against the CONTRACT.
- F-D4: clean (greps + one-way structure verified; π₂ carrier vs π₃ hopfion never conflated).
- F-D5: adjudicated BOTH ways — C5 pass verified independently; C3 correctly recorded as the
  counter-case (anchored dressing ≡ 0 adds no invariant content, targets stay real).
- F-D6: no bank contradiction. Critically for the REVIVAL claim (attack 5): the banked
  vacuity proof is EXPLICITLY scoped to real targets — period-gate TP-1 table says "VACUOUS
  for closed real forms (nP=0 ⇒ P=0)" and limit (vii) says the D∞ theorem is "for CLOSED
  REAL one-forms; twisted/equivariant coefficients would need their own computation (typed)".
  The flip is the named target-dependence made concrete: over ℝ/2πℤ, 2P≡0 mod 2π ⇒ P∈{0,π}
  (two classes, e^{iP}=±1), consistent with the C5d crease datum. NOT a contradiction.
- F-D7: no symbolic failure; exit 0 both scripts.

## Duty 10 — contract compliance

TD-1: run, all four candidates, exact verdicts, period-gate obstructions confronted (C1d/C2
recompute the census; C3c recomputes Route D §1.5). TD-2: run at the contract's five-
requirement grade, zero-residual where computational. TD-3: run — which cycles (quotient:
zero; cyclic: the winding family; torsion: ℤ₂ revival; J11: conditional lattice) and which
parameters (conditional lattice at fixed slope; NO unconditional cut — both directions
witnessed). TD-4: three layers, map facts, one-way. TD-5: decision surface present, fork
stated, no recommendation, declining-costs-nothing stated, catalog language conditional
("COULD be ℤ-indexed... one adoption + one derived coupling away — both gated"). Ceiling
honored: nothing adopted, no spectrum claimed. `AUDIT_REPORT.md` is a prereg deliverable
not yet present — expected post-verifier per the period-gate precedent; owed before commit.

## Observations (non-blocking; no amendment REQUIRED)

- O1 (C5c triviality caveat): "the law ADMITS a central U(1) factor" is satisfiable by ANY
  associative law (direct-product adjunction) — the row's discriminating content is the
  base-law associativity re-proof plus the C3b/C4 owned-nowhere result; the record already
  says ADJOINED-not-owned and hangs the REGISTERED-POSIT tag on exactly that. Accurate, but
  future readers should not read C5c alone as evidence the theory invites a U(1).
- O2 (grade naming): Route D's grade had an orbits/quotient leg; for θ the only banked
  actions are K₄/parity (analyzed in C5d) — the leg is vacuous-or-absorbed, and the frozen
  contract defined the five-requirement list pre-derivation, so nothing was waived; if a
  future coupling ties θ to screen data, the dressing/orbit question re-opens with it.
- O3 (K₄ = real points of U(1)): the identification is of CHARACTER VALUES {±1} and of the
  chart-surviving subgroup {I,−I} — K₄ itself (order 4) does NOT embed in the circle; two of
  its four screen blocks (diag(−1,1), diag(1,−1)) are det=−1 non-circle members. The
  artifacts' wording ("characters", "2-torsion shadow") stays on the right side of this;
  the lay phrase "one structure seen through the chart" should be read with O3.
- O4 (C2a formal thinness): the SymPy content of C2a is thin (a period integral and a
  lattice-point fact); the load is carried by the NAMED Category-A invariance step — same
  convention as banked precedents; honest because named.

## VERDICT: **PASS**

Rerun clean and byte-identical; 33 checks with an honest 29+4 split; every attack-priority
leg independently re-derived and confirmed; all seven falsifiers hunted, none fires; the
contract's targets, ceiling, and outcome classification (OD-4 mixed) are faithful to what
the algebra shows. The C5 registration, the first live integer condition (with its honest
no-unconditional-cut scoping), the C3 spent-as-gauge finding, and the ℤ₂ revival all
survive adversarial re-derivation. Observations O1–O4 are calibration notes, not defects.

## OBSERVATIONS CLOSURE (blind verifier, same-session-spawned; 2026-07-31; not a hosted external model)

Closure confirmation on the finishing pass — attacked, not confirmed:

1. RERUN: exit 0; 35 checks = 31 SUBSTANTIVE + 4 GUARD; stdout matches regenerated
   `DERIVATION_STDOUT.txt`; deterministic (JSON sha 8d1a9248… reproduced across my reruns;
   stdout sha 074a3bae… matches CORRECTION_LAYER). Diff of new vs verification-time stdout:
   ONLY the two credited checks added and the three O1/O3/O4 detail annotations — no other
   line changed. I extracted every check CONDITION from the updated script and compared
   against the verification-time script held in my context: ALL pre-existing conditions are
   character-identical; the two additions are faithful reproductions of my G1 (Stokes on
   ψ_N=ψ+φ/ψ_S=ψ−φ + route-agreement conjunct) and G9 (telescoping increment, 2π-provenance
   certificates, real-target contrast, ℤ-family, slope-absorption) computations.
2. O1 installed at all three C5c sites (script detail, EXACT_DERIVATION bullet, ledger
   stamps); O2 at the grade-comparison sites (C5 verdict + ledger `overall`); O3 at the
   identification sites (script C3b detail, EXACT_DERIVATION C3b, ledger row, AND the
   DECISION_SURFACE lay phrase now reads "read with O3…"); O4 at the C2a sites. All are
   bracketed NOTES attributed to the verifier; none alters a verdict, condition, or stamp.
3. CORRECTION_LAYER's did-NOT-change list verified by inspection: the five candidate
   verdicts, the integer condition + no-unconditional-cut scoping, the revival flip, TD-4's
   three layers, and the ceiling are all byte-level intact in ledger + EXACT_DERIVATION
   (only annotations appended). `VERIFIER_INDEPENDENT_CHECK.py` preserved verbatim (still
   43 checks, exit 0). AUDIT_REPORT faithful: contract-first at fd2b890, 43-check
   independent script, credited strengthenings listed (including the credited-not-recoded
   set), PASS with the same-session/not-external caveat traveling, adoption = Charles's,
   J05 = the named next derivable object, declining-costs-nothing stated.

**CLOSURE VERDICT: CLOSED.**
