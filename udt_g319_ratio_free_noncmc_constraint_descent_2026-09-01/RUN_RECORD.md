# G319 run record

Date: 2026-09-01  
Device: CPU  
Arithmetic: exact Python `Fraction` for load-bearing local identities; double precision only for
explicit periodic replay controls  
Long solve: none  
GPU: unused

## Registered commands

```text
python3 derive_ratio_free_family.py
python3 verify_independent.py
python3 run_catch_proofs.py
python3 verify_package.py
```

## Current results

- production exact assertions: 87,586;
- implementation-distinct direct-tensor assertions: 35,059;
- compatible exact `B=0` germs: 324;
- production periodic variable-ratio controls: 8;
- independent periodic variable-ratio controls: 6;
- hostile mutations caught: 69 of 69;
- maximum production direct residual: below `1.7e-14`;
- maximum independent direct residual: below `6.7e-15`;
- current scientific-premise verifier: PASS, all 301 exact registry rows;
- full repository regression: 214 passed and one known xfail;
- sealed pre-review aggregate package verifier: `PASS_PENDING_EXTERNAL_REVIEW`;
- all G319 Python sources compile;
- no long numerical solve and no observational data.

The fresh external reviewer authenticated all 33 sealed payloads, ran all four registered commands,
reproduced all five generated artifacts byte-for-byte, independently rederived the load-bearing
result, and returned
`G319_ACCEPTED__RATIO_FREE_REGULAR_QUADRATURE_AND_ANSATZ_SCOPE_UPHELD`. The global `B=0` crossing
classification remains open. A CLI output-path collision replaced the detailed response after it
had been recorded verbatim in the transcript; the exact detailed report, two-line CLI final, and
raw transcript are all preserved with hashes in `EXTERNAL_REVIEW_TRANSMISSION.md`.

After review, one missing LaTeX backslash before `\left` in equation (2) was repaired. This is a
typesetting-only correction; the code, generated evidence, equation content, and landing are
unchanged.
