# Preregistration Correction — Source Manifest Transcription

Date: 2026-07-21

Status: preregistered before any atlas outcome was computed or inspected.

The source-manifest table in `PREREGISTRATION.md` contains two transcription errors. The immutable
files on the parent commit independently hash as follows:

| source | erroneous transcription | controlling required SHA-256 |
|---|---|---|
| `udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt` | `b7d61760e3ac3dc9dc2a51a7a505f02dad964fe8d7dfc1f1ed8df3cc3eb1b543` | `b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad` |
| `udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt` | `17780f41355121df4ecf86bd81606ef597cc6f5f26d90c0e443a5d2eac24d13a` | `1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38` |

The ensemble-atlas requirement remains unchanged:
`3d569ed31506f5f7ce44beac30e8419571f734b3973dcc34d6c474bf78636757`.

This correction changes no question, transformation, tolerance, count, payload, classification,
falsification gate, or maximum conclusion. The original preregistration is preserved as historical
evidence; this file controls only the two corrected source-manifest values.
