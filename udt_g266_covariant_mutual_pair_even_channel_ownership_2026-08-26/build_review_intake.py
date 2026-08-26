#!/usr/bin/env python3
"""Build a sealed G266 review intake under /tmp."""

import hashlib
import json
import pathlib
import shutil
import tempfile


ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    out = pathlib.Path(tempfile.mkdtemp(prefix="udt_g266_review_", dir="/tmp"))
    package_out = out / ROOT.name
    package_out.mkdir()
    for source in sorted(ROOT.iterdir()):
        if source.is_file() and source.name != "build_review_intake.py":
            shutil.copy2(source, package_out / source.name)

    source_rows = (ROOT / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]
    private = out / "private_sources"
    for row in source_rows:
        rel, expected, _role = row.split("\t")
        source = REPO / rel
        assert source.is_file() and sha256(source) == expected
        target = private / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    scope = {
        "task": "fresh read-only adversarial review of bounded G266 scientific landing",
        "allowed": [
            ROOT.name + "/",
            "private_sources/ paths listed by SOURCE_MANIFEST.tsv",
        ],
        "forbidden": [
            "editing evidence",
            "continuing the research",
            "repository access outside the intake",
            "protected packages",
            "observational outcomes",
        ],
    }
    (out / "REVIEW_SCOPE.json").write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

    payloads = sorted(
        path for path in out.rglob("*")
        if path.is_file() and path.name != "REVIEW_MANIFEST.tsv"
    )
    manifest = ["path\tsha256\tbytes"]
    for path in payloads:
        manifest.append(f"{path.relative_to(out)}\t{sha256(path)}\t{path.stat().st_size}")
    (out / "REVIEW_MANIFEST.tsv").write_text("\n".join(manifest) + "\n")
    all_files = sorted(path for path in out.rglob("*") if path.is_file())
    print(json.dumps({
        "intake": str(out),
        "file_count": len(all_files),
        "payload_count": len(payloads),
        "scope_sha256": sha256(out / "REVIEW_SCOPE.json"),
        "manifest_sha256": sha256(out / "REVIEW_MANIFEST.tsv"),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
