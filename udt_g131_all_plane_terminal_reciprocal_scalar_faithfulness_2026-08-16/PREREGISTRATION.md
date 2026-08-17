# G131 preregistration — all-plane terminal reciprocal-scalar faithfulness

Date: 2026-08-16

## Whole question

Let `V` be a four-dimensional real vector space, let `g` be a Lorentz bilinear form, and let a
known calibrated clock-ruler embedding be `A=[t,r]:R^2->V`. On the regular pair stratum define

```text
h_g(A)=A^T g A,
Phi_g(A)=(1/4) log[(-det h_g(A))/(h_g(A)_00)^2].
```

If `Phi_g(A)=Phi_g_tilde(A)` for every plane in a shared open all-plane certification domain, must
`g_tilde=g`, must `g_tilde=Omega^2 g`, or can a larger non-conformal kernel survive?

This tests only the information content of the founded terminal reciprocal scalar. It does not
assert that the all-plane certification domain is a physical observer population or that its
values are founded.

## Exact bounded regime

- one regular four-dimensional Lorentzian tangent space;
- known fixed plane embeddings `A`, not metric-renormalized query vectors;
- a nonempty shared open set of clock directions and ruler directions on which both induced pair
  metrics are Lorentzian and the terminal scalar is defined;
- positive smooth conformal factors for the pointwise extension.

Omitted: singular/null pair planes, global topology, cut loci, branch populations, history
dynamics, action, source, transfer, matter, bootstrap, observations, `X_max`, and signalling.

## Metric-led versus free

Pinned by current theory:

- the complete pair pullback `h=A^T g A`;
- the terminal scalar formula above;
- `c_eff/c_E=exp(-2 Phi)` on a supplied regular calibrated pair;
- G129 full-pullback faithfulness and G130's certification/ownership distinction.

Free-and-tested only for certification:

- exact rational Lorentz metrics and vectors;
- finite plane sets used as computational witnesses;
- a positive nonconstant conformal factor used as an independence witness.

No fitted coefficient, source distribution, profile, or desired observational target enters.

## Preregistered theorem and counterexample gates

1. **Conformal invariance:** prove directly that `Phi_(lambda g)(A)=Phi_g(A)` for every positive
   scalar `lambda`, so exact metric faithfulness is impossible from `Phi` alone.
2. **Full kernel classification:** either prove that equality on a shared open all-plane domain
   forces `g_tilde=lambda g` with `lambda>0`, or exhibit an exact non-conformal survivor.
3. **Nonlinear proof:** a Jacobian/rank calculation may diagnose but cannot certify the full
   theorem; the load-bearing argument must use the exact rational scalar functional.
4. **Common-scale witness:** use a nonconstant positive `Omega(x)` to show pointwise identical
   `Phi` fields can coexist with distinct complete metrics and generally distinct curvature.
5. **`c_E` ownership:** determine from the formula and founding source whether fixed observed `c_E`
   removes the conformal factor or only calibrates clock and ruler units. Do not silently promote
   `c_E` into a pointwise norm/volume datum.
6. **Independent route:** reproduce the finite-dimensional identity and conformal witness without
   importing the production simplification.

## Candidate landings

- `ALL_PLANE_TERMINAL_SCALAR_METRIC_FAITHFUL`
- `ALL_PLANE_TERMINAL_SCALAR_CONFORMAL_FAITHFUL_ONLY__COMMON_SCALE_OPEN`
- `ALL_PLANE_TERMINAL_SCALAR_HAS_LARGER_NONCONFORMAL_KERNEL`
- `TYPE_OR_DOMAIN_FAILURE`

## Falsification and maximum conclusion

The conformal-only landing fails if one exact non-conformal pair of Lorentz forms has equal
terminal scalars on the declared shared open domain. Metric-faithful landing fails under any
positive conformal rescaling. A local theorem cannot select a physical conformal factor, history,
query family, or global completion.

At most G131 may classify the pointwise kernel of the complete all-plane terminal scalar map and
state what additional type of pair datum is needed to recover common scale.
