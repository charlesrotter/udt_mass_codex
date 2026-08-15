#!/usr/bin/env python3
"""Deterministic package verifier for G100."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def main() -> None:
    checks = {}

    def require(label: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(label)
        checks[label] = "PASS"

    required = [
        "PREREGISTRATION.md", "EXECUTION_CLARIFICATION.md", "DRY_GATE_REPAIR.md",
        "PREMISE_LEDGER.tsv", "SOURCE_MANIFEST_PREREG.tsv", "TEST_CONTRACT.json",
        "DRY_RUN_RESULT.json", "PRIMARY_RESULT.json", "SECONDARY_RESULT.json",
        "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json", "AUDIT_REPORT.md",
        "EXACT_METHOD.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv", "RESULT_CAVEATS.tsv",
        "EVIDENCE_GATES.md", "run_holdout.py", "verify_independent.py",
        "run_catch_proofs.py", "REPOSITORY_TEST_RECORD.json", "REVIEW_DISPATCH.md",
        "EXTERNAL_REVIEW.md", "EXTERNAL_REVIEW_ADJUDICATION.md"
    ]
    require("required_files", all((HERE / name).is_file() for name in required))

    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST_PREREG.tsv").open(), delimiter="\t"))
    hash_ok = True
    for row in rows:
        path = Path(row["path"])
        if not path.is_absolute():
            path = REPO / path
        hash_ok &= hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
    require("source_hashes_8", len(rows) == 8 and hash_ok)

    contract = json.loads((HERE / "TEST_CONTRACT.json").read_text())
    dry = json.loads((HERE / "DRY_RUN_RESULT.json").read_text())
    primary = json.loads((HERE / "PRIMARY_RESULT.json").read_text())
    secondary = json.loads((HERE / "SECONDARY_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    tests = json.loads((HERE / "REPOSITORY_TEST_RECORD.json").read_text())

    require("frozen_n", contract["frozen_model"]["n"] == 1.0559332414320268)
    require("contract_sample", contract["primary"]["expected_n"] == 1623)
    require("contract_offset_only", contract["frozen_model"]["primary_free_parameters"] ==
            ["B_additive_brightness_offset"])
    require("contract_no_LambdaCDM", "LambdaCDM_distance" in contract["forbidden_inputs"])
    require("dry_status", dry["status"] == "SCHEMA_AND_COVARIANCE_DRY_GATE_PASS")
    require("dry_counts", dry["n_all"] == 1820 and dry["n_des"] == 1623)
    require("dry_no_mu", dry["mu_consumed"] is False)
    require("dry_precision", dry["precision_shape"] == [1820, 1820] and
            dry["precision_symmetry_max_abs"] == 0.0 and dry["precision_cholesky"] == "PASS")

    require("primary_status", primary["status"] ==
            "LOW_CHI2_COVARIANCE_OR_EFFECTIVE_DOF_WARNING")
    require("primary_chi2", abs(primary["chi2"] - 1444.1864417493343) < 1.0e-9)
    require("primary_dof", primary["dof"] == 1622 and primary["n_data"] == 1623)
    require("primary_reduced", abs(primary["reduced_chi2"] - 0.8903738851722159) < 1.0e-14)
    require("primary_low_tail", primary["lower_tail_p"] < 0.01)
    require("primary_typed", primary["redshift"] == "zHD" and
            primary["covariance"] == "STAT+SYS marginal DES block")
    require("primary_no_scale_or_LCDM", primary["absolute_scale_inferred"] is False and
            primary["LambdaCDM_distance_used"] is False)
    require("primary_precedes_secondary", primary["secondary_diagnostics_evaluated"] is False)

    require("secondary_status", secondary["status"] == "SECONDARY_DIAGNOSTICS_COMPLETE")
    require("secondary_no_repair", secondary["may_repair_primary"] is False and
            secondary["primary_status_unchanged"] == primary["status"])
    require("secondary_full", abs(secondary["full_1820_STAT_SYS"]["chi2"] -
                                    1654.530309960246) < 1.0e-9)
    require("secondary_stat", abs(secondary["DES_only_STATONLY"]["chi2"] -
                                    1482.5694020539522) < 1.0e-9)
    require("secondary_zhel", abs(secondary["DES_only_zHEL_STAT_SYS"]["chi2"] -
                                    1443.4738674461842) < 1.0e-9)
    shape = secondary["DES_only_shape_profile"]
    require("secondary_shape", abs(shape["n_best"] - 1.0152457866699016) < 1.0e-12)
    require("secondary_delta", abs(shape["delta_chi2_frozen_minus_best"] -
                                     2.6826984956860542) < 1.0e-12)
    require("secondary_shape_p", abs(shape["delta_chi2_1dof_upper_tail_p"] -
                                       0.10144369696694312) < 1.0e-15)
    require("secondary_bins", len(secondary["DES_only_equal_count_residual_bins"]) == 10 and
            sum(x["n"] for x in secondary["DES_only_equal_count_residual_bins"]) == 1623)

    require("independent_status", independent["status"] ==
            "PASS_INDEPENDENT_SCHUR_AND_DIRECT_POWER_REPLAY")
    require("independent_primary", independent["absolute_differences"]["primary_chi2"] < 1.0e-8)
    require("independent_shape", independent["absolute_differences"]["shape_n"] < 1.0e-6)
    require("catch_proofs", catches["status"] == "PASS" and catches["n_checks"] == 14)
    require("repository_tests", tests["repository_tests"]["passed"] == 90 and
            tests["repository_tests"]["xfailed"] == 1 and
            tests["repository_tests"]["failed"] == 0)
    require("premise_tests", tests["premise_verifier"]["guards_passed"] == 99 and
            tests["premise_verifier"]["registry_rows"] == 87)

    report = (HERE / "AUDIT_REPORT.md").read_text()
    require("report_scope", "LOW_CHI2_COVARIANCE_OR_EFFECTIVE_DOF_WARNING" in report and
            "No Lambda-CDM distance import" in report and "does not derive P1" in report)
    external = (HERE / "EXTERNAL_REVIEW.md").read_text()
    require("external_review", "PASS_WITH_CAVEATS" in external and
            "approximate rather than exact" in external and
            "1444.1864417493343" in external)
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text()
    require("portability_repair", "--data-dir" in adjudication and
            "--check-only" in adjudication)
    run_source = (HERE / "run_holdout.py").read_text()
    require("production_forbidden_columns_absent",
            all(name not in run_source for name in ("MUMODEL", "MURES", "MUPULL")))

    result = {"status": "PASS", "n_checks": len(checks), "checks": checks}
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
