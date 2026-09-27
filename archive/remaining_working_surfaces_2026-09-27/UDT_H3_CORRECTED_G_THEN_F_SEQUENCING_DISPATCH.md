# WORKSTATION DISPATCH — H3 corrected-carrier G first, then F

**Date:** 2026-07-16  
**Branch:** `grok`  
**Execution order:** **G now → STOP FOR AUDIT → F only under a later go**  
**Data discipline:** DATA-BLIND. No particle labels, observed masses, fitted couplings, or target numbers.  
**Record discipline:** preserve unrelated dirty files; do not edit `LIVE.md` or `CANON.md`; do not rewrite the
stability conclusion in this dispatch.

## 0. Why this dispatch is necessary

The FULL-H seal is accepted as the numerical input to this work:

\[
\text{OBSERVED / NUMERICALLY CERTIFIED:}\qquad
H\big|_{U(1)^\perp}>0
\]

at \(128^3,192^3,256^3\), within the stamped finite-grid frame: the corrected eight-orientation
\(L_2+L_4\) carrier, \(L=6\), `HBW=2`, and the saved independently relaxed critical fields.  The statement is
about the complete **finite-grid** tangent space.  It is not an infinite-volume theorem, a dynamical-stability
claim, or a derivation of the carrier from the native UDT action.

The old Phase-C and branch tools are **not production-safe for the corrected carrier**:

- `hopfion_static_mass_common.matter_fields` uses centered first differences;
- `stability_branch_follow_256.py` imports the old centered energy and centered charge;
- the former `hopfion_static_mass_phaseC_redo.py` reads the superseded carrier
  `hopfion_arc_scripts_2026-07-05/prod_an256.npz`.

Do not patch their outputs into the new record.  Build new `noNull`-named tools whose continuum functional is
exactly the already-certified eight-orientation functional.

## 1. Binding theory and provenance labels

The tested carrier functional is

\[
E[\mathbf n]=E_2+E_4,
\qquad \mathbf n:\mathbb R^3\rightarrow S^2,
\]

\[
E_2=\int \frac{\xi}{2}\,\partial_i\mathbf n\!\cdot\!\partial_i\mathbf n\,d^3x,
\qquad
E_4=\int \frac{\kappa}{4}F_{ij}F_{ij}\,d^3x,
\qquad
F_{ij}=\mathbf n\!\cdot(\partial_i\mathbf n\times\partial_j\mathbf n).
\]

Status:

- the \(S^2\) carrier and this \(L_2+L_4\) functional remain **POSIT / CHOSE** in the native-UDT ledger;
- the corrected discretization represents this same continuum functional and is **DERIVED numerically** as
  cubic-symmetric, no-Nyquist-null, and \(O(h^2)\)-consistent;
- the lapse identity below is **CONDITIONAL** on the EH metric-only action premise;
- G is therefore a **conditional consistency readout**, not a native-UDT mass derivation.

For a static carrier, under that named conditional premise,

\[
D^2N=\kappa_gN\rho_4,
\qquad
M_N=\frac{2}{\kappa_g}\oint D_iN\,dS^i
=2\int N\rho_4\,dV.
\]

In the weak-field expansion \(N=1+\kappa_g u+O(\kappa_g^2)\),

\[
\Delta u=\rho_4,
\qquad
M_N^{(0)}=2\oint\nabla u\cdot d\mathbf S=2E_4.
\]

No value of \(\kappa_g\) is needed or permitted in this unit-response test.

## 2. Preflight — read and protect the record

Run the standard branch update and show the result:

```bash
git checkout grok
git fetch origin
git pull --ff-only origin grok
git status --short --branch
git log -8 --oneline
```

Then read, in order:

1. `LIVE.md` CURRENT STATE;
2. `HANDOFF.md`;
3. `stability_branch_follow_256_DECISION.md`;
4. `noNull_energy.py`;
5. `noNull_schur_inertia_ALL.json` and `noNull_schur_verify.json`;
6. the old Phase-C files only as a failure/provenance audit, never as operators to reuse.

Hash and record these input artifacts before calculation:

- `noNull_critical_field_128.npz`;
- `noNull_critical_field_192.npz`;
- `noNull_critical_field.npz`;
- `noNull_energy.py`;
- `noNull_schur_inertia_ALL.json`.

Confirm every carrier has \(L=6\), \(\xi=\kappa=1\), the expected \(N,h\), finite arrays, and unit-vector error
consistent with roundoff after normalization.  Do not overwrite any input NPZ.

## 3. G1 — construct the corrected local source without centered derivatives

Create `noNull_phaseG_mass.py`.  For each orientation
\(s=(s_1,s_2,s_3)\in\{+1,-1\}^3\), use the same one-sided derivatives as `noNull_energy.py`:

\[
D_i^{s_i}f=
\begin{cases}
(f_{i+1}-f_i)/h,&s_i=+1,\\
(f_i-f_{i-1})/h,&s_i=-1.
\end{cases}
\]

Define orientation-local quantities

