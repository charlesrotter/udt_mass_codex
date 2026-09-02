# External Repair Follow-Up Review — G325 R1

## Scope and method

I treated this as a fresh zero-context, repair-only review. I inspected only `/intake`, used `/work` for ephemeral replay, did not edit evidence files, and did not reopen the scientific question. The sealed scope explicitly limits review to R1 and unchanged bounded support: [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:2), [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:7), [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:9), [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:11).

## Authentication

I authenticated the intake before relying on any scientific or replay claims.

- The detached seal matches the manifest SHA-256. `REVIEW_MANIFEST.sha256` contains `151129cbfbb3431118352175eecfa85a03a2f7d9832c2993eecffefc2f371f04`: [REVIEW_MANIFEST.sha256](/intake/REVIEW_MANIFEST.sha256:1). A direct `sha256sum /intake/REVIEW_MANIFEST.tsv` returned the same digest.
- The scope file hash also matches the manifest entry: [REVIEW_MANIFEST.tsv](/intake/REVIEW_MANIFEST.tsv:20).
- The manifest registers 33 payloads, consistent with the scope metadata: [REVIEW_SCOPE.json](/intake/REVIEW_SCOPE.json:7), [verify_review_intake.py](/intake/verify_review_intake.py:22), [verify_review_intake.py](/intake/verify_review_intake.py:29).
- I ran `python3 -S /intake/verify_review_intake.py` from `/work`; it returned `status: PASS`, `manifest_payload_count: 33`, `total_file_count: 35`. The verifier checks file presence, byte counts, and SHA-256 for every manifest payload: [verify_review_intake.py](/intake/verify_review_intake.py:21), [verify_review_intake.py](/intake/verify_review_intake.py:23), [verify_review_intake.py](/intake/verify_review_intake.py:27), [verify_review_intake.py](/intake/verify_review_intake.py:32).

## R1 verification

### 1. Vacuous production assertion removed

Registered R1 states that `derive_modes.py` had recorded `time_shift_lie_derivative_witness` as the tautology `2*P[index] == 2*P[index]`, and required removal of that production gate while retaining the independent witness: [REPAIR_LEDGER.tsv](/intake/REPAIR_LEDGER.tsv:2).

In the current sealed `derive_modes.py`, the gauge section contains only the substantive ODE check
`gauge_ode_solution` at lines 141-145, followed immediately by the sample residual checks at line 147: [derive_modes.py](/intake/derive_modes.py:141), [derive_modes.py](/intake/derive_modes.py:145), [derive_modes.py](/intake/derive_modes.py:147). The current source does not record `time_shift_lie_derivative_witness`, and the current production artifact check list omits it as well: [DERIVATION_RESULT.json](/intake/DERIVATION_RESULT.json:10), [DERIVATION_RESULT.json](/intake/DERIVATION_RESULT.json:46).

### 2. Production accounting is now 36, and the aggregate verifier expects 36 production assertions

The banked production artifact declares `assertion_count: 36`: [DERIVATION_RESULT.json](/intake/DERIVATION_RESULT.json:4). The current `derive_modes.py` writes `"assertion_count": len(checks)` into the artifact: [derive_modes.py](/intake/derive_modes.py:198), [derive_modes.py](/intake/derive_modes.py:202).

The aggregate verifier now explicitly requires the production artifact to carry 36 assertions:
[verify_package.py](/intake/verify_package.py:37), [verify_package.py](/intake/verify_package.py:38). I also ran the literal fourth registered command, `python3 -S verify_package.py`, in the ephemeral copy; it exited successfully and passed its `production_assertion_count` gate. Its own aggregate result has `assertion_count: 37`, but that is the verifier's total number of checks, not a reversion of the production artifact to 37. On the repair question actually posed, the production accounting is consistent.

### 3. Literal four-command replay reproduced the three banked JSON artifacts exactly

The registered commands are exactly these four lines: [REPLAY_COMMANDS.txt](/intake/REPLAY_COMMANDS.txt:1), [REPLAY_COMMANDS.txt](/intake/REPLAY_COMMANDS.txt:2), [REPLAY_COMMANDS.txt](/intake/REPLAY_COMMANDS.txt:3), [REPLAY_COMMANDS.txt](/intake/REPLAY_COMMANDS.txt:4).

I copied `/intake` to a fresh writable directory under `/work/g325_r1_review.pfA9w4` and ran those four commands literally there. All four exited with code 0. For the first three commands, I checked exact artifact equality against the banked intake files with `cmp -s`; all three comparisons returned `0`. I also compared SHA-256 digests:

