#!/usr/bin/env python3
"""Consistency verifier for the bounded complete-geometry SNe replay."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_checks(root: Path = HERE) -> dict[str, bool]:
    required = (
        "PROVISIONAL_RADIATIVE_INTERFACE.md",
        "SNE_REPLAY_PREREGISTRATION.md",
        "SNE_REPLAY_VERIFIER_CORRECTION_PREREGISTRATION.md",
        "run_complete_geometry_sne_replay.py",
        "SNE_COMPLETE_GEOMETRY_CURVE.tsv",
        "SNE_COMPLETE_GEOMETRY_RESULT.json",
        "verify_complete_geometry_sne_independent.py",
        "SNE_COMPLETE_GEOMETRY_INDEPENDENT.json",
        "SNE_REPLAY_REPORT.md",
        "SNE_REPLAY_EVIDENCE_GATES.md",
        "SNE_EXTERNAL_ADVERSARIAL_REVIEW.md",
        "SNE_EXTERNAL_REVIEW_ADJUDICATION.md",
        "SNE_TRANSMISSION_RECORD.md",
        "SNE_REVIEW_MANIFEST.tsv",
    )
    checks = {f"exists:{name}": (root / name).is_file() for name in required}
    if not all(checks.values()):
        return checks
    result = json.loads((root / "SNE_COMPLETE_GEOMETRY_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((root / "SNE_COMPLETE_GEOMETRY_INDEPENDENT.json").read_text(encoding="utf-8"))
    report = (root / "SNE_REPLAY_REPORT.md").read_text(encoding="utf-8")
    interface = (root / "PROVISIONAL_RADIATIVE_INTERFACE.md").read_text(encoding="utf-8")
    prereg = (root / "SNE_REPLAY_PREREGISTRATION.md").read_text(encoding="utf-8")
    review = (root / "SNE_EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    adjudication = (root / "SNE_EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    with (root / "SNE_REVIEW_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        review_manifest = list(csv.DictReader(stream, delimiter="\t"))
    review_by_path = {row["path"]: row for row in review_manifest}
    with (root / "SNE_COMPLETE_GEOMETRY_CURVE.tsv").open(newline="", encoding="utf-8") as stream:
        curve = list(csv.DictReader(stream, delimiter="\t"))
    p1 = json.loads(
        (ROOT / "udt_sne_native_observer_query_replay_2026-08-11/REPLAY_RESULT.json").read_text(encoding="utf-8")
    )["replay"]["fits"]["A:zCMB:P1"]
    checks.update({
        "result_pass": result["status"] == "PASS",
        "landing_scoped": result["landing"].startswith("OBSERVED_CONDITIONAL_ONE_CONTROL_GEOMETRY_SNE_CURVE"),
        "all_production_checks": all(result["checks"].values()),
        "n_1367": result["data"]["n"] == 1367,
        "curve_rows_1367": len(curve) == 1367,
        "curve_hash_owned": digest(root / "SNE_COMPLETE_GEOMETRY_CURVE.tsv") == result["curve_atlas"]["sha256"],
        "shape_not_fitted": result["authority"]["shape_parameter_fitted"] is False,
        "one_offset_only": result["authority"]["single_offset_profiled"] is True,
        "physical_history_open": result["authority"]["physical_history_selected"] is False,
        "native_transfer_open": result["authority"]["native_radiative_law_derived"] is False,
        "xmax_open": result["authority"]["Xmax_identified"] is False,
        "eta_provisional": result["provisional_transfer"]["eta"] == 1.0 and "POSIT__CONDITIONAL" in result["provisional_transfer"]["status"],
        "epsilon_provisional": result["provisional_transfer"]["epsilon"] == "1/Z",
        "independent_pass": independent["status"] == "PASS" and all(independent["checks"].values()),
        "five_independent_anchors": len(independent["anchors"]) == 5,
        "likelihood_reproduced": independent["chi2_absolute_difference"] < 2.0e-4,
        "bad_fit_recorded": result["likelihood"]["chi2"] > 16000.0 and "STRONGLY_INCOMPATIBLE" in report,
        "p1_comparison_frozen": abs(float(p1["chi2"]) - 1260.8480887040496) < 1.0e-10,
        "no_merit_filter": "no lower-chi-square acceptance filter" in prereg,
        "interface_not_derived": "NOT_UDT_DERIVED" in interface,
        "all_sky_guard": "not an isotropy or" in report,
        "external_verdict_owned": "VERIFIED_WITH_CAVEATS__ONE_CONTROL_STRONGLY_SNE_INCOMPATIBLE" in review,
        "external_adjudication_scoped": "This does not reject the reciprocal kernel" in adjudication,
        "guard_role_scoped": "scope/consistency guards, not numerical tamper tests" in report,
        "sealed_manifest_30_rows": len(review_manifest) == 30,
        "sealed_data_hashes_owned": (
            review_by_path["Data/Pantheon+SH0ES.dat"]["sha256"] == result["data"]["catalog_sha256"]
            and review_by_path["Data/Pantheon+SH0ES_STAT+SYS.cov"]["sha256"]
            == result["data"]["covariance_sha256"]
        ),
    })
    return checks


def main() -> None:
    checks = build_checks()
    output = {
        "verifier_role": "package_consistency_not_independent_geometry_or_likelihood",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "all_pass": all(checks.values()),
    }
    (HERE / "SNE_REPLAY_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    if not output["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
