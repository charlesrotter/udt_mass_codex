# F01 lambda/mu Schur check — exact derivation

Date: 2026-08-01  
Frozen source base: `53bdc2c`  
Preregistration commit: `af71724`

## Result

The exact registered outcome is:

```text
SCHUR_SIGN_MIXED_ACROSS_OWNED_BRANCHES
```

At the unique massive crease root in `s in (1,3)`:

- R05, with free angular traces: the lambda/mu Schur scalar is strictly positive for both the
  other-end Dirichlet and registered free/right-Robin `p` domains. The one exact reduced-field
  negative direction therefore remains the only joint negative direction.
- R06, with supplied odd zero angular traces: an explicit admissible joint field-plus-mu witness is
  strictly negative for both `p` domains. The rank-one angular pin removes the reduced-field
  negative direction, but the formerly open lambda/mu direction puts one negative direction back.

Thus all four local conditional joint forms have index one, although the location of the negative
direction differs. This does not select a boundary, carrier, action, cell chain, or stable matter.

## 1. Every root is covered

Put `z=s(x+1)`. Then

```text
w_s(x) = q(z) = 1-z+z^2/2,
F(s) = (1/s) integral_0^(2s) log(q(z)) dz.
```

The quadratic obeys `q-1=z(z-2)/2`. Hence `log(q)<0` on `(0,2)` and `log(q)>0` on
`(2,infinity)`. Its primitive `I(U)` is strictly increasing for `U>2`. Also `I(2)<0`, while

```text
I(6) >= -2 log(2) + 2 log(5) = 2 log(5/2) > 0.
```

The first bound uses `q>=1/2` on `[0,2]`; the second uses `q>=1` on `[2,4]` and `q>=5`
on `[4,6]`. Therefore exactly one root lies in `s in (1,3)`. Outward interval evaluation of the
closed primitive gives

```text
F(1.68102) < 0 < F(1.68103).
```

## 2. The apparent P1 scale is not a sign choice

Write `a=a_F`, `a'=a_Fprime=2`, and `k=a'/a^2`. On the registered massive background,

```text
pbar=log(w)/a,     fbar'=s/(a w),     E0=s^2/a^2,
(w')^2+s^2=2s^2 w.
```

After direct substitution into the frozen joint Hessian, its dependence on the constant mu is

```text
Q = Q_field + 2(k mu)L + (k mu)^2 C.
```

For every finite nonzero `a` on the massive branch, changing the P1 representative only rescales
the Schur scalar by `k^2>0`. It cannot change its sign. The executable certificates use
`a=a'=2`, so `k=1/2`, only after this separation.

## 3. R05 exact response

With free angular derivative variation eliminated pointwise, the scalar field operator is

```text
L0[p] = -(w p')' - s^2 p/w.
```

The mu cross functional and diagonal, in the scale-free coordinate `nu=k mu`, are

```text
ell[p] = integral {
  s^2 p [1 + log(w)(1-1/w)] + log(w) w' p'
} dx,

C = s^2 integral log(w)^2(1-1/w) dx.
```

The relaxed response `u=-L0^-1 ell` solves

```text
L0[u] = s^2 [1-(1-log(w))/w].
```

The source is not an unsolved special function. An exact particular solution and homogeneous basis
are

```text
u_part = 1-log(w),
v1 = w'/w,
v2 = 1-1/w.
```

Imposing `u(-1)=0` and the two registered other-end alternatives gives unique responses:

```text
u_D = 1-log(w) + v1/s + B_D v2,
B_D = -[W(1-log(W))+2s-1]/(W-1),

u_F = 1-log(w) + v1/s - v2/(2s-1),
W=w(1)=1-2s+2s^2.
```

The free response obeys the inhomogeneous natural condition
`w u'+w'u+log(w)w'=0` at the right endpoint. The homogeneous boundary determinants are nonzero for
`s>1`, so no zero mode was silently inverted.

The dimensionless Schur scalar is exactly `C+ell[u]`. Uniform outward interval range integration
over the entire certified root bracket gives:

| R05 p domain | dimensionless Schur enclosure | representative mu enclosure |
|---|---:|---:|
| both-end Dirichlet | `[8.3277421692, 8.3782560319]` | `[2.0819355423, 2.0945640080]` |
| crease Dirichlet / right free | `[8.0222182941, 8.0665676227]` | `[2.0055545735, 2.0166419057]` |

Both exclude zero positively. Combined with the frozen exact reduced-field index one, Sylvester
inertia gives joint index one on each R05 domain.

## 4. R06 exact negative witnesses

For odd zero angular traces the field-only rank-one correction is frozen evidence and makes the
reduced-field core positive. Rather than infer the joint sign from a converged eigenvalue, the
certificate supplies explicit degree-three rational polynomials. It sets

```text
p(x) = P_factor(x) sum_(k=0)^3 p_k x^k,
f'(x) = d/dx [(1-x^2) sum_(k=0)^3 f_k x^k],
mu = 1,
```

where `P_factor=1-x^2` on the both-end Dirichlet domain and `P_factor=1+x` on the free-right domain.
The angular primitive vanishes at both endpoints exactly. Coefficients are recorded as exact decimal
rationals in `NEGATIVE_WITNESS_CERTIFICATE.json`.

Uniform outward interval evaluation on `x in [-1,1]` and every `s in [1.68102,1.68103]` gives:

| R06 p domain | full joint-Q enclosure |
|---|---:|
| both-end Dirichlet | `[-0.6673532483, -0.6427961867]` |
| crease Dirichlet / right free | `[-1.4144177879, -1.3906077163]` |

Both are strictly negative. Because the frozen R06 field core is positive and adding one scalar
coordinate can change inertia by at most one, the joint index is exactly one on each R06 domain.

## 5. Numerical corroboration and validation discipline

`diagnostic_spectral.py` assembled the unreduced full joint Hessian independently in polynomial
spaces of sizes 9 through 33. It located the same branch split and joint index, but is explicitly
marked `CORROBORATION_ONLY`: convergence is not the proof.

The primary certificates use outward interval range enclosures. Each was run at 80 decimal digits
with 4,096 subintervals and at 100 digits with 8,192 subintervals. Every fine enclosure lies inside
its coarse enclosure and excludes zero with a large margin. The R05 differential identities are
also checked symbolically before integration.

## 6. What this does and does not say

This closes the F01 constant-lambda/mu Schur question on the four exact owned local domains. It
corrects the tempting interpretation that the R06 odd-pinned branch supplies a locally positive
joint survivor: its field core is positive, but its full joint space is not.

It does **not** close the independently free second-wall-germ curvature, assemble a full cell chain,
derive a physical boundary, establish time persistence, select the conditional P4 response, derive
a native action/carrier/matter source, or validate the global stability/bootstrap hypothesis.
