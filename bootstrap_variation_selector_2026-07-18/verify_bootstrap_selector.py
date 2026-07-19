#!/usr/bin/env python3
"""Independent fail-closed verifier for the bootstrap selector derivation."""

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
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

import sympy as sp


BASE = "3f0d716bd07f9c9f5d8438638bdced28a7b45bda"
PREREG = "851b8f34a6cda8aebfcd65ab86bff3b7f3f4fd72"
PACKAGE = "bootstrap_variation_selector_2026-07-18"
SOURCE_HASHES = {
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": "ce14075bad1ff4b6ea9b41e35dc6b63dfc5a9ae13478bd57c80b1502f33fb540",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "4bb0da9098da0a9970602e2449615eef151796b0d7fe7a9978f4b66145748a34",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md": "db4a426b021e375fa4bca0d870aaf973de319de3b08072195d001a056630832d",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md": "6a835388e8f7a82a4bb4b9496f99c4a5e4181f5e5ccb2637641a1b4346922cc6",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": "70cab9d5e10b03e0e3418129b67155e01d9f805c4397c69ef8795c4d2aaa5dfd",
    "native_action_final_adjudication_2026-07-18/LAY_DECISION_TREE.md": "cac9da7f47d529eccb06615a25e5158a14a8ffa6b33739fb5b21152758da961a",
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
    "derive_bootstrap_selector.py",
    "requirements-cpu.txt",
    "verify_bootstrap_selector.py",
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
    result: dict[str, str] = {}
    for number, (relative, expected) in enumerate(SOURCE_HASHES.items()):
        observed = sha((repo / relative).read_bytes())
        if corrupt and number == 0:
            observed = "0" * 64
        if observed != expected:
            raise GateError("SOURCE_HASH", relative)
        result[relative] = observed
    final_manifest = repo / "native_action_final_adjudication_2026-07-18/SHA256SUMS.txt"
    if sha(final_manifest.read_bytes()) != PACKAGES["native_action_final_adjudication_2026-07-18"]:
        raise GateError("SOURCE_HASH", str(final_manifest))
    return result


def independent_variation_test(omit_normal: bool = False) -> dict[str, str]:
    u, v = sp.symbols("u v")
    a, b, c, h0, h1, h2 = sp.symbols("a b c h0 h1 h2")
    action = a * u * v + b * v**3 + c * u**2
    section = h0 + h1 * u + h2 * u**2
    direct = sp.diff(sp.expand(action.subs(v, section)), u)
    tangent = sp.diff(action, u).subs(v, section)
    normal = sp.diff(action, v).subs(v, section) * sp.diff(section, u)
    candidate = tangent if omit_normal else tangent + normal
    if sp.expand(direct - candidate) != 0:
        raise GateError("CHAIN_RULE", str(sp.expand(direct - candidate)))
    if sp.expand(normal) == 0:
        raise GateError("CHAIN_RULE", "vacuous normal term")
    return {"result": "PASS", "normal_term": str(sp.expand(normal))}


def independent_countermodel_test(
    drop_post_closure: bool = False,
    broad_window: bool = False,
) -> dict[str, object]:
    shape, scale = sp.symbols("shape scale")
    shape0, scale0, gamma, rho0, kappa = sp.symbols("shape0 scale0 gamma rho0 kappa")
    closure = scale - scale0
    pre = (shape - shape0) ** 2
    post = scale0**2 * (shape - shape0) ** 2 + gamma * (shape - shape0) ** 6
    root = {shape: shape0, scale: scale0}
    checks = [
        sp.diff(pre, shape).subs(root) == 0,
        sp.diff(post, shape).subs(root) == 0,
        closure.subs(root) == 0,
        (rho0 + kappa * closure).subs(root) == rho0,
        sp.expand(post - pre) != 0,
        rho0 not in pre.free_symbols,
        rho0 not in post.free_symbols,
    ]
    if drop_post_closure:
        checks[2] = False
    if not all(checks):
        raise GateError("COUNTERMODEL_CLOSURE", str(checks))
    narrowness_contract = "epsilon > 0" if broad_window else "0 < epsilon << 1"
    if narrowness_contract != "0 < epsilon << 1":
        raise GateError("NARROW_WINDOW", narrowness_contract)
    return {
        "result": "PASS",
        "common_root": True,
        "common_closure": True,
        "different_off_shell_actions": True,
        "density_absent_from_local_actions": True,
        "fractional_width_assumption": narrowness_contract,
    }


def independent_weight_test() -> dict[str, int]:
    dimension = 4
    result = {"sqrt_g_R": dimension - 2, "sqrt_g_C2": dimension - 4}
    if result != {"sqrt_g_R": 2, "sqrt_g_C2": 0}:
        raise GateError("CONFORMAL_WEIGHT", str(result))
    return result


def independent_order_test(force_accept: bool = False) -> dict[str, object]:
    momentum, fourth, second, scale = sp.symbols("p A B L")
    polynomial = sp.Poly(fourth * momentum**4 - second * scale**2 * momentum**2, momentum)
    nonzero_identity = all(value == 0 for value in polynomial.all_coeffs())
    if force_accept:
        nonzero_identity = True
    if nonzero_identity:
        raise GateError("ORDER_BRIDGE", "nontrivial fourth/second order identity accepted")
    conditions = {power: coefficient for (power,), coefficient in polynomial.terms()}
    if conditions != {4: fourth, 2: -second * scale**2}:
        raise GateError("ORDER_BRIDGE", str(conditions))
    return {"result": "PASS", "nontrivial_identity_exists": False}


def validate_result(result: dict[str, object], statuses: dict[str, dict[str, str]]) -> None:
    expected = {
        "result": "PASS",
        "top_level_outcome": "UNDERDETERMINED",
        "bootstrap_variation_domain": "OPEN_NOT_SELECTED",
        "two_stage_bridge": "OPEN_NOT_DERIVED",
        "strongest_bridge_result": "CONDITIONAL_CONTRACT_ONLY",
        "promoted_action": "NONE",
        "carrier_assumed": False,
        "density_normalization_invented": False,
        "gpu_used": False,
    }
    for field, value in expected.items():
        if result.get(field) != value:
            raise GateError("STATUS_OVERSTATEMENT", f"{field}:{result.get(field)}")
    expected_statuses = {
        "B03": "OPEN_NOT_SELECTED",
        "B04": "UNIQUE_CONDITIONAL",
        "B05": "CONDITIONAL",
        "B06": "OPEN",
        "B07": "OPEN_NOT_DERIVED",
        "B09": "REFUTED_AS_SUFFICIENT",
        "B10": "CONDITIONAL_CONTRACT_ONLY",
        "B11": "OPEN",
        "B12": "OPEN",
        "B13": "UNDERDETERMINED",
    }
    observed = {key: statuses[key]["status"] for key in expected_statuses}
    if observed != expected_statuses:
        raise GateError("STATUS_OVERSTATEMENT", str(observed))
    countermodel = result["tests"]["T3_selector_countermodels"]
    if countermodel.get("local_density_insertion") is not False:
        raise GateError("DENSITY_INSERTION", str(countermodel))
    if "epsilon" not in str(countermodel.get("shared_matter_admissibility", "")):
        raise GateError("DENSITY_INSERTION", "narrow-window predicate missing")
    if (
        countermodel.get("fractional_width_assumption") != "0 < epsilon << 1"
        or countermodel.get("fractional_width_fitted") is not False
    ):
        raise GateError("NARROW_WINDOW", str(countermodel))


def validate_report(repo: Path) -> dict[str, object]:
    report = (repo / PACKAGE / "DERIVATION_REPORT.md").read_text(encoding="utf-8")
    required = [
        "`UNDERDETERMINED`",
        "does **not** select",
        "does **not** derive a two-stage bridge",
        "does not claim that the toy models are complete UDT universes",
        "CONDITIONAL_CONTRACT_ONLY",
        "off-shell role and placement of\nbootstrap",
        "Repository reorganization remains paused",
    ]
    missing = [token for token in required if token not in report]
    if missing:
        raise GateError("REPORT", missing[0])
    if re.search(r"bootstrap (forces|derives) (C\^2|EH)", report, re.IGNORECASE):
        raise GateError("REPORT", "forbidden action promotion")
    return {"required_statements": len(required), "result": "PASS"}


def validate_adversarial_audit(repo: Path) -> dict[str, object]:
    audit = (repo / PACKAGE / "ADVERSARIAL_AUDIT.md").read_text(encoding="utf-8")
    required = [
        "/root/bootstrap_selector_audit",
        "/root/positive_bridge_challenge",
        "`VERIFIED-WITH-CAVEATS`",
        "Verdict: `VERIFIED`",
        "0 < epsilon << 1",
        "broad `epsilon > 0` fixture",
        "Both reviewers left the repository unchanged",
        "`UNDERDETERMINED` and `OPEN_NOT_DERIVED` remain verified",
    ]
    missing = [token for token in required if token not in audit]
    if missing:
        raise GateError("ADVERSARIAL_AUDIT", missing[0])
    return {"reviewers": 2, "required_statements": len(required), "result": "PASS"}


def validate_scripts_cpu_only(repo: Path) -> dict[str, object]:
    forbidden = {"torch", "cupy", "jax", "tensorflow"}
    imports: set[str] = set()
    for name in ("derive_bootstrap_selector.py", "verify_bootstrap_selector.py"):
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
    return {"sympy": sp.__version__, "gpu_imports": [], "result": "PASS"}


def validate_package_manifest(repo: Path) -> dict[str, object]:
    package = repo / PACKAGE
    manifest = package / "SHA256SUMS.txt"
    replay = run(package, ["sha256sum", "--check", "SHA256SUMS.txt"])
    entries = [line for line in replay.splitlines() if line]
    manifested = {
        line.split("  ", 1)[1]
        for line in manifest.read_text(encoding="utf-8").splitlines()
        if line
    }
    expected = REQUIRED_PACKAGE_FILES - {"SHA256SUMS.txt"}
    if manifested != expected:
        raise GateError("PACKAGE_MANIFEST", f"{sorted(manifested)}")
    return {
        "manifest_sha256": sha(manifest.read_bytes()),
        "entries_passed": len(entries),
        "result": "PASS",
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
        expected = "0" * 64 if corrupt and number == 0 else digest
        manifest = repo / package / "SHA256SUMS.txt"
        if sha(manifest.read_bytes()) != expected:
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

    sources = sorted((repo / PACKAGE).glob("*.md"))
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links = []
    for source in sources:
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
    if len(statuses) != 13:
        raise GateError("STATUS_OVERSTATEMENT", f"rows={len(statuses)}")
    validate_result(result, statuses)
    report = validate_report(repo)
    adversarial_audit = validate_adversarial_audit(repo)
    variation = independent_variation_test()
    countermodels = independent_countermodel_test()
    weights = independent_weight_test()
    order = independent_order_test()
    cpu = validate_scripts_cpu_only(repo)
    package_manifest = validate_package_manifest(repo)
    frozen = validate_frozen_packages(repo)
    navigation = validate_navigation(repo)
    dirty_count = validate_dirty(repo, args.dirty_checkout.resolve())
    test = json.loads(args.test_result.read_text(encoding="utf-8"))
    if (test.get("passed"), test.get("failed"), test.get("xfailed"), test.get("baseline_match")) != (69, 1, 1, True):
        raise GateError("TEST_BASELINE", str(test))

    overstated = copy.deepcopy(result)
    overstated["top_level_outcome"] = "TWO_STAGE_BRIDGE_DERIVED"
    density_inserted = copy.deepcopy(result)
    density_inserted["tests"]["T3_selector_countermodels"]["local_density_insertion"] = True
    catchproof = {
        "omitted_normal_variation_term_rejected": catch(
            "CHAIN_RULE", lambda: independent_variation_test(True)
        ),
        "missing_countermodel_closure_rejected": catch(
            "COUNTERMODEL_CLOSURE", lambda: independent_countermodel_test(drop_post_closure=True)
        ),
        "broad_density_window_rejected": catch(
            "NARROW_WINDOW", lambda: independent_countermodel_test(broad_window=True)
        ),
        "false_fourth_to_second_order_bridge_rejected": catch(
            "ORDER_BRIDGE", lambda: independent_order_test(True)
        ),
        "overstated_bridge_status_rejected": catch(
            "STATUS_OVERSTATEMENT", lambda: validate_result(overstated, statuses)
        ),
        "density_insertion_rejected": catch(
            "DENSITY_INSERTION", lambda: validate_result(density_inserted, statuses)
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
        "mode": "INDEPENDENT_CPU_ONLY_BOOTSTRAP_SELECTOR_VERIFY",
        "base": BASE,
        "preregistration_commit": PREREG,
        "changed_paths": changed,
        "source_hashes": sources,
        "reported_outcome": result["top_level_outcome"],
        "variation_restriction": variation,
        "selector_countermodels": countermodels,
        "conformal_weights": weights,
        "principal_order": order,
        "report_contract": report,
        "adversarial_audit": adversarial_audit,
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
