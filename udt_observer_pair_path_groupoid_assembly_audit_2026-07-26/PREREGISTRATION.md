# Observer-pair path-groupoid assembly audit — preregistration

Date: 2026-07-26

Mode: CPU-only exact algebra and finite rational witnesses.

## Whole question

The current foundation derives the reciprocal operator on a supplied ordered clock/ruler pair. The
latest authority audit establishes that the pair is intrinsically aligned with the local physical
clock/ruler axes under the recorded declared metric readout, while its global observer/path
assignment remains open. Earlier triangle and transport audits found:

- a middle-frame mismatch when pair-specific frames are collapsed onto one frame per event;
- exact pathwise Levi-Civita conjugation after a complete metric, initial lift, and path are supplied;
- path independence only under a holonomy-centralizer condition; and
- an observer-indexed bilocal depth type whose signed lift and transition law remain open.

This audit asks:

> Does the corrected local alignment assemble consistently when the objects are ordered
> observer/ruler pairs rather than bare events, and exactly which missing datum remains before this
> pathwise kinematic structure becomes a physical observer-pair clock law?

## Bounded regime

The audit covers:

1. a real four-dimensional Lorentz space or tangent fiber;
2. every ordered orthonormal pair `(u,n)` with one future timelike clock and one spacelike ruler;
3. the full scalar-screen family
   `X_lambda(u,n)=-P_u+P_n+lambda(I-P_u-P_n)`;
4. arbitrary metric-isometric path transport maps and their composition/reversal laws;
5. arbitrary vertical Lorentz maps between two ordered pairs at one event, including their screen
   `SO(2)` ambiguity;
6. every real additive depth assignment on path-labelled arrows;
7. endpoint-only depth cocycles, path-integrated one-form controls, loop periods, and path
   independence; and
8. the distinction between a groupoid over pair frames and an attempted collapse to bare events.

The calculation does not select a complete metric solution, path, observer, `lambda`, depth profile,
or global finite-cell branch.

## Method and premise ledger

The question is **metric-led**. The following are fixed:

| ingredient | stamp | use |
|---|---|---|
| Reciprocal-c identity and dual Reciprocity | `pinned-by-THEORY` | founded two-channel character |
| additive pair parameter and `P(phi)` | `pinned-by-THEORY` | abstract finite operator |
| aligned local clock/ruler pair | `pinned-by-THEORY` with its exact `DECLARED_READOUT/SR_CONTINUITY` stamp | local pair object |
| Lorentzian metric compatibility | `pinned-by-THEORY` in the supplied complete-metric stratum | path transport preserves pair type |
| one complete metric | `free-and-explored` as supplied input | no branch selected |
| observer timelike axis, separation direction, and path | `free-and-explored` as typed arrow data | none made universal |
| `lambda` | `free-and-explored` over all real values | no screen premise inserted |
| vertical screen rotation | `free-and-explored` | test whether it drops out of `X_lambda` |
| signed depth on arrows | `free-and-explored` | endpoint, path, exact, and period strata separated |
| endpoint-only path independence | `CHOSE_TEST_PREMISE` | not assumed by default |
| global one-frame-per-event section | `OPEN` | not inserted |
| strong local CSN | inactive | not used |
| action, source, carrier, boundary, density, bootstrap, mass, `X_max`, dynamics | excluded | no conclusion authorized |

No imported SR/GR observer mechanics or field equations are used. Levi-Civita transport is the
unique torsion-free metric connection of a supplied metric, not an imported gravitational equation.

## Frozen candidate outcomes

- `PAIR_FRAME_PATH_GROUPOID_CLOSES_FOR_ALL_LAMBDA`;
- `PAIR_FRAME_PATH_GROUPOID_REQUIRES_LAMBDA_ONE`;
- `SCREEN_SO2_AMBIGUITY_DROPS_OUT_OF_SCALAR_SCREEN_ENDOMORPHISM`;
- `SCREEN_SO2_AMBIGUITY_OBSTRUCTS_ENDOMORPHISM_DESCENT`;
- `MIDDLE_MISMATCH_IS_A_VERTICAL_PAIR_CHANGE_NOT_AN_ALGEBRAIC_INCONSISTENCY`;
- `ONE_FRAME_PER_EVENT_SECTION_IS_STILL_REQUIRED_FOR_ANY_COMPOSITION`;
- `ADDITIVE_PATH_DEPTH_COCYCLE_COMPLETES_TYPED_COMPOSITION_CONDITIONALLY`;
- `METRIC_TRANSPORT_DERIVES_THE_DEPTH_COCYCLE`;
- `METRIC_NATIVE_DEPTH_COCYCLE_REMAINS_OPEN`;
- `ENDPOINT_ONLY_REAL_COCYCLE_IS_A_POTENTIAL_DIFFERENCE`;
- `NONZERO_REAL_DEPTH_PERIOD_DESCENDS_TO_IDENTITY`;
- `NONZERO_REAL_DEPTH_PERIOD_PRODUCES_RECIPROCAL_LOOP_HOLONOMY`;
- `BARE_EVENT_ENDPOINT_COLLAPSE_REQUIRES_SECTION_OR_HOLONOMY_REDUCTION`;
- `INSUFFICIENT_OR_CONTRADICTORY_AUTHORITY`.

## Falsification and certification

The pair-frame groupoid route fails if two composable, correctly typed arrows leave an uncancelled
middle factor after the intermediate ordered pair is made identical, or if the screen `SO(2)`
ambiguity changes `X_lambda` in the registered scalar-screen family.

The endpoint potential theorem fails if an endpoint-only real function obeying exact triangle
additivity and reversal is not representable as `phi(B)-phi(A)` after choosing one base event.

The period result fails if `diag(exp(-Pi),exp(Pi),exp(lambda Pi),exp(lambda Pi))` is the identity for
some nonzero real `Pi`.

The maximum allowed conclusion is a kinematic/type closure conditional on supplied metric,
pair-frame arrows, and an additive depth cocycle. No physical depth law or global branch may be
called derived unless the metric itself selects it without an inserted section, path, or response.

## Required evidence gates

1. this preregistration committed before outcome algebra;
2. complete symbolic proof for all real `lambda`, depth, and screen rotations in the bounded family;
3. independent no-SymPy exact-rational reconstruction of nontrivial arrows and loop cases;
4. fail-closed catches for event/pair-frame conflation, screen-gauge promotion, depth insertion,
   endpoint-potential denial, period erasure, flatness promotion, and `lambda` selection;
5. current-premise verifier, six frozen manifests, current paths, links/frontier, tests, and original
   dirty-checkout metadata unchanged.

Maximum grade: `VERIFIED_WITH_CAVEATS_BOUNDED_PAIR_FRAME_PATH_GROUPOID_CLASSIFICATION`.

