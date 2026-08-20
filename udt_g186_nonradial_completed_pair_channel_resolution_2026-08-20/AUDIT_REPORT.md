# G186 audit report — nonradial completed-pair channels

Date: 2026-08-20

## Primary landing

NONRADIAL_COMPLETED_PAIR_CHANNELS_RESOLVE_WITHOUT_EXTRA_SCALAR
__CLOCK_ANGULAR_NORM_CONTROLS_DEPTH
__FULL_ANGULAR_GRAM_CONTROLS_TAPE_SHIFT_AND_LOCAL_SCREEN

Current grade: EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS.

## What was learned

For the supplied bounded nonradial germ family, the primary metric itself separates the angular
response cleanly:

- angular motion of the calibrated clock leg changes completed endpoint depth through
  \(\nu^2=e^{2\phi}r^2\lvert w_0\rvert^2\);
- angular motion of the ruler leg changes tape density;
- the clock-ruler angular inner product changes shift;
- non-collinearity enters through the squared angular wedge area;
- the full local screen projector follows from \(g\) and the pair plane;
- no scalar mu, mixing coefficient, regime switch, or post-readout correction survives.

The endpoint scalar is

\[
\Phi=\phi-\frac12\log(1-\nu^2).
\]

For a static clock, \(\nu=0\), so \(\Phi=\phi\) even with a nonradial ruler. The angular ruler
remains live in the tape. This explains the exact G185 radial non-regression without suggesting
that angular physics was disabled or numerically tuned away.

## Evidence

- preregistered at commit ac5877d1;
- 10/10 source hashes verified;
- 14/14 production symbolic checks;
- 20,000 independent exact-Fraction witnesses;
- 320,000 independent exact assertions;
- exact collinear, non-collinear, static-clock, rotation, and reparameterization controls;
- 18/18 executable mutation catches;
- 12/12 semantic guards.
- fresh external gpt-5.4 replay: `G186_ACCEPTED_WITH_STATED_BOUNDS`.

## Caveats

The pair germ is supplied, and the clock/ruler component restrictions define one bounded local
query class. The local screen projector is not a finite Jacobi map or luminosity response. G186
does not derive physical observer population, finite propagation, transfer, R(Z), a nonspherical
ambient metric, global completion, or downstream physics.
