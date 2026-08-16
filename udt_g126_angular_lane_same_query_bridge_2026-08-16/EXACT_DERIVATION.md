# G126 exact derivation — angular-lane/same-query bridge map

Date: 2026-08-16

Status: `BLIND_VERIFIED_WITH_REPAIRS__PRODUCTION_15_OF_15__INDEPENDENT_12_OF_12`

## 1. Result first

The banked R5 angular observational lane does not currently provide an independently typed
constraint on G125's `K(R)` or full Jacobi phase on the exact G119 central-spherical query.

The obstruction has three exact parts:

1. G119's endpoint screen is angle preserving and isotropic at fixed radius;
2. G106's ideal per-depth reference removes the remaining pure radial abundance factor;
3. processed `Z` and even an exact `R(Z)` do not determine affine rate `K=dR/dlambda` or phase.

Thus the present bridge fails by object type, not by a poor numerical fit.

## 2. Exact spherical-screen content

On the declared G119 query,

\[
D_{\rm sky}=R O,
\qquad O\in O(2),
\qquad
D_{\rm sky}^{T}D_{\rm sky}=R^2I_2.
\tag{1}
\]

For angular tangent vectors `x,y`,

\[
(D_{\rm sky}x)\cdot(D_{\rm sky}y)=R^2(x\cdot y).
\tag{2}
\]

After normalization, their mutual angle is unchanged. Also

\[
|\det D_{\rm sky}|=R^2.
\tag{3}
\]

With a parallel screen frame, the phase derivative and optical generator are

\[
D'_{\rm sky}=K(R)O,
\qquad
D'_{\rm sky}D_{\rm sky}^{-1}=\frac{K(R)}R I_2,
\qquad
\theta_{\rm sky}=\frac{2K(R)}R.
\tag{4}
\]

Equation (4) has zero shear. It contains an expansion rate, but no direction-dependent angular
pattern on this exact central-spherical branch.

## 3. Reference projection removes the radial-only channel

At one processed-depth stratum, let `s(n)` be any normalized registered angular footprint and
suppose the spherical geometry multiplies it by a positive radial factor `a(Z)`. Normalizing within
that stratum returns the same `s(n)`. G106's ideal reference, which absorbs the depth marginal and
registered angular footprint, therefore gives

\[
p_Z-q_Z=0
\tag{5}
\]

for this pure radial/isotropic contribution. Its Landy--Szalay-style pair numerator is consequently
zero. This is not a claim about the actual finite survey random catalogue; it is the exact ideal
projection already banked by G106.

Therefore G105's lawful one-point kaleidoscope route requires a nonconstant angular Jacobian or
another nonradial/branch/source structure. The G119 exact spherical screen alone does not supply it.

## 4. `R(Z)` does not determine affine screen rate

Even with G125's conditional curve `R(Z)`, the chain rule gives only

\[
K(R)=\frac{dR}{d\lambda}
=\frac{dR}{dZ}\frac{dZ}{d\lambda}.
\tag{6}
\]

The conditional frozen P1 comparison map specifies `R(Z)`; the SNe data only tests its downstream
combined observable and derives neither `R(Z)` nor `dZ/dlambda`.
For the displayed G125 P1 curve, one explicitly vertex-normalized positive witness is

\[
u_1(Z)=\frac{Z^{2/n+1}}{2X},
\qquad
K_1(Z)=\frac{dR}{dZ}u_1(Z)=1.
\tag{7}
\]

For any positive `alpha`, define

\[
u_2(Z)=[1+\alpha(Z-1)]u_1(Z).
\tag{8}
\]

Both rates obey `u_i(1)=1/(2X)` and hence `K_i(1)=1` at the observer vertex, and both preserve the
identical endpoint curve `R(Z)`. Away from the vertex they give

\[
K_2(R)=[1+\alpha(Z-1)]K_1(R),
\tag{9}
\]

so the endpoint position block is unchanged while the phase derivative differs. This is an exact
data-type counterfamily; it does not assert that every member is a globally completed physical
metric history.

## 5. Why R5 cannot be inverted to the missing object

R5 inherits R2's explicitly preregistered Landy--Szalay reference projection and release-coordinate
windows: catalog two-point correlation curves binned in observer angle and observed-redshift
windows. It is not a saved `D_sky`, `D'_sky`, affine rate, or Jacobi phase.

The required forward chain is

```text
(complete history, source measure, observer query, branch family)
  -> one-source map Psi=(Z,n) and its Jacobian
  -> physical observed one-point measure p
  -> survey-reference projection against q
  -> two-point angular curve.
```

None of the arrows is invertible from the R5 curve alone. Even the elementary transformation
`m -> -m` preserves the quadratic autocorrelation `m tensor m`, so a two-point curve does not
uniquely recover its one-point modulation before one asks for `K` or phase.

G103 proves the stronger bounded local/source-measure freedom: while history, query realization,
and source pair measure remain supplied, no nontrivial source-independent angular pattern is owned
in its regular local class.

## 6. Lawful future bridge

An angular constraint on the same physical history remains possible, but it requires at least:

- a metric-owned nonspherical or displaced observer/source query related to the spherical
  background;
- a common complete history joining its angular differential to the G125 radius/frequency leg;
- physical source and branch measures;
- the actual reference-projection semantics or a separately justified idealization;
- and, for `K` or phase, an affine-frequency or phase-sensitive observable.

Those are not coefficients to fit into G126. They are the missing typed bridge.

## 7. Bounded landing

```text
NO_LAWFUL_CURRENT_R5_TO_K_OR_PHASE_BRIDGE
__EXACT_G119_SPHERICAL_SCREEN_IS_ANGLE_PRESERVING_AND_RADIAL_ONLY
__G106_REFERENCE_REMOVES_PURE_RADIAL_MODULATION
__PROCESSED_Z_AND_R_OF_Z_DO_NOT_OWN_AFFINE_RATE
__R5_TWO_POINT_OUTPUT_DOES_NOT_INVERT_TO_SCREEN_PHASE
__CONDITIONAL_NONSPHERICAL_HISTORY_SOURCE_REFERENCE_BRIDGE_OPEN
```

This is not a no-go for future angular constraints. No feature, rank, BAO origin, ruler, physical
history, transfer, `X_max`, CMB relation, action, bootstrap, matter, mass, or signalling result
follows.
