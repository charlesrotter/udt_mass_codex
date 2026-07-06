# N5d Solver — Build Plan (DESIGN ONLY; no solve, no pilot run)

**Status:** DRAFT build plan for driver → Charles review. **Design only** — this doc specifies the
solver; it runs NO coupled/N5d solve. The two cheap read-only self-tests it relies on were re-run and
PASS (see §7). **Author:** solver-architect agent, 2026-07-06.

## The question this solver must answer (structural yes/no, NOT a mass fit)
When the off-round transverse shear `h_AB` is UNFROZEN, does the coupled whole-cell (φ + shear) system,
with the φ-blind native-S² hopfion as source, **PIN** particle size / ξ / mass — or does the continuum
survive? Per the depth/size node (LIVE ★ OUTCOME C, `native_readout_map_depth_size_results.md`): the
ROUND Branch-P vacuum is provably a continuum (bulk equation exactly scale-invariant); the ONE frozen
DOF that could open a discrete closure is the off-round shear, via either **(i)** a sign-changing 𝒦
source → a potential well → turning points, or **(ii)** the transverse-traceless `h_AB` tensor
eigenproblem. N5d must carry `h_AB`'s traceless part as a LIVE DOF.

---

## 1. Module / file structure (EXTEND the one canonical native solver)

**EXTEND `cell_solver_f2d.py`** (the canonical round native Branch-P solver: coupled `φ(r), ρ(r),
f(r,θ)`; `cell_solver_f2d.py:1-69` header, EOMs `:17-27`, residual `:261-275`, LM solve `:299-339`).
Add ONE new field — the transverse traceless **shear** `s(r,θ)` (equivalently the pair `a(r,θ),
bt(r,θ)` of `op_derive2.py:2`) — plus the shear EL row and the off-round terms in the φ-source and
measure. Everything else (SH-exact θ operators `:115-139`, Chebyshev radial `:83-96`, jacrev-LM
`:299-339`, H/Derrick diagnostics `:230-255`) is reused verbatim.

- **New helper module `n5d_shear.py`** — the off-round transverse pieces kept isolated and unit-testable:
  `Kcal_offround(a,bt,ap,btp,phi)` (the exact 𝒦, §2), `sqrt_h(a,bt,theta)`, `EAB_shear_row(...)` (the
  traceless component of E^{AB}), and `lbare_precondition(...)` wrapping the CERTIFIED
  `h4_scripts/lbare_inverse.py:60` BVP inverse (for the linear-response cross-check + initial guess).
- **Fixed source helper** — reuse `h4_scripts/extract_stress_rtheta.py` (+ `stress_profiles.npz`) to
  read the H3-converged hopfion transverse stress `T^{AB}(r,θ)` from
  `hopfion_arc_scripts_2026-07-05/fs_hopfion.py`. The pilot feeds this as a FIXED profile (§3).
- **Harness / tests:** extend `cell_solver_f2d`'s bounded `__main__` smoke test (`:353-399`) and add
  N5d rows to the purity harness — a new `tests/test_n5d_roundlimit.py` (shear→0 recovers
  `cell_solver_f2d` exactly) and a `tests/test_n5d_offround.py` (𝒦[h] round reduction; source
  target-scalar & φ-blind). `tests/test_operator_from_action.py` gets the shear EL added to its
  action-EL identity check so the live operator stays == the EL of `solver_action.py`.

**Anti-proliferation justification (repo discipline "use git AS git", CLAUDE.md):** N5d is the shear
EXTENSION of the round native EOMs, not a new physics frame — so it EDITS the one canonical solver +
its harness, exactly as the discipline requires ("When you improve a solver, EDIT it … do not spawn
branchGP_v2"). It does **not** touch `branch_operator.py` / `prototype/branchGP_*` (the fenced
superseded scalar-tensor frame — §10).

---

## 2. Exact equations implemented (e^{−2φ} kept EXACT; no linearization)

