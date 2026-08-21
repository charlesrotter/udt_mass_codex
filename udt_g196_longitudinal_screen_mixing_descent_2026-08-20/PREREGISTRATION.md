# G196 preregistration — longitudinal screen-mixing descent

Date: 2026-08-20

## Whole question

Does the G195 arbitrary-real screen-mixing theorem survive the smallest spatial extension

\[
\theta^0=a(\eta)d\eta,\qquad \theta^1=a(\eta)dz,\qquad
\theta_{\rm screen}=a(\eta)\left[dX+M(\eta,z)X(d\eta+dz)\right]
\]

on the same supplied central outgoing germ

\[
\gamma(s)=(\eta,z,p,w)=(s,s,0,0)?
\]

Here `a>0` is arbitrary real `C3`, and `M=S+Omega` is an arbitrary real `2x2` `C2` matrix field
in `(eta,z)`. This is metric-led: the four-dimensional metric, Levi-Civita connection, curvature,
screen transport, and Jacobi equation must be reconstructed from the displayed coframe.

## Fixed and omitted structure

- `p=w=0`, outgoing `+z` germ: `CHOSE_QUERY`.
- `a=a(eta)>0`: `FREE_AND_EXPLORED`; spatial common-scale dependence is omitted.
- `M=M(eta,z)`: `FREE_AND_EXPLORED`; no profile, coefficient, sign, or regime shape is selected.
- completed-pair Dual Reciprocity: `WORKING_FOUNDATIONAL_CLARIFICATION` inherited from G176.
- P1, G116, G189, observations, transfer, source, action, matter, bootstrap, and `X_max`: omitted.
- transverse `(p,w)` dependence, another germ, global completion, and physical pair population: open.

## Preregistered outcomes

1. `NULL_DIRECTIONAL_DESCENT__FACTORIZATION_AND_NO_CAUSTIC_SURVIVE`
   - the central connection is the G195 connection evaluated on `M(s,s)`;
   - curvature depends on spatial variation only through
     `dot(M)=(partial_eta+partial_z)M` restricted to the germ;
   - the ordered matrix factorization survives with `d/ds` and `M_bar(s)=M(s,s)`;
   - the positive-Gram no-nonvertex-caustic proof survives.
2. `SPATIAL_GRADIENT_ADDS_NONFACTORIZING_TERMS__G195_BOUNDARY_FOUND`
   - an independently reconstructed term involving `partial_eta-partial_z`, a separately weighted
     `partial_z`, or another spatial jet survives and prevents the G195 factorization.
3. `PAIR_OR_AFFINE_FAILURE`
   - the central pullback, affine null germ, frequency, or regular screen typing changes.
4. `TYPE_OR_VERIFICATION_FAILURE`
   - exact and independent calculations cannot be reconciled within preregistered tolerances.

## Certification and falsification contract

The production derivation must use the full nonlinear metric and direct Christoffel/Riemann
contraction. It must not obtain G196 by textual substitution into G195.

An independent implementation must reconstruct metric jets numerically without importing the
production module or reading its result. It must sample named controls and seeded smooth two-variable
histories with nonzero independent `partial_eta M`, `partial_z M`, mixed derivatives, symmetric
strain, and antisymmetric rotation.

The null-directional-descent outcome is falsified by any of:

- a nonzero affine-ray residual;
- a central connection inconsistent with the exact metric reconstruction;
- a tide component not reproduced by the directional restriction `M_bar(s)=M(s,s)`;
- a nonzero ordered-factorization residual;
- a failed positive-Gram representation or a nonvertex determinant zero in the declared regular
  interval;
- failure of an explicit hostile control that reverses the null derivative, drops `partial_z M`,
  forces symmetry, reverses factor order, or substitutes a commuting exponential.

## Maximum conclusion

At most G196 can classify one spatially extended affine coframe family on one supplied central
outgoing germ. It cannot select the functions, prove arbitrary-coframe closure, select observers,
derive a global history, establish a physical luminosity/transfer law, or determine `X_max`.
