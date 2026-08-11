# G75 exact derivation — center-regular axial profile family

Date: 2026-08-11

Status: `INTERNALLY_REPLAYED_BOUNDED_LEAD`; fresh external adversarial review remains absent.

## 1. Declared control metric

G75 stays inside the preregistered stationary axial control envelope

```text
ds^2 = -A(x)c_E^2 dt^2 + R^2 dx^2/A(x)
       + R^2 x^2(dtheta^2 + sin^2(theta)dpsi^2)
       + 2 R c_E h(x) sin^2(theta) dt dpsi,
A(x)=1+a x^2, h(x)=x^2 q(x^2), x=r/R in [0,1].
```

This is a complete four-dimensional metric in the declared axial envelope. It is not the generic
ten-function complete coframe and it is not a selected physical cosmology. `R>0` remains symbolic;
`c_E` supplies the observed clock/ruler calibration only.

## 2. Exact finite family

Put `s=x^2` and start with

```text
p(s)=c0+c1 s+c2 s^2,
ci in {-2,-1,0,1,2}.
```

Keep each nonzero primitive integer ray once: the gcd of the nonzero absolute coefficients is one,
and the first nonzero coefficient is positive. Direct enumeration gives exactly 49 rays. For each
ray,

```text
M_p = max_{0<=s<=1}|p(s)|,
q(s)=epsilon p(s)/M_p,
epsilon in {1/20,1/5,1/2,1},
a in {-1/4,0,1/4}.
```

For a quadratic, the exact normalization candidates are `s=0`, `s=1`, and the vertex
`s=-c1/(2c2)` when it lies strictly between them. Thus every `M_p` is rational and no floating root
or optimizer enters. The 49 rays, four amplitudes, and three lapse controls give 588 nonzero-mixing
profiles. Adding the three matched `q=0` controls gives 591.

The partner `q -> -q` is retained analytically by the axial chart reflection `psi -> -psi`. This
identifies the same root/multiplicity and signature class; it is not a statement that two possible
physical orientations have been measured or selected.

## 3. Center smoothness

The lapse is an even analytic function of Cartesian radius. The radial spatial block can be written
as the Euclidean spatial metric plus

```text
(A(r)^(-1)-1) dr^2.
```

Because `(A^(-1)-1)/r^2` is analytic at `r=0`, this term is Cartesian smooth. For the axial cross
term, `h=x^2 q(x^2)` and

```text
r^2 sin^2(theta) dpsi = X dY - Y dX.
```

Consequently the apparent spherical-coordinate factor is an analytic Cartesian one-form multiplied
by the polynomial `q(r^2/R^2)`. Every one of the 591 controls is therefore `C-infinity` at the
center. This is why G75 is a new family rather than a repair of G74's twelve center-`C2`-blocked
profiles.

## 4. Lorentz signature

For all three lapse values,

```text
A(x) >= 3/4 > 0 on [0,1].
```

Away from ordinary spherical-coordinate axes, the spatial block is positive. Taking its Schur
complement in the time direction gives, up to positive unit factors,

```text
-A - h^2 sin^2(theta)/x^2 < 0.
```

Since `h=O(x^2)`, this also has a smooth center limit. Hence the declared metric has one timelike and
three spacelike directions throughout the cell; the coordinate degeneracies at the center and
polar axis are not metric degeneracies.

## 5. Exact shape classification

All roots and multiplicities are obtained from the exact quadratic. The 49 primitive rays split as:

| algebraic behavior | shapes |
|---|---:|
| persistent sign, no interior root | 28 |
| interior sign change | 9 |
| center-off, no interior root | 6 |
| endpoint taper, no interior root | 5 |
| zero at both boundaries, no interior root | 1 |

There is no even-multiplicity interior-touch member in this frozen coefficient lattice. That empty
class is an observed property of this 49-ray atlas, not a no-go for broader smooth profiles.

The exact stratum census is:

```text
C0_E0_O0_T0  28
C0_E0_O1_T0   8
C0_E1_O0_T0   4
C0_E2_O0_T0   1
C1_E0_O0_T0   5
C1_E0_O1_T0   1
C1_E1_O0_T0   1
C2_E0_O0_T0   1
```

Here `C` is the center order of `q` in `s`, `E` its endpoint-zero order, `O` the number of odd
interior roots, and `T` the number of even interior roots. Center orders are `41/7/1` for orders
`0/1/2`; endpoint orders are `43/5/1`; 40 shapes have no odd interior root and nine have one.

Three algebraic behaviors that were useful in interpreting the G74 obstruction occur here as new
even-center controls: `S21` is persistent, `S12` endpoint-tapered, and `S11` sign-changing. Their
existence does not select them for a sky solve.

## 6. Verification and maximum conclusion

The production derivation reports 10/10 exact checks. A separately written SymPy real-root-isolation
replay reconstructs all 49 rays and all 591 profile identities and passes 10/10 checks. The package
verifier passes 16/16, and all 10 hostile mutations are caught.

The maximum current conclusion is:

```text
CENTER_REGULAR_FAMILY_HAS_MULTIPLE_EXACT_SHAPE_STRATA
```

This is a bounded, role-neutral profile vocabulary. It derives no physical profile, source,
endpoint, scale, `X_max`, bootstrap rule, action, matter law, CMB spectrum, or polarization field.
Because no fresh blind external reviewer has yet audited G75, it remains a bankable bounded lead,
not an externally verified scientific result.
