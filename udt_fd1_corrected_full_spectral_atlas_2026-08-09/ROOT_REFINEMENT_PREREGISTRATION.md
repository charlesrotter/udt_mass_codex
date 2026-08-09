# Strict root-refinement correction — preregistration

Date: 2026-08-09  
Parent failed artifact: `corrected_full_atlas.json`, SHA-256
`59842d806439827cfd385fb46ea3cfee757b7d24a822674c6fc872a1b2eb160f`

## Frozen diagnosis

The full census and five aggregate gates completed, but 54/1,260 row/channel maxima failed the
unchanged `<2e-8` normalized-wall-residual gate.  All are Dirichlet, `q/qcrit=0.95`, small-frequency
cases.  The worst diagnostic root moved only `1.746e-12` under stricter numerical refinement while
its residual fell from `4.499e-5` to `6.606e-13`.

## Correction contract

- Preserve the failed atlas and transcript byte-for-byte.
- Do not change the equation, center series, endpoint compactification, parameter census, positive
  root count, wall data, integration method, integration tolerances, classifications, or residual
  acceptance gate.
- Re-refine all 5,040 saved positive roots, not only the 54 failing row/channel maxima.
- For each saved root, use its frozen scan step and a symmetric initial bracket of `0.75*step`.
  If that interval does not change sign, fail; do not search a replacement branch.
- Use Brent `xtol=5e-15`, `rtol=1e-14`; this is a stricter numerical certification setting than the
  failed absolute `1e-11` root tolerance.
- Require each refined root to remain within its old one-step scan cell and every channel to remain
  positive and strictly ordered.
- Write a new artifact; do not overwrite the failed one.
- Retain the original `<2e-8` normalized-wall-residual gate and exact q=0 split gate.

Maximum conclusion remains a blind, corrected spectral atlas in the declared scalar slice.  FD2,
observational readout, source weights, and physical interpretation remain stopped until the new
artifact is independently checked and frozen.

## Independent subset frozen before verification

Use 21 atlas identities indexed `i=0..20`:

```text
inv_n = INV_N_VALUES[i mod 3]
q_ratio = Q_RATIOS[i mod 7]
hbar = (0.001,0.05,1.0)[floor(i/7)]
wall = (D,N)[i mod 2]
m = (-1,0,+1)[i mod 3]
radial indices = (0,3,7)
```

This fixed set covers every q stratum, all three n values and amplitudes, both walls, all m channels,
and low/middle/high roots.  It will be recomputed with a separately coded endpoint propagator,
tighter integration tolerances, split points `y=0.7,1.0,1.4`, and center radii `1e-6,1e-7,1e-8`.
No identity may be swapped after outcomes are seen.
