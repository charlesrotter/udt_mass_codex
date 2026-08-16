#!/usr/bin/env python3
"""Package-level G103 verifier."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_LANDING = (
    "LOCAL_REGULAR_ZERO_AND_FIRST_JET_OBSERVABLE_SURJECTION_DERIVED"
    "__COMMON_SKY_GRAM_AND_GENERIC_MEASURE_CONSISTENCY_ONLY"
    "__NO_NONTRIVIAL_SOURCE_INDEPENDENT_PATTERN_RESTRICTION_OWNED_IN_FROZEN_SOURCE_UNIVERSE"
    "__GLOBAL_CRITICAL_BOOTSTRAP_AND_SOURCE_HISTORY_JOINTS_OPEN"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    gates: dict[str, object] = {}
    required = [
        "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "CANDIDATE_RESTRICTION_CLASSES.tsv",
        "FALSIFICATION_CONTRACT.tsv", "SOURCE_MANIFEST_PREREG.tsv", "EXACT_DERIVATION.md",
        "RESTRICTION_ATLAS.tsv", "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "derive_restriction_atlas.py", "verify_restriction_independent.py", "run_catch_proofs.py",
        "EXTERNAL_REVIEW.md", "EXTERNAL_REVIEW_RAW.md", "EXTERNAL_REVIEW_ADJUDICATION.md",
        "REVIEW_DISPATCH.md",
    ]
    gates["required_files"] = all((HERE / name).is_file() for name in required)

    with (HERE / "SOURCE_MANIFEST_PREREG.tsv").open(encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    source_ok = True
    for row in source_rows:
        path = ROOT / row["path"]
        source_ok &= path.is_file() and sha256(path) == row["sha256"]
    gates["source_manifest_9_exact"] = source_ok and len(source_rows) == 9
    gates["protected_sources_absent"] = not any(
        "native_onshell" in row["path"] or "G88" in row["path"] or
        "regime_flow_reciprocal_orchestra" in row["path"]
        for row in source_rows
    )

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    gates["production_pass"] = derivation["status"] == "PASS"
    gates["landing_exact"] = derivation["landing"] == EXPECTED_LANDING
    gates["independent_fraction_pass"] = (
        independent["status"] == "PASS" and not independent["checks"]["imports_production"]
    )
    gates["hostile_mutations_11"] = (
        catches["status"] == "PASS" and len(catches["caught_mutations"]) == 11 and
        all(catches["caught_mutations"].values())
    )
    gates["outcomes_empty"] = (
        derivation["checks"]["outcome_artifacts_read"] == [] and
        independent["checks"]["outcome_artifacts_read"] == []
    )

    with (HERE / "RESTRICTION_ATLAS.tsv").open(encoding="utf-8") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    gates["restriction_atlas_10"] = (
        len(atlas) == 10 and [row["class_id"] for row in atlas] ==
        [f"C{i:02d}" for i in range(1, 11)]
    )
    gates["global_open_rows"] = all(
        next(row for row in atlas if row["class_id"] == cid)["result_status"].startswith("OPEN")
        for cid in ("C07", "C09", "C10")
    )

    banned = ("R2_OUTCOME_REPORT", "R3_OUTCOME_REPORT", "R4_OUTCOME_REPORT",
              "R5_OUTCOME_REPORT", "BOSS_CURVE", ".npz")
    executable_text = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("derive_restriction_atlas.py", "verify_restriction_independent.py")
    )
    gates["executable_outcome_blind"] = not any(token in executable_text for token in banned)
    gates["read_only_replay_mode"] = all(
        "UDT_READ_ONLY_REPLAY" in (HERE / name).read_text(encoding="utf-8")
        for name in (
            "derive_restriction_atlas.py", "verify_restriction_independent.py",
            "run_catch_proofs.py", "verify_package.py",
        )
    )

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    normalized_exact = " ".join(exact.split())
    gates["scope_language_present"] = all(
        phrase in exact for phrase in (
            "regular local/frozen-source ownership result",
            "not a generic no-go",
            "Global criticality, noninjectivity, topology, bootstrap",
        )
    )
    gates["fixed_base_caveat_present"] = all(
        phrase in normalized_exact for phrase in (
            "shared-base and pair-calibration premises are load-bearing",
            "outside the fixed-base positive-Gram order",
        )
    )
    gates["measure_nonuniqueness_present"] = "same marginal" in exact and "angle-cosine law" in exact

    failures = [name for name, passed in gates.items() if not passed]
    result = {
        "status": "PASS" if not failures else "FAIL",
        "gate_count": len(gates),
        "gates": gates,
        "failures": failures,
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
