# FAC1 A — two exact finite-clock sphere controls

Exploratory author candidate, not reviewed acceptance. WORK_ORDER owns scope.
No UDT premise, metric, vacuum sector or physical scale is selected. The first
Kasner derivation was constructed before seeing B's independent calculation;
the plane-wave follow-up followed disclosed exchange through the parent.

## 1. Experiment and actual reverse emission

At (o,U) prepare B0=exp_o(L n) for each unit spatial n and parallel-transport U
along that spacelike geodesic. Release A and B geodesically. Their histories
remain fixed while differentiating neighboring emissions. The first forward
emission occurs at A0; the independent first reverse emission occurs at B0.
Both arrivals are future and on the local regular null branch. p_minus is not
an inverse ratio or a later echo. Both averages use dOmega_n at the original
preparation frame, including for the reverse records whose emitters are spread
over that preparation sphere.

## 2. Original-coordinate Kasner construction

Use g=-dt^2+sum t^(2 r_i) dx_i^2, r=(-1/3,2/3,2/3), o at t=1,
U=partial_t. Spatial translations give conserved covectors. For the preparation,
write t=t(s), x_i'=n_i t^(-2r_i), and transported U components as
C_i(s)=t^(2r_i) U^i(s). The original equations are

    t'' = -sum r_i n_i^2 t^(-2r_i-1),
    C_i' = (r_i/t)(t' C_i-n_i U^t),
    (U^t)' = -sum r_i n_i t^(-2r_i-1) C_i.

Initial data are t=1,t'=0,x=0,C_i=0,U^t=1. Set
R1=sum r_i n_i^2, R2=sum r_i^2 n_i^2 and
S=sum r_i(2r_i+1)n_i^2. The required preparation coefficients are

    T=1-R1 L^2/2-R1 S L^4/24+O(L^6),
    X_i/n_i=L+r_i R1 L^3/3+O(L^5),
    C_i/n_i=-r_i L-r_i[R1(1-2r_i)+R2]L^3/6+O(L^5).

Expressions divided by n_i denote their polynomial extensions; the actual
equations do not divide by a vanishing direction component. After release the
C_i are constant and

    V(t)=dt/dtau_B=sqrt(1+sum C_i^2 t^(-2r_i)),
    dx_B^i/dt=C_i t^(-2r_i)/V(t).

For a null ray with conserved covector k_i put
W(t)=sqrt(sum k_i^2 t^(-2r_i)). Its original equations give
dx_ray^i/dt=k_i t^(-2r_i)/W(t). The forward incidence at t=b satisfies

    X_i+integral_T^b C_i t^(-2r_i)/V dt
        =integral_1^b k_i t^(-2r_i)/W dt.

Its actual proper-clock ratio is

    p_plus=W(1)/(W(b)V(b)-sum k_i C_i b^(-2r_i)).

For reverse emission at B0 use k_i=-n_i K_i and solve instead

    X_i=integral_T^a n_i K_i t^(-2r_i)/W dt,
    p_minus=[W(T)V(T)+sum n_i K_i C_i T^(-2r_i)]/W(a).

These are endpoint frequency contractions of the actual ray and clocks;
R6 establishes equality to the fixed-history arrival derivative. In particular
the reverse source is at T with its transported velocity, not at t=1 with an
invented comoving velocity. The later echo does not appear.

Axial symmetry permits z=n_1^2 and n_2^2+n_3^2=1-z. On a dense regular angular
chart set k_1=n_1,k_transverse=rho*n_transverse; solve the two independent spatial
incidences for arrival and rho. The physical continuation to axes is justified
in section 4, not by assuming that these coordinate quotient equations retain
rank on an axis. Formal original-equation construction gives

    log p_plus = (3z-1)L^2/9 - 2(3z-1)L^3/27
                 -(117z^2-204z+43)L^4/486 + O(L^5),
    log p_minus = (3z-1)L^2/9 - 2(3z-1)L^3/27
                  -(27z^2-114z+31)L^4/486 + O(L^5).

At z=1,0 the forward series reproduce FPC1's independently existing axis
coefficients. That is a regression, not an input to the construction. The new
reverse quartic coefficients are 28/243 and -31/486 at those axes. With the
actual uniform sphere moments <z>=1/3 and <z^2>=1/5,

    M_plus=M_minus=4 L^4/1215+O(L^5).

Each is strictly positive for sufficiently small positive L. This supplied
Ricci-flat geometry has ordinary anisotropic tides and individual blue directions.
FPC1's negative forward principal-axis mean -7L^4/243 therefore does not imply a
negative spherical mean. Uniform positivity in n is not asserted.

## 3. A magnetic-tide control from the original plane-wave metric

Choose g=-2du dv+dx^2+dy^2+(x^2-y^2)du^2. Rescale a=sqrt(2)u,b=sqrt(2)v,
so g=-da db+dx^2+dy^2+sum h_i x_i^2 da^2 with h=(1/2,-1/2).
The origin's U=partial_a+partial_b is unit future timelike. Let the third spatial
frame vector be partial_a-partial_b and write its preparation component as z.
The other components are n_x,n_y with n_x^2+n_y^2+z^2=1.

Define the entire functions C_h and S_h by C_h'=h S_h, S_h'=C_h,
C_h(0)=1,S_h(0)=0. For any affine geodesic a'=c the original equations give
x_i''=c^2 h_i x_i. The norm equation gives

    b(lambda)-b(0)
      =[sum x_i(lambda)x_i'(lambda)-sum x_i(0)x_i'(0)-epsilon*lambda]/c,