Native constrained-two-player frame, Branch P, block-diagonal metric, φ longitudinal
(`native_field_equations_constrained_two_player_results.md:90`, H4_N1 scope caveat `:86-90`):

    ds² = −e^{−2φ(r)}c²dt² + e^{2φ(r)}dr² + h_AB dx^A dx^B ,  A,B∈{θ,ψ}
    h_AB = diag( a(r,θ) , bt(r,θ)·sin²θ )        [block-diagonal, g_rA=0]
    K_AB = ½ e^{−φ} ∂_r h_AB       (native_field:94 ; H4_N1:18)

**Trace / shear split** (round ⇔ shear ≡ 0):

    ρ²(r,θ) ≡ √(a·bt)   (areal-volume scale; √h = ρ² sinθ, φ-BLIND measure — native_field:92)
    s(r,θ) ≡ ½ ln(a/bt) (the TRACELESS shear DOF — the frozen mode N5d unfreezes; round: a=bt=ρ²=r², s=0)

**(a) The exact off-round invariant 𝒦[h]** (from 𝒦 = K_AB K^AB − K² = −2 det(K^A_B), H4_N1:57;
CAS-derived + round-checked in this plan's preflight):

    𝒦 = −½ e^{−2φ} (a' bt')/(a·bt) = e^{−2φ} 𝒦̂[h],   𝒦̂[h] = −½ (a' bt')/(a·bt)
    round a=bt=r²:  𝒦 = −2 e^{−2φ}/r² ,  𝒦̂ = −2/r²    ✓ (native_field:95 ; H4_N1:46)

The **sign-varying** content (mechanism (i), H4_N1:63-66): round has `a'bt' = 4/r² > 0` ⇒ 𝒦̂<0; a
toroidal core has one principal direction expanding, one contracting (`a'>0, bt'<0` or vice versa) ⇒
`a'bt'<0` ⇒ 𝒦̂ FLIPS SIGN. The reduced φ-source is therefore a distribution of varying sign — exactly
the object whose net far-field δq is undecided and which N5d resolves.

**(b) φ-equation (Branch P; e^{−2φ} EXACT; surface-integrated source, H4_N1 scope note :48-50):**

    ∂_r(√h Z_φ φ') = −2√h 𝒦 = √h e^{−2φ} (a'bt')/(a·bt)    [pointwise density; H4_N1:45]
    reduced radial ODE carries the θ-INTEGRAL  ∫ √h 𝒦 dθ    [the N2 surface-average, H4_N1:49-50]
    round shorthand check:  Z_φ (r²φ')' = 4 e^{−2φ}          (native_field:119)

**(c) Transverse tensor equation E^{AB} = −T^{AB}** (H4_N1:19-24, Branch P ⇒ W_χ=1):

    E^{AB} = (Z_φ/2)φ'² h^{AB} + [ ½ h^{AB}𝒦 − 2 K^{AC}K_C^B + 2 K K^{AB} ] − ∂_r π^{AB} = −T^{AB}
    π^{AB} = √h e^{−φ}(K^{AB} − K h^{AB})     (H4_N1:23 ; = the JC2 seal momentum seal_matching:30)

Two independent diagonal components (θθ, ψψ) ⇒ the **TRACE** row (gives the ρ-equation) and the
**TRACELESS** row (gives the shear s-equation — the genuinely new N1 content, H4_N1:79). Round
reduction of the trace row = the ρ-equation already in `cell_solver_f2d.py:222-223`
(`ρ'' = 2φ'ρ' − (Z/4)ρe^{2φ}φ'² + (e^{2φ}/4)(ξρI_r − κN²I_4θ/ρ³)`), with the `e^{2φ}/4` weight
confirmed GEOMETRIC (from √h·W_χ𝒦, NOT an e^{2φ}·T on the φ side — H4_N1:81-83). The traceless row is
NEW; its round linearization is the certified `L_bare[s] = r²s'' − 2rs' + 2s` (roots {1,2},
`op_derive2.py`, `lbare_inverse.py:7`).

**(d) Matter / source coupling n → h_AB → 𝒦 → φ (φ-BLIND, native_field:74-80):**

    T^{AB} ≡ (2/√h) δS_m/δh_AB   from FS L2+L4 on n:cell→S²   (native_field:71-73)
    δS_m/δφ = 0  (φ-blind — matter enters ONLY via T^{AB} on the h-side; NEVER e^{2φ}·T on the φ-side)

Matter sources φ **only indirectly**: n shapes T^{AB} → deforms `a,bt` (shear) via (c) → 𝒦[h] via (a)
→ φ-source via (b). No direct φ-coupling anywhere.

---

## 3. Variables & discretization

| variable | meaning | discretization | provenance |
|---|---|---|---|
| `φ(r)` | longitudinal dilation | Chebyshev-Lobatto `Nr` (`cell_solver_f2d:83-96`) | reused |
| `ρ(r)` | areal-volume trace scale `√(a·bt)` | Chebyshev `Nr` | reused (was `rho`) |
| `s(r,θ)` | **traceless shear** (NEW LIVE DOF) | radial Chebyshev × SH-exact θ (`:115-139`) | new |
| `u(r,θ)=f−θ` | hopfion/winding matter deviation | SH-exact θ; **FIXED profile in pilot** | reused/frozen |
| `L=r_s−r_c` | cell length (free boundary) | Newton unknown | reused |

- **Shear θ-content:** pilot uses the **ℓ=2, m=0** axisymmetric mode `s(r,θ)=a₂(r)·P₂(cosθ)` (the
  leading roundness-breaking mode; the op_derive2 diag(a,bt) split at ℓ=2). Represent as the single
  radial profile `a₂(r)`; higher ℓ deferred (blind-spot, §6/§7). The full nonlinear `s(r,θ)` field is
  the production DOF; the pilot's single-mode restriction is a SCOPED regime (flagged, not a verdict).
- **Hopfion source (chose-or-derived: FROZEN in pilot — ledgered):** matter `n` is φ-blind and already
  H3-converged (`fs_hopfion.py`); the pilot feeds its extracted transverse stress `T^{AB}(r,θ)` as a
  FIXED profile (`extract_stress_rtheta.py`). **This freezes an already-solved DOF** to isolate the
  geometry-shear closure — legitimate for the STRUCTURAL yes/no, NOT the final verdict; the full N5d
  co-relaxes `n`. Tagged as a scoped pilot simplification (no-shortcuts: a frozen DOF is a flag, here
  ledgered + justified because the frozen field is independently solved).
- **Solver method:** monolithic residual `[φ-ODE; ρ-ODE; shear-EL; f-PDE(frozen); all BCs; H=0]`, dense
  Levenberg–Marquardt with jacrev Jacobian (`cell_solver_f2d:299-339`) — Category-A (conditioning), NOT
  operator-split (the φ↔ρ↔s coupling through e^{±2φ} and 𝒦 is stiff).
- **How `L_bare⁻¹` enters:** the certified `lbare_inverse.py:60` BVP inverse is used **two ways, both
  Category-A / cross-checks — never as the physics operator inside the residual** (the residual keeps
  𝒦 and e^{−2φ} EXACT): (1) as a PRECONDITIONER / initial guess for the shear block (the linear-response
  shear to a given T^{AB}); (2) as the independent **mechanism-(ii) eigenproblem** operator (the TT
  tensor eigen-index, §5/§6). The buggy `n4rev_pipeline_GREENBUG.py::green_response` is NOT used (§10).

---

## 4. Boundary conditions (ONE cosmic cell [r_c, r_s]; ρ=r is round-only; NO private wall)

Whole-cell, per `universe_cell_fold_jc_sigma_results.md` + `seal_matching_junction_results.md`. Even
core at `r_c`, odd flux seal at `r_s`. Hopfion = CONTENT, not walled in a private cell/seal.

| field | even core `r_c` | odd flux seal `r_s` |
|---|---|---|
| `φ` | `φ'(r_c)=0` (Neumann), `φ_c` FREE | `φ(r_s)=0` (Dirichlet), `φ'(r_s)` **FREE ⇒ OUTPUT q** |
| `ρ` | `ρ'(r_c)=0`, `ρ_c` FREE | `ρ'(r_s)=0` |
| `s` (shear) | `s'(r_c)=0` (even fold ⇒ shear even) | **PROVISIONAL/CHOSE — see below** |
| `u` (matter) | `u_r(r_c)=0` (mirror) | `u_r(r_s)=0` (mirror) |
| `L` | — | closure row `H(r_s)=0` (`cell_solver_f2d:273`) |

Sources: even fold pins `φ'(r_c)=ρ'(r_c)=0`, values free (`universe_cell_fold:38`); odd fold pins
`φ(r_s)=0`, `ρ'(r_s)=0`, `φ'(r_s)` genuinely FREE ⇒ `q=Z_φ ρ_s² φ'(r_s)` an OUTPUT
(`universe_cell_fold:29`; seal Class B `seal_matching:53-56`).

**The shear seal BC is the ONE load-bearing FREE modeling input (chose-or-derived: CHOSE, provisional).**
Two admissible options, and the pin-vs-continuum answer may DEPEND on it — so the pilot must run BOTH
and report the dependence (whole-before-slice; no single-corner verdict):
- **(S-Dir)** Dirichlet shear pinned to the mirror value `s(r_s)=s_mirror` (closed-cell Class-A fold).
- **(S-JC2)** transverse-momentum continuity `[π^{AB}]=0` (source-free JC2, `seal_matching:34-40`;
  H4_N1:32) — a Neumann-type condition on the shear momentum.
This BC is the exact analogue of the seal Class-A/Class-B fork (`seal_matching:49-64`) for the shear
sector; it is a physics/canon call (Charles holds), NOT adjudicated here.

---

## 5. Conserved / readout quantities

- **Public charge / MS mass:** `q = Z_φ ρ_s² φ'(r_s) = M` (Misner–Sharp mass = cell public charge;
  `universe_cell_fold:29`, seal JC1 `seal_matching:14-27`). **NOT `q ∝ Q_H`** (an import — forbidden).
- **δq the hopfion induces:** the change in `q` between the vacuum (shear off, `s≡0`) and the
  shear-on hopfion-sourced solve — the CF1 far-field monopole (H4_N1:63-68). δq≠0 ⇒ the off-round
  source produces a net mass; δq=0 ⇒ it cancels.
- **Flux / Gauss budget (consistency, not a closure):** `q²/(2Z_φρ_s²) = E_m(r_c) − E_m(r_s)`
  (`universe_cell_fold:50-51`) — the seal flux paid by the matter Legendre-energy drop core→CMB.
- **Radial Hamiltonian closure `H(r)`** (`cell_solver_f2d:230-239`, `:38-40`): conserved on-shell,
  `=0` for a closed Class-A cell; the seal value is the closure row.
- **Branch-label candidates** (criterion-8, the "catalog" — LABELS, read out, never imposed): (1) φ
  radial node count; (2) turning-point count of the shear-modified reduced radial potential (mechanism
  (i)); (3) shear-mode eigen-index of the L_bare-based TT eigenproblem (mechanism (ii)).
- **Derrick identity** `S_a==S_b` (`cell_solver_f2d:242-255`) — per-solution consistency diagnostic.

---

## 6. Expected diagnostics — what ANSWERS the yes/no

**Primary structural outputs:**
1. **Does the shear open a well / turning points?** Evaluate the reduced radial φ-source `∫√h 𝒦 dθ`
   and the effective potential once `a'bt'` goes sign-varying (mechanism (i)). Report: does a turning
   point / potential well appear that the round (monotone-runaway, node-count≡0) equation lacked
   (`native_readout_map_depth_size_results.md`, Node A)?
2. **Is the closure discrete or continuum?** Sweep ξ (and the scale) and ask whether a closed cell
   (`H(r_s)=0` with the shear seal BC satisfied) exists at a DISCRETE set of `(ρ_s/ρ_c, node-count)` or
   over a CONTINUUM. Continuum ⇒ shear does not pin; a discrete admissible set ⇒ it pins.
3. **Is ξ pinned or free?** Whether a solution exists only at isolated ξ (pinned) or for an interval
   (free family — the N5-arc PARKED status, LIVE ★).
4. **Mechanism-(ii) eigen-index:** the TT `h_AB` eigenproblem via `lbare_inverse` — count decaying/
   discrete modes (round has none: roots {1,2}, both growing ⇒ no localized halo; a shear-coupled shift
   could change this).
- **Both S-Dir and S-JC2 seal BCs reported** (§4) — the answer's dependence on the shear seal choice is
  itself a first-class deliverable.

**Convergence / grid (Category-A, soundness only):** Nr-refinement of q and node-count; jacrev
condition number (`cell_solver_f2d:342-347`); H(r) drift; Derrick residual; ℓ-mode truncation check
(pilot ℓ=2 only — higher-ℓ is a flagged BLIND-SPOT, criterion-4, to be widened before any verdict).

---

## 7. Preflight tests BEFORE any pilot (must all pass; recorded before the run)

**The 7-gate preflight** (re-run each; a RED gate BLOCKS the pilot):
1. **Exact operator** — φ-source `−2√h 𝒦` and E^{AB} match H4_N1:19-46 verbatim (no GR G=8πT).
2. **Correct sign / source** — 𝒦=−2det(K^A_B); round source `+4e^{−2φ}` sign (native_field:119).
3. **No archived wrong-operator** — no import of `branch_operator.py` / `p1_residual` / `branchGP` /
   `green_response` (grep the module; §10).
4. **No private cell / seal** — ONE [r_c,r_s]; hopfion is content (not a walled particle cell).
5. **e^{−2φ} EXACT** — no Taylor/linearization of e^{−2φ} anywhere in the residual (grep).
6. **L_bare⁻¹ verified** — `python3 h4_scripts/lbare_inverse.py` all PASS. **RE-RUN 2026-07-06: PASS**
   (indicial {1,2}; L@L⁻¹−I=1.2e−13; 2nd-order convergence; GREENBUG residual 1.06e3 confirmed wrong).
7. **Variables / BCs locked** — the §3/§4 tables committed before the run (pre-registration).

**Unit tests of each assembled piece:**
- **Round-limit recovery** — with `s≡0` (shear frozen off) the N5d residual == `cell_solver_f2d`
  residual to machine precision (`tests/test_n5d_roundlimit.py`). **Smoke test of the base solver
  RE-RUN 2026-07-06: assembles + one LM step decreases Φ** (bounded Nr=8,Nth=8 — unchanged by design).
- **`L_bare⁻¹` identity** — `L@L⁻¹=I`, analytic `r`,`r²` null modes, r³/r²ln r forcing (already in
  `lbare_inverse._tests`; PASS above).
- **𝒦[h] round reduction** — `𝒦̂[a=bt=r²] = −2/r²` ⇒ source `4e^{−2φ}`. **CAS-VERIFIED 2026-07-06 in
  this plan's preflight** (`𝒦=−½e^{−2φ}(a'bt')/(ab)`, round `−2e^{−2φ}/r²`).
- **Source target-scalar & φ-blind** — `δS_m/δφ=0` on the extracted T^{AB}; T^{AB} invariant under
  target-SO(3) (consistency with `no_selector_audit_results.md`).
- **Purity harness** — `python3 -m pytest tests/` GREEN (P1 liveness/provenance/limit-recovery/native-
  object; P2 operator==EL of `solver_action.py` with the shear row added).

---

## 8. Coarse pilot configuration (DEFINE only — do NOT run)

- Grid: **Nr = 16**, **Nth = 8** (SH-exact GL-μ). **ℓ = 2 shear only** (single `a₂(r)`).
- Source: FROZEN hopfion T^{AB} from `extract_stress_rtheta.py` / `stress_profiles.npz`.
- Iter caps: LM `maxit ≤ 30`, inner damping tries ≤ 30, `time_budget = 100 s`, `tol = 1e-12`.
- Continuation: homotopy in the **shear amplitude** (0 → target, so the round solve is the ξ=continuation
  seed) AND, separately, a coarse sweep in **ξ** (the probed family) at fixed κ — both Category-A.
- Seal-BC: run BOTH **S-Dir** and **S-JC2** (§4) — two runs.
- Single FOREGROUND process, hard OS timeout, write straight to a results file.
- **Exact command that WOULD be run (NOT executed here):**

      timeout 700 python3 cell_solver_f2d.py --n5d --Nr 16 --Nth 8 --lmax 2 \
          --source frozen_hopfion --sealbc S-Dir --maxit 30 --budget 100 \
          > n5d_pilot_SDir.out 2>&1

  (then a second run with `--sealbc S-JC2`). If a run would exceed budget: REDUCE Nr to 12 and report
  "throughput-limited", never extend the wall.

---

## 9. Explicit anti-hang limits (binding operational rule)

- BOUNDED grid: `Nr ≤ 16` (pilot), never above 24; `Nth = 8`.
- CAPPED iters: LM `maxit ≤ 30`, hard `time_budget ≤ 100 s` inside + OS `timeout 700` outside.
- ONE clean process at a time; **NEVER concurrent** (GPU/CPU contention stalls everything).
- **FOREGROUND with a hard OS timeout; NEVER background-poll a solve** (six+ agents hung this way).
- Write straight to a file (`> file 2>&1`); **no `| grep`/pipe** (block-buffers → no live progress).
- No `nohup`, no `&`.
- If a solve would exceed budget: **REDUCE (Nr→12) and report "throughput-limited"** — a bounded honest
  partial beats a hang; never blend a field toward a chosen endpoint and call it dynamics.

---

## 10. Old-frame contamination risks + the guard for each

| # | Contamination risk | Guard / check |
|---|---|---|
| 1 | Import the fenced scalar-tensor operator `branch_operator.py` (PRESENT in repo) | preflight gate-3 greps the N5d module for `branch_operator`/`import branch`; the round-limit unit test (§7) would diverge from `cell_solver_f2d` if a foreign operator crept in |
| 2 | Reuse `prototype/branchGP_native_s2_coupled_OBSERVE.py` (fenced, wrong frame — LIVE: "Do NOT run branchGP for N5d") | never referenced; only `cell_solver_f2d` is extended; gate-3 grep |
| 3 | Mine the OPERATOR (not just METHOD) from `p1_residual_general_einstein.py` (PRESENT) | `cell_solver_f2d` already mines only the LM METHOD (`:64`); gate-1 checks the operator == H4_N1; P2 harness checks operator==EL of `solver_action.py` |
| 4 | Direct `e^{2φ}·T` / `a(φ)` matter weight on the φ-side (the retired "dilaton-runaway basin A" coupling) | matter enters ONLY as T^{AB} on the h-side; `δS_m/δφ=0` unit test (§7); grep the residual for `e2p*` on the φ-ODE row (φ-ODE `:221` must have NO matter term) |
| 5 | The X=−2e5 kluge (a Cassini KLUGE mis-tagged FREE) | N5d has NO X parameter (the round solver `cell_solver_f2d` already has none); grep for `X`/`-2e5`/`-200000` → must be absent |
| 6 | Private [core,seal] wall + Dirichlet particle BC (frame C(b)) | §4 BC table pre-registered: ONE cosmic cell, hopfion=content; gate-4; no second seal/Dirichlet on a matter sub-domain |
| 7 | Buggy `n4rev_pipeline_GREENBUG.py::green_response` for the transverse response | use ONLY `lbare_inverse.py:60`; gate-6 (its test proves green_response residual 1.06e3 ≠ 0); grep for `green_response` → absent |
| 8 | Linearized e^{−2φ} used as a result/input | e^{−2φ} via `torch.exp(-2*phi)` EXACT (`cell_solver_f2d:220`); gate-5 grep for any Taylor/`1-2*phi` on the exponential |
| 9 | Impose `q ∝ Q_H` (import an areal/topological charge law) | q is COMPUTED as `Z_φρ_s²φ'(r_s)` (§5); Q_H used only as a topological label of the frozen source, never wired into q; code review of the readout |
| 10 | Assumed-Einstein `G = 8πT` (the Principle-7 scar) | E^{AB} comes from varying the NATIVE action (H4_N1:96-99); `G=8πT` never written; P2 harness (operator==native EL) |
| 11 | Smuggle a MERIT filter (demand a lump/well/the expected size) into a "diagnostic" | diagnostics CHARACTERIZE (report node/turning-point counts, q, closure set) — they never FILTER on shape; `tests/test_solution_space_gate.py` (provenance/honesty only, never merit) |
| 12 | Freeze the shear (revert to round) and call the continuum result an N5d verdict | the shear `s` is a LIVE residual row with its own EL + BC; the round-limit test is a CHECK, not the run; criterion-9/§6 require the shear-on solve |

---

## Regime-of-validity stamp (criterion 10) & completeness (this is ONE tile)

**Covered:** static, Branch P, block-diagonal (g_rA=0), φ longitudinal, ℓ=2 axisymmetric shear, frozen
hopfion source, whole cosmic cell. **DROPPED / blind-spots (must widen before any verdict):** higher-ℓ
shear (criterion-4); radial shift g_rA≠0 and φ=φ(r,x) angular dependence (H4_N1 scope caveat :86-90);
co-relaxed (unfrozen) matter; off-diagonal h_θψ; time-live sector (criterion-7). The pilot answers the
STRUCTURAL yes/no for the ℓ=2 frozen-source corner ONLY; a continuum there is scoped to that corner
(solver-first: a frozen higher-ℓ DOF is "one more thing", not a metric verdict), and a pin there is a
LEAD to verify at higher ℓ + unfrozen source before banking. Every result is PROVISIONAL until the
verifier-before-record pass.

## Premise ledger (chose-or-derived — every FREE physics constant this solver rides)
| item | tag |
|---|---|
| ξ (Skyrme L2 coupling) | **FREE — the probed family** (N5 PARKED; the thing N5d tests) |
| κ (L4 coupling) | **FREE-units** (κ/ξ sets absolute scale; ratios are observables) |
| Z_φ | **FREE** (Route-A) or **=8** (Route-B — carries the open no-mixing-term tension, `universe_cell_fold:71`) |
| φ_c, ρ_c (core values) | **FREE** (even-fold values free, `universe_cell_fold:38`); φ_c=−ln(1101) ONLY if the CMB anchor is imposed (kept FREE for the structural yes/no) |
| r_c | **CHOSE** length label (EOMs autonomous ⇒ only L=r_s−r_c physical, `cell_solver_f2d:34`) |
| r_s, q, φ'(r_s) | **OUTPUTS** (q=Z_φρ_s²φ'(r_s)) |
| N / Q_H (winding / Hopf charge) | **DERIVED-topological** integer (label of the frozen source) |
| shear seal BC (S-Dir vs S-JC2) | **CHOSE — provisional**, load-bearing; BOTH run, dependence reported |
| ℓ=2-only, frozen source | **SCOPED pilot simplification** (ledgered; not the verdict) |

**Interrogation tag:** this push is **METRIC-LED** ("what does the derived off-round shear DOF do to the
closure?") — not template-led. It observes what the unfrozen shear produces; it does not target a mass
or a lump.
