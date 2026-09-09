# NT2 candidate — a restricted variation and its actual vacuum realization

UNPROMOTED. Conditional on the admitted arena and reviewed NT1, not a new UDT
premise, carrier, physical wave interpretation or general realization theorem.
Candidate construction precedes exposure to the separate reviewer's source-first
findings. Question and exclusions are frozen in QUESTION.md and WORK_ORDER.md.

## Precise domain and claim

Let g be a smooth four-dimensional Lorentz metric, Ric(g)=Lambda g, with the
G358 slot convention Q_abcd=g(R(e_a,e_b)e_c,e_d). Lambda is constant. Put
W=Q-(Lambda/3)(eta_bc eta_ad-eta_ac eta_bd). At an event p with W(p)=0,
suppose the first covariant curvature variation has the restricted factorization

    (nabla W)_p = nu tensor P,   nu != 0, P != 0,

where nu is a REAL covector and P a real algebraic Weyl tensor. This is a
conditional class of supplied local data, not a claim that all variations
factorize, a physical phase law or a wave-front ansatz for an entire region.
The scale of nu versus P is redundant: c nu tensor (P/c) is the same jet.

NT2a: the first Bianchi compatibility conditions in NT1 hold for this jet if
and only if nu is null and, in an orthonormal frame with nu=(1,0,0,-1),

    C = [[a,b,0],[b,-a,0],[0,0,0]],
    B = [[b,-a,0],[-a,-b,0],[0,0,0]],  (a,b) != (0,0).

Here P_i00j=C_ij and P_i0jk=epsilon_jkl B_li; the remaining slots are fixed
by Weyl symmetries and P_ijkl=epsilon_ijm epsilon_kln C_mn. An overall
normalization/sign of nu is absorbed in P; transverse frame rotations merely
change amplitude coordinates. The necessity holds in every Lambda sector.

NT2b: every such canonical null jet is attained in an ACTUAL smooth local
Ricci-flat metric (Lambda=0), with explicit induced spacelike data satisfying
the full constraints on a nonempty neighborhood. This is not an existence claim
for nonzero Lambda, all arbitrary compatible jets, or arbitrary initial data.

## Analytic symbol argument, not an example count

Use the reviewed NT1 relations div C=div B=0, D0 C+curl B=0 and
D0 B-curl C=0, where ALL spacetime connection slots are included in D.
Factorization replaces every D_mu by multiplication by nu_mu on the amplitude
tensor. Lorentz covariance reduces a nonzero real covector to timelike,
spacelike or null normal form; multiplication by a nonzero scalar is irrelevant.
We may choose orientation/time orientation consistently with the displayed frame.

For timelike nu=(1,0,0,0), the two evolution equations set C=B=0. For spacelike
nu=(0,0,0,1), the two divergence equations set the third row/column of C and B
to zero. Each is then a two-by-two trace-free symmetric block. On such a block
U=[[r,s],[s,-r]], the spatial curl with derivative in direction3 is
T(U)=[[-s,r],[r,s]]. T is invertible (T squared=-identity). The evolution
equations set both blocks to zero. Neither case permits nonzero P.

For null nu=(1,0,0,-1), the same divergence restrictions apply. The evolution
equations become C-T(B)=0 and B+T(C)=0. Thus C has arbitrary two amplitudes
a,b and B=-T(C) has the stated form; the two equations agree. This proves both
necessity and sufficiency for the FIRST-DERIVATIVE ALGEBRAIC constraint only.
The full symbol ranks 10,10,8 provide a redundant exact check, not the proof of
metric realization. This two-amplitude description is NOT a physical mode count.

At W(p)=0, frame-connection corrections multiply W and vanish; this does not
assume connection coefficients vanish in a neighborhood. The constant-curvature
part is parallel. Hence this restriction applies to the registered first tidal
variation without an unmeasured connection canceling it at this event. Away
from W=0 the full covariant comparison remains necessary.

## Actual development with arbitrary smooth profiles

For arbitrary smooth real functions A(u), F(u), define

    g=-2 du dv+dx^2+dy^2+H du^2,
    H=A(u)(x^2-y^2)+2F(u)xy.

