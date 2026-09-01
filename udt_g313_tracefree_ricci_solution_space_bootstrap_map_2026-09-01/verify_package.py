#!/usr/bin/env python3
"""Dependency-free aggregate replay and semantic verifier for G313."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rerun(script: str, expected_name: str, temporary: Path) -> dict:
    output = temporary / expected_name
    subprocess.run(
        [sys.executable, "-S", str(ROOT / script), "--output", str(output)],
        check=True,
        cwd=ROOT,
    )
    generated = output.read_bytes()
    expected = (ROOT / expected_name).read_bytes()
    if generated != expected:
        raise AssertionError(f"replay differs: {expected_name}")
    return json.loads(generated)


def main() -> None:
    required = [
        "PREREGISTRATION.md",
        "EXACT_DERIVATION.md",
        "SOLUTION_SPACE_ATLAS.tsv",
        "BOOTSTRAP_LEDGER.tsv",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PRODUCT_WITNESS_GLOBAL_PROOF.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REVIEW_RESPONSE.md",
        "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md",
        "REPAIR_FOLLOWUP_TRANSMISSION.md",
    ]
    for name in required:
        if not (ROOT / name).is_file():
            raise AssertionError(f"missing required artifact: {name}")

    with tempfile.TemporaryDirectory(prefix="g313_replay_") as temporary_name:
        temporary = Path(temporary_name)
        production = rerun("derive_solution_space.py", "DERIVATION_RESULT.json", temporary)
        independent = rerun("verify_independent.py", "INDEPENDENT_VERIFICATION.json", temporary)
        catches = rerun("run_catch_proofs.py", "CATCH_PROOF_RESULT.json", temporary)

    landing = "ACTIVE_EQUATION_DEFINES_MULTIBRANCH_EINSTEIN_ARENA__GLOBAL_ADMISSIBILITY_REMAINS_OPEN"
    if production["status"] != "PASS" or production["landing"] != landing:
        raise AssertionError("production landing")
    if production["assertions"] != 181:
        raise AssertionError("production assertion count")
    if independent["status"] != "PASS" or independent["assertions"] != 357:
        raise AssertionError("independent result")
    if not independent["round_uniqueness_refuted"] or not independent["scale_selection_refuted"]:
        raise AssertionError("independent scientific controls")
    if catches["mutations_registered"] != 12 or catches["mutations_caught"] != 12:
        raise AssertionError("hostile catch count")
    if len(production["cosh_checks"]) != 25 or any(row["Q"] != "0" for row in production["cosh_checks"]):
        raise AssertionError("R1 exact G309 residual replay")
    if production["bootstrap_type_check"]["selectors_exhausted"] != 8:
        raise AssertionError("R3 production selector census")
    if not production["bootstrap_type_check"]["hidden_history_response_rejected"]:
        raise AssertionError("R3 production hidden-response rejection")
    if len(independent["explicit_product_rows"]) != 12:
        raise AssertionError("R2 explicit product sample count")
    if not all(row["ricci_equals_lambda_metric"] for row in independent["explicit_product_rows"]):
        raise AssertionError("R2 explicit product Ricci")
    if not independent["product_global_structure"]["slice_compact"]:
        raise AssertionError("R2 compact product slice")
    if independent["bootstrap_type_check"]["factored_selector_response_cases"] != 32:
        raise AssertionError("R3 independent selector-response census")

    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (ROOT / "LAY_REPORT.md").read_text(encoding="utf-8")
    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    proof = (ROOT / "PRODUCT_WITNESS_GLOBAL_PROOF.md").read_text(encoding="utf-8")
    sources = (ROOT / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8")
    external = (ROOT / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    followup = (ROOT / "EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md").read_text(encoding="utf-8")
    required_tokens = [
        "EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_R1_R4_REPAIRS__SCIENTIFIC_LANDING_UNCHANGED",
        "not the complete active",
        "premise supplies a nonidentity predicate",
    ]
    for token in required_tokens:
        if token not in audit:
            raise AssertionError(f"audit token missing: {token}")
    for token in (
        "does not draw one unique universe",
        "an initial/global selection rule still has to choose",
        "This is compatible with Local",
    ):
        if token not in lay:
            raise AssertionError(f"lay token missing: {token}")
    for token in (
        "It is not one",
        "\\mathcal A:\\operatorname{Sol}/\\operatorname{Diff}",
        "C_{abcd}C^{abcd}=\\frac{16}{3}\\Lambda^2",
    ):
        if token not in exact:
            raise AssertionError(f"derivation token missing: {token}")
    for token in ("strictly monotone", "S1 x S2", "It does not assert that UDT physically populates it"):
        if token not in proof:
            raise AssertionError(f"product proof token missing: {token}")
    for token in (
        "udt_g307_directed_relation_hopf_member_reconstruction_2026-08-30/AUDIT_REPORT.md",
        "udt_g308_global_chirality_coherence_parity_classification_2026-08-31/AUDIT_REPORT.md",
    ):
        if token not in sources:
            raise AssertionError(f"R4 direct source missing: {token}")
    if "G313_REPAIRABLE_DEFECTS__SCIENTIFIC_LANDING_RETAINED" not in external:
        raise AssertionError("fresh external verdict missing")
    if "G313_REPAIRS_R1_R4_ACCEPTED__SCIENTIFIC_LANDING_UNCHANGED" not in followup:
        raise AssertionError("repair-only external verdict missing")

    print("G313 package verification PASS")
    print("production assertions: 181")
    print("independent assertions: 357")
    print("hostile semantic mutations caught: 12/12")
    print("preregistered repairs R1-R4 externally accepted; scientific landing unchanged")


if __name__ == "__main__":
    main()
