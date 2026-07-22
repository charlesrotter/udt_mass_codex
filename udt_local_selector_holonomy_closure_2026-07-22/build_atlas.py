#!/usr/bin/env python3
"""Build the preregistered local-output and curvature-holonomy-seed atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STRUCTURAL = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21"
FAMILIES = ROOT / "udt_independent_amplitude_metric_atlas_2026-07-21"
EVALUATOR = ROOT / "udt_canonical_geometry_evaluator_p01_2026-07-21"
JOINT = ROOT / "udt_joint_invariant_subspace_atlas_2026-07-21"
sys.path.insert(0, str(FAMILIES))
sys.path.insert(0, str(EVALUATOR))
sys.path.insert(0, str(JOINT))

import build_independent_amplitude_atlas as family_source  # noqa: E402
from canonical_geometry_evaluator import evaluate_metric_jets  # noqa: E402
from invariant_subspace_core import PAIRS, associative_algebra, classify_family, relmax  # noqa: E402


SCHEMA = "udt-local-selector-holonomy-closure-1.0"
MAXIMUM = (
    "BOUNDED_LOCAL_NATURAL_OUTPUT_AND_CURVATURE_HOLONOMY_SEED_ATLAS_CHARACTERIZED"
    "__NO_ACTION_OR_REALIZATION_LAW_DERIVED"
)
RANK_TOL = 1.0e-9
UNCERTAINTY_LOW = 1.0e-11
UNCERTAINTY_HIGH = 1.0e-7
SHELL_STEPS = (1.0e-3, 5.0e-4)
DIRECT_STEPS = (1.0e-4, 5.0e-5)
TRANSPORT_NODES = (33, 65)

SOURCE_HASHES = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    "udt_metric_native_two_pair_selector_audit_2026-07-21/SHA256SUMS.txt": "d800a5c1f6ec6deaa695d00728809de4fe81129651a8d9194a814637950ccdef",
    "udt_joint_invariant_subspace_atlas_2026-07-21/SHA256SUMS.txt": "973dcc8bb297fad8358087318b24e5db9d1179e8b6a51a2535a0110e30c108c2",
    "udt_instrument_motif_atlas_2026-07-21/SHA256SUMS.txt": "97dac2c32317deb603a054cffd3d2162f537d8bc7806d2276fa7e8544dd22ed5",
    "udt_global_metric_assembly_atlas_2026-07-22/SHA256SUMS.txt": "d4c7e7e16e38496343bbfbc8ef0867de45657ea2e25a724b44b653ff1b276374",
    "udt_century_adjacent_mathematics_survey_2026-07-22/MANIFEST.sha256": "66f1915965a5bd0ee8ff09b54b0ad1275578bfad447b7cb78b0a16e87b3e96f3",
}
LOCAL_HASHES = {
    "PREREGISTRATION.md": "34637bc051d8abd1a1474d15f84391dc4d64d40546da37b01e4d105514384623",
    "IMPLEMENTATION_PREREGISTRATION.md": "27687172f2ab4b6374b9001bf2b4715841c62d543eea82dd24f0c91a30a126d5",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, object]], fields: tuple[str, ...] | None = None) -> None:
    if fields is None:
        if not rows:
            raise ValueError(f"fields required for empty table {name}")
        fields = tuple(rows[0])
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def verify_sources() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for relative, expected in SOURCE_HASHES.items():
        actual = digest(ROOT / relative)
        if actual != expected:
            raise AssertionError(f"source hash {relative}: {actual} != {expected}")
        rows.append({"path": relative, "sha256": actual, "role": "IMMUTABLE_SOURCE"})
    for relative, expected in LOCAL_HASHES.items():
        actual = digest(HERE / relative)
        if actual != expected:
            raise AssertionError(f"preregistration hash {relative}: {actual} != {expected}")
        rows.append({"path": f"{HERE.name}/{relative}", "sha256": actual, "role": "PREREGISTRATION"})
    return rows


def q01_rows() -> list[dict[str, str]]:
    columns = (
        "candidate_id", "output_type", "lowest_jet_order", "primitive_data", "diffeomorphism_status",
        "csn_status", "internal_frame_status", "selection_capacity", "decisive_limit", "status",
        "evidence",
    )
    raw = [
        ("Q01_U00", "UNTYPED_REALIZATION_RELATION", "UNBOUNDED", "unspecified",
         "NOT_DEFINED", "NOT_DEFINED", "NOT_DEFINED",
         "cannot enumerate a natural operator before domain and codomain bundles are supplied",
         "registered UDT does not fix codomain derivative order parity or functional class",
         "CLASS_INFINITE_OR_UNTYPED__EXHAUSTION_NOT_WELL_POSED", "cold packet section 2"),
        ("Q01_S00", "SCALAR", "0", "phi and arbitrary smooth F(phi)",
         "NATURAL_SCALAR", "NEUTRAL_IF_PHI_NEUTRAL", "INVARIANT",
         "can label scalar-depth strata but supplies no preferred axis or common scale",
         "uncountably many smooth coefficient laws and no UDT rule chooses F",
         "INFINITE_FUNCTIONAL_CALCULUS__NO_SELECTION_RULE", "cold packet sections 1.3 and 2"),
        ("Q01_S01", "SCALAR_CURVATURE_CONTRACTION", "2", "g inverse Riemann Ricci Weyl phi jets",
         "NATURAL", "GENERICALLY_NONNEUTRAL_OR_WEIGHTED", "INVARIANT",
         "can characterize local conformal or curvature strata",
         "a weight-zero ratio needs a nonzero denominator and remains constant on a CSN orbit",
         "CONDITIONAL_STRATUM_DIAGNOSTIC", "two-pair selector audit C05-C08"),
        ("Q01_D00", "SCALAR_DENSITY", "0_TO_2", "metric volume density times scalar concomitant",
         "NATURAL_DENSITY", "WEIGHTED_UNLESS_COMPENSATED", "ORIENTATION_DEPENDENT_FOR_SIGNED_FORM",
         "can supply an integration density only after weight and orientation are fixed",
         "neutral compensation does not select a representative; no measure/action is registered",
         "NO_NATIVE_MEASURE_OR_SELECTOR", "cold packet sections 1.3 and 2"),
        ("Q01_V00", "COVECTOR_OR_VECTOR_LINE", "1", "dphi and metric dual",
         "NATURAL", "COVECTOR_NEUTRAL__VECTOR_WEIGHTED__LINE_NEUTRAL", "INVARIANT",
         "selects a line and orthogonal complement where dphi is nonzero and nonnull",
         "zero and null strata prevent a universal nondegenerate split",
         "CONDITIONAL_LOCAL_SELECTOR_ON_EXPLICIT_STRATUM", "two-pair selector audit C04"),
        ("Q01_T00", "SYMMETRIC_TWO_TENSOR", "0", "metric alone",
         "NATURAL", "WEIGHT_TWO", "INVARIANT",
         "mixed endomorphism is only the identity and preserves every subspace",
         "Lorentz stabilizer leaves no distinguished proper self-adjoint block",
         "ZERO_UDT_SELECTION_CREDIT", "two-pair selector audit C01"),
        ("Q01_T01", "SYMMETRIC_TWO_TENSOR", "2", "covariant Hessian of phi",
         "NATURAL", "NOT_CSN_COVARIANT_GENERALLY", "INVARIANT",
         "simple trace-free projected strata can mark axes",
         "conformal derivative terms and zero/repeated strata; projected result needs a supplied screen",
         "CONDITIONAL_LOCAL_SELECTOR_ON_EXPLICIT_STRATUM", "two-pair selector audit C05"),
        ("Q01_T02", "SYMMETRIC_TWO_TENSOR", "2", "Ricci and trace-free Ricci",
         "NATURAL", "NOT_CSN_COVARIANT_GENERALLY", "INVARIANT",
         "simple spectra can mark axes on favorable strata",
         "local conformal rescaling changes Ricci and degeneracies restore ambiguity",
         "CONDITIONAL_LOCAL_SELECTOR_ON_EXPLICIT_STRATUM", "two-pair selector audit C06-C07"),
        ("Q01_P00", "PROJECTOR_OR_INVOLUTION", "0_TO_2", "spectral calculus of registered endomorphisms",
         "NATURAL_WHERE_SPECTRAL_GAPS_PERSIST", "DEPENDS_ON_GENERATOR", "INVARIANT",
         "can encode a real split on simple semisimple strata",
         "undefined or nonunique at zero repeated complex or Jordan strata; full orchestra breaks smaller splits",
         "CONDITIONAL_LOCAL_SELECTOR_ON_EXPLICIT_STRATUM", "joint invariant-subspace atlas"),
        ("Q01_B00", "TWO_FORM_OR_BIVECTOR", "0", "metric plus optional orientation Hodge star",
         "NATURAL_IF_ORIENTED", "CONFORMALLY_NATURAL_ON_MIDDLE_FORMS", "ORIENTATION_REQUIRED",
         "supplies universal Lorentzian Hodge complex structure",
         "universal structure does not select a real simple tangent plane and star squared is minus one",
         "ZERO_UDT_SELECTION_CREDIT", "two-pair selector audit C02"),
        ("Q01_B01", "TWO_FORM_OR_BIVECTOR", "2", "Riemann or Weyl operator eigenbivectors",
         "NATURAL", "WEYL_CONFORMAL__RIEMANN_NONNEUTRAL", "ORIENTATION_OPTIONAL",
         "could mark a real simple plane if an isolated eigenspace existed",
         "zero isolated real simple eigenplanes in all 6144 registered two-jets",
         "NO_SELECTOR_IN_REGISTERED_TWO_JET_ENSEMBLE", "joint invariant-subspace atlas"),
        ("Q01_C00", "CONNECTION_OR_CURVATURE_VALUED", "1_TO_2", "Levi-Civita connection and curvature",
         "CONNECTION_NOT_TENSOR__CURVATURE_NATURAL", "LEVI_CIVITA_CONNECTION_NOT_CSN_INVARIANT", "INVARIANT",
         "curvature can diagnose a preserved reduction through its common algebra",
         "diagnosis is not selection; persistence requires holonomy and global gluing",
         "Q02_PERSISTENCE_TEST_REQUIRED", "global assembly atlas and survey"),
        ("Q01_F00", "COFRAME_ROW_OR_SLOT", "0", "chosen coframe components or row labels",
         "DIFFEOMORPHISM_COVARIANT_ONLY_WITH_INTERNAL_LABELS", "SCALES_WITH_COFRAME", "FRAME_DEPENDENT",
         "can name a plane only after an internal-frame reduction is supplied",
         "local Lorentz changes mix rows without changing metric geometry",
         "FRAME_DEPENDENT__UNSELECTED", "chart/coframe invariance atlas"),
        ("Q01_F01", "COFRAME_GAUGE_INVARIANT_CONTRACTION", "0_TO_2", "coframe with all internal indices contracted",
         "NATURAL", "SAME_AS_METRIC_CONCOMITANT", "INVARIANT",
         "reconstructs metric curvature and optional oriented volume data",
         "adds no selector beyond the corresponding metric-natural class",
         "REDUCES_TO_METRIC_OR_ORIENTATION_CLASS", "chart/coframe invariance atlas"),
        ("Q01_X00", "ARBITRARY_SMOOTH_COMBINATION", "0_TO_2", "smooth scalar coefficients multiplying primitive tensors",
         "NATURAL_IF_COEFFICIENTS_ARE_INVARIANTS", "DEPENDS_ON_WEIGHTS", "INVARIANT_IF_CONTRACTED",
         "can tune individual spectra or degeneracies",
         "coefficient law is itself an unselected infinite functional datum",
         "INFINITE_FUNCTIONAL_CALCULUS__NO_SELECTION_RULE", "century survey M01-M02"),
        ("Q01_H00", "HIGHER_FINITE_JET_OUTPUT", "3_OR_MORE", "covariant derivatives and arbitrary contractions",
         "NATURAL_AFTER_TYPE_IS_FIXED", "UNSPECIFIED", "UNSPECIFIED",
         "may supply new nonparallel local strata",
         "registered UDT fixes neither maximum order nor codomain; not covered by order-two census",
         "OPEN_HIGHER_JETS", "century survey Q01 scope"),
    ]
    return [dict(zip(columns, row)) for row in raw]


def q01_logic_rows() -> list[dict[str, str]]:
    return [
        {
            "logic_id": "L01_CSN_ORBIT_CONSTANCY",
            "premise": "S[Omega^2 g,phi]=S[g,phi] for every positive local Omega",
            "deduction": "S has the same value on every member of one CSN orbit",
            "conclusion": "S cannot distinguish or select a representative inside that orbit",
            "status": "DERIVED_EXACT",
        },
        {
            "logic_id": "L02_COFRAME_GAUGE",
            "premise": "internal coframe changes preserve g while mixing row labels",
            "deduction": "an uncontracted row/slot output changes while metric geometry does not",
            "conclusion": "coframe labels require a separately derived frame reduction",
            "status": "DERIVED_EXACT_GIVEN_LOCAL_FRAME_EQUIVALENCE",
        },
        {
            "logic_id": "L03_UNTYPED_INFINITY",
            "premise": "phi is a natural scalar and F may be any smooth real function",
            "deduction": "already at order zero there are infinitely many scalar natural outputs F(phi)",
            "conclusion": "all finite-jet outputs cannot be finitely enumerated without a codomain and functional class",
            "status": "DERIVED_EXACT",
        },
        {
            "logic_id": "L04_ALGEBRA_MONOTONICITY",
            "premise": "a common invariant subspace must be invariant under every generator",
            "deduction": "adding generators can only preserve or shrink the common invariant-subspace lattice",
            "conclusion": "once curvature generates M4(R), higher curvature jets cannot restore a parallel proper subspace",
            "status": "DERIVED_EXACT",
        },
    ]


def family_geometry(bank: int, amplitudes: np.ndarray, point: np.ndarray):
    family = family_source.regular_family(bank, amplitudes, point)
    return family, evaluate_metric_jets(family["metric_jets"])


def curvature_operators(geometry) -> list[np.ndarray]:
    return [np.asarray(geometry.riemann_up[:, :, mu, nu], dtype=float) for mu, nu in PAIRS]


def algebra_class(operators: list[np.ndarray], metric: np.ndarray) -> dict[str, object]:
    _basis, algebra = associative_algebra(operators)
    dimension = int(algebra["dimension"])
    nonzero = sum(float(np.linalg.norm(operator)) > 1.0e-12 for operator in operators)
    if dimension == 16:
        reducibility = "FULL_MATRIX_ALGEBRA_IRREDUCIBLE"
        central_blocks = "NO_NONTRIVIAL_CENTRAL_BLOCK"
        primitive_block_ranks = "4"
        family_uncertain = False
    elif nonzero == 0:
        reducibility = "PROPER_ALGEBRA_NONCENTRAL_AMBIGUITY"
        central_blocks = "NO_DISTINGUISHED_BLOCK__ZERO_GENERATORS"
        primitive_block_ranks = "4_AMBIGUOUS"
        family_uncertain = False
    else:
        family = classify_family(operators, np.zeros(4), np.asarray(metric, dtype=float))
        reducibility = str(family["reducibility_class"])
        central_blocks = str(family["central_block_status"])
        primitive_block_ranks = str(family["central_block_ranks"])
        family_uncertain = family["numeric_status"] == "NUMERIC_UNCERTAIN"
    return {
        "dimension": dimension,
        "uncertain": bool(algebra["uncertain"] or family_uncertain),
        "closure_residual": float(algebra["closure_residual"]),
        "reducibility": reducibility,
        "central_blocks": central_blocks,
        "primitive_block_ranks": primitive_block_ranks,
    }


def connection_matrix(geometry, displacement: np.ndarray) -> np.ndarray:
    return np.einsum("m,rmn->rn", displacement, np.asarray(geometry.christoffel, dtype=float))


def parallel_transport(bank: int, amplitudes: np.ndarray, point: np.ndarray, displacement: np.ndarray, nodes: int) -> np.ndarray:
    steps = nodes - 1
    step = 1.0 / steps
    matrix = np.eye(4)

    def rhs(s: float, value: np.ndarray) -> np.ndarray:
        _family, geometry = family_geometry(bank, amplitudes, point + s * displacement)
        return -connection_matrix(geometry, displacement) @ value

    for index in range(steps):
        s = index * step
        k1 = rhs(s, matrix)
        k2 = rhs(s + 0.5 * step, matrix + 0.5 * step * k1)
        k3 = rhs(s + 0.5 * step, matrix + 0.5 * step * k2)
        k4 = rhs(s + step, matrix + step * k3)
        matrix = matrix + (step / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return matrix


def pulled_curvature(
    bank: int,
    amplitudes: np.ndarray,
    point: np.ndarray,
    displacement: np.ndarray,
    nodes: int,
) -> tuple[list[np.ndarray], np.ndarray, object, float]:
    _base_family, base_geometry = family_geometry(bank, amplitudes, point)
    _end_family, end_geometry = family_geometry(bank, amplitudes, point + displacement)
    transport = parallel_transport(bank, amplitudes, point, displacement, nodes)
    inverse = np.linalg.inv(transport)
    tensor = np.asarray(end_geometry.riemann_up, dtype=float)
    pulled = []
    for mu, nu in PAIRS:
        endpoint = np.zeros((4, 4))
        for rho in range(4):
            for sigma in range(4):
                endpoint += transport[rho, mu] * transport[sigma, nu] * tensor[:, :, rho, sigma]
        pulled.append(inverse @ endpoint @ transport)
    isometry = relmax(transport.T @ end_geometry.metric @ transport, base_geometry.metric)
    return pulled, transport, end_geometry, isometry


def direct_covariant_curvature_derivative(
    bank: int,
    amplitudes: np.ndarray,
    point: np.ndarray,
    step: float,
) -> list[np.ndarray]:
    _family, base = family_geometry(bank, amplitudes, point)
    gamma = np.asarray(base.christoffel, dtype=float)
    curvature = np.asarray(base.riemann_up, dtype=float)
    operators: list[np.ndarray] = []
    for lam in range(4):
        displacement = np.zeros(4)
        displacement[lam] = step
        _plus_family, plus = family_geometry(bank, amplitudes, point + displacement)
        _minus_family, minus = family_geometry(bank, amplitudes, point - displacement)
        partial = (np.asarray(plus.riemann_up) - np.asarray(minus.riemann_up)) / (2.0 * step)
        covariant = partial.copy()
        for a in range(4):
            for b in range(4):
                for mu in range(4):
                    for nu in range(4):
                        value = partial[a, b, mu, nu]
                        for c in range(4):
                            value += gamma[a, lam, c] * curvature[c, b, mu, nu]
                            value -= gamma[c, lam, b] * curvature[a, c, mu, nu]
                            value -= gamma[c, lam, mu] * curvature[a, b, c, nu]
                            value -= gamma[c, lam, nu] * curvature[a, b, mu, c]
                        covariant[a, b, mu, nu] = value
        operators.extend(covariant[:, :, mu, nu] for mu, nu in PAIRS)
    return operators


def transported_derivative(
    bank: int,
    amplitudes: np.ndarray,
    point: np.ndarray,
    step: float,
) -> tuple[list[np.ndarray], float, float]:
    result: list[np.ndarray] = []
    max_isometry = 0.0
    max_refinement = 0.0
    for lam in range(4):
        displacement = np.zeros(4)
        displacement[lam] = step
        plus33, matrix_plus33, _g, iso_plus33 = pulled_curvature(bank, amplitudes, point, displacement, 33)
        minus33, matrix_minus33, _g, iso_minus33 = pulled_curvature(bank, amplitudes, point, -displacement, 33)
        plus65, matrix_plus65, _g, iso_plus65 = pulled_curvature(bank, amplitudes, point, displacement, 65)
        minus65, matrix_minus65, _g, iso_minus65 = pulled_curvature(bank, amplitudes, point, -displacement, 65)
        max_isometry = max(max_isometry, iso_plus33, iso_minus33, iso_plus65, iso_minus65)
        max_refinement = max(
            max_refinement,
            relmax(matrix_plus33, matrix_plus65),
            relmax(matrix_minus33, matrix_minus65),
        )
        result.extend((plus65[index] - minus65[index]) / (2.0 * step) for index in range(len(PAIRS)))
    return result, max_isometry, max_refinement


def exact_flat_check(bank: int, amplitudes: np.ndarray, point: np.ndarray) -> tuple[bool, float]:
    if not np.all(np.asarray(amplitudes[:10]) == 0.0):
        return False, math.nan
    residual = 0.0
    probes = [point]
    for step in SHELL_STEPS:
        for axis in range(4):
            for sign in (-1.0, 1.0):
                displacement = np.zeros(4)
                displacement[axis] = sign * step
                probes.append(point + displacement)
    for probe in probes:
        family, geometry = family_geometry(bank, amplitudes, probe)
        residual = max(
            residual,
            float(np.max(np.abs(family["metric_jets"].first))),
            float(np.max(np.abs(family["metric_jets"].second))),
            float(np.max(np.abs(geometry.riemann_up))),
        )
    return residual == 0.0, residual


def shell_classification(bank: int, amplitudes: np.ndarray, point: np.ndarray, step: float) -> dict[str, object]:
    _family, base = family_geometry(bank, amplitudes, point)
    operators = curvature_operators(base)
    max_isometry = 0.0
    max_refinement = 0.0
    for axis in range(4):
        for sign in (-1.0, 1.0):
            displacement = np.zeros(4)
            displacement[axis] = sign * step
            pulled33, matrix33, _end, iso33 = pulled_curvature(bank, amplitudes, point, displacement, 33)
            pulled65, matrix65, _end, iso65 = pulled_curvature(bank, amplitudes, point, displacement, 65)
            operators.extend(pulled65)
            max_isometry = max(max_isometry, iso33, iso65)
            max_refinement = max(max_refinement, relmax(matrix33, matrix65))
    classification = algebra_class(operators, base.metric)
    classification.update({"transport_isometry": max_isometry, "transport_refinement": max_refinement})
    return classification


def anchor_ids() -> set[str]:
    result = set()
    for mask in range(16):
        result.add(f"R00_1_M{mask:X}_B0_P0")
        result.add(f"V016_M{mask:X}_B3_P7")
    return result


def frozen_f06_dimensions() -> dict[str, int]:
    rows = read_tsv(JOINT / "FAMILY_SUBSPACE_ATLAS.tsv")
    return {
        row["configuration_id"]: int(row["algebra_dimension"])
        for row in rows if row["family_id"] == "F06_RIEMANN_GENERATORS"
    }


def main() -> None:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    source_rows = verify_sources()
    write_tsv("SOURCE_LINEAGE.tsv", source_rows)
    outputs = q01_rows()
    write_tsv("LOCAL_OUTPUT_TYPE_CENSUS.tsv", outputs)
    logic = q01_logic_rows()
    write_tsv("CSN_AND_EXHAUSTIBILITY_LOGIC.tsv", logic)

    frozen_dimensions = frozen_f06_dimensions()
    anchors = anchor_ids()
    atlas_rows: list[dict[str, object]] = []
    anchor_rows: list[dict[str, object]] = []
    summary_counter: Counter[str] = Counter()
    mask_counter: dict[str, Counter[str]] = defaultdict(Counter)
    seen: set[str] = set()
    maximum_base_closure = 0.0
    maximum_flat_residual = 0.0
    maximum_anchor_derivative_residual = 0.0
    maximum_anchor_isometry = 0.0
    maximum_anchor_transport_refinement = 0.0

    for shard in read_tsv(STRUCTURAL / "RAW_SHARD_REGISTRY.tsv"):
        shard_path = STRUCTURAL / shard["path"]
        if digest(shard_path) != shard["sha256"]:
            raise AssertionError(f"raw shard hash {shard['path']}")
        with shard_path.open(encoding="utf-8") as handle:
            for line in handle:
                raw = json.loads(line)
                configuration_id = str(raw["configuration_id"])
                if configuration_id in seen:
                    raise AssertionError(f"duplicate {configuration_id}")
                seen.add(configuration_id)
                bank = int(str(raw["bank"])[1:])
                amplitudes = np.asarray(raw["effective_amplitudes"], dtype=float)
                point = np.asarray(raw["coordinates"], dtype=float)
                _family, geometry = family_geometry(bank, amplitudes, point)
                base_operators = curvature_operators(geometry)
                base = algebra_class(base_operators, geometry.metric)
                maximum_base_closure = max(maximum_base_closure, float(base["closure_residual"]))
                if frozen_dimensions.get(configuration_id) != int(base["dimension"]):
                    raise AssertionError(f"frozen F06 dimension mismatch {configuration_id}")

                flat_exact, flat_residual = exact_flat_check(bank, amplitudes, point)
                if math.isfinite(flat_residual):
                    maximum_flat_residual = max(maximum_flat_residual, flat_residual)
                shell_a = None
                shell_b = None
                if int(base["dimension"]) == 16 and not bool(base["uncertain"]):
                    final_class = "BASE_CURVATURE_FULL_IRREDUCIBLE__HIGHER_JETS_MONOTONE"
                elif flat_exact:
                    final_class = "EXACT_CONSTANT_METRIC_FLAT__ALL_SUBSPACES_AMBIGUOUS"
                else:
                    shell_a = shell_classification(bank, amplitudes, point, SHELL_STEPS[0])
                    shell_b = shell_classification(bank, amplitudes, point, SHELL_STEPS[1])
                    stable = (
                        shell_a["dimension"] == shell_b["dimension"]
                        and shell_a["reducibility"] == shell_b["reducibility"]
                        and max(shell_a["transport_isometry"], shell_b["transport_isometry"]) <= 2.0e-9
                        and max(shell_a["transport_refinement"], shell_b["transport_refinement"]) <= 2.0e-9
                        and not shell_a["uncertain"] and not shell_b["uncertain"]
                    )
                    if not stable:
                        final_class = "NUMERIC_UNCERTAIN_RETAINED"
                    elif int(shell_b["dimension"]) == 16:
                        final_class = "TRANSPORTED_CURVATURE_FULL_IRREDUCIBLE_BOUNDED"
                    elif shell_b["reducibility"] in {
                        "UNIQUE_CENTRAL_2PLUS2", "MULTIPLE_CENTRAL_2PLUS2"
                    }:
                        final_class = "PROPER_COMMON_REDUCTION_OBSERVED_BOUNDED"
                    else:
                        final_class = "OPEN_NONFULL_BEYOND_SHELL_SCOPE"

                row = {
                    "configuration_id": configuration_id,
                    "carrier_id": raw["carrier_id"],
                    "mask_id": raw["mask_id"],
                    "bank": raw["bank"],
                    "point_id": raw["point_id"],
                    "metric_amplitudes_zero": "YES" if np.all(amplitudes[:10] == 0.0) else "NO",
                    "base_algebra_dimension": base["dimension"],
                    "base_reducibility": base["reducibility"],
                    "base_central_blocks": base["central_blocks"],
                    "base_numeric_status": "UNCERTAIN" if base["uncertain"] else "CLASSIFIED",
                    "base_closure_residual": f"{base['closure_residual']:.17g}",
                    "flat_exact": "YES" if flat_exact else "NO",
                    "flat_certification_residual": f"{flat_residual:.17g}" if math.isfinite(flat_residual) else "-",
                    "shell_h1_dimension": shell_a["dimension"] if shell_a else "NOT_REQUIRED",
                    "shell_h2_dimension": shell_b["dimension"] if shell_b else "NOT_REQUIRED",
                    "shell_h1_reducibility": shell_a["reducibility"] if shell_a else "NOT_REQUIRED",
                    "shell_h2_reducibility": shell_b["reducibility"] if shell_b else "NOT_REQUIRED",
                    "shell_max_isometry": (
                        f"{max(shell_a['transport_isometry'], shell_b['transport_isometry']):.17g}"
                        if shell_a and shell_b else "NOT_REQUIRED"
                    ),
                    "shell_max_refinement": (
                        f"{max(shell_a['transport_refinement'], shell_b['transport_refinement']):.17g}"
                        if shell_a and shell_b else "NOT_REQUIRED"
                    ),
                    "final_class": final_class,
                    "physical_merit": "NOT_EVALUATED",
                }
                atlas_rows.append(row)
                summary_counter[final_class] += 1
                mask_counter[str(raw["mask_id"])][final_class] += 1

                if configuration_id in anchors:
                    per_step = []
                    for step in DIRECT_STEPS:
                        direct = direct_covariant_curvature_derivative(bank, amplitudes, point, step)
                        transported, isometry, refinement = transported_derivative(bank, amplitudes, point, step)
                        residual = max(
                            (relmax(left, right) for left, right in zip(direct, transported)), default=0.0
                        )
                        direct_class = algebra_class([*base_operators, *direct], geometry.metric)
                        transported_class = algebra_class([*base_operators, *transported], geometry.metric)
                        per_step.append((step, residual, isometry, refinement, direct_class, transported_class))
                    maximum_anchor_derivative_residual = max(maximum_anchor_derivative_residual, *(item[1] for item in per_step))
                    maximum_anchor_isometry = max(maximum_anchor_isometry, *(item[2] for item in per_step))
                    maximum_anchor_transport_refinement = max(maximum_anchor_transport_refinement, *(item[3] for item in per_step))
                    anchor_rows.append({
                        "configuration_id": configuration_id,
                        "mask_id": raw["mask_id"],
                        "base_algebra_dimension": base["dimension"],
                        "h1_direct_dimension": per_step[0][4]["dimension"],
                        "h1_transported_dimension": per_step[0][5]["dimension"],
                        "h2_direct_dimension": per_step[1][4]["dimension"],
                        "h2_transported_dimension": per_step[1][5]["dimension"],
                        "h1_derivative_residual": f"{per_step[0][1]:.17g}",
                        "h2_derivative_residual": f"{per_step[1][1]:.17g}",
                        "h1_transport_isometry": f"{per_step[0][2]:.17g}",
                        "h2_transport_isometry": f"{per_step[1][2]:.17g}",
                        "h1_transport_refinement": f"{per_step[0][3]:.17g}",
                        "h2_transport_refinement": f"{per_step[1][3]:.17g}",
                        "algebra_agreement": "YES" if all(item[4]["dimension"] == item[5]["dimension"] for item in per_step) else "NO",
                        "residual_gate": "PASS" if per_step[1][1] <= 2.0e-5 else "FAIL_RETAINED",
                    })

    if len(seen) != 6144 or seen != set(frozen_dimensions):
        raise AssertionError(f"configuration coverage {len(seen)}")
    if len(anchor_rows) != 32:
        raise AssertionError(f"anchor coverage {len(anchor_rows)}")
    atlas_rows.sort(key=lambda row: row["configuration_id"])
    anchor_rows.sort(key=lambda row: row["configuration_id"])
    write_tsv("CURVATURE_HOLONOMY_SEED_ATLAS.tsv", atlas_rows)
    write_tsv("DIRECT_DERIVATIVE_ANCHORS.tsv", anchor_rows)

    summary_rows = []
    for mask in sorted(mask_counter, key=lambda item: int(item[1:], 16)):
        for classification, count in sorted(mask_counter[mask].items()):
            summary_rows.append({"mask_id": mask, "final_class": classification, "count": count})
    write_tsv("HOLONOMY_CLASS_BY_MASK.tsv", summary_rows)

    q01_counter = Counter(row["status"] for row in outputs)
    result = {
        "schema": SCHEMA,
        "maximum_conclusion": MAXIMUM,
        "q01": {
            "candidate_rows": len(outputs),
            "status_counts": dict(sorted(q01_counter.items())),
            "logic_rows": len(logic),
            "representative_selector_ruling": "CSN_NEUTRAL_REPRESENTATIVE_SELECTOR_IMPOSSIBLE_BY_ORBIT_CONSTANCY",
            "exhaustibility_ruling": "ALL_FINITE_JET_OUTPUTS_NOT_FINITELY_ENUMERABLE_WITHOUT_TYPED_CODOMAIN_ORDER_AND_FUNCTIONAL_CLASS",
            "bounded_ruling": "ORDER_ZERO_TO_TWO_JOIN_RELEVANT_GENERATOR_CLASSES_CHARACTERIZED",
        },
        "q02": {
            "configurations": len(atlas_rows),
            "anchors": len(anchor_rows),
            "final_class_counts": dict(sorted(summary_counter.items())),
            "maximum_base_closure_residual": maximum_base_closure,
            "maximum_flat_certification_residual": maximum_flat_residual,
            "maximum_anchor_derivative_residual": maximum_anchor_derivative_residual,
            "maximum_anchor_transport_isometry": maximum_anchor_isometry,
            "maximum_anchor_transport_refinement": maximum_anchor_transport_refinement,
            "global_holonomy_claim": "NOT_MADE",
        },
        "inputs": {row["path"]: row["sha256"] for row in source_rows},
        "gpu_runs": 0,
        "physics_solves": 0,
    }
    result["atlas_rows_sha256"] = canonical_hash(atlas_rows)
    result["anchor_rows_sha256"] = canonical_hash(anchor_rows)
    (HERE / "ATLAS_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
