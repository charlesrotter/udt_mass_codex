# Preregistration — intrinsic reciprocal-screen holonomy audit

Date: 2026-07-27

Base: `ff3d936406e7c3eacc8b61322a860364562c3eb3`

Question type: **METRIC-LED, BOUNDED OFF-SHELL HOLONOMY MAP**.

## Whole question

The parent audits supplied, for the first time in this lane, a complete nonconstant twisted-`S3`
metric with an intrinsic clock, twist-selected ruler, orthogonal screen, and full optical transport.
Does its Levi-Civita connection preserve the reciprocal-screen endomorphism

```text
X_lambda = diag(-1,+1,lambda,lambda)
```

around closed paths, or is the already valid path-groupoid cocycle genuinely unavoidable on these
branches?

This audit computes the actual local covariant derivative, curvature-generated holonomy algebra,
and prescribed-loop parallel transport.  It does not search for a desired universe or select a
branch.

## Premise stamps

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

No co-presence, signalling, action, source, or field-equation premise enters the calculation.

## Frozen configuration family

Use unchanged C01–C06:

```text
theta0 = exp(-phi)(dt+a sigma3),
theta1 = exp(+phi) sigma3,
theta2 = exp(lambda phi) sigma1,
theta3 = exp(lambda phi) sigma2,
g      = -theta0^2+theta1^2+theta2^2+theta3^2,
a      = 1/64,
epsilon= 1/50,
lambda in {-2,-1,0,1/2,1,2},
```

with the same quaternion/Maurer–Cartan coframe and polynomial `phi`.  Units remain `c_E=R=1`.
Every configuration is a free off-shell witness, not a physical solution.

## Frozen local census

At the three parent stereographic events

```text
P00=(0,0,0),
P01=(1/4,-1/5,1/6),
P02=(-1/3,1/7,1/5),
```

compute all components of

```text
(nabla_c X)^a_b = Gamma^a_cb (x_b-x_a),
x=(-1,+1,lambda,lambda).
```

Retain clock–ruler, clock–screen, ruler–screen, and screen-internal block maxima separately.  At
P00 also derive the clock–ruler component exactly for symbolic real `lambda`.  If it is nonzero and
independent of `lambda`, the maximum allowed statement is local non-parallelity for every real
`lambda` on this frozen profile—not a universal UDT theorem.

At every event and sampled `lambda`, form all six curvature endomorphisms `R(E_c,E_d)`, close their
real matrix Lie algebra under commutators, and record numerical rank and singular values.  Relative
rank tolerance is `1e-9`.  A full six-dimensional result is sufficient to identify the local
restricted holonomy algebra as `so(1,3)`; a lower rank is retained without interpretive repair.

Independently recompute the curvature matrices in coordinate components with Torch automatic
differentiation and transform them into the orthonormal frame.  Required scaled agreement is
`<=2e-8`.

## Frozen loop census

At `t=0`, transport the full orthonormal frame around all six prescribed closed spacelike curves for
every sampled `lambda` (36 loop transports total):

```text
G1: q(s)=(cos s, sin s,0,0)       left-invariant sigma1 great circle
G2: q(s)=(cos s,0, sin s,0)       left-invariant sigma2 great circle
G3: q(s)=(cos s,0,0, sin s)       left-invariant sigma3/Hopf-fiber great circle
L12: stereographic x=(rho cos s,rho sin s,0)
L23: stereographic x=(0,rho cos s,rho sin s)
L31: stereographic x=(rho sin s,0,rho cos s)
s in [0,2 pi], rho=1/5.
```

The curves are prescribed probes of connection holonomy.  They are not geodesics, signals,
observer worldlines, or selected boundaries.  No curve may be discarded for giving identity,
nonidentity, closure, or nonclosure.

For the transport matrix `U`, record:

- loop endpoint mismatch and Lorentz residual `U^T eta U-eta`;
- `||U-I||`, determinant, and clock–ruler/clock–screen/ruler–screen block support;
- ordinary closure residual `||U X U^-1-X||`;
- odd/inversion residual `||U X U^-1+X||`; and
- direct-versus-two-half and coarse-versus-fine transport residuals.

Ordinary Levi-Civita holonomy, an externally supplied reciprocal inversion, and resetting the
transported frame to the intrinsic base frame are three different operations and must not be
spliced.

## Numerical and independent-verification contract

- CPU float64 only; `CUDA_VISIBLE_DEVICES` empty.
- Production: SciPy `DOP853`, `rtol=1e-10`, `atol=1e-12`, `max_step=2*pi/512`.
- Fine replay: `rtol=2e-11`, `atol=2e-13`, `max_step=2*pi/1024`.
- Independent loop holdout: fixed-step RK4 with 4096 steps on G1–G3 at `lambda=-2,0,1,2`.
- Global quaternion and stereographic coframes must agree at 24 non-pole overlap points to
  `<=2e-10` scaled.
- Lorentz residual `<=2e-8`, direct/two-half residual `<=2e-8`, fine/coarse difference `<=2e-7`,
  and RK4/DOP853 difference `<=2e-6`.

A tolerance failure is retained as a numerical failure.  It cannot be explained by adding a
mechanism.

## Algebraic inversion contract

Before interpreting an odd residual, compare the Lorentz signatures of the eigenspaces of
`X_lambda` and `-X_lambda`.  If they are not Lorentz-conjugate, ordinary metric holonomy cannot
implement reciprocal inversion.  Even if an algebraic spectrum matches, no seam, quotient,
transition function, or inversion is supplied unless separately derived.

## Falsification and maximum conclusion

If all gates pass, the maximum conclusion is a bounded `OBSERVED` holonomy atlas plus exact local
Cartan statements.  It may determine whether ordinary endpoint closure is compatible with these
six frozen metrics and whether the actual curvature algebra centralizes `X_lambda`.

It may not select a physical `lambda`, profile, topology, path rule, quotient, reciprocal seam,
action, source, carrier, boundary, density, bootstrap, mass, `X_max`, dynamics, signalling law, or
SNe cosmology.  Failure of ordinary endpoint closure leaves the path-groupoid cocycle valid and is
not a no-go for UDT or another on-shell completion.

## Completeness map

Covered: all six frozen branches, three local events, complete connection blocks, curvature Lie
closure, three global great circles, three contractible chart loops, full frame holonomy, ordinary
and odd closure diagnostics, convergence, coordinate-curvature independence, and RK4 holdouts.

Dropped: every other profile, event, loop, topology, seam, quotient, time-live metric, field
equation, on-shell branch, action, source, carrier, boundary variation, bootstrap, density, mass,
`X_max`, operational access, and observation fit.
