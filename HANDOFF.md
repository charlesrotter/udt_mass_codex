# HANDOFF — Resume Instructions and Perspective

> **READ `LIVE.md` FIRST** — it is the short, only-guaranteed-current file (frontier + next action).
> This HANDOFF is the detailed record; if it disagrees with LIVE.md, LIVE.md wins. (P5, 2026-06-23.)
> **CURRENT (2026-07-07): after LIVE.md (its RESUME-HERE = the NO-BUILD per-rung RESONANCE TEST), read the
> `## SESSION RECORD 2026-07-06→07 (EOD-3 + rung derivations)` block immediately below. The full N5d Stage-2 static
> arc is CLOSED; the next session runs a NO-BUILD per-rung classification (Charles's Der 1-7,
> `classB_rung_resonance_prebuild_test_DESIGN.md`) that GATES whether a Class-B embedded-rung build is worth it.**

## SESSION RECORD 2026-07-06→07 (EOD-3, Opus 1M — N5d Stage-2 static arc CLOSED: impl→pilot→collapse→gauge→L-selection→MS→Class-B→rung gate-checks + Charles's rung-resonance derivations)

Charles directed step-by-step; every node committed & pushed on `main` (standing: push on every commit). All
DESIGN/PROVISIONAL/Outcome D; NO physics verdict, NO Outcome A/B banked. pytest 67/1xfail (Class A default
byte-identical; Class-B option added). **Two self-corrections this session, both caught by NEUTRALLY-framed blind
verifiers** (lesson banked in memory `verifier-framing-and-residual-artifacts`): I twice over-read a residual/valley
artifact as physics (the −0.96 "factor-2 structural deficit"; the "q_raw∝L ⇒ physical modulus") — always frame
verifiers to ADJUDICATE (X-vs-Y), never to confirm my read.

**THE ARC (each committed; docs named):**
- **Stage-2b IMPLEMENTED** (`6a0ac15`): off-round f-PDE (e^{±s}) + live source `−(ρ²/4)T_s` (λ=−½) + off-round Hseal;
  8-test gate GREEN (`tests/test_n5d_stage2.py`); code blind-verified vs pinned formulas (agent a3fd5f4f).
- **Preflight READY** (`d3a50a0`, `n5d_stage2_pilot_preflight_results.md`): FIX-1-equilibrated cond ~1e6-1e8 (Nr≤16).
- **S-Dir PILOT = L-COLLAPSE** (`652b484`, `n5d_stage2_sdir_pilot_results.md`): free-L drives L→0, Hseal never closes;
  blind-verified (agent ae5e8adc) no finite-L cell in the naive read.
- **Collapse mechanism**: mis-diagnosed "factor-2 STRUCTURAL deficit" (`f02f3f9`) → **RETRACTED** (`d729dd4`) →
  soft-mode **blind-CONFIRMED** (`5c6f6ac`, agent a50cf051): it's a FREE-BOUNDARY/φ-ρ GAUGE-LIKE DEGENERACY (Hseal
  slides ~free to 0 along a resolution-stable near-null; −0.96 was a valley point). `n5d_stage2_collapse_audit_results.md`.
- **Gauge audit** (`da6bcfa`, `n5d_stage2_gauge_audit_results.md`, blind agent a2969cef): the soft mode = removable
  global ρ-rescale+φ-offset GAUGE (2-pin [ρ(r_c),φ(r_c)] fix, cond 4.3e8→7.6e7, q_raw invariant) + an undetermined L
  flat direction; q_raw≡0 for mirror cells can't distinguish the L-family; L-selection is EXTERNAL.
- **MS/embedded-boundary audit** (`753ff00`, `n5d_stage2_MS_boundary_selector_audit_results.md`): `M=−q` DERIVED
  (`m=−q−q²/r`); the embedded package (JC1/JC2, `H_cell=H_amb`, MS balance) gives a mass-size RELATION + ratios, NOT
  absolute L (needs the cosmic ambient MS mass; z_CMB data-forbidden). Deliverable = RATIOS. φ-depth-sign vs
  positive-mass tension + p_F factor UNPINNED (Charles's canon call).
- **Class-B seal diagnostic** (`164ea11`, `n5d_stage2_classB_diagnostic_results.md`): added `cell_solver_f2d.py`
  `seal_phi="A"|"B"` (Class A default byte-identical). Class B (Dirichlet φ(r_s)=0, φ' free) REMOVES the φ-offset
  gauge (cond 4.76e9→1.47e4) + turns Hseal=0 into a REAL closure — but the ISOLATED Class-B tile does NOT close
  (fixed-L over-determined; free-L stalls); q not genuine; points to needing an exterior/receiver.
- **Class-B embedded-rung gate-checks** (`3e0eca7`, `classB_embedded_rung_gatecheck_results.md`): (a) the z_CMB
  anchor `x_c=1/1101` CANCELS in ratios to leading order (`q_i/q_j→(N_j+1)/(N_i+1)`); (b) `H_amb(N)=0` for every rung
  = a DEAD KNOB → the real junction is a FLUX/DEPTH match (`q_cell=q_N`, `Δφ_cell=Δφ_N`), which is the OLD no-band wall.
- **Charles's rung-resonance derivations (Der 1-7)** → `classB_rung_resonance_prebuild_test_DESIGN.md`: the old no-band
  wall was a MATTER-STRUCTURE wall (R4/R5), NOT a flux wall (q≈3.8-4.0 already closed π_φ). Discreteness helps only if
  a rung hits a RESONANT boundary target. **NEXT = a NO-BUILD per-rung test: compute `(q_N, Δφ_N, I_{r,req}(N), A_N)`,
  classify dead/positive-branch/turning-branch/TRUE candidate; only a TRUE candidate (I_{r,req}≈0 AND A_N≈0) justifies
  a bounded single-rung Class-B build. Formulas in the DESIGN doc.** Matter is φ-blind ⇒ depth-match ⇏ I_r>0 directly.

---

## SESSION RECORD 2026-07-06 (EOD-2 + EOD-1) — ARCHIVED 2026-07-07 → HANDOFF_ARCHIVE.md
(EOD-2 = N5d Stage-1 diagnosed+fixed→retired→Stage-2 DESIGN+CAS+Gate-0 cleared; EOD-1 = readout-map B+C →
provenance floor CLOSED → N5d built → Stage-1 pilot TOOL-LIMITED. Full text in HANDOFF_ARCHIVE.md; canonical =
the result docs. The current record is the 2026-07-06→07 EOD-3 block above.)

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
