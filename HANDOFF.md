# HANDOFF — Resume (lean)

> **READ `LIVE.md` FIRST** — only guaranteed-current frontier + next action.
> If this file disagrees with LIVE.md, **LIVE.md wins.**
>
> **⚠ BRANCH: work is on `grok` (2026-07-10).** If not on it: `git checkout grok`. `main` is stale for this arc.

## CURRENT (2026-07-12 — H3 particle-mass, corrected-operator stability arc)

**Detailed record: `stability_branch_follow_256_DECISION.md`.** Live plan + next action: **LIVE.md CURRENT STATE**.

**One-paragraph state:** The Phase-B "particle unwinding instability" (a −290 negative-Hessian cluster) was
**FALSIFIED as a checkerboard/Nyquist OPERATOR ARTIFACT** — the centered difference `D^c` (fs_hopfion.py:48,
used by energy AND hopf_charge) annihilates `(-1)^i`; the 3 negative modes lived in that exact null (blind-
verified; `R_cb≈0.01`). 384³ can't fix an exact null → that plan is dead. A **corrected no-null operator**
(`noNull_energy.py`, 8-orientation, O(h²), autograd-exact) was built + validated; the old −290 modes flip to
+30000 under it. An overnight "STABLE soliton" verdict was **RETRACTED → OPEN** (Hessian was at a non-critical
field, wide mask, loose convergence, overlaps over-read). **CRITICALITY REACHED (verified):** free-variable
projection `P_free` (2 layers); moving-tangent Riemannian bug fixed (transport curvature pairs); corrected
L-BFGS/CG STALL at ‖g_f‖≈2.5 → Riemannian trust-region **Newton-Krylov** (`STAGE=nk`: Steihaug-CG + LM + U(1)
deflation + projected HVP + **preconditioned inner CG**) drove `‖g_f‖_{M⁻¹}` → **0.0157 < 0.05** (independently
re-verified). `noNull_critical_field.npz` = genuine critical point (E=274.958 lower-E Q=1 min; Q=−0.992). The
0.05 target was MET, not loosened. HONEST STATUS: *Nyquist FALSIFIED; critical Q=1 carrier at 256³; stability
OPEN pending the hybrid spectral test.* EH action stays CONDITIONAL-DERIVED.

**Hessian: bs≥12-vs-32GB WALL → Charles authorized a HYBRID (2026-07-12).** Streaming LOBPCG-with-P at bs=12/256³
OOMs (~30GB; monolithic checkpointing doesn't help). Plan: **bs=10 @256³** (memory-smoke first — no CPU offload/
bespoke checkpointing) + **bs=12 @192³ & @128³** (re-NK-relax each grid). `STAGE=hess`: `HESS_BS` (default 10);
converge **ALL lowest-9 Ritz pairs** r_j<1e-3 ×≥2 seeds; **Q_TR pseudomode projection** s_j (QR of 6 T/R gens
after U(1) removal — record, don't discard); **rank-revealing geneigh**. Certify stability only via h²-fit
λ(h)=λ0+c·h²: physical modes POSITIVE + 192↔256 agreement + neg pseudomodes→0. Don't pre-claim grid-convergence.

**Next (ordered):** bs=10@256³ smoke→run (2 seeds) → regenerate+NK-relax carrier @192³ & @128³ → bs=12 Hessian
there (same gates) → h² fit + agreement → fresh-reimpl verify → **F** behavioral branches → **G** Phase-C recompute
on the corrected carrier. Key files + launch caveats: LIVE.md.

**NOTE:** this particle-mass arc runs in its own (Charles-authorized) frame, SEPARATE from the macro/WR-L
lane below (both live; neither uniquely so).

## CURRENT (2026-07-09)

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
**NEXT:** see LIVE.md (fixed-Q isorotation / residual L).

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
