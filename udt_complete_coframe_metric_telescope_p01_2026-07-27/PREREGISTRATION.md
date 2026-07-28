# P01 preregistration: complete-coframe metric telescope

Date: 2026-07-27

## Purpose

Build the first numerical telescope for the metric's off-shell configuration
space. The question is observational:

> Across a broad, deterministic bounded family in which all eight amplitudes of
> the current complete triangular coframe vary, what causal, curvature,
> reciprocal/angular, screen-tidal, holonomy, and rank-changing structures
> actually occur?

This is not a background solve. Sampled configurations are not asserted to obey
a field equation, represent physical time evolution, or rank as possible
universes. The atlas may reveal structures and formulate sharper questions; it
cannot select physics.

## Configuration chart

Use `x0=c_E t` and coordinates `(x0,x,y,z)` with

```text
theta0 = exp(-phi) dx0
theta1 = exp(+phi) dx
(theta2,theta3)^T = D[(dy,dz)^T+S(dx0,dx)^T]

D = [[exp(sigma/2-alpha), k exp(sigma/2-alpha)],
     [0,                      exp(sigma/2+alpha)]].
```

All eight amplitudes

```text
(phi,sigma,alpha,k,S10,S11,S20,S21)
```

remain live. This is a registered bounded chart of complete configurations,
not a selected extension and not an eight-field ontology. `phi` remains the
founded pair's logarithmic depth rather than an extra scalar.

## Bounded functional family

For each amplitude `q_A`, sample

```text
q_A(t,x) = shell/sqrt(8) * sum_j c_Aj B_j(t,x)
```

with the eight fixed basis functions

```text
1,
x,
(3x^2-1)/2,
sin(pi x),
sin(pi t),
cos(pi t),
sin(pi t) cos(pi x),
cos(2pi t) sin(pi x).
```

The coefficients form one deterministic scrambled Sobol sequence in 64
dimensions, mapped to `[-1,+1]`. Freeze:

```text
seed                 20260727
shells               0.03, 0.10, 0.30, 1.00, 2.50
configurations/shell 1024
production total     5120 plus explicit controls
evaluation grid      17 t points x 33 x points on [-1,+1]^2
transport loop       square with corners (+/-1/2,+/-1/2)
RK4 steps            64 per side, 256 per loop
dtype                float64
device               one Tesla V100-PCIE-32GB process
batch size           64 configurations
```

These coefficient bounds, basis functions, coordinate ranges, loop, and seed
are `pinned-by-HABIT` numerical exploration controls, not physical values.
Every shell is reported separately. No outcome-dependent retuning is allowed.

## Exact evaluated objects

At every sampled grid point, construct the coframe, metric, inverse metric,
first and second metric jets, Levi-Civita connection, Riemann tensor, Ricci
tensor, and scalar curvature. Also compute:

- exact determinant control `det(g)=-exp(2 sigma)`;
- causal class of the founded `dphi` readout;
- the supplied-chart orthonormal Riemann tensor;
- screen tidal matrix `T_AB=R_A0B0`, its trace, determinant, and eigenvalue
  discriminant;
- chart-conditional pair/screen Ricci mixing;
- coordinate-loop Levi-Civita holonomy;
- loop Lorentz-preservation backward error;
- inverse-loop composition error;
- pair/screen holonomy mixing in the supplied coframe; and
- nonfinite, ill-conditioned, causal-type-changing, repeated-tidal, and
  nontrivial-holonomy strata.

The assigned pair/screen split is chart-supplied in this atlas. It must not be
reported as a metric-selected physical pair on every sample.

## Controls and certification

Before production:

1. neutral configuration gives Minkowski metric, zero curvature, and identity
   loop holonomy;
2. arbitrary constant amplitudes give a constant flat metric and identity
   loop holonomy;
3. metric determinant agrees with `-exp(2 sigma)`;
4. direct inverse-metric `dphi` norm agrees with the complete-coframe formula;
5. GPU float64 local jets/curvature agree with an independent CPU
   implementation on at least 32 preregistered configurations;
6. reversing every control loop inverts its holonomy; and
7. doubling RK4 resolution on at least 32 configurations reduces the transport
   discrepancy consistently with fourth-order integration.

Production certification records all configurations. A numerically unresolved
configuration is labeled, not discarded. Stop only for:

- failed neutral or constant-flat control;
- CUDA/device failure or another GPU process occupying the production device;
- projected memory above 6 GiB or CUDA OOM;
- nondeterministic coefficient replay;
- source/manifest mismatch; or
- more than 25% numerically unresolved configurations in any shell, indicating
  the fixed numerical chart/range is not being evaluated reliably.

The last threshold is a numerical-feasibility stop, not a physics filter.

## GPU operations

One process only. Device `cuda:0`; float64. Estimated peak working allocation is
below 6 GiB on the 32 GiB V100. Checkpoint after every shell to distinct
shell-tagged NPZ/JSON files. Never overwrite an existing checkpoint. Hard wall
time: 30 minutes. If interrupted, restart only missing shells after verifying
their coefficient and source hashes.

## Classification, not selection

The atlas must retain flat, weak, strong, singular/numerically unresolved,
causal-type-changing, repeated-eigenvalue, trivial-holonomy, and nontrivial-
holonomy samples. No acceptance rule may demand smooth caps, particles,
localized energy, GR behavior, topology, mass, stability, or cosmological fit.

## Maximum conclusion

At most P01 may report the empirical census and correlations within this exact
5,120-member bounded configuration family, the tested numerical convergence,
and which geometric structures coexist or change strata. It may not infer:

- a field equation or physical time evolution;
- a selected complete extension, profile, path, or branch;
- an action, source, carrier, boundary law, bootstrap closure, density,
  `X_max`, mass, or physical scale;
- completeness of the infinite-dimensional configuration space; or
- a physical prediction.
