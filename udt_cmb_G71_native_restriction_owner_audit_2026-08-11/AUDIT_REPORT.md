# G71 native restriction-owner audit — report

## Landing

`GEOMETRIC_CARRY_OWNED__OBSERVABLE_AND_SELECTION_OWNERS_OPEN`

Evidence state: `INTERNALLY_VERIFIED__EXTERNAL_REVIEW_PENDING`.

The complete query geometry derives azimuthal/normal-screen carry on a supplied path and screen.
It does not currently own a physical source covariance or normalization, a physical CMB endpoint
or profile, or an observation-level channel that independently reads the carry.

## What was tested

G71 froze 21 current sources spanning G68--G70, the complete CMB query map, the common-query/SNe
controls, the observer-relation/global-completion spine, and the premise registry. Every source was
classified against six owner targets. A 16-edge dependency graph separates geometric evaluation,
physical selection, source population, and observation.

The exact source-congruence freedom replayed in 12 rational cases. A separate NumPy/SciPy route
replayed 200 random positive-definite cases with maximum relative congruence error
`8.401e-14`, minimum constructed source eigenvalue `0.04847`, and maximum normalized-shape shift
under source amplitude `3.325e-13`. All 13 registered semantic mutations were caught.

## Ownership result

- `GEOMETRIC_CARRY_OWNER`: `DERIVED_CONDITIONAL_ON_QUERY`.
- The other five targets: `OPEN_NO_OWNER`.
- `OWNED_NATIVE` targets: zero.

The helpful G70 restrictions therefore remain physical premises rather than consequences of the
current metric/query evidence. In particular, known source covariance plus carry remains an
algebraic sufficiency control, not a UDT CMB solution.

## Four evidence gates

1. **Preregistered:** yes, commit `07751b06` before source adjudication or result construction.
2. **Full or bounded:** complete over the exact 21-source, six-target universe; not a survey of all
   possible future UDT laws.
3. **Independent:** separate numerical implementation plus exact rational algebra; semantic
   external review remains pending.
4. **Premises:** all six targets explicitly typed; no query input, control, `X_max`, bootstrap,
   action, source, or observation was promoted.

## Authority boundary

No fit, observational coefficient, new ODE/PDE solve, GPU process, source law, last-scattering
surface, profile, spectrum, action, bootstrap selector, `X_max` value, or signalling rule was used
or derived. The seven protected stopped-draft paths remained unread and unstaged.

## Next gate

Cold-review this ownership result. If upheld, do not run another inverse-rank scan. The next
scientific derivation must target one missing typed map directly: preferably the observation/response
map joining metric-owned screen transport to an orientation-sensitive observable and source state,
or, separately, a native global/source selection law. Neither may be invented merely to make the
CMB system identifiable.
