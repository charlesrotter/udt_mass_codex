# LIVE — the only guaranteed-current file (READ ME FIRST)

**The "## ============ FRONTIER ... CURRENT STATE" block below is the ONLY current frontier** — read it and stop;
everything under the "↓↓↓ HISTORICAL ARC" / "SUPERSEDED" fences is labeled-stale detail (mine for history, not the
plan). `HANDOFF.md` / `STATE.md` are detailed history; **if they disagree with this file's CURRENT STATE block, the
CURRENT STATE block wins.**
**Read order (2026-07-07 PM-3):** LIVE.md FRONTIER (this block — the NEXT-SESSION PLAN is in the CURRENT STATE block
below) → **`derived_background_and_phi_coupling_DESIGN.md`** (the seamless-pickup spec: THREAD A = redo `x_max`
PROPERLY from the observer FRAME-RELATION → the derived data-blind BACKGROUND, do FIRST; THREAD B = the native
φ-matter source → MASS / PARTICLE EMERGENCE; cosmology validation is OUT OF SCOPE) → `udt_phi_blindness_relaxation_results.md`
(Thread B: the source `α·ξ·e^{αφ}ρ²I_r` + the restoring channel, blind-verified) → `udt_canonical_geometry.md`
§1.4 (frame-relation) / §10.4 (Misner–Sharp) / §12.7 (the polynomial + D-POLY-1 gap) for Thread A → CLAUDE.md "How we
work" + "DRIVER TRIGGERS" + the `.claude/skills/` discipline skills → HANDOFF.md §SESSION RECORD 2026-07-07 (PM) →
INDEX.md (repo map). Prior arcs (rung-resonance, Stage-2 static) are CLOSED/superseded — under the fences below, mine
only for history.

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

## ============ CURRENT STATE (2026-07-07 PM-3 — rung-resonance test CLOSED (do-not-build; matter-structure wall survives the discrete ladder); the x_max cosmology ponder was a WASH (my category error, corrected via the SNe frame-relation reading); DURABLE STEP = φ-matter coupling UNFROZEN → the particle-emergence door. NEXT SESSION (spec: `derived_background_and_phi_coupling_DESIGN.md`): Thread A = redo x_max PROPERLY for the derived BACKGROUND (do FIRST), then Thread B = pivot to MASS + PARTICLE EMERGENCE. Cosmology validation OUT OF SCOPE.) ============

