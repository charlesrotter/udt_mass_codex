# UDT H3 Static Mass-Backreaction Dispatch

**Date:** 2026-07-11  
**Branch:** `grok` of `charlesrotter/udt_mass_codex`  
**Mode:** DERIVE → VERIFY → bounded OBSERVE  
**Object:** banked H3-class, (Q_H=1) carrier only; never the drained f2d \(\pi_2\) hedgehog  
**Primary question:** Does the banked static H3 carrier continue to a self-consistent, positive, cutoff-independent local-mass geometry once the metric is allowed to depart from reciprocal form inside matter?

---

## 0. Startup and authority

1. Pull `grok` and read `LIVE.md` from disk first. Disk `LIVE.md` wins over this dispatch if the branch has moved.
2. Record the checked-out commit SHA and the actual `main...grok` comparison. Do not trust an old commit count.
3. Charles has authorized overturning prior canon decisions in this derivation hunt. For this job:
   - **Overturn/demote P16-C:** do not use the channel-corrected \(\bar g\) matter metric.
   - **Demote global reciprocal interior:** \(B=1/A\) is an exterior/clean-dilation relation, not an interior constraint through radial carrier structure.
   - **Demote G/P as a particle-mass foundation:** it belongs to the older constrained two-player action and is not used in this solve.
   - **Retain WR-L only in its macro residual/wall scope.** Do not impose WR-L on the particle interior or local exterior.
4. DATA-BLIND: do not load lepton, hadron, wall-number, SNe, BAO, CMB, or Standard Model targets.
5. One process per GPU. No background polling. Halt rather than silently reduce physics.

---

## 1. Frozen premise ledger

| Item | Status for this dispatch |
|---|---|
| UDT dilation metric form | DERIVED upstream |
| Unit three-vector \(\mathbf n:\Sigma\to S^2\) | POSIT |
| Physical-metric carrier coupling \(S_m[g,\mathbf n]\) | WORKING/REOPENED; minimal metric-native coupling |
| \(L_2\) | DERIVED unique at two derivatives, given carrier |
| \(L_4=|\Omega|_g^2\) | DERIVED native stabilizer, given carrier |
| \(L_6\) | admissible robustness extension; not in primary solve |
| Geometric action \(\int\sqrt{-g}R/(2\kappa_g)\) | CONDITIONAL DERIVED under metric-only/local/two-derivative minimality |
| Staticity | WORKING first solve; no isorotation |
| Axisymmetry | must be MEASURED on the banked H3 stress before imposed |
| Absolute values of \(\xi,\kappa_4,\kappa_g\) | FREE; use dimensionless continuation, do not fit |

### Frozen action

\[
S=\frac{1}{2\kappa_g}\int d^4x\sqrt{-g}\,R[g]
+\int d^4x\sqrt{-g}\left[-\frac{\xi}{2}\,\partial_\mu\mathbf n\cdot\partial^\mu\mathbf n
-\frac{\kappa_4}{4}\,\Omega_{\mu\nu}\Omega^{\mu\nu}\right],
\]

\[
\Omega_{\mu\nu}=\mathbf n\cdot(\partial_\mu\mathbf n\times\partial_\nu\mathbf n),
\qquad |\mathbf n|=1.
\]

Do not add potentials, effective corrections, cutoffs, damping physics, background fluids, or a private particle wall.

---

## 2. Analytic identities the code must reproduce

On a static slice with spatial metric \(\gamma_{ij}\), lapse \(N\), covariant derivative \(D_i\), and \(S=\gamma^{ij}S_{ij}\):

\[
R^{(3)}=2\kappa_g\rho,
\]

\[
D^2N=\frac{\kappa_gN}{2}(\rho+S),
\]

\[
R^{(3)}_{ij}-N^{-1}D_iD_jN
=\kappa_g\left[S_{ij}+\frac12\gamma_{ij}(\rho-S)\right].
\]

Define

\[
X=D_i\mathbf n\cdot D^i\mathbf n,
\qquad F_{ij}=\mathbf n\cdot(D_i\mathbf n\times D_j\mathbf n),
\qquad Y=F_{ij}F^{ij}.
\]

The code must independently recover

\[
\rho=\frac{\xi}{2}X+\frac{\kappa_4}{4}Y,
\]

\[
S_{ij}=\xi\left(D_i\mathbf n\cdot D_j\mathbf n-\frac12\gamma_{ij}X\right)
+\kappa_4\left(F_i{}^kF_{jk}-\frac14\gamma_{ij}Y\right),
\]

