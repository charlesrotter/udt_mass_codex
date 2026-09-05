# G347 exact derivation — arbitrary endpoint-observer angular-area covariance

Date: 2026-09-04
Status: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Bounded landing

```text
EXACT_FINITE_TIMELIKE_ENDPOINT_OBSERVER_COVARIANCE_CLOSES
__QUOTIENT_SCREEN_ISOMETRY_AND_INVERSE_FREQUENCY_SKY_CONFORMALITY
__SOURCE_DOPPLER_SQUARED_DIRECTIONAL_AREAS
__SQUARED_FREQUENCY_REVERSAL_INVERSE_G345_MEAN_AND_STATIONARY_SEWING_RETAIN_COVARIANT_FORM
__NO_PREFERRED_OBSERVER_LIGHT_DISTANCE_POPULATION_SCALE_OR_XMAX_SELECTED
```

G347 selects preregistered alternatives `A`, `Q1`, `S1`, `A1`, `R1`, `G1`, `N1`, `B1`, and
`P1`. Fresh external `gpt-5.6-sol` review independently accepted the bounded result without
required repair. This is an exact local-observer extension of G346 on the same supplied
G340--G346 spacetime and labelled null-ray family. The metric, reciprocal kernel,
angular sector, and owner-provisional response equation are unchanged.

## 1. Observer screens from the metric quotient

At one endpoint let `k` be a nonzero future null vector and let `u` be any future unit timelike
observer. Define

\[
 \omega_u=-g(k,u)>0,
 \qquad s_u={k\over\omega_u}-u.
\tag{1}
\]

Then `s_u` is unit spacelike and orthogonal to `u`. The observer screen is

\[
 S(u,k)=\{X:g(X,u)=g(X,k)=0\}.
\tag{2}
\]

The intrinsic null screen is the quotient

\[
 Q_k=k^\perp/\operatorname{span}(k),
\tag{3}
\]

with positive metric inherited from `g`. Every quotient class has the unique representative in
`S(u,k)`

\[
 \pi_u[X]=X+{g(X,u)\over\omega_u}k.
\tag{4}
\]

Equation (4) is independent of the starting representative: replacing `X` by `X+c k` cancels the
added `c k` exactly. Nullity and `g(X,k)=0` also give

\[
 g(\pi_u[X],\pi_u[Y])=g(X,Y).
\tag{5}
\]

For a second future unit observer `v`, the observer-screen change is therefore

\[
 \boxed{I_{v\leftarrow u}X
 =X+{g(X,v)\over\omega_v}k},
 \qquad X\in S(u,k).
\tag{6}
\]

It is a metric isometry. Direct substitution proves

\[
 I_{u\leftarrow v}I_{v\leftarrow u}=1,
 \qquad
 I_{w\leftarrow v}I_{v\leftarrow u}=I_{w\leftarrow u}.
\tag{7}
\]

Thus changing observers changes the representative two-plane inside the tangent space, not the
metric quotient screen or its area.

## 2. Exact local sky transformation

A tangent to `u`'s celestial sphere is a vector `\theta_u\in S(u,k)`. Choose the fixed-frequency
representative of the projective null variation,

\[
 \delta k=\omega_u\theta_u.
\tag{8}
\]

Observer `v` assigns direction `s_v=k/\omega_v-v`, where

\[
 \delta\omega_v=-g(\delta k,v).
\tag{9}
\]

Differentiating `s_v` and using (6) yields

\[
 \boxed{\theta_v=\delta s_v
 ={\omega_u\over\omega_v}I_{v\leftarrow u}\theta_u.}
\tag{10}
\]

Because `I` is an isometry, the celestial tangent metric and its two-dimensional area form obey

\[
 q_v(\theta_v,\eta_v)
 =\left({\omega_u\over\omega_v}\right)^2q_u(\theta_u,\eta_u),
\tag{11}
\]

\[
 \boxed{d\Omega_v
 =\left({\omega_u\over\omega_v}\right)^2d\Omega_u.}
\tag{12}
\]

This is derived from the local metric normalization; no external aberration or optical theorem is
used.

Relative to a chosen normal reference observer, every future unit timelike observer has a unique
finite boost description

\[
 v=\gamma(u+\beta),\qquad \gamma=(1-|\beta|^2)^{-1/2},\qquad |\beta|<1.
\tag{13}
\]

Writing `k=\omega_u(u+s_u)` gives the positive factor

\[
 \boxed{D_{v\leftarrow u}:={\omega_v\over\omega_u}
 =\gamma(1-\beta\mathbin\cdot s_u)>0.}
\tag{14}
\]

Equations (10)--(14) cover longitudinal, transverse, and oblique finite boosts, not only a
collinear case.

## 3. Bilocal quotient transport does not acquire an observer force

G343's position block is intrinsically a map between the two endpoint quotient screens. Replacing
`u_i` by `v_i` composes that same map with the isometries (6) and their metric duals. In screen
bases transported by those isometries its matrix is unchanged. In arbitrary passive endpoint
coordinates its already-derived law remains

\[
 B'_{10}=R_1B_{10}R_0^T,
 \qquad q_i'=R_i^{-T}q_iR_i^{-1}.
\tag{15}
\]

The determinant and metric-area factors in G346 continue to cancel. No target-observer Doppler
factor appears in the area of the intrinsic endpoint quotient screen. A material detector plane
would be additional structure and is not present here.

