# OEV1 math/numerics source-first reconstruction

Status: independent source-first argument and proposed numerical checks; no new
OEV1 implementation or outcomes exposed and no numerical experiment executed.
This is a scoped reviewer record, not a maintained scientific development.

## Context, exposure and authority

Actual reviewer context: `/root/oev_math`, separate context from the constructing
parent and other reviewer. Same inherited model; exact model revision unexposed.
Fresh context is not different-model, human or formal review. Parent startup is
attributed to BASELINE.json and the dispatch, including its same-session PRT1
406-row/57-test receipts; it is not independently rerun or relabeled my startup.
I independently observed branch `grok`, HEAD
`515513321e145eb4b0964f256f382697b08fa363`, and status with existing untracked
names plus the authorized new package. No protected payload was read or hashed.
Remote freshness is attributed to the parent rather than independently claimed.

Reads before sealing: AGENTS.md; OEV1 WORK_ORDER.md and BASELINE.json; CLAUDE.md
How we work, DRIVER TRIGGERS and Repo discipline; triggered no-shortcuts,
completeness-map and verifier-before-record protocols; UDT_DEVELOPMENT.md exact
R6, R7 and R8PRT passages; PRT1 INITIAL_CANDIDATE.md, PRECISION.md,
REVIEWED_RESULT.md and STEPS_4_5_HANDOFF.md. Thus old arguments and verdicts are
exposed. Source-first means before the new candidate, not blind to prior proofs.
File hashes in SOURCE_FIRST_SEAL.json pin these sources; central passage ranges
are recorded because its full file was not substantively reviewed. No sibling
new research/review and no future parent code/results have been read.

Orientation: the honest claim is conditional metric/ordinary-clock/null
evaluation on supplied controls. Native event/path-to-depth assignment remains
OPEN; no N/C assignment or scale is adopted. The bounded next action is derive
the evaluator independently, then check the parent's frozen finite workload by
an independent high-precision implementation. Ordinary R6 readout is available;
native metric evolution remains a separate entry gate.

## Original metric and its affine equations

Use the supplied four-dimensional metric

    g = -dt^2 + a(t)^2 (dx^2 + dy^2 + dz^2),   a(t)>0.

The unquotiented Cartesian radial slice y=z=0 is invariant under geodesic
evolution with zero transverse velocity. Restriction to it is exact for this
query, not a census of general clocks, directions or perturbed geometries.
The only required connection coefficients on the slice follow directly from
the metric inverse and first derivatives:

    Gamma^t_xx = a a',     Gamma^x_tx = Gamma^x_xt = a'/a.

For future affine null state (t,x,T,X), with T=dt/dlambda and X=dx/dlambda,

    t' = T,               x' = X,
    T' = -a a' X^2,       X' = -2(a'/a) T X.                 (1)

Primes on T,X here mean affine derivatives; a' means da/dt. Differentiating
C=-T^2+a^2 X^2 using (1) gives C'=0. Differentiating J=a^2 X gives J'=0.
Choose the free affine normalization T_e=1 and future spatial sign s=+1 or -1:
X_e=s/a(t_e), J=s a(t_e). On the future null branch,

    T(t)=a(t_e)/a(t),    X(t)=s a(t_e)/a(t)^2.             (2)

These are independent first-integral consequences of the original equations.
Using a different positive affine normalization rescales T and X together and
cannot change a frequency ratio. A replacement of X' by -H T X or a sign flip
of T' violates (1), its first integrals, and the quadrature trajectory.

Coordinate-rest clocks have u=partial_t: g(u,u)=-1 and Gamma^a_tt=0, so their
proper time equals t up to an arbitrary origin and their proper acceleration is
zero. At preparation t=0 all three controls have a(0)=1 and a'(0)=0. Therefore
the straight spatial segment of coordinate length L is a spacelike geodesic
of proper length L and transports partial_t unchanged. The fixed histories
A=(t,0), B=(t,L) are exactly the stipulated parallel-prepared free clocks.

## Actual incidence, frequency and reverse/echo distinction

Dividing (2) gives dx/dt=s/a(t). Define eta'(t)=1/a(t). For a direct first ray
between the same fixed histories,

    eta(t_o)-eta(t_e)=L.                                  (3)

Changing t_e in (3) while keeping A and B fixed yields

    F'(t_e)=dt_o/dt_e=a(t_o)/a(t_e)>0.                    (4)

Proper-time arrival differentiation is therefore this same F'. At a comoving
endpoint omega=-g(k,u)=T, so (2) independently yields

    Z=omega_e/omega_o=T_e/T_o=a(t_o)/a(t_e)=F'(t_e).        (5)

Elapsed travel-time division t_o/t_e is undefined at preparation and never
supplies (4). The finite interval ratio [F(t_e+h)-F(t_e)]/h is an average of
F', not generally F'(t_e). Independent reverse first rays emitted at t=0 from
B obey the same arrival map only because x -> L-x is an isometry of these
supplied controls. Thus p_+=p_-=a(t_1), eta(t_1)=L. This is not inversion of
the same comparison, whose multiplier would be 1/p.

Immediate echo from the actual first receiver at t_1 uses a new future ray:
eta(t_2)=2L, q=a(t_2)/a(t_1). Its total echo map has derivative p q=a(t_2)
at t_e=0. Both first rays may exist while the echo does not. A numerical
implementation must not substitute q=p, q=1/p, or p_-=1/p.

## Domains and exact control anchors

The flat and quadratic controls have time domain R; the cubic control has
t>-1, with all evaluated first/echo flights starting at or near t=0 and moving
to the future. Coordinate domains are unquotiented R^3. Nearby negative
emission times must remain in the cubic domain and retain reception existence.

