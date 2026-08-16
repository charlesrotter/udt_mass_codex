# Lay report — what the kaleidoscope calculation found

The kaleidoscope picture is useful, but it contains an important distinction.

A normal lens bends every incoming ray independently. It can stretch or brighten the picture, but
if the reference catalog correctly describes the resulting overall density, it does not create a
new relationship between otherwise unrelated galaxies.

A kaleidoscope does something stronger. Its mirrors connect different views. One piece of the
original scene can contribute to several related apparent locations, or two viewing paths can share
one geometric rule. That connected part can create a pattern even when the original scene has none.

G104 proved this distinction exactly:

- independent UDT distortions are a simple-lens null after complete one-point correction;
- a physical density modulation omitted from the mask/selection randoms produces its own
  autocorrelation;
- correlated branches or another genuinely coupled two-path rule produce a connected pattern;
- independently choosing one branch per galaxy is still only a simple lens.

The current metric work has built the machinery capable of evaluating all these cases, but it has
not yet selected the mirrors: no physical modulation field, connected pair kernel, branch family,
or branch weights are owned. Consequently the proposed two-to-four coefficients remain switched
off. Turning them on now would put the missing kaleidoscope into the fitting parameters.

The next step is therefore precise: look in the complete global observer-relation geometry for the
actual mirror coupling—a derived one-point area modulation or a derived connected branch/pair
operator. Once one exists, BAO may calibrate its small number of amplitudes and CMB can test the
frozen result independently.
