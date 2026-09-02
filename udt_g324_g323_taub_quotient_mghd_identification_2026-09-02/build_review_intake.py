#!/usr/bin/env python3
"""Build a sealed, self-contained G324 fresh-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE_NAME = "udt_g324_g323_taub_quotient_mghd_identification_2026-09-02"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    package = Path(__file__).resolve().parent
    repo = package.parent
    intake = Path(tempfile.mkdtemp(prefix="udt_g324_review_", dir="/tmp"))
    package_out = intake / "package"
    sources_out = intake / "sources"

    ignored = {
        "EXTERNAL_REVIEW_RESPONSE.md",
        "EXTERNAL_REVIEW_TRANSCRIPT.txt",
        "EXTERNAL_REVIEW_TRANSMISSION.md",
        "PACKAGE_VERIFICATION_RESULT.json",
    }
    package_out.mkdir()
    for path in sorted(package.iterdir()):
        if path.is_file() and path.name not in ignored:
            shutil.copy2(path, package_out / path.name)

    with (package / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        source = repo / row["relative_path"]
        assert source.is_file()
        assert sha(source) == row["sha256"]
        destination = sources_out / row["relative_path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    scope = {
        "schema": "udt-g324-fresh-review-scope-v1",
        "question": "G323 explicit Taub quotient equality with its smooth per-datum G322 MGHD",
        "review_type": "fresh_read_only_adversarial",
        "allowed": [
            "inspect only this sealed intake",
            "run registered checks in a writable ephemeral copy",
            "independently rederive the bounded mathematical result"
        ],
        "forbidden": [
            "edit evidence files",
            "continue the research",
            "access the repository or protected packages",
            "use internet or unsealed observations",
            "select or canonize a law, history, topology, occupancy, scale, or X_max"
        ]
    }
    (intake / "REVIEW_SCOPE.json").write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

    # Confirm the copied package replays against only the copied sources.
    import subprocess
    import sys
    subprocess.run(
        [sys.executable, "-S", str(package_out / "verify_package.py"),
         "--source-root", str(sources_out)],
        cwd=package_out,
        check=True,
        capture_output=True,
        text=True,
    )

    manifest = intake / "REVIEW_MANIFEST.tsv"
    payloads = sorted(
        path for path in intake.rglob("*")
        if path.is_file() and path.name not in {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}
    )
    lines = ["sha256\tbytes\trelative_path"]
    for path in payloads:
        lines.append(f"{sha(path)}\t{path.stat().st_size}\t{path.relative_to(intake)}")
    manifest.write_text("\n".join(lines) + "\n")
    manifest_hash = sha(manifest)
    seal = intake / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{manifest_hash}  REVIEW_MANIFEST.tsv\n")

    # Final no-write seal replay.
    subprocess.run(
        [sys.executable, "-S", str(package_out / "verify_review_intake.py")],
        cwd=package_out,
        check=True,
        capture_output=True,
        text=True,
    )

    result = {
        "intake": str(intake),
        "payload_count": len(payloads),
        "total_file_count": len(payloads) + 2,
        "review_scope_sha256": sha(intake / "REVIEW_SCOPE.json"),
        "review_manifest_sha256": manifest_hash,
        "detached_seal_sha256": sha(seal),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
