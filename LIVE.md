# LIVE — the only guaranteed-current file (READ ME FIRST)

**The "## ============ FRONTIER ... CURRENT STATE" block below is the ONLY current frontier** — read it and stop;
everything under the "↓↓↓ HISTORICAL ARC" / "SUPERSEDED" fences is labeled-stale detail (mine for history, not the
plan). `HANDOFF.md` / `STATE.md` are detailed history; **if they disagree with this file's CURRENT STATE block, the
CURRENT STATE block wins.**
**Read order (2026-07-06 EOD-2):** LIVE.md FRONTIER (this block — the RESUME-HERE directive at its TOP is the next
action = IMPLEMENT N5d Stage-2b; Gate-0 CLEARED, formulas pinned) → the Stage-2 docs (`n5d_stage2_corelaxed_matter_DESIGN.md`
→ `n5d_stage2a_cas_results.md` → `n5d_stage2b_gate05_report.md`) → HANDOFF.md §SESSION RECORD 2026-07-06 (EOD-2). (The
prior EOD-1 read-order below is historical:) → **HANDOFF.md TOP (2026-07-06 session record)** → the N5d chain
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

## ============ CURRENT STATE (2026-07-06 EOD-3 — N5d Stage-2b IMPLEMENTED + gate GREEN + blind-verified → preflight READY → S-Dir PILOT RAN = L-COLLAPSE (Outcome D, blind-verified); NEXT = Charles picks the solver-completeness fork) ============

**➤➤ RESUME HERE / NEXT ACTION (2026-07-06 EOD-3): the bounded static S-Dir co-relaxed π₂ pilot has RUN and its
result is L-COLLAPSE — TOOL-LIMITED / Outcome D, blind-verified.** The solve drives the cell length L→0 (from L0=1;
0.14→0.037→0.017→0.0076 over 150 iters), the seal-closure `Hseal` floors at ≈−6e-3 and NEVER reaches 0, and
`cond_equil`→float64 floor. Independent adversarial verifier (agent `ae5e8adcc16071d11`) hunted for a finite-L
closed cell across seed-L∈{0.05…2.0} and found NONE — the L→0 is a spurious/degenerate root, NOT a solver artifact
(equilibrate on/off + Nr=12/16 all agree), and the collapse is in the BASE geometry+matter closure, NOT the new
shear sector (shear rows ~40× smaller). Record: `n5d_stage2_sdir_pilot_results.md` (+ `n5d_stage2_sdir_pilot.py`/
`.json`). **NO converged tile lead, NO pin/continuum, NO Outcome A/B, NO π₃ claim.** MISMATCH→SOLVER: the collapse
indicts the STATIC + S-Dir + block-diagonal + ℓ=2-only CLOSURE of this corner, never the metric/mechanism — so the
**NEXT ACTION is a CHARLES DECISION on the solver-completeness fork** (what this tile LEAVES OUT, none to be added
unprompted): (a) higher-ℓ shear; (b) the **S-JC2 seal fork** (constant-a2 null, unresolved, no FIX-2); (c) the
**non-static / time-live sector** (this was a STATIC solve; the seal=t→−t canon + Charles's hunch put dynamics in a
separate sector — prime suspect); (d) unfrozen off-diagonal / Branch fork. π₂ tile ONLY; DESIGN/PROVISIONAL/Outcome
D throughout. (The prior EOD-3 build/preflight narrative — Stage-2b impl `6a0ac15`, gate GREEN, preflight READY —
is retained below/in the pinned-formula block; it stands.)**

**What Stage-2b implemented (all pinned, CAS + blind-verified — the historical build reference below is retained):**
Read `n5d_stage2_corelaxed_matter_DESIGN.md` + `n5d_stage2a_cas_results.md` (§1-8) + `n5d_stage2b_gate05_report.md`
(λ=−½). **THE PINNED FORMULAS (all CAS + blind-verified; now LIVE in `cell_solver_f2d.py` `fields()`/`H_of_r()`):**
- **Off-round f-PDE** (Stage-2a §1, λ-free, matches base at s=0): `A/f_r = ξρ²sinθ + κN²sin²f·e^{s}/sinθ`;
  `B/f_θ = ξ·e^{−s}·sinθ + κN²sin²f/(ρ²sinθ)`; `pot = (N²sinf cosf/sinθ)[e^{s}(ξ+κf_r²) + κf_θ²/ρ²]`; `s = a2(r)P2(μ)`.
- **Live shear source** (REPLACES the frozen `Tshear`/`src`): `Tshear_live = −(ρ²/4)·T_s` with
  `T_s = (ξ/ρ²)[N²e^{s}sin²f/sin²θ − f_θ²e^{−s}] + (κN²/ρ²)f_r²e^{s}sin²f/sin²θ` — the **λ=−1/2** coupling
  (Gate-0.5, blind-verified: NOT the naive +(ρ²/2)T_s, which was 2× + sign-flipped). φ-blind, h_AB-side.
