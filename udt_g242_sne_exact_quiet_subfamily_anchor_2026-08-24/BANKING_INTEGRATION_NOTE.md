# G242 append-only banking integration

Date: 2026-08-24

G242 was preregistered against the exact 224-row premise registry in `SOURCE_MANIFEST.tsv` and was
externally accepted after the later G243 row had been banked. Banking G242 now appends its own row;
neither later row may rewrite the historical source manifest.

After banking, the production replay and sealed-intake builder may remove at most one live `G242`
row and at most one live `G243` row in memory. The reconstructed bytes must equal the exact
preregistration digest. Any other registry mutation still fails closed.

This self-lineage integration changes no model, source data, covariance, statistic, threshold,
classification, or scientific conclusion. The earlier packaging-repair prohibition on removing
anything except G243 governed the pre-bank review repair; this note separately governs the
inevitable append-only G242 self row after external acceptance.
