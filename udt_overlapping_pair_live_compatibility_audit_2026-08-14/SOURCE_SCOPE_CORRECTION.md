# Source-scope correction before external review

Date: 2026-08-14

The outcome-blind preregistration commit `aa810251` included the protected, unbanked
`udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/EXACT_DERIVATION.md` as a
historical fixed-response source.

That direct dependency is unnecessary and operationally unsuitable for a clean startup or sealed
review surface:

- the banked G89 package already regrades the fixed-`P` result as a conditional diagnostic;
- this package independently derives the fixed-response trace and terminal-modulation results from
  the uncompressed evaluator;
- no result-producing script imports or reads the protected predecessor; and
- protected untracked contents must not enter the new commit or external intake.

Therefore `SOURCE_MANIFEST.tsv` replaces that one row with the banked
`udt_uncompressed_pair_kernel_reconstruction_2026-08-14/AUDIT_REPORT.md` at SHA-256
`45fa4a9a2a7ff911e3abf20ceae33eb88b2622c9201b4e0c63e9f63693fb9a13`.

This is a provenance-routing correction, not a post-outcome test or landing change. The original
preregistration remains preserved in git. The protected predecessor is neither modified nor staged.
