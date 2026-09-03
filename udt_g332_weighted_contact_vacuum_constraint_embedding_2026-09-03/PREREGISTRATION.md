# G332 preregistration — weighted-contact vacuum-constraint embedding

Date: 2026-09-03

## Frozen question

For the complete positive-weight G331 family

```text
gamma_w = dx^2/[4x(1-x)F] + [x(1-x)/F] zeta^2 + eta^2,
F = w1*x + w2*(1-x),
xi = w1*partial_phi1 + w2*partial_phi2,
w1,w2 > 0,
```

determine whether at least one genuinely unequal-weight member with irrational `w1/w2` admits a
smooth symmetric extrinsic curvature `K` satisfying the complete active provisional vacuum
constraints for one fixed connected scalar `Lambda`:

```text
R(gamma) + tr(K)^2 - |K|^2 = 2 Lambda,
div_gamma[K - tr(K) gamma] = 0.
```

The question permits all six components of `K`. The construction below is a preregistered
existence witness only; it may not be used to claim a full `K` classification.

## Candidate outcomes

1. `EXACT_IRREGULAR_WEIGHTED_DATA_EXIST`: a smooth extrinsic curvature exists for unequal
   irrational weights, so the active constraints do not force closed Ricci-line orbits at the
   initial-data level.
2. `WEIGHTED_FAMILY_CONSTRAINT_OBSTRUCTED`: no symmetric extrinsic curvature can solve the complete
   constraints for any genuinely unequal-weight member. This outcome requires an all-`K`
   obstruction; failure of the registered witness is insufficient.
3. `MIXED_WEIGHTED_SUBFAMILY`: constraint-compatible unequal-weight members exist only under an
   additional, exactly characterized restriction.

No outcome selects physical occupancy or a universe.

## Frozen candidate witness

Let `xi` be the G331 global unit Killing field and set

```text
P = K - tau*gamma = -C*gamma + b*xi_flat tensor xi_flat,
tau = tr_gamma(K),
```

with constant real `C`. In three spatial dimensions, inversion of this trace relation gives

```text
tau = (3*C-b)/2,
K = ((C-b)/2)*gamma + b*xi_flat tensor xi_flat.
```

The only allowed closure of `b` is the one obtained directly from the Hamiltonian constraint. No
coefficient may be fitted or altered after execution.

## Exact gates

1. **Metric gate.** Reconstruct the G331 weighted metric directly on `0<x<1`, with `w1,w2>0`, and
   retain its smooth global `S3` completion from G331. Do not replace it by a Berger metric.
2. **Unit-Killing gate.** Verify from the displayed metric that `gamma(xi,xi)=1`,
   `Lie_xi(gamma)=0`, `div(xi)=0`, and `nabla_xi xi=0`. Confirm that scalar curvature is
   `xi`-invariant.
3. **Momentum gate.** Derive `div(P)=0` covariantly and also by direct coordinate Christoffel
   reconstruction. The direct check must include unequal weights and nonconstant scalar curvature.
4. **Hamiltonian gate.** Derive `R+tau^2-|K|^2` without importing a field equation or action. Solve
   its resulting algebraic equation for `b` and verify both real branches exactly.
5. **Regularity gate.** For any fixed finite `Lambda`, prove using compactness that a finite free
   `C` can make the radicand strictly positive everywhere. Record the equality/crossing boundary
   rather than discarding it.
6. **Irregular-orbit gate.** Use a positive unequal irrational weight ratio from G331's exact dense
   family. Verify that the constraint construction never assumes a common period, quotient `S2`,
   or circle fibre.
7. **Nontriviality gate.** For unequal weights, verify that scalar curvature and the reconstructed
   `b`, `tau`, and `K` are generically nonconstant; the witness must not secretly be pure trace or
   homogeneous.
8. **Branch gate.** Retain both signs of the square root and both signs of `C`. Neither is selected
   physically. Treat the radicand-zero locus separately.
9. **Scale gate.** Check homothety dimensions. `C` and `Lambda` remain free construction data; no
   absolute ruler or physical `X_max` is inferred.
10. **Full-space honesty gate.** A successful witness proves existence only. A negative result from
    the witness cannot be promoted to an obstruction on unrestricted `K`; such an obstruction must
    quantify over all smooth symmetric extrinsic curvatures.
11. **Controls.** Retain equal weights, rational unequal weights, irrational unequal weights, the
    Berger limit, constant-scalar cases, arbitrary fixed `Lambda`, and the radicand boundary.
12. **Provenance gate.** No old `S2` carrier, `L2+L4` action, EH-selection argument, source, matter,
    mass, observation, fit, boundary mechanism, absolute scale, physical `X_max`, protected local
    work, or new field equation may enter.

## Falsification contract

- Outcome 1 fails if either vacuum constraint has a nonzero residual for the displayed smooth
  `K`, if the construction requires `w1=w2`, or if its `Lambda` varies over `S3`.
- The momentum argument fails if it uses only a coordinate component cancellation without proving
  the required unit-Killing identities, or if a derivative of `b` was silently dropped.
- The Hamiltonian argument fails if the square-root closure is fitted pointwise without one common
  constant `C` and one common `Lambda`.
- The irregular witness fails if its generic orbits are actually closed, if the metric loses the
  simple Ricci line, or if the construction uses the common-fibre normalization already shown
  unavailable by G331.
- Any all-family statement fails if only finitely many weights or points are sampled without an
  analytic theorem.

No failed gate may be repaired by fixing a convenient extrinsic-curvature component, selecting an
orbit type, or adding matter, a source, action, boundary condition, fit, or scale.

## Evidence contract

- one covariant analytic derivation valid for the complete positive-weight family;
- one direct coordinate implementation rebuilding metric inverse, Christoffels, Ricci scalar,
  momentum residual, trace, norm, and Hamiltonian residual;
- one implementation-distinct verifier which imports no production code and reads no production
  result;
- hostile mutations of unit norm, Killing/geodesic use, momentum sign, trace inversion,
  Hamiltonian sign, square-root coefficient, constant-`Lambda` typing, and existence-versus-census
  wording;
- aggregate replay and fresh external adversarial review before banking a scientific verdict.

## Maximum conclusion

The maximum grade is `DERIVED_CONDITIONAL` exact existence of active provisional vacuum constraint
data on G331's supplied weighted-contact `S3` family. Even a full-family construction is not an
evolution, stability, occupancy, topology-selection, matter/mass, scale, `X_max`, or canon result.
