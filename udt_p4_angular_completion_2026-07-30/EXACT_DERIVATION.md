# P4 angular completion — exact derivation record (TA-1..TA-5)

Date: 2026-07-30. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
derivation). Script: `derive_angular_completion.py` — **34/34 checks, exit 0 = 30
SUBSTANTIVE zero-residual exact-SymPy checks (27 original + 3 verifier-credited:
AM1/AM3/AM4) + 4 CITATION GUARDS** (guards labeled `[guard]` in-script/stdout/JSON,
never counted as residual computations), deterministic (no floats, no randomness, no
numeric solvers, no GPU; stdout byte-identical across reruns ×3 post-amendment:
stdout sha256 382b1098…, JSON sha256 bf21ee72…), single CPU process, ~10 s wall
(< 75-min budget; **FULL DECLARED SCOPE — no scope-ladder reduction taken**: all six
sources S-A..S-F interrogated). Outputs: `angular_completion_results.json`,
`DERIVATION_STDOUT.txt`, `SELECTOR_LEDGER.tsv`, `DECISION_SURFACE_UPDATE.md`. Every
check named in `monospace` below is one of the 34.

**AMENDMENT BANNER (2026-07-30, post-verifier — verdict PASS-WITH-REQUIRED-AMENDMENTS,
A1–A6, per `VERIFIER_REPORT.md`; all applied, `CORRECTION_LAYER.md`; no pre-amendment
COMPUTED claim changed):** A1 — the "same-closer doubling" class is
**PACKAGE-INTRODUCED, UNREGISTERED, and OUTSIDE the registered R_t×S³ arena**
(same-cycle caps: det(w,w) = 0 fails the banked unimodular two-cap condition —
`AM1_same_closer_unimodularity_failure`, verifier-credited); every claim riding it
(the canon-crease M=I outcome, the ε_k10=+1 reversal, the explicit D3 p-basis) is
rescoped below. **Sharpened tension: {R-A, R-C-pointwise, banked-complete membership}
jointly unsatisfiable — under R-A with the pointwise crease reading, NO banked complete
member realizes the canon fold.** The E0-collapse is UNAFFECTED (fires in every
realized outcome, both classes — verifier-confirmed). A2 — `SB3b` re-implemented
genuinely (two independent routes). A3 — the R-A ⟹ P2 nesting installed
(`AM3_RA_implies_P2_nesting`, verifier-credited). A4 — the f_c ≠ 0 gap closed f-free
(`AM4_cap_cycle_dichotomy_f_free`, verifier-credited; banked `Tc1_fcap_registered`
cited as the independent alternative). A5 — R-D scoped (S08 corner banked-OPEN).

**Outcome class: OA2 (constrained to an exact family) carrying a CONDITIONAL OA1 core**
— under ONE typed (not derived) realization premise the selector IS derived (branch (b),
calibration pinned except p) and the induced parities are definite and CUTTING; without
that premise every source is SILENT and the 07-20 remainder stands, **sharpened to a
single named missing premise**. NOT OA1 outright (the selector rides R-A), NOT OA3
outright (the missing datum is now one typed premise, not a family), NOT OA4.
**[A1] The OA1 core's conditionality set is enlarged by one member: {R-A,
R-C-pointwise, an UNREGISTERED same-closer completion class} — the canon-crease
selection has NO banked witness domain.**

**Binding boundary (the inverted hazard, both directions — F-A1):** the TEMPTING outcome
was "free/underivable" (harmless to the massive class); the derivation reaches the
CUTTING outcome — but only CONDITIONALLY, and the package computes the exact escape (the
¬R-A branch) with the same precision. No source's silence is converted into a choice
(F-A2: S-E/S-F verdicts are SILENT and stay silent; the ¬R-A branch outputs no selector).
Full stamps travel (F-A3 — ONE firing found by the verifier and repaired: the A1
unregistered-class retag, see §5). All consequences per completion class / census
branch / pairing, none adopted (F-A4). Bank fidelity: Route P's family, K₄-honesty,
k_mod/λ oddness, the C 2+2 signature, the E08 law, the gate-(c)/(d) facts are recovered
as consistency checks (F-A5 — one item = the A1 provenance defect, corrected). No
symbolic failure (F-A6: 34/34 post-amendment, exit 0).

