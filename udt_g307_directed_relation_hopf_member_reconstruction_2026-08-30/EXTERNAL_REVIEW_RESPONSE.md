G307_REPAIRABLE_DEFECTS

**Findings**
- `Replay/packaging defect:` one registered command is broken in the sealed layout. [COMMANDS.md](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/COMMANDS.md:6) registers `python3 -S build_review_intake.py`, but [build_review_intake.py](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/build_review_intake.py:55) and [build_review_intake.py](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/build_review_intake.py:65) resolve prerequisite files as `REPO / row["path"]` and `REPO / name`. In the sealed intake those inputs live under `frozen_sources/` and `frozen_current/`, so the registered replay fails with `FileNotFoundError` before sealing logic completes. This is repairable and non-scientific, but it prevents a clean all-commands replay from the review bundle as delivered.
- `Replay weakness:` the “independent” verifier is genuinely import-independent, but it is narrower than the load-bearing theorem. [verify_directed_member_independent.py](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/verify_directed_member_independent.py:94) directly constructs the two `route ± screen` complex operators from an already oriented frame and then checks their properties at [verify_directed_member_independent.py](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/verify_directed_member_independent.py:131). It does not independently reconstruct `u_L=v\bar p`, `u_R=\bar p v`, or independently prove uniqueness from `(p,v)` alone. That is a replay-quality caveat, not a scientific refutation.
- `Replay weakness:` the hostile-control script mutates reported result fields, not the derivation code or premises. [run_catch_proofs.py](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/run_catch_proofs.py:42) reads `DERIVATION_RESULT.json`, and [run_catch_proofs.py](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/run_catch_proofs.py:56) perturbs JSON values only. So the 14 catches are semantic/report guards, not mutation testing of the mathematics.
- `Scientific review:` no scientific defect found in the bounded theorem. The reconstruction formulas and uniqueness claim are correct for every regular ordered `(p,v)`: if `u_L p=v` then `u_L=v\bar p`, and if `p u_R=v` then `u_R=\bar p v`; both are pure imaginary unit quaternions because `Re(v\bar p)=<v,p>=0` and norms multiply. The two survivors agree on `span{p,v}`, hence on the full great-circle `q(θ)=cosθ p+sinθ v`, exactly as stated in [EXACT_DERIVATION.md](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EXACT_DERIVATION.md:43), [EXACT_DERIVATION.md](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EXACT_DERIVATION.md:67), and [EXACT_DERIVATION.md](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EXACT_DERIVATION.md:81).
- `Scientific review:` I do not find the claimed route/screen conflation. The package keeps “complete one-dimensional route and metric carry” separate from “oriented signed transverse-screen first jet” in both the derivation and ledgers: [EXACT_DERIVATION.md](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EXACT_DERIVATION.md:84), [EXACT_DERIVATION.md](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EXACT_DERIVATION.md:100), [PREMISE_LEDGER.tsv](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/PREMISE_LEDGER.tsv:7), [PREMISE_LEDGER.tsv](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/PREMISE_LEDGER.tsv:8), [STATUS_LEDGER.tsv](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/STATUS_LEDGER.tsv:6), [STATUS_LEDGER.tsv](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/STATUS_LEDGER.tsv:7). Parallel transport of a supplied screen frame along the route is longitudinal metric carry; the chirality discriminator is the off-route transverse derivative `∇_w V = ± z/a`, which is extra data.
- `Scientific review:` the chirality sign is orientation-relative, not absolute. The binary datum is meaningful only after the slice orientation and the oriented screen are supplied; reversing either swaps the labels/sign. The package types that correctly at [PREMISE_LEDGER.tsv](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/PREMISE_LEDGER.tsv:4) and [EXACT_DERIVATION.md](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EXACT_DERIVATION.md:89).
- `Scientific review:` the radius dependence is exactly `1/a` for every `a>0`. From the upstream G306 field formula [EXACT_DERIVATION.md](/intake/frozen_sources/udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/EXACT_DERIVATION.md:116) and covariant-derivative formula [EXACT_DERIVATION.md](/intake/frozen_sources/udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/EXACT_DERIVATION.md:123), a transverse screen vector satisfies `∇_w V = Jw/a = ± z/a`. Since `a>0`, only the magnitude changes with radius; the sign census is stable on all positive radii.
- `Scientific review:` the G298/G299/G300 ownership boundary is preserved. The frozen audits keep lawful query family and physical population open, and G307 repeats that boundary rather than promoting conditional reconstruction into a populated route, screen, field, dynamics, or history: [G298 audit](/intake/frozen_sources/udt_g298_causal_diamond_to_pair_germ_transfer_2026-08-29/AUDIT_REPORT.md:24), [G299 audit](/intake/frozen_sources/udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/AUDIT_REPORT.md:14), [G300 audit](/intake/frozen_sources/udt_g300_metric_celestial_query_bundle_descent_2026-08-29/AUDIT_REPORT.md:14), [EXACT_DERIVATION.md](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EXACT_DERIVATION.md:123).
- `Scientific review:` no metric term, reciprocal-kernel term, action, source, matter model, mass law, scale, observation, or physical `X_max` entered. That omission is explicit in [EXACT_DERIVATION.md](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EXACT_DERIVATION.md:14), [PREMISE_LEDGER.tsv](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/PREMISE_LEDGER.tsv:11), and [PREMISE_LEDGER.tsv](/intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/PREMISE_LEDGER.tsv:12).

