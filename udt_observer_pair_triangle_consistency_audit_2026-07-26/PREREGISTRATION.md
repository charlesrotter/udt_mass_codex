# Observer-pair triangle-consistency audit

Date: 2026-07-26

Mode: `MAP -> OBSERVE -> PONDER -> DERIVE`; CPU-only exact algebra and
source-capability audit

Base: `af8c9939fa7a771d1665daff4e99f93623ab6721`

## Whole question

The covariant lift atlas found a fixed-observer directional family

```text
X_lambda(n) = -P_u + P_n + lambda(P_space-P_n).
```

Determine whether reciprocal comparisons among three observers compose
consistently, and whether that requirement selects the remaining physical
screen-response modulus `lambda` or instead exposes missing frame/connection
data.

A nonidentity loop is not automatically a contradiction: in curved or
frame-transported geometry it can be holonomy. The audit therefore keeps four
questions separate:

1. a strong endpoint-only, path-independent rule in one common observer frame;
2. a properly typed groupoid built from one full coframe at each endpoint;
3. pair-dependent direction frames and their transition mismatch; and
4. comparisons that change the observer time axis, not merely a spatial
   direction for one fixed observer.

## Bounded regime

The exact local algebra is on an oriented, time-oriented real Lorentzian
four-space. Finite reciprocal factors are positive. Generic, collinear,
orthogonal, zero-depth, and exceptional-`lambda` strata are all retained.
The source audit separately records finite-cell descent, cut-locus/path
multiplicity, and holonomy capability.

This is not a complete global solution of a finite cell. It does not choose a
connection, a path family, an endpoint section, a carrier, action, source,
boundary, density, or scale closure.

## Premise ledger

| Input | Stamp | Use |
|---|---|---|
| Founded additive `phi` and reciprocal clock/ruler weights | `pinned-by-THEORY / DERIVED` | Pairwise scalar character |
| Calibrated Lorentzian metric and `c_E` | `WORKING` and `OBSERVED anchor` | Frame type and dimensional calibration |
| Signature `(-,+,+,+)` | `CHOSE convention` | Representatives only |
| Observer `u` | supplied relational datum | Fixed-observer stratum |
| Pair direction `n` | supplied path/separation datum | Direction-indexed lift |
| Screen response `lambda` | `OPEN physical modulus` | Exhaustively classified, not fitted |
| One coframe `F_A` at every endpoint | `CHOSE comparison premise` unless derived | Endpoint-factorized route |
| Pair-dependent coframes `F_(A|B)` | available representation of pair assignment | Mismatch route |
| Flat/path-independent comparison | `CHOSE stronger premise`, not founded | Tested conditionally only |
| Connection/parallel transport | `OPEN`; Levi-Civita is metric-available only after a complete metric is supplied | Holonomy route |
| `G_obs`, provisional `hbar` | scalar anchors only | Cannot supply endpoint frame data |
| Carrier, action, source, bootstrap optimizer | `POSIT` or `OPEN` | Excluded |

Strong local CSN remains inactive and is not used.

## Candidate routes

Every route in `ROUTE_UNIVERSE.tsv` must receive a ruling. In particular, the
audit may not identify a common-frame commutator and silently treat it as the
only possible composition law.

## Exact tests

1. Exponentiate the complete directional generator for arbitrary positive
   finite depth factors.
2. Derive its exact two-direction commutator and classify every zero factor.
3. Test the finite group-commutator loop on generic and exceptional strata.
4. Construct endpoint-factorized maps and verify reversal and triangle laws
   for arbitrary endpoint coframes and every `lambda`.
5. Insert pair-dependent coframes and expose the intermediate transition
   matrix rather than cancelling unlike frames.
6. Test when spatial direction-frame mismatch becomes invisible.
7. Replace the fixed observer by two noncollinear timelike observers and test
   whether any fixed-observer selection survives.
8. Audit the global/holonomy interpretation and finite-cell authority against
   the source set.

## Fail-closed catches

Verification must reject:

- treating every nonidentity loop as inconsistency;
- inferring `lambda=1` without stamping flat endpoint-only path independence;
- claiming a properly typed groupoid selects `lambda` when endpoint
  factorization works for the full family;
- cancelling two distinct pair-dependent frames at the shared observer;
- treating fixed-observer direction independence as changing-observer
  covariance;
- omitting collinear, orthogonal, zero-depth, or generic strata;
- importing a Levi-Civita transport before the complete metric/branch is the
  supplied object under test;
- allowing scalar anchors to manufacture a frame section or connection;
- promoting local algebra to global finite-cell descent; and
- importing an action, carrier, source, or bootstrap equation.

## Maximum conclusion

`BOUNDED_TRIANGLE_CONSISTENCY_CLASSIFICATION_FOR_REGISTERED_ROUTES`.

The audit may conditionally determine `lambda` under an explicitly stronger
composition premise and may identify the smallest missing transport object.
It may not declare a native composition law, global flatness, physical
holonomy, complete metric lift, action, matter source, or bootstrap closure.
