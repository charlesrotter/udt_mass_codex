# HANDOFF — Resume (lean)

> **READ `LIVE.md` FIRST** — only guaranteed-current frontier + next action.
> If this file disagrees with LIVE.md, **LIVE.md wins.**
>
> **⚠ BRANCH: work is on `grok` (2026-07-10).** If not on it: `git checkout grok`. `main` is stale for this arc.

## CURRENT (2026-07-18 — H3 particle-mass arc complete; native-action final adjudication and selector audit complete; R0–R1G reorganization/provenance checkpoint complete)

**Read LIVE.md CURRENT STATE topmost layer first.** Session arc 07-13→16 in one paragraph:

**R1 REORGANIZATION CHECKPOINT COMPLETE:** R1E batch planning and R1F/B01 are integrated. Fixed
historical inventories, preregistrations, planning records, and verification records remain
immutable. Five active artifacts moved byte-identically: the R1D S8 note and the four R1F macro
SymPy verifiers; B01 was behaviorally verified before and after movement. Resolve current locations
through `research/_registry/CURRENT_ARTIFACT_PATHS.tsv` and migration provenance through
`research/_registry/MIGRATION_LEDGER.tsv`.

**R1G PROVENANCE AUDIT + READOUT CORRECTION COMPLETE:** the prefix-based pre-native classification
was false. The affected cascade set is 121 `NATIVE_2026-07-01`, zero `MIXED`; B02/B03 are 29
`NATIVE_2026-07-01`, two `MIXED`, one `OPEN`. Reference-only GR/Einstein/Misner–Sharp readouts do
not demote native operator provenance. `phi_source_derivation.py` and `homog_alpha_test.py` remain
`MIXED` because alpha enters the tested action/EOM. The old B02/B03 `archive/pre_2026-07-01/`
destinations are **WITHDRAWN**. For affected paths, R1G supersedes the corresponding fixed-snapshot
classifications in `research/_registry/ROOT_OWNERSHIP.tsv` and
`research/_registry/MIGRATION_READINESS.tsv` until a separately authorized correction is applied;
the registries remain unedited. B02/B03 are paused, and no registry correction, replacement batch
planning, B02/B03 or further migration is authorized.

**NATIVE-ACTION ADJUDICATION COMPLETE AND FROZEN (2026-07-18; `ded310a`):** the mechanical A/B/C
adjudication is under `native_action_final_adjudication_2026-07-18/`. Read
`FINAL_ADJUDICATION_REPORT.md` → `FINAL_STATUS_LEDGER.tsv` → `LAY_DECISION_TREE.md`. Final split:
reciprocal kinematics `DERIVED`; C²/Bach `UNIQUE-CONDITIONAL`; EH/S²/present mass formulas
`CONDITIONAL`; complete action/native source/differentiable finite-cell boundary action/normalized
charge `OPEN`. The shared-static-source route remains `OPEN`, not excluded. Frozen package manifest:
`57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33`.

**EXTERNAL VERIFIER + GR→UDT SELECTOR AUDIT COMPLETE:**
`native_action_external_verifier_2026-07-18/` pins SymPy `1.13.1` and mpmath `1.3.0`; its isolated
CPU-only run copied all 24 CAS scripts to `/tmp`, reproduced every output byte-for-byte, passed all
six internal manifests, and found identical complete package states before/after. Final-package
complete-state digest: `2b4a2c3d6a6881753822bf096e28f170a464d5a29666a4d1d4fb93af8814ba7e`.
`UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md` records: 4D `INHERITED`; fields/covariance/locality/
variation domain/derivative order `OPEN`; boundary completion `MODIFIED` by the finite cell while its
functional and charge remain open. The immediate missing fork is pre-scale equivalence-class versus
post-scale representative variation; it is not a complete-action selector. No carrier is adopted.
Stop before canonization, GPU work, further arms, or further repository migration.

