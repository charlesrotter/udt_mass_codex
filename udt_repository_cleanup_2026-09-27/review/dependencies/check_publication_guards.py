#!/usr/bin/env python3
"""Run actual publication checker against isolated metadata/byte fault fixtures."""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "final"
SOURCE = ROOT / "udt_repository_cleanup_2026-09-27/verify_cleanup.py"

def main():
    spec = importlib.util.spec_from_file_location("publication_checker_under_review", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tree = ast.parse(SOURCE.read_text())
    preserved = next(ast.literal_eval(node.value) for node in ast.walk(tree)
                     if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "unchanged" for target in node.targets))
    payload = b"Synthetic preserved administrative receipt.\n"
    sha = hashlib.sha256(payload).hexdigest()
    oid = hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()
    source = "candidate.md"
    archive = "archive/remaining_working_surfaces_2026-09-27/"
    paths = [source] + preserved
    paths.extend(f"retained/item_{number:05d}.md" for number in range(33380 - len(paths)))
    listing = b"".join(f"100644 blob {oid} {len(payload)}\t{path}\0".encode() for path in paths)
    rows = [dict(path=path, mode="100644", object_id=oid, bytes=str(len(payload)),
                 disposition="ARCHIVE_REVIEWED" if path == source else "RETAIN_COHERENT_PACKAGE",
                 destination=archive + source if path == source else path) for path in paths]
    archived = [dict(source=source, destination=archive + source, source_commit="synthetic_baseline",
                     source_blob_oid=oid, sha256=sha, bytes=str(len(payload)))]
    statuses = [f"?? unrelated_{number:02d}.md" for number in range(52)]
    scratch = Path(tempfile.mkdtemp(prefix="cleanup_publication_guards_"))
    results = {}

    def fixture(name, mutate=None):
        root = scratch / name
        packet = root / "packet"
        packet.mkdir(parents=True)
        (packet / "BASELINE.json").write_text(json.dumps({"HEAD": "synthetic_baseline", "preexisting_status_lines": statuses}))
        for path in preserved:
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        destination = root / archive / source
        destination.parent.mkdir(parents=True)
        local_rows = copy.deepcopy(rows)
        local_archive = copy.deepcopy(archived)
        state = dict(rows=local_rows, archived=local_archive, status=statuses.copy(), changed=[source],
                     mode=0o664, payload=payload, destination=destination, root=root, packet=packet,
                     archive_symlink=False, dangling_root_symlink=False)
        if mutate:
            mutate(state)
        if state["archive_symlink"]:
            actual = root / "symlink_target.md"
            actual.write_bytes(payload)
            destination.symlink_to(actual)
        else:
            destination.write_bytes(state["payload"])
            destination.chmod(state["mode"])
        if state["dangling_root_symlink"]:
            (root / source).symlink_to(root / "absent-target.md")
        module.ROOT = root
        module.PACKET = packet
        module.PREFIX = "packet/"

        def git(*args):
            if args[0] == "ls-tree":
                return listing
            if args[0] == "show":
                return payload
            if args[0] == "diff":
                return ("\n".join(state["changed"]) + "\n").encode()
            if args[0] == "status":
                return ("\n".join(state["status"]) + "\n").encode()
            if args[0] == "branch":
                return b"grok\n"
            raise AssertionError("unexpected synthetic Git operation")

        module.git = git
        module.table = lambda path: state["rows"] if path.name == "TRACKED_DISPOSITIONS.tsv" else state["archived"]
        return module.run()

    for mode in (0o664, 0o644):
        fixture(f"valid_{mode:o}", lambda state, mode=mode: state.update(mode=mode))
        results[f"valid_regular_{mode:o}"] = "PASS"

    negatives = {
        "inventory_destination_mismatch": lambda s: s["rows"][0].update(destination="archive/other.md"),
        "same_bytes_archive_symlink": lambda s: s.update(archive_symlink=True),
        "dangling_original_symlink": lambda s: s.update(dangling_root_symlink=True),
        "executable_archive_mode": lambda s: s.update(mode=0o755),
        "archive_bytes_changed": lambda s: s.update(payload=payload + b"changed\n"),
        "archive_manifest_hash_changed": lambda s: s["archived"][0].update(sha256="0" * 64),
        "archive_manifest_size_changed": lambda s: s["archived"][0].update(bytes="0"),
        "archive_manifest_blob_changed": lambda s: s["archived"][0].update(source_blob_oid="0" * 40),
        "archive_duplicate_row": lambda s: s["archived"].append(copy.deepcopy(s["archived"][0])),
        "retained_destination_changed": lambda s: s["rows"][1].update(destination="elsewhere.md"),
        "unrelated_tracked_change": lambda s: s["changed"].append("unrelated.md"),
        "unrelated_status_change": lambda s: s["status"].append("?? new_unrelated.md"),
    }
    for name, mutation in negatives.items():
        try:
            fixture(name, mutation)
        except (AssertionError, FileNotFoundError, KeyError, ValueError) as error:
            results[name] = {"status": "REJECTED", "reason": str(error)}
        else:
            raise AssertionError("publication checker false pass: " + name)
    result = {"status": "PASS", "checker_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "scratch": str(scratch), "results": results,
              "scope": "Actual run() with Git/table input functions and ROOT/PACKET replaced by isolated synthetic fixtures. Real lstat/read_bytes/sha and guard branches execute. Synthetic bytes only; no production source mutation or protected content."}
    (OUT / "PUBLICATION_GUARD_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
