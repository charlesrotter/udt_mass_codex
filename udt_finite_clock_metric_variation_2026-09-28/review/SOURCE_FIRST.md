# FCV1 independent source-first reconstruction, sealed before direct review

2026-09-28; reviewer `/root/fcv1_review`. Scope, exposure, startup attribution,
runtime uncertainty and resource controls are in SOURCE_FIRST_PLAN.md. No FCV1
candidate/code/results were read before this document and its seal. The dispatch
did reveal the intended world-function method and interior-perturbation idea;
independent origination of those ideas is not claimed. The derivation and code
below were constructed without the author's new derivation or implementation.

## Scientific premises and status

G220 owns the conditional supplied-regular-null-query relation
`r=d tau_B/d tau_A=(k_A.U_A)/(k_B.U_B)>0`. Its same-correspondence completed
clock leg is a compatibility identity, not a full G176 pair construction.
FSL1 is reviewed conditional/unpromoted and retains the intermediate ray in
composition. RMS1 establishes why holding a raw clock leg fixed supplies only
a query-dependent evaluator derivative; that calculation cannot substitute for
varying the actual query here. G310's all-plane algebra gives TF(E)=0 for a
specified symmetric E. The exact G310/G312 registry rows and current G312
authority override historical unadopted or stronger-GR language: DDR and local
metric sufficiency are owner-provisional, GR is FILTER ONLY, physical E remains
unidentified, and the full Ricci-response class is conditional. No new physical
premise or native admission is used. No current source status is strengthened.

## Independent general derivation

Take a smooth Lorentz4 family g_e with h=partial_e g at zero, two smooth
timelike worldline families z_A,e(s), z_B,e(t), and a smooth regular selected
geodesic branch for nearby endpoint pairs. A convex-normal neighborhood is a
sufficient domain. Signature (-+++) and c_E=1 are conventions. All metric
components and observer displacements are retained. Labels s,t and worldline
families are supplied query data, not preferred physical observers.

Write v_i=partial_label z_i, a_i=sqrt(-g(v_i,v_i))>0, and

    F_e(s,t)=sigma_e(z_A,e(s),z_B,e(t)),
    F_e(s,T_e(s))=0,  F_t != 0,
    b=T_s=-F_s/F_t>0,  r=(a_B/a_A)b.

The physical positivity assumes the declared future branch and future clock
orientations. Every expression below is evaluated at e=0,t=T(s) unless stated.
Let xi_i=partial_e z_i at fixed labels. Parametrize the unperturbed affine
geodesic by lambda in [0,1], with k=dot gamma. World-function first variation is

    f := partial_e F|s,t
       = J[h]+p_A.xi_A+p_B.xi_B,
    J[h]=(1/2) integral_0^1 h(k,k) d lambda,
    p_A=-g(k_A,.),  p_B=g(k_B,.).

Proof: sigma equals the geodesic energy action on the fixed unit parameter
interval. Its path variation integrates by parts into the endpoint terms plus
an Euler-Lagrange term that vanishes on the affine geodesic. This remains valid
on the null branch; the zero value of the on-shell action does not make its
metric derivative zero. No field equation or physical variational action is
introduced: this is a mathematical method for geodesic incidence.

The arrival displacement and endpoint clock-rate variations are

    eta := partial_e T|s = -f/F_t,
    nu_i := partial_e log(a_i)|label
          = -[h(v_i,v_i)+2g(nabla_v_i xi_i,v_i)]/(2 a_i^2).

Commuting the smooth label/metric derivatives and differentiating log(r) gives

    q_label := partial_e log(r_e(s))|s
             = nu_B - nu_A + eta partial_t log(a_B) + eta_s/T_s.       (SF1)

Here eta_s is the derivative along the baseline incidence family, not a
fixed-endpoint derivative. It differentiates J, endpoint covectors and endpoint
displacements as the emission label changes. This includes the varied ray and
arrival event. A separately solved Jacobi equation is an alternative means of
computing those derivatives, not an extra additive term omitted by (SF1).
For the depth Phi=-log r, partial_e Phi=-q_label.

The equation is exact first variation; it is neither a finite-perturbation
estimate nor global stability. Required differentiability is enough to form
these mixed derivatives and maintain the smooth nondegenerate branch.

**Evaluation protocol matters.** If instead one fixes the numerical source
proper time tau_A across the metric family, with its clock origin declared,
the source coordinate label shifts by

    kappa_A = -[partial_e tau_A,e(s)|s]/a_A(s),
    q_proper = q_label + kappa_A partial_s log(r).                    (SF2)

One may take s to be source proper time separately in each metric family. Then
a_A=1 and nu_A=0 identically, but the resulting source worldline displacement
xi_A already includes the required reparametrization. One must not both add
(SF2) and encode the same relocation in xi_A.

## Gauge covariance check

