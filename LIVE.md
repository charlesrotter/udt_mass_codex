# LIVE — the only guaranteed-current file (READ ME FIRST)

Everything here is true RIGHT NOW. `HANDOFF.md` / `STATE.md` are detailed history; **if they
disagree with this file, THIS file wins.** No stale next-steps live here.
**Read order:** LIVE.md → CLAUDE.md "How we work" + the discipline skills → (for detail)
HANDOFF.md TOP → INDEX.md (repo map).

## Binding method (never skip)
- CLAUDE.md "How we work": MAP / OBSERVE / PONDER are primary, DERIVE is gated. Let structure
  EMERGE; pre-work discussion in LAY language; "chose or derived?" / "observing or targeting?".
- Discipline skills (`.claude/skills/`, auto-loaded): **solver-first**, **verifier-before-record**
  (incl. cross-model escalation), **no-shortcuts** (run `python3 -m pytest tests/`), **completeness-map**.
- **DRIVER TRIGGERS (CLAUDE.md, always-loaded) + harness HOOKS** (`.claude/hooks/corral_trigger.py`,
  fires on Task/Bash/git-commit) now make the corral fire WITHOUT being challenged — pause+honesty, never
  merit; the allowed-lane clause (category-A technique always GREEN) is non-droppable. Memory freshness:
  every DATED memory carries a CURRENT/SUPERSEDED/HISTORICAL tag (read CURRENT only). Local-LLM cross-check
  to come — wiring = `export_for_local_llm.py` (refuses untagged DATED). Record = `cognitive_corral_triggers_results.md`.
  **PENDING — FIRST ACTION next fresh session (catch-proof §4, Charles will verify):** confirm the `## DRIVER
  TRIGGERS` section AUTO-LOADS — before touching any file, recite the 6 triggers / the allowed-lane clause from
  context; if present unprompted, §4 passes. (Could not self-certify the building session: the section was added
  AFTER that session's CLAUDE.md auto-load.) **DRY-RUN (2026-06-27, empty-instance agent ae0d35a4): a fresh
  SUBAGENT did NOT see the section in its auto-loaded CLAUDE.md (it had How-we-work + Orientation but not the
  Discipline-skills/DRIVER-TRIGGERS block) — a YELLOW FLAG, not a verdict (subagent context may differ from a
  top-level session). BUT the harness HOOKS fired regardless, so enforcement is LIVE either way. → The HOOKS
  (Part B) are the load-bearing mechanism; if the top-level fresh session ALSO lacks the auto-load, rely on the
  hooks and/or relocate `## DRIVER TRIGGERS` earlier in CLAUDE.md (right after "How we work").**
  **HOW YOU'LL KNOW IF THE HOOKS FAIL:** a `SessionStart` hook now prints **`✓ CORRAL GUARDRAILS ACTIVE`**
  at the TOP of every session (+ the startup self-check prompt). Its PRESENCE = hooks loaded (Part B live);
  its ABSENCE at session start = hooks did NOT load — the loud failure signal. (Per-tool-call DRIVER TRIGGER
  reminders are the other visible signal.) First live confirmation = the banner appearing next session.
- **DATA-BLIND:** never load the six lepton wall numbers during a derivation (contract 26fc757). We
  predict RATIOS.
- **ANTI-HANG:** coupled solves are SLOW — bound the grid (Nr<=16/24), ONE clean process, never
  background-poll a solve.

## CURRENT ACTIVITY (2026-06-25 EVENING): STATIC SOLVER now CODE-COMPLETE — next = kap8 characterization (both branches), then DYNAMIC.
Charles's directive this session (BINDING, [[fix-all-flaws-before-dynamic]]): the goal is a WORKING solver to
EXPLORE the solution space; **fix EVERY static-solver flaw (no pick-and-choose) before going dynamic — "no red
gates before the next level."** And ([[apply-purist-logic-proactively]]) pick the PUREST/most-correct option and
FIX THE FLAW yourself; don't take the imposing shortcut. The whole arc landed:
- **Anti-imposition GATE** built (skill `solution-space-not-imposition` + 2 physics-blind lints in
  `tests/test_solution_space_gate.py` + CLAUDE tripwire + the convergence guard reframed filter→CHARACTERIZER),
  blind-verifier passed. Governing limit: a gate checks PROVENANCE & HONESTY, never MERIT.
- **Import-traceability cleaned**: the live solver graph is numeric-method + action-EL modules ONLY (extracted
  `solver_pack.py`; `full3d_solver`/`spectral_radial_soliton` left the graph). Direct solver audit done.
- **Off-diagonal sector COMPLETED** in the derived operator (gate #7): the 3 spatial off-diagonals are live DOF
  again (the kap8 RED was SOLVER-incompleteness — a frozen DOF — not a horizon).
- **Grid fix** `spectral_sph_exact.py`: spherical-harmonic-EXACT d/dtheta (the GL-mu grid mis-differentiated
  winding sin(theta) non-convergently) — unblocked the PURE native matter.
- **NATIVE-S² matter WIRED**: the operator takes matter via `dn`; the imported S³ hedgehog is RETIRED; the live
  matter is the free 3-component carrier (`free_s2_matter.field_dn_components_exact`) with the |n|=1 constraint;
  **the matter CORE IS FREE** (no Theta pin — winding from the seed's homotopy class; `seed_round_native`).
- Provenance gates re-pointed to the tagged source-of-truth (`branch_operator` KAP8/XI_PROD/KAP_PROD).
**`pytest tests/` = 32 passed / 1 xfailed.** The one remaining gate `test_no_habit_pins` = the branch G/P fork
(defaulted 'G') — an EXPLORATION gate, clears when the characterization runs BOTH branches (not a code flaw).

**kap8 CHARACTERIZATION — RAN 2026-06-27 (~40.9 h, both branches), result PARTIAL/CAVEATED — record =
`kap8_characterization_complete_solver_results.md`.** Both branches FLOORED at Nr=8,10 with a MILD warp-trend
(Branch G 1.02→1.18 ×1.16; Branch P 2.53→2.87 ×1.13) — much milder than the old ×2.12. **BUT the blind verifier
(agent a7cd2e2e) returned NOT-CLEAN as first framed and the "divergence CURED / it was the frozen off-diagonal
DOF, not a horizon" headline is REJECTED, NOT banked.** Caveats — ONE now CLOSED, two remain: (1) 2-grid can't
tell converged from slow-creep — need **Nr=12**; **(2) CLOSED 2026-06-28, blind-verified (agent `a63753fff`):
the native-S² winding SURVIVED** — independently recomputed on the SAVED field `solved_fields_nr8_G_kap8_1.pt`
by TWO methods, per-shell degree Q≈1 (interior mean 0.977), |n| in [0.987,1.010], matter density rho_max=0.182
that vanishes EXACTLY when the winding is forced constant, residual Phi=9.13e-22 (converged); a forced-unwind
fool-test collapses Q smoothly to 0 (diagnostic not rigged). PRECISE: real winding matter IS present, but
*part* of the warp stays BC/gauge-driven (NOT "the entire warp is matter"). SCOPE: Nr=8 / Branch G only
(Branch-P + finer grids unchecked for degree leakage); **(3) CLOSED 2026-06-29, blind-verified PARTIALLY-
CONFIRMED (agent `ae5a16bb`): the off-diagonal completion is EXCLUDED as the warp-tamer.** Off-diagonals-OFF
control (`caveat3_offdiag_off_control.py`, e_*=0 frozen): same-grid Nr=8 (off-ON fully floored Φ=9e-22 vs
frozen) moves the diagonal warp only 1.022→1.029 (+0.7%); three independent Nr=8 warps agree (1.022/1.021/
1.029). PRECISE (verifier): off-diagonals don't change the warp MAGNITUDE but ARE required for CONSISTENCY
(they floor the rth row) — not blanket-irrelevant. SOFT leg: cold off-OFF trend ×1.19 vs off-ON ×1.16, but
the off-OFF Nr=10 point is under-floored (Φ=4.54) and off-ON Nr=10 un-reverifiable. ATTRIBUTION: the milder-
than-×2.12 trend is the **S³→native-S² matter swap and/or the SH-exact grid fix** (mutually confounded, no S³
control re-run), NOT the off-diagonals. **The strong-field HORIZON hypothesis REMAINS OPEN** (do NOT retire it
— declaring "cured" on 2-grid data is the impose-the-answer drift the gate exists to stop). `test_no_habit_pins`
NOT flipped.

**NATIVE REFRAME (2026-06-29, blind-verified PARTIALLY-CONFIRMED, agent `a9efe4b`): the kap8 object read in
UDT variables (not the GR horizon lens) is a CORE-CONCENTRATED degree-1 S² WINDING DEFECT in a GENTLE dilation
well** — NOT a forming horizon (lapse e^a≈0.37, 2m/R does not climb to 1; the GR "compact/above-Buchdahl/near-
horizon" reading was a misapplied ruler), NOT a localized lump (clean energy-charge E(<r) keeps rising), and NOT
a clean scale-free monopole (E/r FALLS ~5–6× across the interior, not constant). Gentle φ (~4% redshift, Nr=8),
ρ=r to ~10%, ρ~r^−2.4 core-weighted. **This RESOLVES the horizon scare natively** (consistent with canon: native
matter = winding defect, not a particle). Diagnostics: `ponder_horizon_signatures.py`, `native_object_characterization.py`
(clean energy-charge replaces the spectral-ringing-contaminated Misner-Sharp m(r)). The verifier rejected the
over-claimed "global monopole" headline; conservative identification above is the licensed wording.
**SPECTRAL-RESOLUTION CHECK (2026-06-29, blind-verified PARTIALLY-CONFIRMED, agent `a73caf9`): the SMOOTH sector
is RESOLVED at Nr=8** — φ truncation decays cleanly (~3% at top mode), lapse a dominated by modes 0–1; **so the
gentle-φ / not-a-horizon native reading rides a RESOLVED field (SOLID, not grid-fragile).** The apparent "fat
tails" are NOT generic under-resolution: (i) b's flat spectrum is the EXACT fingerprint of the imposed
`b(core)=−1` BC step (an endpoint cardinal function is exactly flat; excluding the core node b's tail collapses
0.66→0.15 and decays) — benign, exactly captured, a finer Nr won't "converge" a BC step; (ii) ρ is the singular
winding-defect core (ρ~1/r², 3.4e5 dynamic range) regulated by **rc=0.1, NOT Nr**. So the earlier "GRID-FRAGILE
/ φ deepens 6×" worry is RETRACTED — φ is resolved at Nr=8, and the 6× came from the under-floored frozen Nr=10,
NOT real physics. **Genuinely soft = only the core-dominated CHARGE profile (rc-entangled, the defect core).**

## SOLVER AUDIT (2026-06-29) — broad-sweep, 21-agent workflow, FIX-FIRST before time-live (record = `SOLVER_AUDIT_2026-06-29.md`)
Verdict: **the physics core is TRUSTWORTHY** (the live operator is a genuine derived scalar-tensor extension — NO
smuggled GR-form / mechanism; native-S² matter EL correct; off-diagonals correct on the LIVE path; gates physics-
blind), **but FIX-FIRST a bounded list before extending to time-live** (not a hard block). Bounded list:
- **D1 (HIGH, top priority — and itself UNVERIFIED, an incompleteness observation): the static system may be
  UNDERDETERMINED at the grids used** (body mask `[3:Nr-3]` + most fields one BC → rows<cols for Nr<59; at Nr=8
  only ~2 interior layers carry equations; damped-LM lstsq makes the rank-deficient step solvable). **If true,
  residual-smallness is partly seed+Levenberg-regularized, not pinned by the metric — which would REOPEN the
  caveat #2 winding-survival result AND the native characterization (both rode Nr=8).** → **FIRST ACTION: cheap
  determinacy check** (Jacobian SVD / numerical rank at the converged Nr=8 point). Full-rank ⇒ D1 dismissed,
  session results stand; rank-deficient ⇒ re-grade on a resolved grid. Do THIS before anything else.
- **B1/F-4/G8 (med):** the owed gravity-sector SH-exact d/dθ verify (matter uses SH-exact; gravity uses grid
  Legendre — agree only at axisymmetry; off-diagonal/non-round/dynamic would mix exact-RHS with inexact-LHS).
- **A2+D5 (med):** un-derived e^{2φ} field-matter weight is LIVE (tagged CHOSE in 3 places, not hidden) + live
  drivers ride xi=kap=1.0 not the documented 2e-2 (untagged at call site) → resolve/tag at the banking surface.
- **G3 (gap):** no stability notion on the 11-field object — establish a constraint-respecting one before/with dynamic.
- **§3-iii consolidation (owed per CLAUDE.md):** retire the superseded diagonal/prototype solvers to ONE canonical
  solver+harness (live closure ~17 modules; ~1086 root .py to archive) so time-live doesn't branch off a proliferated base.
- **Cheap:** C5 (NameError dead code), D4 (seed ignores p / sign-opposite-BC), doc staleness (solver_action.py stale
  GR-baseline label A1; constants A3; INDEX F-5; B2/B4/E4). 6 false-positives dismissed (don't re-chase — see §5).
Dynamical/topology gaps (G1 time, G4-G6) = the build itself or stamped scope, NOT blockers. **Cross-model verification
still reserved for the first time-live PHYSICS result** (the audit was same-model; its D1 lead needs the cheap rank check).

**NEXT (gated on Charles): work the FIX-FIRST list, D1-determinacy-check FIRST.** Then time-live. (Superseded the
"carry to dynamic" lean below — the audit found a foundation item that must be checked first.)
**(prior lean, now gated behind the audit):** Nr=12 is LOW-VALUE (verified) — the smooth sector (φ/lapse/interior metric) is
already resolved at Nr=8, so a finer Nr won't change "gentle well / not a horizon"; the core ρ is an rc-regulated
singularity (relevant knob = rc, not Nr), and it's the defect core, not "the particle." With caveats #2+#3 closed,
the object natively identified (core-concentrated winding defect, NOT a horizon), and the smooth sector resolved,
the recommendation is **carry forward to DYNAMIC** (time-live / non-stationary native S² — the φ-angular hunch's
home), the next build regardless. (If anything is revisited it's rc-sensitivity of the core charge, not Nr.) Still owed: check whether the GRAVITY sector also needs the SH-exact
d/dtheta (verify, don't assume). Solves are SLOW (Branch-P Nr=10 ~20 h) — run MYSELF, bounded, single process,
background-notify, NO nohup; AVOID `| grep` (block-buffers → no live progress; write straight to file).
archive/MIGRATION.md M4/M5/M6 = SUBSUMED (historical).

## (HISTORICAL) 2026-06-23: solver-integrity-upgrades arc — COMPLETE
A Charles-requested detour to harden the solver's integrity MACHINERY before resuming the physics
build (spec = `SOLVER_INTEGRITY_UPGRADES_SPEC.md`). SPINE: the harness REFERENCES derivations, it
never RE-ASSERTS their values. All committed + blind-verified:
- **P1** — purity harness `tests/test_solver_integrity.py` (liveness, provenance lint, limit/de-Sitter
  normalization, native-object guard). `pytest tests/` = **16 passed / 5 xfails** (at the time; now **23
  passed / 5 xfails** after the migration added the derived-operator + φ tests — see archive/MIGRATION.md).
- **P2** — `solver_action.py` (single source-of-truth GR-baseline action + provenance registry) +
  `tests/test_operator_from_action.py` (operator == EL of the action).
- **P3** — 4 auto-loading discipline skills + CLAUDE.md pointer (tripwires stay inline).
- **P4** — `CROSS_MODEL_VERIFY.md` (cross-tier blind verify for load-bearing calls).
- **P5** — this file.
Records: `p1..p5_*_results.md`. **The 5 documented-gap xfails + the P2 baseline = the MIGRATION
acceptance tests** (kap8=1, a=e^φ, native S², core_mode free, ξ/κ tags). Migration must ALSO resolve:
the curvature **Branch G/P fork** (= the φ-angular tension) and the **e^{2φ} matter weight**
(PARTIALLY-TRACED — a flagged CHOSE, NOT derived for field matter; P4).

## BRANCH-P PUSH — DONE/RESOLVED (2026-06-24): solver fixed, no static localization, X-premise caught
The Branch-P push (does native matter localize / select a scale on the untried φ-angular branch?) is
RESOLVED for STATICS. Record = `branchP_solver_floor_xcontinuation_results.md` (blind-verified
PASS-WITH-FIXES; NEGATIVES_REGISTRY #66). Steps A+B (committed 9cd80ef): `branch_operator.py` (derived
G/P-switch operator) + `branchGP_native_s2_coupled_OBSERVE.py` (static coupled residual, 6 LIVE fields
incl. native S² twist `gtw`). What the floor push found:
- **The solver is FIXED via CONTINUATION-IN-X** (`prototype/x_continuation.py`): warm-start up a geometric X-ladder
  floors X=−2e5 to Φ=0.18 where every cold-started solver sticks (cold −2e5: Φ=2720). The wall was the
  singularly-stiff φ-equation (`2X·div≈2U'(φ)`, X=−2e5 huge → φ forced ~flat; EL_φ≈X·curvature-error).
- **Solver-integrity catches:** the "P stall at Φ=8.67" was a stochastic unseeded-Jacobi-PC artifact (P
  floors ~like G); the interior-Einstein "obstruction" (cond~1e10) was a SCALING artifact — Ruiz
  equilibration drove Einstein residual→0, moving it to EL_φ (NOT under-resolution, NOT a missing term).
- **PREMISE CAUGHT:** X=−2e5 is a CHOSEN placeholder (`FREE`, Cassini-bounded half-line; branch_operator.py:85)
  that throttles φ ∝1/|X| — so "scale-free" was X-conditioned. Unthrottling φ (continuation) reveals NO
  intrinsic localized body. **Static Branch P = no intrinsic scale / no localized particle** (scoped:
  static-only, deep-regime X OPEN).
- **FIRMED at Nr=16 + seal test (2026-06-24, blind-verified; CORRECTS the mechanism):** the Nr=16 floor
  (Φ=5.1e-3) shows the continuation body is NOT featureless — it has BIMODAL structure (peaks r≈2.1/6.1)
  that SHARPENS with resolution. BUT the seal/box scan (cell=6,8,12,16) shows that structure is
  BOX-CONTROLLED: dominant peak at exactly 0.75·r_i in all four (pinned to the outer body grid node,
  scales with the seal) = NOT intrinsic. So the negative STANDS/STRENGTHENED via the corrected mechanism
  "box-controlled structure" (the original "featureless-defect/boundary-layer" shape-read was WRONG). New
  scripts: prototype/grid_refine_{warmstart,resume}.py, prototype/seal_test.py.
- **→ NEXT (Charles's pick at the next ponder):** statics on BOTH branches now say scale-free defect with
  the solver trustworthy → the φ-angular discreteness hunch's one UNTESTED instrument is the **TIME-LIVE /
  non-stationary native S²** (PHYSICS FRONTIER below). Optional firming: Nr=16/24 grid-refine to resolve
  the boundary layers and close the coarse-grid caveat. The "migration" (wire the derived operator into
  the LIVE p1_residual + flip the 5 P1 xfails) remains a SEPARATE gated step.
- **OPERATIONAL (relearned, 2026-06-24):** run solves MYSELF, bounded, single process; `run_in_background`
  WITHOUT `nohup` (nohup detaches from the harness tracker → false "complete"); agents HANG on solves —
  build-only, never delegate a solve.

## PHYSICS FRONTIER (parked, unchanged): TIME-LIVE NATIVE S²
Live foundational state (2026-06-22 native-matter arc, all blind-verified):
- UDT's **native matter = the S²/π₂ winding (n=x/r) = a scale-free global-monopole DEFECT**, NOT a
  localized particle, in EVERY STATIC config played. The round/static soliton was an IMPORTED S³
  Skyrme baryon (its body held by the imported winding BC).
- The gravity operator is **DERIVED** (vacuum ≠ GR; weight e^{2φ}, a(φ)=e^{φ}) but is **NOT yet wired
  into the live solver** (the live operator runs the a=−1 GR-baseline — that wiring IS the migration).
- **LIVE FRONTIER = the TIME-LIVE / non-stationary native S²** object — the standing φ-angular
  discreteness hunch's home and the one major UNTESTED instrument. Every native solve so far is STATIC.
- **Two MAP-first decisions before building** (make-visible, get Charles's sign-off; detail in HANDOFF
  TOP): (i) finish the remaining STATIC native instruments first vs jump straight to time-live;
  (ii) THE DISCRETENESS GATE (Charles 2026-06-23): OBSERVE for emergence first; if discreteness does
  NOT emerge after sufficient development, IMPORT it under Postulate A (the accepted ħ/spin/statistics
  quantum postulate; UDT = quantized dilation-geometry). Emergence is the goal, Postulate A the fallback.
- **OPEN (found 2026-06-23, P4-style check): the curvature Branch G/P fork is already BEHIND us SILENTLY.**
  The native-S² static solves ran the DERIVED operator on **Branch G** (gauges the angular obstruction
  AWAY; scale-free by construction) — never named/flagged. **Branch P** (keeps the φ-angular curvature
  as a physical potential + the scale-breaker e^{2φ}−1) was NEVER tried on the native object. So the
  "scale-free defect" headline is BRANCH-G-CONDITIONED — possibly an artifact of the silent choice, and
  Branch P is where the φ-angular hunch lives. Make the branch an EXPLICIT switch; try Branch P
  (static, then time-live) before banking "featureless defect." (p1_residual GR-baseline solver is a
  SEPARATE line from this derived-Branch-G native-S² solver.)

## DURABLE CANON (must-not-lose)
- CANON **C-2026-06-14-1** (native S² carrier; B=1/A, EOS-softened interior) + **C-2026-06-18-1**
  (metric form derived from "remain relativistic") — both SURVIVE.
- seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass = the cell's public charge
  (Q = 2 p_F); q=1/3, N=3, η=1/18 from the H1 AREA FORM; 7.004 = ln(1+z_CMB) via 1+z = e^φ.
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them.
