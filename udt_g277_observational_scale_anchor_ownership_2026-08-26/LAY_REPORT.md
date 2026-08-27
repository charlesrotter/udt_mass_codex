# G277 lay report

We found a usable route, but it is important to name it honestly.

The ordinary supernova rows tell us the shape of the distance pattern but not its absolute size.
DES has the same limitation. Combining two such relative maps still does not create a tape measure.

Pantheon+ also contains a special calibrator set: supernovae in galaxies whose distances were
estimated independently with Cepheids. Those calibrators can establish how bright a standardized
supernova really is. Once that brightness is known, the rest of the supernova sample can establish
an absolute distance scale.

For UDT this is promising, but conditional. The Cepheid ladder is external observational input, and
we still have to state which UDT distance the photometric distance represents. For now that uses the
temporary light-transfer/area rule Charles already allowed. It does not alter the metric or kernel.

`cmb_temp` is not the right first anchor. A measured sky temperature tells us a redshift only if we
know the source temperature and how the radiation was produced and transferred. Those pieces are
not yet owned. CMB temperature will be more useful later as a far-distance consistency check.

So the next clean experiment is: let the Pantheon+ calibrators set the one scale, freeze everything,
then ask whether DES agrees without retuning. That is calibration followed by a real held-out test.

One data-quality wrinkle was found and kept visible: the published Pantheon+ covariance differs
from its transpose at about three parts in one hundred million in absolute matrix units. Treating
the upper half, lower half, or their average as the intended symmetric covariance gives the same
scale-identifiability result by a wide margin. This does not change the conclusion, but it remains
an explicit release-format caveat.
