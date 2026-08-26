# G264 preregistration

Date: 2026-08-25
Status: `PREREGISTERED_BEFORE_OUTCOME_ALGEBRA`

## Frozen arena

Use only

\[
f=e^{-2\phi}>0,
\qquad
g=-fc_E^2dt^2+f^{-1}dr^2+r^2d\Omega^2,
\]

with real `phi`. Set `c_E=1` only inside curvature algebra because it is a constant clock/ruler unit
conversion and cancels from the registered scalar invariants.

## Provenance ledger

- primary metric: `DERIVED_CONDITIONAL` bounded arena;
- `phi<0 <=> f>1`: `DERIVED_DEFINITIONAL`;
- arbitrary smooth `f>0`: `FREE_AND_EXPLORED`;
- areal center and asymptotic coordinate: `CHOSE` chart/domain;
- smooth-center, asymptotic-flatness, slice-completeness, and bounded-curvature tests:
  `CONDITIONAL_GEOMETRIC_CLASSIFIERS`;
- physical mass positivity, source equations, Einstein equations, energy conditions, and `X_max`:
  `OMITTED`.

## Candidate outcomes

1. `NEGATIVE_SIGN_SELECTS`: every nontrivial smooth negative-`phi` region fails at least one automatic
   local metric gate.
2. `SIGN_ONLY_NONSELECTION_WITH_GROWTH_THRESHOLDS`: smooth negative regions survive all local gates,
   while particular unbounded negative ends cross exact derivative/growth thresholds.
3. `NO_SIGN_OR_GROWTH_CLASSIFICATION`: even the proposed local and asymptotic classes are not
   invariantly distinguishable with the registered metric quantities.

No outcome is preferred before calculation.

## Registered derivations

1. Derive and independently check the scalar curvature and Kretschmann scalar for arbitrary `f`.
2. Derive the exact smooth-center condition in areal gauge.
3. Test the negative bump family for `f>1`, smooth center, asymptotic flatness, bounded curvature,
   and infinite radial proper length on the static slice.
4. For `f~C r^alpha`, classify:
   - static-slice radial proper length `integral dr/sqrt(f)`;
   - spatial volume `integral r^2 dr/sqrt(f)`;
   - scalar/Kretschmann curvature;
   - lapse-normalized static acceleration `d(sqrt(f))/dr`.
5. Test whether any threshold depends on the sign alone rather than on `f`, `f'`, and `f''`.
6. Provide exact symbolic checks plus an implementation-distinct rational/finite-difference replay.
7. Apply mutation catches for sign-only promotion, mass-positivity import, completeness promotion,
   threshold corruption, and deletion of the smooth negative counterfamily.

## Certification and falsification

The landing fails if a finite negative profile is called singular merely because `phi<0`, a
conditional classifier is promoted to a founding premise, geometric mass aspect is treated as
physical mass, an asymptotic threshold is inferred from sign without its jet assumptions, or the
counterfamily is filtered out for not resembling the desired universe.

## Maximum conclusion

An exact bounded classification of what the primary metric itself does and does not restrict in
negative-`phi` regions. No unique profile, physical history, source, mass law, dynamics, or `X_max`
is derivable here.
