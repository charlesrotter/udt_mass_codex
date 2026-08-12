#!/usr/bin/env python3
"""Administrative/artifact consistency checks; not an independent derivation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    checks = {}
    required = [
        "PRE_REGISTRATION.md", "PREMISE_LEDGER.tsv", "SOURCE_MANIFEST.tsv",
        "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md",
        "derive_chord_network.py", "verify_chord_network_independent.py", "run_catch_proofs.py",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOFS.json",
        "PAIR_ATLAS.tsv", "CHAIN_ATLAS.tsv",
        "REVIEW_DISPATCH.md", "EXTERNAL_REVIEW_RAW.md", "EXTERNAL_REVIEW_ADJUDICATION.md",
        "RESULT_MANIFEST.tsv",
    ]
    checks["required_files"] = all((ROOT / name).is_file() for name in required)

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_count"] = len(sources) == 9
    checks["source_hashes"] = all(
        (REPO / row["path"]).is_file() and sha256(REPO / row["path"]) == row["sha256"]
        for row in sources
    )

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((ROOT / "CATCH_PROOFS.json").read_text())
    checks["symbolic_checks"] = production["symbolic_check_count"] == 15 and all(production["symbolic_checks"].values())
    checks["production_states"] = production["state_count"] == 100
    checks["production_pairs"] = production["pair_count"] == 10000 and production["ordered_pair_count"] == 1698
    checks["production_chains"] = production["chain_count"] == 10518
    checks["production_no_reverse_loop"] = (
        production["nontrivial_reverse_psd_count"] == 0
        and production["nontrivial_directed_loop_count"] == 0
    )
    checks["production_strata"] = all(production["pair_counts"][key] > 0 for key in [
        "INCOMPARABLE", "PSD_RANK_0", "PSD_RANK_1", "PSD_RANK_2"
    ])
    checks["independent_states_pairs"] = independent["state_count"] == 64 and independent["pair_count"] == 4096
    checks["independent_all_triples"] = independent["all_triple_composition_checks"] == 262144
    checks["independent_chains"] = independent["ordered_chain_count"] == 3955
    checks["independent_no_reverse_loop"] = (
        independent["nontrivial_reverse_psd_count"] == 0
        and independent["nontrivial_directed_loop_count"] == 0
    )
    checks["independent_middle"] = independent["independent_middle_transition_required"] is True
    checks["independent_scope_wording"] = (
        "replays supplied closed-form transition" in independent["implementation"]
        and "source hashes read parent repo" in independent["implementation"]
    )
    checks["catch_proofs"] = catches["catch_count"] == 11 and all(catches["catches"].values())

    raw_review = (ROOT / "EXTERNAL_REVIEW_RAW.md").read_text()
    adjudication = (ROOT / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text()
    checks["external_verdict"] = (
        "ACCEPT__VERIFIED_WITH_CAVEATS" in raw_review
        and "Mathematical corrections:\n- None." in raw_review
        and "ACCEPT__VERIFIED_WITH_CAVEATS" in adjudication
    )

    with (ROOT / "RESULT_MANIFEST.tsv").open(newline="") as handle:
        result_rows = list(csv.DictReader(handle, delimiter="\t"))
    checks["result_manifest_count"] = len(result_rows) == 20
    checks["result_manifest_hashes"] = all(
        (ROOT / row["path"]).is_file() and sha256(ROOT / row["path"]) == row["sha256"]
        for row in result_rows
    )

    with (ROOT / "PAIR_ATLAS.tsv").open(newline="") as handle:
        pairs = list(csv.DictReader(handle, delimiter="\t"))
    with (ROOT / "CHAIN_ATLAS.tsv").open(newline="") as handle:
        chains = list(csv.DictReader(handle, delimiter="\t"))
    checks["pair_atlas"] = len(pairs) == 10000 and len({row["pair_id"] for row in pairs}) == 10000
    checks["chain_atlas"] = len(chains) == 10518 and len({row["chain_id"] for row in chains}) == 10518
    checks["atlas_composition"] = all(
        row["transition_composes"] == "1"
        and row["Gram_increments_add"] == "1"
        and row["reciprocal_character_composes"] == "1"
        and row["nontrivial_directed_loop"] == "0"
        for row in chains
    )

    assert all(checks.values()), checks
    result = {
        "status": "PASS",
        "scope": "administrative and saved-artifact consistency; not independent derivation",
        "checks": checks,
    }
    (ROOT / "PACKAGE_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
