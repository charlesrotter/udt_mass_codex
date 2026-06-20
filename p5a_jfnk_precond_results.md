# P5a — JFNK PHYSICS-BASED PRECONDITIONER PROTOTYPE (the de-risk crux)

Research record (append-never-edit). **NOT canon.** Mode: OBSERVE/INFRA (a solver
de-risk, no physics claim). **DATA-BLIND** (units L=1; no wall numbers). Driver:
claude-opus-4-8[1m]. Date: 2026-06-20. Branch: `p5a-jfnk-precond`. NEW FILES ONLY
(committed scripts are immutable).
Parent frame: `p5_solver_survey_results.md` (#1 = JFNK + physics PC) +
`EVERYTHING_ON_SOLVER_P5_MAP.md`. Gate anchor: `full3d_newton.py` (dense Newton,
~1e-13). Stall to beat: `full3d_catalog_results.md` #60 (matrix-free Jacobi-PCG LM
stalls off-round ~1e-5).

## VERDICT (up front, honest)

**P5a FAILS the gates.** A Jacobian-Free Newton-Krylov solve with the physics-based
preconditioners attempted here does **NOT** reach the dense-Newton anchor floor and
does **NOT** beat the #60 stall to floor. Both GATE 1 (anchor reproduction) and GATE 2
(beat the #60 stall) FAIL. **This triggers the KEH/Hachisu SCF fallback (#2 in the
survey) — Charles's call.** No convergence was faked; no gate was tuned away.

The de-risk did its job: it surfaced — cheaply, before the multi-week P5 build — that
the #1-ranked method's load-bearing component (a tractable physics PC) does not work
on this operator for the reason diagnosed below. That is a first-class result.

---

## 1. WHAT WAS BUILT

`p5a_jfnk_precond.py` (new, committed):
- **Matrix-free Jacobian operators** `make_jac_ops`: `JT(w)=J^T w` and `JV(v)=J v` via
  the double-backward autograd trick (reused verbatim from `full3d_solver.lm_step`),
  differentiating the **committed** residual `full3d_solver.residual_vector` (the same
  residual the anchor uses; no hand-coded linearization, no dropped term).
