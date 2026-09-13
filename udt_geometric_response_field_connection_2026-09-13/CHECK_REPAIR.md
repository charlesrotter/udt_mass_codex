# GFC1 finite failed-check diagnostic and repair freeze

Original check ran37 named groups,36 passed,1 failed; exit1. The failed group
nodal_frame_regular substituted u=1 on the boosted frame but compared with the
base frame still evaluated at variable u. Its two residuals are precisely the
remaining u-dependent base-frame lapse coefficients. Both sides describe
regular frames; the asserted comparison used different events.

Original script, CHECK_FREEZE, result, stdout/stderr and capture remain unchanged.
The full original metric/Gram/connection/dA/ambient-curvature/source-free checks
passed in that run; the single failure is not suppressed or reclassified PASS.

Before rerun: change only the expected base to base.subs(u,1) for this group;
add a computed off-axis wrong-event control to show the old mismatch is detected.
Add reversed-orientation compatible-screen Gram/connection/curvature controls
for the separately documented O(2) clarification. No scientific equation,
source, domain, symbolic tolerance or original sample is changed. Ordinary
capture limit remains180s/2048MiB, one CPU process/thread. If another error
occurs, preserve it and diagnose within the existing work/review budgets.

Reviewer source-first findings were received while the original run had
already completed but before the parent observed its outcome. They concern
an additional null-lift representation, not this test repair. The exact
exposure chronology is not represented as blind discovery.
