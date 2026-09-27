"""Bounded archive/source/worktree correspondence; not scientific certification."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PACKET = Path(__file__).resolve().parent
PREFIX = PACKET.relative_to(ROOT).as_posix() + "/"
ARCHIVE = "archive/stale_working_documents_2026-09-27/"
MAINTAINED = {
    "LIVE.md", "HANDOFF.md", "INDEX.md", "MEMORY.md",
    "CURRENT_RESEARCH_PROGRAM.md", "UDT_RESEARCH_ROADMAP.md",
    "udt_native_theory_research_plan_2026-09-13/PLAN.md",
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run():
    baseline = json.loads((PACKET / "BASELINE.json").read_text())
    commit = baseline["HEAD"]
    rows = list(csv.DictReader((PACKET / "archive/ARCHIVE_MANIFEST.tsv").open(), delimiter="\t"))
    assert len(rows) == 7 and len({r["source"] for r in rows}) == 7
    details = []
    for row in rows:
        assert row["source_commit"] == commit, "archive source commit mismatch"
        original = git("show", commit + ":" + row["source"])
        destination = ROOT / row["proposed_destination"]
        assert row["proposed_destination"] == ARCHIVE + row["source"]
        assert not (ROOT / row["source"]).exists(), row["source"]
        actual = destination.read_bytes()
        assert actual == original
        assert sha(actual) == row["sha256"] and len(actual) == int(row["bytes"])
        assert git("rev-parse", commit + ":" + row["source"]).decode().strip() == row["source_blob_oid"]
        details.append({"source": row["source"], "destination": row["proposed_destination"],
                        "bytes": len(actual), "sha256": sha(actual)})

    # Guard-owned science and the older fixed relocation registry are unchanged.
    unchanged = ["CANON.md", "CURRENT_SCIENTIFIC_PREMISES.tsv", "founding.md",
                 "research/_registry/CURRENT_ARTIFACT_PATHS.tsv",
                 "verify_current_scientific_premises.py", "tests/test_startup_surface.py"]
    for name in unchanged:
        assert (ROOT / name).read_bytes() == git("show", commit + ":" + name), name
    source_pins = list(csv.DictReader((PACKET / "review/science/SOURCE_PINS.tsv").open(), delimiter="\t"))
    assert len(source_pins) == 41, "source pin count mismatch"
    assert len({pin["path"] for pin in source_pins}) == 41, "duplicate source pin path"
    for pin in source_pins:
        data = (ROOT / pin["path"]).read_bytes()
        assert sha(data) == pin["sha256"] and len(data) == int(pin["bytes"]), pin["path"]
    assert len((ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes().splitlines()) == 407

    changed = git("diff", "--name-only", commit, "--").decode().splitlines()
    allowed = MAINTAINED | {r["source"] for r in rows}
    assert all(p in allowed or p.startswith((PREFIX, ARCHIVE)) for p in changed), changed
    status = git("status", "--short", "--untracked-files=all").decode().splitlines()
    # Status metadata only: never read/hash protected or unrelated local payloads.
    outside = [line for line in status if line[3:].strip('"') not in allowed
               and not line[3:].strip('"').startswith((PREFIX, ARCHIVE))]
    assert outside == baseline["preexisting_status_lines"], "outside status changed"
    assert len(outside) == 52
    assert git("branch", "--show-current").decode().strip() == "grok"
    assert (PACKET / "initial_candidate/ATTACHMENT_CANDIDATE.md").is_file()
    freeze = json.loads((PACKET / "initial_candidate/FREEZE.json").read_text())
    assert sha((ROOT / freeze["frozen_path"]).read_bytes()) == freeze["sha256"]

    archive_readme = (ROOT / ARCHIVE / "README.md").read_text()
    assert "ARCHIVE_MANIFEST.tsv" in archive_readme
    assert ARCHIVE + "README.md" in (ROOT / "INDEX.md").read_text()
    for name in ("RESTART_CHECKPOINT.md", "maintenance_agent_capacity_2026-09-10.md"):
        assert ARCHIVE + name in (ROOT / "HANDOFF.md").read_text()
    return {"status": "PASS", "kind": "integrity and status metadata, not scientific proof",
            "baseline": commit, "archive_files": details,
            "archive_bytes": sum(r["bytes"] for r in details),
            "unchanged_sources": unchanged, "reviewer_source_pins_checked": len(source_pins),
            "registry_rows": 406, "outside_status_entries": len(outside),
            "tracked_changes": changed,
            "limitations": "No protected/untracked payload hashes; no exhaustive reference graph or old scientific campaign replay."}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
