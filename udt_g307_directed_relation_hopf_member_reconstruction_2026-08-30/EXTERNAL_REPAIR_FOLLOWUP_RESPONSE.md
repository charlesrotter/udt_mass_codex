G307_REPAIRS_ACCEPTED

Replay defects: none found.

Scientific regressions: none found.

R1: [build_review_intake.py](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/build_review_intake.py) resolves each frozen source/current file from exactly one of the repository or sealed locations and raises on missing or ambiguous layouts. In the writable sealed copy, `python3 -S build_review_intake.py` passed, and [verify_repair_portability.py](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/verify_repair_portability.py) passed with `rebuilt_manifest_byte_identical: true`, plus all four rejection flags true.

R2: [verify_directed_member_independent.py](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/verify_directed_member_independent.py) imports only standard-library modules, builds independent left/right evaluation maps from `(q,v)`, checks their Gram matrices are the identity, solves coefficients by projection, matches `v conjugate(q)` and `conjugate(q) v`, reconstructs both full operators, and compares them to independently built route/screen operators. Replay passed with `independent_checks: 32000` and `maximum_error: 4.1389114358025836e-13`.

R3: [run_catch_proofs.py](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/run_catch_proofs.py) exercises exactly 8 direct mathematical corruptions on an exact noncommuting witness, in addition to 14 semantic guards. Replay passed with `hostile_cases: 22`, `direct_mathematical_mutations: 8`, `semantic_result_mutations: 14`.

R4: [COMMANDS.md](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/COMMANDS.md) clearly separates sealed package replays from repository-only `verify_current_scientific_premises.py` and `pytest`, and explicitly says those repository gates are recorded, not self-contained sealed replays.

Unchanged landing: `python3 -S derive_directed_member_reconstruction.py` and `python3 -S verify_package.py` both passed. The landing remained exactly `SUPPLIED_DIRECTED_GERM_SELECTS_ONE_MEMBER_PER_CHIRAL_FAMILY__SIGNED_TRANSVERSE_SCREEN_GERM_SELECTS_ONE_MEMBER_CONDITIONALLY__ACTIVE_PREMISES_POPULATE_NEITHER__PHYSICAL_MEMBER_REMAINS_OPEN`. The member census remained unchanged, `metric_and_kernel_changed` remained `false`, and regenerated copy outputs matched the sealed evidence for `DERIVATION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`, `CATCH_PROOF_RESULT.json`, `MEMBER_CENSUS.tsv`, and `PORTABILITY_VERIFICATION_RESULT.json`.

Commands run:
- `cp -a /intake/. /work/g307_review.0JDHqe/`
- `python3 -S derive_directed_member_reconstruction.py`
- `python3 -S verify_directed_member_independent.py`
- `python3 -S build_review_intake.py`
- `python3 -S run_catch_proofs.py`
- `python3 -S verify_repair_portability.py`
- `python3 -S verify_package.py`
- `cmp -s` comparisons for regenerated evidence vs sealed originals