# CRV1 — local conservation completion and the variational boundary

DRAFT conditional mathematics; UNPROMOTED pending independent review. No
physical response, action or scientific premise is adopted. Source scope:
WORK_ORDER.md and LAUNCH.json. Smooth Lorentz4 geometry, signature -+++,
Levi-Civita connection; all tensor equations below specify their quantifiers.

## 1. What the existing postulates supply

Current owner-provisional DDR, on its regular full all-pair domain, imposes
S[g]=TF_g(E[g])=0 for a specified symmetric covariant response E. It does not
define E. Local Metric Sufficiency rules out an independent hidden-history
label once the relevant finite metric jet is fixed; it does not fix differential
order, response type, scaling or an action. Founding positional dilation and
ordinary proper clocks describe one geometry, not a supplied action density.
GR remains FILTER ONLY. GRS1/RMS1 already isolate these boundaries; they are
not newly discovered nonselection results in CRV1.

Equivalence/local inertial coordinates and differential Bianchi identities hold
for the supplied Lorentz metric independently of its field equation. Curvature
does not vanish merely because its connection vanishes in normal coordinates.
In particular div Ric=(1/2)dR and div G=0 are identities; div E=0 is not an
identity for every natural metric response. GRS1's two-term classification and
RMS1's trace-free sufficient class remain conditional with all their hypotheses.

## 2. A local integrability test for the missing trace

For any FIXED supplied smooth metric on a contractible neighborhood, and a
specified smooth symmetric trace-free tensor S, every representative with that
trace-free part is E=S+qg. Put j_b=nabla^a S_ab. Metric compatibility gives

    nabla^a E_ab = j_b + partial_b q.

There exists a smooth scalar q on this neighborhood making E divergence-free
if and only if the one-form j is closed:

    d j = 0,       i.e. partial_a j_b - partial_b j_a = 0.

Necessity is d^2q=0; sufficiency is the local Poincare lemma. The scalar q is
unique up to a constant on a connected neighborhood. On a general domain the
condition is exactness of j, not just closedness; periods can obstruct a global
primitive. This is an exact local criterion for scalar completion ON A FIXED
GEOMETRY. It is NOT a sufficient theorem that q is a natural finite-jet metric
operator, or that E is variational, physically identified or causal/well-posed.
Those are further questions, even if this test passes for every supplied metric.

On a solution S=0, j=0 already and conservation only makes q constant. That
on-solution fact cannot establish an identity on arbitrary trial metrics or
select the response S. The relevant check for an off-shell law must be made
before restricting to its solutions.

## 3. Apply the test to the current conditional Ricci route

If S=a(Ric-Rg/4), with constant a, contracted Bianchi gives

    j=(a/4)dR,       q=-aR/4+C,
    E=a(Ric-Rg/2)+Cg = aG+Cg.

Thus within this already conditional trace-free class, conservation completes
the representative to Einstein form up to a constant trace term. For universal
constants a,C, compactly supported inverse-metric variation of

    I[g]=integral sqrt(|g|) (a R-2 C)

produces precisely this E. This supplies a conditional action representative;
it does not select the constants, nonzero a, physical source coupling, global
completion or initial data. DDR continues to impose only TF(E)=0, not E=0.
Hence neither the full vacuum Einstein equation with a prescribed cosmological
constant nor stationarity under ALL metric variations is adopted. For a!=0,
DDR's trace-free Einstein solutions already have constant R; conservation was
not needed to obtain that prior result. This step completes a representative
and gives its variational meaning; it does not prove native response membership.

## 4. The completion condition is not automatic

Take the UNADOPTED comparison operator S=TF(R Ric)=R Ric-(R^2/4)g.
It is a smooth natural, symmetric, trace-free, metric-only second-order operator.
It is outside RMS1's exact weight-zero class and lacks its nonzero flat linear
shape response; it is not claimed to satisfy the empirical GR filter or all
UDT premises. Product differentiation and Bianchi yield

    j_b = Ric_ab nabla^a R.

