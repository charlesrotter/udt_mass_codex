# Fresh read-only adversarial review

Date: 2026-08-04

Reviewer: fresh ephemeral external Codex `gpt-5.4`, read-only repository sandbox

Verdict: `PASS_WITH_CAVEATS`

## Blocking errors

None. The reviewer independently ran the primary derivation, standard-library rational
reconstruction, and fail-closed verifier. It reproduced `13/13` checks and `26/26` original mutation
catches.

## Reproduced load-bearing results

- map ranks/nullities: `160 -> 100` rank `100` nullity `60`; `100 -> 20` rank `20` nullity `80`;
  `160 -> 20` rank `20` nullity `140`;
- no curvature sign/index drift relative to P02/P01 convention;
- exactly one Bianchi relation with block ranks `1,10,1,4,4,1`;
- source-category ranks `8,11,14,18`, all registered union/intersection ranks, and exactly the two
  reported minimal full triples;
- `N^2=sN`, ranks `3,3,1,0`, nonzero-null rank-one nilpotence, and tidal image ranks `6,6,3,0`;
- correct P02 provenance and no promotion into physical evolution, selection, action, source,
  bootstrap, or mass.

## Caveats

1. The independent replay originally confirmed the null quotient on one basis but did not separately
   re-prove representative-independence.
2. “Mixing is a bridge” is supported only locally, relative to the supplied `2+2` split and registered
   tangent basis; it is not split-independent or physical.

## Reviewer maximum conclusion

The bounded point-local coframe second jet reaches the full algebraic curvature module; the supplied
`2+2` display has one Bianchi relation among 21 displayed entries; and the supplied depth/tidal
objects have the reported stratified behavior. No unique solder, selected split, evolution law,
global branch, action, source, bootstrap, or mass claim follows.

The exact external execution completed successfully with no repository writes.
