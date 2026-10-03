# IEC1 — what the prepared finite echo measures

Conditional mathematical result, subject to the captured verification and final
integration attestations bound with this edition. The initial candidate, source-
first reviews and subsequent proof completion remain fixed evidence. No physical
law, geometry, FC/RG condition, registry grade or canon is adopted here.

## The result and its domain

Supply a smooth time-oriented Lorentz4 metric of signature(-+++) with ∇Riemann=0
on a sufficiently small common normal tube. Use R(X,Y)=[∇X,∇Y]−∇[X,Y]. At o
choose future unit U and unit n⊥U. Clock A(s)=exp_o(sU); clock B begins at
exp_o(Ln), with U parallel transported along that spacelike preparation and
then follows its unit geodesic. Vary emissions on these same prepared clocks.
L>0 is calibrated initial proper separation, with c_E=1 only a unit convention.

Let F(s,b,L) be the squared geodesic interval from A(s) to B(b). The first
reception solves F(0,b,L)=0, b~L, and p=−F_s/F_b there. The immediate later
echo solves F(a,b,L)=0, a~2L, and q=−F_b/F_s there. These are positive proper-
time stretch ratios on their regular future branches. Their product pq is the
total echo stretch. No clock-exchange isometry or inverse/past return is assumed.
For sufficiently small L, p<sqrt2 and

    D(L)=log q−log[p/(2−p²)]

compares the actual echo with ECS1's particular space-form relation. It does not
by itself test every conceivable scalar Q in q=Q(p), nor attribute a positional
part of a combined signal. FCW1's stronger no-Q result also used its unboosted
records to fix Q; that additional argument is not silently generalized here.

At o define C=R(n,U), A=CU, B=Cn, T=g(A,n), V=A−Tn, W=B−TU. The reused
letter B in the tensor formulas means a vector, not the clock worldline.
V,W lie in the positive-definite complement of span(U,n). Write

    aa=g(A,A)=T²+|V|², ab=g(A,B)=<V,W>, bb=g(B,B)=−T²+|W|².

For pairs (V_i,Z_i) indexed0=(A,U),1=(A,n),2=(B,U),3=(B,n), set
Kij=g(R(V_i,Z_i)V_j,Z_j). Curvature integrability under ∇R=0 gives
R(A,n)=R(B,U), so indices1,2 agree. Then

    D(L)=d4 L⁴+d6 L⁶+O(L⁸),
    d4=2aa+ab−2T²=2|V|²+<V,W>,
    d6=[120K00+108K01−120K03+90K11−27K13
         +60T³+120T aa−236T ab−60T bb]/180.

These coefficients have units length^-4 and length^-6. The expansion is for
each fixed supplied metric, event and finite frame. It has no uniform large-
boost bound, explicit finite-distance error constant, global echo/caustic claim
or generic variable-curvature extension. Local symmetry does not mean constant
sectional curvature or constant coordinate metric components.

## Why the earlier sixth-order result was special

If V=0, n is an eigenvector of the electric tidal operator R(.,U)U. Substituting
aa=T²,ab=0,bb=−T²+|W|² and K00=−T³,K01=K11=K13=0,
K03=T³−T|W|² gives

    D(L)=(T|W|²/3)L⁶+O(L⁸).

This extends FCW1's one-family coefficient to every such prepared eigen-direction
in the declared locally symmetric class. A general direction has an earlier
quartic term, which can be positive or negative. Thus neither the order nor sign
of the original example is universal. FCW1 expressly left that question open;
its scoped formula is not refuted. A zero d4 in one direction need not set V=0.

At fixed o,U, reversing the physical preparation direction n while keeping L
positive sends V→−V,W→W,T→T. The future-directed experiments therefore obey

    d4(n)+d4(−n)=4|V|²,
    d4(n)−d4(−n)=2<V,W>.

Both quartic coefficients vanish exactly when V=0 for that fixed direction pair.
This is a direct tensor corollary, not inferred from the partial-tilt examples.
It identifies a way to separate geometric information with an enlarged clock
protocol; it is not complete curvature reconstruction or an all-frame rigidity
theorem. Even V=0 with a vanishing sixth coefficient can leave W when T=0.

## Derivation and analytic control

The detailed local proof is DERIVATION_COMPLETION.md. Parallel curvature makes
the radial Jacobi operator J_X(Y)=R(Y,X)X constant in parallel frames. Thus
dexp_X=P_X S_X with S_X=Σ(-J_X)^r/(2r+1)!, and the normal-chart metric is
g_o(S_XY,S_XZ). This analytic even expression applies also to null X and to
non-diagonalizable J_X. Radial reflection is a local isometry. Composing the
midpoint and origin reflections gives the preparation transvection with exactly
parallel differential; no positive-definite or global decomposition is imported.

