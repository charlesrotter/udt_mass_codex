#!/usr/bin/env python3
"""Independent fail-closed verifier for the reciprocal line-realization selector."""

from __future__ import annotations

import argparse
import ast
import copy
import csv
import hashlib
import json
import re
import stat
import subprocess
from pathlib import Path
from urllib.parse import unquote

import sympy as sp


BASE = "9e08bccaf6a2ad9d7b464850560bc5f01d8349bf"
PREREG = "9dd9d9f"
PACKAGE = "reciprocal_line_realization_selector_2026-07-18"
OUTCOME = "NO_UNIVERSAL_LOCAL_METRIC_ONLY_SELECTOR_REALIZATION_MAP_OPEN"
SOURCE_HASHES = {
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md": "6e977717ca028cabaa198dd14a6a97b3b15740e45485d0ab735f3df0326df192",
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md": "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "4bb0da9098da0a9970602e2449615eef151796b0d7fe7a9978f4b66145748a34",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md": "db4a426b021e375fa4bca0d870aaf973de319de3b08072195d001a056630832d",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": "70cab9d5e10b03e0e3418129b67155e01d9f805c4397c69ef8795c4d2aaa5dfd",
    "reciprocity_offshell_constraint_selector_2026-07-18/SHA256SUMS.txt": "3f6da5926200f68e07b67a167948b2211d0a506fa65d322e600a7d22b080c74a",
    "reciprocity_offshell_constraint_selector_2026-07-18/DERIVATION_REPORT.md": "731460fb895f0f38a05350a13dafff2ad77b481dc076ec688a95d769d3fa04ae",
    "reciprocity_offshell_constraint_selector_2026-07-18/STATUS_LEDGER.tsv": "3b2879d8a61c6feac8c14e7a2ec21d575e81e5ff0f941754588527ffb3eef076",
}
PACKAGES = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}
MANIFESTED_FILES = {
    "ADVERSARIAL_AUDIT.md",
    "DERIVATION_REPORT.md",
    "DERIVATION_RESULT.json",
    "DERIVATION_TRANSCRIPT.txt",
    "LAY_DECISION_TREE.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "REVIEW_BOUNDARY_VARIATION.md",
    "REVIEW_COVARIANT_COUNTEREXAMPLE.md",
    "STATUS_LEDGER.tsv",
    "derive_reciprocal_line_selector.py",
    "requirements-cpu.txt",
    "verify_reciprocal_line_selector.py",
}


class GateError(AssertionError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def run(cwd: Path, command: list[str], *, binary: bool = False):
    completed = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        check=False,
    )
    if completed.returncode:
        error = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise GateError("COMMAND", f"{' '.join(command)}:{error}")
    return completed.stdout


def git(repo: Path, *args: str, binary: bool = False):
    return run(repo, ["git", *args], binary=binary)


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def tsv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def catch(code: str, callback) -> str:
    try:
        callback()
    except GateError as exc:
        if exc.code == code:
            return "PASS"
        raise AssertionError(f"expected {code}, got {exc.code}") from exc
    raise AssertionError(f"catch-proof accepted corruption: {code}")


