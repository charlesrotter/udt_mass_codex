# Displaced startup surface before the Universal Reciprocity clarification

This directory records the exact startup-surface state displaced by the
2026-08-31 G310 refresh. It is a documentary recovery pointer, not current
scientific authority and not a copy of the full files.

The displaced state is commit `dd4f294b`. Recover any exact file with:

```bash
git show dd4f294b:<path>
```

| Path | SHA-256 at `dd4f294b` | Lines |
| --- | --- | ---: |
| `AGENTS.md` | `ffd8348cf6304c0ed5a70ccb13b324096cbad0f002d154b187834e7b715815be` | 217 |
| `LIVE.md` | `ec5efb237d75551e46299f58fd9cd4d3c31e335fe36fb5011a0082b55d44d383` | 133 |
| `HANDOFF.md` | `81f2c35958b5abb319441af9dbc9366b03cda5cb37e49833ac6af41074672069` | 92 |
| `CURRENT_RESEARCH_PROGRAM.md` | `9618c45d865d47efa5a82bc1f9de3f57c1139da7b881891392e0a1ce935a1945` | 131 |
| `CURRENT_SCIENTIFIC_PREMISES.md` | `011fe57767806952c0a2d791c3038529761ceca31f0a568d0eb9f6b604f28843` | 125 |
| `CURRENT_SCIENTIFIC_PREMISES.tsv` | `10c7b53fc2820a63c7fee40d1a9d06325c7a3cb8c17d58329646eaf191de5ba8` | 290 |
| `INDEX.md` | `88cf548baa19509c5d11e7a38b1d891e6aafe874464c2574988fa335807725f3` | 119 |
| `MEMORY.md` | `9bb01c938fdf53869fbb4bd2495ee95f238e9797e0403d086c15e33c775c842a` | 52 |
| `verify_current_scientific_premises.py` | `03d7e95cac5108cdb42263a373e424115f35d4da13e2bff740ceb2aef602b2bc` | 14826 |
| `tests/test_startup_surface.py` | `6117e191a7dc17d8f295f75c09b959e2137c1e4ac1fe8dccd3f00b350e207fad` | 597 |

Why this state became stale:

- the exact registry contained 289 rows and ended at G306;
- G307--G310 were present only in their evidence packages and prose pointers;
- the startup language did not yet distinguish Charles's proposed Universal
  Reciprocity framing from G310's new, unadopted differential curvature
  formalization; and
- it did not explicitly keep the loud--quiet--loud regime behavior with the
  angular-sector cancellation rather than DDR.

The replacement startup surface uses the exact 293-row registry through G310.

No scientific evidence was moved, deleted, or regraded by this archive record.
`LIVE.md` and the current exact registry remain authoritative.
