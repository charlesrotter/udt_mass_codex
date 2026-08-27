# G278 lay report

We successfully attached a real-world length to the previously relative Pantheon+ curve without
changing the UDT kernel or adding angular machinery.

At the primary numerical resolution, that reference length is about `286 Mpc`. The Cepheid-host
supernovae are internally consistent, and the same absolute curve gives an acceptable comparison
to the held-back DES supernova release without adjusting anything to DES.

The important caveat is numerical. The four already-declared ways of drawing the same curve give
reference lengths from about `279` to `299 Mpc`. That spread is too large relative to their formal
uncertainties, so we cannot yet declare one final scale. A separately preregistered follow-up shows
that this is not only an edge-label problem: the flexible reconstructions also diverge in the
sparsely measured high-redshift sector. The well-measured middle is much steadier.

This does not look like a corruption of the native kernel. It shows that the nonparametric G236
curve is an observational reconstruction, not yet the unique metric-native distance curve. Choosing
one knot count, smoothing the curves, or averaging their scales would add scaffolding, so none of
those repairs is allowed.

The later CMB-temperature check remains simple: a supplied `3000 K` radiation state redshifted to
`2.725 K` corresponds to `1+z about 1101`, or reciprocal depth `phi about 7`.
