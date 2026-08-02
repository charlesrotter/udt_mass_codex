# Preregistration — intrinsic projector across a general-screen neighborhood

Date: 2026-08-02  
Branch: `grok`  
Preregistration base: `662d9ca95735a4768c5cb3a09e2b3f375e1a770f`

## Whole question

Within the same stationary, off-shell, complete `R x S3` configuration arena as the verified
intrinsic-contact witness, release the angular screen determinant and both independent screen
shears. Determine, without targeting a desired physical result:

1. which registered metrics retain a unique timelike Killing line and nonzero twist line, so the
   reciprocal pair/screen projector is intrinsic;
2. where the alternating depth/area object `dphi wedge dsigma` is zero or nonzero;
3. where symmetry enhancement, twist loss, slice-null or slice-negative behavior, metric
   degeneration, or failure of the intrinsic-projector certificate occurs; and
4. whether the previously verified witness sits inside an open family that simultaneously permits
   independently varying screen area and both shear modes.

This is a metric-led configuration-space audit. It does not target a nonzero alternating form,
matter, a carrier, a preferred screen, or an action.

## Exact bounded metric family

Use unit-quaternion coordinates `q0,q1,q2,q3`, with `sum q_i^2=1`, and the standard global
Maurer-Cartan coframe `sigma1,sigma2,sigma3` on `S3`. Unless a control says otherwise,

```text
u=exp(2 phi)=3+q0^2+2 q1^2+4 q2^2+8 q3^2,   4 <= u <= 11,
theta0=u^(-1/2)(dt+a sigma3),
theta1=u^(+1/2)sigma3,
g_pair=-theta0^2+theta1^2.
```

The angular metric, expressed in the fixed Maurer-Cartan screen basis, is

```text
g_screen = u^lambda V [r^2 sigma1^2
                       +2 r b sigma1 sigma2
                       +(b^2+r^(-2)) sigma2^2].
```

The bracketed screen matrix has determinant one. Therefore the oriented screen-coframe determinant
is

```text
D=u^lambda V,
sigma=log(D/D0),
```

where `D0>0` is only an additive reference. The exact preregistered profiles are

```text
V0=q0^2+3 q1^2+7 q2^2+9 q3^2,
R0=2 q0^2+5 q1^2+11 q2^2+13 q3^2,
B0=q0 q1+2 q0 q2+3 q0 q3+5 q1 q2+7 q1 q3+11 q2 q3,
epsilon=1/10,
V=1+epsilon V0,
r=1+epsilon R0,
b=epsilon B0.
```

Thus `V>0` and `r>0` globally for every registered nondegenerate profile. `epsilon=0` returns the
isotropic-screen parent continuously. No profile, point, candidate, or epsilon value may be added
after outcome.

## Exact registered candidate universe

`CANDIDATE_UNIVERSE.tsv` freezes all 18 candidates. It includes three parent metrics; separate
area, diagonal-shear, and off-diagonal-shear releases; the combined screens at all three registered
`lambda`; area-slaved and constant-area rank-zero controls; constant-depth and homogeneous
controls; twist-free, slice-null, slice-sign-changing, and degenerate controls.

For every nondegenerate candidate the primary exact curvature certificate is evaluated at both
fixed stereographic points

```text
p1=(x,y,z)=(1/5, 1/7, 1/11),
p2=(x,y,z)=(1/3,-1/5, 1/7),
```

using `q0=(1-rho^2)/(1+rho^2)` and `(q1,q2,q3)=2(x,y,z)/(1+rho^2)`. A nonzero exact determinant at
either point certifies the stated dense-open result. Two zero samples are only `INCONCLUSIVE`, not
a certificate of extra symmetry. The homogeneous control is separately classified by its exact
global symmetries.

## Intrinsic-projector test

The ever-present stationary Killing field is `K=partial_t`, with `g(K,K)=-1/u`. To establish that
its line is metric-selected, compute the three scalar invariants

```text
I1=R,
I2=Ric_ab Ric^ab,
I3=Ric_a^b Ric_b^c Ric_c^a
```

and the spatial Jacobian determinant

```text
J=det[partial_(x,y,z)(I1,I2,I3)].
```

If `J` is exactly nonzero at a point, no nonzero spatial component of any local Killing field can
survive there. The Killing equation then restricts the remaining field to a constant multiple of
`partial_t`; analyticity carries this unique line over the connected dense-open branch. This route
also covers candidates whose hypothetical Killing coefficients depend on time.

