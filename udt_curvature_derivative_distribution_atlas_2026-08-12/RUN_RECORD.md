# Run record

Date: 2026-08-12  
Platform: Linux, Python 3.10.12, NumPy 2.2.6, Torch 2.5.1+cu121  
Execution: sequential CPU; no GPU

## Production

```bash
python3 udt_curvature_derivative_distribution_atlas_2026-08-12/derive_derivative_atlas.py
python3 udt_curvature_derivative_distribution_atlas_2026-08-12/verify_tensor_identities.py
```

Production completed all 1,221 rows. Tensor identities pass with worst normalized defect
`1.454655143374363e-14`.

## Independent replay

```bash
python3 udt_curvature_derivative_distribution_atlas_2026-08-12/verify_derivative_atlas_independent.py
```

The independent program intentionally exits nonzero because exact SPI classification passes on
1,211/1,221 rows rather than all rows. Its saved result is:

```text
status                         FAIL
checks                         1,221
exact row passes               1,211
worst tensor relative error    1.2737741822769707e-4
worst outer-ladder difference  1.9296188076108867e-4
```

All derivative-Gram classifications agree. Ten independent SPI ranks enter the preregistered
uncertainty band.

## Frozen-policy adjudication

```bash
python3 udt_curvature_derivative_distribution_atlas_2026-08-12/adjudicate_derivative_atlas.py
```

The adjudicator does not rerun, retune, or overwrite production. It joins the two saved routes and
marks the ten disputed SPI rows unresolved, exactly as the committed control preregistration
requires.

## Adversarially required spectral completion

```bash
python3 udt_curvature_derivative_distribution_atlas_2026-08-12/map_gram_intrinsic_subspaces.py
python3 udt_curvature_derivative_distribution_atlas_2026-08-12/verify_gram_subspaces_independent.py
python3 udt_curvature_derivative_distribution_atlas_2026-08-12/adjudicate_gram_subspaces.py
```

This evaluates the already-saved tensors only. The production and independent maps contain 3,663
rows each. Frozen-policy adjudication returns 397 fully resolved and 3,266 spectrally unresolved
rows. Maximum eigenvalue error is `6.535617696423746e-05`; maximum finite matched candidate-plane
projector defect is `0.00024305041402851194`.
