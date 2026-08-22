# G224 preregistration

Date: 2026-08-22

## Hypotheses

Let `g` be one supplied time-oriented Lorentz metric.  Let two supplied regular future-null
ribbons `Sigma_AB` and `Sigma_BC` meet the same marked event `b` of observer `B`.  Let `U_B` be
the future-directed metric-unit tangent of `B` at `b`, and let `V_-` and `V_+` be the incoming and
outgoing future-null vertical lines at `b`.

For `e in {-,+}`, define

\[
\mu_e(v)=-g(U_B,v),\qquad v\in V_e.
\]

Time orientation and null regularity imply that each `mu_e` is a positive linear isomorphism on
the oriented ray.

## Preregistered claims to test

1. There is a unique positive line isomorphism

   \[
   S_{+\leftarrow-}=\mu_+^{-1}\mu_-:V_-\to V_+
   \]

   preserving the metric clock pairing.

2. In arbitrary positive affine bases `K_-` and `K_+`, with

   \[
   \omega_-=-g(U_B,K_-)>0,
   \qquad
   \omega_+=-g(U_B,K_+)>0,
   \]

   the map is represented by

   \[
   S_{+\leftarrow-}(K_-)=\frac{\omega_-}{\omega_+}K_+.
   \]

   Its abstract value is invariant under independent positive rescalings of the two affine bases.

3. A common positive recalibration of the middle clock multiplies both `mu` functionals equally
   and cancels from `S`.  Independent endpoint calibration changes are not silently identified.

4. For any finite collection of incident future-null vertical lines at the same observer event,

   \[
   S_{k\leftarrow j}S_{j\leftarrow i}=S_{k\leftarrow i},
   \quad
   S_{i\leftarrow i}=1,
   \quad
   S_{i\leftarrow j}=S_{j\leftarrow i}^{-1}.
   \]

5. On an affinely ruled null edge `e:A->B`, metric affine transport sends its generator at `A` to
   its generator at `B`.  With `omega_{e,A}=-g(U_A,K_{e,A})` and similarly at `B`, the normalized
   vertical generators `N_{e,v}=K_{e,v}/omega_{e,v}` obey

   \[
   P_eN_{e,A}=\frac{\omega_{e,B}}{\omega_{e,A}}N_{e,B}.
   \]

6. If the G216 clock ratio on that same supplied edge is

   \[
   r_e=\frac{d\tau_B}{d\tau_A}=\frac{\omega_{e,A}}{\omega_{e,B}},
   \]

   then vertical carry has coefficient `r_e^-1`.  Consequently the actual broken composite
   `A->B->C` carries the vertical scalar by `(r_AB r_BC)^-1`, the inverse representation of the
   G216 clock product.

7. Equality with a direct `A->C` coefficient is asserted only if that direct arrow is defined to
   be the actual composite relation.  No constraint is imposed on an independently supplied
   direct `A->C` ribbon.

8. The construction is unavailable when the two incidences occur at distinct events of `B`, unless
   an additional transport is supplied.  It does not identify ambient null directions or normal
   screen/Jacobi data.

## Competing outcomes

- **A — canonical closure:** the shared-event metric pairing uniquely supplies the vertical line
  switch, all covariance and cocycle tests pass, and scalar path carry is inverse to the G216 clock
  carry on the same actual relation chain.
- **B — residual torsor:** after all declared metric and incidence data are used, a positive scale
  freedom remains in the line switch.
- **C — extra premise required:** a unique switch exists only after adding a datum not present in
  the declared shared-event geometry; that datum must be named precisely.

## Mandatory controls

1. uniqueness proof using one-dimensional nondegeneracy;
2. identity, inverse, and three-line vertex cocycle;
3. independent positive rescaling of every affine generator;
4. common middle-clock recalibration;
5. exact path product for two and three edges;
6. mutation controls that deliberately omit one frequency factor, reverse the ratio, or use an
   independently supplied direct edge;
7. distinct-middle-event counterexample/type rejection;
8. explicit refusal to infer a screen map or ambient null-direction equality.

## Falsification contract

Outcome A fails if the abstract switch changes under allowed affine-generator rescaling; if common
middle-clock recalibration changes it; if identity, inverse, or vertex associativity fails; if the
edge coefficient is not the inverse of the clock ratio under the declared same-edge convention; or
if the proof requires a screen, a path selector, a profile, or a direct-edge equality not supplied
by the hypotheses.

## Maximum conclusion

At most:

```text
SHARED_MIDDLE_EVENT_AND_METRIC_UNIT_CLOCK_CANONICALLY_IDENTIFY_INCIDENT_FUTURE_NULL_VERTICAL_LINES
__VERTICAL_SCALAR_CARRY_IS_THE_INVERSE_REPRESENTATION_OF_THE_ACTUAL_CLOCK_RATE_CHAIN
__NO_SCREEN_MAP_DISTINCT_EVENT_TRANSPORT_OR_INDEPENDENT_DIRECT_RELATION_IS_DERIVED
```
