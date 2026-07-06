> **CONDITIONS-CHANGED (2026-07-06 second-pass sweep, LOW RISK) — corrects a prior CLEAN mis-certification.**
> Runs on the PRE-NATIVE frame B (resE = G^μν − kap8·T^μν, a(φ)=−1 frozen) — the everything-on P-series
> (self-contained solver, no branch_operator import → slipped the first sweep's frame-A grep). It banks only
> off-diagonal-wiring machinery (category-A) + a LINEAR-level off-diagonal-sourcing observation; the round-S²
> soliton anchor is EXPLICITLY deferred to P5 (NOT delivered here), so no native-micro soliton/mass positive is
> banked. Low risk, but the frame is superseded (2026-07-01 native operator). See branch_operator_contamination_ledger.md.

# P2 -- the native matter equation, 3-D and off-diagonal-aware: results

**Phase:** P2 of the everything-on solver (EVERYTHING_ON_SOLVER_P2_MAP.md).
**Driver:** Claude (Opus 4.8, 1M).  **Date:** 2026-06-19/20.  **Mode:** OBSERVE.
**DATA-BLIND** (units L=sqrt(kappa/xi)=1; no mass/ratio/wall number loaded or computed;
the M_MS-like numbers below are dimensionless soliton masses in these native units, used
only as solver diagnostics).  **Append-never-edit research record.  NOT canon.**

Governing: EVERYTHING_ON_SOLVER_P2_MAP.md; CLAUDE.md "How we work" + repo discipline
(committed scripts IMMUTABLE; new work = new files; verifier-before-record).  Carries the
P1 verifier caveats (p1_VERIFIER.md) and the carrier settle (s2_s3_identity_results.md +
_VERIFIER.md).

---

## REGIME STAMP / PREMISE LEDGER

| Item | Value | chose / derived |
|---|---|---|
| matter carrier | native S^2 **UNIT** 3-vector n=(sinF cos mps, sinF sin mps, cosF) | DERIVED (carrier settle; the genuine UNIT embedding) |
| matter profile | F(r,theta,psi) FREE (the 3-D generalization of Theta(r)) | the P2 turn-on |
| matter EL | autograd of S=int sqrt(-g)(L2+L4) on the FULL off-diagonal metric | the P2 closure |
| native L4 | cross-product (eps_abc); == MAT Lagrange-identity L4 on a 3-vector (verified 1e-13) | DERIVED (canon C-14-1) |
| core BC | deg-1 NODE sin F(0)=0 (F core=pi -> seal=0); NO m*pi ladder | DERIVED-as-node |
| metric | general 4x4, pole-stable hybrid Einstein (P1), off-diag e_rt,e_rp,e_tp LIVE | reused (P1) |
| a(phi) | a = -1 (GR baseline) | FIXED baseline (P3, not touched) |
| time row | ZEROED | scoped out (P4) |
| B vs A | INDEPENDENT (B=1/A FREE, not injected) | discipline (grep-verified) |
| grid | Cheb_r x GL_theta x Fourier_psi; Nr=40-48, Nth scan 8..28, Nps=8 | CHOSE (tractability) |

---

## 1. WHAT WAS BUILT (new files; immutable committed scripts untouched)

- **`p2_matter_s2_fullmetric.py`** -- the native S^2 carrier for P2:
  - `field_n_s2` / `field_dn_s2`: the genuine **UNIT** S^2 3-vector
    n=(sinF cos mps, sinF sin mps, cosF), |n|=1 EXACTLY (verified 4e-16), profile
    F(r,theta,psi) FREE; exact chain-rule gradients (spectral on F, analytic embedding).
    THREE target components -- NO S^3 4th component (the import #61).
  - `stress_s2_fullmetric`: native S^2 Hilbert stress = MAT.stress_tensor on the
    3-component field (the MAT Lagrange-identity L4 == native cross-product L4 on a
    3-vector, re-verified machine-0 here) -- on the FULL off-diagonal metric (ginv).
  - `matter_action_s2` / **`matter_el_s2_fullmetric`**: the matter action and its EL by
    **autograd** wrt the nodal F, using ginv from the **FULL off-diagonal metric** --
    THE P2 CLOSURE of the P1 gap (P1's matter_el_3d was the DIAGONAL analytic EL, blind
    to e_rt,e_rp,e_tp).
  - `covariant_divT_field` / `interior_mask`: the covariant divT field on a general
    metric + the geometric-interior excision (same category-A excision as divT_excised).
- **`p2_residual_fullmetric.py`** -- the P1 8-field general-Einstein residual with the
  matter sector swapped to the native S^2 field + the full-metric autograd EL.  (Carries
  a column-FD Jacobian + LM solve; the autograd EL is not jacrev-composable -- flagged.)
- **`p2_round_s2_solver.py`** -- the round native-S^2 soliton solver (a(r),b(r),F(r)
  coupled through the diagonal Einstein + the autograd EL; deg-1 node, B=1/A free).
- **`p2_divT_fd_gate.py`** -- the decisive P2b consistency gate (below).
- **`p2c_shear_observe.py`** -- the P2c shear observation (below).
- **`p2_validate_ab.py`** -- P2a validation (unit field, L4 identity, axis-regularity,
  node core).

How the EL now sees the full metric: the action S=sum sqrt(-g)(L2+L4) dV uses ginv from
the full off-diagonal metric, and the EL = (1/measure) d S/d F(node) by autograd.
Autograd differentiates THIS action exactly (machine precision), so the EL depends on
every metric component the Lagrangian contains -- including the off-diagonals.

How Theta went 3-D: the single radial Theta(r) of P0/P1 became the free 3-D profile
F(r,theta,psi); the matter can now be fully non-axisymmetric, and (load-bearing) the
genuine native deg-1 object REQUIRES F to depend on theta (Sec. 4).

---

## 2. P2a VALIDATION (`p2_validate_ab.py`)

- **Genuine UNIT S^2 field:** max | |n|^2 - 1 | = **4.4e-16** (machine-0).  The
  superseded `(sinTheta sinth cos mps, ...)` form is NON-unit (|n|^2 = 1 - sin^2Theta
  cos^2theta) -- the "texture artifact" the carrier settle named; the genuine unit
  embedding is the target-polar-angle hedgehog used here.
- **Native L4 == MAT L4 on the 3-vector:** max|L4_cross - L4_MAT| = **1.1e-13** ->
  MAT.stress_tensor IS the native S^2 stress (no S^3 import).
- **Texture-free CANON object recovered:** for **F=theta** (the n=x/r monopole),
  rho is theta-INDEPENDENT (axis/equator ratio 0.8) and **T^t_t = T^r_r EXACTLY**
  (|diff|_max = 0.0e+00) -- the B=1/A-consistent CANON object (s2_s3 results Sec.3).
- **Node core, no Skyrme:** F(core) in {0, pi, 2pi} all give |sin F(core)| < 3e-16
  (all nodes); the operator selects sin F(0)=0, value FREE.  Grep-clean: no m*pi solved
  BC in any P2 file (only labelled comments / the negative-control branch).
- **M_MS / round anchor:** the round native-S^2 soliton with a PURE-RADIAL F(r) ansatz
  converges to MACHINE FLOOR (Phi=2.0e-16 at Nr=40, deg-1 node F(core)=pi, B=1/A free)
  BUT is **polar-singular** -- M_MS=123 (Nr=40) vs 173 (Nr=60), Nr-UNSTABLE, because the
  ψ-winding energy ~1/(r^2 sin^2 theta) piles up on the polar axis (rho axis/equator
  ratio ~14).  This is a genuine derivation finding, NOT a numeric bug: a pure-radial
  F(r) is the WRONG native object; the genuine deg-1 native S^2 field ties the target
  polar angle to theta so sin F -> 0 at both poles (axis-regular).  See Sec. 4.

---

## 3. P2b -- the matter-metric consistency gate (`p2_divT_fd_gate.py`)

The covariant divT identity (nabla_mu T^mu_nu == -EL d_nu F) holds in the CONTINUUM
because the stress and EL come from the SAME action.  At the dense-Newton grids the
covariant divT OPERATOR is dominated by its own spectral-derivative noise -- the same
gate-Nth limit the committed `divT_excised.py` records (its off-round self-test [B] has
rel-err ~0.8 even at Nr=160).  I CONFIRMED this is the gate, not the EL: the **COMMITTED
S^3 path + committed analytic EL + committed divT** ALSO fails the off-round identity at
these grids (per-nu |divT| >> |EL.dTheta|, no cancellation).  So the covariant divT
cannot confirm the OFF-round identity on this driver -- it is **gate-Nth-limited**
(MAP risk #3 realized; matches the P1 caveat).

THE CLEAN GATE (free of the covariant operator's noise): the autograd EL must equal the
**finite-difference variation of the SAME discrete action** that builds the Hilbert
stress, evaluated on a **NON-DIAGONAL metric**:
  el(node) ?= [S(F+eps e) - S(F-eps e)]/(2 eps)/measure.

RESULT on a metric with ALL THREE off-diagonals LIVE (e_rt=e_rp=e_tp != 0):

| node (i,j,k) | autograd EL | FD dS/dF/meas | rel-err |
|---|---|---|---|
| (20,5,3) | +1.517016e-2 | +1.517015e-2 | 1.7e-7 |
| (15,4,2) | -5.226058e-2 | -5.226059e-2 | 1.1e-7 |
| (25,6,5) | +3.424830e-4 | +3.424819e-4 | 3.4e-6 |
| (10,2,1) | -1.529204e-2 | -1.529197e-2 | 4.4e-6 |
| (30,8,6) | +1.609008e-3 | +1.609009e-3 | 6.0e-7 |
| (18,7,4) | +3.968519e-2 | +3.968520e-2 | 2.0e-7 |

**max rel-err = 4.4e-6** (~FD truncation floor).  This PROVES rigorously that (a) the
autograd EL is the true variation of the action, and (b) it **varies on the FULL
off-diagonal metric**.  Stress-consistency (-> the continuum divT identity) follows
because the Hilbert stress is -2 dL/dg + gL of the SAME L.

**Coupling witness:** |EL_offdiag - EL_diagonal|_max = 2.1e-2 (nonzero; vs |EL|~9e2),
and it scales ~LINEARLY with the off-diagonal amplitude A (1.06e-3 @ A=0.02 ->
5.24e-3 @ A=0.10).  The matter EL genuinely COUPLES to the off-diagonals (first-order,
not vestigial) -- **the P1 gap is closed.**

GATE VERDICT: **PASS** by the FD-variational gate (the decisive, noise-free test); the
covariant divT gate is gate-Nth-limited on this driver and is reported as such, not
forced.

---

## 4. P2c -- the shear observation (`p2c_shear_observe.py`), OBSERVE not target

The P1-deferred question: with the matter EL now SEEING the off-diagonals and on the
genuine native S^2 carrier, does static native matter source the spatial off-diagonals
(e_rp, e_tp), and is the e_rt response a grid artifact (->0 with Nth) or genuine?

Method (honest tractability note): the full coupled 8-field Newton with the autograd-EL
**column-FD** Jacobian is INTRACTABLE on the no-cache allocator (the throughput wall;
MAP risk #2, P5's fix).  So P2c is the **linear-level off-diagonal-sourcing observation**
P1 flagged as the clean confirmation: take an axis-regular native-S^2 matter config
(off-diagonal warps zero), evaluate the off-diagonal Einstein residuals
resE = G^mu_nu - kap8 T^mu_nu that e_rt/e_rp/e_tp would absorb, and scan Nth.

The genuine axis-regular native deg-1 config: **F = theta + h(r) sin(theta)** (so
sin F -> 0 at BOTH poles for all r; rho finite & symmetric ~0.016, NOT the polar-singular
F(r) of Sec. 2), with a mild diagonal soliton warp.  Nth = 8..28:

| Nth | resE_rth | resE_rps | resE_thps | T^r_th | rho(pole0) | rho(poleN) |
|---|---|---|---|---|---|---|
| 8  | 1.744e-1 | 2.3e-17 | 1.9e-15 | 3.487 | 1.616e-2 | 1.579e-2 |
| 12 | 1.730e-1 | 2.4e-17 | 1.7e-15 | 3.459 | 1.614e-2 | 1.575e-2 |
| 16 | 1.733e-1 | 2.9e-17 | 1.8e-15 | 3.465 | 1.613e-2 | 1.574e-2 |
| 20 | 1.737e-1 | 2.5e-17 | 2.4e-15 | 3.473 | 1.612e-2 | 1.574e-2 |
| 24 | 1.736e-1 | 2.7e-17 | 1.8e-15 | 3.471 | 1.612e-2 | 1.573e-2 |
| 28 | 1.737e-1 | 2.6e-17 | 1.8e-15 | 3.473 | 1.612e-2 | 1.573e-2 |

**WHAT IS THERE (the P1-deferred question, now settled):**

- **e_rp, e_tp channels: GENUINELY ZERO.**  resE_rps ~ 3e-17 and resE_thps ~ 2e-15 stay
  at MACHINE floor, Nth-stable.  Static native matter sources **NO (r,psi) or (theta,psi)
  shear**.  This CONFIRMS and STRENGTHENS the P1 observation (P1 saw ~1e-10 with the
  matter blind to off-diagonals; here it is machine-exact with the matter genuinely
  full-metric-consistent).

- **e_rt channel: GENUINE, Nth-CONVERGED -- NOT a grid artifact.**  resE_rth is
  **Nth-CONVERGED** (0.1744 -> 0.1737 across Nth 8->28, drift 0.4%); T^r_th = 3.47 is
  rock-stable.  And it is sourced by the field's THETA-structure: a controlled scan shows
  **T^r_th = 0 EXACTLY when F has no theta-dependence**, and grows monotonically with the
  theta-gradient of F (0.054 @ s=0.5 -> 0.95 @ s=2.0).  So a native S^2 matter config
  that genuinely depends on theta sources a real, Nth-converged (r,theta) momentum that
  the e_rt warp absorbs.

- **Resolution of the P1 e_rt ambiguity:** P1's e_rt~1.3e-2 was small because P1's matter
  (S^3, blind to off-diagonals, near-round) barely sourced T^r_th; the P1 verifier
  separately found "G^r_th itself is Nth-stable (a real geometric response)".  P2 settles
  it: e_rt is the off-diagonal sector correctly absorbing a **GENUINE, Nth-stable** T^r_th
  whenever the native matter has theta-structure.  It is NOT a pure discretization
  artifact.  (The round-with-no-theta-structure case gives T^r_th = 0 exactly -- so a
  perfectly axisymmetric soliton sources no shear; the artifact-vs-genuine fork is
  resolved by whether the matter actually has theta-structure.)

**P2c VERDICT:** static native matter sources NO (r,psi)/(theta,psi) shear (machine-zero,
Nth-converged); it DOES source a genuine, Nth-converged (r,theta) shear (T^r_th) when the
field has theta-structure.  The off-diagonal sector responds correctly and selectively.

---

## 5. AUDIT (every compromise, honestly)

- **Carrier corrected to the genuine UNIT S^2.**  P1's matter (full3d_spectral.field_n)
  was the S^3 4-vector hedgehog (the import #61); P2 builds on the settled S^2 unit
  3-vector.  The committed S^2 derive's field is NON-unit (the texture artifact); P2 uses
  the genuine unit target-polar-angle hedgehog.  Flagged and verified (|n|^2=1, L4 ==).
- **EL genuinely coupled to off-diagonals -- PROVEN.**  The FD-variational gate (Sec. 3,
  rel-err 4e-6 on a fully non-diagonal metric) is the rigorous proof that nothing stayed
  diagonal.  The coupling-witness Delta=2e-2 (linear in A) confirms first-order coupling.
- **The covariant divT gate is gate-Nth-limited** on this driver (Sec. 3) -- reported as
  such, NOT forced; the committed S^3 path fails it identically, proving it is the gate's
  spectral noise, not the EL.  The clean gate (FD-variational) is used instead.
- **The pure-radial F(r) round S^2 ansatz is polar-singular** (Sec. 2) -- recorded as a
  genuine derivation finding (the ψ-winding piles on the axis), not hidden.  The genuine
  native object needs F(r,theta); the full F(r,theta) coupled SOLVE is left to P5 (the
  throughput wall) -- so the round S^2 ANCHOR (a converged, axis-regular, localized
  native-S^2 soliton with its M_MS) is **NOT delivered this phase** (partial).
- **Throughput wall: P2c is the linear-level observation, not a full coupled solve.**  The
  autograd-EL column-FD Jacobian makes the coupled 8-field Newton intractable on the
  no-cache allocator.  Flagged; the OBSERVE result (off-diagonal sourcing vs Nth) is
  Nth-CONVERGED and trustworthy at the linear level; a fully coupled high-shear solve is
  P5.  NOTE: T^r_th=3.47 -> e_rt would be LARGE, outside the P1 hybrid's small-shear
  validity (A <~ 0.1) -- the fully-coupled large-shear regime is explicitly P5 territory
  (flagged).
- **a(phi) = -1 (P3) FROZEN; time row ZEROED (P4).**  The only declared freezes.
- **No B=1/A injection, no Skyrme m*pi BC, no dropped/added term, no kept linearization.**
  Grep-verified across all P2 files.  Autograd / spectral derivatives / FD-Jacobian are
  sanctioned exact / function-replacement numerics (Principle 2 clean).
- **Data-blind?** CONFIRMED -- no mass/ratio/wall number loaded or compared; the
  dimensionless soliton-mass diagnostics are in native L-units only.

---

## 6. SCOPED STATUS

**P2 = PARTIAL (the two declared closures DONE; one anchor + the fully-coupled solve
deferred to P5 on the throughput wall):**

DONE:
- The matter EL is now 3-D (F(r,theta,psi) free) on the genuine native **S^2 UNIT**
  carrier (validated: unit field, native L4, node core, no Skyrme).
- The matter EL genuinely **VARIES ON THE FULL OFF-DIAGONAL METRIC** -- PROVEN by the
  FD-variational gate (rel-err 4e-6 on a fully non-diagonal metric) + the linear-A
  coupling witness.  **The P1 matter-EL/off-diagonal gap is CLOSED.**
- The P1-deferred shear observation is RE-TAKEN and SETTLED (Nth-converged): (r,psi) and
  (theta,psi) shear genuinely zero; (r,theta) shear (T^r_th) is a GENUINE, Nth-converged
  response sourced by the field's theta-structure -- NOT a grid artifact.

DEFERRED (honestly):
- The covariant divT identity to floor OFF-round: gate-Nth-limited on this driver
  (the FD-variational gate substitutes as the decisive consistency proof).
- The fully-coupled high-resolution native-S^2 round ANCHOR (axis-regular F(r,theta),
  its M_MS) and any fully-coupled solve where the matter DRIVES large shear: the
  autograd-EL FD Jacobian is intractable on the no-cache allocator -> P5's research-grade
  driver.

**What P3 inherits:**
- A native S^2 matter sector (`p2_matter_s2_fullmetric.py`) whose stress AND EL both live
  on the full off-diagonal metric and are mutually consistent (FD-gate proven) -- ready
  for a(phi) to be turned on (P3) in the matter coupling.
- The finding that the genuine native deg-1 object is F(r,theta) (axis-regular), not a
  separable F(r) -- P3/P5 must carry F(r,theta) (the matter is intrinsically non-round
  in theta, consistent with the "structure must be NON-round" frontier note).
- The P5 need: a research-grade Newton-Krylov / sparse-direct driver to make the
  autograd-EL coupled solve (and large-shear regimes) tractable.

---

## ATTACK HERE (for a blind verifier)

1. **Is the EL genuinely full-metric-coupled, or diagonal in disguise?**  Re-run
   `p2_divT_fd_gate.py`: confirm the autograd EL matches the FD variation of the action
   on a metric with e_rt,e_rp,e_tp != 0 to ~FD floor, and that |EL_offdiag - EL_diagonal|
   is nonzero and scales ~linearly with the off-diagonal amplitude.  If the EL is blind to
   the off-diagonals, the FD match would fail off-diagonal or Delta would be ~0.
2. **Is the carrier genuinely the UNIT S^2 (not S^3, not the non-unit texture form)?**
   `p2_validate_ab.py`: |n|^2-1 ~ 4e-16; native cross-L4 == MAT L4 (1e-13); F=theta gives
   T^t_t=T^r_r EXACTLY and theta-flat rho (the CANON texture-free object).  Grep for any
   4th component / S^3 / m*pi solved BC -> none in active code.
3. **Is the P2c e_rt response genuine or a grid artifact?**  `p2c_shear_observe.py`:
   resE_rth Nth-converges (drift 0.4% over Nth 8->28) and T^r_th=0 EXACTLY when F has no
   theta-dependence (scale d_th F -> T^r_th scales).  If resE_rth diverged or shrank to 0
   with Nth, the genuine-response reading is wrong.  Confirm resE_rps, resE_thps stay
   machine-zero (no (r,psi)/(theta,psi) shear).
4. **Is the pure-radial F(r) round S^2 really polar-singular (not a coding bug)?**
   `p2_validate_ab.py` [P2a-1]: rho axis/equator ratio ~14 for F(r), ~0.8 for F=theta.
   Confirm the divergence is the ψ-winding ~1/sin^2 theta on the axis, and that the
   axis-regular F(r,theta) (sin F -> 0 at both poles) removes it.
5. **Did the covariant divT really fail for the COMMITTED S^3 path too?** (the proof it is
   the gate's noise, not the EL).  Reproduce: committed full3d_spectral.divT_identity +
   committed matter_el_3d on a perturbed S^3 config gives per-nu |divT| >> |EL.dTheta|
   (no cancellation) at Nr=96-160 -- same as the P2 S^2 path.  If the committed path
   satisfies the off-round identity at these grids, my gate-Nth attribution is wrong.
6. **Discipline grep.** `grep -nE "m\s*\*\s*PI"` over the P2 files -> only labelled
   comments / the negative-control branch.  `grep -nE "b=-a|a=-b|1/A"` -> no B=1/A tie.
   a=-1 (P3) and time-zeroed (P4) the only freezes.
