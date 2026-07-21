#!/usr/bin/env python3
"""Independent SymPy regressions and fail-closed corruption catches for P01."""

from __future__ import annotations

import ast
import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import sympy as sp

from canonical_geometry_evaluator import (
    DIM,
    ETA,
    SLOT_NAMES,
    GeometryInputError,
    MetricJets,
    constant_internal_frame_transform_coframe,
    constant_linear_coordinate_transform_coframe,
    csn_scaled_metric_jets,
    evaluate_coframe_jets,
    evaluate_metric_jets,
    local_internal_frame_transform_coframe_jets,
    metric_jets_from_split,
    reconstruct_split,
)
from run_p01_evaluator import fixture


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULT = HERE / "DERIVATION_RESULT.json"
VERIFY = HERE / "VERIFICATION_RESULT.json"
TRANSCRIPT = HERE / "VERIFICATION_TRANSCRIPT.txt"
TOLERANCE = 2e-10


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def maximum(value) -> float:
    array = np.asarray(value, dtype=float)
    return float(np.max(np.abs(array))) if array.size else 0.0


def validate(data: dict) -> None:
    require(data["schema"] == "udt-p01-canonical-geometry-evaluator-1.0", "schema")
    require(data["status"] == "PASS", "status")
    require(data["maximum_conclusion"] == "GEOMETRY_EVALUATOR_VERIFIED_NOT_SOLUTION_SPACE_EXPLORED", "maximum")
    require(data["check_count"] == 36 and all(value == "PASS" for value in data["checks"].values()), "checks")
    implementation = data["implementation"]
    require(implementation["slot_names"] == list(SLOT_NAMES), "slot names")
    require(implementation["slot_count"] == 10, "slot count")
    require(len(set(implementation["slot_names"])) == 10, "slot uniqueness")
    require(implementation["coordinate_count"] == 4, "coordinate count")
    require(implementation["value_channels_exercised"] == 10, "value channels")
    require(implementation["first_jet_channels_exercised"] == 40, "first channels")
    require(implementation["symmetric_second_jet_channels_exercised"] == 100, "second channels")
    require(not implementation["scientific_solve_executed"] and not implementation["gpu_used"], "compute scope")
    require(data["maximum_raw_residual"] < TOLERANCE, "raw residual")
    require(max(data["raw_residuals"].values()) < TOLERANCE, "residual census")
    require(data["premise_stamps"]["two_plus_two"] == "CONDITIONAL_BRANCH_SUPPLIED_SPLIT_NOT_SELECTED", "split promoted")
    require(data["premise_stamps"]["dynamics"] == "OPEN_NOT_EVALUATED", "dynamics promoted")
    require(data["csn_weights"] == {"coframe": 1, "metric": 2, "inverse": -2, "determinant": 8, "volume": 4}, "CSN weights")
    fixtures = data["fixtures"]
    require(abs(fixtures["polar_flat"]["gamma_witnesses"]["Gamma^2_12"] - 0.5) < TOLERANCE, "connection sign")
    require(abs(fixtures["polar_flat"]["scalar_curvature"]) < TOLERANCE, "flat curvature")
    require(abs(fixtures["unit_sphere_product"]["scalar_curvature"] - 2.0) < TOLERANCE, "sphere scalar")
    require(abs(fixtures["unit_sphere_product"]["riemann_witness"] - 0.75) < TOLERANCE, "curvature index/sign")
    require(data["checks"]["first_cartan_identity"] == "PASS", "first Cartan")
    require(data["checks"]["second_cartan_identity"] == "PASS", "second Cartan")
    require(data["checks"]["constant_local_lorentz_invariance"] == "PASS", "frame reconstruction")
    require(data["checks"]["coordinate_coframe_roundtrip"] == "PASS", "coordinate reconstruction")
    scope = data["scope"]
    require(scope["local_metric_two_jets_only"], "local scope")
    require(not any(scope[key] for key in (
        "solution_space_explored", "reciprocal_plane_selected", "phi_metric_join_selected",
        "action_or_equation_evaluated", "boundary_or_topology_completed", "physical_evolution_run",
    )), "scope promotion")


