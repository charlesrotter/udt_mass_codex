# G196 independent execution freeze

Date: 2026-08-20

Frozen before the first outcome-producing execution of
`verify_longitudinal_screen_mixing_independent.py`:

- histories: 204 = 12 named + 192 seeded random;
- per-history assertions: 26;
- global activation/alias/pure-rotation assertions: 9;
- exact total: 5,313 assertions;
- seed: 1960820;
- tensor ceiling: `3e-8`;
- algebra ceiling: `3e-10`;
- IVP: SciPy `DOP853`, `rtol=2e-12`, `atol=2e-13`;
- expected landing only if every gate passes:
  `NULL_DIRECTIONAL_DESCENT__FACTORIZATION_AND_NO_CAUSTIC_SURVIVE`.

The implementation does not import the production module or read its result. Its only output write
is `INDEPENDENT_VERIFICATION.json`, suppressed when `G196_NO_WRITE=1`.
