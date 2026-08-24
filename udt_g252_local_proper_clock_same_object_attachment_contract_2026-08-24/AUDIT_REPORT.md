# G252 audit report — local proper-clock same-object attachment

Date: 2026-08-24

## Landing

`VERIFIED-WITH-CAVEATS`

One independently calibrated positive proper-clock record on one frozen, identified timelike
observer segment conditionally fixes the single G249 scale by

\[
\ell=\tau_*/\bar\tau.
\]

This is a calibration of the metric family, not a modification of the reciprocal kernel.

## Evidence

- Preregistration was committed and pushed at `67684b07` before implementation.
- The production derivation verified 4,096 exact rational cases, 18,451 piecewise segment terms,
  and 20,480 assertions.
- A separate standard-library implementation verified 12,000 cases and 60,000 assertions without
  importing production code or reading production output.
- All 12,000 deliberately inconsistent second attachments were rejected.
- Twenty executable hostile controls were caught, including self-evaluation, object/event/branch
  mismatch, missing calibration identity, nonpositive duration, per-attachment scale proliferation,
  and the false claim that `c_E` alone fixes the scale.
- All six frozen source hashes were verified by both implementations.
- No observational values, fits, new kernel mechanisms, or history selection entered.

## Scientific meaning

G252 closes the algebraic and operational form of one local absolute calibration route. It also
turns every additional independently frozen proper-clock attachment into a possible falsifier of
the supplied dimensionless history: all must recover the same \(\ell\).

It does **not** establish that Nature supplies a particular observer segment, clock value, global
branch population, or complete history. It does not yet apply a clock record. Those remain the next
empirical and global questions.

## Gate status

1. preregistered: **PASS**;
2. full bounded space: **PASS** for positive exact symbolic/rational local attachments in the frozen
   one-scale arena;
3. independently verified: **PASS**;
4. premises audited: **PASS**, subject to the explicit supplied-history and supplied-attachment
   caveats.

The verdict is therefore `VERIFIED-WITH-CAVEATS`, not canon and not a physical-history selection.
