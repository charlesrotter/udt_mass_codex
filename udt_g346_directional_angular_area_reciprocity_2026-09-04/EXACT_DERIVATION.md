# G346 exact derivation — directional angular-area reciprocity

Date: 2026-09-04
Grade: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Bounded landing

```text
TWO_DIRECTIONAL_METRIC_ANGULAR_AREA_JACOBIANS_CLOSE
__SQUARED_FREQUENCY_REVERSAL_AND_INVERSE_G345_GEOMETRIC_MEAN
__EXACT_AFFINE_REFERENCE_GL2_ENDPOINT_RESET_AND_STATIONARY_SEWING
__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED
__NO_BRIGHTNESS_FLUX_LUMINOSITY_PROBABILITY_DISTANCE_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED
```

G346 selects preregistered alternatives `A`, `R1`, `G1`, `C1`, `S1`, `N1`, and `Q1`. Fresh
external `gpt-5.4` review independently reconstructed the load-bearing identities and accepted the
bounded result without required repair. This is an exact infinitesimal geometric result on one supplied
G340--G345 spacetime, normal-observer congruence, and labelled null-ray family. The metric,
completed-pair kernel, angular sector, and owner-provisional response equation are unchanged.

## 1. Metric sky opening and metric screen area

At endpoint `i`, let

\[
 \omega_i=-g(k,n_i)>0
\tag{1}
\]

be the frequency of the supplied null generator `k` measured by the supplied G340 normal observer.
Let `q_i` be the positive metric induced on the observer's quotient screen. A fixed-frequency
infinitesimal celestial-direction variation is a screen vector `theta_i`. Its canonical screen
covector is obtained by the metric musical map:

\[
 \boxed{p_i=\omega_i q_i\theta_i.}
\tag{2}
\]

In an orthonormal screen this is the G342 source normalization: unit sky opening gives unit
`p_i/omega_i`. In arbitrary canonical screen coordinates, `p_i` is a covector; it need not have the
same component transformation as `theta_i`.

The infinitesimal metric solid angle on the celestial-sphere tangent and metric screen area are

\[
 d\Omega_i=\sqrt{\det q_i}\,d^2\theta_i,
 \qquad
 dA_i=\sqrt{\det q_i}\,d^2x_i.
\tag{3}
\]

These are local metric area forms. No intensity, luminosity, detector, or electromagnetic transfer
has entered.

## 2. The two directional Jacobians

In G343 notation, at fixed source position `x_0=0`,

\[
 x_1=B_{10}p_0=B_{10}\omega_0q_0\theta_0.
\tag{4}
\]

Equations (3)--(4) give the positive directional metric angular-area Jacobian

\[
 \boxed{
 \mathscr A_{1\leftarrow0}
 ={dA_1\over d\Omega_0}
 =\omega_0^2|\det B_{10}|\sqrt{\det q_1\det q_0}.}
\tag{5}
\]

Applying the same construction at the other endpoint gives

\[
 \boxed{
 \mathscr A_{0\leftarrow1}
 ={dA_0\over d\Omega_1}
 =\omega_1^2|\det B_{01}|\sqrt{\det q_0\det q_1}.}
\tag{6}
\]

The absolute values make (5)--(6) orientation-free. If endpoint screen orientations are separately
chosen, the corresponding oriented determinant coefficient acquires their relative orientation
sign. In the G342/G343 matched transported orientation, `det B>0` for either endpoint order.

The integrands defining both diagonal entries of `B` have one sign on every noncoincident segment.
Both entries change sign together under endpoint reversal, so `det B>0` analytically throughout
the bounded domain. Thus both Jacobians are finite and strictly positive away from coincidence.

## 3. General screen-coordinate covariance

For arbitrary passive endpoint changes `R_i` in `GL(2)`,

\[
 x_i'=R_ix_i,
 \qquad \theta_i'=R_i\theta_i,
 \qquad p_i'=R_i^{-T}p_i,
\tag{7}
\]

\[
 q_i'=R_i^{-T}q_iR_i^{-1},
 \qquad B_{10}'=R_1B_{10}R_0^T.
\tag{8}
\]

Equation (2) is covariant because

\[
 \omega_iq_i'\theta_i'=R_i^{-T}(\omega_iq_i\theta_i).
\tag{9}
\]

Moreover,

\[
 |\det B_{10}'|=|\det R_1\det R_0|\,|\det B_{10}|,
\]

