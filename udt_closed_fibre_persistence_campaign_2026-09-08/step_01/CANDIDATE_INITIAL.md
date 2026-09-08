# CF1 initial candidate — UNREVIEWED / UNPROMOTED

Question and allowed equivalence were recorded first. Parent has not read any
CF1 reviewer reconstruction/code/output. The proof below is elementary
mathematics in a deliberately declared test class; it is not a vacuum witness.

## 1. Precise global class and equivalence

On S3 in C2 set s=|z2|². Let Z1=(iz1,0) and Z2=(0,iz2) be global rotation
fields with angle periods2pi. For r in C-infinity([0,1]), r>0, put

    X_r=Z1+r(s)Z2,       L_r=span(X_r).

Here smooth on[0,1] means smooth extension to a neighborhood of that interval.
Both fields preserve s; X_r is nowhere zero, including the axes. On each
regular torus0<s<1 it has angle components(1,r(s)); at s=0 only Z1 survives,
at s=1 only Z2 survives. The standard Hopf line is L_1. Multiplying X_r by
any smooth nowhere-zero function changes speed/orientation but not leaves.

A regular circle fibration means the connected leaves are the fibres of a
smooth submersion S3->smooth surface with local circle-bundle charts. Hopf
equivalence means a smooth diffeomorphism sends Hopf leaves onto these leaves;
the diffeomorphism need NOT commute with the torus action. The campaign's
stronger time-dependent equivalence requires a smooth isotopy F_t, F_0=id.
None requires equal lengths, equal speeds or an unaveraged quotient metric.

## 2. Exact closure

The flow on the torus through(z1,z2) is

    (exp(iu)z1, exp(i r(s)u)z2),       u real.                 (1)

An interior orbit closes iff there are integers m,n with u=2pi m>0 and
r(s)u=2pi n; equivalently r(s) is rational. If r=p/q>0 in lowest positive
terms, the primitive interior period of this representative is2pi q. At the
axes, the primitive periods are2pi and2pi/r(1), respectively. Axis circles
are closed regardless of the interior slopes.

Therefore ALL leaves are closed iff r is a CONSTANT positive rational:
necessity follows because continuous r maps the connected interval(0,1) into
Q only if constant (otherwise the intermediate value theorem supplies an
irrational value); continuity extends the same constant to the endpoints.
Sufficiency follows from(1) and the axis flows. Nonconstant r on even one
interior subinterval supplies an actual nonclosed orbit. This is exact real
arithmetic/topology, not a numerical rationality tolerance. No density claim
is needed for the obstruction.

## 3. All closed is weaker than a regular Hopf circle bundle

For constant r=p/q, multiply X_r by q to get the effective weighted circle
action(e^{iqu}z1,e^{ipu}z2). Near the s=0 core, a transverse disk has coordinate
w=z2. Follow one primitive turn of the core, time2pi for X_r, and compare
on the same transverse disk. The holonomy map is

    w -> exp(2pi i p/q) w,        order q.                    (2)

Near s=1 the transverse disk coordinate is z1; one core turn takes2pi/r,
giving w->exp(2pi i q/p)w, order p. Coprimality gives these exact orders.
If p or q exceeds1, some leaf has nontrivial transverse holonomy. A regular
circle-bundle fibre has trivial holonomy: a product chart around the entire
fibre identifies every transverse point after one leaf circuit. Holonomy is
conjugated under any leaf-preserving diffeomorphism. Thus changing speeds or
allowing a NON-equivariant diffeomorphism cannot remove this obstruction.

It follows that the following are equivalent in this positive-slope class:

    regular circle fibration <=> Hopf-equivalent <=> r identically1. (3)

For r=1 the original Hopf map [z1:z2] gives the actual regular bundle and
identity equivalence. For rational r!=1, all leaves still close but form a
Seifert fibration with exceptional axes, not a regular Hopf bundle. These
are smooth nonsingular line fields; 'exceptional' describes leaf holonomy,
not a singular vector field or a failure of UDT.

Primary terminology/control: Albach--Geiges, arXiv2102.08142v2, section2.1
and section5, describes regular versus singular Seifert fibres and weighted
actions on S3. The direct return-map argument above owns the present bounded
claim; no global classification theorem or imported physical model is needed.

## 4. Actual-time use and non-use

For a smooth family r(t,s)>0, r(0,s)=1, if all leaves close for EVERY t in a
connected time interval, the preceding criterion makes r(t,s) a rational
constant in s for each t; continuity in t then forces that rational constant
to remain1. Thus within this class all-time closure, all-time regular Hopf
fibration and the campaign's smooth-isotopy property are equivalent to r=1.
At isolated times all-closed rational exceptional cases remain possible.

More decisively, if an ACTUAL smooth family satisfies partial_s r(t,s0)!=0,
then at that actual time some torus carries nonclosed leaves; there is not
even an isolated-time diffeomorphism to a closed-fibre Hopf foliation. If a
lawful development supplied partial_t partial_s r(0,s0)!=0, differentiability
would force this obstruction for every sufficiently small nonzero t. That
last implication requires an actual development and the symmetry reduction
for all those times; a formal first jet alone does not supply either.

CF1 does not construct lawful metric data, eigenlines or developments. CF2
must prove that join separately. Homotopy of nonsingular directions does
not enforce any of(1)--(3). The result is restricted to the displayed positive
torus-slope family and is not a census of all foliations, arbitrary slicings,
topologies, physical dynamics or stability. No new carrier/action/law adopted.

Finite exact checks below support periods, return-map orders and exclusions.
They do not prove the continuity/holonomy statements by counting fixtures.
