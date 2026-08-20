# G184 preregistration — regular branch equivalence classification

Date: 2026-08-19

## Whole question and bounded regime

Classify when two **supplied regular completed observer-pair realizations** are merely the same
realization written with different pair-domain coordinates, when an explicitly declared symmetry of
the fully typed query may also identify them, and when they remain distinct branch data even though
their endpoints, completed scalar, tape, image, or induced pair metric agree.

The arena is a fixed supplied smooth Lorentzian four-metric `(M,g)` and regular calibrated pair
realizations

```text
R_i=(Sigma_i, q_i, F_i),
F_i:Sigma_i -> M,
h_i=F_i^* g,
h_i00<0, det(h_i)<0.
```

Here `q_i` denotes all query typing that is actually declared: ordered source and target incidence,
clock/ruler calibration, pair orientation, marked boundaries or endpoints, and any admitted ambient
query symmetry. G184 does not invent missing query fields.

This is a metric-led quotient classification of the G183 regular multibranch arena. It is not a
branch selector, preferred path, holonomy calculation, physical-population law, or new reciprocal
kernel.

## Equivalence relations fixed before outcomes

### Strict realization reparameterization

`R_1 ~_0 R_2` exactly when there is a diffeomorphism

```text
psi:Sigma_1 -> Sigma_2
```

that preserves the declared ordering, markings, orientations, and calibrations, satisfies
`q_1=psi^*q_2`, and makes the realization diagram commute:

```text
F_1 = F_2 o psi.
```

This is the claim that the two objects are one ambient realization in different pair coordinates.

### Query-symmetry equivalence

If, and only if, the supplied query declares an ambient automorphism group `Aut_g(Q)`, define
`R_1 ~_Q R_2` when there are a query-preserving `psi` and `A in Aut_g(Q)` with

```text
A^*g=g,
A o F_1 = F_2 o psi.
```

No ambient reflection, orientation reversal, observer swap, or screen flip is silently admitted.
Changing `Aut_g(Q)` changes the quotient being asked for; it does not change the metric evaluator.

## Preregistered claims to test

1. `~_0` is an equivalence relation and its isomorphisms form a groupoid under composition and
   inversion. `~_Q` does likewise when the supplied query automorphisms form a group.
2. Strict equivalence implies

   ```text
   h_1=psi^*h_2,
   m_1 d sigma_1=psi^*(m_2 d sigma_2)
   ```

   with the orientation qualification already fixed by G180, and all completed scalar outputs agree
   after pullback. Thus the accepted kernel descends to strict equivalence classes.
3. Endpoint equality, completed-depth equality, completed-tape equality, induced-metric equality, or
   image-set equality is individually weaker than typed realization isomorphism.
4. Two regular immersions can have the same marked endpoints and exactly the same completed pair
   metric but different extrinsic curvature; they are then not related by a domain reparameterization
   or ambient isometry.
5. Two regular coverings can have the same image but different covering degree. Degree is unchanged
   by a domain diffeomorphism, so image equality does not erase winding or multiplicity.
6. The G183 reflected polynomial branches are strict-distinct. They become `~_Q`-equivalent only if
   the transverse reflection is explicitly in `Aut_g(Q)`; a typed transverse orientation excludes
   that identification.
7. The G183 circle branches with lifted displacements `ell_n=1+2n` are strict-distinct. The pair
   `n <-> -n-1` becomes symmetry-equivalent only if circle reflection is admitted. Distinct
   `|ell_n|` classes remain distinct under circle isometries and query-preserving domain
   diffeomorphisms.
8. Branch equivalence transports any separately supplied non-scalar data according to its own
   functorial law; it does not turn orientation, connection, Jacobi, or holonomy data into the scalar
   kernel and does not infer nontrivial holonomy from winding.

## Exact witnesses fixed before outcomes

1. **Nonlinear reparameterization control.** On `R x [0,1]`,

   ```text
   F(t,s)=(t,s,s^2,0),
   f(u)=(u+u^2)/2,
   F_tilde=F o (t,u |-> t,f(u)).
   ```

   The map fixes both marked ends and has `f'(u)>0`.
