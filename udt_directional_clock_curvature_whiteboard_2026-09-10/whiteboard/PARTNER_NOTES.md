# Construction partner: ambiguity witnesses

Date: 2026-09-10. Scope: the parent `WORK_ORDER.md` and `DATA_FREEZE.md`.
This is construction work, **not independent adversarial review**, scientific promotion,
or a new-mathematics claim. Runtime model/version: **UNATTESTED**. Python 3.10.12,
SymPy 1.13.1. No different-model, physical-instrument, or empirical claim.

The partner attributes top-level startup and premise audit to the parent. Its own
read-only check found branch `grok`, HEAD `896da97dc2484b72fa346d0c0ab17055a1dd6fcd`,
no tracked dirt, and the dispatched untracked material. Protected payload was not read.
Assigned method/source reads are hashed in `SOURCE_SHA256SUMS`. G215/G216 constrain
comparison-clock typing; G220 owns the supplied regular null-clock evaluation. NCI1 is
reviewed with caveats and UNPROMOTED, with its normalization repair retained. G358 is
a different ideal Jacobi-curvature record map in a conditional Einstein arena; it does
not already own this arbitrary-metric clock-plus-motion inverse application. Its
curvature-slot convention was checked without importing its Einstein restriction.

## Record map and scope

Every witness is an actual smooth local Lorentz metric of signature (-,+,+,+), with
its displayed smooth future unit observer field. Parameters are free real constants
within the stated domains; no physical value, boundary, source, or metric response
equation is chosen. Symmetry is an explicit counterexample construction, not a
restriction on the general theorem or on UDT. There are no grids, approximations,
fitted profiles, GPU processes, or numerical tolerances.

Use the parent convention R(X,Y)Z=∇_X∇_Y Z−∇_Y∇_X Z−∇_[X,Y] Z and
Ric(U,U)=sum_i g(R(e_i,U)U,e_i). Set W=w_ab w^ab with **no factor 1/2**.
At a matched event compare the spatial unit direction spheres by the displayed
orthonormal frames. The target is factorization through the declared record map on
metric/congruence germs. Complete metric arrays are not themselves reconstruction
data. Supplying them would trivially permit direct curvature calculation.

The null-clock identity is q(n)=−H−a·n−sigma(n,n), H=(div U)/3, with the
normalization in `DATA_FREEZE.md`. A null-affine derivative of a single record is not
the observer-time derivative of its mean. A Fermi–Walker or rotating orthonormal
frame gives the same angular mean and its proper-time derivative.

## 1. Acceleration-divergence ambiguity

In coordinates (t,x,y,z), let r²=x²+y²+z² and

    N=1+kappa r²/2,   g=−N²dt²+dx²+dy²+dz²,   U=N^−1 partial_t.

For each real kappa restrict to an open neighborhood with N>0. This is exact,
smooth, and Lorentzian. Take p=(0,0,0,0) and the central observer gamma(t)=(t,0,0,0).
The spatial coordinate vectors are orthonormal and Fermi–Walker transported there.

Directly, a=grad(log N), theta=sigma=w=0. Hence q(n)=−a·n; at every central
observer time q(n)=0 for every n, and every observer-time derivative is zero.
The central acceleration, including its proper-time derivatives, is zero. Nevertheless,

    A=div a=(1/N) partial_i(N a^i)=Delta N/N=3 kappa/N.

The only nonzero Christoffels involving time are Gamma^0_0i=N_i/N and
Gamma^i_00=N N_i. Their coordinate Ricci contraction gives Ric_00=N Delta N,
so Ric(U,U)=Delta N/N. At p this is **3 kappa**. Thus kappa=0 and kappa≠0 share
the full clock record (even the complete central q history) and W=0 but have
different Ric(U,U). Omitting A defeats universal reconstruction under this map.
Acceleration at p and its derivative along U do not repair that omission.

The direct coordinate symbolic calculation in `check_witnesses.py` obtained these
expressions from metric coefficients, rather than defining Ric through Raychaudhuri.
It also verifies unit norm, zero shear/expansion, and the all-direction q polynomial.

## 2. Vorticity ambiguity

For any real b, use the exact coframe and metric

    theta^0=dt+(b/2)(x dy−y dx),  theta^1=dx, theta^2=dy, theta^3=dz,
    g=−(theta^0)²+(theta^1)²+(theta^2)²+(theta^3)²,   U=partial_t.

The coframe is invertible with determinant 1, so this is a smooth Lorentz metric;
no coordinate-size cutoff is needed for that assertion. Only a sufficiently small
regular local null-query neighborhood is used. U is a unit timelike Killing field
(time-independent coefficients and g_00=−1), hence a=theta=sigma=0 and A=0.
Therefore q(n)=0 at every point and direction, as are all chosen derivatives.

Here U_flat=−theta^0 and dU_flat=−b dx wedge dy. Since U is Killing and
geodesic, w_12=−b/2 in the displayed spatial coframe, with w_21=b/2. Thus
W=2(b²/4)=b²/2. A direct curvature argument is available without the target
kinematic identity. The dual spatial frame satisfies

    [e1,e2]=−b U,   [U,e_i]=0,
    ∇_e1 U=∇_U e1=−(b/2)e2,
    ∇_e2 U=∇_U e2= (b/2)e1,   ∇_U U=∇_e3 U=0.

