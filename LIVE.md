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

## ============ CURRENT STATE (2026-07-06 EOD-3 — N5d Stage-2b IMPLEMENTED+gate GREEN → preflight READY → S-Dir PILOT = L-COLLAPSE → soft mode = REMOVABLE ρ/φ GAUGE + UNDETERMINED L FLAT DIRECTION (blind-confirmed; gauge quotiented, L-selection = the physics boundary); q_raw≡0 for mirror cells; NEXT = Charles picks the L-selection fork) ============

**➤➤ RESUME HERE / NEXT ACTION (2026-07-06 EOD-3): the static S-Dir π₂ collapse is now fully DIAGNOSED and
BLIND-CONFIRMED (gauge audit, `n5d_stage2_gauge_audit_results.md`). The soft mode is a MIX:** (1) a **removable
global ρ-rescale + φ-offset GAUGE** (cos(v_ρ,ρ)=+1.000, cos(v_φ,1)=+1.000; Hseal moves along it while ρ-shape/matter-
moments/q_raw stay fixed ⇒ Hseal is gauge-dependent) — a **2-pin category-A fix [fix ρ(r_c) + fix φ(r_c)]** removes it
(cond 3.4e8→7.6e7, workable-not-pristine; q_raw invariant to 1e-13) and gives a well-conditioned Hseal=0 closed cell
at a CHOSEN L; PLUS (2) an **undetermined L flat direction** — even after the gauge-fix, H(r_s)=0 does NOT pin L (a
free-L solve runs L away to ~1e3/1e6/negative at Hseal~0). **Unique closure OPEN.** ⚠ **SELF-CORRECTION (2nd this
session, blind-caught): my "q_raw varies with L ⇒ L is a physical modulus" was WRONG — q_raw=Zρ_s²φ'(r_s)≡0 on-shell
for EVERY Class-A mirror cell (φ'(r_s)=0 is a mirror BC), so q_raw can't distinguish L-cells; the q_raw-vs-L trend I
saw was a convergence residual.** So whether L is a physical modulus vs a scaling redundancy is ITSELF OPEN (q_raw≡0
can't tell — and the seal flux + M_readout are structurally ZERO for these mirror cells). **BLIND VERIFIER (agent
`a2969cef559b1ac72`, neutral gauge-vs-modulus framing, forbidden the audit scripts): gauge CONFIRMED, 2-pin fix
CONFIRMED (cond~8e7 caveat), L-modulus PARTIAL (conclusion "no unique L / OPEN" confirmed; the q_raw evidence
refuted).** Records: `n5d_stage2_gauge_audit_results.md` + `n5d_stage2_gauge_audit.py`. **The category-A work is DONE:
the φ/ρ gauge ambiguity is removed; what remains is L-SELECTION.**

**L-SELECTION AUDIT DONE (2026-07-06, `n5d_stage2_Lselection_audit_results.md`; native-geometry synthesis of
blind-verified repo results + 2 self-correcting forward-eval tests):** after gauge quotient exactly ONE unselected
scalar remains = L, and the **isolated static Class-A tile PROVABLY cannot select it** (free-L runs away incl.
negative L; the flat direction is NOT a simple geometric rescaling — tested; q≡0 gives no distinguisher). ⇒
**L-selection is inherently EXTERNAL/embedding.** The native, derived, independent L-selector is the **embedded
Hamiltonian match `H_cell(r_s)=H_amb(r_s)` (+ `π_cell=π_amb`)** (`embedded_cell_closure_H_amb_results.md`). Key
structural results: (i) **q≠0 and L-selection are unlocked by the SAME move** — Class-A mirror (φ'(r_s)=0, q≡0) →
Class-B (Dirichlet φ(r_s)=0, φ' free, q≠0) + exterior match; the current tile is the legitimate ISOLATED Class-A
completion (NOT a superseded BC — checked CANON.md directly; class choice = Charles's call). (ii) embedding SUBSUMES
the 2 gauge pins (Class-B Dirichlet removes φ-offset; ambient-match removes ρ-scale). (iii) **the static embedded
route is TOOL-LIMITED (depth-stiffness wall, `NEGATIVES_REGISTRY.md:20-32`, CONDITIONS-CHANGED under ω≠0)** and the
ABSOLUTE scale is unpinned without a cosmic anchor (universe MS / z_CMB=data-forbidden). (iv) static seal ⇒ NO
time-live needed (sector split). **NEXT = a CHARLES fork decision** (none unprompted): the audit shows the forks
CONVERGE — recommend (a) **reframe to SCALE-FREE RATIOS** (absolute L is cosmic; take the tile's shape/ratios,
matches the data-blind "predict RATIOS" posture — lower-risk, purity-clean) OR (b) the **embedded + ω≠0
(rotating/time-live) sector** (where the depth-stiffness wall lifts and the charged Class-B seal is natural). A
prerequisite for any charged/embedded work = the Class-A→Class-B seal-BC change (Dirichlet φ(r_s)=0), which is
implementation (Charles-gated). Open convention flag: M=−q vs M=+q sign + p_F factor-of-2 (matter once charge is live).
**MS/EMBEDDED-BOUNDARY SELECTOR AUDIT DONE (`n5d_stage2_MS_boundary_selector_audit_results.md`):** the embedded/MS
package (B1 `[h_AB]=0`, B3 `π_cell=π_amb`, B4 `H_cell=H_amb`=size-selector, B5 `m=−q−q²/r`) is a CLOSED native
data-blind framework for a mass–size RELATION + ratios but does NOT select absolute L (B4 needs the ambient/universe
MS mass; only pin = z_CMB via φ_seal=7.004 = DATA-forbidden). SIGN: **`M=−q` DERIVED** (metric identity `m=−q−q²/r`,
code-consistent `M_readout=−q_raw`, gives POSITIVE mass with φ'(r_s)<0); `M=+q`=reporting deviation; genuinely-open
tension = φ-depth-sign (φ<0 deep) ↔ positive-mass-far-field (φ>0) reconciliation (Charles's canon call); p_F factor
separate+unpinned. Data-blind deliverables = RATIOS (compactness `2M/R=1`, shape profiles; with Class B, mass ratios
`M_i/M_j=q_i/q_j`); Class-A NOW gives q=M=0 (shape ratios only). Class-B impl = bounded seal-BC swap (φ'(r_s)=0→
φ(r_s)=0), safe as a DIAGNOSTIC (flag isolated-charge consistency + DOF recount), gated. **Honest static-tile
deliverable = RATIOS, not absolute mass/size.** **NO Outcome A/B, NO pin/continuum, NO π₃; π₂
tile ONLY; DESIGN/PROVISIONAL/Outcome D.** (Session chain, all committed+pushed+blind-verified: Stage-2b impl
`6a0ac15` → preflight READY → S-Dir pilot=L-COLLAPSE `652b484` → mechanism mis-diagnosed `f02f3f9` → RETRACTED
`d729dd4` → soft-mode blind-CONFIRMED `5c6f6ac` → gauge audit = ρ/φ-gauge + L-flat, q_raw≡0 (here). LESSON, now TWICE:
I over-read a residual/valley artifact as physics twice this session; NEUTRALLY-framed blind verifiers caught both —
frame every verifier to adjudicate, never to confirm my read. Pinned-formula block below stands.)**

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
