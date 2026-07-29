# BLIND VERIFIER REPORT — Route D (field-census registration test)

Verifier: blind adversarial verifier, **same-session-spawned** (zero prior context;
worked only from the package artifacts, the banked upstream packages, git, and its own
computations; **not a hosted external model** — the same-session caveat travels with this
record per repo discipline). Date: 2026-07-29.
Target: `udt_p4_routeD_field_registration_2026-07-29/` (claimed outcome OR2 — REGISTERS,
both sectors, Route-B-Stage-1-analog grade).
Independent script: `VERIFIER_INDEPENDENT_CHECK.py` (this package; preserved; 15/15,
exit 0; own constructions throughout — different witnesses/instances from the
derivation's).

## VERDICT: **PASS** (no required amendments; three observations below, none blocking)

The steering duty was run BOTH directions. The contract's tempting outcome was FAILS;
the result is REGISTERS, so the live risk was a FALSE-CLEAN — I attacked the success
side hardest: I attempted to CONSTRUCT obstructions and residual gauge elements the
registration would have missed, including x-dependent ones. Every attack died by exact
computation. I also audited the pass for glossing (conditions stated weaker than the
constant branch's banked analogs; overclaimed dissolution; smuggled parity) and found
none.

## Duty 1 — rerun / contract-first / split

- **Contract-first VERIFIED in git:** `PREREGISTRATION.md` is in commit faf9294
  (2026-07-29) which contains ONLY the two route preregs + a LIVE.md line; all six
  derivation artifacts are untracked (post-contract). Frozen before derivation: genuine.
- **Rerun ×2:** exit 0 both times; stdout, `routeD_results.json`,
  `REGISTRATION_LEDGER.tsv` all **byte-identical** across reruns AND identical to the
  committed package copies (`DERIVATION_STDOUT.txt` matches rerun stdout byte-for-byte).
  Runtime ~2.5 s CPU — full declared scope, no scope-ladder reduction (consistent).
- **36/36 = 29 substantive + 7 guards, split AUDITED:** counted independently from
  stdout and the script. The 7 guards (S0_conventions, R2_requirement_typed,
  R3_declared_entries, R4_typing, R5 two verdicts + map-fact restatement) are all
  genuinely definitional/citation/verdict-assembly bookkeeping with `ok=True`, labeled
  `[guard]` in-script, stdout, and JSON, and excluded from the substantive count. No
  substantive check is a disguised guard; every substantive check computes a real
  zero-residual condition.
- **Exact SymPy only:** grep clean — no floats, no `evalf/nsolve`, no randomness, no
  network, no GPU.

## Duty 2 — independent re-derivations (all 15/15 PASS; own constructions)

- **Gauge-law provenance (V1):** re-derived from scratch on generic Function-valued
  matrices: (LE)′ = (LXL⁻¹ + L′L⁻¹)(LE) identically; metric-equality congruence exact.
  The connection-type law is DERIVED from the banked class definition (E′ = X(x)E,
  which I verified is the banked Route-D spec **verbatim** in
  `udt_p4_bookkeeping_forcing_2026-07-29/RESIDUAL_DECISION_SURFACE.md`, committed at
  38577c9 — the spec is banked, not a choice; F-R2 clean).
- **Stabilizer/K₄ chain (V2a–V2d), with outside-K₄ construction attempts:**
  - Image-span/screen-plane and block-diagonal forcing re-derived with my own algebra
    (own Gröbner reduction, own adjugate route). The key structural point checks out
    independently: V-preservation comes from member DIFFERENCES, where the connection
    term cancels exactly — so it is a derivative-free pointwise condition, and no
    x-dependent term can hide in it.
  - **ATTACK 1 (x-dependent screen rotation):** I required
    (R(θ)KR(θ)⁻¹)[0,1] + θ′ = 0 for EVERY member, coefficient-wise in (k00,k10,k11).
    Exact solve: only θ ∈ {0, π} (both K₄-compatible: R(π) = −I₂ is the K₄ screen
    block) with θ′ = 0. The connection term cannot compensate because the
    triangularity defect is member-dependent while θ′ is not. Killed.
  - **ATTACK 2 (x-dependent boost, closed form):** P = exp(wA) with connection
    coefficient y: PHP⁻¹ + yA = H solves ONLY at w = y = 0 (independent H/N/A
    components). Killed — confirms the derivation's L01-loophole kill and
    `R1_GV_base_block_pinned_connection` by an independent parametrization.
  - **Mirrored quotient / patchwise flips:** L(x) = Ẽ(x)E(x)⁻¹ is automatically
    continuous (both transports are C¹ solutions with invertible values), so the
    locally-constant argument's continuity hypothesis is DERIVED, not chosen; the
    finite mirrored cell (CANON C-2026-06-10-2) is connected (an interval / its
    mirrored double), so discrete-valued ⟹ one global K₄ element. A patchwise flip
    would require a discontinuous L, which cannot arise from transports. No
    x-dependent residual element exists outside pointwise-global K₄. The K₄
    enumeration itself matches the banked Route B T1 list exactly.
- **Anchored orbits at the FINITE level (V2e — verifier strengthening):** the
  derivation's singleton leg is infinitesimal (B(x) ∈ so(1,3)); same grade as the
  banked Route B T1(a), so honestly graded — but I checked the finite level too: the
  finite orbit ODE L′ = X̃L − LX is LINEAR in L; its upper-right block is exactly
  Lu′ = HLu − LuK(x), Lu(0) = 0 ⟹ Lu ≡ 0 (Picard); Lorentz then forces block-diagonal
  pointwise; Lp′ = [H, Lp], Lp(0) = I ⟹ Lp ≡ I; the screen condition's θ ≡ 0 branch is
  the unique anchored solution (smooth RHS vanishing at θ = 0). The singleton claim is
  NOT a linearization artifact.
- **Cocycle closure on a NON-COMMUTING instance (V3 — strictly beyond the
  derivation's):** the derivation's instances (γxE21; affine diagonal) are commuting
  families; I built K(x) = diag(1,−1) + xE21 with [K(x₁),K(x₂)] ≠ 0, closed-form
  transport with Duhamel block, zero residual; segment data in-class; the two-sided
  law and reversal/loop-triviality hold EXACTLY. The transition-law closure is not an
  artifact of commuting witnesses.
- **Alphabet legality (V4):** own witnesses (m = u³): the anchored nonlocal integral
  fails co-translation (residual s⁴/4 ≠ 0), an absolute-point evaluation fails
  (residual (x₀+s)³−x₀³ ≠ 0), local jets to order 2 pass exactly. The derived
  exclusions are CORRECT and correctly two-sided (exclusions derived, not chosen).
  N1–N3 suffice at the declared grade: the only structures the field branch needs
  beyond local m-jets are (a) transports/holonomies — anchored integrals, which
  belong in the J07 transition layer exactly as the banked E08 content does in Route
  B (banked layer type, verified in Route B's ledger), and (b) wall values — the N3
  supplied-structure slots (V8-resolution analog). Nothing needed remains
  undeclarable. The N1/N2/N3 provenance quotes check out verbatim (census rows 11–14
  fork (ii); Stage-2 BR-M row "+ 7 character-typed moduli-jet arguments per jet
  order" — verified against `udt_p4_routeA_stage2_pointwise_reduction_2026-07-29/
  EXACT_DERIVATION.md`; forcing S7 wall term).
- **J05/J06 (V5, V6):** own density (cubic in m′) and a NON-wall-vanishing witness:
  the pointwise-row + wall-slot split is exact and the wall term is genuinely nonzero
  (so the N3 slots are load-bearing, not decorative); slot theorem with
  Function-valued kernel coefficients: Gram diag(2,2,1), R_kmod = 2f₂(x), pure-trace
  kernels k_mod-blind pointwise. Both match the derivation.
- **Registration-grade comparison, requirement-for-requirement (F-R5 duty):** Route B
  Stage 1 = T1 (law/stabilizers/quotient) + T2 (bracket/composition) + T3 (cocycle) +
  T4 (volume/L2) + T5/T6 (extension-selection questions specific to Route B). Route D
  covers T1-analog (R1), T3-analog (R2 — with items 5/6 honestly left supplied/GC,
  which I verified is EXACTLY the constant branch's banked status: Route B C4 "J07
  open for all strata", ledger rows E02/E04/E08 "stated not filled"; Route D in fact
  closes MORE of J07 for the field branch than Route B filled for the constant one),
  T4-analog (R1l, pins kept conditional), strata (§5). T5/T6 are selection questions,
  not registration requirements — correctly out of grade. The one Stage-1 layer with
  no explicit Route-D analog is **T2 (bracket/subalgebra)**: my **V7** computes it —
  [X₁(x), X₂(x)] lands in the class tangent V pointwise and is traceless, verbatim
  extension. NO banked requirement with content is dropped; **F-R5 does not fire.**

## Duty 3 — falsifier hunts

- **F-R3 (FIRST — named scope class):** full stamps travel everywhere I probed:
  standing stamps in §0 of the record + ledger header + script header (chart,
  stationary one-parameter presentation, anchor, off-shell, both-branches-carried);
  per-verdict sector + structure + stratum stamps (GENERIC + KMOD0-level-set;
  promoted loci); the TYPED-NOT-EXHAUSTED inheritances are NAMED (deeper resonance
  census, C ≠ 0 sub-variety, BR-M exhaustive parametrization, unanchored dressing
  classification); the registration GRADE itself is stamped with its not-exhausted
  layers. Instance-vs-generic legs are separately stamped (limits (i)). Not fired.
- **F-R1 (both directions):** success-side attacked by construction (this report,
  Duty 2) — no missed obstruction found; failure-side audited for glossing — no
  coherence condition is stated weaker than the constant branch's banked analog (the
  field-class stabilizer condition is the strictly stronger 12-unknown system; J07
  items 5/6 are left open at exactly the banked constant-branch status, not claimed
  closed). The E04-denominator observation carries its symmetric S1-seniority
  counter-note. Not fired.
- **F-R2:** N1–N3 are genuine declarations with verbatim banked provenance; no
  kernel, equation, or dynamics introduced anywhere in the script (audited line by
  line); exclusions derived (V4 confirms). Not fired.
- **F-R4:** grep + read: every ε_m appearance is conditional-form ("= −1 would
  force…") or SUPPLIED-tagged; no value enters any computation. The
  REGISTERED-CONDITIONAL(ε_m SUPPLIED) status on item (iv) is correctly SHARED with
  the constant branch — verified against forcing S3 (the mirror is not representable
  in-class for either branch; the seal dressing is supplied structure for both). No
  smuggled parity. Not fired.
- **F-R5:** no contradiction with the reduction theorem (the S1/S4 "unregistered"
  stamps are prior-bank provenance which this package discharges going forward — the
  correct reading), Route B (K₄/stabilizer recomputations match), the alphabet
  (anchoring rule untouched, m spectates — verified), or Slice-2b stamps (cited with
  stamps intact; the massless statement correctly kept scoped to the no-moduli-jet
  alphabet with the A1 seat DEFINED, not run). **No citation of Route P's unbanked
  results:** grep clean — the only Route-P mentions are its QUESTION and the
  swap-dressing CANDIDATE, which is banked in the forcing package
  (`ADOPTED_swap_dressing_parity_candidate`) and correctly labeled
  candidate-not-derivation. Not fired.
- **F-R6:** no symbolic failure; 36/36 ×2 byte-identical. Not fired.

## Duty 4 — contract compliance

TD-R1..R6 all addressed (R6 = `DECISION_SURFACE_UPDATE.md`). Scope ladder unused —
consistent (2.5 s runtime; both sectors derived). Ceiling respected: no census branch
adopted anywhere (both verdicts and the map-fact restatement explicitly withhold
adoption); no mass claim beyond cited map facts with stamps; DECISION_SURFACE is
recommendation-free (each item is a handle; item 3 explicitly "a construction-cost
note, not evidence"). `AUDIT_REPORT.md` is not yet present — per prereg §5 it is
scheduled AFTER this verifier pass (step 5); it is OWED before commit, not a violation
now.

## The "dissolution" audit (duty B, called out)

"Provenance asymmetry DISSOLVED" is scoped "AT THE CLASS LEVEL (pending verifier +
Charles)" and travels WITH the honest residue in both the record (§6 (a)/(b)) and the
decision surface (items 2–3): (a) exhaustive-vs-typed response parametrization
(Stage-2-analog unrun) and (b) the Slice-2b stakes attachment with the A1-clause
re-derivation seat DEFINED-not-run. That is the correct weight: S4's banked demand was
precisely "a Route-B-analog registration is REQUIRED before any response is DEFINED
there," and that is what this package supplies — no more is claimed. Not overclaimed.

## Observations (non-blocking; adoption at driver's discretion)

1. **T2-analog now on record:** my V7 (bracket layer extends verbatim pointwise) fills
   the one Route-B Stage-1 layer without an explicit Route-D check; adopting it (credited)
   would make the grade comparison airtight requirement-for-requirement.
2. **Finite-level orbit leg:** my V2e strengthens the anchored-singleton claim from
   infinitesimal to finite grade; adoption optional (the banked grade claim is honest
   as stated).
3. **Wording:** DECISION_SURFACE item 3's parenthetical "(honest, small)" — "small" is
   a mild merit adjective for the residual asymmetry; the stakes-bearing part is
   properly carried as item 2, so this is cosmetic only.

## Data for the driver

- Independent script: 15/15, exit 0, ~2.6 s; preserved as
  `VERIFIER_INDEPENDENT_CHECK.py` in-package. Nothing committed by the verifier.
- Strongest independent contributions: the two outside-K₄ construction attempts (both
  killed exactly), the non-commuting K(x) cocycle instance, the finite-level orbit
  argument, and the T2-analog bracket check.

## ADOPTION CLOSURE (same verifier, 2026-07-29 — attack pass on the finishing edits)

**Verdict: CLOSED.**

1. **Rerun:** `derive_routeD_registration.py` ×2 — exit 0 both, **38/38 = 31
   substantive + 7 guards** (counts independently verified from stdout), stdout/JSON/
   TSV byte-identical across reruns AND identical to the package copies. The two
   adopted checks reproduce my computations FAITHFULLY:
   `ADOPTED_T2analog_bracket_pointwise` is my V7 verbatim in structure (generic
   Function-valued members, all class-tangent constrained entries + trace, zero
   residual); `ADOPTED_finite_level_orbit_linear` is my V2e verbatim in structure
   (finite L-ODE upper-right/upper-left block identities computed; the Picard/
   block-diagonal/θ≡0 completion argued as named Category-A steps — exactly as in my
   original, no overstatement of what the check computes). Both correctly labeled
   substantive, credited, and set apart in an ADOPTED section.
2. **No silent drift:** JSON-level comparison of the 36 pre-adoption checks —
   **zero missing, zero changed** (name, kind, passed, AND detail strings all
   identical); only the two ADOPTED checks added; outcome class OR2 and all TD_R1–R5
   verdict fields unchanged. Ledger: all 12 statuses content-identical; only the
   count stamp and the two i-class-coherence basis strings gained the credited
   citations. `EXACT_DERIVATION.md` §1.5 grading-upgrade note and §6 grade-closure
   note state exactly what V2e/V7 established (finite-level singleton = not a
   linearization artifact; T2 bracket layer closed, T5/T6 out of grade) — no
   overclaim found. DECISION_SURFACE: "small" removed from item 3; item 2's stakes
   content (A1-seat, contract ceiling) and the no-recommendation posture untouched;
   status line correctly updated to reflect this pass.
3. **CORRECTION_LAYER (slim) and AUDIT_REPORT:** faithful to my findings — PASS /
   first no-required-amendments verdict of the arc (consistent with the commit
   history: prior packages were VERIFIED-WITH-AMENDMENT), the two killed
   constructions, the non-commuting cocycle instance, F-R1..R6 none fired, and the
   §4 did-not-change inventory is accurate. **Route P leakage re-grep: clean** — no
   citation of `udt_p4_routeP_*` artifacts or results anywhere in the package; ε_m
   remains SUPPLIED/pending-Route-P, cited as banked forcing-package content only.

No new defect. Nothing committed by the verifier.
