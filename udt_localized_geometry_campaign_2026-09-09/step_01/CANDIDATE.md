# LG1 — local matching gates (initial frozen candidate)

UNPROMOTED conditional mathematics; author/root context,2026-09-09. Question,
premises and resource freeze: ../CAMPAIGN_LOG.md. No physical identification.

## Exact scope and ownership

Take the supplied G324 compact Taub/Kasner quotient at T0>0, with an embedded
Euclidean ball smaller than the injectivity scale. In constant rescaled spatial
coordinates on the ball its data are

    gamma0=I, K0=diag(a,-2a,-2a), a=1/(3T0)>0, tau0=-3a.

Our sign convention is K=-one-half of the future normal metric derivative.
G310/G312 supply the OWNER-PROVISIONAL vacuum equation, not a derived physical
law: Ric=Lambda g with connected constant Lambda. G303/G315 give the constraints

    H=R(gamma)+tau^2-|K|^2=2Lambda,
    M_i=D_j K^j_i-d_i tau=0.

Matching BOTH gamma and K to the Ricci-flat background on an exterior open set
forces Lambda=0 for this comparison. This is not UDT selection of Lambda.
Topology/marking/background/T0/matching balls are supplied data. The ball and
collar are bookkeeping domains, not physical boundaries or X_max.

Consider smooth positive gamma and symmetric K on the same compact slice,
equal to background near and outside the outer boundary. Let h=gamma-gamma0
and p=pi-pi0, where pi^{ij}=sqrt(det gamma)(K^{ij}-tau gamma^{ij}) is a
contravariant tensor DENSITY. Do not confuse p with a change in covariant K.

## Claim A: full local adjoint symmetry space

On a connected embedded ball or connected annular collar the local vacuum
Killing-initial-data (KID) space has dimension four, all zero lapse:

    (0,d_x), (0,d_y), (0,d_z), (0,y d_z-z d_y).

Here a KID means a solution of the full formal-adjoint vacuum-constraint
equations, equivalently the initial restriction of a local spacetime Killing
field in the justified development. This equivalence is a standard mathematical
method, not an extra UDT premise (Chrusciel--Isenberg--Pollack, gr-qc/0403066,
section1). The following proof uses the ACTUAL G324 spacetime, not an arbitrary
direction field or a finite-mode count.

Write its metric as -dT^2+A^2 T^(-2/3)dX^2+B^2 T^(4/3)(dy^2+dz^2).
Its Kretschmann scalar is 64/(27T^4), with nonzero derivative for T>0.
Consequently every spacetime Killing field Z has Z^T=0 on any open domain.
The Ti Killing equations then give d_T Z^i=0. The Xi spatial cross-equations,
with their unequal time powers, separately require d_X Z^y=d_y Z^X=0 and
d_X Z^z=d_z Z^X=0. The XX equation gives d_X Z^X=0. The remaining two-dimensional
Euclidean Killing equations yield only two translations and the yz rotation.
These coefficients are constant on the connected domain. All four fields
actually solve the Killing equation. Thus this is the FULL local space, not
merely four displayed examples. The rotation usually does not descend to a
periodic quotient; its absence globally does not remove its local matching gate.
No time-lapse adjoint mode survives on this nonflat background. This does not
claim absence of scalar nonlinear constraints or a general absence of energy.

For a supported linear correction satisfying the linearized constraints P u=f,
integration against each of these adjoint modes requires its pairing with f to
vanish (up to the fixed, immaterial normalization of the momentum constraint).
These four necessary adjoint conditions are NOT a sufficiency/range theorem.
A generic local gluing theorem assuming no local KIDs cannot be applied directly.

## Claim B: exact finite and tangent matching identities

For EVERY exact smooth completion in the stated class and each of the four Y,

    integral_B p^{ij} (L_Y h)_{ij} d^3x = 0.                  (1)

The original nonlinear momentum equation in the chosen coordinates is

    sqrt(det gamma) M_i
      = d_j(gamma_ik pi^{jk}) - (1/2) pi^{jk} d_i gamma_jk.

Contract with Y and integrate by parts, using the full covariant-tensor Lie
derivative: integral pi:L_Y gamma equals twice the associated boundary flux.
The boundary flux agrees exactly with background because BOTH initial tensors
match there. Subtract the background identity. L_Y gamma0=0; also L_Y pi0=0
as a tensor density, since Y preserves gamma0 and K0. Integration by parts and
compact support therefore kill integral pi0:L_Y h. This leaves (1).
Rotational L_Y h includes the index-rotation terms, not just Y^k d_k h_ij.
No field equation has been replaced by this integrated test.

For a twice differentiable exact family through background, put
u=d_e gamma|0 and v=d_e pi|0. Differentiating (1) twice gives

    integral_B v^{ij}(L_Y u)_{ij} d^3x = 0.                (2)

The second derivatives of gamma and pi do not appear. Thus arbitrary compactly
supported higher-order corrections cannot repair a violated tangent condition.
The statement presupposes an actual differentiable exact family; it is NOT a
classification of every isolated exact solution. It does not require fixing
the higher-order lapse/slicing description of its later development.

Splitting B into prescribed interior and free collar makes (1) an exact
interior-plus-collar balance. A nonzero interior contribution does not prohibit
localization if the collar can compensate. Conversely a balance total of zero
does not solve the pointwise constraints, positivity, matching regularity, or
the subsequent evolution problem. Matching metric alone is insufficient.

## Checks, controls and limits

author_check.py recomputes the four-dimensional curvature contraction directly
from the diagonal metric, solves the spatial antisymmetric-generator commutant,
and checks the density first variation. Invalid data with gamma=I and
K=K0+epsilon b I pass all four finite integrated gates (h=0) while violating H;
that deliberate control prevents a false sufficiency claim. It is not lawful
data and is not counterevidence against UDT. The exact proof, not these finite
checks, supplies the universal quantifiers. Author checks are same-context;
fresh review is required before LG2 uses LG1.

No localization existence theorem, generic obstruction, physical content,
conservation-law adoption, stability, or particle claim is made here.
NR1--NR2 motivated the question but are not mathematical dependencies of this
independent local proof; they remain unpromoted. The existing full365 G325
failure is not repaired or waived. LG1 is unpromoted regardless of review.

Primary method reference: https://arxiv.org/pdf/gr-qc/0403066 (v2), section1.
Source SHA256 manifest identifies the repository premise/equation versions.
