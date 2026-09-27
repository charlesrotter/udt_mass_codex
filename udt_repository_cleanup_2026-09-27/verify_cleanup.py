"""Publication integrity for this cleanup, not validation of underlying science."""
import csv
import hashlib
import json
import stat
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKET = Path(__file__).resolve().parent
PREFIX = PACKET.relative_to(ROOT).as_posix() + "/"
ARCHIVE = "archive/remaining_working_surfaces_2026-09-27/"
MAINTAINED = {"README.md", "INDEX.md", "LIVE.md", "HANDOFF.md", "research/_registry/README.md"}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def table(path):
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run():
    baseline = json.loads((PACKET / "BASELINE.json").read_text())
    commit = baseline["HEAD"]
    frozen = {}
    for item in git("ls-tree", "-r", "-l", "-z", commit).decode().split("\0"):
        if item:
            meta, name = item.split("\t", 1)
            mode, kind, oid, size = meta.split()
            frozen[name] = (mode, oid, size)
    rows = table(PACKET / "inventory/TRACKED_DISPOSITIONS.tsv")
    assert len(rows) == len(frozen) == 33380, "inventory cardinality"
    assert {r["path"] for r in rows} == set(frozen), "inventory membership"
    for row in rows:
        assert (row["mode"], row["object_id"], row["bytes"]) == frozen[row["path"]], "immutable metadata"
    archived = table(PACKET / "archive/ARCHIVE_MANIFEST.tsv")
    archive_by_name = {r["source"]: r for r in archived}
    inventory_by_name = {r["path"]: r for r in rows}
    assert archived and len(archive_by_name) == len(archived), "archive empty/duplicate"
    assert {r["path"] for r in rows if r["disposition"] == "ARCHIVE_REVIEWED"} == set(archive_by_name), "archive/inventory mismatch"
    destinations = set()
    for row in archived:
        name, destination = row["source"], row["destination"]
        assert "/" not in name and name in frozen, "archive scope"
        assert destination == ARCHIVE + name and destination not in destinations, "archive destination"
        destinations.add(destination)
        assert inventory_by_name[name]["destination"] == destination, "inventory destination mismatch"
        assert row["source_commit"] == commit, "archive commit"
        original = git("show", commit + ":" + name)
        destination_mode = (ROOT / destination).lstat().st_mode
        assert stat.S_ISREG(destination_mode) and stat.S_IMODE(destination_mode) in (0o644, 0o664), "archive file type/mode"
        assert frozen[name][0] == "100644", "archive baseline Git mode"
        current = (ROOT / destination).read_bytes()
        assert current == original, "archive content"
        assert not (ROOT / name).exists() and not (ROOT / name).is_symlink(), "root duplicate remains"
        assert hashlib.sha256(current).hexdigest() == row["sha256"], "archive hash"
        assert len(current) == int(row["bytes"]), "archive size"
        assert frozen[name][1] == row["source_blob_oid"], "archive blob"
    for row in rows:
        if row["path"] not in archive_by_name:
            assert row["destination"] == row["path"], "retained path changed"
    packet_bytes = sum(p.stat().st_size for p in PACKET.rglob("*") if p.is_file())
    assert packet_bytes < 50 * 1024 * 1024, "maintenance packet exceeds 50MiB"
    unchanged = ["AGENTS.md", "CLAUDE.md", "CANON.md", "founding.md",
                 "CURRENT_SCIENTIFIC_PREMISES.tsv", "CURRENT_SCIENTIFIC_PREMISES.md",
                 "CURRENT_RESEARCH_PROGRAM.md", "UDT_METRIC_KERNEL_DEVELOPMENT.md",
                 "research/_registry/CURRENT_ARTIFACT_PATHS.tsv",
                 "verify_current_scientific_premises.py", "tests/test_startup_surface.py"]
    for name in unchanged:
        assert (ROOT / name).read_bytes() == git("show", commit + ":" + name), "changed fixed source: " + name
    allowed = set(archive_by_name) | MAINTAINED
    changed = git("diff", "--name-only", "--no-renames", commit).decode().splitlines()
    assert all(n in allowed or n.startswith((PREFIX, ARCHIVE)) for n in changed), "unexpected tracked edit"
    status = git("status", "--short", "--untracked-files=all").decode().splitlines()
    outside = [line for line in status if line[3:].strip('"') not in allowed
               and not line[3:].strip('"').startswith((PREFIX, ARCHIVE))]
    assert outside == baseline["preexisting_status_lines"], "outside status changed"
    assert len(outside) == 52
    assert git("branch", "--show-current").decode().strip() == "grok"
    return dict(status="PASS", baseline=commit, tracked_paths=len(rows),
                archived_files=len(archived), archive_bytes=sum(int(r["bytes"]) for r in archived),
                packet_bytes_at_check=packet_bytes,
                unchanged_sources=unchanged, outside_status_entries=len(outside),
                scope="Exact inventory/blob/byte/status correspondence; protected content unread; no scientific proof or full dynamic dependency claim.")


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
