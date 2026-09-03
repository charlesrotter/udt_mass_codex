# G334 preregistration — boosted pair first-jet response

Date: 2026-09-03
Status: `PREREGISTERED_BEFORE_OUTCOME_EXECUTION`

## Frozen question

Let `q=gamma(Hv,v)` be G333's exact first normal logarithmic length rate for an arbitrary unit
direction `v`. At the initial slice, form the finite locally boosted orthonormal pair

```text
u = cosh(z) n + sinh(z) v,
s = sinh(z) n + cosh(z) v.
```

Derive the first `n`-derivative of the complete pair matrix `h_ab=g(e_a,e_b)` and of
`Phi=-(1/2)log(-h00)`. Keep the local boost, G332 branch, direction, and vector transport explicit.
Determine whether the boost creates new response information, whether the pointwise boost value is
sufficient for an arbitrary pair germ, and exactly when terminal `Phi` loses information retained
by the complete matrix in the declared inherited transport class.

## Pinned, free, chosen, and omitted

- `pinned-by-THEORY_CONDITIONAL`: G333's tensor first jet, G315's sign convention, the exact G332
  family, and the complete pair pullback/readout typing.
- `free-and-explored`: all finite boost signs and magnitudes, every `mu` in `[0,1]`, both G332
  square-root branches, and positive/negative/zero directional response controls.
- `CHOSE_GAUGE_PRESENTATION_CONTROL`: G333's Gaussian normal presentation at the initial slice.
- `CHOSE_TRANSPORT_PRESENTATION_CONTROL`: the inherited subclass begins with `[n,v]=0`; local
  Lorentz-frame-rate terms are retained and tested rather than silently set to zero.
- `free-and-explored_GERM_DATA`: a general first-order extension is encoded by the components of
  `[n,u]` and `[n,s]`; it is not identified with the inherited subclass.
- `OMITTED_OPEN`: derivative along `u`, acceleration, arbitrary screen mixing, the null limit,
  nonzero time, evolution, persistence, stability, physical germ population, topology, occupancy,
  matter/mass, observations, scale, and physical `X_max`.

## Frozen analytic checks

Production must derive and check, without importing a new physical equation:

1. The tensor differentiation identity
   `n h_ab=(L_n g)(e_a,e_b)+g([n,e_a],e_b)+g(e_a,[n,e_b])`.
2. The Lorentz congruence of G333's base first-jet matrix for the inherited pair plane.
3. Closed component formulas for `n(h00)`, `n(h01)`, and `n(h11)` for every finite boost.
4. Boost-invariant trace/determinant or equivalent characteristic data of the inherited
   first-response endomorphism.
5. Boost-reversal parity of all three entries and terminal `n(Phi)`.
6. Cancellation, or failure of cancellation, of an arbitrary first normal rapidity rate inside the
   Lorentz-carried subclass.
7. The most general in-plane commutator contribution, with screen-orthogonal contributions kept
   visible and classified at this derivative order.
8. Whether a re-orthonormalized moving frame can erase raw component derivatives by shifting the
   same geometry into frame transport.
9. Exact blind and reconstructible strata of terminal `Phi`, including the unboosted and zero-rate
   controls.
10. Retention of every G333 direction and both G332 square-root branches without selecting one.
11. An explicit type guard that `n`-derivative is not the derivative along boosted `u`.
12. No dependence on Hopf closure, orbit period, carrier normalization, fitted profile, source,
   action, scale, or `X_max`.

The production implementation will use exact standard-library arithmetic on a dense set of
rational Lorentz controls plus an analytic derivation valid for all finite boosts. An
implementation-distinct verifier must reconstruct the matrix transformation without importing
production code or reading its result. Hostile mutations must catch at least: wrong cross sign,
dropped transport terms, false terminal completeness at zero boost, branch collapse, promotion of
`n` into observer proper time, and insertion of Hopf/topology input.

## Falsification and classification contract

- Land `BOOST_VALUE_SUFFICIENT` only if all allowed first-order vector transports yield the same
  component first jet from `(q,z)` alone.
- Land `TRANSPORT_QUALIFIED_CONGRUENCE` if the inherited Lorentz-carried class closes exactly but a
  general supplied germ contains additional transport data.
- Land `TERMINAL_FIRST_JET_COMPLETE` only if `Phi` reconstructs `q` on every included stratum.
- Land `COMPLETE_MATRIX_STRONGER_ON_DECLARED_TRANSPORT` only if an exact matrix invariant retains
  `q` where terminal `Phi` does not, with the transport qualification explicit.
- Land `NEW_RESPONSE_CHANNEL` only if a boost introduces invariant data not determined by G333's
  metric first jet and supplied transport.
- Any hidden pin, unresolved transport term, omitted branch, residual failure, or shared-code false
  independence limits the result to `LEAD` or `OPEN`.

## Maximum grade

`DERIVED_CONDITIONAL_BOUNDED`, pending independent and fresh adversarial verification. No outcome
may be promoted to a full observer-response law or finite-time dynamics.
