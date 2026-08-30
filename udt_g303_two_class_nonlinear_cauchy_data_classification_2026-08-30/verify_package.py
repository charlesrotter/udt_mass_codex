#!/usr/bin/env python3
"""Mechanical package verifier for G303."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
LANDING = (
    "BOTH_G301_CLASSES_HAVE_THE_SAME_LOCAL_CAUSAL_PRINCIPAL_SYSTEM"
    "__TRACEFREE_DATA_ARE_THE_UNION_OVER_ONE_CONSTANT_SCALAR_DATUM"
    "__WELLPOSEDNESS_DOES_NOT_SELECT"
)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> None:
    required = {
        "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION_ANCESTRY.md",
        "SOURCE_MANIFEST.tsv", "derive_cauchy_classes.py", "verify_independent.py",
        "run_catch_proofs.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json", "EXACT_DERIVATION.md", "LAY_REPORT.md", "AUDIT_REPORT.md",
        "EVIDENCE_GATES.md", "STATUS_LEDGER.tsv", "COMMANDS.md", "RUN_RECORD.md",
        "verify_kernel_no_evolution_residual.py", "KERNEL_NO_EVOLUTION_RESIDUAL.json",
        "EXTERNAL_REVIEW_RESPONSE.md", "EXTERNAL_REVIEW_TRANSMISSION.md",
        "EXTERNAL_REVIEW_RUNTIME_REPAIR.md", "REPAIR_PREREGISTRATION.md",
    }
    missing = sorted(name for name in required if not (ROOT / name).is_file())
    assert not missing, missing

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catch = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    kernel = json.loads((ROOT / "KERNEL_NO_EVOLUTION_RESIDUAL.json").read_text(encoding="utf-8"))
    assert production["status"] == "PASS" and production["landing"] == LANDING
    assert production["nonlinear_equivalence"]["generic"] == "Ric_ab=0"
    assert production["nonlinear_equivalence"]["tracefree"] == "Ric_ab=Lambda*g_ab with dLambda=0"
    assert production["cauchy_constraints"]["generic_hamiltonian"].endswith("=0")
    assert production["cauchy_constraints"]["tracefree_hamiltonian"].endswith("=2*Lambda")
    assert production["principal_system"]["raw_tracefree_output_rank"] == 9
    assert production["principal_system"]["bianchi_completed_fixed_lambda_metric_rank"] == 10
    assert production["principal_system"]["lambda_is_lower_order"] is True
    assert production["lawful_data"]["extra_functional_degree"] is False
    assert production["lawful_data"]["extra_connected_region_constants"] == 1
    assert production["selection"]["wellposedness_selects_class"] is False
    assert production["selection"]["reciprocal_kernel_adds_evolution_residual"] is False

    assert independent["status"] == "PASS" and independent["landing"] == LANDING
    assert independent["imports_production_code"] is False
    assert independent["raw_tracefree_rank"] == 9
    assert independent["fixed_lambda_full_rank"] == 10
    assert independent["rank_nine_construction"].startswith("kernel basis")
    assert independent["extra_connected_constants"] == 1
    assert independent["extra_scalar_functions"] == 0
    assert catch["status"] == "PASS" and catch["count"] == 10
    assert catch["method"].startswith("formula and artifact mutations")
    assert all(item["caught"] for item in catch["caught"].values())
    assert kernel["status"] == "PASS"
    assert kernel["second_normal_jet_jacobian_rank"] == 0
    assert kernel["independent_cauchy_or_evolution_residuals_generated"] == 0

    with (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 6
    for row in sources:
        path = REPO / row["path"]
        assert path.is_file(), row["path"]
        assert digest(path) == row["sha256"], row["path"]

    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (ROOT / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    for document in (exact, audit):
        assert LANDING in document.replace("\n", "")
    for document in (exact, lay, audit):
        lowered = document.lower()
        assert "not" in lowered and "history" in lowered and "mass" in lowered
    assert "local boundary-free Cauchy slab" in audit
    assert "one additional number" in lay
    assert "D_i\\mathcal H=0" in exact
    assert "Bianchi-completed fixed-`Lambda` sector" in exact
    assert "conditional on the imported standard" in exact
    assert "raw trace-free equation by itself" in " ".join(lay.split())
    review = (ROOT / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    assert "VERIFIED_WITH_CAVEATS" in review
    assert "Scientific repair required:" in review

    output = {
        "status": "PASS",
        "landing": LANDING,
        "required_files": len(required),
        "source_hashes_verified": len(sources),
        "production_assertions": production["assertions"],
        "independent_assertions": independent["assertions"],
        "hostile_mutations_caught": catch["count"],
        "kernel_second_normal_jet_jacobian_rank": kernel["second_normal_jet_jacobian_rank"],
        "external_review": "VERIFIED_WITH_CAVEATS_REPAIRED",
    }
    (ROOT / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("G303 package verification PASS")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
