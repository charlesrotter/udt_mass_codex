G308_REPAIRABLE_DEFECTS

**Findings**
- `Medium, replay/packaging defect`: the registered no-write verifier is not portable to the sealed intake layout it is supposed to check. [verify_package.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_package.py:12) sets `ROOT = HERE.parent` and then hashes `ROOT / row["path"]` at [line 113](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_package.py:113), but [build_review_intake.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/build_review_intake.py:72) stores those frozen sources under `frozen_sources/`. In a fresh `/work` copy of the sealed intake, `python3 -S verify_package.py` failed with `FileNotFoundError`; it passed only after I added ephemeral sibling symlinks. This is repairable and not a bounded scientific defect.
- `Low, evidence-quality caveat`: the claimed “independent” verifier is non-importing, but not fully independent of the constructive ansatz. [verify_global_chirality_independent.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_global_chirality_independent.py:136) rebuilds the same outer-product `complex_structure` and the same `reflection` as production at [derive_global_chirality_coherence.py](/intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/derive_global_chirality_coherence.py:119). It is still a useful randomized algebraic stress test, but its independence claim is weaker than advertised.

Scientific defects: none found within the bounded G305/G307/G308 scope.

**Strongest Landing**
Within the bounded positive-standard G305 setting, yes: both G307 chiral members extend as smooth nowhere-zero global Hopf fields on `R x S3`, their normalized slice fields satisfy `nabla_{∂T}(K/a)=0`, and the package correctly distinguishes slice geodesicity from four-dimensional spacetime geodesicity since `nabla^{(4)}_V V = (a'/a) ∂T` in general. A transverse-orientation-reversing reflection in `O(4)` with determinant `-1` globally conjugates `J_+` to `J_-`, while no `SO(4)` map can do so because Pfaffian chirality is `SO(4)`-invariant. Pair reversal `J -> -J` preserves the 4D Pfaffian sign, so it is not parity. Connected smooth regular carry cannot switch chirality without leaving the regular orthogonal-complex/Hopf stratum; only degeneracy, discontinuity, singular or boundary routes, topology change, or orientation-forgetting mirror identification remain outside the theorem. The metric alone still selects neither physical sector, and G308 changes neither the G305 metric nor the reciprocal kernel.

**Commands**
```text
pwd  # exit 0
rg --files /intake  # exit 127, rg not installed
find /intake -maxdepth 2 -type d | sort  # exit 0
find /intake -maxdepth 3 -type f | sort  # exit 0
find /intake -maxdepth 4 -type f \( -name '*.py' -o -name '*.md' -o -name '*.txt' -o -name '*.json' -o -name '*.toml' -o -name 'Makefile' -o -name '*.sh' \) | sort  # exit 0
sed -n '1,220p' /intake/REVIEW_SCOPE.json  # exit 0
sed -n '1,260p' /intake/frozen_current/CURRENT_SCIENTIFIC_PREMISES.md  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/EXTERNAL_REVIEW_REQUEST.md  # exit 0
sed -n '1,320p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/EXACT_DERIVATION.md  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/derive_global_chirality_coherence.py  # exit 0
sed -n '1,320p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_global_chirality_independent.py  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/run_catch_proofs.py  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_package.py  # exit 0
sed -n '261,520p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/derive_global_chirality_coherence.py  # exit 0
sed -n '1,240p' /intake/frozen_sources/udt_g305_global_completion_hopf_domain_bridge_2026-08-30/DERIVATION_RESULT.json  # exit 0
sed -n '1,240p' /intake/frozen_sources/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/DERIVATION_RESULT.json  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/COMMANDS.md  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/RUN_RECORD.md  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/DERIVATION_RESULT.json  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/INDEPENDENT_VERIFICATION.json  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/CATCH_PROOF_RESULT.json  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/SOURCE_MANIFEST.tsv  # exit 0
sed -n '1,220p' /intake/frozen_sources/udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/DERIVATION_RESULT.json  # exit 0
sed -n '1,240p' /intake/frozen_sources/udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30/AUDIT_REPORT.md  # exit 0
sed -n '1,240p' /intake/frozen_sources/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/AUDIT_REPORT.md  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/AUDIT_REPORT.md  # exit 0
sed -n '1,240p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/VERIFICATION_RESULT.json  # exit 0
sed -n '1,240p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/COHERENCE_CENSUS.tsv  # exit 0
sed -n '1,220p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/EVIDENCE_GATES.md  # exit 0
mkdir -p /work/g308_review && cp -a /intake/. /work/g308_review/  # exit 0
python3 -S derive_global_chirality_coherence.py  # exit 0
python3 -S verify_global_chirality_independent.py  # exit 0
python3 -S run_catch_proofs.py  # exit 0
python3 -S verify_package.py  # exit 1, FileNotFoundError on missing sibling source path
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/build_review_intake.py  # exit 0
sed -n '1,260p' /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/SOURCE_SCOPE.tsv  # exit 0
find /work/g308_review -maxdepth 2 -type d | sort  # exit 0
ln -s /work/g308_review/frozen_sources/udt_g305_global_completion_hopf_domain_bridge_2026-08-30 /work/g308_review/udt_g305_global_completion_hopf_domain_bridge_2026-08-30 && ln -s /work/g308_review/frozen_sources/udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30 /work/g308_review/udt_g306_intrinsic_hopf_section_frame_descent_classification_2026-08-30 && ln -s /work/g308_review/frozen_sources/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30 /work/g308_review/udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30  # exit 0
python3 -S verify_package.py  # exit 0 after ephemeral symlink repair
cmp -s /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/DERIVATION_RESULT.json /work/g308_review/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/DERIVATION_RESULT.json; echo $?  # 0
cmp -s /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/INDEPENDENT_VERIFICATION.json /work/g308_review/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/INDEPENDENT_VERIFICATION.json; echo $?  # 0
cmp -s /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/CATCH_PROOF_RESULT.json /work/g308_review/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/CATCH_PROOF_RESULT.json; echo $?  # 0
cmp -s /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/COHERENCE_CENSUS.tsv /work/g308_review/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/COHERENCE_CENSUS.tsv; echo $?  # 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_package.py | sed -n '1,180p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/verify_global_chirality_independent.py | sed -n '1,260p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/derive_global_chirality_coherence.py | sed -n '1,280p'  # exit 0
nl -ba /intake/udt_g308_global_chirality_coherence_parity_classification_2026-08-31/build_review_intake.py | sed -n '1,180p'  # exit 0
```

I did not run the repository-only gates `python3 verify_current_scientific_premises.py` or `python3 -m pytest -q`, because the sealed scope explicitly excludes inspecting or relying on the wider repository.
