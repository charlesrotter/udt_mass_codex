# Audit report — null-carrier measure ownership from the complete query

Date: 2026-08-15

## Result

On one supplied regular null observer-query tube, every fixed source label measure has a unique
closed pushforward three-form. This is valid query-label bookkeeping, not a new metric-owned carrier
law. The complete metric/coframe supplies its invariant volume, density, focusing, and Jacobi
representation. In adapted labels,

```text
R^*(vol_g)=J dlambda wedge ds wedge dy1 wedge dy2,
j_C=(C/J)K,
N_C=i_(j_C)vol_g,
dN_C=0                 when partial_lambda C=0.
```

The same result appears in the screen Jacobi map:

```text
theta=tr(D'D^-1)=d log(det D)/dlambda,
n=C/det D,
n'+theta n=0,
n det D=C.
```

Thus the full orchestra changes the detailed beam shape and density while the query's source labels
remain labels by construction. The bookkeeping label-survival factor is exactly one.

This does **not** set G94's physical `eta=1`. The metric/query has not identified radiative cargo
with the label measure. It supplies a transport operator, not the physical statement that emitted
amount follows that operator without absorption, scattering, branch exchange, creation, or loss.

## Landing

```text
EXTERNALLY_REVIEWED_WITH_CAVEATS
__LABEL_CURRENT_VALID_BUT_TAUTOLOGICAL
__NO_NEW_OWNERSHIP_BEYOND_QUERY_TYPING
__METRIC_DENSITY_AND_JACOBI_REPRESENTATION_EXACT
__PHYSICAL_CARRIER_IDENTIFICATION_POPULATION_ZERO_SIDE_FLUX_AND_ETA_OPEN
```

## What this improves

G95 described a closed physical carrier measure as missing. This audit cleanly separates:

1. a closed **geometric label measure**, valid as the tautological pushforward of supplied query
   labels, with its density/focusing readout supplied by the metric; and
2. the **physical carrier identification**, still open.

This supplies no new physical ownership beyond G94/G95. A full Maxwell derivation is not required
merely to relabel a regular query tube, but physical survival still requires identification of the
G94 radiative amount with the transported measure plus physical zero side flux. G95's separate
covector-energy identification would then give `epsilon=1/Z`. Neither premise is adopted.

## Candidate-space result

All thirteen preregistered classes remain in `CANDIDATE_MEASURE_ATLAS.tsv`. Exact catches show:

- the four-volume is closed but is not a three-current;
- raw coframe triples, `*K_flat`, `*dphi`, and Abelian Chern–Simons forms are not generally closed;
- the Jacobi/van-Vleck class supplies the exact query-label current;
- the future-null shell has canonical preserved measure but no selected population;
- projectivization leaves a scale/normalization gap;
- screen response and special curvature currents are not the general null-query cargo.

No candidate was filtered for physical merit.

## Exact evidence

- primary SymPy determinant, transport, relabelling, null-current, coframe, reciprocal-gradient,
  Chern–Simons, null-shell scaling, and Hamiltonian checks;
- implementation-distinct standard-library exact-Fraction replay with no SymPy or primary import;
- explicit nonclosure and nontransport catches;
- source census, premise ledger, and thirteen-class ownership atlas.

## Scope

One local regular orientation-preserving query tube only. Physical history/query selection,
caustics, branch changes, multiple images, absorption/scattering, physical population, source and
detector law, action, matter, global completion, SNe, `X_max`, BAO/CMB, bootstrap, mass, and
signalling remain open.

## Four gates before fresh review

1. Preregistered: **PASS**.
2. Full or bounded: **PASS for the declared thirteen-class local regular-query ownership census**.
3. Independently verified: **PASS WITH CAVEAT**. The implementation-distinct exact-Fraction replay
   and fresh sealed adversary reproduce the load-bearing algebra; the package verifier is only a
   saved-record consistency gate.
4. Premises audited: **PASS AFTER EXTERNAL DOWNGRADE** for metric, coframe, query labels, physical
   carrier, population, physical zero side flux, and excluded global/singular scopes.