The u,v metric block has determinant -1, so g is Lorentzian everywhere on its
coordinate domain. Direct Levi-Civita curvature calculation gives
Q_i u u j=-(1/2)partial_i partial_j H for i,j=x,y, with all other independent
components zero. Ric_uu=-(1/2)(H_xx+H_yy)=0 and all other Ricci components
vanish throughout the neighborhood, for arbitrary profile functions and their
u derivatives. This is an exact smooth metric, not a formal jet followed by
an assumed realization theorem. It uses no earlier curvature-product recipe.

Let L=partial_u+(H/2)partial_v, V=partial_v. Choose the supplied frame
e0=L+V/2, e3=-L+V/2, e1=partial_x, e2=partial_y. It is orthonormal and
du(e_mu)=(1,0,0,-1). Set A(0)=F(0)=0, A'(0)=-a, F'(0)=-b.
At p=(0,0,0,0), W=Q=0. Direct differentiation of all slots gives precisely
(nabla W)_p=du tensor P with the displayed amplitudes; connection/frame
derivative terms multiply the zero curvature at p. Higher derivatives of the
two profiles are unrestricted by this jet prescription. Nonzero (a,b) gives
nonzero P; zero amplitudes are a valid zero-jet survivor but excluded from NT2a's
nonzero factorization. Any normalized null covector/frame case can be represented
by an orthonormal change of frame at p and a rescaling of P. This is pointwise
covariance, not a claim that every realization must have this metric form.

## Genuine constraint-compatible initial data

Take the local slice Sigma: v+2u=0, with coordinates (u,x,y). On H+4>0 put
S=H+4. Its induced metric, future normal (relative to e0) and extrinsic curvature
in convention K=-one-half L_n gamma are

    gamma=diag(S,1,1),  n=(partial_u+(H+2)partial_v)/sqrt(S),
    K=(1/(2sqrt(S)))*[[H_u,H_x,H_y],[H_x,0,0],[H_y,0,0]].

The normal has norm -1 and is orthogonal to all slice tangents. K is computed
from the projected derivative of n, so its sign is not inferred from the
squared Hamiltonian constraint. On this slice,

    R(gamma)=-(H_xx+H_yy)/S+(H_x^2+H_y^2)/(2S^2),
    (tr K)^2-|K|^2=-(H_x^2+H_y^2)/(2S^2).

Consequently R+(tr K)^2-|K|^2=0 throughout the slice domain. The momentum
constraint D^j K_ij-D_i tr K=0 follows either by direct differentiation or
contracted Codazzi from the already verified full Ricci-flat metric; the checker
also recomputes it intrinsically. At p, S=4, so a nonempty spacelike patch exists
by continuity. No closed spatial manifold, box boundary or global extension is
asserted. H_u is retained: the data are not silently time-symmetric or restricted
to constant profiles. The actual displayed metric is a development of these
data; no unverified PDE existence assertion is needed to connect them.

## What this adds and leaves open

The admitted vacuum geometry imposes a new restriction on this declared
rank-one first-variation class: a nonzero variation has a null derivative
covector and paired transverse Weyl amplitudes. This derives a constraint, not
a law selecting the class, profile functions, initial geometry or a physical
carrier. The exact local metrics show the permitted class is nonempty and
realizable beyond isolated numerical examples, while leaving two arbitrary
smooth profile functions beyond their specified first jet. The assertion is
shared Einstein-vacuum mathematics conditional on the current UDT arena.

There is no claim of physical propagation/energy/content, a signal speed inferred
from these amplitudes, detector transfer, G351/G352 identification, generic
stability, completeness of initial data, or sufficiency of NT1 for general
neighboring records. These remain outside scope. No new premise is adopted.

## Checks and exposure

check_symbol.py reuses the REVIEWED NT1 full exact matrix and checks the three
symbol ranks and the exact null kernel. This is conditional reuse, not an
independent second derivation. check_development.py reuses geometry() only from
the prior general tensor utility; it never calls the old quadratic recipe. It
checks all256 curvature slots, all1024 first-jet slots, normalization and actual
full-neighborhood Ricci and intrinsic constraints with symbolic free profiles.
These are symbolic checks supporting the analytic argument, not formal proof
assistant certification. DISCOVERY_HISTORY.md records pre-freeze coding failures.
Fresh source-first separate-context review and any bounded repair must be read
alongside this candidate before using it downstream; this initial document is
preserved unchanged after its freeze.