---

## 0. Premise ledger (chose or derived — stamped; the load-bearing premise is R-A)

| Premise | Tag |
|---|---|
| P0: fold = isometric Z₂ identification, φ→−φ, fixed surface φ=0=r_s | **CANON** (C-2026-06-10-2; C-2026-07-04-1 sector split) |
| **R-A: the completed fold's screen block is realized by (descends from) a point involution of the banked toric arena** | **TYPED, NOT DERIVED.** Without R-A all S-B/S-D conclusions are VOID and silence stands. The 07-20 "smallest missing object" (source-authorized physical readout + complete coframe lift) is exactly what would settle R-A. **[A3 NESTING, verifier-credited] R-A ⟹ P2: the derived J_real is an in-chart member-to-member map of Route P's dressing family (`AM3_RA_implies_P2_nesting`), so R-A is strictly STRONGER than P2 — not a sibling; ¬P2 ⟹ ¬R-A; granting R-A discharges ε_kmod's P2-conditionality (ε_kmod = −1 becomes R-A-unconditional); Route P's chart-escape witness doubles as a ¬R-A escape witness.** |
| R-B: the doubled cell is a member of a completion class | carried PER CLASS, none adopted (F-A4). **[A1 RETAG] The two-cap c=1 class is the BANKED complete class (unimodular cap basis → S³). The "same-closer doubling" class is PACKAGE-INTRODUCED, NOT BANKED (no banked source defines it), and OUTSIDE the registered R_t×S³ arena: same-cycle caps give det(w,w) = 0, failing the banked unimodular two-cap condition (`AM1_same_closer_unimodularity_failure`) — an S²×S¹-type toric completion, UNREGISTERED.** |
| R-C: "fixed surface" = POINTWISE-fixed codim-1 crease | **THEORY-reading** of the canon wording; the setwise-only alternative carried in parallel throughout |
| R-D: the fold conjugates the banked Killing torus to itself, hence acts on the lattice by an integral involution M; caps (degenerate-orbit loci) → caps, so M preserves the closer-line set | DERIVED under R-A (isometry maps the canonical torus to itself; metric distinguishes the degenerate loci). **[A5 SCOPE] Holds for members whose isometry identity component is the registered R_t×T² (the banked bounded family, incl. the swap-augmented c=1 stratum); the S08 corner (higher isometry not preserving the registered Hopf bundle) is banked-OPEN (`OPEN_OUTSIDE_BOUNDED_FAMILY`, higher-isometry package) — the stamp travels.** |
| R-E: A(V)=1, A radial-component-free (registered arena form) | THEORY (banked 07-28 arena registration) |
| Screen basis on the R×T² stratum = (radial, Y-horizontal) | DERIVED from the banked registered plane span(K,V) (clock=K, ruler=V; screen = orthogonal complement); slot-labeling freedom handled by `SB8` (basis-robust) |
| Linear algebra / eigen-decompositions / sign-condition solves | Category-A |

## 1. TA-1 — the banked state, exact (`TA1_banked_state_ledger` [guard])

