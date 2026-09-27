#!/usr/bin/env python3
"""Direct archive audit using Git blob IDs, independent of construction/checker code."""
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "final"
PACKET = ROOT / "udt_repository_cleanup_2026-09-27"
BASE = "8aac11e13a2311347771e11f507f4f2042ea02a2"
PREFIX = "archive/remaining_working_surfaces_2026-09-27/"
MAINTAINED = {"README.md", "INDEX.md", "LIVE.md", "HANDOFF.md", "research/_registry/README.md"}

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)

def tsv(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))

def main():
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    assert git("branch", "--show-current").decode().strip() == "grok"
    manifest = tsv(PACKET / "archive/ARCHIVE_MANIFEST.tsv")
    inventory = {row["path"]: row for row in tsv(PACKET / "inventory/TRACKED_DISPOSITIONS.tsv")}
    cleared = {row["path"] for row in tsv(OUT.parent / "DEPENDENCY_CLASSIFICATION.tsv")
               if row["dependency_disposition"] == "DEPENDENCY_CLEAR_FOR_REVIEWED_ARCHIVE"}
    sources = [row["source"] for row in manifest]
    assert len(sources) == len(set(sources)) == 34
    assert set(sources) == cleared
    observed = []
    for row in manifest:
        source, target = row["source"], row["destination"]
        assert row["source_commit"] == BASE
        assert target == PREFIX + source == inventory[source]["destination"]
        old = ROOT / source
        assert not old.exists() and not old.is_symlink()
        dest = ROOT / target
        metadata = dest.lstat()
        assert stat.S_ISREG(metadata.st_mode) and not dest.is_symlink()
        assert stat.S_IMODE(metadata.st_mode) in {0o644, 0o664}
        oid = git("rev-parse", BASE + ":" + source).decode().strip()
        original = git("cat-file", "blob", oid)
        current = dest.read_bytes()
        assert current == original
        independently_derived_oid = hashlib.sha1(b"blob " + str(len(current)).encode() + b"\0" + current).hexdigest()
        assert independently_derived_oid == oid == row["source_blob_oid"] == inventory[source]["object_id"]
        assert inventory[source]["mode"] == "100644"
        assert str(len(current)) == row["bytes"] == inventory[source]["bytes"]
        assert hashlib.sha256(current).hexdigest() == row["sha256"]
        assert oct(stat.S_IMODE(metadata.st_mode)) == row["filesystem_mode"]
        observed.append({"source": source, "destination": target, "git_blob_oid": oid,
                         "sha256": row["sha256"], "bytes": len(current),
                         "mode": row["filesystem_mode"], "regular_non_symlink": True})
    changed = {}
    for line in git("diff", "--name-status", "--no-renames", BASE).decode().splitlines():
        marker, path = line.split("\t", 1)
        changed[path] = marker
    assert changed == {**{source: "D" for source in sources}, **{path: "M" for path in MAINTAINED}}
    preserved = ["AGENTS.md", "CLAUDE.md", "CANON.md", "founding.md",
                 "CURRENT_SCIENTIFIC_PREMISES.tsv", "CURRENT_SCIENTIFIC_PREMISES.md",
                 "CURRENT_RESEARCH_PROGRAM.md", "UDT_METRIC_KERNEL_DEVELOPMENT.md",
                 "UDT_METRIC_KERNEL_COVERAGE.tsv", "research/_registry/CURRENT_ARTIFACT_PATHS.tsv",
                 "verify_current_scientific_premises.py", "tests/test_startup_surface.py",
                 "CODEX_STARTUP_REHEARSAL_2026-07-17.md", "codex_rehearsal_final.md", "codex_rehearsal_transcript.txt"]
    preserved_metadata = []
    for source in preserved:
        oid = git("rev-parse", BASE + ":" + source).decode().strip()
        data = (ROOT / source).read_bytes()
        assert data == git("cat-file", "blob", oid)
        preserved_metadata.append({"path": source, "git_blob_oid": oid, "sha256": hashlib.sha256(data).hexdigest()})
    baseline = json.loads((PACKET / "BASELINE.json").read_text())
    statuses = git("status", "--short", "--untracked-files=all").decode().splitlines()
    other = []
    for line in statuses:
        path = line[3:].strip('"')
        if path in sources or path in MAINTAINED or path.startswith((PREFIX, PACKET.name + "/")):
            continue
        other.append(line)
    assert other == baseline["preexisting_status_lines"] and len(other) == 52
    navigation = sorted(MAINTAINED | {
        PACKET.name + "/README.md", PACKET.name + "/REPOSITORY_MAP.md",
        PREFIX + "README.md",
    })
    links = []
    for source in navigation:
        source_path = ROOT / source
        text = source_path.read_text()
        for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if raw.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = unquote(raw.strip("<>").split("#", 1)[0])
            resolved = source_path.parent / target
            assert resolved.exists(), f"missing maintained link: {source}: {raw}"
            links.append({"source": source, "target": raw})
    archive_navigation = (ROOT / PREFIX / "README.md").read_text()
    assert all("](" + source + ")" in archive_navigation for source in sources)
    assert "manuscript bytes nor coverage" in archive_navigation
    result = {"status": "PASS", "baseline": BASE, "archive_files": len(observed),
              "archive_bytes": sum(row["bytes"] for row in observed),
              "archive_file_modes": dict(collections.Counter(row["mode"] for row in observed)),
              "files": observed, "preserved_sources": preserved_metadata,
              "changed_tracked_paths": changed, "unchanged_untracked_status_entries": len(other),
              "maintained_markdown_links": links,
              "limits": "Direct selected-byte/type/path checks and maintained-link resolution. No scientific tests; historical relative references inside original bytes remain explicitly historical and resolve through archive map or baseline Git tree."}
    (OUT / "DIRECT_CONSTRUCTION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in ["status", "baseline", "archive_files", "archive_bytes", "archive_file_modes", "unchanged_untracked_status_entries"]}, indent=2))

if __name__ == "__main__":
    main()
