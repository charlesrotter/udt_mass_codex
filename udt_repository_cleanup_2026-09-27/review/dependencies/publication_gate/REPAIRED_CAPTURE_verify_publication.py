"""Read-only exact index/commit membership and blob check for this cleanup.

Run after PUBLICATION_SCOPE.json and SHA256SUMS.txt have been sealed.
This checks delivery of the reviewed files, not their scientific validity.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import stat
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKET = Path(__file__).resolve().parent
PREFIX = PACKET.relative_to(ROOT).as_posix() + "/"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def verify(commit=None):
    scope = json.loads((PACKET / "PUBLICATION_SCOPE.json").read_text())
    files = scope["required_files"]
    deleted = scope["deleted_originals"]
    maintained = {"README.md", "INDEX.md", "LIVE.md", "HANDOFF.md", "research/_registry/README.md"}
    archive_prefix = "archive/remaining_working_surfaces_2026-09-27/"
    assert all(name in maintained or name.startswith((PREFIX, archive_prefix)) for name in files), "publication scope"
    assert all(not Path(name).is_absolute() and ".." not in Path(name).parts for name in files)
    mandatory = maintained | {PREFIX + n for n in ("PUBLICATION_SCOPE.json", "SHA256SUMS.txt", "archive/ARCHIVE_MANIFEST.tsv", "verify_publication.py", "README.md")}
    mandatory.add(archive_prefix + "README.md")
    assert mandatory <= set(files), "required publication interfaces omitted"
    with (PACKET / "archive/ARCHIVE_MANIFEST.tsv").open() as handle:
        archive_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(archive_rows) == len({row["source"] for row in archive_rows})
    assert set(deleted) == {row["source"] for row in archive_rows}
    for row in archive_rows:
        assert "/" not in row["source"]
        assert row["destination"] == archive_prefix + row["source"]
        assert row["destination"] in files, "archive destination omitted from publication"
    owned = {p.relative_to(ROOT).as_posix() for folder in (PACKET, ROOT / archive_prefix)
             for p in folder.rglob("*") if (p.is_file() or p.is_symlink()) and "__pycache__" not in p.parts}
    assert set(files) == owned | maintained, "owned artifact omitted or extra publication path"
    assert len(files) == len(set(files)) and len(deleted) == len(set(deleted))
    assert not set(files) & set(deleted)
    baseline = scope["baseline"]
    if commit is None:
        assert git("rev-parse", "HEAD").decode().strip() == baseline
        changed = git("diff", "--cached", "--name-status", "--no-renames", "-z", baseline)
        tree_metadata = git("ls-files", "--stage", "-z")
        target = ":"
    else:
        commit = git("rev-parse", commit).decode().strip()
        assert git("rev-list", "--parents", "-n", "1", commit).decode().split() == [commit, baseline], "unexpected commit parent(s)"
        changed = git("diff", "--name-status", "--no-renames", "-z", baseline, commit)
        tree_metadata = git("ls-tree", "-r", "-z", commit)
        target = commit + ":"
    modes = {}
    for record in tree_metadata.decode().split("\0"):
        if record:
            meta, name = record.split("\t", 1)
            assert name not in modes, "unmerged or duplicate path"
            modes[name] = meta.split()[0]
    assert set(scope["required_modes"]) == set(files), "mode manifest membership"
    assert set(scope["required_modes"].values()) == {"100644"}, "publication requires regular non-executable files"
    assert all(modes.get(name) == scope["required_modes"][name] for name in files), "delivered file mode"
    assert not set(deleted) & set(modes), "deleted originals remain"
    fields = changed.decode().split("\0")
    assert fields[-1] == ""
    assert len(fields[:-1]) % 2 == 0, "malformed diff metadata"
    observed = {}
    for status, name in zip(fields[:-1:2], fields[1:-1:2]):
        assert name not in observed
        observed[name] = status
    assert set(observed) == set(files) | set(deleted), "exact publication membership"
    assert all(observed[name] == "D" for name in deleted)
    assert all(observed[name] in ("A", "M") for name in files)
    hashes = {}
    for line in (PACKET / "SHA256SUMS.txt").read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert name not in hashes
        hashes[name] = digest
    manifest_name = PREFIX + "SHA256SUMS.txt"
    assert set(hashes) == set(files) - {manifest_name}, "manifest membership"
    total = 0
    for name in files:
        mode = (ROOT / name).lstat().st_mode
        assert stat.S_ISREG(mode) and not mode & 0o111, "working publication file type/mode"
        current = (ROOT / name).read_bytes()
        delivered = git("show", target + name)
        assert current == delivered, "delivered blob differs: " + name
        digest = hashlib.sha256(delivered).hexdigest()
        if name != manifest_name:
            assert digest == hashes[name], "manifest hash differs: " + name
        total += len(delivered)
    return dict(status="PASS", target=commit or "index", baseline=baseline,
                published_files=len(files), deleted_originals=len(deleted),
                delivered_bytes=total,
                manifest_sha256=hashlib.sha256((PACKET / "SHA256SUMS.txt").read_bytes()).hexdigest(),
                scope="Exact changed-path membership and every expected delivered blob against sealed working files; not scientific evidence.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", help="Commit to verify; omit for the staged index")
    print(json.dumps(verify(parser.parse_args().commit), indent=2))
