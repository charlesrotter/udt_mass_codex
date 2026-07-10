# Thread B — f2d drain: MIRROR vs WR-L WALL seal (static)

## HYGIENE HEADER

| Field | Value |
|-------|--------|
| **Date** | 2026-07-10 |
| **Mode** | OBSERVE (solver-first — test whether the drain is an artifact of the finite-mirror closure: the `f_r=0` matter channel and/or the free-boundary `L` under `H=0`) |
| **Slice scope** | STATIC, diagonal, Branch-P (W=1) finite cell (φ,ρ,f), round. Z=8, ξ=κ=1. The ONE DOF varied vs the banked runs = the OUTER (r_s) **seal**, along two INDEPENDENT knobs: (a) φ-seal `mirror` (φ′=0) vs **WR-L wall** (φ(r_s)=φ_wall, φ′ FREE; A=e^{−2φ_wall}→0 character, macro A=1−r/X NOT imposed inside); (b) matter-seal `mirror` (f_r=0) vs **open** (natural PDE at seal, imposes no shape). Core (r_c) always even mirror fold. Grid (Nr,Nθ)∈{(16,8),(24,8)}. No prescribed I_r, no new coupling, no hard Dirichlet edge. |
| **Observing or targeting?** | OBSERVING. I_r, L, Q, q_raw, ‖F‖², φ endpoints are CHARACTERIZERS (measured, not filters). The open matter seal is non-imposing (does NOT demand structure = not a merit filter). A_wall is swept, NOT tuned to a target I_r. No lump/mass/particle targeted. |
| **Verifier status** | Self-checked bounded GPU (V100) pilots; base residual byte-identical to the mirror system when seal=None (`max|F_seal=None − F_base| = 0`, verified); all arms square/finite. Control arm A reproduces the prior banked drain table to 3 sig-figs (L=0.0144, I_r=4.6e-6 at Nr=16/it120). **Independent blind verifier: see §7** (run before banking). |
| **Build-on grade** | **CONDITIONAL** (scoped negative). The drain SURVIVES the mirror-vs-wall seal across both knobs, α, N, and grid. Recorded as a clean failure of the seal/closure DOF; do NOT bank as a metric verdict, do NOT patch, do NOT claim a closed cell. |
| **Re-run commands** | `PYTHONPATH=$(pwd) python3 scratchpad/run_f2d_mirror_vs_wall.py` (full matrix, ~20s). Solver seal knob: `cell_solver_f2d.residual(..., seal=dict(phi="wall"\|"mirror", phi_wall=…, matter="open"\|"mirror"))`. `python3 -m pytest tests/ -q` (69 pass, 1 xfail, 1 pre-existing unrelated hygiene-header doc-backlog fail). |

### Premise ledger

| Item | Tag |
|------|-----|
| Static, diagonal, Branch-P (W=1), round cell | **SCOPE** (inherited) |
| WR-L wall CHARACTER (A→0 depth, φ′ free) borrowed as the φ-seal | **THEORY-motivated** (C-2026-07-09-1) — macro solution A=1−r/X NOT imposed inside the cell; character only |
| A_wall ∈ {0.3, 0.1} → φ_wall = −½ln A_wall ∈ {0.602, 1.151} | **CHOSE** — swept to characterize, NOT tuned to a target I_r |
| Open matter seal (natural PDE at seal replacing f_r=0) | **CHOSE-BC** — non-imposing (imposes no shape; not a merit filter) |
| Z=8 | **CHOSE-fixed** |
| ξ=κ=1 | **CHOSE-units** (ratios observable) |
| N∈{1,2} winding degree | **DERIVED-topological**, swept |
| α∈{0,−1,−2}; ASRC_C=−0.5 | α **CHOSE** (frozen); ASRC_C **anchor-verified** (−α/2) |
| Grid (Nr,Nθ), maxit, LM damping | **WORKING** (category-A conditioning; soundness only) |

---

## 1. What was tested

Per the dispatch `threadB_WORKSTATION_DISPATCH_mirror_vs_wall.md` and the solver-first MAP
(`threadB_f2d_drain_solver_first_MAP.md` §1.3), the ONE untested left-out DOF after non-round + topology
(both drained, `threadB_f2d_nonround_topological_audit_results.md`) is the **mirror-vs-wall closure**.
The audit motivation: the finite-mirror seal `f_r(r_s)=0` is exactly the condition the drained state
satisfies for free (a **drain channel**), and `H=0` is "too quiet" — once matter drains it is trivially
satisfied so nothing pins `L`. The WR-L wall was proposed to (i) close the `f_r=0` channel and (ii) pin `L`.

**Whole-before-slice**: the two seal knobs were varied INDEPENDENTLY so the effect of each is isolated:

