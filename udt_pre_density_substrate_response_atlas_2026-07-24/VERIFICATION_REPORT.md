# Verification report

## Production

- Python: `3.10.12`
- SymPy: `1.13.1`
- Source hashes: `20/20`
- Local objects: `15`
- Transformation groups: `10/10`
- Compatibility tests: `12`
- Completion classes: `12/12`
- Conditional probes: `10/10`
- Shape grid: `25/25`
- Maximum determinant residual: `8.882e-16`
- Dual selector: `22` unique, `3` ties
- `GL(2,Z)` selector covariance: `6/6`
- Maximum manufactured conformal residual: `8.882e-16`
- Result: `PASS`

## Independent implementation

The verifier uses the Python standard library only and never imports the
production module.

- Source hashes: `20/20`
- Shape residual: `1.776e-15`
- Dual-selector norm residual: `3.553e-15`
- Dual-selector counts: `22/3`
- Selector covariance: `6/6`
- Five-point conformal residual: `1.393e-12`
- Five-point anisotropy residual: `5.297e-12`
- Catch-proofs: `16/16`
- Result: `PASS`

## Scope

The independent evidence verifies exact formulas and the preregistered finite
atlas. It does not convert the sampled atlas into a theorem about the entire
continuous torus-moduli space, and it does not supply external peer review.

