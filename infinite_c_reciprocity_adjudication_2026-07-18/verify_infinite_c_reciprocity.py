#!/usr/bin/env python3
"""Independent fail-closed verifier for the infinite-c / Reciprocity adjudication."""

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


BASE = "b3cd93bd92960b89935b9946b88f2e6017195c99"
PREREG = "de6c264"
PACKAGE = "infinite_c_reciprocity_adjudication_2026-07-18"
OUTCOME = "LAYERED_COMPATIBILITY_METRIC_NONDISCRIMINATING"
SOURCE_HASHES = {
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md": "6e977717ca028cabaa198dd14a6a97b3b15740e45485d0ab735f3df0326df192",
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md": "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "4bb0da9098da0a9970602e2449615eef151796b0d7fe7a9978f4b66145748a34",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": "70cab9d5e10b03e0e3418129b67155e01d9f805c4397c69ef8795c4d2aaa5dfd",
    "reciprocity_offshell_constraint_selector_2026-07-18/SHA256SUMS.txt": "3f6da5926200f68e07b67a167948b2211d0a506fa65d322e600a7d22b080c74a",
    "reciprocal_line_realization_selector_2026-07-18/SHA256SUMS.txt": "4fe297e81414977f5eb75b6e535e1fca0f60a1d872e1fd42921f25aee0e59a16",
    "reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md": "e05cc6b0f124419104dde530305e1cd3779b5e3f7136f59e2000af67812a948e",
    "reciprocal_line_realization_selector_2026-07-18/STATUS_LEDGER.tsv": "b3a0edea452a7873b8bf8a7aeacaa4339a620f7901e673f942a8319dc6023faa",
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
    "ADVERSARIAL_AUDIT.md", "DERIVATION_REPORT.md", "DERIVATION_RESULT.json",
    "DERIVATION_TRANSCRIPT.txt", "LAY_DECISION_TREE.md", "POST_PREREG_OWNER_CLARIFICATION.md",
    "POST_PREREG_METRIC_ENDPOINT_CLARIFICATION.md",
    "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "REVIEW_CAUSALITY_PROVENANCE.md",
    "REVIEW_PROJECTIVE_COUNTERAUDIT.md", "STATUS_LEDGER.tsv", "derive_infinite_c_reciprocity.py",
    "requirements-cpu.txt", "verify_infinite_c_reciprocity.py",
}


class GateError(AssertionError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


def run(cwd: Path, command: list[str], *, binary: bool = False):
    completed = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=not binary, check=False)
    if completed.returncode:
        error = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise GateError("COMMAND", f"{' '.join(command)}:{error}")
    return completed.stdout


def git(repo: Path, *args: str, binary: bool = False):
    return run(repo, ["git", *args], binary=binary)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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
    if not resolved.startswith(PREREG) or parent != BASE or paths != [f"{PACKAGE}/PREREGISTRATION.md"]:
        raise GateError("PREREGISTRATION", f"{resolved}:{parent}:{paths}")


def validate_scope(repo: Path, injected: str | None = None) -> list[str]:
    paths = set(str(git(repo, "diff", "--name-only", BASE)).splitlines())
    paths.update(str(git(repo, "ls-files", "--others", "--exclude-standard")).splitlines())
    if injected:
        paths.add(injected)
    invalid = sorted(path for path in paths if not path.startswith(PACKAGE + "/"))
    if invalid:
        raise GateError("SCOPE", invalid[0])
    return sorted(paths)


def validate_sources(repo: Path, corrupt: bool = False) -> dict[str, str]:
    observed = {}
    for index, (relative, expected) in enumerate(SOURCE_HASHES.items()):
        value = sha((repo / relative).read_bytes())
        if corrupt and index == 0:
            value = "0" * 64
        if value != expected:
            raise GateError("SOURCE_HASH", relative)
        observed[relative] = value
    return observed


