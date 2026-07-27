# Preregistration — intrinsic-to-optical transport atlas

Date: 2026-07-27

Base: `cc7aa2947e1d8377c175d3cdc7958689ad06dac6`

Question type: **METRIC-LED, BOUNDED OFF-SHELL TRANSPORT MAP**.

## Whole question

The parent audit proved that a nonconstant stationary depth on the complete twisted `S3` forces the
metric-intrinsic clock/ruler screen and a ruler-launched null ray to mix somewhere.  What does that
mixing actually look like along metric geodesics, and how does it affect the full transverse Jacobi
map?

This audit maps that transport in the unchanged frozen C01–C06 configurations.  It does not ask for
a particle, an SNe match, a preferred `lambda`, or an on-shell universe.

## Premise stamps

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

No co-presence or signalling premise enters the ODEs.

## Frozen metric and profile

Use exactly

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

with the parent quaternion/Maurer–Cartan coframe and unchanged polynomial profile.  Units remain
`c_E=R=1`.  These are free bounded configuration witnesses, not solutions.

## Frozen path census

Use stereographic spatial events at `t=0`:

```text
P00=(0,0,0),
P01=(1/4,-1/5,1/6),
P02=(-1/3,1/7,1/5).
```

At each event and for every `lambda`, launch both future null directions

```text
k_plus = E0+E1,
k_minus= E0-E1,
```

with initial frequency `-g(E0,k)=1`.  Parallel transport the initial screen `E2,E3`.  Integrate to
affine length `L=1/4`, retaining checkpoints `L/4,L/2,3L/4,L`.  The frozen census therefore contains
`6 x 3 x 2 = 36` paths and 144 checkpoint rows.  No path may be discarded for looking unhelpful.

## Equations and observables

Integrate the affine geodesic and parallel screen:

```text
dx^mu/ds = k^mu,
dk^mu/ds = -Gamma^mu_ab k^a k^b,
DS_A/ds = 0.
```

Use the parallel screen to form the symmetric optical curvature matrix

```text
F_AB=g(S_A,R(k,S_B)k).
```

The full Jacobi phase-space propagator obeys

```text
dM/ds = [[0,I],[F,0]] M,
M(0)=I_4.
```

Its upper-right block `B` is the vertex map and

```text
D_A=sqrt(abs(det B)).
```

Record, without threshold-based filtering:

- null residual `|g(k,k)|`;
- Killing-energy drift;
- screen orthonormality and `g(k,S_A)` residuals;
- curvature-screen symmetry residual;
- symplectic and determinant residuals of `M`;
- direct-versus-two-half composition residual;
- endpoint intrinsic-screen leakage of the transported screen;
- mismatch between transported initial pair and the endpoint intrinsic pair, modulo screen `SO(2)`;
- `D_A`, `det B`, `Delta phi`, local screen-weight ratio, and WR-L comparison readouts.

The primary screen-leakage scalar is the sum of squared endpoint contractions of the two transported
screen vectors with the local intrinsic `u` and `n`.  Zero means equality of the two screen planes;
positive means connection-induced mixing.  It is a diagnostic, not an energy.

## SNe comparison contract

At each checkpoint record

```text
W=abs[1-exp(-2 Delta phi)].
```

This is a preserved WR-L shape readout, not a target.  Record raw `D_A` and `W`; when both endpoint
values are nonzero also compare the endpoint-normalized four-checkpoint shapes.  This normalization
is diagnostic and may not be called a fit or physical scale calibration.

For every `lambda`, also record `abs[1-exp(lambda Delta phi)]`.  The `lambda=-2` equality with `W`
is an algebraic identity and must be labeled tautological.  Only the independently integrated
Jacobi `D_A` can provide a nontrivial optical comparison.

No observational data, nuisance offset, density, `X_max`, cosmological parameter, or parameter
optimization is allowed.

## Numerical and independent-verification contract

- CPU and float64 only; `CUDA_VISIBLE_DEVICES` empty.
- Production integration: SciPy `DOP853`, `rtol=1e-9`, `atol=1e-11`, `max_step=1/64`.
- Convergence replay: `rtol=2e-10`, `atol=2e-12`, `max_step=1/128`.
- Independent integration holdout: fixed-step RK4 with step `1/512` on all six `lambda` values at
  P00 in the `plus` direction.
- Independent geometry holdouts: a coordinate-metric Christoffel/Riemann implementation at twelve
  preregistered path checkpoints, compared with the production orthonormal-frame implementation.
- Exact local anchor: the initial transverse mismatch derivative must reproduce the parent Cartan
  formula from `E2(phi),E3(phi)` with the registered sign convention.

Certification tolerances:

```text
null residual                         <= 2e-8
relative Killing-energy drift        <= 2e-8
screen Gram and k-screen residual     <= 2e-8
screen-curvature asymmetry            <= 2e-8
symplectic residual                   <= 2e-7
|det M-1|                             <= 2e-7
direct/composed M max difference      <= 8e-7
fine/coarse endpoint-state difference <= 3e-6
RK4/DOP853 holdout difference         <= 5e-5
frame/coordinate geometry holdout     <= 2e-8 scaled
```

A failed tolerance is retained as a numerical failure, not explained by adding physics.

## Falsification and maximum conclusion

If the gates pass, the maximum conclusion is a bounded `OBSERVED` transport atlas plus exact local
anchors.  It may state which candidate paths mix, focus, defocus, or approach a projected caustic.
It may not select a physical `lambda`, profile, topology, action, source, carrier, density, mass,
`X_max`, signalling law, or SNe cosmology.

An apparent Jacobi/WR-L resemblance is at most a preregistered configuration-level lead because the
metric profiles are off shell.  A mismatch is not a no-go for UDT, WR-L, another completion, or an
on-shell branch.

## Completeness map

Covered: all 36 frozen short geodesics, both ruler directions, all six candidate `lambda` values,
four checkpoints, local intrinsic screens, parallel optical screens, full Jacobi phase-space
transport, composition, and bounded readout comparisons.

Dropped: longer paths, complete cut-locus atlas, all initial null directions, all profiles and
events, alternate topologies, time-live metrics, field equations, on-shell selection, action,
source, carrier, boundary variation, bootstrap, density, mass, `X_max`, operational access, and
observational fitting.
