#!/usr/bin/env python3
"""Fail-closed integrity and semantic verifier for the Cartan ensemble atlas."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "c5e343a"
PREREG_FILES = (
    "CHANNEL_UNIVERSE.tsv",
    "COMPLETION_UNIVERSE.tsv",
    "DENSITY_FUTURE_PROTOCOL.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "OUTPUT_UNIVERSE.tsv",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "SOURCE_SCOPE.tsv",
    "build_source_manifest.py",
)
GENERATED = (
    "COFRAME_INTEGRABILITY.tsv",
    "COMPLETION_APPLICABILITY.tsv",
    "CONNECTION_COEFFICIENTS.tsv",
    "CURVATURE_COMPONENTS.tsv",
    "CURVATURE_CONTRACTIONS.tsv",
    "IDENTITY_DYNAMICS_LEDGER.tsv",
    "NONLINEAR_CHANNEL_GRAPH.tsv",
    "RESULT.json",
    "STRUCTURE_EQUATIONS.tsv",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_state() -> dict[str, object]:
    return {
        "channels": rows("CHANNEL_UNIVERSE.tsv"),
        "outputs": rows("OUTPUT_UNIVERSE.tsv"),
        "completion_universe": rows("COMPLETION_UNIVERSE.tsv"),
        "completions": rows("COMPLETION_APPLICABILITY.tsv"),
        "connection": rows("CONNECTION_COEFFICIENTS.tsv"),
        "curvature": rows("CURVATURE_COMPONENTS.tsv"),
        "graph": rows("NONLINEAR_CHANNEL_GRAPH.tsv"),
        "identity": rows("IDENTITY_DYNAMICS_LEDGER.tsv"),
        "density": rows("DENSITY_FUTURE_PROTOCOL.tsv"),
        "result": json.loads((HERE / "RESULT.json").read_text(encoding="utf-8")),
    }


def validate(state: dict[str, object]) -> set[str]:
    errors: set[str] = set()
    channels = state["channels"]
    outputs = state["outputs"]
    completion_universe = state["completion_universe"]
    completions = state["completions"]
    connection = state["connection"]
    curvature = state["curvature"]
    graph = state["graph"]
    identity = state["identity"]
    density = state["density"]
    result = state["result"]

    expected_symbols = ["u0", "u1", "s0", "s1", "a0", "a1", "h0", "h1", "f2", "f3"]
    if [row["symbol"] for row in channels] != expected_symbols:
        errors.add("CHANNEL_UNIVERSE")
    if [row["output_id"] for row in outputs] != [f"O{i:02d}" for i in range(1, 12)]:
        errors.add("OUTPUT_UNIVERSE")
    if [row["class_id"] for row in completion_universe] != [f"FC{i:02d}" for i in range(1, 13)]:
        errors.add("COMPLETION_UNIVERSE")
    completion_ids = [row["class_id"] for row in completions]
    if completion_ids != [f"FC{i:02d}" for i in range(1, 13)] or len(set(completion_ids)) != 12:
        errors.add("COMPLETION_COVERAGE")
    fc11 = [row for row in completions if row["class_id"] == "FC11"]
    if len(fc11) != 1 or fc11[0]["local_cartan_status"].startswith("EXACT"):
        errors.add("FC11_SCOPE")
    if any(row["selection_status"] != "REGISTERED_NOT_SELECTED" for row in completions):
        errors.add("COMPLETION_SELECTION")

    connection_keys = [(row["lower_pair"], row["basis_leg"]) for row in connection]
    if len(connection_keys) != 24 or len(set(connection_keys)) != 24:
        errors.add("CONNECTION_COVERAGE")
    curvature_keys = [(row["lower_pair"], row["two_form_leg"]) for row in curvature]
    if len(curvature_keys) != 36 or len(set(curvature_keys)) != 36:
        errors.add("CURVATURE_COVERAGE")

    quadratic = {
        tuple(sorted((row["family_left"], row["family_right"])))
        for row in graph if row["coupling_kind"] == "QUADRATIC"
    }
    forbidden_phi_f = {
        tuple(sorted(("PHI_ANHOLONOMY", "CONNECTION_CURVATURE_1"))),
        tuple(sorted(("PHI_ANHOLONOMY", "CONNECTION_CURVATURE_2"))),
    }
    if quadratic.intersection(forbidden_phi_f):
        errors.add("PHI_F_EDGE")
    if len(graph) != 25 or len(quadratic) != 19:
        errors.add("GRAPH_COVERAGE")
    families = {row["family"] for row in channels}
    adjacency = {family: set() for family in families}
    for left, right in quadratic:
        if left not in adjacency or right not in adjacency:
            errors.add("GRAPH_UNKNOWN_FAMILY")
            continue
        adjacency[left].add(right)
        adjacency[right].add(left)
    if adjacency:
        seen: set[str] = set()
        pending = [next(iter(adjacency))]
        while pending:
            node = pending.pop()
            if node in seen:
                continue
            seen.add(node)
            pending.extend(adjacency[node] - seen)
        if seen != families:
            errors.add("GRAPH_DISCONNECTED")

    identity_map = {row["object"]: row for row in identity}
    if identity_map.get("global_local_response_one_form", {}).get("status") != "OPEN_NOT_DERIVED":
        errors.add("RESPONSE_PROMOTION")
    if identity_map.get("first_and_second_Bianchi", {}).get("does_not_supply") != "dynamics_or_selector":
        errors.add("BIANCHI_PROMOTION")
    if any("UDT_DERIVED" in row["status"] for row in density):
        errors.add("DENSITY_PROMOTION")
    if result.get("interpretation", {}).get("physical_response_one_form") != "NOT_SUPPLIED_BY_IDENTITIES":
        errors.add("RESPONSE_PROMOTION")
    if result.get("interpretation", {}).get("density_sweep") != "DEFERRED":
        errors.add("DENSITY_PROMOTION")
    if result.get("status") != "PASS" or set(result.get("checks", {}).values()) != {"PASS"}:
        errors.add("RESULT_CHECK")
    counts = result.get("counts", {})
    if (
        counts.get("connection_pair_labeled_slots") != 24
        or counts.get("nonzero_connection_slots") != 18
        or counts.get("curvature_pair_labeled_slots") != 36
        or counts.get("nonzero_curvature_coefficients") != 36
        or counts.get("generic_four_dimensional_Riemann_algebraic_slots") != 20
    ):
        errors.add("SLOT_SEMANTICS")
    correction = (HERE / "PREREGISTRATION_CORRECTION.md")
    if not correction.is_file() or "pair-labeled curvature two-form slots" not in correction.read_text(encoding="utf-8"):
        errors.add("SLOT_SEMANTICS")
    return errors


def source_manifest_errors() -> set[str]:
    errors: set[str] = set()
    manifest = rows("SOURCE_MANIFEST.tsv")
    if len(manifest) != 10 or len({row["source_id"] for row in manifest}) != 10:
        errors.add("SOURCE_MANIFEST")
    for row in manifest:
        path = ROOT / row["path"]
        if not path.is_file() or str(path.stat().st_size) != row["size_bytes"] or sha256(path) != row["sha256"]:
            errors.add("SOURCE_MANIFEST")
    return errors


def prereg_errors() -> set[str]:
    errors: set[str] = set()
    for name in PREREG_FILES:
        path = f"{HERE.name}/{name}"
        committed = subprocess.run(
            ["git", "show", f"{PREREG_COMMIT}:{path}"], cwd=ROOT, check=True, capture_output=True
        ).stdout
        if committed != (HERE / name).read_bytes():
            errors.add("PREREG_MUTATED")
    return errors


def run_catches(state: dict[str, object]) -> list[dict[str, str]]:
    catches: list[tuple[str, str, callable]] = []

    def expect(code: str, mutate: callable) -> callable:
        def check() -> bool:
            trial = copy.deepcopy(state)
            mutate(trial)
            return code in validate(trial)
        return check

    catches.extend([
        ("C01", "missing_registered_channel", expect("CHANNEL_UNIVERSE", lambda s: s["channels"].pop())),
        ("C02", "duplicate_registered_channel", expect("CHANNEL_UNIVERSE", lambda s: s["channels"].append(copy.deepcopy(s["channels"][0])))),
        ("C03", "missing_registered_output", expect("OUTPUT_UNIVERSE", lambda s: s["outputs"].pop())),
        ("C04", "missing_completion", expect("COMPLETION_COVERAGE", lambda s: s["completions"].pop())),
        ("C05", "duplicate_completion", expect("COMPLETION_COVERAGE", lambda s: s["completions"].append(copy.deepcopy(s["completions"][0])))),
        ("C06", "FC11_global_toric_overclaim", expect("FC11_SCOPE", lambda s: s["completions"][10].update(local_cartan_status="EXACT_GLOBAL_TORIC"))),
        ("C07", "fabricated_direct_phi_f_edge", expect("PHI_F_EDGE", lambda s: s["graph"].append({"coupling_kind":"QUADRATIC","family_left":"PHI_ANHOLONOMY","family_right":"CONNECTION_CURVATURE_1","term_count":"1","component_count":"1","components":"fake"}))),
        ("C08", "response_one_form_promotion", expect("RESPONSE_PROMOTION", lambda s: next(row for row in s["identity"] if row["object"] == "global_local_response_one_form").update(status="DERIVED"))),
        ("C09", "Bianchi_dynamics_promotion", expect("BIANCHI_PROMOTION", lambda s: next(row for row in s["identity"] if row["object"] == "first_and_second_Bianchi").update(does_not_supply="none"))),
        ("C10", "Lambda_CDM_promoted_to_UDT", expect("DENSITY_PROMOTION", lambda s: s["density"][0].update(status="UDT_DERIVED"))),
        ("C11", "result_check_failure", expect("RESULT_CHECK", lambda s: s["result"]["checks"].update(torsion_zero_exact="FAIL"))),
        ("C12", "slot_count_called_independence", expect("SLOT_SEMANTICS", lambda s: s["result"]["counts"].update(generic_four_dimensional_Riemann_algebraic_slots=36))),
    ])
    out = []
    for catch_id, mutation, check in catches:
        passed = bool(check())
        if not passed:
            raise AssertionError((catch_id, mutation))
        out.append({"catch_id": catch_id, "mutation": mutation, "result": "REJECTED_AS_REQUIRED"})
    return out


def main() -> None:
    if sys.version_info < (3, 10):
        raise SystemExit("Python >=3.10 required")
    import sympy
    if sympy.__version__ != "1.13.1":
        raise SystemExit(f"wrong SymPy version: {sympy.__version__}")

    before = {name: sha256(HERE / name) for name in GENERATED}
    pinned_site = os.environ.get("UDT_PINNED_SITE")
    if pinned_site:
        bootstrap = (
            "import runpy,sys;"
            f"sys.path.insert(0,{pinned_site!r});"
            f"runpy.run_path({str(HERE / 'derive_cartan_ensemble.py')!r},run_name='__main__')"
        )
        production_command = [sys.executable, "-I", "-S", "-c", bootstrap]
    else:
        production_command = [sys.executable, str(HERE / "derive_cartan_ensemble.py")]
    production = subprocess.run(
        production_command,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    (HERE / "PRODUCTION_STDOUT.txt").write_text(production.stdout, encoding="utf-8")
    (HERE / "PRODUCTION_STDERR.txt").write_text(production.stderr, encoding="utf-8")
    if production.returncode != 0:
        raise SystemExit(production.returncode)
    after = {name: sha256(HERE / name) for name in GENERATED}
    if before != after:
        raise AssertionError(("nondeterministic generated outputs", before, after))

    state = load_state()
    errors = validate(state) | source_manifest_errors() | prereg_errors()
    if errors:
        raise AssertionError(sorted(errors))
    catches = run_catches(state)
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["catch_id", "mutation", "result"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)

    result = {
        "status": "PASS",
        "python": sys.version.split()[0],
        "sympy": sympy.__version__,
        "deterministic_generated_files": len(GENERATED),
        "semantic_and_integrity_errors": [],
        "catch_proofs_passed": len(catches),
        "preregistration_commit": PREREG_COMMIT,
        "preregistration_files_unchanged": len(PREREG_FILES),
        "source_manifest_rows_verified": 10,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
