# G83 exact derivation

## 1. Metric and ownership

The banked G75 stationary control family is

\[
ds^2=-A(x)c_E^2dt^2+\frac{R^2}{A(x)}dx^2
+R^2x^2(d\theta^2+\sin^2\theta\,d\psi^2)
+2Rc_Eh(x)\sin^2\theta\,dt\,d\psi,
\]

with

\[
A(x)=1+a x^2,\qquad h(x)=x^2q(x^2).
\]

The 591 G75 rows are `CHOSE_CONTROL`, not selected physical profiles. Their registered domain is `0<=x<=1`. The continuation below is `FREE_AND_EXPLORED`: it preserves the exact formula but does not claim that the G75 construction owned the region `x>1`.

## 2. Strict registered-domain result

For `a in {-1/4,0,+1/4}`,

\[
\min_{0\le x\le1}A(x)\in\{3/4,1,1\}>0.
\]

Therefore every one of the 591 registered profiles has a finite stationary endpoint ratio at the G75 control surface `x=1`. No G75 row realizes infinite stationary reciprocal depth on its declared domain.

This is `DERIVED_WITHIN_THE_G75_CONTROL_DOMAIN`. It does not say that UDT lacks an observer-pair asymptote.

## 3. Transparent lapse continuation

The three lapse families behave differently if the same formulas are continued to positive `x`:

\[
A_-(x)=1-\frac{x^2}{4},\qquad A_0(x)=1,\qquad
A_+(x)=1+\frac{x^2}{4}.
\]

Only `AM` has a positive lapse zero, at `x=2`. For a fixed stationary receiver `x_r<2` and a continued source `x_s<2`, the G79 stationary Killing-observer readout gives

\[
\phi_{\rm pair}(x_r,x_s)
=\frac12\log\frac{A(x_r)}{A(x_s)},
\]

and the terminal reciprocal calibration gives conditionally

\[
\frac{c_{\rm eff}(x_s)}{c_{\rm eff}(x_r)}
=e^{-2\phi_{\rm pair}}
=\frac{A(x_s)}{A(x_r)}.
\]

Hence, on this stationary continuation,

\[
x_s\to2^-\quad\Longrightarrow\quad
\phi_{\rm pair}\to+\infty,
\qquad
\frac{c_{\rm eff}(x_s)}{c_{\rm eff}(x_r)}\to0.
\]

That is an exact stationary asymptote candidate. It is not yet the physical `X_max`: `x` is a chart/control variable, `R` is unselected, the source surface is unowned, and no global observer-pair separation operator has been supplied.

`A0` and `AP` have no positive stationary lapse zero. This classifies those two lapse ansatz continuations only; it does not exclude a different global pair relation from realizing `X_max`.

## 4. Why radial proper length does not close `X_max`

For the AM radial stationary slice,

\[
\frac{\ell(x_r,x_s)}{R}
=\int_{x_r}^{x_s}\frac{dx}{\sqrt{1-x^2/4}}
=2\left[\arcsin\frac{x_s}{2}-\arcsin\frac{x_r}{2}\right].
\]

The candidate limit is finite:

\[
\lim_{x_s\to2^-}\frac{\ell}{R}
=\pi-2\arcsin\frac{x_r}{2}.
\]

But

\[
\frac{d}{dx_r}\left(\pi-2\arcsin\frac{x_r}{2}\right)
=-\frac{2}{\sqrt{4-x_r^2}}\ne0.
\]

Thus this one-sided radial proper length depends on the receiver chart position. It is not, by itself, the frame-shared maximum distance between two observers. A pair-recentering or global-completion rule is still required.

## 5. Complete path result

The lapse calculation does not exhaust the metric. G83 continued all 197 AM G75 rows—zero mixing plus every polynomial shape and amplitude—to three fixed lapse levels:

\[
A_s\in\{2^{-4},2^{-8},2^{-12}\},
\qquad x_s=2\sqrt{1-A_s}.
\]

The complete 32-state null-geodesic, transported-screen, and Jacobi system retained `h=x^2q(x^2)` and all induced metric mixing. From the fixed receiver `x_r=1/4`, the 591 paths classified as:

| status | rows |
|---|---:|
| `ENDPOINT_REGULAR_NO_CAUSTIC` | 516 |
| `TURNING_NO_ENDPOINT` | 18 |
| `AFFINE_CAP_NO_ENDPOINT` | 57 |
| solver/nonfinite failure | 0 |

All 516 reached rows passed every preregistered raw residual threshold. Their maxima were:

| residual | maximum |
|---|---:|
| null | `2.204e-14` |
| screen Gram | `1.981e-11` |
| screen-ray orthogonality | `3.371e-10` |
| stationary `p_t` | `3.602e-11` |
| axial `p_psi` | `7.541e-13` |

The six profiles that turned did so at all three approach levels. Ten profiles hit the affine cap at all three levels; twelve first reached at `2^-4` but hit the cap at `2^-8` and `2^-12`; three reached through `2^-8` but hit the cap at `2^-12`; 166 reached all three surfaces.

This is the main structural result: the AM lapse supplies one common stationary endpoint asymptote candidate, but complete observer-ray accessibility remains profile dependent once the angular/mixing orchestra is active. The scalar lapse endpoint and the path/screen channels are related but not interchangeable.

The 75 unreached rows are not no-go results. `AFFINE_CAP_NO_ENDPOINT` is explicitly a bounded numerical status, and the G75 polynomials were normalized only on `0<=x<=1`; their continuation to `x>1` is exploratory.

## 6. Independent gates

- Exact SymPy reconstruction independently proved the lapse/source identity, the divergent reciprocal depth, the vanishing conditional `c_eff` ratio, and the receiver-dependent finite proper-length limit.
- Eighteen stratified Radau replays covered zero mixing and every represented behavior class at all three approach levels. All 18 matched the DOP853 endpoint status, affine endpoint, and screen determinant within `1e-7`.
- This Radau check is an independent solver-family replay, not an independent geometry implementation. The exact scalar proof is the independent load-bearing check for the asymptote statement.

## 7. Landing

`BOUNDED_STATIONARY_ENDPOINT_ASYMPTOTE_CANDIDATE_ATLAS`

The AM continuation realizes the defining divergence pattern of an `X_max` candidate within a stationary chart, and the complete angular/mixing sector materially changes path accessibility to its neighborhood. Physical `X_max`, its numerical value, its observer-pair re-centering, the scale `R`, a source surface, and global completion all remain `OPEN`.
