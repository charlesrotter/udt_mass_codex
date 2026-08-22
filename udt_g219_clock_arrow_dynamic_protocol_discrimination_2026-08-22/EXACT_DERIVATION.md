# G219 exact derivation — clock arrow under relative motion

Date: 2026-08-22

## 1. One scalar arrow

For a supplied regular clock correspondence `b=f(a)`, define at one paired event

\[
r_{AB}=f'(a)>0,\qquad \delta_{AB}=-\log r_{AB}.
\]

After source-clock normalization the founded reciprocal block is

\[
T=r,\quad L_r=r^{-1},\quad q=T/L_r=r^2,
\quad \chi=\frac{L_r-T}{L_r+T}=\frac{1-r^2}{1+r^2}.
\]

Thus G166--G217 require no second reciprocal-kernel scalar coefficient after the positive arrow is
supplied. Density, shift, incidence, pair-plane, and higher-germ data remain separately typed.
Reversal sends `r` to `1/r`; actual matched composition sends `(r_AB,r_BC)` to `r_BC r_AB`.

For `f_c(a)=r a+c a^2` at the anchor `a=0`,

\[
f_c(0)=0,\qquad f_c'(0)=r,\qquad f_c''(0)=2c.
\]

Incidence, first jet, and depth are independent of `c`; higher-germ data are not.

## 2. Moving-flat control

Set `c_E=1` as a unit choice and use rapidity `eta`:

\[
A(a)=(a,0),\qquad
B(b)=(\cosh\eta\,b,\ L+\sinh\eta\,b).
\]

Both parameters are proper clocks and `L>0` is symbolic.
All null formulas below are local to the connected regular interval on which B is to the future/right
of the chosen A emission event. No global crossing, caustic, or multi-branch claim is made.

### Outgoing null incidence

The right-moving condition `t_B-a=x_B` gives

\[
b=e^\eta(a+L),\qquad r_{\rm null}=e^\eta,
\qquad \delta_{\rm null}=-\eta.
\]

Its mathematical inverse is

\[
a=e^{-\eta}b-L,
\]

with inverse slope `e^{-eta}`.

### A-Fermi and A-radar incidence

The hyperplane orthogonal to `U_A=(1,0)` is constant Minkowski time, hence

\[
b=\frac{a}{\cosh\eta},\qquad r_{A\mathrm F}=\operatorname{sech}\eta,
\qquad \delta_{A\mathrm F}=\log\cosh\eta.
\]

For the B event `b`, the A-clock null emission and reception times are

\[
a_-=e^{-\eta}b-L,\qquad a_+=e^\eta b+L.
\]

Their midpoint and half-difference are

\[
\frac{a_-+a_+}{2}=\cosh\eta\,b,\qquad
\frac{a_+-a_-}{2}=L+\sinh\eta\,b.
\]

Therefore A-radar simultaneity equals A-Fermi simultaneity only in this inertial flat control.

### B-Fermi incidence

Orthogonality of `A(a)-B(b)` to `U_B=(cosh eta,sinh eta)` gives

\[
b=\cosh\eta\,a+\sinh\eta\,L,
\qquad r_{B\mathrm F}=\cosh\eta,
\qquad \delta_{B\mathrm F}=-\log\cosh\eta.
\]

For nonzero rapidity the null, A-Fermi/radar, and B-Fermi slopes differ.

## 3. Actual future return is not inversion

A future null ray emitted by B at `b` reaches A at

\[
a_+=e^\eta b+L.
\]

Composing this with the outgoing ray from A gives the echo map

\[
a_+=L+e^{2\eta}(a_-+L),
\qquad \frac{da_+}{da_-}=e^{2\eta}.
\]

The inverse outgoing arrow has slope `e^{-eta}`; the future return has slope `e^eta`. They coincide
only in the static limit.

## 4. Ownership result

Every displayed correspondence is metric-derived after its query is declared and has a positive
clock slope. The founded sources specify a positive positional comparison at supplied depth and its
composition, but contain no condition selecting null, A-Fermi, B-Fermi, or radar incidence. Therefore
the bounded scalar chain factors through one arrow while moving protocol ownership remains query-typed.
