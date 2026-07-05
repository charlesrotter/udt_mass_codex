# LIVE — the only guaranteed-current file (READ ME FIRST)

**The "## ============ FRONTIER ... CURRENT STATE" block below is the ONLY current frontier** — read it and stop;
everything under the "↓↓↓ HISTORICAL ARC" / "SUPERSEDED" fences is labeled-stale detail (mine for history, not the
plan). `HANDOFF.md` / `STATE.md` are detailed history; **if they disagree with this file's CURRENT STATE block, the
CURRENT STATE block wins.**
**Read order (2026-07-05):** LIVE.md FRONTIER (this block — the RESUME-HERE directive at its TOP is the next
action) → **HANDOFF.md TOP (2026-07-05 (PM) session record — H3=A + the full H4 arc + RESUME HERE)** → the H4 arc
docs `H4_backreaction_mass_MAP.md`, `H4_N1_offround_transverse_equation_results.md`,
`H4_N2_farfield_reduction_results.md`, `H4_N4_backreaction_solve_preregistration.md`,
`H4_N4_backreaction_solve_results.md`, `H4_N4a_source_background_audit_results.md`, `H4_screening_taxonomy_MAP.md`,
`H4_GP_switch_hopfion_MAP.md`, `H4_N4rev_conditional_mass_response_results.md` (+ the H3 docs
`node_H3_hopfion_solve_results.md`, `H3_hopfion_solve_preregistration.md`) → CLAUDE.md "How we work" + the
discipline skills → INDEX.md (repo map).

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

## ============ CURRENT STATE (2026-07-05 EOD — H3=A + full H4 armchair+solve arc DONE; H4 compute STOPPED at revised-N4=D; NEXT SESSION = N5-reframed whole-cell-criticality/ξ-anchor MAP) ============

**➤➤ RESUME HERE / NEXT-SESSION FIRST ACTION (Charles, 2026-07-05): N5 REFRAMED = a WHOLE-CELL CRITICALITY /
ξ-ANCHOR MAP (armchair/MAP only — DO NOT run the fully-coupled non-perturbative solve until this MAP is banked AND
blind-verified).** Driven by the revised-N4 finding that the hopfion's gravitational mass is a **WHOLE-CELL
response, not a localized halo** (the transverse operator has no decaying mode ⇒ cell-filling shear; the
backreaction is non-perturbative ε≫1). **Question:** if the hopfion's gravitational mass is a whole-cell response
rather than a localized halo, what native WHOLE-CELL criticality condition anchors ξ, the hopfion scale, and the
emergence machinery? **Focus:** (1) cell-scale criticality, NOT particle siting depth; (2) E_ang(core)=2 /
criticality closure — is it still native?; (3) how the resolved hopfion acts as the SCALE-BREAKER; (4) whether the
whole-cell response SUPPLIES the mass anchor; (5) what a later non-perturbative solve must compute. Deliver as a
MAP (premise ledger + clean failures + verifier targets), then blind-verify before any coupled solve.
**H4 COMPUTE IS STOPPED** — the H3→H4 arc (below) is banked+pushed; the non-perturbative fully-coupled
(φ+h_AB, running ambient) solve is the eventual magnitude-certifier but is GATED behind the N5 MAP.


**One-paragraph current state:** the concentric ω≠0 embedded-cell frame was closed (P16 canon C-2026-07-05-1:
spin→φ not natively available); the reframe converged on the **HOPFION** — native L2+L4 IS the Faddeev–Skyrme
model, a UDT particle = a π₃ hopfion, charge = Hopf linking Q_H∈ℤ (D1 reinforced). Full armchair chain
(R0/Q1/H1/H2) blind-verified. **H3 RESOLVED (2026-07-05) = OUTCOME A, blind-verified (agent af9b56bc845e0eb97):**
the FIRST solve (Adam) unwound and was correctly caught as a false pass → D (verifier a2199a0aa1218ddc0); the
**production rerun** (topology-preserving arrested-Newton + Derrick scale accelerator + a coarse-to-fine
resolution ladder) **RESOLVES a stable, localized, virial-balanced Q_H=1 hopfion** — N=96 unwinds (lattice
pathology) but **N≥160 HOLDS + CONVERGES**: |Q| held 0.985→0.992 (→1 with h), E2/E4→~0.99–1.00, Ehat≈285–286
(box-independent L=5/6/7, grid-converged N=160/224/256), genuine off-axis torus (⟨ρ⟩=1.28, core ring ρ≈1.17).
The load-bearing rescaler-OFF control confirms the virial balance is a genuine stationary point (not manufactured).
Exactly the Vakulenko–Kapitansky prediction: continuum Q=1 ⟹ E≥c>0, so the coarse-grid collapse is a pure
resolution artifact — MISMATCH→SOLVER vindicated. **Three resolution-level caveats disclosed** (|Q|≈0.99
integer-consistent+trending, not certified-to-3-digits; E2/E4=1.000 is a rescaler snapshot vs ~0.99 true equil;
absolute-vs-published energy normalization not established).