- **ρ-EOM matter term: UNCHANGED** (Stage-2a §6: `δS_m/δρ` is s-independent → already the base's `ξρI_r − κN²I_4θ/ρ³`).
- **φ off-round correction: UNCHANGED** (certified `n5d_shear.phi_source_offround_correction = +(1/5Z)e^{−2φ}a2'²`).
- **Off-round Hseal** (Gate-0.1 + Gate-0.5): base H **+ shear kinetic `+(1/10)e^{−2φ}ρ²a2'²`** + off-round matter
  moments `−(ξ/2)ρ²I_r + (ξ/2)(I_θ^{e^{−s}} + N²I_s^{e^{s}}) − (κN²/2)I_4r^{e^{s}} + (κN²/2)I_4θ/ρ²` (fold `e^{±s}`
  INSIDE the θ-integral: I_θ×e^{−s}, I_s×e^{s}, I_4r×e^{s}; I_r, I_4θ unchanged) − 2. → base H at s=0.
- **Frozen `stress_profiles.npz`: RETIRED from the residual** (embedding audit §4d/§4g invalidated it for verdicts);
  keep only as an OPTIONAL initial-guess seed. **S-Dir = first well-posed tile; S-JC2 constant-a2 null UNCHANGED (no FIX-2).**
**TESTS (DONE — GREEN, `tests/test_n5d_stage2.py`, 8 required gates as 12 functions):** round-limit (s=0→base
byte-identical) · φ-blindness · self-stress (source = −(ρ²/4)T_s, NOT +(ρ²/2)) · rigid hedgehog (T_s(L2)=0 @
s=0,f=θ,N=1) · no-flat-source (residual byte-unchanged with npz/source_interp disabled) · Hseal round-limit ·
K=1/5 pin (H shear kinetic ↔ φ-correction) · preflight (square, finite Jac, both BCs, FIX-1 on, bounded, one
foreground process). Also updated: `test_n5d_roundlimit` (rigid null), `test_n5d_offround` (live-source φ-blind),
`test_n5d_pullback` (frozen src/Tshear now a SEED helper, guarded OUT of the residual). **ANTI-HANG binding. NO
finite-L target/penalty/barrier/anti-collapse/fitted-scale/mass-anchor. TOPOLOGY: π₂ tile ONLY — CANNOT bank
Outcome A/B for the π₃ hopfion question (open premise for Charles).** Stage-2 PILOT = SEPARATE Charles gate (above).
Status: DESIGN/PROVISIONAL/Outcome D throughout.
**Do NOT run `branchGP` (fenced wrong frame).**
**COMMIT + PUSH discipline (binding, standing): commit per logical milestone (the residual edit, then each test as
it passes) AND `git push origin main` in the SAME step as every commit** (Charles 2026-07-06 — never leave commits
local; see CLAUDE.md "Repo discipline" + memory `always-push-on-commit`). End every commit body with the
`Co-Authored-By` trailer.

### ↓↓↓ SUPERSEDED (2026-07-06 EOD → EOD-2): the "diagnose N5d conditioning" frontier below is DONE. Chain of this
### session (all committed/pushed, PROVISIONAL/Outcome D): conditioning diagnosis (Outcome-D artifact, not a soft mode;
### 3 near-null modes) → **FIX-1** (equilibration: column-scale + damped lstsq in `newton_lm_solve`) → FIX-3 (structured
### seed INEFFECTIVE — round base flattens) → shear-forcing audit (forcing strong+correct; tiny a2 = L-collapse) →
### **pullback audit** (Registration-B: source at current-L physical r) → **ρ²/2 frame factor** (blind-verified) →
### embedding audit (frozen flat hopfion INVALID for verdicts → retire Stage-1, go Stage-2 co-relaxed) → Stage-2 DESIGN
### → Stage-2a CAS (f-PDE, T_s sign +, ρ²/2 emergence; blind-verified) → Stage-2a H audit (dH/dr=0 geo+shear) →
### Stage-2b Gate-0 (BLOCKER: matter→geo coupling −2×) → **Gate-0.5 (RESOLVED λ=−½, blind-verified)**. Docs:
### `n5d_stage1_conditioning_diagnosis.md`, `n5d_stage2_corelaxed_matter_DESIGN.md`, `n5d_stage2a_cas_results.md`,
### `n5d_stage2b_gate0_report.md`, `n5d_stage2b_gate05_report.md`; scripts in `h4_scripts/n5d_stage2*`. ↓↓↓

### ↓ 2026-07-06 EOD-1 readout-map + provenance-floor detail (readout-map selector→B / depth-size→C; provenance floor CLOSED both sides; N5d built) — ARCHIVED 2026-07-06 EOD-2 → `archive/LIVE_2026-07-06_EOD1_readout_provenance_arc.md` (canonical = the result docs: `native_readout_map_*_results.md`, `pre_native_era_census.md`, `macro_spine_provenance_2026-07-06.md`). ↓

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
