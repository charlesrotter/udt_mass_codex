# FCL1 source-first operational-clock and premise-fidelity review

Status: SOURCE-FIRST CONDITIONAL ASSESSMENT, sealed before candidate exposure.
Reviewer: `/root/fcl_fidelity`, a fresh separate agent context using the inherited
parent model. No different-model or human-review claim. This report supplies an
independent mathematical argument; it is not a scientific adoption or canon act.

## Authority, exposure and orientation

The reviewer independently observed branch `grok`, HEAD
`4d9f202f8e557c8714af1d284ecaf1ee35d67ebb`, and the dirty-name listing. Continuing
top-level startup is attributed to the parent, including its reported full406
PASS in405.626s, normal PASS and57maintenance PASS. Those checks were not rerun
here. BASELINE records76 preexisting unrelated untracked names, which are
preserved. No protected file content was opened or hashed. No checkout, fetch,
commit or repository-wide mutation was performed by this reviewer.

Read on disk: AGENTS.md; CLAUDE.md's How we work, DRIVER TRIGGERS and Repo
discipline; the triggered no-shortcuts, completeness-map and verifier-before-record
protocols; FCL1 WORK_ORDER and BASELINE; CPW1 SUCCESSOR_SCOPE; central R6,
R16FCW and R16CPW. The bounded central-file extraction also displayed adjacent
existing text; no parent FCL1 candidate, control implementation, control output,
or sibling report was read. Exact core-source hashes matched BASELINE. Detailed
parent startup evidence is attributed rather than independently reconstructed.

The honest incoming result is CPW1's exact conformal clock bookkeeping. Receiver
convergence was its open gate. RG is supplied and UNADOPTED; no native field,
action or source equation enters. The authorized next action is a pointwise
conditional free-clock derivation, not physical RG admission.

## Source-first conclusion

The stated local hypotheses suffice for the requested pointwise receiver limit.
For the supplied future geodesic approaching the specified regular spacelike
boundary point, the physical unit tangent divided by Omega tends to the future
unit conformal normal at that point. The needed velocity bound can be derived;
it need not be assumed. The specified regular interior-emitter null family then
gives a finite positive *rescaled* endpoint frequency and

    Omega_o Z -> C > 0.

With physical emission frequency normalized to1, physical received frequency
itself tends to zero. Describing it as a positive finite physical endpoint
frequency would be incorrect. The endpoint is a limiting event in the supplied
completion, not an actual finite-proper-time reception.

This is an independent proposed proof for later comparison with the candidate,
not a verdict on an unseen candidate.

## Independent local receiver proof

Use signature(-+++), put r=Omega, and denote the conformal metric by b. The
assumed boundary endpoint permits a sufficiently small relatively compact
coordinate neighborhood and a final tail of the actual receiver inside it.
Continuity gives timelike dr throughout a smaller collar. Define

    h = sqrt(-b^{-1}(dr,dr)),       n = grad_b(r)/h.

Choose the stipulated future side, so n is future and n(r)=-h. On the compact
closure, h has positive lower and finite upper bounds. The C3 inputs imply that
n and its first covariant derivative are continuous and bounded. These bounds
follow from the admitted local geometry; they are not physical numerical inputs
or an extra compact-population assumption.

For the physical unit geodesic tangent u let v=u/r. Then b(v,v)=-1. Independently
substituting g=r^-2 b into metricity and the torsion-free connection gives

    nabla^g_X Y = nabla^b_X Y - X(log r)Y - Y(log r)X
                 + b(X,Y)grad_b(log r).

Consequently nabla^g_u u=0 is exactly

    nabla^b_v v = [v(r)v + grad_b(r)]/r.

Decompose v=gamma n+w with b(n,w)=0, gamma=-b(v,n)>=1, and
q=b(w,w)=gamma^2-1. Since v(r)=-h gamma<0, r is a valid decreasing parameter
on the final tail; this follows without a velocity bound. Write

    Q = b(v,nabla^b_v n).

Differentiating gamma along v, then dividing by v(r), gives the exact identities

    v(gamma) = (h/r)(1-gamma^2)-Q,
    dgamma/dr = (gamma^2-1)/(r gamma) + Q/(h gamma),
    d(log gamma)/dr = (1-gamma^-2)/r + Q/(h gamma^2).

To justify the crucial Q bound, use the auxiliary positive metric
H=b+2 n_flat tensor n_flat. H(v,v)=2gamma^2-1<=2gamma^2, and the continuous
bilinear tensor (X,Y)->b(X,nabla^b_Y n) has bounded H norm on the compact
collar. Thus |Q|<=C gamma^2. With h>=h_min, for a geometry-dependent K,

    d(log gamma)/dr >= -K.

Integrating with the correct reversed orientation, from r to r0>r, yields

    gamma(r) <= gamma(r0) exp(K(r0-r)).

The initial value here is a finite tangent at an actual interior point r0 of
the supplied smooth geodesic, not a uniform preparation bound. No statement
about geodesic existence before this tail is being added.

This proves bounded gamma. Hence |2Q/h|<=D for a finite constant on the tail.
The exact equation for q is

    dq/dr = 2q/r + 2Q/h,
    d(q/r^2)/dr = 2Q/(h r^2).

Integrating again from r to r0 gives

    0 <= q(r) <= q(r0)(r/r0)^2 + D r(1-r/r0).