**Landing**
Strongest defensible bounded landing remains:
```text
SUPPLIED_DIRECTED_GERM_SELECTS_ONE_MEMBER_PER_CHIRAL_FAMILY
__SIGNED_TRANSVERSE_SCREEN_GERM_SELECTS_ONE_MEMBER_CONDITIONALLY
__ACTIVE_PREMISES_POPULATE_NEITHER__PHYSICAL_MEMBER_REMAINS_OPEN
```
That scientific landing is supported. The downgrade from full acceptance is due to replay/packaging defects, not because the bounded theorem was refuted. In `/work`, `derive_directed_member_reconstruction.py`, `verify_directed_member_independent.py`, `run_catch_proofs.py`, and `verify_package.py` all passed; the regenerated `DERIVATION_RESULT.json`, `INDEPENDENT_VERIFICATION.json`, `CATCH_PROOF_RESULT.json`, and `MEMBER_CENSUS.tsv` matched the sealed copies byte-for-byte. I did not run `python3 verify_current_scientific_premises.py` because the sealed intake does not contain that script and your scope barred inspection outside `/intake`; I relied on the sealed `PREMISE_AUDIT_RESULT.json` plus the frozen current registry instead.

**Commands**
```bash
pwd
rg --files /intake
find /intake -maxdepth 2 -type d | sort
find /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30 -maxdepth 3 -type f | sort
find /intake/frozen_current -maxdepth 3 -type f | sort
find /intake/frozen_sources -maxdepth 3 -type f | sort
sed -n '1,220p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EXACT_DERIVATION.md
sed -n '1,220p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/AUDIT_REPORT.md
sed -n '1,220p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EVIDENCE_GATES.md
sed -n '1,220p' /intake/frozen_current/CURRENT_SCIENTIFIC_PREMISES.md
sed -n '1,220p' /intake/frozen_sources/udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/EXACT_DERIVATION.md
sed -n '1,220p' /intake/frozen_sources/udt_g298_causal_diamond_to_pair_germ_transfer_2026-08-29/AUDIT_REPORT.md
sed -n '1,220p' /intake/frozen_sources/udt_g299_complete_relation_kernel_domain_ownership_2026-08-29/AUDIT_REPORT.md
sed -n '1,220p' /intake/frozen_sources/udt_g300_metric_celestial_query_bundle_descent_2026-08-29/AUDIT_REPORT.md
sed -n '1,260p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/COMMANDS.md
sed -n '1,260p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/verify_package.py
sed -n '1,320p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/derive_directed_member_reconstruction.py
sed -n '1,320p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/verify_directed_member_independent.py
sed -n '1,340p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/run_catch_proofs.py
sed -n '1,260p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/build_review_intake.py
sed -n '1,240p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/VERIFICATION_RESULT.json
find /intake -maxdepth 2 -name 'verify_current_scientific_premises.py' -o -name 'verify_current_scientific_premises.py'
sed -n '1,220p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/MAP.md
sed -n '1,220p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/COMPLETENESS_MAP.md
sed -n '1,240p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/SOURCE_MANIFEST.tsv
sed -n '1,240p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/PREMISE_LEDGER.tsv
sed -n '1,240p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/PREMISE_AUDIT_RESULT.json
grep -RIn "complete one-dimensional route and metric frame carry\|transverse\|screen first jet\|parallel transport\|frame carry" /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30 /intake/frozen_sources/udt_g299_complete_relation_kernel_domain_ownership_2026-08-29 /intake/frozen_sources/udt_g300_metric_celestial_query_bundle_descent_2026-08-29
sed -n '1,220p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/LAY_REPORT.md
sed -n '1,240p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EXTERNAL_REVIEW_REQUEST.md
sed -n '1,240p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/STATUS_LEDGER.tsv
mkdir -p /work/g307_review && cp -a /intake/. /work/g307_review/
python3 -S derive_directed_member_reconstruction.py
python3 -S verify_directed_member_independent.py
python3 -S run_catch_proofs.py
python3 -S verify_package.py
python3 -S build_review_intake.py
sha256sum /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/DERIVATION_RESULT.json /work/g307_review/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/DERIVATION_RESULT.json
sha256sum /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/INDEPENDENT_VERIFICATION.json /work/g307_review/udt_g307_review/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/INDEPENDENT_VERIFICATION.json
sha256sum /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/CATCH_PROOF_RESULT.json /work/g307_review/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/CATCH_PROOF_RESULT.json
sha256sum /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/MEMBER_CENSUS.tsv /work/g307_review/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/MEMBER_CENSUS.tsv
sha256sum /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/INDEPENDENT_VERIFICATION.json /work/g307_review/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/INDEPENDENT_VERIFICATION.json
nl -ba /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/EXACT_DERIVATION.md | sed -n '1,180p'
nl -ba /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/build_review_intake.py | sed -n '1,180p'
nl -ba /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/verify_directed_member_independent.py | sed -n '1,220p'
nl -ba /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/run_catch_proofs.py | sed -n '1,220p'
nl -ba /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/PREMISE_LEDGER.tsv | sed -n '1,80p'
nl -ba /intake/frozen_sources/udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/EXACT_DERIVATION.md | sed -n '90,160p'
nl -ba /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/COMMANDS.md | sed -n '1,80p'
nl -ba /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/STATUS_LEDGER.tsv | sed -n '1,80p'
sed -n '1,240p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/SOURCE_SCOPE.tsv
sed -n '1,220p' /intake/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/RUN_RECORD.md
```