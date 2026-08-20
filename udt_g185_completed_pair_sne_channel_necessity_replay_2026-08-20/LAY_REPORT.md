# G185 lay report

The rebuilt kernel passed its first observational non-regression check.

The important simplification is that nothing was manually switched off. For the particular SNe
setup, the line connecting the observer and source points straight outward, so that line has no
sideways motion. That is why the *pair line's* angular contribution is exactly zero. But the light
image still spreads across the observer's sky, and the metric supplies its full area as `R^2`.

Think of looking straight down a long trumpet. Your path through the trumpet can be perfectly
straight while the circular opening still has a nonzero area. “No sideways motion along the path”
does not mean “no opening.”

Keeping that distinction reproduces the earlier Pantheon+ and DES-SN5YR curves essentially digit
for digit. Deliberately removing the sky opening, counting it twice, or using the wrong temporary
light-transfer rule makes both comparisons dramatically worse.

So the good news is: the simpler metric-native pair kernel is compatible with the frozen SNe work,
and its quiet angular contribution here is produced by the query geometry rather than a regime
switch. The remaining caveat is substantial but clean: the temporary light-transfer law and the
radius-versus-redshift curve are still imported/frozen, not newly derived by G185.
