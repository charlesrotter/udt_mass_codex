#!/usr/bin/env python3
"""Consistency verifier for the null-carrier measure ownership package."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def table(root: Path, name: str) -> list[dict[str, str]]:
    with (root / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def build_checks(root: Path) -> dict[str, bool]:
    required = (
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "CANDIDATE_MEASURE_ATLAS.tsv",
        "SOURCE_CENSUS.tsv",
        "EXACT_DERIVATION.md",
        "derive_null_carrier_measure.py",
        "DERIVATION_RESULT.json",
        "verify_null_carrier_measure_independent.py",
        "INDEPENDENT_VERIFICATION.json",
        "STATUS_LEDGER.tsv",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EXTERNAL_ADVERSARIAL_REVIEW.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
    )
    checks = {f"exists:{name}": (root / name).is_file() for name in required}
    if not all(checks.values()):
        return checks

    primary = json.loads((root / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((root / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    candidates = {row["candidate_id"]: row for row in table(root, "CANDIDATE_MEASURE_ATLAS.tsv")}
    statuses_list = table(root, "STATUS_LEDGER.tsv")
    statuses = {row["object"]: row for row in statuses_list}
    exact = (root / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (root / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    external = (root / "EXTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    adjudication = (root / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    prereg = (root / "PREREGISTRATION.md").read_text(encoding="utf-8")
    checks.update(
        {
            "candidate_count_13": len(candidates) == 13,
            "status_objects_unique": len(statuses) == len(statuses_list),
            "preregistered_before_claim": "PENDING_DERIVATION" not in report and "Falsification and certification contract" in prereg,
            "determinant_identity": primary["determinant_expansion_identity"] is True,
            "inverse_area_transport_zero": primary["inverse_area_density_transport_residual"] == "0",
            "relabel_invariant": primary["source_relabelling_ratio_residual"] == "0",
            "tube_first_integral_closed": primary["query_tube_divergence_first_integral"] == "0",
            "star_k_catch": primary["outgoing_null_star_k_not_closed_divergence"] == "2/r",
            "coframe_triple_catch": primary["raw_coframe_triple_not_closed_coefficient"] != "0",
            "star_dphi_catch": primary["star_dphi_not_closed_box_phi"] != "0",
            "chern_simons_catch": primary["chern_simons_not_closed_F_wedge_F_coefficient"] != "0",
            "null_shell_scale_open": primary["null_shell_measure_scaling"] == "scale**2",
            "phase_volume_preserved": primary["hamiltonian_phase_divergence"] == "0",
            "arbitrary_distribution_not_transported": primary["arbitrary_phase_density_transport_residual"] != "0",
            "query_pushforward_valid_tautological": primary["query_label_pushforward_valid_but_tautological"] is True,
            "no_new_query_owner": primary["new_ownership_beyond_query_typing"] is False,
            "metric_representation_exact": primary["metric_density_and_jacobi_representation_exact"] is True,
            "physical_carrier_open": primary["physical_carrier_identification_selected"] is False,
            "physical_population_open": primary["physical_population_selected"] is False,
            "physical_eta_open": primary["physical_eta_selected"] is False,
            "independent_replay": independent["all_pass"] is True and "no_SymPy" in independent["implementation"],
            "label_current_typed_bookkeeping": candidates["C05"]["status"] == "VALID_QUERY_LABEL_BOOKKEEPING__TAUTOLOGICAL_PUSHFORWARD",
            "target_identification_open": candidates["C13"]["status"] == "OPEN_PHYSICAL_IDENTIFICATION_AND_ZERO_SIDE_FLUX_JOINT",
            "overall_externally_downgraded": statuses["overall"]["status"] == "EXTERNALLY_REVIEWED_WITH_CAVEATS__LABEL_CURRENT_VALID_BUT_TAUTOLOGICAL__NO_NEW_OWNERSHIP_BEYOND_QUERY_TYPING__PHYSICAL_ETA_OPEN",
            "metric_not_overcredited": "closure itself is already encoded in query typing" in exact,
            "eta_label_not_eta_physical": "physical `eta=1`" in report,
            "external_landing_preserved": "LABEL_CURRENT_VALID_BUT_TAUTOLOGICAL__NO_NEW_OWNERSHIP_BEYOND_QUERY_TYPING" in external,
            "external_replay_recorded": "independently replayed" in adjudication,
            "no_new_owner_recorded": "G96 supplies no new owner beyond" in adjudication,
        }
    )
    return checks


def main() -> None:
    checks = build_checks(ROOT)
    result = {
        "verifier_role": "package_consistency_not_independent_derivation",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "all_pass": all(checks.values()),
    }
    (ROOT / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
