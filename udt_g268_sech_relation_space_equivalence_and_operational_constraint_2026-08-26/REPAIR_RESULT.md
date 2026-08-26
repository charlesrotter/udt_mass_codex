# G268 evidence-repair result

Date: 2026-08-26
Repair preregistration commit: `89670c8a`

## R1 — symbolic-proof honesty

`derive_relation_equivalence.py` now mechanically establishes the flagged positivity claims using
exact exponential/rational forms and explicit SymPy assumption queries. The global interior
diffeomorphism flag is a conjunction of the constituent inverse, surjectivity, rank, and positivity
checks and is not counted separately.

Zero relation/network/history rejection and absence of an owned operational protocol remain in the
result ledger as analytic or premise-scope conclusions. They are absent from the symbolic-check
dictionary. The repaired production count is 41 mechanically evaluated exact checks.

## R2 — genuine mutation catches

`run_catch_proofs.py` now sends the baseline and eight separately mutated candidate implementations
through the same exact-rational validator. The baseline returns no failures. Every mutation returns
a nonempty named failure set containing its preregistered target:

| Mutation | Required caught failure |
| --- | --- |
| loss of signed `chi` | `reversal_sign` |
| wrong inverse | `inverse_reconstruction` |
| multiplicative `M` composition | `composition_law` |
| deleted `chi` denominator | `composition_law` |
| accepting an off-circle state | `off_circle_rejection` |
| composing opposite ideal endpoints | `opposite_endpoint_rejection` |
| injecting history rejection | `zero_history_selection` |
| claiming protocol ownership | `open_protocol_ownership` |

## Scope

No formula, scientific landing, premise status, source universe, or maximum conclusion changed.
This is an evidence-only repair. External repair-only acceptance remains pending.

## Internal replay gates

- production: `PASS`, 41 mechanically evaluated exact symbolic checks;
- independent replay: `PASS`, 95,617 exact-rational assertions;
- mutation replay: `PASS`, baseline clean and 8/8 targeted mutations caught;
- package no-write replay: `PASS`, all recorded artifacts byte-identical before and after;
- repository suite: `172 passed, 1 xfailed`;
- exact premise registry: `PASS`, 250 rows plus startup/archive guards.
