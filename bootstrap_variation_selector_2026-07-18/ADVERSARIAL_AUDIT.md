# Fresh adversarial audit record

Date: 2026-07-18  
Mode: two read-only, zero-context reviewers; CPU only; no repository edits

## Reviewer 1 — selector countermodel and verifier audit

Agent: `/root/bootstrap_selector_audit`

Initial verdict: `VERIFIED-WITH-CAVEATS`.

The reviewer independently reproduced the common countermodel root and closure, confirmed that
`rho_star` enters neither local action, rederived the chain-rule normal term, four-dimensional
conformal weights, and principal-polynomial obstruction, and found no hidden positive bridge. It
identified one substantive verifier weakness: `epsilon > 0` did not enforce the required narrow
window.

Correction applied:

- exact contract `0 < epsilon << 1` is now recorded in the derivation result;
- `fractional_width_fitted = false` is required;
- the independent verifier rejects a broad `epsilon > 0` fixture;
- catch-proofs increased from 9/9 to 10/10.

On follow-up the reviewer confirmed that hardening, then caught a stale `DERIVATION_REPORT.md` hash
after a later wording precision edit. The manifest was rebuilt and the final verifier replayed before
banking.

## Reviewer 2 — strongest affirmative bridge challenge

Agent: `/root/positive_bridge_challenge`

Verdict: `VERIFIED` within the preregistered selector scope.

The reviewer attempted the strongest positive paths:

- pre-scale selection from the premise that scale is emergent;
- post-scale selection from the need for physical mass and proper volume in the density predicate;
- a two-stage bridge from CSN plus bootstrap endpoints.

None follows. Emergent scale does not order variation; the density predicate is post-scale/on-shell
without placing fundamental variation; and the sources provide no selection map, field/variation map,
principal-operator matching, or finite-boundary/source matching. The reviewer independently
reproduced the chain rule and the `alpha k^4` versus `beta M^2 k^2` polynomial result.

Wording precision applied: equality of the two tangent equations requires `S_y f'=0`, while
equivalence to the full unrestricted problem additionally requires the normal equation or a
redundancy theorem.

## Final audit status

Both reviewers left the repository unchanged. Their corrections refine the verification contract,
not the scientific outcome. Final status after the rebuilt manifest and machine replay:
`UNDERDETERMINED` and `OPEN_NOT_DERIVED` remain verified within the stated scope.