| Arm | φ-seal | matter-seal | isolates |
|-----|--------|-------------|----------|
| **A** | mirror φ′(r_s)=0 | mirror f_r=0 | control (expect drain) |
| **B1** | **WALL** φ(r_s)=φ_wall, φ′ free | mirror f_r=0 | does L-pin-by-wall-depth alone stop it? |
| **B2** | mirror | **OPEN** natural PDE seal | does removing the f_r=0 channel alone stop it? |
| **B3** | **WALL** | **OPEN** | the intended Arm B |

### ⚠ Obstruction flagged in the MAP (before the run), now confirmed

The WR-L wall is a **geometry (φ) wall**, but in the Branch-P native frame the matter radial channel is
**φ-blind** (undilated). So a geometric wall on φ **cannot by construction reach the φ-blind matter radial
drain**, and a constant φ≡φ_wall would satisfy the wall depth trivially. A "pure WR-L geometric wall"
therefore does not express as a matter-drain blocker on these variables. The run confirms this precisely
(§2, §3): on any BOUNDED cell the wall arms cannot reach the wall depth (the depth is satisfiable only on
the drained L→∞ delocalization branch).

---

## 2. Results table

Solve endpoints (bounded GPU LM, one process). `phi=[c,s]` = φ at core and seal; `q_raw`=Z ρ_s² φ′(r_s).

| tag | arm | N | (Nr,Nθ) | it | α | A_wall | final ‖F‖² | L | I_r mean/max | Q[min,max] | φ[c,s] | q_raw |
|-----|-----|---|---------|----|----|--------|-----------|---|--------------|------------|--------|-------|
| A_it40        | A  | 1 | (16,8) | 40  | 0  | —    | 6.80e-3 | 0.1122 | 2.94e-4 / 2.97e-4 | [1.000,1.000] | [−0.003,−0.003] | +9.8e-5 |
| A_it120       | A  | 1 | (16,8) | 120 | 0  | —    | 1.32e-4 | 0.0144 | 4.62e-6 / 4.62e-6 | [1.000,1.000] | [−0.003,−0.003] | +2.2e-7 |
| B1_w0.3_it120 | B1 | 1 | (16,8) | 120 | 0  | 0.30 | **3.16e-1** | 0.0126 | 2.94e-10 / 7.04e-10 | [1.000,1.000] | [+0.040,+0.040] | +2.8e-2 |
| B1_w0.1_it120 | B1 | 1 | (16,8) | 120 | 0  | 0.10 | **8.52e-1** | 0.0042 | 5.78e-10 / 1.51e-9 | [1.000,1.000] | [+0.229,+0.229] | +1.4e-2 |
| B2_it40       | B2 | 1 | (16,8) | 40  | 0  | —    | 3.58e-3 | 0.0844 | 3.25e-4 / 3.98e-4 | [1.000,1.000] | [−0.004,−0.004] | +4.5e-5 |
| B2_it120      | B2 | 1 | (16,8) | 120 | 0  | —    | 4.79e-5 | 0.0075 | 2.54e-6 / 3.17e-6 | [1.000,1.000] | [−0.005,−0.005] | +3.4e-8 |
| B2_am1_it120  | B2 | 1 | (16,8) | 120 | −1 | —    | 4.79e-5 | 0.0075 | 2.54e-6 / 3.17e-6 | [1.000,1.000] | [−0.005,−0.005] | +3.6e-8 |
| B2_am2_it120  | B2 | 1 | (16,8) | 120 | −2 | —    | 4.79e-5 | 0.0075 | 2.54e-6 / 3.17e-6 | [1.000,1.000] | [−0.005,−0.005] | +3.9e-8 |
| B3_w0.3_it40  | B3 | 1 | (16,8) | 40  | 0  | 0.30 | 2.81e-1 | 0.0782 | 1.90e-4 / 2.45e-4 | [1.000,1.000] | [+0.073,+0.075] | +1.2e-1 |
| B3_w0.3_it120 | B3 | 1 | (16,8) | 120 | 0  | 0.30 | **2.76e-1** | 0.0065 | 1.56e-6 / 1.99e-6 | [1.000,1.000] | [+0.077,+0.077] | +9.8e-3 |
| B3_w0.1_it120 | B3 | 1 | (16,8) | 120 | 0  | 0.10 | **8.25e-1** | 0.0047 | 4.23e-7 / 6.08e-7 | [1.000,1.000] | [+0.244,+0.244] | +1.6e-2 |
| B3_w0.3_am1   | B3 | 1 | (16,8) | 120 | −1 | 0.30 | 2.76e-1 | 0.0064 | 1.55e-6 / 1.98e-6 | [1.000,1.000] | [+0.077,+0.077] | +9.8e-3 |
| B3_w0.3_am2   | B3 | 1 | (16,8) | 120 | −2 | 0.30 | 2.75e-1 | 0.0064 | 1.51e-6 / 1.92e-6 | [1.000,1.000] | [+0.077,+0.077] | +9.7e-3 |
| B3_w0.3_Nr24  | B3 | 1 | (24,8) | 120 | 0  | 0.30 | 2.77e-1 | 0.0090 | 3.03e-6 / 3.87e-6 | [1.000,1.000] | [+0.076,+0.076] | +1.4e-2 |
| B3_w0.3_N2    | B3 | 2 | (16,8) | 120 | 0  | 0.30 | 1.03e+0 | 3.5911 | 3.48e-2 / 1.25e-1 | [1.954,2.009] | [−0.094,+0.176] | +7.2e-1 |

