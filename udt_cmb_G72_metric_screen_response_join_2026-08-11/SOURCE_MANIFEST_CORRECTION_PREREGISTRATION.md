# G72 source-manifest correction — preregistration

Date: 2026-08-11

Base preregistration commit: `17c87230`

## Finding

The registered derivation includes a bounded replay of all `21` frozen G68 response matrices. The
original `SOURCE_MANIFEST.tsv` froze the G68 exact derivation but omitted the machine-readable table
from which those matrices are read:

```text
udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/FINITE_PATH_ATLAS.tsv
```

Its SHA-256 before correction is:

```text
a3c013122640f36526915d5ea458559ab3086031e3fabe5797cd9076cfdd66aa
```

## Correction contract

1. Preserve the original preregistration and commit unchanged.
2. Add exactly this one frozen data source to `SOURCE_MANIFEST.tsv` with role
   `FINITE_JACOBI_DATA`.
3. Change the expected source count from `13` to `14` in all verifiers and reports.
4. Make the independent verifier read the original frozen G68 table directly rather than trusting
   the production-derived response atlas.
5. Regenerate every result after the correction.
6. Do not change a scientific status or threshold unless direct replay contradicts the first run.

Maximum conclusion remains the registered G72 landing set. This correction repairs provenance; it
does not authorize a new source, endpoint, profile, observable, or physical claim.