def exact_algebra(force_singular_endpoint: bool = False, force_pairing_from_gauge: bool = False,
                  force_metric_distinction: bool = False, force_deformed_boost: bool = False) -> dict[str, object]:
    regulator, observed = sp.symbols("regulator observed", positive=True, finite=True)
    pairing = sp.Matrix([[0, 1], [1, 0]])
    reciprocal = sp.diag(sp.sqrt(observed / regulator), sp.sqrt(regulator / observed))
    nonreciprocal = sp.diag(observed / regulator, 1)
    if sp.simplify(reciprocal.T * pairing * reciprocal) != pairing:
        raise GateError("ALGEBRA", "reciprocal pairing")
    nonreciprocal_pairing = sp.simplify(nonreciprocal.T * pairing * nonreciprocal)
    if force_pairing_from_gauge or nonreciprocal_pairing == pairing:
        raise GateError("PAIRING_FROM_GAUGE", str(nonreciprocal_pairing))
    common = sp.sqrt(regulator / observed)
    if sp.simplify(common * nonreciprocal - reciprocal) != sp.zeros(2):
        raise GateError("ALGEBRA", "CSN relation")
    metric_effective = sp.diag(-observed**2, 1)
    metric_reciprocal = sp.diag(-regulator**2 * reciprocal[0, 0]**2, reciprocal[1, 1]**2)
    if force_metric_distinction or sp.simplify(metric_reciprocal - (regulator / observed) * metric_effective) != sp.zeros(2):
        raise GateError("CSN_METRIC", str(metric_reciprocal))
    u_limit = sp.limit(reciprocal[0, 0], regulator, sp.oo)
    v_limit = sp.limit(reciprocal[1, 1], regulator, sp.oo)
    if force_singular_endpoint or (u_limit, v_limit) != (0, sp.oo):
        raise GateError("SINGULAR_ENDPOINT", f"{u_limit}:{v_limit}")
    projective = sp.simplify(sp.sqrt(observed / regulator) * reciprocal)
    projective_endpoint = projective.applyfunc(lambda entry: sp.limit(entry, regulator, sp.oo))
    if projective_endpoint != sp.diag(0, 1) or projective_endpoint.det() != 0:
        raise GateError("ALGEBRA", "projective endpoint")
    velocity = sp.symbols("velocity", real=True)
    gamma = 1 / sp.sqrt(1 - velocity**2 / observed**2)
    boost = sp.Matrix([[gamma, -gamma * velocity / observed**2], [-gamma * velocity, gamma]])
    boost_residual = sp.simplify(boost.T * metric_effective * boost - metric_effective)
    if force_deformed_boost or boost_residual != sp.zeros(2):
        raise GateError("LORENTZ_DEFORMATION", str(boost_residual))

    anchor = sp.symbols("anchor", positive=True, finite=True)
    depth = sp.symbols("depth", real=True)
    metric_flow = sp.diag(-anchor**2 * sp.exp(-2 * depth), sp.exp(2 * depth))
    coordinate_speed = sp.simplify(sp.sqrt(-metric_flow[0, 0] / metric_flow[1, 1]))
    reversed_product = sp.simplify(coordinate_speed * coordinate_speed.subs(depth, -depth))
    local_speed = sp.simplify(sp.exp(depth) * coordinate_speed / sp.exp(-depth))
    if coordinate_speed != anchor * sp.exp(-2 * depth) or reversed_product != anchor**2 or local_speed != anchor:
        raise GateError("ALGEBRA", "H6 metric flow")
    endpoint_limits = [sp.limit(coordinate_speed, depth, -sp.oo), sp.limit(coordinate_speed, depth, sp.oo)]
    if endpoint_limits != [sp.oo, 0]:
        raise GateError("ALGEBRA", "H6 endpoints")
    fast_metric_endpoint = (sp.exp(2 * depth) * metric_flow).applyfunc(lambda entry: sp.limit(entry, depth, -sp.oo))
    slow_metric_endpoint = (sp.exp(-2 * depth) * metric_flow).applyfunc(lambda entry: sp.limit(entry, depth, sp.oo))
    if fast_metric_endpoint != sp.diag(-anchor**2, 0) or slow_metric_endpoint != sp.diag(0, 1):
        raise GateError("ALGEBRA", "H6 projective metrics")
    radius, wall = sp.symbols("radius wall", positive=True, finite=True)
    wrl_depth = -sp.log(1 - radius / wall) / 2
    wrl_speed = sp.simplify(coordinate_speed.subs(depth, wrl_depth))
    wrl_limits = [sp.limit(wrl_speed, radius, 0, dir="+"), sp.limit(wrl_speed, radius, wall, dir="-")]
    if wrl_limits != [anchor, 0]:
        raise GateError("ALGEBRA", "H6 WRL")
    return {
        "result": "PASS", "reciprocal_pairing": True,
        "nonreciprocal_pairing_factor": str(observed / regulator),
        "CSN_related": True, "component_limits": [str(u_limit), str(v_limit)],
        "projective_rank_one_endpoint": str(projective_endpoint),
        "ordinary_lorentz_residual": str(boost_residual),
        "H6_coordinate_speed": str(coordinate_speed),
        "H6_reversed_product": str(reversed_product),
        "H6_endpoint_limits": [str(value) for value in endpoint_limits],
        "H6_local_proper_speed": str(local_speed),
        "H6_projective_metric_endpoints": [str(fast_metric_endpoint), str(slow_metric_endpoint)],
        "H6_conditional_WRL_speed": str(wrl_speed),
        "H6_conditional_WRL_limits": [str(value) for value in wrl_limits],
    }


