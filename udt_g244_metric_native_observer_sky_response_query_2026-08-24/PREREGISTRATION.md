# G244 preregistration — metric-native observer-sky response query

Date: 2026-08-24

Status: `PREREGISTERED_BEFORE_G244_DERIVATION__OBSERVATIONAL_OUTCOMES_CLOSED`

## Question and regime

Derive the intrinsic angular response carried by the G188 matrix Jacobi map on one supplied smooth,
regular, finite, noncaustic affine null observation sheet. The construction must remain valid for a
generic full two-by-two Jacobi map and must not diagonalize, linearize, fit an amplitude, or select
G225 pointwise screen comparison as physical transport.

## Preregistered mathematical objects

For a regular branch endpoint let

```text
D : S_observer -> S_source
H = D^dagger D
A = sqrt(det H) = abs(det D)
C = H/A
shear_power = (tr(H)^2)/(4 det(H)) - 1
parity = sign(det D).
```

The expected types are:

- `H`: a positive symmetric covariant response tensor on the observer celestial screen;
- `A`: positive geometric area response;
- `C`: positive determinant-one shape tensor;
- `shear_power`: nonnegative, dimensionless, and zero exactly for conformal/isotropic screen maps;
- `parity`: a separate regular-branch orientation sign.

For a supplied normalized positive reference measure `Q` and positive area field `A`, define the
explicitly chosen geometric-area query

```text
dP_A = A dQ / integral(A dQ)
f_A = dP_A/dQ
w_K^area = <K,(f_A-1) tensor (f_A-1)>_Q / <K,1 tensor 1>_Q.
```

This is a geometric query of the metric area field. It is not yet an observed galaxy process. A
catalogue identification would additionally require a source/incidence and detector/transfer
contract.

## Required identities

The production and independent routes must establish:

1. `det(H)=det(D)^2` and `det(C)=1` on every regular case;
2. under endpoint screen bases `D -> Q_s^T D Q_o`, source gauge cancels and
   `H -> Q_o^T H Q_o`; `A`, `shear_power`, and parity are invariant;
3. under positive common screen scaling `D -> c D`, `A -> c^2 A`, while `C`,
   `shear_power`, and parity are unchanged;
4. `shear_power >= 0`, with equality exactly when the two singular values agree;
5. an isotropic/conformal response gives `C=I`, zero shear power, and an angularly constant `A`
   cancels from the normalized area query;
6. a nonconstant positive area field can give a nonzero reference-projected curve without a fitted
   coefficient;
7. supplied segment composition occurs in the full G226 phase. If
   `M_ij=[[A_ij,B_ij],[C_ij,D_ij]]`, then
   `B_20=A_21 B_10+B_21 D_10`; generally `B_20 != B_21 B_10`;
8. no inverse position block is used; at `det(D)=0`, `H` remains semidefinite but `C`,
   `shear_power`, and the regular density formula leave scope while the full phase remains lawful;
9. direct reciprocal redshift is untouched and no observational outcome is read.

## Verification contract

- Production: symbolic identities plus exact rational finite-dimensional cases and one fixed
  coefficient-free finite-cell area-query witness.
- Independent: standard-library `Fraction` implementation, importing neither production code nor
  production output, over at least 5,000 regular matrices, endpoint gauges, positive rescalings,
  and symplectic phase compositions.
- Hostile catches: wrong transpose, missing absolute determinant, fitted angular coefficient,
  diagonal-only reduction, scalarization that drops `C`, multiplying Jacobi position blocks,
  inverting at a caustic, promoting G225 transport, deriving a source/detector law, opening BOSS/CMB,
  or importing P1/G116/G189/`X_max`/Lambda-CDM/protected work.

## Preregistered landings

- `METRIC_NATIVE_OBSERVER_SKY_AREA_SHAPE_QUERY_DERIVED_CONDITIONALLY__NO_FITTED_ANGULAR_COEFFICIENT__CATALOG_IDENTIFICATION_AND_HISTORY_OPEN`
- `ALGEBRA_OR_COVARIANCE_FAILURE__NO_SCIENTIFIC_LANDING`
- `SCAFFOLDING_OR_OUTCOME_LEAKAGE__STOP`

## Scope and maximum conclusion

A passing result will show that the complete metric already supplies a native angular area/shape
response on any supplied regular null sheet, and supplies a coefficient-free geometric angular
projection after the reference query is declared. It will not select the metric history, source or
observer population, null sheet, detector semantics, feature scale, or physical catalogue map. It
will not open or compare BOSS/CMB outcomes.

