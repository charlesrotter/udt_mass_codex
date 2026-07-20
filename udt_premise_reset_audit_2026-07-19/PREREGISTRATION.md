# UDT premise-reset audit — preregistration

Date: 2026-07-19

Base: `3b6dedf9bd2692b0ff5ba9e871d7952cf8752aad`

Trigger: Charles's concern that the July 19 chain may contain additional semantic misconceptions
after negative physical distance, loss of the Reciprocal-c anchor, and conflation of signed local
`phi` with nonnegative separation were identified.

Mode: audit and confidence regrade only. No new field equation, action, source, carrier, boundary
formula, or numerical solution may be constructed. Every existing package remains byte-identical.

## Whole question

Which claims in the complete tracked July 19 scientific-package chain remain supported when the
owner-approved meanings of `c`, `phi`, physical distance, observer comparison, `X_max`, density, and
the finite-cell boundary are held fixed? Which calculations remain algebraically useful but lose
their UDT interpretation, and which results require clean rederivation?

## Frozen owner-meaning ledger

These are controlling interpretations for this audit, not additions to `CANON.md`:

1. `c_E` is finite Einsteinian `c`, measured at terrestrial and solar scales. It is the ordinary
   clock/length conversion baseline.
2. Apparent extreme-scale propagation changes, if any, must come from the metric's dilation/readout;
   this audit does not postulate a replacement local constant.
3. `phi(p)` may be signed and belongs to a location. Its exact physical normalization remains to be
   traced to the metric.
4. Physical distance or separation magnitude is nonnegative. Negative `phi` is not negative
   distance.
5. An ordered comparison between observers may be signed and reverses when observer order reverses.
   It is not identical to physical distance or angular direction reversal.
6. `X_max` is one global value shared by all observational frames of a completed universe. It is a
   derived output of the metric/bootstrap involving `c_E` and possibly global mass/density; it is not
   a freely supplied numerical ceiling or a second founding constant.
7. Global density is total universe mass divided by total universe volume. Local density effects are
   unresolved because native mass emergence/source coupling remains open.
8. The finite-cell boundary is expected to arise as an asymptotic limit of time and mass dilation.
   Finiteness may be structural, but the numerical `X_max` and boundary location must not be inserted
   and then reported as derived.
9. UDT remains metric-led. Standard-theory structures may be comparison/readout only.

## Frozen package universe

`PACKAGE_UNIVERSE.tsv` contains every tracked top-level scientific evidence package dated
2026-07-19 and carrying `SHA256SUMS.txt` at the base. It was frozen by path, manifest SHA-256, entry
count, and introducing commit before substantive package-content inspection. Expected count: 19.

Generated audit records must not change this universe or modify its packages.

## Required distinctions

Every reviewed claim must distinguish:

- exact algebra or computation;
- semantic identification of its variables;
- physical UDT interpretation;
- dependence on the corrected owner meanings;
- remaining conditional premises; and
- whether clean rederivation is required.

Allowed primary regrades are exactly:

- `SURVIVES_INDEPENDENT`;
- `SURVIVES_CONDITIONAL_RELABELED`;
- `ALGEBRA_VALID_PHYSICS_WITHDRAWN`;
- `CONTAMINATED_RERUN_REQUIRED`;
- `REFUTED_BY_OWNER_MEANING`;
- `OUT_OF_SCOPE_NOT_REVIEWED`.

No package may receive a blanket grade solely from its filename, date, or manifest status. A package
may have multiple claim rows, but must receive one conservative package-level navigation grade.

## Registered audit procedure

1. Inventory exact premise words and symbols used by each package.
2. Build a machine-readable dependency graph from owner meanings through package premises to
   conclusions.
3. Identify every use of signed distance, signed `phi`, fixed or freely supplied `X_max`, imported
   observer mechanics, local/global `c`, density/source, hard boundary, carrier, action, and
   Lorentzian readout.
4. Re-run load-bearing algebra only to check what the package actually computed. Do not use that
   replay to repair its interpretation.
5. Regrade each load-bearing conclusion and each of the 19 packages.
6. Separately identify older inputs on which July 19 packages rely; do not silently certify those
   older inputs.
7. Update live controls only after the evidence package and independent verifier pass.

## Fail-closed checks

The verifier must reject:

- a missing or duplicate package;
- any mutation of the 19 frozen package manifests or their entries;
- treating signed `phi` as negative physical distance;
- treating nonnegative distance as proof that `phi` is nonnegative;
- treating `X_max` as an independently postulated constant or freely selected physical boundary;
- treating global density as a derived local matter source;
- treating asymptotic boundary examples as a completed derivation without premise review;
- promoting an algebraic identity directly to UDT physics;
- treating a prior verification result as semantic validation under corrected meanings;
- declaring all prior work either valid or invalid without claim-level dependency evidence;
- changing `CANON.md`, research artifacts, prior packages, scripts, data, or manifests; and
- declaring the action, source, carrier, boundary, `X_max`, or unconditional mass closed.

## Evidence gates

Before banking:

1. preregistration must precede substantive package audit;
2. all 19 packages and all selected load-bearing claims must be covered;
3. an independent verifier must reconstruct package coverage and semantic catches;
4. every new premise and every inherited premise must be status-stamped.

## Maximum conclusion

This audit may withdraw inherited confidence, preserve exact computations in narrower scopes, and
identify the smallest clean rederivation frontier. It may not derive new physics or claim complete
UDT closure.

## Stop line

After the dependency ledger, regrade, independent verification, package freeze, lean live-navigation
correction, commit, push, and normal non-force integration to `grok`, stop before derivation, GPU
work, canonization, repository reorganization, or matter/action continuation.
