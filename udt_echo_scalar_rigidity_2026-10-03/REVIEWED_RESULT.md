# ESR1 — scalar echo selectivity within locally symmetric geometry

VERIFIED-WITH-CAVEATS conditional mathematical return. Actual exposed/final
reviews, exact bindings and captured checks own acceptance of this edition.
FC remains a hypothetical UNADOPTED physical condition; this result neither
adopts it nor shows that UDT's founding interpretation requires it.

## Result

On a connected smooth time-oriented Lorentz4 region with ∇Riemann=0, the
following are equivalent:

1. There exists one smooth scalar Q near1 such that q=Q(p) for every PSW
   preparation: every event, future unit observer U, unit spatial n⊥U, both
   physical directions and every sufficiently small positive separation L on
   the regular actual first/immediate future-return branches.
2. The supplied metric has constant sectional curvature κ on that region.

The interval may depend on the fixed preparation; no uniform radius for unlimited
boosts is assumed. C² regularity of Q is enough for necessity. This classifies
local curvature under the stated hypothetical condition, not global topology,
completeness, a unique physical metric or a selected equation/source/scale.
κ has arbitrary sign and magnitude, including0.

For nonzero κ the exact curve is Q0(p)=p/(2−p²) on the attained one-sided
interval near1. Q'(1)=3,Q''(1)=14 are necessary. Smooth values off the attained
side need not equal Q0; a function flat at1 supported on that side may be added.
For κ=0 all records are p=q=1, so only Q(1)=1 is fixed and its derivatives
remain arbitrary. Finite Taylor coefficients alone do not establish the exact
rational identity; it follows after geometry classification and original incidence.

## Necessary chain

Use IEC1's reviewed P=log p=−TL²/2+O(L⁴) and
log q−H0(P)=d4L⁴+O(L⁶), where H0(P)=3P+4P²+O(P³) and
d4=2|V|²+<V,W>. Here T=g(R(n,U)U,n), V=R(n,U)U−Tn,
W=R(n,U)n−TU, in signature(-+++), R=[∇,∇]−∇_[,].

If curvature is nonzero somewhere, some electric tidal operator E_U on Euclidean
U⊥ is nonzero. Otherwise polynomial continuation of R(X,U)U from the timelike
cone and curvature polarization imply R=0. A nonzero self-adjoint E_U has a
nonzero eigenvalue T and eigenvector n, for which V=0. This is a Euclidean
spectral argument on U⊥, not an indefinite-signature diagonalization assumption.

Set H(P)=log Q(exp P). Along that eigen-direction, matching the L² and L⁴
terms forces H'(0)=3,H''(0)=8. Therefore the same H makes d4=0 for all
preparations, even directions with T=0; no division by their T is used.
IEC1's opposite-future-direction identity then gives

    0=d4(n)+d4(−n)=4|V|².

Every spatial n is consequently an eigenvector of E_U. Linearity forces
E_U=λ(U)Id. Any two future timelike unit U,U' are related inside their common
timelike plane by a determinant-one boost. Its sectional contraction is unchanged,
so λ(U')=λ(U) at that event. With κ=−λ, subtract
Rκ(X,Y)Z=κ[g(Y,Z)X−g(X,Z)Y]. The difference has zero timelike Jacobi
operators. Polynomial continuation followed by polarization and the first Bianchi
identity makes the entire difference tensor zero. This includes all-leading-zero
curvature and excludes a hidden nonflat branch, without assuming T≠0 everywhere.
Finally ∇R=0 and ∇g=0 give dκ=0; connectedness supplies one constant κ.

INITIAL_CANDIDATE contains the full boost/polarization steps. The fidelity
review supplies a complementary Ricci null-cone argument for the tensor step.
No Lorentzian symmetric-space classification theorem is imported. The sixth-order
IEC1 coefficient is unnecessary for this selectivity conclusion.

## Sufficient chain and proper chronology

IEC1's normal-chart Jacobi metric shows that a tangent reflection fixing
span(U,n) is a local isometry for Rκ. Its fixed surface is totally geodesic;
the preparation, free clocks and unique short null connectors stay in it.
Its original constant-curvature quadric incidence, with c=Cκ(L), is

    F(s,b)=c C_{−κ}(s)C_{−κ}(b)−κ S_{−κ}(s)S_{−κ}(b)−1=0,

where Cκ'=−κSκ,Sκ'=Cκ,Cκ(0)=1,Sκ(0)=0. First reception obeys
c C_{−κ}(b)=1,b~L. Differentiating gives p=1/c. For the later return
F(a,b)=0,a~2L, let h=S_{−κ}(b),z=κh²=1/c²−1. Then
C_{−κ}(a)=(1+z)/(1−z),S_{−κ}(a)=2h/(1−z), and

    q=−F_b/F_s=1/[c(1−z)]=c/(2c²−1)=p/(2−p²).

The first and return derivatives are evaluated at different events. The return
is not an inverse/past signal or an assumed Q-generated record. Small positive
L supplies positive p,q with p<sqrt2. At κ=0 the original flat incidence gives
b=L,a=2L,p=q=1 separately; the displayed unscaled F cannot be divided by κ
there. For κ>0, c=cos(sqrtκ L), so attained p>1. For κ<0,
c=cosh(sqrt(−κ)L), so attained p<1. No global causal-domain extension is claimed.

## Actual checks and review limits

The parent exact check initially failed a structural SymPy equality: two equal
polynomials were factored with opposite sign placements. The original script,
freeze, failed capture and finite diagnostic are preserved. The repaired script
changes three assertions to exact expanded-difference=0, retaining every equation,
case and threshold. Its actual PASS includes11 exact groups,16 signed original-
incidence root cases at80 digits with errors<1e-65, a separate flat control and
six unused-side Q checks. These supplement the proof; they do not classify a
metric class by sampling or prove smoothness from finite evaluations.

Two actual fresh contexts reconstructed the necessity proof before parent
candidate exposure. Both independently authored exact curvature linear systems
with all21 symmetric bivector components and the first Bianchi constraint.
The math review's36×21 system has rank20 and exactly the space-form kernel
(seven rational frames;19 exact assertions in two families). The fidelity
review's46×21 isotropy system also has rank20, while its55×21 zero-electric
system has full rank21 (nine frames;155 scalar constraints in three families).
Its nonflat ultrastatic control has zero rest-frame tides but nonzero boosted
tides, guarding against “one observer sees zero” being mistaken for flatness.

The exact finite rank implications concern the full declared algebraic tensor
space, with independent checks of its representation/Bianchi condition. They
support the analytic all-frame proof; they are not a numerical geometry census.
Both use shared SymPy and related bivector methods. The parent original-clock
check is complementary. Source-first arguments, exposed reviews, source versions,
metadata correction and final accepted-map bindings are retained. Fresh contexts,
independent code/argument, common model/library, source-coefficient dependence
and exposure are stated separately. No different-model, human, formal-assistant,
empirical or physical-admission review is claimed.

## Meaning for the program

This closes the specified all-frame scalar selectivity question inside the
supplied locally symmetric class. Restricted aligned-sheet mimics remain valid
counterexamples to the earlier weaker reconstruction claim; they simply do not
satisfy this stronger all-frame condition. The theorem does not extend to generic
variable curvature, test a real instrument or attribute an additional positional
effect. Universal governing law remains weaker than scalar sufficiency.

Imposing FC here selects the constant-curvature class and removes anisotropic
curvature within it, but selects neither κ nor native physical admission.
The result gives the proposed condition a concrete mathematical cost. Retain it
as a conditional diagnostic; do not silently promote it to the UDT postulates.
