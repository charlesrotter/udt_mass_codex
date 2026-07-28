# Append-only P03 source-scope correction

This file corrects the interpretation of
`udt_global_coframe_compatibility_p03_2026-07-27/` without modifying that frozen package.

P03 froze 57 sources and correctly reported its own 57-source and 713-row census. However, the
repository already contained
`udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/AUDIT_REPORT.md`.
Git records its introducing commit as
`cacfaa178d2199ecb13d5196545ff36797c82177`, and that commit is an ancestor of P03 base
`6727b74878103a91eac855bad91a97b0a5c2e167`. The file is absent from P03's manifest.

That source derives an explicit complete global `R x S3` non-ultrastatic reciprocal configuration
family. Consequently, P03's claim that the strongest registered complete controls were only two
ultrastatic `S3` metrics is valid only inside its incomplete frozen source universe and is
superseded as a repository-wide statement.

The correction does **not** authorize P03-B. The recovered family is off shell, carries arbitrary
smooth `phi` and real `lambda`, and does not select the physical observer semantics, global
completion class, native equations, or scale. P03's procedural block on a lossy P02 projection also
remains valid; this audit froze both omitted detailed P02 ledgers but did not activate them.

Machine-readable rulings are in `P03_SCOPE_CORRECTION.tsv`.
