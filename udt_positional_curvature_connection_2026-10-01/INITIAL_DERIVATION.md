# PCC1 initial candidate — isotropic addition, not isotropic total geometry

UNREVIEWED conditional candidate. The physical requirement tested here is explicitly
UNADOPTED. It is not inferred from no preferred observer, the existence of c_E,
ordinary clocks, or DDR. Source: PSW1's reviewed preparation and leading clock
theorem, SGE1's physical matching distinction, and current G312 GR-filter authority.
Discovery: the parent identified algebraic curvature polarization and a radial
nonuniform comparison before exposing this candidate to reviewers. Both fresh
contexts have sent short, concordant source-first observations, before this freeze;
their full arguments/code have not been read. This is not blind discovery.

## 1. An operational statement with explicit supplied matching

Supply smooth time-oriented Lorentz4 metrics g and g0, matched events p,p0 and a
time-oriented linear isometry I:T_p M -> T_p0 M0. I matches orthonormal laboratory
frames, not coordinate components. For every future unit U and spatial unit n
orthogonal to U, prepare the PSW1 free-clock experiment in each geometry with
(U,n) and (IU,In), equal small initial proper L, parallel initial velocity, units
c_E=1 and regular direct null branches. Each experiment holds its own prepared
worldlines fixed when differentiating nearby emission times. Ordinary clocks are
not clocks held at constant spatial coordinates.

Let p_L,p0_L be their first received-tick ratios. With
A_g(X,Y,Z,W)=g(R_g(X,Y)Z,W) and the PSW1 curvature convention, define

    D=A_g-I* A_g0,
    C(U,n)=lim_(L->0) 2 log(p_L/p0_L)/L²=-D(n,U,U,n).

The existing O(L³) theorem justifies this limit for each fixed regular smooth
comparison. It supplies no uniform finite-distance or empirical error bound.
The trial law is C(U,n)=kappa(p), the SAME scalar for every U,n at the matched
event. Its all-frame domain and leading L² identification are additional physical
choices. No uniformity over arbitrarily boosted laboratories is claimed for the
remainders. Positive kappa means positive leading ADDITIONAL log contrast; the
total received shift can have either sign.

This experiment is operationally specifiable in supplied geometries, but UDT has
not selected its reference or I. Under a common Lorentz change of matched frames
the statement is unchanged. Changing I relative to the reference generally
changes the comparison. A field of pointwise frame isometries need not be the
derivative of a spacetime isometry or preserve either connection. No metric sum
g=g0+delta g, physical second spacetime, or second propagation mechanism is adopted.

## 2. Exact pointwise implication

Define B_g(X,Y,Z,W)=g(Y,Z)g(X,W)-g(X,Z)g(Y,W), so B(n,U,U,n)=-1.
Then the trial law is equivalent, at the matched event, to

    D=kappa B_g.                                             (PCC-a)

Proof: F=D-kappa B is an algebraic curvature tensor with F(n,U,U,n)=0 for every
unit timelike U and orthogonal unit n. Homogeneity and projection of an arbitrary
X onto U-perp extend this to F(X,U,U,X)=0 for every X and timelike U. Polynomial
identity on the open timelike cone extends it to all U. Polarizing X gives
F(X,Y,Y,Z)=0; polarizing Y gives F(X,Y,W,Z)=-F(X,W,Y,Z). Combined with antisymmetry
in the first two slots, F is alternating in its first three slots. Algebraic
Bianchi gives 3F=0. The converse is direct. Thus no finite sampling of observers
is being substituted for the all-frame theorem.

Contracting gives

    Ric[g]-I*Ric[g0]=3 kappa g,
    R[g]-R[g0]=12 kappa,
    Weyl[g]-I*Weyl[g0]=0.                                  (PCC-b)

The last identity follows by substituting these contractions in the4D algebraic
trace decomposition. Ordinary anisotropic Weyl curvature may remain nonzero.
Only the difference has space-form type. This is not G212's total all-germ
isotropy, and not PSW1's identification of Ric with DDR's response.