\[
 \sqrt{\det q_1'\det q_0'}
 ={\sqrt{\det q_1\det q_0}\over|\det R_1\det R_0|}.
\tag{10}
\]

The factors cancel in (5). The same holds for (6). The construction therefore needs no preferred
orthonormal endpoint frame.

## 4. Affine gauge, reference event, and reversal

Under one common affine rescaling `k -> a k`,

\[
 \omega_i\mapsto a\omega_i,
 \qquad B_{10}\mapsto a^{-1}B_{10}.
\tag{11}
\]

The frequency square and the two-dimensional determinant cancel exactly, leaving both (5) and (6)
unchanged. G343's marked-event conversion leaves `B` and the endpoint frequencies separately
unchanged, so no reference event or hidden scale remains.

In one common affine gauge,

\[
 B_{01}=-B_{10}^T,
 \qquad |\det B_{01}|=|\det B_{10}|.
\tag{12}
\]

Therefore

\[
 \boxed{
 {\mathscr A_{1\leftarrow0}\over\mathscr A_{0\leftarrow1}}
 =\left({\omega_0\over\omega_1}\right)^2.}
\tag{13}
\]

This is directional reciprocity, not equality. It is determined by the metric frequency ratio
already derived in G340/G343; no transfer law supplies it.

Now choose unit frequency at endpoint zero and put

\[
 \alpha_{01}={\omega_1\over\omega_0},\qquad\omega_0=1.
\tag{14}
\]

G343 gives the separately source-normalized reverse block

\[
 B_{01}^{[1]}=-\alpha_{01}[B_{10}^{[0]}]^T.
\tag{15}
\]

Consequently

\[
 \boxed{
 \mathscr A_{0\leftarrow1}^{[1]}
 =\alpha_{01}^2\mathscr A_{1\leftarrow0}^{[0]}.}
\tag{16}
\]

Equations (13) and (16) are the same law in two correctly typed affine conventions.

## 5. Exact relation to the G345 scalar

G345's accepted scalar is

\[
 \widehat\Delta_{10}
 ={1\over
 |\det B_{10}|\omega_1\omega_0\sqrt{\det q_1\det q_0}}.
\tag{17}
\]

Using (5), (6), and (12),

\[
 \boxed{
 \sqrt{\mathscr A_{1\leftarrow0}\mathscr A_{0\leftarrow1}}
 ={1\over\widehat\Delta_{10}}.}
\tag{18}
\]

Thus G345 was not an unrelated scalar: its inverse is exactly the symmetric geometric mean of the
two metric directional angular-area Jacobians. If

\[
 r_{10}={\omega_0\over\omega_1},
 \qquad \mathscr G_{10}={1\over\widehat\Delta_{10}},
\tag{19}
\]

then

\[
 \boxed{
 \mathscr A_{1\leftarrow0}=\mathscr G_{10}r_{10},
 \qquad
 \mathscr A_{0\leftarrow1}={\mathscr G_{10}\over r_{10}}.}
\tag{20}
\]

This factorization separates the reversal-symmetric beam geometry from the endpoint clock
asymmetry. It does not select a physical route, distance protocol, or observer population.

## 6. Exact stationary sewing

For three nonidentity endpoints on the same labelled ray in one common affine gauge, G344 gives

\[
 H_1=B_{21}^{-1}B_{20}B_{10}^{-1}.
\tag{21}
\]

Taking determinants,

\[
 |\det B_{20}|=|\det H_1|\,|\det B_{21}|\,|\det B_{10}|.
\tag{22}
\]

Define the G345 normalized join scalar

\[
 \widehat h_1={|\det H_1|\over\omega_1^2\det q_1}.
\tag{23}
\]

Substitution of (5) into (22) proves the directional law

\[
 \boxed{
 \mathscr A_{2\leftarrow0}
 =\widehat h_1
 \mathscr A_{2\leftarrow1}\mathscr A_{1\leftarrow0}.}
\tag{24}
\]

The reverse order obeys the analogous formula. Taking the geometric mean of the two directions
recovers

\[
 \mathscr G_{20}=\widehat h_1\mathscr G_{21}\mathscr G_{10},
\tag{25}
\]

which is exactly the inverse of G345's scalar sewing law. Bare multiplication is false in general:
the intermediate screen must be stationary-eliminated. When the outer endpoints coincide, the
total map is the identity and both the type-I endpoint chart and `H_1` are singular, as in G344.

## 7. Reference-free mixed-direction formula

