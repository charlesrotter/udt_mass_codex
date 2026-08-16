# Exact derivation — complete screen Jacobi/Riccati propagation atlas

Date: 2026-08-16
Status: `EXTERNALLY_VERIFIED_WITH_CAVEATS__REPAIRS_VERIFIED__ORIGINAL_G108_LANDING_STANDS`

## 1. Bounded question

G107 showed that the weakest constant complete extension of the founded reciprocal character can
contain one common screen-dilation parameter `a`, while several stronger but currently unowned
complete gates remove it. The physical active carry of the complete coframe `E` and pair
realization `J` remained open.

This audit asks whether, after a complete metric history and a Jacobi-type observer query are
supplied, that apparent parameter is simply the propagated screen-area rate. It does not ask which
history, query, branch, initial screen, or depth profile is physical.

## 2. Complete-pair screen area

For the exact complete coframe and pair realization,

\[
E=\begin{pmatrix}B&0\\QS&Q\end{pmatrix},\qquad
J=\begin{pmatrix}Y\\Z\end{pmatrix},
\]

the physical screen block of `V=EJ` is

\[
\boxed{W=Q N,\qquad N=SY+Z.}
\]

On the regular rank-two screen stratum, its positive Gram matrix and area are

\[
C_\perp=W^TW=N^TQ^TQN,
\]

\[
\boxed{\mathcal A_\perp=\sqrt{\det C_\perp}=|\det W|.}
\]

This is invariant under a left orthonormal screen-frame rotation. It is also unchanged by any
exact redistribution `Q -> QM^-1`, `N -> MN` that keeps `W` fixed. Such a redistribution need not
preserve every gauge-fixing convention on `Q`; its role here is the hostile algebraic proof that
the physical scalar belongs to the product, not to either factor by itself.

Differentiating along an affine parameter `lambda` gives

\[
\frac{d\log\mathcal A_\perp}{d\lambda}
=\operatorname{tr}(\dot W W^{-1})
=\operatorname{tr}(\dot Q Q^{-1})
 +\operatorname{tr}(\dot N N^{-1}).                 \tag{1}
\]

Because

\[
\dot N=\dot S Y+S\dot Y+\dot Z,
\]

the screen shape/scale, all retained mixing entries—including any component historically called
`mu`—and the evolving pair realization contribute before the scalar is read. There is no lawful
separate post-processing orchestra in (1).

## 3. Jacobi and Riccati ownership

For a supplied geodesic or null screen query with a parallel orthonormal screen, let `W` be its
regular Jacobi screen map. The full metric curvature supplies the screen tidal matrix
`R_screen`, and

\[
\ddot W+R_{\rm screen}W=0.                            \tag{2}
\]

No GR field equation or matter equation is used: (2) is differential geometry of the supplied
metric and query.

Where `W` is invertible, define

\[
L=\dot W W^{-1}.
\]

Then (2) is exactly equivalent to

\[
\boxed{\dot L+L^2+R_{\rm screen}=0.}                 \tag{3}
\]

The trace

\[
\theta=\operatorname{tr}L
\]

is the affine logarithmic screen-area rate by (1).

## 4. Reciprocal-depth rate

Let the founded ordered depth along this supplied relation be a monotone function
`delta(lambda)` with `delta_dot != 0`. The scalar that matches G107's isotropic screen weight is

\[
\boxed{
a_{\rm eff}(\delta)
=\frac12\frac{d\log\mathcal A_\perp}{d\delta}
=\frac{\operatorname{tr}L}{2\dot\delta}.
}                                                     \tag{4}
\]

This result is dimensionless because `delta` is dimensionless. By contrast,

\[
\alpha_\lambda=\frac12\operatorname{tr}L
\]

has inverse-affine-parameter units. An affine rate must not be reported as a G107 weight until the
same relation owns or supplies `delta(lambda)`.

With

\[
K=W_{,\delta}W^{-1},\qquad
f=\frac{\ddot\delta}{\dot\delta^2},\qquad
T=\frac{R_{\rm screen}}{\dot\delta^2},
\]

the exact reparameterized equations are

\[
W_{,\delta\delta}+fW_{,\delta}+TW=0,                 \tag{5}
\]

\[
K_{,\delta}+K^2+fK+T=0.                              \tag{6}
\]

Since `a_eff=tr(K)/2`, tracing (6) gives

\[
\boxed{
2a_{\rm eff}' +\operatorname{tr}(K^2)
 +2f a_{\rm eff}+\operatorname{tr}T=0.
}                                                     \tag{7}
\]

Equation (7) shows why the rate is generally not a universal function of scalar distance alone:
it reads the full tidal, shear/rotation, reparameterization, branch, and initial-data history.
Symmetry can reduce those dependencies to one variable, but the reduction must be proved on the
branch in question.

## 5. Relation to the G107 constant family

For

\[
W(\delta)=e^{a\delta}R(b\delta)W_0,
\]

one has

\[
\mathcal A_\perp(\delta)
=e^{2a\delta}\mathcal A_\perp(0),
\]

and therefore

\[
a_{\rm eff}=a.
\]

The rotation rate `b` cancels from the area exactly. A changing screen-frame rotation also leaves
the trace rate invariant because its generator has zero trace.

Thus G107's determinant weight `a` is the constant special case of (4). Recovery of the full G107
matrix family requires, in an oriented orthonormal screen frame,

\[
\boxed{K=W_{,\delta}W^{-1}=aI_2+b\epsilon}
\]

with constant `a,b`. Equivalently, the symmetric trace-free part must vanish, the isotropic trace
must be constant, and the oriented antisymmetric rate must be the constant `b` (or be removed by
the declared screen-frame convention). Constant area rate alone is necessary but not sufficient:
a general propagated map can carry nonzero shear at the same constant determinant rate and then
recovers only the scalar determinant character.