---

## 3. What survived / what failed

**The drain SURVIVES the mirror-vs-wall seal. Two clean, independent findings:**

1. **The `f_r=0` mirror was NOT the drain channel.** B2 (open matter seal, φ-mirror kept) is a
   *converged* solve (‖F‖²=4.8e-5) whose I_r drains **monotonically with convergence** (it40→it120:
   3.25e-4 → 2.54e-6), identical to the control A drain (4.62e-6). Replacing the suspected `f_r=0`
   drain channel with a **non-imposing natural/open seal changes nothing** — the drain is **intrinsic
   to the static matter minimizer**, not a boundary artifact of the mirror fold. α<0 (B2_am1/am2) is
   bit-identical to α=0: once I_r→0 the α-source ∝ I_r vanishes with it (consistent with the banked runs).

2. **The WR-L geometric wall is held by NO BOUNDED CELL** — it is satisfiable only on the L-degenerate,
   delocalized (L→∞) branch, where matter has drained regardless. (Corrected from an earlier overstatement
   — see verifier §7.) From the **physical / collapse branch** (default seed, L→0) the wall depth is
   MISSED: B1/B3 stall with ‖F‖² ≈ 0.28 (A_wall=0.3) / 0.85 (A_wall=0.1), flat across it40→it120, α, and
   Nr (16→24), and Phi ≈ 0.276 = exactly (φ_wall − φ_s)² = (0.602 − 0.077)² — the solver satisfies **every
   row except the wall-depth row**. Mechanism: the φ-climb is sourced only by ρ′² (φ″ = 4e^{−2φ}ρ′²/(Zρ²)
   − 2φ′ρ′/ρ); when the matter drains ρ flattens, so φ cannot climb to the wall depth *at bounded L*.
   From a warm seed placed AT the wall depth, the wall row IS satisfiable to machine precision
   (‖F‖²=7e-14, φ_s=0.602 exact) — but **only on a runaway branch: L≈4×10⁹, I_r≈4×10⁻¹⁷** (fully drained),
   with the Jacobian null-vector loading on L (the known "L undetermined" gauge degeneracy). So the wall
   and the drain are the same failure at bounded L: no sustained radial matter structure ⇒ no φ-gradient
   ⇒ no wall on any bounded cell; the only wall-reaching state is the drained L→∞ delocalization. Where the
   solver drives I_r down during the (stalled) collapse-branch attempt, it drains anyway (B3: 1.9e-4→1.6e-6).

3. **L still degenerate; topology still intact.** Q pins to N machine-exactly (N=1→1.000, N=2→2.000)
   in every arm — the winding sector is orthogonal to the drain, as in the prior audit. Once matter
   drains, L is unconstrained: collapses (N=1: L~0.006) or runs away (N=2: L=3.59). The wall depth did
   NOT pin L, because the wall itself cannot be reached (finding 2).

**Convergence-axis verdict (the banking gate):** in the *converged* arms (A, B2), driving ‖F‖² down
drives I_r further down monotonically — the nonzero I_r at it40 is an under-converged snapshot, not a
solution. In the *wall* arms (B1, B3) the solve does not converge at all (obstruction). Neither route
sustains I_r. **The drain survives the mirror-vs-wall seal.** Nothing here is banked as a nonzero cell.

---

## 4. Solver-first accounting (mismatch → solver, not mechanism)

This job was itself a solver-completeness step (a left-out DOF: the seal/closure). It is now tested:

- **Left out?** The seal DOF (mirror vs wall) and the matter-channel BC (f_r=0 vs open) are now BOTH
  exercised. Neither sustains I_r.
- **Numeric?** The B2 drain is converged (‖F‖²~5e-5, monotone under maxit and stable under Nr). The
  B1/B3 non-convergence is a *characterized structural over-constraint* (Phi = the single wall-depth
  residual), not a conditioning failure — it is stable across grid and iteration.
- **Frozen DOF?** No DOF was frozen here beyond the inherited static/diagonal/round scope.
- **Whole space with everything on?** Within the STATIC sector: seal, matter-BC, α, N, grid all swept.
  The one remaining untested left-out DOF is **time-live / nonstatic** (MAP DOF 1, highest priority).