\[
S=-\frac{\xi}{2}X+\frac{\kappa_4}{4}Y,
\qquad
\boxed{\rho+S=\frac{\kappa_4}{2}Y=2\rho_4\ge0},
\]

and hence

\[
\boxed{D^2N=\kappa_gN\rho_4}.
\]

For any closed surface \(\mathcal S\), define

\[
M_N[\mathcal S]=\frac{2}{\kappa_g}\oint_{\mathcal S}D_iN\,dS^i.
\]

The volume identity is

\[
\boxed{M_N[\partial V]=2\int_VN\rho_4\,dV}.
\]

In the weak-backreaction limit, the banked virial \(E_2\simeq E_4\) predicts

\[
M_N\simeq2E_4\simeq E_2+E_4.
\]

This identity—not a chosen radius—is the mass readout.

---

## 3. Required repository inputs

Locate; do not synthesize:

1. The banked H3 \(Q_H=1\) field, preferably the production `prod_an256.npz` or its current successor.
2. The exact grid coordinates, spacing, compactification/mapping, and boundary convention used to bank it.
3. Existing H3 energy and Hopf-charge routines.
4. Existing `L2`, `L4`, virial, and topology verification routines.
5. GPU environment used for the N=192/N=256 H3 runs.

If the production field is absent, **HALT with `BLOCKED_MISSING_H3`**. Do not replace it with a new ansatz, a hedgehog, a lower-topology seed, or synthetic data.

Before any new calculation, reproduce on the loaded field:

\[
|Q_H|\approx0.99,
\qquad E_2/E_4\approx1,
\]

within the banked discretization error. Report actual values; do not force these targets.

---

## 4. File set to implement

Create these repo files unless equivalent current files already exist:

```text
hopfion_static_mass_common.py
hopfion_static_mass_hessian.py
hopfion_static_mass_linear_metric.py
hopfion_static_mass_continue.py
hopfion_static_mass_verify.py
hopfion_static_mass_out.json
hopfion_static_mass_results.md
```

### `hopfion_static_mass_common.py`

Own all shared, tested operations:

- production H3 loading;
- unit-vector projection;
- grid derivatives with the banked boundary convention;
- \(X,F_{ij},Y,\rho_2,\rho_4,S_{ij},S\);
- \(E_2,E_4,Q_H\);
- surface-flux integration;
- symmetry generators and projection;
- domain/radius masks used only for diagnostics, never to define mass.

Every tensor identity in Section 2 must have a unit test on random smooth unit-vector fields and on the banked H3 field.

### `hopfion_static_mass_hessian.py`

Matrix-free Hessian-vector products for the flat-background carrier energy. Use tangent perturbations

\[
\boldsymbol\eta=(I-\mathbf n\mathbf n^T)\delta\mathbf n.
\]

Do not assemble the full Hessian. Use automatic differentiation or an independently verified analytic HVP.

Project out:

- translations;
- spatial rotations present in the computational sector;
- global target rotations compatible with the fixed asymptotic \(\mathbf n_\infty\);
- any grid gauge/null artifacts identified analytically.

Compute low modes by matrix-free Lanczos/LOBPCG. Start on bounded grids/domains; production resolution only after convergence behavior is understood.

**Critical interpretation:** the exterior is gapless. Extended eigenvalues approaching zero as domain size grows are expected and are not instability. Classify modes by eigenvalue, symmetry overlap, localization fraction, inverse participation ratio, and domain scaling.

### `hopfion_static_mass_linear_metric.py`

First solve only the frozen-H3, first-order lapse equation:

\[
N=1+\kappa_g u+O(\kappa_g^2),
\qquad
\Delta u=\rho_4,
\qquad u\to0.
\]

Use a solver with a residual and independent Gauss-law check. Do not infer mass from a fitted \(1/r\) interval alone.

Required checks:

\[
\oint_{\mathcal S_R}\nabla u\cdot d\mathbf S
\longrightarrow\int\rho_4\,d^3x=E_4,
\]

\[
M_N(R)=2\oint_{\mathcal S_R}\nabla u\cdot d\mathbf S
\longrightarrow2E_4,
\]

\[
\frac{M_N}{E_2+E_4}
\longrightarrow
\frac{2E_4}{E_2+E_4}.
\]

Then derive and solve the complete first-order static metric response in a documented spatial gauge. Derive the linear equations symbolically or by action variation; do not paste textbook component equations. Verify the linearized Hamiltonian and spatial constraints independently.

### `hopfion_static_mass_continue.py`

Only after Hessian and linear-metric gates pass:

