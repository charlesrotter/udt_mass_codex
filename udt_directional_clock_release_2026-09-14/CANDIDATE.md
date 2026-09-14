# DCR1 candidate — coupled directional clock and angular jets

UNPROMOTED mathematical candidate; R1 scope clarification applied. Final verdict and exact reviewed versions are recorded in review/. All statements below
refer to WORK_ORDER's supplied static analytic-even class, not native physical
admission. DDR/G301 is an explicitly conditional diagnostic at ONE center.

## 1. Complete second jet of the declared expanded class

Use the inherited auxiliary Cartesian marking, r=|x|, n=x/r, P=I-nn^T,
C(x)v=x cross v, and x0=c_E t. Write

    f(x)=1+x^T A x+O(r^4),   A=c I+K,   tr K=0,   c=tr A/3.

A, K and the tensor S below are constant real symmetric matrices with units
length^-2. K is the newly released directional clock quadratic coefficient;
S is the residual angular coefficient, matching LSR1/NAP1 when K=0.

For EVERY metric in the declared class its full spatial second jet is uniquely

    gamma=I-(x^T A x)I+C(x)^T B C(x)+O(r^4),   B=c I+S, tr S=0,
         =I-c xx^T-(x^T K x)I+C(x)^T S C(x)+O(r^4).       (D1)

Thus the marked second-jet space has 11 real components: c, five K and five S.
These are coefficients in this marked restricted class, not physical propagating
modes, independent invariant scalars, or an all-metric census. Frame rotations
conjugate K and S together. Higher jets remain outside this classification.

Necessity: if gamma=I+G2+O(r^4), exact gamma x=x/f gives
G2 x=-(x^T A x)x. Therefore [G2+(x^T A x)I]x=0. LSR1's already proved
six-dimensional transverse quadratic kernel gives G2+(x^T A x)I=C^T B C
for a unique symmetric B. This is reuse of that algebraic theorem.
The tangent trace of G2(rn) is

    r^2[-2 n^T A n+tr B-n^T B n].

Using the spherical average of n_i n_j, the leading relative area is

    Area(r)/(4 pi r^2)=1+(tr B-tr A)r^2/3+O(r^4).

Exact retained area requires tr B=tr A. This proves (D1), including its trace
condition. Areal normalization here concerns the supplied comparison spheres;
it does not define a pre-existing physical distance or a material boundary.

## 2. Converse: actual analytic metrics realize every allowed second jet

For ANY A,B symmetric with tr A=tr B, put f=1+x^T A x, D=C^T B C, and

    M(r)=average_(n in S^2) sqrt(det_(n-perp)( f(rn)^-1 I_T+D(rn) )),
    q(r)=1/M(r),
    gamma=f^-1 nn^T+q(r)[f^-1 P+D].                    (D2)

Take a small neighborhood where ||A||op r^2<1/2 and ||B||op r^2<1/3.
Then f>0 and the tangent matrix is positive: f^-1>2/3 and ||D||<1/3.
M,q are positive and analytic in r^2 by uniform analytic expansion and compact
sphere averaging. The leading area coefficient above vanishes, so q=1+O(r^4).
In Cartesian form

    gamma=f^-1 I+(q-1)f^-1 P+qD.

This is analytic and even at the center: q-1 is divisible by r^4, so its product
with P is analytic despite n being undefined at x=0. The second jet is (D1).
Exact gamma x=x/f follows from Dx=0; induced sphere area is exactly 4 pi r^2
by the definition of q. Positivity gives an actual Lorentz metric on a sufficiently
small neighborhood. These parameter-dependent existence bounds are not a cutoff
or a selected physical length. The normalizer enforces the inherited geometric
class, not a field equation or fitted observation.

This constructive family proves realization of every claimed jet. It does not
claim to recover every higher-jet metric. The expanded CLASS contains the entire
old radial-f LSR1 class exactly; (D2) need not reproduce every old higher-jet member.
No additional symmetry or condition has been released to obtain this converse.

## 3. Clock, ruler and angular records remain a single relation

On the same supplied surfaces F_(a,v)(x0,sigma)=(x0,a+sigma v), v!=0,

    h=diag(-f,gamma(v,v)), m_v^2=f gamma(v,v),
    H=diag(-f,1/f), Phi=-log(sqrt(f)), chi=tanh(Phi).

Completion is the already owned W1 operation, with the retained positive density.
At corresponding marked events, not independently integrated ruler coordinates,

    Phi=-1/2 x^T A x+O(r^4),
    m_v^2=|v|^2+(x cross v)^T B(x cross v)+O(r^4).       (D3)

The clock Hessian retains A, the density second jets retain B by the existing
polarization/reconstruction argument, and their traces obey the retained area
condition. Releasing K changes the clock AND the spatial metric. It is not an
independent angular correction with the complete distance record held fixed.
On radial pairs m_n^2=1 exactly. The full metric is used before readout; a scalar
kernel is not substituted for a distance or for the other relation data.