\[
X_s=\sum_i D_i^{s_i}\mathbf n\cdot D_i^{s_i}\mathbf n,
\qquad
F^{(s)}_{ij}=\mathbf n\cdot
\left(D_i^{s_i}\mathbf n\times D_j^{s_j}\mathbf n\right),
\]

\[
\rho_{2,s}=\frac{\xi}{2}X_s,
\qquad
\rho_{4,s}=\frac{\kappa}{4}\sum_{i,j}F^{(s)}_{ij}F^{(s)}_{ij}.
\]

The production densities are the eight-orientation averages

\[
\rho_2^{\rm NN}=\frac18\sum_s\rho_{2,s},
\qquad
\rho_4^{\rm NN}=\frac18\sum_s\rho_{4,s}.
\]

Required exact checks, separately at all three grids:

1. \(\rho_4^{\rm NN}\geq0\) to roundoff;
2. `sum(rho2_NN)*h**3` and `sum(rho4_NN)*h**3` reproduce the `E2,E4` returned by
   `energy_noNull` to relative error \(<10^{-12}\);
3. independently form, orientation by orientation,
   \[
   S_s=-\frac{\xi}{2}X_s+\frac{\kappa}{4}Y_s,
   \quad Y_s=\sum_{i,j}(F^{(s)}_{ij})^2,
   \]
   and verify pointwise after averaging
   \[
   \rho^{\rm NN}+S^{\rm NN}=2\rho_4^{\rm NN}
   \]
   to relative max error \(<10^{-12}\);
4. report \(E_2,E_4,E_2/E_4,E_2+E_4,2E_4\), and
   \[
   \delta_{\rm vir}=\frac{E_2-E_4}{E_2+E_4};
   \]
5. report both existing no-null charge readouts (`Q_fwd`, `Q_sym`) and the carrier criticality already stored
   or freshly recomputed.  A centered charge may be printed only as a clearly marked deprecated comparison.

Do not import or call `hopfion_static_mass_common.matter_fields`, `fs_hopfion.energy`,
`energy_centered`, or any centered-difference source builder.

## 4. G2 — source localization and three-grid continuum audit

For each grid, compute the enclosed fractions of \(E_4\) on nested **cubic** and spherical readout regions.  Report
the omitted source fraction rather than calling a finite radius a physical wall.  The fixed carrier boundary is a
solver boundary, not an invented UDT cutoff.

Use the three independently relaxed carriers—not subsamples of the \(256^3\) field—to report numerical
convergence.  For each of \(E_2,E_4,E_2+E_4,2E_4,\delta_{\rm vir}\):

- list the raw \(128/192/256\) values;
- list successive \(h^2\)-slopes;
- give a fine-pair \(h^2\) extrapolation;
- give a three-point \(h^2+h^4\) sensitivity readout;
- do not hide non-pure-\(h^2\) behavior and do not fit any observational number.

The extrapolation is a numerical-discretization audit only.

## 5. G3 — solve the unit Poisson response with a consistent discrete operator

The previous isolated Hockney convolution used the continuum Green kernel and consequently had an approximately
\(1.75\%\) seven-point residual.  Do not call that an exact discrete solve.

Solve

\[
\Delta_h u=\rho_4^{\rm NN}
\]

with the standard seven-point Laplacian on a centered, zero-source-padded cube.  Use matrix-free PCG or multigrid
on \(-\Delta_h\) with Dirichlet \(u=0\) at the outer computational boundary.  This boundary is a numerical
approximation to \(u\to0\); it carries no physical-wall status.

Run padding factors approximately \(p\in\{1,1.5,2\}\) at fixed physical \(h\), recording the actual padded
\(N_p,L_p\).  Embed the original source without interpolation and set it identically to zero outside the original
carrier box.  Required raw residual gate:

\[
r_P=\frac{\|\Delta_hu-\rho_4^{\rm NN}\|_{2,\mathrm{interior}}}
{\|\rho_4^{\rm NN}\|_2}<10^{-9}.
\]

Report convergence of the response quantities \(u(0)\), \(\min u\), and several fixed-radius values as the
padding boundary recedes.  Do not require or claim that the potential normalization is boundary-independent at
finite padding.

## 6. G4 — exact discrete flux and the conditional mass identity

For every solved padding and multiple nested cubic surfaces, evaluate the one-sided bond flux that telescopes the
seven-point Laplacian:

\[
\Phi_h(C)=h\sum_{\text{bonds crossing }\partial C}
(u_{\rm outside}-u_{\rm inside}).
\]

For the same cube compute

\[
Q_h(C)=h^3\sum_{x\in C}\rho_4^{\rm NN}(x).
\]

The primary Gauss gate is raw and local:

\[
\max_C\frac{|\Phi_h(C)-Q_h(C)|}
{\max(|Q_h(C)|,10^{-30})}<10^{-6}.
\]

Also report the value predicted directly from the accumulated Poisson residual, so the flux error is explained
rather than merely thresholded.  On surfaces enclosing all but a reported tail fraction of the source, form