| Layer | What is fixed | What remains |
|---|---|---|
| 07-20 `complete_coframe_seal_involution` | base block family F_b=[[0,b],[1/b,0]] forced; MULTIPLE_COMPLETIONS primary outcome; angular extensions X01 (+I) / X02 (−I) / X03 (axis continuum) all conditional; **"selector: not supplied"**; smallest missing object = physical readout + complete coframe lift | the angular/time-on selection |
| Route P (ea5d8a3) | in-chart family J=[[P,0],[R,S]], P=antidiag(p,1/p) (recomputed `S0_P_antidiagonal_forced_recompute`), S ∈ branch (a) ±I / branch (b) [[s0,0],[s1,−s0]] (`S0_branch_involutions_and_dets`: det S = the branch invariant, +1 vs −1), R in a 2-dim space (`S0_R_space_dim2_recompute`); ε_λ=ε_kmod=−1; k10 branch-split; C 2 odd + 2 even | **branch × calibration (p, s0/σ, s1) × R** — this package's target |
| Gradient seat (f521222) | cutting condition (a): the massive landing class is nonempty exactly when the SUPPLIED f/bh wall data leave an affine slope free; either definite parity on both fields collapses E0 | the f/bh parities (SUPPLIED tags) |
| Arena (07-28 audits + gates) | g=−u(c_E dt+αA)²+u⁻¹A²+q_B on R_t×S³; A(V)=1, A(Y)=f, bh=q_B(H,H), H=Y−fV; closers (V±Y)/2; **f_cap=±1 with OPPOSITE signs at the two caps** (`Tc1_fcap_opposite`); c=1 forced for complete two-cap members; plane-swap isometry ⇔ c=1 | (this is S-B's substrate) |

## 2. TA-2 — the selector interrogation (verdicts in `SELECTOR_LEDGER.tsv`)

**The load-bearing derivation (S-B, all conditional on R-A), five exact steps:**

1. **Lattice enumeration** (`SB1`): integral involutions preserving the closer-line set
   {±(V+Y)/2, ±(V−Y)/2} = exactly 6: {±I, ±D, ±W} (closer basis; antidiag(a,b) squares
   to ab·I so only ab=+1 survives).
2. **In-family cut** (`SB2`, `SB2b`): Route P's forced Q=0 (no ruler→screen mixing;
   `TC_Q_block_zero_forced` cited) requires ι\*V ∝ V. This excludes ±D — which act as
   **V ↔ Y, exactly the gate-(d) plane swap**: a genuine isometry at c=1, but NOT an
   in-family fold (the banked swap-isometry and the seal fold are now cleanly separated
   objects). Survivors: the four diagonal actions (ε_V, ε_Y) ∈ {±1}².
3. **The parity chain** (`SB3`, `SB3b`, `SB4`): ι\*A = ε_A·A with A(V)=1 forces
   ε_A = ε_V and **ε_f = ε_V·ε_Y** (exact, per case); the curvature pullback identity
   d(ι\*A) = ι\*(dA) holds in every case (no further cut) — **[A2] `SB3b` now a
   GENUINE two-sided computation** (exterior-derivative-of-the-pullback vs
   pullback-of-the-exterior-derivative, computed by independent routes with f generic;
   the original coding was lhs≡rhs by construction). ι_\*(Y−fV) = ε_Y(Y−fV)
   exactly ⟹ with the isometric identification (P0), **ε_bh = +1 for EVERY realized
   completion** — the horizontal norm is quadratic; no realized fold can make bh odd.
4. **The cap-value dichotomy** (`SB5`; f_c-gap closed by `AM4_cap_cycle_dichotomy_f_free`
   [A4, verifier-credited]): the fold's radial reflection exchanges the two deep ends.
   On **two-cap c=1 members** (the BANKED complete class; f_cap = +1/−1 OPPOSITE —
   gate (c) banked): f∘ι = ε_f·f at the ends forces ε_f = −1 — only the cap-EXCHANGING
   folds M = ±W are consistent; M = ±I would force +1 = −1. On **same-closer doublings**
   (**[A1] PACKAGE-INTRODUCED, UNREGISTERED — outside the registered arena:
   `AM1_same_closer_unimodularity_failure` shows det(w,w) = 0 fails the banked
   unimodular two-cap condition**): only M = ±I are consistent. An exact,
   class-separating dichotomy — **reproduced f-FREE by the cap-cycle argument (`AM4`):
   end-exchange forces closer-line-1 ↦ closer-line-2 (exactly ±W exchange; ±I fix), and
   a same-cycle doubling forces M to FIX its closer line (exactly ±I) — no f_c ≠ 0
   condition anywhere; independent alternative closure: banked `Tc1_fcap_registered`
   (f_cap = ±1 EXACTLY at genuine caps).**
