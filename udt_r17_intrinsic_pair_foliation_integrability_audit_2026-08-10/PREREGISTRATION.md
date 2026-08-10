# Preregistration — R17 intrinsic-pair foliation and integrability

Date: 2026-08-10

Mode: metric-led, exact analytic/CPU

## Whole question

On the already bounded regular off-shell R17/W01 configurations C01--C06, determine what global
surface, foliation, and normal-bundle structures are supplied by the complete metric after the
branch-local reciprocal magnitude and vertical metric class have been established.

The audit does **not** ask for a desired physical tape. It classifies whether each metric-owned
distribution is locally involutive, what its maximal global leaves are, what pair metric those
leaves inherit, whether the terminal reciprocal depth agrees with `delta_K`, and whether the
four-slot vertical factor becomes an integrated physical observer arrow.

## Exact bounded arena

The candidate arena is frozen in `CANDIDATE_ARENA.tsv` before algebra. No candidate may be removed
because it is nonintegrable, query-dependent, path-dependent, multi-valued, or physically
unattractive.

The configurations are the six supplied smooth regular C01--C06 metrics

```text
theta_0=exp(-phi)(dt+a sigma_3),
theta_1=exp(+phi)sigma_3,
theta_2=exp(lambda phi)sigma_1,
theta_3=exp(lambda phi)sigma_2,
g=-theta_0^2+theta_1^2+theta_2^2+theta_3^2,
```

with their frozen nonzero twist and six supplied `lambda` values. The proof must be profile-generic
where possible and must not use the frozen polynomial coefficients to manufacture integrability.

## Questions and required classifications

1. Is the intrinsic reciprocal distribution `E=image(P_u+P_n)` Frobenius integrable?
2. Is the angular screen `H` integrable, or only a normal/contact bundle?
3. What are the maximal global leaves of `E` on `R x S3`? Are they selected individually or only
   as a family?
4. What complete two-metric is induced on every leaf, including the twist/mixing term?
5. Does the leaf metric itself enforce reciprocal area and reproduce
   `delta_K=phi(q)-phi(p)` without adding `TL=1`?
6. Which ordered endpoint pairs lie on one intrinsic leaf? What happens for endpoints on distinct
   leaves or for multiple windings?
7. Does the complete screen-decorated leaf integrate the four-slot factor into a unique physical
   map, or does normal-bundle carry remain path-labelled?
8. Does any result select the R17 branch, one `lambda`, a physical path, endpoint reset, action,
   bootstrap law, or dynamics?

## Premise discipline

- The complete R17 coframes and their C01--C06 configuration values are conditional branch inputs,
  not selected universe solutions.
- The intrinsic clock line, twist-ruler line, projector triple, Killing endpoint depth, and
  vertical metric class are pinned only at their cited banked scopes.
- `S3` Maurer--Cartan structure is geometry, not imported matter physics.
- Smooth `phi` is retained as a general stationary function; no radial, harmonic, or fitted profile
  is imposed.
- No field equation, action, source, boundary condition, observer dynamics, geodesic
  postselection, shortest-path rule, or preferred screen phase is supplied.
- Integrability is a characterizer. Nonintegrable and multi-valued branches remain results rather
  than failures.

## Falsification and certification

The preregistered tests are frozen in `FALSIFICATION_CONTRACT.tsv`. Load-bearing identities require
an exact symbolic controller and an independent standard-library reconstruction using a different
representation. Catch proofs must reject at least:

- omitting the twist term from the induced pair metric;
- calling the screen integrable after deleting its transverse bracket;
- using a special `phi` profile to obtain the result;
- selecting one leaf or one winding from the foliation;
- promoting same-leaf endpoint depth to an arbitrary-endpoint complete arrow;
- erasing screen holonomy or setting the endpoint reset to identity;
- selecting `lambda`, R17, an action, matter, bootstrap, `X_max`, CMB physics, or signalling.

## Preregistered possible landings

- `INTRINSIC_PAIR_DISTRIBUTION_NOT_INTEGRABLE`;
- `LOCAL_PAIR_LEAVES_ONLY__GLOBAL_COMPLETION_OBSTRUCTED`;
- `GLOBAL_PAIR_FOLIATION_DERIVED__PAIR_METRIC_OR_DEPTH_DOES_NOT_CLOSE`;
- `GLOBAL_PAIR_FOLIATION_AND_SCALAR_DEPTH_DERIVED__FULL_NORMAL_BUNDLE_ARROW_OPEN`;
- `COMPLETE_PHYSICAL_PAIR_SURFACE_FAMILY_DERIVED`;
- `TYPE_OR_SOURCE_FAILURE`.

No ordering is a preferred outcome.

## Maximum conclusion

At most this audit may classify intrinsic surfaces, their induced pair metrics and scalar depth,
and the associated normal-bundle/path structure on the supplied regular C01--C06 off-shell
configurations. It cannot put them on shell, select one as the universe, derive a universal
observer law, or infer an action, source, matter, mass, bootstrap closure, `X_max` value, CMB
spectrum, polarization, or signalling law.
