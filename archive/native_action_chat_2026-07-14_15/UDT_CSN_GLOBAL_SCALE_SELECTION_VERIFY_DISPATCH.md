# Workstation dispatch — cold audit of CSN global scale selection

## Scope

Audit the claim that Common-Scale Neutrality turns the positive-\(X\) WR-L family into one pre-scale
gauge orbit, so the existing wall and global-bootstrap equations can select dimensionless
compactness but not absolute \(X\).

Read:

1. UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md
2. UDT_CSN_GLOBAL_SCALE_SELECTION_MAP.md
3. UDT_CSN_GLOBAL_SCALE_SELECTION_DERIVATION_RESULTS.md
4. verify_udt_csn_global_scale_selection.py
5. verify_udt_csn_global_scale_selection_out.txt

For provenance challenges only, consult:

- UDT_RECIPROCAL_C_CONFORMAL_ACTION_DERIVATION_RESULTS.md
- UDT_GLOBAL_BOOTSTRAP_DERIVATION_RESULTS.md
- UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md

Do not alter LIVE.md or CANON.md, adopt a carrier, introduce a scale-setting field, fit \(X\), or
start F/G.

## 1. Scale-orbit audit

Independently pull back

\[
ds^2=-\left(1-\frac rX\right)c^2dt^2
+\left(1-\frac rX\right)^{-1}dr^2+r^2d\Omega^2
\]

under

\[
\rho=r/X,\qquad\tau=ct/X.
\]

Check whether the \(X_1\) and \(X_2\) spacetimes, including their domains and causal wall, are related
by a diffeomorphism plus an allowed CSN factor. Look for a dimensionless local or global observable
that distinguishes them before scale setting.

## 2. Boundary adversary

Audit separately:

- WR-L causal wall;
- canonical odd-fold quotient, one-copy boundary, and matched interface;
- numerical carrier box.

Determine whether any currently derived boundary condition or boundary functional—not merely a
boundary value—breaks the \(X\) orbit. Check endpoint variation, boundary primitive, allowed
variations, and charge normalization. If a boundary term selects \(X\), identify its dimensionful
input and provenance.

## 3. Conformal-action audit

Recheck that the full Bach equations admit the WR-L branch with arbitrary slope \(a_1=-1/X\).
Determine whether a full-tensor equation, regularity condition, or permitted boundary condition
previously omitted in the report fixes \(a_1\). Do not infer native status for the conformal action
beyond its named premises.

## 4. Bootstrap homogeneity

From independently computed response functions

\[
M_{\rm pred}=\frac{c^2X}{G}\mu(\delta),
\qquad
V=X^3\nu(\delta),
\]

audit:

\[
\delta_{\rm rec}=\frac{\mu}{\nu},
\qquad
\chi=\mu,
\qquad
\mu(\delta)-\nu(\delta)\delta=0.
\]

Distinguish exact bookkeeping on a completed solution from a genuine nonlinear root problem.
Check the full \(X\mapsto\lambda X\) weights, including possible scale weight of the normalization
called \(G\). Identify any lawful response that makes the root select absolute \(X\) without an
independent dimensional datum.

## 5. Charge and conservation audit

Challenge the statement that conservation does not select a charge value. Keep separate:

1. existence of a conserved generator;
2. invariant normalization as mass;
3. selection of its numerical value;
4. observational calibration.

Determine whether the owner recycling/constant-total-mass principle supplies any item beyond
conservation.

## 6. Anchor formulas

Verify or correct:

\[
X=\frac{GM_0}{c^2\mu_*}
=\frac{GM_0}{c^2\nu_*\delta_*},
\qquad
X=\left(\frac{V_0}{\nu_*}\right)^{1/3}.
\]

State exactly which quantities are derived, fixed, observed, or still unnormalized. Test whether
\(c\) alone, a dimensionless topological charge, or a dimensionless density root can form a length.

## 7. Required verdict

Return:

1. PASS/FAIL for sections 1–6;
2. corrected equations and any hidden scale input;
3. raw scripts and outputs;
4. one orbit verdict:
   - **WR-L \(X\) IS A PRE-SCALE CSN GAUGE MODULUS**;
   - **BOUNDARY/GLOBAL OBSTRUCTION BREAKS THE ORBIT**;
   - **CSN AND WR-L ARE INCONSISTENT**;
5. one bootstrap verdict:
   - **DIMENSIONLESS COMPACTNESS ONLY**;
   - **ABSOLUTE SCALE DERIVED**;
   - **BOOTSTRAP RESPONSE NOT YET FORMABLE**;
6. the smallest additional datum required if absolute scale remains open.

Stop after reporting. No numerical scan is warranted unless the audit first identifies a complete
off-shell action and boundary problem whose solution can break the scale orbit.

