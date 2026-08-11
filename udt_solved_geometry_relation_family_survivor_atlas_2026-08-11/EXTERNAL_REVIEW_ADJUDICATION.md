# External-review adjudication

Date: 2026-08-11  
Scientific landing: **`MULTIPLE_GEOMETRIC_SURVIVOR_FAMILIES`**  
Package grade after review: **`VERIFIED_WITH_CORRECTIONS`**

## Adjudication

The external reviewer accepted the bounded scientific landing and independently reconstructed one
R17 witness and one complete time-live witness without importing the production solver. The
recomputed endpoint maps, geodesic-deviation regularity, Levi-Civita holonomy, and R17 normal angle
agree with the frozen rows at approximately `1e-12` scale. The reviewer also confirmed that no
action, source, matter model, bootstrap tuning, `c_E`, or `X_max` enters the solver.

The review found two real procedural defects in the original sealed-review package:

1. the source-verification scripts understood repository-root paths but not the sealed intake's
   `sources/` relocation;
2. the original catch-proof runner regenerated output files and therefore could not run on a
   read-only intake.

These are accepted. They do not change a metric, witness, equation, threshold, output row,
classification, or scientific conclusion.

## Additions-only repair

The preregistered repair adds:

- `REVIEWED_INTAKE_SHA256SUMS.tsv`, freezing the exact original `50`-file review intake;
- `verify_reviewed_intake.py`, which rejects missing, extra, duplicated, hash-mismatched, protected,
  or stopped-draft paths;
- `verify_source_layout_readonly.py`, which accepts exactly one complete layout—repository root or
  sealed `sources/`—and rejects partial or mixed layouts;
- `verify_catch_proofs_readonly.py`, which re-evaluates all `23` registered predicates in memory,
  compares them to the frozen result rows and summary, and writes nothing;
- `verify_package_postreview.py`, the authoritative post-review package verifier.

The original preregistrations, solvers, outputs, classifications, dispatch, review return, and
pre-review verifiers remain preserved as historical evidence.

## Corrected replay result

The original reviewed intake replays as exactly:

- `50` total files;
- `28` original package files;
- `22` exact manifest sources;
- zero protected-atlas paths;
- zero stopped native-on-shell draft paths.

In a fresh read-only sealed layout, the correction layer reports:

- source layout: `SEALED_SOURCES`, `22/22` exact;
- catch proofs: `23/23 PASS` with no writes;
- package landing and all registered counters: `PASS`.

The same source-layout and catch-proof verifiers pass from the repository's exact frozen Git source
snapshot. The later G63 navigation row is intentionally absent from that historical source
snapshot and present in the current live registry; `POSTBANK_MUTABLE_SOURCE_PREREGISTRATION.md`
records this separation.

## Scientific conclusion retained

Within the `14` preregistered solved witnesses and declared paths at affine endpoint `s=0.4`:

- `14/14` endpoint pair constructions remain regular;
- `28/28` causal geodesic-deviation propagators remain regular;
- `28/28` declared loops carry nonidentity Levi-Civita holonomy;
- `18/18` R17 loop evaluations carry nonzero normal-connection angle;
- `56/56` independent numerical comparisons reproduce their registered classes.

The coexistence is typed, not contradictory: endpoint reciprocal depth is an endpoint channel;
full-coframe and normal holonomy are path-labelled channels. This is bounded geometric persistence,
not a physical relation selector, native evolution equation, dynamical stability result, or global
completion theorem.

## Four gates after adjudication

1. **Preregistered:** yes, including the post-review correction before mutation.
2. **Full space or bounded scope:** bounded, exact `14`-witness universe; not exhaustive.
3. **Independent verification:** yes for the load-bearing numerical classifications and two cold
   representative reconstructions; source ownership remains premise-audited rather than independently
   rederived from first principles.
4. **Premises audited:** yes within the declared package; physical observer-query selection, native
   on-shell dynamics, time-live global completion, singular strata, and physical boundary remain
   `OPEN`.

Maximum justified conclusion: **`VERIFIED_WITH_CORRECTIONS` bounded geometric coexistence**.
