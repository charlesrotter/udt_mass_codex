#!/usr/bin/env python3
"""Publication gate tests with real Git trees/indexes confined to owned /tmp repos."""
import copy
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / "udt_repository_cleanup_2026-09-27/verify_publication.py"
MAINTAINED = ["README.md", "INDEX.md", "LIVE.md", "HANDOFF.md", "research/_registry/README.md"]
PREFIX = "udt_repository_cleanup_2026-09-27/"
ARCHIVE = "archive/remaining_working_surfaces_2026-09-27/"

def command(repo, *args):
    return subprocess.check_output(["git", *args], cwd=repo, stderr=subprocess.PIPE)

def fixture(scratch, name, fault=None):
    repo = scratch / name
    repo.mkdir()
    command(repo, "init", "-q")
    command(repo, "config", "user.name", "Publication gate fixture")
    command(repo, "config", "user.email", "fixture@example.invalid")
    for path in MAINTAINED + ["original.md", "unrelated.md"]:
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"Synthetic baseline bytes.\n")
    command(repo, "add", "--", *MAINTAINED, "original.md", "unrelated.md")
    command(repo, "commit", "-qm", "synthetic baseline")
    baseline = command(repo, "rev-parse", "HEAD").decode().strip()
    for path in MAINTAINED:
        (repo / path).write_bytes(b"Synthetic reviewed navigation.\n")
    packet = repo / PREFIX
    (packet / "archive").mkdir(parents=True)
    archived = repo / ARCHIVE
    archived.mkdir(parents=True)
    (repo / "original.md").rename(archived / "original.md")
    (archived / "README.md").write_text("Synthetic archive guide.\n")
    (packet / "README.md").write_text("Synthetic maintenance guide.\n")
    (packet / "verify_publication.py").write_bytes(SOURCE.read_bytes())
    archive_rows = [dict(source="original.md", destination=ARCHIVE + "original.md")]
    if fault == "wrong_archive_destination":
        archive_rows[0]["destination"] = ARCHIVE + "elsewhere.md"
    if fault == "duplicate_archive_row":
        archive_rows.append(copy.deepcopy(archive_rows[0]))
    with (packet / "archive/ARCHIVE_MANIFEST.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "destination"], delimiter="\t")
        writer.writeheader(); writer.writerows(archive_rows)
    files = sorted(MAINTAINED + [PREFIX + name for name in ["PUBLICATION_SCOPE.json", "SHA256SUMS.txt", "archive/ARCHIVE_MANIFEST.tsv", "verify_publication.py", "README.md"]] + [ARCHIVE + "original.md", ARCHIVE + "README.md"])
    if fault == "omitted_archive_destination":
        files.remove(ARCHIVE + "original.md")
    if fault == "omitted_scope_delivery":
        files.remove(PREFIX + "PUBLICATION_SCOPE.json")
    if fault == "owned_artifact_omission":
        (packet / "unlisted_report.md").write_text("Must be included.\n")
    modes = {path: "100644" for path in files}
    if fault == "executable_index_mode":
        modes[PREFIX + "verify_publication.py"] = "100755"
        (packet / "verify_publication.py").chmod(0o755)
    scope = dict(baseline=baseline, required_files=files, deleted_originals=["original.md"], required_modes=modes)
    if fault == "duplicate_required_file":
        scope["required_files"].append(files[0])
    (packet / "PUBLICATION_SCOPE.json").write_text(json.dumps(scope, indent=2) + "\n")
    hashes = [(hashlib.sha256((repo / path).read_bytes()).hexdigest(), path)
              for path in files if path != PREFIX + "SHA256SUMS.txt"]
    if fault == "manifest_hash_mismatch":
        hashes[0] = ("0" * 64, hashes[0][1])
    if fault == "manifest_membership_omission":
        hashes.pop()
    (packet / "SHA256SUMS.txt").write_text("".join(f"{digest}  {path}\n" for digest, path in hashes))
    command(repo, "add", "--", "original.md", *files)
    if fault == "working_same_bytes_symlink":
        target = repo / "preserved_target.md"
        (archived / "original.md").rename(target)
        (archived / "original.md").symlink_to(target)
    if fault == "working_bytes_after_stage":
        (archived / "original.md").write_text("Changed after staging.\n")
    if fault == "extra_staged_path":
        (repo / "unrelated.md").write_text("Unauthorized staged edit.\n")
        command(repo, "add", "--", "unrelated.md")
    if fault == "original_still_in_index":
        (repo / "original.md").write_text("Synthetic baseline bytes.\n")
        command(repo, "add", "--", "original.md")
    spec = importlib.util.spec_from_file_location("publication_gate_" + name, SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = repo
    module.PACKET = packet
    module.PREFIX = PREFIX
    return repo, baseline, module

def main():
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    scratch = Path(tempfile.mkdtemp(prefix="cleanup_publication_real_git_"))
    results = {}
    repo, base, module = fixture(scratch, "valid_index_and_commit")
    staged = module.verify()
    assert staged["status"] == "PASS"
    results["valid_staged_index"] = staged
    tree = command(repo, "write-tree").decode().strip()
    commit = command(repo, "commit-tree", tree, "-p", base, "-m", "synthetic reviewed publication").decode().strip()
    committed = module.verify(commit)
    assert committed["status"] == "PASS"
    results["valid_single_parent_commit"] = committed
    faults = ["omitted_archive_destination", "omitted_scope_delivery", "owned_artifact_omission",
              "wrong_archive_destination", "duplicate_archive_row", "duplicate_required_file",
              "executable_index_mode", "manifest_hash_mismatch", "manifest_membership_omission",
              "working_same_bytes_symlink", "working_bytes_after_stage", "extra_staged_path",
              "original_still_in_index"]
    for fault in faults:
        repo, base, module = fixture(scratch, fault, fault)
        try:
            module.verify()
        except (AssertionError, KeyError, ValueError, subprocess.CalledProcessError) as error:
            results[fault] = {"status": "REJECTED", "reason": str(error)}
        else:
            raise AssertionError("publication false pass: " + fault)
    repo, base, module = fixture(scratch, "parent_controls")
    tree = command(repo, "write-tree").decode().strip()
    base_tree = command(repo, "rev-parse", base + "^{tree}").decode().strip()
    side = command(repo, "commit-tree", base_tree, "-p", base, "-m", "synthetic extra parent").decode().strip()
    wrong_parent = command(repo, "commit-tree", tree, "-p", side, "-m", "synthetic wrong parent").decode().strip()
    merge = command(repo, "commit-tree", tree, "-p", base, "-p", side, "-m", "synthetic two-parent publication").decode().strip()
    for name, candidate in [("wrong_single_parent", wrong_parent), ("merge_first_parent_matches", merge)]:
        try:
            module.verify(candidate)
        except AssertionError as error:
            results[name] = {"status": "REJECTED", "reason": str(error)}
        else:
            raise AssertionError("commit parent false pass: " + name)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == source_hash, "checker changed during exercise"
    result = {"status": "PASS", "source_sha256": source_hash, "scratch_root": str(scratch),
              "actual_repository_index_touched": False, "results": results,
              "scope": "Real Git in owned temporary repositories, actual production verify() with ROOT/PACKET/PREFIX redirected. Two healthy states and15 faults; no scientific/protected inputs or remote activity."}
    (OUT / "SCRATCH_GIT_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
