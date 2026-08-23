# G231 preregistration — Cartan regional realization bridge

Date: 2026-08-23
Status: `PRE_OUTCOME__METRIC_LED__EXTERIOR_SYSTEM_AND_SYMBOL_AUDIT`

## Frozen question

Determine the smallest complete input type for locally realizing one regional Lorentz metric from
the G227--G230 curvature-jet grammar. Test whether a bare supplied curvature field closes the
torsion-free Cartan system, or whether a compatible directional-derivative/classifying law is
required.

## Frozen structure equations

Work on the local orthonormal-frame bundle and fix

```text
d theta^a = - omega^a_b wedge theta^b
d omega^a_b = - omega^a_c wedge omega^c_b
              + (1/2) R^a_bcd theta^c wedge theta^d
omega_ab = -omega_ba.
```

Curvature-component differentiation is typed as

```text
d R_abcd
 = R_abcd;e theta^e
   + omega^p_a R_pbcd + omega^p_b R_apcd
   + omega^p_c R_abpd + omega^p_d R_abcp,
```

with the sign checked directly against the covariant-derivative convention. Higher derivative
coefficients are introduced only when exterior closure requires them.

## Required derivations

1. Apply `d^2=0` to the solder equation and derive the algebraic first Bianchi identity.
2. Apply `d^2=0` to the connection equation and derive covariant differential Bianchi.
3. Differentiate the curvature-component equation and derive the antisymmetric second-derivative
   Ricci commutator, with the G230 sign convention.
4. State the recursive prolonged system for `nabla^k R` and distinguish identities from supplied
   values.
5. Prove the input trilemma:
   - moving-frame curvature without frame/derivative carry is incomplete;
   - curvature relative to an already supplied coframe is evaluative/tautological;
   - curvature plus a compatible classifying derivative law defines the actual realization problem.
6. Type the finite-classifying-data and analytic formally-integrable local-existence routes without
   claiming smooth generic or global existence.

## Exact checks

An implementation independent of G227--G230 production must rebuild the exterior symbol maps and
verify:

- torsion-closure map `Lambda^2 V* tensor so(1,3) -> V tensor Lambda^3 V*` has source dimension 36,
  rank 16, and kernel dimension 20;
- differential-Bianchi map on `V* tensor K` has dimension 80, rank 20, and kernel 60;
- the G230 second-prolongation dimension/rank closure is reproduced or checked from an independent
  full-slot construction, not asserted from prose;
- constant-curvature data close with zero horizontal derivative as a finite-type control;
- a mutation omitting directional derivative data, vertical Lorentz action, algebraic Bianchi,
  differential Bianchi, or Ricci commutation is caught.

## Preregistered landings

```text
A_CARTAN_REGIONAL_BRIDGE__BARE_R_NOT_CLOSED__CLASSIFYING_DERIVATIVE_DATA_REQUIRED
  The exterior system reproduces G227--G230 as successive integrability conditions. Bare moving-
  frame curvature does not close the regional problem. Finite classifying data satisfying the
  algebroid identities, or an analytic formally integrable prolongation, supplies a conditional
  local realization route.

B_BARE_CURVATURE_FIELD_CLOSES_REGIONAL_SYSTEM
  R values alone determine all required horizontal and vertical carry and the Cartan system closes
  without additional derivative/classifying data.

C_EXTRA_OBSTRUCTION_OR_RANK_MISMATCH
  The exterior closure produces a constraint not present in the G227--G230 grammar or the symbol
  ranks fail to match.

D_TYPING_OR_CONVENTION_FAILURE
  Frame-bundle typing, signs, or the claimed realization theorem cannot be made precise; no bridge
  is banked.
```

## Certification and hostile contract

- Exact rational or integer exterior/symbol algebra only.
- Production and independent implementations may share index conventions but not construction code.
- Every standard theorem must be cited with its analytic/smooth, local/global, and finite/infinite-
  type hypotheses.
- Hostiles must catch omitted frame carry, omitted derivative law, deleted Bianchi stages, reversed
  Ricci sign, and promotion of conditional local realization into value generation or history.
- Fresh adversarial review must distinguish a regional realization architecture from an actual
  realized UDT history.

## Maximum conclusion

G231 may identify the correct regional integration architecture and prove exact agreement between
its first prolongations and G227--G230. It may not generate curvature values, select a classifying
law, prove an unconditional smooth or global realization, populate observer relations, select
transport, derive dynamics, action, source, matter, bootstrap, boundary, `X_max`, transfer,
observation, mass, signalling, or a physical/global history.
