# LIVE — the only guaranteed-current file (READ ME FIRST)

**The "## ============ FRONTIER ... CURRENT STATE" block below is the ONLY current frontier** — read it and stop;
everything under the "↓↓↓ HISTORICAL ARC" / "SUPERSEDED" fences is labeled-stale detail (mine for history, not the
plan). `HANDOFF.md` / `STATE.md` are detailed history; **if they disagree with this file's CURRENT STATE block, the
CURRENT STATE block wins.**
**Read order (2026-07-09):** LIVE.md FRONTIER → **`UDT_METHOD_MUSIC.md`** (how to sit) →
**`UDT_DOTTED_LINE.md`** → **`UDT_ELEGANCE_UNCOVER.md`** → **`SIMPLE_METRIC_MACRO.md`** → MEMORY.md TOP.
Free-\(D_A\) / mixed scoreboards = **`grok/quarantine_free_DA/`** only (not live).
Prior-plan specs (mine for the Thread-B cell forward-thread, NOT the macro frame): `derived_background_and_phi_coupling_DESIGN.md`,
`matter_filled_background_closure_DESIGN.md`. — OLD read order (2026-07-07 PM-3, SUPERSEDED): LIVE.md FRONTIER
→ **`derived_background_and_phi_coupling_DESIGN.md`** (the seamless-pickup spec: THREAD A = redo `x_max`
PROPERLY from the observer FRAME-RELATION → the derived data-blind BACKGROUND, do FIRST; THREAD B = the native
φ-matter source → MASS / PARTICLE EMERGENCE; cosmology validation is OUT OF SCOPE) → `udt_phi_blindness_relaxation_results.md`
(Thread B: the source `α·ξ·e^{αφ}ρ²I_r` + the restoring channel, blind-verified) → `udt_canonical_geometry.md`
§1.4 (frame-relation) / §10.4 (Misner–Sharp) / §12.7 (the legacy polynomial + its unforced-form note) for Thread A → CLAUDE.md "How we
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

## ============ CURRENT STATE (2026-07-08 — SIMPLE METRIC ONLY; free \(D_A\) quarantined). ============

**➤➤➤ LATEST (Charles: stick to simple metric; derive everything from it; quarantine free \(D_A\)).**

**Binding frame:** `UDT_ELEGANT_FRAME.md`.  
**LIVE foundation:** **`SIMPLE_METRIC_MACRO.md`** + CAS `simple_metric_FE_rederive.py`.  
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
Under join **J1** (\(r\equiv x\)): hyperbolic \(A\) ⇒ \(m=c^2 x^2/(G(X+x))\) ⇒ \(M_{\mathrm{tot}}=c^2 X/(2G)\) ⇒ **\(x_{\max}=2GM_{\mathrm{tot}}/c^2\)** (\(k=2\)). Closure \(A\to0\) and compactness→1 at the bound are **identities** of the profile (filled cosmos, not empty Schw). Absolute scale still needs one ruler; relation is theory. J1 tagged CHOSE.

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

**PATH–AREAL split observe (2026-07-09):** `simple_metric_path_areal_split_results.md`  
P_ell full-cov χ²/dof **2.17→1.02** (LCDM ref 0.88). J1 over-join suspect.

**P_ell mass lock (2026-07-09):** `simple_metric_Pell_mass_lock_derive.md`  
Motivation: static rods measure \(d\ell=e^{\phi}dr\) ⇒ composition chart on **proper** path (motivated, not unique theorem).  
Exact: \(r_{\max}/X=\pi/2-1\); **\(r_{\max}=2GM/c^2\)**; \(X=r_{\max}/(\pi/2-1)\). Mass locks to areal saturation, not to \(X=r\).  
Compactness \(2Gm/(c^2r)=2x/(X+x)\) unchanged in \(x\).

**Success criterion (Charles 2026-07-09):** Do **not** require beating ΛCDM on every observable/χ². Goal = **one theory resolving multiple ΛCDM tensions** (goal, not yet demonstrated). Continue **refining hyperbolic**, not trophy-chasing.

**Structure hygiene (process, not physics):** `STRUCTURE_HYGIENE.md` — layered L1 machine / L2 artifact headers / L3 periodic audit / L4 Charles+blind; build-on grades DEMO|LEAD|CONDITIONAL|BANKED-FOR-STRUCTURE.