For a nonzero registered twist parameter `a`, reconstruct the normalized timelike line `T`, its
metric twist line `S`, the intrinsic pair projector, and the orthogonal screen projector before
forming projected twist norms. Never treat the displayed coframe slots as intrinsic after a passive
frame change.

The formulas under test, not assumed as outcomes, are

```text
Q_T=4 a^2/(u D^2),
Q_S=4 u/D^2,
Q=Q_S-Q_T=4(u-a^2/u)/D^2,
Phi_contact=(1/4)log(Q_S/Q_T)=phi-(1/2)log|a|.
```

`a=1` is the existence-unit parent. The twist-free candidate `a=0` must not be assigned a ruler
line or pair projector by continuity through the singular formula.

## Alternating depth/area classification

For every nondegenerate screen,

```text
dphi wedge dsigma
  = dphi wedge dlog(V)
  = (du wedge dV)/(2 u V).
```

The two shear profiles do not enter this determinant identity directly, but they remain active in
the full metric and may alter the curvature/Killing certificate. The registered exterior class is
`ZERO` when the two-form vanishes identically and `NONZERO_SIMPLE` when it is nonzero on an open
set. Here `SIMPLE` means one decomposable wedge; it is not a claim that the associated antisymmetric
matrix has rank one.

An exact nonzero coefficient at either registered point proves `NONZERO_SIMPLE` on a neighborhood.
Global analytic nonidentity then makes the nonzero set open and dense relative to the connected
analytic branch; its exact zero locus is retained rather than discarded. Constant `V`, `V=u`, or
constant `u` are preregistered zero controls.

## Neighborhood statement under test

For each `lambda in {-1,0,+1}`, the parent exact invariant Jacobian is already nonzero at a fixed
point. Curvature invariants and their first derivatives depend continuously on a nondegenerate
metric through its finite jet. If the registered computations reproduce the parent determinant,
there exists some open `C^3` neighborhood of the parent in which the unique Killing-line
certificate persists. The analytic `epsilon` profiles converge to that parent as `epsilon -> 0`.

If `du wedge dV0` is also exactly nonzero, every sufficiently small `epsilon != 0` produces an
independent area response together with both independently supplied shear profiles while the
projector certificate persists. This would be an existence/open-neighborhood result only. It would
not select the profiles, quantify a universal neighborhood radius, or supply an equation.

The explicit `epsilon=1/10` candidates are computed separately, so the concrete witness result does
not rely solely on an unquantified continuity statement.

## Causal and degeneration controls

- `a=4`: `Q=0` exactly at `u=4` and `Q>0` for `u>4`.
- `a=5`: `Q<0` for `4<=u<5`, `Q=0` at `u=5`, and `Q>0` for `u>5`.
- These are pair-derived causal/slice-sign strata, not selected physical branches. The four-metric
  remains Lorentzian and nondegenerate while the coframe is invertible.
- `V=0`: the screen and four-metric are degenerate. Curvature and inverse-metric calculations must
  be skipped, not regularized or silently continued.

## Certification, falsification, and independence

Production will use exact rational Taylor-jet curvature algebra, not floating thresholds. Every
nonzero certificate and alternating-form coefficient must be stored exactly. A fresh adversarial
implementation must rebuild the coordinate metric, curvature invariants, projector quantities, and
registered controls without importing production functions. Numerical autodifferentiation may be a
secondary regression check, but it cannot replace the exact load-bearing nonzero/zero certificates.

Every mutation in `FALSIFICATION_CONTRACT.tsv` must be exercised. No outcome-dependent candidate
cut, point change, profile retuning, or reinterpretation is allowed.

## Maximum allowed conclusion

At most:

1. an exact explicit off-shell complete-cell coexistence atlas for the 18 registered candidates;
2. an analytic open-neighborhood existence statement around the three parent witnesses, if its
   exact premises pass;
3. exact local/open-dense alternating-form classes for the registered analytic profiles; and
4. exact causal and degeneracy strata for the registered `a` and `V` controls.

No on-shell or physical screen selection, universal full-screen theorem, response/dynamical law,
action, source, boundary, density/bootstrap value, carrier, `X_max`, matter, mass, stability,
phenomenology, GPU work, or canonization may follow.
