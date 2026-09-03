# G329 run record

Date: 2026-09-02

## Environment

- branch: `grok`
- symbolic engine: intake-local SymPy 1.13.1 / mpmath 1.3.0 runtime inherited unchanged from the
  accepted G328 package
- arithmetic: exact symbolic rational algebra
- GPU: not used
- grid, tolerance, fitted parameters: none

## Commands

```bash
python3 -S derive_oblique_modes.py --output DERIVATION_RESULT.json --raw-output RAW_RESIDUALS.json
python3 -S verify_independent.py --output INDEPENDENT_VERIFICATION.json
python3 -S run_catch_proofs.py --output CATCH_PROOF_RESULT.json
```

## Results

- production: exit 0, 121/121 gates;
- independent ADM verification: exit 0, 28/28 gates;
- hostile catches: exit 0, 11/11 mutations rejected;
- aggregate package verifier: exit 0, 55/55 gates;
- production and independent landing tokens agree exactly;
- no long process remains running.

The output JSON files preserve the exact check names. `RAW_RESIDUALS.json` preserves every
upper-triangle raw residual from all ten unrestricted amplitudes.
