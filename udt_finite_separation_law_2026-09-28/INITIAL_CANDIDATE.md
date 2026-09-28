# FSL1 — a universal comparison rule and its asymptotic condition

Initial candidate for review. CONDITIONAL, UNPROMOTED. No native field equation
or physical protocol adoption. WORK_ORDER controls scope. Discovery recovered
G269/G272/G274: their clock/screen and composition results are reused, not new.

## 1. Objects and the sense of universal

Take a supplied smooth time-oriented Lorentz four-metric g of signature (-+++),
two supplied proper-clock worldlines, and a regular smooth branch of free null
geodesics between them. Set c_E=1 using length units for proper time. Endpoint
unit future clocks are u_e,u_o. A nonzero future affine tangent k obeys

    dx^a/dlambda=k^a,
    dk^a/dlambda=-Gamma^a_bc k^b k^c,
    dP^a_b/dlambda=-Gamma^a_cd k^c P^d_b,  P(e)=I.           (1)

Gamma is the Levi-Civita connection of this same metric; no independent
connection or Einstein field equation is inserted. Metric compatibility makes
P an isometry of tangent spaces and P k_e=k_o. Endpoint orthonormal frame maps
E_e,E_o (time columns u_e,u_o) give Lambda=E_o^-1 P E_e in SO^+(1,3), consistent
with G274's forward-vector convention. Local frame choices are coordinate data;
changing the physical observer is a different comparison. G269/G273 sometimes
express the target clock in the transported source frame instead; that is the
inverse convention and must not be mixed with the forward clock column below.

Universal here means one covariant functional of supplied metric, events,
observers and branch, not equal results for every pair or a distance-only law.
W4's one-geometry status remains provisional. G220 makes null correspondence a
conditional query, not a universal UDT physical protocol selected by this paper.

## 2. Finite clock law from the actual null correspondence

Write omega_i=-g(u_i,k_i)>0. The existing G220 relation is

    Z=d tau_o/d tau_e=omega_e/omega_o,  D=log Z,
    delta_clock=-D,  chi_clock=tanh(delta_clock).             (2)

For completeness, varying a smooth family x(lambda,s) of null geodesics gives
J=partial_s x, nabla_k J=nabla_J k, and
d[g(k,J)]/dlambda=g(k,nabla_J k)=1/2 J[g(k,k)]=0. Choose fixed parameter
endpoints for the family. Its endpoint J values are u_e and Z u_o if s=tau_e,
so (2) follows. Smooth regular branch/clock incidence, compatible affine
normalization and no re-emission are essential. This is the existing geometric
clock theorem, not a photon, energy, luminosity or detector law. A finite source
duration is the integral of Z over source proper time, not generally one Z times
the duration (G417/G423).

Let n_e,n_o be unit spatial directions of FUTURE propagation in the respective
endpoint frames (n_o is opposite the usual observer-to-source sky direction).
Define l(n)=(1,n). Then

    Lambda l(n_e)=f(Lambda,n_e) l(A(Lambda,n_e)),
    f(Lambda,n)=[Lambda l(n)]^0>0,
    A(Lambda,n)=[Lambda l(n)]^spatial/f(Lambda,n).

Since k_o=P k_e, A=n_o and f=omega_o/omega_e=1/Z. Thus, for supplied geometry,
there is no second free redshift response function. The normalized null vector's
time component fixes it. This is standard Lorentz/null geometry applied to the
existing UDT full-frame data, not a new law selecting g.

## 3. What composes, and what inversion means

For subdivision of the same ray, with a compatible intermediate frame,

    f(Lambda_2 Lambda_1,n)
      =f(Lambda_2,A(Lambda_1,n)) f(Lambda_1,n),
    A(Lambda_2 Lambda_1,n)
      =A(Lambda_2,A(Lambda_1,n)).                            (3)

Proof: apply Lambda_2 to the normalized-null decomposition after Lambda_1 and
read its positive time component. The intermediate direction MUST be carried.
This gives exact associative subdivision consistency and additive D on that ray.
An arbitrary intermediate observer changes the two factors but cancels in the
product. It does not change the emitted/reception clock ratio.

Inversion satisfies f(Lambda^-1,A(Lambda,n))=1/f(Lambda,n).
It inverts the same mathematical comparison. A later causal return, a redirected
ray or a physical relay is a new protocol. Different paths can carry holonomy;
no path independence, global simultaneity or instantaneous observable signal is
assumed. G274 already proves full-frame composition and loss of screen carry
under clock-column projection; (3) is its direction-retaining clock readout.

## 4. Explicit link to W5 and scalar kernel scope

Let c=Lambda e0=(gamma,s), and chi=s/gamma. Metricity gives
gamma=(1-|chi|^2)^(-1/2). In the reception frame c represents P u_e, so

    Z= -eta(c,l(n_o))
     = gamma(1-chi dot n_o)
     = (1-chi dot n_o)/sqrt(1-|chi|^2).                      (4)

Equation (4) applies to W5's projective state IF its supplied pair arrow is the
same full transported comparison on this actual null branch, with the same
clocks and orientation. It does not assign all physical W5 relations to null
queries or assemble their complete G176 pullbacks. The resemblance to SR's
Doppler expression is exact frame algebra; chi is the path-dependent projective
relation, not thereby a measured recession velocity or an expansion hypothesis.

