# External repair-only follow-up review of G350 R1–R4

Date: 2026-09-05

## Review boundary and disposition

I reviewed only the corrected sealed intake mounted at `/intake`, after copying it in full to the
fresh writable directory `/work/g350-repair-followup.QbEEn2`. I did not edit the intake, access a
repository or protected package, use the network, install anything, or continue the research. All
executions were confined to the registered dependency-free routes in the writable copy.

No defect was found within repairs R1–R4, and no regression was found in the retained bounded G350
landing. Documentary and text-token checks are credited only as integrity guards; the mathematical
landing rests on the explicit character argument and the stated hypotheses.

## 1. Intake authentication

Authentication was completed before reviewing claims.

- `/intake` is an ext4 read-only mount with `ro,nosuid,nodev` options.
- The copy was made before evidence checks. The mounted source and the copy were byte-identical both
  before and after all registered replays.
- `REVIEW_SCOPE.json` is valid JSON, declares `payload_count: 48`, and contains 48 ordered, unique,
  safe relative paths.
- The manifest contains exactly 48 data rows. Its path column is identical, in order and content,
  to the scope file's `files` array.
- The actual intake contains exactly those 48 payloads plus `REVIEW_MANIFEST.tsv` and
  `REVIEW_MANIFEST.sha256`: 50 regular files total, with no symbolic links or other nonregular
  entries.
- Every declared byte count and every payload SHA-256 value matches.
- The detached seal verifies `REVIEW_MANIFEST.tsv` at
  `f6deb035df78d05cc38ef5b5198fb6a805d65eeb2496bf74cc761eaaf47e2173`.
- Independently computed control-file hashes are:
  - `REVIEW_SCOPE.json`:
    `53e3962bdb1f0594dfeb82f0d38411ea009bac9abe5fff071b9bbaca2a35868b`;
  - `REVIEW_MANIFEST.tsv`:
    `f6deb035df78d05cc38ef5b5198fb6a805d65eeb2496bf74cc761eaaf47e2173`;
  - `REVIEW_MANIFEST.sha256`:
    `f5f319c54eb55b6d14ed178472e508c1ead959ffcb618dabc5287e075e36a4b0`.

This authenticates internal checksum consistency relative to the supplied detached digest. It is
not an externally signed provenance result or a trusted timestamp.

## 2. Original external response and twelve retained caveats

`EXTERNAL_REVIEW_RESPONSE.md` is byte-exact at the required SHA-256
`f31bef79fe98a7c6e265366e1549c5509ccc32bf162e0abc405db715f37f57d9`. Its required-repairs section
still contains the complete consecutive numbered list 1 through 12. The caveats were retained as
historical evidence rather than deleted or rewritten.

The repaired records address all twelve items:

1. Manifest authentication is explicitly limited to internal checksum consistency.
2. Commit and push timing is explicitly graded as documentary to an intake-only reviewer.
3. The former `21/23` event is described as a reconstruction because the former verifier bytes,
   raw output, and exact patch were not sealed.
4. The three outcome-bearing scientific scripts are identified as hash-frozen; the repaired
   aggregate is not represented as outcome-unseen or frozen.
5. The retained `25/25` route is labelled hard-coded contract enumeration, while a separate
   semantic route supplies behavioral witnesses.
6. The `35295/35295` exact-log route is labelled implementation-distinct verification of the
   proposed formulas, not a completeness proof.
7. The floating diagnostic is accurately described as mixed absolute/relative normalized error;
   a wide log-domain route was added without loosening the tolerance.
8. Sewing is universally quantified over the chosen full positive two-ratio domain, with the
   realized-subgroup caveat explicit.
9. Endpoint weights are required to be consistently endpoint-assigned positive zero-cochains.
10. `C_i` is typed as a scalar-valued component or a section of a one-dimensional weight
    representation when its observer weight is nonzero.
11. The caustic statement is one-sided under the stated positive-denominator and finite-nonzero
    ratio assumptions; reversal exchanges limits, and simultaneous zeros remain unclassified.
12. `(1.7,2.3)` is expressly an abstract group-domain witness, not asserted geometric data.

## 3. R1 — provenance and chronology grade

R1 passes.

The repaired audit, exact derivation, evidence gates, repair premise ledger, and execution record
consistently separate three grades: internal package checksums, documentary chronology, and the
bounded mathematical result. The nine entries in `FROZEN_PREREGISTRATION_HASHES.tsv` match their
recorded digests, including the three scientific scripts. The current aggregate source is not in
that frozen list and is explicitly described as repaired after the first recorded aggregate
failure.

The intake does not contain a Git object database, trusted external timestamp, or remote receipt.
Accordingly, this review does not independently authenticate the reported commit/push timing. It
also does not claim to replay the historical `21/23` result from unavailable former bytes. Those
limitations are correctly preserved in the repaired evidence grade.

## 4. R2 — mathematical domain, typing, and boundary repair

R2 passes.

