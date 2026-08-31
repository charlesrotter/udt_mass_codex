# G309 run record

## Production

```bash
python3 derive_strengthened_history_audit.py --output DERIVATION_RESULT.json
```

Result: PASS, 13 symbolic checks. At `X=1`, `epsilon=0.1`, `T=1`, the deformation has
`Q=-0.1122170734375668...` and `R=12.7896011305518...`, versus base `Q=0`, `R=12`.

## Independent verification

```bash
python3 verify_strengthened_history_independent.py --output INDEPENDENT_VERIFICATION.json
```

Result: PASS, 28 checks. Maximum base trace-free gap `2.220446049250313e-16`; maximum deformed gap
`0.13333930068074173`; maximum sampled scalar-curvature difference from 12
`1.7723697334331678`.

## Hostile mutations

```bash
python3 run_catch_proofs.py --output CATCH_PROOF_RESULT.json
```

Result: PASS, four of four mutations caught.

## Repository gates

```bash
python3 verify_current_scientific_premises.py
python3 -m pytest -q
```

Results: current 289-row premise registry PASS; `199 passed, 1 xfailed in 137.51s`.

The first production attempt was interrupted after an unnecessary full symbolic expansion proved
slow. The exact logarithmic-derivative identity was then used; it changed no preregistered witness,
formula, or conclusion.

