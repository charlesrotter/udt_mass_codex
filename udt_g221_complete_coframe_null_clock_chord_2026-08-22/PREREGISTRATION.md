# G221 preregistration

Date: 2026-08-22

## Hypotheses

Let

```text
H = Q^T Q
D = A^2 - N^2 beta^2 > 0
P^2 = N^2 - s_t^T H s_t > 0
Pi = p_x - s_x^T p_z
q2 = p_z^T H^-1 p_z
R = sqrt(Pi^2 + D q2)
```

on one supplied smooth complete-coframe chart. Require `(p_x,p_z)` nonzero. For a time-only
spatially homogeneous specialization, the spatial covector is conserved along each affinely
parametrized null geodesic. In a general supplied null germ, its endpoint values are carried by that
germ and are not independently chosen.

## Preregistered derivation

The inverse-metric null equation in orthonormal coframe components must have exactly two roots

```text
p0hat(epsilon) = (-N beta Pi + epsilon A R)/D, epsilon in {-1,+1}.
```

Under the declared time orientation, `epsilon=-1` must be the unique future root. Its coordinate
energy and measured frequency must be

```text
p_t = s_t^T p_z - N (A R + N beta Pi)/D
W = -p_t/P
  = [N (A R + N beta Pi)/D - s_t^T p_z]/P > 0.
```

For the supplied null clock correspondence,

```text
r_AB = W_A/W_B
delta_AB = -log(r_AB).
```

The magnitude of a common positive affine rescaling must cancel. In a time-only homogeneous chart,
the incidence ray must obey the exact Hamilton--Jacobi velocity

```text
d xi^i/dt = - partial p_t^-/partial p_i,
```

with its spatial momentum direction allowed to vary across neighboring rays. No fixed-momentum
differentiation may be substituted for the event-pair Jacobi problem.

Using `y=tau_A`, the target comparison-clock tangent must be `r_AB U_B`, hence its completed clock
coefficient must satisfy `T_B=r_AB`. This is compatibility on the same supplied correspondence,
not an independent proof of G176 or a construction of the full rank-two pair plane.

## Mandatory exact controls

1. `p_z=0`, `s_t=s_x=0`, `p_x>0` gives `W=p_x/(A-N beta N)` and therefore the G220 law
   `r_AB=C_+B/C_+A`.
2. Nonzero `p_z` makes `Q` enter through `p_z^T H^-1 p_z`.
3. Nonzero `s_x` enters through `Pi`; nonzero `s_t` enters both observer normalization `P` and
   coordinate energy `p_t`.
4. Passive screen coordinate changes `z=K z'`, with
   `Q'=QK`, `S'=K^-1 S`, `p_z'=K^T p_z`, leave `Pi`, `q2`, `P`, and `W` invariant.
5. Positive affine scaling multiplies `W` but leaves `r_AB` invariant.
6. Direct inverse-metric contraction and coframe-root calculations must agree.
7. The past root must have negative frequency against the declared future observer.
8. `D=0`, `P=0`, zero covector, non-real or nonregular branch data must fail closed rather than be
   silently continued.

## Falsification contract

The proposed landing fails if any retained regular exact witness violates the root, positivity,
covariance, affine-cancellation, Hamilton--Jacobi, clock-leg, or G220-reduction identities. It also
fails if screen or mixing terms are appended after scalar readout, if a query is selected, or if a
time-only conserved spatial covector is asserted for a general spatially varying metric.

## Maximum conclusion

At most:

```text
COMPLETE_COFRAME_NULL_CLOCK_CHORD_DERIVED_CONDITIONALLY
__SCREEN_AND_MIXING_ENTER_UPSTREAM
__G220_RECOVERED
__NULL_AND_FULL_PAIR_REMAIN_QUERY_TYPED
```

No physical history, query population, branch aggregation, full pair plane, screen/Jacobi transfer,
`X_max`, observation, radiative transfer, action, source, matter, bootstrap, mass, or signalling law
may be inferred.