The production controls demonstrate the broader behavior exactly:

| Tidal matrix | Jacobi map | `a_eff` for `delta=lambda` |
|---|---|---|
| `-kappa^2 I` | `cosh(kappa lambda) I` | `kappa tanh(kappa lambda)` |
| `+kappa^2 I` | `cos(kappa lambda) I` | `-kappa tan(kappa lambda)` before the first caustic |
| `diag(-p^2,+q^2)` | `diag(cosh(p lambda),cos(q lambda))` | `(p tanh(p lambda)-q tan(q lambda))/2` |

All three exact Jacobi residuals vanish. The independent solver integrates the second-order
Jacobi and first-order Riccati systems separately and agrees with the analytic maps and with each
other.

## 6. Active/passive resolution

The G107 ambiguity can now be stated precisely.

If the complete metric and query merely supply unrelated histories of `Q,S,Y,Z`, then the
coframe contribution

\[
\tfrac12\operatorname{tr}(\dot Q Q^{-1})
\]

can be increased, decreased, or cancelled by the realization contribution

\[
\tfrac12\operatorname{tr}(\dot N N^{-1}).
\]

It is not physical by itself.

If the supplied query identifies this same `W=QN` with the physical Jacobi screen map and ties it
to the initial-value problem (2), then their sum is fixed by the propagated metric and initial
data. The net `a_eff` is an output, not a fit coefficient.
This is the exact conditional sense in which the evolving metric determines the instrument's
volume.

It does not yet prove that UDT owns the physical Jacobi query, initial screen, branch, or
`delta(lambda)`. Those inputs are the remaining ownership boundary, not an extra free screen
amplitude after they are supplied.

## 7. Saved finite-path control replay

The frozen G68 control ensemble contains 21 full finite null-geodesic/Jacobi solves with saved
endpoint `D` and `Ddot`. Recomputing

\[
\alpha_\lambda=\tfrac12\operatorname{tr}(\dot D D^{-1})
\]

from those artifacts gives:

```text
regular finite rates                       21/21
F01 exact alpha_lambda=1/lambda residual   1.11e-15
determinant/trace area-identity residual   8.88e-16
alpha_lambda range                         1.2984280688 to 1.3438129665
maximum F02 shear Frobenius norm            9.7895911e-3
maximum twist Frobenius norm                2.73e-33
```

These numbers are in the normalized G68 affine units. They are not physical G107 coefficients.
They demonstrate only that a complete supplied metric/query history already produces a finite,
profile-dependent screen-volume rate and shear without a separately fitted `a`.

## 8. Independent verification

The independent implementation uses fixed numerical controls (`kappa=0.7`, `p=0.6`, `q=0.8`,
`lambda=0.8`) and integrates the exact matrix equations with DOP853 in float64. These values are
solver controls, not physical constants.

Maximum residuals are:

```text
Jacobi versus analytic map                 1.26e-15
Riccati versus Jacobi optical matrix       2.29e-16
Riccati versus analytic optical matrix     1.11e-16
reparameterized Riccati                    1.57e-16
screen-rotation invariance                 5.55e-17
Q/N factorization invariance               5.55e-17
finite-difference half-log-area rate       4.50e-11
independent versus production G68 rate     2.22e-16
```

Hostile checks also confirm that omitting `delta_dot` changes the answer for a nonlinear depth
parameter and that the general analytic controls have nonconstant rates. An exact
`W=e^(a lambda)I`, `R=-a^2 I`, `Wdot(0)=aI` witness realizes the constant-`a` special subfamily.

## 9. Degenerate and global strata

Equation (4) genuinely fails or branches when:

- `det W=0` at coincidence, a focal point, or a caustic;
- `delta_dot=0`, so reciprocal depth is not a valid local parameter;
- the screen ceases to be positive rank two;
- the query crosses a cut locus or changes path branch;
- no global screen section exists, although local area and trace can still be patched
  gauge-invariantly on regular overlaps.

The divergence of `a_eff` near a caustic is an optical degeneracy. It is not automatically
`X_max`, a physical wall, infinite signalling, or a source singularity.

## 10. Landing

```text
CONDITIONAL_SCREEN_DILATION_RATE_DERIVED_FROM_PROPAGATED_PAIR_AREA
__WHEN_QUERY_IDENTIFIES_THE_COMPLETE_PAIR_SCREEN_WITH_THE_JACOBI_MAP
__CONSTANT_A_IS_A_SPECIAL_PROPAGATION_SUBFAMILY
__SCREEN_ROTATION_REMAINS_ZERO_ORDER_GAUGE
__NO_INDEPENDENT_SCREEN_AMPLITUDE_REMAINS_AFTER_W_DELTA_AND_INITIAL_DATA_ARE_SUPPLIED
__METRIC_HISTORY_QUERY_INITIAL_DATA_BRANCH_AND_DEPTH_MAP_REMAIN_SUPPLIED
```

Premise stamps:

- `DERIVED_CONDITIONAL`: equations (1)--(7) and the identification of `a_eff` on a supplied regular
  Jacobi-type pair relation;
- `OBSERVED_CONDITIONAL`: the 21-row saved G68 affine-rate range;
- `DERIVED`: exact analytic controls, gauge cancellation, and constant-family reduction;
- `OPEN`: physical history, query, branch, initial data, depth map, global continuation, and any
  observational score.

This validates the proposed intuition in its precise conditional form. It does not yet turn
distance alone into a universal screen-volume law or select the physical UDT symphony.
