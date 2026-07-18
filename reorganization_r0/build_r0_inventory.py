#!/usr/bin/env python3
"""Build the Phase-R0 base-root census and static dependency map.

The repository scan is pinned to a Git tree. Dirty-workstation content is never
opened: its separate inventory uses `git status` and `os.lstat` only.
"""

from __future__ import annotations

import argparse
import ast
import csv
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat
import subprocess
from typing import Any, Iterable
from urllib.parse import unquote


CLASSIFICATIONS = {
    "CONTROL",
    "ACTIVE",
    "FROZEN_EVIDENCE",
    "ARCHIVE_CANDIDATE",
    "MOVE_CANDIDATE",
    "UNKNOWN/BLOCKED",
}

TEXT_SUFFIXES = {
    ".cfg",
    ".csv",
    ".ini",
    ".json",
    ".log",
    ".md",
    ".py",
    ".rst",
    ".sh",
    ".tex",
    ".toml",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}

CONTROL_ROOT = {
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CANON.md",
    "CLAUDE.md",
    "COGNITIVE_CORRAL_TRIGGERS_SETUP.md",
    "CROSS_MODEL_VERIFY.md",
    "FOUNDATIONAL_ASSUMPTIONS_LEDGER.md",
    "HANDOFF.md",
    "HYGIENE_HEADER_TEMPLATE.md",
    "INDEX.md",
    "LIVE.md",
    "MEMORY.md",
    "NEGATIVES_REGISTRY.md",
    "PROBLEM_STATEMENT.md",
    "PROVENANCE.md",
    "STRUCTURE_HYGIENE.md",
    "pytest.ini",
    "requirements.txt",
}

STARTUP_SOURCES = {
    "AGENTS.md",
    "CLAUDE.md",
    "HANDOFF.md",
    "INDEX.md",
    "LIVE.md",
    "MEMORY.md",
}

FILE_CALLS = {
    "Path",
    "PurePath",
    "open",
    "builtins.open",
    "glob.glob",
    "glob.iglob",
    "json.load",
    "json.dump",
    "np.load",
    "np.save",
    "np.savez",
    "np.savez_compressed",
    "numpy.load",
    "numpy.save",
    "numpy.savez",
    "os.listdir",
    "os.makedirs",
    "os.mkdir",
    "os.path.join",
    "os.scandir",
    "pd.read_csv",
    "pd.read_json",
    "pd.read_table",
    "pd.to_csv",
    "read_csv",
    "read_json",
    "shutil.copy",
    "shutil.copy2",
    "shutil.move",
    "torch.load",
    "torch.save",
}

PATH_METHODS = {
    "glob",
    "mkdir",
    "open",
    "read_bytes",
    "read_text",
    "rglob",
    "touch",
    "with_name",
    "write_bytes",
    "write_text",
}

