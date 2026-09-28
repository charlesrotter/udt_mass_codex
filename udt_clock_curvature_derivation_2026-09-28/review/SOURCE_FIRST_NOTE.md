# CRD1 reviewer source-first derivation

Sealed source-first stage, 2026-09-28. Reviewer `/root/crd_review`.
This note predates candidate, author code/results, and CGW1 exposure. Source
versions and exposure are pinned separately. No scientific adoption is made.

## Scope and premises

Independently observed branch `grok`, HEAD
`653c9a5779eb6e2919d3103edb8ae2cb787dcb1f`; unrelated untracked/protected
payloads were visible in status and left untouched. Top-level startup/sync
are attributed to the parent as directed for this scoped review. The parent's
current premise verifier was still running when this note was composed; this
review does not claim its result.

G176 owns conditional completed-pair calibration `m=NL`, `Phi=-log N`
under its WORKING foundational clarification. G220 owns conditional supplied
regular null-query clock evaluation. G310 DDR is now OWNER_ADOPTED_PROVISIONAL,
not derived/canon; the original candidate-status sentence is superseded by
its adoption record. G312's current authority keeps GR FILTER ONLY and Local
Metric Sufficiency owner-provisional; the full response-class membership
route is UNCLOSED. No physical field equation or population is added here.

Question: for every supplied smooth local 2D Lorentz pair
`h=-N(t,x)^2(dt+b(t,x)dx)^2+L(t,x)^2 dx^2`, `N,L>0`, derive a differential
clock/curvature identity retaining arbitrary shift and time-varying `m=NL`.
The chart, fixed-x congruence, example functions and optional immersion are
free-and-explored. Differential geometry is a method under these hypotheses,
not a physical premise. No boundary, initial data, action, numerical mesh,
empirical fit, or approximation is supplied. Maximum claim: exact local
identity and the explicitly identified remaining closure/ambient hypotheses.

## Independent coframe derivation

Let `theta0=N(dt+b dx)`, `theta1=L dx` and their dual frame be

```
e0 = N^-1 partial_t,
e1 = L^-1 (partial_x-b partial_t).
a = [N_x-(Nb)_t]/(NL),
H = L_t/(NL).
```

Direct differentiation gives `dtheta0=-a theta0 wedge theta1` and
`dtheta1=H theta0 wedge theta1`. The metric-compatible torsion-free
connection has `omega^0_1=omega^1_0=a theta0+H theta1`. Consequently

```
domega^0_1 = K theta0 wedge theta1,
K = e0(H)+H^2-e1(a)-a^2,
R[h] = 2K.
```

Convention: `R(X,Y)Z=nabla_X nabla_Y Z-nabla_Y nabla_X Z-nabla_[X,Y]Z`;
in coordinates `R^a_{bcd}=partial_c Gamma^a_{db}-partial_d Gamma^a_{cb}
+Gamma^a_{ce}Gamma^e_{db}-Gamma^a_{de}Gamma^e_{cb}`.
The independently authored general-coordinate Christoffel/Ricci calculation
returns exactly zero for `R_coordinate-2K`. It does not start from Cartan's
curvature formula. SymPy 1.13.1, Python 3.10.12; exact symbolic arithmetic,
no tolerances, 2x2 matrix, approximately 49 MiB maximum RSS and 0.71 seconds.
The capture contains the actual command, versions, stdout/stderr and limits.

With `Phi=-log N` and `m=NL`,

```
a = -e1(Phi)-b_t/L,
H = e0(log m+Phi).
Q = e1(Phi)+b_t/L,
R[h]/2 = e0[e0(log m+Phi)] + [e0(log m+Phi)]^2
         + e1(Q)-Q^2.
```

This is the requested explicit local differential relation. It retains all
three pair functions. It is an identity on the supplied metric, not an
equation selecting that metric. `Phi` belongs to the declared clock
congruence/chart; an arbitrary observer's received clock ratio is not the
pointwise lapse. `m` is the declared auxiliary spatial density, not a scalar
under unrestricted spacetime chart changes.

The one-form `m(t,x)dx` is generally nonclosed: `d(m dx)=m_t dt wedge dx`.
Thus writing it as the exact differential of a new coordinate while leaving
the time coordinate and frame intact requires `m_t=0`. One may instead use
it as an anholonomic tape form, or integrate `s_x=m` while retaining the
additional `s_t dt` term. The latter transformation changes the fixed-s
congruence and generally changes the lapse/shift interpretation. Neither
route permits dropping `e0(log m)`.

