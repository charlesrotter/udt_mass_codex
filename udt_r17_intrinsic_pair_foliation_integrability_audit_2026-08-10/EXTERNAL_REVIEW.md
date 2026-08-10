# External adversarial review

Date: 2026-08-10

Reviewer: external Codex `gpt-5.4`, fresh sealed read-only intake

Verdict: **ACCEPT at the package's bounded conditional strength, with two repairable evidence defects**

Accepted landing:

```text
GLOBAL_PAIR_FOLIATION_AND_SCALAR_DEPTH_DERIVED__FULL_NORMAL_BUNDLE_ARROW_OPEN
```

The reviewer independently reconstructed the dual frame, the Frobenius closure of
`E=span(e0,e1)`, the nonclosure of `H=span(e2,e3)`, the global `R x S1` Hopf-cylinder leaves,
the leaf-metric determinant `-1`, and the terminal return `phi_pair=phi`. It found no manifested-
source refutation of the scoped result.

The reviewer rejected every stronger promotion: no preferred leaf, winding, cross-leaf connecting
surface, path-independent normal carry, carried-to-intrinsic reset, branch selection, or complete
physical observer arrow follows.

Two corrections were required:

1. the original independent verifier assigned final bracket and leaf-metric coefficients rather
   than deriving them constructively from the coframe and Maurer--Cartan data; and
2. `H` is a nonintegrable rank-two normal bundle in four dimensions. The word `contact` applies to
   its restriction to each spatial `S3` slice, not to a literal four-dimensional contact
   structure.

Those corrections are recorded in `POST_REVIEW_CORRECTION.md`. The first review's raw text is
preserved byte-for-byte except for the repository-required terminal newline in
`EXTERNAL_REVIEW_RAW.md`.

## Review provenance

- pre-ingest external-output SHA-256:
  `cb63e12244103dc92bcc554297b7a44e2a8c7ca425453762c62beff3a885196a`
- tracked raw-review SHA-256:
  `d5a17ecc1d2319218488f91da778251f1ebe9bfe4e11268b622efa82d13eac45`
- first sealed intake: 41 files, zero writable; 26 package files plus the exact 15 manifested
  repository sources

A corrected second transmission was not performed: the permission service required a new exact-
payload authorization. The local correction is therefore supported by the accepted first review,
the constructive independent implementation, and exercised mutation catches; it is not described
as a second external review.
