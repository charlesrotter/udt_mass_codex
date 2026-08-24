# G245 append-only banking integration

Date: 2026-08-24

The externally accepted G245 result was produced against the exact 227-row premise registry frozen
in `SOURCE_MANIFEST.tsv`. Its accepted row is now present exactly once at the head of the 228-row
live registry.

The preregistered suffix-lineage helper reconstructs the frozen pre-G245 registry digest exactly:

```text
bb2bbc2c3574dc0c10845c4472d00b10f64459bddc990859b8b830857c92deb1
```

The current 228-row registry digest is:

```text
e731b06847688c0466799d82c1ffbd3333250596e29bbadd21cb9e375c1142b5
```

The same suffix rule lets G244 continue reconstructing its exact pre-G244 authority beneath the
later G245 row. Both G244 and G245 live no-write package replays pass. No saved scientific output,
classification, tolerance, historical source manifest, or observational boundary changed.
