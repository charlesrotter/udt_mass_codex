# ARCHIVED LIVE layers — H3 stability arc 2026-07-11/12 (superseded by the 2026-07-14→16 record)

Moved out of LIVE.md on 2026-07-16 (Charles: archive truly stale startup material).
These layers are HISTORY: the corrected-operator repair plan (07-12) and the pre-correction
static-mass frame (07-11). The live record is LIVE.md CURRENT STATE + HANDOFF.md CURRENT.
Note: the 07-12 layer here says "lowest-8 Ritz pairs" while HANDOFF's archived copy said
"lowest-9" — a historical-cosmetic inconsistency; the production run converged NRJ=min(nc,9).

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


---

**★ H3 STATIC MASS-BACKREACTION (new frame, `UDT_H3_STATIC_MASS_BACKREACTION_DISPATCH.md`; EH geom action + physical-metric carrier coupling; demote reciprocal/G-P/ḡ for the particle):** `hopfion_static_mass_results.md` (`b114a88`+)  
- **Phase A/C PASS (rigorous):** identities ρ+S=2ρ_4≥0 machine-exact (L2 cancels; only compact L4 sources the lapse); local mass **M_N=2E_4=E_2+E_4** confirmed by **isolated-BC (Hockney) Poisson + INDEPENDENT discrete face fluxes to 0.05%** (plateau-flat; NOT the earlier tautological volume self-check nor the periodic-image-drifting sphere flux). Axisymmetric to 0.02% (Fourier).  
- **Phase B (stability) UNRESOLVED — with concern; 256³ mode-following test DONE:** topology-safe relaxation drove gradnorm 0.12→**0.085** (Q=0.9918 held; ~0.12 NOT a floor), but beyond that the flow drifts to unwinding ⇒ no true critical point at 256³. A localized negative mode **PERSISTS** through relaxation (λ_phys −312@0.13, −318@0.11, **−285@0.085**, 3 seeds, in_core 0.997) — it does NOT lift; the earlier "+69" stable-lean was an unconverged probe (RETRACTED). Orthogonal to gradient, Q-preserving, real-curvature. NOT PASS, NOT FAIL (non-critical field; res/|λ|~0.15 not tight; **contradicts the KNOWN stability of the Q_H=1 FS hopfion** ⇒ likely a 256³ grid-scale artifact). **Decisive next = 384³** (Charles-sequenced): re-solve finer, recompute Hessian at a critical point — vanishes ⇒ grid artifact (stable); persists converged ⇒ real FAIL.  
- **⇒ clean mass NOT established:** CONDITIONAL on (i) EH-action premise (Lovelock, not native-dilation-derived — trigger #6) AND (ii) an UNRESOLVED (floor-limited) Phase B. D/E HALTED. (Infra: a GPU-zombie holding 30.8GB caused repeated 256³ OOMs; cleared.)  

**➤➤ NEXT [SUPERSEDED 2026-07-12→14: the "384³ decisive" plan died with the Nyquist-artifact finding; Phase B was then closed via the corrected-operator certification — see CURRENT STATE at top]:** ~~close Phase B on a **finer grid** (≥384³ or higher-order/spectral) to lower the residual-gradient floor below the mode, then recompute the Hessian; only then trust the Phase-A/C mass.~~ (Prior lane: seal-matching/ambient gate; no private wall at ℓ_hopf; not O(0.4)-mass without continuum.)  