Consider the supplied local metric

    g=-N(x,y)^2 dt^2+dx^2+dy^2+dz^2,
    N=1+x^2+y^3,

in a small neighborhood of x=y=1 where N>0. Coordinates and coefficients
are free mathematical witness data, not a physical scale or preferred observer.
For this static lapse geometry,

    Ric_tt=N(N_xx+N_yy), Ric_ij=-N_ij/N, R=-2(N_xx+N_yy)/N.

Consequently

    j_x=-16x(3y+1)/N^3,
    j_y=72y(x^2-2y^3-y^2+1)/N^3,
    (partial_x j_y-partial_y j_x)|_(1,1)=16/3 != 0.

No scalar trace q, even an otherwise unrestricted smooth scalar, makes this S
conserved near that event. This refutes automatic trace completion from natural
single-metric geometry alone. It is not a no-go result for UDT or its admissible
responses. A familiar time-only homogeneous example would miss this curl test:
a time-only one-form is locally closed. Full metric-data recomputation and a
nonzero wrong-claim control are required by the check plan.

Even the simpler E=Ric is not identically conserved on metrics with varying R,
although it has the same trace-free part as G. This demonstrates why response
representative and reciprocal equation cannot be conflated. E=R g makes DDR
vacuous for every metric while div E=dR need not vanish; it illustrates the
degenerate case, not an admissible nontrivial UDT response.

## 5. What does and does not follow about an action

For an assumed differentiable local metric-only diffeomorphism-invariant action,
define E by delta I=integral sqrt(|g|) E_ab delta g^ab for compactly supported
variations. A compactly supported diffeomorphism gives delta g^ab=-2nabla^(a X^b).
Integrating by parts and using arbitrary X proves div E=0 off shell. This is
Noether's geometric identity. It needs the action and its metric-only variational
meaning; covariance of a tensor expression alone does not supply it. Extra
independent fields would add their Euler expressions to the Noether identity;
they are excluded here rather than silently put on shell.

Conversely, the general inverse problem asks whether the linearization of the
proper tensor-density Euler expression obeys formal self-adjointness (Helmholtz
conditions, including the volume/raising factors). Checking div E=0 alone is
not our proof of those conditions at arbitrary finite order. However, one must
not claim an action always requires an independent physical postulate:
Anderson and Pohjanpelto, Theorem 1 (arXiv:1202.5811), prove that symmetric
natural metric tensor-density operators of differential order at most three,
obeying the off-shell divergence identity, are locally variational. Under their
everywhere-smooth hypothesis, in dimension four a natural Lagrangian density
exists. Their result applies to fixed arbitrary signature. Conversion is
T^ab=sqrt(|g|) E^ab, whose density divergence is sqrt(|g|) nabla_b E^ab.
This is an external mathematical theorem used conditionally, not proved by our
finite symbolic checks. It selects neither a physical response nor a unique
action, and finite local jet sufficiency is not the order-at-most-three premise.

Lovelock's second-order natural symmetric divergence-free classification gives
the stronger Einstein-plus-metric form in four dimensions under its own full
smooth/natural metric-only hypotheses. This is an alternative conditional route;
it cannot be combined silently with unproved native derivative-order bounds.

## 6. Exact ownership and maximum conclusion

The constructive addition beyond RMS1/GRS1 is the local divergence-one-form
criterion, its explicit failure witness, and the qualified inverse-variational
route. The current sufficient Ricci class can be completed to a conserved,
variational representative without another arbitrary tensor shape, but that
class and physical identification remain conditional.

Current G351 conserved label measure is a different object from div E=0; its
conservation alone does not identify a stress tensor or UDT response. Neither
equivalence, local metric sufficiency, the pair determinant nor the positional-c
interpretation supplies the off-shell identity in the arguments examined here.
This is an audited unclosed join, not a proof that no consequence of current
UDT could ever close it, or that another physical postulate is necessary.

The next physical question is which metric variation/observable is represented
by S and why its divergence must admit the required scalar primitive. A supplied
action would be a conditional comparison unless natively justified. No response
or source is introduced to obtain a desired equation; no successor is dispatched.
