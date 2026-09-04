# G343 map — bilocal screen phase-space propagation

Date: 2026-09-04
Status: preregistration stage

## Whole question

On the exact supplied G341/G342 Taub/Kasner spacetime and a single labelled null ray, does the
four-metric determine a full bilocal four-by-four map carrying arbitrary screen separation and
screen direction from any positive-time point to any other? If so, classify its exact composition,
Wronskian/symplectic invariant, endpoint reversal, relation between common-affine and separately
source-normalized descriptions, both principal-direction limits, and compact-lattice path labels.

This is `METRIC_LED` and observing rather than targeting. It extends G342's vertex map to arbitrary
screen phase-space data. It does not attach luminosity, electromagnetic transfer, observational
distance, a physical route, or a population.

## Exact bounded arena

Use only

\[
 g=-dT^2+C_X^2T^{-2/3}dX^2+C_\perp^2T^{4/3}(dY^2+dZ^2),\qquad T>0,
\]

the G341 parallel quotient-screen basis, every projective null direction, one supplied positive-time
reference event on the ray, one positive affine normalization held fixed along the ray, arbitrary
positive endpoint times, and every supplied compact-lattice lift. The reference event is coordinate
bookkeeping and the affine normalization is gauge; neither is a physical energy or selected scale.

Write the projective direction without an axis singularity as

With the G341 invariant `lambda=C_X p_perp/(C_perp |p_X|)` and supplied reference time `T_*`, write

\[
 \rho={T_*^2\over T_*^2+\lambda^2}\in[0,1],\qquad
 \nu=\left.{dT\over ds}\right|_{T_*}>0.
\]

Thus `rho` depends only on the dimensionless ratio `lambda/T_*`, while `nu` fixes affine gauge.
Changing `T_*` merely re-coordinates the same ray and must leave the propagator unchanged after the
derived parameter conversion. No unlike dimensionful quantities are added.

The calculation must retain both screen coordinates and both screen derivatives. Axial symmetry
may diagonalize the two scalar sectors, but the four-dimensional phase-space invariant and its
endpoint transformations must be checked rather than inferred from G342's determinant.

## Pure and easy routes

- Pure route used here: mark one arbitrary reference event, keep its affine gauge along the entire
  ray, derive the full metric tidal system, construct the bilocal fundamental matrix, verify
  reference-event covariance, and only afterward translate to separate endpoint clock
  normalizations. This keeps composition and reversal well typed without inserting a scale.
- Easier control only: multiply independently source-normalized G342 vertex maps. That loses the
  common derivative units at intermediate points and is therefore preregistered as an invalid
  shortcut, not a candidate physical construction.

## Required classifications

1. Derive every block of the `4 x 4` map from the metric Jacobi system for arbitrary positive
   endpoint times.
2. Prove or refute exact composition and preservation of the canonical screen Wronskian.
3. Derive endpoint reversal in a common affine gauge and the conversion law when each endpoint
   independently declares unit local frequency.
4. Prove that changing the supplied reference event only changes the direction/gauge coordinates,
   not the physical propagator.
5. Recover the G342 vertex map as a boundary case rather than treating it as a new premise.
6. Take nonsingular longitudinal and transverse principal limits.
7. Retain each compact lift as a separate path-labelled propagator and distinguish composition on
   one lift from summing or selecting lifts.
8. Audit affine gauge, endpoint basis, direction chart, and every forbidden physical attachment.

## Maximum conclusion

At most G343 may derive and classify the bilocal geometric screen phase-space propagator on this one
supplied exact spacetime and its supplied labelled null rays. It cannot turn the map into observed
brightness or distance, choose signal routes or populations, select topology or occupancy, establish
generic or nonlinear stability, attach matter/mass, determine a physical scale or `X_max`, or enter
canon.
