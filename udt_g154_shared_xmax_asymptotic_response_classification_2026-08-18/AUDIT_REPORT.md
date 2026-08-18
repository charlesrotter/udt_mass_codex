# G154 shared-Xmax asymptotic response classification

Date: 2026-08-18
Status: `VERIFIED_WITH_CAVEATS__COLD_EXTERNAL_REVIEW__INDEPENDENT_LOCAL_REPLAY_PASS`

## Result first

The cold external review strengthens the primary landing to:

```text
CONFORMAL_NETWORK_NONSELECTION__CURRENT_IDENTITIES_ONLY_EVALUATE_SUPPLIED_HISTORY
```

The exact distinction is between the supplied position-group scale `X_star` and the pair metric's
common clock/ruler scale `exp(kappa)`. The reciprocal-position law contains the former and
`phi_pair`; the normalized metric-frame response also contains `kappa`. Current network, causal,
metric, Cartan, Bianchi, transport, rank, and overlap identities do not relate the two.

The adopted **normalized** Mobius law does not derive a fixed dimensionful `X_max`. A fresh
adversarial review caught the circular step: the first derivation inserted one fixed \(X_*\) into
the dimensionful Mobius law before proving it. The strongest valid limited theorem is only this:
if a leaf is additionally supplied with that one-scale law, consistency forces
\(x=X_*\tanh\phi\) and hence \(X=X_*\) inside that leaf.

More importantly, even a conditionally supplied fixed leaf scale does not select the asymptotic
metric-frame response. With

\[
\rho=X_*\tanh\phi,
\qquad
V(\rho)=X_*\operatorname{sech}^2\phi\,V(\phi),
\]

the full product may tend to zero, a finite nonzero limit, infinity, or no limit. Exact regular
interior pair metrics realize all four classes with the same `phi(q)`, the same `rho(q)`, and the
same `X_*`; only the retained metric common scale changes.

The live-`dX` term therefore remains generally intrinsic. It is excluded only after a fixed-scale
leaf premise is independently supplied or derived. A finite common endpoint for `X` still does not
control `dX`.

Positive common rescaling provides the decisive complete-network counterfamily. It preserves
`phi_pair`, `beta`, `rho`, causal cones, and the reciprocal-position subnetwork while shifting
`kappa` and rescaling every normalized response. Each twin is a different complete metric/network,
not a gauge copy, but every twin remains globally pullback- and overlap-consistent. The complete
network may reconstruct its supplied metric; coherence does not select which metric is physical.

## Strongest implication

The persistent gap is now exactly typed. The endpoint asymptote is a working relational frame, but
neither its fixed scale realization nor the relation between additive depth and normalized metric
clock/ruler rate is selected. The missing object is the common-scale/history law that would own
both the scale carry and the manner of approach.

## Evidence

- preregistration committed at `f5946fa0` before execution;
- production SymPy derivation: all registered checks pass;
- independent stdlib numerical/source-hash replay: all registered checks pass;
- both asymptotic orientations and temporal/spatial duals checked;
- same-profile common-scale witnesses separate all four response classes;
- live-scale endpoint, oscillation, and exact-cancellation witnesses checked;
- fresh adversarial review required repairs; its four-class replay passed, the registered type
  correction plus stronger independent checks were applied, and repair-only follow-up passed.
- cold external SymPy check replay: byte-identical stdout and all checks pass;
- independent stdlib conformal/network replay: first insufficient-tail failure preserved, then
  `12/12 PASS` after extending the unchanged grid through `q=1e-60`.

## Bounded landing

```text
CONFORMAL_NETWORK_NONSELECTION__CURRENT_IDENTITIES_ONLY_EVALUATE_SUPPLIED_HISTORY__
EVEN_FIXED_LEAF_SCALE_NOT_DERIVED__RESPONSE_CLASS_NOT_SELECTED__
COMMON_SCALE_CONTROLS_NORMALIZED_APPROACH_RATE_WITHOUT_CHANGING_TERMINAL_RECIPROCAL_POSITION__
LIVE_DXMAX_REMAINS_INTRINSIC_UNTIL_FIXED_SCALE_DESCENT_IS_INDEPENDENTLY_SUPPLIED_OR_DERIVED__
DIFFEOMORPHISM_NATURAL_NONIDENTITY_COMMON_SCALE_HISTORY_ADMISSIBILITY_LAW_MISSING_TYPE__
GLOBAL_SHARED_XMAX_PHYSICAL_HISTORY_PROPER_LENGTH_VALUE_DYNAMICS_AND_COMPLETION_OPEN
```
