# branch_operator.py — SCOPED CONTAMINATION LEDGER (ERA-WIDE re-grade)

> SUPERSEDED by / subsumed into the full `pre_native_era_census.md` (2026-07-06 date-based census); this ledger =
> the branch_operator-specific slice.

**Driver:** Claude (Opus 4.8, 1M). **Date:** 2026-07-06 (supersession sweep; rewritten from the
2026-07-06 first pass). **Mode:** armchair / code-and-provenance audit. **DATA-BLIND. NO solves.**
Classify-only (nothing deleted; in-file stamps + registry entries added).

> **ERA-LEVEL NOTE:** Pre-2026-07-01 coupled-solver native-micro results predate the native
> constrained-two-player operator and require premise scoping before use.

**CORRECTION to the first pass:** the earlier version of this ledger claimed the contamination was
"exactly ONE" banked native-microphysics result (#66) and that the code footprint was "~6 files." Both
are WRONG. The blast radius is ERA-WIDE — EVERY pre-2026-07-01 coupled-solve native-micro result rode a
pre-native frame (scalar-tensor `f=e^{2φ}`, X=−2e5; or EH-era `a=−1`, `G=8πT`). The one genuinely
DANGEROUS miss the first pass overlooked was **kap8** (a LIVE, unflagged, positive native-micro
identification) — now QUARANTINED (NEGATIVES_REGISTRY #77). The rest were already registry-tagged but
lacked in-file stamps (now added).

## The finding that triggered this audit
`branch_operator.py` implements the SUPERSEDED **scalar-tensor** frame — φ riding OUTSIDE the metric
as an independent player, weight `f = e^{+2φ}`, Branch-P potential `U = e^{2φ}−1`, the `e^{2φ}`-weighted
matter coupling `− kap8 f T^μ_ν` (the "basin-A runaway" the native derivation REJECTED), and the
Cassini kluge `X_PROD = −2e5` (branch_operator.py:90, tagged FREE). The CERTIFIED native operator
(constrained-two-player, derived 2026-07-01) is instead the **geometric-source, φ-BLIND-matter**
operator `∂_r(√h Z_φ φ') = −2√h·e^{−2φ}·𝒦̂[h]` (round shorthand `Z_φ(r²φ')' = 4e^{−2φ}`) — source
`e^{−2φ}` (OPPOSITE sign/exponent), no X kluge.

**Contamination test (fair):** a script/result is CONTAMINATED only if it used a PRE-NATIVE operator
(scalar-tensor OR EH-era) to MAKE or FEED a **native-microphysics** claim. MACRO / Branch-G / exterior
use, or honestly-premise-tagged pre-native use, is **premise-scoped, NOT silent contamination** — but
after 2026-07-01 it still needs an in-file SUPERSEDED stamp so it is not mis-cited as native-micro.

---

## 1. Code footprint (era-wide, NOT "~6 files")

The operator FAMILY that produced pre-native native-micro results spans the whole coupled-solver era:
`branch_operator.py` (scalar-tensor assembly) + its live importer `p1_residual_general_einstein.py` +
`migration_convergence_guard.py` (the kap8 driver) + `b1prime_3d_offround_residual.py` (the covariant
building blocks reused by the assembly) + `check_winding_survival.py` (kap8 saved-field sibling) + the
`prototype/branchGP_native_s2_coupled_OBSERVE.py` re-implementation of the same scalar-tensor frame (fed
#66) + the archived legacy prototype/one-off family (`legacy/root_oneoffs_2026-07-01/d1_radial_localize.py`,
`x_solution_space_explore.py`). Code-level importer detail (unchanged, accurate):

| # | File | Kind | Class |
|---|---|---|---|
| 1 | `p1_residual_general_einstein.py` | LIVE importer (`import branch_operator as BR`) | MICROPHYSICS solver (feeds kap8 + p1_offdiag) |
| 2 | `migration_convergence_guard.py` | kap8 CHARACTERIZER driver (→ p1_residual → branch_operator) | fed the QUARANTINED kap8 identification (#77) |
| 3 | `prototype/branchGP_native_s2_coupled_OBSERVE.py` | re-implements the SAME scalar-tensor frame (own `E_mixed_s2`) | fed banked negative #66 |
| 4 | `check_winding_survival.py` + kap8 saved-field siblings | recompute on saved kap8 fields | INHERIT the #77 quarantine |
| 5 | `legacy/root_oneoffs_2026-07-01/d1_radial_localize.py` | LEGACY/archived importer | prototype only — feeds no results doc |
| 6 | `legacy/root_oneoffs_2026-07-01/x_solution_space_explore.py` | LEGACY/archived indirect importer | prototype only — provenance trail only |
| 7 | `tests/test_branch_operator.py`, `test_solver_integrity.py`, `test_solution_space_gate.py` | infra guards | no physics claim (provenance/tagging guards) |
| — | `cell_solver_f2d.py` | docstring-only mention; does NOT import | native-frame REPLACEMENT (not a vector) |

---

## 2. Re-grade table — first pass, docs 1–16 (EXTENDED to 20 by the second pass; see §2b)

| # | Doc | Pre-native frame | Native-micro claim | Already registry-handled? | Action (2026-07-06) |
|---|---|---|---|---|---|
| 1 | `kap8_characterization_complete_solver_results.md` | scalar-tensor (X=−2e5) | YES — core-concentrated degree-1 S² winding defect; not-horizon | **NO — genuine miss (LIVE unflagged positive)** | **QUARANTINE banner + NEGATIVES_REGISTRY #77** |
| 2 | `check_winding_survival.py` (kap8 saved-field) | scalar-tensor | winding-survived readout | NO — inherits #1 | inherits #77 quarantine |
| 3 | `caveat3_offdiag_off_control` (kap8 saved-field) | scalar-tensor | off-diag control | NO — inherits #1 | inherits #77 quarantine |
| 4 | `ponder_horizon_signatures` (kap8 saved-field) | scalar-tensor | horizon signatures | NO — inherits #1 | inherits #77 quarantine |
| 5 | `native_object_characterization` (kap8 saved-field) | scalar-tensor | object characterization | NO — inherits #1 | inherits #77 quarantine |
| 6 | `branchP_solver_floor_xcontinuation_results.md` (#66) | scalar-tensor (X=−2e5) | NO interior localization (negative) | YES — #66 (frame-robust, sharpened by #76) | registry #66 CONDITIONS-CHANGED note → #76 |
| 7 | `static_soliton_rerun_derived_operator_results.md` | scalar-tensor (X=−2e5) | L=1 localization; B=1/A break; 1/r hair (→null) | YES — object-identity + banked-correction + 07-04 | in-file SUPERSEDED stamp |
| 8 | `STEP2_timelive_matter_results.md` | scalar-tensor (X=−2e5) | box-control / must-quantize | YES — object-identity + 07-04 | in-file SUPERSEDED stamp |
| 9 | `P5e_proper_results.md` | scalar-tensor (X=−2e5) | no intrinsic discreteness (coupled) | YES — object-identity + 07-04 | in-file SUPERSEDED stamp |
| 10 | `coupled_timelive_solve_results.md` | EH-era (a=−1, G=8πT) | catalog negative | YES — #65 (no blocking authority) + 07-04 | in-file SUPERSEDED stamp |
| 11 | `b1prime_round_gate_derived_operator_results.md` | scalar-tensor (X=−2e5) | Gate-A survivor legs; box-control | YES — object-identity + 07-04 | in-file SUPERSEDED stamp |
| 12 | `matter_regrade_derived_operator_results.md` | scalar-tensor (a(φ)=e^{+φ} weight) | matter-sector re-grade (armchair CAS) | YES — this sweep (armchair, no solver) | in-file SUPERSEDED stamp |
| 13 | `F1F3_closure_results.md` | scalar-tensor ("vacuum≠GR", free-X) | closure record (armchair) | YES — this sweep | in-file SUPERSEDED stamp |
| 14 | `P1P5_reaudit_vs_derived_operator_results.md` | scalar-tensor 'derived operator' (a=e^{+φ}) | auditor triage (UNVERIFIED, self-labeled NOT canon) | YES — this sweep | in-file SUPERSEDED stamp |
| 15 | `p1_offdiag_wiring_results.md` | EH-era (a=−1, G=kap8·T) + imported S³ | off-diag wiring (cat-A) + scoped shear-selectivity neg | YES — object-identity + subsumed everything-on arc | in-file SUPERSEDED stamp (LOW RISK) |
| 16 | `matter_object_identity_native_vs_import_results.md` | re-derivation/armchair (refs e^{2φ} weight) | covariance/topology (operator-independent, SURVIVE) | YES — object-identity + 07-04 per-sub-claim | in-file SUPERSEDED stamp (pointer only) |

**CLEAN (did NOT route through a pre-native operator; NO stamp needed):** `native_dilation_weight_derivation`,
`F0_SYSTEMATIC_AUDIT`, `p5_solver_survey`, `native_readout_map_depth_size_results.md`
(#76 — runs on the CORRECT native operator `Z_φ(r²φ')'=4e^{−2φ}`), the DERIVATION docs
(`udt_field_equations_derivation`, `udt_gravity_sector_rederivation`, `F2_closure`, `angular_lagrangian` — DERIVE/
OBSERVE-CAS, no solve), and the entire recent armchair/CAS arc (J(s) deflection/Shapiro, N5a/N5b, D1 charge-channel,
no-selector, i-flow/ℏ). **NOTE: `p2_matter_fullmetric` was struck from CLEAN by the second-pass sweep — see rows 17–20.**

## 2b. SECOND-PASS CORRECTION (2026-07-06) — the everything-on P-series (frame B), a SECOND undercount

The first pass (§2) undercounted AGAIN, by the same pattern that missed kap8: it keyed CLEAN-certification on the
**frame-A (scalar-tensor) import chain** (`grep branch_operator / p1_residual / branchGP → 0`). But the everything-on
**P-series (P2/P3/P4)** uses SELF-CONTAINED **frame-B (EH-era)** solvers (`p2_round_s2_solver.py`, `p3_*`,
`p4_time_live.py`; `a(φ)=−1`, `G=kap8·T`, `vacuum=GR`) that DON'T import `branch_operator` — so a frame-A grep sails
past them. P1 was flagged (row 15) but its P2/P3/P4 siblings were missed; p2 was affirmatively MIS-certified CLEAN.
Caught by the mandated second adversarial pass. Root-cause fix: completeness must enumerate **BOTH** frames
(frame-A scalar-tensor AND frame-B EH-era self-contained solvers), keyed on "ran a coupled solve + banked a
native-micro claim", not on an import fingerprint.

| # | Doc | Pre-native frame | Native-micro claim | Prior status | Action (2026-07-06 second pass) |
|---|---|---|---|---|---|
| 17 | `p3_aphi_coupling_results.md` | **frame B** (EH-era, vacuum=GR, a(φ) weight) | **YES — coupled round soliton exists + M_MS mass table** (studies the now-non-native a(φ)=e^{+φ} weight) | UNFLAGGED, absent from §2 | **CONDITIONS-CHANGED** in-file stamp (substantive) |
| 18 | `p3_aphi_FIX_results.md` | frame B (a(φ) running-weight fix) | running-a(φ) coefficient fix (a(φ) weight now non-native) | UNFLAGGED, absent | CONDITIONS-CHANGED stamp (sibling) |
| 19 | `p4_time_live_results.md` | frame B (a(φ)=−1 GR baseline) | time-live WIRING; ω=0 == the P3 frame-B soliton | UNFLAGGED, absent | CONDITIONS-CHANGED stamp (LOW RISK; soliton = P3's) |
| 20 | `p2_matter_fullmetric_results.md` | frame B (`resE=G−kap8·T`, a=−1 frozen) | off-diag wiring (cat-A) + linear off-diag-sourcing OBSERVE; **soliton anchor explicitly DEFERRED to P5 (not delivered)** | **MIS-CERTIFIED CLEAN by §2** | CONDITIONS-CHANGED stamp (LOW RISK); struck from CLEAN |

**RESIDUAL ZONE (owed, not yet swept — flagged for Charles):** the very-early **W-series** (w5/w8, 2026-06-11/12)
predates even frame A/B and ran its own early coupled/catalog solvers; `w8` self-labels "CONTINUUM; the lead
withdrawn". Also any **script-only** frame-A/B solve whose output lives only in `.py`/`.json` (no `_results.md`).
Neither is confirmed contaminated OR confirmed clean — a date-based enumeration (every coupled-solve result doc
2026-06-11→07-01) would close it. Not swept this pass; awaiting a scope decision.

---

## 3. Corrected blast-radius summary

- **ONE genuine QUARANTINE:** kap8 (+ 4 saved-field siblings) — a LIVE, positive, previously-UNFLAGGED
  native-micro identification that rode the scalar-tensor operator at X=−2e5. This is the miss the first
  pass overlooked. Now QUARANTINED (NEGATIVES_REGISTRY #77, banner on the doc). NO blocking authority as a
  native-micro result until re-run on the native operator.
- **SECOND-PASS ADDITIONS (§2b):** the everything-on **P2/P3/P4** arc (frame B, self-contained EH-era solvers)
  was missed by the first pass's frame-A grep — p3 banks a frame-B soliton+mass (substantive), p2/p4 low-risk,
  all now CONDITIONS-CHANGED-stamped; p2 struck from CLEAN. No new QUARANTINE (kap8 remains the only one). The
  undercount happened TWICE via the same fingerprint gap — root-cause fix recorded in §2b; residual W-era zone owed.
- **The rest were already registry-tagged** (object-identity 2026-06-21 / #65 / #66 / 2026-07-04 re-grade /
  this sweep) but lacked in-file stamps — 9 in-file SUPERSEDED stamps + the #66 CONDITIONS-CHANGED note added
  so none is mis-cited as native-micro.
- **The code footprint is ERA-WIDE, NOT "~6 files":** `branch_operator.py` + `migration_convergence_guard.py`
  + `p1_residual_general_einstein.py` + `check_winding_survival.py` + `b1prime_3d_offround_residual.py` + the
  `prototype/branchGP` re-implementation + the archived legacy prototype/one-off family. Every pre-2026-07-01
  coupled-solve native-micro result rode a pre-native frame.
- **The live forward risk** is feeding any of these pre-native operators into a NEW native-micro solve (e.g.
  N5d). The FRAME FENCE on `branch_operator.py` (corrected 2026-07-06) states this era-wide scope.

---

## 4. Actions taken / owed
- **DONE (2026-07-06 sweep):** kap8 QUARANTINE banner + NEGATIVES_REGISTRY #77; #66 CONDITIONS-CHANGED note
  (→ #76); 9 in-file SUPERSEDED stamps (docs 7–16 above); INDEX.md stale "current foundation" labels fixed
  (matter_regrade, F1F3_closure, P1P5_reaudit) + kap8 line flagged QUARANTINED; `branch_operator.py` FRAME
  FENCE contamination-scope line corrected (era-wide, not "exactly ONE"); this ledger rewritten. No code
  deleted; all provenance tags preserved.
- **OWED (gated, to the frontier driver):** re-run the kap8 object identification on the NATIVE operator
  before any native-micro use; the gated N5d off-round shear solve must use a native solver, NOT this module.
