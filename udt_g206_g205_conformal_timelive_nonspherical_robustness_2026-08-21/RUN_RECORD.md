# G206 run record

Date: 2026-08-21

## Commands

```bash
python3 derive_conformal_robustness.py
python3 verify_conformal_robustness_independent.py
python3 run_boundary_diagnostics.py
python3 run_catch_proofs.py
python3 verify_source_manifest_repository.py
```

CPU/SymPy only; no GPU process and no long solve.

## Outcomes

- Production: 27/27 symbolic assertions passed.
- Independent: 160,006 assertions across a direct coordinate-geodesic proof and 10,000 distinct
  algebraic cases passed.
- Boundary: 160-digit controls passed.
- Mutation catches: 19/19 caught.
- Source provenance: seven live repository hashes matched the preregistered manifest.
- External review: `VERIFIED_WITH_CAVEATS`; no mathematical error and no scientific change.

## Fail-closed diagnostic repair

The first boundary run at 80 working digits stopped on the strict inequality between the cutoff-8
partial Gaussian integral and its full value. The remaining tail is about `1.12e-105`, below the
working resolution. The script was changed only to compute that positive tail directly at 160
digits. The registered metric family, witnesses, formulas, and classification were unchanged.

## External-review precision repairs

The landing now says `OMEGA_PULLBACK`, matching `omega=Omega composed F`, and the unsupported word
`first` was removed from the classification description. Neither edit changes a formula or result.
