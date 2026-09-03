# G336 repair-only external follow-up

Date: 2026-09-03
Mode: zero-context, repair-only, sealed-intake review

## Scope authentication

I inspected only `/intake`, then copied the sealed tree to `/work/g336_repair_followup_lJONa0` before running any executable checks.

Authentication results:

1. `REVIEW_SCOPE.json` matched its manifest entry exactly.
2. `sha256sum /intake/REVIEW_MANIFEST.tsv` matched `REVIEW_MANIFEST.sha256` exactly:
   `7a89ada1da5713ffd294df59855f90c0818f43f593b6674fc1efa658d028bad6`.
3. The exact sealed file set matched the manifest contract: 42 files total, consisting of 40 manifest payloads plus the two detached manifest files.
4. Every manifest payload matched its declared byte count and SHA-256 exactly.
5. The copied intake passed the sealed verifier:
   `python3 -B -S /work/g336_repair_followup_lJONa0/package/verify_review_intake.py /work/g336_repair_followup_lJONa0`
   returning `G336 intake PASS: 40 payloads`.

## Repair review

1. The inherited zero-surface statement is now restricted to the strict interior only.
   `package/EXACT_DERIVATION.md:132` states: `For the strict interior 0<mu<1`.
   `verify_package.py` also explicitly enforces both the repaired strict-domain text and the absence of the old `0<mu<=1` wording, and that aggregate verifier passed.

2. `mu=1` remains only a branch-meeting closure-boundary diagnostic.
   `package/EXACT_DERIVATION.md:160-167` classifies `mu=1` as the vertical closure boundary and states that it is not counted as a lawful strict two-branch G332 datum.
   `package/EXACT_DERIVATION.md:223-224` again keeps that boundary outside the strict family.
   `package/DERIVATION_RESULT.json` retains `vertical_mu_one: branch-meeting closure boundary only`.

3. I found no evidence that the repair changed algebra, coefficients, branches, check counts, premises, conclusions, or the bounded landing.
   The reduced formula is unchanged at `package/EXACT_DERIVATION.md:123-125`:
   `s1 = 1 + (Lambda-3)mu + 3b^2 mu^2(1-mu) = 1 + (R-6)mu/2 + b^2 mu^2`.
   The bounded landing string is unchanged in `package/EXACT_DERIVATION.md:8-13`, `package/AUDIT_REPORT.md:8-13`, `package/DERIVATION_RESULT.json`, and `package/PACKAGE_VERIFICATION_RESULT.json`.
   The registered replay counts remain unchanged and exact:
   production `48375`, strict silent `576`, vertical boundary `48`, strict boost `9792`, independent `3860`, hostile mutations caught `14`.

4. Every registered no-write replay still passes in the writable ephemeral copy.
   I ran only the preregistered commands from `package/COMMANDS.md` in `/work/g336_repair_followup_lJONa0/package`:
   `python3 -B -S derive_silent_second_response.py --output DERIVATION_RESULT.json`
   `python3 -B -S verify_silent_second_response_independent.py --output INDEPENDENT_VERIFICATION.json`
   `python3 -B -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json`
   `python3 -B -S verify_package.py --output PACKAGE_VERIFICATION_RESULT.json`
   Results:
   production replay passed with `48375` checks;
   independent replay passed with `3860` checks;
   hostile replay passed with `14` mutations caught;
   aggregate verifier passed with `97` gates.
   The regenerated registered outputs in the writable copy were byte-identical to the sealed registered outputs for `DERIVATION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`, `CATCH_PROOF_RESULT.json`, and `PACKAGE_VERIFICATION_RESULT.json`.

## Conclusion

The sealed intake authenticates cleanly. The R2 repair is present in the exact derivation at the intended scope boundary, `mu=1` remains only a closure-boundary diagnostic, the bounded landing and registered scientific content remain unchanged, and all preregistered no-write replays still pass in a writable ephemeral copy.

REPAIRS_ACCEPTED__G336_BOUNDED_SILENT_SECOND_JET_RETAINED
