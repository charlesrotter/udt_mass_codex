#!/usr/bin/env python3
"""No-write integrity and semantic verifier for the G306 package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "ROUND_S3_METRIC_INTRINSICALLY_DEFINES_TWO_ORIENTED_HOPF_CONGRUENCE_FAMILIES"
    "__ISOTROPY_SELECTS_NO_PHYSICAL_MEMBER"
    "__SUPPLIED_GEOMETRIC_MEMBER_HAS_FRAME_INDEPENDENT_SCALE_BLIND_NORMALIZED_HELICITY"
    "__RAW_COMPONENT_HOPF_NUMBER_FAILS_FULL_LOCAL_FRAME_DESCENT"
    "__FIELD_QUERY_POPULATION_TARGET_ACTION_DYNAMICS_HISTORY_MAGNITUDE_MASS_AND_XMAX_REMAIN_OPEN"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    required = [
        "MAP.md", "PREREGISTRATION.md", "PREREGISTRATION_ANCESTRY.md",
        "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md", "SOURCE_SCOPE.tsv",
        "SOURCE_MANIFEST.tsv", "derive_intrinsic_hopf_section.py",
        "verify_intrinsic_hopf_section_independent.py", "run_catch_proofs.py",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json", "CANDIDATE_CENSUS.tsv", "STATUS_LEDGER.tsv",
        "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md",
        "EVIDENCE_GATES.md", "RUN_RECORD.md", "COMMANDS.md",
    ]
    for name in required:
        assert (HERE / name).is_file(), name

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert derivation["landing"] == LANDING
    assert derivation["candidate_landing"] == "A"
    assert derivation["production_assertions"] == 172
    assert derivation["isotropy_fixed_tangent_dimension"] == 0
    assert derivation["oriented_chiral_family_count"] == 2
    assert derivation["normalized_helicity_by_chirality"] == [-1, 1]
    assert derivation["individual_member_selected"] is False
    assert derivation["field_or_query_population_selected"] is False
    assert derivation["metric_and_kernel_changed"] is False
    assert independent["status"] == "PASS"
    assert independent["independent_checks"] == 22237
    assert independent["source_landing"] == LANDING
    assert catches["status"] == "PASS"
    assert catches["hostile_cases"] == 17
    assert catches["direct_computed_or_required_premise_mutations"] == 17

    for name in ("EXACT_DERIVATION.md", "AUDIT_REPORT.md"):
        assert LANDING in (HERE / name).read_text(encoding="utf-8").replace("\n", "")

    source_rows = 0
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            rel = Path(row["path"])
            assert not any(token in str(rel) for token in (
                "8_25",
                "udt_native_onshell_timelive_reset_owner_audit",
                "udt_pair_regime_flow_reciprocal_orchestra_amplification",
                "udt_sne_xmax_G88_am_radial_compatibility_atlas",
                "udt_kernel_plane_global_curvature_holonomy_atlas",
            ))
            assert sha256(ROOT / rel) == row["sha256"], rel
            source_rows += 1
    assert source_rows == 15
    print(f"PASS: G306 package; {len(required)} required files; {source_rows} source hashes")


if __name__ == "__main__":
    main()