The local isometry algebra splits into isotropy h and transvections p=T_oM.
The Killing-jet identity fixes [X,Y]=−R(X,Y) and [H,X]=HX. Local inverse-function
factorization G=exp(Z)k and the point-reflection involution σ then give
exp(2Z)=Gσ(G)^−1. For the actual two geodesic clocks this yields

    Z=1/2 log[exp(−sU)exp(Ln)exp(2bU)exp(Ln)exp(−sU)],
    F=g_o(Z,Z).

With s=Lx,b=Ly the palindrome makes Z odd in L. Its exact associative product/
log through degree7 determines F through degree8. All nested-curvature terms,
interval coefficients, arrival roots and p/q coefficients are saved in
UNIVERSAL_FORMAL_RESULT.json; no invariant is fitted to examples. In particular

    F/L²=1−(y−x)²−T(x²+xy+y²)L²/3+O(L⁴).

Metric skew-adjointness/pair symmetry reduce the higher contractions to aa,ab,bb
and Kij. The ∇R=0 derivation identity gives R(A,n)=R(B,U); that step is not valid
for an arbitrary algebraic curvature tensor without its integrability hypothesis.
Solving the two original null incidences and differentiating at their respective
endpoints gives d4,d6. The separate hand quartic audit checks the leading formula.

The normal-chart metric and local group formulas are analytic. F/L² is analytic
in L², with first/return limit-root partial derivatives −2 at(0,1) and(2,1).
The analytic implicit function theorem supplies the actual branches, their
emission derivatives and O(L⁸) remainder. Continuing signed L changes the root's
time orientation; its formal evenness does not equate the two physical future
experiments with n and−n.

## Verification and independence

The exact parent construction is not independent verification. Its separate
check re-expands every saved nested commutator into free associative words and
compares the original product/log coefficientwise through degree7. Independently
arranged original product-quadric and plane-wave null incidences challenge the
formula without using it to construct propagation or root data. Captured receipts
and PARENT_POLYNOMIAL_CHECK_RESULT.json record PASS for all13 exact cases in
five families and the complete word identity. The initial general-purpose series
run was manually interrupted after this equivalent fixed-degree implementation
passed; its streams/receipt are preserved and it is not counted as a pass. Full plane-wave curvature and ∇R are checked from its original
connection, including mixed-sign transverse eigenvalues and mixed directions.

Two actual fresh contexts sealed source-first controls before seeing the parent
candidate. Each independently derived tilted ultrastatic spherical controls.
Their off-sheet dimensions differ, but the tested sheet and main parameters
coincide: these are not two complementary tensor-space surveys. Each gives
d4=3483/10000,d6=−1371951/16000000 for the stated unit-curvature preparation.
The negative-tilt variant has d4=−567/10000. The fidelity review additionally
checks all interval polynomials through degree8 and p/q/D through degree6:
52 exact comparisons and24 actual-root cases at90 digits, residuals<1e-70,
with correct future time order. The math review supplies16 pre-exposure numerical
cases and a separate hand quartic extraction. Finite observed convergence is
corroboration; the local analytic argument owns the remainder.

Both reviewed the signature-independent completion, contraction signs, actual
return and direction corollary. They share the parent model and Python/SymPy/
mpmath, and the symmetric-space/embedding methods overlap. Fresh context,
independent original-incidence code, exposed checks and common libraries are
distinct independence axes. No different-model, formal-assistant, human,
empirical or native-admission review is claimed. Final maintained-file review
and normal/maintenance/full406 receipts remain explicit closure requirements.

## What has and has not been connected

Prepared finite clock records now have an invariant curvature interpretation
through sixth order in a declared class. FCW1's restricted result becomes a
proved eigen-direction case; an opposite-direction protocol separates the first
transverse contribution. This is geometric progress without adopting an equation.

The metric itself, ∇R=0 restriction, frame and preparation are supplied. The
native kernel still evaluates supplied pair data; it does not yet assign this
geometry. ULC1 universality is not scalar sufficiency FC. No Einstein/action/
source/light/matter law is added. DDR response identification, physical admission,
positional attribution, native scale and X_max remain open at their existing
grades. FCW1's completion lead/RG is unchanged and was not pursued in IEC1.
Neither a new postulate's necessity nor complete UDT underdetermination follows.
