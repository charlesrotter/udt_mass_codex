# Audit report — stationary R17 local one-form selection

Date: 2026-08-10

## Result

The complete stationary R17 metric owns several canonical local one-forms beyond `dphi`, but its
local finite-jet algebra does not select any one of them as the additional physical reciprocal
transgression.

At order zero, residual screen `SO(2)` invariance leaves exactly the unit clock and twist-ruler
coforms. At a generic first jet, those two forms together with the screen projection of `dphi` and
its angular quarter-turn span the full cotangent space. Metric naturality therefore becomes less
selective—not more selective—once the complete orchestra is retained.

Two constructive obstruction families make the nonselection sharp:

```text
alpha_c=dphi+c H*dphi
```

preserves the founded depth on every intrinsic pair leaf but is generically path-dependent, while

```text
beta_c=dphi+c dJ,
J=|H*dphi|^2/(|H*dphi|^2+|omega_K|^2)
```

is exact, dimensionless, and preserves the pair-pure reduction. Every real `c` survives the
current local gates.

An actual smooth global `S3` R17 witness with `phi=w`, `lambda=0`, and `a=1/64` gives both
`d(H*dphi)(Z,Y)=1/2` and `d|H*dphi|^2 wedge dphi(Z,Y)=1/2`. This closes the previous result's caveat
that stationary R17 nonexactness had not yet been exhibited.

## Type ruling

- `dphi` remains selected for the already-owned endpoint depth `delta_K=phi(q)-phi(p)`.
- The unit clock and twist-ruler forms are metric-owned geometric forms, not selected reciprocal
  path laws.
- The normal connection is globally owned, but a local potential `A` is screen-gauge dependent.
- Line-integral composition is automatic for every one-form and cannot select an integrand.
- Path independence still leaves inequivalent exact endpoint potentials.
- No manifest-backed R17 equation selects a coefficient, profile, `lambda`, path, or global period.

## Evidence gates

1. **Preregistered:** yes, commit `1caa97f9` before outcome inspection.
2. **Full or bounded:** complete census of the 16 frozen structural candidate families and a
   constructive nonuniqueness result in the regular stationary local finite-jet arena; not an
   exhaustive classification of every finite-jet natural operator. Time-live/null/other branches
   are excluded.
3. **Independently verified:** exact SymPy controller 17/17; independent standard-library/Fraction
   reconstruction 17/17; 20/20 exercised mutations rejected; fresh external review returned
   `CONSTRUCTIVE_NONUNIQUENESS_ONLY` and accepted all load-bearing algebra.
4. **Premises audited:** yes. No action, source, bootstrap, physical path, universal `c_eff`, or
   downstream physics was imported.

## Maximum conclusion

```text
CANONICAL_STATIONARY_R17_GEOMETRIC_ONE_FORMS_BEYOND_dphi_DERIVED__
GENERIC_FIRST_JET_SPANS_FULL_COTANGENT__
ACTUAL_GLOBAL_R17_NONEXACT_TRANSGRESSION_WITNESS_DERIVED__
EXACT_PAIR_PURE_PRESERVING_ENDPOINT_FAMILY_SURVIVES__
NO_DISTINGUISHED_RECIPROCAL_TRANSGRESSION_SELECTED_BY_LOCAL_METRIC_ALGEBRA__
ADDITIONAL_QUERY_ON_SHELL_OR_GLOBAL_OWNER_REQUIRED
```

The smallest possible owner type is an explicit physical query/measurement premise. An on-shell
equation or global-completion rule remains a larger possible owner. This is not canon and does not
select which missing owner supplies the eventual physical law.
