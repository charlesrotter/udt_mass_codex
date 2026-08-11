# Cold external review dispatch — F01/F02 observer-sky Jacobi controls

## Role and containment

Act as a fresh hostile differential-geometric, computational, and type-system reviewer. Inspect
only the sealed read-only intake. Do not edit files, continue the research, inspect anything
outside the intake, choose a physical control/profile/query, or infer local signal propagation.

## Provisional claim to attack

```text
LOCAL_SKY_MAP_GEOMETRY_DISTINGUISHES_F01_F02_WITH_PROFILE_REMAINDER
```

On one identical preregistered equatorial observer-sky query, the package claims:

```text
T_F01=0,
T_F02=diag(0,tau),
tau=h0*N/[4*A0*(A0*r0^2+h0^2)^2],
D(s)=sI-s^3 T/6+O(s^4).
```

It further claims that weak F02 mixing enters at quadratic order, that the antisymmetric screen
rotation vanishes at this local order, and that F01 integrates conditionally to `D=sI` on a
regular radial null branch. No physical CMB prediction or local signalling claim is made.

## Required review

1. Verify every path and SHA-256 in `REVIEW_MANIFEST.tsv` before using it.
2. Reconstruct the exact F01/F02 metrics and the equatorial tetrad. Check signature,
   orthonormality, `k=u+n` nullity, and the endpoint metric/cross-term conventions.
3. Decide whether the declared query is genuinely identical between the controls and whether it is
   a legitimate metric-derived local observer-sky control. Attack the distinction between a null
   comparison generator and an asserted material signal trajectory.
4. Independently derive the screen tidal matrix under the declared Riemann convention. Check every
   index order and sign. Try to refute the exact F02 `tau` polynomial.
5. Rebuild F01 independently. Decide whether `T_F01=0` for arbitrary regular `A(r)` is correct and
   whether the conditional whole-regular-radial-segment statement `D=sI` follows.
6. Check exact F02-to-F01 reduction, screen symmetry, zero antisymmetric part, the `h0=0` cubic
   degeneracy, the `N=0` nonzero-mixing cancellation, and the positive/negative rational witnesses.
7. Verify the weak-mixing expansion. In particular, determine whether linear and cubic amplitude
   terms vanish and whether the stated quadratic coefficient is exact.
8. Attack the evidence architecture. The production implementation differentiates Christoffel
   symbols; the local independent implementation uses a lowered-Riemann formula but still shares
   SymPy and the declared metric. State precisely what is and is not independent. Treat mutation
   catches as validator sensitivity, not semantic proof.
9. Adversarially review the projection-freedom ruling: does the Jacobi map correctly own remote
   transverse-scale-to-angle conversion, while mode-ladder offset remains boundary/operator phase?
   Decide whether the package overstates what it replaces before a remote endpoint, complete
   profile, source scale, and population are supplied.
10. Check all premise boundaries: F01/F02 remain `CHOSE` controls; P1 remains a low-z pair anchor;
    `c_eff^(pair)` remains inter-observational; `X_max` remains a pair asymptotic guard; no source,
    population, action, bootstrap, local speed, physical screen, or CMB prediction is inferred.

## Required landing

Return exactly one primary verdict:

```text
VERIFIED_WITH_CAVEATS
VERIFIED_AFTER_SPECIFIED_CORRECTIONS
TYPE_ERROR
ALGEBRAIC_ERROR
QUERY_MISMATCH
REFUTED
```

Report exact reproduced formulas/counts, every defect or overstatement, the maximum justified
conclusion, whether the proposed finite-path next gate is justified, and a concise lay explanation.

Do not derive a CMB spectrum, fit data, choose `A` or `h`, select F01/F02, restart FD2, invent a
source/population/polarization rule, derive an action/bootstrap law, or infer local signalling.