The corrected-operator stability question was closed in TWO layers, both blind/independently verified:
(1) the T/R-DEFLATED physical spectrum certified positive at 128/192/256 (Charles's raw-backward-error
protocol: doublet η_c<1e-3 via invariant-subspace residual, isolated raw r_j<1e-3, ε-sweep, cross-seed
1e-9; refined values doublet 0.25088/isolated 0.32261 at 256³, h→0 ≈ +0.249/+0.322); (2) **full
U(1)^⊥ inertia positive** via the T/R Schur-complement seal (S=B−CᵀA⁻¹C exact, no mode discarded;
margins +2.0e-6/+3.3e-7/+4.1e-9; 256³ on the EXACT double-backward Hessian; fresh own-code verifier
PASS ×3, S-spectra match 9e-15). Translation-pair walls collapse with grid (0.0024→0.00004 phys) →
marginal in continuum = box-artifact walls (theorem-route candidate). THEN **G** (dispatch): conditional
mass readout on the corrected carrier — M_N⁽⁰⁾=2E4 (EH-conditional Gauss/lapse identity); continuum
2E4≈283.3–283.5 vs E_carrier≈275.9; **virial gap δ_vir→−2.7%** (vs 0.05% closure on the superseded
centered carrier). THEN **boundary-virial** (dispatch): identity E4−E2=B_∂Ω+W_res DERIVED+CAS'd;
exact scale response 2e-16; E2-rich pinned-wall skin found; **box scout monotone at both h** →
**BOX-STRESS LEAD** (gap = boundary dilation stress; local surface theorem OPEN; L→∞ OPEN).
Corrections en route (all committed): verifier's ±1.2e-3 bound RETRACTED (→±2e-2 within-span); one
false "NEGATIVE-CURVATURE WITNESS" headline was a control-flow bug (measured curvature +0.384 — a
solver event, not physics); FD noise floor → exact-HVP layer; CAS caught my EL sign error.

**F COMPLETE (2026-07-17, `UDT_H3_BOUNDARY_AUDIT_PATCH_THEN_F_DISPATCH.md`; commits 442c64e→2f024f8):**
Part-A evidence patch green (5 defects fixed, verifiers 62/62 + CAS 4/4, zero scalar change). F basin
characterization: exact 83-endpoint census (128³: 1 RETURNED BASIN + 58 OTHER STATIONARY BRANCH;
fine grids: 24/24 RETURNED BASIN), with zero topology changes, lower stationary states, or resolved
basin exits. The 128³ OTHER family is consistent with measured near-degenerate T/R box drift; only
the negative Rz offset is claimed to fade monotonically with refinement. **Single robust basin =
STRONG finite-slice LEAD**, not the literal class of all endpoints. Repaired verifier PASS 51/51
(independent own-energy symmetric FD; shared exact-HVP cross-check labeled); catch-proof RED and
byte-restored; endpoint NPZ hashes unchanged. Scope: basin behavior, NOT dynamics/infinite-volume/
mass. Records: `noNull_behavioral_F_results.md` + `noNull_F_*.json` + `F_evidence/`.

**Pending Charles:** audit of the F return; review the frozen native-action final adjudication and
GR→UDT selector audit; canonization calls; next-push direction. No native-action continuation,
carrier adoption, GPU launch, or further repository migration follows without a new dispatch.
**Key commits:** da51ec4→1c2196c (spectrum cert), d131557 (inertia seal), 493d104 (G), 837d633
(boundary-virial). **Records:** noNull_hess_h2fit_log.txt, noNull_schur_inertia_ALL.json,
noNull_phaseG_mass_results.md, noNull_boundary_virial_results.md, noNull_virial_identity_derivation.md.

## [ARCHIVED] 2026-07-12 layer → `HANDOFF_ARCHIVE.md` (superseded by CURRENT above)

## MACRO LANE (2026-07-09 — SEPARATE lane; particle lane above wins on conflict)

**Frame:** simple reciprocal metric only; free \(D_A\) quarantined (`grok/quarantine_free_DA/`).