def sympy_geometry(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]):
    inverse = sp.simplify(metric.inv())
    gamma = sp.MutableDenseNDimArray.zeros(DIM, DIM, DIM)
    for rho in range(DIM):
        for mu in range(DIM):
            for nu in range(DIM):
                gamma[rho, mu, nu] = sp.simplify(sum(
                    inverse[rho, sigma]
                    * (
                        sp.diff(metric[sigma, nu], coordinates[mu])
                        + sp.diff(metric[sigma, mu], coordinates[nu])
                        - sp.diff(metric[mu, nu], coordinates[sigma])
                    ) / 2
                    for sigma in range(DIM)
                ))
    riemann = sp.MutableDenseNDimArray.zeros(DIM, DIM, DIM, DIM)
    for rho in range(DIM):
        for sigma in range(DIM):
            for mu in range(DIM):
                for nu in range(DIM):
                    riemann[rho, sigma, mu, nu] = sp.simplify(
                        sp.diff(gamma[rho, nu, sigma], coordinates[mu])
                        - sp.diff(gamma[rho, mu, sigma], coordinates[nu])
                        + sum(
                            gamma[rho, mu, lam] * gamma[lam, nu, sigma]
                            - gamma[rho, nu, lam] * gamma[lam, mu, sigma]
                            for lam in range(DIM)
                        )
                    )
    ricci = sp.Matrix(DIM, DIM, lambda sigma, nu: sp.simplify(sum(
        riemann[rho, sigma, rho, nu] for rho in range(DIM)
    )))
    scalar = sp.simplify(sum(inverse[mu, nu] * ricci[mu, nu] for mu in range(DIM) for nu in range(DIM)))
    return inverse, gamma, riemann, ricci, scalar


def point_jets(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...], point: dict) -> MetricJets:
    value = np.array(metric.subs(point), dtype=float)
    first = np.zeros((DIM, DIM, DIM))
    second = np.zeros((DIM, DIM, DIM, DIM))
    for a in range(DIM):
        for mu in range(DIM):
            for nu in range(DIM):
                first[a, mu, nu] = float(sp.diff(metric[mu, nu], coordinates[a]).subs(point))
                for b in range(DIM):
                    second[a, b, mu, nu] = float(
                        sp.diff(metric[mu, nu], coordinates[a], coordinates[b]).subs(point)
                    )
    return MetricJets(value, first, second)