5. **The crease selection** (`SB6`, `SB6b` — the S-D leg): fixed-set dimensions of the
   four realized folds in the 3-space: M=I: **2 (the codim-1 SURFACE)**; ±W: 1 (circle
   type, codim-2); −I: 0 (points). det(dι) = (−1)^codim verified per case. **CANON's
   pointwise-fixed SURFACE (R-C) selects M = I uniquely.** The induced screen block
   (`SB7`, `SB7b`, `SB8`, `SB8b`): S_real = diag(−1, ε_Y); at M=I this is
   **diag(−1,+1) = branch (b), s0 = −1 (mod the K₄ R23-flip), s1 = 0, R = 0 (derived
   under R-A: Killing directions map to Killing directions — no base→screen mixing),
   p FREE** (the base block is not point-realized; the η-readout caveat travels).
   s1 = 0 and the branch verdict are basis-robust (`SB8`: the conjugated reflection is
   lower-triangular iff sin2θ = 0; det S is basis-invariant).

**The structural dichotomy this exposes (per completion class, none adopted) — [A1]
restated in the verifier's SHARPENED form:** the canon-crease fold (M=I) is consistent
ONLY with the same-closer doubling class, which is **PACKAGE-INTRODUCED, UNREGISTERED,
and outside the registered R_t×S³ arena** — while the banked complete members ARE the
two-cap c=1 S³ class, and those admit NO codim-1-crease in-family fold realization at
all (their only in-family involutions are the codim-2 ±W class: ε_f = −1; branch (a)
σ=−1 for W, branch (b) for −W — violating the R-C pointwise reading). Therefore:
**{R-A, R-C-pointwise, banked-complete membership} jointly unsatisfiable — under R-A
with the pointwise crease reading, NO banked complete member realizes the canon fold.**
The escape routes are exactly three: ¬R-A; the setwise crease reading (→ ±W, parities
still definite); or registering a new completion class (none exists in the bank).
Stated as a map fact; which yields is a Charles-level call.

**Other sources:** S-A CONSTRAINS (supplies P0 + R-C; no branch alone). S-C CONSTRAINS
(no K₄ branch flip — `SB8b` + Route P cited; s0-sign is gauge) but SILENT on selection.
S-D CONSTRAINS (the codim/orientation chain — load-bearing inside S-B; det J_real=+1 on
realized branch (b)). S-E SILENT (`TA3_E07_member_map_*`: k ↦ −k both branches;
`TA3_E08_image_ruler_sourced`: the E08 stratum is not fold-invariant — its image is the
ruler-sourced mixing member c01 = p·s; consistent, non-discriminating). S-F SILENT
(`TA4_SF_wall_slot_parity_table`: slot-kill table consistent with the banked N3 census).

## 3. TA-3 — the induced parities (full stamps; per surviving outcome)

Stamps: registered positive triangular chart; banked stationary arena; premise ladder
P0 + R-A(TYPED; ⟹ P2 [A3]) + R-B(per-class; same-closer UNREGISTERED [A1]) +
R-C(reading) + R-D(R_t×T²-identity-component scope; S08 banked-OPEN [A5]); moduli mod
K₄; p free; η-caveat.

| Outcome | ε_k10 | ε_f | ε_bh | C-calibration |
|---|---|---|---|---|
| **Realized, canon codim-1 crease** (M=I; branch (b), s0=−1 mod K₄, s1=0, R=0, p free; **[A1] rides the PACKAGE-INTRODUCED, UNREGISTERED same-closer class ONLY — NO banked witness domain**) | **+1 (EVEN)** (`TA3_k10_parity_realized`: the branch-(b) shear term 2(s1/s0)k_mod vanishes at s1=0) **[A1: rides the UNREGISTERED class]** | **+1** | **+1** | 2 EVEN {c01=+p·c00, c11=−p·c10} + 2 ODD {c01=−p·c00, c11=+p·c10} (`TA3_C_action_realized_2even_2odd`, `TA3_C_calibrated_basis_eigenvectors`) — the banked 2+2 signature with the basis now EXPLICIT up to free p **[A1: the explicit D3 basis rides the UNREGISTERED class]** |
| **Realized, setwise crease, two-cap c=1 class (the BANKED complete class)** (M=±W; codim-2 fixed set — R-C-pointwise violated) | −1 on (a) [W] / +1 on (b) [−W] | **−1 (ODD)** | **+1** | per branch, same machinery |
| **Non-realized (¬R-A)** | branch-open (07-20 remainder) | SUPPLIED-free | SUPPLIED-free | calibration open |

