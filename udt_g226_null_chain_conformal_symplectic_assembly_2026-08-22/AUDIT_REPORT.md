# G226 audit — composable null-chain conformal-symplectic assembly

Date: 2026-08-22

## Landing

```text
CONFORMAL_SYMPLECTIC_NULL_CHAIN_INTERLOCK_DERIVED_CONDITIONALLY
```

Current grade after fresh external review and implementation of its two evidence-layer repairs:
`DERIVED_CONDITIONAL__EXTERNALLY_ACCEPTED__PACKAGING_REPAIRS_PENDING_FOLLOWUP`.

## Decisive result

For each supplied G188 affine null edge, let `F_e` be the full symplectic Jacobi phase transfer and
let `omega_s,omega_t` be its endpoint observer frequencies. In clock-normalized endpoint phases,

\[
M_e=R(\omega_t)^{-1}F_eR(\omega_s),
\qquad R(\omega)=\operatorname{diag}(I_2,\omega I_2),
\]

and exactly

\[
M_e^T\Omega M_e=r_e\Omega,
\qquad
r_e=\omega_s/\omega_t=d\tau_t/d\tau_s.
\]

G224's vertical coefficient is `q_e=r_e^-1`. At a supplied shared event, the G225 screen
isometry has the first-jet lift `diag(C,C)`, which is symplectic. Hence

\[
M_{ABC}=M_{BC}\operatorname{diag}(C_B,C_B)M_{AB}
\]

has multiplier `r_BC r_AB`. This is a path-labelled functor into `CSp^+(4,R)`.

## Structural consequences

- The proper-clock scalar and the full angular phase interlock without an added coefficient.
- The reciprocal ruler carry is the inverse conformal multiplier.
- Independent middle `O(2)` screen gauges cancel.
- Constant affine-generator rescaling cancels.
- A singular Jacobi position block does not destroy the full invertible phase.
- G225 direction-space holonomy embeds as `diag(H,H)` and remains matrix-valued.
- General edge phases and vertex rotations do not commute, so their order cannot be scalarized.

## Verification

- Production: 28 exact symbolic/rational checks.
- Independent: 20,000 exact-Fraction chains, 200,007 assertions.
- Every independent chain had a noncommuting ordered edge/vertex product.
- Hostile catches: 8/8.
- Fresh external adversarial review: `G226_ACCEPTED_WITH_REPAIRS`; no scientific defect found.
- Repair scope: strict-read-only aggregate replay and bounded verifier-coverage wording only.
- Repair-only external follow-up: pending before banking the final evidence grade.

## Scope ceiling

The result applies to supplied regular affine null edges meeting at supplied calibrated events,
using the G225 non-antipodal pointwise evaluator. It does not select the physical null protocol,
promote that evaluator to physical transport, force an independently supplied direct relation,
aggregate branches, choose a history, or derive `X_max`, transfer, observation, action, source,
matter, bootstrap, mass, or signalling.
