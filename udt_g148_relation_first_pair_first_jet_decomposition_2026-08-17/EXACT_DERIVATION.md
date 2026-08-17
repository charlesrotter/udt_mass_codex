# G148 exact derivation — relation-first complete-pair first jet

Date: 2026-08-17

## 1. Working relation-first constitution

G137 already records Charles's `CHOSE / WORKING_FOUNDATIONAL_CLARIFICATION` that physical normalized
position is the unit-slope projective coordinate of the completed reciprocal relation. On a supplied
regular calibrated pair,

\[
\rho=X_{\max}\tanh\phi_{\rm pair}.
\]

G147 conditionally tested the multidirectional representation `xi=rho n` in the query clock's rest
space. Charles has now authorized proceeding with the relation-first interpretation: this ball is a
working representation of the completed pair relation, not a second independently existing carrier
and not a spacetime displacement.

For this bounded calculation, that working representation requires no additional local solder
coefficient. It bypasses rather than resolves G147's open physical-carrier ownership gate. An
independently owned carrier retains its `O(2)` solder freedom. The working representation does not
derive an exponential-map displacement, proper length, areal radius, signal distance, physical
history, or global completion.

## 2. Complete pair input

For the complete coframe and supplied pair realization,

\[
E=\begin{pmatrix}B&0\\QS&Q\end{pmatrix},
\qquad
J=\binom YZ,
\qquad
h=J^TE^T\eta EJ.
\]

Every `B,Q,S,Y,Z` block enters before the terminal readout. On the regular calibrated stratum,

\[
\phi=\phi_{\rm pair}
=\frac14\log\!\left(\frac{-\det h}{h_{00}^2}\right).
\]

For a time-live first jet,

\[
\dot\phi
=\frac14\operatorname{tr}(h^{-1}\dot h)
-\frac12\frac{\dot h_{00}}{h_{00}}.
\]

In the covariant theorem below, the dot means derivative along the supplied query clock flow. It is
a kinematic derivative of a supplied smooth metric/query history, not an equation selecting that
history. Section 6's registered matrix-family parameter `lambda` is a separate algebraic liveness
control and is not identified with this clock flow.

## 3. Query flag and screen

Let `u` be the future unit clock tangent and `n` the orthogonal unit ruler tangent recovered from the
pair metric as in G147:

\[
g(u,u)=-1,
\qquad
g(n,n)=1,
\qquad
g(u,n)=0.
\]

The metric pair screen is

\[
H_{\rm pair}=\{w:g(w,u)=g(w,n)=0\}.
\]

Define the exact scalar and screen parts of the ruler derivative by

\[
a_n=g(\nabla_u u,n),
\qquad
\Omega=P_H\nabla_u n.
\]

Differentiating the unit and orthogonality identities gives

\[
g(n,\nabla_u n)=0,
\qquad
g(u,\nabla_u n)=-a_n.
\]

Therefore the complete decomposition is

\[
\boxed{\nabla_u n=a_nu+\Omega},
\qquad
\Omega\in H_{\rm pair}.
\]

No coefficient was chosen. `a_n` and `Omega` are metric/query first-jet readouts.

## 4. The coefficient-free relation-first identity

With

\[
\boldsymbol\xi=\rho n,
\qquad
\rho=X_{\max}\tanh\phi,
\]

the scalar derivative is

\[
\dot\rho
=X_{\max}\operatorname{sech}^2\phi\,\dot\phi.
\]

The product rule and the exact ruler decomposition give

\[
\boxed{
\nabla_u\boldsymbol\xi
=X_{\max}\operatorname{sech}^2\phi\,\dot\phi\,n
+X_{\max}\tanh\phi\,\Omega
+X_{\max}\tanh\phi\,a_nu.}
\]

This is one vector equation, not three mechanisms added afterward. Its pieces have distinct types:

- radial change inside the ruler line;
- directional turn inside the metric pair screen;
- timelike component recording change of the instantaneous query rest space.

Projecting into `u^perp` removes only the last component:

\[
P_{u^\perp}\nabla_u\boldsymbol\xi
=\dot\rho\,n+\rho\Omega.
\]

Because `n` and `Omega` are orthogonal,

\[
\boxed{
\left\|P_{u^\perp}\nabla_u\boldsymbol\xi\right\|^2
=X_{\max}^2\left[
\operatorname{sech}^4\phi\,\dot\phi^2
+\tanh^2\phi\,\|\Omega\|^2
\right].}
\]