where epsilon is its constant norm and limits at c=0 are analytic. Along the
unit spacelike preparation,

    a0=zL,  X_i=n_i S_hi(zL)/z,
    b0=[sum n_i^2 S_hi(zL) C_hi(zL)-zL]/z^2,
    U^a=1,  U^i=n_i[C_hi(zL)-1]/z.

These expressions have analytic z=0 limits after using sum n_i^2=1-z^2.
Transport follows from dU^i/dL=h_i z X_i; the remaining component is fixed by
normalization and the original connection. The released timelike B, parametrized
by its own proper time tau, is exactly

    a_B=zL+tau,
    x_B^i=n_i[S_hi(zL+tau)-S_hi(tau)]/z,
    b_B=b0+tau+sum[x_B^i (dx_B^i/dtau)-X_i U^i].

A(s)=(s,s,0,0) is the central proper geodesic. On a local branch before any
conjugate denominator zero, integration of the original null equation between
one transverse-zero endpoint and the B endpoint gives

    F(s,tau)=(a_B-s)(b_B-s)
             -sum [(a_B-s)C_hi(a_B-s)/S_hi(a_B-s)](x_B^i)^2=0.

The ratio d C_h(d)/S_h(d) extends regularly at d=0. This incidence equation is
derived from x_i''=h_i x_i with a as parameter and
Delta b=sum[x_i dx_i/da]_endpoints; no UDT dynamics or external optical law is
inserted. The two measured ratios are

    p_plus=-F_s/F_tau at s=0, tau=the future root,
    p_minus=-F_tau/F_s at tau=0, s=the future root.

Set X=n_x^2 and z=n_z. The original-equation series yields

    log p_plus=(2X+z^2-1)L^2/4
      +[4X^2+4Xz^2-4X+2z^4+4z^3-3z^2-4z+1]L^4/96+O(L^6),
    log p_minus=(2X+z^2-1)L^2/4
      +[4X^2+4Xz^2-4X+2z^4-4z^3-3z^2+4z+1]L^4/96+O(L^6).

Odd z terms integrate to zero. The exact sphere moments give

    M_plus=M_minus=L^4/720+O(L^6).

The even-in-L analytic scaled incidence explains the stated O(L^6) remainder;
this is not an assumption that arbitrary curved clocks have no odd powers.
Original metric differentiation confirms Ric=0 and covariantly constant Riemann.
In the declared orthonormal frame,

    E=diag(-1/2,1/2,0), B_12=B_21=1/2,
    E_ij E^ij=B_ij B^ij=1/2.

Here E_ij=g(R(e_i,U)U,e_j), and B_ij=(1/2)epsilon_i^kl g(R(e_k,e_l)U,e_j).
The Kasner coefficient equals E^2/90 in its chosen frame, but the plane-wave
coefficient is 1/720 rather than E^2/90=1/180. Thus this second supplied control
refutes the electric-only conjecture C1 recorded before its calculation.

The two controls alone do not establish a universal E/B formula. If a universal
linear combination a E^2+b B^2 were separately justified, they would fix it to
(4E^2-3B^2)/360. That conditional fit is a lead, not a classification or proof
that derivative terms are absent. No sign assertion for arbitrary vacuum Weyl
data, arbitrary frames or finite distances is made.

## 4. Angular uniformity and the actual small-distance claim

Both metrics are analytic near the fixed preparation event; choose a compact
regular coordinate neighborhood there. The preparation exponential and parallel
transport depend analytically on (L,n), and the released clocks have analytic
dependence on their initial data. Rescale flight parameter by L. At L=0 the
original endpoint shooting map is the ordinary flat one: a flight length r
and unit direction v yield displacement r v. At r=1,v=n its derivative is

    (delta r,delta v) -> delta r*n+delta v, delta v perpendicular to n,

an isomorphism. For the reverse experiment the limiting direction is -n and
the same statement holds. In local sky charts the analytic implicit-function
theorem therefore supplies the unique short future incidence, together with
its emission derivative. A finite cover of compact S^2 and a reduced common
positive L interval give uniformly bounded Taylor remainders. Timelike/null
regularity and positive arrival derivatives persist by continuity.

This full shooting construction supplies continuous analytic physical records
on the axes and at the coordinate-chart boundaries. Directional polynomial
identities proved on a dense chart consequently extend there. Uniform remainders
may be integrated against the fixed finite sphere measure, yielding the displayed
means and sufficiently-small-L signs. No explicit certified numerical radius or
uniformity over unbounded laboratory boosts follows.

## 5. Learning, evidence and limits

The immediate suspected negative Kasner sphere control is absent: ordinary
Ricci-flat Kasner gives positive first means. A second Ricci-flat control also
gives positive means, with a genuinely different magnetic contribution. These
facts prevent identifying positive angular means with a newly isolated UDT
effect. They neither prove positivity automatic for all GR vacua nor eliminate
the possibility of a nonautomatic conditional clock inequality.

AMS remains an UNADOPTED physical interpretation. Logarithmic clock depth and
uniform preparation angles motivate this statistic but do not establish its
positional attribution or universal applicability. The work does not restrict
native UDT geometry. A negative GR comparison, if later found, would exclude
only the explicitly strengthened positivity/recovery conjunction, retaining the
work order's shrinking-domain, distant-onset and finite-tolerance qualifications.

Source scripts and exact JSON are formal author computations, not independent
proofs. checks/formal_01, checks/plane_wave_01 and checks/plane_wave_geometry_01
preserve commands, stdout/stderr, source hashes, versions and resource receipts.
The source-level equations and uniformity argument above carry the intended
analytic claim, pending fresh review. B's original-ODE comparison is a distinct
implementation whose exact exposure and scope belong to B's source record.
