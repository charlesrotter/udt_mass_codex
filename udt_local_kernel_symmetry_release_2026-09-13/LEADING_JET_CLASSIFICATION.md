# LSR1 additional candidate — complete leading angular jet in the retained class

UNPROMOTED mathematical candidate, direct review pending at its own freeze.
This is an advance within the work-order question, discovered analytically
after the first candidate's exact check; it is not a retroactive preregistration
or a correction hidden inside that earlier candidate. No new physical premise,
geometry law or resource allocation is introduced. Native admission stays OPEN.

## Exact class and statement

Fix the same Cartesian comparison marking. Let g=-f(r)(dx0)^2+gamma_ij(x)dxi dxj
be any analytic-even static metric near x=0, with f=1+c2 r^2+O(r^4)>0,
gamma(0)=I, gamma positive definite, and the strong radial condition

    gamma(x)x=x/f(r).

This retains both the reciprocal radial block and zero radial-angular mixing;
it is stronger than testing gamma(n,n) alone. Require each small centered
sphere's total area to be 4 pi r^2; no pointwise angular density is prescribed.
These are the inherited comparison restrictions declared in the initial work
order, not asserted universal physical UDT postulates.

Then its full spatial second jet has the unique form

    gamma(x)=I-c2 xx^T+C(x)^T S C(x)+O(r^4),

where S is a constant real symmetric tracefree 3 by 3 tensor. Conversely,
EVERY such S is realized by an exact local analytic-even metric with these
retained properties, via INITIAL_CANDIDATE plus SCOPE_CLARIFICATION. Thus five
tensor components exhaust the marked leading angular freedom. They are not
five propagating physical modes, a full-metric classification, or five
coordinate-invariant scalar parameters; rotations conjugate S and rotate the
supplied marking together. No coordinate/frame is physically preferred.

## Derivation from the retained conditions

Write gamma=I+A(x)+O(r^4), where A is a symmetric matrix of homogeneous
quadratic polynomials. Expanding the exact radial condition gives
A(x)x=-c2 r^2 x. Set B(x)=A(x)+c2 xx^T; then B(x)x=0.

Let H_ij,kl=partial_k partial_l B_ij, a constant tensor symmetric in ij and
kl. Differentiating B(x)x=0 gives the cyclic identity

    H_ij,kl+H_ik,jl+H_il,jk=0.

Build the original-metric curvature of I+B at its zero-connection center:

    R^B_ikjl=(H_il,kj+H_kj,il-H_ij,kl-H_kl,ij)/2.

Contracting with xk xl gives -3 B_ij: the four unhalved contractions are
-B_ij, -B_ij, -2B_ij, -2B_ij respectively, by the cyclic identity.
Therefore

    B_ij=-(1/3) R^B_ikjl xk xl.

In three spatial dimensions, an algebraic curvature tensor is a symmetric
bilinear form on the three-dimensional space of two-forms. Contraction with
epsilon identifies it uniquely with a symmetric matrix S by

    R^B_ijkl=-3 epsilon_ijp epsilon_klq S_pq,
    S_pq=-(1/12) epsilon_pij epsilon_qkl R^B_ijkl.

Substitution gives B=C(x)^T S C(x). This is a checked standard algebraic
identification, not a physical response law. It can also be verified as a
36-coefficient polynomial linear system: the constraint Bx=0 leaves six
independent symmetric-S coefficients before area is imposed.

For a unit n, the tangent restriction of B(rn) has trace
r^2[tr S-n^T S n]. The radial -c2 xx^T term vanishes on the tangent plane.
Consequently the induced area expansion is

    Area(r)=4 pi r^2[1+(tr S)r^2/3+O(r^4)],

using <n_i n_j>=delta_ij/3. Exact areal normalization forces tr S=0.
It imposes further higher-jet conditions, but these cannot further restrict
S: the exact q-normalized construction realizes every tracefree S locally.
This converse is why the leading classification is sufficient as well as
necessary; a mere coefficient count would not prove exact realization.

## Consequences at the center, and their limit

All center tensor formulas in INITIAL_CANDIDATE now apply to every member
of this retained comparison class, with c=c2. In particular the radial
clock/ruler/acceleration relations survive, R(0)=-12c2 remains fixed, and

    T(v,w)|0=-3(v cross n)^T S(w cross n),
    Weyl^2|0=18 tr(S^2).

Every central null-screen tide vanishes if and only if S=0, within this class.
For S nonzero the leading tide need not vanish, despite unchanged radial
records and leading scalar curvature. This is an exact leading-jet statement,
not a linearized field equation or a global nonlinear result. Every admitted
coefficient in this geometric class has the full local realization just proved.
Here 'admitted' means satisfying the DECLARED GEOMETRIC CLASS ONLY, not native
UDT physical admission or an inherited stronger G312 response condition.

S=0 only establishes central quietness. Higher angular jets remain free subject
to the exact retained conditions; this theorem does not restore the spherical
4:1 quartic ratio, classify those higher jets, or imply exact zero tide away
from the center. A full ray/path history, source, observation or new signal
model does not enter. Native UDT restrictions on the angular jet remain open;
this result locates precisely what such a restriction would have to address.

## Additional frozen checks and review request

Before executing this additional classification check, freeze this file and
its implementation. In exact symbolic arithmetic, build all 36 coefficients
of symmetric quadratic B, impose every coefficient of Bx=0, check rank30
and nullity6, verify the six-dimensional C^T S C image is exactly that kernel,
and verify the integrated leading area condition removes only tr S, leaving
five components. Independently check the inverse curvature-to-B identity
on the general kernel. These are algebraic checks, not an alternate physical
premise or an independent reviewer. The existing fresh reviewer should
adversarially check necessity, exact realization, quantifiers and data/gauge
typing within the original forty-minute allocation.
