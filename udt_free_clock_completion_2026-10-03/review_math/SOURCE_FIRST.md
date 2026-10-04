# FCL1 mathematical review — source-first reconstruction

Status: independent conditional argument, sealed before exposure to the parent
candidate, its code/results, or the sibling review. This is a review artifact,
not scientific promotion, physical adoption, or canon.

Reviewer context: `/root/fcl_math`, fresh separate subagent context, inherited
model (no different-model or human-review claim). Parent startup and full-406/
maintenance checks are attributed, not independently rerun here. I independently
observed branch `grok`, HEAD `4d9f202f8e557c8714af1d284ecaf1ee35d67ebb`, and
the status containing the new FCL1 package plus preserved unrelated untracked
work. No protected payload was opened or hashed. No repository-wide mutation,
fetch, switch, or test was performed.

Sources opened: AGENTS.md; CLAUDE.md's working, driver, review and repo rules;
the triggered no-shortcuts, completeness-map and verifier-before-record skill
files; FCL1 WORK_ORDER.md and scalar/key metadata in BASELINE.json; CPW1
SUCCESSOR_SCOPE.md; UDT_DEVELOPMENT.md R6, R16FCW, R16CPW (the bounded excerpt
also exposed the adjacent end of CD2 and R16 calibration). The four source hashes
for AGENTS, CLAUDE, UDT_DEVELOPMENT and SUCCESSOR_SCOPE match BASELINE. No parent
FCL1 proof, control script, output or candidate verdict was read.

## Scope and anticipated strongest conclusion

For each one of the specified physical unit timelike geodesics, the supplied
C3 regular spacelike conformal completion implies

    u/Omega -> n_p,
    n = grad_bar(Omega)/alpha, alpha = sqrt(-gbar^-1(dOmega,dOmega)).

Here n is future directed because this is the stipulated future boundary: Omega
decreases along future timelike curves near it. Thus the rescaled tangent does
not merely have a finite timelike limit; it approaches the conformal unit normal
at the specified boundary endpoint p. The proof below derives its boost bound.
It needs no Einstein equation or constant lapse, and supplies no native RG
admission, geometric selection, physical light law or population theorem.

For the specified ray family with the supplied regular affine-data extensions,
normalized at emission to physical frequency 1, this gives

    Omega_o Z -> 1 / [-gbar_p(kbar_*,n_p)] in (0,infinity).

The asterisk denotes the consistently normalized limiting conformal ray tangent
at p. The existence/nonzero nature of that null limit is a supplied branch
hypothesis; the receiver limit is derived. This is varying emissions to one
receiver, not fixed emission to a receiver population.

## Local bounds follow from the endpoint premise

Take a coordinate neighborhood of p small enough that dOmega remains timelike,
the metric remains nondegenerate, and Omega is a regular defining function.
Choose a smaller coordinate neighborhood whose closure K is compact inside the
first. By convergence of the receiver to p, its final tail lies in K. Shrinking
once more if needed gives positive constants alpha_min, alpha_max with

    0 < alpha_min <= alpha <= alpha_max < infinity on K.

The future normal n is C2. Define the positive definite auxiliary metric

    H = gbar + 2 n_flat tensor n_flat.

Its eigenvalues and those of its inverse are bounded on K, and the coefficients
of gbar and nabla_bar n are bounded. This uses compactness and continuity only.
It implies a constant C0, independent of the receiver velocity, such that

    |gbar(V,nabla_bar_V n)| <= C0 H(V,V).

All these constants can depend on the supplied geometry and the final collar.
There is no uniform statement over geometries or receivers. This compact tail
is a consequence of the specified endpoint, not an extra global collar premise.
The chart, H, and unit convention c_E=1 are mathematical controls. The completion
and clock/branch restrictions are supplied conditional choices; arbitrary
nonuniform geometry remains free-and-explored within RG. No physical value is
pinned by habit or by an unstated theory.

## Independent conformal-geodesic calculation