**Self-audit (2026-07-09):** `simple_metric_session_self_audit_2026-07-09.md`  
P_ell = **explore join (CHOSE)**, not canon — χ² improvement must not freeze it. LCDM = residual **reference only**. MS mass = GR-form conditional. Full light = derived on static simple metric (scoped).

**Hyperbolic stack (refine target — premise-tagged):**
- PATH: \(x=X\tanh\phi\), \(1+z=e^{\phi}\), bound \(X\) — **POSTULATE** + derived form
- Full light: \(d_L=(1+z)^2 D_A\) — **DERIVED** (static SSS scope)
- **P_ell** \(x=\ell\): **CHOSE explore** (motivated rods; uniqueness OPEN) — demo χ²/dof~1.02 vs J1~2.17 vs LCDM-ref~0.88
- Mass under P_ell: **conditional** on P_ell + MS form; \(r_{\max}=2GM/c^2\), \(X=r_{\max}/(\pi/2-1)\)
- J1 demoted as **scoped residual**, not “metric forbids J1”

**R1 path ops (2026-07-09):** `simple_metric_R1_path_proper_results.md`  
Path=proper **not forced** by metric. Ops lengths characterized.

**J1 WORKING POSTURE (Charles 2026-07-09):** \(x_{\max}\) **literally defines sphere size** — long-standing intuition (~decades).  
Tag: **CHOSE by Charles physical picture** (not χ²-picked; P_ell SNe improvement does **not** override).  
Stack: PATH composition \(x=X\tanh\phi\) **with** \(D_A=r=x\) (J1); full light \(d_L=(1+z)^2 r\); mass lock under J1 \(X=2GM/c^2\).  
P_ell = archived **explore contrast** only (LEAD), not live foundation.

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
**SNe clues:** L linear \(p=1\) near (0.91); P P_ell-hyp near (1.02); H hyp+J1 fail (2.17).  
**Candidates zoom:** `simple_metric_promising_candidates_ZOOM.md`  
**L selection:** \(p_t=-\rho/2\Rightarrow A=1-r/X\) unique; L own ⊕.  
**H/L unification:** `simple_metric_HL_unification_results.md`  
- **Spine (forced):** \(A=e^{-2\phi}\), φ additive ⇒ **\(A\) multiplies**, wall \(A\to0\).  
- **Fork only:** areal embedding \(r/X=f(A)\):  
  - **H:** \(f=(1-A)/(1+A)=\tanh\phi\) (rapidity map)  
  - **L:** \(f=1-A\) (residual map)  
- Same kinematics underneath; SNe rank **embeddings**, not kinematics-vs-continuum.  
- \(p_t=-\rho/2\) ⇔ L embedding + Einstein (two faces).  
- P_ell = third branch (composition chart ≠ areal).  

**Dotted line:** residual \(A\); fork embeddings.  
**Winner path (WR-L DERIVED):** **L** (\(r/X=1-A\)) — form from wall-regular residual selector; mass lock + SNe joint best as package (clues, not form selectors).  
**★ L STATUS:** **DERIVED under WR-L** (Charles accepts wall package, 2026-07-09).  
  Records: `simple_metric_L_equivalence_principle_GAP.md` · **`simple_metric_L_wall_regularity_closure_results.md`**  
- Package **WR-L**: residual re-centering ⇒ family \(A=(1-r/X)^{\alpha}\); ∞ optical + finite proper + finite wall \(G^\theta{}_\theta\) ⇒ **\(\alpha=1\)** only ⇒ **\(A=1-r/X\)**.  
- Tag: **DERIVED** under WR-L — **canonized C-2026-07-09-1** — not SNe-selected / not bare R1–R3 alone.  
- P-opt / \(p_t=-\rho/2\) / \(S_r=S_A\) are now **consequences / duals** of L under WR-L.  

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

**Time-live AP:** `simple_metric_timelive_AP_results.md` · **intermediates:** `simple_metric_timelive_AP_intermediate_results.md`  
- Mean \(\Delta z/\theta\) still on \(R_L\) (even wall-loud).  
- **Needle:** wall-loud + **non-adiabatic** \(k_t\) ⇒ **phase scatter grows with \(z\)** (~1%→7% by \(z\sim 2.3\)).  
- Mean high‑\(z\) BAO gap **not** closed by FREE 5% oscillation. Full Einstein+AP still open, not yet crash-priority for mean alone.  

**Principle-closure:** bare NPC **FAIL**; **WR-L accepted** ⇒ L form **DERIVED**  
  (`simple_metric_L_wall_regularity_closure_results.md`).  