2. **Same endpoints and pair metric, different extrinsic data.** In flat `1+3`, compare a unit-speed
   semicircle and a unit-speed helix on `0<=s<=pi R`:

   ```text
   c_1(s)=(R sin(s/R), R[1-cos(s/R)], 0),
   c_2(s)=(a sin(2s/R), (2/pi)s, a[1-cos(2s/R)]),
   a=(R/2)sqrt(1-4/pi^2).
   ```

   Both join `(0,0,0)` to `(0,2R,0)`, both have unit speed, and both give
   `h=-dt^2+ds^2`, while `|c_1''|^2` and `|c_2''|^2` differ.
3. **Same image, different covering degree.** On `R x S^1`,

   ```text
   F_n(t,u)=(t, cos(nu), sin(nu), 0), n=1,2.
   ```

4. **Conditional symmetry controls.** Reuse the G183 reflected polynomial and antipodal winding
   fixtures, once with transverse/circle reflection admitted and once with the corresponding
   orientation fixed.

## Physical-choice ledger

- Lorentz signature, complete pullback, and regular kernel domain: `pinned-by-THEORY` through G179
  and G183.
- Completed-pair normalization and auxiliary reparameterization covariance:
  `WORKING_FOUNDATIONAL_CLARIFICATION`, G176--G180.
- Ambient metric, realizations, query markings, symmetry group, endpoints, radius, and winding
  degree: `free-and-explored` controls; none is selected as physical.
- The strict and query-symmetry equivalence definitions: `CHOSE` as the typed mathematical question,
  not asserted physical ontology.
- `X_max`, observations, action, source, matter, bootstrap, radiative transfer, dynamics,
  signalling, and global completion: omitted and inactive.
- No `pinned-by-HABIT` coefficient, fit, carrier, boundary, or branch preference enters.

## Verification contract

- Production: exact symbolic and rational checks of the commuting diagrams, pullback covariance,
  groupoid closure, witness metrics, extrinsic invariants, and degree/orientation classifications;
  at least 12,000 exact rational reparameterization families.
- Independence: a separately written dependency-free implementation using direct Jacobians,
  determinant identities, endpoint maps, curvature invariants, and integer degree; at least 20,000
  exact rational families.
- Mutation catches must kill omitted calibration preservation, reversed composition order, false
  metric-to-immersion faithfulness, image-to-map conflation, degree loss, unconditional reflection
  identification, orientation erasure, branch selection, and scalarization of transport.
- The package must replay read-only and dependency-free, verify immutable source hashes, run the
  full premise audit and repository tests, and receive a fresh adversarial review before banking.

## Falsifiers

The preregistered landing fails if any of the following occurs:

- a strict commuting realization diagram does not imply pullback/kernel covariance;
- strict morphisms fail identity, inverse, or associative composition;
- the semicircle and helix witness have unequal endpoints or induced metrics, or equal extrinsic
  curvature invariant;
- a domain diffeomorphism changes covering degree magnitude;
- reflected or oppositely wound branches have one unconditional equivalence status independent of
  the supplied query symmetry/orientation typing;
- the classification selects one branch, imports a path law, or folds non-scalar transport into
  completed depth.

## Preregistered landing and maximum conclusion

If all claims survive, the strongest allowed landing is

```text
TYPED_REALIZATION_ISOMORPHISM_CLASSIFIES_REGULAR_BRANCH_EQUIVALENCE__KERNEL_EVALUATION_IS_NOT_FAITHFUL
```

At most G184 may define the exact quotient on the supplied regular branch arena, prove that the
accepted kernel descends to that quotient, and show by fixed witnesses that scalar, tape, metric, or
image equality do not generally identify realization classes. It may not decide which quotient is
the physical one without supplied query typing, select a branch, infer holonomy, or make any global,
observational, dynamical, source, matter, `X_max`, or signalling claim.