Constants-census vs field-census (stated separately, stamps intact): on the constants
census the realized canon-crease completion leaves the constant k10 dial ALIVE
(ε_k10=+1 — this REVERSES the branch-(a)-only kill scenario Route P tabled; **[A1] the
reversal is scoped to R-A + R-C-pointwise + the UNREGISTERED same-closer class — on the
BANKED two-cap class the realized outcomes are ±W with ε_k10 = −1 on (a) / +1 on (b)**)
and forces the two ODD C-combinations (S3 lever, cited not re-derived — to 0 at R=0);
λ, k_mod kills are banked and unchanged. On the field census: λ(x), k_mod(x) odd
(banked); f(x), bh(x) forced EVEN about the walls (canon-crease outcome, UNREGISTERED
class) or f ODD / bh EVEN (two-cap setwise outcome, banked class) — **definite in every
realized outcome, both classes**.

## 4. TA-4 — consequences as map facts (no eulogy, no relief)

- **Condition (a) adjudicated** (`TA4_affine_parity_lemmas`,
  `TA4_condition_a_E0_collapse_all_realized`): the gradient-seat lemma recomputed
  (affine even-about-both-walls ⟹ slope 0; odd ⟹ killed entirely). **In EVERY
  realized outcome both f and bh carry DEFINITE parities ⟹ f1 = h1 = 0 on the massive
  landing class's affine members ⟹ E0 = L̃_fh(0,0) = 0 exactly: the massive landing
  class COLLAPSES, conditional on R-A** (+ its own banked conditions: AM-1/AM-2 stamps
  unchanged). **[A1] This consequence is UNAFFECTED by the unregistered-class retag —
  it fires in BOTH completion classes, banked and unregistered (verifier-confirmed:
  "The E0-collapse consequence is UNAFFECTED (it fires in every realized outcome, both
  classes)").** The free-slope survival route is exactly ¬R-A. Neither leg is promoted;
  the choice between them is not made here (R-A is TYPED).
