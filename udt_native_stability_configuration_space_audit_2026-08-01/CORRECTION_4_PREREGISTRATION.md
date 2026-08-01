# Cold-review correction 4 preregistration

Date: 2026-08-01  
Trigger: fresh cold adversarial review, before result banking

## Defect

The audit correctly makes the basin question well posed only inside declared conditional models,
but two census labels overstate the Hopfion evidence as an explicitly certified basin count. The
registered evidence certifies static finite-box stability within its carrier/action/boundary
premises; it does not enumerate attraction basins or establish a taxonomy count.

## Exact correction

- Replace `conditional_stable_basin_count` with `conditional_stability_scope_count` in the machine
  result.
- Replace “conditional explicitly certified basin scopes” with “conditional
  stability-certificate/model scopes” in prose.
- Preserve the gate statement that the stability/basin question is well posed in the conditional
  Hopfion model, while explicitly denying a certified basin count or taxonomy.
- Update verifiers and dependent hashes.

The native realized-family count remains zero. The primary outcome remains unchanged unless this
wording repair exposes a missing persistence gate.