- `DERIVATION_RESULT.json`: regenerated and banked both `1e37ab61628aa9bd156dd573d37bd74bc6dbeac1464661f4d70c7b8312817e71`
- `INDEPENDENT_VERIFICATION.json`: regenerated and banked both `103a8b40e208fb831d8661154359c4109ca4023bfe24c3071ca8a4d3e22bea94`
- `CATCH_PROOF_RESULT.json`: regenerated and banked both `7f1d2cb484c25bb7d773f5dd5cd9f71ea5c2265491ee622111d5b1293a35b609`

This satisfies the exact replay requirement, not merely semantic JSON equality.

### 4. The genuine independent direct Lie-derivative witness remains, and the external derivation still supports the gauge classification

The independent verifier still contains the direct Lie-derivative calculation in synchronous coordinates:
[verify_independent.py](/intake/verify_independent.py:221), [verify_independent.py](/intake/verify_independent.py:227). It computes the gauge mode metric directly, differentiates the background metric, and gates equality componentwise as `direct_time_shift_lie_derivative:{spatial}`. The banked independent artifact records those checks and `time_shift_is_lie_derivative: true`: [INDEPENDENT_VERIFICATION.json](/intake/INDEPENDENT_VERIFICATION.json:107), [INDEPENDENT_VERIFICATION.json](/intake/INDEPENDENT_VERIFICATION.json:109), [INDEPENDENT_VERIFICATION.json](/intake/INDEPENDENT_VERIFICATION.json:136).

The external review's own derivation remains present in the sealed intake and still supports classification of the `1/T` mode as residual time-origin gauge. It derives the six-constant solution
[EXTERNAL_REVIEW_RESPONSE.md](/intake/EXTERNAL_REVIEW_RESPONSE.md:50), [EXTERNAL_REVIEW_RESPONSE.md](/intake/EXTERNAL_REVIEW_RESPONSE.md:75),
then states the time-shift classification directly via the Lie derivative
[EXTERNAL_REVIEW_RESPONSE.md](/intake/EXTERNAL_REVIEW_RESPONSE.md:79), [EXTERNAL_REVIEW_RESPONSE.md](/intake/EXTERNAL_REVIEW_RESPONSE.md:85).

## Unchanged bounded landing

R1 did not reopen or change the scientific landing supported in the sealed intake.

- The adopted bounded equation and background metric are unchanged: [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:12), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:22), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:25).
- The general solution and six-constant census are unchanged: [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:117), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:142).
- The gauge, quotient-modulus, local shear, and connected scalar classifications are unchanged: [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:146), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:168), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:203), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:216).
- The bounded non-promotion remains explicit: [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:236), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:247), [EXACT_DERIVATION.md](/intake/EXACT_DERIVATION.md:249), [LAY_REPORT.md](/intake/LAY_REPORT.md:16), [LAY_REPORT.md](/intake/LAY_REPORT.md:20).
- The banked production artifact still carries the same landing token, same mode dimensions, and the same open-sector flags: [DERIVATION_RESULT.json](/intake/DERIVATION_RESULT.json:49), [DERIVATION_RESULT.json](/intake/DERIVATION_RESULT.json:52), [DERIVATION_RESULT.json](/intake/DERIVATION_RESULT.json:55), [DERIVATION_RESULT.json](/intake/DERIVATION_RESULT.json:61), [DERIVATION_RESULT.json](/intake/DERIVATION_RESULT.json:64), [DERIVATION_RESULT.json](/intake/DERIVATION_RESULT.json:67).
- The status ledger still keeps the result at the already bounded grade, with full linear stability, nonlinear stability, occupancy, scale, and `X_max` all open, and with no metric/kernel/angular change: [STATUS_LEDGER.tsv](/intake/STATUS_LEDGER.tsv:2), [STATUS_LEDGER.tsv](/intake/STATUS_LEDGER.tsv:7), [STATUS_LEDGER.tsv](/intake/STATUS_LEDGER.tsv:12).

## Verdict

R1 is complete. The vacuous production assertion has been removed from `derive_modes.py`; the production artifact now declares 36 assertions; the aggregate verifier now expects 36 production assertions; the four registered commands replay literally and reproduce the three banked JSON artifacts byte-for-byte; the independent direct Lie-derivative witness remains intact; and the already accepted bounded G325 landing remains unchanged and supported within the sealed scope.

ACCEPT__G325_R1_REPAIR_AND_UNCHANGED_BOUNDED_LANDING
