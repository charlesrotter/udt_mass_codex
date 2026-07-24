# Exact observer depth–angle transition derivation

## 1. Reciprocal response and projective coordinate

On the registered reciprocal positive ray,

```text
u = exp(-rho),   v = exp(+rho),   u v = 1,
r = v/u = exp(2 rho).
```

Common-scale neutrality removes a common positive multiplier of `(u,v)`,
leaving the ratio `r`. If that ray is assigned an oriented projective
coordinate with

```text
r=0 -> -1,   r=1 -> 0,   r=infinity -> +1,
```

the unique fractional-linear coordinate (up to the fixed normalization) is

```text
xi = (r-1)/(r+1) = tanh(rho).
```

This is `UNIQUE_GIVEN_ANCHORED_PROJECTIVE_INTERPRETATION`. The projective
role is a premise; the algebra after that premise is exact.

Multiplication of reciprocal ratios gives

```text
xi_12 = (xi_1 + xi_2)/(1 + xi_1 xi_2).
```

Changing the observer's zero by `beta`, with `alpha=tanh(beta)`, gives

```text
xi' = (xi-alpha)/(1-alpha xi).
```

`xi` is signed because it is an oriented chart coordinate. Physical
distance is nonnegative; its direction is separate. The derivation does not
identify physical distance with `Dmax |xi|`.

## 2. The metric discriminator

For a physical spatial metric `h` and a transnormal reciprocal depth,

```text
B(rho) = h^-1(d rho,d rho) > 0,
dD/d rho = 1/sqrt(B(rho)).
```

Consequently each candidate distance profile requires a different metric
gradient:

| Candidate | `D(rho)` | Required `B(rho)` | Endpoint |
|---|---|---|---|
| projective tanh | `Dmax tanh(rho)` | `cosh(rho)^4/Dmax^2` | finite |
| exponential saturation | `Dmax(1-exp(-rho))` | `exp(2rho)/Dmax^2` | finite |
| linear control | `L rho` | `1/L^2` | infinite |
| full-frame radial control | `L(exp(rho)-1)` | `exp(-2rho)/L^2` | infinite |

The WR-L radial proper-distance slice supplies the second row with
`Dmax=2X`. The reciprocal projective ray supplies the first row as a display
coordinate. No registered complete branch supplies the first row as its
physical proper distance, and the WR-L slice has not been promoted to a
global two-observer diameter.

## 3. What “exponential near the limit” resolves

Both bounded candidates approach their endpoint exponentially in reciprocal
depth, but not with the same exponent:

```text
Dmax - D_tanh
  = 2 Dmax/(exp(2 rho)+1)
  ~ 2 Dmax exp(-2 rho),

Dmax - D_exp
  = Dmax exp(-rho).
```

The reciprocal clock/ruler response itself remains exactly `exp(±rho)`.
Thus the proposed exponential behavior is real, but it is shared by more
than one candidate physical-distance realization.

The small-depth series show why an early first-order Taylor approximation
could not decide the issue:

```text
tanh(rho)             = rho - rho^3/3 + ...
1-exp(-rho)           = rho - rho^2/2 + rho^3/6 + ...
```

They share the same origin and unit slope; they first separate beyond linear
order.

## 4. Angular completion

In the complete round `S3` control, observer-relative position is a unit
quaternion. For

```text
q=(cos chi, sin chi n),
```

composition contains both `n_1 dot n_2` and `n_1 cross n_2`. Exact rational
controls verify unit norm, inverse, left-relative invariance, and
noncommutativity. Therefore the one-dimensional fractional law is complete
only on an ordered fixed direction. Non-collinear comparison requires
angular data.

The constant-squashed homogeneous control retains left-relative group
composition, but its Hopf-direction and horizontal lengths differ.
Therefore group composition does not by itself select a universal radial
distance profile.

## 5. Failed solders retained

- The local Lorentz `3+3` algebra has boost–boost commutators that generate
  rotations, but reciprocal weighting is not an automorphism of that
  bracket. No native identification of `rho` with Lorentz rapidity follows.
- Complete triangular coframe multiplication closes in a chosen
  trivialization but changes under independent coframe gauge
  representatives. Using it as physical observer composition would be
  `CHOSE`, not `DERIVED`.
- `c` remains the founding observational clock–length conversion in the
  metric. It does not, by itself, determine which dimensionless
  distance–depth profile or which finite spatial endpoint the complete
  branch realizes.

## Result

The projective radial transition is exact once the anchored projective role
is admitted. The exponential reciprocal response is exact. Exponential
approach to a finite endpoint is supported in both registered bounded
candidates. The complete metric has not yet selected the physical
observer-distance solder, so a physical `tanh` law, a unique simple
exponential law, and global `X_max` remain open.