**➤➤ NEXT:** time-live residual / appearance; micro when ready. Canon ledger: **C-2026-07-09-1** (WR-L).  
**Red:** claim L from bare R1–R3 alone; fluid BAO; χ²-shop \(A(r)\); screening kludge; demote WR-L to SNe chart shopping.

### ↓↓↓ SUPERSEDED-as-frontier (2026-07-08 EOD — n=2 optics + macro-needs-a-source). Still true as results, not the live framing priority. Full record: `luminosity_distance_n2_optics_results.md`. n=2 forced; n=1 Pantheon flattery = artifact; sourceless vacuum fails SNe under n=1 and n=2. Matter budget / closure guardrails remain available when matter is on-stage — subordinate to elegant frame. ↓↓↓

**➤➤➤ (archived summary)** n=2 `d_L=(1+z)²D_A` verified; §12.8 n=1 form was √g_rr error. Vacuum sourceless fails; Q1/matter-source path was the prior NEXT. Branch G/P = one 𝒦-weight switch; cell package ≠ P-type. Matter GUARDRAIL: bracket to closure not SNe fit. Vacuum-as-limit lead (√-shaped) = historical lead only under new frame.

### ↓↓↓ SUPERSEDED-as-frontier (2026-07-08 midday — the "PIVOT to native-macro / MAP Q1" block; still the live PROGRAM, but
### the n=2 optics result above is the latest state). The two-player = cell-specialized; macro never solved natively; MAP =
### `macro_universe_native_MAP.md` (both G/P branches open); CRUX Q1 = what sources the macro φ. All still current — the n=2
### block above SHARPENS it (the source question is now confirmed as THE crux, under n=2 optics). ↓↓↓

**➤➤➤ LATEST (2026-07-08 — PIVOT to native-macro; Thread-A "derive the background" reframed).** This session ran the
2026-07-07 PM-3 plan (Thread A = derive the background) and, in doing so, discovered the plan's tool was wrong: (1) the
"round-cell cosine" macro background is a leading-order, cycle-averaged, ρ-frozen, MATTER-SOURCED reduction — NOT a
solution of the native two-player equation in any gauge; the native VACUUM two-player has no φ→∞ edge (blind-verified,
932 ICs, `cosine_native_reconciliation_results.md`, commit 0742063). (2) Matter is REQUIRED for scale AND edge (vacuum =
scale-free/featureless; dimensional: x_max-as-a-length can't come from c,G alone). (3) A Stage-1 matter scan
(`stage1_edge_scan.py`) found NO v→0 edge for any (α, matter-amount, shape, Z) — but it used the CELL (Branch-P)
equations for a MACRO question = the session's rabbit hole. (4) Charles's zoom-out + provenance trace (a9865905):
**the two-player equation is the Branch-P finite-cell/microphysics specialization** (founding doc §6, commit f766478);
**the macro universe has NEVER been solved natively** (F5 M-scan "a PLAN, never run"; macro φ always fit/reduced/circular).
**PIVOT (Charles): model the macro universe WHOLE from the native ACTION `S=∫c√h[(Z_φ/2)φ'²+R^{(2)}[h]+𝒦+L_m]`** —
dropping the cell PACKAGE (Y=frozen h_AB=r²Ω [the finite-domain ARTIFACT], Z=winding-defect+finite-core+seal-BCs). [CORRECTED 2026-07-08: NOT "drop Branch-P" — matter-sourcing REQUIRES the P-type uncompensated-𝒦 route; P-type≠cell once h_AB unfrozen. See the BRANCH NOTE in the n=2 block above.]
**MAP = `macro_universe_native_MAP.md` (both G/P branches OPEN per Charles).** ⚠ **NEXT STEP IS NOT A SOLVE — it is the
PONDER of the CRUX Q1: what SOURCES the macro φ?** Native eqs say matter does NOT directly source φ (δS_m/δφ=0; indirect,
Branch-P only); the macro source has always been an ASSUMED premise, never derived — the silent assumption under the whole
project. WATCH-ITEM (Charles): does a proper native macro solve reproduce the cosine `e^{−φ/2}=A cos(kr)` NATURALLY
(→ vindicated as the real macro object) or something else (→ cosine stays a cell-artifact)? Data-blind; depth is a
DERIVED goal (1101 OUT); don't use circular c²=2GM/R.

### ↓↓↓ SUPERSEDED-as-frontier (2026-07-07 PM-3 — the "derive the background (Thread A) then pivot to particle emergence
### (Thread B)" plan). The Thread-A start ran THIS session and pivoted to native-macro (above); Thread B (the α·ξ·e^{αφ}ρ²I_r
### restoring channel) remains a LIVE forward thread FOR THE CELL/particle sector, to resume AFTER the macro background is
### derived. `derived_background_and_phi_coupling_DESIGN.md` + `matter_filled_background_closure_DESIGN.md` are the specs;
### the latter's Stage-1 (no v→0 edge in Branch-P) is a CELL-regime result, not a macro verdict. ↓↓↓

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
POORLY SCAFFOLDED (unforced polynomial ansatz + the 1101 anchor) — do NOT lean on it.** LESSON: don't over-literalize
the observational frame-relation as a physical field, and don't overmodel (I built ISW/recycling mechanisms + homogeneity
field-solves on a category error; Charles corrected via the SNe work). **LIVE FORWARD THREAD (needs a fresh session —
context ~60%): the PARTICLE-EMERGENCE door** — relaxing φ-blindness (α≠0) gave matter a RESTORING channel (I_r sources
φ → supports I_r vs draining; which sign supports the cell is OPEN) for the matter-structure wall that killed the resonance test; the coupled `(f,φ,ρ)` solve
testing whether it closes a cell with `I_r>0` is the core test.
**➤➤ NEXT-SESSION PLAN (Charles) — spec = `derived_background_and_phi_coupling_DESIGN.md`. SEQUENCE: THREAD A FIRST
(flesh out the universe BACKGROUND), THEN pivot to THREAD B (MASS + PARTICLE EMERGENCE). Cosmology VALIDATION (SNe/BAO/CMB)
is OUT OF SCOPE — self-evident later; do not get pulled into it.**
- **THREAD A (do first) = redo `x_max` PROPERLY from the OBSERVER FRAME-RELATION** (`1+z=e^{φ(r)}`, §1.4 canonical
  geometry; NOT the "invariant distance" error) → a DERIVED data-blind BACKGROUND for the particle sector: derive the
  φ(r) FORM FROM the native two-player equations (which supply the scalar φ-eq the legacy framework lacked), the φ→∞ asymptotic edge, the depth anchor natively (1101/7.004 OUT). Use the CURRENT
  native two-player operators, NOT the legacy Einstein+KG/μ² machinery. GRAB from old work: frame-relation §1.4,
  `d_L=r(1+z)`, Misner–Sharp marginal; do NOT grab polynomial-as-derived / 1101 anchor / BAO-CMB scaffolding.
