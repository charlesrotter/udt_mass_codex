#!/usr/bin/env python3
"""Exercise the G306 standard-library replay in both allowed source layouts."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "PORTABILITY_VERIFICATION_RESULT.json"
PACKAGE = HERE.name
COMMANDS = (
    "derive_intrinsic_hopf_section.py",
    "verify_intrinsic_hopf_section_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def current_source(rel: Path) -> Path:
    matches = [
        path for path in (ROOT / rel, ROOT / "frozen_sources" / rel)
        if path.is_file()
    ]
    assert len(matches) == 1, (rel, matches)
    return matches[0]


def run(command, cwd: Path, expect_success: bool = True):
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    if expect_success:
        assert completed.returncode == 0, (command, completed.stdout, completed.stderr)
    else:
        assert completed.returncode != 0, command
    return completed


def main() -> None:
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(source_rows) == 15

    expected_derivation = digest(HERE / "DERIVATION_RESULT.json")
    expected_census = digest(HERE / "CANDIDATE_CENSUS.tsv")
    records = []

    with tempfile.TemporaryDirectory(prefix="g306_portability_") as temporary:
        sealed_root = Path(temporary)
        sealed_package = sealed_root / PACKAGE
        shutil.copytree(HERE, sealed_package)
        for row in source_rows:
            rel = Path(row["path"])
            source = current_source(rel)
            assert digest(source) == row["sha256"], rel
            destination = sealed_root / "frozen_sources" / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        for script in COMMANDS:
            completed = run([sys.executable, "-S", str(sealed_package / script)], sealed_root)
            records.append({"script": script, "returncode": completed.returncode})

        assert digest(sealed_package / "DERIVATION_RESULT.json") == expected_derivation
        assert digest(sealed_package / "CANDIDATE_CENSUS.tsv") == expected_census

        # Missing source must fail package verification.
        first_rel = Path(source_rows[0]["path"])
        frozen_first = sealed_root / "frozen_sources" / first_rel
        saved = frozen_first.read_bytes()
        frozen_first.unlink()
        missing = run(
            [sys.executable, "-S", str(sealed_package / "verify_package.py")],
            sealed_root,
            expect_success=False,
        )
        assert "source resolution must be unique" in missing.stderr
        frozen_first.parent.mkdir(parents=True, exist_ok=True)
        frozen_first.write_bytes(saved)

        # The same source in both allowed layouts must fail as ambiguous.
        direct_first = sealed_root / first_rel
        direct_first.parent.mkdir(parents=True, exist_ok=True)
        direct_first.write_bytes(saved)
        ambiguous = run(
            [sys.executable, "-S", str(sealed_package / "verify_package.py")],
            sealed_root,
            expect_success=False,
        )
        assert "source resolution must be unique" in ambiguous.stderr

    result = {
        "status": "PASS",
        "implementation": "standard_library_subprocess_and_fresh_temp_layout",
        "sealed_commands": records,
        "sealed_command_count": len(records),
        "source_hashes": len(source_rows),
        "missing_source_rejected": True,
        "ambiguous_source_rejected": True,
        "production_derivation_byte_identical": True,
        "candidate_census_byte_identical": True,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
