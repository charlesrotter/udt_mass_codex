"""Construct the explicitly reviewed archive; preserve every original byte.

Idempotent only for the same baseline and already-identical destinations.
No scientific files, historical manifests or protected payloads are rewritten.
"""
import csv
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKET = Path(__file__).resolve().parent
PREFIX = PACKET.relative_to(ROOT).as_posix()
DEST = "archive/remaining_working_surfaces_2026-09-27/"


def table(path):
    with path.open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_table(path, rows):
    with path.open("w") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    baseline = json.loads((PACKET / "BASELINE.json").read_text())["HEAD"]
    surface_file = PACKET / "review/surfaces/SURFACE_CLASSIFICATION.tsv"
    sources = {r["path"]: (r, surface_file) for r in table(surface_file)}
    supplement = PACKET / "review/surfaces/supplemental_transfer/SUPPLEMENTAL_CLASSIFICATION.tsv"
    if supplement.exists():
        for row in table(supplement):
            assert row["path"] in sources
            sources[row["path"]] = (row, supplement)
    dependency_file = PACKET / "review/dependencies/DEPENDENCY_CLASSIFICATION.tsv"
    dependencies = {r["path"]: r for r in table(dependency_file)}
    selected = sorted((name, row, ref) for name, (row, ref) in sources.items()
                      if row["disposition"] == "ARCHIVE_ELIGIBLE")
    assert selected
    manifest, overrides, payloads = [], [], {}
    for name, row, reference in selected:
        assert "/" not in name and Path(name).suffix == ".md"
        assert dependencies[name]["dependency_disposition"] == "DEPENDENCY_CLEAR_FOR_REVIEWED_ARCHIVE"
        assert row["actual_read_depth"].startswith("FULL"), "full source review required"
        original = subprocess.check_output(["git", "show", baseline + ":" + name], cwd=ROOT)
        sha = hashlib.sha256(original).hexdigest()
        oid = subprocess.check_output(["git", "rev-parse", baseline + ":" + name], cwd=ROOT).decode().strip()
        assert row["baseline_sha256"] == sha and row["baseline_git_blob"] == oid
        source, destination = ROOT / name, ROOT / (DEST + name)
        assert not source.is_symlink() and not destination.is_symlink()
        assert source.exists() != destination.exists(), "exactly one original or archived file required"
        present = source if source.exists() else destination
        mode = present.lstat().st_mode
        assert stat.S_ISREG(mode) and stat.S_IMODE(mode) in (0o644, 0o664)
        assert present.read_bytes() == original
        payloads[name] = original
        refs = reference.relative_to(ROOT).as_posix() + ";" + dependency_file.relative_to(ROOT).as_posix()
        manifest.append(dict(source=name, destination=DEST + name, source_commit=baseline,
                             source_blob_oid=oid, sha256=sha, bytes=len(original), filesystem_mode=oct(stat.S_IMODE(mode)),
                             group=row["grouping"], reason=row["reason"],
                             reference_handling=row["required_pointer_or_consumer_action"],
                             review_references=refs))
        overrides.append(dict(path=name, disposition="ARCHIVE_REVIEWED", reason_id="A01",
                              read_depth="FULL_CONTENT_REVIEW_PLUS_SEPARATE_DEPENDENCY_REVIEW",
                              destination=DEST + name, review_reference=refs))
    # Rehearse relocation and restoration on selected original bytes in scratch.
    with tempfile.TemporaryDirectory(prefix="udt-cleanup-restore-") as scratch:
        folder = Path(scratch)
        for name, original in payloads.items():
            old, moved, restored = folder / name, folder / (name + ".archived"), folder / (name + ".restored")
            old.write_bytes(original)
            old.rename(moved)
            moved.rename(restored)
            assert restored.read_bytes() == original and not old.exists() and not moved.exists()
    write_table(PACKET / "archive/ARCHIVE_MANIFEST.tsv", manifest)
    write_table(PACKET / "inventory/REVIEWED_OVERRIDES.tsv", overrides)
    (ROOT / DEST).mkdir(parents=True, exist_ok=True)
    for name in payloads:
        if (ROOT / name).exists():
            (ROOT / name).rename(ROOT / (DEST + name))
    result = dict(status="PASS", baseline=baseline, archived_files=len(manifest),
                  archived_bytes=sum(r["bytes"] for r in manifest),
                  scratch_relocation_and_restoration="exact bytes for every selected file",
                  source_and_dependency_rows_matched=True)
    (PACKET / "archive/CONSTRUCTION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
