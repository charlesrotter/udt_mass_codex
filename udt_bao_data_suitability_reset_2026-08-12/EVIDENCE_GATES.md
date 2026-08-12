# Evidence gates

1. **Preregistered:** yes. `PREREGISTRATION.md`, the ten fixed gates, candidate lineages, result
   classes, and maximum conclusion were committed before the official DR2 numbers were inspected.
2. **Full space or bounded scope justified:** yes for the declared six-lineage data-suitability
   audit. This is not a raw-survey census and not a cosmological fit.
3. **Independently verified:** yes for the load-bearing public covariance and Gaussian likelihood.
   The released Cobaya implementation, a NumPy replay, and a no-NumPy `Decimal` implementation agree.
4. **Premises audited:** yes for data ontology. Fiducial conversion is a declared readout layer;
   release normalization is a nuisance; acoustic/ruler/Lambda-CDM interpretations are excluded.

Verdict grade: `VERIFIED-WITH-CAVEATS` data suitability, not a UDT physics verdict. A fresh sealed
external `gpt-5.4` review returned `SUSTAINED_VERIFIED_WITH_CAVEATS`; both requested documentary
repairs have been implemented without changing any number or classification.

Open caveats:

- the public Gaussian widths do not exactly equal every separately marginalized Table 4 width;
- the six ratio uncertainties in `OFFICIAL_DR2_AP_SHAPE.tsv` use a delta-method projection and are
  not a replacement for the original covariance in a fit;
- the Git timestamp is repository provenance, not a separately signed third-party timestamp;
- no UDT prediction, normalization profile, source interpretation, or `X_max` estimate was tested.
