#!/usr/bin/env python3
"""Build a sealed read-only G297 external-review intake under /tmp."""

from hashlib import sha256
import json
from pathlib import Path
import shutil
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g297_review_", dir="/tmp"))

    excluded = {"__pycache__"}
    package_files = sorted(
        path for path in HERE.rglob("*") if path.is_file() and not any(part in excluded for part in path.parts)
    )
    for source in package_files:
        relative = source.relative_to(ROOT)
        target = intake / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    for raw in (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        expected, relative_text = raw.split("\t", 1)
        source = ROOT / relative_text
        if digest(source) != expected:
            raise AssertionError(f"source changed before sealing: {relative_text}")
        target = intake / relative_text
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    scope = {
        "package": HERE.name,
        "purpose": "fresh read-only adversarial review of repaired G297 bounded landing",
        "allowed": [
            "inspect only this intake",
            "run registered checks in a writable ephemeral copy",
            "report defects and bounded verdict",
        ],
        "forbidden": [
            "edit evidence files",
            "continue the research",
            "access repository or protected packages outside intake",
            "import observations fits sources matter actions field equations scales or X_max",
            "promote candidate clarification into canon",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")

    payloads = sorted(
        path for path in intake.rglob("*") if path.is_file() and path.name not in {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}
    )
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    lines = ["sha256\tbytes\tpath"]
    for path in payloads:
        lines.append(f"{digest(path)}\t{path.stat().st_size}\t{path.relative_to(intake)}")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    seal_path = intake / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{digest(manifest_path)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")

    for path in intake.rglob("*"):
        if path.is_file():
            path.chmod(0o444)
    output = {
        "intake": str(intake),
        "payload_count": len(payloads),
        "total_file_count": len(payloads) + 2,
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest_path),
        "seal_sha256": digest(seal_path),
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