\[
M_{N,h}^{(0)}(C)=2\Phi_h(C),
\qquad
\frac{M_{N,h}^{(0)}(C)}{2E_4}.
\]

The conclusion may be no stronger than:

\[
\boxed{
\text{CONDITIONAL on the EH lapse identity, weak-field unit response: }
M_N^{(0)}=2E_4
}
\]

within the displayed discretization, source-tail, linearization, and boundary errors.  Compare
\(2E_4\) with \(E_2+E_4\) through the measured virial discrepancy; do not silently replace one by the other.

## 7. Independent verifier

Create `verify_noNull_phaseG_mass.py`.  It must not import the production density or flux functions.  It may read
the same carrier NPZs and use the already-audited `energy_noNull` only as a black-box comparison.

The verifier must independently:

1. implement the eight one-sided orientations;
2. recompute \(\rho_2^{\rm NN},\rho_4^{\rm NN},E_2,E_4\);
3. check \(\rho+S=2\rho_4\);
4. recompute at least three cubic face fluxes directly from saved \(u\);
5. recompute the seven-point residual and flux-versus-enclosed-source errors;
6. compare every reported scalar against the production JSON;
7. issue `PASS`, `FAIL`, or `UNRESOLVED`—never repair production numbers in memory.

Run AST/syntax checks and the existing evidence checker.  A preconditioned residual may be reported for solver
diagnosis but may not replace \(r_P\).

## 8. Required G deliverables

Commit and push one evidence-only G commit containing:

- `noNull_phaseG_mass.py`;
- `noNull_phaseG_mass_ALL.json` plus compact per-grid JSON if useful;
- `noNull_phaseG_mass_results.md`;
- raw stdout/stderr logs under a clearly named evidence directory;
- `verify_noNull_phaseG_mass.py`;
- `noNull_phaseG_mass_verify.json` and verifier stdout;
- saved scalar response fields, or an artifact manifest with SHA-256/shape/dtype/origin command when fields are
  too large for Git;
- updated artifact manifest entries for every input and generated NPZ;
- exact commands, software versions, device, elapsed time, and final `git status --short --branch`.

Do not edit `LIVE.md` or `CANON.md`.  Preserve all pre-existing dirt.  Stop after pushing G and return the raw
report for audit.

## 9. F preregistration — locked sequence, DO NOT RUN IN THIS DISPATCH

F begins only after the G return is audited.  Its purpose is finite-amplitude behavior, not another Hessian sign
test.

The later F dispatch will require:

1. only `energy_noNull` / `grad_noNull` and the no-null charge readouts;
2. the certified \(256^3\) physical doublet and isolated mode, freshly projected into the free tangent,
   \(U(1)+T/R\)-complement and re-orthonormalized;
3. doublet-plane directions
   \[
   v_\alpha=\cos\alpha\,v_5+\sin\alpha\,v_6
   \]
   at preregistered angles, plus both signs of the isolated mode;
4. pointwise geodesic perturbations
   \[
   \operatorname{Exp}_{\mathbf n}(s v)=
   \cos(s|v|)\mathbf n+
   \sin(s|v|)\frac{v}{|v|},
   \]
   scaled by maximum pointwise rotation rather than arbitrary coefficient size;
5. a small-amplitude symmetric-curvature check against the exact HVP before any long branch;
6. adaptive finite-amplitude bracketing first at \(128^3\), followed by confirmation of the bracketed behavior
   at \(192^3\) and \(256^3\)—not a blind exhaustive amplitude scan;
7. the repaired moving-tangent trust-region Newton–Krylov machinery, fixed boundary, no Derrick rescaling;
8. free evolution as the primary result; any additional T/R-held run is diagnostic and must be labeled as a
   constrained comparison;
9. complete trajectories: \(E,E_2,E_4,Q_{\rm fwd},Q_{\rm sym},\|g_f\|_{M^{-1}}\), maximum neighbor angle,
   maximum imposed/realized rotation, localization, and displacement;
10. separate translation/rotation controls.  Their small finite-box walls must not be called intrinsic carrier
    modes until a boundary-layer theorem or box/mask study establishes that interpretation.

No existing centered branch output may seed an F conclusion.

## 10. Stop conditions

Stop G and report `UNRESOLVED` if any of the following occurs:

- the new local densities fail to reproduce `energy_noNull`;
- a centered derivative enters the production source or energy path;
- the raw Poisson residual gate is missed;
- the exact discrete Gauss comparison fails without an accounted residual/source-tail explanation;
- grid or padding behavior is nonconvergent;
- the independent verifier disagrees;
- completion would require choosing a physical cutoff, fitting a coupling, or importing a non-UDT mechanism.

Do not proceed to F merely because \(M_N/(2E_4)\) is close to one: for a consistent Poisson solve that equality is
a Gauss identity.  The informative G outputs are the corrected \(E_4\), virial relation, convergence, source
localization, and conditional mass readout on the certified carrier.
