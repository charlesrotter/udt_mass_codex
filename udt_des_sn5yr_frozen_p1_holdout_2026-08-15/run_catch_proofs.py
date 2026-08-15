#!/usr/bin/env python3
"""Hostile semantic and covariance mutations for G100."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("g100_run", HERE / "run_holdout.py")
RUN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUN)


def require(condition: bool, label: str, checks: dict) -> None:
    if not condition:
        raise AssertionError(label)
    checks[label] = "PASS_REJECTED"


def main() -> None:
    checks = {}
    contract = json.loads((HERE / "TEST_CONTRACT.json").read_text())
    primary = json.loads((HERE / "PRIMARY_RESULT.json").read_text())
    secondary = json.loads((HERE / "SECONDARY_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    source = (HERE / "run_holdout.py").read_text()

    require(contract["frozen_model"]["n"] == primary["n_frozen"] == RUN.N_G99,
            "move_frozen_n", checks)
    require(primary["sample"] == "IDSURVEY==10" and primary["n_data"] == 1623,
            "replace_primary_sample", checks)
    require(primary["redshift"] == "zHD", "replace_primary_redshift", checks)
    require(primary["covariance"] == "STAT+SYS marginal DES block",
            "replace_primary_covariance", checks)
    require(primary["secondary_diagnostics_evaluated"] is False and
            secondary["may_repair_primary"] is False,
            "secondary_repairs_primary", checks)
    require(primary["status"] == "LOW_CHI2_COVARIANCE_OR_EFFECTIVE_DOF_WARNING" and
            primary["lower_tail_p"] < 0.01,
            "promote_low_chi2_to_clean_success", checks)
    require(primary["absolute_scale_inferred"] is False,
            "infer_absolute_scale_from_offset", checks)
    require(primary["LambdaCDM_distance_used"] is False and
            secondary["LambdaCDM_distance_used"] is False,
            "import_LambdaCDM_distance", checks)
    require(all(name not in source for name in ("MUMODEL", "MURES", "MUPULL")),
            "consume_forbidden_metadata_columns", checks)
    require(independent["status"] == "PASS_INDEPENDENT_SCHUR_AND_DIRECT_POWER_REPLAY",
            "skip_independent_replay", checks)

    tab = RUN.read_table(include_mu=True)
    keep = np.flatnonzero(tab["IDSURVEY"] == 10)
    w = RUN.unpack_precision(RUN.STAT_SYS)
    wrong_precision = w[np.ix_(keep, keep)]
    wrong = RUN.profile_from_precision(
        wrong_precision, tab["MU"][keep], RUN.mu_shape(tab["zHD"][keep]))
    require(abs(wrong["chi2"] - primary["chi2"]) > 1.0e-3,
            "subset_precision_instead_of_marginal_covariance", checks)
    require(abs(secondary["DES_only_STATONLY"]["chi2"] - primary["chi2"]) > 1.0,
            "drop_systematics_in_primary", checks)
    require(abs(secondary["DES_only_zHEL_STAT_SYS"]["chi2"] - primary["chi2"]) > 0.1,
            "silently_swap_zHD_for_zHEL", checks)
    require(secondary["DES_only_shape_profile"]["delta_chi2_frozen_minus_best"] > 1.0,
            "replace_frozen_shape_with_DES_best", checks)

    result = {"status": "PASS", "n_checks": len(checks), "checks": checks,
              "wrong_precision_chi2": wrong["chi2"],
              "primary_chi2": primary["chi2"]}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