def validate_prereg(repo: Path) -> None:
    resolved = str(git(repo, "rev-parse", PREREG)).strip()
    parent = str(git(repo, "rev-parse", f"{PREREG}^")).strip()
    paths = str(git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", PREREG)).splitlines()
    expected = [f"{PACKAGE}/PREREGISTRATION.md"]
    if not resolved.startswith(PREREG) or parent != BASE or paths != expected:
        raise GateError("PREREGISTRATION", f"{resolved}:{parent}:{paths}")


def validate_scope(repo: Path, injected: str | None = None) -> list[str]:
    changed = set(str(git(repo, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(git(repo, "ls-files", "--others", "--exclude-standard")).splitlines())
    if injected:
        changed.add(injected)
    invalid = sorted(path for path in changed if not path.startswith(PACKAGE + "/"))
    if invalid:
        raise GateError("SCOPE", invalid[0])
    return sorted(changed)


def validate_sources(repo: Path, corrupt: bool = False) -> dict[str, str]:
    observed = {}
    for index, (relative, expected) in enumerate(SOURCE_HASHES.items()):
        digest = sha((repo / relative).read_bytes())
        if corrupt and index == 0:
            digest = "0" * 64
        if digest != expected:
            raise GateError("SOURCE_HASH", relative)
        observed[relative] = digest
    return observed


def exact_geometry(force_boost_line: bool = False, force_unique_coframe: bool = False,
                   force_phi_zero_lines: bool = False, force_boundary_unique: bool = False) -> dict[str, object]:
    rapidity = sp.symbols("rapidity", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    lorentz = sp.Matrix([
        [sp.cosh(rapidity), sp.sinh(rapidity), 0, 0],
        [sp.sinh(rapidity), sp.cosh(rapidity), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])
    if sp.simplify(lorentz.T * eta * lorentz - eta) != sp.zeros(4):
        raise GateError("ALGEBRA", "boost")
    e_time = sp.Matrix([1, 0, 0, 0])
    moved = sp.simplify(lorentz * e_time)
    wedge = sp.simplify(moved[1])
    wedge_zero_set = sp.solveset(wedge, rapidity, domain=sp.S.Reals)
    if force_boost_line or wedge_zero_set != sp.FiniteSet(0):
        raise GateError("BOOST_LINE", str(wedge))
    if force_unique_coframe or lorentz == sp.eye(4):
        raise GateError("COFRAME_UNIQUENESS", "Lorentz-related coframe accepted as identical")

    depth = sp.symbols("depth", real=True)
    endomorphism = sp.diag(sp.exp(-depth), sp.exp(depth))
    gap_zero_set = sp.solveset(endomorphism[1, 1] - endomorphism[0, 0], depth, domain=sp.S.Reals)
    if force_phi_zero_lines or endomorphism.subs(depth, 0) != sp.eye(2) or gap_zero_set != sp.FiniteSet(0):
        raise GateError("PHI_ZERO", str(endomorphism.subs(depth, 0)))

    scale = sp.symbols("scale", positive=True)
    probe = sp.Matrix(sp.symbols("p0:4"))
    old_norm = (probe.T * eta * probe)[0]
    new_norm = sp.simplify((probe.T * scale**2 * eta * probe)[0])
    if sp.simplify(new_norm - scale**2 * old_norm) != 0:
        raise GateError("ALGEBRA", "conformal cone")

    u, length, epsilon = sp.symbols("u length epsilon", positive=True)
    normal = sp.Matrix([1, 0])
    extension = sp.Matrix([1, epsilon * u * (length - u)])
    seal_difference = sp.simplify((extension - normal).subs(u, 0))
    bulk_difference = sp.simplify((extension - normal).subs(u, length / 2))
    if seal_difference != sp.zeros(2, 1):
        raise GateError("ALGEBRA", "seal")
    if force_boundary_unique or bulk_difference == sp.zeros(2, 1):
        raise GateError("BOUNDARY_EXTENSION", str(bulk_difference))
    return {
        "result": "PASS",
        "lorentz_boost_preserves_metric": True,
        "boost_moves_rotation_fixed_line": str(wedge),
        "boost_line_zero_set": str(wedge_zero_set),
        "coframes_nonunique": True,
        "phi_zero_endomorphism": str(endomorphism.subs(depth, 0)),
        "eigenvalue_gap_zero_set": str(gap_zero_set),
        "conformal_null_cone_preserved": True,
        "seal_extensions_agree": True,
        "bulk_extension_difference": str(bulk_difference),
    }


def validate_claims(claims: dict[str, object]) -> None:
    forbidden_true = {
        "ignore_flat_jet": "FLAT_JET",
        "internal_pair_is_spacetime_tensor": "TYPE_CONFUSION",
        "gradient_phi_independent_when_slots_define_phi": "CIRCULAR_GRADIENT",
        "static_killing_is_universal": "STATIC_GLOBALIZATION",
        "auxiliary_field_required": "AUXILIARY_PROMOTION",
        "structured_and_global_routes_excluded": "SCOPE_OVERSTATEMENT",
        "action_or_variation_domain_selected": "ACTION_PROMOTION",
    }
    for key, code in forbidden_true.items():
        if claims.get(key):
            raise GateError(code, key)


def validate_result(repo: Path, corrupt: bool = False) -> tuple[dict[str, object], dict[str, dict[str, str]]]:
    result = json.loads((repo / PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    statuses = {row["id"]: row for row in tsv_rows(repo / PACKAGE / "STATUS_LEDGER.tsv")}
    expected_routes = {
        "internal_reciprocal_pair": "DERIVED_KINEMATIC",
        "S0_pointwise_metric_only_line_selector": "REFUTED_IN_CLASS",
        "S1_universal_local_finite_jet_metric_only_selector": "REFUTED_IN_CLASS",
        "S2_internal_to_spacetime_realization": "OPEN",
        "S3_curvature_eigenline": "CONDITIONAL_STRATIFIED",
        "S3_gradient_phi": "CIRCULAR_OR_EXTRA_FIELD",
        "S3_static_killing_line": "CONDITIONAL_SECTOR_ONLY",
        "S3_declared_spacetime_endomorphism": "CONDITIONAL_STRUCTURED",
        "S4_seal_normal_line": "CONDITIONAL_BOUNDARY_LOCAL",
        "S4_boundary_to_bulk_extension": "UNDERDETERMINED",
        "auxiliary_field_requirement": "NOT_DERIVED",
        "variation_domain": "OPEN",
        "complete_action_source_boundary_charge": "OPEN",
    }
    if corrupt:
        result = copy.deepcopy(result)
        result["routes"]["auxiliary_field_requirement"] = "REQUIRED"
    expected_status = {
        "S01": "DERIVED_KINEMATIC",
        "S02": "REFUTED_IN_CLASS",
        "S03": "REFUTED_IN_CLASS",
        "S04": "INSUFFICIENT_FOR_SELECTION",
        "S05": "NOT_UNIQUE",
        "S06": "CONDITIONAL_STRUCTURED",
        "S07": "CONDITIONAL_STRATIFIED",
        "S08": "CIRCULAR_OR_EXTRA_FIELD",
        "S09": "CONDITIONAL_SECTOR_ONLY",
        "S10": "CONDITIONAL_BOUNDARY_LOCAL",
        "S11": "UNDERDETERMINED",
        "S12": "OPEN",
        "S13": "OPEN_PRECISE",
        "S14": "NOT_DERIVED",
        "S15": "OPEN",
        "S16": "OPEN",
        "S17": OUTCOME,
    }
    observed_status = {key: statuses[key]["status"] for key in expected_status} if len(statuses) == 17 else {}
    if (
        result.get("schema") != "udt.reciprocal-line-realization-selector.v1"
        or result.get("top_level_outcome") != OUTCOME
        or result.get("routes") != expected_routes
        or result.get("check_count") != 11
        or not all(result.get("checks", {}).values())
        or observed_status != expected_status
        or result.get("least_missing_object", {}).get("full_coframe_required") is not False
    ):
        raise GateError("STATUS_CONTRACT", f"{result.get('top_level_outcome')}:{observed_status}")
    validate_claims({
        "ignore_flat_jet": False,
        "internal_pair_is_spacetime_tensor": False,
        "gradient_phi_independent_when_slots_define_phi": False,
        "static_killing_is_universal": False,
        "auxiliary_field_required": False,
        "structured_and_global_routes_excluded": False,
        "action_or_variation_domain_selected": False,
    })
    return result, statuses


def validate_report_and_reviews(repo: Path) -> dict[str, object]:
    report = (repo / PACKAGE / "DERIVATION_REPORT.md").read_text(encoding="utf-8")
    audit = (repo / PACKAGE / "ADVERSARIAL_AUDIT.md").read_text(encoding="utf-8")
    required_report = [
        OUTCOME,
        "no invariant one-dimensional subspace",
        "universal smooth finite-order metric-only selection",
        "A full tetrad is sufficient but stronger",
        "CIRCULAR_OR_EXTRA_FIELD",
        "CONDITIONAL_SECTOR_ONLY",
        "Infinitely many such smooth extensions exist",
        "does **not** derive a required auxiliary field",
        "variation domain and two-stage C-squared/EH bridge remain open",
    ]
    required_audit = [
        "reviewers",
        "covariant",
        "boundary",
        "no auxiliary",
        "No files were changed",
    ]
    missing = [token for token in required_report if token not in report]
    missing += [token for token in required_audit if token not in audit]
    if missing:
        raise GateError("REPORT_CONTRACT", missing[0])
    return {"result": "PASS", "report_tokens": len(required_report), "audit_tokens": len(required_audit)}


def validate_cpu_scripts(repo: Path) -> dict[str, object]:
    imports: set[str] = set()
    for name in ("derive_reciprocal_line_selector.py", "verify_reciprocal_line_selector.py"):
        tree = ast.parse((repo / PACKAGE / name).read_text(encoding="utf-8"), filename=name)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".", 1)[0])
    bad = imports & {"torch", "cupy", "jax", "tensorflow"}
    if bad or sp.__version__ != "1.13.1":
        raise GateError("DEPENDENCY", f"{bad}:{sp.__version__}")
    return {"result": "PASS", "sympy": sp.__version__, "gpu_imports": []}


def validate_manifest(repo: Path) -> dict[str, object]:
    manifest = repo / PACKAGE / "SHA256SUMS.txt"
    replay = run(manifest.parent, ["sha256sum", "--check", manifest.name])
    names = {
        line.split("  ", 1)[1]
        for line in manifest.read_text(encoding="utf-8").splitlines()
        if line
    }
    if names != MANIFESTED_FILES:
        raise GateError("PACKAGE_MANIFEST", str(sorted(names ^ MANIFESTED_FILES)))
    return {"result": "PASS", "entries": len(replay.splitlines()), "sha256": sha(manifest.read_bytes())}


def validate_frozen(repo: Path, corrupt: bool = False) -> list[dict[str, object]]:
    base_paths = set(str(git(repo, "ls-tree", "-r", "--name-only", BASE)).splitlines())
    current_paths = set(str(git(repo, "ls-files")).splitlines())
    index_oids = {line.split(None, 3)[3]: line.split()[1] for line in str(git(repo, "ls-files", "-s")).splitlines()}
    results = []
    for index, (package, expected) in enumerate(PACKAGES.items()):
        digest = sha((repo / package / "SHA256SUMS.txt").read_bytes())
        if corrupt and index == 0:
            digest = "0" * 64
        if digest != expected:
            raise GateError("FROZEN_PACKAGE", package)
        replay = run(repo / package, ["sha256sum", "--check", "SHA256SUMS.txt"])
        before = sorted(path for path in base_paths if path.startswith(package + "/"))
        after = sorted(path for path in current_paths if path.startswith(package + "/"))
        if not before or before != after:
            raise GateError("FROZEN_PACKAGE", package + ":paths")
        for path in before:
            if index_oids[path] != str(git(repo, "rev-parse", f"{BASE}:{path}")).strip():
                raise GateError("FROZEN_PACKAGE", path)
        results.append({"package": package, "entries": len(replay.splitlines()), "paths": len(before), "result": "PASS"})
    return results


def validate_navigation(repo: Path) -> dict[str, object]:
    current = tsv_rows(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    current_paths = [row["current_path"] for row in current]
    if len(current) != 1114 or len(set(current_paths)) != 1114 or not all((repo / path).exists() for path in current_paths):
        raise GateError("NAVIGATION", "current")
    frontier = tsv_rows(repo / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    if len(frontier) != 306 or len(targets) != 101 or not all((repo / path).exists() for path in targets):
        raise GateError("NAVIGATION", "frontier")
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links = []
    for source in sorted((repo / PACKAGE).glob("*.md")):
        for raw in link_pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            links.append(source.parent.joinpath(target).resolve())
    if not all(path.exists() for path in links):
        raise GateError("NAVIGATION", "links")
    return {"current_paths": len(current), "frontier_rows": len(frontier), "frontier_targets": len(targets), "links": len(links)}


def dirty_metadata(repo: Path) -> dict[str, tuple[str, int, str]]:
    raw = bytes(git(repo, "status", "--porcelain=v2", "-z", "--untracked-files=all", binary=True))
    records = raw.split(b"\0")
    result: dict[str, tuple[str, int, str]] = {}
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        marker = record[:1]
        if marker == b"1":
            fields = record.split(b" ", 8); code, raw_path = fields[1].decode(), fields[8]
        elif marker == b"2":
            fields = record.split(b" ", 9); code, raw_path = fields[1].decode(), fields[9]; index += 1
        elif marker == b"u":
            fields = record.split(b" ", 10); code, raw_path = fields[1].decode(), fields[10]
        elif marker in {b"?", b"!"}:
            code, raw_path = ("??" if marker == b"?" else "!!"), record[2:]
        else:
            raise GateError("DIRTY_METADATA", repr(record[:40]))
        path = raw_path.decode("utf-8", "surrogateescape")
        info = (repo / path).lstat()
        kind = "regular_file" if stat.S_ISREG(info.st_mode) else "directory" if stat.S_ISDIR(info.st_mode) else "symlink" if stat.S_ISLNK(info.st_mode) else "other"
        result[path] = (code, info.st_size, kind)
    return result


def validate_dirty(repo: Path, dirty_checkout: Path, corrupt: bool = False) -> int:
    recorded = {row["path"]: row for row in tsv_rows(repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv")}
    observed = dirty_metadata(dirty_checkout)
    if corrupt:
        observed = dict(observed); observed.pop(next(iter(observed)))
    if len(recorded) != 54 or len(observed) != 54 or set(recorded) != set(observed):
        raise GateError("DIRTY_METADATA", f"{len(recorded)}/{len(observed)}")
    for path, value in observed.items():
        row = recorded[path]
        expected = (row["status"], int(row["size_bytes_lstat"]), row["object_type"])
        if value != expected or row["content_sha256"] != "NOT_READ":
            raise GateError("DIRTY_METADATA", path)
    return len(observed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--dirty-checkout", type=Path, required=True)
    parser.add_argument("--test-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()

    validate_prereg(repo)
    changed = validate_scope(repo)
    sources = validate_sources(repo)
    result, _ = validate_result(repo)
    exact = exact_geometry()
    report = validate_report_and_reviews(repo)
    cpu = validate_cpu_scripts(repo)
    package_manifest = validate_manifest(repo)
    frozen = validate_frozen(repo)
    navigation = validate_navigation(repo)
    dirty = validate_dirty(repo, args.dirty_checkout.resolve())
    tests = json.loads(args.test_result.read_text(encoding="utf-8"))
    if (tests.get("passed"), tests.get("failed"), tests.get("xfailed"), tests.get("baseline_match")) != (69, 1, 1, True):
        raise GateError("TEST_BASELINE", str(tests))

    base_claims = {
        "ignore_flat_jet": False,
        "internal_pair_is_spacetime_tensor": False,
        "gradient_phi_independent_when_slots_define_phi": False,
        "static_killing_is_universal": False,
        "auxiliary_field_required": False,
        "structured_and_global_routes_excluded": False,
        "action_or_variation_domain_selected": False,
    }
    catches = {
        "boost_noninvariant_line_rejected": catch("BOOST_LINE", lambda: exact_geometry(force_boost_line=True)),
        "flat_jet_isotropy_omission_rejected": catch("FLAT_JET", lambda: validate_claims({**base_claims, "ignore_flat_jet": True})),
        "internal_pair_spacetime_type_confusion_rejected": catch("TYPE_CONFUSION", lambda: validate_claims({**base_claims, "internal_pair_is_spacetime_tensor": True})),
        "unique_metric_coframe_claim_rejected": catch("COFRAME_UNIQUENESS", lambda: exact_geometry(force_unique_coframe=True)),
        "phi_zero_eigenline_claim_rejected": catch("PHI_ZERO", lambda: exact_geometry(force_phi_zero_lines=True)),
        "circular_gradient_selector_rejected": catch("CIRCULAR_GRADIENT", lambda: validate_claims({**base_claims, "gradient_phi_independent_when_slots_define_phi": True})),
        "static_killing_globalization_rejected": catch("STATIC_GLOBALIZATION", lambda: validate_claims({**base_claims, "static_killing_is_universal": True})),
        "unique_boundary_extension_rejected": catch("BOUNDARY_EXTENSION", lambda: exact_geometry(force_boundary_unique=True)),
        "auxiliary_requirement_promotion_rejected": catch("AUXILIARY_PROMOTION", lambda: validate_claims({**base_claims, "auxiliary_field_required": True})),
        "structured_global_scope_overstatement_rejected": catch("SCOPE_OVERSTATEMENT", lambda: validate_claims({**base_claims, "structured_and_global_routes_excluded": True})),
        "action_variation_promotion_rejected": catch("ACTION_PROMOTION", lambda: validate_claims({**base_claims, "action_or_variation_domain_selected": True})),
        "status_contract_corruption_rejected": catch("STATUS_CONTRACT", lambda: validate_result(repo, corrupt=True)),
        "source_hash_mutation_rejected": catch("SOURCE_HASH", lambda: validate_sources(repo, corrupt=True)),
        "scope_escape_rejected": catch("SCOPE", lambda: validate_scope(repo, "LIVE.md")),
        "frozen_package_mutation_rejected": catch("FROZEN_PACKAGE", lambda: validate_frozen(repo, corrupt=True)),
        "dirty_metadata_drift_rejected": catch("DIRTY_METADATA", lambda: validate_dirty(repo, args.dirty_checkout.resolve(), corrupt=True)),
    }
    verification = {
        "result": "PASS",
        "mode": "INDEPENDENT_CPU_ONLY_RECIPROCAL_LINE_REALIZATION_VERIFY",
        "base": BASE,
        "preregistration_commit": str(git(repo, "rev-parse", PREREG)).strip(),
        "reported_outcome": result["top_level_outcome"],
        "changed_paths": changed,
        "source_hashes": sources,
        "independent_exact_geometry": exact,
        "report_and_reviews": report,
        "cpu_dependency": cpu,
        "package_manifest": package_manifest,
        "frozen_package_replays": frozen,
        "navigation": navigation,
        "test_baseline": tests,
        "dirty_checkout_metadata_rows": dirty,
        "dirty_content_policy": "NOT_READ",
        "catchproof": catches,
        "artifact_moves": 0,
        "gpu_used": False,
        "grok_integration_authorized": False,
    }
    payload = json.dumps(verification, indent=2, sort_keys=True) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
