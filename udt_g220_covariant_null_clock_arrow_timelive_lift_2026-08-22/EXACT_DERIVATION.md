# G220 exact derivation — covariant null clock arrow on a time-live pair metric

Date: 2026-08-22

## Primary bounded result

For a supplied smooth Lorentz metric, supplied future-timelike observer curves, and one supplied
unique regular future null branch joining their events, the metric determines the positive clock
arrow

\[
r_{AB}=\frac{d\tau_B}{d\tau_A}
=\frac{k_A\cdot U_A}{k_B\cdot U_B}
=\frac{\omega_A}{\omega_B}>0,
\qquad
\delta_{AB}=-\log r_{AB}.
\]

This is a covariant dynamic formula on the declared null query. It is not a claim that null
incidence is the universal UDT positional protocol.

## 1. Covariant implicit-incidence derivation

Let `sigma(x,x')` be Synge's world function on a convex normal neighborhood and define

\[
F(\tau_A,\tau_B)
=\sigma\!\left(z_A(\tau_A),z_B(\tau_B)\right).
\]

The supplied null incidence relation is `F=0`. On a regular branch,
`sigma_{a'}U_B^{a'} != 0`, so the implicit-function theorem gives

\[
0=\sigma_aU_A^a+\sigma_{a'}U_B^{a'}\frac{d\tau_B}{d\tau_A},
\]

and hence

\[
\boxed{
r_{AB}=\frac{d\tau_B}{d\tau_A}
=-\frac{\sigma_aU_A^a}{\sigma_{a'}U_B^{a'}}}.
\]

If `k` is the future null affine tangent and `Delta lambda>0` is its affine span, then

\[
\sigma_a=-(\Delta\lambda)k_{A a},
\qquad
\sigma_{a'}=(\Delta\lambda)k_{B a'}.
\]

Therefore

\[
r_{AB}
=\frac{k_A\cdot U_A}{k_B\cdot U_B}
=\frac{-k_A\cdot U_A}{-k_B\cdot U_B}
=\frac{\omega_A}{\omega_B}.
\]

Both measured frequencies are positive. A common affine rescaling of `k` cancels. This is the
general covariant statement; it already allows a genuinely time-dependent metric and accelerating
observers, provided the declared null branch remains regular.

## 2. Exact time-live triangular metric

Set `c_E=1` only as a coordinate-unit choice and consider

\[
h=-N(t)^2\bigl(dt+\beta(t)dx\bigr)^2+A(t)^2dx^2,
\qquad N>0,\quad A>0.
\]

Define the two null chords

\[
C_+(t)=A(t)-N(t)\beta(t),
\qquad
C_-(t)=A(t)+N(t)\beta(t).
\]

On the right-moving regular branch `C_+>0`, the null condition gives

\[
\frac{dx}{dt}=\frac{N}{C_+}.
\]

For fixed-`x` observers separated by coordinate distance `L>0`, their paired null events obey

\[
L=\int_{t_A}^{t_B}\frac{N(t)}{C_+(t)}\,dt.
\]

Differentiating this exact incidence relation yields

\[
\frac{dt_B}{dt_A}
=\frac{N_A C_{+B}}{C_{+A}N_B}.
\]

The observer proper clocks satisfy `d tau=N dt`, so the lapse factors cancel only after proper-clock
normalization:

\[
\boxed{
r_{AB}=\frac{d\tau_B}{d\tau_A}
=\frac{N_Bdt_B}{N_Adt_A}
=\frac{C_{+B}}{C_{+A}}},
\qquad
\boxed{
\delta_{AB}=\log\frac{C_{+A}}{C_{+B}}}.
\]

Thus lapse, ruler scale, and shift do not enter as three fitted post-readout modifiers. They combine
inside the metric into the one right-null chord `C_+=A-N beta` before the clock arrow is read.

## 3. Same-correspondence completed clock-leg compatibility

Use the source proper clock `y=tau_A` as the pair parameter. Then

\[
\frac{dt_A}{dy}=\frac1{N_A},
\qquad
\frac{dt_B}{dy}=\frac{r_{AB}}{N_B}.
\]

The source clock leg is unit normalized, while the target observer clock leg has

\[
h_B(\partial_y,\partial_y)
=-N_B^2\left(\frac{dt_B}{dy}\right)^2
=-r_{AB}^2.
\]

Consequently the positive completed target clock coefficient is exactly

\[
\boxed{T_B=r_{AB}},
\]

and the G176 working completed-pair readout gives

\[
\boxed{\Phi_{AB}=-\log T_B=-\log r_{AB}=\delta_{AB}}.
\]

This is a same-correspondence compatibility identity: the definition of the target comparison-clock
tangent on the already supplied event relation gives the same `r_AB` as implicit null incidence.
It is not an independent confirmation of G176, a construction of the full pair plane, or an entry of
the omitted angular orchestra. It does show that no separate post-readout clock modifier is needed.

## 4. Mandatory exact controls

### Moving flat

For the G219 inertial observers of relative rapidity `eta`, the covariant frequency ratio gives

\[
r_{AB}=e^\eta,
\qquad
\delta_{AB}=-\eta.
\]

### Primary static reciprocal metric

For

\[
ds^2=-e^{-2\phi(x)}dt^2+e^{2\phi(x)}dx^2,
\]

static coordinate incidence has `dt_B/dt_A=1`, while proper clocks have
`d tau=e^{-phi}dt`. Hence

\[
r_{AB}=e^{\phi_A-\phi_B},
\qquad
\delta_{AB}=\phi_B-\phi_A.
\]

This spatially static control must not be confused with the preceding time-only endpoint formula.

### Conformal time-live control

For `N=A=e^{Omega(t)}` and `beta=0`, coordinate null speed remains one, but proper clocks vary:

\[
r_{AB}=e^{\Omega_B-\Omega_A},
\qquad
\delta_{AB}=\Omega_A-\Omega_B.
\]

### Affine ruler/shift time-live control

Let

\[
N=1,\qquad A=a_0+a_1t,\qquad \beta=st,
\qquad d=a_1-s.
\]

Then `C_+=a_0+dt`, and exact integration gives

\[
t_B=\frac{(a_0+dt_A)e^{dL}-a_0}{d},
\qquad
\frac{dt_B}{dt_A}=e^{dL}.
\]

Therefore

\[
r_{AB}=e^{(a_1-s)L}.
\]

This is genuinely time-live and includes nonzero shift. Its `d -> 0` limit is
`t_B=t_A+a_0L`.

## 5. Return is not inversion

The left-moving null branch uses

\[
\frac{dx}{dt}=-\frac{N}{C_-},
\qquad C_-=A+N\beta.
\]

A later B-to-A return therefore samples `C_-` at its own emission and reception events. Its proper
clock slope is a `C_-` endpoint ratio, not generically the inverse of the earlier outgoing `C_+`
ratio. Mathematical inversion reverses the same paired-event map; causal return is a different
incidence map.

## 6. Scope and ownership

G220 closes one exact dynamic tile: after a regular null query is supplied, the metric covariantly
determines its clock slope, and the same correspondence is compatible with the completed clock-leg
definition. No second reciprocal-kernel coefficient is introduced.

Still open are the physical query population, multiple/null-degenerate branches, cuts and caustics,
angular screen shape, base-screen mixing, transverse Jacobi transport, the full pair plane, global
history/completion, and every transfer, `X_max`, action, source, matter, bootstrap, mass, and
signalling claim.
