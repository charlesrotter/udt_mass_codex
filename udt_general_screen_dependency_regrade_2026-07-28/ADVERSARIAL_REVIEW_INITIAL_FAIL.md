# Initial fresh adversarial review — FAIL and correction record

Date: 2026-07-28

Verdict: `FAIL_COMPLETENESS_NOT_CENTRAL_SCIENTIFIC_REGRADE`

The fresh zero-context reviewer independently replayed the original 22-source/390-row manifest and
accepted the central scientific narrowing, but rejected the first audit design for two reasons.

1. It automatically assigned 289 rows to `D0_NONE` unless manually overridden instead of requiring
   an explicit decision for every row.
2. It called most of the 248 lexically discovered primary-claim sources generically supporting or
   superseded without proving their current-authority route. In particular, the founded-phi and
   native-Hopfion controlling reports were not in the manifest.

The reviewer also identified four exact row corrections:

- parent screen `S06`: classify `D4` and stronger-nonuniqueness;
- parent screen `S09`: retain `D1` but use explicit scope correction;
- metric-natural no-go `full_holonomy_endpoint_lift`: classify `D1` and limit it to registered
  `lambda` strata;
- null/Hopf `N18`: classify `D2` and retain it as a diagonal-witness result.

## Applied correction

- `build_regrade.py` now has no automatic decision fallback. All 390 claim identities are
  explicitly enumerated; an omitted identity aborts generation.
- `LOAD_BEARING_SOURCE_MANIFEST.tsv` now includes 34 exact fixed-base sources, including every
  current premise controller, the founded-phi report and extension ledger, the native-Hopfion
  report, and the top current navigation/report sources.
- `PRIMARY_CLAIM_AUTHORITY_ROUTING.tsv` gives all 248 primary sources an explicit current authority
  role, owner, and routing basis.
- `FAMILY_AUTHORITY_ROUTING.tsv` gives all 174 discovered families an explicit route. High-risk
  July 25–27, C2/angular/coframe/boundary, Hopf, bootstrap/pre-density, projective/transverse,
  Cartan/holonomy, and `Xmax` lineages have named later owners rather than a generic supersession
  label.
- The four row corrections above are applied.

The failed review is preserved rather than overwritten. A new fresh adversarial context must pass
the corrected package before banking.
