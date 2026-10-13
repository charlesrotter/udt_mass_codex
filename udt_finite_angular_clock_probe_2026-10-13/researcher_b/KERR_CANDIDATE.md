# FAC1 Kerr control — magnetic dominance at a regular vacuum event

Status: frozen contributor candidate; the clock prediction is conditional on
the proposed general vacuum quartic theorem and its fresh review. The exact
Kerr metric checks below establish pointwise curvature facts independently of
the proposed clock coefficient. No UDT admission or physical premise is adopted.
This continuation preserves the earlier CANDIDATE.md and MANIFEST.json unchanged.

## Source and scope

The coordinator proposed using a Kerr principal-frame event after A's plane-wave
result suggested a magnetic contribution. B inspected primary sources and then
differentiated the original metric independently. This is parent-exposed lead
development, not independent origin of the Kerr idea or of A's clock theorem.

[Wylleman, Costa and Natario, arXiv:2007.15384v2](https://arxiv.org/html/2007.15384v2),
section6.2, equations147 and155--161, supplies the Kerr-Newman coframe and
principal Carter observer. Its zero-charge specialization is the standard
vacuum Kerr solution: the supplied Einstein-Maxwell solution has vanishing
electromagnetic field when Q=0, so its GR equation reduces to Ric=0 throughout
each regular Kerr neighborhood. This is a property of the supplied GR control,
not UDT dynamics. The exact point checks below do not themselves prove regional
Ricci-flatness.

[Mashhoon, arXiv:2007.12023v3](https://arxiv.org/pdf/2007.12023v3), Appendix C,
equations C3--C8, gives the canonical Petrov-frame electric and magnetic Weyl
matrices. The [published correction](https://www.mdpi.com/2218-1997/7/2/39)
concerns earlier tidal-motion equations; the inspected revised Appendix C retains
the component formulas used here. No accelerated-observer tidal-motion equation
from this source enters the FAC1 free-clock preparation.

The precise inspection record and computation freeze are KERR_LEAD_SCOPE.md.

## Geometry and initial observer

Let y=cos(theta), Sigma=r^2+a^2 y^2 and Delta=r^2-2Mr+a^2. The nonzero
Boyer-Lindquist metric components in(t,r,y,phi) are

    gtt=-(1-2Mr/Sigma),  gtphi=-2Mar(1-y^2)/Sigma,
    grr=Sigma/Delta,     gyy=Sigma/(1-y^2),
    gphiphi=(r^2+a^2+2Ma^2 r(1-y^2)/Sigma)(1-y^2).

Use the orthonormal Carter coframe

    theta0=sqrt(Delta/Sigma)[dt-a(1-y^2)dphi],
    theta1=sqrt(Sigma/Delta)dr,
    theta2=sqrt(Sigma/(1-y^2))dy,
    theta3=sqrt((1-y^2)/Sigma)[(r^2+a^2)dphi-a dt].

Its future time vector is

    U=[(r^2+a^2)partial_t+a partial_phi]/sqrt(Sigma Delta).

**This specifies only A's initial tangent.** For FAC1, A subsequently follows
the geodesic through that event with tangent U. It is not held on a circular
Carter orbit. B clocks are then prepared by the stipulated spacelike exponential
map and parallel transport and freely released. The spherical quartic theorem,
if proved, applies to that preparation and its initial E(U),B(U); it must not
inherit the acceleration of an observer held on the Carter congruence.

Write E0+iH0=M/(r+i a y)^3. The source principal-frame matrices are diagonal
with proportions(-2,1,1). Thus

    E0=Mr(r^2-3a^2 y^2)/Sigma^3,
    H0=-May(3r^2-a^2 y^2)/Sigma^3,
    |E|^2=6E0^2, |B|^2=6H0^2.

Our dy coframe reverses a spatial orientation relative to the usual dtheta
frame. The independently calculated magnetic matrix consequently has the
opposite overall sign from this H0 convention. Its squared norm agrees.
The Schwarzschild control checks the electric curvature sign under
R(X,Y)=[nabla_X,nabla_Y]-nabla_[X,Y].

## A nonextremal exact control

Take M=1, a=sqrt(15)/4, r=3/2 and y=2/sqrt(5). Then

    r_plus=5/4 < r, Sigma=3, Delta=3/16 >0,
    E=0, B=diag(-2sqrt(3)/9,sqrt(3)/9,sqrt(3)/9),
    |B|^2=2/9, C_abcd C^abcd=-16/9.

The metric is smooth and Lorentzian at this point: Sigma,Delta and1-y^2 are
strictly positive and the displayed orthonormal coframe is invertible. It lies
on the stationary-limit surface gtt=0, which is not a metric degeneracy or
horizon. The Carter U is still unit timelike. This is a pointwise purely
magnetic measurement, not a claim of a purely magnetic vacuum open region.

The same nonextremal geometry at r=31/20, with y unchanged, removes even the
stationary-limit coincidence:

    Delta=6/25, Sigma=1261/400, gtt=-21/1261 <0, r>r_plus,
    |E|^2=1373138304000000/4020596770139341561,
    |B|^2=768601612800000000/4020596770139341561.

Hence4|E|^2-3|B|^2<0 strictly outside both the horizon and ergosphere.
Continuity gives a neighborhood with the same strict magnetic-dominance sign.
The pointwise E=0 claim does not extend to that neighborhood.

For the parent's original extremal point M=a=1,r=sqrt(3/2),y=1/sqrt(2),
the check independently returns |E|^2=0 and |B|^2=3/4. Nonextremality therefore
does not remove the algebraic phenomenon.

## Conditional clock consequence — not supplied by the Kerr calculation

The proposed general vacuum result from A has the form

    M_±(U,L)=[4|E(U)|^2-3|B(U)|^2] L^4/360+O(L^5).

**Its proof and review are separate load-bearing requirements.** Fitting Kasner
and one plane wave cannot prove it, and none of the Kerr curvature assertions
proves it. If that theorem is established for the FAC1 free-clock preparation
on a smooth Ricci-flat neighborhood, the nonextremal pure-magnetic point gives

    M_+(U,L)=M_-(U,L)=-L^4/540+O(L^5),

where equality here means the displayed leading coefficient, not equality of
the two complete finite functions. Both means would then be negative for every
sufficiently small positive L in this fixed laboratory. The extremal point
would instead give coefficient-1/160. The off-stationary-limit point likewise
has a strictly negative proposed coefficient.

Until the general theorem passes review, these are conditional predictions.
No Kerr clock trajectories, ray incidences or numerical sphere means were
integrated by this contributor.

## Meaning and recovery limits

A verified negative coefficient would refute automatic AMS for all Ricci-flat
metrics/preparations. It would not refute UDT, whose physical admission of this
control and AMS attribution are open. The example is a strong-field Kerr
laboratory; no claim is made that the observationally tested GR recovery mandate
requires precisely this region, observer or freely prepared apparatus.

Smooth matched recovery to a fixed such laboratory would obstruct a universal
nonnegative mean at a common finite L, by continuity. Shrinking positive-query
domains, finite-tolerance recovery and a distant-onset additional effect do not
inherit that contradiction. Likewise the mere existence of a supplied GR
control does not assert a physically admitted UDT recovery family.

Under an overall Kerr length rescaling, curvature squared and the proposed
quartic coefficient scale as inverse length^4. Magnetic dominance is unchanged.
Thus an absolute small-curvature criterion alone would not reverse the sign,
but this scaling does not turn the dimensionless strong-field configuration
into a solar-system experiment or determine a physical mass/scale.

## Exact check record

check_kerr_curvature.py forms original metric first and second derivatives,
the lowered Christoffel symbols, and the full curvature bivector matrix at four
points. An independently constructed Carter coframe transforms that matrix.
The checks cover all16 Ricci components at each point, orthonormality, electric
and magnetic symmetry/traces, source-formula norms, the Schwarzschild electric
sign, Kretschmann contraction, horizon placement, and strict magnetic dominance
at the outside-ergosphere point. No source E/B formula is substituted for the
metric curvature calculation.

kerr_curvature.stdout/.stderr/.json preserve the exact invocation and result.
All four cases pass; SymPy1.13.1, duration1.678seconds captured wall time,
max RSS56764KiB,2GiB virtual-memory cap,one thread,no killing timeout. This is
exact finite symbolic arithmetic plus source-qualified geometry, not a
generic numerical certificate, regional symbolic Ricci proof, independent
different-model review or native scientific promotion. No failure or repair
preceded this successful execution.
