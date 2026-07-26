# Preregistration: founded-pair first-jet one-form atlas

Date: 2026-07-26

Question type: `METRIC_LED_OBSERVATION`

Repository base: `e869a980a8b2cb1fb06d41e227aa62dec4e12e7e`

## Whole question

Given a supplied smooth founded ordered pair field `(u,n)` in a Lorentzian metric `g`, what is the
complete pointwise vocabulary of real spacetime one-forms that is:

- linear in the first derivatives `nabla u` and `nabla n`;
- algebraic in `g,u,n` and the screen tensors;
- equivariant under the unresolved screen `SO(2)` frame; and
- available without adding a profile, connection, action, source, carrier, density, boundary, or
  preferred solution?

For every resulting one-form, classify orientation dependence, ruler-line reversal, generic closure,
exactness, normalization, and possible identification with the founded reciprocal depth.

This is a first-jet availability atlas. It does not assume that a global founded pair field has
already been selected.

## Frozen notation and candidate universe

Use signature `(-,+,+,+)`, with

```text
g(u,u)=-1, g(n,n)=+1, g(u,n)=0,
s=I+u tensor u_flat-n tensor n_flat,
epsilon_S=spacetime_volume_contracted_with_u_and_n.
```

Decompose the pair derivatives as

```text
omega_a = n^c nabla_a u_c = -u^c nabla_a n_c,
U_(aA)  = s_A^c nabla_a u_c,
N_(aA)  = s_A^c nabla_a n_c.
```

The 22 preregistered `SO(2)`-equivariant candidate maps are frozen in
`ONE_FORM_BASIS.tsv`. No candidate may be removed because it is not closed or does not resemble a
clock law. If an omitted independent map is found, the preregistration fails and the outcome stops.

## Exact tests

1. Derive the constrained first-jet dimension of an orthonormal pair and verify the
   `omega + U + N = 4+8+8=20` decomposition.
2. Compute the rank of the 22 candidate equivariant linear maps from the 20-dimensional pair jet to
   a four-dimensional covector; retain every independent map.
3. Classify the `SO(2)` versus orientation-free `O(2)` vocabularies.
4. Classify parity under `n -> -n`, noting that the projector generator is insensitive to ruler-axis
   sign while an oriented path may retain it.
5. Confirm that every algebraic zero-jet scalar made only from the normalized pair Gram data is
   constant, so its differential supplies no nonzero first-jet depth.
6. Use valid flat-metric Lorentz-frame Taylor jets, not arbitrary inconsistent derivatives, to test
   whether any nonzero linear combination of the 22 maps is universally closed.
7. Independently repeat the map-rank, parity, and closure-rank calculations with exact rational
   arithmetic and a separately written implementation.
8. Separate the metric-skew pair boost connection `omega` from the metric-self-adjoint founded
   reciprocal generator. Test boost-only reductions without identifying boost rapidity with founded
   depth.
9. Regrade the historical conformal/Weyl reciprocal-connection route under the current inactive
   strong-local-CSN premise.
10. Audit whether current Reciprocity, observed `c_E`, `G_obs`, finite-cell, or bootstrap records fix
    any coefficient, orientation, closure condition, or global pair section.

## Closure witness method

The production closure test will generate exact second-order Taylor jets

```text
F(x)=exp(K(x)),
K(x)=x^a A_a + 1/2 x^a x^b B_ab,
```

with every `A_a` and symmetric `B_ab` in `so(1,3)`, and set

```text
u(x)=F(x)e_0,
n(x)=F(x)e_1.
```

These witnesses obey the orthonormal constraints identically. The stacked exact rank of the exterior
derivatives of the 22 one-forms decides whether a universally closed coefficient combination survives
in this bounded class. A rank defect is a positive candidate and must be reported, not tuned away.

## Premise and interpretation guards

- The pair field is `SUPPLIED_CONDITIONAL_INPUT`, not globally selected.
- The Levi-Civita derivative is `pinned-by-THEORY given g`; no nonmetric connection is introduced.
- Screen orientation is classified both with `SO(2)` and without it (`O(2)`); neither is selected.
- All coefficients are `free-and-explored` symbolically.
- `c_E` and `G_obs` remain observed calibration anchors.
- Strong local CSN is inactive under current premise precedence.
- Closure is characterized, not used to discard nonclosed forms.
- No action, source, carrier, density, bootstrap equation, boundary, `X_max`, mass, or dynamics enters.

## Falsification and maximum conclusion

The audit is falsified by an omitted independent first-jet one-form, invalid Lorentz-frame witness,
incorrect rank/parity, or an unrecorded current premise that uniquely selects a nonzero closed founded
form.

At most the audit may derive the complete bounded first-jet vocabulary and classify whether current
UDT structure selects a normalized closed reciprocal form within it. It may not infer that no
higher-jet or global solution can supply depth, adopt a pair field or connection, select a branch,
or promote any downstream physics.

CPU exact algebra only. No GPU, canonization, navigation edit, or repository reorganization.
