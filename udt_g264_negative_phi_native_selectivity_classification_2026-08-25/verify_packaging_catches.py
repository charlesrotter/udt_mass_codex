#!/usr/bin/env python3
"""Fail-closed altered-copy checks for the self-contained G264 replay layout."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


PACKAGE_NAME = "udt_g264_negative_phi_native_selectivity_classification_2026-08-25"


def run_verifier(root: Path) -> subprocess.CompletedProcess[str]:
    package = root / PACKAGE_NAME
    return subprocess.run(
        ["python3", str(package / "verify_package.py")],
        cwd=package,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def first_source(package: Path) -> Path:
    with (package / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        row = next(csv.DictReader(handle, delimiter="\t"))
    return package.parent / row["path"]


def mutate_and_expect_failure(replay_root: Path, mutation: str) -> bool:
    with tempfile.TemporaryDirectory(prefix=f"g264_packaging_{mutation}_") as temporary:
        candidate = Path(temporary) / "replay_root"
        shutil.copytree(replay_root, candidate)
        package = candidate / PACKAGE_NAME
        source = first_source(package)
        if mutation == "source_manifest_missing":
            (package / "SOURCE_MANIFEST.tsv").unlink()
        elif mutation == "frozen_source_altered":
            source.write_bytes(source.read_bytes() + b"\n# altered-copy catch\n")
        elif mutation == "frozen_source_missing":
            source.unlink()
        else:
            raise ValueError(mutation)
        return run_verifier(candidate).returncode != 0


def verify(replay_root: Path) -> dict[str, object]:
    replay_root = replay_root.resolve()
    package = replay_root / PACKAGE_NAME
    if not package.is_dir():
        raise AssertionError(f"missing replay package: {package}")
    baseline = run_verifier(replay_root)
    if baseline.returncode != 0:
        raise AssertionError(
            "baseline sealed replay failed:\n" + baseline.stdout + baseline.stderr
        )
    mutations = {
        name: mutate_and_expect_failure(replay_root, name)
        for name in (
            "source_manifest_missing",
            "frozen_source_altered",
            "frozen_source_missing",
        )
    }
    if not all(mutations.values()):
        raise AssertionError(
            f"uncaught packaging mutations: {[name for name, caught in mutations.items() if not caught]}"
        )
    package_result = json.loads(baseline.stdout)
    return {
        "status": "PASS",
        "baseline_package_status": package_result["status"],
        "baseline_landing": package_result["landing"],
        "mutation_count": len(mutations),
        "caught_count": sum(mutations.values()),
        "mutations": mutations,
        "qualification": "sealed_replay_packaging_regression_not_scientific_proof",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replay-root", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.replay_root)
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()

