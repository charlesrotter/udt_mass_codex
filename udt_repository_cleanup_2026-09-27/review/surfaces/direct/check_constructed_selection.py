#!/usr/bin/env python3
"""Bounded independent metadata/byte/routing review; no scientific execution."""
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
BASE = "8aac11e13a2311347771e11f507f4f2042ea02a2"
PACKET = ROOT / "udt_repository_cleanup_2026-09-27"
SURFACES = PACKET / "review/surfaces"


def rows(path):
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def base_bytes(path):
    return git("show", f"{BASE}:{path}")


def main():
    initial = rows(SURFACES / "SURFACE_CLASSIFICATION.tsv")
    supplemental = rows(SURFACES / "supplemental_transfer/SUPPLEMENTAL_CLASSIFICATION.tsv")
    effective = {row["path"]: row for row in initial}
    effective.update({row["path"]: row for row in supplemental})
    eligible = {name for name, row in effective.items() if row["disposition"] == "ARCHIVE_ELIGIBLE"}
    manifest = rows(PACKET / "archive/ARCHIVE_MANIFEST.tsv")
    assert len(effective) == 90
    assert len(eligible) == 34
    assert len(manifest) == 34
    assert {row["source"] for row in manifest} == eligible
    assert all(effective[name]["actual_read_depth"] == "FULL_PROSE" for name in eligible)
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    assert git("branch", "--show-current").decode().strip() == "grok"

    per_file = []
    for row in manifest:
        source, target = row["source"], row["destination"]
        assert row["source_commit"] == BASE
        assert not os.path.lexists(ROOT / source), source
        destination = ROOT / target
        metadata = destination.lstat()
        assert stat.S_ISREG(metadata.st_mode), target
        preserved = destination.read_bytes()
        original = base_bytes(source)
        assert preserved == original, target
        digest = hashlib.sha256(original).hexdigest()
        assert digest == row["sha256"] == effective[source]["baseline_sha256"], source
        assert len(original) == int(row["bytes"]), source
        assert git("rev-parse", f"{BASE}:{source}").decode().strip() == row["source_blob_oid"], source
        assert oct(stat.S_IMODE(metadata.st_mode)) == row["filesystem_mode"], source
        per_file.append({"source": source, "destination": target, "bytes": len(original),
                         "sha256": digest, "mode": oct(stat.S_IMODE(metadata.st_mode)), "pass": True})
    assert sum(row["bytes"] for row in per_file) == 223085

    retained = set(effective) - eligible
    for name in retained:
        assert (ROOT / name).is_file(), name
        if name != "README.md":
            assert (ROOT / name).read_bytes() == base_bytes(name), name

    fixed_and_controls = [
        "CODEX_STARTUP_REHEARSAL_2026-07-17.md", "codex_rehearsal_final.md", "codex_rehearsal_transcript.txt",
        "AGENTS.md", "CLAUDE.md", "CANON.md", "CURRENT_SCIENTIFIC_PREMISES.md",
        "CURRENT_SCIENTIFIC_PREMISES.tsv", "verify_current_scientific_premises.py",
        "UDT_METRIC_KERNEL_DEVELOPMENT.md", "UDT_METRIC_KERNEL_COVERAGE.tsv",
        "research/_registry/CURRENT_ARTIFACT_PATHS.tsv",
    ]
    for name in fixed_and_controls:
        assert (ROOT / name).read_bytes() == base_bytes(name), name

    prior_archive = "archive/stale_working_documents_2026-09-27/"
    old_paths = git("ls-tree", "-r", "--name-only", BASE, "--", prior_archive).decode().splitlines()
    assert old_paths
    for name in old_paths:
        assert (ROOT / name).read_bytes() == base_bytes(name), name

    archive_readme = ROOT / "archive/remaining_working_surfaces_2026-09-27/README.md"
    link_docs = [PACKET / "README.md", archive_readme, ROOT / prior_archive / "README.md"]
    local_links = []
    for doc in link_docs:
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", doc.read_text()):
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            resolved = (doc.parent / target).resolve()
            assert resolved.exists(), (str(doc.relative_to(ROOT)), target)
            local_links.append({"source": str(doc.relative_to(ROOT)), "target": target})
    archived_links = set(re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", archive_readme.read_text()))
    assert eligible <= archived_links
    manuscript_receipt = "UDT_METRIC_KERNEL_OBSERVER_PAIR_FIDELITY_REVIEW_2026-09-05.md"
    assert manuscript_receipt in (ROOT / "UDT_METRIC_KERNEL_DEVELOPMENT.md").read_text()
    assert manuscript_receipt in archived_links
    assert "Fixed-manuscript review history" in archive_readme.read_text()
    assert "stale_working_documents_2026-09-27/README.md" in (PACKET / "README.md").read_text()
    assert "remaining_working_surfaces_2026-09-27/README.md" in (PACKET / "README.md").read_text()

    tracked_diff = git("diff", "--name-status", BASE).decode().splitlines()
    deleted = {line.split("\t", 1)[1] for line in tracked_diff if line.startswith("D\t")}
    modified = {line.split("\t", 1)[1] for line in tracked_diff if line.startswith("M\t")}
    assert deleted == eligible
    assert modified == {"README.md", "INDEX.md", "LIVE.md", "HANDOFF.md", "research/_registry/README.md"}

    result = {
        "status": "PASS", "baseline": BASE, "reviewed_union": len(effective),
        "full_prose_archive_selection": len(eligible), "retained": len(retained),
        "archive_bytes_independently_recomputed": sum(row["bytes"] for row in per_file),
        "archive_modes": sorted({row["mode"] for row in per_file}),
        "local_markdown_links_checked": len(local_links),
        "unchanged_prior_archive_paths": len(old_paths),
        "unchanged_fixed_or_control_paths_checked": len(fixed_and_controls),
        "tracked_diff_exact_selected_moves_plus_five_navigation_edits": True,
        "no_unprocessed_eligible_item_in_reviewed_union": True,
        "scientific_checks_not_replayed": True,
        "limits": "Metadata/byte/static-link checks only; substantive source-first placement review is separately recorded. No complete dynamic dependency graph or scientific reproof.",
    }
    (OUT / "PER_FILE_BYTE_CHECK.json").write_text(json.dumps(per_file, indent=2) + "\n")
    (OUT / "LINK_CHECK.json").write_text(json.dumps(local_links, indent=2) + "\n")
    (OUT / "CONSTRUCTED_SELECTION_CHECK.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
