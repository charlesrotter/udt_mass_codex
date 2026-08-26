# G265 exact derivation — infinite-bare-c and mutual pair null closure

Date: 2026-08-26

## Primary landing

```text
INFINITE_BARE_C_METRIC_NULL_READING_IS_IDENTITY
__LITERAL_DISTANCE_TIME_CLOSURE_TRIVIALIZES_THE_STATIC_PROFILE
__SAME_CORRESPONDENCE_MUTUAL_SLOWDOWN_IS_NOT_THE_SIGNED_NULL_ARROW
__THE_RECIPROCAL_KERNEL_ALREADY_CONTAINS_DISTINCT_EVEN_AND_DIRECTIONAL_CHANNELS
__DISTANCE_OWNERSHIP_STILL_REQUIRES_A_TIMELIVE_OR_TWO_POINT_VALUE_LAW
```

This is a bounded static-radial classification. It does not reject the original infinite-bare-`c`
or mutual-distance postulates. It shows exactly what they do and do not force in the current
primary metric realization.

## 1. Metric null delay

Use

\[
ds^2=-f(r)c_E^2dt^2+\frac{dr^2}{f(r)}+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0,
\qquad N=\sqrt f=e^{-\phi}.
\]

On a radial future-null branch,

\[
0=-fc_E^2dt^2+\frac{dr^2}{f}
\]

gives

\[
\boxed{c_E\frac{dt}{|dr|}=\frac1f.}
\]

For endpoints in one regular interval, define

\[
D_{\rm opt}(A,B)=\int_A^B\frac{|dr|}{f(r)},
\qquad
\ell(A,B)=\int_A^B\frac{|dr|}{\sqrt{f(r)}}.
\]

Then

\[
\boxed{c_E\Delta t=D_{\rm opt}.}
\]

This is an exact null-cone identity for every positive `f`. Writing a proposed bare contribution as

\[
\Delta t_{\rm obs}=\Delta t_{\rm bare}+\Delta t_g,
\qquad c_{\rm bare}^{-1}=0,
\]

and setting `Delta t_g=D_opt/c_E` adds zero to the existing metric evaluator. It rejects none of the
G264 profiles. Therefore the statement “all observed delay is metric-owned” is meaningful
provenance, but not yet a value equation.

The local static observer proper time and radial proper length satisfy

\[
d\tau=Ndt,
\qquad d\ell=\frac{|dr|}{N}.
\]

Using the null relation,

\[
\boxed{\frac{d\ell}{d\tau}=c_E.}
\]

Thus W4's local measured speed is exactly `c_E` for every positive `f`. The coordinate-null speed

\[
\frac{|dr|}{dt}=c_Ef
\]

is not a second local signal cone.

## 2. Why literal distance equals null time is too strong

If one additionally identifies the F1 length with static-slice proper length and requires

\[
c_E\Delta t=\ell
\]

for every subinterval, differentiation at the upper endpoint gives

\[
\frac1f=\frac1{\sqrt f}.
\]

Positivity forces

\[
\boxed{f=1.}
\]

Allowing one constant calibration `kappa` in `D_opt=kappa ell` gives

\[
f=\kappa^{-2},
\]

a constant lapse. A smooth areal center fixes `f(0)=1`, hence `kappa=1`. The nontrivial G257, G201,
and G264 profiles all fail this stronger equality.

This does not mean `P_INF` selects flatness. It means that identifying optical null distance with
static-slice proper distance was an additional premise strong enough to erase the intended UDT
sector.

## 3. Infinite bare c reproduces the existing directional evaluator

At two static endpoints,

\[
f_A=e^{-2\phi_A},\qquad f_B=e^{-2\phi_B},\qquad
\delta_{AB}=\phi_B-\phi_A.
\]

The relative coordinate-null speed is

\[
\boxed{\frac{c_{{\rm coord},B}}{c_{{\rm coord},A}}
=\frac{f_B}{f_A}=e^{-2\delta_{AB}}.}
\]

The G220 null clock/frequency arrow is

\[
\boxed{r_{AB}=\frac{N_B}{N_A}=e^{-\delta_{AB}}.}
\]

Both are exact functions of the supplied metric. Interpreting them as entirely geometric rather
than as a finite bare propagation law changes their ownership story, but supplies no derivative or
integral residual for `f`.

## 4. Mutual slowdown and directional reversal are different channels

For the same exact endpoint correspondence,

\[
r_{BA}=r_{AB}^{-1}.
\]

If one demands that this same signed arrow itself equal one common slowdown in both directions,

\[
r_{AB}=r_{BA},
\]

then positivity gives

\[
r_{AB}=1,
\qquad N_A=N_B.
\]

Across every pair in a connected static interval, `N` is constant. This is not a no-go for the
original mutuality statement. It proves only that the signed null arrow is not the mutual
time-dilation magnitude.

The reciprocal representation already contains the correct algebraic distinction:

\[
D(\delta)=\operatorname{diag}(e^{-\delta},e^{+\delta})
=\cosh\delta\,I
+\sinh\delta\,\operatorname{diag}(-1,+1).
\]

Its reversal-even magnitude is

\[
\boxed{\Gamma_{\rm pos}=\frac12\operatorname{Tr}D=\cosh\delta,}
\]

