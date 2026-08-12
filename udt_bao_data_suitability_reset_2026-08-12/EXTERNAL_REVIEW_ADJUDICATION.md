# External-review adjudication

The cold external landing `SUSTAINED_VERIFIED_WITH_CAVEATS` is accepted.

The reviewer found no mathematical, data, likelihood, ontology, or classification defect. Its two
requested repairs concern evidence presentation only:

1. `PREREGISTRATION_COMMIT_PROOF.md` now records the exact pushed Git commit, tree, blobs, and remote
   branch containment of the frozen preregistration.
2. `TABLE4_REPRESENTATION_NOTE.md` now states explicitly why a separately marginalized paper width
   and a diagonal entry of the released joint Gaussian covariance are different objects.

No numerical output was regenerated after these repairs. No tolerance, row, data product, landing,
or conclusion was changed.

Final grade:

```text
VERIFIED_WITH_CAVEATS__OBSERVED_PATTERN_DATA_SUITABILITY_ONLY
```

The caveats remain:

- the official vector is a fiducial/template-compressed publication product, not raw observer-pair
  data;
- the full vector requires a free publication-normalization nuisance in UDT;
- the ratio table's delta-method widths are characterization, not a substitute likelihood;
- a future UDT comparison requires its own preregistration and owned prediction map.
