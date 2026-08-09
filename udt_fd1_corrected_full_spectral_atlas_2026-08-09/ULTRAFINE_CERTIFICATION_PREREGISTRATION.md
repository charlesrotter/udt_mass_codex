# Ultrafine certification correction — preregistration

Date: 2026-08-09  
Parent strict artifact SHA-256:
`46e8aeda120f6c51fbfc000cf56e5db5a78fe2092ae12b06b20523bc468ec1d5`

## Arithmetic correction

The complete atlas has 10,080 positive roots (`420*3*8`), not 5,040.  Correct the count key and
associated label.  Do not change the row census or infer a scientific distinction from this typo.

## Frozen numerical correction

Re-refine exactly the 24 roots in the only three failing row/channels:

```text
inv_n=0.9284, q/qcrit=0.95, hbar=0.001, wall=D,
m in {-1,0,+1}, radial indices 0..7.
```

Use the same equation, center series, endpoint chart, scan-cell bracket, DOP853 method, and
integration tolerances.  Change only Brent `xtol` from `5e-15` to `1e-18`; keep `rtol=1e-14`.
Require all 24 roots to remain within their saved scan cells and move by `<2e-14` from the strict
artifact.  Recompute their dependent split/displacement/order fields.

The other 10,056 frequencies and all physical/configuration fields must remain exactly equal to the
strict artifact.  The unchanged normalized residual gate is `<2e-8`; the q=0 exact-split gate stays
`<2e-8`.  Write a new artifact and preserve both prior failed returns unchanged.

After this correction, independent verification is still required; a passing production file alone
does not authorize interpretation, observational readout, or FD2.
