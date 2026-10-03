# CBR1 implementation inspection before main outcome exposure

Reviewed forward.py, inverse.py, RUN_PLAN and smoke as listed in EXPOSED_PLAN.
No main benchmark outcome has been read when this note is written. This is an
exposed implementation review; source-first independence was sealed earlier.

For g=-dt²+a(t)² dx² the nonzero connection terms used are
Gamma(t,ij)=a²H delta_ij and Gamma(i,tj)=H delta_ij. The preparation ODE evolves
a unit spacelike tangent V and independently transports U using those connection
terms. Initial boosted U and longitudinal/transverse N are orthonormal. The
reported norm/orthogonality checks are consistency residuals, not a separate
proof of a correct connection; direct inspection establishes the displayed
equations' agreement with this supplied metric.

Timelike geodesic spatial momentum K=a²u^i is constant and u^t=sqrt(1+K²/a²).
Thus x(t)=x0+K integral dt/[a²sqrt(1+K²/a²)]. In the flat spatial slices a null
ray satisfies |xr-xe|=integral dt/a and has conserved spatial covector direction
n. Its endpoint frequency, up to one common normalization, is u^t/a-n.u^i.
The code computes the prepared receiver worldline, roots this incidence
relation, then uses the ratio of endpoint frequencies for the proper period
ratio. It does not insert T, Ric or a leading clock series into output logs.
Calling observe with an emission_offset keeps the same preparation (t0,L,U,N),
which is the fixed-worldline differentiation required by PSW1.

The forward positive metric is constructed using the UNADOPTED ERC1 comparison
equation. That truth is explicitly outside inverse.py; recovering its trace
cannot validate the physical equation. Although ah() calls a state vector that
contains H,R,P, only a,H enter the forward geodesic/transport formulas. H enters
as a connection derivative, not as a curvature oracle supplied to the inverse.

Isotropy and homogeneity justify three forward classes for21 directional/frame
labels and one spatial-site time for six positions. The chosen rest triads can
be reordered to put the longitudinal direction first in every boosted frame.
Those copies are not independent geometric experiments. Synthetic independent
perturbations of serialized copies are permitted by the frozen noise experiment
but do not demonstrate independent apparatus errors or add ideal information.

The spatial site uses the actual exponential map. Independently, t(s)=t0−H0 s²/2
+O(s⁴) along the comoving unit spatial geodesic, so its six scalar samples
contribute −3H R' in the Box limit. Substituting constant-coordinate-time offsets
would miss that term; a constant-R or H=0 control alone would hide the defect.
Synthetic metric knowledge supplies placement calibration and frame setup;
physical calibration capability has not been established.

Inverse input rows contain only case/center/site labels, proper h/L, frame and
direction, and log p; a global declared speed is supplied. The implementation
does not import the forward module or a curvature/equation/oracle. Its weights
match CMF1, it preserves the shared center weight−4, and its Richardson step is
preselected. Finite bias is not bounded solely by the deterministic noise bound.
The endpoint fit and three interior holdouts match RUN_PLAN. An uninformative
status means failure to infer parameters at this chosen resolution; it is not
proof of a constant scalar field, equation compatibility or alpha's absence.

Independent50-digit Decimal recombination of all2268 smoke records disagrees
with parent by at most1.023e-17 in R and2.881e-14 in Q. It imports no parent code.
This checks the inverse mapping on the saved records, not the forward geometry's
truth. The source version used for that replay is preserved byte-for-byte as
replay_inverse_smoke_initial.py. A subsequent explicit row-label range guard
changes validation only; current replay_inverse.py is used for main replay.

No implementation defect requiring parent repair was found in this bounded
inspection. Main numerical accuracy, noise behavior, scalar/full-tensor
discrimination and final central integration remain pending their actual data.
