# G269 preregistration — null-transport mutual-clock ownership

Date: 2026-08-26

## Frozen question

On one supplied regular affine null relation, does the complete metric independently construct a
reversal-even mutual-clock scalar by transporting one endpoint's metric-unit clock to the other?
If so, what is its exact relation to the already-derived directional clock ratio and to the
transported pair-plane screen component?

## Frozen type definitions

Let `P_AB` be Levi-Civita parallel transport along the supplied future-null branch `gamma:A->B`,
with affine tangent `k`. Let

```text
omega_A = -g(k_A,U_A) > 0
omega_B = -g(k_B,U_B) > 0
r_AB = omega_A/omega_B
delta_AB = -log(r_AB)
```

as in G220. Normalize the initial null generator by `K_A=k_A/omega_A` and define

```text
n_A = K_A-U_A
U_tilde = P_AB U_A
n_tilde = P_AB n_A.
```

The transport scalar and its inverse are

```text
Gamma_PT = -g(U_tilde,U_B)
M_PT = 1/Gamma_PT.
```

Decompose `U_B` into the transported Lorentzian plane and its positive screen:

```text
U_B = Gamma_PT U_tilde + a n_tilde + W,
W perpendicular to U_tilde and n_tilde.
```

`W^2=g(W,W)>=0` is a metric-derived transported-screen mismatch. It is not a Jacobi area, source
pattern, fitted angular coefficient, or post-readout orchestra term.

## Preregistered landings

1. `N0__NO_CANONICAL_TRANSPORT_MUTUAL_SCALAR`: affine normalization, reversal, or path typing
   prevents `Gamma_PT` from being a well-defined scalar even after the null branch is supplied.
2. `N1__UNIVERSAL_SECH_EQUALITY`: `M_PT=sech(delta_AB)` for every supplied regular null relation in
   the full Lorentzian arena, with no remaining screen condition.
3. `N2__SCREEN_INTERLOCK`: `M_PT` is a metric-owned bilocal scalar, obeys a sharp coefficient-free
   inequality against `sech(delta_AB)`, and equality holds exactly on the transported-planar
   stratum `W=0`.
4. `N3__ALGEBRA_OR_TYPE_FAILURE`: the proposed decomposition, sign, reversal, or comparison with
   the G220 ratio is inconsistent.

## Required derivations and controls

Production must establish or refute:

1. `n_A` is unit spacelike and orthogonal to `U_A`; transport preserves the orthonormal pair;
2. `Gamma_PT>=1`, affine-generator rescaling invariance, and path-reversal evenness;
3. the exact target decomposition, normalization identity, and frequency contraction;
4. the relation among `Gamma_PT`, `r_AB`, and `W^2`;
5. the induced relation or inequality for `M_PT`;
6. the necessary-and-sufficient equality condition;
7. a planar moving-flat control;
8. a primary static-radial control;
9. a flat transverse family with fixed `r_AB` and varying nonzero `W`, proving whether the two
   constructions are genuinely independent in dimension at least three.

An implementation-distinct standard-library verifier must use exact rational arithmetic on at
least 10,000 positive `(r,w)` cases, import no production module, and read no production result.

Hostile mutations must catch at least: reversed frequency ratio, missing inverse in `M_PT`, wrong
sign in the Lorentz decomposition, deleted screen term, negative screen norm, universal equality
with nonzero screen, loss of reversal evenness, affine-scale dependence, conflation with Jacobi
area, and promotion to query/history selection.

## Premise classification

- metric, endpoint unit clocks, null branch, and affine tangent: `SUPPLIED_CONDITIONAL_QUERY`;
- proper-clock frequency ratio: `DERIVED_CONDITIONAL` from G220;
- Levi-Civita transport and its isometry: `DERIVED_FROM_SUPPLIED_METRIC`;
- inverse transported Lorentz factor as the named mutual-clock protocol: `WORKING_OPERATIONAL_READOUT`
  to be tested for coefficient-free metric ownership, not canonized;
- physical population of null relations and histories: `OPEN`;
- observations, distance, `X_max`, source, matter, transfer, and canon: `OMITTED`.

## Certification and falsification contract

The result fails if any displayed identity depends on an affine normalization, if mathematical path
reversal changes `Gamma_PT`, if the planar equality fails, if a nonzero transverse screen component
is compatible with a claimed necessary-and-sufficient planar condition, or if a conclusion is
widened beyond supplied regular null relations.

## Frozen maximum conclusion

At most, G269 may derive one coefficient-free bilocal mutual-clock transport scalar and its exact
screen-conditioned relation to the directional reciprocal clock ratio on a supplied regular null
branch. It may regrade the G267 `sech` projection on planar versus nonplanar strata. It may not
select the null query, observers, metric history, distance law, `X_max`, observation, source, matter,
radiative transfer, signalling mechanism, or canon.
