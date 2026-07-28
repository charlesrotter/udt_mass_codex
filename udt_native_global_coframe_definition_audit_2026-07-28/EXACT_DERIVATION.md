# Exact derivation and non-uniqueness controls

## 1. Founded pair and the full Lorentz commutant

On the founded clock/ruler pair the infinitesimal reciprocal action is

`H = diag(-1,+1)`.

Solving `[X,L]=0` for a generic real four-by-four `X` and all six generators `L` of the full
Lorentz algebra leaves a one-dimensional commutant: scalar multiples of the identity. This proves
that a single non-scalar reciprocal plane cannot be invariant under every Lorentz transformation.
Observer equivalence must therefore act equivariantly on the observer-selected pair; it cannot mean
one fixed preferred plane.

## 2. Sharp pointwise physical extension

Fix an ordered timelike/spacelike physical pair, its orthogonal two-dimensional screen, the exact
pair action `H`, metric self-adjointness, and `SO(2)` covariance on the screen. Solving the complete
linear system gives

`X_lambda = diag(-1,+1,lambda,lambda)`.

Exactly one real modulus remains. The finite response is

`P_lambda(phi) = exp(phi X_lambda)`

and obeys

`P_lambda(phi) P_lambda(psi) = P_lambda(phi+psi)`

for every real `lambda`. Its trace is `2 lambda`; sample spectra
`(-1,1,-1,-1)`, `(-1,1,0,0)`, `(-1,1,1,1)`, and `(-1,1,2,2)` are distinct. Thus group
composition, pair reciprocity, self-adjointness, and screen covariance do not select `lambda`.

Complete trace zero would choose `lambda=0`, but complete trace zero is not derived by the current
foundation and is therefore an additional premise, not a result.

## 3. One coherent complete non-ultrastatic family

Use global Maurer-Cartan forms `sigma_i` on `S3`, with
`d sigma_3 = kappa sigma_1 wedge sigma_2`, and define on `R x S3`

```
tau     = c_E dt + a sigma_3
theta_0 = exp(-phi) tau
theta_1 = R exp(+phi) sigma_3
theta_2 = R exp(lambda phi) sigma_1
theta_3 = R exp(lambda phi) sigma_2
g       = -theta_0^2 + theta_1^2 + theta_2^2 + theta_3^2.
```

Relative to `(c_E dt,sigma_3,sigma_1,sigma_2)`, direct determinant evaluation gives

```
det E = R^3 exp(2 lambda phi)
det g = -R^6 exp(4 lambda phi).
```

Hence the coframe is nondegenerate and Lorentzian for every smooth finite `phi`, real `lambda`, and
positive `R`. A constant-time slice is spacelike exactly where

`R^2 exp(2 phi) - a^2 exp(-2 phi) > 0`.

For the stationary field `K=partial_t`, the physical norm is

`g(K,K) = -c_E^2 exp(-2 phi)`,

so, once this stationary line is supplied or intrinsically selected, its norm ratio gives

`delta_K(p,q) = phi(q)-phi(p)`.

When `a kappa` is nonzero, the Killing twist is proportional to `theta_1` and therefore selects the
reciprocal ruler direction within this configuration. The prior source does not prove that `K` is
the unique timelike Killing line in this same family. Its separate generic-lapse witness proves
line uniqueness but not the ruler; those witnesses are not spliced here.

This family proves compatible global existence, not native selection. It contains all real
`lambda`, arbitrary smooth admissible `phi`, twist amplitude `a`, and scale `R`, and it is off shell.

## 4. Composition does not select depth

For any scalar function `f` on the chosen comparison objects,

`delta_f(p,q)=f(q)-f(p)`

satisfies neutrality, reversal, and

`delta_f(p,q)+delta_f(q,r)=delta_f(p,r)`.

The zero function and infinitely many nonzero functions all pass. Therefore the groupoid law is a
consistency condition on a supplied depth; it is not a metric-native depth selector. A physical
observer/event/path assignment and a rule obtaining `f` from the complete geometry remain open.

## 5. Scalar anchors do not select shape

For monomials `c_E^alpha G_obs^beta`, the dimensional exponent matrix in `(L,M,T)` is

```
[ 1  3]
[ 0 -1]
[-1 -2].
```

It has rank two and zero nullity. There is no nontrivial dimensionless monomial made from `c_E` and
`G_obs` alone. In particular, those anchors cannot choose dimensionless `lambda`, a dimensionless
profile, topology, or join data. They also cannot form an absolute length without an additional
native dimensional quantity. This does not remove `c_E` from the metric; it distinguishes observed
calibration from construction-law selection.

## 6. Minimal selector decomposition

The exact countercontrols separate three kinematic operations:

1. `S01`: physical comparison base plus metric-native signed depth;
2. `S02`: finite reciprocal lift plus transverse/mixing response;
3. `S03`: global descent, completion, and causal-interface law.

An on-shell physical branch additionally needs `S04`, native equations or an equivalent
whole-solution closure. Absolute physical scale additionally needs `S05`, native placement of
`G_obs` or another dimensional relation. The word *selector* here names a missing mathematical
operation; it does not license inventing a postulate.
