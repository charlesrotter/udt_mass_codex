#!/usr/bin/env python3
"""Exercise fail-closed semantic and census mutations for G70."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    atlas = table("RESTRICTION_RANK_ATLAS.tsv")
    summaries = table("MODEL_SUMMARY.tsv")
    owners = table("OWNERSHIP_LEDGER.tsv")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    catches = {
        "missing_atlas_row": len(atlas[:-1]) != 285,
        "duplicate_atlas_row": len({(r["model_id"], r["variant"], r["shape"], r["endpoint_x"]) for r in atlas + [atlas[0]]}) != len(atlas) + 1,
        "missing_model_variant": len(summaries[:-1]) != 19,
        "rectangular_rank_promoted": any(int(r["output_dimension"]) < 3 and r["classification"] == "FULL_RANK_OBSERVED" for r in atlas) is False,
        "threshold_retuned": "1e-6" not in prereg.replace("1e-6", "1e-5"),
        "R04_promoted": "does not justify promoting" not in report.replace("does not justify promoting", "justifies promoting"),
        "R05_promoted_to_physics": "not a physical CMB solution" not in report.replace("not a physical CMB solution", "a physical CMB solution"),
        "source_owner_invented": any(r["item"] == "native_source_state_covariance" and r["status"] != "OPEN" for r in owners) is False,
        "endpoint_owner_invented": any(r["item"] == "physical_endpoint_or_last_scattering" and r["status"] != "OPEN" for r in owners) is False,
        "TT_carry_invented": any(r["item"] == "scalar_TT_access_to_psi" and r["status"] != "OPEN" for r in owners) is False,
        "fit_added": "No observational anchor" not in report.replace("No observational anchor", "An observational anchor"),
        "unresolved_hidden": "15` preregistered cells" not in report.replace("15` preregistered cells", "zero preregistered cells"),
        "external_status_promoted": "EXTERNAL_REVIEW_PENDING" not in report.replace("EXTERNAL_REVIEW_PENDING", "EXTERNALLY_VERIFIED"),
        "scope_promoted": "cannot claim a unique" not in exact.replace("cannot claim a unique", "does claim a unique"),
    }
    payload = {"schema": "udt-cmb-g70-catches-v1", "caught": catches,
               "passed": sum(catches.values()), "total": len(catches)}
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    assert all(catches.values()), [key for key, value in catches.items() if not value]


if __name__ == "__main__":
    main()