1. Determine whether the banked H3 stress is axisymmetric to discretization error.
2. If yes, use

   \[
   ds^2=-N^2dT^2+e^{2a}(dR^2+R^2d\theta^2)+e^{2b}R^2\sin^2\theta\,d\varphi^2.
   \]

3. If not, **do not average it**. Use a full 3D static metric formulation or halt with `AXISYMMETRY_FAILS` and emit the measured nonsymmetric stress components.
4. Continue from \(\kappa_g=0\) using damped Newton-Krylov/pseudo-arclength continuation. Step size may respond to Newton convergence, never to a preferred mass.
5. Re-normalize \(|\mathbf n|=1\) through tangent updates or a constraint multiplier; do not normalize away residuals after the solve.

### `hopfion_static_mass_verify.py`

Independent read-only verifier. It must recompute from saved fields:

- field-equation residuals;
- constraints;
- \(Q_H\);
- \(E_2,E_4\) and virial residual;
- lapse Gauss law;
- mass-flux convergence;
- domain enlargement;
- grid refinement;
- reciprocal recovery in the unwound exterior;
- axis regularity and absence of conical defect.

The verifier must not import solver internals other than neutral I/O/grid utilities.

---

## 5. Phased execution

### Phase A — provenance and baseline

Deliver:

- commit SHA;
- source field path and SHA256;
- grid description;
- baseline \(Q_H,E_2,E_4,E_2/E_4\);
- axisymmetry residual of \(\rho,S_{ij},\rho_4\).

Stop if the object or baseline cannot be reproduced.

### Phase B — Hessian classification

Use at least three increasing grid/domain combinations before a production statement. Do not demand a positive spectral gap.

Classify every low mode as one of:

- `SYMMETRY_ZERO`;
- `EXTENDED_CONTINUUM` with \(\lambda\sim L_{\rm box}^{-2}\);
- `LOCALIZED_POSITIVE`;
- `LOCALIZED_ZERO_MODULUS`;
- `LOCALIZED_NEGATIVE`;
- `UNRESOLVED`.

**Gate:** no converged `LOCALIZED_NEGATIVE`; no unexplained `LOCALIZED_ZERO_MODULUS`.

The scale perturbation must be tested explicitly and compared with

\[
E''(1)=2E_4>0
\]

for \(L_2+L_4\).

### Phase C — frozen-source linear mass

Solve \(\Delta u=\rho_4\). Measure flux on nested surfaces and enlarged domains.

**Pass:** volume-source and surface-flux estimates converge to the same limit under grid and domain refinement, with error decreasing at the scheme's observed order.

**Fail:** stable nonzero drift after the \(L_4\) tail and discretization errors are resolved.

No inner cutoff is permitted. The origin/core is part of the loaded smooth H3 field.

### Phase D — complete linear metric response

Solve all gauge-fixed first-order metric variables and verify every constraint. Check:

- lapse depression has the source-predicted sign;
- exterior surface flux is conserved;
- reciprocal departure is localized with the carrier stress;
- no gauge mode is mistaken for physical growth.

### Phase E — nonlinear continuation

Continue in dimensionless \(\kappa_g\). At each step record:

- Newton residual and constraint norms;
- \(Q_H\);
- \(E_2,E_4\), total carrier energy;
- \(\min N\);
- metric regularity;
- surface mass flux versus radius;
- reciprocal-departure norm inside and outside the texture;
- domain/grid sensitivity.

Stop before \(N\le0\) or loss of ellipticity; characterize the endpoint rather than stepping through it.

### Phase F — optional \(L_6\) robustness

Only after the primary \(L_2+L_4\) result is banked. Add \(L_6\) with symbolic coefficient; do not tune it. Verify

\[
\rho_6+S_6=4\rho_6,
\]

and the scale identity

\[
E_2=E_4+3E_6,
\qquad
M_N=2E_4+4E_6=E_2+E_4+E_6
\]

in the weak-backreaction stationary limit.

---

## 6. Boundary and regularity conditions

For the local-room continuum solve:

- carrier: \(\mathbf n\to\mathbf n_\infty\), fixed \(Q_H=1\), no fixed profile;
- lapse: \(N\to1\) as relative clock normalization;
- spatial metric: asymptotically flat local-room normalization for this scoped test;
- origin: smooth Cartesian regularity;
- symmetry axis, if axisymmetric: \(a=b\) and the appropriate even/odd derivative conditions; no conical defect;
- no private wall at the hopfion radius;
- no WR-L macro wall inside this local-room solve.

