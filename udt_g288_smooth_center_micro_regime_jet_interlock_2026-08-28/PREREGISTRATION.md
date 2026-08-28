# G288 preregistration — smooth-center micro-regime jet interlock

Date: 2026-08-28
State: frozen before outcome computation

## Question

Within the bounded primary static-spherical analytic even smooth-center class, determine whether
the metric forces a shared leading micro germ across reciprocal, angular/tidal, curvature, causal,
and mass-aspect diagnostics.

## Candidate exact statements to test

For

\[
f=1+\sum_{k\ge1}c_{2k}r^{2k},
\]

test without assuming the answer:

1. whether the quadratic coefficient contributes to either G201 angular channel;
2. whether the first possible angular term is quartic and, if so, whether its two channel
   coefficients have a fixed ratio;
3. whether the leading curvature motif is constant-curvature/isotropic and the Weyl diagnostic
   begins at a strictly higher order;
4. whether the lapse, static acceleration, and geometric mass aspect share the same leading
   coefficient while remaining distinct physical types;
5. whether radial coordinate-null slope and normalized local null speed have the already registered
   distinct behavior;
6. whether negative \(\phi\) near the center selects any numerical scale or physical mass law.

## Certification contract

Production must:

- start from the current metric components and rebuild all load-bearing differential geometry;
- import no formula from G201, G262, G264, or the July center audit into executable assertions;
- derive the general coefficient formulas, not just sample profiles;
- specialize through at least \(r^8\);
- verify the exact G201 zero-tide family \(f=1+Cr^2\);
- preserve the G262 distinction between geometric mass aspect and physical mass;
- preserve the distinction between coordinate null slope and local normalized speed;
- use exact symbolic/rational arithmetic only.

Independent verification must:

- import no production module or production result;
- reconstruct the connection and curvature from the metric by a different implementation;
- obtain angular, acceleration, mass-aspect, and null expressions from their definitions rather
  than copying an older audit formula;
- test at least 1,000 nondegenerate exact rational coefficient tuples;
- include both signs of \(c_2\) and cases with \(c_4=0\) and \(c_4\ne0\).

Hostile mutations must be caught for at least:

1. an angular \(r^2\) term proportional to \(c_2\);
2. an incorrect leading angular ratio;
3. a nonzero Weyl term for the exact quadratic family;
4. interpreting \(\mu\) as derived physical mass;
5. treating \(c_E f\) as the local normalized light speed;
6. inserting a Planck length or \(X_{\max}\) into the coefficient map;
7. identifying negative profile sign with negative pair-arrow orientation.
8. silently treating agreement with an older audit as certification.

## Falsification

The proposed local-universality reading fails if any exact analytic even smooth-center germ:

- has a quadratic angular/tidal term;
- has a leading curvature germ not controlled by the quadratic metric coefficient;
- makes the exact quadratic family angularly nonquiet;
- or changes the normalized local radial null speed away from \(c_E\).

## Allowed landings

1. `SMOOTH_CENTER_FORCES_A_SHARED_LEADING_MICRO_GERM__NO_SCALE_OR_HISTORY_SELECTED`
2. `PARTIAL_CENTER_INTERLOCK_ONLY__INDEPENDENT_MICRO_JET_FREEDOM_SURVIVES`
3. `NO_CENTER_INTERLOCK__CHANNELS_REMAIN_INDEPENDENT`
4. `PREREGISTERED_TEST_FAILED__NO_SCIENTIFIC_LANDING`

## Maximum conclusion

At most an exact local theorem for the declared analytic even primary-metric center germ.  No
Planck-scale identification, microphysical matter model, physical mass, signal ontology, complete
history, nonspherical/time-live extension, or observational claim may be made.
