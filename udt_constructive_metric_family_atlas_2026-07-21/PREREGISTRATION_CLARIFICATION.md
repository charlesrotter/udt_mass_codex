# Post-outcome clarification of preregistered sampling geometry

Date: 2026-07-21

The historical `PREREGISTRATION.md` remains unchanged. Its R02 design registers one common
`lambda` per coefficient bank, but later prose could be misread as an independent ten-amplitude
scan. Fresh adversarial review exposed that ambiguity.

The correct distinction is:

- all ten latent metric fields are present and none is frozen;
- the abstract latent-to-slot chart Jacobian has rank ten;
- inside each bank, all ten fields and `phi` share one continuous amplitude `lambda`;
- the sampled parameter tuple is `(lambda,x0,x1,x2,x3)` and has only five entries; and
- its observed slot-value tangent ranks are `0:4`, `1:28`, `4:16`, and `5:112`.

Therefore the package is a four-bank correlated-path observation, not an independent scan of ten
metric amplitudes. The finite 128/128 nonzero-record census is unchanged. No genericity, open/dense,
dynamics, or physics conclusion follows.
