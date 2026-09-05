# G347 run record

Date: 2026-09-04

## Environment

```text
repository: /home/udt-admin/udt_mass_codex
branch: grok
preregistration HEAD: c80d26666d78ff2da28cc8d9b700d7c01bbb6a4d
python: 3.10.12
kernel: Linux 6.8.0-124-generic x86_64
device: CPU
dtype: Python binary64 float
random seeds: 3470904 production; 743471 independent
write mode: UDT_NO_WRITE=1 and PYTHONDONTWRITEBYTECODE=1
```

No GPU process or long solve was used. The computation is bounded local Lorentzian algebra and
one-dimensional quadrature.

## Frozen executions

```text
PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S derive_endpoint_observer_covariance.py
exit 0; PASS; 73924/73924; 1200 boosts above 0.99; 600 explicit noninvariant examples

PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S verify_endpoint_observer_covariance_independent.py
exit 0; PASS; 23547/23547; 345 near-null cases; 206 five-point sky derivatives

PYTHONDONTWRITEBYTECODE=1 UDT_NO_WRITE=1 python3 -S run_catch_proofs.py
exit 0; PASS; 22/22 hostile mutations caught
```

Production and independent stdout are preserved exactly in `DERIVATION_RESULT.json` and
`INDEPENDENT_VERIFICATION.json`; hostile stdout is preserved in `CATCH_PROOF_RESULT.json`.

## Stop conditions

All commands were short deterministic checks. No checkpoint or restart was needed. Any failed
assertion, uncaught hostile mutation, domain violation, or nonzero exit would have stopped the
route and selected a non-`A` alternative.

## External review

The sealed 30-file intake contained 28 manifest payloads plus manifest and detached seal. The
initial authorized `gpt-5.4` launch stopped before review because that model was unavailable.
Charles authorized `gpt-5.6-sol` as the only substitution. External session
`01a06eb8-a333-7d30-a192-f7bec5c8dd53` authenticated the unchanged intake, reran the aggregate,
passed 10,831 independent checks, and accepted the bounded result without required repair.
