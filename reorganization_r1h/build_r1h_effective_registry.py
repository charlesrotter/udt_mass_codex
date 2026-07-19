#!/usr/bin/env python3
"""Deterministically build the R1H effective registry and B02/B03 closure table."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import subprocess
from collections import Counter
from pathlib import Path


BASE = "2058f69db3f5c3a4322c5a9404e7145a62eeef2d"
INPUT_HASHES = {
    "research/_registry/ROOT_OWNERSHIP.tsv": "4e8a4e82d4698f24dea7510932a919773267dfad3ad4033999e195044a056edc",
    "research/_registry/MIGRATION_READINESS.tsv": "4fbdb4e71aae4caf18df9142e7ab822bb5b348b3b364b72e97707679bd244062",
    "research/_registry/CURRENT_ARTIFACT_PATHS.tsv": "9c1f7c9a9f11dbf31706268d5dbd3c2ffd4247e3f981a603d86e2095925e729c",
    "research/_registry/CURRENT_FRONTIER_TARGETS.tsv": "5ad9408676d788063165d5b41d6e4002d81f157c2b2a22a5dd23714740d2ec61",
    "reorganization_r1g/AFFECTED_CASCADE_FILE_CENSUS.tsv": "d44c2b8b55c3e16350dec8ce55349426e57cce4d1035859e29898c9fa0736c9d",
    "reorganization_r1g/B02_B03_ADJUDICATION.tsv": "cbae13c1d79f3d16a2c6542dfe003559fd3abadffb1d56e8490fdecc3070de11",
    "reorganization_r1g/READOUT_PROVENANCE_CORRECTION_AUDIT.tsv": "16f2237db4a3188e9668fa3f57cac265e473f9bbaddabf9f767a4fef5281252c",
    "reorganization_r1e/PROPOSED_BATCH_FILE_PLAN.tsv": "c9089c1885f2f618c12567885f1e3d416abeeaa026cd6c442cf7ae64ae70f82c",
}
REGISTRY_FIELDS = [
    "original_path",
    "current_path",
    "fixed_snapshot_owner",
    "fixed_snapshot_evidence",
    "effective_primary_owner",
    "operator_provenance",
    "imported_action_or_coupling",
    "comparison_readout",
    "role",
    "scientific_lifecycle",
    "path_migration_safety",
    "migration_review_status",
    "scientific_family",
    "adjudication_source",
    "review_status",
]
CLOSURE_FIELDS = [
    "batch_id",
    "original_path",
    "current_path",
    "introducing_commit",
    "operator_provenance",
    "imported_action_or_coupling",
    "comparison_readout",
    "role",
    "scientific_lifecycle",
    "scientific_family",
    "runtime_import_modules",
    "runtime_local_imports",
    "runtime_file_io",
    "introducing_commit_family_paths",
    "result_evidence_companions",
    "conceptual_operator_companions",
    "frozen_or_manifest_bound_companions",
    "current_control_frontier_companions",
    "atomic_family_current_paths",
    "standalone_move_safe",
    "closure_ruling",
    "execution_batch_status",
    "adjudication_source",
    "review_status",
    "ruling_basis",
]
PROVENANCE_FIELDS = (
    "operator_provenance",
    "imported_action_or_coupling",
    "comparison_readout",
    "role",
    "scientific_lifecycle",
    "primary_owner",
)


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def render_tsv(fields: list[str], records: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer,
        fieldnames=fields,
        delimiter="\t",
        lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(records)
    return buffer.getvalue().encode("utf-8")


def git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {completed.stderr}")
    return completed.stdout


def joined(values: list[str] | set[str]) -> str:
    clean = sorted({value for value in values if value})
    return ";".join(clean) if clean else "NONE"


def runtime_audit(repo: Path, path: str) -> tuple[str, str, str]:
    tree = ast.parse((repo / path).read_text(encoding="utf-8"), filename=path)
    modules: set[str] = set()
    local: set[str] = set()
    io_calls: set[str] = set()
    io_attributes = {
        "load", "save", "loadtxt", "savetxt", "fromfile", "tofile",
        "read_text", "write_text", "read_bytes", "write_bytes", "open",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".", 1)[0])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "open":
                io_calls.add("open")
            elif isinstance(node.func, ast.Attribute) and node.func.attr in io_attributes:
                io_calls.add(node.func.attr)
    for module in modules:
        if (repo / f"{module}.py").exists() or (repo / module).is_dir():
            local.add(module)
    return joined(modules), joined(local), joined(io_calls)


def resolve_historical_path(
    repo: Path,
    original: str,
    current_by_original: dict[str, str],
    tracked_by_basename: dict[str, list[str]],
) -> str:
    if original in current_by_original:
        return current_by_original[original]
    if (repo / original).exists():
        return original
    matches = tracked_by_basename.get(Path(original).name, [])
    if len(matches) != 1:
        raise AssertionError(f"cannot uniquely resolve historical companion {original}: {matches}")
    return matches[0]


def immutable_or_manifest_bound(
    original: str,
    current: str,
    ownership: dict[str, dict[str, str]],
    readiness: dict[str, dict[str, str]],
    original_by_current: dict[str, str],
) -> bool:
    stable = original if original in ownership else original_by_current.get(current, "")
    own = ownership.get(stable, {})
    ready = readiness.get(stable, {})
    frozen = own.get("frozen_manifest_status", "")
    frozen_bound = frozen != "NOT_FROZEN_OR_MANIFEST" and (
        "R0_FROZEN_EVIDENCE" in frozen
        or "REFERENCED_BY_SIX_FROZEN_PACKAGES" in frozen
        or "MANIFEST_EDGE_TARGET" in frozen
    )
    return (
        ready.get("migration_readiness") == "IMMUTABLE_PATH"
        or frozen_bound
    )


def build(repo: Path) -> tuple[bytes, bytes, dict[str, object]]:
    if git(repo, "rev-parse", BASE).strip() != BASE:
        raise AssertionError("fixed base is unavailable")
    for relative, expected in INPUT_HASHES.items():
        observed = sha((repo / relative).read_bytes())
        if observed != expected:
            raise AssertionError(f"frozen input hash mismatch: {relative}: {observed}")

    current = read_rows(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    ownership_rows = read_rows(repo / "research/_registry/ROOT_OWNERSHIP.tsv")
    readiness_rows = read_rows(repo / "research/_registry/MIGRATION_READINESS.tsv")
    affected = read_rows(repo / "reorganization_r1g/AFFECTED_CASCADE_FILE_CENSUS.tsv")
    candidates = read_rows(repo / "reorganization_r1g/B02_B03_ADJUDICATION.tsv")
    definitions = json.loads(
        (repo / "reorganization_r1h/SCIENTIFIC_FAMILY_DEFINITIONS.json").read_text(encoding="utf-8")
    )["families"]

    originals = [row["original_path"] for row in current]
    current_paths = [row["current_path"] for row in current]
    if len(current) != 1114 or len(set(originals)) != 1114 or len(set(current_paths)) != 1114:
        raise AssertionError("stable identity/current-path universe is not exactly 1,114 unique rows")
    missing_current = [path for path in current_paths if not (repo / path).exists()]
    if missing_current:
        raise AssertionError(f"missing current artifact: {missing_current[0]}")

    current_by_original = {row["original_path"]: row["current_path"] for row in current}
    original_by_current = {row["current_path"]: row["original_path"] for row in current}
    ownership = {row["current_path"]: row for row in ownership_rows}
    readiness = {row["current_path"]: row for row in readiness_rows}
    if set(ownership) != set(originals) or set(readiness) != set(originals):
        raise AssertionError("fixed snapshot coverage does not match stable identity universe")

    affected_by_path = {row["current_path"]: row for row in affected}
    candidate_by_path = {row["current_path"]: row for row in candidates}
    if len(affected_by_path) != 121 or len(candidate_by_path) != 32:
        raise AssertionError("R1G input coverage mismatch")
    overlap = set(affected_by_path) & set(candidate_by_path)
    union = set(affected_by_path) | set(candidate_by_path)
    if len(overlap) != 19 or len(union) != 134:
        raise AssertionError(f"R1G union/overlap mismatch: {len(union)}/{len(overlap)}")
    if not union <= set(originals):
        raise AssertionError("R1G override lacks stable identity")
    for path in overlap:
        if any(affected_by_path[path][field] != candidate_by_path[path][field] for field in PROVENANCE_FIELDS):
            raise AssertionError(f"R1G overlap disagrees on provenance axes: {path}")

    definition_candidates = [path for family in definitions for path in family["candidate_paths"]]
    if len(definition_candidates) != 32 or len(set(definition_candidates)) != 32 or set(definition_candidates) != set(candidate_by_path):
        raise AssertionError("scientific-family definition coverage is missing or duplicate")

    tracked = git(repo, "ls-files").splitlines()
    tracked_by_basename: dict[str, list[str]] = {}
    for path in tracked:
        tracked_by_basename.setdefault(Path(path).name, []).append(path)

    closure_records: list[dict[str, str]] = []
    family_by_candidate: dict[str, dict[str, object]] = {}
    for family in definitions:
        commit = family["introducing_commit"]
        commit_originals = [
            path for path in git(repo, "show", "--format=", "--name-only", commit).splitlines() if path
        ]
        commit_current = {
            original: resolve_historical_path(repo, original, current_by_original, tracked_by_basename)
            for original in commit_originals
        }
        external_originals = list(family["external_conceptual_original_paths"])
        external_current = {
            original: resolve_historical_path(repo, original, current_by_original, tracked_by_basename)
            for original in external_originals
        }
        result_originals = list(family["result_evidence_original_paths"])
        result_current = {
            original: resolve_historical_path(repo, original, current_by_original, tracked_by_basename)
            for original in result_originals
        }

        all_pairs = {**commit_current, **external_current}
        controls: list[str] = []
        scientific: list[str] = []
        for original, current_path in all_pairs.items():
            stable = original if original in ownership else original_by_current.get(current_path, "")
            own = ownership.get(stable, {})
            if own.get("primary_owner") == "CONTROL_ROOT" or own.get("current_frontier_target") == "YES":
                controls.append(current_path)
            else:
                scientific.append(current_path)

        immutable: list[str] = []
        for original, current_path in all_pairs.items():
            if current_path in scientific and immutable_or_manifest_bound(
                original, current_path, ownership, readiness, original_by_current
            ):
                immutable.append(current_path)
        if not immutable:
            raise AssertionError(f"family has no immutable scientific companion: {family['family_id']}")

        for candidate_path in family["candidate_paths"]:
            candidate = candidate_by_path[candidate_path]
            resolved_candidate = current_by_original[candidate_path]
            modules, local_imports, file_io = runtime_audit(repo, resolved_candidate)
            conceptual = [path for path in scientific if path != resolved_candidate]
            immutable_companions = [path for path in immutable if path != resolved_candidate]
            if not immutable_companions:
                raise AssertionError(f"candidate lacks immutable companion: {candidate_path}")
            basis = (
                f"Runtime closure is {local_imports}/{file_io}; scientific family {family['family_id']} "
                f"contains immutable companion(s) {joined(immutable_companions)}. Moving only this script "
                "would split the recorded derivation/verifier from required frozen result or provenance evidence."
            )
            record = {
                "batch_id": candidate["batch_id"],
                "original_path": candidate_path,
                "current_path": resolved_candidate,
                "introducing_commit": commit,
                "operator_provenance": candidate["operator_provenance"],
                "imported_action_or_coupling": candidate["imported_action_or_coupling"],
                "comparison_readout": candidate["comparison_readout"],
                "role": candidate["role"],
                "scientific_lifecycle": candidate["scientific_lifecycle"],
                "scientific_family": family["family_id"],
                "runtime_import_modules": modules,
                "runtime_local_imports": local_imports,
                "runtime_file_io": file_io,
                "introducing_commit_family_paths": joined(list(commit_current.values())),
                "result_evidence_companions": joined(list(result_current.values())),
                "conceptual_operator_companions": joined(conceptual),
                "frozen_or_manifest_bound_companions": joined(immutable_companions),
                "current_control_frontier_companions": joined(controls),
                "atomic_family_current_paths": joined(scientific),
                "standalone_move_safe": "NO",
                "closure_ruling": "BLOCKED_IMMUTABLE_FAMILY_COMPANION",
                "execution_batch_status": "WITHDRAWN_NO_EXECUTION_AUTHORITY",
                "adjudication_source": "R1G_PROVENANCE+R1H_SCIENTIFIC_FAMILY_CLOSURE",
                "review_status": "R1H_SCIENTIFIC_FAMILY_REVIEWED",
                "ruling_basis": basis,
            }
            closure_records.append(record)
            family_by_candidate[candidate_path] = record

    closure_records.sort(key=lambda row: (row["batch_id"], row["original_path"]))

    registry_records: list[dict[str, str]] = []
    for identity in current:
        original = identity["original_path"]
        own = ownership[original]
        ready = readiness[original]
        base_record = {
            "original_path": original,
            "current_path": identity["current_path"],
            "fixed_snapshot_owner": own["primary_owner"],
            "fixed_snapshot_evidence": own["ownership_evidence"],
        }
        if original not in union:
            record = {
                **base_record,
                "effective_primary_owner": own["primary_owner"],
                "operator_provenance": "INHERITED_UNREVIEWED",
                "imported_action_or_coupling": "INHERITED_UNREVIEWED",
                "comparison_readout": "INHERITED_UNREVIEWED",
                "role": "INHERITED_UNREVIEWED",
                "scientific_lifecycle": "INHERITED_UNREVIEWED",
                "path_migration_safety": f"INHERITED_UNREVIEWED:{ready['migration_readiness']}",
                "migration_review_status": "INHERITED_UNREVIEWED",
                "scientific_family": "INHERITED_UNREVIEWED",
                "adjudication_source": "R1C_FIXED_SNAPSHOT_INHERITANCE",
                "review_status": "INHERITED_UNREVIEWED",
            }
        else:
            source = candidate_by_path.get(original, affected_by_path.get(original))
            assert source is not None
            if original in candidate_by_path:
                closure = family_by_candidate[original]
                family_name = closure["scientific_family"]
                migration = closure["closure_ruling"]
                migration_review = "FAMILY_REVIEWED_BLOCKED"
                review = "R1H_SCIENTIFIC_FAMILY_REVIEWED"
                layers = ["R1G:B02_B03_ADJUDICATION.tsv", "R1H:B02_B03_SCIENTIFIC_FAMILY_CLOSURE.tsv"]
                if original in affected_by_path:
                    layers.insert(0, "R1G:AFFECTED_CASCADE_FILE_CENSUS.tsv")
                adjudication = "+".join(layers)
            else:
                family_name = source["family_id"]
                migration = source["migration_safety"]
                if migration == "BLOCKED_PROVENANCE_CORRECTION_REQUIRED":
                    migration = "BLOCKED_SCIENTIFIC_FAMILY_REVIEW_REQUIRED"
                    migration_review = "FAMILY_REVIEW_REQUIRED"
                elif migration == "IMMUTABLE_PATH_RETAIN":
                    migration_review = "IMMUTABLE_PATH"
                else:
                    raise AssertionError(
                        f"unexpected non-candidate R1G migration state: {original}:{migration}"
                    )
                review = "R1G_ADJUDICATED"
                adjudication = "R1G:AFFECTED_CASCADE_FILE_CENSUS.tsv"
            record = {
                **base_record,
                "effective_primary_owner": source["primary_owner"],
                "operator_provenance": source["operator_provenance"],
                "imported_action_or_coupling": source["imported_action_or_coupling"],
                "comparison_readout": source["comparison_readout"],
                "role": source["role"],
                "scientific_lifecycle": source["scientific_lifecycle"],
                "path_migration_safety": migration,
                "migration_review_status": migration_review,
                "scientific_family": str(family_name),
                "adjudication_source": adjudication,
                "review_status": review,
            }
        registry_records.append(record)

    review_counts = Counter(row["review_status"] for row in registry_records)
    provenance_counts = Counter(row["operator_provenance"] for row in registry_records)
    migration_review_counts = Counter(row["migration_review_status"] for row in registry_records)
    closure_counts = Counter(row["closure_ruling"] for row in closure_records)
    family_counts = Counter(row["scientific_family"] for row in closure_records)
    if review_counts != Counter({
        "INHERITED_UNREVIEWED": 980,
        "R1G_ADJUDICATED": 102,
        "R1H_SCIENTIFIC_FAMILY_REVIEWED": 32,
    }):
        raise AssertionError(f"review counts mismatch: {review_counts}")
    if provenance_counts != Counter({
        "INHERITED_UNREVIEWED": 980,
        "NATIVE_2026-07-01": 131,
        "MIXED": 2,
        "OPEN": 1,
    }):
        raise AssertionError(f"provenance counts mismatch: {provenance_counts}")
    if migration_review_counts != Counter({
        "FAMILY_REVIEW_REQUIRED": 101,
        "FAMILY_REVIEWED_BLOCKED": 32,
        "IMMUTABLE_PATH": 1,
        "INHERITED_UNREVIEWED": 980,
    }):
        raise AssertionError(f"migration-review counts mismatch: {migration_review_counts}")
    if any(
        row["path_migration_safety"] == "BLOCKED_PROVENANCE_CORRECTION_REQUIRED"
        for row in registry_records
    ):
        raise AssertionError("stale provenance-correction migration state remains")
    if closure_counts != Counter({"BLOCKED_IMMUTABLE_FAMILY_COMPANION": 32}):
        raise AssertionError(f"closure counts mismatch: {closure_counts}")

    registry_bytes = render_tsv(REGISTRY_FIELDS, registry_records)
    closure_bytes = render_tsv(CLOSURE_FIELDS, closure_records)
    summary = {
        "base": BASE,
        "stable_identity_rows": len(registry_records),
        "unique_original_paths": len({row["original_path"] for row in registry_records}),
        "unique_current_paths": len({row["current_path"] for row in registry_records}),
        "r1g_affected_rows": len(affected_by_path),
        "r1g_b02_b03_rows": len(candidate_by_path),
        "r1g_overlap_rows": len(overlap),
        "r1g_union_rows": len(union),
        "review_status_counts": dict(sorted(review_counts.items())),
        "operator_provenance_counts": dict(sorted(provenance_counts.items())),
        "migration_review_status_counts": dict(sorted(migration_review_counts.items())),
        "closure_ruling_counts": dict(sorted(closure_counts.items())),
        "scientific_family_counts": dict(sorted(family_counts.items())),
        "b02_rows": sum(row["batch_id"].startswith("B02") for row in closure_records),
        "b03_rows": sum(row["batch_id"].startswith("B03") for row in closure_records),
        "execution_batches_withdrawn": [
            "B02_LEGACY_STANDALONE_ALGEBRA_A",
            "B03_LEGACY_STANDALONE_ALGEBRA_B",
        ],
        "registry_sha256": sha(registry_bytes),
        "closure_sha256": sha(closure_bytes),
    }
    return registry_bytes, closure_bytes, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    registry, closure, summary = build(repo)
    targets = {
        repo / "research/_registry/CURRENT_CLASSIFICATION.tsv": registry,
        repo / "reorganization_r1h/B02_B03_SCIENTIFIC_FAMILY_CLOSURE.tsv": closure,
    }
    if args.check:
        for path, expected in targets.items():
            if not path.exists() or path.read_bytes() != expected:
                raise AssertionError(f"generated output drift: {path.relative_to(repo)}")
    else:
        for path, payload in targets.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
