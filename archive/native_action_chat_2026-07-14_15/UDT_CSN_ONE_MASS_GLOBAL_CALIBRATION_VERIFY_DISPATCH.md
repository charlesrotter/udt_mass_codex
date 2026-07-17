# Workstation dispatch — cold audit of the CSN one-mass global calibration theorem

## Scope

Audit the theorem that a complete dimensionless CSN solution plus a normalized \(G\)-bridge and one
observed electron mass can fix \(X\) and the overall action scale while leaving mass/size ratios as
predictions.

Read:

1. UDT_CSN_ONE_MASS_GLOBAL_CALIBRATION_MAP.md
2. UDT_CSN_ONE_MASS_GLOBAL_CALIBRATION_DERIVATION_RESULTS.md
3. verify_udt_csn_one_mass_global_calibration.py
4. verify_udt_csn_one_mass_global_calibration_out.txt

For provenance:

- UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md
- UDT_CSN_GLOBAL_SCALE_SELECTION_DERIVATION_RESULTS.md
- UDT_ELECTRON_CALIBRATION_BRIDGE_DERIVATION_RESULTS.md
- UDT_CSN_BOUNDARY_CHARGE_SELECTION_DERIVATION_RESULTS.md
- UDT_COMMON_SCALE_MATTER_EMERGENCE_DERIVATION_RESULTS.md

Do not load any observational value, identify the historical carrier as the electron, set
\(\widehat g=1\), alter LIVE.md/CANON.md, or start a GPU solve.

## 1. Static action and Hamiltonian scaling

Independently derive, for a complete CSN cell,

\[
S_{\rm on}=\mathcal A\frac{c\Delta t}{X}\ell,
\qquad
E=\frac{\mathcal A c}{X}\varepsilon,
\qquad
m=\frac{\mathcal A}{cX}\varepsilon.
\]

Audit the sign, constraints, boundary/corner terms, and whether the Hamiltonian generator equals the
negative on-shell static Lagrangian in the admissible action class. If not, determine whether the
\(1/X\) weight survives even when the coefficient changes.

## 2. Action-normalization census

For the most general finite set of dimensionless CSN invariants, test whether all dimensionful
coefficients can be factored as one \(\mathcal A\) times dimensionless ratios \(\lambda_a\).
Identify exceptions involving topological sectors, independent boundary normalizations, or
superselection constants. Determine which relative coefficients enter the field equations and
charges.

## 3. One-mass degeneracy

Verify that

\[
m_e=\frac{\mathcal A}{cX}\varepsilon_e
\]

is invariant under

\[
(\mathcal A,X)\mapsto(\lambda\mathcal A,\lambda X).
\]

Look for any already-derived UDT equation that breaks this orbit without a second normalized input.

## 4. \(G\)-bridge provenance

Audit

\[
\widehat g=\frac{G\mathcal A}{c^3X^2},
\qquad
\beta_i=\widehat g\varepsilon_i.
\]

Determine whether \(\widehat g\) is:

- a native dimensionless response calculable from the full equations;
- an overall charge-normalization convention;
- fixed only after observed \(G\);
- or an additional free dimensionless coupling.

Do not conflate dimensional uniqueness with dynamical derivation.

## 5. One-mass inversion and predictions

Verify:

\[
X=\frac{Gm_e}{c^2\widehat g\varepsilon_e},
\qquad
\mathcal A=\frac{Gm_e^2}{c\widehat g\varepsilon_e^2},
\]

\[
\frac{M_{\rm total}}{m_e}
=\frac{\varepsilon_U}{\varepsilon_e}
=\frac{\mu_U}{\beta_e},
\qquad
R_e=\sigma_eX.
\]

List every condition required for these ratios to share a common native normalization. Test whether
one accepted mass genuinely remains only a calibration rather than a fitted action coefficient.

## 6. Finite dimensionless size

Audit

\[
E(R;X)=\frac{\mathcal A c}{X}\varepsilon(R/X),
\qquad
\varepsilon'(\sigma_*)=0.
\]

Determine whether complete-cell topology/geometry can in principle produce a finite \(\sigma_*\)
without local scale breaking. Contrast with the exact unbounded-flat quartic-only
\(\varepsilon=k/\sigma\) result. Do not construct a target-shaped potential.

## 7. Numerical readiness

State whether the present repo supplies:

1. a complete CSN action and relative coefficients;
2. a complete global domain/interface law;
3. a native charge and \(\widehat g\);
4. a carrier/emergent sector and data-blind electron-branch criterion.

If any is absent, no numerical value may be sought.

## 8. Required verdict

Return:

1. PASS/FAIL for sections 1–7;
2. corrected equations and raw scripts/output;
3. one calibration verdict:
   - **ONE-MASS GLOBAL CALIBRATION THEOREM HOLDS**;
   - **ONE MASS STILL LEAVES AN UNFIXED DIMENSIONLESS BRIDGE**;
   - **ENERGY/CHARGE SCALING INVALID**;
4. one finite-size verdict:
   - **FINITE DIMENSIONLESS SIZE ALLOWED**;
   - **CSN EXCLUDES LOCALIZED MATTER**;
   - **BOUNDARY/DOMAIN PREVENTS A VERDICT**;
5. the exact next analytic object required before numerics.

Stop after reporting. No frontier or canon update without Charles's verdict.