def array_at(array, point: dict) -> np.ndarray:
    shape = array.shape
    output = np.zeros(shape)
    for index in np.ndindex(shape):
        output[index] = float(sp.N(array[index].subs(point), 17))
    return output


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, GeometryInputError, KeyError, ValueError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation unexpectedly passed: {name}")


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}
    before = sha256(RESULT)
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["CUDA_VISIBLE_DEVICES"] = ""
    replay = subprocess.run(
        [sys.executable, "-B", str(HERE / "run_p01_evaluator.py")],
        cwd=ROOT,
        env=environment,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    require(replay.returncode == 0, f"main replay: {replay.stderr}")
    require(not replay.stderr, "main replay stderr")
    require(sha256(RESULT) == before, "main result changed")
    require((HERE / "DERIVATION_TRANSCRIPT.txt").read_text(encoding="utf-8") == replay.stdout, "main transcript")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    validate(data)
    checks["deterministic_main_replay_and_contract"] = "PASS"

    t, r, theta, azimuth = sp.symbols("t r theta azimuth", real=True)
    coordinates = (t, r, theta, azimuth)
    metrics = {
        "cartesian_flat": (sp.diag(-1, 1, 1, 1), {t: 0, r: 0, theta: 0, azimuth: 0}),
        "polar_flat": (sp.diag(-1, 1, r**2, 1), {t: 0, r: 2, theta: 0, azimuth: 0}),
        "unit_sphere_product": (
            sp.diag(-1, 1, 1, sp.sin(theta) ** 2),
            {t: 0, r: 0, theta: sp.pi / 3, azimuth: 0},
        ),
    }
    regression_residuals: dict[str, float] = {}
    for name, (metric, point) in metrics.items():
        inverse, gamma, riemann, ricci, scalar = sympy_geometry(metric, coordinates)
        evaluation = evaluate_metric_jets(point_jets(metric, coordinates, point))
        residual = max(
            maximum(evaluation.inverse - np.array(inverse.subs(point), dtype=float)),
            maximum(evaluation.christoffel - array_at(gamma, point)),
            maximum(evaluation.riemann_up - array_at(riemann, point)),
            maximum(evaluation.ricci - np.array(ricci.subs(point), dtype=float)),
            abs(evaluation.scalar_curvature - float(sp.N(scalar.subs(point), 17))),
        )
        require(residual < TOLERANCE, f"independent SymPy regression {name}")
        regression_residuals[name] = residual
        checks[f"independent_sympy_{name}"] = "PASS"

    rng = np.random.default_rng(20260721)
    frame_value = np.eye(DIM) + 0.12 * rng.normal(size=(DIM, DIM))
    generic_metric = frame_value.T @ ETA @ frame_value
    generic_first = 0.025 * rng.normal(size=(DIM, DIM, DIM))
    generic_first = 0.5 * (generic_first + np.swapaxes(generic_first, 1, 2))
    generic_second = 0.015 * rng.normal(size=(DIM, DIM, DIM, DIM))
    generic_second = 0.5 * (generic_second + np.swapaxes(generic_second, 0, 1))
    generic_second = 0.5 * (generic_second + np.swapaxes(generic_second, 2, 3))
    generic = evaluate_metric_jets(MetricJets(generic_metric, generic_first, generic_second))
    generic_inverse = np.linalg.inv(generic_metric)
    generic_inverse_first = np.array(
        [-generic_inverse @ generic_first[k] @ generic_inverse for k in range(DIM)]
    )
    reference_gamma = np.zeros((DIM, DIM, DIM))
    reference_dgamma = np.zeros((DIM, DIM, DIM, DIM))
    for rho in range(DIM):
        for mu in range(DIM):
            for nu in range(DIM):
                for sigma in range(DIM):
                    hterm = (
                        generic_first[mu, sigma, nu]
                        + generic_first[nu, sigma, mu]
                        - generic_first[sigma, mu, nu]
                    )
                    reference_gamma[rho, mu, nu] += 0.5 * generic_inverse[rho, sigma] * hterm
                    for k in range(DIM):
                        dhterm = (
                            generic_second[k, mu, sigma, nu]
                            + generic_second[k, nu, sigma, mu]
                            - generic_second[k, sigma, mu, nu]
                        )
                        reference_dgamma[k, rho, mu, nu] += 0.5 * (
                            generic_inverse_first[k, rho, sigma] * hterm
                            + generic_inverse[rho, sigma] * dhterm
                        )
    reference_riemann = np.zeros((DIM, DIM, DIM, DIM))
    for rho in range(DIM):
        for sigma in range(DIM):
            for mu in range(DIM):
                for nu in range(DIM):
                    reference_riemann[rho, sigma, mu, nu] = (
                        reference_dgamma[mu, rho, nu, sigma]
                        - reference_dgamma[nu, rho, mu, sigma]
                        + sum(
                            reference_gamma[rho, mu, lam] * reference_gamma[lam, nu, sigma]
                            - reference_gamma[rho, nu, lam] * reference_gamma[lam, mu, sigma]
                            for lam in range(DIM)
                        )
                    )
    reference_ricci = np.einsum("rsrn->sn", reference_riemann)
    reference_scalar = float(np.einsum("sn,sn", generic_inverse, reference_ricci))
    generic_residual = max(
        maximum(generic.christoffel - reference_gamma),
        maximum(generic.christoffel_first - reference_dgamma),
        maximum(generic.riemann_up - reference_riemann),
        maximum(generic.ricci - reference_ricci),
        abs(generic.scalar_curvature - reference_scalar),
    )
    require(generic_residual < TOLERANCE, "generic off-diagonal direct tensor reference")
    regression_residuals["generic_offdiagonal_two_jet"] = generic_residual
    checks["independent_generic_offdiagonal_two_jet"] = "PASS"

    symbols = sp.symbols("h00 h01 h11 q22 q23 q33 a20 a30 a21 a31")
    h00, h01, h11, q22, q23, q33, a20, a30, a21, a31 = symbols
    base = sp.Matrix([[h00, h01], [h01, h11]])
    screen = sp.Matrix([[q22, q23], [q23, q33]])
    shifts = sp.Matrix([[a20, a21], [a30, a31]])
    full = (base + shifts.T * screen * shifts).row_join(shifts.T * screen).col_join(
        (screen * shifts).row_join(screen)
    )
    expected_inverse = base.inv().row_join(-base.inv() * shifts.T).col_join(
        (-shifts * base.inv()).row_join(screen.inv() + shifts * base.inv() * shifts.T)
    )
    require(sp.factor(full.det() - base.det() * screen.det()) == 0, "exact split determinant")
    require(all(value == 0 for value in (full * expected_inverse - sp.eye(DIM)).applyfunc(sp.factor)), "exact split inverse")
    checks["independent_exact_split_determinant"] = "PASS"
    checks["independent_exact_split_inverse"] = "PASS"

    jet_coordinates = sp.symbols("z0:4", real=True)
    rational_values = [sp.Rational(value) for value in (-2, sp.Rational(13, 100), sp.Rational(7, 5), sp.Rational(6, 5), sp.Rational(17, 100), sp.Rational(9, 10), sp.Rational(21, 100), sp.Rational(-3, 25), sp.Rational(4, 25), sp.Rational(2, 25))]
    rational_first = [[sp.Rational(((a + 2) * (slot + 3)) % 13 - 6, 100) for slot in range(10)] for a in range(4)]
    rational_second = [[[sp.Rational(((a + b + 3) * (slot + 2)) % 17 - 8, 200) for slot in range(10)] for b in range(4)] for a in range(4)]
    for a in range(4):
        for b in range(a):
            rational_second[a][b] = rational_second[b][a]
    slot_expressions = []
    for slot in range(10):
        expression = rational_values[slot]
        expression += sum(rational_first[a][slot] * jet_coordinates[a] for a in range(4))
        expression += sp.Rational(1, 2) * sum(
            rational_second[a][b][slot] * jet_coordinates[a] * jet_coordinates[b]
            for a in range(4) for b in range(4)
        )
        slot_expressions.append(expression)
    sh = sp.Matrix([[slot_expressions[0], slot_expressions[1]], [slot_expressions[1], slot_expressions[2]]])
    sq = sp.Matrix([[slot_expressions[3], slot_expressions[4]], [slot_expressions[4], slot_expressions[5]]])
    sa = sp.Matrix([[slot_expressions[6], slot_expressions[8]], [slot_expressions[7], slot_expressions[9]]])
    symbolic_full = (sh + sa.T * sq * sa).row_join(sa.T * sq).col_join((sq * sa).row_join(sq))
    origin = {coordinate: 0 for coordinate in jet_coordinates}
    symbolic_value = np.array(symbolic_full.subs(origin), dtype=float)
    symbolic_first = np.zeros((4, 4, 4))
    symbolic_second = np.zeros((4, 4, 4, 4))
    for a in range(4):
        symbolic_first[a] = np.array(symbolic_full.diff(jet_coordinates[a]).subs(origin), dtype=float)
        for b in range(4):
            symbolic_second[a, b] = np.array(
                symbolic_full.diff(jet_coordinates[a], jet_coordinates[b]).subs(origin), dtype=float
            )
    split_jets = metric_jets_from_split(
        np.array(rational_values, dtype=float),
        np.array(rational_first, dtype=float),
        np.array(rational_second, dtype=float),
    )
    split_jet_residual = max(
        maximum(split_jets.metric - symbolic_value),
        maximum(split_jets.first - symbolic_first),
        maximum(split_jets.second - symbolic_second),
    )
    require(split_jet_residual < TOLERANCE, "exact symbolic split jets")
    regression_residuals["exact_symbolic_split_jets"] = split_jet_residual
    checks["independent_exact_symbolic_split_jets"] = "PASS"

    _, polar_frame, polar_first, polar_second, _ = fixture("polar_flat")
    polar_coframe = evaluate_coframe_jets(polar_frame, polar_first, polar_second)
    require(abs(polar_coframe.spin_connection[2, 1, 2] + 1.0) < TOLERANCE, "polar spin connection")
    require(abs(polar_coframe.spin_connection[2, 2, 1] - 1.0) < TOLERANCE, "polar spin antisymmetry")
    _, sphere_frame, sphere_first, sphere_second, _ = fixture("unit_sphere_product")
    sphere_coframe = evaluate_coframe_jets(sphere_frame, sphere_first, sphere_second)
    require(abs(sphere_coframe.cartan_curvature[2, 3, 2, 3] - np.sqrt(3) / 2) < TOLERANCE, "sphere Cartan curvature")
    checks["independent_known_coframe_connection"] = "PASS"
    checks["independent_known_cartan_curvature"] = "PASS"

    sigma0, sigma1 = sp.symbols("sigma0 sigma1", real=True)
    conformal = sp.exp(2 * (sigma0 * t + sigma1 * r)) * sp.diag(-1, 1, 1, 1)
    _, conformal_gamma, _, _, _ = sympy_geometry(conformal, coordinates)
    point = {t: 0, r: 0, theta: 0, azimuth: 0, sigma0: sp.Rational(1, 10), sigma1: -sp.Rational(1, 25)}
    base_jets = MetricJets(np.diag([-1.0, 1.0, 1.0, 1.0]), np.zeros((4, 4, 4)), np.zeros((4, 4, 4, 4)))
    scaled = csn_scaled_metric_jets(base_jets, 1.0, np.array([0.1, -0.04, 0.0, 0.0]), np.zeros((4, 4)))
    scaled_evaluation = evaluate_metric_jets(scaled)
    csn_residual = maximum(scaled_evaluation.christoffel - array_at(conformal_gamma, point))
    require(csn_residual < TOLERANCE, "independent conformal connection")
    regression_residuals["variable_csn_connection"] = csn_residual
    checks["independent_sympy_variable_csn_connection"] = "PASS"

    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    coverage = read_tsv(HERE / "INTERFACE_COVERAGE.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(len(sources) == 15 and len({row["id"] for row in sources}) == 15, "source ledger")
    require(len({row["path"] for row in sources}) == 15, "source path uniqueness")
    require(all((ROOT / row["path"]).exists() for row in sources), "source path")
    require(all("PRE_JULY" not in row["authority_class"] for row in sources), "pre-July source")
    require(len(coverage) == 15 and len({row["id"] for row in coverage}) == 15, "coverage ledger")
    require(all(row["covered"] == "YES" and row["not_covered"] for row in coverage), "coverage disclosure")
    require(len(statuses) == 16 and len({row["id"] for row in statuses}) == 16, "status ledger")
    status_by_id = {row["id"]: row for row in statuses}
    require(status_by_id["P03"]["status"] == "TOOL_VERIFIED_CONDITIONAL", "split status")
    require(status_by_id["P12"]["status"] == "OPEN_NOT_EVALUATED", "split selection status")
    require(status_by_id["P15"]["status"] == "NOT_EXPLORED", "solution-space status")
    require(status_by_id["P16"]["status"] == "NOT_AUTHORIZED", "P02 authority")
    checks["source_status_and_coverage_ledgers"] = "PASS"

    api = json.loads((HERE / "API_SCHEMA.json").read_text(encoding="utf-8"))
    require(api["conditional_two_plus_two_slots"] == list(SLOT_NAMES), "API slots")
    require(api["dimension"] == 4 and len(api["out_of_scope"]) == 5, "API scope")
    checks["machine_readable_api_schema"] = "PASS"

    allowed_imports = {
        "__future__", "ast", "copy", "csv", "dataclasses", "hashlib", "json", "os",
        "pathlib", "platform", "subprocess", "sys", "typing", "numpy", "sympy",
        "canonical_geometry_evaluator", "run_p01_evaluator",
    }
    for script in ("canonical_geometry_evaluator.py", "run_p01_evaluator.py", "verify_p01_evaluator.py"):
        tree = ast.parse((HERE / script).read_text(encoding="utf-8"), filename=script)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        require(imported <= allowed_imports, f"provenance import lint {script}: {sorted(imported - allowed_imports)}")
    requirements = (HERE / "requirements.txt").read_text(encoding="utf-8").splitlines()
    require(requirements == ["numpy==2.2.6", "sympy==1.13.1"], "dependency pins")
    checks["import_provenance_and_dependency_lint"] = "PASS"

    formulae = (HERE / "FORMULAE_AND_INDEX_CONVENTIONS.md").read_text(encoding="utf-8")
    for phrase in (
        "conditional on a supplied base/screen split",
        "These are geometric identities, not field equations.",
        "without selecting a physical representative",
    ):
        require(phrase in formulae, f"formula scope disclosure: {phrase}")
    checks["formula_and_scope_disclosures"] = "PASS"

    mutation = copy.deepcopy(data)
    mutation["implementation"]["slot_names"].pop()
    expect_failure("missing_metric_slot", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["implementation"]["slot_names"][9] = mutation["implementation"]["slot_names"][8]
    expect_failure("duplicate_metric_slot", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["implementation"]["first_jet_channels_exercised"] = 39
    expect_failure("omitted_coordinate_first_jet", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["implementation"]["symmetric_second_jet_channels_exercised"] = 99
    expect_failure("omitted_coordinate_second_jet", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["raw_residuals"]["split_block_inverse"] = 1.0
    expect_failure("wrong_inverse", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["fixtures"]["polar_flat"]["gamma_witnesses"]["Gamma^2_12"] = -0.5
    expect_failure("wrong_connection_sign", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["fixtures"]["unit_sphere_product"]["riemann_witness"] = -0.75
    expect_failure("wrong_curvature_sign_or_index_order", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["checks"]["first_cartan_identity"] = "FAIL"
    expect_failure("broken_first_cartan", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["checks"]["second_cartan_identity"] = "FAIL"
    expect_failure("broken_second_cartan", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["csn_weights"]["metric"] = 1
    expect_failure("broken_csn_weight", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["checks"]["constant_local_lorentz_invariance"] = "FAIL"
    expect_failure("failed_frame_reconstruction", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["checks"]["coordinate_coframe_roundtrip"] = "FAIL"
    expect_failure("failed_coordinate_reconstruction", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["premise_stamps"]["two_plus_two"] = "DERIVED_GLOBAL_SPLIT"
    expect_failure("conditional_split_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["premise_stamps"]["dynamics"] = "NATIVE"
    expect_failure("dynamics_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["scope"]["solution_space_explored"] = True
    expect_failure("solution_space_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["maximum_conclusion"] = "NATIVE_METRIC_SOLVED"
    expect_failure("maximum_conclusion_promoted", lambda: validate(mutation), catches)

    flat_jets, _, _, _, _ = fixture("cartesian_flat")
    bad_first = flat_jets.first.copy()
    bad_first[0, 0, 1] = 1.0
    expect_failure("asymmetric_metric_first_jet", lambda: evaluate_metric_jets(MetricJets(flat_jets.metric, bad_first, flat_jets.second)), catches)
    bad_metric = flat_jets.metric.copy()
    bad_metric[0, 1] = 1.0
    expect_failure("asymmetric_metric_value", lambda: evaluate_metric_jets(MetricJets(bad_metric, flat_jets.first, flat_jets.second)), catches)
    bad_second = flat_jets.second.copy()
    bad_second[0, 1, 0, 0] = 1.0
    expect_failure("asymmetric_metric_second_jet", lambda: evaluate_metric_jets(MetricJets(flat_jets.metric, flat_jets.first, bad_second)), catches)
    bad_second_metric = flat_jets.second.copy()
    bad_second_metric[0, 0, 0, 1] = 1.0
    expect_failure("asymmetric_metric_indices_in_second_jet", lambda: evaluate_metric_jets(MetricJets(flat_jets.metric, flat_jets.first, bad_second_metric)), catches)
    non_lorentz = MetricJets(np.eye(4), np.zeros((4, 4, 4)), np.zeros((4, 4, 4, 4)))
    expect_failure("non_lorentzian_metric", lambda: evaluate_metric_jets(non_lorentz), catches)
    expect_failure("singular_coordinate_transform", lambda: constant_linear_coordinate_transform_coframe(np.eye(4), np.zeros((4,4,4)), np.zeros((4,4,4,4)), np.zeros((4,4))), catches)
    expect_failure("non_lorentz_frame_transform", lambda: constant_internal_frame_transform_coframe(np.eye(4), np.zeros((4,4,4)), np.zeros((4,4,4,4)), 2*np.eye(4), ETA), catches)
    expect_failure("nonpositive_csn_factor", lambda: csn_scaled_metric_jets(flat_jets, 0.0, np.zeros(4), np.zeros((4,4))), catches)
    expect_failure("nonfinite_metric", lambda: evaluate_metric_jets(MetricJets(np.full((4,4), np.nan), flat_jets.first, flat_jets.second)), catches)
    expect_failure("wrong_metric_shape", lambda: evaluate_metric_jets(MetricJets(np.eye(3), flat_jets.first, flat_jets.second)), catches)
    bad_coframe_second = np.zeros((4,4,4,4)); bad_coframe_second[0,1,0,0] = 1.0
    expect_failure("asymmetric_coframe_second_jet", lambda: evaluate_coframe_jets(np.eye(4), np.zeros((4,4,4)), bad_coframe_second), catches)
    singular_coframe = np.eye(4); singular_coframe[3] = singular_coframe[2]
    expect_failure("singular_coframe", lambda: evaluate_coframe_jets(singular_coframe, np.zeros((4,4,4)), np.zeros((4,4,4,4))), catches)
    bad_sigma_second = np.zeros((4,4)); bad_sigma_second[0,1] = 1.0
    expect_failure("asymmetric_csn_second_jet", lambda: csn_scaled_metric_jets(flat_jets, 1.0, np.zeros(4), bad_sigma_second), catches)
    bad_slot_second = np.zeros((4,4,10)); bad_slot_second[0,1,0] = 1.0
    expect_failure("asymmetric_split_second_jet", lambda: metric_jets_from_split(np.array([-2.,0.,1.,1.,0.,1.,0.,0.,0.,0.]), np.zeros((4,10)), bad_slot_second), catches)
    expect_failure("nonpositive_split_screen", lambda: reconstruct_split(np.diag([-1.,1.,-1.,1.])), catches)
    expect_failure("nonlorentzian_split_base", lambda: reconstruct_split(np.eye(4)), catches)
    bad_lorentz_first = np.zeros((4,4,4)); bad_lorentz_first[0,0,0] = 1.0
    expect_failure("invalid_local_lorentz_first_jet", lambda: local_internal_frame_transform_coframe_jets(np.eye(4), np.zeros((4,4,4)), np.zeros((4,4,4,4)), np.eye(4), bad_lorentz_first, np.zeros((4,4,4,4))), catches)

    output = {
        "schema": "udt-p01-canonical-geometry-independent-verification-1.0",
        "status": "PASS",
        "maximum_conclusion": data["maximum_conclusion"],
        "main_result_sha256": sha256(RESULT),
        "checks": checks,
        "check_count": len(checks),
        "independent_regression_residuals": regression_residuals,
        "maximum_independent_residual": max(regression_residuals.values(), default=0.0),
        "catch_proofs": catches,
        "catch_proof_count": len(catches),
        "scope": {
            "independent_sympy_coordinate_implementation": True,
            "exact_symbolic_split_identity": True,
            "scientific_solve_executed": False,
            "gpu_used": False,
        },
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    VERIFY.write_text(rendered, encoding="utf-8")
    TRANSCRIPT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
