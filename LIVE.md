# LIVE — the only guaranteed-current file (READ ME FIRST)

**⚠ BRANCH: work is on `grok` (2026-07-10).** If not on it: `git checkout grok`. `main` is stale for this arc.
**The CURRENT STATE block below is the only current frontier** — read it and stop.
Stale historical frontier layers live under `archive/LIVE_historical_frontier_through_2026-07-08.md`
(and older `archive/LIVE_*.md`). `HANDOFF.md` is lean; older session detail is in `HANDOFF_ARCHIVE.md`.
**If anything disagrees with this file's CURRENT STATE block, the CURRENT STATE block wins.**
**⚠ TWO LIVE LANES (2026-07-17):** the **PARTICLE-MASS lane** (H3 stability→mass→basin arc) is COMPLETE-and-WAITING —
read `LIVE.md` CURRENT STATE topmost (below; next action = WAIT on Charles's desk items) →
`noNull_behavioral_F_results.md` + `noNull_boundary_virial_results.md` + `noNull_phaseG_mass_results.md` →
**`stability_branch_follow_256_DECISION.md`** (detailed arc record) → MEMORY.md TOP. The **MACRO lane** (simple-metric / WR-L) is a separate ongoing lane; its read
order is: **`UDT_METHOD_MUSIC.md`** → **`UDT_DOTTED_LINE.md`** → **`UDT_ELEGANCE_UNCOVER.md`** → **`SIMPLE_METRIC_MACRO.md`**.
Free-\(D_A\) / mixed scoreboards = **`grok/quarantine_free_DA/`** only (not live).
Prior cell / Thread-A/B / macro-native pivots: **history** — see `archive/LIVE_historical_frontier_through_2026-07-08.md` and `archive/INDEX_pre_simple_metric_WR_L_2026-07-09.md`.

## Binding method (never skip)
- CLAUDE.md "How we work": MAP / OBSERVE / PONDER are primary, DERIVE is gated. Let structure
  EMERGE; pre-work discussion in LAY language; "chose or derived?" / "observing or targeting?".
- Discipline skills (`.claude/skills/`, auto-loaded): **solver-first**, **verifier-before-record**
  (incl. cross-model escalation), **no-shortcuts** (run `python3 -m pytest tests/` — **expect 1 FAILED** = the known hygiene-header doc backlog on 36 `simple_metric_*` result docs, NOT a code failure; ~69 passed / 1 xfailed otherwise), **completeness-map**.
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

## ============ CURRENT STATE (2026-07-18 — H3 PARTICLE-MASS arc COMPLETE THROUGH F: stability SETTLED (twice-verified) → G conditional mass readout → boundary-virial (BOX-STRESS LEAD) → audit patch → **F finite-slice characterization DONE (83 endpoints, no resolved basin exit; single robust basin = STRONG LEAD; verifier 51/51)**. Native-action Stage I A/B COMPLETE, mechanically checked, frozen, and returned; Charles's package audit pending. Stage II, Arm C, and GPU work NOT launched.) ============

**➤➤➤ NATIVE-ACTION STAGE-I RETURN (2026-07-18; `UDT_NATIVE_ACTION_STAGE1_RETURN_2026-07-18.md`):**
- **✅ TWO COLD ARMS COMPLETE AND FROZEN:** genuinely separate Bubblewrap namespaces and Codex
  sessions (`gpt-5.6-sol` and `gpt-5.4`) received only byte-identical C0/C1. Both returned complete
  D0–D5, CAS scripts + captured outputs, final responses, and raw outer transcripts. All 15 CAS
  scripts compile, exit zero, and reproduce captured output byte-for-byte. Per-file manifests pass;
  external manifest hashes are recorded in the return. Arm A's disclosed private-tmpfs self-check
  deviation is preserved and driver-classified noncontaminating, not hidden.
- **STOP / AUDIT BOUNDARY:** packages are read-only under `native_action_stage1_2026-07-18/`.
  No cross-arm physics comparison or conclusion was banked. Charles audits the two immutable packages
  next. Stage II, Arm C, independent physics adjudication, and GPU work remain NOT AUTHORIZED / NOT
  LAUNCHED.

**➤➤➤ TOPMOST LAYER (2026-07-16 — read this + the two result docs, then stop):**
- **G (conditional mass readout on the corrected carrier) COMPLETE** — `noNull_phaseG_mass_results.md`
  (verifier PASS 90/90; commit `493d104`). All gates crushed (r_P~1e-12 via direct DST-I 7-point solve;
  Gauss 4e-12). CONDITIONAL (EH lapse) unit response: **M_N⁽⁰⁾=2E4; continuum 2E4≈283.3–283.5 vs
  E_carrier=E2+E4≈275.9** — the **virial does NOT close at L=6: δ_vir→≈−2.7% continuum** (E2<E4;
  contrast: the superseded centered-carrier record had 0.05% closure). NO κ_g used; DATA-BLIND.
- **BOUNDARY-VIRIAL dispatch COMPLETE** — `noNull_boundary_virial_results.md` (verifier PASS 38/38 +
  CAS 4/4; commit `837d633`). V1 identity DERIVED+CAS'd: **E4−E2 = B_∂Ω + W_res ⇒ M_N⁽⁰⁾ = E_carrier
  + B_∂Ω + W_res** (for an exact critical point W_res=0; the saved carrier retains its reported
  residual work). V2 exact (2e-16). V3: the
  **E2-rich pinned-wall skin** found (E2 only ~86% inside a=2.5 vs E4 99.5%); surface closure
  converging ~h² empirically (33%→15.4%→8.5%; powers p=1.88, 2.07 — audit-patch corrected from ~O(h)), local theorem OPEN. **V4 box scout (pad+re-relax, fixed h): |δ_vir|
  falls MONOTONE at BOTH resolutions** — h_c: 0.0521→0.0439→0.0379 (L=6→7.5→9); h_f: 0.0363→0.0256
  (L=6→7.5; the 0.0363 anchor = the N=192 raw δ_vir in `noNull_phaseG_mass_ALL.json`, the 0.0256 in
  `noNull_boxscout_observables.json`). All criticality gates met, topology held. **VERDICT: BOX-STRESS LEAD; local surface
  theorem OPEN; infinite-volume closure OPEN — audit patch (442c64e): literal 1/L intercepts are
  unstable/nonphysical (fine 2-pt gap −4.76); NO intercept identifiable from this scout.** CAS note: the
  first CAS pass CAUGHT a sign error in the hand-written EL (production unaffected — audited
  grad_noNull everywhere); corrected + re-verified.
- **✅ AUDIT-PATCH + F DONE (2026-07-16→17, `UDT_H3_BOUNDARY_AUDIT_PATCH_THEN_F_DISPATCH.md`;
  commits 442c64e→2f024f8):** Part-A evidence patch green (5 record defects fixed; verifiers 62/62 +
  CAS 4/4; zero scalar change). **F finite-slice characterization COMPLETE**
  (`noNull_behavioral_F_results.md`, repaired verifier PASS 51/51 + catch-proof): exact 83 endpoints
  (128³: 1 RETURNED BASIN + 58 OTHER STATIONARY BRANCH; 192/256: 24/24 RETURNED BASIN) — **zero
  topology changes, lower stationary states, or resolved basin exits**. The 128³ OTHER family is
  consistent with the measured near-degenerate T/R box drift; the negative Rz offset narrows with
  grid (−2.22e-3→−4.12e-4→−1.62e-4), while the full control set is nonuniform. **Single robust basin
  = STRONG LEAD within the preregistered finite-grid slice**, not a literal class for all endpoints.
  Endpoint hashes unchanged. Scope: relaxation/basin behavior in the L=6 frame — NOT dynamics,
  NOT infinite-volume, NOT a mass statement.
- **⏳ ON CHARLES'S DESK:** (1) audit of the F return (+ the G / boundary-virial / audit-patch chain);
  (2) **audit both frozen native-action Stage-I packages** (`UDT_NATIVE_ACTION_STAGE1_RETURN_2026-07-18.md`;
  no Stage II / Arm C / GPU launch until separately authorized); (3) any canonization (stability
  seal; basin characterization); (4) direction for the next push (candidates: boundary-layer theorem
  route / native-action Stage II after package audit / box-mask study / spin-isorotation on the certified carrier).
- **Ops for a fresh session:** launch pattern = `setsid bash -c '… timeout … python3 …' & disown`
  (plain `&` dies with the tool shell); ONE GPU process; **exact Hessian tools** `hvp_exact`/
  `hvp_exact_chunked` in `noNull_energy.py` (machine-precision; FD-HVP noise floor ~1e-10 rel blocks
  deep certification); hess outputs N-tagged; `.gitignore` has `*.log` — **git add -f** for evidence
  logs; scout fields `noNull_boxscout_N{160,192,240}.npz`; evidence dirs `phaseG_evidence_2026-07-16/`
  + `boundary_virial_evidence_2026-07-16/`; artifact_manifest.json = SHA-256 of every npz.

**[prior layer of the same arc — stability certification, 2026-07-14→16, still-true record:]**

**➤➤➤ [prior layer] (2026-07-14 — STABILITY CERTIFICATION COMPLETE; records = `noNull_hess_h2fit_log.txt` +
`noNull_hess_refine_{256,192}_log.txt`; commits `da51ec4..1c2196c`):**
- **All numerical gates MET at 128/192/256, both seeds** (Charles-directed raw-backward-error protocol
  2026-07-13): refined physical spectrum POSITIVE — doublet 0.25293/0.25175/0.25088, isolated
  0.32086/0.32254/0.32261 (h→0: doublet ~+0.2494–0.2498, isolated ~+0.3223–0.3227). Gates: doublet
  invariant-subspace η_c<1e-3, isolated raw r_j<1e-3, HVP-ε sweep stable, cross-seed 1e-9. Tools:
  `noNull_hess_residual_diag.py` (proved production Ritz vectors were genuinely unconverged — backward
  error, NOT near-degenerate mixing, NOT FD noise) + `noNull_hess_refine.py` (block ortho-LOBPCG +
  soft-locking in U(1)+T/R complement; plain block-4 stalls ~0.05 — use the guard+lock version).
- **BLIND ADVERSARIAL VERIFIER PASS (zero-context, own code, adjudicate framing):** criticality
  quantified; eigenvalues reproduced to 2e-9; **independent negative-mode hunt (128³) finds NOTHING
  below our floor** (reproduces doublet+isolated at overlap 0.999–1.0; full-space Ritz values all
  POSITIVE). AMENDMENTS (scoped, quantified): doublet convergence is T/R-DEFLATION-scoped (raw backward
  error 3.4e-2 lies wholly in the T/R quasi-symmetry span); cross-seed identity = fixed-point check,
  not independent evidence; h² NOT pure (h⁴ significant at 128³; ~1e-3 systematic on extrapolants).
- **⚠ CORRECTIONS (2026-07-14 evidence seal + dispatch):** (1) the verifier's "raw-operator doublet
  = 0.2509±1.2e-3" is **RETRACTED** — its gap used converged pseudomode eigenvalues; the exact
  within-span algebra (raw Rayleigh block of the Q_TR generators runs 0.03–35, near-resonant 0.245
  element at 256³) gives ±~2e-2 within the probed span (`verifier_evidence_2026-07-14/
  perturbation_bound_algebra_note.md`). (2) The N=128 full-space hunt produced positive Ritz values
  but did **NOT raw-converge** (T/R-cluster residuals ~0.99) — it was a variational floor probe, NOT
  an eigenpair certification. **⇒ CERTIFIED: the T/R-DEFLATED physical spectrum is positive**
  (doublet+isolated, raw-backward-error gates, 3 grids, ε-sweep, blind-verified).
- **✅ FULL U(1)^⊥ INERTIA SETTLED POSITIVE (2026-07-14→16, Schur-complement seal per dispatch):**
  S = B − CᵀA⁻¹C computed at 128/192/256 with error-controlled margins — **all six S eigenvalues
  positive at every grid** (margins +2.0e-6 / +3.3e-7 / +4.1e-9 raw; the 256³ certification on the
  EXACT double-backward Hessian `hvp_exact`/`_chunked`, η_Z=3.5e-11, bound 400× under λ_min(S)).
  By Sylvester inertia (A≻0 certified + S≻0) the complete U(1)^⊥ Hessian is positive — **no T/R
  mode discarded**. **Fresh independent verifier (own code, exact operator): PASS at all 3 grids**
  (S-spectra match to 9e-15). Records: `noNull_schur_inertia_ALL.json` (+ per-grid),
  `noNull_schur_verify.json`, raw logs `scratchpad/schur_inertia_*.log` (incl. the honest failure
  records: FD-noise-floor wall, two solver-divergence episodes, one mislabeled-abort bug — each
  diagnosed+fixed; the physics answer never moved). **FINDING (ponder):** the translation-pair S
  eigenvalues collapse with grid (0.0024→0.0020→0.00004 phys) → marginal (flat) in the continuum
  limit — box-artifact walls, physically expected (sliding costs nothing in infinite space); prime
  candidate for the analytic boundary-layer theorem (numerics→algebraics transition). Rotations +
  the remaining T/R combinations stay finite-positive. **STATIC STABILITY OF THE Q=1 CARRIER: the
  strongest statement this frame can make is now made, scoped as stamped (this carrier, L=6.0 box,
  HBW=2, EH-action CONDITIONAL, carrier=posit). Charles's physics verdict/canonization PENDING.
  F/G NOT started (per dispatch). Native-action dispatch DRAFT awaiting Charles §0/§1 review.**
- **SCOPE STAMPS (travel with the verdict):** static; THIS Q≈1 lower-E carrier; box L=6.0 (FREE);
  mask HBW=2 (FREE; wider-mask boundary sweep NOT done); EH/metric-only action = CONDITIONAL-DERIVED;
  S² carrier = posit (bedrock memory). Hess outputs now N-tagged (anti-clobber; converged vectors =
  `noNull_hess_refine_s{0,1,192_*,128_*}.npz`).
- **STATUS: `Stability SETTLED (2 verified layers) · conditional mass M_N⁽⁰⁾=2E4 read out
  (continuum ≈283.4; virial gap −2.7% = boundary stress, BOX-STRESS LEAD) · finite-slice basin
  characterized (no resolved exit; single robust basin = STRONG LEAD; verifier 51/51). All corrected-carrier work dispatched to date is COMPLETE,
  scoped, and verified; physics verdicts / canonization / next direction = Charles.`**

**➤➤➤ DETAILED ARC RECORD = `stability_branch_follow_256_DECISION.md` (full arc, retractions, fork). The superseded 2026-07-11/12 layers are archived in `archive/LIVE_h3_stability_layers_2026-07-11_12.md`.**

**Macro lane (SEPARATE, still valid — NOT the uniquely-live frontier):** `UDT_ELEGANT_FRAME.md` / `SIMPLE_METRIC_MACRO.md` (WR-L
`A=1−r/X`, C-2026-07-09-1). The 2026-07-09 "stick to simple metric" directive governs the MACRO sector; the particle-mass sector above
runs in its own (Charles-authorized) frame. Both are live; neither is uniquely so.

**Binding frame (macro):** `UDT_ELEGANT_FRAME.md`.  
**LIVE macro foundation:** **`SIMPLE_METRIC_MACRO.md`** + CAS `simple_metric_FE_rederive.py`.  
**MAP:** `macro_sector_MAP.md`.

**Metric (only):**
\[
ds^2=-e^{-2\phi(r)}c^2 dt^2+e^{2\phi(r)}dr^2+r^2 d\Omega^2
\]
Field = **\(\phi(r)\)** only. Free \(D_A\) work → **`grok/quarantine_free_DA/`** (includes old explore tiles + mixed P0–P3 scoreboards). Those are **not** theory verdicts against the simple metric.

**φ-only FE (vacuum), derived on this metric:**
- \(W=e^{2\phi}\): \((r^2\phi')'=0\) → Coulomb \(\phi=\phi_\infty-q/r\)
- \(W=1\): \(Z(r^2\phi')'=4e^{-2\phi}\)
- \(Z\) free until observation; \(W\) still a fork

**Scar corrected:** general free-\(D_A\) FE then freeze-to-\(r\) is **invalid provenance** for convicting the simple theory.

**\(c\)-analogy MAP:** `simple_metric_c_analogy_MAP.md` + operator inventory `simple_metric_operator_inventory.md`.  
Charles: edge should be **like approach to \(c\)** (asymptotic, effect diverges, unattainable). Present geometric EL on simple metric give **finite \(\phi_\infty\) + open \(r\)** — **fail that test**. Root cause: bulk sources \(\propto e^{-2\phi}\) are **self-quenching** as dilation deepens (opposite of \(\gamma\to\infty\) as \(v\to c\)).

**Asymptotics (scoped, still valid as “what those EL do”):** vacuum + dilated dust → Coulomb/plateau, not \(c\)-edge.  
**Implication:** operators/FE cut suspect under \(c\)-test; simple **metric** still live; free \(D_A\) still quarantined; **no hand \(x_{\max}\)**.

**Both forks tried** (Charles: try both) — `simple_metric_F1_F2_dual_explore.md`:  
- **F1** (R1 on bulk): `simple_metric_F1_complete.md` — unique vacuum Coulomb; \(c\)-like **law** \(\gamma_{\mathrm{pos}}=e^{\Delta\phi}\); **no** bulk \(c\)-wall.  
- **F2** (R1 on metric only): `simple_metric_F2_completeness.md` — known geometric bulk is Coulomb or **self-quenching**; **no** derived non-SQ density in the stated class; bulk \(c\)-edge **not found**.  
**Agreement:** simple metric OK; present operators not a bulk \(c\)-edge; no hand \(x_{\max}\); no free \(D_A\).

**Repo inspiration search:** `simple_metric_operator_inspiration_SEARCH.md` — near-misses for \(c\)-like edge:  
(1) **xmax boost** \(\phi=\mathrm{arctanh}(x/X)\), \(A=(X-x)/(X+x)\to0\) (best *form*; \(X\) often postulated);  
(2) **unweighted vacuum** \(e^{-\phi}=C_0+C_1/r\) (finite-\(r\) lapse zero; R1-flawed);  
(3) **Branch-P** \(U=e^{2\phi}-1\) (**non-SQ** +2 weight; ST/packaging scar);  
(4) MS \(f\to0\) / HE1 questions. SQ \(\mathcal{K}\)/dilated dust = far misses.

**Near-miss explore (repo+git):** `simple_metric_near_miss_explore_results.md`.  
- **Unweighted vacuum** \(\Box\phi+e^{-2\phi}(\phi')^2=0\Rightarrow e^{-\phi}=C_0+C_1/r\): **passes** \(c\)-like tests (φ→∞ at finite \(r_*\), \(\ell\) diverges, \(A\to0\)); flawed vs R1 kinetic weight (`f766478`).  
- **xmax boost** (`867ead9`): best kinematic \(c\)-form; **different** profile than unweighted; \(A=(X-x)/(X+x)\).  
- R1-weighted + SQ geometric: fail \(c\)-edge (history moved toward these).  

**Kinetic ledger:** `simple_metric_kinetic_ledger.md` — **K-R1** \((r^2\phi')'=0\) (shift-clean, no \(c\)-wall) vs **K-UW** \(\Box\phi+e^{-2\phi}(\phi')^2=0\Rightarrow e^{-\phi}=C_0+C_1/r\) (horizon at \(r_*=-C_1/C_0\), \(\phi\to\infty\), \(\ell\) diverges — **\(c\)-like**). Not the same as xmax \(A=(X-x)/(X+x)\). Fork = bulk shift purity vs horizon vacuum.

**Third path derived:** `simple_metric_third_path_derive.md`.  
Harmonic triangle on simple metric: \(\Delta\phi=0\) (K-R1), \(\Delta e^{-\phi}=0\) (K-UW), \(\Delta e^{-2\phi}=0\) (K-A \(\Leftrightarrow G_{\theta\theta}=0\), CAS exact).  
K-A ⇒ \(e^{-2\phi}=C_0+C_1/r\) (Schwarzschild-like branch) — **\(c\)-horizon** at finite \(r_s\).  
**Working lean:** K-A for \(c\)-like vacuum; K-R1 shift-pure; K-UW clock-harmonic. Not free \(D_A\); \(G_{\theta\theta}=0\) tagged geometric condition (not EH bulk scar).

**K-A developed:** `simple_metric_KA_develop.md`.  
Schw branch \(A=1-r_s/r\) = standard Schwarzschild areal metric; \(\phi\to\infty\) at finite \(r_s\); static \(z\to\infty\); proper distance to horizon **finite** (unlike K-UW); outer infinity flat. \(c\)-like **horizon**, not outer cosmic wall. Exotic \(C_0<0\) outer zero of \(A\) flagged OPEN.

**K-A outer + matter:** `simple_metric_KA_outer_and_matter.md`.  
- Exotic \(C_0<0\) outer \(A=0\): **not vacuum** (\(G^t_t\neq 0\)); drop as empty-space edge.  
- Full vacuum from \(G^t_t=0\): only \(A=1-r_s/r\) (Schw).  
- MS: \(m=c^2 r(1-A)/(2G)\); matter ⇒ \(m'=4\pi r^2\rho\); **outer** \(c\)-edge ⇔ compactness \(2Gm/c^2r\to 1\) at finite \(r\) (critical-universe style).  
- Old SQ dilated-dust kinetic path ≠ this Einstein/MS continuum.

**\(x_{\max}\) POSTULATE ACCEPTED (Charles, working):** `simple_metric_xmax_POSTULATE.md`.  
Form cascade held: `simple_metric_hyperbolic_derive.md` — \(x=x_{\max}\tanh\phi\), \(1+z=\sqrt{(X+x)/(X-x)}\), \(A=(X-x)/(X+x)\).  
Consilience checklist C0–C8 in the postulate doc; **continue cascade** (relational, \(X\sim k GM/c^2\), closure, n=2 optics check). If consilience stalls, revisit — no mechanism patches.

**Mass–\(x_{\max}\) cascade (C3–C4):** `simple_metric_mass_xmax_cascade.md`.  
Under join **J1**: MS packaging yields \(M\leftrightarrow X\) with \(k=2\). **⚠ PRINCIPLE-7 (audit 2026-07-09):** do **not** present \(2GM/c^2\) as native UDT prediction (`simple_metric_mass_xmax_cascade.md`). J1 CHOSE.

**J1 + C2 + C5:** `simple_metric_cascade_C2_C5_J1.md`.  
- **J1** (\(r\equiv x\)): default under simple metric (else free areal vs distance).  
- **C2** relational: structural pass (bound = distance ahead of each observer).  
- **C5** n=2 form: \(d_L=X(1+z)^2\frac{(1+z)^2-1}{(1+z)^2+1}\); low-\(z\): \(d_L/X=z+\frac32 z^2+\cdots\).

**Pantheon one-fit (2026-07-08):** `simple_metric_pantheon_xmax_fit_results.md`  
Data: `Data/Pantheon+SH0ES.dat` + `Data/Pantheon+SH0ES_STAT+SYS.cov` (full cov script).  
Pre-registered: free = scale offset only (absolute \(X\) needs conventional \(M_B\)); no shape knobs.  
- **Shape: FAIL** (full cov): hyp χ²/dof ≈ **2.17** vs LCDM-ref ≈ **0.88**; Δχ²≈+2031; RMS 0.31 vs 0.15; high-\(z\) systematic over-distance.  
- **Scale pin only:** \(X\approx 3600\,\mathrm{Mpc}\) at \(M_B=-19.25\) (convention) — **Pantheon-calibrated**, not pure prediction.  
- **Mass lock** \(M=c^2X/(2G)\sim 4\times10^{22}M_\odot\) = rename of that scale under J1, **not** independent consilience.  
No mechanism patches. Cascade **stalls on C5 numeric**.

**SNe validator reconstruct (2026-07-09):** `simple_metric_sne_validator_reconstruct_MAP.md`  
Old stack: cubic + n=1 still **χ²/dof≈0.94** full cov; naive n=2 same \(r\) → 4.56. Partial components only — not a complete model.

**Native \(D_A\) (2026-07-09):** `simple_metric_DA_native_derive.md`  
Chart-origin observer on simple metric: **geometric \(D_A=r\) forced** ⇒ \(d_L=r(1+z)^2\).  
Old \(r(1+z)\) = correct **\(D_M\)**, mislabeled as \(d_L\) (missing one \(\sqrt{g_{rr}}\)).  
Counterfactual \(D_A=r/(1+z)\) is **not** native geometry. Cubic under true \(d_L\) still fails — profile/join still open.

**Upstream ranking:** `simple_metric_root_upstream_MAP.md`  
Root A (old \(D_M\) as \(d_L\)) **diagnosed**. Root B most likely **#1 profile/source**, then **#2 J1**.

**Sourced profile observe (2026-07-09):** `simple_metric_sourced_profile_observe_results.md`  
Compensated + dilated dust on simple metric, true n=2: can reach high \(z\), but **best SNe demo χ²/dof~10**.  
**Structural:** regular origin ⇒ \(\phi\sim ar^2\) ⇒ \(d_L\sim\sqrt{z}\) at low \(z\) — **wrong linear Hubble**; ρ scans cannot fix.  
Old cubic’s \(\phi\sim kr\) bought linear \(z\) via irregular origin. Hyp low-\(z\) OK; high-\(z\) still fails.

**Cross-sector root check (2026-07-09):** `simple_metric_cross_sector_root_check.md`  
Wrong \(d_L=r(1+z)\) was **SNe-load-bearing only**; BAO used \(D_M=r\) (partner labeling, not same bug symbol); CMB mostly not \(d_L\) (scaffolding weak). Clue real; BAO not “clean theory.”

**Free \(D_A\) unquarantined for hunt (Charles 2026-07-09):** `simple_metric_freeDA_unquarantine_HUNT.md`  
Low-\(z\) observe: `simple_metric_freeDA_lowz_observe_results.md`  
- Free \(D_A\) **does not** fix low-\(z\): when redshift runs, \(d_L\propto z^{p}\) with **\(p\sim 1/2\)** (same √).  
- Dilated Path B + quiet center: \(\phi\equiv 0\) invariant (no redshift bootstrap).  
Free \(D_A\) still allowed **in this hunt** for other questions; it is **not** the low-\(z\) fix.

**Lorentz light clue (2026-07-09):** `lorentz_light_clue_results.md` + `verify_lorentz_light_clue.py` (PASS)  
Root = **half** energy×rate; full rule \(d_L=(1+z)^2 D_A\). Not a SNe trophy.

**Distance profile dimensional MAP (2026-07-09):** `simple_metric_distance_profile_dimensional_MAP.md`  
Layer A light count closed; **Layer B profile** = hunt.

**PATH–AREAL / P_ell:** **RETIRED** (external audit V2 — imposition). Do not re-read 2.17→1.02 as a win.  
Record (banner only): `simple_metric_path_areal_split_results.md`.

**P_ell mass lock:** **RETIRED** — `simple_metric_Pell_mass_lock_derive.md` (banner).  
Motivation: static rods measure \(d\ell=e^{\phi}dr\) ⇒ composition chart on **proper** path (motivated, not unique theorem).  
Historical P_ell-only formula (RETIRED with P_ell): \(r_{\max}=2GM/c^2\) etc. — **Principle-7**, not live.  
Compactness \(2Gm/(c^2r)=2x/(X+x)\) unchanged in \(x\).

**Success criterion (Charles 2026-07-09):** Do **not** require beating ΛCDM on every observable/χ². Goal = **one theory resolving multiple ΛCDM tensions** (goal, not yet demonstrated). Continue **refining hyperbolic**, not trophy-chasing.

**Structure hygiene (process, not physics):** `STRUCTURE_HYGIENE.md` — layered L1 machine / L2 artifact headers / L3 periodic audit / L4 Charles+blind; build-on grades DEMO|LEAD|CONDITIONAL|BANKED-FOR-STRUCTURE.

**Self-audit (2026-07-09):** `simple_metric_session_self_audit_2026-07-09.md`  
P_ell = **RETIRED**. LCDM residual reference only. MS mass = **Principle-7** (do not lean). Full light n=2 = sound, **generic Etherington**.

**Hyperbolic stack (refine target — premise-tagged):**
- PATH: \(x=X\tanh\phi\), \(1+z=e^{\phi}\), bound \(X\) — **POSTULATE** + derived form
- Full light: \(d_L=(1+z)^2 D_A\) — **DERIVED** (static SSS scope)
- **P_ell** \(x=\ell\): **RETIRED** (2026-07-09 audit) — not live
- Mass under P_ell: **RETIRED** with P_ell; any MS \(2GM/c^2\) face remains **Principle-7**
- J1 demoted as **scoped residual**, not “metric forbids J1”

**R1 path ops (2026-07-09):** `simple_metric_R1_path_proper_results.md`  
Path=proper **not forced** by metric. Ops lengths characterized.

**J1 WORKING POSTURE (Charles 2026-07-09):** \(x_{\max}\) **literally defines sphere size** — long-standing intuition (~decades).  
Tag: simple metric + **WR-L** working stack.  
Mass packaging \(X=2GM/c^2\): **Principle-7** — do not lean. n=2: sound, generic Etherington.  
P_ell = **RETIRED**.

**Zoom-out:** `simple_metric_macro_elegance_ZOOM.md` — uncover metric, no mechanisms.

**Solution-space S1–S9 + zoom-out:**  
- **E-map / A-map** as before; critical \(M\) closes spheres not packages; S3 dust dead.  
- **Zoom:** `simple_metric_solution_space_ZOOM.md`.  
- **S9 native action honesty:** `simple_metric_S9_native_action_honesty_results.md`  
  - Forced: metric, measure; shift-clean R1 kinetic = **candidate**.  
  - Forks: angular \(W\), \(Z\), \(L_m\).  
  - **EH reduced + vary only φ ⇒ EL ≡ 0** — E-primary is **Einstein-on-ansatz**, not a φ-EL theory.  
  - A-primary = true R1 φ-variational. Different **problem types**.  
  - **Native package still OPEN** (Charles / deeper principle).  

**GR corpus mine:** method `simple_metric_GR_corpus_mine_MAP.md`.  
**Pass 1:** SSS Einstein — \(p_r=-\rho\); E-vacuum≠Coulomb.  
**Pass 2:** EH+constraint — substitute≠constrain; stuffed-φ EH empty.  
**Pass 3 junction:** `simple_metric_mine_junction_results.md`  
- \(A\) cont ⇔ MS mass cont.  
- Ceiling family \(A=1-cr^p\) **cannot \(C^1\)-match** exterior Schw (\(A'\) sign).  
- Thin shell: \(\sigma=0\), anisotropic \(S^\theta{}_\theta\); diverges at wall — **not** adopted as edge mechanism.  
- **Two rooms:** star+exterior vs filled cosmos/critical wall.  

**Nature lean frame (working):** `UDT_NATURE_LEAN_FRAME.md`  
- UDT → relational place, reach (kin to \(c\)), reciprocity, filled critical closure.  
- E-room continuum **working**; R1 = probe; no χ² muse; two rooms (filled cosmos vs local mass).  
**Skeleton deepen:** `simple_metric_skeleton_reach_closure_results.md`  
- J1 hyperbolic reach **is** critical fill \(M=X/2\).  
- Unattainability **compositional**; proper distance to wall **finite** \(X(1+\pi/2)\).  
**J1 honesty:** `simple_metric_J1_honesty_skeleton_results.md` — J1 CHOSE working; join-free still coherent.  
**Rooms:** `simple_metric_rooms_filled_local_results.md` — filled vs local; C1⇔ρ_s=0; hyp J1 sheet.  
**Relational + margin:** `simple_metric_relational_rooms_continue_results.md`  
- **No preferred center:** every observer sees wall at compositional \(X\); same \(d_L(z)\) form.  
- Hyp vs linear filled characters contrasted (no crown); both linear low-\(z\), different slope.  
- Local compactness \(C\to1\) **bridges** to filled wall.  

**Elegance uncover:** `UDT_ELEGANCE_UNCOVER.md` — kinematic chain, one scale \(X\), no EOS menu.  
**SNe clues:** L (WR-L) \(\chi^2/\mathrm{dof}\sim 0.91\); H hyp+J1 fail (~2.17). P_ell (~1.02) **RETIRED**.  
**Candidates zoom:** `simple_metric_promising_candidates_ZOOM.md`  
**L selection:** **WR-L / C-2026-07-09-1** ⇒ \(A=1-r/X\); half-stress / P-opt = duals; L own ⊕.  
**H/L unification:** `simple_metric_HL_unification_results.md`  
- **Spine (forced):** \(A=e^{-2\phi}\), φ additive ⇒ **\(A\) multiplies**, wall \(A\to0\).  
- **Fork only:** areal embedding \(r/X=f(A)\):  
  - **H:** \(f=(1-A)/(1+A)=\tanh\phi\) (rapidity map)  
  - **L:** \(f=1-A\) (residual map)  
- Same kinematics underneath; SNe rank **embeddings**, not kinematics-vs-continuum.  
- \(p_t=-\rho/2\) ⇔ L embedding + Einstein (two faces).  
- P_ell third branch **RETIRED** (detour; composition chart ≠ areal).  

**Dotted line:** residual \(A\); fork embeddings.  
**Winner path (WR-L DERIVED + audit PASS):** **L** (\(r/X=1-A\)). SNe ~0.91 character clue. Mass packaging **Principle-7** (do not lean).  
**★ L STATUS:** **DERIVED under WR-L** (Charles accepts wall package, 2026-07-09).  
  Records: `simple_metric_L_equivalence_principle_GAP.md` · **`simple_metric_L_wall_regularity_closure_results.md`**  
- Package **WR-L**: residual re-centering ⇒ family \(A=(1-r/X)^{\alpha}\); ∞ optical + finite proper + finite wall \(G^\theta{}_\theta\) ⇒ **\(\alpha=1\)** only ⇒ **\(A=1-r/X\)**.  
- Tag: **DERIVED** under WR-L — **C-2026-07-09-1** + audit **1a** — not SNe-selected / not bare R1–R3 alone.  
- External triple-blind audit **PASS**: `simple_metric_WR_L_external_triple_blind_audit_results.md`.  
- Own consciously: only **finite proper** kills \(\alpha=2\); \(\alpha=1\) = **causal horizon** (interior beyond \(r=X\)), not hard edge of space.  
- P-opt / \(p_t=-\rho/2\) / \(S_r=S_A\) are **consequences / duals** of L under WR-L.  

**Native L (consistent under P-opt or wall package):** `simple_metric_L_native_optical_derive_results.md`  
- Under P-opt \(\mathrm{d}r/A=\kappa\mathrm{d}\phi\) ⇒ unique \(r/X=1-A\), \(X=\kappa/2\).  
- Continuum half-ratio and \(M=X/2\) follow on L.  

**Angular-on MAP:** `simple_metric_angular_on_solution_space_MAP.md`  
**Angular/time on L:** static multipoles wall-loud; time-live densifies (infinite optical wall).  
**Hard explores:** `simple_metric_hard_explore_results.md` + **`simple_metric_local_cavity_HG_results.md`**  
- \(A=H+G\): **wall deforms** \(r_{\mathrm{wall}}/X=1+G(\theta)\).  
- **Local residual interiors:** discrete \(\omega_n\) **converge** with N; \(\Delta\omega\cdot L_{\mathrm{opt}}\to\pi\).  
- Filled L wall still densifies — **not** a finite drum.  
- **News:** discrete residual ringing is a **local-room** phenomenon; filled L is distance/mass room.  

**SOLUTION-SPACE FOCUS (Charles):** **kaleidoscope** — inter-frame *appearance* (not local physics changing with \(r\)).  
MAP: `simple_metric_kaleidoscope_MAP.md` · **MINE:** `simple_metric_kaleidoscope_MINE_results.md` · K1–K4.  
- **Static L kaleidoscope largely mined:** universal seat ladder; \(H\times L_{\mathrm{rem}}=1\) characterizes L; wall-as-sky; four distances; clocks=\(z\); Tolman mimic.  
- **★ Critical depth** \(r=2X/3\), \(z=\sqrt{3}-1\): max null impact, geometric \(dN/dz\) peak (proper-homog.), \(d_L=L_{\mathrm{room}}\), \(H_0 d_L=1\), MS \(m/M=4/9\).  
- **Pure L:** no preferred *angular* BAO scale — Charles cell/micro BAO **shelved** (agree).  
- **Open appearance sector:** time-live residual (Killing fails). Full caustics = thin residual. Local drums = side.  

**BAO pure two-leg (no \(r_d\)/DE packaging):** `simple_metric_bao_pure_AP_character_results.md`  
- \(F_{\mathrm{obs}}=(D_M/r_d)/(D_H/r_d)\approx\Delta z/\theta\); L predicts \(R_L=z+z^2/2\).  
**BAO proper pass:** `simple_metric_bao_proper_pass_results.md`  
- Low‑\(z\) LRG on \(R_L\); high‑\(z\) \(F\sim 4.5\)–4.7 vs \(R_L\sim 5.1\).  

**Time-live AP (prior probes):** `simple_metric_timelive_AP_results.md` · intermediates.  
- Mean \(\Delta z/\theta\) still on \(R_L\); wall-loud non-adiabatic scatter character (prior).  
**★ Time-live residual appearance MAP (2026-07-09):** `simple_metric_timelive_residual_appearance_MAP.md`  
- Root: \(\partial_t A\neq 0\) ⇒ \(p_t\) not conserved ⇒ **path-integrated** redshift (static L is endpoint-only).  
- Exact (WORKING \(A(t,r)\), \(B=1/A\)): \(1+z=\sqrt{A_o/A_e}\,\exp[-\int_e^o \partial_t\ln A\,dt]\).  
- **Faces of same integral:** redshift drift \(dz/dt_o\) **and** AP two-leg residual (related, not identical). Static L cannot fake either.  
- Scatter/caustics/**loud** **not** forced by symmetric \(A(r,t)\) alone.  
- Birkhoff = GR-form warning only; reciprocal diagonal time-live still **WORKING**.  
- Grade: **STRONG LEAD / MAP** — not canon until time-live sector chosen.  
**★ Exact time-live AP derive:** `simple_metric_timelive_AP_exact_derive_results.md`  
- \(1+z=\sqrt{A_o/A_e}\exp[-\int_e^o (A_T/A)\,dT]\); \(R_{\mathrm{AP}}=-\frac{r}{2A}(A_r+A_T/A)\).  
- Static L recovers \(R_L=z+z^2/2\). Time-live L: pure \(H_X=X_T/X\) correction.  
- **Moving WR-L wall is horizon-loud** unless \(A_T=O(A^{1+\varepsilon})\) or \(X_T=0\) at wall (or form fails).  
- Grade: **DERIVED** under WORKING reciprocal diagonal.  

**Principle-closure:** bare NPC **FAIL**; **WR-L accepted** ⇒ L form **DERIVED**  
  (`simple_metric_L_wall_regularity_closure_results.md`).  

**★ Center of static WR-L (2026-07-09):** three external passes; local CAS.  
  `…center_nogo_atlas…` · `…center_invariants_second_pass…` · **`simple_metric_WR_L_center_recenter_exclusion_results.md`**  
- Center-regular \(\Leftrightarrow A'(0)=0\). Residual family: \(A'(0)=-\alpha/X\neq 0\) — **no** \(\alpha\) is center-regular.  
- **\(\boxed{\text{residual re-centering }\bot\text{ center regularity}}\)** if re-centering is exact globally — singularity is structural, not optional paint.  
- Wall package still silent as *wall* selector; global re-centering is what forces the cusp.  
- **Charles ruling (A):** re-centering **exact** as residual law; \(r=0\) is \(\phi=0\) seat — singularity OK as **regime boundary** (macro residual vs micro/particle handoff character). **Not (B).**  
- Atlas: re-centering ≠ manifold coord change. Character lead: clean exterior, not global vacuum on \([0,X]\).  
- \(\rho\sim 1/r\) not a derived particle core.  

**★ EOS power window (2026-07-09, external + CAS):** `simple_metric_EOS_power_window_dS_results.md`  
- **Different family** from residual re-centering: \(A=1-(r/X)^{\beta}\), \(\beta=-2w\), under **CHOSE** \(p_t=w\rho\) + Einstein reciprocal.  
- L = \(\beta=1\) (\(w=-1/2\)); dS = \(\beta=2\) (\(w=-1\), \(A=1-r^2/X^2\), \(\rho=3/(8\pi X^2)\)).  
- Center-regular \(\Leftrightarrow\beta\ge 2\); + DEC \(\Rightarrow\) window collapses to **\(w=-1\) only**.  
- Unifies center singularity of L with “narrow window” → a point (Λ). **NOT** derived from WR-L re-centering.  
- **Choice 2 / dS (softened verify):** EOS \(w=-1\) uniqueness **PASS** inside GR-form box; \(A=1-r^2/X^2\) **native-forbidden** under φ-blind — **GR-form heuristic only**, not dual-layer native macro.  
- **dS native CLOSED for any α** (sign-changing source vs fixed-sign coupling) — `simple_metric_dS_native_any_alpha_closed_results.md`. Thread B ≠ dS road.  
- **Kaleidoscope / frame-relation:** no cosmic dS ball; ruling **(A)** is whole seat story.  
- V-CENTER **PASS**; V-EOS math PASS + caveats: `simple_metric_center_dS_external_verify_pass_results.md`.  

**★ Thread B workstation RAN (2026-07-09, pull `3c827f6`):** `threadB_coupled_cell_flatness_Lselector_results.md`  
- **Coeff settled:** \(S=-(\alpha/2)\,\xi\,e^{\alpha\phi}\rho^2 I_r\) (`verify_alpha_coeff_ANCHORED.py` PASS). For \(\alpha<0\), \(S>0\).  
- **Probe (prescribed \(I_r\)):** T1 flat deficit can cross 0; T2 matter selects \(r_s\); T3 finite core. Flat cross is **mainly \(T_{AB}\)** (also at \(\alpha=0\)); \(\alpha\) only modulates.  
- **Self-consistent f2d:** **NO closed flat cell** — matter **drains** (\(I_r\to0\), \(L\to0\)); robust under iters/grid/\(\alpha\); not under-iteration.  
- **Grade: CONDITIONAL** — do **not** bank closed cell / L-pin.  
- **Solver-first MAP:** `threadB_f2d_drain_solver_first_MAP.md`.  
- **Non-round+topo audit RAN (`452e1f7`):** `threadB_f2d_nonround_topological_audit_results.md` — **drain SURVIVES** (scoped FAILURE). Topology does **not** unwind (\(Q=N\)); \(I_r\) drains (rigid hedgehog).  
- **Mirror-vs-wall RAN (`1457994`/`5b107d0`):** `threadB_f2d_mirror_vs_wall_results.md` — **drain SURVIVES** (scoped FAILURE; 2× blind-verify).  
  - Open matter seal still drains (`f_r=0` **not** the channel).  
  - WR-L geometric φ-wall **obstructed** on bounded cell (wall depth only with L→∞ drained branch).  
  - α-source LIVE but ∝\(I_r\) vanishes with drain.  
- Dispatch (done): `threadB_WORKSTATION_DISPATCH_mirror_vs_wall.md`.  

**★ Carrier provenance (2026-07-10, workstation):** `matter_carrier_provenance_audit_results.md` — S² carrier is a **POSIT** (not metric-derived); L2/L4 native *given* the posit. Blind-refutation held.  
**★ H4·N4rev:** CF2 mass-sign **box-controlled** in parked two-player frame (`H4_N4rev_sign_certification_results.md`); hedgehog drain ≠ hopfion mass (object guard).  
**★ Time-live linear gate (2026-07-10, external derive):** `threadB_timelive_linear_nogo_and_finite_amp_MAP.md`  
- About drained hedgehog \(f_0=\theta\): **no linear growing mode** (\(\omega^2\ge0\)) — static drain **not** rescued by linear time-live.  
- Finite-amp: \(\langle\Sigma_\phi\rangle>0\); collective breathing + fixed-\(Q\) isorotation = **DEMO/LEAD** persistence candidates (not full PDE).  
- Oscillating core **cannot** stay reciprocal \(B=1/A\) throughout (\(\rho+p_r>0\)).  
- **Next full solve:** H3 + fixed-\(Q\) isorotation + metric backreaction (not more static seals).  
**★ Hopfion / mass / ambient-φ MAP (2026-07-10):** `hopfion_mass_background_coupling_MAP.md`  
- Particle mass = action on **posited** S² carrier (H3 object), **not** residual L.  
- H3 exists; local φ-source ON in core; \(\phi_{\mathrm{amb}}\) sets far-field regime.  
- CF2/δm box-controlled in **parked** two-player frame — not absolute masslessness.  
- Crux: **G/P exterior switch**; hedgehog drain ≠ hopfion.  
- LEAD: fixed-\(Q\) isorotation from H3 + non-reciprocal backreaction.  
**★ H3 G/P exterior probe RAN (`8a09ef2`):** `hopfion_GP_exterior_probe_results.md` (MAP frozen first). Blind-verify held.  
- **Native Branch-P (source ON):** exterior flux **DRIFTS** (boxy-P) — theorem \(dq/dr=4e^{-2\phi}\); no localized conserved flux; depth-invariant class.  
- **Branch-G control (source OFF):** **PLATEAUS** (machine conservation).  
- Probe does **NOT** decide the branch (switch still underived); shows P⇒drift, G⇒plateau cleanly.  
- Static reciprocal frame alone does **not** give branch-honest localized mass.  

**★ Fixed-\(Q\) Phase 0 DEMO (`hopfion_fixedQ_*`):** reduced \(E_Q(R)\) has stable finite-\(R\) min for \(Q>0\) (H3 virial; CHOSE inertia norm) — DEMO not PDE/mass.  
  MAP: `hopfion_fixedQ_isorotation_MAP.md` · results: `hopfion_fixedQ_collective_phase0_results.md`.  

**★ Fixed-Q Phase 1 pilot:** `hopfion_fixedQ_phase1_isorotation_results.md` — \(E_Q\)/\(I\) machinery LIVE on CUDA; plain GD **does not** hold hopfion topology (N=48 slips).  
  Need production Newton + H3 restart (Phase 1b).  

**★ Fixed-Q Phase 1b (`hopfion_fixedQ_phase1b_production_results.md`):** N=192 held hopfion; \(Q\in\{0,0.5,1,2\}\) continuation **HOLDS** \(|Q_H|\sim0.968\).  
  Arrested-Newton on \(E_Q\); flat FS only.  

**★ Phase 2 metric backreaction RAN (`30c5bd2`):** `hopfion_phase2_metric_backreaction_results.md`  
- Fixed-Q isorotation **does NOT de-box** exterior (all P arms DRIFT; G controls PLATEAU).  
- Compact sources cannot change vacuum-P exterior — near-theorem; ω→1 still drifts.  
- Grade **LEAD/CONDITIONAL** (partial blind; driver JSON doublecheck agrees).  
- **Routing:** stop core source-engineering; mass de-box ⇒ **G/P switch** on hopfion exterior.  

**★ G/P switch apply RAN (`aba76a1`/`9b1d41c`):** `hopfion_GP_switch_apply_MAP.md` + `hopfion_GP_switch_apply_results.md`  
- Hopfion supplies **no N1** (compact; ambient A=4πr² free).  
- Branch **not decided by the object**: unbounded scope leans G (clean flux if G); finite-cell wall could supply N1⇒P (drift).  
- Mass crux localized: **seal-matching / ambient** (continuum vs finite-cell wall location).  
- Grade **CONDITIONAL/LEAN** — not mass, not branch canon.  

**★ H3 STATIC MASS-BACKREACTION (2026-07-11 frame): SUPERSEDED** — Phase B settled + Phase-C mass recomputed by the
corrected-carrier arc (see CURRENT STATE topmost). Historical block archived: `archive/LIVE_h3_stability_layers_2026-07-11_12.md`.

**Red:** bank Thread B as closed cell / L-pin from probe; undo ruling (A) with smooth L core; treat global residual re-centering as center-regular; treat WR-L as smooth global SSS on \([0,X]\); bare-metric L claim; revive **P_ell**; lean on MS \(2GM/c^2\) as native; fluid BAO; χ²-shop \(A(r)\); treat \(x_{\max}\) as hard spatial wall (it is a **causal horizon**).

---

## Archive pointer (stale LIVE layers)

Historical frontier narratives (n=2 pivot, native-macro Q1, Thread A/B, rung-resonance, Stage-2 static, hopfion, …) moved 2026-07-09 to:

**`archive/LIVE_historical_frontier_through_2026-07-08.md`**

Also: `archive/LIVE_*.md` per-arc slices; `HANDOFF_ARCHIVE.md`.

## Durable canon (must-not-lose — short)

- **C-2026-07-09-1 (WR-L):** residual form \(A=1-r/X\) under residual re-centering + wall regularity.
- Earlier: C-2026-06-14-1, C-2026-06-18-1, finite-cell / R-areal (C-2026-06-10-*), seal sector split C-2026-07-04-1, P16 C-2026-07-05-1 — full text in **`CANON.md`**.
- DATA-BLIND: never load six lepton wall numbers in a derivation (contract 26fc757); predict ratios.