The repaired exact derivation states the sewing law for every pair in the chosen abstract group
`R_+ x R_+`. Positivity and continuity allow logarithmic coordinates, where sewing becomes the
continuous additive Cauchy equation on `R^2`; hence the log transfer is `p x + q y`, and conversely
every such linear functional supplies a character. This supports exactly

```text
T_(p,q)(R,A) = R^p A^q,  (p,q) in R^2.
```

The proof also states that, if only a realized subset were available, the conclusion would be
limited to the subgroup it generates absent an attainability or density hypothesis. The six named
characters are separated by abstract group-domain directions, and `(1.7,2.3)` is used only as an
abstract witness.

The observer transformation is correctly typed: for a chosen `p`, `C_i` is a weighted
scalar-valued component or a one-dimensional representation section, not an observer-independent
scalar when `p` is nonzero. Covariance works for every `p` and therefore selects none.

The endpoint extension has the necessary zero-cochain condition: `W_i` is positive, assigned
consistently at each endpoint on one retained label, and independent of the comparison partner.
The intermediate factor therefore cancels under sewing; arbitrary pair-dependent factors are not
silently admitted.

The boundary statement assumes `J_i>0`, `J_j` approaching zero from above, and a finite nonzero
frequency ratio. It classifies only that one-sided limit. Reversal exchanges the corresponding
one-sided behaviors rather than evaluating an inverse at zero area. Simultaneous numerator and
denominator zeros are explicitly left unclassified because their ratio depends on relative
vanishing order.

## 5. R3 — behavioral evidence repair

R3 passes. I ran the four original registered commands followed by the three repair commands with
`PYTHONDONTWRITEBYTECODE=1`, `UDT_NO_WRITE=1`, and `python3 -B -S`.

| Route | Fresh result | Evidence grade |
|---|---:|---|
| Frozen production | `120010/120010` | Formula and regression checks |
| Frozen exact-log route | `35295/35295` | Exact proposed-formula verification; not completeness proof |
| Frozen historical hostile route | `25/25` | Hard-coded contract enumeration only |
| New semantic mutant route | `14/14` | Independent semantic witnesses |
| New numerical repair route | `4000/4000` | 2,000 direct and 2,000 wide-log-domain cases |

The new semantic route behaviorally distinguishes the required failure modes: nonlinear log
sewing, attempted observer selection of `p`, attempted metric-only selection of `q=-1`,
comparison-dependent endpoint factors, inversion at zero area, simultaneous-zero overreach, and
cross-label aggregation. It also verifies the abstract witness separation. Its assertions are
mathematical checks of the corresponding counterexamples rather than equality comparisons with the
old 25-field baseline.

The numerical repair route reported maximum mixed absolute/relative normalized error
`1.0706291899391277e-14` and maximum log-domain absolute error
`4.547473508864641e-13`. Both are below the unchanged `2e-11` tolerance. The 2,000 log-domain cases
remain sensitive when direct transfer values would be very small.

All recorded result JSON objects were reproduced exactly. Direct source inspection of all six
Python files found only standard-library imports, no dynamic import mechanism, and no network call.
The aggregate's static import scan and its documentary substring checks are bounded integrity
guards only; neither is credited as mathematical proof.

## 6. R4 — repaired aggregate and byte stability

R4 passes.

The repaired aggregate was run twice in the writable ephemeral copy, including once in the original
four-command sequence and once in the registered repair sequence. Both executions returned
`30/30`. The aggregate confirmed:

- all original frozen hashes;
- all read-only source hashes available within the intake;
- exact reproduction of the production, exact-log, contract-enumeration, semantic, and repair
  numerical result objects;
- the repaired provenance and evidence labels;
- the exact bounded landing;
- no-write execution and absence of bytecode.

An independent in-memory SHA-256 snapshot around all seven invocations found no changed, added, or
removed package file. A final complete-tree comparison showed that all 50 copied files remained
byte-identical to `/intake`; no persistent result or bytecode output was created.

## 7. Unchanged bounded G350 landing

The retained landing is unchanged and mathematically consistent within its declared scope:

- The central continuous positive character family remains `T=R^p A^q`, with arbitrary real
  `p,q`; identity, reversal, and sewing do not remove the nonuniqueness.
- Observer covariance types the chosen frequency weight `p` but does not select it.
- `q=-1` follows only after adding the explicitly unadopted sheet invariant; it is not obtained from
  the metric area ratio alone.
- The homogeneous multiplier preserves zero and leaves nonzero source normalization and source
  distribution free.
- Every statement is pointwise and per retained label; no cross-label combination rule follows.
- Endpoint extensions, caustic continuation, a supplied measure, and broader transfer classes
  remain outside the classified two-ratio character problem.

No excluded physical attachment is selected or derived. In particular, the repair does not adopt
photons, energy, optics, brightness, flux, luminosity, probability, detector response,
observational distance, a carried field, a conservation law, a metric/history/source/population,
matter/mass, a scale, `X_max`, or canon. The prior metric kernel, reciprocal result, angular sector,
and owner-provisional response equation remain unchanged.

## Final verdict

ACCEPT_G350_R1_R4_REPAIR_FOLLOWUP