## 4. Both directional angular-area transformations

Let the original endpoint observers be `u_0,u_1`, the replacements be `v_0,v_1`, and set

\[
 D_i={\omega_{v_i}\over\omega_{u_i}}>0.
\tag{16}
\]

The metric screen area at the target is preserved by (6), while the source solid angle transforms
by (12). Therefore G346's two directional Jacobians obey

\[
 \boxed{
 \mathscr A'_{1\leftarrow0}=D_0^2\mathscr A_{1\leftarrow0},
 \qquad
 \mathscr A'_{0\leftarrow1}=D_1^2\mathscr A_{0\leftarrow1}.}
\tag{17}
\]

The source endpoint, not the target endpoint, supplies each factor. The Jacobians are covariant,
not numerically observer invariant. Production exhibited 600 cases with a nontrivial numerical
change; no preferred observer was inferred.

## 5. Reversal and the G345 mean retain their form

G346 gives in a common affine gauge

\[
 {\mathscr A_{1\leftarrow0}\over\mathscr A_{0\leftarrow1}}
 =\left({\omega_{u_0}\over\omega_{u_1}}\right)^2.
\tag{18}
\]

Using (17),

\[
 \boxed{
 {\mathscr A'_{1\leftarrow0}\over\mathscr A'_{0\leftarrow1}}
 =\left({\omega_{v_0}\over\omega_{v_1}}\right)^2.}
\tag{19}
\]

Thus the numerical ratio changes, while the squared-frequency reversal law does not.

G345's observer-calibrated scalar transforms as

\[
 \boxed{
 \widehat\Delta'_{10}
 ={\widehat\Delta_{10}\over D_0D_1}.}
\tag{20}
\]

Combining (17), (20), and G346 gives

\[
 \boxed{
 \sqrt{\mathscr A'_{1\leftarrow0}\mathscr A'_{0\leftarrow1}}
 ={1\over\widehat\Delta'_{10}}.}
\tag{21}
\]

The inverse-G345 mean is therefore observer covariant, not an observer-independent number.

## 6. Stationary sewing

For a three-endpoint join, G346 has

\[
 \mathscr A_{2\leftarrow0}
 =\widehat h_1\mathscr A_{2\leftarrow1}\mathscr A_{1\leftarrow0},
 \qquad
 \widehat h_1={|\det H_1|\over\omega_1^2\det q_1}.
\tag{22}
\]

Changing the middle observer by `D_1` leaves the metric quotient Hessian unchanged and gives

\[
 \boxed{\widehat h'_1={\widehat h_1\over D_1^2}.}
\tag{23}
\]

The source factors cancel at the join:

\[
 \boxed{
 \mathscr A'_{2\leftarrow0}
 =\widehat h'_1\mathscr A'_{2\leftarrow1}\mathscr A'_{1\leftarrow0}.}
\tag{24}
\]

Leaving `hhat_1` unchanged or multiplying it by `D_1^2` is false. Bare multiplication remains false
for the same stationary-elimination reason as G344--G346.

## 7. Gauge, principal directions, compact labels, and boundary

Under a common affine rescaling `k -> a k`, both `\omega_u` and `\omega_v` gain `a`, so every `D_i`
is unchanged. The position block gains `a^{-1}` and both final directional areas remain affine
invariant. Equation (15) proves general endpoint `GL(2)` covariance. Production checked both
principal ray families and every mixed projective direction without deleting either screen
component.

Each supplied compact lift retains its own `k_L`, endpoint directions, Doppler factors, quotient
propagator, and directional-area pair. Nothing here sums, weights, identifies, or selects lifts.

Every finite `|\beta|<1` gives `D>0`. The boundary is not uniformly regular. If an observer chases
the ray with `\beta\to s`, then `D\to0`, `d\Omega_v/d\Omega_u\to\infty`, and the corresponding
source angular-area Jacobian tends to zero. If `\beta\to-s`, the reciprocal behavior occurs.
A null vector is not a unit timelike observer, so `|\beta|=1` is classified as a singular boundary,
not appended to the domain.

At endpoint coincidence the G346 areas still vanish quadratically; equation (17) only multiplies
that behavior by the finite positive source factor for every included observer.

## 8. Evidence and ownership

The frozen production route passed `73924/73924` checks, including 1,200 boosts with speed above
`0.99`, 80 longitudinal and 80 transverse principal cases, mixed directions, independent endpoint
changes, affine scales, arbitrary endpoint `GL(2)` frames, reversal, G345 mean, and stationary
sewing. All normalized errors were below the preregistered tolerances.

An implementation-distinct verifier used a rapidity chart, independently reconstructed the
Lorentz quotient projection, checked 206 celestial derivatives by a five-point finite difference,
rebuilt reference-free bilocal blocks by Simpson integration, and passed `23547/23547`. It imported
no production or G340/G343/G345/G346 implementation. All 22 hostile mutations were caught.

External acceptance does not widen any of these boundaries. This is exact metric-derived
infinitesimal causal geometry **conditional on** the supplied exact
spacetime, supplied labelled null ray, endpoint events, and owner-provisional vacuum premises. It
does not select an observer population or preferred frame. It is not finite-beam evolution, a
light-transfer law, detector response, brightness, flux, luminosity, probability, observational
distance, physical route, generic spacetime theorem, stability, occupancy, matter/mass, physical
scale, `X_max`, or canon.