FROZEN_MANIFESTS = (
    (
        "stage1_A",
        "native_action_stage1_2026-07-18/arm_A",
        "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    ),
    (
        "stage1_B",
        "native_action_stage1_2026-07-18/arm_B",
        "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    ),
    (
        "stage2_A",
        "native_action_stage2_2026-07-18/arm_A",
        "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    ),
    (
        "stage2_B",
        "native_action_stage2_2026-07-18/arm_B",
        "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    ),
    (
        "arm_C",
        "native_action_arm_c_2026-07-18",
        "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    ),
    (
        "final_adjudication",
        "native_action_final_adjudication_2026-07-18",
        "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
    ),
)


@dataclass(frozen=True)
class TreeEntry:
    mode: str
    object_type: str
    oid: str
    path: str


def run(
    command: list[str], cwd: Path, *, binary: bool = False, env: dict[str, str] | None = None
) -> str | bytes:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return completed.stdout if binary else completed.stdout.decode("utf-8", "replace")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def tree_entries(repo: Path, base: str) -> list[TreeEntry]:
    raw = run(["git", "ls-tree", "-r", "-z", base], repo, binary=True)
    assert isinstance(raw, bytes)
    rows: list[TreeEntry] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, object_type, oid = metadata.decode().split()
        rows.append(
            TreeEntry(
                mode=mode,
                object_type=object_type,
                oid=oid,
                path=raw_path.decode("utf-8", "surrogateescape"),
            )
        )
    return rows


def read_blobs(repo: Path, entries: Iterable[TreeEntry]) -> dict[str, bytes]:
    entries = list(entries)
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    blobs: dict[str, bytes] = {}
    try:
        for entry in entries:
            if entry.object_type != "blob":
                continue
            process.stdin.write(entry.oid.encode() + b"\n")
            process.stdin.flush()
            header = process.stdout.readline().decode().strip().split()
            if len(header) != 3 or header[1] != "blob":
                raise RuntimeError(f"bad cat-file header for {entry.path}: {header}")
            size = int(header[2])
            payload = process.stdout.read(size)
            if process.stdout.read(1) != b"\n":
                raise RuntimeError(f"bad cat-file terminator for {entry.path}")
            blobs[entry.path] = payload
    finally:
        if process.stdin:
            process.stdin.close()
        process.wait(timeout=30)
    if process.returncode != 0:
        stderr = process.stderr.read().decode("utf-8", "replace") if process.stderr else ""
        raise RuntimeError(f"git cat-file failed: {stderr}")
    return blobs


def is_text_path(path: str, payload: bytes) -> bool:
    basename = PurePosixPath(path).name
    if basename in {"Dockerfile", "Makefile", "SHA256SUMS"}:
        return b"\0" not in payload[:8192]
    return PurePosixPath(path).suffix.lower() in TEXT_SUFFIXES and b"\0" not in payload[:8192]


def last_commit_map(repo: Path, base: str, tracked: set[str]) -> dict[str, tuple[str, str, str]]:
    raw = run(
        [
            "git",
            "-c",
            "core.quotepath=false",
            "log",
            "--no-renames",
            "--format=R0COMMIT:%H%x1f%cs%x1f%s",
            "--name-only",
            base,
            "--",
        ],
        repo,
    )
    assert isinstance(raw, str)
    result: dict[str, tuple[str, str, str]] = {}
    current: tuple[str, str, str] | None = None
    for line in raw.splitlines():
        if line.startswith("R0COMMIT:"):
            fields = line[len("R0COMMIT:") :].split("\x1f", 2)
            if len(fields) == 3:
                current = (fields[0], fields[1], fields[2])
            continue
        path = line.strip()
        if current and path in tracked and path not in result:
            result[path] = current
    missing = tracked - set(result)
    if missing:
        raise RuntimeError(f"missing last-commit metadata: {sorted(missing)[:20]}")
    return result


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def normalize_candidate(path: str) -> str:
    normalized = posixpath.normpath(path)
    return normalized[2:] if normalized.startswith("./") else normalized


def resolve_target(
    raw_target: str,
    source: str,
    tracked: set[str],
    directories: set[str],
    basenames: dict[str, list[str]],
) -> tuple[str, str]:
    raw = unquote(raw_target.strip().strip("<>").strip("'\""))
    if not raw:
        return "", "EMPTY"
    if raw.startswith("#"):
        return source, "RESOLVED_ANCHOR"
    if re.match(r"^(?:https?|ftp|mailto|data|file|app)://", raw):
        return raw, "EXTERNAL"
    if raw.startswith(("git@", "urn:")):
        return raw, "EXTERNAL"
    raw = raw.split("#", 1)[0].split("?", 1)[0]
    if re.search(r"[{}*$?]", raw) or "..." in raw:
        return raw, "DYNAMIC_OR_GLOB"
    if raw.startswith("/"):
        return raw, "ABSOLUTE_EXTERNAL"
    candidates = [
        normalize_candidate(posixpath.join(posixpath.dirname(source), raw)),
        normalize_candidate(raw),
    ]
    for candidate in candidates:
        if candidate in tracked:
            return candidate, "RESOLVED_TRACKED"
        if candidate in directories:
            return candidate + "/", "RESOLVED_DIRECTORY"
    basename_matches = basenames.get(PurePosixPath(raw).name, [])
    if len(basename_matches) == 1:
        return basename_matches[0], "RESOLVED_BY_BASENAME"
    if len(basename_matches) > 1:
        return "|".join(sorted(basename_matches)), "AMBIGUOUS_BASENAME"
    return candidates[0], "MISSING_OR_GENERATED"


def function_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = function_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def literal_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        try:
            return ast.unparse(node)
        except Exception:
            return "<dynamic-f-string>"
    return None


def looks_pathlike(value: str) -> bool:
    if not value or len(value) > 500:
        return False
    return bool(
        "/" in value
        or "\\" in value
        or re.search(
            r"\.(?:cfg|csv|ini|json|log|md|npy|npz|pt|py|sh|toml|tsv|txt|yaml|yml)(?:$|[#?])",
            value,
            re.IGNORECASE,
        )
    )


def module_index(paths: Iterable[str]) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for path in paths:
        if not path.endswith(".py"):
            continue
        pure = PurePosixPath(path)
        if pure.name == "__init__.py":
            module = ".".join(pure.parent.parts)
        else:
            module = ".".join(pure.with_suffix("").parts)
        index.setdefault(module, []).append(path)
        if len(pure.parts) == 1:
            index.setdefault(pure.stem, []).append(path)
    return index


def resolve_import(
    module: str,
    source: str,
    modules: dict[str, list[str]],
    level: int = 0,
) -> tuple[str, str]:
    target_module = module
    if level:
        package_parts = list(PurePosixPath(source).parent.parts)
        keep = max(0, len(package_parts) - level + 1)
        prefix = package_parts[:keep]
        target_module = ".".join(prefix + ([module] if module else []))
    candidates = modules.get(target_module, [])
    if not candidates and "." in target_module:
        candidates = modules.get(target_module.split(".", 1)[0], [])
    candidates = sorted(set(candidates))
    if len(candidates) == 1:
        return candidates[0], "RESOLVED_INTERNAL"
    if len(candidates) > 1:
        return "|".join(candidates), "AMBIGUOUS_INTERNAL"
    return target_module, "EXTERNAL_OR_STDLIB"


def parse_dirty_status(checkout: Path) -> list[dict[str, Any]]:
    environment = os.environ.copy()
    environment["GIT_OPTIONAL_LOCKS"] = "0"
    raw = run(
        [
            "git",
            "--no-optional-locks",
            "status",
            "--porcelain=v2",
            "-z",
            "--untracked-files=all",
        ],
        checkout,
        binary=True,
        env=environment,
    )
    assert isinstance(raw, bytes)
    records = raw.split(b"\0")
    rows: list[dict[str, Any]] = []
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        marker = record[:1]
        original_path = ""
        if marker == b"1":
            fields = record.split(b" ", 8)
            status_code = fields[1].decode("ascii", "replace")
            raw_path = fields[8]
            kind = "TRACKED_DIRTY"
        elif marker == b"2":
            fields = record.split(b" ", 9)
            status_code = fields[1].decode("ascii", "replace")
            raw_path = fields[9]
            original_path = records[index].decode("utf-8", "surrogateescape")
            index += 1
            kind = "TRACKED_RENAME_OR_COPY"
        elif marker == b"u":
            fields = record.split(b" ", 10)
            status_code = fields[1].decode("ascii", "replace")
            raw_path = fields[10]
            kind = "TRACKED_UNMERGED"
        elif marker == b"?":
            status_code = "??"
            raw_path = record[2:]
            kind = "UNTRACKED"
        elif marker == b"!":
            status_code = "!!"
            raw_path = record[2:]
            kind = "IGNORED"
        else:
            raise RuntimeError(f"unrecognized porcelain-v2 record: {record[:100]!r}")
        path = raw_path.decode("utf-8", "surrogateescape")
        target = checkout / path
        try:
            metadata = os.lstat(target)
            if stat.S_ISREG(metadata.st_mode):
                object_type = "regular_file"
            elif stat.S_ISDIR(metadata.st_mode):
                object_type = "directory"
            elif stat.S_ISLNK(metadata.st_mode):
                object_type = "symlink"
            else:
                object_type = "other"
            size = metadata.st_size
            mode = f"{stat.S_IMODE(metadata.st_mode):04o}"
        except FileNotFoundError:
            object_type = "missing"
            size = ""
            mode = ""
        rows.append(
            {
                "path": path,
                "status": status_code,
                "kind": kind,
                "object_type": object_type,
                "size_bytes_lstat": size,
                "mode_lstat": mode,
                "original_path": original_path,
                "content_sha256": "NOT_READ",
                "firewall": "STATUS_AND_LSTAT_ONLY",
            }
        )
    return sorted(rows, key=lambda row: row["path"])


def verify_frozen_manifests(repo: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for label, relative, expected_manifest_hash in FROZEN_MANIFESTS:
        package = repo / relative
        manifest = package / "SHA256SUMS.txt"
        manifest_payload = manifest.read_bytes()
        actual_manifest_hash = sha256(manifest_payload)
        failures: list[str] = []
        entries = 0
        for row in manifest_payload.decode("utf-8").splitlines():
            entries += 1
            expected, listed = row.split("  ", 1)
            listed = listed[2:] if listed.startswith("./") else listed
            target = package / listed
            if not target.is_file():
                failures.append(f"missing:{listed}")
            elif sha256(target.read_bytes()) != expected:
                failures.append(f"hash:{listed}")
        passed = actual_manifest_hash == expected_manifest_hash and not failures
        if not passed:
            raise RuntimeError(
                f"frozen package failure {label}: manifest={actual_manifest_hash}, "
                f"expected={expected_manifest_hash}, failures={failures}"
            )
        results.append(
            {
                "label": label,
                "package": relative,
                "manifest_sha256": actual_manifest_hash,
                "manifest_entries": entries,
                "internal_manifest": "PASS",
            }
        )
    return results


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    def normalized(value: Any) -> Any:
        if isinstance(value, str):
            return value.replace("\t", "\\t").replace("\r", "\\r").replace("\n", "\\n")
        return value

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(
            {field: normalized(row.get(field, "")) for field in fieldnames}
            for row in rows
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    arguments = parser.parse_args()

    repo = arguments.repo.resolve()
    output_dir = arguments.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    base = str(run(["git", "rev-parse", arguments.base], repo)).strip()
    print("R0_SCAN phase=tree", flush=True)
    entries = tree_entries(repo, base)
    tracked = {entry.path for entry in entries}
    root_entries = [entry for entry in entries if "/" not in entry.path]
    root_paths = {entry.path for entry in root_entries}
    blobs = read_blobs(repo, entries)
    print(f"R0_SCAN phase=blobs entries={len(blobs)}", flush=True)
    texts = {
        path: payload.decode("utf-8", "replace")
        for path, payload in blobs.items()
        if is_text_path(path, payload)
    }
    directories = {
        "/".join(PurePosixPath(path).parts[:index])
        for path in tracked
        for index in range(1, len(PurePosixPath(path).parts))
    }
    basenames: dict[str, list[str]] = {}
    for path in tracked:
        basenames.setdefault(PurePosixPath(path).name, []).append(path)
    modules = module_index(tracked)
    commits = last_commit_map(repo, base, tracked)
    print(f"R0_SCAN phase=metadata commits={len(commits)}", flush=True)

    edges: list[dict[str, Any]] = []
    edge_keys: set[tuple[Any, ...]] = set()

    def add_edge(
        source: str,
        line: int | str,
        category: str,
        kind: str,
        raw_target: str,
        resolved_target: str,
        status: str,
        detail: str = "",
    ) -> None:
        key = (source, line, category, kind, raw_target, resolved_target, status, detail)
        if key in edge_keys:
            return
        edge_keys.add(key)
        edges.append(
            {
                "source": source,
                "line": line,
                "category": category,
                "kind": kind,
                "raw_target": raw_target.replace("\t", "\\t").replace("\n", "\\n"),
                "resolved_target": resolved_target,
                "status": status,
                "detail": detail or "-",
            }
        )

    # Exact textual references to base-root filenames.
    alternation = "|".join(re.escape(path) for path in sorted(root_paths, key=len, reverse=True))
    root_reference_pattern = re.compile(
        rf"(?<![A-Za-z0-9_.-])(?P<target>{alternation})(?![A-Za-z0-9_.-])"
    )
    for source, text in texts.items():
        first_hits: dict[str, int] = {}
        for match in root_reference_pattern.finditer(text):
            first_hits.setdefault(match.group("target"), match.start())
        for target, position in first_hits.items():
            add_edge(
                source,
                line_number(text, position),
                "TEXT_REFERENCE",
                "TEXT_REFERENCE",
                target,
                target,
                "RESOLVED_TRACKED",
            )
    print(f"R0_SCAN phase=text-references edges={len(edges)}", flush=True)

    # Python imports and static/dynamic file-path calls.
    for source, text in texts.items():
        if not source.endswith(".py"):
            continue
        try:
            tree = ast.parse(text, filename=source)
        except SyntaxError as exc:
            add_edge(
                source,
                exc.lineno or "",
                "PYTHON_IMPORT",
                "PY_PARSE_ERROR",
                exc.msg,
                "",
                "UNRESOLVED",
            )
            continue
        is_test = source.startswith("tests/")
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    resolved, status = resolve_import(alias.name, source, modules)
                    add_edge(
                        source,
                        node.lineno,
                        "PYTHON_IMPORT",
                        "PY_IMPORT",
                        alias.name,
                        resolved,
                        status,
                    )
                    if is_test:
                        add_edge(
                            source,
                            node.lineno,
                            "TEST",
                            "TEST_IMPORT",
                            alias.name,
                            resolved,
                            status,
                        )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                resolved, status = resolve_import(module, source, modules, node.level)
                add_edge(
                    source,
                    node.lineno,
                    "PYTHON_IMPORT",
                    "PY_FROM_IMPORT",
                    "." * node.level + module,
                    resolved,
                    status,
                    ",".join(alias.name for alias in node.names),
                )
                if is_test:
                    add_edge(
                        source,
                        node.lineno,
                        "TEST",
                        "TEST_FROM_IMPORT",
                        "." * node.level + module,
                        resolved,
                        status,
                    )
            elif isinstance(node, ast.Call):
                name = function_name(node.func)
                final_name = name.split(".")[-1] if name else ""
                if name in FILE_CALLS or final_name in PATH_METHODS:
                    values: list[str] = []
                    dynamic = False
                    for argument in node.args:
                        literal = literal_string(argument)
                        if literal is None:
                            dynamic = True
                            try:
                                values.append(ast.unparse(argument))
                            except Exception:
                                values.append("<dynamic-expression>")
                        else:
                            values.append(literal)
                    if name == "os.path.join" and values and not dynamic:
                        raw_target = "/".join(value.strip("/") for value in values)
                    elif values:
                        raw_target = values[0]
                    else:
                        try:
                            raw_target = ast.unparse(node.func)
                        except Exception:
                            raw_target = name or "<dynamic-call>"
                        dynamic = True
                    if dynamic or raw_target.startswith(("f'", 'f"')):
                        resolved, status = raw_target, "DYNAMIC"
                    else:
                        resolved, status = resolve_target(
                            raw_target, source, tracked, directories, basenames
                        )
                    add_edge(
                        source,
                        node.lineno,
                        "FILE_PATH",
                        "FILE_PATH_CALL",
                        raw_target,
                        resolved,
                        status,
                        name,
                    )
                    if is_test:
                        add_edge(
                            source,
                            node.lineno,
                            "TEST",
                            "TEST_PATH_CALL",
                            raw_target,
                            resolved,
                            status,
                            name,
                        )
            elif is_test and isinstance(node, ast.Constant) and isinstance(node.value, str):
                if looks_pathlike(node.value):
                    resolved, status = resolve_target(
                        node.value, source, tracked, directories, basenames
                    )
                    add_edge(
                        source,
                        getattr(node, "lineno", ""),
                        "TEST",
                        "TEST_LITERAL",
                        node.value,
                        resolved,
                        status,
                    )
    print(f"R0_SCAN phase=python edges={len(edges)}", flush=True)

    # Markdown links and wiki links.
    markdown_pattern = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
    wiki_pattern = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
    for source, text in texts.items():
        if not source.endswith((".md", ".rst")):
            continue
        for match in markdown_pattern.finditer(text):
            raw_target = match.group(1)
            resolved, status = resolve_target(raw_target, source, tracked, directories, basenames)
            add_edge(
                source,
                line_number(text, match.start()),
                "MARKDOWN_LINK",
                "MARKDOWN_LINK",
                raw_target,
                resolved,
                status,
            )
        for match in wiki_pattern.finditer(text):
            raw_target = match.group(1)
            resolved, status = resolve_target(raw_target, source, tracked, directories, basenames)
            add_edge(
                source,
                line_number(text, match.start()),
                "MARKDOWN_LINK",
                "WIKI_LINK",
                raw_target,
                resolved,
                status,
            )
    print(f"R0_SCAN phase=markdown edges={len(edges)}", flush=True)

    # SHA-256 and JSON manifests.
    sha_row = re.compile(r"^([0-9a-fA-F]{64})\s{2,}(.+)$")
    for source, text in texts.items():
        basename = PurePosixPath(source).name
        if "SHA256SUMS" in basename or "sha256" in basename.lower():
            for number, row in enumerate(text.splitlines(), start=1):
                match = sha_row.match(row)
                if not match:
                    continue
                raw_target = match.group(2)
                resolved, status = resolve_target(
                    raw_target, source, tracked, directories, basenames
                )
                add_edge(
                    source,
                    number,
                    "MANIFEST",
                    "MANIFEST_SHA256",
                    raw_target,
                    resolved,
                    status,
                    match.group(1).lower(),
                )
        if source.endswith(".json") and "manifest" in basename.lower():
            try:
                document = json.loads(text)
            except json.JSONDecodeError as exc:
                add_edge(
                    source,
                    exc.lineno,
                    "MANIFEST",
                    "MANIFEST_PARSE_ERROR",
                    exc.msg,
                    "",
                    "UNRESOLVED",
                )
                continue

            def visit_json(value: Any, locator: str = "$") -> None:
                if isinstance(value, dict):
                    for key, child in value.items():
                        if isinstance(key, str) and looks_pathlike(key):
                            resolved, status = resolve_target(
                                key, source, tracked, directories, basenames
                            )
                            add_edge(
                                source,
                                "",
                                "MANIFEST",
                                "MANIFEST_JSON_KEY",
                                key,
                                resolved,
                                status,
                                locator,
                            )
                        visit_json(child, f"{locator}.{key}")
                elif isinstance(value, list):
                    for child_index, child in enumerate(value):
                        visit_json(child, f"{locator}[{child_index}]")
                elif isinstance(value, str) and looks_pathlike(value):
                    resolved, status = resolve_target(
                        value, source, tracked, directories, basenames
                    )
                    add_edge(
                        source,
                        "",
                        "MANIFEST",
                        "MANIFEST_JSON_VALUE",
                        value,
                        resolved,
                        status,
                        locator,
                    )

            visit_json(document)
    print(f"R0_SCAN phase=manifests edges={len(edges)}", flush=True)

    # Startup instructions: path-like tokens and backtick-delimited paths.
    startup_token = re.compile(
        r"(?:[A-Za-z0-9_.{}*,-]+/)*[A-Za-z0-9_.{}*,-]+"
        r"\.(?:cfg|csv|ini|json|log|md|npy|npz|pt|py|sh|toml|tsv|txt|yaml|yml)"
    )
    backtick = re.compile(r"`([^`\n]+)`")
    for source in sorted(STARTUP_SOURCES & set(texts)):
        text = texts[source]
        candidates: list[tuple[int, str]] = []
        candidates.extend((match.start(), match.group(0)) for match in startup_token.finditer(text))
        for match in backtick.finditer(text):
            value = match.group(1).strip()
            if looks_pathlike(value) or ("/" in value and " " not in value):
                candidates.append((match.start(), value))
        seen_startup: set[tuple[int, str]] = set()
        for position, raw_target in candidates:
            key = (line_number(text, position), raw_target)
            if key in seen_startup:
                continue
            seen_startup.add(key)
            resolved, status = resolve_target(raw_target, source, tracked, directories, basenames)
            add_edge(
                source,
                key[0],
                "STARTUP",
                "STARTUP_REFERENCE",
                raw_target,
                resolved,
                status,
            )
    print(f"R0_SCAN phase=startup edges={len(edges)}", flush=True)

    edges.sort(
        key=lambda row: (
            row["source"],
            int(row["line"]) if str(row["line"]).isdigit() else -1,
            row["category"],
            row["kind"],
            row["raw_target"],
        )
    )

    textual_inbound: dict[str, set[str]] = {path: set() for path in root_paths}
    dependency_inbound: dict[str, set[str]] = {path: set() for path in root_paths}
    startup_targets: set[str] = set()
    manifest_targets: set[str] = set()
    live_code_targets: set[str] = set()
    for edge in edges:
        resolved_targets = edge["resolved_target"].split("|")
        for target in resolved_targets:
            if target in root_paths:
                dependency_inbound[target].add(edge["kind"])
                if edge["kind"] == "TEXT_REFERENCE":
                    textual_inbound[target].add(edge["source"])
                if edge["category"] == "STARTUP" and edge["status"].startswith("RESOLVED"):
                    startup_targets.add(target)
                if edge["category"] == "MANIFEST" and edge["status"].startswith("RESOLVED"):
                    manifest_targets.add(target)
                if edge["category"] in {"PYTHON_IMPORT", "TEST"} and edge["status"].startswith(
                    "RESOLVED"
                ):
                    live_code_targets.add(target)

    def classify(path: str, text: str) -> tuple[str, str]:
        suffix = PurePosixPath(path).suffix.lower()
        lowered = path.lower()
        upper = path.upper()
        if path in CONTROL_ROOT:
            return "CONTROL", "startup/governance/configuration root"
        if (
            path.startswith("UDT_NATIVE_ACTION_")
            or path.startswith("UDT_GR_TO_UDT_SELECTOR_AUDIT")
            or path.startswith("UDT_WORKSTATION_TRANSFER_")
            or path.startswith("CODEX_STARTUP_REHEARSAL_")
            or path.startswith("codex_rehearsal_")
        ):
            return "FROZEN_EVIDENCE", "accepted dispatch/return/audit provenance record"
        if path.startswith(
            (
                "UDT_COMMON_SCALE_NEUTRALITY_",
                "UDT_GLOBAL_BOOTSTRAP_",
                "UDT_RECIPROCAL_C_",
                "UDT_S2_CARRIER_STATUS_",
                "UDT_XMAX_STATUS_",
            )
        ):
            return "ACTIVE", "current owner/foundation ledger named by startup wildcard"
        if path in startup_targets or path in live_code_targets:
            return "ACTIVE", "resolved startup/test/import dependency"
        if path in manifest_targets or "manifest" in lowered:
            return "FROZEN_EVIDENCE", "manifest or manifest-listed evidence"
        if re.search(
            r"(?im)^(?:>\s*)?(?:#{1,6}\s*)?[\[(]?(?:\*\*)?"
            r"(?:STATUS\s*[:=-]\s*)?(?:SUPERSEDED|RETRACTED|ARCHIVED)\b",
            text[:800],
        ):
            return "ARCHIVE_CANDIDATE", "document-level superseded/retracted/archive marker; audit required"
        if any(token in upper for token in ("RETURN", "TRANSCRIPT", "LAUNCH_RECORD", "SHA256SUMS")):
            return "FROZEN_EVIDENCE", "return/transcript/launch/hash evidence record"
        if lowered.endswith(("_results.md", "_result.md")):
            return "FROZEN_EVIDENCE", "research result record; preserve until provenance audit"
        if suffix in {".py", ".sh"}:
            return "MOVE_CANDIDATE", "code/tool family not root-pinned by resolved live edges"
        if suffix in {".md", ".rst", ".tex"}:
            return "MOVE_CANDIDATE", "documentation suitable for later grouped relocation"
        if suffix in {".json", ".csv", ".log", ".npy", ".npz", ".pt", ".tsv", ".txt"}:
            if textual_inbound[path]:
                return "FROZEN_EVIDENCE", "referenced artifact/evidence; path provenance must be preserved"
            return "UNKNOWN/BLOCKED", "data/evidence object lacks sufficient move provenance"
        return "UNKNOWN/BLOCKED", "no conservative R0 rule resolves role"

    inventory_rows: list[dict[str, Any]] = []
    for entry in sorted(root_entries, key=lambda item: item.path):
        payload = blobs[entry.path]
        commit, commit_date, subject = commits[entry.path]
        classification, basis = classify(entry.path, texts.get(entry.path, ""))
        if classification not in CLASSIFICATIONS:
            raise RuntimeError(f"bad classification for {entry.path}: {classification}")
        references = sorted(textual_inbound[entry.path])
        inventory_rows.append(
            {
                "path": entry.path,
                "git_mode": entry.mode,
                "git_blob_oid": entry.oid,
                "sha256": sha256(payload),
                "size_bytes": len(payload),
                "last_commit": commit,
                "last_commit_date": commit_date,
                "last_commit_subject": subject.replace("\t", " "),
                "reference_count": len(references),
                "referenced_by": ";".join(references),
                "dependency_kinds": ";".join(sorted(dependency_inbound[entry.path])),
                "classification": classification,
                "classification_basis": basis,
            }
        )

    dirty_rows = parse_dirty_status(arguments.dirty_checkout.resolve())
    frozen_results = verify_frozen_manifests(repo)
    print(
        f"R0_SCAN phase=outputs inventory={len(inventory_rows)} dirty={len(dirty_rows)}",
        flush=True,
    )
    tree_digest_payload = b"".join(
        entry.path.encode("utf-8", "surrogateescape")
        + b"\0"
        + entry.oid.encode()
        + b"\n"
        for entry in sorted(entries, key=lambda item: item.path)
    )
    categories = sorted({edge["category"] for edge in edges})
    status_counts: dict[str, int] = {}
    category_counts: dict[str, int] = {}
    classification_counts: dict[str, int] = {}
    for edge in edges:
        status_counts[edge["status"]] = status_counts.get(edge["status"], 0) + 1
        category_counts[edge["category"]] = category_counts.get(edge["category"], 0) + 1
    for row in inventory_rows:
        classification_counts[row["classification"]] = (
            classification_counts.get(row["classification"], 0) + 1
        )

    write_tsv(
        output_dir / "ROOT_FILE_INVENTORY.tsv",
        inventory_rows,
        [
            "path",
            "git_mode",
            "git_blob_oid",
            "sha256",
            "size_bytes",
            "last_commit",
            "last_commit_date",
            "last_commit_subject",
            "reference_count",
            "referenced_by",
            "dependency_kinds",
            "classification",
            "classification_basis",
        ],
    )
    write_tsv(
        output_dir / "DEPENDENCY_MAP.tsv",
        edges,
        [
            "source",
            "line",
            "category",
            "kind",
            "raw_target",
            "resolved_target",
            "status",
            "detail",
        ],
    )
    write_tsv(
        output_dir / "DIRTY_WORKSTATION_INVENTORY.tsv",
        dirty_rows,
        [
            "path",
            "status",
            "kind",
            "object_type",
            "size_bytes_lstat",
            "mode_lstat",
            "original_path",
            "content_sha256",
            "firewall",
        ],
    )
    summary = {
        "result": "GENERATED",
        "date": "2026-07-18",
        "base_commit": base,
        "base_tree_entries": len(entries),
        "base_tree_path_oid_sha256": sha256(tree_digest_payload),
        "base_root_file_count": len(root_entries),
        "root_inventory_rows": len(inventory_rows),
        "classification_counts": dict(sorted(classification_counts.items())),
        "dependency_edge_count": len(edges),
        "dependency_categories": categories,
        "dependency_category_counts": dict(sorted(category_counts.items())),
        "dependency_status_counts": dict(sorted(status_counts.items())),
        "dirty_workstation_checkout": str(arguments.dirty_checkout.resolve()),
        "dirty_workstation_rows": len(dirty_rows),
        "dirty_content_policy": "NOT_READ; git status plus lstat only",
        "frozen_packages": frozen_results,
        "scope": "base-snapshot tracked root files plus static dependency edges",
        "limitations": [
            "dynamic runtime path values are surfaced but not guessed",
            "static imports do not prove runtime execution",
            "classification is an R0 proposal, not move authorization",
            "R0-generated files are outside the self-referential base census",
        ],
    }
    (output_dir / "SCAN_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