The ambient Lorentz norm retains the rest-space-tilt term with negative sign:

\[
g(\nabla_u\boldsymbol\xi,\nabla_u\boldsymbol\xi)
=\dot\rho^2+\rho^2\|\Omega\|^2-\rho^2a_n^2.
\]

## 5. Coefficient limits inside the working representation

Inside the chosen working representation, the identity contains the coefficient functions

\[
\text{radial position gain}=\operatorname{sech}^2\phi,
\]

\[
\text{screen-turn and rest-space-tilt gain}=\tanh\phi,
\]

\[
\text{reciprocal clock/ruler gains}=e^{-\phi},e^{+\phi}.
\]

They have exact limits:

| regime | radial gain | screen/tilt gain | reciprocal scales |
|---|---:|---:|---:|
| `phi -> 0` | `1` | `0` with unit slope | both approach `1` |
| `phi -> +infinity` | `0` | `+1` | one vanishes, one diverges |
| `phi -> -infinity` | `0` | `-1` | the reciprocal roles exchange |

These are exact coefficient limits. On a regular continuation with bounded `Omega` and `a_n`, the
nonradial positional terms are suppressed to first order in `phi` near neutral depth. Toward either
positional asymptote, the radial coefficient tends to zero, the screen/tilt coefficient tends to a
signed unit value, and reciprocal dilation becomes unbounded.

This does **not** establish a physical regime pattern or the empirical phrase “loud, quiet, loud.”
Actual amplitudes also contain `dot phi`, `Omega`, and `a_n`, all determined only after a complete
time-live history and query are supplied. No boundedness of those first jets near either limit is
proved here. In particular, the radial coefficient is maximal rather than minimal at `phi=0`; a
quiet central regime additionally requires a small realized first jet.

## 6. Full-live exact witness

The witness was frozen before execution in `WITNESS_REGISTRATION.md`. Each of `B,Q,S,Y,Z` has an
independent nonzero rational first jet. The base pair is regular:

\[
h_{00}=-\frac{7619}{2025}<0,
\qquad
\det h=-\frac{8157287}{233280}<0.
\]

The registered `lambda` witness establishes algebraic liveness of `dh/dlambda`,
`dphi_pair/dlambda`, and the coordinate-component derivative `dP_H/dlambda` along the chosen matrix
family. Every block changes all three registered outputs. The exact `dphi_pair/dlambda` values are
distinct and nonzero, and the all-live `dh/dlambda` is the sum of the five exact first variations.

This witness does not identify `lambda` with query clock flow, compute the Levi-Civita connection,
or independently verify `nabla_u n`, `a_n`, or `Omega`. The covariant identity in Sections 3--4
follows analytically from metric compatibility and differentiated orthonormality for a supplied
smooth query history. The scripts' abstract-vector calculation is a consistency and regression
check of that identity, not an independent connection derivation.

## 7. Degenerate and global boundaries

At `phi=0`, `xi=0` and a sphere tangent at a nonzero radial point is unavailable, although the
query metric screen itself remains well defined for a regular pair. The displayed first-jet formula
has a continuous limit; it does not derive a direction at coincidence.

Null or degenerate pair metrics do not admit the same normalized flag. Cut loci, branch changes,
global topology, cross-query screen carry, and comparison with path-labelled `U_gamma` remain open.
No claim is made that reversible pair differentiation is future-directed signal propagation.

## 8. Maximum result

```text
WORKING_RELATION_FIRST_REPRESENTATION_ONLY__
EXACT_COVARIANT_FIRST_JET_IDENTITY_FOR_A_SUPPLIED_SMOOTH_REGULAR_CALIBRATED_PAIR__
LAMBDA_WITNESS_ESTABLISHES_COMPLETE_PAIR_ALGEBRAIC_FIRST_VARIATION_LIVENESS_ONLY__
COEFFICIENT_LIMITS_CHARACTERIZED__
PHYSICAL_CARRIER_HISTORY_DYNAMICS_AND_OBSERVATIONAL_REGIME_PATTERN_OPEN
```

The chosen representation permits the derivation to proceed without resolving the independent
carrier question. It does not close carrier ownership, numerical metric history, global completion,
or observational prediction.
