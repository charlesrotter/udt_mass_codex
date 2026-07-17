# Workstation dispatch — cold audit of CSN finite-boundary charge selection

## Scope

Audit the claim that CSN fixes inverse-length boundary weight but does not select a unique finite
charge, and that the Euler \(4/X\) result is a one-sided WR-L static-patch readout rather than the
current canonical finite-cell charge.

Read:

1. UDT_CSN_BOUNDARY_CHARGE_SELECTION_MAP.md
2. UDT_CSN_BOUNDARY_CHARGE_SELECTION_DERIVATION_RESULTS.md
3. verify_udt_csn_boundary_charge_selection.py
4. verify_udt_csn_boundary_charge_selection_out.txt

For provenance:

- UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md
- UDT_ELECTRON_CALIBRATION_BRIDGE_DERIVATION_RESULTS.md
- UDT_RECIPROCAL_C_CONFORMAL_ACTION_DERIVATION_RESULTS.md
- UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md
- the canonical fold/horizon scope in CANON.md, read-only

Do not alter LIVE.md or CANON.md, fit a coefficient, declare the WR-L horizon a hard boundary, adopt a
carrier, or start F/G.

## 1. Reduced homogeneity

Independently prove or refute that every local first-jet reciprocal endpoint energy with CSN weight
has

\[
B=\frac{\gamma}{r}b(A,rA').
\]

Check whether coordinate covariance or reparameterization changes this reduced classification.
Repeat with the minimum higher-jet arguments required by a fourth-order bulk action.

## 2. Endpoint variation

Re-derive

\[
\delta(S_C+B)\big|_\partial
=\left(P_0+\frac{\gamma}{r}b_A\right)\delta A
+\left(P_1+\gamma b_v\right)\delta A'
\]

and audit fixed-jet, Dirichlet, Neumann, mixed, and free-jet classes. Determine whether any live UDT
boundary class fixes \(b(0,-1)\), not merely its derivatives.

## 3. Covariant countermodel challenge

The supplied reduced family

\[
b_k=k(1-A^2)
\]

is only an inverse-problem counterexample. Either:

1. construct at least two full covariant CSN-compatible boundary improvements with the same live
   boundary data but different finite charges; or
2. prove that covariance, derivative order, parity, null regularity, and the declared variation
   class uniquely exclude the reduced ambiguity.

Include intrinsic curvature, trace-free extrinsic-curvature, Euler/Chern, corner, and null-boundary
possibilities as mathematical classes. Do not adopt them as UDT physics without derivation.

## 4. Euler completion

Verify

\[
b_E=4(A-1)(rA')
\]

and its values:

\[
b_E(0,-1)=4,\qquad b_E(1,v)=0.
\]

Compute the complete covariant Euler contribution for:

- a stretched timelike surface approaching the WR-L horizon;
- a smooth two-region continuation through the causal surface;
- the canonical odd-fold quotient;
- a one-copy physical boundary;
- time-slab corners.

Determine whether the \(4/X\) survives, cancels, becomes topological, or diverges in each ontology.

## 5. Clock and endpoint scaling

Audit

\[
S_B=c\Delta t\,\frac{\gamma k}{X}
=\gamma k\,\Delta\tau,
\qquad
\Delta\tau=\frac{c\Delta t}{X}.
\]

Determine which quantity is fixed in an allowed endpoint variation and whether any honest
scale-neutral transversality equation selects \(X\).

## 6. Charge normalization

Separate:

1. boundary functional shape;
2. additive reference subtraction;
3. multiplicative action normalization;
4. physical time normalization;
5. identification with mass and \(G\).

Test whether accepting one observed mass can fix only item 3 after items 1, 2, 4, and 5 are derived,
or whether additional ambiguities survive.

## 7. Required verdict

Return:

1. PASS/FAIL for sections 1–6;
2. corrected equations and raw scripts/output;
3. one uniqueness verdict:
   - **UNIQUE CSN BOUNDARY GENERATOR DERIVED**;
   - **INVERSE-\(X\) WEIGHT ONLY; FUNCTION/NORMALIZATION OPEN**;
   - **REDUCED COUNTERFAMILY FAILS FULL COVARIANCE BUT UNIQUENESS STILL OPEN**;
4. one ontology verdict:
   - **WR-L \(4/X\) SURVIVES AS PHYSICAL BOUNDARY CHARGE**;
   - **ONE-SIDED STATIC-PATCH READOUT ONLY**;
   - **EULER TERM CANCELS/IS TOPOLOGICAL**;
5. whether any current continuum problem can compute \(\beta_e\);
6. the smallest remaining analytic fork.

Stop after reporting. No numerical solve or frontier update without Charles's verdict.

