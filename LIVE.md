# LIVE — the only guaranteed-current file (READ ME FIRST)

**The "## ============ FRONTIER ... CURRENT STATE" block below is the ONLY current frontier** — read it and stop;
everything under the "↓↓↓ HISTORICAL ARC" / "SUPERSEDED" fences is labeled-stale detail (mine for history, not the
plan). `HANDOFF.md` / `STATE.md` are detailed history; **if they disagree with this file's CURRENT STATE block, the
CURRENT STATE block wins.**
**Read order (2026-07-06 EOD):** LIVE.md FRONTIER (this block — the RESUME-HERE directive at its TOP is the next
action = DIAGNOSE the N5d conditioning) → **HANDOFF.md TOP (2026-07-06 session record)** → the N5d chain
(`N5d_solver_build_plan.md` → `n5d_pilot_stage1_results.md` → `n5d_pilot.py` / `n5d_shear.py` / `cell_solver_f2d.py`)
+ the readout-map docs (`native_readout_map_selector_audit_results.md`, `native_readout_map_depth_size_results.md`)
+ the provenance floor (`pre_native_era_census.md`, `macro_spine_provenance_2026-07-06.md`,
`branch_operator_contamination_ledger.md`, NEGATIVES_REGISTRY #76/#77). (The 2026-07-05 evening docs below are prior:)
`H4_N5_whole_cell_criticality_MAP.md`, `H4_N5a_whole_cell_criticality_rederivation_results.md`,
`H4_N5b_flux_budget_closure_results.md` (the ξ/N5 arc); `J_of_s_light_deflection_confrontation_MAP.md`,
`one_body_null_deflection_results.md`, `one_body_shapiro_delay_results.md`,
`solar_light_sector_confrontation_results.md` (the solar light sector);
`d1_charge_channel_projection_MAP.md`, `no_selector_audit_results.md` (charge / q=1/3); `i_flow_hbar_clock_MAP.md`
(structural i / ℏ) → CLAUDE.md "How we work" + the discipline skills → INDEX.md (repo map). (The PM H3/H4-arc docs
are HISTORY the evening built on — see the HANDOFF (PM) block if needed.)

## Binding method (never skip)
- CLAUDE.md "How we work": MAP / OBSERVE / PONDER are primary, DERIVE is gated. Let structure
  EMERGE; pre-work discussion in LAY language; "chose or derived?" / "observing or targeting?".
- Discipline skills (`.claude/skills/`, auto-loaded): **solver-first**, **verifier-before-record**
  (incl. cross-model escalation), **no-shortcuts** (run `python3 -m pytest tests/`), **completeness-map**.
- **DRIVER TRIGGERS (CLAUDE.md, always-loaded) + harness HOOKS** (`.claude/hooks/corral_trigger.py`, fires on
  Task/Bash/git-commit) make the corral fire WITHOUT being challenged — pause+honesty, never merit; the allowed-lane
  clause (category-A technique always GREEN) is non-droppable. **CONFIRMED LIVE (2026-07-01 startup): the
  `✓ CORRAL GUARDRAILS ACTIVE` banner appears + the 6 triggers auto-load** (self-check passed). Memory freshness: the
  TOP entry in MEMORY.md is the CURRENT frontier; older FRONTIER-labeled entries are tagged "SUPERSEDED as frontier"
  (durable lesson only); the rest are durable principle-memories. Read the TOP entry + this LIVE file for the live plan. **The auto-loaded memory snapshot can LAG disk
  (observed 2026-07-03): on resume, re-read MEMORY.md FROM DISK — this file + disk memory win over the snapshot.**
- **DATA-BLIND:** never load the six lepton wall numbers during a derivation (contract 26fc757). We
  predict RATIOS.
- **ANTI-HANG:** coupled solves are SLOW — bound the grid (Nr<=16/24), ONE clean process, never
  background-poll a solve.

## ============ CURRENT STATE (2026-07-06 EOD — readout-map (channel B + depth/size C) + provenance floor CLOSED both sides + N5d solver BUILT + Stage-1 pilot = TOOL-LIMITED (Outcome D); NEXT = diagnose the N5d conditioning) ============

**➤➤ RESUME HERE / NEXT ACTION (2026-07-06 EOD): DIAGNOSE the N5d Stage-1 pilot CONDITIONING (Charles-gated) —
the coupled ℓ=2 shear solve is NON-CONVERGED / near-singular, so the pin-vs-continuum question is UNANSWERED (tool-
limited, NOT a verdict).** The N5d solver is BUILT (`cell_solver_f2d.py` + `n5d_shear.py`, commit `84287b6`; pytest
48/1xfail, 8 gates green, contamination-clean) and the Stage-1 pilot RAN (`n5d_pilot.py`, commit `bf54957`; frozen
REAL H3-hopfion source Q=0.9917 + live ℓ=2 shear + exact φ, both seal BCs, fast ~1s/BC). RESULT = **Outcome D
(tool-limited), NO A/B banked** (`n5d_pilot_stage1_results.md`): both BCs `converged=False`, `jac_cond ~4e15 (S-Dir)
/ 9e16 (S-JC2)` (float64 floor), maxit=30 hit every continuation step, shear response a2_peak ~5e-3/2e-5 and induced
q ~±2.5e-8 at solver NOISE; `closed_cell_exists=False` reflects NON-CONVERGENCE, not a physics "no"; BC-fork
UNDETERMINED (both non-converged). **NEXT (gated, solver-first — NOT a mechanism hunt): SVD the Jacobian's near-zero
mode — is it (a) a GAUGE freedom (fix it), (b) a block-SCALING issue (rescale shear-vs-φ/ρ blocks / apply the
already-wired `lbare_precondition`), or (c) a genuine PHYSICAL soft mode (which would itself be CONTINUUM evidence,
confirm at higher precision)? Only once it CONVERGES can Outcome A/B be read for the ℓ=2 tile.** Then re-run the
pilot; then (if a pin candidate) Stage-2 co-relaxed source + higher-ℓ + BC-fork survival before banking.
**Do NOT run `branchGP` (fenced wrong frame). ANTI-HANG binding (bounded, foreground, no background-poll).**

### ↓ 2026-07-06 provenance-floor + earlier-frontier detail (historical this session) ↓
**Earlier 2026-07-06 (the arc that got here):** (1) readout-map CHANNEL-selector audit → **Outcome B** (no native
selector; q=1/3 unforced; solve-independent — `native_readout_map_selector_audit_results.md`). (2) readout-map
DEPTH/SIZE node → **Outcome C** (round Branch-P vacuum PROVABLY a continuum; hopfion RIDES; the frozen off-round
shear h_AB is the ONE door → this is what N5d tests; registry #76). (3) N5d preflight FAILED (no native solver
existed; the only coupled solver ran the SUPERSEDED scalar-tensor frame) → L_bare⁻¹ bug FIXED (`h4_scripts/
lbare_inverse.py`, `fe85a14`). (4) CONTAMINATION arc: `kap8_characterization` = SOLE QUARANTINE (#77); full date
census (`pre_native_era_census.md`, 4 classifiers + 2 adversarial passes) + macro-spine pass
(`macro_spine_provenance_2026-07-06.md`) ⇒ **PROVENANCE FLOOR CLOSED BOTH SIDES**; 10 SUPERSEDED docs → `archive/
pre_native_coupled/` (stubs); banners on CC docs; `native_dilation_weight §5-7` SPLIT (X=−2e5 birthplace). (5) N5d
build plan approved-with-edits → built. **RESIDUAL OWED (cosmetic): W-series phase-2 physical relocation.**
The pre-2026-07-06 CURRENT-STATE narrative (N5d-preflight-fail framing) is now superseded by the pilot outcome above;
the operator math was CAS-locked
and the L_bare⁻¹ bug is FIXED + committed (`h4_scripts/lbare_inverse.py`, `fe85a14`), BUT **no solver implements the
native constrained-two-player operator** — the only coupled φ+shear solver (`branchGP`/`branch_operator.py`) runs the
SUPERSEDED scalar-tensor frame (f=e^{2φ}, X=−2e5, e^{2φ}-matter). A scoped CONTAMINATION AUDIT + a full SUPERSESSION
SWEEP followed (blind-verified; commit `7441992`): the 2026-07-01 native operator superseded the pre-native
coupled-solver era, and the sweep was INCOMPLETE. **ONE genuine QUARANTINE found: `kap8_characterization` (+4
siblings) — a live unflagged native-micro identification banked on the scalar-tensor operator at X=−2e5 → registry
#77, banner, INDEX flag.** The rest of the era was already registry-tagged (given in-file stamps now); recent frontier
verified CLEAN. **PROVENANCE FLOOR NOW CLOSED (2026-07-06):** a date-based pre-native-era census (`pre_native_era_census.md`,
2026-06-11→07-01, 4 classifiers + 2 adversarial passes) confirms **kap8 (#77) is the SOLE QUARANTINE**; everything
else is CLEAN / SUPERSEDED / CONDITIONS-CHANGED. 10 SUPERSEDED coupled-solve docs relocated → `archive/pre_native_
coupled/` (redirect stubs left); CC docs stay live with banners. **MACRO-scope provenance pass NOW DONE
(2026-07-06, `macro_spine_provenance_2026-07-06.md`, 3 classifiers + adversarial pass): NO hard quarantine; N5d
triple-confirmed unaffected.** Live macro (solar R2 / universe-cell / ladder / cascade / H4_N5 / F7 / AUDIT-surviving)
is CLEAN native; the pre-native macro residue is bannered (native_dilation_weight §5–§7 SPLIT = birthplace of the
X=−2e5 kluge; F5 CC; scale_symmetry_bootstrap / macro_sector_fork / weld×2 / lepton_ladder_test SUPERSEDED; AUDIT.md
CC = stale header). **Provenance floor now closed on BOTH micro and macro sides.** Only residual left = W-series
phase-2 physical relocation (cosmetic; registry-retired + census-pointed). **NEXT (Charles-gated): BUILD the native N5d solver** — the
certified operator `∂_r(√h Z_φ φ')=−2√h e^{−2φ}𝒦̂[h]` + the E^{AB} shear sector (via the fixed L_bare⁻¹) + φ-blind
native-S² matter source + whole-cell BCs; then re-run the preflight gate, then the coarse pilot (Nr≤16–24, one
process, foreground, ANTI-HANG). **Do NOT run `branchGP` for N5d** (wrong frame, fenced). **Prior state today:** q=1/3 channel-selector CLOSED (★ selector entry
below); depth/size node = OUTCOME C (★ entry below).** All FIVE 2026-07-05 evening arcs (N5/ξ · solar light sector · D1 charge-channel ·
no-selector theorem · i-flow/ℏ) PLUS the 2026-07-06 readout-map selector audit are BANKED + blind-verified + pushed;
**H4 compute STILL STOPPED** (the gated non-perturbative N5d solve was NOT opened). **OPEN LEADS:** (a) **CLOSED
2026-07-06** — no target-selector for q=1/3 is derivable from ANY of the four named native sources (seal · spin ·
φ-angular · flux); the negative is SOLVE-INDEPENDENT (target-SO(3) is an exact symmetry of the full backreacted
functional). Closing q=1/3 now genuinely REQUIRES new physics (a natively-derived target-SO(3)-breaking coupling) or
accepting Q=1. (b) the gated N5d φ+h_AB solve (the ONLY route to pin ξ; ANTI-HANG binding, Charles-gated — NB this
audit proved N5d canNOT pin the target axis, only settle minimizer shape); (c) the η Zρ_s² anchor; (d) **NEW** — the
general readout-map's LIVE axis is now DEPTH/SIZE discreteness (Branch P `Z_φ(r²φ')'=4e^{-2φ}`, the φ-angular hunch
survives for magnitude-not-channel) — a distinct node Charles may open. q=1/3 & η=1/18 remain OWED targets. Do NOT
re-open a closed arc without a new premise. *(This directive is the ONLY current next-action; the per-result ★ blocks
below are the banked summaries — they do NOT carry their own live "NEXT".)*

**★ NATIVE READOUT-MAP — DEPTH/SIZE NODE (Branch P) (2026-07-06, BANKED + blind-verified,
`native_readout_map_depth_size_results.md`, verifier ae3142d4ba6d9e825) — PRIMARY OUTCOME C, banked B-separation,
sharp D-pointer.** Second axis of the readout-map (⊥ the closed channel axis). FIRST characterization on the CORRECT
native operator (`Z_φ(r²φ')'=4e^{−2φ}`, source = geometric 𝒦, e^{−2φ} EXACT — the archived `e^{+2φ}` scalar-tensor
form is a superseded different equation; prior continuum negatives #34/#39/#52/#54/#66 rode wrong operators / imported
S³ / pinned-X / private cells ⇒ this is FRESH, not a re-tread). **The bulk equation is exactly SCALE-INVARIANT ⇒ any
discreteness must be a whole-cell closure, not a bulk spectrum.** Node A (rigorous, verifier re-ran 2000-sample
shooting): in autonomous form `φ_tt+φ_t=(4/Z_φ)e^{−2φ}` = a MONOTONE runaway (force sign-definite) ⇒ φ monotone,
node-count ≡0, no turning point ⇒ the round vacuum is a CONTINUUM (size R + depth φ_c both FREE; r_s/r_c, q continuous
outputs). Node B: the hopfion RIDES (λ*~√(κ/ξ) rides free couplings, `solve(E₂=E₄,ξ)→∅`); mass = flux = M = q =
Z_φρ_s²φ'(r_s), a CONTINUOUS whole-cell response (L_bare roots {1,2}, no decaying mode ⇒ cell-filling shear not a
localized halo). **⇒ C: Branch P does NOT pin particle size/ξ as posed.** Banked B-SEPARATION: the discreteness that
DOES exist (Q_H∈ℤ, D2b depth-N) is a LABEL/depth structure ORTHOGONAL to the continuous mass-scale. D-POINTER: the one
FROZEN DOF (off-round transverse shear h_AB) is the exclusive route to size/mass discreteness — two candidate
mechanisms (sign-changing 𝒦 well; TT h_AB tensor eigenproblem), settled only by the gated **N5d** solve. Solver-first
(frozen DOF, NOT a metric verdict, NOT a mechanism); SCOPED to the round+perturbative corner, off-round UNENTERED.
Registry: SHARPENS (does not re-confirm) the prior continuum negatives; ξ stays a FREE family (consistent, N5 arc).

