# HANDOFF — Resume Instructions and Perspective

> **READ `LIVE.md` FIRST** — it is the short, only-guaranteed-current file (frontier + next action).
> This HANDOFF is the detailed record; if it disagrees with LIVE.md, LIVE.md wins. (P5, 2026-06-23.)
> **CURRENT (2026-07-06 EOD-2): after LIVE.md (its RESUME-HERE = IMPLEMENT N5d Stage-2b), read the
> `## SESSION RECORD 2026-07-06 (EOD-2)` block immediately below — the N5d Stage-1 diagnosis→fix→retire→Stage-2
> design+CAS chain. Gate-0 is FULLY CLEARED + blind-verified; the next session IMPLEMENTS Stage-2b (a bounded code
> edit + 7 tests, NO pilot). The EOD-1 record (readout-map B+C → provenance floor → N5d built → Stage-1 pilot
> TOOL-LIMITED) follows it, then the 2026-07-05 EVENING record (prior session).**

## SESSION RECORD 2026-07-06 (EOD-2) (Opus 1M — N5d Stage-1 diagnosed+fixed → retired → Stage-2 co-relaxed matter DESIGNED + CAS COMPLETE + Gate-0 CLEARED)

Charles directed step-by-step; every node CAS/audit + committed & pushed on `main` (standing instruction: push on
every commit). NO pilot/verdict run this session — all DESIGN/PROVISIONAL/Outcome D. pytest 59/1xfail at close
(+11 pullback/frame tests). The one code change to physics is FIX-1 (equilibration) + Registration-B + the ρ²/2
source factor in `cell_solver_f2d.py`; Stage-2b implementation is NOT yet done (Gate-0 just cleared).

**THE ARC (each committed; docs named):**
1. **Conditioning diagnosis** (`n5d_stage1_conditioning_diagnosis.md`): the Stage-1 near-singular Jacobian = a
   COMPOUND numerical artifact (NOT a physical soft mode) — 3 stacked, all-UNOBSERVABLE near-null modes: (1) row/col
   scaling imbalance (D2 rows ~1e8, L column under-scaled; inherited from the BASE), (2) S-JC2 constant-a2 EXACT
   Neumann null, (3) stalled-state constant-φ null. All leave q/Pi/M/Hseal/nodes unchanged ≤1e-11.
2. **FIX-1** (`cell_solver_f2d.newton_lm_solve`): category-A equilibration = COLUMN scaling + damped **lstsq** (avoids
   the J^TJ cond-squaring; ROW-scaling the objective was tried+REJECTED — it stalls the solve). `equilibrate=True`
   default; `=False` = original byte-for-byte. No regression; removes contributor 1.
3. **FIX-3** structured seed = INEFFECTIVE (the round Branch-P mirror cell flattens any structured seed back to
   near-homogeneous; the L-collapse is the round-continuum closure degeneracy, not a seed artifact).
4. **Shear-forcing audit**: the ℓ=2 source is STRONG (‖rhs‖≈3) + correctly normalized; the tiny nonlinear a2 =
   the L-COLLAPSE (L 1.0→9e-3, source fixed at seed L0 while geom coeff ∝(2/L)² stiffens ~1e4×). ℓ=2 captures only
   ~17.6% of the traceless shear power (ℓ=0 dominates 81%).
5. **Pullback / Registration-B** (`cell_solver_f2d.fields` + `n5d_shear.source_interp`): the source now interpolates
   at the CURRENT-L physical r=rc+(L/2)(ζ+1) (was frozen at seed L0). +8 regression tests.
6. **ρ²/2 frame factor** (`fields` live-src path): stored `sh2` (orthonormal component) needs ×ρ²/2 to be the
   cell-frame `T_s`; CAS-derived (`n5d_frame_factor_cas.py`) + BLIND-VERIFIED (agent a83a6c…). +3 tests.
