# LIVE — the only guaranteed-current file (READ ME FIRST)

**⚠ BRANCH: work is on `grok` (2026-07-10).** If not on it: `git checkout grok`. `main` is stale for this arc.
**The CURRENT STATE block below is the only current frontier** — read it and stop.
Stale historical frontier layers live under `archive/LIVE_historical_frontier_through_2026-07-08.md`
(and older `archive/LIVE_*.md`). `HANDOFF.md` is lean; older session detail is in `HANDOFF_ARCHIVE.md`.
**If anything disagrees with this file's CURRENT STATE block, the CURRENT STATE block wins.**
**⚠ TWO LIVE LANES (2026-07-12):** the **PARTICLE-MASS lane** (H3 corrected-operator stability) is the arc under
active work — read `LIVE.md` CURRENT STATE (below, has the ▶ START-HERE command) → **`stability_branch_follow_256_DECISION.md`**
(detailed record) → MEMORY.md TOP. The **MACRO lane** (simple-metric / WR-L) is a separate ongoing lane; its read
order is: **`UDT_METHOD_MUSIC.md`** → **`UDT_DOTTED_LINE.md`** → **`UDT_ELEGANCE_UNCOVER.md`** → **`SIMPLE_METRIC_MACRO.md`**.
Free-\(D_A\) / mixed scoreboards = **`grok/quarantine_free_DA/`** only (not live).
Prior cell / Thread-A/B / macro-native pivots: **history** — see `archive/LIVE_historical_frontier_through_2026-07-08.md` and `archive/INDEX_pre_simple_metric_WR_L_2026-07-09.md`.

## Binding method (never skip)
- CLAUDE.md "How we work": MAP / OBSERVE / PONDER are primary, DERIVE is gated. Let structure
  EMERGE; pre-work discussion in LAY language; "chose or derived?" / "observing or targeting?".
- Discipline skills (`.claude/skills/`, auto-loaded): **solver-first**, **verifier-before-record**
  (incl. cross-model escalation), **no-shortcuts** (run `python3 -m pytest tests/` — **expect 1 FAILED** = the known hygiene-header doc backlog on some `simple_metric_*`/`threadB_*` result docs, NOT a code failure; ~69 passed / 1 xfailed otherwise), **completeness-map**.
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

## ============ CURRENT STATE (2026-07-14 — H3 STATIC PARTICLE-MASS arc: Phase-B stability NUMERICALLY CERTIFIED + BLIND-VERIFIED (positive spectrum, 3 grids); awaiting Charles's verdict; NEXT = F (behavioral) / G (recompute Phase-C mass on corrected carrier)). ============