def validate_claims(claims: dict[str, object]) -> None:
    rejected = {
        "literal_infinity_is_invertible": "INFINITE_INVERTIBILITY",
        "zero_times_infinity_equals_one": "INDETERMINATE_PRODUCT",
        "nonreciprocal_countermodel_currently_admissible": "CURRENT_LEDGER",
        "constant_background_is_curvature": "CONSTANT_WARP",
        "units_select_foundation": "UNIT_ARGUMENT",
        "adopt_abandon_reciprocity": "FOUNDATION_MUTATION",
        "adopt_infinite_c": "FOUNDATION_MUTATION",
        "line_realization_closed": "LINE_PROMOTION",
        "action_or_variation_selected": "ACTION_PROMOTION",
        "H5_no_signalling_already_proved": "NO_SIGNALLING_PROMOTION",
        "atemporal_layer_is_literal_speed_without_time_distance": "TYPE_CONFUSION",
        "full_4d_equivalence_claimed": "FULL4D_PROMOTION",
        "coordinate_speed_is_scalar": "COORDINATE_SCALAR",
        "local_c_varies_with_phi": "LOCAL_C_PROMOTION",
        "distance_CMB_endpoint_map_derived": "ENDPOINT_MAP_PROMOTION",
        "H5A_H5B_conflated": "LAYER_CONFLATION",
        "historical_electron_picture_derived": "HISTORICAL_PROMOTION",
    }
    for key, code in rejected.items():
        if claims.get(key):
            raise GateError(code, key)