- **JFNK outer loops** (Newton + matrix-free inner Krylov; NO dense Jacobian ever built):
  - `jfnk_solve` (PCG on the Gauss-Newton normal operator `J^T J + lam I`) — the exact
    #60 inner structure, with the preconditioner swappable: `none` / `jacobi` (the #60
    control) / `radial` / `radial+col` / `radial_col` (the physics PCs).
  - `jfnk_lsmr_solve` (matrix-free **damped LSMR** on the rectangular `J` directly — the
    matrix-free analogue of the anchor's `torch.linalg.lstsq` step), right-PC
    `none` / `fieldblock`.
- **Physics-based preconditioners attempted** (the NEW component, the one #60 got wrong):
  1. `radial` — per-field **angle-averaged** radial-elliptic block inverse `(L_f+mu I)^{-1}`
     (attacks the steep-core radial conditioning), measured directly from the JVP.
  2. `radial_col` — per-field **per-(theta,psi)-column** radial-elliptic block inverse
     (preserves angular structure).
  3. `fieldblock` — physics-based per-field diagonal scaling `1/sqrt(diag J^T J)`
     (normalizes heterogeneous field-block magnitudes), Hutchinson-estimated.
  4. (diagnostic) full per-field **dense** block inverse — the strongest block PC.
- `axi_l2_seed` — the documented #60 stall seed (axisymmetric l=2 Θ perturbation,
  amp=0.25), built from the committed `full3d_campaign.perturb('axi_l2')` recipe.

Gate harnesses (new, committed): `p5a_gate1.py`, `p5a_gate2.py`, `p5a_gates.py`.

---

## 2. GATE 1 — ANCHOR REPRODUCTION + PC-INDEPENDENCE  → **FAIL**

Shared small case the dense anchor can solve: round seed, grid (Nr,Nth,Nps)=(16,6,8),
p=0.4, kap8=0.05, m=1. nU=3840, nF=4224.

| solver | final Phi | reaches anchor floor? |
|--------|-----------|------------------------|
| **dense Newton ANCHOR** | **3.76e-11** (25 iters, 290 s) | reference |
| JFNK-LSMR [pc=none] | 9.08e-06 (22 iters, 369 s) | **NO** (~5 orders short) |
| JFNK-LSMR [pc=fieldblock] | 4.34e-05 (16 iters, 285 s) | **NO** |

Field-by-field vs the anchor solution (max|diff| over a,b,c,d,Θ):
- [none]       a=3.4e-2 b=5.1e-2 c=2.7e-2 d=3.0e-2 Θ=1.5e-2  — **does NOT match the anchor**
- [fieldblock] a=3.6e-1 b=1.1e0  c=1.8e-1 d=1.7e-1 Θ=3.2e-1  — does NOT match

PC-independence (none vs fieldblock): max|diff| ~1.1 — the two PCs give **different**
results, but ONLY because neither converged; the PC-independence test is meaningful
only at the shared fixed point, which was not reached. **No valid PC-independence
claim can be made** (and the fixed-point-preservation guard is therefore unverified by
convergence — though it is preserved in principle: a right-PC `du=P y` cannot move the
zero set; the failure is convergence, not a wrong fixed point).

GATE 1 = **FAIL**: JFNK does not reproduce the anchor (neither floor nor fields).

---

## 3. GATE 2 — BEAT THE #60 STALL  → **FAIL**

The #60 case: axisym-l2 control seed (a KNOWN relax-to-round case), grid (16,6,8).
SEED: Phi=1.22e3, tvar=8.05e-2, psivar≈0.

| solver | final Phi | tvar | psivar | iters | time |
|--------|-----------|------|--------|-------|------|
| #60 control (Jacobi-PCG) | 1.04e-5 | 0.156 | 7.7e-2 | 24 | 87 s |
| JFNK-LSMR [pc=none]      | 1.14e-5 | 0.105 | 2.0e-8 | 16 | 231 s |

Both **plateau at ~1e-5** (the documented #60 wall), NOT the required floor (≤~1e-9).
JFNK-LSMR does NOT drive Φ to floor and the shape does NOT relax to round (tvar≈0.10,
still far from the round ~1e-3). It does scrub the spurious non-axisymmetry the Jacobi
solver developed (psivar 7.7e-2 → 2e-8) — a marginal, non-decisive improvement.

PASS criterion (Φ→floor where Jacobi stalled) is **NOT met**. GATE 2 = **FAIL**.

(The anchor on the SAME stall case reaches the floor — the relax-to-round target
exists; the failure is the matrix-free solver's, exactly as #60 reported. The anchor
cross-check on the stall case was not separately rerun here; the round-case anchor
floor 3.76e-11 + the catalog's documented axisym-relax establish the target.)

---

## 4. THE ROOT CAUSE (the diagnosis — why every physics PC failed)

Built the **dense** `J^T J` on a tiny grid (12,6,8) to inspect the operator directly:

- **`J^T J` is massively rank-deficient: 622 of 2880 eigenvalues (~22%) are numerically
  zero** (< 1e-8·λ_max). Condition number κ(J^T J) ≈ **2.3e20**.
- The near-nullspace is the **body-mask excision**: `full3d_spectral.Grid3D.body` zeroes
  3 Chebyshev edge rows at each radial end; those DOF (and the steep core/seal edges)
  appear in **no body residual row**, only weakly in the strong-BC rows → near-zero
  columns in `J`.
- Field-block structure is **benign**: diagonals are uniform (~900 across a,b,c,d,Θ),
  inter-field off-blocks are weak (O(30) vs O(900)). So the stiffness is **not**
  block-structured and **not** dominated by a steep-core radial elliptic operator that a
  radial/block inverse could capture.

Consequences (each measured):
- **CG on `J^T J`** inherits κ² → the inner solve cannot converge in the Newton tail
  (relres degrades from 2e-9 at lam=1e-3 to 1.8e-2 at lam=2e-7, even with a
  2000-iteration budget). This is the #60 stall's mechanism: not "Jacobi is the wrong
  PC" alone, but a **squared, rank-deficient** operator.
- **LSMR on `J`** (κ not κ², damping-robust to the nullspace — the matrix-free form of
  the anchor's `lstsq`) is a genuine descent direction and reduces Φ monotonically, but
  still **plateaus at ~1e-6** because the inner solve is iteration-capped by the residual
  ill-conditioning; tightening to 2000 iters does not recover the quadratic tail.
- **Every physics PC made the inner solve WORSE, not better** (relres at lam=1e-3, RHS
  `b=J^T(-F)`, round seed, 300 CG iters):
  | PC | inner relres |
  |----|--------------|
  | none | 5.0e-5 |
  | jacobi (#60) | 1.4e-4 |
  | radial (angle-avg block) | 1.7e-3 |
  | radial_col (per-column block) | 2.1e-2 |
  | full per-field dense block (tail, lam=1e-9) | 1.1e1 (vs none 9.5e-2) |
  Block/diagonal preconditioners amplify the null directions because the conditioning
  root is the **global nullspace + cross-field coupling**, not an intra-field elliptic
  block. No tractable physics PC of the surveyed kind repairs it.

**Why the anchor works and JFNK does not:** `torch.linalg.lstsq` on the augmented
`[J; sqrt(lam) I]` is a **direct, rank-revealing QR/SVD** that handles the 22% nullspace
exactly; iterative Krylov has no equivalent without a preconditioner that captures that
nullspace — which a radial/block/diagonal physics PC does not.

---

## 5. PREMISE LEDGER (chose / derived)

| Item | tag | note |
|---|---|---|
| Residual = `full3d_solver.residual_vector` verbatim | DERIVED (reused) | byte-identical to the anchor's `residual_vector_vsafe`; no term changed |
| Matrix-free JVP/VJP (double-backward) | CHOSE (numerics) | reused from `lm_step`; autograd of the SAME residual, not a hand linearization |
| LSMR inner solver (on J) | CHOSE (numerics) | matrix-free analogue of the anchor's lstsq; category-A |
| physics PCs (radial / radial_col / fieldblock) | CHOSE (numerics) | the de-risk subject; all measured from the actual JVP, none imported |
| LM damping lam, schedule | CHOSE (numerics) | standard; no tuning to a target |
| grid (16,6,8), p=0.4, kap8=0.05, m=1 | CHOSE (control) | the shared anchor-solvable case; the canonical regime |
| body-mask (3-row Cheb edge excision) | INHERITED | from `full3d_spectral`; **this is the conditioning root** (see §4) — NOT introduced here |

**Frozen DOF / gauge / BC introduced to aid convergence: NONE.** B=1/A free; matter Θ
free over (r,θ,ψ); winding/seal/depth BCs imported verbatim; no injection, no dropped
term, no linearization kept as a result. The body-mask is pre-existing (it is what
makes `J^T J` rank-deficient — flagged as the root, not a P5a choice). Box-control: no
box dependence baked into any PC (the radial PC scales with the physical operator, not
cell size R; moot, since it failed). DATA-BLIND throughout.

---

## 6. SCOPED STATUS + WHAT THE NEXT P5 SUB-STEP INHERITS

- **P5a = FAIL** for a simple physics-based preconditioner (radial-elliptic / block /
  diagonal). The #1-ranked JFNK line, in the matrix-free-Krylov form prototyped here,
  does not reach the floor on this operator. → **KEH/Hachisu SCF fallback (#2) is
  triggered, Charles's call.**
- **What the next step inherits (the real finding):** the blocker is **not** steep-core
  elliptic stiffness (the survey's hypothesis) — it is **`J^T J` rank-deficiency
  (κ~1e20, ~22% nullspace) from the body-mask edge-excision**, which only a direct
  rank-revealing factorization (the anchor) handles. Two honest forward options for
  Charles:
  1. **KEH/SCF (#2):** its integral Green's-function inversion sidesteps forming/
     inverting the stiff differential operator entirely — structurally immune to this
     nullspace. The survey's runner-up; this result promotes it.
  2. **Re-pose the discretization** so `J` is full-rank (e.g. solve only the body DOF
     with the edge rows determined by the BC/regularity relations, instead of carrying
     excised DOF that no residual constrains). This is a re-scoping of the operator, not
     a preconditioner — it would make the anchor's success transferable to a matrix-free
     Krylov solve. (Flagged for Charles; out of P5a scope.)
- The matrix-free JVP machinery + LSMR-on-J + the dense-`J^T J` diagnostic are reusable
  for whichever path is chosen.

---

## 7. ATTACK HERE (for a blind verifier)

1. **The root-cause claim (load-bearing):** rebuild dense `J^T J` on (12,6,8), confirm
   ~22% near-zero eigenvalues and κ~1e20; confirm the near-nullspace coincides with the
   `Grid3D.body`-excised Cheb edge rows. If the nullspace is NOT the body-mask, the
   diagnosis (and both forward options) must be re-derived.
2. **GATE 1 FAIL:** re-run `p5a_gate1.py` / the §2 numbers; confirm JFNK-LSMR floors at
   ~1e-5..1e-6 (not the anchor 3.8e-11) and the fields do not match the anchor.
3. **Every-PC-worse claim:** re-run the §4 inner-relres table; confirm no physics PC
   (radial / radial_col / fieldblock / full dense block) beats `none`. If ANY PC
   converges the inner solve tightly AND drives the outer Φ to floor, P5a should be
   RE-GRADED (the de-risk would flip to PASS).
4. **No smuggle:** confirm no frozen DOF / gauge / BC was added; the residual is the
   committed `full3d_solver.residual_vector` unmodified (JVP is autograd of it).
5. **Anchor sanity:** confirm the dense anchor still reaches ~1e-11 on (16,6,8) round
   (it does — the target exists; only the matrix-free solver fails to reach it).