For g_e=phi_e^*g and z_i,e=phi_e^{-1}z_i, h=L_X g, xi_i=-X. Affine geodesic
motion gives J[L_Xg]=[g(X,k)]_A^B, exactly canceled by endpoint displacements.
Also nu_i=0, so eta=0 and q_label=0. Holding coordinate observers fixed while
changing the metric by L_Xg specifies a different physical query family; its
possible nonzero response does not violate covariance. The independent exact
test takes Minkowski g, X=t^2 partial_t, unit null chord, and finds both
incidence and clock-rate cancellation. Removing endpoint motion fails.

## Reciprocal inversion is an identity, not stationarity

Use source and target proper clocks with declared origins, and write the
arrival map R_e(tau), r_e=R'_e. Its inverse S_e obeys

    S_e(R_e(tau))=tau,
    S'_e(R_e(tau)) r_e(tau)=1.

At the *moving paired target argument*, the total variation of log S'_e is
-q_proper. At a *fixed target proper-time argument*, it is instead

    partial_e log S'_e(tau_B)
      = -q_proper(tau_A) + [partial_e R_e(tau_A)/r_e(tau_A)]
                                  partial_tau_A log r_e(tau_A).     (SF3)

The chain term follows from partial_e S=-partial_e R/r. An algebra check with
R_e(s)=s^2+e*s, s>0, gives q=1/(2s), while the inverse fixed-target log-slope
variation is zero: the argument-shift term cancels it. This is realizable as
a supplied flat timelike query: null coordinates u=s,
v=v0+4s^3/3+2e*s^2+e^2*s on B have proper-clock derivative 2s+e>0;
choose v0 so B is to the right of the emitting inertial worldline on a bounded
interval. Thus the nonlinear-map check need not rely on an inadmissible clock.

Composition likewise differentiates both factors and the changed intermediate
arrival argument. These statements hold for every smooth increasing regular
query map. Demanding them does not restrict a metric. A later causal return
has different events and branch data and is not this inverse map.

## Explicit controls that challenge the direct E identification

For a rightward chord x in [0,1], use the supplied Lorentz metric

    g_e=-dt^2+(1+e*t*f(x))^2 dx^2+dy^2+dz^2,
    f=x^2(1-x)^2,

on a bounded domain where 1+e*t*f>0, with coordinate-static observers x=0,1.
Their proper time equals t. Null propagation satisfies dt/dx=1+e*t*f(x).
Differentiating with respect to emission time s solves a homogeneous linear
ODE exactly, so

    r_e=exp(e integral_0^1 f dx)=exp(e/30),
    eta=s/30+1/60,  partial_e log r=1/30.

The endpoint metric perturbations vanish; the observed variation is a finite
ray effect. Independently, the world-function integral gives the same eta.
For the stronger locality statement choose a smooth nonnegative bump f supported
strictly inside (0,1), with nonzero integral. The same ODE proof gives a nonzero
ratio variation even though h and every derivative vanish near either endpoint.
The bump proof is analytic; the exact polynomial control does not pretend to
have compact interior support or endpoint-jet vanishing of all orders.

Therefore this finite observable's derivative cannot be identified with the
variation of a metric-only finite-jet object at either endpoint. More generally
it depends on the observer/branch/separation query and is a linear functional
of a field perturbation, representable using distributions on the ray and
endpoints. That is not automatically DDR's physical local symmetric rank-two
response. This does not deny the possibility of local integral representations
with query-dependent kernels or a separately justified reconstruction procedure.

Conversely, for conformal g_e=exp(2e*w)eta, fixed static observers have unchanged
coordinate arrival t_B=s+1 but q=w(B)-w(A). Conformal perturbations supported
strictly inside the ray give q=0 despite changing interior geometry. Thus neither
one clock ratio nor its reciprocal supplies general metric reconstruction.

The homothety control g_e=exp(2e)*(1+t)^2 eta makes a further protocol issue
explicit: r=(s+2)/(s+1) is unchanged at fixed coordinate source label, but at
fixed source proper time (origin t=0) its log-ratio response is
s/[2(s+1)^2]. Homothety invariance of the comparison requires transporting its
event protocol. It cannot be asserted across mismatched anchoring conventions.

## Source-first landing and verification limits

The direct join is unsupported: inverse/composition reciprocity makes the
derivative of an identity vanish for all regular metrics; it does not impose
zero response to every G310 reciprocal shape tangent. Treating the derivative
of that identity as E would produce a vacuous zero response, not a nondegenerate
metric law. The actual single-query derivative is nontrivial but of the wrong
unjustified locality/query type for direct physical E identification. No claim
that all possible response reconstruction is impossible, that UDT cannot close,
or that a new postulate is necessary follows. Actual measured comparison data
could constrain geometry; reciprocity alone supplies no such data or dynamics.

Independent Python3.10.12/SymPy1.13.1 exact arithmetic ran successfully under
the declared 60-second/512-MiB capture: 18 checks including four explicitly
wrong simplifications rejected, 0.309 seconds, 49,724 KiB peak RSS. These finite
checks support controls, not the generic theorem. Source packages were not
broadly replayed; full premise audit and operational preservation remain the
parent's closure duties. No producer code, numerical geodesic solve, GPU,
floating-point comparison, formal proof assistant, human or demonstrated
different-model review was used. Source hashes and actual command metadata
are retained separately. Direct candidate audit has not yet occurred.
