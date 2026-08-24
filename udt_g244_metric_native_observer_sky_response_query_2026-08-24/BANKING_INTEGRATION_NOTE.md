# G244 append-only banking integration

Date: 2026-08-24

The externally accepted G244 result was produced against the exact 226-row premise registry frozen
in `SOURCE_MANIFEST.tsv`. Its accepted row is now present exactly once in the 227-row live registry.

The preregistered lineage helper removes only that one `G244` row in memory. It reconstructs the
frozen source digest exactly:

```text
1cad6bf0a437157a87013f0ac718a6e54213f093a6088670ed5ad7e233668126
```

The current 227-row registry digest is:

```text
bb2bbc2c3574dc0c10845c4472d00b10f64459bddc990859b8b830857c92deb1
```

No earlier registry row, source manifest, scientific output, classification, tolerance, or
observational boundary changed.