* Flat a=1: t_o=t_e+L, p=q=1, no finite future conformal horizon.
* Quadratic a=1+t^2: eta=arctan(t), L_*=pi/2 at t_e=0;
  t_1=tan(L), p=sec(L)^2 for 0<L<pi/2. Echo requires 2L<pi/2;
  q=sec(2L)^2/sec(L)^2. At or beyond the bound there is no finite reception.
* Cubic a=1+t^3: eta(t)=integral_0^t du/(1+u^3),
  L_*=2pi/(3 sqrt(3)) at t_e=0. Strict eta monotonicity gives a unique
  direct finite first reception exactly for 0<L<L_*. Echo requires 2L<L_*.

For arbitrary allowed t_e, replace L_* in the existence condition by
integral_(t_e)^infinity dt/a(t). Checking this for both finite-difference
perturbations matters near a horizon. The analytic statements are from the
supplied positive integrand and its exact tail; finite numerics cannot establish
the global horizon, asymptote, uniqueness or physical X_max.

The affine parameter itself has an independent anchor from d lambda/dt=a/a_e:

    lambda-lambda_e = [A(t)-A(t_e)]/a(t_e),
    A(t) = t                    (flat),
           t+t^3/3             (quadratic),
           t+t^4/4             (cubic).                   (6)

Thus every saved (lambda,t,x,T,X), not merely its endpoint, can be checked by
independent quadrature (3), polynomial (6), and first integrals (2). Monotonic
root inversion of (6) is also an independent full-trajectory construction.

At small positive L, local analytic inversion gives

    quadratic: log p=L^2+L^4/6+O(L^6),    2 log p/L^2 -> 2;
    cubic: log p=L^3+L^6/4+O(L^9),        2 log p/L^2 -> 0,
                                               log p/L^3 -> 1.

These are control identities. They do not supply a universal onset order.
At quadratic delta=pi/2-L ->0+, p~delta^-2. At cubic
delta=L_*-L ->0+, t~(2 delta)^-1/2 and p~(2 delta)^-3/2.
Their different pole exponents are already mathematical control properties,
not finite-sample conclusions and not native physical predictions.

## Conditioning and proposed independent checks

The incidence derivative with respect to distance is dt_o/dL=a(t_o), which
grows near either finite conformal horizon. Relative p sensitivity to an
incidence error dL is d log p=a'(t_o) dL. Arrival-time root errors and
quadrature errors must be propagated through these derivatives. For cubic
large-t work evaluate the tail or split the quadrature instead of subtracting
two nearly equal conformal integrals in float64. High precision is an anchor,
not a claim of interval-certified bounds unless enclosures are supplied.

Symmetric finite differences D_h=[F(h)-F(-h)]/(2h) have truncation
h^2 F'''(0)/6+O(h^4) on a smooth reception branch; subtractive endpoint error
contributes roughly epsilon_t/h. Here a'(0)=0 gives

    F'''(0)=a(t_1)*([a'(t_1)]^2+a(t_1)*a''(t_1)-a''(0)).

It vanishes in flat space; equals 6 t_1^2(1+t_1^2) for the quadratic control;
and equals (1+t_1^3)(6t_1+15t_1^4) for the cubic control. Close to the horizon
fixed h can both lose accuracy and leave the finite-reception domain. Compare
a finite-difference ladder with the frequency ratio, never just one h. An
exact formula copied into two columns is regression rather than this check.

If log p has absolute numerical error epsilon, extracting 2 log p/L^2
amplifies it by 2/L^2; the cubic normalized coefficient amplifies by 1/L^3.
Shrinking L without shrinking actual numerical error eventually worsens the
estimate. log1p helps only if its input p-1 has not already lost the signal.
Report finite errors and truncation separately, including noise-dominated
samples; a zero numerical value cannot refute a higher-order onset.

Once the parent freezes equations/code/matrix, an independently written
mpmath implementation will use direct metric quadrature and monotonic root
bracketing, with no imports of parent scientific code. Proposed strongest
useful checks, to be bound to the frozen matrix before execution:

1. Every accepted first/echo endpoint and saved trajectory: (2), (3), (6),
   incidence, future direction, null condition and finite-domain inequalities.
   Compare arrival times and frequency ratios to high-precision anchors.
2. Independent finite differences of the high-precision fixed-history arrival
   map and each parent's saved emission ladder; check convergence/truncation
   against (4), including high sensitivity near each horizon.
3. Flat exactness; quadratic closed form versus independent quadrature;
   cubic root/quadrature precision doubling or separated quadrature method.
4. Reverse first equality only at the actual reflected histories; echo
   q and total p*q versus first p, with a point whose first ray exists while
   immediate echo does not. Exact horizon/beyond-horizon classification must
   use the analytic domain rule rather than unsuccessful finite integration.
5. Small-L observed errors against the admitted orders, with amplification
   disclosed; finite samples neither prove asymptotics nor certify signs below
   their noise floor.
6. Deliberately corrupt a copied result's receive frequency, sign/direction,
   arrival incidence or affine parameter and require the appropriate independent
   guard to reject it. Mutations stay in reviewer-owned scratch artifacts.
7. Inspect original-equation residual logic for differentiation independence,
   units, tolerances and sampling; direct same-RHS reevaluation is not an
   independent residual. Inspect output/checkpoint/config/resource guards and
   retained failures, separating engineering regression from scientific checks.

Ceiling: a checked finite evaluator for these conditional supplied controls.
No field equation, native metric admission, positional attribution, source
content, observational fit, complete solution space or scientific promotion.

Execution is pending the parent's frozen workload. This source-first seal
does not assert that any of these proposed numerical checks already ran.