**➤➤➤ LATEST (2026-07-07 PM-3 — REFRAME + wind-down): the whole "no-preferred-frame / homogeneous universe" tangle was
a CATEGORY ERROR (mine), corrected via the canonical SNe work.** UDT's redshift is a **FRAME-RELATION** (`1+z=e^{φ(r)}`,
observer-centered, `udt_canonical_geometry.md` §1.4 + shell-theorem cancellation): every observer at their own `φ=0`,
identical isotropic law, **no preferred frame, NO cosmic center, NO Copernican problem.** So no-preferred-frame SURVIVES
(as the frame-relation); only the finite-invariant-*distance* `x_max` postulate is DROPPED. The banked "no homogeneous
universe" results (`udt_no_homogeneous_universe_results.md`, `udt_phi_blindness_relaxation_results.md`) are the
PHYSICAL-FIELD layer — a different question, NOT the operative cosmology; frame-notes added to all three docs +
`archive/udt_max_distance_invariance_FRAME.md` banner reframed + boost-deriv demoted (re-coordinatization of `1+z=e^φ`). **The
canonical SNe fit is SIMPLE + WORKS:** `1+z=e^{φ(r)}`, `φ(r)`=derived cubic, `d_L=r(1+z)` (static reciprocity, no FLRW
`(1+z)²`), Pantheon+ 1701 SNe = 0.166 mag RMS (1.08× ΛCDM), ZERO free cosmological params. **BAO/CMB old work is
POORLY SCAFFOLDED (polynomial ansatz D-POLY-1 + the 1101 anchor) — do NOT lean on it.** LESSON: don't over-literalize
the observational frame-relation as a physical field, and don't overmodel (I built ISW/recycling mechanisms + homogeneity
field-solves on a category error; Charles corrected via the SNe work). **LIVE FORWARD THREAD (needs a fresh session —
context ~60%): the PARTICLE-EMERGENCE door** — relaxing φ-blindness (α<0) gave matter a RESTORING channel (I_r sources
φ → supports I_r vs draining) for the matter-structure wall that killed the resonance test; the coupled `(f,φ,ρ)` solve
testing whether it closes a cell with `I_r>0` is the core test.
**➤➤ NEXT-SESSION PLAN (Charles) — spec = `derived_background_and_phi_coupling_DESIGN.md`. SEQUENCE: THREAD A FIRST
(flesh out the universe BACKGROUND), THEN pivot to THREAD B (MASS + PARTICLE EMERGENCE). Cosmology VALIDATION (SNe/BAO/CMB)
is OUT OF SCOPE — self-evident later; do not get pulled into it.**
- **THREAD A (do first) = redo `x_max` PROPERLY from the OBSERVER FRAME-RELATION** (`1+z=e^{φ(r)}`, §1.4 canonical
  geometry; NOT the "invariant distance" error) → a DERIVED data-blind BACKGROUND for the particle sector: derive the
  φ(r) FORM (= the D-POLY-1 gap), the φ→∞ asymptotic edge, the depth anchor natively (1101/7.004 OUT). Use the CURRENT
  native two-player operators, NOT the legacy Einstein+KG/μ² machinery. GRAB from old work: frame-relation §1.4,
  `d_L=r(1+z)`, Misner–Sharp marginal; do NOT grab polynomial-as-derived / 1101 anchor / BAO-CMB scaffolding.
- **THREAD B (then pivot) = the native direct source `α·ξ·e^{αφ}ρ²I_r`** → the matter-structure RESTORING channel +
  matter L-selector; derive/characterize `α` (verdict C; α<0 opens it; re-adjudicate the α=−2 import-tag); the coupled
  `(f,φ,ρ)` solve = does a cell close with `I_r>0` SUPPORTED. A furnishes the background B embeds a matter-coupled cell
  into = the particle-emergence setup we never had. Below the fences = CLOSED-ARC history (archived x_max detour, rung-resonance, Stage-2) — mine for history, NOT the plan.

### ↓↓↓ THIS SESSION'S DETOUR — ARCHIVED (2026-07-07 PM-3). Most of the session chased an INCORRECT vision (the
### `x_max` "invariant maximum distance" postulate + a homogeneity/Copernican field-solve) that was a CATEGORY ERROR —
### over-literalizing the redshift FRAME-RELATION as a physical field. Corrected by the PM-3 block ABOVE (redshift =
### observer frame-relation, no preferred frame, no center). Full detour + the lesson →
### **`archive/LIVE_xmax_homogeneity_detour_2026-07-07.md`** (incl. the archived x_max FRAME + boost docs). DURABLE
### residue kept live (two lines):
### - **φ-MATTER COUPLING (Thread-B foundation, blind-verified — `udt_phi_blindness_relaxation_results.md`):** φ-blindness
###   (α=0) is a CHOSE lever NOT forced; native direct source `α·ξ·e^{αφ}ρ²I_r`; relaxing it (α<0) opens the
###   matter-structure RESTORING channel (the particle door) + a matter L-selector. Owed: derive α (p16 verdict C).
### - **RUNG-RESONANCE TEST CLOSED (blind-verified — `classB_rung_resonance_classification_results.md`):** no rung is a
###   TRUE candidate → do-not-build; the matter-structure wall SURVIVES the discrete ladder = WHY particle emergence
###   needs the φ-coupling unlock (Thread B). ↑↑↑

