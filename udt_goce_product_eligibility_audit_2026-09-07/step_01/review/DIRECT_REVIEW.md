# PE1 direct adversarial review

Date: 2026-09-07. Reviewer: `/root/pe1_source_review`, Codex, exact model
UNKNOWN. Candidate independently hash-checked before direct inspection:
`dc9614726e856f39bfffcb4fa3a314336b178603afdc8eb9cfe98d09e15906ac`.
This review applies to that text, not a later revision or delivered GOCE data.

Verdict: **VERIFIED-WITH-CAVEATS**, for a bounded documentation audit whose
product eligibility remains OPEN. No substantive scientific defect found in
the stated limits. One small source-ledger repair is requested before closing
the package; no scientific promotion follows from this verdict.

## Independence and exposure

| Axis | Actual status |
| --- | --- |
| Context | Fresh separate context; not main's conversation |
| Model | Exact model UNKNOWN; different-model UNTESTED |
| Sources | Catalogue and TN3397 retrieved independently; current TN URL supplied by main |
| Argument | SOURCE_FIRST.md sealed before candidate; direct normalization challenge followed candidate exposure |
| Implementation | New symbolic matrix calculation; author-code reruns are regression only |
| Human specialist | UNTESTED |

Source-first seal is preserved: SOURCE_FIRST.md SHA-256
`a3d64cccfe674946e11d4a871f146d7a069c0f41f37d91b7cc0d70cebf106941`.
After seal I sent main a summary before its candidate byte-freeze, including
the cached processor07.00 item. Main disclosed this author exposure. My direct
review then saw the candidate, source ledger, access record, diagnostic plan,
code and outputs. SOURCE_FIRST.md was not retrospectively altered. Initial
web/abstract/performance-prose exposure and retrieval failures are in
REVIEW_SCOPE.md and WEB_ACCESS_LOG.md; no flight outcomes informed the verdict.

## Challenges and strongest survivors

1. **Final-stage trace versus end-to-end sensitivity.** The printed Algorithm
   16 identity is correct. It does not itself set a diagonal from the other
   two. That rejects a claim of explicit trace projection in this block.
   It proves neither retention of a proposed scalar through calibration nor
   a nonzero `CP delta` for the delivered product. The candidate states that
   restriction explicitly and survives this challenge.

2. **Calibration and temporal reuse.** TN3397's external estimation blocks
   are distinct from its matrix-application algorithm; Figure 1 was checked
   visually. Interpolation endpoints, data-dependent outlier decisions and
   filtering support prevent a processed-file split from establishing unused
   support by itself. Calibration interpolation does not imply an additive
   affine scalar nuisance. The candidate does not make those substitutions.
   The strongest survivor is the identified dependency graph, not a complete
   external objective/configuration/support/error dossier.

3. **Length convention.** I inspected printed equations 6–10 and Algorithm
   16 layouts. With the same supplied half-separation matrix, their gradient
   reconstructions differ. My independent symbolic matrix reconstruction
   includes general symmetric off-diagonal entries and nonzero rotation:
   Algorithm 16 on the introductory half lengths gives `2*V - Omega^2`;
   on full pair lengths it gives `V`. At zero rotation this reduces to the
   candidate's factor-of-two comparison. The candidate correctly restricts
   this to the document as written. There is no demonstrated flight bug.
   The referenced TM1 file's hash and full-baseline/half-difference convention
   were checked; this review did not re-prove its physical interface.

4. **Algorithm 10's scope.** Its prose refers to common and differential
   accelerations, while its replacement loop assigns differential entries.
   The candidate records this as an unresolved written discrepancy and does
   not silently implement a repair. The statement survives the direct text
   check; no actual processor behavior is inferred.

5. **Versions and source limits.** Catalogue, TN3397 and old handbook hashes
   match the ledger. P2's saved official HTML has the named older processor
   versions; the handbook cover confirms issue 2 revision 0, 25/06/2008.
   These two files were inspected from main's captured temporary retrieval,
   not independently downloaded. The candidate keeps collection version,
   baseline, processor and document issue distinct and labels cached item
   provenance honestly. It does not equate the Level-2 release with L1b.

