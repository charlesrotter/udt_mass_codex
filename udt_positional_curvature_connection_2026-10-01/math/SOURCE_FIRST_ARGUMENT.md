# PCC1 mathematical reconstruction before candidate exposure

Frozen source-first draft, 2026-10-01. Reviewer context `/root/pcc_math`, a fresh
separate context with the parent's inherited model. The available context does
not independently expose its exact serving-model identifier. Different-model,
human and formal-proof review are not claimed. Parent startup is attributed to
the parent; locally checked branch `grok`, HEAD
`ab1e0671feccc58ccb8ef735c9dc7dbc04a623e5`, no tracked changes and no matching
Python/scientific workers at entry. No PCC1 parent candidate, code, output, other
reviewer argument or verdict was seen before this file and independent code were
frozen. Shared sources are the work order, snapshot, central SGE1/PSW1 sections
and the PSW1 controlling repair/result. The parent's initial untracked-name
inventory was seen in SNAPSHOT; no protected payload was opened or hashed.

The applicable no-shortcuts, completeness-map and verifier-before-record
protocols were read. Their checklists are methods, not scientific premises.
No scientific process has run at this freeze: the parent's CPU slot is reserved.
This is an independent argument, not yet an adversarial review of PCC1.

## Operational quantifier and sign

Use the PSW1 prepared free-clock protocol in two supplied smooth Lorentz4
metrics, matched by a time-oriented tangent isometry I at the chosen events.
For all future unit timelike u and unit n perpendicular to u, transport both
vectors by I; match proper L, parallel preparation and the regular null rule.
Define A(u,n)=lim[L^-2(log p_L-log p0_L)]. The trial assumption is A(u,n)=a,
one number at the matched event, for every such pair. It is UNADOPTED and is not
a consequence of Lorentz covariance or of the kernel. The PSW1 theorem says
A=-Delta R(n,u,u,n)/2. Thus put k=2a. The outgoing coefficient is k/2, and the
actual return coefficient is 3k/2. These signs use (-+++) and
R(X,Y)=[nabla_X,nabla_Y]-nabla_[X,Y], with
R(X,Y,Z,W)=g(R(X,Y)Z,W).

## Algebraic implication: all timelike planes determine curvature

Pull the reference curvature back by I. It and the physical curvature are
algebraic curvature tensors on the same Lorentz vector space. Write their
difference D. Let

    G(x,y,z,w)=g(y,z)g(x,w)-g(x,z)g(y,w).

G(n,u,u,n)=-1. Consequently B=D-kG has B(n,u,u,n)=0 on every prepared pair.
For any fixed timelike y, projection of x perpendicular to y leaves
B(x,y,y,x) unchanged, by the curvature antisymmetries. Homogeneity and the
prepared-pair condition therefore give B(x,y,y,x)=0 for every x and timelike y.
For fixed x this is a polynomial in y, zero on an open cone; it is zero for all
y. Polarization and the first Bianchi identity then determine the complete
algebraic curvature tensor from this sectional polynomial, giving B=0.

For completeness, polarizing in x gives B(x,y,y,z)=0. Replacing y by y+w
gives B(x,y,w,z)+B(x,w,y,z)=0. Thus B is antisymmetric also in the middle
two arguments, in addition to its first-two antisymmetry. The cyclic first
Bianchi identity now consists of three identical terms, hence 3B=0.

Therefore the pointwise equivalence is

    all-frame, all-direction outgoing contrast a  <=>  D=2a G.

It entails Delta Ric=3k g, Delta scalar=12k, and equality of the Weyl tensors
under I. It does not impose zero Weyl on either individual metric or erase the
ordinary tidal anisotropy. It does not add metrics; only compared curvatures
are subtracted after the declared tangent matching. Nor does it turn DDR's
response into Ricci curvature.

One-frame isotropy is much weaker. In an ultrastatic product with a spatial
three-metric of sectional curvature c, the time-aligned electric curvature
vanishes in every spatial direction. For u=gamma(e0+v e1), however, the
transverse electric value is c gamma^2 v^2, while the longitudinal value
along gamma(v e0+e1) is zero. With v=3/5 these are 9c/16 and 0. The tensor is
not kG when c is nonzero. This control is an algebraic/product-geometry
comparison, not a UDT alternative selected by present premises.

## Regional integrability is a separate question

A pointwise isometry I does not provide a neighborhood map or differentiated
comparison. Even a smooth field of such isometries generally does not intertwine
the two Levi-Civita connections. The pulled reference curvature need not obey
the target connection's differential Bianchi identity. One cannot subtract the
two covariant Bianchi equations as though they used one connection.

