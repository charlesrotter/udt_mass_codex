# G284 External Repair Follow-Up

Verdict: `CONFIRM R1`, `CONFIRM R2`, bounded scientific landing unchanged.

Accepted landing retained unchanged:

```text
EMERGENT_CE_CAUSAL_PROJECTIVE_NETWORK_RECONSTRUCTS_BUT_DOES_NOT_SELECT_TIDAL_HISTORY
```

## Scope

This was a fresh repair-only follow-up against `REPAIR_PREREGISTRATION.md`. I did not reopen the
scientific question or assess anything outside preregistered repairs `R1` and `R2`.

## Materials Read

- `/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/REPAIR_PREREGISTRATION.md`
- `/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/derive_causal_projective.py`
- `/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/derive_causal_projective_sympy.py`
- `/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/verify_package.py`
- `/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/verify_preregistration.py`
- `/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/verify_independent.py`
- `/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/run_catch_proofs.py`
- `/intake/udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/COMMANDS.md`

## Execution Boundary

I executed commands only in writable ephemeral copies.

Baseline disposable root:

```bash
python3 -S udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/verify_preregistration.py
python3 -S udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/derive_causal_projective.py
python3 -S udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/verify_independent.py
python3 -S udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/run_catch_proofs.py
python3 -S udt_g284_emergent_ce_causal_projective_value_law_audit_2026-08-27/verify_package.py
```

The disposable root was constructed with:

- the full package directory;
- the exact 15 manifest-tracked frozen source files at the parent-root paths expected by the
  preregistered hash checks.

Independent hostile bounded repair check:

- created a second disposable copy from the baseline temp root;
- inserted `raise SystemExit("external repair follow-up mutation")` at the start of
  `derive_causal_projective.py`;
- reran `python3 -S .../verify_package.py` without changing the saved JSON artifacts.

## Findings

No repair defects found.

## R1 Review

Confirmed.

Evidence:

- `derive_causal_projective.py` is standard-library only. Its imports are `fractions`,
  `itertools`, and `json`, with no third-party dependency and no `sympy`
  (`derive_causal_projective.py:10-14`).
- The production replay retains all three arbitrary smooth tidal functions as live algebraic atoms:
  `T_xx`, `T_xy`, `T_yy`, together with their first and second `u`-derivative placeholders
  (`derive_causal_projective.py:21-35`), and the `u` derivative rule propagates through exactly
  those three functions (`derive_causal_projective.py:132-152`).
- The production replay still emits 20 exact checks and passes them all. The command output in the
  temp root reported `"status": "PASS"`, `"exact_checks": 20`, and the unchanged landing.
- I extracted the `checks` dictionary keys from both `derive_causal_projective.py` and
  `derive_causal_projective_sympy.py`; the two scripts expose the same 20 check identifiers.
- The former SymPy implementation remains present as supplemental only, consistent with
  `derive_causal_projective.py:2-7` and `COMMANDS.md:13-16`.

Conclusion:

- `R1` satisfies the preregistered acceptance conditions.

## R2 Review

Confirmed.

Evidence from implementation:

- `verify_package.py` defines the four registered replays exactly as required:
  `verify_preregistration.py`, `derive_causal_projective.py`, `verify_independent.py`, and
  `run_catch_proofs.py` (`verify_package.py:42-47`).
- It constructs an ephemeral replay root, copies the package there, and copies each manifest-tracked
  frozen source file into the same temp root layout before execution (`verify_package.py:49-57`).
- Each replay is executed with `sys.executable`, `-S`, and the temp-root script path
  (`verify_package.py:59-68`).
- The verifier records command name, interpreter mode, exit code, and expected-token status for all
  four commands (`verify_package.py:69-77`) and fails closed if any replay exits nonzero or misses
  its status token (`verify_package.py:78-87`).
- The verifier also includes its own hostile mutation check inside the ephemeral copy by breaking
  `derive_causal_projective.py` after baseline certification and requiring that replay to fail
  (`verify_package.py:89-111`).

Evidence from bounded execution:

- In the correctly constructed disposable root, all four registered replays passed under `python -S`.
- `verify_package.py` then passed under `python -S` and reported:
  `replay_commands = [verify_preregistration.py, derive_causal_projective.py, verify_independent.py, run_catch_proofs.py]`
  with exit codes `[0, 0, 0, 0]`, expected tokens found for all four, and
  `"broken_replay_mutation_caught": true`.
- In the second disposable copy, I broke `derive_causal_projective.py` while leaving the saved JSON
  artifacts untouched. `verify_package.py` failed immediately with:
  `failed_replay = derive_causal_projective.py`, `exit_code = 1`,
  `expected_token_found = false`.

Conclusion:

- `R2` satisfies the preregistered acceptance conditions.
- The verifier no longer trusts artifact files alone; it rejects an artifact-level broken replay.

## Landing Status

The accepted bounded scientific landing remains unchanged.

Reasons:

- the production derivation replay in the temp root emitted the same landing string;
- the package verifier in the temp root emitted the same landing string;
- `verify_package.py` explicitly checks the unchanged landing, unchanged counts, frozen-source hash
  integrity, retained premise count, and absence of new imported scientific content
  (`verify_package.py:166-240`);
- nothing in `R1` or `R2` altered the scientific boundary stated in
  `REPAIR_PREREGISTRATION.md`.

## Final Determination

`ACCEPT-WITH-REPAIRS` is now satisfied on the preregistered repair scope. `R1` and `R2` are
confirmed, and the accepted bounded landing remains unchanged.