The eventual local-to-WR-L ambient matching is a later problem. Do not contaminate this mass-existence test with it.

---

## 7. Pre-registered verdicts

### `PASS_LOCAL_MASS_BRANCH`

All must hold:

1. H3 baseline and topology reproduced.
2. No converged localized negative Hessian mode after symmetry projection.
3. Linear lapse source/flux identity converges.
4. Nonlinear continuation exists for a nonzero interval of \(\kappa_g\).
5. \(M_N>0\) and converges under surface, domain, and grid enlargement.
6. Reciprocal departure is nonzero where \(\rho+p_r>0\) and returns toward the exterior relation.

### `FAIL_H3_INSTABILITY`

A localized negative carrier mode converges with grid/domain refinement. Report its field shape and symmetry; do not stabilize it artificially.

### `FAIL_GEOMETRIC_OPERATOR`

Gauge-fixed metric operator loses ellipticity, constraints cannot converge, or flat space fails the independent variation checks.

### `FAIL_MASS_FLUX`

The volume/source and surface/flux identities disagree after verified discretization convergence, or the flux remains domain-controlled.

### `BLOCKED_ACTION_FORK`

Implementation discovers that the metric-only action is insufficient to define a required equation without adding a preferred-coframe invariant. Stop and identify the exact missing term; do not choose its coefficient.

---

## 8. Required JSON output

`hopfion_static_mass_out.json` must contain at least:

```json
{
  "provenance": {
    "git_sha": "",
    "branch": "grok",
    "h3_path": "",
    "h3_sha256": "",
    "device": "",
    "dtype": "float64"
  },
  "baseline": {
    "grid": {},
    "Q_H": null,
    "E2": null,
    "E4": null,
    "E2_over_E4": null,
    "axisymmetry_residuals": {}
  },
  "hessian": {
    "runs": [],
    "mode_classification": [],
    "scale_curvature_numeric": null,
    "scale_curvature_expected": null,
    "gate": "PASS|FAIL|UNRESOLVED"
  },
  "linear_lapse": {
    "runs": [],
    "volume_E4": null,
    "surface_fluxes": [],
    "mass_flux_limit": null,
    "predicted_2E4": null,
    "mass_over_carrier_energy": null,
    "gate": "PASS|FAIL|UNRESOLVED"
  },
  "linear_metric": {
    "gauge": "",
    "residuals": {},
    "constraints": {},
    "reciprocal_departure": {},
    "gate": "PASS|FAIL|UNRESOLVED"
  },
  "continuation": {
    "steps": [],
    "endpoint_class": "",
    "gate": "PASS|FAIL|NOT_RUN"
  },
  "verdict": ""
}
```

Use `null`, never fabricated fallback values.

---

## 9. Results document requirements

`hopfion_static_mass_results.md` must include:

1. Hygiene header and premise ledger.
2. Exact commit and H3 provenance.
3. Methods sufficient to reproduce every run.
4. Hessian mode table with localization and domain scaling.
5. Nested-surface mass-flux table.
6. Grid/domain convergence tables.
7. Constraint and equation residuals.
8. Derived / conditional / chose / open labels.
9. Explicit statement of what failed if any gate fails.
10. No particle labels, measured-mass comparison, fitted coupling, or publication claim.

---

## 10. Suggested commands

Adapt only to the repository's actual CLI conventions:

```bash
python3 hopfion_static_mass_hessian.py --input PATH_TO_PROD_H3 --phase baseline
python3 hopfion_static_mass_hessian.py --input PATH_TO_PROD_H3 --phase spectrum
python3 hopfion_static_mass_linear_metric.py --input PATH_TO_PROD_H3 --phase lapse
python3 hopfion_static_mass_linear_metric.py --input PATH_TO_PROD_H3 --phase full-linear
python3 hopfion_static_mass_continue.py --input PATH_TO_PROD_H3 --resume-linear
python3 hopfion_static_mass_verify.py --json hopfion_static_mass_out.json
python3 -m pytest tests/
```

Expected repository test status must be read from current `LIVE.md`; do not reinterpret a documented hygiene-only failure as a new code failure.

---

## One-line dispatch

**Load the real banked H3 carrier; verify topology and virial; classify the matrix-free Hessian without mistaking the gapless continuum for instability; solve the exact positive lapse source \(D^2N=\kappa_gN\rho_4\); verify volume-to-surface mass conservation and domain independence; then continue the unconstrained static metric and carrier together—never imposing reciprocal geometry inside the radial texture, never using \(\bar g\), G/P, a private wall, or a fitted mass.**
