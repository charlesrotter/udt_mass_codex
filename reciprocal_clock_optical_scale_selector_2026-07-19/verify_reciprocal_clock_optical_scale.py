#!/usr/bin/env python3
"""Independent fail-closed verifier for the clock–optical–scale selector."""

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


BASE = "2092a047da4b1267eabdb6be59e5b50b41e3db62"
PREREG = "a1a2fd15b362931feb815289318efa74bdec15b3"
PACKAGE = "reciprocal_clock_optical_scale_selector_2026-07-19"
OUTCOME = "RECIPROCAL_CLOCK_OPTICAL_LINK_DERIVED_SCALE_REALIZATION_AND_MASS_OPEN"
SOURCE_HASHES = {
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md": "6e977717ca028cabaa198dd14a6a97b3b15740e45485d0ab735f3df0326df192",
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md": "b2bdf9dd427871c6e951c6b47748b7663aa4a6264fcfcbff59b51f1ea2272003",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "4bb0da9098da0a9970602e2449615eef151796b0d7fe7a9978f4b66145748a34",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": "70cab9d5e10b03e0e3418129b67155e01d9f805c4397c69ef8795c4d2aaa5dfd",
    "reciprocal_line_realization_selector_2026-07-18/SHA256SUMS.txt": "4fe297e81414977f5eb75b6e535e1fca0f60a1d872e1fd42921f25aee0e59a16",
    "infinite_c_reciprocity_adjudication_2026-07-18/SHA256SUMS.txt": "f15235b149dd915aabcefbb405a776234fb4a68ac8da4b706a09583d3c64a5f6",
    "invariant_reciprocal_causal_flow_2026-07-18/SHA256SUMS.txt": "786f3dc190d929bac6540a452c4bade8c41517f2169dfdc7de13daf46978801c",
    "invariant_reciprocal_causal_flow_2026-07-18/DERIVATION_RESULT.json": "491401f2235ee3c33ec2e637845b20ba7c3b2199ef9d9163a494313b12c836f4",
    "invariant_reciprocal_causal_flow_2026-07-18/STATUS_LEDGER.tsv": "f490bba0c4b0fc819f575e0d3062d8e78529901303d0d7df2d080746d0f98ef0",
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
    "POST_PREREG_SCALE_SYMBOL_CLARIFICATION.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "REVIEW_MASS_COSMOLOGY.md",
    "REVIEW_SCALE_CAUSALITY.md",
    "STATUS_LEDGER.tsv",
    "derive_reciprocal_clock_optical_scale.py",
    "requirements-cpu.txt",
    "verify_reciprocal_clock_optical_scale.py",
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


def exact_algebra(*, omit_ruler: bool = False, miss_square: bool = False,
                  common_changes: bool = False, mass_increases: bool = False,
                  floor_confusion: bool = False) -> dict[str, object]:
    c0, N, B = sp.symbols("c0 N B", positive=True, finite=True)
    speed = sp.simplify(c0 * N / B)
    local = sp.simplify(B * speed / N)
    optical = sp.simplify(B / N)
    if omit_ruler or speed != c0 * N / B:
        raise GateError("RULER_OMITTED", str(speed))
    if local != c0:
        raise GateError("ALGEBRA", "local null speed")

    Ne, No, Be, Bo = sp.symbols("Ne No Be Bo", positive=True, finite=True)
    z1 = No / Ne
    general_ratio = sp.simplify((c0 * Ne / Be) / (c0 * No / Bo))
    if general_ratio != sp.simplify((1 / z1) * (Bo / Be)):
        raise GateError("ALGEBRA", "general redshift relation")
    reciprocal_ratio = sp.simplify(general_ratio.subs({Be: 1 / Ne, Bo: 1 / No}))
    reciprocal_optical_ratio = sp.simplify(((Be / Ne) / (Bo / No)).subs({Be: 1 / Ne, Bo: 1 / No}))
    if miss_square or reciprocal_ratio != z1**-2 or reciprocal_optical_ratio != z1**2:
        raise GateError("RECIPROCAL_SQUARE", f"{reciprocal_ratio}:{reciprocal_optical_ratio}")
    Je, Jo = sp.symbols("Je Jo", positive=True, finite=True)
    transformed_ratios = [sp.simplify(reciprocal_ratio * Jo / Je), sp.simplify(reciprocal_optical_ratio * Je / Jo)]
    if transformed_ratios != [reciprocal_ratio * Jo / Je, reciprocal_optical_ratio * Je / Jo]:
        raise GateError("ALGEBRA", "endpoint radial standards")

    slopes = [sp.simplify(speed.subs(B, 1)), sp.simplify(speed.subs(B, N)), sp.simplify(speed.subs(B, 1 / N))]
    if slopes != [c0 * N, c0, c0 * N**2]:
        raise GateError("ALGEBRA", "countermodels")
    Omega = sp.symbols("Omega", positive=True, finite=True)
    csn_speed = sp.simplify(c0 * Omega * N / (Omega * B))
    if common_changes or csn_speed != speed:
        raise GateError("COMMON_SCALE", str(csn_speed))
    Omega_e, Omega_o, J, lambda_t = sp.symbols("Omega_e Omega_o J lambda_t", positive=True, finite=True)
    csn_redshift = sp.simplify((Omega_o * No) / (Omega_e * Ne))
    if csn_redshift != (Omega_o / Omega_e) * z1:
        raise GateError("ALGEBRA", "endpoint CSN redshift")
    reciprocal_constraint_transforms = [sp.simplify(N * (J / N)), sp.simplify((N / lambda_t) * (1 / N)), sp.simplify((Omega * N) * (Omega / N))]
    if reciprocal_constraint_transforms != [J, 1 / lambda_t, Omega**2]:
        raise GateError("ALGEBRA", "NB representative pins")

    m, hbar = sp.symbols("m hbar", positive=True, finite=True)
    local_energy = m * c0**2
    compton = local_energy / hbar
    observer_energy = sp.simplify(Ne * local_energy / No)
    if mass_increases or observer_energy != local_energy / z1 or compton != m * c0**2 / hbar:
        raise GateError("MASS_PROMOTION", str(observer_energy))

    phi = sp.symbols("phi", real=True, finite=True)
    scale_speed = c0 * sp.exp(-2 * phi)
    scale_optical = sp.exp(2 * phi)
    if sp.simplify(scale_speed * scale_speed.subs(phi, -phi)) != c0**2:
        raise GateError("ALGEBRA", "dual speed")
    if sp.simplify(scale_optical * scale_optical.subs(phi, -phi)) != 1:
        raise GateError("ALGEBRA", "dual optical")
    if floor_confusion or scale_speed.subs(phi, 0) != c0 or scale_optical.subs(phi, 0) != 1:
        raise GateError("SPEED_FLOOR", "one-sided terminology")
    return {
        "result": "PASS",
        "general_speed": str(speed),
        "local_metric_null_speed": str(local),
        "optical_stretch": str(optical),
        "one_plus_z": str(z1),
        "general_slope_ratio": str(general_ratio),
        "reciprocal_slope_ratio": str(reciprocal_ratio),
        "reciprocal_optical_ratio": str(reciprocal_optical_ratio),
        "radially_reparameterized_ratios": [str(value) for value in transformed_ratios],
        "endpoint_CSN_redshift": str(csn_redshift),
        "NB_constraint_transforms": [str(value) for value in reciprocal_constraint_transforms],
        "same_clock_slopes": [str(value) for value in slopes],
        "observer_energy": str(observer_energy),
        "dual_scale_speed_product": str(c0**2),
    }


def base_claims() -> dict[str, bool]:
    return {key: False for key in [
        "coordinate_speed_scalar",
        "local_c_varies",
        "redshift_speed_numerically_identical",
        "boxed_square_is_CSN_physical_theorem",
        "NB_one_is_invariant",
        "killing_energy_is_native_mass",
        "native_mass_constancy_derived",
        "photon_coupling_derived",
        "r_equals_ell",
        "single_local_metric_has_many_scale_cones",
        "pivot_selected",
        "plateau_proves_GR",
        "broad_plateau_derived",
        "unique_minimum_architecture_selected",
        "observer_line_gap_closed",
        "UV_speedup_foundationally_selected",
        "IR_profile_foundationally_selected",
        "superluminal_signalling_authorized",
        "coordinate_ceiling_is_invariant_signal_bound",
        "static_promoted_cosmology",
        "CMB_wall_seal_substrate_identified",
        "action_source_carrier_selected",
    ]}


def validate_claims(claims: dict[str, bool]) -> None:
    rejected = {
        "coordinate_speed_scalar": "COORDINATE_SCALAR",
        "local_c_varies": "LOCAL_C_PROMOTION",
        "redshift_speed_numerically_identical": "NUMERICAL_IDENTITY",
        "boxed_square_is_CSN_physical_theorem": "REPRESENTATIVE_PROMOTION",
        "NB_one_is_invariant": "REPRESENTATIVE_PROMOTION",
        "killing_energy_is_native_mass": "KILLING_MASS_PROMOTION",
        "native_mass_constancy_derived": "MASS_CONSTANCY_PROMOTION",
        "photon_coupling_derived": "PHOTON_COUPLING_PROMOTION",
        "r_equals_ell": "TYPE_CONFUSION",
        "single_local_metric_has_many_scale_cones": "SCALE_ARCHITECTURE",
        "pivot_selected": "PIVOT_PROMOTION",
        "plateau_proves_GR": "GR_PROMOTION",
        "broad_plateau_derived": "PLATEAU_PROMOTION",
        "unique_minimum_architecture_selected": "ARCHITECTURE_PROMOTION",
        "observer_line_gap_closed": "LINE_PROMOTION",
        "UV_speedup_foundationally_selected": "SCALE_PROFILE_PROMOTION",
        "IR_profile_foundationally_selected": "SCALE_PROFILE_PROMOTION",
        "superluminal_signalling_authorized": "SIGNALLING_PROMOTION",
        "coordinate_ceiling_is_invariant_signal_bound": "SIGNAL_BOUND_PROMOTION",
        "static_promoted_cosmology": "COSMOLOGY_PROMOTION",
        "CMB_wall_seal_substrate_identified": "BOUNDARY_PROMOTION",
        "action_source_carrier_selected": "DYNAMICS_PROMOTION",
    }
    for key, code in rejected.items():
        if claims.get(key):
            raise GateError(code, key)


def validate_result(repo: Path, corrupt: bool = False) -> dict[str, object]:
    result = json.loads((repo / PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    if corrupt:
        result = copy.deepcopy(result)
        result["adjudication"]["local_rest_mass_increase_derived_from_redshift"] = True
    expected_classes = {
        "J0_GENERAL_CLOCK_RULER_DECOMPOSITION": "TIME_DILATION_ALONE_INSUFFICIENT",
        "J1_UDT_RECIPROCAL_STATIC_BLOCK": "INVERSE_SQUARE_REDSHIFT_OPTICAL_LINK_DERIVED_CONDITIONAL",
        "J2_COUNTERMODELS": "SAME_CLOCK_FACTOR_THREE_DISTINCT_OPTICAL_RESPONSES",
        "J3_OPERATIONAL_ENERGY_AND_MASS": "STATIC_REDSHIFT_DOES_NOT_DERIVE_MASS_CHANGE_NATIVE_MASS_OPEN",
        "J4_RELATIONAL_SCALE_REALIZATION": "KINEMATIC_IDENTITIES_CONDITIONAL_ARCHITECTURE_AND_PROFILE_OPEN",
        "J5_ONE_SIDED_FALLBACK": "PINNED_ADAPTED_COORDINATE_SLOPE_CEILING_AND_OPTICAL_DENSITY_FLOOR",
    }
    adjudication = result.get("adjudication", {})
    required_true = [
        "time_dilation_and_effective_speed_share_one_dilation_field_in_reciprocal_block",
        "reciprocal_speed_ratio_is_inverse_redshift_squared",
        "boxed_square_relations_are_pinned_adapted_component_identities",
        "received_energy_redshift_derived_in_static_class",
        "one_sided_c0_is_pinned_adapted_coordinate_slope_ceiling",
        "one_sided_unity_is_pinned_optical_density_floor",
    ]
    required_false = [
        "time_dilation_alone_uniquely_determines_effective_speed",
        "boxed_square_relations_are_CSN_class_physical_redshift_theorems",
        "NB_equals_one_is_coordinate_time_normalization_or_local_CSN_invariant",
        "redshift_and_effective_speed_are_numerically_identical",
        "common_scale_dilation_changes_null_slope",
        "coordinate_effective_speed_is_local_scalar_constant",
        "local_rest_mass_increase_derived_from_redshift",
        "native_mass_emergence_or_mass_increase_derived",
        "native_invariant_mass_constancy_derived",
        "fixed_mass_compton_branch_is_native_UDT",
        "material_photon_emission_propagation_detection_coupling_derived",
        "coordinate_position_and_relational_scale_identical",
        "scale_indexed_metric_architecture_selected",
        "scale_realization_unique_minimum_architecture_selected",
        "UV_speedup_selected_by_current_foundation",
        "IR_slowdown_profile_selected_by_current_foundation",
        "ordinary_scale_plateau_thresholds_selected",
        "broad_ordinary_scale_plateau_tested",
        "dual_scale_pivot_selected",
        "operational_scale_involution_and_domain_selected",
        "same_scale_endpoint_or_cross_scale_coupling_rule_selected",
        "observable_superluminal_signalling_authorized",
        "one_sided_c0_is_speed_floor",
        "one_sided_c0_is_invariant_material_signal_speed_ceiling",
        "one_sided_unity_is_invariant_optical_scalar_floor",
        "prior_observer_line_representative_normalization_gap_closed",
        "static_result_promoted_to_time_live_or_CMB",
        "action_source_carrier_boundary_or_substrate_selected",
    ]
    if (
        result.get("schema") != "udt.reciprocal-clock-optical-scale-selector.v1"
        or result.get("top_level_outcome") != OUTCOME
        or result.get("check_count") != 45
        or len(result.get("checks", {})) != 45
        or not all(result.get("checks", {}).values())
        or result.get("class_results") != expected_classes
        or any(adjudication.get(key) is not True for key in required_true)
        or any(adjudication.get(key) is not False for key in required_false)
        or result.get("conditional_obligation_set", {}).get("status") != "NO_UNIQUE_MINIMUM_ARCHITECTURE_SELECTED"
    ):
        raise GateError("STATUS_CONTRACT", str(adjudication))
    return result


def validate_ledgers(repo: Path) -> dict[str, object]:
    status_rows = tsv_rows(repo / PACKAGE / "STATUS_LEDGER.tsv")
    premise_rows = tsv_rows(repo / PACKAGE / "PREMISE_LEDGER.tsv")
    statuses = {row["id"]: row["status"] for row in status_rows}
    expected = {
        "S01": "DERIVED_CONDITIONAL", "S02": "NO", "S03": "DERIVED_CONDITIONAL",
        "S04": "DERIVED_CONDITIONAL", "S05": "DERIVED_CONDITIONAL", "S06": "DERIVED_CONDITIONAL",
        "S07": "NO", "S08": "DERIVED_COUNTERMODELS", "S09": "NO", "S10": "NO",
        "S11": "NOT_DERIVED", "S12": "DERIVED_CONDITIONAL", "S13": "OPEN", "S14": "NO",
        "S15": "REQUIRED_IF_LITERAL", "S16": "DERIVED_CONDITIONAL", "S17": "NO",
        "S18": "DERIVED_CONDITIONAL", "S19": "OPEN", "S20": "CONDITIONAL_OWNER_HYPOTHESIS",
        "S21": "CONDITIONAL_OWNER_HYPOTHESIS", "S22": "NO", "S23": "YES_CONDITIONAL",
        "S24": "NOT_AUTHORIZED", "S25": "NO", "S26": "OPEN", "S27": "OPEN",
        "S28": "CONDITIONAL_OBLIGATION_SET", "S29": "NO", "S30": OUTCOME,
    }
    if len(status_rows) != 30 or statuses != expected or len(premise_rows) != 17:
        raise GateError("LEDGER_CONTRACT", f"{len(status_rows)}:{len(premise_rows)}")
    return {"result": "PASS", "status_rows": len(status_rows), "premise_rows": len(premise_rows)}


def validate_report(repo: Path) -> dict[str, object]:
    report = (repo / PACKAGE / "DERIVATION_REPORT.md").read_text(encoding="utf-8")
    decision = (repo / PACKAGE / "LAY_DECISION_TREE.md").read_text(encoding="utf-8")
    review_a = (repo / PACKAGE / "REVIEW_MASS_COSMOLOGY.md").read_text(encoding="utf-8")
    review_b = (repo / PACKAGE / "REVIEW_SCALE_CAUSALITY.md").read_text(encoding="utf-8")
    audit = (repo / PACKAGE / "ADVERSARIAL_AUDIT.md").read_text(encoding="utf-8")
    required = [
        OUTCOME,
        "different operational readings of one dilation field",
        "c_0\\frac{N}{B}",
        "same clock factor",
        "c_{\\rm eff}=c_0N^2",
        "(1+z)^{-2}",
        "(1+z)^2",
        "do not derive a local mass increase",
        "g_{\\mu\\nu}(x;\\sigma)",
        "scale Reciprocity",
        "coordinate-slope ceiling",
        "No unique smallest architecture has been selected",
        "Observable superluminal signalling remains unauthorized",
    ]
    missing = [token for token in required if token not in report]
    if (
        missing
        or "PASS" not in review_a
        or "PASS" not in review_b
        or "No files were changed" not in audit
        or "same dilation field" not in decision
    ):
        raise GateError("REPORT_CONTRACT", missing[0] if missing else "supporting record")
    return {"result": "PASS", "report_tokens": len(required), "reviews": 2}


def validate_cpu(repo: Path) -> dict[str, object]:
    imports: set[str] = set()
    for name in ("derive_reciprocal_clock_optical_scale.py", "verify_reciprocal_clock_optical_scale.py"):
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
        "ruler_omission_rejected": catch("RULER_OMITTED", lambda: exact_algebra(omit_ruler=True)),
        "coordinate_speed_scalar_rejected": catch("COORDINATE_SCALAR", lambda: validate_claims({**claims, "coordinate_speed_scalar": True})),
        "local_c_variation_rejected": catch("LOCAL_C_PROMOTION", lambda: validate_claims({**claims, "local_c_varies": True})),
        "common_scale_speed_change_rejected": catch("COMMON_SCALE", lambda: exact_algebra(common_changes=True)),
        "reciprocal_square_loss_rejected": catch("RECIPROCAL_SQUARE", lambda: exact_algebra(miss_square=True)),
        "redshift_speed_numerical_identity_rejected": catch("NUMERICAL_IDENTITY", lambda: validate_claims({**claims, "redshift_speed_numerically_identical": True})),
        "boxed_square_CSN_theorem_rejected": catch("REPRESENTATIVE_PROMOTION", lambda: validate_claims({**claims, "boxed_square_is_CSN_physical_theorem": True})),
        "NB_one_invariance_rejected": catch("REPRESENTATIVE_PROMOTION", lambda: validate_claims({**claims, "NB_one_is_invariant": True})),
        "local_mass_increase_rejected": catch("MASS_PROMOTION", lambda: exact_algebra(mass_increases=True)),
        "Killing_energy_native_mass_rejected": catch("KILLING_MASS_PROMOTION", lambda: validate_claims({**claims, "killing_energy_is_native_mass": True})),
        "native_mass_constancy_promotion_rejected": catch("MASS_CONSTANCY_PROMOTION", lambda: validate_claims({**claims, "native_mass_constancy_derived": True})),
        "photon_material_coupling_promotion_rejected": catch("PHOTON_COUPLING_PROMOTION", lambda: validate_claims({**claims, "photon_coupling_derived": True})),
        "position_scale_type_confusion_rejected": catch("TYPE_CONFUSION", lambda: validate_claims({**claims, "r_equals_ell": True})),
        "single_metric_many_scale_cones_rejected": catch("SCALE_ARCHITECTURE", lambda: validate_claims({**claims, "single_local_metric_has_many_scale_cones": True})),
        "pivot_selection_rejected": catch("PIVOT_PROMOTION", lambda: validate_claims({**claims, "pivot_selected": True})),
        "plateau_as_full_GR_proof_rejected": catch("GR_PROMOTION", lambda: validate_claims({**claims, "plateau_proves_GR": True})),
        "broad_plateau_promotion_rejected": catch("PLATEAU_PROMOTION", lambda: validate_claims({**claims, "broad_plateau_derived": True})),
        "unique_architecture_promotion_rejected": catch("ARCHITECTURE_PROMOTION", lambda: validate_claims({**claims, "unique_minimum_architecture_selected": True})),
        "observer_line_gap_closure_rejected": catch("LINE_PROMOTION", lambda: validate_claims({**claims, "observer_line_gap_closed": True})),
        "UV_profile_promotion_rejected": catch("SCALE_PROFILE_PROMOTION", lambda: validate_claims({**claims, "UV_speedup_foundationally_selected": True})),
        "IR_profile_promotion_rejected": catch("SCALE_PROFILE_PROMOTION", lambda: validate_claims({**claims, "IR_profile_foundationally_selected": True})),
        "superluminal_signalling_rejected": catch("SIGNALLING_PROMOTION", lambda: validate_claims({**claims, "superluminal_signalling_authorized": True})),
        "coordinate_ceiling_as_invariant_signal_bound_rejected": catch("SIGNAL_BOUND_PROMOTION", lambda: validate_claims({**claims, "coordinate_ceiling_is_invariant_signal_bound": True})),
        "c0_speed_floor_confusion_rejected": catch("SPEED_FLOOR", lambda: exact_algebra(floor_confusion=True)),
        "static_cosmology_promotion_rejected": catch("COSMOLOGY_PROMOTION", lambda: validate_claims({**claims, "static_promoted_cosmology": True})),
        "boundary_identity_promotion_rejected": catch("BOUNDARY_PROMOTION", lambda: validate_claims({**claims, "CMB_wall_seal_substrate_identified": True})),
        "dynamics_promotion_rejected": catch("DYNAMICS_PROMOTION", lambda: validate_claims({**claims, "action_source_carrier_selected": True})),
        "status_corruption_rejected": catch("STATUS_CONTRACT", lambda: validate_result(repo, corrupt=True)),
        "source_mutation_rejected": catch("SOURCE_HASH", lambda: validate_sources(repo, corrupt=True)),
        "scope_escape_rejected": catch("SCOPE", lambda: validate_scope(repo, "LIVE.md")),
        "frozen_package_mutation_rejected": catch("FROZEN_PACKAGE", lambda: validate_frozen(repo, corrupt=True)),
        "dirty_metadata_drift_rejected": catch("DIRTY_METADATA", lambda: validate_dirty(repo, args.dirty_checkout.resolve(), corrupt=True)),
    }
    verification = {
        "result": "PASS",
        "mode": "INDEPENDENT_CPU_ONLY_RECIPROCAL_CLOCK_OPTICAL_SCALE_SELECTOR",
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
        "grok_integration_authorized": False,
    }
    payload = json.dumps(verification, indent=2, sort_keys=True) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