while

\[
\boxed{\chi=\tanh\delta}
\]

is odd. Exactly,

\[
\boxed{e^{\pm\delta}=\Gamma_{\rm pos}(1\pm\chi).}
\]

Consequently an SR-like mutual clock-rate interpretation would be

\[
\boxed{M_{AB}=M_{BA}=\Gamma_{\rm pos}^{-1}=\operatorname{sech}\delta.}
\]

No new coefficient or fitted function is needed for that candidate. But the physical statement
that `sech(delta)` is the positional mutual clock rate is a recovered candidate premise, not a
consequence of F4 or W1's present directional clock-leg readout.

The signed factor and this even candidate coincide only at

\[
e^{-\delta}=\operatorname{sech}\delta
\quad\Longleftrightarrow\quad
\delta=0.
\]

This corrects the stronger preliminary claim that mutuality itself invalidates signed depth.
Signed depth can remain the oriented group coordinate while physical mutual time dilation lives in
its reversal-even channel, just as directional and mutual observables differ in ordinary
relativistic kinematics.

## 5. The most direct symmetric two-clock closure also trivializes

For one static interval, let each endpoint clock time the same Killing-time span. The corresponding
finite speeds are

\[
\frac{v_A}{c_E}=\frac{\ell}{N_A D_{\rm opt}},
\qquad
\frac{v_B}{c_E}=\frac{\ell}{N_B D_{\rm opt}}.
\]

Their ratio is

\[
\frac{v_A}{v_B}=\frac{N_B}{N_A}=r_{AB}.
\]

Therefore requiring `v_A=v_B` for this same static correspondence again forces `N_A=N_B`.

One may instead form the symmetric geometric-mean normalization

\[
M_g(A,B)=
\frac{\ell}{\sqrt{N_A N_B}\,D_{\rm opt}}.
\]

Identifying `M_g=sech(log(N_A/N_B))` is another possible but new functional equation. Its
small-interval expansion for `B=A+h` begins with

\[
M_g-\operatorname{sech}\!\left(\log\frac{N_A}{N_B}\right)
=h^2\left[-\frac{N''}{12N}+\frac{11(N')^2}{24N^2}\right]+O(h^3).
\]

Vanishing at second order requires

\[
2NN''=11(N')^2.
\]

Its local solutions are constant `N`, or, after affine reparameterization,

\[
N=C(ar+b)^{-2/9}.
\]

The nonconstant candidate fails the original all-interval equation at fourth order. With
`x=1+z`, its exact difference begins

\[
\boxed{M_g-\operatorname{sech}\delta=\frac7{13122}z^4+O(z^5).}
\]

Thus the all-interval symmetric closure also retains only constant lapse. More importantly, neither
the geometric mean nor its identification with `sech(delta)` follows from `P_INF`; choosing it would
be a new pair protocol.

## 6. Separating profiles

The G264 family

\[
f=1+\epsilon(r/L)^2e^{-(r/L)^2}
\]

and the G201 alpha-two family

\[
f=1+\epsilon(r/L)^2
\]

both satisfy the metric-null identity `c_E Delta t=D_opt` exactly. They therefore prove that the
metric-owned reading of infinite bare `c` is nonselective.

Both violate `D_opt=ell` and the same-correspondence mutual-arrow equality on generic intervals.
They are rejected only after those stronger pair-distance identifications are supplied.

The independent replay used flat, G257 quiet-comparator, G201 alpha-two, and G264 bump profiles on
three intervals. It confirmed the null integral by an RK4 solve against Gauss quadrature, exact
reversal of the signed arrow, and separation of optical, proper, endpoint-clock, symmetric-speed,
and `sech(delta)` channels.

## 7. Ownership result

`P_INF` has genuine conceptual content:

- `c_E` is treated as the completed metric's clock/ruler calibration, not a separate bare signal
  speed;
- no propagation delay or light cone may be bolted onto the metric independently;
- the existing null and redshift factors are interpreted as pair geometry.

In the bounded primary metric, however, it supplies no value law because it does not specify which
metric delay the separation must generate. The missing mathematical statement is still a
nonidentity relation

\[
\mathcal Q\bigl(s(A,B),\delta(A,B),g;A,B\bigr)=0
\]

that owns the physical separation type and constrains values without equating distinct metric
lengths by fiat.

The recovered mutuality statement narrows the target: `Q` must distinguish the reversal-even
mutual magnitude from the directed null/redshift character. A time-live realization may also use
distinct outgoing and return incidences; G220 already proves that causal return is not algebraic
inversion. Neither option has been derived here.

## 8. Exact ceiling

The infinite-bare-`c` statement is not disproved. It is also not yet the missing static value law.
The primary advance is a corrected output typing:

\[
\boxed{
\text{one signed reciprocal depth}
\longrightarrow
\begin{cases}
\text{directional factors }e^{\pm\delta},\\
\text{reversal-even magnitude }\cosh\delta,\\
\text{candidate mutual clock rate }\operatorname{sech}\delta.
\end{cases}}
\]

The next justified question is whether Charles's recovered distance-equivalence postulate owns the
`sech(delta)` projection and an intrinsic two-point separation law in the complete time-live metric.
It is not another static profile sweep.
