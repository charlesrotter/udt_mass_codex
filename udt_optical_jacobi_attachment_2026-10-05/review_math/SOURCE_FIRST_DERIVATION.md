# OJM1 source-first mathematical derivation

This is a fresh separate reviewer context (`/root/ojm_math`), same inherited
model family as parent, runtime version not independently attested. No parent
OJM1 candidate or implementation was read. Parent supplied the question, source
paths and startup evidence. Independently checked branch `grok` and HEAD
`278a8f126dc7a1283c0c2dcdb074c183fce7cdde`; no tracked dirt at intake. Parent
full startup, synchronization and 406-row verifier are attributed, not rerun
here. Protected payloads were not opened, hashed or modified.

Sources read: AGENTS; selected CLAUDE sections; no-shortcuts,
completeness-map and verifier-before-record; OJM1 WORK_ORDER; central R8CGE,
R8CPR, R8OAA and R13; original CPR1 and OAA1 candidates and clarifications;
G348 EXACT_DERIVATION and its exact registry scope. An overbroad locator also
returned several unrelated registry hits; none is a dependency of this review.

## Derivation

Use exactly supplied f=1-2m/r-H²r², m,H>0, a>3m, f(a)>0,
Omega²=m/a³-H²>0, escaping fixed finite-E receiver and strict outward ray.
Coordinates are (u,r,theta,phi), equatorial theta=pi/2. Its energy-one tangent
is k=(b²/[r²(1+s)],s,0,b/r²), s=sqrt(1-fb²/r²). These are conditional,
free-and-explored histories, not selected native physics.

Put P(r)=integral_a^r b/(rho² s)d rho, I(r)=integral_a^r
1/(rho²s³)d rho. The two normalized quotient axes can be represented by

    e_perp=(1/r)partial_theta,
    e_parallel=(b partial_u+partial_phi)/(r s).

They have unit norm, are orthogonal to k and each other, and are parallel
in the quotient. For e_perp this follows directly from the Christoffels;
metric compatibility and orthogonality then establish the second axis.
They need not be orthogonal to either physical endpoint observer. G348's
isometric lift is e_i^phys=e_i+g(e_i,u)/omega k. It puts each axis into that
observer's physical rest-screen without changing any quotient inner product.

A variation of b, at a fixed source point and fixed endpoint radius r, gives
J=I(b partial_u+partial_phi), since U_b=b I and P_b=I. Its source initial
quotient slope is 1/(a s_a), giving the in-plane Jacobi width

    B_parallel=a r s_a s(r) I(r)>0.                    (M1)

Rotating the ray's orbital plane about its source radial line gives transverse
displacement r sin P. Its source initial quotient slope is b/a, giving

    B_perp=a r sin P(r)/b,                            (M2)

with continuous value r-a at b=0. These are the two position-from-unit-affine-
slope widths for a source vertex. Finite-r endpoint matching adds a multiple
of k to the Jacobi field and hence does not affect their quotient values.

The radial equation gives r''=b²/r³-3mb²/r⁴. Thus
(r sin P)''=-3mb²/r⁵(r sin P). Direct differentiation of M1 gives the opposite
sign, yielding tide diag(-3mb²/r⁵,+3mb²/r⁵) in (parallel,perp) order and
B''+T B=0, with B(e)=0, B'(e)=I. The H² Ricci contribution vanishes on k;
the Weyl tide remains. For b=0 the tide vanishes identically and B=(r-a)I.

Reciprocity supplies the reverse position block -B^T. Up to the declared
orientation convention, the complete sky-angle to source-screen map is

    J_o_to_e=-A diag(B_parallel,B_perp),              (M3)
    A=omega_o=1/(E+v)+v b²/[R²(1+s_R)].

Using past-ray instead of future-affine initial momentum changes the common
sign. The physical source-screen to sky map is its inverse only at rank two.
There is no source-frequency factor in M3. Source observer replacement is a
quotient isometry; the observing endpoint supplies the angular normalization.
Geometric angular area distance is

    D_A=A sqrt(abs(B_parallel B_perp)).              (M4)

Forward directional area equals omega_e² abs(det B), reverse directional
area A² abs(det B), and their division-free reciprocity is forward=Z² reverse.
Neither the determinant nor its square root specifies each directional ruler.

## Limits, poles and failures of broader identification

Write S=sqrt(1+H²b²). Smooth strict-source bounds justify uniformly near b_*
the limits I->I_inf, P->P_inf, s_R->S and A R->S/H. Thus

    D_A,*=(a/H) sqrt(abs(s_a S³ I_inf sin(P_inf)/b)). (M5)

At b=0 the continuous expression is1/H. For b!=0 this factor is not generally
one; affine and angular definitions are not interchangeable. For a ray before
its first conjugate point, the area width obeys Sachs concavity because the
trace tide is zero and shear contributes negatively. Nonzero m b² gives
nonzero shear and strict area-width suppression relative to affine interval.
This is an analytic observation, not a universal bound after conjugate points.

The in-plane width never vanishes for R>a. The perpendicular width vanishes
precisely when P(R)=n pi, n!=0 (P has sign b and increases in magnitude).
These are rank-one conjugate endpoints, not metric singularities. An outward
monotone ray is not automatically caustic-free: as a approaches3m from above
and the source direction approaches its strict tangential bound, the angular
integral can exceed pi. All proposed global no-caustic claims need a restriction.
If P_inf=n pi with b*!=0, M5 vanishes and the late angular asymptotics require
the next term; a universal finite positive angular endpoint is false.

For the principal actual-incidence preparation b*=0, CPR1 proves b(R)=O(1/R).
The widths divided by R and their integrals are smooth even functions of b,
uniformly near0, so comparison with b=0 changes the leading normalized widths
by O(b²). A(R,b) likewise has a uniform expansion. Consequently along the
actual, generally nonradial finite rays,

    D_A=1/H-(a/H+E/H²)/R+O(R^-2),
    Z(1/H-D_A)->(a+E/H)/sqrt(h).                    (M6)

Smooth inverse-radius tails justify differentiation and eventual monotone
approach from below. Near this limit |P|<pi, so both widths are positive.
This is an eventual-tail result, not a global distance ceiling or proof of no
earlier crossing. The source emission endpoint is finite; receiver proper time
diverges. M6 retains the affine leading pole without asserting affine=angular
on finite nonradial rays.

## Scope and omitted evidence

All maps are exact infinitesimal metric Jacobi maps on a supplied path.
Using a finite physical source patch needs its geometry and controlled
higher-order error; a linear map alone is not a finite-image or material-source
model. Source rest-screen assignment is declared above. No physical ruler,
flux/luminosity, matter model, empirical fit, native metric admission, population,
Hubble identification, X_max or canon follows. Matched metric/clock/ray data
in GR yield the same record. Old source tests were not replayed wholesale.