Therefore gamma->1 and w->0 in any fixed local auxiliary norm. Since the
curve approaches the supplied endpoint and n is continuous,

    v = u/Omega -> n_*.

This proof uses a deliberately sufficient O(sqrt(r)) estimate for w; it does
not claim that rate is sharp. An O(r log r) refinement is unnecessary to the
requested result. In particular, the proof does not turn two-sided bounds into
a limit without the q equation.

Also dr/dtau=u(r)=-r h gamma. Bounded h gamma makes the remaining physical
proper time infinite; its limiting positive value h_* gives
log r / tau -> -h_* after an arbitrary finite proper-time origin. This is a
conditional endpoint asymptote, not a selected cosmological scale.

## Independent operational clock relation and endpoint limit

Let k be a physical affine null tangent on one ray, and J the connecting
variation for emission proper-time label s. Commuting variation parameters,
metricity, affine propagation and the null constraint imply

    d[g(k,J)]/dlambda = g(k,nabla_J k) = (1/2)J[g(k,k)] = 0.

If endpoint affine coordinates vary with s, actual endpoint derivatives differ
from J by multiples of k; their contractions with k are the same because k is
null. Thus at emission and reception the constant contractions are -omega_e
and -Z omega_o, respectively, where Z=d tau_o/ds. Hence

    Z = omega_e/omega_o > 0.

This handles a varying affine interval and does not silently require a common
fixed affine length for all rays. The ratio is unchanged under any positive
raywise constant affine rescaling. It requires the supplied smooth branch;
caustics and branch switches are not covered by asserting this formula.

If kbar is affine null for b, direct substitution in the same connection
formula gives k=r^2 kbar affine for g. Hence

    omega = -g(k,u) = r[-b(kbar,v)] = r omegabar.

Start with the stipulated regular nonzero future conformal affine data. At the
interior emission limit, r_e>0 and the ordinary emitter tangent is finite and
future timelike. Therefore A_e=r_e[-b(kbar_e,v_e)] has a finite strictly
positive limit. Rescaling each entire ray by a(s)=1/A_e(s) enforces physical
omega_e=1, with a finite positive limiting rescaling. It preserves a nonzero
finite future endpoint kbar_* under the supplied regular-extension hypothesis.

For this normalized family, the receiver result proves

    omegabar_o -> B_* = -b_*(kbar_*,n_*) in (0,infinity),
    omega_o = r_o omegabar_o -> 0,
    r_o Z = 1/omegabar_o -> 1/B_* > 0.

Positivity follows from the contraction of a nonzero future null vector with
a future unit timelike vector at the same regular endpoint. The required
nonzero limiting null vector is a supplied ray-family hypothesis. It is not
deduced from receiver dynamics or pointwise nullness alone.

## Gauge, controls and possible false promotions

For a regular positive gauge factor a(x), set r'=a r and b'=a^2 b. Holding the
physical u and k fixed gives v'=v/a, kbar'=kbar/a^2 and
omegabar'=omegabar/a. Thus Z is invariant, but (r' Z)_*=a_* C. The residue in
the defining function is not itself gauge invariant. The limiting normal
transforms consistently to n'_*=n_*/a_*. These statements do not attach r to a
measured separation or to X_max.

An exact analytic comparison is b=Minkowski with r=-eta on eta<0. Conserved
physical spatial covector P gives v_spatial=r P and
gamma=sqrt(1+r^2|P|^2), directly verifying the convergence for arbitrary fixed
finite P. This calculation is a comparison object, not a native solution or a
numerical control. Allowing P to depend unboundedly on the final r would change
the quantifier to a population and defeats this pointwise argument.

The CPW1 rapidity cancellation rho=log r is not a geodesic rescue. For the same
flat conformal metric, a geodesic's rapidity obeys v(rho)=-sinh(rho)/r, whereas
rho=log r gives v(rho)=-cosh(rho)/r; equality would require cosh rho=sinh rho.
The assumed unit norm alone therefore cannot replace the geodesic hypothesis.

No implication is claimed for a null conformal boundary, vanishing dr,
nonsmooth/degenerate completion, accelerated receiver, absent endpoint limit,
nonregular or zero-limit affine data, boundary emitter, caustic or global
existence problem. FCW1's beta2 counterexample violates the current nonzero
timelike-gradient premise; its interior-bump nonuniqueness remains unaffected.

This is one receiver with varying emissions approaching an interior limit. It
does not establish uniformity over receiver populations, a fixed-emission
distance law, echo access, selection of a geometry, a light-energy mechanism,
an anomalous proper clock, an Einstein/action/source equation, physical RG
admission, or a need for UDT to adopt an additional premise. The boundary
normal is part of the supplied completion's mathematical description, not an
imposed finite-time preferred observer population.

## Verification character and omissions

The load-bearing relations above were independently rederived and their signs,
parameter orientation, positivity, normalization and quantifiers checked from
the sources. No parent implementation or numerical output was reused. No
control script was run; the optional reviewer script budget is unused.
Consequently this report makes no floating-point, residual, convergence-test,
catch-proof or empirical claim. Existing source packages, premise verifier and
maintenance suites were not replayed by this reviewer. Their parent results
remain separately attributed. Later candidate-exposed review must compare the
actual proof and public wording with these requirements and report any defect.

Conditional physical-fidelity ceiling: VERIFIED-WITH-CAVEATS for this source-first
argument's stated mathematical scope only. RG remains UNADOPTED, and the
candidate is still unseen.
