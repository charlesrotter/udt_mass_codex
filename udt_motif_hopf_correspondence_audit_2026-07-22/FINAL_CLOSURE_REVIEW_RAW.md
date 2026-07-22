# Verdict: FAIL

The validator repair is sound, but the frozen package is not reproducibly closed.

## Blocking findings

1. Committed `HEAD` `9104ac19f6692018ac99f4191f2e2e36c771f9a1` omits required generated evidence, including `ATLAS_RESULT.json`, `COHERENT_IDENTITY_REGISTRY.tsv`, and the raw compressed ledgers. In an isolated `git archive HEAD`, unchanged [verify_package.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/verify_package.py:61) immediately failed with `FileNotFoundError: ATLAS_RESULT.json`.

2. The committed rebuild path regresses source lineage. [build_correspondence_atlas.py](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/build_correspondence_atlas.py:54) defines only eight sources and overwrites `SOURCE_LINEAGE.tsv` at [line 480](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/build_correspondence_atlas.py:480). The corrected validator requires ten sources at [verify_review_corrections.py:470](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/verify_review_corrections.py:470). The isolated replay consequently failed `complete source lineage` after performing the covariance computation.

3. Therefore the full registered raw-ledger census cannot be independently reproduced or authenticated from the frozen closure commit. The committed [PACKAGE_VERIFICATION_TRANSCRIPT.txt](/tmp/udt_motif_hopf_20260722_zpmwYU/repo/udt_motif_hopf_correspondence_audit_2026-07-22/PACKAGE_VERIFICATION_TRANSCRIPT.txt:1) records a prior passing run, but no frozen raw ledgers or their hashes are present to audit that run.

## Findings that survived attack

- Supplying only a registry freshly generated from committed frozen sources allowed the correction verifier to reproduce byte-for-byte:

  - `67,396 / 33 / 27` point statuses;
  - all `63,488 = 63,438 + 50` edges, with the sole registered skip reason;
  - zero eligible-edge discordance;
  - all 29 mutation catches.

- The coordinated third-review corruption was rejected by `verify_package.py` with `exact point status census`.
- Negative, NaN, and infinite covariance/inversion/seed residuals, non-finite determinant, fabricated seed path, and negative point count were all rejected.
- All ten lineage hashes and 278 manifest entries passed.
- Independent symbolic/CPU replay reproduced the exact mixed Hessian, angular gap `2/A(phi)^2`, `Ω`-independent supplied-action connection, and a fresh 2,048-point Hopf-seed residual of `2.49e-14`.
- Scientific scope is honestly stated: supplied circle action; absent `S2` carrier and `L2+L4`; registered-chart Frobenius; 17-node sampled paths; overall `LEAD`. No repair strengthened the maximum.

## Four gates

1. Preregistered: **YES, confirmatory**.
2. Full or justified bounded scope: **NO for frozen package certification**; raw evidence is absent.
3. Independently verified: **YES for correction accounting and toric/seed witness; NO for the complete raw census from this closure state**.
4. Premises audited: **YES**.

Strongest independently supported conclusion in this audit:

`EXACT_CONDITIONAL_RECIPROCAL-TORIC/HOPF-SEED_COMPATIBILITY_WITNESS`.

The bounded motif/Frobenius census was not refuted, but cannot be re-certified from the frozen package. The conjunction requested as the scientific maximum therefore remains a reported `LEAD`, not a successfully closed certification.

No repository file was edited; untracked contents and `/home/udt-admin/udt_mass_codex` were not inspected.