A concrete control shows that k can vary in a smooth comparison. Compare

    g0=-dt^2+exp(t^2) sum_i (dx^i)^2,
    g =-dt^2+exp(t^2+2ct) sum_i (dx^i)^2,

at equal t and matching comoving orthonormal frames. This is a supplied family
with c free-and-explored, not an evolution law. Write H0=t and H=t+c.
Direct Levi-Civita curvature gives timelike sectional values a''/a=H'+H^2
and spatial sectional values H^2. Their six differences are all

    k(t)=2ct+c^2.

The mixed components vanish. Hence D=k(t)G everywhere, with nonconstant k
for c nonzero. Both metrics are smooth nondegenerate on all real t. Their
separate Bianchi identities hold automatically; the comparison matching is
not connection preserving. This directly refutes a general inference that the
trial condition forces a constant contrast throughout any connected region.

Additional hypotheses can restore constancy. If the reference is flat,
R=kG gives Ric=3k g. Contracted Bianchi gives 3 dk=(1/2)d(12k), hence dk=0.
Likewise, if the reference curvature transported into the target obeys the
target differential Bianchi identity, subtracting is legitimate and forces
constancy. A Weyl-plus-kG decomposition of the actual R also forces constancy
because Weyl has zero Ricci contraction. None of these extra hypotheses follows
from a collection of matched preparations.

## Nonuniform anisotropic metric witness

On a common static patch with r>0 and 0<theta<pi, supply

    g_k=-f_k dt^2+dr^2/f_k+r^2(dtheta^2+sin(theta)^2 dphi^2),
    f_k=1-2m/r-k r^2.

Compare g_k with g_0 at the same r and match their static orthonormal tetrads.
Require f_k>0 and f_0>0 on an open patch containing the infinitesimal clock
experiments. m and k, reference and matching are free-and-explored. This family
is a targeted compatibility witness; no field equation or physical source is
imported. In the order 01,02,03,12,13,23, direct curvature has sectional values

    (2m/r^3+k, -m/r^3+k, -m/r^3+k,
     -m/r^3+k, -m/r^3+k, 2m/r^3+k).

All mixed tetrad components vanish. Thus the full matched difference is kG,
while m nonzero leaves nonzero spatially varying Weyl curvature and unequal
radial/transverse tides. The physical metric is one metric; the reference is
a comparison. A regular concrete patch exists around m=1, r=4, k=1/100,
where f_0=1/2 and f_k=17/50. Nearby points satisfy both strict inequalities.
For these choices the physical electric values are (-33/800,9/1600,9/1600):
net radial and transverse prepared clock effects have opposite leading signs,
although the additional outgoing coefficient is +1/200 in every boosted frame.

The full tensor equality, not a finite boost sample, justifies every timelike
frame. This witness does not classify metrics or match arbitrary prescribed
gravitational fields, establish empirical compatibility at any precision,
select k, or derive UDT's additional positional effect. Its common patch
does not certify a global clock protocol, horizon crossing or finite distance
law. Positive k fixes the additional leading sign only; reference tides remain.

## Planned exact controls and omissions

The independently written `check_geometry.py` constructs Christoffel symbols and
the full original-coordinate curvature from generic diagonal metric entries.
It saves all six sectional values, Ricci and scalar contractions, mixed-component
zero checks, the static witness, the variable-k control and the boosted
one-frame counterexample. SymPy is a shared mathematical library, not a distinct
proof assistant. Exact symbolic assertions check this derivation; the algebraic
all-frame argument above supplies its quantifier. No empirical observations,
finite-L accuracy, PDE solver, general initial-data existence, numerical
continuum certification or physical adoption are tested. Preserved outputs
will distinguish actual checks from these plans.

## Source hashes at reconstruction

* AGENTS.md: bcab9b67305e0314af9eaf25162d203660eae8f2ff4fd87d17e83588970ef38d
* CLAUDE.md: 4ad2e773defb89cc79541fd0ababd75af5a3344ab134ee83722dfd943966e6e4
* UDT_DEVELOPMENT.md: db031b9386687dea9ffb0642fb0caa4d67a947be9648494d4f376ecfb14e26ce
* WORK_ORDER.md: aa618e3337dc450386672cfcf50491a405ad665a5ba2d5bcc462bdb2f0fd687f
* SNAPSHOT.json: a5351d880f4bc2cab23d38e32f8ac0efd05a72ffaac00bc3c44a55df7df8fb82
* PSW1/REPAIR.md: 696a97a3b59c37a88a1044dae940df9a18414aabada55335f495217e4f226a97
* PSW1/REVIEWED_RESULT.md: 1b217aa30932d3986557abb7e95f7d1e8a8196946e75091794b1ef06058e2911
