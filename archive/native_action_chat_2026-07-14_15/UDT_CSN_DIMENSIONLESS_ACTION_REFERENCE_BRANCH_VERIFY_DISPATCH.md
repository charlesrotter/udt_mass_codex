# Workstation dispatch — cold audit of the CSN dimensionless action and reference branch

## Scope

Audit the quartic matter-action census, conditional area-form uniqueness, dimensionless
charge-to-energy response, and data-blind reference-particle criterion.

Read:

1. UDT_CSN_DIMENSIONLESS_ACTION_REFERENCE_BRANCH_MAP.md
2. UDT_CSN_DIMENSIONLESS_ACTION_REFERENCE_BRANCH_DERIVATION_RESULTS.md
3. verify_udt_csn_dimensionless_action_reference_branch.py
4. verify_udt_csn_dimensionless_action_reference_branch_out.txt

For provenance:

- UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md
- UDT_CSN_ONE_MASS_GLOBAL_CALIBRATION_DERIVATION_RESULTS.md
- UDT_COMMON_SCALE_MATTER_EMERGENCE_DERIVATION_RESULTS.md
- matter_carrier_provenance_audit_results.md
- noNull_energy.py

Do not load observational masses, adopt \(S^2\), promote rank-one-zero to a postulate, fit
\(\lambda_4\), alter LIVE.md/CANON.md, or start numerics.

## 1. Overall normalization and response

Independently verify that the overall action factor cancels from the classical equations while
relative dimensionless coefficients survive. Determine the exact conditions under which a
dimensionless geometric charge \(q_i\) and energy \(\varepsilon_i\) share one native normalization,
so that

\[
\widehat g=\frac{q_i}{\varepsilon_i}.
\]

Challenge whether boundary improvements or topological terms make the ratio branch-dependent or
ambiguous.

## 2. Covariant quartic invariant census

For a dimensionless \(S^2\) probe, classify every parity-even scalar built from four first
derivatives at this order, modulo target identities and total derivatives. Verify whether

\[
Q_1=(\operatorname{tr}M)^2,\qquad Q_2=\operatorname{tr}(M^2)
\]

span the class. Identify any curvature-improved or parity-odd terms separately without adopting
them.

## 3. Pullback identity

Re-derive, with all index-sum normalizations,

\[
F_{ij}F_{ij}=Q_1-Q_2
\]

on a static positive spatial slice. State how the identity and sign change in the full Lorentzian
action.

## 4. Positivity cone

Prove or correct the claimed necessary-and-sufficient conditions

\[
a+b\ge0,\qquad 2a+b\ge0
\]

for

\[
a(x+y)^2+b(x^2+y^2)\ge0
\]

for all \(x,y\ge0\). Audit boundaries, zero directions, coercivity, and whether static positivity
has any implication for time-live hyperbolicity.

## 5. Area-only conditional uniqueness

Test whether zero cost for every rank-one derivative field forces

\[
a+b=0
\quad\Longrightarrow\quad
\rho_4\propto Q_1-Q_2=F^2.
\]

Search the existing UDT foundation for an actual premise implying rank-one-zero. If none exists,
retain CHOSE status. Determine whether a target other than \(S^2\) changes the result.

## 6. Relative coupling and global selection

Audit the conditional family

\[
S=\mathcal A[I_C+\lambda_4 I_{F^2}+I_\partial].
\]

Determine whether any current bootstrap, reciprocity, boundary, or regularity equation fixes
\(\lambda_4\). Distinguish an internally selected existence eigenvalue from fitting to observed
matter.

## 7. Reference-particle criterion

Determine whether “lightest stable nontrivial localized branch” is well-defined data-blindly in a
complete UDT action. Check degeneracy, disconnected topological sectors, boundary dependence, and
whether massless/delocalized branches obstruct an ordering.

Return a separate verdict on whether equating its mass to \(m_e\) is:

- a legitimate one-number calibration;
- an unearned electron identification;
- or both in their distinct scopes.

## 8. Existing carrier audit

Using only saved provenance, determine exactly which elements of

\[
(\varepsilon_\star,\sigma_\star,\beta_\star)
\]

the corrected \(Q_H=1\) carrier currently supplies. Preserve all conditional action, box, mask,
carrier, and static-stability stamps.

## 9. Required verdict

Return:

1. PASS/FAIL for sections 1–8;
2. corrected equations and raw scripts/output;
3. one action verdict:
   - **\(F^2\) DERIVED WITHOUT EXTRA PREMISE**;
   - **AREA-ONLY CONDITIONAL UNIQUENESS**;
   - **QUARTIC CENSUS/POSITIVITY INCORRECT**;
4. one calibration verdict:
   - **DATA-BLIND REFERENCE BRANCH DEFINABLE**;
   - **BRANCH ORDERING UNDERDETERMINED**;
5. one electron verdict:
   - **REFERENCE MASS CALIBRATION LEGITIMATE; ELECTRON ID OPEN**;
   - **ELECTRON BRANCH DERIVED**;
   - **CALIBRATION ITSELF NOT YET WELL-POSED**;
6. the exact next analytic discriminator.

Stop after reporting. No canon/frontier update without Charles's verdict.

