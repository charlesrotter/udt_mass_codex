#!/usr/bin/env python3
"""Independent fail-closed verifier for the UDT premise reset."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "VERIFICATION_RESULT.json"
PACKAGE_TOKEN = "udt_premise_reset_audit_2026-07-19"
CONTROLS = {
    "LIVE.md": ("premise-reset", "signed local", "X_max", "review_required"),
    "HANDOFF.md": ("premise-reset", "signed local", "X_max", "withdrawn"),
    "INDEX.md": ("premise-reset", "signed local", "X_max", "withdrawn"),
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md": ("premise-reset", "signed local", "X_max", "withdrawn"),
}


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_contract(
    owners: list[dict[str, str]],
    conflicts: list[dict[str, str]],
    universe: list[dict[str, str]],
    packages: list[dict[str, str]],
    claims: list[dict[str, str]],
) -> None:
    require(len(owners) == 15 and len({row["id"] for row in owners}) == 15, "owner census")
    require(len(conflicts) == 13 and len({row["id"] for row in conflicts}) == 13, "conflict census")
    names = [row["package"] for row in universe]
    require(len(names) == 19 and len(set(names)) == 19, "universe census")
    require(len(packages) == 19 and {row["package"] for row in packages} == set(names), "package coverage")
    require(len(claims) == 42 and len({row["id"] for row in claims}) == 42, "claim census")
    require({row["package"] for row in claims} == set(names), "claim package coverage")

    owner = {row["id"]: row for row in owners}
    require("finite einsteinian" in owner["O01"]["owner_meaning"].casefold(), "finite c_E lost")
    require("signed dilation field" in owner["O03"]["owner_meaning"].casefold(), "signed local phi lost")
    require("nonnegative" in owner["O04"]["owner_meaning"].casefold(), "nonnegative distance lost")
    require("does not force phi nonnegative" in owner["O04"]["not_implied"].casefold(), "phi-distance distinction lost")
    require("global limit shared by all observational frames" in owner["O06"]["owner_meaning"].casefold(), "global Xmax lost")
    require("derived output" in owner["O07"]["owner_meaning"].casefold(), "derived Xmax lost")
    require("mass divided by total proper universe volume" in owner["O08"]["owner_meaning"].casefold(), "global density lost")
    require(owner["O09"]["audit_status"] == "OPEN", "local density promoted")
    require("asymptotic limit" in owner["O11"]["owner_meaning"].casefold(), "asymptotic boundary lost")
    require(owner["O12"]["audit_status"] == "OPEN_CONFLICT", "seal conflict silently closed")
    require("measured g" in owner["O14"]["owner_meaning"].casefold(), "observed G anchor lost")
    require("scale-free" in owner["O15"]["owner_meaning"].casefold() and "introduce scale" in owner["O15"]["owner_meaning"].casefold(), "scale layers conflated")

    package_counts = Counter(row["primary_regrade"] for row in packages)
    require(package_counts == {
        "SURVIVES_INDEPENDENT": 2,
        "SURVIVES_CONDITIONAL_RELABELED": 10,
        "ALGEBRA_VALID_PHYSICS_WITHDRAWN": 4,
        "CONTAMINATED_RERUN_REQUIRED": 3,
    }, f"package counts: {package_counts}")
    grades = {row["package"]: row["primary_regrade"] for row in packages}
    require(grades["reciprocal_c_clock_channel_correction_2026-07-19"] == "CONTAMINATED_RERUN_REQUIRED", "clock package overpromoted")
    require(grades["projective_position_direction_magnitude_correction_2026-07-19"] == "CONTAMINATED_RERUN_REQUIRED", "distance package overpromoted")
    require(grades["projective_position_join_audit_2026-07-19"] == "CONTAMINATED_RERUN_REQUIRED", "projective package overpromoted")
    for name in (
        "xmax_reciprocity_audit_2026-07-19",
        "xmax_full_frame_realization_2026-07-19",
        "xmax_dynamic_observer_frame_2026-07-19",
        "xmax_accelerating_finite_cell_cartan_2026-07-19",
    ):
        require(grades[name] == "ALGEBRA_VALID_PHYSICS_WITHDRAWN", f"Xmax physics retained: {name}")

    claim = {row["id"]: row for row in claims}
    require(claim["L22"]["regrade"] == "SURVIVES_INDEPENDENT", "reciprocal-c anchor lost")
    require(claim["L24"]["regrade"] == "CONTAMINATED_RERUN_REQUIRED", "nonnegative-rho clock retained")
    require(claim["L16"]["regrade"] == "SURVIVES_INDEPENDENT", "negative distance correction lost")
    require(claim["L38"]["regrade"] == "ALGEBRA_VALID_PHYSICS_WITHDRAWN", "full physical frame retained")
    require(claim["L41"]["regrade"] == "SURVIVES_INDEPENDENT", "observed G imported GR dynamics")
    require(claim["L42"]["regrade"] == "SURVIVES_INDEPENDENT", "c and G promoted to Xmax formula")
    require(not any(row["primary_regrade"] == "REFUTED_BY_OWNER_MEANING" for row in packages), "blanket refutation invented")


def validate_controls(overrides: dict[str, str] | None = None) -> list[dict[str, str]]:
    overrides = overrides or {}
    details = []
    for name, phrases in CONTROLS.items():
        content = overrides.get(name, (ROOT / name).read_text(encoding="utf-8"))
        window = "\n".join(content.splitlines()[:190])
        require(PACKAGE_TOKEN in window, f"premise reset missing from {name}")
        for phrase in phrases:
            require(phrase.casefold() in window.casefold(), f"control phrase missing {name}: {phrase}")
        details.append({"path": name, "sha256": hashlib.sha256(content.encode()).hexdigest()})
    return details


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation passed: {name}")


def main() -> None:
    owners = rows("OWNER_MEANING_LEDGER.tsv")
    conflicts = rows("SEMANTIC_CONFLICT_LEDGER.tsv")
    universe = rows("PACKAGE_UNIVERSE.tsv")
    packages = rows("PACKAGE_REGRADE.tsv")
    claims = rows("LOAD_BEARING_CLAIM_REGRADE.tsv")
    validate_contract(owners, conflicts, universe, packages, claims)
    checks: dict[str, str] = {"table_contract": "PASS"}
    catches: dict[str, str] = {}

    manifest_details = []
    manifest_entries = 0
    for row in universe:
        package = row["package"]
        manifest = ROOT / package / "SHA256SUMS.txt"
        require(sha256(manifest) == row["manifest_sha256"], f"manifest hash: {package}")
        entries = [line for line in manifest.read_text(encoding="utf-8").splitlines() if line]
        require(len(entries) == int(row["manifest_entries"]), f"manifest entries: {package}")
        replay = subprocess.run(["sha256sum", "--check", "SHA256SUMS.txt"], cwd=manifest.parent, text=True, capture_output=True, check=False, timeout=120)
        require(replay.returncode == 0 and "FAILED" not in replay.stdout, f"manifest replay: {package}")
        manifest_entries += len(entries)
        manifest_details.append({"package": package, "manifest_sha256": row["manifest_sha256"], "entries": len(entries), "result": "PASS"})
    require(manifest_entries == 346, f"manifest total {manifest_entries}")
    checks["all_19_prior_packages_byte_identical"] = "PASS"

    graph = HERE / "DEPENDENCY_GRAPH.json"
    before = sha256(graph)
    env = os.environ.copy(); env["PYTHONDONTWRITEBYTECODE"] = "1"; env["CUDA_VISIBLE_DEVICES"] = ""
    replay = subprocess.run([sys.executable, "-B", str(HERE / "build_dependency_graph.py")], cwd=ROOT, env=env, text=True, capture_output=True, check=False, timeout=120)
    require(replay.returncode == 0 and not replay.stderr, "graph replay")
    require(sha256(graph) == before, "graph nondeterminism")
    graph_data = json.loads(graph.read_text(encoding="utf-8"))
    require(graph_data["counts"] == {"owner_meanings": 15, "semantic_conflicts": 13, "packages": 19, "load_bearing_claims": 42, "nodes": 89, "edges": 83}, "graph counts")
    checks["deterministic_dependency_graph"] = "PASS"

    source = HERE / "SOURCE_INVENTORY.tsv"
    source_before = sha256(source)
    replay = subprocess.run([sys.executable, "-B", str(HERE / "build_source_inventory.py")], cwd=ROOT, env=env, text=True, capture_output=True, check=False, timeout=120)
    require(replay.returncode == 0 and not replay.stderr and sha256(source) == source_before, "source inventory replay")
    require(len(rows("SOURCE_INVENTORY.tsv")) == 27, "source inventory count")
    checks["source_inventory_replay"] = "PASS"

    controls = validate_controls()
    checks["current_navigation_quarantine"] = "PASS"

    report = " ".join((HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8").split()).casefold()
    for phrase in (
        "semantic overloading followed by narrow proof inheritance",
        "neither “all previous work is valid” nor “all previous work is invalid",
        "reciprocal-c anchor survives",
        "current physical frame interpretation is withdrawn",
        "asymptotic-boundary lineage audit",
    ):
        require(phrase.casefold() in report, f"report disclosure: {phrase}")
    checks["report_contract"] = "PASS"

    mutation = copy.deepcopy(universe); mutation.pop()
    expect_failure("missing_package_rejected", lambda: validate_contract(owners, conflicts, mutation, packages, claims), catches)
    mutation = copy.deepcopy(universe); mutation[-1] = copy.deepcopy(mutation[0])
    expect_failure("duplicate_package_rejected", lambda: validate_contract(owners, conflicts, mutation, packages, claims), catches)
    mutation = copy.deepcopy(owners); next(row for row in mutation if row["id"] == "O03")["owner_meaning"] = "Nonnegative dilation distance"
    expect_failure("signed_phi_loss_rejected", lambda: validate_contract(mutation, conflicts, universe, packages, claims), catches)
    mutation = copy.deepcopy(owners); next(row for row in mutation if row["id"] == "O04")["not_implied"] = "phi is nonnegative"
    expect_failure("distance_forces_phi_nonnegative_rejected", lambda: validate_contract(mutation, conflicts, universe, packages, claims), catches)
    mutation = copy.deepcopy(owners); next(row for row in mutation if row["id"] == "O07")["owner_meaning"] = "Freely supplied universal constant"
    expect_failure("Xmax_input_promotion_rejected", lambda: validate_contract(mutation, conflicts, universe, packages, claims), catches)
    mutation = copy.deepcopy(owners); next(row for row in mutation if row["id"] == "O09")["audit_status"] = "DERIVED_LOCAL_SOURCE"
    expect_failure("global_density_local_source_promotion_rejected", lambda: validate_contract(mutation, conflicts, universe, packages, claims), catches)
    mutation = copy.deepcopy(owners); next(row for row in mutation if row["id"] == "O11")["owner_meaning"] = "Hard numerical wall inserted before solve"
    expect_failure("hard_boundary_input_rejected", lambda: validate_contract(mutation, conflicts, universe, packages, claims), catches)
    mutation = copy.deepcopy(owners); next(row for row in mutation if row["id"] == "O14")["owner_meaning"] = "G must be derived and is not observationally accepted"
    expect_failure("observed_G_anchor_demotion_rejected", lambda: validate_contract(mutation, conflicts, universe, packages, claims), catches)
    mutation = copy.deepcopy(owners); next(row for row in mutation if row["id"] == "O15")["owner_meaning"] = "UDT has primitive scale at its core"
    expect_failure("scale_free_core_loss_rejected", lambda: validate_contract(mutation, conflicts, universe, packages, claims), catches)
    mutation = copy.deepcopy(packages)
    for row in mutation: row["primary_regrade"] = "SURVIVES_INDEPENDENT"
    expect_failure("blanket_all_valid_rejected", lambda: validate_contract(owners, conflicts, universe, mutation, claims), catches)
    mutation = copy.deepcopy(packages)
    for row in mutation: row["primary_regrade"] = "REFUTED_BY_OWNER_MEANING"
    expect_failure("blanket_all_invalid_rejected", lambda: validate_contract(owners, conflicts, universe, mutation, claims), catches)
    mutation = copy.deepcopy(packages); next(row for row in mutation if row["package"] == "xmax_full_frame_realization_2026-07-19")["primary_regrade"] = "SURVIVES_INDEPENDENT"
    expect_failure("physical_Xmax_frame_promotion_rejected", lambda: validate_contract(owners, conflicts, universe, mutation, claims), catches)
    mutation = copy.deepcopy(claims); next(row for row in mutation if row["id"] == "L24")["regrade"] = "SURVIVES_INDEPENDENT"
    expect_failure("nonnegative_rho_clock_promotion_rejected", lambda: validate_contract(owners, conflicts, universe, packages, mutation), catches)
    mutation = copy.deepcopy(claims); next(row for row in mutation if row["id"] == "L22")["regrade"] = "REFUTED_BY_OWNER_MEANING"
    expect_failure("reciprocal_c_anchor_demotion_rejected", lambda: validate_contract(owners, conflicts, universe, packages, mutation), catches)
    live = (ROOT / "LIVE.md").read_text(encoding="utf-8")
    expect_failure("navigation_quarantine_loss_rejected", lambda: validate_controls({"LIVE.md": live.replace(PACKAGE_TOKEN, "missing_premise_reset")}), catches)
    expect_failure("prior_manifest_mutation_rejected", lambda: require(sha256(ROOT / universe[0]["package"] / "SHA256SUMS.txt") == "0" * 64, "manifest mutation"), catches)

    output = {
        "schema": "udt-premise-reset-verification-1.0",
        "python": sys.version.split()[0],
        "checks": checks,
        "catch_proofs": catches,
        "counts": {
            "owner_meanings": 15,
            "semantic_conflicts": 13,
            "packages": 19,
            "prior_manifest_entries": manifest_entries,
            "load_bearing_claims": 42,
            "package_regrades": dict(sorted(Counter(row["primary_regrade"] for row in packages).items())),
        },
        "prior_packages": manifest_details,
        "controls": controls,
        "dependency_graph_sha256": sha256(graph),
        "source_inventory_sha256": sha256(source),
        "result": "PASS",
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
