# HANDOFF — Resume Instructions and Perspective

> **READ `LIVE.md` FIRST** — it is the short, only-guaranteed-current file (frontier + next action).
> This HANDOFF is the detailed record; if it disagrees with LIVE.md, LIVE.md wins. (P5, 2026-06-23.)
> **CURRENT (2026-07-06 EOD): after LIVE.md (its RESUME-HERE = DIAGNOSE the N5d conditioning), read the
> `## SESSION RECORD 2026-07-06` block immediately below — readout-map (channel B + depth/size C) → N5d preflight
> fail → the full PROVENANCE-FLOOR excavation (kap8 #77 quarantine + date census + macro-spine, floor CLOSED both
> sides) → N5d solver BUILT → Stage-1 pilot = TOOL-LIMITED (Outcome D, non-converged/near-singular). NEXT = diagnose
> the N5d Jacobian conditioning (gauge vs scaling vs physical soft mode) before any pin-vs-continuum reading.** The
> 2026-07-05 EVENING record follows it (prior session).

## SESSION RECORD 2026-07-06 (Opus — readout-map B+C → provenance floor CLOSED both sides → N5d BUILT → Stage-1 pilot TOOL-LIMITED)

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

## SESSION RECORD 2026-07-05 (EVENING) (Opus — N5/ξ arc CLOSED (ξ parked) → SOLAR LIGHT-SECTOR arc (UDT passes γ=1) → D1 CHARGE-CHANNEL MAP → NO-SELECTOR THEOREM → i-FLOW/ℏ-CLOCK MAP; all blind-verified + pushed)

Charles directed step-by-step; every node armchair/CAS, DATA-BLIND (except the one authorized solar-data
confrontation), committed + blind-verified before the next (all on `main`, pushed). No compute solves run — the
gated non-perturbative N5d solve was NOT opened. pytest 32/1xfail throughout.

**1. N5 whole-cell criticality / ξ-anchor arc — CLOSED; ξ PARKED as a free family (Charles decision).**
- **N5 MAP** (`H4_N5_whole_cell_criticality_MAP.md`, verifier aabaa3929f5f0864f): the named ξ-anchor candidate
  `E_ang(core)=2` rides the RETIRED concentric/private-cell MIGRATION (shared seal + outer-fold H_amb≡0 + carve) —
  it CANNOT transport to the no-wall hopfion frame C(a). Reframe = keep criticality on the WHOLE cell, hopfion as
  content. Verdict: E_ang(core)=2 value survives, migration/private-core locus undercut.
- **N5a** (`H4_N5a_..._rederivation_results.md`, verifier ad85bcc2907db3df4): whole-cell criticality re-derived
  OFF the carve does NOT pin ξ — it is ONE relation (M/R=c²/2G) with R the unpinned data-blind dilatation modulus
  (F7 §B.2 gap corroborates). The E1 migration's apparent ξ-pin was ENTIRELY the carve (pins ρ_c(ξ,κ), not ξ).
  **CF-N5c:** negative #75's ξ<2-vs-ξ≥2 contradiction does NOT transport — dissolves via CARRIER SWAP (toroidal π₃
  hopfion's virial = E₂=E₄, ξ-unconstrained; the round rigid-N=1 "4−2ξ" is carrier-specific), NOT the
  "no-seal⇒dissolves" fallacy. #75 flagged **CONDITIONS-CHANGED** in NEGATIVES_REGISTRY. Off-round object = FS
  (E₂,E₄); Q_H a topological (Vakulenko–Kapitansky) CONSTRAINT, not an N² coefficient.
- **N5b** (`H4_N5b_flux_budget_closure_results.md`, verifier a40dce45cfcede943): the whole-cell dilation-flux
  budget is Gauss's law + a CO-VARYING cosmic-seal charge (Q=MS mass; p_F=γ/2 continuous z_CMB-sourced) ⇒ NOT
  independent of N5a — it is criticality in Z_φ-charge language, Z_φ cancels, pins neither ξ nor Z_φ nor (ξ,Z_φ).
  The one native quantization (the D2b flux LADDER) is real but quantizes DEPTH/PROFILE not size/ξ (registry P-B);
  its hopfion-coupled form = the gated candidate D.
- **CHARLES DECISION:** candidates A(criticality)+B(flux)+C(onset)+E(z_CMB) all CLOSED at armchair; candidate D
  (the gated non-perturbative N5d φ+h_AB solve on the running ambient) is the ONLY surviving ξ-anchoring channel
  but is NOT currently necessary (we predict RATIOS; absolute scale is the known-hard, possibly-data-bound part).
  **ξ PARKED as an honest free family; N5d NOT opened; H4 compute STILL STOPPED.**