- **Route P sharpened:** ε_k10 was "supplied datum decides" — now: **+1 under the
  realized canon-crease completion ([A1] which rides the UNREGISTERED same-closer
  class); −1 on the W-realization / +1 on the −W-realization of the BANKED two-cap
  class; open under ¬R-A.** The C-calibration (D3) is pinned to the explicit
  p-dependent basis above (p the ONE remaining continuous calibration; s0-sign
  K₄-gauge; s1=0; R=0) — **[A1] the explicit basis rides the UNREGISTERED class.**
  **[A3] The nesting travels here too: granting R-A discharges ε_kmod's
  P2-conditionality (Route P's ε_kmod = −1 becomes R-A-unconditional).**
- **Constants-census massive branch (triad certificate):** untouched at the computed
  level — the P1-triad certificate rides a_F = 1 ≠ 0 (banked, Route P A1-corrected
  chain) and does not consume f/bh wall parities in its banked form; any deeper
  supplied-data interaction is TYPED (not computed here — banked machinery does not
  reach it). The collapse fact above lives on the FIELD-census P1-4D landing class
  only. Both census branches carried; neither adopted (F-A4).
- **The gate-(d) swap disentangled:** the plane-swapping isometry (⇔ c=1) is V↔Y —
  provably NOT an in-family seal fold (`SB2`); prior intuitions conflating the seal
  with the swap are now separated by a computed exclusion.

## 5. Falsifier record (derivation-side)

- **F-A1 (inverted steering): not fired — structure audit both directions.** The
  cutting outcome is reached only through the explicit premise ladder, with R-A typed
  NOT derived and the ¬R-A escape stated with equal precision; the harmless outcome is
  not left vague (its exact content: the 07-20 remainder, sharpened to R-A). No step
  was chosen for the outcome it favors: the lattice enumeration, parity chain, cap
  dichotomy, and crease selection are each forced by the cited banked structure.
- **F-A2 (silence→choice): not fired** — S-E, S-F verdicts are SILENT and remain so;
  ¬R-A yields no selector (`FA2_silence_not_converted` [guard]).
- **F-A3 (stamps — TENTH-catch watch): ONE FIRING = the verifier's A1 catch,
  MEMORIALIZED WITH ITS DIRECTION.** The consequence claims riding the canon-crease
  outcome carried the stamp "same-closer class only" — but that class's PROVENANCE was
  untagged: it is package-introduced (not banked; "same-closer" appears nowhere in the
  repo outside this package) and outside the registered arena (det(w,w) = 0 fails the
  banked unimodular two-cap condition — now the zero-residual check
  `AM1_same_closer_unimodularity_failure`). **The TENTH catch of the named scope class
  (ordinal continues the gradient seat's NINTH), and this one CUT BOTH WAYS: it narrows
  the k10-dial revival (and the D3 basis) to an UNREGISTERED class, AND it sharpens the
  package's own tension finding into the jointly-unsatisfiable form.** Retagged at
  every site (ledger, tables, JSON, decision surface). All other stamps were present
  and correct (`FA3_stamps` [guard]).
- **F-A4 (census/pairing pre-emption): not fired** — per-class/per-branch statements
  throughout; no step-(3) anticipation (`FA4_per_class_statements` [guard]).
- **F-A5 (bank contradiction): ONE item = the same A1 defect** (R-B's pre-amendment
  claim that BOTH classes were "banked completion classes" — corrected). Everything
  else recomputed and recovered: the Route P family (P antidiagonal, branches, R-space
  dim, k10/C laws, λ/k_mod oddness), K₄ and its honesty operation, the E08 form, the
  C 2+2 signature, gate-(c)/(d) facts used as cited inputs. The 07-20
  MULTIPLE_COMPLETIONS verdict is REFINED (conditional selection + a named missing
  premise), not contradicted.
- **F-A6 (symbolic failure): none** — 34/34 post-amendment, exit 0, byte-identical
  reruns ×3 (was 31/31 pre-amendment; the 27 original substantive checks ALL survive;
  `SB3b` re-implemented genuinely [A2]; 3 verifier-credited checks added).

## 6. Limits that travel

(i) **Everything selective is conditional on R-A** — typed, not derived; the 07-20
smallest-missing-object is restated as this single premise. **[A3] R-A is strictly
STRONGER than Route P's P2 (R-A ⟹ P2, `AM3_RA_implies_P2_nesting`): not a parallel
sibling — ¬P2 ⟹ ¬R-A; granting R-A discharges ε_kmod's P2-conditionality; Route P's
chart-escape witness doubles as the ¬R-A escape witness.** (ii) R-C is a canon-WORDING
reading (pointwise-fixed surface); the setwise alternative is carried and changes the
selected branch set (±W) and ε_f (−1) but NOT ε_bh (+1) and NOT the condition-(a)
collapse (fires in all realized outcomes). (iii) p is free everywhere (base block not
point-realized; the η-readout caveat travels with any Lorentz statement). (iv) **[A1]
The canon-crease (M=I) selection, the ε_k10=+1 reversal, and the explicit D3 p-basis
ride the PACKAGE-INTRODUCED, UNREGISTERED same-closer class — outside the registered
R_t×S³ arena (det(w,w)=0, `AM1`); NO banked complete member realizes the canon fold
under R-A + R-C-pointwise: {R-A, R-C-pointwise, banked-complete membership} jointly
unsatisfiable.** The completion-class dichotomy is stated per class, none adopted; the
sharpened tension is a map fact for Charles, not a verdict. (v) The E0-collapse
consequence is class-independent among realized outcomes ([A1] unaffected) and
inherits ALL gradient-seat conditionality stamps (AM-1 full locked-row condition, AM-2
nondegeneracy, p0≡0 admissibility OPEN, pairing branch P1-4D). (vi) Time-on sector
untouched (banked OPEN). (vii) **[A5] R-D's "canonical torus" leg holds for members
whose isometry identity component is the registered R_t×T²; the S08 higher-isometry
corner is banked-OPEN — the stamp travels with every lattice-classification claim.**
(viii) Blind verifier pass RUN (2026-07-30, same-session-spawned, caveat travels):
verdict PASS-WITH-REQUIRED-AMENDMENTS (`VERIFIER_REPORT.md`); amendments A1–A6 applied
per `CORRECTION_LAYER.md`; same-verifier closure on the restatements OWED before the
driver banks (multi-round precedent).
