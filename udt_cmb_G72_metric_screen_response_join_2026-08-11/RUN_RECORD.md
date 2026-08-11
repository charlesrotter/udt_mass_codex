# G72 run record

Date: 2026-08-11

Base: `074e8939eb24ee2644f1472b4ce9ef6d42c8dbb8`

Preregistration commit: `17c87230`

Source-manifest correction preregistration commit: `9966057f`

## Commands

```text
python3 udt_cmb_G72_metric_screen_response_join_2026-08-11/derive_screen_response.py
python3 udt_cmb_G72_metric_screen_response_join_2026-08-11/verify_screen_response_independent.py
python3 udt_cmb_G72_metric_screen_response_join_2026-08-11/run_catch_proofs.py
python3 udt_cmb_G72_metric_screen_response_join_2026-08-11/verify_package.py
python3 udt_cmb_G72_metric_screen_response_join_2026-08-11/verify_repository_gates.py
```

CPU only. No ODE/PDE solve, fit, GPU process, or external physics input was used.

## Exact outcomes

- corrected frozen source universe: `14` paths;
- symbolic identities: `6/6` pass;
- production gauge/source trials: `512/512` pass;
- independent SVD gauge trials: `1000/1000` pass;
- G68 frozen map replay: `21/21`;
- semantic mutations caught: `14/14`;
- package gates: `12/12`;
- frozen action packages: six manifests, `127` members / `133` paths;
- premise guards: `66`;
- current artifact paths: `1114`;
- frontier registry: `306` rows / `101` targets;
- tests: `98 passed, 1 xfailed`.

Maximum production gauge errors:

```text
M covariance       1.1749496091904413e-15
scale              6.661338147750939e-16
shear              6.217248937900877e-15
relative angle     4.440892098500626e-16
reflection angle   0
source congruence  1.1887038541924998e-14
```

Independent maximum errors:

```text
scale              4.440892098500626e-15
shear              5.551115123125783e-15
relative angle     6.661338147750939e-16
reflection angle   0
```

G68 control replay:

```text
production max relative polar angle    3.549305994648684e-24
independent SVD max angle               1.4354682897494368e-20
max shear magnitude                     0.0023238059699749714
```

Both angle values are unresolved numerical zero on this control tile. The discrepancy is
floating-point polar-factor noise at order `10^-20`, not a physical rotation.

## Provenance correction

The first preregistration froze the G68 exact report but omitted the machine-readable
`FINITE_PATH_ATLAS.tsv` used for the 21-map replay. Before banking, the omission was explicitly
preregistered at `9966057f`; the atlas was added with SHA-256
`a3c013122640f36526915d5ea458559ab3086031e3fabe5797cd9076cfdd66aa`, and every result was
regenerated under the corrected 14-source universe. The scientific landing did not change.

## Protected worktree

Seven untracked stopped-draft paths under
`udt_native_onshell_timelive_reset_owner_audit_2026-08-10/` remained unread, unmodified, and
unstaged.
