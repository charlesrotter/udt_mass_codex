# LIVE — the only guaranteed-current file (READ ME FIRST)

**The CURRENT STATE block below is the only current frontier** — read it and stop.
Stale historical frontier layers live under `archive/LIVE_historical_frontier_through_2026-07-08.md`
(and older `archive/LIVE_*.md`). `HANDOFF.md` is lean; older session detail is in `HANDOFF_ARCHIVE.md`.
**If anything disagrees with this file's CURRENT STATE block, the CURRENT STATE block wins.**
**Read order (2026-07-09):** LIVE.md FRONTIER → **`UDT_METHOD_MUSIC.md`** (how to sit) →
**`UDT_DOTTED_LINE.md`** → **`UDT_ELEGANCE_UNCOVER.md`** → **`SIMPLE_METRIC_MACRO.md`** → MEMORY.md TOP.
Free-\(D_A\) / mixed scoreboards = **`grok/quarantine_free_DA/`** only (not live).
Prior cell / Thread-A/B / macro-native pivots: **history** — see `archive/LIVE_historical_frontier_through_2026-07-08.md` and `archive/INDEX_pre_simple_metric_WR_L_2026-07-09.md`.

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

## ============ CURRENT STATE (2026-07-09 — SIMPLE METRIC + WR-L canon; free \(D_A\) quarantined). ============

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

**Time-live AP:** `simple_metric_timelive_AP_results.md` · **intermediates:** `simple_metric_timelive_AP_intermediate_results.md`  
- Mean \(\Delta z/\theta\) still on \(R_L\) (even wall-loud).  
- **Needle:** wall-loud + **non-adiabatic** \(k_t\) ⇒ **phase scatter grows with \(z\)** (~1%→7% by \(z\sim 2.3\)).  
- Mean high‑\(z\) BAO gap **not** closed by FREE 5% oscillation. Full Einstein+AP still open, not yet crash-priority for mean alone.  

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
- **Thread B real content:** restoring channel + L-selector + bounded cell — probe `simple_metric_alpha_restoring_probe_results.md`; charter `threadB_coupled_cell_flatness_Lselector_CHARTER.md`.  
- V-CENTER **PASS**; V-EOS math PASS + caveats: `simple_metric_center_dS_external_verify_pass_results.md`.  

**➤➤ NEXT:** Thread B **coupled cell** charter (flatness T1 + L-selector T2 + core T3) when Charles dispatches — not dS. Else residual L kaleidoscope / time-live. Do **not** chase native continuum dS.  
**Red:** undo ruling (A) with smooth L core; treat global residual re-centering as center-regular; treat WR-L as smooth global SSS on \([0,X]\); bare-metric L claim; revive **P_ell**; lean on MS \(2GM/c^2\) as native; fluid BAO; χ²-shop \(A(r)\); treat \(x_{\max}\) as hard spatial wall (it is a **causal horizon**).

---

## Archive pointer (stale LIVE layers)

Historical frontier narratives (n=2 pivot, native-macro Q1, Thread A/B, rung-resonance, Stage-2 static, hopfion, …) moved 2026-07-09 to:

**`archive/LIVE_historical_frontier_through_2026-07-08.md`**

Also: `archive/LIVE_*.md` per-arc slices; `HANDOFF_ARCHIVE.md`.

## Durable canon (must-not-lose — short)

- **C-2026-07-09-1 (WR-L):** residual form \(A=1-r/X\) under residual re-centering + wall regularity.
- Earlier: C-2026-06-14-1, C-2026-06-18-1, finite-cell / R-areal (C-2026-06-10-*), seal sector split C-2026-07-04-1, P16 C-2026-07-05-1 — full text in **`CANON.md`**.
- DATA-BLIND: never load six lepton wall numbers in a derivation (contract 26fc757); predict ratios.
