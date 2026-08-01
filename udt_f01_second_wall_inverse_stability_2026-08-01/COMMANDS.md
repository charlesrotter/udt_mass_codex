# Reproduction commands

Run from the repository root on branch `grok`:

```bash
python3 udt_f01_second_wall_inverse_stability_2026-08-01/build_source_inventory.py
python3 udt_f01_second_wall_inverse_stability_2026-08-01/certify_inverse_surface.py
python3 udt_f01_second_wall_inverse_stability_2026-08-01/verify_inverse_surface.py
python3 udt_f01_second_wall_inverse_stability_2026-08-01/cold_verify_inverse_surface.py
python3 udt_f01_second_wall_inverse_stability_2026-08-01/verify_repository_gates.py
python3 udt_f01_second_wall_inverse_stability_2026-08-01/build_package_manifest.py
python3 udt_f01_second_wall_inverse_stability_2026-08-01/verify_package_manifest.py
```

The primary certificate uses nested 80/100-decimal-digit outward interval integration with
4096/8192 subintervals. The primary-side verifier separately solves the root and recomputes the
same formulas by 80-digit adaptive midpoint quadrature. The cold verifier supplies the genuinely
distinct DOP853 shooting and FEM inertia paths.