Put

\[
 h_i=\sqrt{T_i^2+\lambda^2},
\]

\[
 J_\parallel=\int_{T_0}^{T_1}
 {u^{4/3}\over(u^2+\lambda^2)^{3/2}}\,du,
 \qquad
 J_Z=\int_{T_0}^{T_1}
 {u^{-2/3}\over\sqrt{u^2+\lambda^2}}\,du.
\tag{26}
\]

G343/G345 give

\[
 \mathscr G_{10}
 ={h_0^2h_1^2|J_\parallel J_Z|\over(T_0T_1)^{1/3}},
 \qquad
 r_{10}=\left({T_1\over T_0}\right)^{2/3}{h_0\over h_1}.
\tag{27}
\]

The arbitrary common affine normalization and marked reference event have cancelled. Equations
(20) and (27) are the complete mixed-direction answer.

## 8. Both principal limits and coincidence

For the longitudinal principal family, let

\[
 d=T_1^{2/3}-T_0^{2/3}.
\]

Then

\[
 \boxed{
 \mathscr A_{1\leftarrow0,X}={9\over4}T_0^{2/3}d^2,
 \qquad
 \mathscr A_{0\leftarrow1,X}={9\over4}T_1^{2/3}d^2.}
\tag{28}
\]

For the transverse principal family define

\[
 P=\left|(T_1^{7/3}-T_0^{7/3})(T_1^{1/3}-T_0^{1/3})\right|.
\tag{29}
\]

Then

\[
 \boxed{
 \mathscr A_{1\leftarrow0,\perp}={9\over7}P{T_1^{1/3}\over T_0},
 \qquad
 \mathscr A_{0\leftarrow1,\perp}={9\over7}P{T_0^{1/3}\over T_1}.}
\tag{30}
\]

Both screen directions remain present in both limits. For
`epsilon=T_1-T_0 -> 0`, G343's local identity behavior and the endpoint frequency attachment give

\[
 \boxed{
 \mathscr A_{1\leftarrow0}=|\epsilon|^2(1+O(\epsilon)),
 \qquad
 \mathscr A_{0\leftarrow1}=|\epsilon|^2(1+O(\epsilon)).}
\tag{31}
\]

The directional areas vanish quadratically at coincidence while G345's inverse-area scalar has the
corresponding quadratic pole. This is the identity boundary of the endpoint generating chart, not
an interior caustic.

## 9. Compact labels and exact remaining dependence

Every supplied compact lift `L` retains its own pair

\[
 (\mathscr A_{1\leftarrow0,L},\mathscr A_{0\leftarrow1,L}).
\tag{32}
\]

Nothing in G346 sums, weights, identifies, or physically selects lifts. Each Jacobian still depends
on the supplied spacetime, endpoint observer congruence, endpoint events, projective ray direction,
and path label. Coordinate and affine invariance remove bookkeeping; they do not remove physical
observer or ray dependence.

## 10. Evidence and ownership

The frozen production route passed `11204/11204` checks. Its largest affine, endpoint-reset,
general-screen, geometric-mean, mixed-formula, principal, reference, reversal, and stationary-sewing
relative errors were respectively
`4.0225473063105635e-16`, `2.98457122214132e-16`,
`1.7710785995225723e-15`, `4.987843226005652e-16`,
`1.2212453270876722e-15`, `3.774758283725532e-15`,
`7.105427357601002e-15`, `1.7609972333806675e-15`, and
`3.542999227335031e-14`.

An implementation-distinct verifier rebuilt the `lambda-gamma` scalar fundamental bases with
Simpson-log quadrature, constructed the sky musical map explicitly, recomputed both endpoint-unit
gauges independently, and integrated Jacobi columns directly with log-time RK4. It imported no
production or G342--G345 implementation and passed `4251/4251`; its largest error was the full
block composition error `9.98350167131679e-11`. All twenty hostile mutations were caught.

This is metric-derived infinitesimal causal geometry **conditional on** the supplied exact
spacetime, supplied normal observers, supplied fixed labelled ray, and owner-provisional vacuum
premises underlying that arena. It is not a finite-beam theorem, light-transfer law, brightness,
flux, luminosity, probability, amplitude, selected observational distance, selected route or
observer population, generic spacetime result, stability result, matter/mass law, physical scale,
`X_max`, or canon. External acceptance does not widen any of these boundaries. Documentary and
text-token guards remain integrity scaffolding rather than substantive mathematical proof.
