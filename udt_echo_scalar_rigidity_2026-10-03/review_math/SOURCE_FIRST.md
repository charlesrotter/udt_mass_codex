# ESR1 independent source-first mathematical argument

Reviewer: actual separate context `/root/esr_math`, inherited parent model;
2026-10-03. This is independent argument authorship, not a different model or
formal proof assistant. Parent ESR1 candidate/code/results were not read. The
ESR1 WORK_ORDER and BASELINE were read, together with the exact IEC1 reviewed
result, direction corollary and hand quartic audit, ECS1 reviewed result/initial
derivation, FCW1 reviewed result and the central R8IEC excerpt. Source versions
and this argument/check/output are sealed separately before candidate exposure.

Scoped startup: parent reports completed current startup/synchronization and a
verified prior exact-edition full406 receipt, with fresh closure audit pending.
I independently read AGENTS, applicable CLAUDE sections and the no-shortcuts,
completeness-map and verifier-before-record protocols. I checked branch grok,
HEAD fd66e831edf2ce1e4b9c8bda02a61c44105524f1 and empty tracked diff at entry.
Unrelated untracked names were visible only in status/baseline. Protected
payloads were not read, hashed or used. A container process listing is not an
actual-host process check; that startup claim is attributed to the parent.

## Scope and controls frozen before the check

Question: a single smooth scalar Q on a neighborhood of 1 covers every event,
future unit U, unit n in U-perp, both physical directions and every sufficiently
small positive separation in a connected supplied locally symmetric Lorentz4
region. Is the supplied geometry necessarily constant sectional curvature?
Metric-led; the locally symmetric class is FREE-AND-EXPLORED and the PSW
protocol/tensor conventions are PINNED-BY-THEORY only inside their supplied
conditional sources. FC is UNADOPTED. No physical equation, native selector,
matter/light law, scale, boundary or X_max enters this argument.

One independently authored finite exact-arithmetic check: two algebra families
(scalar Taylor matching and the Lorentz4 curvature linear system), fewer than
500 scalar assertions, one CPU process/thread, 2 GiB address-space cap through
the existing capture.py, no elapsed/CPU timeout and no GPU. Degree is at most
four in L for the scientific argument; the tensor system has 21 variables and
36 equations. Stop on a failed assertion or exception; preserve failure streams.
No empirical fitting. Finite checks corroborate the proof below and do not own
the all-frame conclusion. No sixth-order or raw IEC free-word replay is claimed.

## Proof of necessity, including zero-leading cases

Write e=L^2. IEC1's reviewed formulas give, for a fixed preparation,

    p = 1 - T e/2 + (T^2/6 - ab/6 - bb/24)e^2 + O(e^3),
    q = 1 - 3T e/2 + (T^2/4 + 2aa + ab/2 - bb/8)e^2 + O(e^3),
    aa=T^2+|V|^2, ab=<V,W>.

The first two lines are also independently hand-extracted in IEC1's saved audit.
All small-L limits give Q(1)=1. First consider the case that some prepared tidal
value T is nonzero. Matching the e coefficient forces Q'(1)=3. Set
c=Q''(1)/2, so Q(1+z)=1+3z+c z^2+o(z^2). For every preparation, even when its
own T vanishes, matching e^2 gives

    2|V|^2 + <V,W> = (c-7)T^2/4.                     (1)

This coefficient equation uses a twice differentiable Q only; smoothness is
stronger than necessary here. The analytic IEC expansions apply separately to
each fixed event/frame, so no radius uniform over boosts is used.

For fixed event and U the electric operator E_U:X -> R(X,U)U is self-adjoint
on the positive definite 3-space U-perp. If a T is nonzero somewhere, E_U is
nonzero there and has an orthonormal eigenvector n with nonzero eigenvalue T.
For this eigenvector V=0, hence (1) forces c=7. Therefore the common Q satisfies
Q'(1)=3, Q''(1)=14 and every preparation has d4=0.

IEC1's physical direction reversal, not formal signed-L continuation, gives
d4(n)+d4(-n)=4|V|^2. Thus V=0 for every event, U and n, including T=0 directions.
Consequently E_U has every unit vector as an eigenvector and is scalar:

    R(n,U)U = t(U)n for all n perpendicular to U.       (2)