Useful hand-derived controls, not fitted physical solutions:

* Static reciprocal `b=0,L=1/N`: `R=-(N^2)_{xx}`.
* Rindler `N=x,L=1,b=0,x>0`: `R=0` despite nonconstant clock factor.
* `N=1,L=exp(H0 t),b=0`: `R=2H0^2` despite `Phi=0`; setting `m_t=0`
  would lose the curvature.
* `N=L=1,b=k t`: `a=-k,H=0,R=-2k^2`; dropping `b_t/L` gives a false zero.

These do not prove genericity or unique metric reconstruction from clocks.

## Intrinsic null transport and observer dependence

For an intrinsic affinely parametrized future null geodesic
`k=omega(e0+epsilon e1)`, `epsilon=+1` or `-1`,

```
(e0+epsilon e1)(log omega) = -H-epsilon a.
```

Proof: `omega=-h(k,e0)` and `nabla_k k=0` imply
`k(omega)=-h(k,nabla_k e0)=-omega^2(H+epsilon a)` because
`nabla_e0 e0=a e1`, `nabla_e1 e0=H e1`.
For endpoints on the e0 congruence, G220 gives `r_AB=omega_A/omega_B`.
Other supplied endpoint observers require their actual contractions with k.
The complete metric/query, not curvature alone or an endpoint lapse ratio
in a time-live chart, determines this measurement.

## Ambient 4D use needs additional supplied geometry

A supplied Lorentzian 2D metric is not by itself an ambient 4D null query.
One needs an actual timelike immersion with this pullback, the ambient metric,
specified emitter/receiver curves and events, and a chosen regular null branch.
An intrinsic null geodesic in the immersion is an ambient affine null geodesic
only when `II(k,k)=0` along it, where II is the normal second fundamental
form. A supplied ambient null geodesic contained in the surface satisfies
this normal condition. Without containment the 2D transport equation is not
a replacement for the ambient G220 evaluation.

With the above sign convention define
`K_ambient=-g(R^g(e0,e1)e1,e0)`. Gauss gives

```
K_h = K_ambient - [<II00,II11>-<II01,II01>].
```

Thus ambient sectional curvature and extrinsic geometry both enter.
Ambient Ricci is additionally a contraction over transverse directions;
the one pair sectional curvature cannot supply it. Even an Einstein
ambient metric would retain Weyl/sectional freedom and embedding terms.
No claim of full pair-to-ambient reconstruction or physical immersion
selection follows. General ambient frequency transport obeys
`k^a nabla_a omega=-k^a k^b nabla_a U_b`, for a supplied unit observer
field U along the branch, and needs its actual metric/congruence data.

## DDR closure assessment

Current source-first conclusion: DDR on its regular full all-pair domain
implies `TF(E)=0`, hence `E=lambda g`. This is a statement about the
specified response E; it does not identify E with Ricci or with `R[h]`.
Local Metric Sufficiency supplies no such identification or choice of jet
order, tensor type, weight, or nondegeneracy.

Conditional on the ENTIRE G301 class, including `E=a Ric+b Rg`, `a!=0`,
the reviewed source theorem gives `Ric=(R/4)g`, and contracted Bianchi
makes R constant on a connected regular region. Current filter-only GR
does not close that membership implication. Calling the pair identity
a derived 4D field equation, substituting `E=Ric` without its premises,
or setting pair scalar curvature equal to the ambient scalar is invalid.

This is a precise unsupported identification, not a proof that no
independent same-premise closure route exists or that new physics must
be adopted. Supplied legitimate initial/query data are not a defect.

## Review limits at sealing

No parent candidate, parent scripts/results, CGW1 synthesis, or prior
CRD1 verdict has been read. Source-package historical numerical tests
were not replayed; source grades are attributed. The generic coordinate
calculation checks this reviewer's curvature argument independently of
its Cartan calculation, but is not a formal proof or model-independent
review. Ambient Gauss and null-transport statements above were derived
analytically; no ambient symbolic example was executed in this stage.
No exact registry row was queried while the current premise audit was
pending. Source-first time/resource budget and sole-write `review/`
scope were respected.
