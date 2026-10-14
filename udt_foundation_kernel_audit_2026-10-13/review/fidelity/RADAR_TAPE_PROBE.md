# FKA1 fidelity-review supplement — specified timing ruler versus completed tape

Status: exact analytic continuation of CLOCK_MAP_REALIZATION.md, preserving
that frozen file. Originated in `/root/fka_review_fidelity` during direct review.
This is new constructor work by the reviewer, so the reviewer's own derivation
is not independent certification of this supplement. No sibling review or
checker was read. The parent was notified of the equations before this freeze.

Question: can an explicitly prepared ruler from the same clock records be
identified with the G176 completed tape merely by reciprocal normalization?
This performs the informative operational-ruler test proposed by explorer B.
The timing convention is a declared **free-and-explored protocol**, not a new
physical premise or the uniquely intended owner meaning of “length.”

## 1. A ruler convention defined from the clock records

Use precisely the previous control's maps and common length-time units:

    f_AB(a)=Za,       f_BA(b)=Zb,       Z>1, a>0.

Let the B record be returned immediately under that chosen protocol. A's
return time is a_ret=Z²a. Define the radar convention

    D_rad(a)=(a_ret-a)/2=(Z²-1)a/2,
    t_rad(a)=(a_ret+a)/2=(Z²+1)a/2.

In physical time units multiply D_rad by c_E. These are functions of the
stipulated clock/event records and a synchronization convention. They do not
assert an independent physical flight-time cause. The previous metric family
has exactly these same records for every epsilon, so D_rad is unchanged.

## 2. The actual affine null ribbon and its completed tape

Retain the previous definitions

    C(a,v)=Z exp(2 epsilon H(a,v)),
    H(u,v)=[(v-u/Z)(v-Zu)]²/ell⁴,
    S(a)=integral from a/Z to Za of C(a,v) dv > 0.

Define the outgoing family by F(a,lambda)=(a,V(a,lambda),0,0), 0≤lambda≤1,
where the positive integral implicitly specifies V:

    integral from a/Z to V(a,lambda) of C(a,v) dv = lambda S(a).

Positivity gives a unique smooth V on each regular finite segment. F(a,0)=A(a)
and F(a,1)=B(Za), so the family retains the actual endpoint correspondence.
Differentiating with respect to lambda gives

    K=F_lambda=(0,S/C,0,0),
    J=F_a=(1,V_a,0,0).

C K^v=S is constant on each ray. This is exactly the affine geodesic equation
derived in CLOCK_MAP_REALIZATION, with the endpoint-normalized interval [0,1].
Direct contraction in the original metric, before any completion, gives

    h00=-C V_a,
    h01=-S/2,
    h11=0,
    det h=-S²/4.

At epsilon=0,

    V(a,lambda)=a[(1-lambda)/Z+lambda Z],
    -h00=1+lambda(Z²-1) ≥ 1.

On any compact emission window 0<a0≤a≤a1, smooth dependence and compactness
therefore give some epsilon_*>0 such that h00 remains strictly negative for
all |epsilon|<epsilon_* and 0≤lambda≤1. This existence argument suffices for
the two-sided local test; no explicit universal numerical bound is claimed.
Rank two and negative determinant hold throughout. Beyond this small-parameter
regularity range no whole-ribbon timelike-J conclusion is asserted.

For this regular family G176's exact completed density is

    m(a,lambda)=sqrt(-det h)=S(a)/2,

which is constant along lambda. Consequently its one-family completed tape is

    L_completed(a)=integral from 0 to 1 of m d lambda
                  = (1/2) integral from a/Z to Za of C(a,v) dv.

The clock and shift remain explicit. At the source T=1; at the target T=Z.
The kernel still gives the same Phi_clock=-log Z and chi for every epsilon.
No nonzero shift or density has been discarded.

## 3. Exact comparison

At epsilon=0, C=Z, hence

    L_completed(a)=Z(Za-a/Z)/2=(Z²-1)a/2=D_rad(a).

For each a>0, H(a,v)>0 on the open interior a/Z<v<Za and vanishes only at
the endpoints. Thus, within the established regularity window,

    epsilon>0  =>  C>Z in the interior  =>  L_completed>D_rad,
    epsilon<0  =>  C<Z in the interior  =>  L_completed<D_rad.

The inequalities are strict on a nonempty interval and require no numerical
quadrature. Infinitesimally,

    partial_epsilon L_completed at epsilon=0
      = Z integral from a/Z to Za of H(a,v) dv > 0.

This is an exact sign check, not a controlled approximation replacing the finite
inequalities. The completed tape is not the null proper length, which is zero;
it is the already declared G176 density integrated along its supplied family.
Nor is the radar convention automatically the length of a spacelike ruler.

## 4. Consequence and limits

The same ordinary free clocks, alignment, full timing maps, bilateral slowing,
return record and radar convention coexist with different completed tapes.
Thus an actual choice of timing ruler does not become the G176 ruler merely by
algebraically normalizing each pair. If equality with this radar convention
were additionally required, it would be a substantive condition; within this
one-parameter family it excludes all nonzero sufficiently small epsilon.
No such physical equality is adopted or attributed to Charles here.

This closes the bounded compatibility test that the initial candidate left as
a possible next probe. It neither selects the radar protocol nor proves that
the owner intended it, and does not classify all metrics compatible with any
larger observation set or all UDT commitments. It selects no source, field law,
scale, X_max realization, cosmic history or physical pair population. More
numerical sampling cannot strengthen the exact conditional conclusion above.

Checks are direct analytic differentiation, metric contraction, compactness
on the stated regular strip and positivity of a displayed integral. No numerical
or symbolic worker, external theorem lookup, source-checker reuse or empirical
observation was involved. Fresh separate-context review is still required.
