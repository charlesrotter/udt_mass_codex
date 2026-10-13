# GRC1-A supplement: optical reciprocity and conformal domain selection

**UNREVIEWED CONDITIONAL CANDIDATE; all physical trials UNADOPTED.** This
supplements, and does not edit or replace, the frozen initial CANDIDATE.md
(`07c14efd301fc3337e747fd312d647265454c61e6791e22c5420df6b3b7377fb`).
Baseline is grok `89b4b473bed869f5ca296e9bfc67559a3c9ceaff`. The question is
whether ordinary optical reciprocity supplies the extra geometry restriction,
and what a physically specified conformal reference adds to the clock-sign
proposal. There is no source equation, matter model, fitting, action,
independent physical field, native UDT adoption, or canon claim here.

## 1. Optical reciprocity leaves radial null curvature free

Use the initial candidate's spherical metric, regular r>0 patch and an affine
radial null geodesic gamma(lambda). The metric optical screen is isotropic
along this ray. With curvature convention

    A(X,Y,Z,W)=g(W,R(X,Y)Z),
    Ric(k,k)=sum_i A(e_i,k,k,e_i),

its transverse Jacobi equation is

    D'' + (Ric(k,k)/2)D = 0,
    Ric(k,k) = -2r''/r.

Spherical rotations give a Jacobi solution r; reduction of order gives the
vertex-normalized fundamental solution on any interval where r>0:

    D_e(lambda) = r_e r(lambda) integral_[lambda_e,lambda] ds/r(s)^2,
    D_e(lambda_e)=0, D'_e(lambda_e)=1.                         (S1)

Differentiating proves the equation directly. Antisymmetry of the integral
then gives

    D_e(lambda_o) = -D_o(lambda_e)                            (S2)

for arbitrary r''. This is the scalar spherical version of the Jacobi-map
reciprocity identity. A local angular launch displacement at e has transverse
initial tangent omega_e delta n, so its physical transverse map is omega_e
D_e(o); the map with endpoints interchanged has magnitude omega_o |D_o(e)|.
Their positive area-distance factors therefore have ratio omega_e/omega_o=Z.
Screens and affine normalization are matched along the same ray. This reverses
the same geometric segment mathematically; it does not identify a second
future signal with the past-directed reverse segment. The statement concerns
linear optical maps, not a finite-angle beam, flux, photon number, luminosity
law, or two-leg future clock experiment.