Per the pre-registered logic: **drain survives the wall seal ⇒ scoped FAILURE of this DOF ⇒ next =
time-live eigenmode** (a non-static perturbation/eigenmode about the drained solution — does any mode
with nonzero I_r restore?). No mechanism is added; time-live is a metric-completeness (Category-A) DOF.
This rhymes with the macro lesson (`simple_metric_timelive_residual_appearance_MAP.md`): static L is a
regime chart; the residual/appearance structure lives in the time-live sector.

---

## 5. Seal implementation note (what BC rows changed; CHOSE vs THEORY)

Implemented in `cell_solver_f2d.residual(..., seal=None)` (base byte-identical when seal is None/empty):
- **φ-seal `wall`** (CHOSE value, THEORY-motivated character): the outer φ-Neumann row φ′(r_s)=0 is
  replaced by the Dirichlet **depth** row φ(r_s) − φ_wall = 0 with φ′(r_s) FREE (⇒ q_raw a live output).
  φ_wall = −½ln A_wall. The core row stays φ′(r_c)=0 (even fold). One-for-one row swap ⇒ system square.
- **matter-seal `open`** (CHOSE-BC, non-imposing): the outer matter mirror row f_r(r_s)=0 is replaced by
  the f-PDE residual evaluated at the seal row (natural/outflow BC). Nθ-for-Nθ swap ⇒ system square.
  This imposes NO shape (not a merit filter); it removes the f_r=0 condition without demanding structure.
- **H=0** closure and all interior ODE/PDE rows unchanged. No new coupling, no hard Dirichlet edge, no
  prescribed I_r. The macro WR-L solution A=1−r/X is NOT imposed inside — only the wall CHARACTER (A→0
  depth, φ′ free) is borrowed.

---

## 6. NOT claimed

- NOT: a self-consistent cell with sustained I_r>0 (every converged arm drains; the wall arms do not
  converge and drain during the attempt).
- NOT: that the mirror `f_r=0` was the drain cause (the non-imposing open seal drains identically).
- NOT: that the WR-L wall stops the drain (no bounded cell holds the wall; the only wall-reaching state
  is the drained L→∞ delocalization — the wall and the drain are the same missing-radial-structure failure).
- NOT: that L is pinned by the wall (on the bounded/collapse branch the wall depth is missed and L
  collapses; on the wall-reaching branch L runs away to ~4×10⁹ — L stays degenerate either way).
- NOT: a metric verdict. This is a scoped negative on the seal/closure DOF of the static Branch-P cell;
  the **time-live / nonstatic** DOF is UNTESTED and is the pre-registered next step.
- NOT: any mass, ratio, particle, SNe, or cosmology result. No dS. No prescribed I_r. No mechanism.

---

## 7. Verifier status — DONE (blind adversarial, agent aae6f904119d7ddb7, 2026-07-10)

Independent zero-context adversarial pass, framed to ADJUDICATE (not confirm), own bounded solves:
- **Q1 base integrity — CONFIRMED.** seal=None / {} / dict(phi="mirror",matter="mirror") byte-identical
  to the original mirror system (`torch.equal`=True, incl. the α=−1 source-on path). Control valid.
- **Q2 open-seal drain REAL — CONFIRMED.** I_r drains monotonically as ‖F‖² falls (maxit 40→250:
  I_r 3.25e-4→1.8e-7; random-kick seed reaches ‖F‖²=1e-7, I_r=2.7e-9). Adversarial "open seal secretly
  pins f_r≈0" RULED OUT: f_r@seal ≈ f_r@interior at every maxit (channel genuinely removed). Finite I_r
  appears ONLY at non-converged points.
- **Q3 wall obstruction — CONFIRMED, with an OVERSTATEMENT flagged and now corrected.** The identity
  ‖F‖²≈(φ_wall−φ_s)² is confirmed on the collapse branch (dominated by the single wall-depth row, stable
  across lam0∈{1e-1,1e-3,1e-6} and maxit — not under-iteration). BUT a warm seed reaches the wall depth
  exactly (‖F‖²=7e-14, φ_s=0.602) on a **runaway L≈4×10⁹, I_r≈4×10⁻¹⁷** branch (Jacobian null-vector on
  L). Correct statement (now in Finding 2): *no bounded cell holds the wall; the wall is reachable only
  in the drained L→∞ limit* — NOT "physically unreachable."
- **Overall: headline SUPPORTED** — the I_r drain survives the mirror-vs-wall seal across every arm,
  seed, and branch (converged collapse, non-converged stall, wall-reaching runaway); I_r→0 (1e-9…1e-17)
  everywhere. All table numbers (A, B2, B1, B3) reproduced to full precision. Verifier scratch:
  `scratchpad/verify_q1.py … verify_q3e.py`.
