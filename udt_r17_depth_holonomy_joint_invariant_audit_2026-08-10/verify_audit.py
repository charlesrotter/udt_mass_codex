#!/usr/bin/env python3
"""Fail-closed verifier for the R17 depth/holonomy joint audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "7c1cf38dfc9eaad6d55705eeae701243b3d41b34"
PREREG = "996da387"
PREREG_FILES = (
    "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "CANDIDATE_UNIVERSE.tsv",
    "FALSIFICATION_CONTRACT.tsv", "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv",
    "COMPLETENESS_MAP.md",
)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git(*args: str) -> bytes:
    return subprocess.check_output(("git", *args), cwd=ROOT)


def validate() -> dict[str, bool]:
    checks: dict[str, bool] = {}
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    candidates = rows("JOINT_CANDIDATE_CLASSIFICATION.tsv")
    chars = rows("CHARACTER_ATLAS.tsv")
    gauge = rows("GAUGE_INVARIANT_QUERY_ATLAS.tsv")
    one_forms = rows("LOCAL_ONE_FORM_COCYCLE_ATLAS.tsv")
    external_raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_bytes()
    external = (HERE / "EXTERNAL_REVIEW.md").read_text(encoding="utf-8")

    checks["preregistration_parent"] = git("rev-parse", f"{PREREG}^").decode().strip() == BASE
    checks["preregistered_files_unchanged"] = all(
        (HERE / name).read_bytes() == git("show", f"{PREREG}:{HERE.name}/{name}")
        for name in PREREG_FILES
    )

    manifest_ok = True
    manifest = rows("SOURCE_MANIFEST.tsv")
    for row in manifest:
        raw = git("show", row["source_ref"])
        manifest_ok &= git("rev-parse", row["source_ref"]).decode().strip() == row["git_blob"]
        manifest_ok &= hashlib.sha256(raw).hexdigest() == row["sha256"]
        manifest_ok &= len(raw) == int(row["size"])
    checks["source_manifest_16_exact"] = manifest_ok and len(manifest) == 16
    checks["external_raw_hash"] = hashlib.sha256(external_raw).hexdigest() == (
        "6aa844eefdff76af17e7934ffc249587e352e4dc11e7ebd58faa673446051f65"
    )
    checks["external_verdict"] = "`VERIFIED_WITH_CORRECTIONS`" in external_raw.decode("utf-8")
    checks["external_adjudication"] = all(token in external for token in (
        "product-groupoid type",
        "general rectangle line-integral control is not an R17 solution witness",
        "No scientific premise was promoted",
    ))

    checks["production_12_of_12"] = result["status"] == "PASS" and result["passed"] == result["total"] == 12
    checks["independent_16_of_16"] = independent["status"] == "PASS" and independent["passed"] == independent["total"] == 16
    checks["catches_17_of_17"] = catches["status"] == "PASS" and catches["rejected"] == catches["total"] == 17
    checks["candidate_ids_exact"] = [row["candidate_id"] for row in candidates] == [f"J{i:02d}" for i in range(1, 13)]
    checks["typed_joint_groupoid"] = result["joint_path_functor"] == (
        "R_ADDITIVE_TIMES_ORIENTED_NORMAL_ISOMETRY_GROUPOID__LOCALLY_R_TIMES_SO2"
    )
    checks["co2_all_weights"] = "ALL_REAL_w" in result["co2_family"]
    checks["vector_weight"] = result["complete_coframe_vector_weight"] == "w=-lambda"
    checks["covector_weight"] = result["complete_coframe_covector_weight"] == "w=+lambda"
    checks["unique_real_character"] = result["continuous_real_character"] == "UNIQUE_NORMALIZED_CHARACTER_IS_delta_K"
    checks["zero_angular_real_character"] = result["angular_real_character"] == "ZERO"
    checks["no_open_path_angular_scalar"] = result["open_path_representative_free_angular_scalar"] == "NONE"
    checks["semidirect_trivial"] = result["continuous_semidirect_depth_action"] == "TRIVIAL"
    checks["C08_independence_witness"] = "F23=-4097/2048" in result["depth_does_not_determine_holonomy"]
    checks["higher_jet_scope"] = result["higher_jet_scalar_path_cocycles"] == (
        "LINE_INTEGRALS_COMPOSE__GENERAL_NONEXACT_CONTROL_EXISTS__"
        "STATIONARY_R17_NONEXACT_REALIZATION_OPEN__NO_MEMBER_SELECTED"
    )
    checks["physical_path_open"] = result["physical_path_or_arrow_selected"] is False
    checks["character_targets"] = [row["target"] for row in chars] == ["R_additive", "U1", "R_universal_cover_angle"]
    checks["gauge_query_count"] = len(gauge) == 4
    checks["one_form_family_count"] = len(one_forms) == 4

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    checks["scope_guards"] = all(token in exact for token in (
        "not the missing four-dimensional physical observer arrow",
        "does not select the path",
        "Higher-jet line integrals: composition is general; stationary non-exactness is open",
        "No path, branch, `lambda`, on-shell equation, action, source",
        "not an R17 solution witness",
    ))
    checks["nonlinear_character_proof_present"] = "without assuming linearity" in exact
    checks["preregistered_refutation_recorded"] = (
        "preregistered claim" in exact or "preregistered possibility" in exact
    ) and "**refuted at the level of composition**" in exact
    checks["coframe_sign_conventions_disambiguated"] = all(token in exact for token in (
        "finite metric lift `exp(delta X_lambda)`",
        "reference coefficients carry the inverse factor",
        "inverse transpose according to arrow direction",
    ))

    return checks


def main() -> int:
    checks = validate()
    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "schema_version": 1,
        "checks": checks,
        "passed": len(checks) - len(failed),
        "total": len(checks),
        "failed": failed,
        "status": "PASS" if not failed else "FAIL",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