These connection coefficients follow from the metric Koszul formula. Consequently
R(e1,U)U=(b²/4)e1, R(e2,U)U=(b²/4)e2, R(e3,U)U=0, and

    Ric(U,U)=b²/2.

The symbolic coordinate computation independently of this frame argument yields
that same expression directly from g and its derivatives. It is a second
constructor calculation, not a separate-context review. Comparing b=0 with b≠0
gives identical clock records and A=0 but different Ric(U,U), so omitting W fails.
Vorticity is an antisymmetric spatial derivative of the **congruence**. It is not
the arbitrary rotation of a reporting frame; choosing a nonrotating frame does not
set w=0.

There is a stronger but carefully limited scalar-value statement. Because U is
Killing, g(U,k) is constant on every affinely parametrized null geodesic. Every
G220 scalar depth delta_AB is therefore zero on every regular branch in each
member. **This is not equality of complete finite null-query datasets.** Their
event-pair incidence domains, additive pairing offsets, flight times, endpoint
coordinates, path shapes and screen/frame transport can differ. Knowing the full
null incidence relation is additional data. No equality of full reciprocal kernels,
pair pullbacks, or all operational observations is asserted.

## 3. Missing observer-time mean derivative

Take g=−dt²+F(t)²(dx²+dy²+dz²), U=partial_t, with
F(t)=exp(beta t²/2)>0 for arbitrary real beta. At t=0 all members have the same
metric-unit coordinate frame. The congruence is geodesic and irrotational, A=W=0,
and H=beta t, sigma=0. Thus q(n)=m=−beta t, so q_p(n)=0 for all beta, while
dot m=−beta. The direct Christoffel contraction gives

    Ric(U,U)=−3 F''/F=−3(beta+beta²t²).

At t=0 the target is −3 beta. Therefore q_p alone, even together with A and W,
does not determine it. The missing dot m is ordinary additional derivative data,
not newly created from a single event's ratios.

## 4. Missing even directional quadrupole

Take g=−dt²+exp(2s t)dx²+exp(−2s t)dy²+dz² and U=partial_t, with real s.
The orthonormal frame e_i=F_i^−1 partial_i is parallel along U. The directional
rates are (s,−s,0): H=0, sigma=diag(s,−s,0), a=w=0. Thus A=W=0,

    q(n)=−s(n1²−n2²),  m=dot m=0,  Ric(U,U)=−2s².

Here sigma_ab sigma^ab=2s² and V=4s²/15. The controls s=0 and s≠0 have
identical mean-only records and motion scalars but different targets. They are
distinguished by the retained even quadrupole. This is an omission counterexample
for a mean-only map, not a failure of the full q map. NCI1 already gives the
diagonal homogeneous kinematics; the curvature comparison is the present application.

For either diagonal family, direct metric differentiation yields
Gamma^i_0i=F_i'/F_i and Gamma^0_ii=F_i F_i', with other time-coupled terms zero.
Then Ric_00=−sum_i[partial_t(F_i'/F_i)+(F_i'/F_i)²]. The additional script
checks these exact expressions and the stated controls. It does not certify them
by substituting the target reconstruction formula into itself.

## Evidence and chronology

The static-lapse and twist examples were anticipated and first checked during
pre-freeze mathematical exploration. They are **not** blind confirmation data or
a predicted observational outcome. `/tmp/udt_clock_partner_20260910/` holds the
original exploratory files; the parent subsequently assigned this `whiteboard/`
subdirectory and the files were copied here without changing their bytes.

The first exact command was:

    python3 /tmp/udt_clock_partner_20260910/check_witnesses.py

It failed before any witness result because a SymPy Matrix(4,1,...) callback was
declared `lambda a` instead of `lambda a,_`. `INITIAL_check_witnesses.py`,
`INITIAL_STDOUT.txt` and `INITIAL_STDERR.txt` preserve that source and a reproduced
failure. `REPAIR_NOTE.txt` records the one-argument correction. No metric,
equation, domain, tolerance, hypothesis, or desired result changed. The corrected
command (same path) exited 0. `STDOUT.txt`, `STDERR.txt`, `CHECK_OUTPUT.txt`, and
`CHECK_RESULT.json` preserve its actual outputs; the initial `SHA256SUMS` covers
the corrected source and two generated result files only.

Post-freeze additional check:

    python3 udt_directional_clock_curvature_whiteboard_2026-09-10/whiteboard/check_additional_witnesses.py

This command is run by a subprocess capture with timeout=120 seconds; stdout,
stderr, exit code, and the exact command are saved. The original exploratory
commands predated that explicit timeout control and were not timeout-wrapped;
observed runtime was under two seconds and no process remained running. This is
disclosed rather than retroactively describing them as timeout-controlled.

These witnesses support only the specified failure-of-reconstruction quantifiers.
No number of examples proves a complete census, minimum-information theorem,
metric selection law, physical signal identification, or instrument access to A/W.
For the scalar target the combination A+W suffices algebraically; separating them
is transparent provenance, not an absolute information-theoretic minimum.