6. **PE2 authority.** A bounded written-method sensitivity/dependency check
   is within WORK_ORDER.md's second conditional step, provided its freeze
   retains all open estimator, baseline, linearity and error hypotheses.
   PE1 alone does not establish a deployed fixed-linear P, justified N,
   independent errors or unused observations. A second stage may return that
   precise unresolved bridge; it must not manufacture an empirical test or
   a native detector law. The candidate's stated PE2 limits satisfy this.

## Repair request and optional evidence

**R1 — source-ledger omission, small packaging defect.** The candidate's
processor07.00 statement is load-bearing but its exact cached ESA item URL is
absent from SOURCE_LEDGER.tsv, which currently ends at P7. The statement has
support, so it need not be withdrawn. Smallest repair: add a row with the
exact URL below, complete product identifier, cache-only status, directcurl
timeout, and explicit one-item/no-census limit. No new data retrieval or
scientific work is required. Focused re-review can check this row only.

https://eocat.esa.int/eo-catalogue/collections/GOCE_Level_1/items/GO_CONS_EGG_NOM_1b_20091111T013534_20091111T030518_0202?httpAccept=text%2Fhtml

Optional support, not a prerequisite for PE1's OPEN verdict: the public
[2019 calibration-paper publisher page](https://link.springer.com/article/10.1007/s00190-019-01271-9)
has a Data Availability Statement distinguishing shaking-mode data from its
other GOCE data. This helps locate a historical access dependency. It cannot
prove present global unavailability or that raw shaking arrays are the only
possible way to justify calibration-support/error provenance. Main's omission
of that additional source does not make its narrower uncertainty claim false.

## Actual checks, results and repair history

The author script SHA-256 was
`a64ff0fd30f03db49e590c6cacfb728ba62f097c6abf46677c6901061afb316b`.
`author_control_replay` returned 0 and independently reran its same-code
three Fraction assertions: `(2,3,5)`, `(4,6,10)`, `(2,3,5)` for the three
conventions. `author_mutant_replay` returned 1 at the designated printed
two-convention assertion. This catch-proof is regression, not an independent
argument about flight processing.

My independently implemented check was frozen in DIRECT_CHECK_PLAN.md.
`matrix_control_computed_witness` returned 0 under SymPy 1.13.1, checking four
exact symbolic identities. Its rotating rational witness has expected trace
10; the same-symbol convention gives `3040032/148225`; the full-separation
convention gives 10. `matrix_mutant` returned 1 at the deliberately false
half-length-as-full assertion. The full matrix identities, not one witness,
support the stated mathematical convention result.

An initial reporting-only defect was repaired in my own check: the first
`nonrotating_witness_diagonal_same` JSON entry echoed a constant list instead
of calculating it. The four symbolic assertions already computed their
results, so they were unaffected. Initial script SHA-256 was
`f6260be66743845085bd9a1cb769fe8ed2c578c749bb7f7dc78d9b536f28c988`;
its exact changed line was
`'nonrotating_witness_diagonal_same': ['4', '6', '10'],`.
It was replaced with direct substitution in the symbolic matrix. Initial
`matrix_control.*` and subsequent control/mutant records are all preserved.
Current script SHA-256:
`1c087c1117ea6efa297c79a46b13cf94f9bc0a8ded220aab3d4be9d044f68017`.
This self-repair adds no source assumption or scientific result.

All computational/replay children used the pre-read existing run_capture.py,
512 MiB address space and 60 s CPU/wall limits. Observed runtimes were below
one second each; recorded maximum RSS was below 60 MiB. No GPU or production
process was used. Full source documents/page renders remain temporary.
Captured method conversion/render stdout is empty, network stdout contains
request metadata only, and no long source text needs exclusion from this
review directory.

Skipped: all observation arrays and interval selection; actual processor
source/configuration/parameter replay; full external calibration objective;
retention injection through the delivered pipeline; flight noise/covariance;
raw-support partition; science premise re-audit and source theorem reproving;
different-model and human-specialist review. These omissions are consistent
with an OPEN product-eligibility result, never evidence of product absence.

No unresolved substantive review disagreement remains. R1 is the only
requested package repair. Evidence preservation and any later commit do not
adopt a premise, promote TM1/TM2, change registry grades or establish canon.
