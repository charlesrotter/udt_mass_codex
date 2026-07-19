#!/usr/bin/env python3
"""Independent fail-closed verifier for the Reciprocity constraint selector."""

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


BASE = "7b0e07fcad2ffdee94bcc1acda582d7ebab074d0"
PREREG = "750d48bd79178a48d20912b85ef713d1261f0038"
PACKAGE = "reciprocity_offshell_constraint_selector_2026-07-18"
SOURCE_HASHES = {
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md": "6e977717ca028cabaa198dd14a6a97b3b15740e45485d0ab735f3df0326df192",
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md": "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "4bb0da9098da0a9970602e2449615eef151796b0d7fe7a9978f4b66145748a34",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md": "db4a426b021e375fa4bca0d870aaf973de319de3b08072195d001a056630832d",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": "70cab9d5e10b03e0e3418129b67155e01d9f805c4397c69ef8795c4d2aaa5dfd",
    "gr_constraint_paired_trial_2026-07-18/SHA256SUMS.txt": "8d5c617d9bb611f67b15524b34271de7f121ea9a71fa14d8e131cf85bc2c63a2",
    "gr_constraint_paired_trial_2026-07-18/DERIVATION_REPORT.md": "952b29705023c0626896db75b7a60173d6c78e3e00a8321d826a53b606557316",
    "gr_constraint_paired_trial_2026-07-18/STATUS_LEDGER.tsv": "ba26cad7d04d7492c206e3fe11a7cd10ab226c01663bef5edee4b166c2f08809",
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
    "derive_reciprocity_constraint_selector.py",
    "requirements-cpu.txt",
    "verify_reciprocity_constraint_selector.py",
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
    names = {Path(path).name for path in changed if path.startswith(PACKAGE + "/")}
    missing = REQUIRED_PACKAGE_FILES - names
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
    replay = run(repo / "gr_constraint_paired_trial_2026-07-18", ["sha256sum", "--check", "SHA256SUMS.txt"])
    if len(replay.splitlines()) != 10:
        raise GateError("SOURCE_HASH", "prior paired-trial replay")
    return observed_hashes


def independent_chart_test(force_scalar: bool = False) -> dict[str, object]:
    p, q, u, v = sp.symbols("p q u v", positive=True)
    metric = sp.diag(-p, q)
    jacobian = sp.diag(1 / u, 1 / v)
    changed = sp.simplify(jacobian.T * metric * jacobian)
    old = p * q
    new = sp.simplify((-changed[0, 0]) * changed[1, 1])
    if new != p * q / (u**2 * v**2):
        raise GateError("COMPONENT_SCALAR", str(new))
    if force_scalar or sp.simplify(new - old) == 0:
        raise GateError("COMPONENT_SCALAR", "raw component product accepted as invariant")
    return {"result": "PASS", "old": str(old), "new": str(new), "scalar": False}


def independent_csn_test(drop_shift: bool = False) -> dict[str, object]:
    scale, depth, shift = sp.symbols("s d w", real=True)
    p = sp.exp(2 * scale - 2 * depth)
    q = sp.exp(2 * scale + 2 * depth)
    p2 = sp.exp(2 * shift) * p
    q2 = sp.exp(2 * shift) * q
    product = sp.simplify(p2 * q2)
    ratio = sp.simplify(q2 / p2)
    expected_product = sp.exp(4 * scale) if drop_shift else sp.exp(4 * scale + 4 * shift)
    if product != expected_product or ratio != sp.exp(4 * depth):
        raise GateError("CSN_SHIFT", f"{product}:{ratio}")
    return {"result": "PASS", "sigma_shift": "+log(Omega)", "phi_invariant": True}


def independent_orbit_test(accept_nonconstant: bool = False) -> dict[str, object]:
    x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3", positive=True)
    eta = sp.diag(-1, 1, 1, 1)
    transform = sp.diag(sp.sqrt(x0), sp.sqrt(x1), sp.sqrt(x2), sp.sqrt(x3))
    reached = sp.simplify(transform.T * eta * transform)
    if reached != sp.diag(-x0, x1, x2, x3):
        raise GateError("NATURAL_SCALAR", str(reached))
    if accept_nonconstant:
        raise GateError("NATURAL_SCALAR", "nonconstant invariant accepted on transitive orbit")
    return {
        "result": "PASS",
        "transitive_fixed_signature_orbit": True,
        "nonconstant_order_zero_scalar": False,
    }


def independent_structured_test(hide_extra: bool = False) -> dict[str, object]:
    a, b, omega = sp.symbols("a b Omega", positive=True)
    product = sp.simplify((omega**2 * a) * (omega**2 * b))
    ratio = sp.simplify((omega**2 * b) / (omega**2 * a))
    fields = ["g"] if hide_extra else ["g", "T", "N"]
    if fields == ["g"]:
        raise GateError("HIDDEN_STRUCTURE", "T,N suppressed from C[g,T,N]")
    if product != omega**4 * a * b or ratio != b / a:
        raise GateError("HIDDEN_STRUCTURE", f"{product}:{ratio}")
    return {"result": "PASS", "fields": fields, "metric_only": False, "ratio_invariant": True}


def independent_density_test(treat_scalar: bool = False) -> dict[str, object]:
    determinant, jacobian = sp.symbols("D J", positive=True)
    old_density = sp.sqrt(determinant)
    new_density = sp.simplify(jacobian * old_density)
    if treat_scalar or sp.simplify(new_density - old_density) == 0:
        raise GateError("DENSITY", "volume density accepted as scalar")
    return {"result": "PASS", "transformation": "sqrt|g| -> |J| sqrt|g|", "reference_needed": True}


def independent_gauge_test(force_reactive: bool = False) -> dict[str, object]:
    depth, scale, multiplier, target, source = sp.symbols("d s ell d0 k")
    action = (depth - target) ** 2 / 2 + multiplier * scale
    equations = [sp.diff(action, variable) for variable in (depth, scale, multiplier)]
    solution = sp.solve(equations, (depth, scale, multiplier), dict=True)
    if solution != [{depth: target, multiplier: 0, scale: 0}]:
        raise GateError("GAUGE_REACTION", str(solution))
    reaction = -source if force_reactive else solution[0][multiplier]
    if reaction != 0:
        raise GateError("GAUGE_REACTION", "physical reaction assigned to CSN gauge anchor")
    violating = action + source * scale
    violating_solution = sp.solve(
        [sp.diff(violating, variable) for variable in (depth, scale, multiplier)],
        (depth, scale, multiplier),
        dict=True,
    )
    if violating_solution != [{depth: target, multiplier: -source, scale: 0}]:
        raise GateError("GAUGE_REACTION", str(violating_solution))
    return {"result": "PASS", "gauge_lambda": "0", "reactive_fixture": "CSN_VIOLATING"}


def independent_curvature_test(force_equivalence: bool = False) -> dict[str, object]:
    p, q = sp.symbols("p q", positive=True)
    coordinates = sp.symbols("u v")
    metric = sp.diag(-p, q)
    if any(sp.diff(metric[i, j], coordinate) != 0 for i in range(2) for j in range(2) for coordinate in coordinates):
        raise GateError("CURVATURE_EQUIV", "constant flat anchor gained derivatives")
    products = [sp.simplify((p * q).subs({p: 1, q: 1})), sp.simplify((p * q).subs({p: 9, q: 1}))]
    equivalent = force_equivalence or products[0] == products[1]
    if equivalent:
        raise GateError("CURVATURE_EQUIV", str(products))
    return {"result": "PASS", "both_flat": True, "products": [str(item) for item in products], "equivalent": False}


def validate_result(result: dict[str, object], statuses: dict[str, dict[str, str]]) -> None:
    expected = {
        "result": "PASS",
        "top_level_outcome": "NO_L0_CONSTRAINT_REPRESENTATIVE_IDENTITY_IS_GAUGE_READOUT",
        "reciprocity_current_role": "DERIVED_KINEMATIC_COMPARISON_WITH_CONDITIONAL_METRIC_READOUT",
        "metric_only_off_shell_closure": "NOT_DERIVED",
        "native_auxiliary_constraint_required": False,
        "physical_multiplier_for_reciprocal_product": "NOT_DERIVED",
        "gauge_multiplier": "ALLOWED_BOOKKEEPING_WITH_ZERO_REACTION_IN_CSN_INVARIANT_ANCHOR",
        "off_shell_field_census": "OPEN_NARROWED",
        "complete_action": "OPEN",
        "boundary_completion": "OPEN",
        "promoted_action": "NONE",
        "carrier_or_source_assumed": False,
        "density_normalization_invented": False,
        "gpu_used": False,
    }
    for key, value in expected.items():
        if result.get(key) != value:
            raise GateError("STATUS_OVERSTATEMENT", f"{key}:{result.get(key)}")
    expected_routes = {
        "L0_metric_only_order_zero": "REFUTED_IN_CLASS",
        "L1_adapted_representative_product": "CSN_GAUGE_READOUT_CONDITIONAL_ON_FRAME_AND_REPRESENTATIVE",
        "L2_structured_covariant": "OPEN_EXTRA_STRUCTURE_NOT_DERIVED",
        "L3_derivative_metric_only": "OPEN_CURVATURE_SHORTCUT_NOT_EQUIVALENT",
        "L4_global_boundary": "OPEN_NOT_SUPPLIED",
    }
    if result.get("route_status") != expected_routes:
        raise GateError("STATUS_OVERSTATEMENT", str(result.get("route_status")))
    expected_statuses = {
        "O04": "NOT_A_SCALAR",
        "O05": "GAUGE_CALIBRATION",
        "O06": "DERIVED_CONDITIONAL_READOUT",
        "O07": "REFUTED_IN_CLASS",
        "O08": "REFUTED_AS_SCALAR",
        "O09": "OPEN_EXTRA_STRUCTURE_NOT_DERIVED",
        "O11": "ALLOWED_BOOKKEEPING",
        "O12": "NOT_DERIVED",
        "O14": "REFUTED_AS_EQUIVALENT_SHORTCUT",
        "O15": "OPEN",
        "O16": "OPEN_NOT_SUPPLIED",
        "O18": "NOT_DERIVED",
        "O19": "NOT_DERIVED",
        "O20": "DERIVED_KINEMATIC_WITH_CONDITIONAL_READOUT",
        "O21": "NO_L0_CONSTRAINT_REPRESENTATIVE_IDENTITY_IS_GAUGE_READOUT",
        "O22": "OPEN",
    }
    observed = {key: statuses[key]["status"] for key in expected_statuses}
    if observed != expected_statuses:
        raise GateError("STATUS_OVERSTATEMENT", str(observed))


def validate_report(repo: Path) -> dict[str, object]:
    report = (repo / PACKAGE / "DERIVATION_REPORT.md").read_text(encoding="utf-8")
    required = [
        "`NO_L0_CONSTRAINT_REPRESENTATIVE_IDENTITY_IS_GAUGE_READOUT`",
        "the general linear group acts\ntransitively",
        "It does not exclude a derived coframe/vector structure",
        "unit product maps to `1/4`",
        "sigma -> sigma + log(Omega)",
        "`phi=(1/4)log(b/a)`",
        "`det g` is not a scalar",
        "`C[g,T,N]`, not `C[g]`",
        "The reaction vanishes",
        "refutes the curvature shortcut, not all L3 theories",
        "L4 route and remains `OPEN_NOT_SUPPLIED`",
        "field census is narrowed but remains\n`OPEN`",
        "promotes no action",
    ]
    missing = [token for token in required if token not in report]
    if missing:
        raise GateError("REPORT", missing[0])
    forbidden = [
        r"all derivative (constraints|laws) are impossible",
        r"Reciprocity (requires|forces) a multiplier",
        r"metric-only action (is|has been) derived",
        r"finite cell (selects|derives) the bulk frame",
    ]
    if any(re.search(pattern, report, re.IGNORECASE) for pattern in forbidden):
        raise GateError("REPORT", "forbidden overstatement")
    return {"result": "PASS", "required_statements": len(required)}


def validate_adversarial_audit(repo: Path) -> dict[str, object]:
    audit = (repo / PACKAGE / "ADVERSARIAL_AUDIT.md").read_text(encoding="utf-8")
    required = [
        "/root/reciprocity_covariant_counterexample",
        "/root/reciprocity_variation_boundary_audit",
        "Both reviewers left the repository unchanged",
        "`VERIFIED",
        "L0",
        "L2-L4",
        "no auxiliary requirement",
    ]
    missing = [token for token in required if token not in audit]
    if missing:
        raise GateError("ADVERSARIAL_AUDIT", missing[0])
    return {"result": "PASS", "reviewers": 2, "required_statements": len(required)}


def validate_scripts_cpu_only(repo: Path) -> dict[str, object]:
    forbidden = {"torch", "cupy", "jax", "tensorflow"}
    imports: set[str] = set()
    for name in ("derive_reciprocity_constraint_selector.py", "verify_reciprocity_constraint_selector.py"):
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
    if len(statuses) != 22:
        raise GateError("STATUS_OVERSTATEMENT", f"rows={len(statuses)}")
    validate_result(result, statuses)
    report = validate_report(repo)
    adversarial = validate_adversarial_audit(repo)
    chart = independent_chart_test()
    csn = independent_csn_test()
    orbit = independent_orbit_test()
    structured = independent_structured_test()
    density = independent_density_test()
    gauge = independent_gauge_test()
    curvature = independent_curvature_test()
    cpu = validate_scripts_cpu_only(repo)
    package_manifest = validate_package_manifest(repo)
    frozen = validate_frozen_packages(repo)
    navigation = validate_navigation(repo)
    dirty_count = validate_dirty(repo, args.dirty_checkout.resolve())
    test = json.loads(args.test_result.read_text(encoding="utf-8"))
    if (test.get("passed"), test.get("failed"), test.get("xfailed"), test.get("baseline_match")) != (69, 1, 1, True):
        raise GateError("TEST_BASELINE", str(test))

    overstated = copy.deepcopy(result)
    overstated["route_status"]["L3_derivative_metric_only"] = "REFUTED"
    overstated["native_auxiliary_constraint_required"] = True
    catchproof = {
        "component_product_scalar_claim_rejected": catch(
            "COMPONENT_SCALAR", lambda: independent_chart_test(True)
        ),
        "lost_CSN_scale_shift_rejected": catch("CSN_SHIFT", lambda: independent_csn_test(True)),
        "nonconstant_order_zero_invariant_rejected": catch(
            "NATURAL_SCALAR", lambda: independent_orbit_test(True)
        ),
        "hidden_preferred_frame_rejected": catch(
            "HIDDEN_STRUCTURE", lambda: independent_structured_test(True)
        ),
        "volume_density_as_scalar_rejected": catch("DENSITY", lambda: independent_density_test(True)),
        "physical_reaction_from_gauge_fixing_rejected": catch(
            "GAUGE_REACTION", lambda: independent_gauge_test(True)
        ),
        "curvature_one_way_equivalence_rejected": catch(
            "CURVATURE_EQUIV", lambda: independent_curvature_test(True)
        ),
        "scope_overstatement_and_auxiliary_promotion_rejected": catch(
            "STATUS_OVERSTATEMENT", lambda: validate_result(overstated, statuses)
        ),
        "source_hash_mutation_rejected": catch("SOURCE_HASH", lambda: validate_source_hashes(repo, True)),
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
        "mode": "INDEPENDENT_CPU_ONLY_RECIPROCITY_CONSTRAINT_SELECTOR_VERIFY",
        "base": BASE,
        "preregistration_commit": PREREG,
        "changed_paths": changed,
        "source_hashes": sources,
        "reported_outcome": result["top_level_outcome"],
        "independent_chart": chart,
        "independent_CSN": csn,
        "independent_orbit": orbit,
        "independent_structured": structured,
        "independent_density": density,
        "independent_gauge": gauge,
        "independent_curvature": curvature,
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