def validate_result(repo: Path, corrupt: bool = False) -> dict[str, object]:
    result = json.loads((repo / PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    expected_hypotheses = {
        "H0_FINITE_RECIPROCAL_EFFECTIVE": "CONSISTENT_CURRENT_FOUNDATION",
        "H1_LITERAL_INFINITY_SAME_LAYER": "INCOMPATIBLE_WITH_FINITE_INVERTIBLE_RECIPROCAL_PAIR",
        "H2_REGULATED_PROJECTIVE_INFINITY": "COMPATIBLE_LIMIT_NOT_GROUP_ENDPOINT",
        "H3_CSN_APPARENT_RECIPROCITY": "METRIC_EQUIVALENT_INTERNAL_PAIRING_NOT_DERIVED",
        "H4_GALILEAN_TO_LORENTZ_EMERGENCE": "OPEN_REPLACEMENT_REQUIRES_NEW_DYNAMICS_AND_UNIVERSAL_COUPLING",
        "H5A_ATEMPORAL_GLOBAL_CLOSURE": "CONCEPTUALLY_COMPATIBLE_NOT_DERIVED",
        "H5B_TIMED_INSTANTANEOUS_SUBSTRATE": "OPEN_REPLACEMENT_REQUIRES_PREFERRED_CAUSAL_STRUCTURE",
        "H6_RECIPROCAL_CAUSAL_ENDPOINT_FLOW": "CONDITIONALLY_COHERENT_METRIC_BLOCK_INTERPRETATION",
    }
    if corrupt:
        result = copy.deepcopy(result)
        result["adjudication"]["abandon_reciprocity_now"] = True
    adjudication = result.get("adjudication", {})
    required_false = [
        "abandon_reciprocity_now", "adopt_literal_infinite_c_now", "current_owner_foundation_changed",
        "underlying_infinite_speed_well_typed_without_pregeometric_time_and_distance",
        "observable_superluminal_signalling_authorized", "line_realization_gap_closed",
        "variation_domain_or_action_selected", "full_4d_metric_discrimination_established",
        "metric_endpoint_interpretation_requires_abandoning_reciprocity",
        "metric_coordinate_speed_is_diffeomorphism_scalar", "local_orthonormal_speed_varies_with_phi",
        "distance_to_phi_endpoint_map_derived", "CMB_identified_with_phi_positive_infinity",
    ]
    required_true = [
        "regulated_infinite_c_logically_compatible_with_reciprocity",
        "owner_clarification_received_after_preregistration",
        "layered_atemporal_and_geometric_reciprocity_logically_compatible",
    ]
    if (
        result.get("schema") != "udt.infinite-c-reciprocity-adjudication.v1"
        or result.get("top_level_outcome") != OUTCOME
        or result.get("check_count") != 23
        or not all(result.get("checks", {}).values())
        or result.get("hypotheses") != expected_hypotheses
        or any(adjudication.get(key) is not False for key in required_false)
        or any(adjudication.get(key) is not True for key in required_true)
        or adjudication.get("local_time_parallel_conformal_block_discriminates_internal_reciprocity") is not False
    ):
        raise GateError("STATUS_CONTRACT", str(adjudication))
    return result


def validate_ledgers(repo: Path) -> dict[str, object]:
    statuses = {row["id"]: row["status"] for row in tsv_rows(repo / PACKAGE / "STATUS_LEDGER.tsv")}
    expected = {
        "S01": "FOUNDING_UNCHANGED", "S02": "FOUNDING_UNCHANGED", "S03": "INCOMPATIBLE_IN_CLASS",
        "S04": "CONDITIONAL_COMPATIBLE", "S05": "FINITE_PROJECTIVE_RESIDUAL",
        "S06": "LOGICAL_COUNTERMODEL_NOT_CURRENT_ADMISSIBLE",
        "S07": "GAUGE_REPRESENTATIVE_AVAILABLE", "S08": "NO", "S09": "NOT_DERIVED",
        "S10": "NOT_DERIVED", "S11": "EXACT_REPARAMETRIZATION", "S12": "NOT_DERIVED",
        "S13": "ORDINARY_EFFECTIVE_LORENTZ", "S14": "OPEN_REPLACEMENT_THEORY",
        "S15": "NOT_A_FOUNDATION_DISCRIMINATOR", "S16": "OPEN", "S17": "OPEN", "S18": "OPEN",
        "S19": "CONCEPTUALLY_COMPATIBLE_NOT_DERIVED", "S20": "OPEN_REPLACEMENT_THEORY",
        "S21": "OBSERVATIONAL_ROLE_COMPATIBLE", "S22": "DERIVED_CONDITIONAL_READOUT",
        "S23": "DERIVED_CONDITIONAL_READOUT", "S24": "DERIVED_CONDITIONAL_READOUT",
        "S25": "OPEN", "S26": "HISTORICAL_OWNER_INTUITION_QUESTION_ONLY",
        "S27": "NO_CHANGE_AUTHORIZED", "S28": OUTCOME,
    }
    observed = {key: statuses.get(key) for key in expected}
    if len(statuses) != 28 or observed != expected:
        raise GateError("STATUS_CONTRACT", str(observed))
    return {"result": "PASS", "rows": len(statuses)}


def validate_report(repo: Path) -> dict[str, object]:
    report = (repo / PACKAGE / "DERIVATION_REPORT.md").read_text(encoding="utf-8")
    audit = (repo / PACKAGE / "ADVERSARIAL_AUDIT.md").read_text(encoding="utf-8")
    clarification = (repo / PACKAGE / "POST_PREREG_OWNER_CLARIFICATION.md").read_text(encoding="utf-8")
    endpoint_clarification = (repo / PACKAGE / "POST_PREREG_METRIC_ENDPOINT_CLARIFICATION.md").read_text(encoding="utf-8")
    required = [
        OUTCOME, "literal infinite conversion at the same foundational layer", "0*infinity",
        "P_R=sqrt(C/c_eff) P_NR", "derive the physical internal statement",
        "CONCEPTUALLY_COMPATIBLE_NOT_DERIVED", "intervention-level no-signalling",
        "O(1,1)` time/parallel boost block", "does not warrant abandoning Reciprocity",
        "c_coord(phi)c_coord(-phi)=c_0^2", "d ell/d tau=c_0",
    ]
    missing = [token for token in required if token not in report]
    if (missing or "received after preregistration" not in clarification
            or "straight property of the metric" not in endpoint_clarification
            or "No files were changed" not in audit):
        raise GateError("REPORT_CONTRACT", missing[0] if missing else "review/clarification")
    return {"result": "PASS", "tokens": len(required)}


def validate_cpu(repo: Path) -> dict[str, object]:
    imports: set[str] = set()
    for name in ("derive_infinite_c_reciprocity.py", "verify_infinite_c_reciprocity.py"):
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
    names = {line.split("  ", 1)[1] for line in manifest.read_text(encoding="utf-8").splitlines() if line}
    if names != MANIFESTED_FILES:
        raise GateError("PACKAGE_MANIFEST", str(sorted(names ^ MANIFESTED_FILES)))
    return {"result": "PASS", "entries": len(replay.splitlines()), "sha256": sha(manifest.read_bytes())}


def validate_frozen(repo: Path, corrupt: bool = False) -> list[dict[str, object]]:
    base_paths = set(str(git(repo, "ls-tree", "-r", "--name-only", BASE)).splitlines())
    current_paths = set(str(git(repo, "ls-files")).splitlines())
    index_oids = {line.split(None, 3)[3]: line.split()[1] for line in str(git(repo, "ls-files", "-s")).splitlines()}
    output = []
    for index, (package, expected) in enumerate(PACKAGES.items()):
        value = sha((repo / package / "SHA256SUMS.txt").read_bytes())
        if corrupt and index == 0:
            value = "0" * 64
        if value != expected:
            raise GateError("FROZEN_PACKAGE", package)
        replay = run(repo / package, ["sha256sum", "--check", "SHA256SUMS.txt"])
        before = sorted(path for path in base_paths if path.startswith(package + "/"))
        after = sorted(path for path in current_paths if path.startswith(package + "/"))
        if not before or before != after:
            raise GateError("FROZEN_PACKAGE", package + ":paths")
        for path in before:
            if index_oids[path] != str(git(repo, "rev-parse", f"{BASE}:{path}")).strip():
                raise GateError("FROZEN_PACKAGE", path)
        output.append({"package": package, "entries": len(replay.splitlines()), "paths": len(before), "result": "PASS"})
    return output


def validate_navigation(repo: Path) -> dict[str, object]:
    current = tsv_rows(repo / "research/_registry/CURRENT_ARTIFACT_PATHS.tsv")
    paths = [row["current_path"] for row in current]
    if len(current) != 1114 or len(set(paths)) != 1114 or not all((repo / path).exists() for path in paths):
        raise GateError("NAVIGATION", "current")
    frontier = tsv_rows(repo / "research/_registry/CURRENT_FRONTIER_TARGETS.tsv")
    targets = {row["target_path"].rstrip("/") for row in frontier}
    if len(frontier) != 306 or len(targets) != 101 or not all((repo / path).exists() for path in targets):
        raise GateError("NAVIGATION", "frontier")
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links = []
    for source in sorted((repo / PACKAGE).glob("*.md")):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            links.append(source.parent.joinpath(target).resolve())
    if not all(path.exists() for path in links):
        raise GateError("NAVIGATION", "links")
    return {"current_paths": len(current), "frontier_rows": len(frontier), "frontier_targets": len(targets), "links": len(links)}


def dirty_metadata(repo: Path) -> dict[str, tuple[str, int, str]]:
    records = bytes(git(repo, "status", "--porcelain=v2", "-z", "--untracked-files=all", binary=True)).split(b"\0")
    output: dict[str, tuple[str, int, str]] = {}
    index = 0
    while index < len(records):
        record = records[index]; index += 1
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
        output[path] = (code, info.st_size, kind)
    return output


def validate_dirty(repo: Path, dirty_checkout: Path, corrupt: bool = False) -> int:
    recorded = {row["path"]: row for row in tsv_rows(repo / "reorganization_r1b/postmove_forensic_census/DIRTY_WORKSTATION_INVENTORY.tsv")}
    observed = dirty_metadata(dirty_checkout)
    if corrupt:
        observed = dict(observed); observed.pop(next(iter(observed)))
    if len(recorded) != 54 or len(observed) != 54 or set(recorded) != set(observed):
        raise GateError("DIRTY_METADATA", f"{len(recorded)}/{len(observed)}")
    for path, value in observed.items():
        row = recorded[path]
        if value != (row["status"], int(row["size_bytes_lstat"]), row["object_type"]) or row["content_sha256"] != "NOT_READ":
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
    result = validate_result(repo)
    ledger = validate_ledgers(repo)
    exact = exact_algebra()
    report = validate_report(repo)
    cpu = validate_cpu(repo)
    manifest = validate_manifest(repo)
    frozen = validate_frozen(repo)
    navigation = validate_navigation(repo)
    dirty = validate_dirty(repo, args.dirty_checkout.resolve())
    tests = json.loads(args.test_result.read_text(encoding="utf-8"))
    if (tests.get("passed"), tests.get("failed"), tests.get("xfailed"), tests.get("baseline_match")) != (69, 1, 1, True):
        raise GateError("TEST_BASELINE", str(tests))
    base_claims = {key: False for key in [
        "literal_infinity_is_invertible", "zero_times_infinity_equals_one",
        "nonreciprocal_countermodel_currently_admissible", "constant_background_is_curvature",
        "units_select_foundation", "adopt_abandon_reciprocity", "adopt_infinite_c",
        "line_realization_closed", "action_or_variation_selected", "H5_no_signalling_already_proved",
        "atemporal_layer_is_literal_speed_without_time_distance",
        "full_4d_equivalence_claimed", "coordinate_speed_is_scalar", "local_c_varies_with_phi",
        "distance_CMB_endpoint_map_derived", "H5A_H5B_conflated", "historical_electron_picture_derived",
    ]}
    catches = {
        "literal_infinity_invertibility_rejected": catch("INFINITE_INVERTIBILITY", lambda: validate_claims({**base_claims, "literal_infinity_is_invertible": True})),
        "zero_times_infinity_identity_rejected": catch("INDETERMINATE_PRODUCT", lambda: validate_claims({**base_claims, "zero_times_infinity_equals_one": True})),
        "singular_endpoint_as_invertible_reciprocal_element_rejected": catch("SINGULAR_ENDPOINT", lambda: exact_algebra(force_singular_endpoint=True)),
        "determinant_one_gauge_as_pairing_proof_rejected": catch("PAIRING_FROM_GAUGE", lambda: exact_algebra(force_pairing_from_gauge=True)),
        "countermodel_current_admissibility_rejected": catch("CURRENT_LEDGER", lambda: validate_claims({**base_claims, "nonreciprocal_countermodel_currently_admissible": True})),
        "CSN_related_metric_distinction_rejected": catch("CSN_METRIC", lambda: exact_algebra(force_metric_distinction=True)),
        "constant_background_curvature_claim_rejected": catch("CONSTANT_WARP", lambda: validate_claims({**base_claims, "constant_background_is_curvature": True})),
        "deformed_effective_lorentz_claim_rejected": catch("LORENTZ_DEFORMATION", lambda: exact_algebra(force_deformed_boost=True)),
        "unit_value_foundation_selector_rejected": catch("UNIT_ARGUMENT", lambda: validate_claims({**base_claims, "units_select_foundation": True})),
        "reciprocity_abandonment_adoption_rejected": catch("FOUNDATION_MUTATION", lambda: validate_claims({**base_claims, "adopt_abandon_reciprocity": True})),
        "literal_infinite_c_adoption_rejected": catch("FOUNDATION_MUTATION", lambda: validate_claims({**base_claims, "adopt_infinite_c": True})),
        "line_realization_promotion_rejected": catch("LINE_PROMOTION", lambda: validate_claims({**base_claims, "line_realization_closed": True})),
        "action_variation_promotion_rejected": catch("ACTION_PROMOTION", lambda: validate_claims({**base_claims, "action_or_variation_selected": True})),
        "H5_no_signalling_promotion_rejected": catch("NO_SIGNALLING_PROMOTION", lambda: validate_claims({**base_claims, "H5_no_signalling_already_proved": True})),
        "atemporal_speed_type_confusion_rejected": catch("TYPE_CONFUSION", lambda: validate_claims({**base_claims, "atemporal_layer_is_literal_speed_without_time_distance": True})),
        "full_4d_equivalence_promotion_rejected": catch("FULL4D_PROMOTION", lambda: validate_claims({**base_claims, "full_4d_equivalence_claimed": True})),
        "coordinate_null_slope_as_scalar_rejected": catch("COORDINATE_SCALAR", lambda: validate_claims({**base_claims, "coordinate_speed_is_scalar": True})),
        "local_c_variation_promotion_rejected": catch("LOCAL_C_PROMOTION", lambda: validate_claims({**base_claims, "local_c_varies_with_phi": True})),
        "distance_CMB_endpoint_map_promotion_rejected": catch("ENDPOINT_MAP_PROMOTION", lambda: validate_claims({**base_claims, "distance_CMB_endpoint_map_derived": True})),
        "H5A_H5B_conflation_rejected": catch("LAYER_CONFLATION", lambda: validate_claims({**base_claims, "H5A_H5B_conflated": True})),
        "historical_electron_picture_promotion_rejected": catch("HISTORICAL_PROMOTION", lambda: validate_claims({**base_claims, "historical_electron_picture_derived": True})),
        "status_contract_corruption_rejected": catch("STATUS_CONTRACT", lambda: validate_result(repo, corrupt=True)),
        "source_mutation_rejected": catch("SOURCE_HASH", lambda: validate_sources(repo, corrupt=True)),
        "scope_escape_rejected": catch("SCOPE", lambda: validate_scope(repo, "LIVE.md")),
        "frozen_package_mutation_rejected": catch("FROZEN_PACKAGE", lambda: validate_frozen(repo, corrupt=True)),
        "dirty_metadata_drift_rejected": catch("DIRTY_METADATA", lambda: validate_dirty(repo, args.dirty_checkout.resolve(), corrupt=True)),
    }
    verification = {
        "result": "PASS", "mode": "INDEPENDENT_CPU_ONLY_INFINITE_C_RECIPROCITY_ADJUDICATION",
        "base": BASE, "preregistration_commit": str(git(repo, "rev-parse", PREREG)).strip(),
        "reported_outcome": result["top_level_outcome"], "changed_paths": changed,
        "source_hashes": sources, "independent_exact_algebra": exact, "ledger": ledger,
        "report_and_reviews": report, "cpu_dependency": cpu, "package_manifest": manifest,
        "frozen_package_replays": frozen, "navigation": navigation, "test_baseline": tests,
        "dirty_checkout_metadata_rows": dirty, "dirty_content_policy": "NOT_READ",
        "catchproof": catches, "artifact_moves": 0, "gpu_used": False,
        "current_foundation_changed": False, "grok_integration_authorized": False,
    }
    payload = json.dumps(verification, indent=2, sort_keys=True) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
