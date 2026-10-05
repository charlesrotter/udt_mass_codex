# Independent saved-state and finite-record replay

VERIFIED-WITH-CAVEATS for the saved construction. No parent implementation was
read or imported; only declared sources, protocol and saved states/readouts
were used. The implementation uses original dimensionless ray quadrature and
proper-time quadrature in log radial coordinate, independently recomputing
each stored derivative/readout. Parent's reused TSI evaluator is not counted
as parent-independent evidence; this replay is a different implementation.

All 25 saved high-precision states passed, including the five E=10 states.
Maximum original incidence residual was 2.652e-74, maximum proper-time residual
4.083e-68, and maximum scaled readout discrepancy 8.395e-69. This is numerical
agreement at 90-digit working precision; it is not rigorous error certification.
The associated analytic inequalities continue to own the continuum claims.

All short-record midpoint/window certificates and both long interval outputs
were independently recomputed. In declared synthetic length units:

- Short H enclosure: (0, .007523827554180344], includes both .0025 and .005.
- Long E=1: [.004972583595655606, .005067684169969094].
- Long E=10: [.004972299857938960, .005067399010009679].
- Long two-history angular separation margin after the declared window,
  center-time and measurement penalties: 6.387337469268697e-7 radians.

The intervals enclose the supplied H=.005 and exclude its H=.0025 companion.
They are necessary conservative enclosures for the declared record class;
they do not establish unique values of every model parameter. No actual
window-mean quadrature is claimed: exact bounds certify the center-constructed
synthetic readings against those means.

Two deliberately corrupted replays were rejected: multiplying the saved
terminal E=10 radius by1.001 generated proper-time residual .19990006648;
multiplying its ray parameter by1.01 generated incidence residual2.2973558e-7.
These check nonvacuity of the original-equation replay, not a physical claim.

Resource/case record: first independent check36 incidences; saved replay25;
corruption controls2; cumulative63 of100. Exact-rational bound checks consume
no incidence cases. Both commands used the owned capture utility with 2GiB
virtual memory, one BLAS thread and no CPU/wall timeout. Independent36-case run
took4.596s, saved27-case run .896s. JSON and stdout/stderr own commands/versions.

Scope limitations and omitted empirical/native interfaces are unchanged from
EXPOSED_REVIEW.md. Final integration and exact-version correspondence remain
to be checked; this note does not claim parent final premise audit execution.
