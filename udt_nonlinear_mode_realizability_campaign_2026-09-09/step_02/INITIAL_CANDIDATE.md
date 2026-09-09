# NR2 initial candidate — exact realization of the balanced tangents

UNPROMOTED mathematical candidate; independent review PENDING. 2026-09-09.
Dependency: NR1 necessity at its reviewed scope and mixed-regularity caveat,
step_01/REVIEWED_RESULT.md and entire source-first/direct review. The extra
right-inverse exploration in that review is NOT a premise or proof input here.
G310/G312 equation remains owner-provisional. No scientific source is modified.

## Statement, including quantifiers

Fix a registered compact G324 split-lattice quotient, C1,Cperp>0 and T0>0.
For any of the eight-real-parameter G327 axial tensor first variations h, set
Q=v_c dot u_s-v_s dot u_c at T0 as in NR1. Then

    Q=0  iff  h is tangent (modulo legal periodic gauge) to an exact family
              solving Ric(g_epsilon)-(R(g_epsilon)/4)g_epsilon=0
              near the entire supplied compact slice.                  (NR2)

For necessity use NR1, with a family C2 in a field topology sufficient for the
mixed derivatives and compact constraint pairing. For sufficiency construct a
family analytic jointly in epsilon and spacetime coordinates. For EACH fixed
h there exist epsilon0,delta>0 and a common slab |T-T0|<delta, |epsilon|<epsilon0.
These bounds may depend on h and the supplied background. No uniform bound over
all amplitudes, prescribed long time interval, endpoints or other mode sectors.

The positive implication is conditional on the standard analytic
Cauchy--Kovalevskaya (CK) method under the explicit interface below, not on a new
physical premise. It supplies actual analytic developments, not only formal
Taylor coefficients. Analytic competitors suffice to establish existence in the
larger smooth class; no smooth well-posedness/stability theorem is asserted.

## 1. Parametrize metric data, not a carrier or action

At T0 put a=C1 T0^(-1/3), b=Cperp T0^(2/3), s0=-2/(3T0).
Write H=[[f,w],[w,-f]] and Hdot=[[p,r],[r,-p]], where f,w,p,r are the
prescribed real first-harmonic functions of X. A prime below means ∂X.

Use the positive determinant-one matrix chart

    M(u,v) = [[exp(2u), exp(2u)v],
              [exp(2u)v, exp(-2u)+exp(2u)v²]].

These two coordinates parametrize a transverse spatial metric; they are not an
additional field, a metric-selected phase/current recipe, physical polarization
identification or a restriction used in NR1 necessity. Let

    E_u=M^-1 ∂u M, E_v=M^-1 ∂v M,
    G_ab=(1/2)tr(E_a E_b)=diag(4,exp(4u)),
    V=(p_u/4)E_u + p_v exp(-4u) E_v.

