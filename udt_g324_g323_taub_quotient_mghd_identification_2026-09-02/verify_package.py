#!/usr/bin/env python3
"""Aggregate, replay, and source-containment verifier for G324."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


LANDING = (
    "EXPLICIT_TAUB_QUOTIENTS_ARE_SMOOTH_MGHDS__"
    "REGISTERED_LATTICE_MODULUS_SURVIVES"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_source_root(package: Path, supplied: str | None) -> Path:
    if supplied:
        return Path(supplied).resolve()
    direct = package.parent
    name = "udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01"
    if (direct / name).is_dir():
        return direct
    return direct / "sources"


def load(path: Path):
    return json.loads(path.read_text())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    package = Path(__file__).resolve().parent
    source_root = resolve_source_root(package, args.source_root)
    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    production = load(package / "DERIVATION_RESULT.json")
    independent = load(package / "INDEPENDENT_VERIFICATION.json")
    hostile = load(package / "CATCH_PROOF_RESULT.json")
    gate(production["landing"] == LANDING, "production_landing")
    gate(production["assertion_count"] == 29, "production_assertion_count")
    gate(independent["assertion_count"] == 32, "independent_assertion_count")
    gate(hostile["assertion_count"] == 5, "hostile_assertion_count")
    gate(production["explicit_quotient_equals_smooth_per_datum_MGHD"], "mghd_positive")
    gate(production["registered_lattice_modulus_survives_MGHD"], "modulus_positive")
    gate(production["proper_time_oriented_C2_extension_excluded"], "c2_extension_excluded")
    gate(not production["C0_past_inextendibility_proved"], "c0_past_not_overclaimed")
    gate(not production["physical_occupancy_selected"], "occupancy_not_selected")
    gate(not production["physical_scale_selected"], "scale_not_selected")
    gate(not production["Xmax_selected"], "xmax_not_selected")
    gate(not production["metric_changed"] and not production["kernel_changed"],
         "metric_kernel_unchanged")
    gate(independent["production_imported"] is False, "independent_no_production_import")
    gate(independent["production_result_read"] is False, "independent_no_result_read")
    gate(independent["kretschmann"] == {"R^-6*mu^2": "12"}, "independent_kretschmann")
    gate(all(hostile["controls"].values()), "all_hostile_controls")

    independent_text = (package / "verify_independent.py").read_text()
    gate("import derive_taub_mghd" not in independent_text, "static_no_production_import")
    gate("DERIVATION_RESULT.json" not in independent_text, "static_no_production_result_read")

    source = load(package / "GLS_PRIMARY_SOURCE_EVIDENCE.json")
    quoted = source["hypotheses_fragment"].split() + source["endpoint_fragment"].split()
    gate(len(quoted) == source["bounded_excerpt_word_count"] == 23, "source_quote_count_exact")
    gate(source["arxiv"] == "1704.00353v4", "source_primary_identifier")
    gate(source["theorem_label"] == "Theorem 2", "source_theorem_label")
    gate(source["primary_pdf_sha256"] ==
         "069c6f4bcb1c1569ec8546f8579250c6128f1f3fa893516bb3a147a1570cf92a",
         "source_pdf_hash")

    with (package / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    gate(len(rows) == 12, "source_manifest_count")
    for row in rows:
        path = source_root / row["relative_path"]
        gate(path.is_file(), f"source_exists:{row['relative_path']}")
        gate(digest(path) == row["sha256"], f"source_hash:{row['relative_path']}")

    exact = (package / "EXACT_DERIVATION.md").read_text()
    lay = (package / "LAY_REPORT.md").read_text()
    status = (package / "STATUS_LEDGER.tsv").read_text()
    premise = (package / "PREMISE_LEDGER.tsv").read_text()
    gate(LANDING in exact, "exact_landing_token")
    gate("does **not** prove that the\npast singular end is `C0`-inextendible" in exact,
         "exact_c0_boundary")
    gate("choose which compact shape Nature uses" in lay, "lay_occupancy_boundary")
    gate("PASS_PENDING_REPAIR_ONLY_EXTERNAL_FOLLOWUP" in status,
         "status_repair_followup_pending")
    gate("IMPORTED_MATHEMATICAL_METHOD" in premise, "premise_import_typed")

    # Reproduce the first three registered commands literally in a fresh package copy. The current
    # verifier invocation is itself the fourth registered command, so it must not recurse.
    with tempfile.TemporaryDirectory(prefix="udt_g324_replay_") as temp:
        temp_path = Path(temp)
        replay_package = temp_path / "package"
        replay_sources = temp_path / "sources"
        shutil.copytree(package, replay_package, ignore=shutil.ignore_patterns(".review_runtime"))
        for row in rows:
            source_path = source_root / row["relative_path"]
            target = replay_sources / row["relative_path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target)
        replay_lines = [
            line.strip() for line in (package / "REPLAY_COMMANDS.txt").read_text().splitlines()
            if line.strip()
        ]
        gate(len(replay_lines) == 4, "registered_command_count")
        expected_outputs = (
            "DERIVATION_RESULT.json",
            "INDEPENDENT_VERIFICATION.json",
            "CATCH_PROOF_RESULT.json",
        )
        for line, output in zip(replay_lines[:3], expected_outputs):
            completed = subprocess.run(
                shlex.split(line), cwd=replay_package, check=True, capture_output=True, text=True
            )
            gate(completed.returncode == 0, f"literal_replay_exit:{line}")
            generated = replay_package / ".review_runtime" / output
            gate(generated.is_file(), f"literal_replay_output:{output}")
            gate(load(generated) == load(package / output), f"literal_replay_exact:{output}")
        gate(replay_lines[3] == "python3 -S verify_package.py", "current_invocation_is_command_4")

    result = {
        "schema": "udt-g324-package-verification-v1",
        "status": "PASS_PENDING_REPAIR_ONLY_EXTERNAL_FOLLOWUP",
        "landing": LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "python_version": sys.version,
        "registered_source_count": len(rows),
        "replay_exact": True,
        "evidence_directory_unchanged_by_replay": True,
    }
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