### ↓↓↓ SUPERSEDED-as-frontier (2026-07-07 AM — the RUNG-RESONANCE arc, now CLOSED). The OWED-FIRST identity gate
### PASSED (`classB_rung_resonance_owed_first_adjudication.md`) and the NO-BUILD per-rung RESONANCE TEST RAN →
### do-not-build; the matter-structure wall SURVIVES the discrete ladder (`classB_rung_resonance_classification_results.md`,
### blind-verified). See the two-line summary in the ARCHIVED-DETOUR block above. Spec/gate-checks:
### `classB_rung_resonance_prebuild_test_DESIGN.md`, `classB_embedded_rung_gatecheck_results.md`. (This block was the
### live frontier earlier in the session; its stale "NEXT ACTION = run the resonance test" is DONE.) ↓↓↓

### ↓↓↓ SUPERSEDED-as-frontier (2026-07-06 EOD-3): the static-collapse diagnosis arc below is DONE (all committed/
### pushed/blind-verified). Chain: Stage-2b impl `6a0ac15` → preflight READY `d3a50a0` → S-Dir pilot=L-COLLAPSE
### `652b484` → mechanism mis-diagnosed `f02f3f9` → RETRACTED `d729dd4` → soft-mode blind-CONFIRMED `5c6f6ac`
### (free-boundary/φ-ρ gauge degeneracy) → gauge audit `da6bcfa` (ρ/φ gauge removable by 2-pin; L undetermined;
### q_raw can't distinguish L) → MS/embedded-boundary audit `753ff00` (M=−q derived; embedded gives mass-size
### RELATION+ratios not absolute L; deliverable=ratios) → Class-B seal diagnostic `164ea11` (Dirichlet φ(r_s)=0
### removes the φ-offset gauge + makes Hseal a REAL closure, but isolated Class-B doesn't close → needs a receiver)
### → rung gate-checks `3e0eca7` (anchor cancels in ratios; H_amb(N)=0 dead knob → flux/depth match = the no-band
### wall). Detail below + in the named result docs. ↓↓↓

### ↓ N5d Stage-2 static-arc DETAIL (historical RESUME-HERE) + Stage-2b PINNED FORMULAS — ARCHIVED 2026-07-07
### → `archive/LIVE_stage2_static_arc_2026-07-06.md` (the arc is CLOSED; canonical = the `n5d_stage2_*_results.md`
### docs + `cell_solver_f2d.py`; the arc-chain fence above is the lean summary). ↓

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

**STILL-OWED / PARKED THREADS — PRE-STAGE-2 carry-forwards (from ≤2026-07-05; NOT the current frontier — the
frontier is the rung-resonance test at the TOP. These are older open items to revisit later, not the next action):**
q=1/3 (a proven-hard NEW-PHYSICS gap — the no-selector theorem ⇒ needs a natively-DERIVED target anisotropy, else
Q=1) + η=1/18 (needs a Zρ_s² anchor) — both native re-derivations still OWED, NOT from Q_H. (Resolved earlier, no
longer owed, kept for context: the i-flow/ℏ clock → Outcome 7 (structural i native, ℏ not derived); J(s)
light-deflection → the full solar light-sector predictions, UDT passes γ=1 — both 2026-07-05.) **Pre-hopfion parked
threads** (detail: `archive/LIVE_route_fork_E2_arc_2026-07-04.md` + HANDOFF_ARCHIVE §2026-07-04;
`PURSUIT_CHARTER_2026-07-04.md` = the traps list only): the durable **s=2μ/Z + J(s)** macro lever; **R3** = does the
ladder survive a Route-B universe cell; the other **5 D2 forks** (charter §4); **photon/EM-native re-grade**
(#47-pos/#50); Charles's **R1 flag** (adopt single-curvature-origin premise? lean=decline); **Bin-2 registry
re-grades** at point of use; destruction/black-holes PARKED post-emergence. (D4=ω≠0 was addressed 2026-07-04/05 → the
ω≠0 reframe, closed.)

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
