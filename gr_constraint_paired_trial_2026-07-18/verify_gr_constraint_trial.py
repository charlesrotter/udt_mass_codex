#!/usr/bin/env python3
"""Independent fail-closed verifier for the GR-constraint paired trial."""

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


BASE = "378eac0ae0b615f4e64828d50bbe5d7d027393c1"
PREREG = "3e1d8a3cb6cb9ea3589f75e55f93b7cececa0ea4"
PACKAGE = "gr_constraint_paired_trial_2026-07-18"
SOURCE_HASHES = {
    "bootstrap_variation_selector_2026-07-18/SHA256SUMS.txt": "cad3c4f0dccc1599c5b4ff48c6adafa32fb64b590e4ef4f0f6e20e5e96de9bed",
    "bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md": "05a84a7bfeca3d78c628a3a6a343463db11497d66c5889ac0590655728d056f9",
    "bootstrap_variation_selector_2026-07-18/STATUS_LEDGER.tsv": "d271b483a02e0732bbab7f597b59827810586894ea29a8717f3cfff3c87949e6",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "4bb0da9098da0a9970602e2449615eef151796b0d7fe7a9978f4b66145748a34",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md": "db4a426b021e375fa4bca0d870aaf973de319de3b08072195d001a056630832d",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": "70cab9d5e10b03e0e3418129b67155e01d9f805c4397c69ef8795c4d2aaa5dfd",
}
PACKAGES = {
    "native_action_stage1_2026-07-18/arm_A": "d72e8d6e1b4bc8682bd5518264a1a43a3b5f7b3b246b3d218ea6bfecc6927d19",
    "native_action_stage1_2026-07-18/arm_B": "a99937a8fbba57ac24f490c2974937718f7dfbc2f2f7dd7c960d57fc5e839b92",
    "native_action_stage2_2026-07-18/arm_A": "ad63ffacdd5282a35fe0aef62269464d987aa61b710a4d393d95836234fd670a",
    "native_action_stage2_2026-07-18/arm_B": "30b2a3863f1d16e3b3507b5d0bf10a6b5b59c1e54d769cacc53127cc676d6d45",
    "native_action_arm_c_2026-07-18": "99fc0d6c26aff24e43b8636d74f80e3486c56131590552308b47c1d107ed500f",
    "native_action_final_adjudication_2026-07-18": "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33",
}
REQUIRED_PACKAGE_FILES = {
    "ADVERSARIAL_AUDIT.md",
    "DERIVATION_REPORT.md",
    "DERIVATION_RESULT.json",
    "LAY_DECISION_TREE.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SHA256SUMS.txt",
    "STATUS_LEDGER.tsv",
    "derive_gr_constraint_trial.py",
    "requirements-cpu.txt",
    "verify_gr_constraint_trial.py",
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
    parent = str(git(repo, "rev-parse", f"{PREREG}^")).strip()
    paths = str(git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", PREREG)).splitlines()
    expected = [
        f"{PACKAGE}/PREMISE_LEDGER.tsv",
        f"{PACKAGE}/PREREGISTRATION.md",
        f"{PACKAGE}/requirements-cpu.txt",
    ]
    if parent != BASE or paths != expected:
        raise GateError("PREREGISTRATION", f"{parent}:{paths}")


def validate_scope(repo: Path, injected: str | None = None) -> list[str]:
    changed = set(str(git(repo, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(git(repo, "ls-files", "--others", "--exclude-standard")).splitlines())
    if injected:
        changed.add(injected)
    invalid = sorted(path for path in changed if not path.startswith(PACKAGE + "/"))
    if invalid:
        raise GateError("SCOPE", invalid[0])
    package_names = {Path(path).name for path in changed if path.startswith(PACKAGE + "/")}
    missing = REQUIRED_PACKAGE_FILES - package_names
    if missing:
        raise GateError("SCOPE", "missing:" + ",".join(sorted(missing)))
    return sorted(changed)


def validate_source_hashes(repo: Path, corrupt: bool = False) -> dict[str, str]:
    observed_hashes: dict[str, str] = {}
    for number, (relative, expected) in enumerate(SOURCE_HASHES.items()):
        observed = sha((repo / relative).read_bytes())
        if corrupt and number == 0:
            observed = "0" * 64
        if observed != expected:
            raise GateError("SOURCE_HASH", relative)
        observed_hashes[relative] = observed
    replay = run(repo / "bootstrap_variation_selector_2026-07-18", ["sha256sum", "--check", "SHA256SUMS.txt"])
    if len(replay.splitlines()) != 10:
        raise GateError("SOURCE_HASH", "prior bootstrap package replay")
    return observed_hashes


def independent_kkt_test(drop_multiplier_equation: bool = False) -> dict[str, object]:
    p, q, eta = sp.symbols("p q eta")
    base = sp.Function("F")(p, q)
    constraint = sp.Function("K")(p, q)
    augmented = base + eta * constraint
    observed = [sp.diff(augmented, p), sp.diff(augmented, q)]
    if not drop_multiplier_equation:
        observed.append(sp.diff(augmented, eta))
    expected = [
        sp.diff(base, p) + eta * sp.diff(constraint, p),
        sp.diff(base, q) + eta * sp.diff(constraint, q),
        constraint,
    ]
    if len(observed) != 3 or any(sp.simplify(a - b) != 0 for a, b in zip(observed, expected)):
        raise GateError("MULTIPLIER_EQUATION", str(observed))
    return {"result": "PASS", "equations": [str(item) for item in observed]}


def independent_pair_test(discard_reactive: bool = False) -> dict[str, object]:
    p, q, eta = sp.symbols("p q eta")
    aligned_f = (p - 2) ** 2 + (q + 1) ** 2
    aligned_k = p + q - 1
    aligned = sp.solve(
        [sp.diff(aligned_f + eta * aligned_k, variable) for variable in (p, q, eta)],
        (p, q, eta),
        dict=True,
    )
    reactive_f = p**2 + 3 * q**2
    reactive_k = p + q - 2
    reactive = [] if discard_reactive else sp.solve(
        [sp.diff(reactive_f + eta * reactive_k, variable) for variable in (p, q, eta)],
        (p, q, eta),
        dict=True,
    )
    metric_root = sp.solve([sp.diff(reactive_f, p), sp.diff(reactive_f, q)], (p, q), dict=True)
    expected_reactive = [{eta: -3, p: sp.Rational(3, 2), q: sp.Rational(1, 2)}]
    if aligned != [{eta: 0, p: 2, q: -1}]:
        raise GateError("REACTIVE_CASE", f"aligned:{aligned}")
    if reactive != expected_reactive or metric_root != [{p: 0, q: 0}]:
        raise GateError("REACTIVE_CASE", f"reactive:{reactive}:{metric_root}")
    if reactive_k.subs(metric_root[0]) != -2 or reactive[0][eta] == 0:
        raise GateError("REACTIVE_CASE", "normal reaction was erased")
    return {"result": "PASS", "aligned_lambda": "0", "reactive_lambda": "-3"}


def independent_penalty_test(force_exact: bool = False) -> dict[str, object]:
    p, q, beta = sp.symbols("p q beta", positive=True)
    constraint = p + q - 1
    penalized = p**2 + q**2 + beta * constraint**2 / 2
    roots = sp.solve([sp.diff(penalized, p), sp.diff(penalized, q)], (p, q), dict=True)
    residual = sp.simplify(constraint.subs(roots[0]))
    accepted_exact = force_exact or residual == 0
    if accepted_exact or residual != -1 / (beta + 1) or sp.limit(residual, beta, sp.oo) != 0:
        raise GateError("FINITE_PENALTY", str(residual))
    return {"result": "PASS", "residual": str(residual), "finite_exact": False}


def independent_covariance_test(select_metric_only: bool = False) -> dict[str, object]:
    a, b = sp.symbols("a b")
    invariant_action = (a - b) ** 4
    identity = sp.simplify(sp.diff(invariant_action, a) + sp.diff(invariant_action, b))
    if identity != 0:
        raise GateError("COVARIANCE_CENSUS", str(identity))
    if select_metric_only:
        raise GateError("COVARIANCE_CENSUS", "covariance falsely promoted metric-only census")
    curvature, multiplier = sp.symbols("curvature multiplier")
    branch_a = curvature**2
    branch_b = (1 + multiplier) * curvature**2
    bulk_root_checks = [
        sp.diff(branch_a, curvature).subs(curvature, 0),
        sp.diff(branch_b, curvature).subs(curvature, 0),
        sp.diff(branch_b, multiplier).subs(curvature, 0),
    ]
    if bulk_root_checks != [0, 0, 0]:
        raise GateError("COVARIANCE_CENSUS", str(bulk_root_checks))
    return {
        "result": "PASS",
        "finite_identity": str(identity),
        "metric_plus_scalar_identity": "2 div(E_g)=E_lambda grad(lambda)",
        "illustrative_4D_bulk_root_checks": [str(item) for item in bulk_root_checks],
        "field_census_selected": False,
    }


def independent_weight_test(wrong_weight: bool = False) -> dict[str, object]:
    w_constraint = sp.symbols("w")
    w_multiplier = -w_constraint if wrong_weight else -4 - w_constraint
    total = sp.simplify(4 + w_multiplier + w_constraint)
    if total != 0:
        raise GateError("CSN_WEIGHT", str(total))
    return {"result": "PASS", "w_lambda": str(w_multiplier), "total": str(total)}


def independent_boundary_test(drop_added_term: bool = False) -> dict[str, object]:
    z = sp.symbols("z")
    f = sp.Function("f")(z)
    mu = sp.Function("mu")(z)
    density = sp.diff(f, z) ** 2 / 2 + mu * sp.diff(f, z)
    momentum = sp.diff(density, sp.diff(f, z))
    expected = sp.diff(f, z) if drop_added_term else sp.diff(f, z) + mu
    if sp.simplify(momentum - expected) != 0 or not momentum.has(mu):
        raise GateError("BOUNDARY_TERM", str(momentum))
    return {"result": "PASS", "endpoint_coefficient": str(momentum)}


def validate_result(result: dict[str, object], statuses: dict[str, dict[str, str]]) -> None:
    expected = {
        "result": "PASS",
        "top_level_outcome": "BOTH_CONDITIONALLY_ADMISSIBLE",
        "branch_A_metric_only": "UNRESOLVED_TRIAL",
        "branch_B_auxiliary_constraint": "UNRESOLVED_TRIAL",
        "field_census_selected": False,
        "bootstrap_selects_branch": False,
        "metric_is_theory_excludes_auxiliary_bookkeeping": "NOT_ESTABLISHED",
        "locality": "OPEN_NOT_ADOPTED",
        "derivative_order": "OPEN_NOT_ADOPTED",
        "invariant_inventory": "OPEN_NOT_ADOPTED",
        "complete_action": "OPEN",
        "native_source": "OPEN",
        "boundary_completion": "OPEN",
        "promoted_action": "NONE",
        "matter_or_carrier_assumed": False,
        "density_normalization_invented": False,
        "gpu_used": False,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            raise GateError("STATUS_OVERSTATEMENT", f"{key}:{result.get(key)}")
    if result.get("common_trial") != {
        "diffeomorphism_covariance": "RETAIN_TRIAL_CONDITIONAL",
        "finite_mirrored_cell": "CANONIZED_BINDING",
        "four_dimensions": "INHERITED",
        "full_finite_cell_diffeomorphism_group": "UNRESOLVED_TRIAL",
        "unrestricted_variation_of_declared_fields": "RETAIN_TRIAL",
    }:
        raise GateError("STATUS_OVERSTATEMENT", str(result.get("common_trial")))
    expected_statuses = {
        "G02": "RETAIN_TRIAL_CONDITIONAL",
        "G03": "RETAIN_TRIAL",
        "G04": "UNRESOLVED_TRIAL",
        "G05": "UNRESOLVED_TRIAL",
        "G06": "BOTH_CONDITIONALLY_ADMISSIBLE",
        "G10": "REFUTED_FOR_FINITE_POSITIVE_ALPHA",
        "G12": "REFUTED_AS_SUFFICIENT",
        "G13": "REFUTED_AS_GENERIC_EXCLUSION",
        "G14": "OPEN",
        "G15": "NOT_ESTABLISHED",
        "G16": "OPEN_NOT_SELECTED",
        "G17": "OPEN_NOT_ADOPTED",
        "G18": "OPEN_NOT_ADOPTED",
        "G19": "OPEN",
    }
    observed = {key: statuses[key]["status"] for key in expected_statuses}
    if observed != expected_statuses:
        raise GateError("STATUS_OVERSTATEMENT", str(observed))


def validate_report(repo: Path) -> dict[str, object]:
    report = (repo / PACKAGE / "DERIVATION_REPORT.md").read_text(encoding="utf-8")
    required = [
        "`BOTH_CONDITIONALLY_ADMISSIBLE`",
        "does not mean that two\ncomplete UDT theories have been built",
        "`RETAIN_TRIAL_CONDITIONAL`",
        "full active diffeomorphism\n  group compatible with the mirrored boundary is `UNRESOLVED_TRIAL`",
        "neither metric-only fields nor metric-plus-auxiliary-constraint fields are selected",
        "No particular UDT `C[g]` is supplied",
        "finite `alpha`",
        "Covariance\ntherefore permits both field censuses",
        "`CATEGORY_A_EXISTENCE_WITNESS_NOT_NATIVE_ACTION`",
        "only a weight\nclassification",
        "Neither branch inherits GR's asymptotic or GHY\ncompletion",
        "would be a new rule",
        "Repository reorganization remains paused",
    ]
    missing = [token for token in required if token not in report]
    if missing:
        raise GateError("REPORT", missing[0])
    forbidden = [
        r"covariance (forces|derives) (EH|metric-only)",
        r"bootstrap (selects|requires) (Branch A|Branch B)",
        r"multiplier (is|becomes) native matter",
    ]
    if any(re.search(pattern, report, re.IGNORECASE) for pattern in forbidden):
        raise GateError("REPORT", "forbidden promotion")
    return {"result": "PASS", "required_statements": len(required)}


def validate_adversarial_audit(repo: Path) -> dict[str, object]:
    audit = (repo / PACKAGE / "ADVERSARIAL_AUDIT.md").read_text(encoding="utf-8")
    required = [
        "/root/gr_constraint_selector_challenge",
        "/root/gr_bundle_boundary_audit",
        "Both reviewers left the repository unchanged",
        "`BOTH_CONDITIONALLY_ADMISSIBLE`",
        "Verdict: `VERIFIED",
        "no branch selection",
    ]
    missing = [token for token in required if token not in audit]
    if missing:
        raise GateError("ADVERSARIAL_AUDIT", missing[0])
    return {"result": "PASS", "reviewers": 2, "required_statements": len(required)}


def validate_scripts_cpu_only(repo: Path) -> dict[str, object]:
    forbidden = {"torch", "cupy", "jax", "tensorflow"}
    imports: set[str] = set()
    for name in ("derive_gr_constraint_trial.py", "verify_gr_constraint_trial.py"):
        tree = ast.parse((repo / PACKAGE / name).read_text(encoding="utf-8"), filename=name)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".", 1)[0])
    bad = imports & forbidden
    if bad:
        raise GateError("GPU_IMPORT", ",".join(sorted(bad)))
    if sp.__version__ != "1.13.1":
        raise GateError("DEPENDENCY", sp.__version__)
    return {"result": "PASS", "sympy": sp.__version__, "gpu_imports": []}


def validate_package_manifest(repo: Path) -> dict[str, object]:
    package = repo / PACKAGE
    manifest = package / "SHA256SUMS.txt"
    replay = run(package, ["sha256sum", "--check", "SHA256SUMS.txt"])
    manifested = {
        line.split("  ", 1)[1]
        for line in manifest.read_text(encoding="utf-8").splitlines()
        if line
    }
    expected = REQUIRED_PACKAGE_FILES - {"SHA256SUMS.txt"}
    if manifested != expected:
        raise GateError("PACKAGE_MANIFEST", str(sorted(manifested)))
    return {
        "result": "PASS",
        "entries_passed": len(replay.splitlines()),
        "manifest_sha256": sha(manifest.read_bytes()),
    }


def validate_frozen_packages(repo: Path, corrupt: bool = False) -> list[dict[str, object]]:
    base_paths = set(str(git(repo, "ls-tree", "-r", "--name-only", BASE)).splitlines())
    current_paths = set(str(git(repo, "ls-files")).splitlines())
    index_oids = {
        line.split(None, 3)[3]: line.split()[1]
        for line in str(git(repo, "ls-files", "-s")).splitlines()
    }
    results = []
    for number, (package, digest) in enumerate(PACKAGES.items()):
        expected_digest = "0" * 64 if corrupt and number == 0 else digest
        manifest = repo / package / "SHA256SUMS.txt"
        if sha(manifest.read_bytes()) != expected_digest:
            raise GateError("FROZEN_PACKAGE", package)
        replay = run(repo / package, ["sha256sum", "--check", "SHA256SUMS.txt"])
        before = sorted(path for path in base_paths if path.startswith(package + "/"))
        after = sorted(path for path in current_paths if path.startswith(package + "/"))
        if not before or before != after:
            raise GateError("FROZEN_PACKAGE", package + ":paths")
        for path in before:
            if index_oids[path] != str(git(repo, "rev-parse", f"{BASE}:{path}")).strip():
                raise GateError("FROZEN_PACKAGE", path)
        results.append({
            "package": package,
            "manifest_entries_passed": len(replay.splitlines()),
            "tracked_paths_byte_identical_to_base": len(before),
            "result": "PASS",
        })
    return results


def validate_navigation(repo: Path) -> dict[str, object]:
    current = tsv_rows(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    paths = [row["current_path"] for row in current]
    if len(current) != 1114 or len(set(paths)) != 1114 or not all((repo / path).exists() for path in paths):
        raise GateError("NAVIGATION", "current paths")
    frontier = tsv_rows(repo / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    if len(frontier) != 306 or len(targets) != 101 or not all((repo / path).exists() for path in targets):
        raise GateError("NAVIGATION", "frontier")
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links: list[Path] = []
    for source in sorted((repo / PACKAGE).glob("*.md")):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            links.append(source.parent.joinpath(target).resolve())
    if not all(target.exists() for target in links):
        raise GateError("NAVIGATION", "package link")
    return {"current_paths": len(current), "frontier": [len(frontier), len(targets)], "links": len(links)}


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
        kind = (
            "regular_file" if stat.S_ISREG(info.st_mode)
            else "directory" if stat.S_ISDIR(info.st_mode)
            else "symlink" if stat.S_ISLNK(info.st_mode)
            else "other"
        )
        result[path] = (code, info.st_size, kind)
    return result


def validate_dirty(repo: Path, dirty_checkout: Path, corrupt: bool = False) -> int:
    recorded = {
        row["path"]: row
        for row in tsv_rows(repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv")
    }
    observed = dirty_metadata(dirty_checkout)
    if corrupt:
        observed = dict(observed)
        observed.pop(next(iter(observed)))
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
    sources = validate_source_hashes(repo)
    result = json.loads((repo / PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    statuses = {row["id"]: row for row in tsv_rows(repo / PACKAGE / "STATUS_LEDGER.tsv")}
    if len(statuses) != 19:
        raise GateError("STATUS_OVERSTATEMENT", f"rows={len(statuses)}")
    validate_result(result, statuses)
    report = validate_report(repo)
    adversarial = validate_adversarial_audit(repo)
    kkt = independent_kkt_test()
    paired = independent_pair_test()
    penalty = independent_penalty_test()
    covariance = independent_covariance_test()
    weights = independent_weight_test()
    boundary = independent_boundary_test()
    cpu = validate_scripts_cpu_only(repo)
    package_manifest = validate_package_manifest(repo)
    frozen = validate_frozen_packages(repo)
    navigation = validate_navigation(repo)
    dirty_count = validate_dirty(repo, args.dirty_checkout.resolve())
    test = json.loads(args.test_result.read_text(encoding="utf-8"))
    if (test.get("passed"), test.get("failed"), test.get("xfailed"), test.get("baseline_match")) != (69, 1, 1, True):
        raise GateError("TEST_BASELINE", str(test))

    bundled = copy.deepcopy(result)
    bundled["promoted_action"] = "EH"
    selected = copy.deepcopy(result)
    selected["branch_A_metric_only"] = "SELECTED"
    selected["field_census_selected"] = True
    catchproof = {
        "missing_multiplier_equation_rejected": catch(
            "MULTIPLIER_EQUATION", lambda: independent_kkt_test(True)
        ),
        "discarded_reactive_case_rejected": catch(
            "REACTIVE_CASE", lambda: independent_pair_test(True)
        ),
        "false_finite_penalty_equivalence_rejected": catch(
            "FINITE_PENALTY", lambda: independent_penalty_test(True)
        ),
        "covariance_metric_only_promotion_rejected": catch(
            "COVARIANCE_CENSUS", lambda: independent_covariance_test(True)
        ),
        "wrong_CSN_multiplier_weight_rejected": catch(
            "CSN_WEIGHT", lambda: independent_weight_test(True)
        ),
        "dropped_constraint_boundary_term_rejected": catch(
            "BOUNDARY_TERM", lambda: independent_boundary_test(True)
        ),
        "bundled_EH_promotion_rejected": catch(
            "STATUS_OVERSTATEMENT", lambda: validate_result(bundled, statuses)
        ),
        "overstated_branch_selection_rejected": catch(
            "STATUS_OVERSTATEMENT", lambda: validate_result(selected, statuses)
        ),
        "source_hash_mutation_rejected": catch(
            "SOURCE_HASH", lambda: validate_source_hashes(repo, True)
        ),
        "scope_escape_rejected": catch("SCOPE", lambda: validate_scope(repo, "LIVE.md")),
        "frozen_package_mutation_rejected": catch(
            "FROZEN_PACKAGE", lambda: validate_frozen_packages(repo, True)
        ),
        "dirty_metadata_drift_rejected": catch(
            "DIRTY_METADATA", lambda: validate_dirty(repo, args.dirty_checkout.resolve(), True)
        ),
    }

    verification = {
        "result": "PASS",
        "mode": "INDEPENDENT_CPU_ONLY_GR_CONSTRAINT_TRIAL_VERIFY",
        "base": BASE,
        "preregistration_commit": PREREG,
        "changed_paths": changed,
        "source_hashes": sources,
        "reported_outcome": result["top_level_outcome"],
        "independent_KKT": kkt,
        "independent_paired_anchors": paired,
        "independent_penalty": penalty,
        "independent_covariance": covariance,
        "independent_CSN_weight": weights,
        "independent_boundary": boundary,
        "report_contract": report,
        "adversarial_audit": adversarial,
        "cpu_dependency": cpu,
        "package_manifest": package_manifest,
        "frozen_package_replays": frozen,
        "navigation": navigation,
        "test_baseline": test,
        "dirty_checkout_metadata_rows": dirty_count,
        "dirty_content_policy": "NOT_READ",
        "catchproof": catchproof,
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