E_a and V have zero trace and are M-self-adjoint. The variables p_u,p_v merely
parametrize the trace-free transverse extrinsic curvature; no Hamiltonian action
or physical momentum assignment is used. Direct matrix algebra yields

    tr((M^-1 M')V)=2(p_u u'+p_v v'),
    tr(V²)=p_u²/2+2p_v² exp(-4u).                      (1)

Choose a witnessing family, retaining all prescribed FIRST-order data,

    u=epsilon f, v=2epsilon w,
    p_u=-2epsilon p, p_v=-epsilon r.                  (2)

This chart and completion are chosen methods to demonstrate existence, not a
claim that the metric physically selects this nonlinear completion.

## 2. Exact periodic mean correction

Q=0 is exactly the zero-period condition

    ∫_0^LX (p f'+r w')dX = (k LX/2) Q = 0.

Hence choose the global periodic analytic primitive Psi with

    Psi'=p f'+r w', Psi(0)=0.

All f,w,p,r are trigonometric polynomials, so zero mean gives an analytic periodic
primitive; it is not obtained by tuning or discarding any phase or time branch.
Set

    s_epsilon=s0+epsilon² Psi+c(epsilon),            (3)

where c is any real analytic scalar function O(epsilon²) near zero. Its value is
a supplied homogeneous correction, not a selected background law. Compactness
and s0!=0 give s_epsilon!=0 for all X at sufficiently small |epsilon|.

Let Lambda(epsilon) be any real analytic function with Lambda(0)=Lambda'(0)=0.
This includes Lambda identically zero. Lambda remains one spacetime-constant
number in each family member, not a function of X or T. The first derivative
must vanish for the specified G327 tangent since delta R=0; higher derivatives
have NOT been fixed by the necessity argument or by a physical premise.

## 3. Full exact initial constraints

Define the positive spatial metric and symmetric second fundamental form by

    gamma = a² dX² + b² M_AB dz^A dz^B,
    K^i_j = diag(kappa, s I_2+V),
    K_ij = gamma_ik K^k_j,

using K=-(1/2)∂T gamma. No positivity condition is placed on K. The metric has
det gamma=a²b^4>0, and all entries are globally periodic analytic fields.
Full Levi-Civita reconstruction, not discarding any constraint component, gives

    R3 = -tr((M^-1 M')²)/(4a²)
       =-[4(u')²+exp(4u)(v')²]/(2a²),
    M_X = D_j K^j_X -∂X trK = -2s'-(p_u u'+p_v v'),
    M_y=M_z=0,
    H = R3+(trK)²-tr(K²) = R3+4s kappa+2s²-tr(V²).  (4)

With (2)--(3), M_X vanishes POINTWISE, not merely after averaging. Choose

    kappa=[2Lambda-R3-2s²+tr(V²)]/(4s).              (5)

Its denominator is nonzero for small epsilon. Equation (5) gives H=2Lambda
pointwise. Thus ALL full constraints of the admitted equation hold on the entire
compact slice for every small epsilon. Higher harmonics, the axial K correction
and the mean correction have not been suppressed by a nonlinear tensor truncation.
The family is analytic in epsilon and X; no finite residual approximation is used.

## 4. Match the prescribed complete first-order Cauchy data

At epsilon=0, M=I, V=0, s=s0, Lambda=0 and kappa=-s0/2=1/(3T0).
Thus gamma0 and K0 exactly match G324 in the negative-K convention.
Since E_u(0)=2diag(1,-1), E_v(0)=[[0,1],[1,0]], equations (2) imply

    (∂epsilon M)|0=2H, (∂epsilon V)|0=-Hdot,
    (∂epsilon s)|0=0, (∂epsilon kappa)|0=0.

Consequently

    delta gamma_AB=2b²H,
    delta K_AB=-b²[Hdot+4H/(3T0)],
    delta gamma_XX=delta K_XX=delta gamma_XA=delta K_XA=0. (6)

These are exactly the G327 initial field AND its normal derivative, not only a
spatial metric match. c and Lambda begin at second order and leave (6) unchanged.
The zero-amplitude and two-polarization cancellation cases are included. All eight
coefficients remain in the question; only the one quadratic condition restricts
their ability to be exact-family tangents in this specified sector.

## 5. Actual common local developments — explicit method interface

Use Gaussian coordinates g=-dT²+gamma_ij(T,x)dx^i dx^j on the given slice and solve
the six spatial equations Ric_ij=Lambda gamma_ij. The geometric identities give

    ∂T gamma_ij=-2K_ij,
    ∂T K_ij=R3_ij+(trK)K_ij-2K_ik K^k_j-Lambda gamma_ij.  (7)

This is equivalently a system solved for all six ∂T²gamma_ij with analytic
coefficients on positive-definite gamma; spatial second derivatives remain in
R3_ij. The coefficient of the highest pure normal derivative is invertible.
Apply analytic CK to this reduced system, NOT to the degenerate unreduced
trace-free equation. A first-order CK presentation uses gamma, ∂Tgamma and
spatial first derivatives; all spatial directions/components are retained.

Treat epsilon as an additional mathematical independent variable, with zero
epsilon-derivative coefficient in the evolution operator. Analytic initial data
and analytic Lambda(epsilon) give joint analytic local solutions by the same
noncharacteristic theorem. This is parameter dependence, not a fifth dimension
of physical spacetime. The initial surface T=T0 remains noncharacteristic.

Finite covering of the compact slice (and a smaller compact epsilon interval),
local uniqueness and the fixed translation transition maps yield one common
positive time neighborhood. Uniqueness identifies overlapping solutions and
their periodic translates. Positivity, Lorentzian signature and the supplied
future orientation persist on a smaller common slab by continuity. This is a
local construction near the whole compact slice, not global-in-time existence.

### Recover all original Ricci equations, not just spatial evolution

Put E_ab=Ric_ab-Lambda g_ab; spatial evolution gives E_ij=0. Let C=E_00 and
D_i=E_0i. Since Lambda is spacetime constant, contracted Bianchi applies to
F_ab=E_ab-(tr_g E)g_ab/2. In Gaussian coordinates with K=-gamma_dot/2 and τ=trK,
its remaining equations are the homogeneous first-order system

    ∂T C = 2 div_gamma(D^sharp)+2τ C,
    ∂T D_i = (1/2)∂i C+τ D_i.                       (8)

In the first line div_gamma(D^sharp) is the spatial covariant divergence of
the raised one-form D, not its squared norm. No nonlinear source appears in (8).
The exact initial constraints imply C=D_i=0 on the initial slice. Analytic
uniqueness for (8) gives zero throughout the local slab. Thus E_ab=0 in every
component and the original S(g)=0 holds. Formula (8) is a Bianchi calculation;
code checks cannot substitute for this propagation/existence argument.

### Match the spacetime tangent, not just initial data

The family at epsilon=0 has the same analytic Gaussian Cauchy data as g0, so CK
uniqueness identifies it with the G324 background. Differentiate (7): Lambda'(0)=0
and (6) provide the exact G327 linearized Cauchy data. The known G327 perturbation
solves those linearized spatial equations; analytic uniqueness of the linearized
system therefore identifies the full spacetime derivative with that perturbation
on the common slab. Gaussian lapse/shift are fixed as coordinate method only.
This closes the passage from exact constraints to exact-family tangent.

## Method sources and limitations

METHOD_REFERENCES.md records the actually opened primary/academic sources:
Choquet-Bruhat arXiv:1410.3490, sections2--3 (analytic reduction, Gaussian slicing,
constraints/Bianchi), and the academic CK theorem/system statement in Chapter2,
Theorem4.1 and (4.1), https://www2.math.upenn.edu/~qze/notes/pde2.pdf.
The candidate application, compact gluing and parameter argument above are our
mathematical inferences, not quoted source theorems about UDT. The full general CK
theorem is a standard mathematical method, not re-proved or machine-certified here.

No claim of typicality, physical momentum/count/energy, generic metric behavior,
smooth Sobolev stability, nonlinear time persistence or complete solution-space
classification. The compact quotient causes the NR1 global obstruction; neither
this supplied topology nor this completion is chosen by UDT. Conditional analytic
existence does not identify a carrier, action, coupling or physical object.

The exact iff statement is ONLY about realizable tangents in the declared G327
sector. It does not classify all nearby exact metrics or select their legitimate
initial data. c(epsilon), Lambda(epsilon) and other possible completions remain
free; (2)--(5) give witnesses, not uniqueness. Accepted G327 linear science stands.

## Discovery and checks

After NR1 review, the construction used a positive metric-coordinate chart and
its dual extrinsic-curvature coordinates to make the periodicity condition exact.
The full spatial coordinate check is separate from the chosen closed constraint
formulas. It tests original Ricci/momentum/Hamiltonian, tangent matching, free
second-order scalar/mean data, and an actual balanced two-polarization case.
Finite/structural checks are not a proof of the CK theorem, all gauges, or infinite
time existence. Original check source and outputs are preserved before review;
three specific arithmetic/normalization defects will be injected and rerun.
Fresh source-first and direct adversarial review must assess the full analytic
argument and method hypotheses, not just these passing checks. No banking.