**L form:** **canon C-2026-07-09-1 (WR-L)** + audit precision **C-2026-07-09-1a**
\[
A = 1 - r/X \qquad\Leftrightarrow\qquad r/X = 1 - A
\]
Residual re-centering + wall regularity. External triple-blind audit: **PASS**  
(`simple_metric_WR_L_external_triple_blind_audit_results.md`).

**Own consciously:** only **finite proper room** kills \(\alpha=2\). \(\alpha=1\) = **causal horizon** at finite proper distance (interior beyond \(r=X\)), not a hard edge of space.

**Records:**  
- `simple_metric_L_wall_regularity_closure_results.md` · `CANON.md` C-2026-07-09-1 / 1a  
- Foundation: `SIMPLE_METRIC_MACRO.md` · frame: `UDT_ELEGANT_FRAME.md`  
- Kaleidoscope / BAO / time-live: `simple_metric_kaleidoscope_*`, `simple_metric_bao_*`, `simple_metric_timelive_*`

**Retired / soft:**  
- **P_ell RETIRED** (SNe imposition detour).  
- MS mass-lock \(2GM/c^2\): **Principle-7** — do not present as native prediction.  
- n=2 optics: sound, **generic Etherington** (not UDT-unique).

**Center (2026-07-09):** **re-centering ⊥ center regularity** (if re-centering exact globally).  
Fork (A) global re-center → singularity forced · (B) wall-asymptotic → regular core possible.  
`simple_metric_WR_L_center_recenter_exclusion_results.md`.  

**EOS window (2026-07-09):** CHOSE \(p_t=w\rho\) scan → unique regular point \(w=-1\) (static dS, \(\Lambda=3/X^2\)). L is singular \(\beta=1\) member. Different family from WR-L.  
`simple_metric_EOS_power_window_dS_results.md`.  

**dS native closed any α.** Thread B ≠ dS.  
**Thread B static series:** drain SURVIVES (round / non-round / mirror-vs-wall).  
**Carrier posit:** `matter_carrier_provenance_audit_results.md`.  
**Time-live gates:** linear no-go + finite-amp LEAD — `threadB_timelive_linear_nogo_and_finite_amp_MAP.md`.  
**H4·N4rev:** CF2 box-controlled.  
**NEXT:** see LIVE.md.

**Red:** bare-metric L claim; revive P_ell; lean on MS mass as native; χ²-shop \(A(r)\); free \(D_A\) as theory; \(x_{\max}\) as hard spatial wall.


## Charles rulings (2026-07-09)

**Choice 1 = (A):** residual re-centering exact; \(r=0\) = \(\phi=0\) seat; singularity OK as macro/micro regime boundary. Not (B).

**Choice 2 (softened):** dS = **GR-form heuristic** only (\(w=-1\) uniqueness in Einstein+EOS+DEC box). \(A=1-r^2/X^2\) **native-forbidden** under φ-blind. Native dS closed any α. L residual stands.

**Record:** `simple_metric_Charles_rulings_center_dS_2026-07-09.md`

**NEXT:** see CURRENT block above + LIVE.md (Thread B CONDITIONAL; residual L appearance).

## Read order (every session)

1. `LIVE.md` FRONTIER  
2. `MEMORY.md` TOP (from disk)  
3. Method docs as needed · `CLAUDE.md` + skills  
4. `CANON.md` / `NEGATIVES_REGISTRY.md` when load-bearing  

## Archive

- Stale LIVE layers → `archive/LIVE_historical_frontier_through_2026-07-08.md`  
- Pre-lean INDEX → `archive/INDEX_pre_simple_metric_WR_L_2026-07-09.md`  
- Old HANDOFF sessions → `HANDOFF_ARCHIVE.md`

## Must-not-lose (short)

- DATA-BLIND wall numbers (contract 26fc757).  
- Full canon: **`CANON.md`**.  
- Method: MAP / OBSERVE / PONDER primary; DERIVE gated.