7. **Embedding audit** (`§4d/§4g`): the frozen FLAT hopfion stress is INVALID as a cell-frame source for verdicts
   (ρ≠r by up to 2×; an uncomputed (r/ρ)^{2..4} regrade; scale-incoherent). ⇒ **RETIRE Stage-1 frozen source;
   go Stage-2 co-relaxed matter.**
8. **Stage-2 DESIGN** (`n5d_stage2_corelaxed_matter_DESIGN.md`): the base `cell_solver_f2d` ALREADY co-relaxes the
   native S² winding matter f(r,θ); Stage-2 = make f feel the shear (off-round f-PDE) + source the shear from the
   LIVE matter's own T_s. π₂ tile (flagged: NOT the π₃ hopfion).
9. **Stage-2a CAS** (`n5d_stage2a_cas_results.md`, script `h4_scripts/n5d_stage2a_cas.py`): off-round f-PDE (A,B,pot
   with e^{±s}, matches base at s=0 EXACT); T_s derived; ρ²/2 emergence exact; ρ-force s-independent; φ-blind; rigid
   hedgehog 0. **The design's T_s candidate was SIGN-FLIPPED — CAS caught it.** T_s sign + then BLIND-VERIFIED
   (agent a44bfe…, §7). H audit: off-round H = base + shear-kinetic; **dH/dr=0 on-shell EXACT** (geo+shear).
10. **Stage-2b Gate-0** (`n5d_stage2b_gate0_report.md`): ran BEFORE any residual edit and CAUGHT A BLOCKER — the
    standard FS L_m gives a matter→geometry coupling **−2×** the base's (ρ-EOM matter force + H matter both −2×),
    while the f-PDE (homogeneous δS_m/δf) is unaffected. Pinned shear-kinetic **C=1/10** (matches the certified
    φ-correction + E_s_geom). HALTED implementation per Gate-0.5 rule.
11. **Gate-0.5 RESOLVED** (`n5d_stage2b_gate05_report.md`, script `n5d_stage2b_gate05.py`): the base coupling is
    **λ=−1/2**, CONSISTENT across the ρ-EOM AND H (both give −½ exactly) ⇒ a deliberate base convention (the
    𝒦-mediated/e^{2φ}/4 weight, per H4_N1), NOT an inconsistency. **Corrected live source = −(ρ²/4)T_s** (the naive
    +(ρ²/2)T_s was 2× + sign-flipped). **BLIND-VERIFIED** (agent a99914…: λ_ρ=−½, λ_H=−½, source −(1/4)ρ²T_s).

**⇒ NEXT SESSION: Stage-2b IMPLEMENTATION** — see LIVE.md RESUME-HERE for the exact pinned formulas + the 7 required
tests. Bounded code edit to `cell_solver_f2d.py` (+ `H_of_r`), delete frozen source from the residual, NO pilot, NO
verdict, NO FIX-2, π₂-only. All Gate-0 formulas are CAS + blind-verified; nothing more to derive.

## SESSION RECORD 2026-07-06 (EOD-1) (Opus — readout-map B+C → provenance floor CLOSED both sides → N5d BUILT → Stage-1 pilot TOOL-LIMITED)

Charles directed step-by-step; every node armchair/CAS + code, committed + pushed on `main`. The one coupled solve
(the N5d Stage-1 pilot) ran bounded/foreground (~1s/BC). pytest 48/1xfail at close.