Linearity shows the scalar is independent of n: apply E_U to the sum of two
orthonormal eigenvectors. This does not set W=0 from a single direction's d6;
instead the all-U tensor conclusion below closes that possible loophole.

To cover the alternative omitted above, suppose every prepared T is zero.
Polarizing the quadratic form of the self-adjoint E_U gives E_U=0 for each U.
The tensor polarization argument below, with t=0, then gives R=0. Thus there
is no missing nonflat branch in which all leading shifts vanish.

## Elementary tensor step, with no classification import

At a fixed event choose future unit U0. Any other future unit U has the form
U=cosh(r)U0+sinh(r)n0 for some spatial unit n0 (r=0 is trivial). The associated
unit n=sinh(r)U0+cosh(r)n0 spans the same timelike two-plane and
n wedge U=n0 wedge U0. Pair antisymmetry and multilinearity therefore give

    g(R(n,U)U,n) = g(R(n0,U0)U0,n0).

By (2), t(U)=t(U0)=t at this event. Let K=-t and define the space-form algebraic
curvature tensor R_K(X,Y)Z=K[g(Y,Z)X-g(X,Z)Y]. Its electric operator is t I.
For S=R-R_K, g(S(X,U)U,X)=0 for every timelike U and arbitrary X: first project
X into U-perp, since its parallel component drops by curvature symmetries,
and rescale U. For each fixed X this is a quadratic polynomial in U, vanishing
on the open timelike cone, so it vanishes for every vector U.

Here is the final polarization explicitly. Write S(x,y,z,w)=g(S(x,y)z,w).
Starting with S(x,y,y,x)=0 for all x,y, polarizing x gives S(x,y,y,z)=0.
Polarizing y then gives S(x,y,w,z)=-S(x,w,y,z). Together with skew-symmetry
in the first two arguments this makes S alternating in its first three slots.
The first Bianchi identity is then 3S(x,y,w,z)=0. Hence S=0.

Thus R=R_K pointwise. The contraction defining K is smooth, and parallel
curvature plus metric compatibility gives dK=0 (the metric wedge tensor is
nonzero). Connectedness makes K constant across the region. This establishes
local constant sectional curvature, including K=0, without a Lorentzian
symmetric-space classification theorem or a positive-definite assumption on
the entire tangent space.

## Sufficiency and what Q is actually determined

Conversely, constant sectional curvature supplies the ordinary local space-form
normal geometry. This can be seen directly from the radial Jacobi construction
already proved in IEC1: with R=R_K its normal metric agrees with the constant-K
model near each point. An orthonormal frame can be mapped to the model frame;
PSW preparation and the selected local first/immediate return are isometric.
ECS1's original signed metric/null-clock reconstruction consequently applies:

    p=1/c, q=c/(2c^2-1)=p/(2-p^2),
    c=cos(sqrt(K)L) for K>0,
    c=cosh(sqrt(-K)L) for K<0,
    p=q=1 for K=0.

Only a sufficiently small common regular branch is used. The rational Q0 is
smooth near 1, so existence of a single smooth Q follows for every constant K.
The theorem does not select K's sign/magnitude or global topology/completeness.

For nonzero K, varying small positive L at just one event/frame attains an open
one-sided interval adjacent to 1: above 1 for K>0, below 1 for K<0. Therefore
any admissible Q equals Q0 on that attained interval. Smoothness fixes its full
jet at 1, but not its values on the unattained opposite side: a smooth function
flat at 1 supported there may be added. No analytic-Q premise was supplied.
For flat geometry the only attained value is p=1, and the entire requirement
on Q is Q(1)=1; its derivatives are free.

## Adversarial conclusion before candidate exposure

The all-preparation arbitrary-smooth-Q question has an elementary conditional
rigidity proof using only the reviewed quartic coefficient, spectral positivity
on U-perp, physical opposite-direction experiments and curvature polarization.
The sixth-order term is unnecessary. No surviving non-space-form counterexample
fits these quantifiers. Restricted sheets, fixed-U-only data, one direction,
finite observed cases, nonsmooth Q, variable-curvature metrics and physical
adoption are outside this conclusion. Old ECS restricted-record mimics and
Kasner/FCW counterexamples retain their existing scoped meanings.

Status of this source-first argument: candidate independent proof, awaiting
exact finite check receipt and substantive exposed-candidate comparison. This
does not constitute acceptance of an unread parent candidate or final package.