- **THREAD B (then pivot) = the native direct source `α·ξ·e^{αφ}ρ²I_r`** → the matter-structure RESTORING channel
  (open for **`α≠0`**) + matter L-selector; derive/characterize `α` (verdict C; re-adjudicate the α=−2 import-tag); the
  coupled `(f,φ,ρ)` solve = does a cell close with `I_r>0` SUPPORTED — **characterize ACROSS `α` (both signs); which sign
  supports the cell is OPEN (α<0 was the homogeneity/L-selector result, a DIFFERENT question — don't pre-fix it).** A
  furnishes the background B embeds a matter-coupled cell into = the particle-emergence setup we never had. Below the fences = CLOSED-ARC history (archived x_max detour, rung-resonance, Stage-2) — mine for history, NOT the plan.

### ↓↓↓ THIS SESSION'S DETOUR — ARCHIVED (2026-07-07 PM-3). Most of the session chased an INCORRECT vision (the
### `x_max` "invariant maximum distance" postulate + a homogeneity/Copernican field-solve) that was a CATEGORY ERROR —
### over-literalizing the redshift FRAME-RELATION as a physical field. Corrected by the PM-3 block ABOVE (redshift =
### observer frame-relation, no preferred frame, no center). Full detour + the lesson →
### **`archive/LIVE_xmax_homogeneity_detour_2026-07-07.md`** (incl. the archived x_max FRAME + boost docs). DURABLE
### residue kept live (two lines):
### - **φ-MATTER COUPLING (Thread-B foundation, blind-verified — `udt_phi_blindness_relaxation_results.md`):** φ-blindness
###   (α=0) is a CHOSE lever NOT forced; native direct source `α·ξ·e^{αφ}ρ²I_r`; relaxing it (α≠0) opens the
###   matter-structure RESTORING channel (the particle door; cell-restoring sign OPEN) + a matter L-selector. Owed: derive α (p16 verdict C).
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
