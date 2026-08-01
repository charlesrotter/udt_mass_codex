# Exact derivation of the conditional F01 inverse wall-stability surface

## 1. Scope

This calculation stays inside the frozen conditional F01 local crease model, at its unique
registered massive root `1.68102 < s* < 1.68103`, with `ell=1`, the two owned `p` endpoint
domains, and the P4 quadratic response. It does not derive a boundary law. It asks the inverse
question: what two aggregate quadratic wall responses would be sufficient in one explicitly
declared trace-aligned slice?

The coordinates are

```text
tau >= 0 : effective angular-trace coefficient after eliminating the angular fields,
eta       : aggregate direct curvature in nu^2, where nu=k mu.
```

Intermediate `tau` values are diagnostic response coordinates, not banked F01 postures. The
banked endpoints are R05 at `tau=0` and the R06 zero-angular-trace field-core limit at
`tau=tau_infinity`. `eta` is likewise an effective second-wall Hessian coordinate, not a selected
per-wall functional.

## 2. Angular elimination and its two endpoints

Let `g(x)=1/w(x)` and let `J=integral[-1,1] dx/w`. The frozen P4 angular block depends on the
combined angular trace. Eliminating it with free endpoint traces leaves no penalty: this is R05.
Constraining the angular primitive to have zero trace at both walls instead gives the exact
rank-one term already derived in the parent audit,

```text
tau_infinity |g><g|,             tau_infinity = s^2/J.
```

To derive rather than merely draw the intermediate path, introduce one normalized finite aligned
angular-trace Hessian coordinate `beta>=0`. The trace being penalized must be a **trace
difference**, not an absolute angular value: the angular block is derivative-only and a free
constant shift would otherwise make a one-wall absolute-value term vacuous.

For each angular channel `i` in `{f,h}`, set

```text
q_i = v_i',
Delta v_i = integral[-1,1] q_i dx
X_i = a_F c_i p/(g_i w).
```

Equivalently fix the derivative-invisible reference `v_i(-1)=0`, so `Delta v_i=v_i(1)`. The
finite aligned second germ adds `beta g_i (Delta v_i)^2` to

```text
integral[-1,1] w g_i (q_i+X_i)^2 dx.
```

Varying `q_i` gives

```text
q_i+X_i = -beta Delta v_i/w,
Delta v_i = -[a_F c_i/g_i] [integral p/w]/(1+beta J).
```

Substitution leaves

```text
[a_F^2(c_i^2/g_i) beta/(1+beta J)] (integral p/w)^2.
```

Summing the two channels, using the frozen `sigma=sum_i c_i^2/g_i` and
`a_F^2 sigma=s^2`, gives

```text
tau(beta) = s^2 beta/(1+beta J).
```

The scalar “two springs in series” form used by the exact control is the equivalent reduction

```text
min_z [(s^2/J)(q-z)^2 + s^2 beta z^2].
```

The minimizer and eliminated coefficient are

```text
z = q/(1+beta J),
tau(beta) = s^2 beta/(1+beta J).
```

Hence `beta=0` is R05, every finite positive `beta` gives `0<tau<s^2/J`, and only
`beta->infinity` reaches the R06 zero-angular-trace limit. Conversely,
`beta=tau/(s^2-tau J)` on the open interval. These identities are exact symbolic controls.

The inverse audit therefore connects the field operators by

```text
A_tau = A0 + tau |g><g|,         0 <= tau <= tau_infinity.
```

This derived parameterization makes the slice mathematically permissible under the currently free
second wall germ. It is not a claim that UDT supplies, selects, or realizes `beta`, or that this
aligned one-coordinate germ exhausts the possible wall responses.

## 3. Field crossing

Write

```text
m = <g,A0^-1 g>.
```

The exact response `phi=A0^-1 g` is verified symbolically, including both endpoint domains.
Integrating `phi/w`, with the endpoint identities for `w'/w` and `1-1/w`, gives

```text
m_D = -J/s^2 - 2/[s^2(s-1)],
m_F = -J/s^2 - 2(4s^2-3s+1)/[s^2(2s-1)w(1)].
```

The primary code also integrates `phi/w` directly with outward intervals; those independent
enclosures overlap the displayed formulas in both domains. The cold audit separately reconstructs
the same response by a shooting boundary-value solve.

Define

```text
d_D = 2/(s-1),
d_F = 2(4s^2-3s+1)/[(2s-1)w(1)].
```

Then the unique rank-one crossing is

