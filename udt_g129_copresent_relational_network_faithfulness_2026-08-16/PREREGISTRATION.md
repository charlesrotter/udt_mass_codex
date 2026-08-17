# G129 preregistration — co-present relational-network faithfulness

Date: 2026-08-16

## Whole question

On a bounded regular four-dimensional Lorentzian region, does a complete compatible network of
calibrated observer-pair pullback metrics determine the ambient metric uniquely up to lawful
coordinate and frame gauge? Or can distinct ambient metric germs give exactly the same declared
pair network?

This tests whether the repeatedly stated “physical-history selection” gap is partly a reconstruction
category error. It does not ask the metric to choose a cosmology, fit observations, or invent a
dynamical selector.

## Exact bounded arena

At one regular event let `V` be a real four-dimensional vector space and let `g` be a Lorentzian
symmetric bilinear form. Each calibrated pair query supplies an injective map

```text
A_a : R^2 -> V
```

and its complete pair pullback

```text
h_a = A_a^T g A_a.
```

Define the linear restriction map

```text
M_A : Sym^2(V*) -> direct_sum_a Sym^2(R^2*),
M_A(k)_a = A_a^T k A_a.
```

The pointwise network is faithful exactly when `ker(M_A)=0`, equivalently when the exact design
matrix has rank ten.

On regular overlaps, supplied observer charts `F_i: U_i -> M` carry pullback metrics
`H_i=F_i^*g` and transition maps `f_ji=F_j^-1 o F_i`. The descent test requires

```text
f_ki=f_kj o f_ji,
f_ji^* H_j=H_i.
```

Only covers whose quotient is a regular Hausdorff second-countable manifold are included. Singular
fibers, caustics, cut loci, topology change, and branch aggregation are excluded.

## Metric-led versus free

Pinned by current UDT geometry:

- complete pair pullback before terminal reciprocal readout;
- Lorentz signature and regular calibrated pair planes;
- lawful overlap composition, reversal, and pullback covariance;
- terminal `phi_pair` and `c_eff/c_E` as outputs of each supplied `h_a`.

Free-and-explored certification data:

- the finite collection of pair planes at one event;
- exact rational Lorentz metric witnesses;
- exact rational invisible perturbations on rank-deficient networks;
- a finite regular chart-overlap toy cover.

No observational coefficient, source, action, bootstrap rule, history profile, angular amplitude,
`mu`, transfer law, or `X_max` profile is used.

## Exact tests

1. Build the exact restriction matrix in a fixed ten-component basis of `Sym^2(V*)`.
2. Verify that six clock-ruler planes with ruler directions
   `e1,e2,e3,e1+e2,e1+e3,e2+e3` have rank ten.
3. Reconstruct a generic exact rational Lorentz metric from those six pullbacks.
4. Verify basis covariance under an exact invertible change of ambient frame.
5. Verify that the three axial clock-ruler planes have rank seven and exhibit an exact
   three-dimensional invisible spatial-cross-term kernel.
6. Construct `g_epsilon=g+epsilon k` for an invisible nonzero `k`, verify identical declared pair
   pullbacks, retained Lorentz signature for the registered rational epsilon, and a changed
   invariant determinant or curvature surrogate only if one is independently justified.
7. Verify exact chart-transition cocycle and pullback descent on a finite affine overlap witness.
8. Verify that terminal reciprocal scalars alone are nonfaithful even when the full pair metrics
   are faithful by constructing two distinct regular `h` with equal `phi_pair`.
9. Construct two smooth scalar profiles that agree on a registered quiet interval and share the
   same registered end limits but differ on an intermediate compact region. This is a bounded
   counterexample to continuation rigidity from quiet overlap and endpoint behavior alone; it is
   not a spacetime solve.

## Independent route

A separate standard-library `Fraction` verifier must rebuild the design rows from bilinear
evaluation, compute ranks by independent Gaussian elimination, solve the faithful reconstruction,
verify the rank-deficient perturbation, and check the terminal-scalar and quiet-interval
counterexamples. It must not import SymPy or production code.

## Candidate landings

- `FULL_NETWORK_FAITHFUL_ON_DECLARED_REGULAR_COVER`: every declared complete pair network is
  automatically faithful without a coverage condition.
- `FAITHFUL_IFF_PAIR_PLANE_SPAN_HAS_RANK_TEN`: full pair pullbacks reconstruct the metric exactly
  when the restriction map has rank ten; rank-deficient networks possess an explicit invisible
  metric fiber.
- `PAIR_NETWORK_NOT_FAITHFUL_EVEN_AT_RANK_TEN`: two distinct symmetric forms survive identical
  full pullbacks despite a rank-ten design matrix.
- `TYPE_OR_ALGEBRA_FAILURE`: the declared restriction/descent problem is ill-typed or an exact
  certification gate fails.

## Certification gates

- preregistration committed before executable construction or outcome artifacts;
- exact production algebra passes every registered test;
- independent `Fraction` implementation agrees on ranks, reconstruction, and counterexamples;
- source hashes and package replay pass;
- repository premise verifier and regression suite pass;
- a fresh adversarial review is required before promotion beyond an internal result.

## Maximum conclusion

At most: a necessary-and-sufficient pointwise coverage criterion and a regular-overlap descent
statement showing when a complete observer-pair network reconstructs one metric up to isometry.
Failure of coverage may identify exact metric components invisible to that network. No unique
physical universe, metric dynamics, initial/boundary data, cosmology, observational prediction,
source, action, bootstrap law, `X_max`, matter, mass, or signalling claim can follow.
