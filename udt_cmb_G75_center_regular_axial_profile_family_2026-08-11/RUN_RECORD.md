# G75 run record

Date: 2026-08-11

Base: `ac01381bf2ec624ec401f1fb13f5db013f0605e0`

Preregistration commit: `e88d7511`

Commands:

```text
python3 udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/derive_profile_family.py
python3 udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/verify_profile_family_independent.py
python3 udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/verify_package.py
python3 udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/run_catch_proofs.py
```

Execution: bounded CPU exact algebra only. No GPU, ODE/PDE, geodesic, Jacobi, source, survey, or
spectrum process was launched.

The first independent root replay used an endpoint-subtraction interpretation of SymPy root counts
that mishandled double boundary roots. Before any result was banked, it was replaced with exact real
root isolation and explicit exclusion of point intervals at `s=0` and `s=1`. The corrected replay
passes all 49 shapes. No candidate definition, outcome, tolerance, or classification was changed.

Fresh external adversarial review: not yet run. The package is therefore recorded as an internally
replayed bounded lead.
