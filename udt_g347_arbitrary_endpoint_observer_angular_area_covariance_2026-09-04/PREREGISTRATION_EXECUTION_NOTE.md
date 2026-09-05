# G347 preregistration execution note

Date: 2026-09-04

The complete preregistration package was committed and pushed at `c80d2666` before any outcome
script was executed.

The first executions used the exact commands frozen in `COMMANDS.md`:

```text
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S derive_endpoint_observer_covariance.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_endpoint_observer_covariance_independent.py
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S run_catch_proofs.py
```

They returned respectively `73924/73924`, `23547/23547`, and `22/22` with no failure. No candidate
formula, alternative, tolerance, domain, or maximum conclusion was changed after execution.

The first aggregate execution returned `17/19`. Both failures were exact documentary-token checks:
one phrase was split across a Markdown line break, and the audit said `provisional` plus
`owner-adopted` rather than the exact verifier token `owner-provisional`. The derivation, JSON
evidence, scripts, candidate formulas, tolerances, alternatives, and maximum conclusion were
unchanged. Those two wording hooks were repaired before rerunning the aggregate. Fresh external
`gpt-5.6-sol` review later authenticated the unchanged sealed intake and accepted the bounded
result without required repair.
