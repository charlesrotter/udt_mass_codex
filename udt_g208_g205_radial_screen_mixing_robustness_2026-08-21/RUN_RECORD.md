# G208 run record

Date: 2026-08-21

## Commands

```bash
python3 derive_radial_screen_mixing.py
python3 verify_radial_screen_mixing_independent.py
python3 run_boundary_diagnostics.py
python3 verify_source_manifest_repository.py
python3 run_catch_proofs.py
python3 verify_package.py
```

CPU, SymPy, exact standard-library fractions, and mpmath only. No GPU process or long solve.

## Outcomes

- Production: 20 exact symbolic assertions passed.
- Independent: 120,004 assertions across 10,000 distinct exact-rational cases passed.
- Boundary: 240-digit controls passed for four odd-`n` profiles and five mixing magnitudes.
- The direct infinite integral was deliberately replaced by finite quadrature plus an analytic
  incomplete-gamma tail bound; this is faster and stronger than brute-force quadrature to infinity.
- Mutation catches: 23 passed.
- Source provenance: nine live repository hashes matched the preregistered manifest.
- External review: `VERIFIED_WITH_CAVEATS`; no mathematical refutation. The reviewer required only
  explicit evidence-scope wording and replacement of one imprecise lay phrase.

The exact-rational implementation certifies the finite-dimensional local algebra and pair
response. The high-precision diagnostic separately certifies the finite witness-tail and
sharp-bound anchors. Neither mechanizes the global analytic proofs. The nine live source hashes
were checked in repository context and are recorded, but the sealed no-write replay does not rerun
that live-repository step.
