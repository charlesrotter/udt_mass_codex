# G278 lay report

We successfully attached a real-world length to the previously relative Pantheon+ curve without
changing the UDT kernel or adding angular machinery.

At the primary numerical resolution, that reference length is about `286 Mpc`. The Cepheid-host
supernovae are internally consistent, and the same absolute curve gives an acceptable comparison
to the held-back DES supernova release without adjusting anything to DES.

The important caveat is numerical. The four already-declared ways of drawing the same smooth curve
give reference lengths from about `279` to `299 Mpc`. That spread is too large relative to their
formal uncertainties, so we cannot yet declare one final scale.

This does not look like new non-native scaffolding. Only one overall ruler setting was calibrated;
the redshift rule, curve shape, metric, reciprocal kernel, and angular sector were frozen. The next
check asks whether the variation is mostly caused by defining the ruler at the poorly populated edge
of the data, or whether the physical curve itself really changes in the well-measured middle.

The later CMB-temperature check remains simple: a supplied `3000 K` radiation state redshifted to
`2.725 K` corresponds to `1+z about 1101`, or reciprocal depth `phi about 7`.