**★ NATIVE READOUT-MAP — TARGET-SELECTOR AUDIT (2026-07-06, BANKED + blind-verified,
`native_readout_map_selector_audit_results.md`, verifier aa75efc94282e7099) — OUTCOME B (solve-independent), C-form
identified, D-pointer.** Framed as the first test of the general native readout-map problem. Five armchair/CAS audits
(one per named source + a cross-cutting spatial→target-locking crux) all return B: NO target-indexed selector is
derivable from seal/involution (target-scalar), time-live/spinning (rotor axis = FREE zero-mode; discretization rides
imported ℏ, still no axis pin), φ-angular (Branch P coupling is SPATIAL-angular via n→h_AB→𝒦→φ, target-blind; a
metric function structurally cannot carry a target index — Charles's prime suspect, closed for CHANNEL-selection), or
whole-cell flux/read-surface (all native read observables are target-scalars; a 1/3-projector must hand-pick ê_a).
**Load-bearing + verifier-reproduced: the equivariance lock is RELATIVE (diagonal SO(2)); global target-SO(3) stays
an EXACT symmetry of the backreacted (n+h_AB+φ) functional because T_μν[n] is target-scalar (L2 AND L4 generic-R CAS
`diff=0`) ⇒ a spatial-axis pin NEVER transmits to a target pin ⇒ Outcome B is NOT gated on N5d** (the solve settles
minimizer SHAPE only). q=1/3 UNFORCED; native public charge = summed Q=1. C-form = a natively-derived target-SO(3)-
breaking coupling (V_ab / target-charged background / single-axis projector) — none native, adding one = new physics.
D-split: readout-map = (i) target-channel selection [CLOSED here] ⊥ (ii) depth/size discreteness [ALIVE, Branch P].
SHARPENS the no-selector theorem (adds solve-independence + four-source coverage); overturns no banked negative.

### ↓ 2026-07-05 EVENING ★ blocks (N5/ξ · solar light-sector γ=1 · D1 charge-channel · no-selector theorem · i-flow/ℏ) — ARCHIVED 2026-07-06 → `archive/LIVE_2026-07-05_evening_arc.md` (canonical = the result docs). ↓

### ↓ PM H3=A + H4-arc "current state" narrative (SUPERSEDED by the EVENING frontier above) — ARCHIVED out of
### LIVE 2026-07-05 EVENING to keep it lean → `archive/LIVE_H3_H4_arc_2026-07-05.md`. Canonical detailed record =
### HANDOFF.md §SESSION RECORD 2026-07-05 (PM) + the `node_H3_*.md` / `H4_*.md` result docs.
### ↓ (Both this session's chronological arcs are ARCHIVED out of LIVE to keep it lean — the CURRENT STATE block
### above is the only frontier. (a) The 2026-07-04→05 concentric-ω≠0-reframe → hopfion-route arc: HANDOFF.md
### §2026-07-05(AM) + `node_R0/_H1/_H2/_H3_*.md` + `native_hopfion_route_MAP.md`. (b) The H3=OUTCOME-A frontier
### bullets (superseded by the H4 arc): `archive/LIVE_hopfion_H3_arc_2026-07-05.md`. Canonical = the `node_*.md`
### / `H4_*.md` result docs. ↓

**STILL-OWED / PARKED THREADS (not the frontier, but not resolved — carry forward):** q=1/3 (now a proven-hard
NEW-PHYSICS gap — the no-selector theorem ⇒ needs a natively-DERIVED target anisotropy, else Q=1) + η=1/18 (needs
a Zρ_s² anchor) — both native re-derivations still OWED, NOT from Q_H. **[DONE this evening, no longer owed: the
i-flow/ℏ clock → Outcome 7 (structural i native, ℏ not derived); J(s) light-deflection → the full solar
light-sector predictions + data confrontation, UDT passes γ=1.]** **Pre-hopfion parked threads** (superseded AS FRONTIER by the hopfion arc but NOT resolved —
detail: `archive/LIVE_route_fork_E2_arc_2026-07-04.md` + HANDOFF_ARCHIVE §2026-07-04; `PURSUIT_CHARTER_2026-07-04.md` =
the traps list only): the durable **s=2μ/Z + J(s)** macro lever; **R3** = does the ladder survive a Route-B
universe cell; the other **5 D2 forks** (charter §4); **photon/EM-native re-grade** (#47-pos/#50); Charles's
**R1 flag** (adopt single-curvature-origin premise? lean=decline); **Bin-2 registry re-grades** at point of
use; destruction/black-holes PARKED post-emergence. (D4=ω≠0 was ADDRESSED this session → the ω≠0 reframe, closed.)

### ↓↓↓ HISTORICAL — the 2026-07-02 universe-cell/ladder arc layered updates ARCHIVED 2026-07-03 →
### `archive/LIVE_universe_cell_ladder_arc_2026-07-02.md` (canonical records = the results docs; this file's
### TOPMOST block above is the only frontier). Earlier arcs: `archive/LIVE_native_frame_round_static_2026-07-01.md`,
### `archive/LIVE_basin_D1_galerkin_arc_2026-06-30.md`.

## DURABLE CANON (must-not-lose)
- CANON **C-2026-06-14-1** (native S² carrier; B=1/A, EOS-softened interior) + **C-2026-06-18-1**
  (metric form derived from "remain relativistic") — both SURVIVE.
- seal = same-minus MIRROR FOLD = TIME REVERSAL (t→−t); Misner-Sharp mass = the cell's public charge
  (Q = 2 p_F); 7.004 = ln(1+z_CMB) via 1+z = e^φ. **D1-CORRECTED (2026-07-04): of the old
  area-form trio, only N=3 (+ the 1+3+5 algebra + structural-i) is NATIVE cargo; q=1/3 and
  η=1/18 are IMPORT-DEPENDENT → targets (d1_angular_constants_native_rederivation.md); the
  matter-cell core = even fold at FINITE depth (canon C-2026-07-03-3, φ→−∞ retired).**
- **This session's canon (2026-07-04/05):** **C-2026-07-04-1** = seal-involution SECTOR SPLIT — the spatial
  depth mirror φ→−φ governs STATIC seal BCs (φ odd ⇒ **Dirichlet φ(r_s)=0**, the flux seal), t→−t governs the
  TIME-ON sector; this CLARIFIES (does NOT overturn) the "seal = t→−t" line above. **C-2026-07-05-1** = P16:
  spinning matter stays **φ-blind** (spin→φ NOT natively available; the physical-metric minimal coupling that
  would give it = a forbidden import) — conservative, not a universal theorem. [Working-hypothesis, not canon:
  a UDT particle = a native Faddeev–Skyrme **HOPFION**, charge = Hopf linking Q_H∈π₃(S²)=ℤ — see the frontier block.]
- Provenance: commit scripts WITH results docs; AUDIT.md / step0_bridge*.py / dpf_verify_indep.py are
  Charles's untracked working files — leave them.