Write r=Omega and u=dq/dtau with g(u,u)=-1 and nabla_g_u u=0. Define conformal
proper time s by ds/dtau=r and v=dq/ds=u/r. Then gbar(v,v)=-1. With l=log r,
the exact conformal connection difference is

    nabla_g_X Y = nabla_bar_X Y - X(l)Y - Y(l)X
                 + gbar(X,Y) grad_bar l.

Substituting u=r v and the unit norm gives, without approximation,

    nabla_bar_v v = v(log r) v + grad_bar(log r).

Define E=-gbar(v,n)>=1. Since grad_bar r=alpha n,

    v(r)=-alpha E,
    nabla_bar_v v = (alpha/r)(n-E v).

In particular r strictly decreases, so it is a legitimate parameter on the
final tail. Set T=gbar(v,nabla_bar_v n). Direct differentiation yields

    dE/ds = alpha(1-E^2)/r - T,
    dE/dr = (E^2-1)/(r E) + T/(alpha E).                 (1)

Because H(v,v)=2E^2-1<=2E^2, compactness gives |T|<=2C0 E^2. Thus for
C=2C0/alpha_min,

    d(log E)/dr >= (1-E^-2)/r - C >= -C.

Integrating in the actual direction r<r0 is important:

    log E(r0)-log E(r) >= -C(r0-r),
    1 <= E(r) <= E(r0) exp[C(r0-r)] <= M < infinity.    (2)

Finite interior initial timelike data imply finite E(r0) at any regular point
on the stipulated final tail. No bound at the boundary has been assumed.

Set Q=E^2-1>=0. Equation (1) becomes

    dQ/dr = 2Q/r + F(r),   F=2T/alpha,   |F|<=D,        (3)

where D=4C0 M^2/alpha_min is finite by (2). Variation of constants gives

    Q(r) = (r/r0)^2 Q(r0) - r^2 integral_r^r0 F(t)/t^2 dt,
    0 <= Q(r) <= (r/r0)^2 Q(r0) + D(r-r^2/r0) = O(r).  (4)

Consequently E->1. Decompose v=E n+w with gbar(w,n)=0. Then
gbar(w,w)=Q and H(w,w)=Q. Since n(q(r))->n_p, (4) gives v->n_p in any regular
coordinate trivialization. This proves boundedness and convergence from the
geodesic equation with the full, variable-lapse geometry present.

This O(sqrt(r)) bound on the spatial component is sufficient, not claimed
optimal. The proof does not require differentiating sqrt(Q) at its zeros or
asserting convergence from a merely bounded velocity.

## Proper-time and parameter checks

The exact physical proper-time rate is

    dr/dtau = -r alpha E,
    tau(r)-tau(r0) = integral_r^r0 dt/[t alpha(q(t)) E(t)].

The positive upper and lower bounds on alpha and E prove divergence of tau as
r approaches zero. No endpoint reception at finite proper time is created.
Conformal proper time has finite remaining length since |dr/ds|>=alpha_min.

There is also a source-preserving optional refinement: because

    dq/dr = -v/(alpha E)

has bounded coordinate components on the compact tail, q(r)-p=O(r).
Since alpha is C1 and E-1=Q/(E+1)=O(r), alpha(q(r))E(r)=alpha_p+O(r).
Thus tau(r)+(1/alpha_p)log r has a finite limit. This is a conditional
asymptotic proper-time relation, not a physical selected scale or distance law.
The principal free-clock result does not need the refinement.

## Clock factors: actual emitter and null data

For any conformally affine future null tangent ell, k=r^2 ell is physically
affine. Its physical frequency at an endpoint is

    omega = -g(k,u) = -gbar(ell,u) = r[-gbar(ell,v)].

Let the supplied regularly extended family have limits ell_e*,ell_o*, both
future, null, finite, nonzero in the regular metric. The actual emitter's
regular compact proper-time interval away from r=0 supplies a finite timelike
u_e* and r_e*>0. Hence

    A(s)=-gbar_e(ell_e,u_e) -> A*>0.

