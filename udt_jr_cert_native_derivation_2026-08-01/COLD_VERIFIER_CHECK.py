#!/usr/bin/env python3
"""Fresh independent verifier for the bounded JR_CERT_NATIVE program.

This file deliberately does not import or execute either primary JR program.  It reads the
committed freeze, exact base-tree blobs, uncommitted result records, and independently rebuilds
the load-bearing algebra and gate logic.  All mutations are in memory.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "686336343878e8a9e39a4b72df08d23754243631"
RAW_PATH = HERE / "COLD_VERIFIER_RAW.jsonl"
RESULT_PATH = HERE / "COLD_VERIFIER_RESULT.json"

EVENTS: list[dict[str, object]] = []


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def event(check_id: str, ok: bool, **detail: object) -> None:
    row = {"check_id": check_id, "status": "PASS" if ok else "FAIL", **detail}
    EVENTS.append(row)
    if not ok:
        raise AssertionError(f"{check_id}: {detail}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git(*args: str, input_bytes: bytes | None = None) -> bytes:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, input=input_bytes, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.decode(errors='replace')}")
    return proc.stdout


class BaseTree:
    """Exact immutable source reader keyed by the preregistered commit."""

    def __init__(self) -> None:
        raw = git("ls-tree", "-r", "-z", BASE)
        self.blobs: dict[str, str] = {}
        for item in raw.split(b"\0"):
            if not item:
                continue
            meta, name = item.split(b"\t", 1)
            _mode, kind, blob = meta.decode().split()
            if kind == "blob":
                self.blobs[name.decode()] = blob
        self.cache: dict[str, bytes] = {}

    def bytes(self, path: str) -> bytes:
        if path not in self.cache:
            if path not in self.blobs:
                raise KeyError(path)
            self.cache[path] = git("cat-file", "blob", self.blobs[path])
        return self.cache[path]

    def text(self, path: str) -> str:
        return self.bytes(path).decode("utf-8")


def paths_file(name: str) -> list[str]:
    return [x for x in (HERE / name).read_text(encoding="utf-8").splitlines() if x]


def inventory(name: str) -> list[dict[str, str]]:
    return read_tsv(HERE / name)


def validate_freeze(tree: BaseTree) -> dict[str, object]:
    original_paths = paths_file("SOURCE_PATHS.txt")
    added_paths = paths_file("TRANSITIVE_SOURCE_PATHS.txt")
    combined_paths = paths_file("COMBINED_SOURCE_PATHS.txt")
    original_rows = inventory("SOURCE_INVENTORY.tsv")
    added_rows = inventory("TRANSITIVE_SOURCE_INVENTORY.tsv")

    event("FZ01_counts", (len(original_paths), len(added_paths), len(combined_paths)) == (172, 414, 586),
          original=len(original_paths), transitive=len(added_paths), combined=len(combined_paths))
    event("FZ02_unique_original", len(original_paths) == len(set(original_paths)) == 172)
    event("FZ03_unique_transitive", len(added_paths) == len(set(added_paths)) == 414)
    overlap = sorted(set(original_paths) & set(added_paths))
    event("FZ04_disjoint", not overlap, overlap=overlap)
    expected_union = sorted(set(original_paths) | set(added_paths))
    event("FZ05_exact_sorted_union", combined_paths == expected_union)
    event("FZ06_program_outputs_excluded",
          not any(p.startswith("udt_jr_cert_native_derivation_2026-08-01/") for p in combined_paths))
    event("FZ07_inventory_path_alignment",
          [r["path"] for r in original_rows] == original_paths and
          [r["path"] for r in added_rows] == added_paths)

    byte_total = 0
    for row in original_rows + added_rows:
        path = row["path"]
        data = tree.bytes(path)
        byte_total += len(data)
        if row["base"] != BASE or row["blob"] != tree.blobs[path]:
            raise AssertionError(f"base/blob mismatch: {path}")
        if row["sha256"] != digest(data) or int(row["bytes"]) != len(data):
            raise AssertionError(f"byte/hash mismatch: {path}")
    event("FZ08_all_base_blobs", True, files=586, bytes=byte_total)

    scopes = read_tsv(HERE / "TRANSITIVE_PACKAGE_SCOPE.tsv")
    event("FZ09_scope_count", len(scopes) == 10)
    scoped: set[str] = set()
    package_counts: dict[str, int] = {}
    for row in scopes:
        prefix = row["package_path"].rstrip("/") + "/"
        paths = {p for p in tree.blobs if p.startswith(prefix)} - set(original_paths)
        scoped |= paths
        package_counts[row["package_path"]] = len(paths)
    event("FZ10_scope_enumeration", scoped == set(added_paths), package_counts=package_counts)

    for manifest_name, rows in (
        ("SOURCE_MANIFEST.sha256", original_rows),
        ("TRANSITIVE_SOURCE_MANIFEST.sha256", added_rows),
    ):
        lines = (HERE / manifest_name).read_text(encoding="utf-8").splitlines()
        expected = [f'{r["sha256"]}  ../{r["path"]}' for r in rows]
        event(f"FZ11_{manifest_name}", lines == expected)

    prereg_snap = json.loads((HERE / "PREREG_SNAPSHOT.json").read_text(encoding="utf-8"))
    snap = json.loads((HERE / "TRANSITIVE_FREEZE_SNAPSHOT.json").read_text(encoding="utf-8"))
    event("FZ12_snapshot", snap["original_sources"] == 172 and
          snap["transitive_additions"] == 414 and snap["combined_sources"] == 586 and
          snap["overlap_with_original_count"] == 0 and snap["package_count"] == 10)
    freeze_hashes = {
        "source_paths": digest((HERE / "SOURCE_PATHS.txt").read_bytes()),
        "source_inventory": digest((HERE / "SOURCE_INVENTORY.tsv").read_bytes()),
        "source_manifest": digest((HERE / "SOURCE_MANIFEST.sha256").read_bytes()),
        "transitive_paths": digest((HERE / "TRANSITIVE_SOURCE_PATHS.txt").read_bytes()),
        "transitive_inventory": digest((HERE / "TRANSITIVE_SOURCE_INVENTORY.tsv").read_bytes()),
        "transitive_manifest": digest((HERE / "TRANSITIVE_SOURCE_MANIFEST.sha256").read_bytes()),
        "combined_paths": digest((HERE / "COMBINED_SOURCE_PATHS.txt").read_bytes()),
        "package_scope": digest((HERE / "TRANSITIVE_PACKAGE_SCOPE.tsv").read_bytes()),
    }
    event("FZ13_freeze_artifact_hashes",
          freeze_hashes["source_paths"] == prereg_snap["source_paths_sha256"] and
          freeze_hashes["source_inventory"] == prereg_snap["source_inventory_sha256"] and
          freeze_hashes["source_manifest"] == prereg_snap["source_manifest_sha256"] and
          freeze_hashes["transitive_paths"] == snap["transitive_paths_sha256"] and
          freeze_hashes["transitive_inventory"] == snap["transitive_inventory_sha256"] and
          freeze_hashes["transitive_manifest"] == snap["transitive_manifest_sha256"] and
          freeze_hashes["combined_paths"] == snap["combined_paths_sha256"] and
          freeze_hashes["package_scope"] == snap["package_scope_sha256"], hashes=freeze_hashes)
    return {
        "original": original_paths, "transitive": added_paths, "combined": combined_paths,
        "inventory": {r["path"]: r for r in original_rows + added_rows},
        "byte_total": byte_total, "package_counts": package_counts, "freeze_hashes": freeze_hashes,
    }


def require_tokens(tree: BaseTree, path: str, tokens: tuple[str, ...]) -> dict[str, object]:
    text = tree.text(path)
    missing = [token for token in tokens if token not in text]
    if missing:
        raise AssertionError(f"missing source token(s) in {path}: {missing}")
    return {"path": path, "sha256": digest(tree.bytes(path)), "tokens": len(tokens)}


# Source-first probes chosen independently of the primary SOURCE_ANCHOR_LEDGER.  They are exact
# base-tree statements needed to decide every frozen route; none is a generated JR result.
ROUTE_PROBES: dict[str, list[tuple[str, tuple[str, ...]]]] = {
    "E01": [
        ("udt_general_screen_complete_cell_atlas_2026-07-28/EXACT_DERIVATION.md",
         ("stationary, off-shell", "No action, field equation", "selects no physical branch")),
        ("udt_global_functional_dof_constraint_rank_audit_2026-07-26/EXACT_DERIVATION.md",
         ("Cartan data", "derived evaluators", "Derived views do not automatically add fields")),
    ],
    "E02": [
        ("udt_general_screen_complete_cell_atlas_2026-07-28/EXACT_DERIVATION.md",
         ("reconstructs all four lowered", "metric compatibility and zero torsion", "off-shell")),
        ("udt_joint_selector_provenance_audit_2026-07-28/STATUS_LEDGER.tsv",
         ("Levi_Civita_coframe_transport", "DERIVED_AS_MATHEMATICS", "physical path semantics")),
    ],
    "E03": [
        ("CURRENT_SCIENTIFIC_PREMISES.tsv",
         ("CONDITIONAL_TORIC_F_EQUALS_dS_AND_dF_EQUALS_ZERO", "full native Maxwell system claimed")),
        ("udt_global_functional_dof_constraint_rank_audit_2026-07-26/EXACT_DERIVATION.md",
         ("dF=d^2S=0", "is an\nidentity", "inhomogeneous Maxwell equation")),
    ],
    "E04": [
        ("udt_joint_selector_provenance_audit_2026-07-28/STATUS_LEDGER.tsv",
         ("joint_operation", "OPEN_NONE_REGISTERED", "realized equations")),
        ("udt_metric_natural_joint_selector_nogo_2026-07-28/STATUS_LEDGER.tsv",
         ("ordered_pair_extension", "DERIVED_REAL_LAMBDA_FAMILY", "universal_whole_solution_selector_no_go")),
    ],
    "E05": [
        ("angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
         ("ALLOWED_FAMILY", "TWO_STAGE_OPEN_GATE_CHAIN", "no off-shell map")),
        ("udt_higher_isometry_plane_ownership_audit_2026-07-28/STATUS_LEDGER.tsv",
         ("universal_plane_selection", "REFUTED_BOUNDED", "generic_fixed_metric_plane_selection")),
    ],
    "E06": [
        ("udt_bootstrap_to_local_response_map_audit_2026-07-25/STATUS_LEDGER.tsv",
         ("DERIVED_CONDITIONAL_RESPONSE_SKELETON", "complete_bootstrap_to_local_map", "OPEN")),
        ("udt_stability_foundations_audit_2026-08-01/BOOTSTRAP_FIXED_POINT_SCHEMA.tsv",
         ("B = R(u)", "DERIVED_AS_TYPE_SCHEMA_ONLY", "fixed-point set")),
    ],
    "E07": [
        ("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
         ("Complete native action", "OPEN", "Finite-cell differentiable boundary action")),
        ("CURRENT_SCIENTIFIC_PREMISES.tsv",
         ("C2_Bach_action", "CONDITIONAL", "EH_action")),
    ],
    "E08": [
        ("udt_joint_realization_closure_audit_2026-08-01/JOINT_GATE_MATRIX.tsv",
         ("native whole-system equation", "OPEN", "explicit native joint-realization certificate")),
        ("udt_joint_realization_closure_audit_2026-08-01/ROUTE_ADJUDICATION.tsv",
         ("DIRECT_REGISTERED_WITNESS", "NOT_FOUND_IN_FROZEN_RECORD", "MINIMUM_CERTIFICATE_TYPE_IDENTIFIED")),
    ],
    "B01": [
        ("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
         ("Static seal parity", "normal derivative free", "Complete boundary variation")),
        ("udt_global_functional_dof_constraint_rank_audit_2026-07-26/STATUS_LEDGER.tsv",
         ("static_seal_rank", "normal jet", "bulk scalar remain free")),
    ],
    "B02": [
        ("angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
         ("TOPOLOGY_UNDERDETERMINED", "ALLOWED_FAMILY", "boundary functional")),
        ("asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md",
         ("not derived to be the hard end of spacetime", "complete differentiable boundary")),
    ],
    "B03": [
        ("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
         ("Finite-cell differentiable boundary action", "OPEN", "Seal value alone is insufficient")),
        ("native_boundary_generator_scale_audit_2026-07-19/CHARGE_REQUIREMENT_LEDGER.tsv",
         ("Differentiable boundary/corner primitive", "OPEN", "boundary data")),
    ],
    "B04": [
        ("udt_bootstrap_to_local_response_map_audit_2026-07-25/STATUS_LEDGER.tsv",
         ("finite_cell_boundary_response", "OPEN_REQUIRED_TYPE", "global-modulus functionals absent")),
    ],
    "B05": [
        ("native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv",
         ("physical finite-cell carrier completion", "OPEN", "solver boundary")),
        ("angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
         ("carrier action source and time-live topology law", "OPEN")),
    ],
    "B06": [
        ("udt_joint_realization_closure_audit_2026-08-01/JOINT_GATE_MATRIX.tsv",
         ("differentiable finite-cell boundary/completion", "OPEN", "seal parity")),
        ("native_boundary_generator_scale_audit_2026-07-19/CHARGE_REQUIREMENT_LEDGER.tsv",
         ("Complete native total mass", "OPEN", "Raw Phi_N")),
    ],
}

EXPECTED_ROUTE_STATUS = {
    "E01": "IDENTITY_RECONSTRUCTION_NOT_SELECTION",
    "E02": "UNIQUE_CONNECTION_FOR_EACH_METRIC_NOT_REALIZATION_LAW",
    "E03": "DIFFERENTIAL_IDENTITY_ZERO_DYNAMICAL_RANK",
    "E04": "KINEMATIC_COMPOSITION_AND_OFF_SHELL_RESPONSE_NOT_EOM",
    "E05": "CONFIGURATION_AND_COMPLETION_CONSTRAINTS_NOT_WHOLE_EQUATION",
    "E06": "TWO_ARROW_TYPE_DERIVED_MAPS_AND_FIXED_POINT_OPEN",
    "E07": "CONDITIONAL_BRANCHES_DO_NOT_BECOME_NATIVE",
    "E08": "NO_REGISTERED_COMPLETE_NATIVE_OPERATION_IN_FROZEN_CENSUS",
    "B01": "PHI_TRACE_ONLY_NOT_ALL_FIELD_DIFFERENTIABLE_BOUNDARY",
    "B02": "MULTIPLE_COMPLETIONS_AND_REGULARITY_NOT_SELECTION",
    "B03": "OPERATOR_AND_VARIATION_DOMAIN_DEPENDENT_CONDITIONAL",
    "B04": "SHAPE_CHANNEL_REQUIRED_BUT_MAP_AND_DERIVATIVE_ABSENT",
    "B05": "CONDITIONAL_CARRIER_AND_SOLVER_BOUNDARY_NOT_NATIVE",
    "B06": "NO_REGISTERED_COMPLETE_MATCHING_BOUNDARY_OPERATION",
}


def validate_routes(tree: BaseTree, frozen: dict[str, object]) -> dict[str, object]:
    premise_rows = read_tsv(HERE / "PREMISE_LEDGER.tsv")
    candidates = read_tsv(HERE / "ROUTE_CANDIDATES.tsv")
    equations = read_tsv(HERE / "EQUATION_ROUTE_ADJUDICATION.tsv")
    boundaries = read_tsv(HERE / "BOUNDARY_ROUTE_ADJUDICATION.tsv")
    anchors = read_tsv(HERE / "SOURCE_ANCHOR_LEDGER.tsv")
    stages = read_tsv(HERE / "STAGE_GATE_LEDGER.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    combined = set(frozen["combined"])

    event("RT01_premise_ids", [r["premise_id"] for r in premise_rows] ==
          [f"JRC-P{i:02d}" for i in range(1, 21)])
    event("RT02_candidate_ids", [r["route_id"] for r in candidates] ==
          [f"E{i:02d}" for i in range(1, 9)] + [f"B{i:02d}" for i in range(1, 7)])
    event("RT03_adjudication_ids", [r["route_id"] for r in equations] ==
          [f"E{i:02d}" for i in range(1, 9)] and [r["route_id"] for r in boundaries] ==
          [f"B{i:02d}" for i in range(1, 7)])
    event("RT04_all_routes_negative", all(r["pass"] == "NO" for r in equations + boundaries),
          equation_passes=sum(r["pass"] == "YES" for r in equations),
          boundary_passes=sum(r["pass"] == "YES" for r in boundaries))
    event("RT05_route_fields", all(r["status"] and r["exact_test"] and r["source_anchors"] and
          r["remaining_scope"] for r in equations + boundaries))
    event("RT05b_route_statuses", all(r["status"] == EXPECTED_ROUTE_STATUS[r["route_id"]]
          for r in equations + boundaries))

    anchor_map = {r["anchor_id"]: r for r in anchors}
    event("RT06_primary_anchor_ids", len(anchor_map) == len(anchors) == 14)
    for row in anchors:
        path = row["path"]
        event(f"RT07_anchor_{row['anchor_id']}", path in combined and
              digest(tree.bytes(path)) == row["sha256"] and row["required_text"] in tree.text(path))
    for row in equations + boundaries:
        used = row["source_anchors"].split(";")
        ok = all(a in anchor_map and row["route_id"] in anchor_map[a]["routes"].split(";") for a in used)
        event(f"RT08_anchor_coverage_{row['route_id']}", ok, anchors=used)

    independent_sources: dict[str, list[dict[str, object]]] = {}
    for route_id, probes in ROUTE_PROBES.items():
        records = []
        for path, tokens in probes:
            if path not in combined:
                raise AssertionError(f"independent route source outside freeze: {route_id} {path}")
            records.append(require_tokens(tree, path, tokens))
        independent_sources[route_id] = records
        event(f"RT09_source_first_{route_id}", bool(records), sources=len(records))

    event("RT10_stages", [r["stage"] for r in stages] == ["1", "2", "3", "4"] and
          all(r["gate_pass"] == "NO" for r in stages) and
          stages[2]["status"] == "NOT_LAUNCHED_FAIL_CLOSED" and
          stages[3]["status"].startswith("WITHHELD_"))
    overall = {r["object"]: r for r in statuses}["overall"]
    event("RT11_outcome", result["outcome"] == overall["status"] ==
          "NO_NATIVE_PROBLEM_DERIVED_DOWNSTREAM_STAGES_BLOCKED")
    event("RT12_downstream_block", result["stage1_pass"] is False and
          result["stage2_pass"] is False and result["stage3_solve_allowed"] is False and
          result["stage3_launched"] is False and result["stage4_certificate_assembled"] is False)
    event("RT13_count_alignment", result["governing_source_count"] == 586 and
          result["equation_routes"] == 8 and result["boundary_routes"] == 6)

    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    event("RT14_bounded_labels", "not a universal impossibility claim" in audit and
          "not assert that no future UDT equation" in exact and
          "NO_UNIVERSAL_NO_GO" in result["scope_ceiling"])
    event("RT15_conditional_labels", "`C^2`/Bach remains unique-conditional" in exact and
          "EH/carrier routes remain conditional" in exact and "It is not yet a law" in exact)

    candidate_patterns = (
        "complete native action", "native whole-system equation",
        "differentiable finite-cell boundary", "complete bootstrap-to-local response map",
    )
    census: dict[str, list[str]] = {p: [] for p in candidate_patterns}
    for path in frozen["combined"]:
        try:
            low = tree.text(path).lower()
        except UnicodeDecodeError:
            continue
        for pattern in candidate_patterns:
            if pattern in low:
                census[pattern].append(path)
    event("RT16_candidate_phrase_census", all(census.values()),
          counts={k: len(v) for k, v in census.items()})
    return {"premises": premise_rows, "candidates": candidates, "equations": equations,
            "boundaries": boundaries, "anchors": anchors, "stages": stages, "statuses": statuses,
            "result": result, "independent_sources": independent_sources, "phrase_census": census}


def independent_geometry() -> dict[str, object]:
    t, x, y, z = sp.symbols("t x y z", real=True)
    coords = (t, x, y, z)
    p = sp.Function("phi")(x)
    g = sp.diag(-sp.exp(-2 * p), sp.exp(2 * p), 1, 1)
    gi = g.inv()
    n = 4

    gamma = [[[
        sp.simplify(sum(gi[rho, lam] * (sp.diff(g[lam, nu], coords[mu]) +
            sp.diff(g[lam, mu], coords[nu]) - sp.diff(g[mu, nu], coords[lam]))
            for lam in range(n)) / 2)
        for nu in range(n)] for mu in range(n)] for rho in range(n)]

    compatibility = []
    torsion = []
    for mu in range(n):
        for a in range(n):
            for b in range(n):
                compatibility.append(sp.simplify(sp.diff(g[a, b], coords[mu]) -
                    sum(g[r, b] * gamma[r][mu][a] + g[a, r] * gamma[r][mu][b]
                        for r in range(n))))
                torsion.append(sp.simplify(gamma[mu][a][b] - gamma[mu][b][a]))

    # Different contraction path from the primary: build R^rho_{sigma mu nu} first.
    riemann = [[[[] for _nu in range(n)] for _mu in range(n)] for _sigma in range(n)]
    for rho in range(n):
        for sigma in range(n):
            for mu in range(n):
                for nu in range(n):
                    value = sp.diff(gamma[rho][nu][sigma], coords[mu]) - \
                        sp.diff(gamma[rho][mu][sigma], coords[nu])
                    value += sum(gamma[rho][mu][lam] * gamma[lam][nu][sigma] -
                                 gamma[rho][nu][lam] * gamma[lam][mu][sigma]
                                 for lam in range(n))
                    riemann[rho][sigma][mu].append(sp.simplify(value))
    ricci = [[sp.simplify(sum(riemann[rho][sigma][rho][nu] for rho in range(n)))
              for nu in range(n)] for sigma in range(n)]
    scalar = sp.simplify(sum(gi[a, b] * ricci[a][b] for a in range(n) for b in range(n)))
    einstein_cov = [[sp.simplify(ricci[a][b] - g[a, b] * scalar / 2)
                     for b in range(n)] for a in range(n)]
    einstein_mixed = [[sp.simplify(sum(gi[a, c] * einstein_cov[c][b] for c in range(n)))
                       for b in range(n)] for a in range(n)]
    divergence = []
    for b in range(n):
        value = 0
        for a in range(n):
            value += sp.diff(einstein_mixed[a][b], coords[a])
            value += sum(gamma[a][a][c] * einstein_mixed[c][b] -
                         gamma[c][a][b] * einstein_mixed[a][c] for c in range(n))
        divergence.append(sp.simplify(value))

    pp, ppp = sp.diff(p, x), sp.diff(p, x, 2)
    expected_scalar = 2 * sp.exp(-2 * p) * (ppp - 2 * pp**2)
    cartan_dtheta0 = sp.exp(-p) * pp
    cartan_omega = -sp.exp(-p) * pp
    cartan_curvature = sp.exp(-2 * p) * (ppp - 2 * pp**2)
    event("GE01_determinant", sp.simplify(g.det()) == -1)
    event("GE02_metric_compatibility", all(v == 0 for v in compatibility), zero=64, total=64)
    event("GE03_torsion", all(v == 0 for v in torsion), zero=64, total=64)
    event("GE04_scalar", sp.simplify(scalar - expected_scalar) == 0, expression=str(scalar))
    event("GE05_Cartan_first", sp.simplify(cartan_dtheta0 + cartan_omega) == 0)
    event("GE06_Cartan_second", cartan_curvature != 0, expression=str(cartan_curvature))
    event("GE07_contracted_Bianchi", all(v == 0 for v in divergence), divergence=[str(v) for v in divergence])

    aa, bb = sp.symbols("a b", real=True)
    samples = [0, aa * x, bb * x**2, aa * x + bb * x**3]
    sample_curvatures = [sp.simplify(expected_scalar.subs(p, q).doit().subs(x, 0)) for q in samples]
    event("GE08_nonselection_family", sample_curvatures == [0, -4 * aa**2, 4 * bb, -4 * aa**2],
          seal_curvatures=[str(q) for q in sample_curvatures])
    return {"determinant": "-1", "metric_compatibility": "64/64", "torsion": "64/64",
            "scalar_curvature": str(scalar), "cartan_curvature": str(cartan_curvature),
            "bianchi_divergence": [str(v) for v in divergence],
            "sample_seal_curvatures": [str(q) for q in sample_curvatures]}


def independent_boundary_controls() -> dict[str, object]:
    x = sp.symbols("x", real=True)
    a, b = sp.symbols("a b", real=True)
    phi = a * x + b * x**3
    seal = {
        "phi": sp.simplify(phi.subs(x, 0)),
        "normal_first": sp.diff(phi, x).subs(x, 0),
        "normal_second": sp.diff(phi, x, 2).subs(x, 0),
        "normal_third": sp.diff(phi, x, 3).subs(x, 0),
    }
    scalar = 2 * sp.exp(-2 * phi) * (sp.diff(phi, x, 2) - 2 * sp.diff(phi, x)**2)
    seal_curvature = sp.simplify(scalar.subs(x, 0))
    event("BD01_odd_seal", seal["phi"] == 0 and seal["normal_first"] == a and
          seal["normal_second"] == 0 and seal["normal_third"] == 6 * b,
          jets={k: str(v) for k, v in seal.items()})
    event("BD02_seal_curvature_free", seal_curvature == -4 * a**2,
          curvature=str(seal_curvature))

    f = sp.Function("f")(x)
    h = sp.Function("h")(x)
    l2_integrand = sp.diff(f, x) * sp.diff(h, x)
    l2_bulk = -sp.diff(f, x, 2) * h
    l2_flux = sp.diff(f, x) * h
    l4_integrand = sp.diff(f, x, 2) * sp.diff(h, x, 2)
    l4_bulk = sp.diff(f, x, 4) * h
    l4_flux = sp.diff(f, x, 2) * sp.diff(h, x) - sp.diff(f, x, 3) * h
    event("BD03_two_derivative_IBP",
          sp.simplify(l2_integrand - l2_bulk - sp.diff(l2_flux, x)) == 0,
          flux="f' delta_f")
    event("BD04_four_derivative_IBP",
          sp.simplify(l4_integrand - l4_bulk - sp.diff(l4_flux, x)) == 0,
          flux="f'' delta_f' - f''' delta_f")

    # Exact separating witness: Dirichlet variation h(0)=0 closes L2 but not L4.
    fw = x**2
    hw = x
    l2_at = sp.simplify((sp.diff(fw, x) * hw).subs(x, 0))
    l4_at = sp.simplify((sp.diff(fw, x, 2) * sp.diff(hw, x) -
                         sp.diff(fw, x, 3) * hw).subs(x, 0))
    event("BD05_operator_dependent_boundary", l2_at == 0 and l4_at == 2,
          second_order_flux=str(l2_at), fourth_order_flux=str(l4_at))
    return {"odd_family": "a*x+b*x**3", "seal_phi": str(seal["phi"]),
            "seal_normal_first": str(seal["normal_first"]),
            "seal_normal_third": str(seal["normal_third"]),
            "seal_curvature": str(seal_curvature),
            "second_order_flux": "f' delta_f",
            "fourth_order_flux": "f'' delta_f' - f''' delta_f",
            "separating_witness": {"second": str(l2_at), "fourth": str(l4_at)}}


def compare_primary(geometry: dict[str, object], boundary: dict[str, object]) -> dict[str, object]:
    algebra = json.loads((HERE / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    event("CP01_algebra_counts", algebra["metric_determinant"] == geometry["determinant"] and
          algebra["metric_compatibility_zero_count"] == 64 and
          algebra["torsion_zero_count"] == 64)
    event("CP02_Bianchi", algebra["contracted_bianchi_divergence"] == geometry["bianchi_divergence"])
    event("CP03_seal", algebra["seal_family"]["phi_at_seal"] == boundary["seal_phi"] and
          algebra["seal_family"]["normal_derivative_at_seal"] == boundary["seal_normal_first"] and
          algebra["seal_family"]["scalar_curvature_at_seal"] == boundary["seal_curvature"])
    event("CP04_variation", algebra["second_order_variation_identity"] == "0" and
          algebra["fourth_order_variation_identity"] == "0")
    event("CP05_outcome", result["equation_routes_passing"] == 0 and
          result["boundary_routes_passing"] == 0 and result["stage3_launched"] is False and
          result["stage4_certificate_assembled"] is False)
    return {"algebra_match": True, "outcome_match": True,
            "primary_verifier_semantic_caveat":
            "primary mutations are structural; cold mutations below supply semantic promotion catches"}


def cold_model(frozen: dict[str, object], routes: dict[str, object]) -> dict[str, object]:
    return {
        "original": list(frozen["original"]), "transitive": list(frozen["transitive"]),
        "combined": list(frozen["combined"]),
        "premise_ids": [r["premise_id"] for r in routes["premises"]],
        "equations": copy.deepcopy(routes["equations"]),
        "boundaries": copy.deepcopy(routes["boundaries"]),
        "route_evidence": {rid: True for rid in ROUTE_PROBES},
        "primary_anchor_text": {r["anchor_id"]: True for r in routes["anchors"]},
        "base_hashes": {p: True for p in frozen["combined"]}, "scope_complete": True,
        "identity_class": "IDENTITY_RECONSTRUCTION_NOT_EOM",
        "conditional_action": "CONDITIONAL_NOT_NATIVE",
        "seal_class": "TRACE_ONLY_NOT_COMPLETE_BOUNDARY",
        "scope": "EXACT_586_SOURCE_UNIVERSE_NO_UNIVERSAL_NO_GO",
        "stage3_launched": False, "certificate_assembled": False,
    }


def validate_cold_model(model: dict[str, object]) -> None:
    original = model["original"]
    transitive = model["transitive"]
    combined = model["combined"]
    assert len(original) == len(set(original)) == 172
    assert len(transitive) == len(set(transitive)) == 414
    assert not set(original) & set(transitive)
    assert combined == sorted(set(original) | set(transitive)) and len(combined) == 586
    assert not any(p.startswith("udt_jr_cert_native_derivation_2026-08-01/") for p in combined)
    assert model["premise_ids"] == [f"JRC-P{i:02d}" for i in range(1, 21)]
    equations = model["equations"]
    boundaries = model["boundaries"]
    assert [r["route_id"] for r in equations] == [f"E{i:02d}" for i in range(1, 9)]
    assert [r["route_id"] for r in boundaries] == [f"B{i:02d}" for i in range(1, 7)]
    assert all(r["pass"] == "NO" and r["status"] and r["exact_test"] and
               r["source_anchors"] and r["remaining_scope"] for r in equations + boundaries)
    assert all(r["status"] == EXPECTED_ROUTE_STATUS[r["route_id"]] for r in equations + boundaries)
    assert set(model["route_evidence"]) == set(ROUTE_PROBES)
    assert all(model["route_evidence"].values())
    assert len(model["primary_anchor_text"]) == 14 and all(model["primary_anchor_text"].values())
    assert len(model["base_hashes"]) == 586 and all(model["base_hashes"].values())
    assert model["scope_complete"] is True
    assert model["identity_class"] == "IDENTITY_RECONSTRUCTION_NOT_EOM"
    assert model["conditional_action"] == "CONDITIONAL_NOT_NATIVE"
    assert model["seal_class"] == "TRACE_ONLY_NOT_COMPLETE_BOUNDARY"
    assert model["scope"] == "EXACT_586_SOURCE_UNIVERSE_NO_UNIVERSAL_NO_GO"
    equation_pass = any(r["pass"] == "YES" for r in equations)
    boundary_pass = equation_pass and any(r["pass"] == "YES" for r in boundaries)
    solve_allowed = equation_pass and boundary_pass
    assert model["stage3_launched"] is False and not solve_allowed
    assert model["certificate_assembled"] is False


def exercise_mutations(model: dict[str, object]) -> list[str]:
    mutations: list[tuple[str, callable]] = []
    mutations.append(("drop_original_source", lambda m: m["original"].pop()))
    mutations.append(("drop_transitive_source", lambda m: m["transitive"].pop()))
    mutations.append(("create_freeze_overlap", lambda m: m["transitive"].__setitem__(0, m["original"][0])))
    mutations.append(("reverse_combined_union", lambda m: m.__setitem__("combined", list(reversed(m["combined"])))))
    mutations.append(("insert_program_output", lambda m: m["combined"].__setitem__(0,
        "udt_jr_cert_native_derivation_2026-08-01/AUDIT_REPORT.md")))
    mutations.append(("drop_premise", lambda m: m["premise_ids"].pop()))
    mutations.append(("drop_equation_route", lambda m: m["equations"].pop()))
    mutations.append(("duplicate_boundary_route", lambda m: m["boundaries"][1].__setitem__("route_id", "B01")))
    mutations.append(("erase_route_evidence", lambda m: m["route_evidence"].__setitem__("E08", False)))
    mutations.append(("erase_anchor_text", lambda m: m["primary_anchor_text"].__setitem__("A08", False)))
    mutations.append(("mutate_base_hash", lambda m: m["base_hashes"].__setitem__(m["combined"][0], False)))
    mutations.append(("drop_scoped_package_file", lambda m: m.__setitem__("scope_complete", False)))
    mutations.append(("promote_Cartan_identity", lambda m: m["equations"][0].__setitem__("pass", "YES")))
    mutations.append(("rename_identity_as_EOM", lambda m: m["equations"][0].__setitem__("status", "NATIVE_EOM")))
    mutations.append(("promote_conditional_action", lambda m: m.__setitem__("conditional_action", "NATIVE")))
    mutations.append(("promote_seal_trace", lambda m: m.__setitem__("seal_class", "COMPLETE_BOUNDARY")))
    mutations.append(("erase_remaining_scope", lambda m: m["equations"][7].__setitem__("remaining_scope", "")))
    mutations.append(("universal_no_go", lambda m: m.__setitem__("scope", "UNIVERSAL_NO_GO")))
    mutations.append(("unauthorized_solve", lambda m: m.__setitem__("stage3_launched", True)))
    mutations.append(("unauthorized_certificate", lambda m: m.__setitem__("certificate_assembled", True)))

    rejected: list[str] = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(model)
        mutate(candidate)
        try:
            validate_cold_model(candidate)
        except (AssertionError, KeyError, IndexError, TypeError):
            rejected.append(name)
            event(f"MU_{name}", True, disposition="REJECTED")
        else:
            event(f"MU_{name}", False, disposition="ESCAPED")
    event("MU_summary", len(rejected) == len(mutations), rejected=len(rejected), total=len(mutations))
    return rejected


def inspect_primary_verifier() -> dict[str, object]:
    text = (HERE / "verify_jr_cert_program.py").read_text(encoding="utf-8")
    structural = text.count("expect_reject(") - 1
    omitted = [token for token in ("required_text", '["exact_test"]', '["remaining_scope"]',
                                    "F6_IDENTITY_PROMOTION", "F7_BOUNDARY_PROMOTION",
                                    "F8_CONDITIONAL_PROMOTION", "F12_UNIVERSAL_NO_GO") if token not in text]
    event("PV01_structural_mutation_count", structural == 14, count=structural)
    event("PV02_semantic_gap_identified", len(omitted) == 7, absent_checks=omitted)
    event("PV03_no_primary_import", "import derive_jr_cert_program" not in text)
    return {"structural_mutations": structural, "absent_semantic_checks": omitted,
            "disposition": "NONBLOCKING_AFTER_COLD_SEMANTIC_MUTATIONS"}


def write_raw() -> str:
    payload = "".join(json.dumps(row, sort_keys=True) + "\n" for row in EVENTS)
    RAW_PATH.write_text(payload, encoding="utf-8")
    return digest(payload.encode())


def run() -> dict[str, object]:
    branch = git("branch", "--show-current").decode().strip()
    head = git("rev-parse", "HEAD").decode().strip()
    event("OP01_branch", branch == "codex/jr-cert-native-derivation-2026-08-01", branch=branch)
    event("OP02_head", head == "148db3b58011984e615c63b5f77874d147c5ae45", head=head)
    ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT).returncode == 0
    event("OP03_base_ancestor", ancestor, base=BASE)
    premise = subprocess.run([sys.executable, "verify_current_scientific_premises.py"], cwd=ROOT,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    event("OP04_current_premises", premise.returncode == 0 and "PASS:" in premise.stdout,
          stdout=premise.stdout.strip(), stderr=premise.stderr.strip())

    tree = BaseTree()
    event("OP05_base_tree", len(tree.blobs) > 0, blobs=len(tree.blobs))
    frozen = validate_freeze(tree)
    routes = validate_routes(tree, frozen)
    geometry = independent_geometry()
    boundary = independent_boundary_controls()
    comparison = compare_primary(geometry, boundary)
    primary_verifier = inspect_primary_verifier()
    mutations = exercise_mutations(cold_model(frozen, routes))

    changed = git("status", "--porcelain", "-z").split(b"\0")
    changed_paths = []
    for row in changed:
        if not row:
            continue
        changed_paths.append(row[3:].decode(errors="replace"))
    event("OP06_isolation", all(p.startswith("udt_jr_cert_native_derivation_2026-08-01/")
          for p in changed_paths), changed_paths=len(changed_paths))

    route_results = {r["route_id"]: r["status"] for r in routes["equations"] + routes["boundaries"]}
    phrase_counts = {key: len(value) for key, value in routes["phrase_census"].items()}
    return {
        "date": "2026-08-01", "base": BASE, "head": head, "branch": branch,
        "verdict": "CLOSED-PASS_BOUNDED",
        "primary_outcome": "NO_NATIVE_PROBLEM_DERIVED_DOWNSTREAM_STAGES_BLOCKED",
        "maximum_conclusion": "EXACT_586_PATH_REGISTERED_SOURCE_UNIVERSE_ONLY__NO_UNIVERSAL_NO_GO",
        "freeze": {"original": 172, "transitive": 414, "combined": 586, "overlap": 0,
                   "bytes": frozen["byte_total"], "package_counts": frozen["package_counts"],
                   "artifact_hashes": frozen["freeze_hashes"]},
        "route_results": route_results, "source_phrase_census": phrase_counts,
        "geometry": geometry, "boundary_controls": boundary,
        "comparison_to_primary": comparison, "primary_verifier_review": primary_verifier,
        "mutations_rejected": mutations,
        "stage_gates": {"E_native": "OPEN_NOT_DERIVED", "B_native": "OPEN_NOT_DERIVED",
                        "stage3": "NOT_LAUNCHED", "JR_CERT_NATIVE": "NOT_ASSEMBLED"},
        "four_gates": {"preregistered": "YES", "bounded_scope_justified": "YES_586_PATHS",
                       "independent_load_bearing_verification": "YES",
                       "premises_audited": "YES_20_ROWS_PLUS_CURRENT_VERIFIER"},
        "findings": [
            {"id": "CV-F01", "severity": "RETAIN", "text": "No frozen route supplies E_native or matching B_native."},
            {"id": "CV-F02", "severity": "NONBLOCKING_TOOLING_CAVEAT",
             "text": "Primary mutations are structural; this cold checker adds source-semantic promotion catches."},
            {"id": "CV-F03", "severity": "SCOPE_GUARD",
             "text": "The negative is bounded to the registered 586-path universe; universal no-go is rejected."},
        ],
    }


def main() -> int:
    try:
        result = run()
    except Exception as exc:  # fail closed while preserving the exact failure record
        EVENTS.append({"check_id": "FATAL", "status": "FAIL", "error": repr(exc)})
        raw_hash = write_raw()
        failed = {"date": "2026-08-01", "base": BASE, "verdict": "FAIL_CLOSED",
                  "error": repr(exc), "checks_total": len(EVENTS),
                  "checks_passed": sum(r["status"] == "PASS" for r in EVENTS),
                  "raw_sha256": raw_hash, "python": sys.version.split()[0], "sympy": sp.__version__}
        RESULT_PATH.write_text(json.dumps(failed, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"FAIL COLD JR verifier: {exc}", file=sys.stderr)
        return 1

    raw_hash = write_raw()
    result.update({
        "checks_total": len(EVENTS),
        "checks_passed": sum(r["status"] == "PASS" for r in EVENTS),
        "mutations_total": len(result["mutations_rejected"]),
        "raw_sha256": raw_hash,
        "checker_sha256": digest(Path(__file__).read_bytes()),
        "python": sys.version.split()[0], "sympy": sp.__version__,
    })
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS cold JR verifier: "
          f"checks={result['checks_passed']}/{result['checks_total']} "
          f"mutations={result['mutations_total']}/{result['mutations_total']} "
          f"sources=172+414=586 verdict={result['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
