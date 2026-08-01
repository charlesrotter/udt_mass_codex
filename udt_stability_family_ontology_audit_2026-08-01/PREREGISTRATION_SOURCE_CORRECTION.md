# Preregistered Source-Correction Layer

Date: 2026-08-01

Parent preregistration commit: `c21d512`

## Trigger

The mandatory cold reviewer reproduced the original 1,605-path freeze exactly but identified three
tracked, potentially decisive sources omitted by the inherited-freeze rule. The first audit outputs
remain provisional and uncommitted. This correction is registered before the primary agent inspects
or uses the omitted source contents.

The original `SOURCE_INVENTORY.tsv`, `SOURCE_PATHS.txt`, `SOURCE_MANIFEST.sha256`, and
`SOURCE_SCOPE.tsv` remain immutable historical preregistration evidence.

## Additions-only correction

Add exactly:

1. `udt_p4_bookkeeping_forcing_2026-07-29/EXACT_DERIVATION.md`
2. `udt_p4_routeD_field_registration_2026-07-29/AUDIT_REPORT.md`
3. `NEGATIVES_REGISTRY.md`

`SOURCE_ADDENDUM.tsv` records their base blobs, bytes, and hashes.
`EFFECTIVE_SOURCE_INVENTORY.tsv` is the sorted unique union of the original 1,605 rows and these
three rows. Expected effective count: 1,608.

No other source may become load-bearing. Finding a further decisive omission requires either an
explicitly scoped limitation or another preregistered correction before its content is used.

## Required re-audit

The corrected audit must:

- determine whether the constants-census and fields-census branches have an exact common parent
  solution set, are separately conditional realized families, or remain open;
- distinguish shared source/program lineage from identity, containment, or overlap of solution sets;
- re-grade every inherited negative against `NEGATIVES_REGISTRY.md` without rewriting it;
- preserve union-valued F03/F06 labels and avoid whole-label containment from component relations;
- rerun the family, 70-axis, 28-pair, 210 pair-axis, premise, and readiness adjudications;
- replace assertion-based output checking with an independent classification derived from raw source
  fields and source anchors; and
- retain the original maximum conclusion ceiling.

No solve, GPU process, readiness promotion, carrier/action/boundary/time selection, or physics
adoption is authorized.