Static has its inherited meaning: time-independent metric and the fixed-position
clock congruence. It does not mean every such observer has zero proper acceleration.
The metric-derived static acceleration is a_i=partial_i log(sqrt(f)); anisotropic
f can give a tangential component. No physical source or force law is added.

## 4. Center curvature and the conditional DDR response

Use LSR1's R^a_bcd=partial_c Gamma^a_db-partial_d Gamma^a_cb+... convention.
All first metric derivatives vanish at x=0. Direct original-metric differentiation
of (D1), with eta=diag(-1,1,1,1), gives

    R_0i0j=A_ij=c delta_ij+K_ij,  R_0ijk=0,
    R_ijkl=delta_ik A_jl+delta_jl A_ik-delta_il A_jk-delta_jk A_il
             -3 epsilon_ijp epsilon_klq B_pq,
    Ric_00=3c, Ric_0i=0, Ric_ij=-3c delta_ij+3S_ij, R=-12c,
    TF(Ric)=3 diag(0,S),
    C_0i0j=K_ij+3S_ij/2,  magnetic Weyl=0,
    Weyl^2=8 tr[(K+3S/2)^2].                           (D4)

The cancellation of K in Ricci comes from the COUPLED clock and spatial changes;
it is not permission to discard K from the full curvature or observer records.

Only INSIDE the entire previously reviewed G301 class and its declared curvature
domain, E=a Ric+b Rg, a!=0, the adopted all-pair DDR constraint gives at this center

    TF(E)=3a diag(0,S)=0  iff  S=0.                    (D5)

Every K survives this algebraic center test. Applying it to a specified G301
response additionally requires the center curvature to lie in that response's
declared domain. Arbitrary finite A,B have geometric realizations by D2; this
does not enlarge the response domain. Retain metric-only local two-jet/curvature
order, unoriented natural symmetric rank-two typing, flat-quiet differentiability
F(0)=0, exact positive curvature-weight-one homogeneity on the stated star-shaped
quiet domain, and the scale/principal gates with a!=0. The same five NAP1 directions suffice on this
restricted response image; no full arbitrary-response test is inferred from five
directions. At S=0, E=-3(a+4b)c eta need not vanish. At a=0 DDR is blind here;
that stratum is excluded from the specified G301 diagnostic. Locality/GR filter
does NOT establish G301 membership. FE1 remains unadopted.

## 5. What changes in the geometric conclusion

S=0 no longer implies zero central Weyl or zero central null-screen tide. For
k=U+n and screen v,w perpendicular to n, normalized in the center metric,

    R(v,k,w,k)=2 v^T K w+(n^T K n)(v dot w)
                  -3(v cross n)^T S(w cross n).       (D6)

Its screen trace is 3 n^T S n, agreeing with Ric(k,k). At S=0 the screen trace
vanishes while its trace-free part can survive. All central null-screen tides
vanish for ALL n,v,w iff K=S=0 in THIS class: the traces first force S=0;
with K diagonalized, n along each eigenvector gives differences of the remaining
two eigenvalues, forcing K to be scalar and hence zero. This is an exact center
statement, not a physical light-transfer or all-neighborhood quietness theorem.

For example c=0, K=diag(kappa,-kappa,0), S=0, kappa!=0, has an exact local
realization (D2), Ric(0)=0 and Weyl^2(0)=16 kappa^2. For n=e3 and screens e1,e2,
the center tide is diag(2kappa,-2kappa). It is not a coordinate relabeling of the
old quiet center, since Weyl^2 differs. Its complete clock/ruler/angular records
also differ; this is not equal operational distance with an extra hidden effect.

There is NO claim that these examples solve Ric=Lambda g away from the center,
are physically admitted by all UDT postulates, represent stable modes, or yield
an observable new effect. A center condition is not a field-equation development.

## 6. Novelty, provenance and limits

Generic Einstein geometry already permits Weyl/tidal freedom; that is NOT new.
The scoped extension is the complete 11-component marked second-jet class and
its exact local realization under the RETAINED strong radial and areal conditions,
with its coupled record map and conditional center test. NAP1's original S=0
result survives on its original class. Its implication of center quietness used
K=0 and does not extend to the released class. This neither derives a field
equation nor proves broader native geometry admission. All original source grades,
registry, fixed manuscript and protected work remain unchanged.

Discovery was analytic before computational freeze. Parent derived this form and
center cancellation in its reasoning before receiving the reviewer's preliminary
source-first message; that private reasoning has no independent timestamped file
freeze. This initial written candidate follows that message and is therefore not
claimed blind to it. The reviewer has not yet seen this proof or parent code/output.
Exact source-first exposure and separate implementation are recorded in review/.
