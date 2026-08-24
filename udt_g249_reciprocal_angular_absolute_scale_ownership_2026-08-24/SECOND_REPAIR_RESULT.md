# G249 second certification-repair result

Date: 2026-08-24

## Result

`DERIVED_CONDITIONAL__SECOND_REPAIR_COMPLETE__FOLLOWUP_PENDING`

Both repairs preregistered at commit `24d0dee1` pass without changing the scientific landing.

## R1a — explicit equal-phi witnesses

The independent replay now constructs two witnesses in every one of 10,000 cases:

- both have exact `phi = 0`;
- their radial jets `(p,q)` are distinct;
- their exact G201 angular tuples `(2 p^2 + p - q, -p)` are distinct.

The claim Boolean is accumulated from those direct comparisons. The replay remains independent of
production code and output and passes 248,310 exact assertions. The other five registered claim
classes, including 512 degree-16 two-method IVPs, remain unchanged and pass.

## R3a — exact hostile ledger

The aggregate verifier now contains the exact preregistered set of 23 hostile/control identifiers
and requires exact set equality, `total == caught == 23`, an empty missed list, and every Boolean
true. Internal negative controls prove the gate rejects both:

- deletion of a hostile entry with self-consistent decremented counts;
- renaming of a hostile entry while retaining 23 self-consistent entries.

## Complete replay

- production derivation: PASS, 4,096 cases and 61,448 assertions;
- independent verification: PASS, 10,000 cases and 248,310 assertions;
- hostile controls/mutations: PASS, exact 23/23 ledger;
- aggregate package verifier: PASS, 27/27 gates including deletion and renaming rejection;
- current scientific premise verifier: PASS, 231-row registry.

Observational outcomes remained closed and unread. Fitted coefficients remain zero. No premise,
formula, physical history, absolute anchor value, `X_max`, source, detector, transfer, or scientific
claim changed.
