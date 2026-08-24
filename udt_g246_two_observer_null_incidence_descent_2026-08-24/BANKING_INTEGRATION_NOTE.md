# G246 append-only banking integration

Date: 2026-08-24

The externally accepted G246 result was produced against the exact 228-row premise registry frozen
in `SOURCE_MANIFEST.tsv`. Its accepted row is now present exactly once at the head of the 229-row
live registry.

The preregistered suffix-lineage helper reconstructs the frozen pre-G246 registry digest exactly:

```text
e731b06847688c0466799d82c1ffbd3333250596e29bbadd21cb9e375c1142b5
```

The current 229-row registry digest is:

```text
66e38c8b530946402d04b05bf7573fc473c28a0aec81b201c3aeb189dd23d3e5
```

G244, G245, and G246 live no-write package replays all pass. No saved scientific output,
classification, tolerance, frozen source manifest, prior registry row, or observational boundary
changed.
