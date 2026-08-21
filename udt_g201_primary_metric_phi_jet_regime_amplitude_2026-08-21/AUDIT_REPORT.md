# G201 audit report — primary-metric phi-jet regime amplitude

Date: 2026-08-21

## Landing

```text
TWO_SIDED_RECIPROCAL_MAGNITUDE
__ANGULAR_VOLUME_IS_PHI_JET_DEPENDENT
__NO_LOCKSTEP_LOUDNESS_FORCED
```

Grade: `INDEPENDENTLY_VERIFIED_WITH_CAVEATS`

## Result first

Charles's reframe was correct: the instruments do not have to march in lockstep.

The founded reciprocal block has a two-sided algebraic magnitude, minimal at zero and increasing
toward either signed depth extreme.  But the primary metric's two angular modes are

\[
A_\parallel=e^{-2\phi}(2p^2+p-q),
\qquad
A_\perp=1-e^{-2\phi}(1+p),
\]

where \(p=r\phi'\) and \(q=r^2\phi''\).  Their volume depends on the radial shape of the same metric
history, not only on the value or sign of \(\phi\).

## Consequences

- At \(\phi=0\), both angular modes are quiet exactly when \(p=q=0\).  Merely crossing zero does
  not guarantee the quiet regime.
- At every \(\phi\), specific lawful jets can cancel both modes.
- The cancellation integrates to the exact smooth primary family \(f=1+Cr^2\), which can approach
  either signed \(\phi\) extreme with zero angular tide.
- Other simple primary histories are naturally loud at one or both extremes.

So loud--quiet--loud is automatic for the **magnitude of reciprocal depth**, but not as one fixed
envelope imposed on every angular instrument.  A complete physical history may still produce the
proposed regime pattern by changing their native ratios with distance.

## Evidence

- preregistered and pushed at `28d48506` before confirmatory implementation;
- 20/20 symbolic assertions;
- 10,000 independent exact metric-jet/phi-jet comparisons;
- 1,000 independent arbitrary-phi cancellation controls;
- 400 exact smooth-family controls spanning both signs of `C`;
- 23,606 independent assertions total;
- production initially failed closed on a derivative-substitution ordering bug; simultaneous
  substitution repaired it before any result was accepted;
- independent verifier imports no production module and reads no production artifact;
- hostile catches, source hashes, no-write package replay, premise verifier, repository tests, and
  diff checks are recorded in `EVIDENCE_GATES.md`.

## Four gates

1. Preregistered: yes.
2. Full or bounded: exact local amplitude classification for every smooth positive primary-metric
   second jet at a regular nonradial source; no full finite-path or global-profile selection claim.
3. Independent: yes, standard-library exact-`Fraction` replay.
4. Premises: audited; the primary slice is declared, while the radial history and query remain
   supplied and completed-pair Dual Reciprocity remains a working clarification.

## Maximum conclusion

The primary metric algebra allows changing relative instrument volumes across regimes and does not
force a universal lockstep loudness envelope.  It does not select which allowed profile Nature
realizes.
