# G341 preregistration — nonprincipal finite null relation and screen carry

Date: 2026-09-04
Outcome status: unseen at preregistration

## Frozen spacetime and state

Use only

\[
 g=-dT^2+C_X^2T^{-2/3}dX^2+C_\perp^2T^{4/3}(dy^2+dz^2),\qquad T>0,
\]

on a supplied compact translation quotient, with supplied fixed-label normal observers. Work on
the universal cover first and attach an explicit lattice lift to every route. The input is a
positive emission time and a nonzero spatial lift. Momentum magnitude is affine gauge; its
projective direction is to be solved, not pinned.

## Preregistered alternatives

1. `A__EACH_NONZERO_LIFT_HAS_ONE_REGULAR_FUTURE_NULL_SOLUTION__MIXED_RAYS_HAVE_EXACT_SCREEN_CARRY__QUOTIENT_MULTIPLICITY_IS_PATH_LABELLED`:
   the universal-cover endpoint map is globally one-to-one and full-rank away from the cone vertex;
   mixed rays have a nonzero G269 endpoint-clock screen mismatch while screen-quotient transport
   closes exactly; compact multiplicity comes from distinct lattice lifts and ties.
2. `B__A_FIXED_UNIVERSAL_COVER_LIFT_HAS_MULTIPLE_FUTURE_NULL_SOLUTIONS_OR_AN_INTERIOR_CAUSTIC`:
   the exact endpoint map folds, is not onto, or loses rank for some regular positive-time input.
3. `C__ENDPOINT_INVERSE_CLOSES_BUT_NONPRINCIPAL_SCREEN_CARRY_REQUIRES_AN_EXTRA_PROPAGATION_OR_LIGHT_MODEL`:
   the metric determines the route but not the endpoint screen relation.
4. `D__ONLY_LOCAL_INVERSE_OR_NUMERICAL_BRANCH_EVIDENCE_IS_AVAILABLE`:
   local Jacobian control survives, but global uniqueness or complete boundary classification
   cannot be established.

## Required derivations

1. Reduce transverse rotations without deleting their azimuthal screen direction, and derive the
   exact two-variable endpoint map from the four-metric.
2. Derive its local Jacobian and classify its sign for every mixed direction.
3. Prove or refute global existence and uniqueness for every nonzero universal-cover lift; treat
   both principal-axis limits in regular Cartesian direction charts.
4. Separate true rank loss/conjugate caustics from polar-coordinate degeneracy and compact-quotient
   branch crossings.
5. Derive the general endpoint frequency ratio and classify any nonprincipal zero-shift direction
   without calling it zero distance or zero screen response.
6. Derive the orthonormal-frame connection directly from the metric and parallel-transport both
   screen directions along every mixed ray.
7. Compute the exact G269 mismatch `W`, its principal limits, its reversal typing, and the two G298
   pair-plane projections without selecting one as the physical kernel input.
8. Retain every lattice lift; prove only those finiteness/earliest-arrival statements actually
   supported by the endpoint map.
9. Audit light-model, route, protocol, population, scale, `X_max`, equation, and canon ownership.

## Certification and falsification

- production: exact sign/limit identities plus at least 2,000 nonlinear endpoint, Jacobian,
  frequency, screen-transport, pair-plane, and lattice checks over all quadrants and axis limits;
- independent route: reconstruct the four-metric Christoffels, null propagation, endpoint inverse,
  and vector parallel transport without importing production code or reading production results;
- global uniqueness must be supported by an analytic monotonicity/properness argument, not merely
  by converged roots from sampled starting guesses;
- hostile controls must catch at least: a folded endpoint derivative, deleted winding, polar-axis
  chart degeneracy called a caustic, mixed-screen mismatch forced to zero, omitted null-gauge term,
  quotient branch crossing called a conjugate point, zero frequency shift called zero relation,
  target-local and transported-source planes conflated, signed depth called signed distance,
  physical route selection, imported light dynamics, and scale/`X_max` promotion;
- raw residual tolerance: `3e-10` for double-precision quadrature/RK checks; exact algebraic signs
  and limits where available;
- every script must run with `python3 -S`, support `UDT_NO_WRITE=1`, and alter no evidence bytes in
  no-write mode;
- no conclusion may exceed `MAP.md`.

## Omitted scope

Accelerated observers, generic developments, perturbed metrics, physical route populations,
Jacobi brightness/area or polarization dynamics, electromagnetic fields, sources, detectors,
matter/mass, observations, stability, topology selection, absolute scale, physical `X_max`, and
canon.
