# G248 evidence gates

1. **Preregistered:** PASS. Alternatives, finite gates, forbidden promotions, and landing ceiling
   were committed at `76f12551` before production or independent outcomes.
2. **Bounded scope:** PASS WITH STATED BOUND. The proof covers locally finite, transverse,
   noncaustic regular ordered null incidences. Caustics, infinite/nonproper fibers, source
   population, detection, and observational aggregation are excluded.
3. **Independently verified:** PASS. Production used SymPy and shear-generated symplectic matrices;
   the independent replay used only standard-library `Fraction` arithmetic and a Fourier/GL(2)
   symplectic construction. It imported neither production code nor production output.
4. **Premise audited:** PASS FOR THE BOUNDED LANDING. Every input is stamped in
   `PREMISE_LEDGER.tsv`; observational outcomes remained closed.

Pre-review status: `DERIVED_CONDITIONAL__INDEPENDENTLY_VERIFIED__EXTERNAL_REVIEW_PENDING`.
