#!/usr/bin/env python3
"""Independent fail-closed verifier for invariant reciprocal causal flow."""

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


BASE = "f813572826bcabd8c2dfe3c247f6a709e3eee508"
PREREG = "38077b0cb3257325a783bd6532a1a42ed6ebb101"
PACKAGE = "invariant_reciprocal_causal_flow_2026-07-18"
OUTCOME = "STATIC_OPTICAL_REALIZATION_CONDITIONAL_UNIVERSAL_REALIZATION_OPEN"
SOURCE_HASHES = {
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md": "6e977717ca028cabaa198dd14a6a97b3b15740e45485d0ab735f3df0326df192",
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md": "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "4bb0da9098da0a9970602e2449615eef151796b0d7fe7a9978f4b66145748a34",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": "70cab9d5e10b03e0e3418129b67155e01d9f805c4397c69ef8795c4d2aaa5dfd",
    "reciprocity_offshell_constraint_selector_2026-07-18/SHA256SUMS.txt": "3f6da5926200f68e07b67a167948b2211d0a506fa65d322e600a7d22b080c74a",
    "reciprocal_line_realization_selector_2026-07-18/SHA256SUMS.txt": "4fe297e81414977f5eb75b6e535e1fca0f60a1d872e1fd42921f25aee0e59a16",
    "infinite_c_reciprocity_adjudication_2026-07-18/SHA256SUMS.txt": "f15235b149dd915aabcefbb405a776234fb4a68ac8da4b706a09583d3c64a5f6",
    "infinite_c_reciprocity_adjudication_2026-07-18/DERIVATION_RESULT.json": "2c88a586feddca236ca86eabf46e243c526c45e6f9a5cf55ddec206438ab7188",
    "infinite_c_reciprocity_adjudication_2026-07-18/STATUS_LEDGER.tsv": "e984654e1f649f2a9d9daca20fa41a88f3122a8231fcd61482025b4141037988",
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
    "POST_PREREG_SUBSTRATE_FALLBACK.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "REVIEW_BOUNDARY_SUBSTRATE.md",
    "REVIEW_INVARIANT_GEOMETRY.md",
    "STATUS_LEDGER.tsv",
    "derive_invariant_causal_flow.py",
    "requirements-cpu.txt",
    "verify_invariant_causal_flow.py",
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
    if resolved != PREREG or parent != BASE or paths != [f"{PACKAGE}/PREREGISTRATION.md"]:
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


def exact_algebra(*, finite_optical: bool = False, infinite_proper: bool = False,
                  csn_changes: bool = False, singular_wall: bool = False) -> dict[str, object]:
    c0, phi, omega, jacobian, scale = sp.symbols(
        "c0 phi omega jacobian scale", positive=True, finite=True
    )
    lapse = sp.exp(-phi)
    hrr = sp.exp(2 * phi)
    optical = sp.simplify(hrr / lapse**2)
    speed = sp.simplify(c0 * lapse / sp.sqrt(hrr))
    local = sp.simplify(sp.sqrt(hrr) * speed / lapse)
    if optical != sp.exp(4 * phi) or speed != c0 * sp.exp(-2 * phi) or local != c0:
        raise GateError("ALGEBRA", "reciprocal static block")
    if csn_changes or sp.simplify((omega**2 * hrr) / (omega * lapse) ** 2) != optical:
        raise GateError("CSN_INVARIANCE", "optical")
    if sp.simplify(sp.sqrt(optical) * sp.sqrt(optical.subs(phi, -phi))) != 1:
        raise GateError("ALGEBRA", "reciprocal stretch")
    transformed_optical = sp.simplify(optical * jacobian**2)
    transformed_speed = sp.simplify(speed / jacobian)
    if sp.simplify(transformed_speed * sp.sqrt(transformed_optical) / c0) != 1:
        raise GateError("ALGEBRA", "coordinate transform")
    if sp.simplify(hrr / (lapse / scale) ** 2 - scale**2 * optical) != 0:
        raise GateError("ALGEBRA", "time normalization")
    transformed_stretch_product = sp.simplify(
        sp.sqrt(transformed_optical) * sp.sqrt(transformed_optical.subs(phi, -phi))
    )
    rescaled_optical = sp.simplify(scale**2 * optical)
    rescaled_stretch_product = sp.simplify(
        sp.sqrt(rescaled_optical) * sp.sqrt(rescaled_optical.subs(phi, -phi))
    )
    if transformed_stretch_product != jacobian**2 or rescaled_stretch_product != scale**2:
        raise GateError("ALGEBRA", "component reciprocity frame pins")

    r, X = sp.symbols("r X", positive=True, finite=True)
    A = 1 - r / X
    proper = 2 * X * (1 - sp.sqrt(A))
    optical_distance = -X * sp.log(A)
    proper_wall = sp.limit(proper, r, X, dir="-")
    optical_wall = sp.limit(optical_distance, r, X, dir="-")
    if finite_optical or optical_wall != sp.oo:
        raise GateError("FINITE_OPTICAL_WALL", str(optical_wall))
    if infinite_proper or proper_wall != 2 * X:
        raise GateError("INFINITE_PROPER_WALL", str(proper_wall))
    r0 = sp.symbols("r0", positive=True, finite=True)
    A0 = 1 - r0 / X
    proper_from_r0 = 2 * X * (sp.sqrt(A0) - sp.sqrt(A))
    optical_from_r0 = X * sp.log(A0 / A)
    proper_r0_wall = sp.limit(proper_from_r0, r, X, dir="-")
    optical_r0_wall = sp.limit(optical_from_r0, r, X, dir="-")
    if sp.simplify(proper_r0_wall / (2 * X * sp.sqrt(A0))) != 1 or optical_r0_wall != sp.oo:
        raise GateError("ALGEBRA", "regular interior start")

    rho = sp.symbols("rho", positive=True, finite=True)
    r_of_rho = X - rho**2 / (4 * X)
    A_rho = sp.simplify(A.subs(r, r_of_rho))
    radial = sp.simplify((1 / A_rho) * sp.diff(r_of_rho, rho) ** 2)
    temporal = sp.simplify(-A_rho * c0**2)
    if radial != 1 or temporal != -c0**2 * rho**2 / (4 * X**2):
        raise GateError("ALGEBRA", "Rindler map")
    ef = sp.Matrix([[-A * c0**2, c0], [c0, 0]])
    if ef.det() != -c0**2:
        raise GateError("ALGEBRA", "EF determinant")
    theta = sp.symbols("theta", real=True, finite=True)
    ef_full_determinant = sp.simplify(ef.det() * r**4 * sp.sin(theta) ** 2)
    if ef_full_determinant != -c0**2 * r**4 * sp.sin(theta) ** 2:
        raise GateError("ALGEBRA", "full EF determinant")
    curvature_R = sp.simplify(-sp.diff(A, r, 2) - 4 * sp.diff(A, r) / r + 2 * (1 - A) / r**2)
    curvature_K = sp.simplify(sp.diff(A, r, 2) ** 2 + 4 * (sp.diff(A, r) / r) ** 2 + 4 * ((1 - A) / r**2) ** 2)
    wall_curvature = [sp.limit(curvature_R, r, X, dir="-"), sp.limit(curvature_K, r, X, dir="-")]
    if singular_wall or wall_curvature != [6 / X**2, 8 / X**4]:
        raise GateError("CURVATURE_WALL", str(wall_curvature))

    kappa, rho_r = sp.symbols("kappa rho_R", positive=True, finite=True)
    rindler_lapse = kappa * rho_r / c0
    rindler_speed = sp.simplify(c0 * rindler_lapse)
    if rindler_speed != kappa * rho_r or sp.simplify(rindler_speed / rindler_lapse) != c0:
        raise GateError("ALGEBRA", "flat observer counterexample")
    t_r = sp.symbols("t_R", real=True, finite=True)
    minkowski_coordinates = sp.Matrix([rho_r * sp.sinh(kappa * t_r), rho_r * sp.cosh(kappa * t_r)])
    coordinate_jacobian = minkowski_coordinates.jacobian([t_r, rho_r])
    rindler_pullback = sp.simplify(coordinate_jacobian.T * sp.diag(-1, 1) * coordinate_jacobian)
    if rindler_pullback != sp.diag(-kappa**2 * rho_r**2, 1):
        raise GateError("ALGEBRA", "explicit Minkowski/Rindler pullback")
    return {
        "result": "PASS",
        "optical_rr": str(optical),
        "coordinate_slope": str(speed),
        "local_proper_speed": str(local),
        "reciprocal_stretch_product": "1",
        "frame_pinned_stretch_products": [str(transformed_stretch_product), str(rescaled_stretch_product)],
        "WRL_proper_wall": str(proper_wall),
        "WRL_optical_wall": str(optical_wall),
        "WRL_regular_start_wall": [str(proper_r0_wall), str(optical_r0_wall)],
        "WRL_Rindler_block": [str(temporal), str(radial)],
        "WRL_EF_determinant": str(ef.det()),
        "WRL_full_EF_determinant": str(ef_full_determinant),
        "WRL_curvature": [str(curvature_R), str(curvature_K)],
        "WRL_wall_curvature": [str(value) for value in wall_curvature],
        "flat_Rindler_coordinate_slope": str(rindler_speed),
        "Minkowski_Rindler_pullback": str(rindler_pullback),
    }


def base_claims() -> dict[str, bool]:
    return {key: False for key in [
        "coordinate_speed_is_scalar",
        "local_c_varies",
        "optical_metric_without_static_flow",
        "rindler_coordinate_variation_proves_curvature",
        "minkowski_selects_unique_observer",
        "normalization_metric_selected",
        "wall_is_material_from_metric",
        "wall_is_CMB",
        "wall_is_substrate",
        "static_promoted_time_live",
        "optical_proves_internal_pairing",
        "line_selector_closed",
        "action_source_carrier_selected",
        "substrate_recycling_derived",
        "observable_superluminal_signalling",
        "WRL_center_regular",
    ]}


def validate_claims(claims: dict[str, bool]) -> None:
    rejected = {
        "coordinate_speed_is_scalar": "COORDINATE_SCALAR",
        "local_c_varies": "LOCAL_C_PROMOTION",
        "optical_metric_without_static_flow": "STATIC_FLOW_OMITTED",
        "rindler_coordinate_variation_proves_curvature": "RINDLER_CURVATURE",
        "minkowski_selects_unique_observer": "OBSERVER_SELECTION",
        "normalization_metric_selected": "NORMALIZATION_PROMOTION",
        "wall_is_material_from_metric": "MATERIAL_WALL_PROMOTION",
        "wall_is_CMB": "CMB_PROMOTION",
        "wall_is_substrate": "SUBSTRATE_PROMOTION",
        "static_promoted_time_live": "TIME_LIVE_PROMOTION",
        "optical_proves_internal_pairing": "PAIRING_PROMOTION",
        "line_selector_closed": "LINE_PROMOTION",
        "action_source_carrier_selected": "DYNAMICS_PROMOTION",
        "substrate_recycling_derived": "RECYCLING_PROMOTION",
        "observable_superluminal_signalling": "SIGNALLING_PROMOTION",
        "WRL_center_regular": "CENTER_REGULARITY",
    }
    for key, code in rejected.items():
        if claims.get(key):
            raise GateError(code, key)


def validate_result(repo: Path, corrupt: bool = False) -> dict[str, object]:
    result = json.loads((repo / PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    if corrupt:
        result = copy.deepcopy(result)
        result["adjudication"]["WRL_metric_alone_proves_material_wall_or_substrate"] = True
    expected_classes = {
        "I0_UNIVERSAL_METRIC_ONLY_LOCAL_CAUSAL_SCALAR_OR_FLOW": "NULL_CONE_DERIVED_SPEED_DECOMPOSITION_NOT_UNIVERSAL",
        "I1_STATIC_OPTICAL_REALIZATION": "DERIVED_CONDITIONAL_ON_STATIC_FLOW_QUOTIENT_AND_NORMALIZATION",
        "I2_STATIONARY_REALIZATION": "FERMAT_RANDERS_EXTENSION_CONDITIONAL_NOT_EXECUTED",
        "I3_GENERAL_TIME_LIVE_REALIZATION": "OPEN_FULL_NULL_ARRIVAL_MAP_REQUIRED",
        "I4_FINITE_CELL_GLOBAL_COMPLETION": "OPEN_BOUNDARY_MATCHING_AND_NORMALIZATION_REQUIRED",
        "I5_SUBSTRATE_RECYCLING_FALLBACK": "OPEN_SEPARATE_ONTOLOGY_AND_DYNAMICS_NOT_USED",
    }
    adjudication = result.get("adjudication", {})
    required_true = [
        "metric_determines_null_cone",
        "static_optical_metric_CSN_invariant_given_static_flow",
        "integrated_static_optical_arrival_is_coordinate_invariant",
        "WRL_wall_is_finite_proper_distance",
        "WRL_wall_is_infinite_static_optical_distance",
    ]
    required_false = [
        "coordinate_null_slope_is_scalar",
        "local_orthonormal_light_speed_varies_with_phi",
        "physical_matter_clocks_signals_proven_to_follow_metric_cone",
        "metric_universally_selects_observer_and_parallel_line",
        "Killing_normalization_selected_without_reference_data",
        "WRL_wall_is_curvature_singularity",
        "WRL_metric_alone_proves_material_wall_or_substrate",
        "WRL_full4D_center_is_regular",
        "WRL_static_wall_identified_with_CMB",
        "static_result_establishes_time_live_cosmology",
        "optical_reciprocity_proves_internal_K_pairing",
        "line_realization_gap_closed",
        "native_action_source_carrier_or_boundary_charge_selected",
        "substrate_recycling_mechanism_derived",
    ]
    if (
        result.get("schema") != "udt.invariant-reciprocal-causal-flow.v1"
        or result.get("top_level_outcome") != OUTCOME
        or result.get("check_count") != 38
        or len(result.get("checks", {})) != 38
        or not all(result.get("checks", {}).values())
        or result.get("class_results") != expected_classes
        or any(adjudication.get(key) is not True for key in required_true)
        or any(adjudication.get(key) is not False for key in required_false)
    ):
        raise GateError("STATUS_CONTRACT", str(adjudication))
    return result


def validate_ledgers(repo: Path) -> dict[str, object]:
    rows = tsv_rows(repo / PACKAGE / "STATUS_LEDGER.tsv")
    statuses = {row["id"]: row["status"] for row in rows}
    expected = {
        "S01": "DERIVED_FROM_METRIC",
        "S02": "NO",
        "S03": "DERIVED_CONDITIONAL_READOUT",
        "S04": "DERIVED_CONDITIONAL",
        "S05": "DERIVED_CONDITIONAL",
        "S06": "REQUIRED",
        "S07": "DERIVED_CONDITIONAL",
        "S08": "DERIVED_CONDITIONAL",
        "S09": "NO",
        "S10": "NO_UNIVERSAL_LOCAL_SELECTOR",
        "S11": "NO",
        "S12": "DERIVED_CONDITIONAL",
        "S13": "DERIVED_CONDITIONAL",
        "S14": "DERIVED_CONDITIONAL",
        "S15": "DERIVED_CONDITIONAL",
        "S16": "DERIVED_LOCAL_EXTENSION",
        "S17": "DERIVED_CONDITIONAL",
        "S18": "NO",
        "S19": "NOT_DERIVED",
        "S20": "OPEN_SEPARATE_HYPOTHESIS",
        "S21": "OPEN_SEPARATE_HYPOTHESIS",
        "S22": "OPEN",
        "S23": "CONDITIONAL_EXTENSION",
        "S24": "OPEN",
        "S25": "OPEN",
        "S26": "OPEN",
        "S27": "OPEN",
        "S28": "OPEN",
        "S29": "NOT_AUTHORIZED",
        "S30": OUTCOME,
    }
    premises = tsv_rows(repo / PACKAGE / "PREMISE_LEDGER.tsv")
    if len(rows) != 30 or statuses != expected or len(premises) != 18:
        raise GateError("LEDGER_CONTRACT", f"{len(rows)}:{len(premises)}")
    return {"result": "PASS", "status_rows": len(rows), "premise_rows": len(premises)}


def validate_report(repo: Path) -> dict[str, object]:
    report = (repo / PACKAGE / "DERIVATION_REPORT.md").read_text(encoding="utf-8")
    decision = (repo / PACKAGE / "LAY_DECISION_TREE.md").read_text(encoding="utf-8")
    substrate = (repo / PACKAGE / "POST_PREREG_SUBSTRATE_FALLBACK.md").read_text(encoding="utf-8")
    review_a = (repo / PACKAGE / "REVIEW_INVARIANT_GEOMETRY.md").read_text(encoding="utf-8")
    review_b = (repo / PACKAGE / "REVIEW_BOUNDARY_SUBSTRATE.md").read_text(encoding="utf-8")
    audit = (repo / PACKAGE / "ADVERSARIAL_AUDIT.md").read_text(encoding="utf-8")
    required = [
        OUTCOME,
        "optical travel geometry",
        "h^{\\rm opt}_{rr}=e^{4\\phi}",
        "q(\\phi)q(-\\phi)=1",
        "Flat Minkowski spacetime is the decisive counterexample",
        "D_{\\rm prop}(X^-)=2X",
        "D_{\\rm opt}(X^-)=\\infty",
        "exactly a Rindler block",
        "\\det g_{\\rm EF}=-c_0^2r^4\\sin^2\\theta",
        "R=\\frac{6}{Xr}",
        "material edge, energy substrate, CMB, or recycling surface",
        "native UDT structure selects the timelike clock flow",
        "\\mathcal L_K\\Omega=0",
        "canonical static mirror seal",
        "owner-termed",
    ]
    missing = [token for token in required if token not in report]
    if (
        missing
        or "separate open hypothesis" not in decision
        or "not treated as a premise" not in substrate
        or "PASS" not in review_a
        or "PASS" not in review_b
        or "No files were changed" not in audit
    ):
        raise GateError("REPORT_CONTRACT", missing[0] if missing else "supporting record")
    return {"result": "PASS", "report_tokens": len(required), "reviews": 2}


def validate_cpu(repo: Path) -> dict[str, object]:
    imports: set[str] = set()
    for name in ("derive_invariant_causal_flow.py", "verify_invariant_causal_flow.py"):
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
        record = records[index]
        index += 1
        if not record:
            continue
        marker = record[:1]
        if marker == b"1":
            fields = record.split(b" ", 8)
            code, raw_path = fields[1].decode(), fields[8]
        elif marker == b"2":
            fields = record.split(b" ", 9)
            code, raw_path = fields[1].decode(), fields[9]
            index += 1
        elif marker == b"u":
            fields = record.split(b" ", 10)
            code, raw_path = fields[1].decode(), fields[10]
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
        observed = dict(observed)
        observed.pop(next(iter(observed)))
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
    ledgers = validate_ledgers(repo)
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

    claims = base_claims()
    catches = {
        "coordinate_speed_scalar_rejected": catch("COORDINATE_SCALAR", lambda: validate_claims({**claims, "coordinate_speed_is_scalar": True})),
        "local_c_variation_rejected": catch("LOCAL_C_PROMOTION", lambda: validate_claims({**claims, "local_c_varies": True})),
        "CSN_noninvariance_rejected": catch("CSN_INVARIANCE", lambda: exact_algebra(csn_changes=True)),
        "missing_static_flow_rejected": catch("STATIC_FLOW_OMITTED", lambda: validate_claims({**claims, "optical_metric_without_static_flow": True})),
        "Rindler_curvature_claim_rejected": catch("RINDLER_CURVATURE", lambda: validate_claims({**claims, "rindler_coordinate_variation_proves_curvature": True})),
        "unique_Minkowski_observer_rejected": catch("OBSERVER_SELECTION", lambda: validate_claims({**claims, "minkowski_selects_unique_observer": True})),
        "missing_normalization_rejected": catch("NORMALIZATION_PROMOTION", lambda: validate_claims({**claims, "normalization_metric_selected": True})),
        "finite_WRL_optical_wall_rejected": catch("FINITE_OPTICAL_WALL", lambda: exact_algebra(finite_optical=True)),
        "infinite_WRL_proper_wall_rejected": catch("INFINITE_PROPER_WALL", lambda: exact_algebra(infinite_proper=True)),
        "WRL_curvature_singularity_rejected": catch("CURVATURE_WALL", lambda: exact_algebra(singular_wall=True)),
        "material_wall_from_metric_rejected": catch("MATERIAL_WALL_PROMOTION", lambda: validate_claims({**claims, "wall_is_material_from_metric": True})),
        "CMB_wall_identity_rejected": catch("CMB_PROMOTION", lambda: validate_claims({**claims, "wall_is_CMB": True})),
        "substrate_from_metric_rejected": catch("SUBSTRATE_PROMOTION", lambda: validate_claims({**claims, "wall_is_substrate": True})),
        "static_to_time_live_promotion_rejected": catch("TIME_LIVE_PROMOTION", lambda: validate_claims({**claims, "static_promoted_time_live": True})),
        "optical_to_internal_pairing_promotion_rejected": catch("PAIRING_PROMOTION", lambda: validate_claims({**claims, "optical_proves_internal_pairing": True})),
        "line_selector_promotion_rejected": catch("LINE_PROMOTION", lambda: validate_claims({**claims, "line_selector_closed": True})),
        "action_source_carrier_promotion_rejected": catch("DYNAMICS_PROMOTION", lambda: validate_claims({**claims, "action_source_carrier_selected": True})),
        "substrate_recycling_promotion_rejected": catch("RECYCLING_PROMOTION", lambda: validate_claims({**claims, "substrate_recycling_derived": True})),
        "superluminal_signalling_promotion_rejected": catch("SIGNALLING_PROMOTION", lambda: validate_claims({**claims, "observable_superluminal_signalling": True})),
        "WRL_center_regularity_rejected": catch("CENTER_REGULARITY", lambda: validate_claims({**claims, "WRL_center_regular": True})),
        "status_corruption_rejected": catch("STATUS_CONTRACT", lambda: validate_result(repo, corrupt=True)),
        "source_mutation_rejected": catch("SOURCE_HASH", lambda: validate_sources(repo, corrupt=True)),
        "scope_escape_rejected": catch("SCOPE", lambda: validate_scope(repo, "LIVE.md")),
        "frozen_package_mutation_rejected": catch("FROZEN_PACKAGE", lambda: validate_frozen(repo, corrupt=True)),
        "dirty_metadata_drift_rejected": catch("DIRTY_METADATA", lambda: validate_dirty(repo, args.dirty_checkout.resolve(), corrupt=True)),
    }
    verification = {
        "result": "PASS",
        "mode": "INDEPENDENT_CPU_ONLY_INVARIANT_RECIPROCAL_CAUSAL_FLOW",
        "base": BASE,
        "preregistration_commit": PREREG,
        "reported_outcome": result["top_level_outcome"],
        "changed_paths": changed,
        "source_hashes": sources,
        "independent_exact_algebra": exact,
        "ledgers": ledgers,
        "report_and_reviews": report,
        "cpu_dependency": cpu,
        "package_manifest": manifest,
        "frozen_package_replays": frozen,
        "navigation": navigation,
        "test_baseline": tests,
        "dirty_checkout_metadata_rows": dirty,
        "dirty_content_policy": "NOT_READ",
        "catchproof": catches,
        "artifact_moves": 0,
        "gpu_used": False,
        "current_foundation_changed": False,
        "substrate_recycling_derived": False,
        "grok_integration_authorized": False,
    }
    payload = json.dumps(verification, indent=2, sort_keys=True) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