The general symplectic origin and endpoint frequency factors were inspected
in the primary article [Algebraic symmetries of the observables on the sky:
Variable emitters and observers](https://arxiv.org/html/2405.05105v1), eq(47),
the Jacobi/magnification discussion around eq(140), and section V.4. No
claim of a complete catalog of optical identities is used here; (S1)-(S2)
are proved directly within the stated spherical domain.

**Metric-realized counterexample.** Supply H>0 and

    g = -exp(Ht)dt^2 + exp(-Ht)dr^2 + r^2 dOmega^2.

On the regular ray t=lambda, r=exp(Hlambda)/H, k=(1,exp(Ht),0,0) is null
and affine. Direct original-coordinate curvature gives Ric(k,k)=-2H^2,
while (S1) becomes

    D_e(lambda) = sinh(H(lambda-lambda_e))/H.

It obeys (S2) exactly. Thus optical reciprocity holds although NAR's r''=0
fails. With a flat optical-curvature reference, this also violates an added
no-extra-null-defocusing inequality. Neither restriction follows from
reciprocity. This conclusion does not rely on spherical point-source beams
being identical to the sphere-centered expanding congruence: the
vertex-normalized D solves the transverse Jacobi initial-value problem.

## 2. Conformal null rigidity (CNR): a conditional global consequence

**Physical comparison trial, UNADOPTED:** the extra positional geometry
preserves a supplied reference's unparameterized null paths and cones, using
the same events and

    g = psi^-2 g0,       psi>0, psi in C^2(M),
    I : (T_p M,g) -> (T_p M,g0), I=psi^-1 Id.                 (S3)

This is a physical comparison hypothesis, not a gauge redundancy, native
founding reciprocity, or derived identification. Optical lengths, affine
parameters and clock rates need not be preserved. Supply connected M,
smooth time-oriented Lorentz4 g0, and enough smoothness for the local PSW1
coefficient where that readout is invoked. The theorem's geometric argument
needs only the displayed C^2 curvature/conformal relations.

Adopt provisionally B's **S**: every orthonormal timelike/spacelike pair
U,n of g satisfies the nonnegative additional leading prepared-clock
coefficient

    C(U,n) := -D(n,U,U,n) >= 0,
    D := A_g - I^* A_0.                                    (S4)

The extra attribution, reference matching, and quantifier over all prepared
frames are supplied physical assumptions. They are not extracted from a
single clock pair, angular cancellation, or a measured common scale.

For clarity, the required implication is rederived here. At a point choose
future null k,l with g(k,l)=-1 and a unit screen vector e orthogonal to both.
For each s>0, U_s=(s k+s^-1 l)/sqrt(2) is unit future timelike and e is a
permitted n. Divide D(e,U_s,U_s,e)<=0 by s^2 and take s to infinity:

    D(e,k,k,e) <= 0.

Sum over two screen directions. Because I is an isometry,

    Ric_g(k,k) - Ric_0(Ik,Ik) <= 0.                         (S5)

This limits the algebraic leading coefficient after taking the short-distance
PSW1 limit for each fixed frame. It makes no claim of a uniform finite-distance
remainder under unbounded boosts.

**Theorem (necessary constancy).** In addition to (S3)-(S4), suppose g0 has
zero null Ricci curvature and every maximal g0-affine null geodesic extends
over the entire real affine line. Then psi is constant on connected M.

Proof: the conformal Ricci identity in dimension four is

    Ric_g = Ric_0 + 2 psi^-1 Hess_0(psi)
            + [psi^-1 Box_0 psi - 3 psi^-2 |dpsi|_0^2] g0.

Along any g0-affine null geodesic this reduces to

    Ric_g(k,k) = Ric_0(k,k) + 2 psi''/psi.                   (S6)

(S5) and Ric_0(null,null)=0 give psi''<=0. A positive differentiable concave
function on the entire real line is constant: a nonzero tangent slope would
give an upper supporting line that becomes negative at one end. Hence
dpsi(k)=0 in every null direction. Null directions span each tangent space,
so dpsi=0 and connectedness gives global constancy. QED.

The conformal identity and affine-null reduction are primary-source
equations (2.2)-(2.3),(3.1) of Folkestad and Hernandez-Cuenca,
[Conformal Rigidity from Focusing](https://arxiv.org/pdf/2106.09037).
Their investigated nonnegative null curvature gives the opposite convexity
sign. We use their transformation identity, then prove the concavity
consequence above; their main focusing theorem is not asserted to cover it.
No energy condition or Einstein equation is imported.

The completeness hypothesis is about the **reference g0**. Completeness of g
alone does not replace it. The result is necessary, not sufficient, for full
directional S: a constant rescaling of a curved reference still requires the
full timelike-plane inequalities. Constancy does not set the constant to one
or identify physical common rescalings as gauge. Relative to flat g0 it leaves
zero curvature and zero additional leading PSW1 signal; for curved g0 the
remaining directional test must still be performed. No statement of general
UDT impossibility or generic quiet-GR recovery follows.

## 3. Complete physical control on an incomplete reference domain

To test whether the reference-domain qualification matters, supply Minkowski
g0=-deta^2+dx^2+dy^2+dz^2 on |H eta|<pi/2, H>0, and psi=cos(H eta)>0.
With proper cosmic time

    t = H^-1 log[sec(H eta)+tan(H eta)],

the physical metric is

    g = -dt^2 + a(t)^2 (dx^2+dy^2+dz^2),
    a(t)=cosh(Ht),  t in R.                                (S7)

This free geometric family is a domain control, not a selected cosmology,
source model, or fitted UDT solution. Direct coordinate curvature gives the
orthonormal electric coefficients -A=-a''/a=-H^2 and spatial coefficients
B=(a'/a)^2=H^2 tanh^2(Ht), with zero mixed blocks. For a unit simple timelike
plane bivector U wedge n, its electric/spatial components b,m satisfy
|b|^2-|m|^2=1 and b dot m=0. Relative to flat curvature, (S4) is therefore

    C = A |b|^2 - B |m|^2
      = H^2 [1+sech^2(Ht)|m|^2] > 0.                       (S8)

This verifies full directional S, not just its necessary null trace. Yet
for a reference-affine null k0=(1,n), |n|=1, (S6) gives Ric_g(k0,k0)=-2H^2.
The metric is not spaceform: its scalar curvature
R=6H^2[1+tanh^2(Ht)] is nonconstant, with unequal A and B at every finite t.

**Physical causal completeness.** Spatial translations conserve
P_i=a^2 dx^i/ds for affine geodesics. For a unit timelike geodesic,

    dt/dtau = sqrt(1+|P|^2/a^2),
    d tau/dt >= 1/sqrt(1+|P|^2).

Thus infinite cosmic time in either direction has infinite proper time.
For a nonzero null geodesic, |P|>0,

    dt/dlambda = |P|/a,     d lambda/dt = a/|P|,

and both affine ends diverge as t tends to plus/minus infinity. At finite t,
a>=1 and finite conserved P bound the coordinate velocities; ordinary smooth
geodesic continuation excludes any finite-time endpoint. This proves null
and timelike geodesic completeness, without claiming general spacelike
completeness or relying on a numerical integration.

In contrast, a straight reference null line meets the slab boundary in finite
g0-affine parameter. The reference is null incomplete, as required to evade
the theorem. At each conformal boundary psi=0 and dpsi has nonzero timelike
norm -H^2 in the extended flat metric, so these are regular spacelike
conformal boundaries, not material walls. There is no X_max identification.

Actual comoving clock redshift is Z=a(t_o)/a(t_e). Expansion and contraction
have different signs; this control does not establish finite universal
slowing, the founding past-asymptotic target, or a unique preferred clock
population. Only the additional local prepared-clock coefficient in (S8)
has the all-frame sign. The family has a Minkowski limit on fixed compact
coordinate patches as H tends to zero; no general quiet-GR recovery theorem
is claimed.

## 4. Discovery, checks, limits, and return

NAR and the recurrent-line alternative were independently originated before
exposure to B. B's all-frame prepared-clock sign route was disclosed before
this supplement and is expressly credited as a premise source. The CNR
positive-concavity idea formed after that disclosure. Parent subsequently
disclosed its separate conformal Weyl-scaling C2 argument; C2 is not used
here. We did not inspect B's working files. No new primary source replaces
any central premise grade. Initial CANDIDATE and its freeze are preserved.
The initial source log's stale access wording and the first fidelity
review's total-Ricci wording correction are handled in REVIEW_REPAIR.md,
including current reinspection and the limit on earlier access timestamps.

`check_optical_conformal.py` starts from the displayed metric entries and
computes Christoffels, Riemann and Ricci. Its 19 grouped exact checks include
the generic scalar Jacobi reduction, metric null/affine equations, nonzero
radial Ricci, time-dependent conformal identity, and the cosh curvature
blocks/coefficient. The generic conformal proof is analytic plus the cited
identity; the executable does not test arbitrary spacetime-dependent psi.
The constancy, all-frame argument, and completeness proofs are analytic.
Checks are same-author SymPy regression/algebra checks, not independent
review or numerical certification.

The initial capture `checks/optical_conformal.*` preserved one failed
automatic comparison: SymPy did not simplify a mixed sinh/exponential form
to zero. The exact formula sinh(x)=(exp(x)-exp(-x))/2 was then applied to that
residual, with no equation, domain or expected value change. Initial source
is retained as `checks/optical_conformal.initial.py`. The second capture
`checks/optical_conformal_normalized.*` passes all 19 groups and records the
zero normalized residual (1.24 seconds, 50,808 KiB RSS, 2 GiB virtual limit,
one BLAS thread, no wall/CPU killing timeout). This is a representation
repair, not evidence that a nonzero mathematical residual was accepted.

**Scoped return:** an actual radial clock/ruler equality conditionally
selects a stationary reciprocal spherical sector, while ordinary optical
reciprocity does not impose it. A separate all-frame local clock-sign trial,
when combined with a complete null-Ricci-zero conformal reference, rules out
nonconstant conformal factors; a causally complete physical countercontrol
shows why reference completeness cannot be silently replaced by physical
completeness. These are decision-ready conditional candidates for fresh
review. They do not adopt NAR, S, the conformal matching, a scale/profile,
or a full physical asymptotic history. No outstanding proof defect is known
to the author; final fresh review and review of the first bounded fidelity
repair remain pending at this freeze.