**2. Solar LIGHT-SECTOR arc — predictions derived + DATA CONFRONTATION done; UDT PASSES the leading solar tests.**
- **J(s) confrontation MAP** (`J_of_s_light_deflection_confrontation_MAP.md`, verifier a66e2da69bfc3c7d9): pre-reg
  contract for the frame-robust light-deflection confrontation. Load-bearing finding — TWO frame-robust light
  observables: (i) the ambient J(s) sector (only the pure NUMBER J(s) is impact-parameter-independent; the measured
  azimuth is D(ρ₀)·J(s), b-dependent + gauge-carrying, s=0 conical ⇒ whether it bounds s is OPEN, CF-ABS) and (ii)
  the one-body/solar sector ⇒ **Cassini bounds the ONE-BODY sector, NOT s** (CF-CAT). Corrected an inherited R2
  row-R2-1 overstatement (the ambient deflection is NOT b-independent). Found the one-body null deflection OWED.
- **One-body DEFLECTION** (`one_body_null_deflection_results.md` + `_cas.py`, verifier a2a421e68678e4687): derived
  natively from the R2 one-body metric (A=e^{−2ν·artanh(β/x)}ρ^{2s}, B=1/(a²A)). s=0 clean: **Δα = 4(m̂/b) +
  (9π/4)(m̂/b)²** — γ_UDT=1 leading (MATCHES GR, forced by form reciprocity ⇒ passes the leading test
  automatically); second order **9π/4 vs Schwarzschild 15π/4** (the exponential/"Yilmaz"-lapse O(1/b²) signature).
  Fully frame-robust. Leading mass coeff K₁(s) is s-DEPENDENT (refutes the MAP's no-s×q-mixing conjecture for null)
  but rides the conical anomaly for s≠0 (only s=0 clean). 9π/4 re-derived two independent ways by the verifier.
- **One-body SHAPIRO** (`one_body_shapiro_delay_results.md` + `shapiro_delay_cas.py`, verifier a758095ce3b865414):
  **c·Δt_oneway = 2m̂·ln(4ρ₁ρ₂/ρ₀²) + 2m̂** — γ_UDT=1 leading log (MATCHES GR); second order per leg **9π/4−2 vs
  15π/4−2** (convention-free departure −3π/2, same 9π/4 signature). Only PARTIALLY frame-robust: the measured
  proper-time delay carries a clock factor √A(ρ_obs) that rides the g-vs-ĝ fork (leading log frame-clean;
  normalization + 2nd-order + ambient frame-conditional). Radar class, not the deflection's pure class.
- **DATA CONFRONTATION** (`solar_light_sector_confrontation_results.md`, verifier adb471c72a1f5b552; the one
  authorized data step — Charles-gated): frozen predictions vs Cassini γ−1=(2.1±2.3)e−5 (Bertotti+ 2003, Shapiro)
  and VLBI γ−1≈(−0.8±1.2)e−4. **UDT PASSES: γ_UDT=1 at 0.91σ (Cassini) / 0.67σ (VLBI)** — a CONSISTENCY
  confirmation, NOT a discriminating test (γ=1 matches GR by construction). The 9π/4-vs-15π/4 second-order departure
  = **4.38 μas (deflection) / ~49 ps/leg (Shapiro)**, FAR below current reach ⇒ CANNOT be resolved now; a FUTURE
  ≲1-μas / tens-of-ps target. NO retuning; solar data does NOT bound s (CF-CAT). Verifier caught+dismissed a
  search-engine hallucination of the Cassini value.

**3. D1 CHARGE-CHANNEL MAP** (`d1_charge_channel_projection_MAP.md` + `_cas.py`, verifier a5cf5a27f637302df) —
tested Charles's hypothesis (q=1/3 = single-channel projection of Q_H=1 through the N=3 carrier; η=½q²). RESULT =
**partially confirmed STRUCTURE, refuted READOUT.** A native equal-thirds partition of the unit charge EXISTS and
is STRONGER than proposed — a TOPOLOGICAL INVARIANT of the whole degree-1 class (⟨n_a n_b⟩=δ/3 = per-axis winding
∫n_a²dΩ, value frame-invariant, NOT the End(H1) triplet) ⇒ Charles's structural intuition confirmed. BUT the native
charge readouts (degree, Hopf Q_H) = the scalar FULL sum = 1; reaching 1/3 needs a public COUPLING to one axis
(anisotropic V_ab, NOT native) ⇒ NO native projector. η: ½ native (ξ/2, seal U_seal=2−q²/(2Zρ_s²)) but η=½q² rides
Zρ_s²=1 (UNANCHORED). Q_H=1 stands; q=1/3 & η=1/18 not-natively-forced.

**4. NO-SELECTOR THEOREM** (`no_selector_audit_results.md` + `_cas.py`, verifier ac28a9c57dcfd18be) — Charles-
requested audit before hunting a selector. **OUTCOME B — no selector.** Under the native FS L2+L4 action
(manifestly target-SO(3)-invariant) + frame C(a), NO native object breaks the three equivalent target-S² channels
⇒ public charge = summed **Q=1**; q=1/3 UNFORCED. Premises: P1 target-SO(3)-invariant action; P2 isotropic
frame-C(a) couples only via the target-SCALAR stress (L2 AND L4 Skyrme stress both CAS-verified target-invariant);
P3 charge observables are target-SO(3) scalars (moment proof: vector moment=0, 2-tensor=(4π/3)δ ⇒ only the scalar
survives). Nearest miss = the self-induced shear (equivariance-locked to n_∞) — fails (target-scalar source, free
zero-mode, never enters the scalar observable = spontaneous orientation, not selection). Overturnable ONLY by a
natively-DERIVED target-indexed anisotropy (V_ab / target-charged background / single-axis projector) = outcome A
if derived, outcome C (NEW PHYSICS) if merely added — none exist. ⇒ **closing q=1/3 now requires new physics or
accepting Q=1.** (Verifier caught 2 CAS demonstration gaps — L4 Skyrme stress asserted-not-computed; T1 printed
nonzero — both FIXED + re-run clean; moment-observable strengthening folded in.)

**5. i-FLOW / ℏ-CLOCK MAP** (`i_flow_hbar_clock_MAP.md`, verifier a847ba3e0429d6c4a) — **OUTCOME 7: structural i
is NATIVE, ℏ is NOT derived.** Structural i = J_n(v)=n×v (J²=−1 on T_nS², ω Kähler-compatible) — CAS-exact, a
property of the target. The i-flow = the free orientation zero-mode / target-U(1) collective coordinate (SAME
object the no-selector audit found). Its native time-live action is a SECOND-ORDER rigid rotor ½Iθ̇² (I=∫(ξe^{2φ}
/c²)|∂_θn|²√g, positive, FREE ∝ξ) with **NO native first-order Berry/Wess-Zumino/symplectic term** — three
convergent lines: absent from L2+L4 (#49), rotor Berry connection=0 (#53), phase t→−t-odd (seal-projection NODE-1
open) + the only continuous θ-term ∫F∧F≡0 (ω∧ω=0 on S²) ⇒ no ℤ theta-angle. **The "area form ⟹ ℏ" shortcut is
REFUTED** (a symplectic FORM ≠ a symplectic SCALE; Q_H∈ℤ is a count). The flip point (G^t_r momentum constraint,
linear in ω) was hunted hard → a first-class constraint giving O(ω²) renormalization of I, NOT a symplectic term
(no Outcome 6). Quantizing the rotor still needs an EXTERNAL ℏ (postulate A). DERIVES (not merely parks) the F6 gap.

**THE THROUGH-LINE (for the next session):** this session drew a lot of honest boundaries. What UDT gives NATIVELY:
structural i, the equal-thirds topological partition, γ=1 light bending + Shapiro (with a distinctive 9π/4
second-order signature), the whole-cell mass response. What it does NOT yet force, each now a SHARP well-posed gap
(not a vague import): (a) **ξ's absolute scale** — only the gated non-perturbative N5d solve could pin it; (b)
**q=1/3's channel selection** — needs a natively-DERIVED target-indexed anisotropy (no-selector theorem), else
Q=1; (c) **ℏ's action scale** — the native time-live action is second-order (no symplectic scale); (d) **η's
normalization** — needs a Zρ_s² anchor.

**OPEN LEADS / NEXT-SESSION PICKUP (Charles's call — none started):**
- Whether a target-selector for q=1/3 can be natively DERIVED (vs added) — the no-selector theorem names exactly
  the three forms it must take; candidate native sources to probe: the seal involution structure, the time-live/
  spinning sector, a φ-angular coupling. If DERIVED ⇒ outcome A closes q=1/3; if only added ⇒ new physics.
- The gated non-perturbative N5d solve (φ+h_AB on the running ambient) — the ONLY route to pin ξ; ANTI-HANG
  binding (bound grid Nr≤16/24, ONE process, never background-poll); open only on Charles's go.
- The η Zρ_s² anchor (the other missing D1 link).
- q=1/3 & η=1/18 remain OWED targets (import-dependent; the channel route is now a proven-hard new-physics gap).
- The J(s)/light-sector data confrontation could be EXTENDED (the 9π/4 future-precision target; more γ tests) — but
  it's consistency-only at current precision.

---

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
