# G271 preregistration — primary-metric null screen first-jet interlock

Date: 2026-08-26
Status: `PREREGISTERED_BEFORE_OUTCOME_COMPUTATION`

## Whole question

On the arbitrary smooth regular primary static reciprocal metric

\[
ds^2=-e^{-2\phi(r)}c_E^2dt^2+e^{2\phi(r)}dr^2+r^2d\Omega^2,
\]

does the complete metric determine the first generation of G269's transported mismatch `W` along
a supplied nonradial affine null relation, and does that generation interlock with the direct
reciprocal-depth/redshift jet? This is a supplied-family evaluation, not a history-selection audit.

## Mode and bounded regime

- `METRIC_LED`, observing rather than targeting;
- arbitrary `C^2` primary profile on a regular finite-radius patch;
- one supplied equatorial future affine null germ and the static metric-unit observer congruence;
- local first jet at the source, plus any exact all-path identity that follows without choosing a
  profile;
- units may set `c_E=1` inside normalized contractions, with dimensional restoration declared.

No profile, distance law, branch population, field equation, source, action, observation, fit,
`X_max`, singular endpoint, caustic, or global completion is admitted.

## Frozen definitions

Write

\[
N=e^{-\phi},\qquad A=e^{+\phi},\qquad
U=N^{-1}\partial_t.
\]

For affine null tangent `k`, define the local frequency and spatial direction

\[
\omega=-g(k,U)>0,\qquad k=\omega(U+n),\qquad g(n,n)=1.
\]

At the source let

\[
n=\cos\alpha\,e_{\hat r}+\sin\alpha\,e_{\hat\varphi},
\]

and choose the in-plane screen orientation

\[
s=-\sin\alpha\,e_{\hat r}+\cos\alpha\,e_{\hat\varphi}.
\]

Parallel transport `U`, `n`, and an orthonormal screen basis from the source. At affine parameter
`lambda`, decompose the local static clock against that transported null pair plane as in G269;
its screen components are `W_I(lambda)` and vanish at the source.

The directional depth to the nearby endpoint is the already-derived static relation

\[
\delta(\lambda)=\phi(r(\lambda))-\phi(r(0)).
\]

## Preregistered alternatives

1. `A__PRIMARY_STATIC_FAMILY_FORCES_W_ZERO`: every supplied static-spherical null germ remains
   transported-planar, including nonradial germs.
2. `B__W_FIRST_JET_EXISTS_BUT_IS_NOT_INTERLOCKED`: the metric generates a nonzero transverse jet,
   but no coefficient-free relation joins it to the direct depth jet.
3. `C__NATIVE_LONGITUDINAL_TRANSVERSE_FIRST_JET_SPLIT`: the static congruence acceleration and
   Levi-Civita transport give an exact screen-evolution identity and a coefficient-free local
   angular split between depth generation and `W` generation. Radial and quiet limits follow as
   exact strata.
4. `D__TYPE_SIGN_OR_REGULARITY_FAILURE`: the proposed transported screen, static-clock derivative,
   or endpoint-depth comparison is inconsistent in the declared regime.

## Required derivations

Production must establish or refute, without choosing `phi(r)`:

1. the static congruence identity for `nabla_X U` and acceleration `a=nabla_U U`;
2. the primary-metric orthonormal acceleration component;
3. the exact evolution of transported screen components
   `dW_I/dlambda = omega g(a,E_I)`;
4. direct depth differentiation along the same null germ;
5. the local radial/transverse angular decomposition and its squared norm;
6. exact radial planarity, local quiet behavior, and the nonradial/nonquiet separator;
7. the leading small-affine mismatch and `M_PT`-versus-`sech(delta)` gap;
8. compatibility with G269 reversal scaling and affine normalization;
9. the distinction between value sign `phi`, gradient sign `phi_prime`, and incidence angle.

## Premise ledger

| Item | Status | Role |
|---|---|---|
| primary static reciprocal metric form | `DERIVED_CONDITIONAL/DECLARED_READOUT` | supplied family |
| arbitrary smooth `phi(r)` | `FREE_AND_EXPLORED` | no history selected |
| affine null germ and static endpoints | `SUPPLIED_CONDITIONAL_QUERY` | common comparison |
| Levi-Civita connection/transport | `DERIVED_FROM_SUPPLIED_METRIC` | generates bilocal frame carry |
| `delta=phi_B-phi_A` on static branch | `DERIVED_CONDITIONAL` | longitudinal channel |
| G269 `W`, `Gamma_PT`, `M_PT` | `DERIVED_CONDITIONAL`; mutual interpretation `WORKING` | transverse channel |
| angle `alpha` | `SUPPLIED_QUERY_DATA` | local null incidence, not a coefficient |
| profile law, population, distance, `X_max` | `OPEN_OMITTED` | forbidden promotion |

No item is `pinned-by-HABIT`.

## Certification and falsification contract

1. direct symbolic Christoffel reconstruction from the metric, not an asserted congruence formula;
2. a separate implementation deriving the load-bearing identities without importing production;
3. exact rational angle/slope trials on at least 10,000 regular cases;
4. controls at radial incidence, tangential incidence, `phi_prime=0`, both signs of `phi_prime`, and
   both path orientations;
5. hostile mutations for connection sign, lapse derivative, screen orientation, omitted frequency,
   false universal `W=0`, and promotion from first jet to finite-path/history selection;
6. raw outputs, hashes, no-write replay, premise audit, and bounded conclusion wording.

Alternative C fails if the direct Christoffel calculation does not reproduce the covariant
static-congruence identity, if the longitudinal/transverse square does not close, or if radial or
quiet controls generate a transverse first jet. No finite-path uniqueness may be inferred from a
first-jet result.

## Maximum conclusion

At most G271 may derive how the supplied primary metric locally divides one reciprocal-gradient
effect into direct depth/redshift and transported-screen mismatch channels as a function of null
incidence. It may show that `W` is not an added coefficient on this family. It may not determine a
finite path from local data, select `phi(r)`, populate observers or branches, derive distance or
`X_max`, fit observations, or supply dynamics.