**➤➤➤ LATEST (2026-07-14 — STABILITY CERTIFICATION COMPLETE; records = `noNull_hess_h2fit_log.txt` +
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
  below our floor** (reproduces doublet+isolated at overlap 0.999–1.0; full-space floor = POSITIVE T/R
  cluster). AMENDMENTS (scoped, quantified): doublet convergence is T/R-DEFLATION-scoped (raw backward
  error 3.4e-2 lies wholly in the T/R quasi-symmetry span; raw-operator doublet = 0.2509±1.2e-3 —
  positivity robust); cross-seed identity = fixed-point check, not independent evidence; h² NOT pure
  (h⁴ significant at 128³; ~1e-3 systematic on extrapolants). NOT probed: hunts at 192/256; T/R floor
  below +3e-3 (≥97% translation/rotation = pinned-box boundary class).
- **SCOPE STAMPS (travel with the verdict):** static; THIS Q≈1 lower-E carrier; box L=6.0 (FREE);
  mask HBW=2 (FREE; wider-mask boundary sweep NOT done); EH/metric-only action = CONDITIONAL-DERIVED;
  S² carrier = posit (bedrock memory). Hess outputs now N-tagged (anti-clobber; converged vectors =
  `noNull_hess_refine_s{0,1,192_*,128_*}.npz`).
- **STATUS: `Nyquist instability FALSIFIED; corrected-operator static stability of the Q=1 carrier:
  POSITIVE SPECTRUM, numerically certified + blind-verified (scoped as stamped). Charles verdict
  pending.`** NEXT (on his go): **F** geodesic/trust-region behavioral branches (max-rotation
  amplitude) → **G** recompute Phase C (E4/source/flux, M_N=2E4) on the corrected carrier.

**➤➤➤ DETAILED ARC RECORD = `stability_branch_follow_256_DECISION.md` (full arc, retractions, fork).
The 2026-07-12 layer below is HISTORY of this arc (kept for the record):**

**➤➤➤ [SUPERSEDED-by-above] (2026-07-12 — Phase-B stability arc, corrected-operator repair):**
- **The Phase-B "localized negative mode / unwinding instability" (λ≈−290 cluster) was a CHECKERBOARD /
  NYQUIST OPERATOR ARTIFACT — FALSIFIED, blind-verified.** The energy AND hopf_charge used the centered
  difference `D^c=(f_{i+1}−f_{i-1})/2h` (`fs_hopfion.py:48`), which annihilates `(-1)^i` exactly. All 3
  negative modes lived in that null (`R_cb≈0.01` vs smooth 0.997; >96% Nyquist-face power). **An exact
  operator null is NOT removed by 384³ — the earlier "384³ is decisive" plan is SUPERSEDED.** See
  `nyquist-operator-artifact-negative-modes` memory + `stability_checkerboard_audit.py`.
- **Corrected operator built + validated:** `noNull_energy.py` — same continuum Faddeev-Skyrme functional,
  8-orientation one-sided (no Nyquist null), O(h²) to the same limit, autograd-exact (grad matches full
  autograd to 1e-16). The old −290 modes flip to +30000 under it (`noNull_curvature_check.py`).
- **"Stable soliton" (banked overnight) was RETRACTED → STABILITY LEAN / OPEN (Charles).** The Hessian
  had been computed at a NON-critical field with a too-wide core mask, loose convergence, and overlaps
  over-read as exact zero modes. Residual decomp: `‖g_f‖_{M⁻¹}=4.2` (true 2-layer free mask), core-
  concentrated, genuinely physical — field is NOT critical.
- **CRITICALITY REACHED (verified).** Fixed a moving-tangent Riemannian bug (transport curvature pairs —
  Charles caught it); corrected first-order (L-BFGS/CG) STALL at `‖g_f‖≈2.5` → Riemannian trust-region
  **Newton-Krylov** (`STAGE=nk`: Steihaug-CG, LM μ→0, U(1) deflation, projected HVP, Newton-decrement) with a
  **preconditioned inner CG** drove `‖g_f‖_{M⁻¹}` → **0.0157 < 0.05** (INDEPENDENTLY re-verified, fresh gradient).
  `noNull_critical_field.npz` = genuine critical point: E=274.958 (lower-E Q=1 min), Q=−0.992, θ_max=0.135.
  The 0.05 target was MET, not loosened.
- **HESSIAN: bs≥12-vs-32GB MEMORY WALL → Charles authorized a HYBRID (2026-07-12).** Streaming LOBPCG-with-P
  (correct: [X,W,P], stream H·S, generalized eigenproblem SᵀHS c=λSᵀS c) at bs=12 AND bs=10 /256³ OOMs at it=1
  (~31.5GB; monolithic checkpointing doesn't help; NO CPU offload / bespoke checkpointing allowed). **bs=8
  CONFIRMED to FIT** (smoke: clears it=1,2, rank 24/24, ~320s/iter, λ descend 80→4→1.4). Block ≥12 was a numerical
  safety margin (Charles), not a UDT premise; bs=8 holds the 6 T/R pseudomodes + 2 physical — enough for the first
  physical mode's sign at 256³; the fuller spectrum comes from bs=12 @192³/128³.
  **▶ START-HERE COMMAND (256³ Hessian, both seeds):**
  `STAGE=hess HESS_BW=2 HESS_BS=8 HESS_SEEDS=0,1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True timeout 36000 python3 noNull_resolve.py`
  (reliable pattern: `timeout … python3`, NOT `nohup … &`; ONE clean GPU process — pkill+verify free first;
  outputs `noNull_hess_bw2_out.json` + `..._ritz_bw2_s{0,1}.npz`).
  `STAGE=hess`: `HESS_BS` **default is now 8** (the confirmed-fit value; bs=10/12 OOM at 256³), converge **ALL lowest-8 Ritz
  pairs** r_j<1e-3 across ≥2 seeds; **Q_TR pseudomode projection** s_j=|Q_TRᵀv_j|² (>0.5 ⇒ pseudomode; RECORDED,
  never used to discard); **rank-revealing geneigh** (logs `rank=rk/k0`). True 2-layer mask PRIMARY; wider masks
  (`HESS_BW=4/8/12`) = boundary-sensitivity only.
- **⚠ KEY OPEN RISK — the `r_j<1e-3` gate may be UNREACHABLE (dress-rehearsal finding, undetermined).** A 5-iter
  bs=8 run shows eigenVALUES descend beautifully (80→0.845) but `max_r_j` stays FLAT ~0.95 (NOT the T/R pseudomodes
  — s_TR~0.01–0.09 for all lowest-8). Math: `r_j=√((‖Hv‖−λ)/(‖Hv‖+λ))`; r_j≈0.96 at λ≈0.845 ⇒ ‖Hv‖≈20, i.e. the low
  Ritz vector carries ~20% contamination from far-stiffer modes (spectrum runs ~0→+30000). **Undetermined from 5
  iters:** either (benign) eigenvalues still moving so high residual is expected → watch if `r_j` drops after the
  values stabilize (~it=15–25); or (fatal) the operator's huge dynamic range means a tiny stiff-mode contaminant
  dominates the RAW residual → `r_j<1e-3` unreachable and the run spins to maxit. **If it stalls after eigenvalue
  stabilization, the fix is a PRECONDITIONED-residual measure (‖M_pre^{1/2}(Hv−λv)‖) or stiff-band deflation — NOT
  more iters.** Decision for Charles before/early in the real run. Do NOT bank on a raw-r_j that won't converge.
- **THEN — 192³ & 128³ (bs=12), turnkey.** `noNull_resolve.py` reads params (N,L,h,xi,kap) from `BASE_FIELD`
  (default `controlled_best_field.npz`=256³) and the field from `CRIT_FIELD` — BOTH now env-configurable (was a
  hardcoded-256³ bug, fixed 2026-07-12). Steps: (1) `TARGET_N=192 python3 noNull_downsample.py` → `noNull_critical_field_192.npz`;
  (2) `BASE_FIELD=noNull_critical_field_192.npz CRIT_FIELD=noNull_critical_field_192.npz STAGE=nk NK_BUDGET_S=6000 … timeout 9000 python3 noNull_resolve.py`
  (MUST re-relax: the interpolated field is NOT critical for the coarse operator — drive `‖g_f‖_{M⁻¹}<0.05`);
  (3) same env + `STAGE=hess HESS_BS=12 HESS_SEEDS=0,1 … python3 noNull_resolve.py` (bs=12 fits at coarse N). Repeat for `TARGET_N=128`.
- **▶ CHEAP FIRST TEST of the r_j risk (do this BEFORE the 256³ run):** 128³ is ~5× faster/iter (~59s vs 320s)
  and the r_j-stall is grid-independent (verified: bs=12 @128³ runs clean, rank 36/36, same flat r_j~0.95 while
  λ descend). So: `TARGET_N=128 python3 noNull_downsample.py` → NK-relax → `STAGE=hess HESS_BS=12` and run ~30–40
  iters (~40min). If r_j drops toward 1e-3 AFTER the λ stabilize → benign, proceed to 256³. If it stalls ~0.9 →
  the raw-r_j gate is unreachable → switch to a preconditioned-residual measure / stiff-band deflation FIRST.
- **STABILITY CERTIFIED ONLY IF** (h²-fit λ(h)=λ0+c·h²): all genuine physical low modes POSITIVE; first physical
  eigenvalue agrees 192³↔256³ within discretization error; small negative T/R pseudomodes trend →0 (not a negative
  continuum limit). Do NOT pre-claim smooth modes grid-converged — the 128/192/256 comparison must establish it.
- **NEXT (ordered):** bs=8@256³ run (2 seeds, watch r_j) → downsample+NK-relax carrier @192³ & @128³ → bs=12
  Hessian there (same gates) → h² fit + agreement → fresh-reimplementation verify → **F** geodesic/trust-region
  behavioral branches (max-rotation amplitude) → **G** recompute Phase C (E4/source/flux) on the corrected carrier.
- **HONEST STATUS:** `Nyquist instability FALSIFIED; critical Q=1 carrier obtained at 256³; stability OPEN pending
  the hybrid spectral test.` EH/metric-only action stays **CONDITIONAL-DERIVED** (separate premise). DATA-BLIND.

**Key files (this arc):** `noNull_energy.py` (corrected operator), `noNull_precond.py` (SPD preconditioner),
`noNull_resolve.py` (STAGE=relax corrected Riemannian L-BFGS/CG + STAGE=nk Newton-Krylov + STAGE=hess),
`noNull_residual_decomp.py` / `noNull_residual_modes.py` (residual diagnostics), `stability_checkerboard_audit.py`,
`noNull_curvature_check.py`, `stability_eigenmode_256.py` (block LOBPCG). Fields (gitignored `.npz`):
`controlled_best_field.npz` (old centered carrier), `noNull_critical_field.npz` (**the verified critical field, ‖g_f‖=0.0157**), `stability_lowmode_256.npz`. Hessian outputs: `noNull_hess_bw{W}_out.json` + `noNull_hess_ritz_bw{W}_s{seed}.npz`.
Reliable launch = `timeout N … python3` (NOT `nohup … &` — process-group cleanup kills it early). Grad = manual
autograd (functorch leaked at 256³); one clean GPU process; ~5 min/NK-step (HVP-heavy).

**[SUPERSEDED plan]** The 07-11 "Phase A/C PASS + Phase B unresolved-with-concern, 384³ decisive" is
superseded by the 07-12 operator-artifact finding above. Phase A/C's clean `M_N=2E4` (0.05%) must be
RECOMPUTED on the corrected carrier (step G) — its prior numbers used the superseded centered operator.

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

**★ H3 STATIC MASS-BACKREACTION (new frame, `UDT_H3_STATIC_MASS_BACKREACTION_DISPATCH.md`; EH geom action + physical-metric carrier coupling; demote reciprocal/G-P/ḡ for the particle):** `hopfion_static_mass_results.md` (`b114a88`+)  
- **Phase A/C PASS (rigorous):** identities ρ+S=2ρ_4≥0 machine-exact (L2 cancels; only compact L4 sources the lapse); local mass **M_N=2E_4=E_2+E_4** confirmed by **isolated-BC (Hockney) Poisson + INDEPENDENT discrete face fluxes to 0.05%** (plateau-flat; NOT the earlier tautological volume self-check nor the periodic-image-drifting sphere flux). Axisymmetric to 0.02% (Fourier).  
- **Phase B (stability) UNRESOLVED — with concern; 256³ mode-following test DONE:** topology-safe relaxation drove gradnorm 0.12→**0.085** (Q=0.9918 held; ~0.12 NOT a floor), but beyond that the flow drifts to unwinding ⇒ no true critical point at 256³. A localized negative mode **PERSISTS** through relaxation (λ_phys −312@0.13, −318@0.11, **−285@0.085**, 3 seeds, in_core 0.997) — it does NOT lift; the earlier "+69" stable-lean was an unconverged probe (RETRACTED). Orthogonal to gradient, Q-preserving, real-curvature. NOT PASS, NOT FAIL (non-critical field; res/|λ|~0.15 not tight; **contradicts the KNOWN stability of the Q_H=1 FS hopfion** ⇒ likely a 256³ grid-scale artifact). **Decisive next = 384³** (Charles-sequenced): re-solve finer, recompute Hessian at a critical point — vanishes ⇒ grid artifact (stable); persists converged ⇒ real FAIL.  
- **⇒ clean mass NOT established:** CONDITIONAL on (i) EH-action premise (Lovelock, not native-dilation-derived — trigger #6) AND (ii) an UNRESOLVED (floor-limited) Phase B. D/E HALTED. (Infra: a GPU-zombie holding 30.8GB caused repeated 256³ OOMs; cleared.)  

**➤➤ NEXT [SUPERSEDED 2026-07-12→14: the "384³ decisive" plan died with the Nyquist-artifact finding; Phase B was then closed via the corrected-operator certification — see CURRENT STATE at top]:** ~~close Phase B on a **finer grid** (≥384³ or higher-order/spectral) to lower the residual-gradient floor below the mode, then recompute the Hessian; only then trust the Phase-A/C mass.~~ (Prior lane: seal-matching/ambient gate; no private wall at ℓ_hopf; not O(0.4)-mass without continuum.)  
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
