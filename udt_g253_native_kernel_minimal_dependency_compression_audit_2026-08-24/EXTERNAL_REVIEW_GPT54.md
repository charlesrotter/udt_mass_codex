# Fresh external adversarial review — G253

Date: 2026-08-24

Reviewer: external Codex `gpt-5.4`, fresh zero-context read-only context

Authorized sealed intake:

- path: `/tmp/udt_g253_review_xcnll8p9`
- `REVIEW_SCOPE.json` SHA-256:
  `f5a93dc2308c1c376263a5d4316f9115695259bc874d4f6250fa26ca2b97df8a`
- 45 payloads plus the scope file

## Verbatim adjudication

**Findings**

1. High: the sealed intake cannot reproduce its own required no-write evidence. The reviewer
   verified `REVIEW_SCOPE.json` and all 45 payload hashes successfully, but the three substantive
   registered replays failed immediately because the frozen scientific sources live under
   `sources/` while the scripts dereference them from the intake root. In this intake, all 21
   manifest entries are absent from root and present under `sources/`. `run_catch_proofs.py
   --no-write` passes, but it is in-memory only and does not rescue sealed-source reproducibility.

**Adjudication**

1. Scalar chain: mostly yes, but not literally only the five items named. The compressed
   scalar/redshift chain still needs G243's source-observer query typing, and the current premise
   authority is load-bearing for status/precedence. No frozen evidence was found that P1, G116,
   G189, fits, or outcomes are active construction inputs.
2. `log(1+z)=Phi_source-Phi_observer`: yes, within the declared supplied source-observer query. The
   frozen sources keep it separate from angular response, luminosity, transfer, profiles, and
   outcomes.
3. Older arbitrary-calibration scalar as control after G176: yes. G176/G179/G197 consistently
   regrade it as a lawful control, not the active completed scalar.
4. Angular response as a distinct sibling channel: yes. G245/G244/G249 support metric-derived
   angular geometry upstream of readout, not a fitted patch and not a function of `Phi` alone.
5. G249-G252 and downstream normalization: yes. The frozen trace supports one downstream homothety
   scale only; it does not rewrite the dimensionless kernel or fit a history.
6. Mislabeled derived objects or premises: none material found. The ledgers keep G176 as
   `WORKING_FOUNDATIONAL_CLARIFICATION` and preserve the mixed-status ceiling.
7. Removable source in `MINIMAL_SOURCE_CUT.tsv`: none obvious without dropping one of the retained
   scalar, angular, or downstream-scale claims.
8. Excluded historical scaffold shown load-bearing: not from this frozen intake. The
   exclusion/control classification is internally consistent.

`REPAIRS_REQUIRED`.

The scientific landing is still supportable on a bounded source-first read: under a read-only
surrogate check against `sources/`, all 21 manifest hashes matched, all 8 production token sets and
5 independent token sets resolved, all 12 edge-source references resolved, and the hostile replay
caught 20/20 mutations. But the package as delivered fails its own required replay surface, so it
is not bankable as `VERIFIED` or `VERIFIED_WITH_CAVEATS`.

Required repairs:

1. Normalize source-path resolution across the sealed intake. Either prefix manifest and
   source-ledger paths with `sources/`, or make the verifier scripts resolve the `sources/` subtree
   explicitly.
2. Re-run `verify_package.py` and the two broken `--no-write` replays in the sealed layout and
   refresh the sealed run record/results only if the regenerated outputs are identical.

No further scientific repair is compelled by this intake beyond that packaging/replay defect.

## Local disposition

The scientific landing is retained without promotion. The certification defect is preregistered
for repair in `REPAIR_PREREGISTRATION.md`. A fresh sealed repair-only follow-up is required before
the package may be graded externally verified.