**1. READOUT-MAP — two axes closed.** (a) CHANNEL-selector audit (`native_readout_map_selector_audit_results.md`,
verifier aa75efc94282e7099) → **Outcome B**: NO native target-selector from any of the 4 sources (seal/spin/φ-angular/
flux); q=1/3 UNFORCED; **solve-independent** (target-SO(3) is an exact symmetry of the backreacted functional — a
spatial pin never transmits to a target pin; L2+L4 generic-R CAS diff=0). (b) DEPTH/SIZE node (Branch P,
`native_readout_map_depth_size_results.md`, verifier ae3142d4ba6d9e825, registry **#76**) → **Outcome C**: the round
Branch-P vacuum is PROVABLY a continuum (autonomous form φ_tt+φ_t=(4/Z)e^{−2φ} = monotone runaway, node-count≡0); the
hopfion RIDES (mass=continuous whole-cell flux); native discreteness exists only as ORTHOGONAL LABELS (Q_H, D2b
depth-N). **The ONE frozen DOF that could pin size = the off-round shear h_AB (via sign-changing 𝒦 or the TT
eigenproblem) — this is exactly what N5d tests.**

**2. N5d PREFLIGHT FAILED → the provenance excavation.** Charles approved N5d with strict gates. The preflight gate
STOPPED it: **no solver implemented the native operator** — the only coupled φ+shear solver (`branchGP`/
`branch_operator.py`) ran the SUPERSEDED scalar-tensor frame (f=e^{2φ}, X=−2e5). The L_bare⁻¹ bug was FIXED
(`h4_scripts/lbare_inverse.py`, `fe85a14`; the old `green_response` inverted a different operator). This triggered:
- **kap8 = SOLE QUARANTINE** (`kap8_characterization`, registry **#77**) — a live unflagged native-micro
  identification banked on the scalar-tensor operator at X=−2e5.
- **Date-based pre-native-era census** (`pre_native_era_census.md`, 2026-06-11→07-01, 4 classifiers + 2 adversarial
  passes) — kap8 sole quarantine; the everything-on **P2/P3/P4** arc (frame B) was a SECOND undercount caught by the
  adversarial pass; W-series all retired/self-withdrawn. Organization: 10 SUPERSEDED docs → `archive/pre_native_
  coupled/` (redirect stubs), banners on CC docs, INDEX/ledger/registry pointers.
- **Macro-spine provenance pass** (`macro_spine_provenance_2026-07-06.md`, 3 classifiers + adversarial) — NO hard
  quarantine; N5d triple-confirmed unaffected. `native_dilation_weight §5-7` = SPLIT (the X=−2e5 BIRTHPLACE),
  F5 CC, AUDIT.md CC, scale_symmetry/macro_fork/weld×2/lepton_ladder SUPERSEDED. **PROVENANCE FLOOR CLOSED BOTH SIDES.**
  RESIDUAL OWED (cosmetic): W-series phase-2 physical relocation.

**3. N5d BUILT.** Build plan (`N5d_solver_build_plan.md`, approved-with-edits — frozen-source staging, both seal BCs,
BC-fork banking rule, neutral q_raw/M_readout sign convention + Gate-8, pilot-verdict scope rule). Built as an
ADDITIVE extension: `n5d_shear.py` (exact 𝒦=−½e^{−2φ}(a'bt')/(a·bt), sqrt_h, EAB_shear_row, lbare wrappers) +
`cell_solver_f2d.py` (+ℓ=2 shear DOF a₂(r), shear-EL row, S-Dir/S-JC2 BCs, q_raw/Pi_phi/M_readout with
SIGN_CONVENTION=−1) + 3 test files. commit `84287b6`; pytest 48/1xfail (existing 32 preserved — shear-off = exact
round recovery); 8 preflight gates GREEN; contamination-clean.

**4. N5d STAGE-1 PILOT = TOOL-LIMITED (Outcome D; NO A/B banked)** (`n5d_pilot.py` + `n5d_pilot_stage1_results.md`,
commit `bf54957`). Frozen REAL H3-hopfion source (Q=0.9917, virial-balanced) + live ℓ=2 shear + exact φ, both seal
BCs, Nr=16/Nth=8, foreground ~1s/BC. RESULT: both BCs **converged=False**; **jac_cond ~4e15 (S-Dir) / 9e16 (S-JC2)**
(float64 floor); maxit=30 hit every continuation step (Φ floored ~1e-4); shear response a2_peak ~5e-3/2e-5 and induced
q ~±2.5e-8 at solver NOISE; `closed_cell_exists=False` = NON-CONVERGENCE not a physics "no"; BC-fork UNDETERMINED. Per
MISMATCH→SOLVER: a near-singular Jacobian is ambiguous between a numerical/gauge artifact and a genuine soft/flat
shear mode (which would itself be CONTINUUM evidence) — cond~1e16 can't distinguish. ⇒ tool-limited.

**NEXT-SESSION PICKUP (Charles-gated):** DIAGNOSE the N5d conditioning (solver-first, NOT a mechanism hunt) — SVD the
Jacobian's near-zero mode: (a) GAUGE freedom → fix it; (b) block-SCALING → rescale shear-vs-φ/ρ blocks / apply the
already-wired `lbare_precondition`; (c) genuine PHYSICAL soft mode → CONTINUUM evidence, confirm at higher precision.
Only once it CONVERGES read Outcome A/B for the ℓ=2 tile; then re-run the pilot; then (if a pin candidate) Stage-2
co-relaxed source + higher-ℓ + BC-fork survival before banking. Do NOT run branchGP (fenced). ANTI-HANG binding.

---

## SESSION RECORD 2026-07-05 (EVENING) — ARCHIVED 2026-07-06 → HANDOFF_ARCHIVE.md
(N5/ξ CLOSED · solar γ=1 · D1 charge-channel · no-selector theorem · i-flow/ℏ; all blind-verified)

## SESSION RECORD 2026-07-05 (PM) — ARCHIVED 2026-07-05 (EVENING) → HANDOFF_ARCHIVE.md
(H3 → OUTCOME A + the full H4 backreaction/mass arc → revised-N4 = D, whole-cell mass — the arc the EVENING built
on; canonical detail = the `node_H3_*.md` / `H4_*.md` result docs + `archive/LIVE_H3_H4_arc_2026-07-05.md`.)

## SESSION RECORD 2026-07-05 (AM) — ARCHIVED 2026-07-05 (EOD) → HANDOFF_ARCHIVE.md
The concentric ω≠0 arc CLOSED → the HOPFION route R0→Q1→H1→H2→H3 (H3 = PROVISIONAL-A). Superseded by the PM block
above; canonical = the `node_R0/_H1/_H2/_H3_*.md` + `native_hopfion_route_MAP.md` docs. Full narrative → `HANDOFF_ARCHIVE.md`.

## SESSION RECORD 2026-07-04 — ARCHIVED 2026-07-05 (EOD) → HANDOFF_ARCHIVE.md
Route fork R1/R2 → S²-regrade → E2c/E2d/E2e optimizer arc (FREE-ON-A-SHEET s=2μ/Z; J(s) frame-robust lever;
embedded-cell existence UNDECIDED = the depth-stiffness wall). Superseded as frontier by the hopfion arc; the
still-owed PARKED threads (s=2μ/Z + J(s), R3, the 5 D2 forks, R1 flag, photon/EM re-grade, Bin-2 re-grades) are
carried forward in LIVE.md. Detail → `archive/LIVE_route_fork_E2_arc_2026-07-04.md` + `HANDOFF_ARCHIVE.md`.

## SESSION RECORD 2026-07-03 → 07-04 (Fable's closing session) — ARCHIVED 2026-07-05
Rulings → Stage-D (13/13 blind) → microphysics re-entry → D1/D2 (route fork) → R1/R2/S²-regrade/E2c–e. Full
verbatim record → `HANDOFF_ARCHIVE.md`. (Superseded as frontier by the 2026-07-05 hopfion arc above.)

## SESSION RECORD 2026-07-02 → 07-03 — ARCHIVED
Universe cell → integer ladder N=0..22 → derived laws (Theorems A/B, Lemma D) → stability arc; canon C-2026-07-02-1 (anchor = Δφ). Full verbatim record (14+ verifier agents; the four pending stability rulings; method notes) → `HANDOFF_ARCHIVE.md`.


> **Earlier frontiers:** see `HANDOFF_ARCHIVE.md` (2026-07-02-morning block archived 2026-07-03) — the
> sections below (STANDING BINDING DISCIPLINE / Foundation / STANDING RISKS / REUSABLE MACHINERY /
> Must-not-lose) are DURABLE, not frontier. NB Risk 1 (round-static walls) is now RESOLVED-IN-CONTEXT by
> the ladder arc (static discreteness exists via closures, not towers); Risk 2 (Z_phi fork) remains open,
> now with derived observational handles (window ceiling, a_seal, q all scale with Z).

## *** STANDING BINDING DISCIPLINE — read every resume (Charles 2026-06-19) ***
**MISMATCH -> SOLVER, NOT MECHANISM.** If a result is far from observation, the FIRST hunt is the
SOLVER and our application of it — NEVER a mechanism. In order:
1. What did we leave OUT of the solver? (a term, a coupling, a sector, a boundary)
2. Is it a NUMERIC problem? (convergence, box-control, conditioning, a bug, grid)
3. Did we FREEZE or forget to turn on a degree of freedom?
4. Have we actually EXPLORED THE SOLUTION SPACE with everything on, or only a corner?
Plus the many WAYS to examine the same solve (different bases, grids, seeds, continuation, gauge
tests, independent re-derivation). **Reaching for a mechanism to close a gap is FORBIDDEN** until the
solver is demonstrably complete and the solution space genuinely explored. A mismatch indicts the
solver's COMPLETENESS first, the metric last, and a mechanism never (the import reflex). This is
Principle 1 applied to our own numerics. And: **the microphysics space is UNENTERED, not walled** —
the pre-postulate negative corpus is RETIRED (mine for TOOLING only). BOUND the grid, never FREEZE a
DOF ([[full-dimensional-complete-solver]]); test gravitating-soliton stability by a constraint-respecting
COUPLED re-solve, never off-constraint stiffness ([[gravitating-soliton-stability-test]]). (Also in
CLAUDE.md tripwires + the `.claude/skills/` discipline skills + memory [[solver-first-not-mechanism]].)

## Foundation (the DERIVED native frame the solver now builds on) + read order

**The native UDT frame is DERIVED + verified (2026-07-01) — this is the foundation the new solver stands on** (five docs:
`native_field_equations_constrained_two_player_results.md`, `gp_switch_criterion_results.md`,
`native_geometric_action_results.md`, `seal_matching_junction_results.md`, `round_matter_reduction_results.md`; each
CAS + blind-verified). Metric = constrained-two-player `ds²=-e^{-2φ}c²dt²+e^{2φ}dr²+h_AB dx^A dx^B`; native geometric
action `∫c√h[(Z_φ/2)φ'² + R^{(2)} + W_χ𝒦]`, `W_χ=e^{2φ}(G)/1(P)`; matter is **φ-BLIND** (sources geometry via
`n→h_AB→𝒦→φ`, not `e^{2φ}T`). One open constant `Z_φ` (held fixed; free vs `=8`-with-forced-mixing fork → consilience).

**The OLD static solver is the WRONG FRAME (retained only for the tests).** The p1 MIGRATION solver (`p1_residual`,
`branch_operator`, `full3d_*`, …) realizes the φ-OUTSIDE-the-metric two-player scalar-tensor frame that Phase 1 showed
is a CHOSE extension, NOT canonical UDT. Its `e^{2φ}L_m`/`e^{2φ}T` matter weight is the NON-native artifact that
manufactured the "basin A" runaway; the X=−2e5 was the Cassini KLUGE. `pytest tests/` = **32 passed / 1 xfailed** still
imports these modules, so they STAY until the new solver + test rewrite land (then retire to `legacy/`). Do NOT tune them.

**Durable native-matter facts (SURVIVE, and the new solver uses them):** UDT's native matter = the **S²/π₂ winding**
(`n=x/r`), a scale-free defect; its charge is the **integer TOPOLOGICAL degree N** (native quantization — the "lump"
search was frame-creep, Charles's 2026-06-25 catch). In the new round solver: rigid `f=θ` collapses (I_r=0); the
minimally-free `f(r,θ)` test RAN (arc archived; the universe-cell/ladder line superseded it — see LIVE.md). The φ-angular hunch now appears NATIVELY (Branch-P `𝒦`-source;
the route-B kinetic-completion mixing term; the seal source that charges a matter cell).

**Read order for a new instance:** (0) **LIVE.md FRONTIER block** (THE only-guaranteed-current file). (1) CLAUDE.md
"How we work" + ANTI-HANG + the `.claude/skills/` discipline skills; frontier memory **[[universe-cell-rigidity-frontier]]** (foundation one back: [[native-field-equations-frontier]])
+ the principle memories ([[apply-purist-logic-proactively]], [[solution-space-not-imposition]],
[[charles-workflow-preferences]], native-matter-defect-import-discovery, solver-first-not-mechanism). (2) THIS FILE +
the five native-frame result docs + `discreteness_preregistration.md` + `round_matter_reduction_results.md` +
`cell_solver_round.py`. (3) CANON.md (C-2026-06-14-1; C-2026-06-18-1 — both SURVIVE); NEGATIVES_REGISTRY;
FOUNDATIONAL_ASSUMPTIONS_LEDGER. **HANDOFF_ARCHIVE.md + STATE.md + git + `archive/` = the deep historical record.**

## STANDING RISKS — the two flagged open items in the derived frame (Charles 2026-07-01, do NOT lose)
Both are correctly TAGGED (unlike the X-kluge, which was mislabeled `# FREE` and so contaminated silently). A tagged
open choice is manageable; the danger is only if we forget it's open. They come due at DIFFERENT stages — convenient
for keeping them honest.

**RISK 1 — the CONSTRAINED-METRIC FORM (the CHOSE) may WALL OFF the structure we're hunting.** Derived + solid: the
exp clock law `g_tt=-e^{-2φ}` + the reciprocal tie `g_tt g_rr=-c²`. CHOSEN (not forced): static, diagonal, and the
"φ purely longitudinal + h_AB independent transverse" split. The serious danger: if discreteness actually needs a
metric structure our ansatz excludes — OFF-ROUND angular shape, a NON-STATIC/time-live piece, or φ mixing DIRECTLY
into the angular sector at the METRIC level (not just via the matter/𝒦 coupling) — we could scan the round-static
space forever, see only a continuum, and WRONGLY conclude "UDT has no discreteness." **A "round static → continuum"
result must be read STRICTLY as "this SLICE is a continuum," NEVER as the theory's verdict** (whole-before-slice;
frozen-DOF≠verdict). Load-bearing: ALL our derivations are SCOPED to this form — so if it's incomplete they're
PARTIAL, not wrong; the staged plan (round → off-round → time-live) exists to un-freeze these one at a time. This is
the bigger risk to WHETHER we find discreteness at all.

**RISK 2 — the OPEN CONSTANT Z_φ.** (a) **It could become the new X-kluge**: if a quantitative result rides on Z_φ,
the pull to "tune Z_φ until the ratios match" is the exact failure mode we just escaped — the pre-reg fence (held
fixed, ONE global choice, no per-solution retuning, decided BEFORE checking the match, blind-verified) must actually
hold. (b) **The fork is STRUCTURAL, not just a number**: Route B (`Z_φ=8`) FORCES an extra action term `e^φKφ'` (a
longitudinal-transverse = φ-angular coupling); Route A omits it. So "open constant" is really "**is there an extra
coupling term?**" — build in Route A and we may be missing a native channel (possibly THE φ-angular channel). (c)
**Scoped:** Z_φ (overall kinetic normalization) mostly rescales SIZES → it does NOT gate the first question ("are
there isolated cells?"); it DOES gate the QUANTITATIVE program (mass ratios) later. This is the bigger risk to
getting the numbers right and NOT fooling ourselves.

**Shared deep risk = INCOMPLETENESS** (a missing DOF for Risk 1; a missing term for Risk 2). Neither will announce
itself — this is exactly where "keep auditing and digging until it's correct" earns its keep: is this scoped or
general? chose or derived? whole or slice?

## REUSABLE MACHINERY (the old solver = a PARTS BIN, not a foundation) — Charles 2026-07-01
The old 3-D solver was the WRONG frame, but it has TWO layers: the **physics recipe** layer is DEAD (wrong frame),
the **numerical machinery** layer is Category-A ("how we solve", frame-agnostic) and is a REUSABLE parts bin. Raid it
DELIBERATELY, one audited part at a time, as the difficulty climbs — do NOT build on it wholesale.

**REUSABLE (Category-A numerics — mine the METHOD, in `legacy/` + the kept root closure):**
- `glm` step = Levenberg-Marquardt in a conditioned basis + Nielsen damping + line-search (in
  `p1_residual_general_einstein.py::newton_solve_p1`) — a general robust nonlinear solver for when the 2-D/off-round
  problem gets stiff.
- galerkin BC-recombined basis (`galerkin_basis.py`) — bake BCs into the basis for conditioning (the mirror-seal cell
  has its own tricky BCs).
- spectral methods — **`spectral_sph_exact.py` (SH-EXACT angular d/dθ) is the most directly relevant**: the naive
  GL-μ grid mis-differentiated the winding `sinθ` non-convergently; the new `f(r,θ)` winding field is EXACTLY that
  structure. Also `spectral_cheb.py` (Chebyshev radial). GPU batching (torch float64) for large scans.
- the junction/DtN/Israel formalism (already used for the seal JC1/JC2), and the grid/method-convergence harness
  (a pre-reg acceptance criterion).
- **Operational know-how (frame-independent, do NOT relearn the hard way):** the GL-μ-grid-mis-differentiates-winding
  gotcha; the V100/cu121 batched-Cholesky-with-broadcast-factor corruption at batch ≳150 (use explicit inverse +
  matmul); the ANTI-HANG rules (bound the grid, ONE process, never background-poll a solve).

**DEAD (wrong-frame PHYSICS — do NOT reuse the ASSEMBLY):** `p1_residual_general_einstein.py` (the 11-field residual),
`branch_operator.py` / `b1prime_3d_offround_residual.py` (the e^{2φ}-weighted derived operator), the X-continuation,
`solver_action.py` GR-baseline. These build the φ-OUTSIDE-the-metric frame.

**CAVEATS:** (1) the old modules INTERTWINE physics + numerics — you cannot just `import full3d_spectral` (it builds the
wrong metric; the matter EL bakes in e^{2φ}); pull the METHOD, never the assembly, or you re-import the flaw
(Category-A not B; the "audit-solving-infrastructure" discipline applies). (2) The near-term problem is MUCH simpler
(1-D ODE now, 2-D PDE next — scipy-handled; `cell_solver_round.py` is ~60 lines), so for a while a FRESH small tool is
CLEANER than untangling a 3-D module. (3) The parts bin being full is a real head start; assembling from it wholesale
would drag the wrong frame back in.

## Must-not-lose (durable facts)
- DATA-BLIND wall numbers (NEVER load during a derivation): the six lepton wall numbers, contract
  26fc757. We predict RATIOS.
- CANON C-2026-06-14-1 (B=1/A sourced by the angular sector; EOS-softened interior) — SURVIVES.
  CANON C-2026-06-18-1 (metric form derived from relativity) — the new foundation.
- Durable GEOMETRY: the seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass =
  the cell's public charge (Q=2 p_F); N=3 from the area form (D1-corrected 2026-07-04: N=3 + the 1+3+5 algebra + structural-i = NATIVE cargo; q=1/3 and eta=1/18 = IMPORT-DEPENDENT -> targets; d1_angular_constants_native_rederivation.md); 7.004 = ln(1+z_CMB)
  via 1+z=e^phi.
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them.
