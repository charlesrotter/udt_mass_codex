# G263 exact derivation — pair reversal versus profile-sign conjugation

Date: 2026-08-25

## 1. Two different involutions

On the regular primary static-spherical metric,

\[
g_\phi=-e^{-2\phi}c_E^2dt^2+e^{2\phi}dr^2+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0,
\]

define two operations.

The endpoint-pair reversal `R_pair` exchanges the ends of one supplied calibrated relation:

\[
\delta_{AB}\mapsto\delta_{BA}=-\delta_{AB},
\qquad g_\phi\mapsto g_\phi.
\]

The profile-sign conjugation `C_phi` is a diagnostic map between supplied metric histories:

\[
(\phi,p,z)\mapsto(-\phi,-p,-z),
\qquad p=r\phi',\quad z=r^2\phi'',
\]

so

\[
f\mapsto f^{-1},
\qquad g_\phi\mapsto g_{-\phi}.
\]

Both maps square to the identity, but only `R_pair` is the G170 derived conditional endpoint
reversal. `C_phi` is not promoted to a physical UDT symmetry.

## 2. Exact pair-arrow parity

For

\[
D(\delta)=\operatorname{diag}(e^{-\delta},e^{+\delta}),
\]

endpoint reversal gives

\[
D(-\delta)=D(\delta)^{-1}.
\]

Its reversal-even and reversal-odd pieces are

\[
\boxed{D_{\rm even}=\cosh\delta\,I},
\]

\[
\boxed{D_{\rm odd}=\operatorname{diag}(-\sinh\delta,+\sinh\delta)}.
\]

Thus the same reciprocal relation separates natively into an unsigned magnitude and a signed
orientation. For the clock character `q_pair=e^{-delta}`,

\[
q_{\rm even}=\cosh\delta,
\qquad
q_{\rm odd}=-\sinh\delta,
\]

while `chi=tanh(delta)` is odd. The already-derived G201 contrast is

\[
\mathcal C_{\rm rec}=\cosh(2\delta)-1=2\sinh^2\delta,
\]

which is even and nonnegative. This is an algebraic diagnostic, not a universal observable score.

## 3. Whole-profile parity

For any channel `F[phi]`, define

\[
F_{\rm even}=\frac12\left(F[\phi]+F[-\phi]\right),
\qquad
F_{\rm odd}=\frac12\left(F[\phi]-F[-\phi]\right).
\]

Let

\[
N=e^{-\phi},\qquad
c_1=\cosh\phi,\quad s_1=\sinh\phi,
\quad c_2=\cosh2\phi,\quad s_2=\sinh2\phi.
\]

Then

\[
N_{\rm even}=c_1,
\qquad N_{\rm odd}=-s_1,
\]

and

\[
f_{\rm even}=c_2,
\qquad f_{\rm odd}=-s_2.
\]

The clock and radial coefficients exchange reciprocal values, but the areal term
`r^2 dOmega^2` does not change. Therefore `C_phi` is not a full clock/ruler coframe swap and is not
generically an isometry.

## 4. Geometric mass aspect and acceleration are mixed

For the G262 geometric mass aspect

\[
\mu=\frac r2(1-e^{-2\phi}),
\]

the profile-conjugate value is

\[
\mu^C=\frac r2(1-e^{2\phi}).
\]

The exact split is

\[
\boxed{\mu_{\rm even}=-r\sinh^2\phi},
\qquad
\boxed{\mu_{\rm odd}=\frac r2\sinh2\phi}.
\]

Hence `mu` is neither odd nor even. This remains a geometric change of variables, not physical
mass.

The signed outward static acceleration is

\[
a_{\hat r}=N'=-e^{-\phi}\phi'.
\]

Under `C_phi`, `a_hat -> e^phi phi_prime`, giving

\[
\boxed{a_{{\hat r},{\rm even}}=\phi'\sinh\phi},
\qquad
\boxed{a_{{\hat r},{\rm odd}}=-\phi'\cosh\phi}.
\]

It too has both parities.

## 5. Residual and angular parity

Using `p=r phi_prime` and `z=r^2 phi_doubleprime`, the G260 residuals are

\[
E_0=e^{-2\phi}(1-2p)-1,
\qquad
E_1=e^{-2\phi}(2p^2-2p-z).
\]

Their exact profile-parity pieces are

\[
(E_0)_{\rm even}=c_2+2p s_2-1,
\qquad
(E_0)_{\rm odd}=-s_2-2p c_2,
\]

\[
(E_1)_{\rm even}=2p^2c_2+(2p+z)s_2,
\qquad
(E_1)_{\rm odd}=-2p^2s_2-(2p+z)c_2.
\]

For the two G201 angular channels,

\[
A_\parallel=e^{-2\phi}(2p^2+p-z),
\qquad
A_\perp=1-e^{-2\phi}(1+p),
\]

one obtains

\[
\boxed{(A_\parallel)_{\rm even}=2p^2c_2-(p-z)s_2},
\]

\[
\boxed{(A_\parallel)_{\rm odd}=-2p^2s_2+(p-z)c_2},
\]

\[
\boxed{(A_\perp)_{\rm even}=1-c_2+p s_2},
\]

\[
\boxed{(A_\perp)_{\rm odd}=s_2-p c_2}.
\]

Both parity sectors retain the complete identity

\[
A_\parallel+A_\perp=E_1-E_0.
\]

Thus negative and positive profile sectors need not have equal angular volume or opposite angular
signs.

## 6. Exact separator from the G201 zero-tide family

G201's family

\[
f=1+Cr^2
\]

has `A_parallel=A_perp=0` wherever `f>0`. Under profile conjugation,

\[
f^C=\frac1{1+Cr^2}.
\]

Writing `x=Cr^2`, its angular channels become

\[
\boxed{A_\parallel^C=\frac{4x^2}{(1+x)^3}},
\qquad
\boxed{A_\perp^C=\frac{x^2}{(1+x)^2}}.
\]

Except at `x=0`, the conjugate is not zero-tide. This explicitly separates `C_phi` from pair-arrow
reversal and proves that angular quietness is not preserved by whole-profile sign conjugation.

## 7. Signed-end interpretation

On the illustrative local constant-jet subclass `p=z=0`,

| Limit | `N` | `mu/r` | `A_parallel` | `A_perp` |
|---|---:|---:|---:|---:|
| `phi -> +infinity` | `0` | `1/2` | `0` | `1` |
| `phi -> -infinity` | `infinity` | `-infinity` | `0` | `-infinity` |

This table characterizes one lawful local subclass only. G201's exact zero-tide family reaches
either signed extreme, so neither end is universally angularly loud.

## 8. Landing and ceiling

```text
PAIR_ARROW_REVERSAL_IS_EXACT_RECIPROCAL_INVOLUTION
__WHOLE_PROFILE_SIGN_CONJUGATION_IS_A_DISTINCT_METRIC_INVOLUTION
__SCALAR_DEPTH_INVERSION_SHARED_BUT_COMPLETE_CHANNEL_PARITIES_MIXED
```

The bounded primary algebra supplies an exact signed-orientation/even-magnitude split for one
ordered reciprocal pair. It does not make the positive and negative whole-profile sectors physical
copies, select either sector, select a valued history, or derive physical mass, source, dynamics,
transfer, or `X_max`.
