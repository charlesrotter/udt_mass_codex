# FAC1 Kerr recovery supplement — mathematical review

Verdict: **VERIFIED-WITH-CAVEATS** at the supplement's stated conditional scope.
No defect found. This same-model exposed review extends the already sealed
DIRECT_REVIEW.md; it does not modify that review or its source-first history.
The reviewed supplement is KERR_RECOVERY_APPLICATION.md, SHA
`4641cb612b5dedef520801b13de6152c445cd1c9481ff582b373fcae3cadbb13`,
with SCIENCE_SUPPLEMENT.json bound to the unchanged initial SCIENCE_FREEZE.

Kerr is analytic near the specified regular exterior event, and a local
analytic coordinate with the prescribed nonzero cotangent at that point exists.
For f=epsilon*tau²/2, tau(q)=0 gives f=df=0 and
Hess f=epsilon*d tau tensor d tau exactly at q. Thus the old tangent U remains
unit, calibration and first metric jets match, and the same conformal Ricci
calculation gives Ric_epsilon(U,U)=-3epsilon. The result concerns clocks freshly
prepared with each metric, so the changed free-fall paths are accounted for.

At fixed positive epsilon, each mean consequently has positive quadratic
coefficient epsilon/2. At epsilon=0 the reviewed neighborhood-vacuum theorem
instead gives zero cubic mean and quartic coefficient -1/540 for this Kerr
frame. Analytic ODE/incidence dependence in the local regular tube, with compact
preparation sphere, supplies a common joint Taylor neighborhood. Therefore

    M_±(epsilon,L)=epsilon L²/2-L⁴/540
                    +O(epsilon L³+epsilon L⁴+L⁵)

is justified locally. It is not being inferred from a fitted curve or from
pointwise Ricci flatness alone.

Put h=sqrt(epsilon) and L=hs. After division by h⁴ the mean extends analytically
near h=0 and any fixed positive s near s0. Its limiting expression is
F(s)=s²/2-s⁴/540. The nonzero root has s0²=270, and
F'(s0)=s0-s0³/135=-s0, which is nonzero. The implicit-function theorem thus
gives a sign crossing for each separate mean,

    L_±=sqrt(270)*sqrt(epsilon)+O(epsilon)
       =3sqrt(30)*sqrt(epsilon)+O(epsilon).

For fixed positive s below/above s0 and separated from it, the limiting signs
are respectively positive/negative. This proves local crossings; it does not
prove global uniqueness, a common finite positive interval, positivity for all
observers/events, or any distant branch. For every fixed sufficiently small
L0>0 the vacuum mean is negative, so continuity makes that query negative for
small enough epsilon. Thus no epsilon-independent positive initial interval can
survive this family. This is compatible with positive means on an interval for
every fixed epsilon>0, because the interval shrinks.

The coordinate tau and perturbation amplitude are supplied choices. The
coefficients use M=1; if Kerr lengths are restored, the quartic scales as M^-4
and the leading crossing length as M²*sqrt(epsilon). No physical mass, amplitude,
preferred time, native metric, positional attribution or selected scale follows.
The construction is not a requirement that this exact strong-field Kerr
laboratory fall within UDT's empirical recovery regime.

No additional numerical run was needed: this is a same-premise analytic
consequence of the reviewed FAC-Q/FAC-K coefficient, exact conformal Ricci
calculation and previously reviewed smooth-dependence argument. The supplement
does not change the direct review's caveats, does not provide a numerical sign
radius, and leaves central-edition fidelity and repository closure gates pending.
