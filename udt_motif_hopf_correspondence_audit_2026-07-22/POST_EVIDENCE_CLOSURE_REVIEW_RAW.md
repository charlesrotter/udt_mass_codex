## Verdict: PASS-WITH-CAVEATS

No blocking closure defect was found in archived commit `f1111f10f1b55e35fcc69e47662efb8fcdefd879`.

- All 71 package files other than the self-excluding manifest are present and covered exactly once by `SHA256SUMS.txt`.
- SHA-256 replay passed before and after verification. All ten lineage hashes also passed, including 278 nested-manifest entries and two direct files.
- Unchanged `verify_package.py` passed with `PASS_WITH_REGISTERED_SCOPE`.
- `source_lineage_rows()` is exactly identical to committed `SOURCE_LINEAGE.tsv`: ten ordered rows, two `DIRECT_PRODUCTION_SOURCE_MANIFEST`, eight `FROZEN_SOURCE`.
- The coordinated point/edge attack failed immediately in the corrected validator with `exact point status census`, before raw-ledger or other evidence evaluation.
- Negative, NaN, and infinite residuals; a fabricated seed path; a negative point count; and a non-finite determinant were rejected.
- The mutation harness reproduced 29 unique catches, byte-identical to the committed catch ledger.
- Pre-correction frozen hashes for the correction result and 29-catch ledger equal the current hashes. Raw counts and scientific statuses remain unchanged; the evidenced fourth correction is limited to banking artifacts and lineage-generation/verification metadata.
- Independent ledger replay reproduced:
  - 3,072 identities;
  - 1,618,944 path rows;
  - 95,232 paths, including 93,920 stable at all 17 sampled nodes;
  - 143,487 unique distribution rows;
  - 6,669/1,536 nonintegrable/integrable primitive `1+1+2` planes;
  - 8,370 nonintegrable four-line split sides;
  - 13 explicitly retained unresolved stencils.
- Independent metric algebra reproduced the mixed Hessian, angular gap `2/A²`, supplied-action connection, unit quotient norm, and conditional endpoint limit. A fresh 2,048-point CPU execution of frozen `hopf_seed` agreed with the independently reconstructed quotient to `8.23×10⁻16`.

Caveats are correctly disclosed: the nonlinear-map evidence is confirmatory; Frobenius certification is registered-chart only; continuation is sampled at 17 nodes; the circle action is supplied; no `S2` carrier or `L2+L4` action is derived; global completion, dynamics, stability, source, and mass remain open.

Four gates: preregistered—yes, confirmatory caveat disclosed; bounded scope—yes; independently verified—yes at that scope; premises audited—yes.

Strongest honest maximum:

`OBSERVED_BOUNDED_REGISTERED-CHART_SAMPLED_MOTIF_AND_FROBENIUS_CENSUS`

plus

`EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS`.

The overall correspondence remains a `LEAD`. No full atlas rebuild was required or performed, and no repository or dirty-worktree content was inspected or edited.