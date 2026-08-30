# G305 external repair-follow-up response

`REPAIRABLE_DEFECTS_REMAIN`

- `R3` is still not fully satisfied. The preregistration requires each hostile claim to be applied
  as a mutation to the computed evidence state or a required-premise set. The implementation loads
  computed evidence unchanged, adds an empty `promotions` label set, and then executes only
  `candidate["promotions"].add(promotion)` on a deep copy. That yields named failures and detects a
  corrupted baseline, but does not make the ten hostile cases mutations of computed evidence.
- The bounded landing is unchanged. The frozen landing matches the production and package-verifier
  landings; production remains 77 assertions with Hopf integer `-1`; and `metric_or_kernel_change`
  remains `NONE` / `unchanged`.
- `R1` and `R2` passed. Unique two-layout source resolution is enforced with 11 verified hashes.
  The independent replay imports no production code and reports the required category counts and
  Hopf normalization.

The exact returned response and transcript are identified by SHA-256 in
`EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md`.