**H4 ARC — DONE (armchair+solve chain, all blind-verified; compute STOPPED — see the RESUME-HERE block above).**
MAP banked + verifier-hardened (the "seal" disambiguated
to the reframe-consistent read-surface, NOT a private cell). **N1 ✓** (`H4_N1_...`) general off-round transverse
equation E^{AB}=−T^{AB}; the −2𝒦 φ-source survives off-round (CF5 doesn't trip); R^(2) exerts zero local stress.
**N2 ✓** (`H4_N2_...`) native far-field reduction: mass = a pure MONOPOLE in φ (δφ=−δq/r, 1/r native from ρ=r
area growth), multipoles in the h_AB SHEAR (no ℓ(ℓ+1) tower = a native GR-departure); geometric mass = Coulomb
charge up to Z_φ; **CF1 (does it have a mass) stays OPEN — provably FINITE-AMPLITUDE ⇒ an N4 solve output.**
**N3 ✓ RULED (Charles 2026-07-05):** frame **C(a) confirmed** (read-surface in bulk, NO private seal / boundary /
mini-cell unless forced); report both masses, Z_φ open, CF1 open. **N4 ✓ DONE = OUTCOME D (tool-limited)**, blind-verified (`H4_N4_backreaction_solve_results.md`; solver
a9073db162d6d6456, verifier af34ae7d0781fb7bd). SOLID: Phase-A reduction — the O(amp²) flux collapses to a LINEAR
response (only δh⁽¹⁾ needed; δh⁽²⁾ drops as a total derivative) ⇒ **δm = −δq = (e^{−2φ₀}/4πZ_φ)⟨T, L⁻¹T⟩**, L an
Euler-type operator (roots 1,2), sign-INDEFINITE; a genuine **native no-stress-only-shortcut** departure (φ-blind
⇒ mass is irreducibly the geometric response, can't read it off a GR-style stress constraint). SOLID source:
T^{AB} from the resolved field, compact-support (read-surface-independent), sectors **trace −90 / shear +139**
(opposite signs = the phase1_geon negative-mass prime-risk structure); geometric mass +286.5 is a DIFFERENT object,
does NOT settle the flux-mass. **CF1 LEANS δq≠0** (B/massless disfavored), **CF2 OPEN**, **CF3 = D**.
**★ N4a SOURCE/BACKGROUND AUDIT (2026-07-05, blind-verified `H4_N4a_...`) = FAIL → N4 RECLASSIFIED D-BUDGET →
D-SOURCE-FRAME.** The N4 response operator was the locally-flat approximation and DROPPED the ambient
self-screening term +8e^{−2φ_amb}δφ (the Branch-P source 4e^{−2φ} is φ-dependent). True exterior perturbation eq:
Z_φ(r²δφ')' + 8e^{−2φ_amb}δφ = 0, roots −½±√(Z_φ−32e^{−2φ_amb})/(2√Z_φ). ⇒ a clean 1/r monopole mass survives
ONLY on a **Branch-G / continuum** or **shallow** (e^{−2φ_amb}<Z_φ/32) far field; on a **deep Branch-P** ambient
(φ_amb ≲ 1.73) it is SCREENED / log-periodic r^{−1/2}cos(ω ln r) — **NO clean far-field mass.** **So whether the
hopfion has a clean mass reduces to the OPEN G/P switch criterion for its far field (≡ its unpinned depth) — a
FRAME question, not a compute-budget one.** This CONDITIONS-CHANGED banked N2 (its monopole was an unconditional
Branch-P claim; now conditional — N2 already half-saw this via "round+φ≡0 isn't a vacuum" but applied it only to
the shear). INTACT: the H3 source, ℓ=0/ℓ=2, frame C(a)/no-seal, and the Phase-A algebra (as a Branch-G/shallow
statement). **NEXT (revise N4 before any compute; Charles-gated): rebuild the monopole+shear operator on the true
φ_amb(r) WITH screening; determine the far-field character vs depth / the G/P assignment; report the mass
CONDITIONALLY. The bare-Euler BVP must NOT be run as-was (spurious clean monopole).** N5 ξ-anchor + q/η + i-flow/ℏ
+ J(s) still owed. Method win: a source/background AUDIT caught a frame error BEFORE compute, in a doubly-verified
banked result.

**★ SCREENING TAXONOMY MAP (2026-07-05, blind-verified `H4_screening_taxonomy_MAP.md`) — refines N4a + KILLS a
discreteness lead.** The N4a log-periodic far field is a FROZEN-W ARTIFACT: the true ambient runs
(φ_amb≈½ln((8/Z_φ)ln r)) ⇒ W=e^{−2φ_amb}→0 ⇒ the clean 1/r monopole is RECOVERED over all physical radii (exactly
in Branch-G/shallow); the oscillation never completes a cycle (bounded near-core skirt). ⇒ **"log-periodicity =
discreteness" is DEAD** (if native discreteness exists it's in the P-interior flux-ladder/closure machinery, D2b,
NOT a far-field DSI). N4a screening REFINED (log-periodic → at most marginal-logarithmic, physically-moot tail),
not overturned. **The taxonomy COLLAPSES from a 3-way far-field split to a 2-way INTERIOR distinction: active-P
interior (𝒦≠0 sources φ, emergence machinery ON) vs dead-G interior (source-free, holds geometric mass, conducts
flux, no emergence).** Far-field mass is NEARLY branch-blind ⇒ **the G/P switch governs the INTERIOR, not the mass
existence.** Pure-G flux-conduit native but "force" NOT established (no two-body interaction derived). Critical
depth φ_amb^crit=½ln(32/Z_φ) (≈1.73 at Z_φ=1). **G/P-SWITCH MAP for the hopfion (option 1) DONE (2026-07-05, blind-verified `H4_GP_switch_hopfion_MAP.md`).**
The H4 program CONVERGES: **mass (CF1), pinning (CF3), and the dead-G/active-P emergence switch are the SAME
question.** LOCALLY the hopfion core is active-P (derived: local 𝒦≠0 → −2𝒦 φ-source); GLOBALLY undecidable at
armchair, reduces to the revised-N4 solve. **switch ⇒ CF1 is ONE-WAY** (δq≠0 ⟹ active-P EXACT; isolated dead-G ⟹
δq=0; but a FLUX-NEUTRAL active-P is a live δq=0 outcome ⇒ the δq=0 branch needs an added INTERIOR φ'-flatness
check). Character = **threshold × non-cancellation** conjunction, **NOT topology-forced** (Q_H spectator; the
active-P lean via the toroidal turning-surface anchors is a FAIR LEAN, not a derivation — d2a dis-analogy +
O(amp²) cancellation keep it open). Both outcomes first-class (active-P emergence particle vs dead-G massive
flux-conductor; "conductor" ≠ "force").

**REVISED-N4 SOLVE DONE (2026-07-05, blind-verified `H4_N4rev_conditional_mass_response_results.md`) = OUTCOME D
(box-control) with a DERIVED cause + 2 robust physics findings.** L_bare (roots 1,2) has **NO decaying shear
mode** ⇒ the hopfion's geometric response is **CELL-FILLING, not a localized halo** ⇒ **its mass is a WHOLE-CELL
property, not a separable localized quantity** (no read-surface-independent δq(φ_amb) curve at finite frozen depth
⇒ the frozen-const sweep is D). ROBUST: **(1) interior ACTIVE-P everywhere — a genuine dead-G is NOT reachable**
(any apparent δq=0 is flux-neutral active-P; discharges the interior-φ' check); **(2) coupling-independent
POSITIVE-mass SIGN lean (δm>0) ⇒ NEGATIVE-mass prime risk DISFAVORED** (leading-order lean, not certified);
**(3) NON-PERTURBATIVE (ε≫1)** ⇒ perturbative machinery invalid for the MAGNITUDE. Caveats: Green's-fn numerics
bug (magnitude ~8× off, SIGN robust, magnitude non-banked); shallow/deep LABEL FIX (SHALLOW=screened/oscillatory,
DEEP=clean — N4a/taxonomy had it backwards; physics unchanged). **NEXT TOOL = a NON-PERTURBATIVE fully-coupled
(φ+h_AB) solve on the running ambient φ_amb(r)≈½ln((8/Z_φ)ln r)** (not a flat box / wall / perturbative L⁻¹).
**N5 IMPLICATION: "anchor φ_amb from the response curve" is UNDERCUT (no clean perturbative curve); N5 must drive
the non-perturbative solve OR reframe the anchor around whole-cell criticality E_ang(core)=2 (mass = a whole-cell
property).** q/η + i-flow/ℏ + J(s) still owed. Frontier detail in the two bullets below.

### ↓ (Both this session's chronological arcs are ARCHIVED out of LIVE to keep it lean — the CURRENT STATE block
### above is the only frontier. (a) The 2026-07-04→05 concentric-ω≠0-reframe → hopfion-route arc: HANDOFF.md
### §2026-07-05(AM) + `node_R0/_H1/_H2/_H3_*.md` + `native_hopfion_route_MAP.md`. (b) The H3=OUTCOME-A frontier
### bullets (superseded by the H4 arc): `archive/LIVE_hopfion_H3_arc_2026-07-05.md`. Canonical = the `node_*.md`
### / `H4_*.md` result docs. ↓

**STILL-OWED / PARKED THREADS (not the frontier, but not resolved — carry forward):** q=1/3, η=1/18 (native
re-derivation, NOT from Q_H); the i-flow/ℏ clock; **J(s) light-deflection** (frame-robust, un-gated NEW push — MAP
scope + confirm with Charles, loads Cassini bounds, pre-register s-dependence, data never-retune; "Anytime" ≠
self-authorized). **Pre-hopfion parked threads** (superseded AS FRONTIER by the hopfion arc but NOT resolved —
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