Positivity uses the elementary Lorentz inner-product fact: in an orthonormal
frame of a future unit timelike vector, a nonzero future null vector has
strictly positive time component and its negative inner product is positive.
No extra rest population or preferred emitter was substituted.

Rescale each ray by the positive constant 1/A(s), the same constant all along
that ray, to obtain kbar=ell/A(s) and physical omega_e=1. Because A(s)->A*>0,
this rescaling preserves the supplied finite nonzero endpoint limits. At the
receiver,

    B(s)=-gbar_o(kbar_o,v_o) -> B*=-gbar_p(kbar_*,n_p)>0,
    omega_o=r_o B(s),  Z=omega_e/omega_o=1/[r_o B(s)].

Therefore r_o Z->1/B* in (0,infinity). The R6 null-variation argument gives
Z=d tau_o/d tau_e on the stipulated smooth regular correspondence, so this
frequency statement is the actual clock statement at source scope. The emitter
does not need to be geodesic. Smooth family/affine-data regularity must actually
include the limiting reception and emission endpoints; uniqueness or a merely
bounded set of ray directions alone would not ensure a limiting B*.

## Gauge check and a useful variable-lapse adversarial control

For a smooth finite positive gauge a, set r'=a r and gbar'=a^2 gbar. Then
v'=u/r'=v/a and at the boundary n'_p=n_p/a_p. Consistent conformal affine
tangents satisfy kbar'=a^-2 kbar, so B'=B/a, with the endpoint quantities
evaluated in their respective metrics. The physical Z is unchanged and
r'_o Z->a_p/B*. Thus existence and positive finiteness are stable under these
regular gauges, while the numerical residue is gauge dependent. It is not an
invariant distance pole or an identification with X_max.

A potential overstrong rate must be avoided. For the exact control

    gbar = -(1+b x)^2 dr^2 + dx^2 + dy^2 + dz^2, r>0,

on a small regular collar with N=1+b x>0, take a future geodesic with motion only
in x. Write v^r=-E/N, v^x=Y, E=sqrt(1+Y^2). The physical spatial momentum is
p_x=Y/r. Its exact Euler-Lagrange equation gives

    dp_x/dtau = -b E^2/N,
    dr/dtau=-r E/N,
    dY/dr=Y/r+b E.

Hence Y/r=Y(r0)/r0+b integral_r0^r E(t)/t dt. The estimate (4) gives
E=1+O(r), so for b!=0,

    Y=b r log r+O(r).

This remains consistent with v->n_p but need not satisfy Y=O(r). It is an
analytic variable-lapse diagnostic, not an executed numerical control or a
native admitted solution. The family can be confined to a regular collar by
taking a sufficiently short final segment; dx/dr=-N Y/E is bounded and
integrable. The proof above makes no incorrect constant-lapse rate claim.

## Review position, omissions and next stage

Source-first conclusion: no counterexample found to the specified conditional
limit; equations (1)-(4) supply an independent argument for it without assuming
bounded rescaled velocity. The nontrivial step is the correctly oriented
integration of the E inequality, followed by the forced Q equation. Actual
emitter/affine-data regularity supplies the other clock factor.

Candidate review must still inspect every load-bearing step, signs, norms,
compactness justification, proper-time parameter, gauge scaling and null-family
normalization. In particular, check for an implicit boundedness assumption,
an unjustified constant lapse, a claimed O(r) tangential rate, or conversion to
a fixed-emission distance curve. Source and premise labels must stay conditional.

No computational control or code was required for this analytic reconstruction;
none was run. Full registry, maintenance, earlier source tests, population and
global-caustic questions were not independently replayed. The parent owns its
closure checks; their attributed results are not my fresh verification. This
proof covers neither existence of the stipulated conformal completion/receiver/
ray family nor a quantitative bound uniform across arbitrary data. It does not
establish physical RG, a field/source/action law, X_max realization, scale
selection, microscopic light physics or a complete-postulate insufficiency.

Seal this file, retain its hash, and await the parent's frozen candidate for an
exposed adversarial review. The source-first seal records byte correspondence
and exposure sequence, not truth or independent chronology by itself.
