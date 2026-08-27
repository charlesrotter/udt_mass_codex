# G281 preregistration execution note

The original committed `SOURCE_SCOPE.tsv` included two live startup authorities,
`CURRENT_SCIENTIFIC_PREMISES.tsv` and `CURRENT_RESEARCH_PROGRAM.md`, while intentionally omitting
them from the immutable source manifest. Fresh external review correctly found that this made the
claimed 34-source sealed scope impossible to audit and allowed the primary verifier to pass while
two nominally scoped files were absent.

Repair R1 removes those mutable files from the scientific source scope. G281 therefore covers
exactly the 32 immutable historical/evidentiary sources present in `SOURCE_MANIFEST.tsv`. Startup
alignment remains a separate repository closure check and is not evidence for the scientific
landing. This repair changes neither the six prediction gates nor the landing.