One observer alone is inadequate: an algebraic curvature tensor with only a
nonzero spatial constant-curvature block has T=0 for U=e0. For
U=(5e0+3e1)/4 and n=e2 its tidal contraction is9K/16, so it fails the same
zero-addition condition in that boosted frame. A trace/triad mean is weaker again.

## 3. Regional consequences and what Bianchi does not supply

Suppose matching events/frames is smoothly supplied across a region and (PCC-a)
holds there. Put S=I*Ric[g0] as a tensor field on that region. Contracted Bianchi
for g and (PCC-b) give the NECESSARY compatibility condition

    3 d kappa=div_g S-(1/2)d tr_g S.                       (PCC-c)

It is not legitimate to set its right side to zero using Bianchi for g0:
the pulled reference tensor is differentiated by the g connection, and I may
vary. Full curvature Bianchi and realization requirements also remain; (PCC-c)
is not a sufficient metric construction theorem.

A useful special case is a supplied Einstein reference Ric[g0]=Lambda0 g0 with
constant Lambda0. Then S=Lambda0 g independently of variation in I. Consequently
Ric[g]=(Lambda0+3kappa)g and Bianchi gives d kappa=0 on a connected regular region.
In particular, a Ricci-flat reference yields Ric[g]=3kappa g. This repeats an
Einstein-with-constant-curvature-term possibility; it does not select the sign or
value, native admission, global state, matter coupling or the response E in DDR.
Matching Weyl in (PCC-b) remains an extra condition beyond that Ricci equation.

## 4. Exact nonuniform compatibility witness

Supply, on a common regular static patch r>0,0<theta<pi,f_k>0,f_0>0,

    g_k=-f_k dt²+dr²/f_k+r²(dtheta²+sin²theta dphi²),
    f_k=1-2 mu/r-kappa r²,   f_0=1-2 mu/r.

Here mu is a supplied geometric length parameter, not a derived material mass;
kappa is constant and freely explored. Matching uses equal areal sphere radius,
the same mu, and the corresponding time-oriented radial/angular orthonormal
frames (f^(-1/2)dt-dual, f^(1/2)dr-dual, r^(-1)dtheta-dual,
(r sin theta)^(-1)dphi-dual). Clocks are RELEASED with these initial velocities
and their simultaneous boosts; they are not held static during the experiment.
The common choices exploit this supplied symmetry, not a universal center.

Direct original-coordinate connection/curvature calculation is to check every
component in these matched frames, not only one contraction. Writing w=mu/r³,
the independent A_abba components are

    A_1001=-2w-kappa, A_2002=A_3003=w-kappa,
    A_1221=A_1331=-w+kappa, A_2332=2w+kappa.

All other components follow by curvature symmetries or vanish. Therefore
A_k-A_0=kappa B, Ric=3kappa g, R=12kappa, while the nonzero w-dependent Weyl
curvature survives. For any matched U,n the leading additional first clock
contrast is kappa L²/2; the return contrast is3kappa L²/2, with inherited local
O(L³) scope. This is not the finite sec(sqrt(kappa)L) law on a space form.

The family is the familiar Schwarzschild-(anti)-de Sitter/Kottler comparison,
not a newly derived UDT metric. Its role is a regional existence witness with
ordinary nonuniform tides. No Einstein equation was used as a native selection
input. Physical source, interior, horizon, boundary, stability, empirical filter
pass and X_max claims are outside this patch test.

## 5. Reference dependence and surviving meaning

Even a fixed supplied space-form metric has additional coefficient kappa-kappa0
when compared with a matched space-form reference kappa0. The choice of reference
therefore matters physically; tensorial covariance does not remove it. Selecting
kappa>0 would add a sign condition rather than follow from the all-frame law.

This candidate is a definite restriction once its comparison data are supplied.
It does not force total uniformity, and the witness shows regional compatibility
with anisotropic tides. In the vacuum-reference sector its Ricci consequence is
already an established GR possibility. No distinct UDT prediction, complete
field equation, finite-distance redshift/asymptote or reference-selection rule
has been obtained. Failure of this trial would not refute other finite/global
interpretations of the founding postulate; success does not adopt the trial.
