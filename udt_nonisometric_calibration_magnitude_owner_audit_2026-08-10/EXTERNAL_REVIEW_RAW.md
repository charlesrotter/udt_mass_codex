TYPE_FAILURE

- The intake cannot satisfy the dispatch’s required manifest-confined reconstruction because the bundled verifier and catch-proof runner depend on upstream sibling paths and git objects that are not present in this read-only intake. The verifier reads external paths and `git show` sources at `verify_magnitude_ownership_independent.py:79` and `verify_magnitude_ownership_independent.py:124`; the catch-proof runner does the same at `run_catch_proofs.py:21`. That breaks the review contract in `COLD_REVIEW_DISPATCH.md:3` and the F11 fail-closed rule in `FALSIFICATION_CONTRACT.tsv:12`.

- The atlas cites load-bearing evidence outside `SOURCE_MANIFEST.tsv`, so the adjudication is not source-bounded as claimed. Examples at `MAGNITUDE_OWNER_ATLAS.tsv:2`, `:7`, `:83`, `:88`, and `:98` point to sources not listed in `SOURCE_MANIFEST.tsv`. Under the package’s own falsifier, that is a `TYPE_FAILURE`.

- The package overstates reproducibility inside this intake. `INDEPENDENT_VERIFICATION_RESULT.json` claims `source_hashes_verified: 24` and `VERIFIED`, but the bundled verifier can only make that claim by accessing the missing git/source store and then rewriting outputs. Likewise the production derivation is not runnable as dispatched because it regenerates outputs rather than auditing the frozen intake.

- Within the cached local outputs alone, the reviewer reproduced the internal shape of the claim: the atlas has 120 unique cells and the stated disposition counts, with only R17 and R18 marked `OWNER_CONDITIONAL_BRANCH_ONLY`. That does not cure the provenance defect, because the package’s own rule is that any load-bearing dependence outside the manifest escalates to `TYPE_FAILURE`.

Raw external return SHA-256 before transcription:

```text
3d905a6509364044e7a24aef34c26c5d1d9bd790f3da5dcda3921cb0096bdf18
```

The absolute temporary-intake links in the raw return were normalized to package-relative citations in this repository transcription. No scientific wording was strengthened.