G220 separately supplies T_comparison=Z when source proper time parametrizes the
actual event correspondence. G176 then gives Phi_comparison=-log Z. That clock
leg is compatible even with nonzero transverse data; it is not generally the
rapidity magnitude of c, nor construction of the full reciprocal pair plane.

Put rho=artanh |chi|. Cauchy--Schwarz gives

    exp(-rho) <= Z <= exp(rho),  |log Z| <= rho.             (5)

For rho>0 either endpoint equality requires chi parallel or antiparallel to
n_o, respectively. If chi=tanh(alpha)n_o for signed alpha, then Z=exp(-alpha)
and delta_clock=alpha. This is the matched oriented planar tanh law. At rho=0,
Z=1 in every direction. G269's W=0 criterion and G272's rapidity inequality
already own this planarity distinction. A generic planar clock leg is not
permission to discard transverse motion in the full four-dimensional arrow.

## 5. The limiting position needs a directional condition

For any family of regular supplied comparisons, let r=|chi| and (when r>0)
mu=(chi dot n_o)/r. Each member has r<1, -1<=mu<=1, and

    Z=(1-r mu)/sqrt(1-r^2).                                 (6)

The intended divergent redshift Z->infinity necessarily has r->1, by (5).
The converse fails without a directional condition. Set epsilon=1-r->0+.
Because 1-r mu=epsilon+r(1-mu) and sqrt(1-r^2)=sqrt(epsilon(2-epsilon)),

    Z->infinity  iff  (1-mu)/sqrt(epsilon)->infinity,
    Z->Z_*>0     iff  (1-mu)/sqrt(epsilon)->sqrt(2) Z_*,
    Z->0         iff  (1-mu)/sqrt(epsilon)->0.               (7)

These are necessary-and-sufficient LIMIT statements on the r->1 family. They do
not assert a limit for an oscillating family. Fixed mu<1 gives redshift
divergence; exactly mu=1 gives Z=sqrt((1-r)/(1+r))->0. Intermediate approach
angles permit every finite positive Z_*. No fitted profile is inserted.

An exact all-regular finite-redshift family uses a free parameter q>0:

    gamma=1+q^2/2,
    s=(q^2/2,q,0),   n_o=(1,0,0).

Then gamma^2-|s|^2=1, Z=gamma-s_x=1, while |chi|->1 as q->infinity.
A canonical Lorentz boost with this future clock column realizes the arrow;
its inverse maps l(n_o) to a future null launch direction. Each member can be
realized by inertial clocks and a null segment in Minkowski geometry. This is
a supplied comparison/control family, not a native cosmological UDT history or
an assertion that the intended physical population includes it. It is the
finite-law boundary consequence of the existing G269 fixed-clock-ratio freedom.

Conversely |chi_clock| can stay zero for that family. W5's full projective norm
and the scalar clock readout cannot be substituted at the boundary. No assertion
is made that their boundaries correspond to finite measured distance, or to
X_max. A physical asymptote requires a realized family, its distance/clock
protocol, and (7), not just the algebraic open-ball bound.

## 6. What this develops and the remaining equation

(1)-(4) provide a closed conditional TRANSPORT/READOUT system on supplied g and
observer/branch data. They are universal in form, covariant and subdivision
consistent, and use the same geometry as local clocks and cones. They close
no native metric dynamics. The substantive new return is the explicit null-ray
composition/readout synthesis and boundary test (7), with exact source matching;
most individual identities are recovered established mathematics/source results.

The omitted equation is not another z-versus-Phi function. It is a native
restriction on the allowed evolving metric/response that realizes the intended
positional comparisons. Current DDR still reads TF(E[g])=0 with physical E
unidentified; RMS1/CRV1 conditional response routes remain available. W4 and
universal comparison by themselves impose no new field equation. This work does
not prove that a new physical postulate is necessary.

The differential integral of -d log omega along an actual ray is another form
of (2), already developed in CRD1/G403; it is not offered as fresh closure.
Likewise G402's endpoint-potential condition is stronger than universality:
requiring it would add restrictions on g and the chosen congruence. It is not
silently imposed. Ordinary free initial/query data remain legitimate.

The next specific research target, if authorized, is to connect a candidate
native metric response to a realized family satisfying (7), retaining clocks,
direction/frame transport and curvature together. We must not choose an angle
or depth profile merely to obtain the target. No automatic successor solve.

## External method references

Levi-Civita uniqueness requires BOTH metric compatibility and vanishing torsion;
metric compatibility alone is insufficient. See David Tong, General Relativity,
section3.2.3: https://www.davidtong.org/teaching/general-relativity/grhtml/S3 .
This connection is already the G274 geometric method, not a new UDT postulate.

Bunn and Hogg, arXiv:0808.1081v2, discuss redshift via comparison along a null
path: https://arxiv.org/html/0808.1081v2 . We reuse only the geometric method,
not their cosmological model or preferred physical interpretation. Equations
above are derived explicitly and source ownership is kept separate.