```text
tau_critical = -1/m,
t_critical   = tau_critical/tau_infinity = J/(J+d).
```

The frozen R05 field form has index one. Rank-one interlacing and the nonzero crossing show:

- `tau < tau_critical`: the field form still has index one;
- `tau = tau_critical`: the field form has one zero mode, proportional to `A0^-1 g`;
- `tau > tau_critical`: the field core is positive in the owned reduced space.

Numerically certified enclosures are:

| `p` endpoint domain | `t_critical` | `tau_critical` | `tau_infinity` |
|---|---:|---:|---:|
| Dirichlet | `[0.4417740924, 0.4423464119]` | `[0.5362796589, 0.5374600571]` | `[1.2139228354, 1.2150207228]` |
| free right | `[0.5541992847, 0.5549826638]` | `[0.6727551671, 0.6743154373]` | `[1.2139228354, 1.2150207228]` |

## 4. Restoring the constant lambda/mu direction

Let `ell` be the exact cross-functional and `C` its direct diagonal in the dimensionless
`nu=k mu` coordinate. The joint form in this slice is

```text
Q_tau,eta[v,nu]
  = <v,A_tau v> + 2 nu ell(v) + (C+eta) nu^2.
```

At `tau=0`, define the exact relaxed scalar

```text
S0 = C - <ell,A0^-1 ell>.
```

With `u0=-A0^-1 ell`, self-adjointness gives

```text
n = <ell,A0^-1 g> = -integral[-1,1] u0/w dx.
```

The scripts verify the identity two ways: by the Green/self-adjoint overlap and by direct
evaluation of `ell(A0^-1 g)`. Their interval enclosures overlap and exclude zero in both endpoint
domains.

The Sherman-Morrison identity now gives, away from the crossing,

```text
S_nu(tau)
  = C - <ell,A_tau^-1 ell>
  = S0 + tau n^2/(1+tau m).
```

This separates the three regions:

1. Below the field crossing, choose `nu=0` and retain the field negative direction. No `eta` can
   repair the joint form.
2. At the crossing, the zero mode couples to `nu` because `n != 0`. Its two-dimensional block has
   a nonzero off-diagonal and zero field diagonal, so it is indefinite for every finite `eta`.
3. Above the crossing, the field core is positive and completing the square is legitimate. The
   complete joint form in this two-coordinate slice is nonnegative exactly when
   `eta >= eta_critical(tau)=-S_nu(tau)`. Equality is semidefinite.

Thus angular pinning alone moves the negative direction; it does not remove it. Both the angular
trace response and the direct lambda/mu wall curvature have to act.

## 5. Frozen sample nodes

Before evaluating the surface, four points above each crossing were frozen as

```text
t = t_critical + alpha(1-t_critical),
alpha = 1/4, 1/2, 3/4, 1.
```

At those points the exact simplification is

```text
S_nu(alpha)
  = S0 - s^2 n^2 (J+alpha d)/[alpha d(J+d)].
```

Every certified `eta_critical=-S_nu` interval is strictly positive. At the R06 field-core
endpoint (`alpha=1`, `t=1`) the required aggregate thresholds are:

| `p` endpoint domain | `eta_critical` in `nu` | representative direct `mu^2` curvature |
|---|---:|---:|
| Dirichlet | `[8.2620654877, 8.4157055785]` | `[2.0655163719, 2.1039263946]` |
| free right | `[13.9722626768, 14.1511395881]` | `[3.4930656692, 3.5377848970]` |

The last column uses only the representative normalization `a_F=a_Fprime=2`, for which
`k=1/2` and therefore `eta_mu=k^2 eta=eta/4`. It is not a universal physical normalization.
All preregistered nodes and full outward intervals are in `THRESHOLD_SURFACE.tsv` and
`PRIMARY_CERTIFICATE.json`.

## 6. What was and was not derived

Derived inside the frozen conditional slice:

- the exact rank-one crossing formulas;
- the index partition below, at, and above each crossing;
- the exact relaxed Schur surface and finite-`eta` obstruction at the crossing;
- positive threshold intervals at all preregistered sample nodes.

Not derived:

- that `tau` or `eta` is supplied, selected, native, or physical;
- the other components of the unrestricted wall Hessian;
- a per-wall functional, realized variation law, boundary, action, carrier, source, bootstrap
  return, global matter configuration, time persistence, or mass.

The result is therefore an inverse design constraint on any future native closure law, not a
stability theorem for UDT matter.
