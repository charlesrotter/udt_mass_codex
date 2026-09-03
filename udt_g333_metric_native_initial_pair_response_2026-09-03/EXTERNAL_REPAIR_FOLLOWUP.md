# G333 External Repair Follow-Up

Date: 2026-09-03
Mode: zero-context, repair-only, intake-only review

## Scope and method

I inspected only `/intake` and used `/work/g333_followup_1788442871` as the writable ephemeral
copy for registered execution. I did not edit any intake evidence file, access any repository, use
web/network tooling, or broaden the research target beyond preregistered repairs R1-R4 and the
unchanged bounded G333 landing.

Authentication performed:

1. `REVIEW_SCOPE.json` matched the allowed repair-only scope in `/intake`.
2. `REVIEW_MANIFEST.sha256` authenticated `REVIEW_MANIFEST.tsv` when checked from the intake root.
3. `python3 -S /intake/package/verify_review_intake.py /intake` passed.
4. An independent manifest replay over every TSV row also passed: all `41` manifest payloads were
   present, size-matched, and SHA-256-matched.

The historical text in `package/EXTERNAL_REVIEW_TRANSMISSION.md` records the prior fresh-review
launch state, including `manifest payloads     36 PASS` at line 14. That is not the current
follow-up intake payload count. The current sealed follow-up intake manifest authenticated `41`
payloads in this review.

## Registered checks

In `/work/g333_followup_1788442871/package` I ran the registered commands from `COMMANDS.md`:

1. `python3 -S derive_initial_pair_response.py --output DERIVATION_RESULT.json`
2. `python3 -S verify_initial_pair_response_independent.py --output INDEPENDENT_VERIFICATION.json`
3. `python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json`
4. `python3 -S verify_package.py --output PACKAGE_VERIFICATION_RESULT.json`

Observed results:

- Production replay passed with `6882` checks, `360` cases, and classifications
  `["METRIC_2_PLUS_1", "COMPLETE_PULLBACK_STRONGER"]`.
- Independent replay passed with `146` checks.
- Hostile mutation replay passed with `9` caught mutations.
- Aggregate package verification passed with `99` gates.
- The regenerated JSON outputs in the work copy were byte-identical to the sealed intake payloads:
  `DERIVATION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`,
  `CATCH_PROOF_RESULT.json`, and `PACKAGE_VERIFICATION_RESULT.json`.

## Repair findings

### R1

Pass. The derivation explicitly types the two-argument notation as the bilinear contraction at
`package/EXACT_DERIVATION.md:37-43`, with the defining line
`H(v,v) := gamma(Hv,v) = (1/2)(L_n gamma)(v,v).` at line 40. The downstream scalar usage is also
written as `gamma(Hv,v)` in the all-direction and pair-germ formulas at lines 105, 157, and 163.
The audit report reflects the same correction at `package/AUDIT_REPORT.md:6-10`.

### R2

Pass. The theorem-level general derivative appears at
`package/EXACT_DERIVATION.md:137-145`, with
`n[gamma(v,v)] = (L_n gamma)(v,v) + 2 gamma(L_n v,v),` at line 141 and the reduced formula tied to
the declared evaluation-point condition `[n,v]=L_n v=0` at line 145. The bounded pair-germ jet is
then stated as `n(h11)=(L_n gamma)(v,v)=2 gamma(Hv,v)` at line 157. The transport convention is
explicitly presented as a calculation convention, not added physical data.

### R3

Pass. The production analytic proof and the independent sampled confirmation are cleanly separated.
`package/EXACT_DERIVATION.md:197-200` states that the independent implementation checks
representative directions, is not a second continuum symbolic proof, and that the exact analytic
all-`mu` proof is carried by the production derivation. The audit report repeats the same boundary
at `package/AUDIT_REPORT.md:27-30`.

### R4

Pass. `package/EXTERNAL_REVIEW_TRANSMISSION.md:32-33` states that the detached manifest seal
establishes internal payload integrity and replay consistency for the sealed intake and does not
establish third-party authorship or provenance outside the intake. The audit report repeats the
same limitation at `package/AUDIT_REPORT.md:44-45`.

## Unchanged bounded landing

I found no evidence that the repair implementation changed any coefficient, sign, branch,
classification, topology boundary, or scientific landing.

Supporting checks:

- The exact formulas remain
  `H_horizontal=(b-C)/2`, `H_vertical=-(C+b)/2`, `H_vertical-H_horizontal=-b`,
  trace-free eigenvalues `(b/3,b/3,-2b/3)`, norm `2b^2/3`, and all-direction scalar
  `gamma(Hv,v)=(b-C)/2-b mu` at `package/EXACT_DERIVATION.md:57-90` and `102-125`.
- Both algebraic branches remain retained at `package/EXACT_DERIVATION.md:24` and line 133.
- The production result still records `checks_passed: 6882` at
  `package/DERIVATION_RESULT.json:6906`, the same landing token at line 6912, and
  `topology_inputs_used: []` at line 14128.
- The maximum conclusion in the derivation remains exactly
  `G332_METRIC_NATIVE_FIRST_RESPONSE_IS_COMMON_PLUS_DIRECTIONAL__COMPLETE_NORMAL_SPATIAL_PAIR_PULLBACK_EXCEEDS_ITS_TERMINAL_SCALAR__FIRST_JET_ONLY_NO_HOPF_SELECTION_OR_STABILITY`
  at `package/EXACT_DERIVATION.md:206-212`.
- The aggregate verifier enforces the same landing, exact classifications, no topology inputs, no
  Hopf selection, repaired wording gates, and byte-exact registered outputs; it passed all `99`
  gates.

## Conclusion

All four preregistered repairs R1-R4 are implemented and bounded correctly. The repaired intake
preserves the sealed G333 scientific landing and replayed evidence without changing the registered
mathematics or scope boundary.

REPAIRS_ACCEPTED__G333_BOUNDED_FIRST_RESPONSE_RETAINED
