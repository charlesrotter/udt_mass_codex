# Independent numerical check freeze

This plan follows SOURCE_FIRST.md and its fixed seal. New parent code/config,
but no numerical outcomes, were exposed before this plan. Parent code was read
from the files bound by numerics/FREEZE.json. No parent scientific module is
imported. This is a distinct implementation using metric integrals and
high-precision monotone root inversion, not a separate physical premise.

The question is whether all finite saved queries and center trajectories in
the frozen 14-query/3-setting matrix agree with the original metric equations.
The supplied controls, radial comoving queries and physical omissions are those
in SOURCE_FIRST.md. Every saved center sample receives independent affine,
conformal-distance, frequency, momentum and transport checks. Every saved
endpoint, including emission perturbations, reverse and echo, receives an
independent root and direct quadrature anchor. This does not re-solve native
metric dynamics or survey omitted degrees of freedom.

Additional pre-outcome transport derivation: in orthonormal (t,x) frames,
parallel transport on a sign-s null ray is the boost of rapidity
-s log(a(t)/a(te)). Its coordinate matrix is

    [[cosh(r),       -s ae sinh(r)],
     [-s sinh(r)/a,   ae cosh(r)/a]],  r=log(a/ae).

It follows by transforming the Levi-Civita connection from SOURCE_FIRST's
metric to orthonormal frames; the frame connection on the ray is
s (a'/a) dt times the boost generator. It sends (1,s/ae) at emission to
(ae/a,s ae/a^2) and preserves endpoint metrics. This independent exact control
anchor will check the parent's saved P entries, in addition to its null tangent.

Implementation uses mpmath at 60 decimal digits. Cubic conformal integration
has an independently derived elementary primitive; its scalar root is bracketed
and bisected to approximately 1e-48 relative t, then checked with direct
mpmath quadrature. Flat/quadratic use their direct inverse controls plus the
same quadrature check. Selected extreme centers are recomputed at90 digits.
No interval bounds are claimed. At most1000 scalar root/integral anchors;
algebraic evaluation at every saved sample is separately counted.

Acceptance is finite floating agreement: endpoint and sample scaled errors at
each tolerance must be <=max(1e-9,500*rtol), and the parent's Richardson
arrival derivative must agree with the exact ratio within2e-5 relative.
The endpoint/root comparison uses actual stored te and distance and separately
checks those against the frozen query data, so a changed query cannot silently
pass. Analytic first/echo horizon conditions and their failure at the exact
limits are checked separately; omitted echo rays are not invented outcomes.
Direct quadrature/primitive discrepancies must be <1e-45. Float comparison
thresholds are deliberately stated rather than interpreted as rigorous bounds.

Calculate and retain actual errors at all settings, amplified small-L
coefficient error and finite-difference truncation/error separately. No required
monotone convergence rate is asserted; the finite workload can be checked even
where floating roundoff eventually dominates. Precision repeats must agree
to <1e-45 in relative arrival time. Each cutoff is frozen before output exposure.

Catch proofs operate only on reviewer-owned copies: invert a nonflat receive
frequency, reverse a saved spatial tangent without changing the supplied branch,
and shift reception off the worldline incidence. Require the corresponding
independent guard to reject each; a passing original is required first.

Resources: CPU only, one BLAS thread, process address cap2GiB, no grid/GPU,
no wall/CPU timeout. Output is compact JSON plus logs, well below100MiB.
Manual SIGINT/SIGTERM uses ordinary interruption; parent saved artifacts remain
untouched and completed parent queries survive independently of this check.
Source/config drift, >1000 anchors, failed tolerance or quadrature convergence
stops approval and preserves the result/diagnostic. No numeric outcome was read
before INDEPENDENT_FREEZE.json was written.
