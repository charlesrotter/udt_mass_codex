# LIVE — the only guaranteed-current file (READ ME FIRST)

**The "## ============ FRONTIER ... CURRENT STATE" block below is the ONLY current frontier** — read it and stop;
everything under the "↓↓↓ HISTORICAL ARC" / "SUPERSEDED" fences is labeled-stale detail (mine for history, not the
plan). `HANDOFF.md` / `STATE.md` are detailed history; **if they disagree with this file's CURRENT STATE block, the
CURRENT STATE block wins.**
**Read order (2026-07-07):** LIVE.md FRONTIER (this block — the RESUME-HERE directive at its TOP is the next action =
the NO-BUILD per-rung RESONANCE TEST) → **`classB_rung_resonance_prebuild_test_DESIGN.md`** (the spec: §OWED FIRST =
the blind re-derivation to do first, then the per-rung classification) → `classB_embedded_rung_gatecheck_results.md`
(why the junction is flux/depth, not H) → the Stage-2 arc RESULT docs only if needed (`n5d_stage2_*_results.md`,
`n5d_stage2_MS_boundary_selector_audit_results.md`; the ladder law lives in `stageD_frozen_forecast.md` /
`ladder_lemmaD_sealing_amplitude_results.md`) → CLAUDE.md "How we work" + "DRIVER TRIGGERS" + the `.claude/skills/`
discipline skills → HANDOFF.md §SESSION RECORD 2026-07-06→07 (EOD-3) → INDEX.md (repo map). The closed Stage-2
static-arc detail is archived → `archive/LIVE_stage2_static_arc_2026-07-06.md` (mine only for history).

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

## ============ CURRENT STATE (2026-07-07 — the full Stage-2 static arc is CLOSED (impl→pilot→collapse→gauge→L-selection→MS→Class-B→rung gate-checks, all committed/pushed/blind-verified); NEXT = a NO-BUILD per-rung RESONANCE TEST (Charles's Der 1-7) that GATES whether a Class-B embedded-rung build is worth it) ============

**➤➤ OWED-FIRST DONE (2026-07-07): the load-bearing identities are BLIND-CONFIRMED + the old numbers re-confirmed —
but the classification now hinges on TWO reconstruction premises, one of which (`m_amb(N)`) needs Charles.** Record:
`classB_rung_resonance_owed_first_adjudication.md` (agents `aa57c76d…` blind-derivation + `a68053f6…` numbers).
Two independent blind agents: (A) re-derived `π_ρ'=Zρφ'²−ξρI_r+κN_w²I_{4θ}/ρ³` → `I_{r,req}(N)` and `E_ang`→`A_N`
from the NATIVE ACTION (walled off from the DESIGN/classB docs) = EXACT match (CAS; 2φ'ρ' cancels; π_ρ convention
confirmed in-source); (B) re-ran the CAS + own bounded solves = `q=+3.95/+3.82`→π_φ,amb=4.0, seeded `I_r` DRAINS to
~1e-17/1.1e-5, two-branch floor 0.786/2.679 — all re-confirmed. **TWO REFINEMENTS surfaced (both = DESIGN-doc
"reconstruct/flag" items, NOT refutations): (1) the I_r branch is controlled by `π'_{ρ,amb}(N)` (ambient momentum-
DERIVATIVE, set by the ambient's OWN R4), NOT `sign(ρ'_amb)`; (2) `m_amb(N)` in A_N is UNDETERMINED — Agent A's seal
condition `E_ang(r_s)=2+H_amb` + gate-check-b's `H_amb(N)=0` ⇒ possibly `m_amb≡2` (constant), making A_N vary with
the rung ONLY through ρ_s(N) and N_w. Whether m_amb = the geometric "2" / H_amb(=0) / a separate ambient MS mass is
a PHYSICS identification = Charles's fork before any A_N column is banked as a build gate.** ⇒ NEXT = get Charles's
read on the `m_amb` reconstruction, THEN run the per-rung classification with both ambient inputs (`π'_{ρ,amb}(N)`,
`m_amb(N)`) explicitly tagged reconstructed-vs-derived.

**➤➤ NEXT ACTION (2026-07-07, after Charles's m_amb read): run the NO-BUILD per-rung RESONANCE TEST (spec =
`classB_rung_resonance_prebuild_test_DESIGN.md`, Charles's Derivations 1-7). OWED-FIRST identity gate = PASSED.** The Stage-2 static arc has CONVERGED on
this: the isolated Class-B charged cell can't close (needs a receiver); the universe-ladder RUNG is the discrete
receiver; the gate-checks showed (a) the z_CMB anchor cancels in ratios to leading order (`q_i/q_j→(N_j+1)/(N_i+1)`),
(b) `H_amb(N)=0` is a DEAD KNOB, so the real junction is a FLUX/DEPTH match (`q_cell=q_N`, `Δφ_cell=Δφ_N`, NOT H, NOT
raw `φ_s=φ_N` — Class B fixes `φ_s=0` so depth matches a DIFFERENCE `Δφ_cell=φ_c`). **The old no-band wall was NOT a
flux wall (`q≈3.8-4.0` already closed `π_φ`) — it was a MATTER-STRUCTURE wall (R4/R5): Branch A needs `I_r>0` but
minimal matter drains to `I_r≈0`; Branch B blocks on angular-skin energy R5.** So discreteness helps ONLY if a rung
hits a RESONANT boundary target. **THE NEXT PASS (no build): for each rung N compute `(q_N, Δφ_N, I_{r,req}(N), A_N)`
[I_{r,req}(N)=(q_N²/(Zρ_s³)+κN_w²I_{4θ}/ρ_s³−π'_{ρ,amb}(N))/(ξρ_s); A_N=E_{ang,natural}−m_amb(N)] and classify: dead /
positive-branch (I_{r,req}≈0) / turning-branch (A_N≈0) / TRUE candidate (both). BUILD GATE: only a TRUE candidate
justifies a bounded single-rung Class-B build; if none, DO NOT build (matter-structure wall survives).** Matter is
φ-blind so a depth match ⇏ I_r>0 directly — escape is either resonance (cheap, no-build) or geometry-coupled (needs
build). Class-B seal is already coded (`cell_solver_f2d.py` `seal_phi="B"`). Reconstruct `π'_{ρ,amb}(N)`, `m_amb(N)`,
`E_{ang,natural}` from the rung + minimal-matter solution (ladder does NOT tabulate them — flag reconstructed-vs-derived).
**Template tripwire: run as OBSERVE (which rungs hit resonance), never TARGET the lepton ladder.** ⚠ **OWED FIRST
(Charles 2026-07-07): a BLIND re-derivation of the load-bearing identities before the classification is trusted —
independently re-derive `I_{r,req}(N)` (from R4: `π'_ρ=Zρφ'²−ξρI_r+κN_w²I_{4θ}/ρ³`) and `A_N` (from R5), from the
native action NOT from the DESIGN doc (which only TRANSCRIBES Charles's Der 1-7), and confirm the old no-band
two-branch numbers (`q≈3.8-4.0` closed π_φ; minimal matter `I_r→0`). Frame NEUTRALLY (adjudicate, not confirm — this
session's residual-artifact lesson). Only then trust the (q_N,Δφ_N,I_{r,req},A_N) classification as a build gate.**
Records: `classB_rung_resonance_prebuild_test_DESIGN.md` (§OWED FIRST), `classB_embedded_rung_gatecheck_results.md`.
NO Outcome A/B, NO
pin/continuum, NO π₃; π₂ static S-Dir tile; DESIGN/PROVISIONAL/Outcome D.

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
