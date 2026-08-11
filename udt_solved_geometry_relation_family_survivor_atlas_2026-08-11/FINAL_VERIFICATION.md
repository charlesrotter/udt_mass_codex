# Final verification

Date: 2026-08-11  
Status: **PASS**  
Package grade: **`VERIFIED_WITH_CORRECTIONS`**  
Scientific landing: **`MULTIPLE_GEOMETRIC_SURVIVOR_FAMILIES`**

## Scientific evidence

- bounded sample universe: `14` exact preregistered witnesses;
- endpoint constructions: `14/14 REGULAR`;
- timelike/spacelike propagators: `28/28 REGULAR_PROPAGATOR`;
- declared Levi-Civita loops: `28/28 NONIDENTITY`;
- R17 normal-holonomy evaluations: `18/18 NONZERO`;
- independent finite-difference/RK4 comparisons: `56/56 PASS`;
- read-only catch predicates: `23/23 PASS`.

Independent maximum discrepancies/defects:

| quantity | maximum |
|---|---:|
| atlas defect | `6.718286562879488e-16` |
| R17 `phi_pair=phi` defect | `1.6653345369377348e-16` |
| geodesic endpoint difference | `1.0777702837323036e-11` |
| geodesic norm drift | `3.5177416535248085e-12` |
| holonomy matrix difference | `6.632855803971152e-10` |
| R17 normal-angle difference | `2.1001256289565617e-13` |
| transport metric defect | `8.186194983820604e-12` |

## Load-bearing hashes

| artifact | SHA-256 |
|---|---|
| `SOLVED_GEOMETRY_ATLAS.tsv` | `65d28f50109fbcdb056eeb365a9b51d8bc4806dce0cc2f4e730d5d4f17c13b7b` |
| `GEODESIC_DIAGNOSTICS.tsv` | `9f245659ce01e7de0a5bd3dedef2baf68f40dbb3dc731117500f80d247b24e44` |
| `PATH_DIAGNOSTICS.tsv` | `ea0a7214e3f5a63dfd6440f7cc9ebea53c0ee1ef5c3ee87d88df0cc36c4c4eb2` |
| `DERIVATION_RESULT.json` | `7106ebb1857a74d7d02becf29e33856473b50a8dbfde4899658bc8fad949efd8` |
| `INDEPENDENT_VERIFICATION.json` | `a5e6d6c2951b5760ee4a8a63c9444855ed122507fdcfa5d05277eead1ae7e9a5` |
| `REVIEWED_INTAKE_SHA256SUMS.tsv` | `d009a7720d7ec72aea71efdd244918948e902837a40cd8ff005a5afee6ffecda` |
| `EXTERNAL_REVIEW_RAW.md` | `4725d389bbdfc37843ddbf048d555df8121f687d56863a4d22a308ef647fc019` |

## Provenance replay

- original cold-review intake: exactly `50` files = `28` original package files + `22` sources;
- exact frozen source commit: `4046b46279e87121e1c84373cafa3068d5b50354`;
- repository Git-snapshot source replay: `22/22 PASS`;
- fresh sealed read-only `sources/` replay: `22/22 PASS`;
- protected curvature-atlas paths in reviewed intake: zero;
- stopped native-on-shell draft paths in reviewed intake: zero;
- original manifest and reviewed-intake hash table: unchanged.

The original `verify_preregistration.py` remains historical pre-result evidence and intentionally
reads the then-current working-tree registry. After the current G63 navigation row was added, the
authoritative final replay became `verify_package_postreview.py` plus
`verify_source_layout_readonly.py`, using the frozen Git snapshot or sealed sources. This avoids
rewriting provenance to follow a mutable live registry.

## Repository gates

- current scientific premise verifier: `PASS`, exactly `63` guarded rows;
- full test baseline: `98 passed, 1 xfailed`;
- the xfail remains the documented known HABIT-pin gate;
- protected curvature-atlas contents: unread and unmodified;
- stopped native-on-shell draft: seven untracked paths preserved, unread and unmodified;
- `CANON.md`: unchanged.

## Maximum conclusion

The package independently verifies bounded geometric coexistence of endpoint and path-labelled
relation channels. It does not derive the physical channel combination, a native on-shell law,
global time-live completion, dynamical stability, action, source, carrier, matter, mass, bootstrap
selection, `X_max`, CMB physics, or signalling.

