# G74 external-review correction layer — preregistration

Date: 2026-08-11

The fresh sealed gpt-5.4 review reached the science after verifying all `34/34` payload hashes and
returned `VERIFIED_WITH_CAVEATS`. Before changing any status or navigation text, this file freezes
the exact additions-only correction layer.

## Frozen reviewer return

```text
raw         ab76e853842442289ea0296866687c9be00bb6522f0754cc645f46ce6f89a9dd
transcript  c00b1ebd1496e25b277d7c5cf2bcea4acf8ea2fc577d43f74618cb83909620a8
verdict     VERIFIED_WITH_CAVEATS
landing     MIXED_GLOBAL_COMPLETION_CLASSES
```

## Exact corrections

1. Preserve `PREREGISTRATION.md` as historical evidence. Its line describing the independent route
   as using “Cartesian Hamiltonian variables” is superseded for method description only: the
   implemented replay uses the direct Cartesian metric, independently constructs the
   Levi-Civita/Christoffel connection, and integrates position/velocity geodesics with `DOP853`.
2. Grade that replay as a `SEPARATE_EQUATION_CROSS_CHECK_WITH_SHARED_PROFILE_AND_MESH_HELPERS`, not
   a clean-room independent implementation. It does not reuse the production Hamilton equations,
   but imports the production profile loader and icosphere helper and compares against saved
   production endpoints.
3. Treat `derive_topology_atlas.py::exact_checks` as executable mnemonic/sanity checks. The proof
   ownership remains the written derivation, standard topology/geometry arguments, and the fresh
   external rederivation—not the boolean code checks alone.

No profile classification, threshold, trajectory, endpoint, degree, center gate, exact theorem,
premise status, source status, physical owner, or maximum conclusion may change under this layer.

## Required verification

- reproduce both external-review hashes;
- find the exact `34/34`, verdict, landing, `3/6/12`, and caveat statements in the raw return;
- replay the existing package, semantic-catch, repository, manifest, link, frontier, and test gates;
- preserve the seven protected stopped-draft paths by metadata only.

