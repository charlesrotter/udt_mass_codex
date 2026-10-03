# IEC1 fidelity reviewer: source-first design

Fresh separate context `/root/iec_fidelity`, inherited parent model (no different
model claimed), 2026-10-03. Source-first means no IEC construction/candidate,
code, coefficients or output read. The task prompt, IEC WORK_ORDER/BASELINE and
the existing PSW/ECS/FCW central/source claims were exposed. Parent startup,
synchronization, prior full406 and host-process evidence is attributed to
WORK_ORDER/BASELINE; this reviewer independently read grok HEAD7186fc34, current
status and the assigned scientific sources. Existing unrelated untracked work is
preserved without payload inspection. Only this review directory is writable.

The live argument fixes ordinary proper clocks, PSW preparation and actual
immediate future return. W4 remains WORKING/POSIT; W5/W6 are working
clarifications, not geometry equations. ULC1 supplies one law with circumstance-
dependent comparisons, not FC scalar sufficiency. Local symmetry and every
comparison parameter below are FREE-AND-EXPLORED supplied restrictions. FC and
RG remain UNADOPTED. No native geometry, equation, scale or positional assignment
will be inferred from the control.

## Question, frame and scope

Independently construct a contrasting Lorentz4 locally symmetric control:
ultrastatic time times three-space of constant sectional curvature K. Its clocks
and rays use the same metric. Determine the actual small-L echo discrepancy
through L6 by original incidence. In addition to transverse preparation, tilt
the preparation direction within U-perp so both R(n,U)U and R(n,U)n may leave
span(U,n). This tests the unproved possibility of lower-order cancellation.
Do not substitute a target coefficient into the clock problem.

Construction is analytic, with exact rational polynomial algebra to finite
degree8 in incidence. A small high-precision root check supports branch and
coefficient handling, not the analytic proof or a certified error constant.
Two nontrivial supplied preparation families (u=3/4, gamma=5/4, tilt b=0 or3/5),
plus u=0 flat-clock control are allowed, with either sign K; at most30 scalar
checks total. This is one scientific script. No tensor classification, unbounded
boost limit, physical data, GPU or long solve. No inherited candidate code.

CPU Python/SymPy/mpmath; one BLAS thread; capture.py with2GiB virtual memory,
no elapsed/CPU timeout, finite degree/family/case stops and manual interruption.
Outputs are small JSON and stdout/stderr. Stop if symbolic polynomial sizes
exceed the finite design or memory ceiling. One same-premise implementation repair
is authorized and must preserve the original. Maximum conclusion: an exact
conditional control coefficient/counterexample, source-fidelity verdict or gap.

## Independent incidence design

Write U=gamma e0+u ey, m=u e0+gamma ey and n=a ex+b m,
a2+b2=1, gamma2-u2=1. Set h2=1+b2u2 and d=b gamma/h.
Along spacelike preparation the initial time coordinate changes by b u L,
while the spatial geodesic length is h L. The spatial initial clock tangent
ey is parallel-transported along that geodesic. For K=1 sphere embedding,

 B0=cos(hL)X0+sin(hL)n_sp/h,
 ey_B=ey+d[-sin(hL)X0+(cos(hL)-1)n_sp/h],
 A_sp(s)=cos(us)X0+sin(us)ey,
 B_sp(t)=cos(ut)B0+sin(ut)ey_B,
 A_time(s)=gamma s, B_time(t)=b u L+gamma t.

The radius-one embedding is only notation here; general K follows by rescaling
and the signed trigonometric functions. The free clocks have unit norm because
their spatial speed is u and time speed is gamma. B's initial tangent is exactly
parallel-transported U. Product Levi-Civita curvature has nabla Riemann=0.
In a small convex neighborhood, an ultrastatic null ray has time difference
equal to the unique spatial geodesic length. Its original scalar incidence is

 F(s,t,L)=cos(u(s-t))
 +(cos(hL)-1)[cos(us)cos(ut)+d2 sin(us)sin(ut)]
 -d sin(hL)sin(u(t-s))-cos(gamma(t-s)+b u L)=0.

This comes from the spatial embedding inner product, not an echo ansatz. For
K<0 replace cos by cosh and each corresponding sine-product sign according to
the constant-curvature inner product; the script uses signed Taylor coefficients.

At the first incidence t=f(s), p=-F_s/F_t. At the later return A time r=g(t),
F(r,t,L)=0 and q=-F_t/F_s at (r,t). A tilted preparation need not have a
clock-exchanging isometry that preserves both velocities, so do NOT silently
replace q by f'(f(0)). The return root has r>t in the L-scaled Minkowski limit
and positive product-time difference. The same fixed prepared worldlines are
used at all neighboring emissions.

After s=Lx,t=Ly, F/(K L2) tends to ((y-x)2-1)/2. Its first root y=x+1 has
nonzero derivative. The return swap has the same root. Analytic implicit
dependence gives even power series with differentiable remainders for fixed
finite supplied u,b,K and sufficiently small L, retaining a unique direct future
branch. No uniform high-boost or finite-distance remainder bound is claimed.

The script solves the two implicit branches separately from degree8 incidence,
composes the return at the actual first arrival, and forms log q-log[p/(2-p2)].
Tests: scaled leading incidence, leading PSW coefficients, exact zero control,
future branch, high-precision original-incidence residual, and O(L8) behavior of
the truncated D. Test output is evidence for this finite control only.
