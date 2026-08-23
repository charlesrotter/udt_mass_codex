# G230 fresh adversarial review

Date: 2026-08-23

## Scope

Three independent roles reviewed the bounded one-event calculation after production:

1. index/sign and nonlinear-affine algebra;
2. geometric meaning and scope;
3. evidence completeness and provenance.

None was authorized to promote the result beyond a supplied event, fixed tangent frame, and
pointwise fourth-order metric realization.

## Algebra and sign review

Landing: `BOUNDED_ACCEPT`.

The reviewer independently checked the curvature convention, the order of the derivative indices,
the minus sign in

\[
(\nabla_f\nabla_e-\nabla_e\nabla_f)R_{abcd}
=-R^p{}_{afe}R_{pbcd}-R^p{}_{bfe}R_{apcd}
-R^p{}_{cfe}R_{abpd}-R^p{}_{dfe}R_{abcp},
\]

and the complete connection-product and covariantization terms in the affine offset. A direct
polynomial-metric check of the frozen witness found

\[
E_{01\,0212}=-\frac49,
\qquad
E_{10\,0212}=\frac59,
\]

so their difference is exactly `-1`, agreeing with production and the independent replay. The
reviewer also confirmed that the rank equalities prove pointwise affine sufficiency, not merely
necessity.

## Geometry and scope review

Landing: bounded acceptance with a strict infinitesimal interpretation.

The reviewer agreed that differentiated Bianchi plus the nonlinear Ricci commutator are the first
second-curvature-derivative overlap obstruction, and that every compatible target has a metric
fourth-jet representative. “Overlap” means the infinitesimal square at one event. G230 does not
construct two distinct events, overlapping finite charts, or a regional field.

The reviewer requested explicit residuals for the counterexample rather than inference from typed
bases. Repair R3 added direct checks:

- G227 algebraic-Bianchi residual nonzero count: `0`;
- G228 zero-`D` differential-Bianchi residual nonzero count: `0`;
- G230 zero-`E` differentiated-Bianchi residual nonzero count: `0`;
- G230 zero-`E` commutator residual nonzero count: `2`.

## Evidence and provenance review

Landing: `BOUNDED_ACCEPTANCE_WITH_MECHANICAL_PROVENANCE_CLOSEOUT`.

The reviewer accepted the complete production arenas and ranks, the 210-case coefficient-complete
quadratic polarization, the independent full-21-slot two-prime and exact-Fraction replay, and all
nine hostile catches. It identified two evidence defects during review: stale saved production JSON
after R3 and the initially missing structured history-promotion hostile. Both were repaired and the
saved evidence was regenerated before final acceptance.

The requested mechanical closeout consists of the recorded full 13/13 replay and the exact SHA-256
evidence manifest. Both are package gates, not scientific extensions.

## Joint landing

`DERIVED_CONDITIONAL__ONE_SUPPLIED_EVENT__FIXED_TANGENT_FRAME__COMPATIBLE_CURVATURE_SECOND_JETS_HAVE_LOCAL_LORENTZ_METRIC_FOURTH_JET_REPRESENTATIVES_MODULO_224_DIMENSIONAL_QUINTIC_COORDINATE_GAUGE__POINT_JET_ONLY`

Open: finite-neighborhood gluing, arbitrary smooth or analytic field realization, value generation,
population, selected transport, dynamics, and physical/global history.
