#!/usr/bin/env python3
"""Build a fresh or repair-only sealed G213 intake from exact frozen sources."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


parser = argparse.ArgumentParser()
parser.add_argument("--repair-followup", action="store_true")
args = parser.parse_args()


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
prefix = "udt_g213_repair_followup_" if args.repair_followup else "udt_g213_review_"
DEST = Path(tempfile.mkdtemp(prefix=prefix, dir="/tmp"))
PACKAGE_DEST = DEST / PACKAGE.name
PACKAGE_DEST.mkdir()

package_files = sorted(path for path in PACKAGE.iterdir() if path.is_file())
for source in package_files:
    shutil.copy2(source, PACKAGE_DEST / source.name)

source_rows = []
for line in (PACKAGE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
    expected, relative = line.split("\t", 1)
    source = ROOT / relative
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    if actual != expected:
        raise AssertionError(f"source hash mismatch: {relative}")
    target = DEST / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    source_rows.append(relative)

scope = {
    "audit": "G213",
    "purpose": (
        "repair-only follow-up of dependency-free replay and independent mode-rank coverage"
        if args.repair_followup
        else "fresh read-only adversarial review of the local spatial-mode census and completed-pair rank bridge"
    ),
    "review_mode": "repair_only_followup" if args.repair_followup else "fresh_adversarial",
    "package": PACKAGE.name,
    "package_file_count": len(package_files),
    "frozen_source_count": len(source_rows),
    "allowed_actions": ["inspect intake", "run bounded read-only checks", "run registered no-write replay"],
    "forbidden_actions": ["edit evidence", "continue research", "access repository outside intake"],
    "scientific_ceiling": "local conditional decomposition and metric-information reconstruction only",
}
if args.repair_followup:
    scope["required_verifications"] = [
        "production and hostile scripts import no third-party module",
        "registered no-write replay passes in sealed standard-library Python",
        "independent mode ranks are five four five",
        "ten-thousand-case completed-tuple and density-blind replay remains exact",
        "bounded scientific landing and supplied-premise caveats remain unchanged",
    ]
    scope["forbidden_actions"].append("change or extend scientific landing")
(DEST / "REVIEW_SCOPE.json").write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

manifest_rows = []
for path in sorted(item for item in DEST.rglob("*") if item.is_file() and item.name != "REVIEW_MANIFEST.tsv"):
    manifest_rows.append((hashlib.sha256(path.read_bytes()).hexdigest(), path.relative_to(DEST).as_posix()))
manifest = "sha256\tpath\n" + "".join(f"{digest}\t{relative}\n" for digest, relative in manifest_rows)
(DEST / "REVIEW_MANIFEST.tsv").write_text(manifest)

for path in DEST.rglob("*"):
    if path.is_file():
        path.chmod(0o444)
for path in sorted((item for item in DEST.rglob("*") if item.is_dir()), reverse=True):
    path.chmod(0o555)
DEST.chmod(0o555)

print(json.dumps({
    "status": "PASS",
    "intake": str(DEST),
    "file_count": len(manifest_rows) + 1,
    "manifest_sha256": hashlib.sha256((DEST / "REVIEW_MANIFEST.tsv").read_bytes()).hexdigest(),
    "scope_sha256": hashlib.sha256((DEST / "REVIEW_SCOPE.json").read_bytes()).hexdigest(),
    "package_files": len(package_files),
    "frozen_sources": len(source_rows),
}, sort_keys=True))
