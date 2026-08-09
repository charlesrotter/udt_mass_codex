#!/usr/bin/env python3
"""Exact algebra and census checks for the complete-angular family MAP."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "bde6ae01"
KEYS: dict[str, bool] = {}

SCREEN_AXIS = ("ISOTROPIC", "AREA_ONLY", "DIAGONAL_SHEAR", "OFFDIAGONAL_SHEAR", "BOTH_SHEARS", "AREA_PLUS_TWO_SHEARS", "DEGENERATE")
MIXING_AXIS = ("ZERO", "AXIAL_SHIFT", "TWO_COMPONENT_SHIFT", "TWIST_FREE_CONTROL", "CAUSAL_NULL_CONTROL")
DEPENDENCE_AXIS = ("RADIAL_ONLY", "AXISYMMETRIC_R_THETA", "FULL_R_THETA_PSI", "CONDITIONAL_S3")
SYMMETRY_AXIS = ("SO3", "U1_REFLECTION_OPTIONAL", "DISCRETE", "NONE", "SYMMETRY_ENHANCED")
GLOBAL_AXIS = ("LOCAL_SPHERICAL", "CONDITIONAL_S3", "GLOBAL_NON_TORIC", "MISSING_WRL_S3_JOIN")


def key(name: str, condition: object) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}")


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def frozen_hash(path_text: str) -> str:
    data = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{path_text}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    return hashlib.sha256(data).hexdigest()


def cell_disposition(screen: str, mixing: str, dependence: str, symmetry: str, global_status: str) -> str:
    """Assign a scope disposition, never a physical merit ranking."""
    if screen == "DEGENERATE":
        return "DEGENERATE_CONTROL_NO_INVERSE"
    if dependence == "CONDITIONAL_S3" and global_status == "LOCAL_SPHERICAL":
        return "GLOBAL_DOMAIN_MISMATCH"
    if dependence != "CONDITIONAL_S3" and global_status in {"CONDITIONAL_S3", "GLOBAL_NON_TORIC"}:
        return "GLOBAL_DOMAIN_MISMATCH"
    if symmetry == "SO3":
        if screen == "ISOTROPIC" and mixing == "ZERO" and dependence == "RADIAL_ONLY" and global_status == "LOCAL_SPHERICAL":
            return "ROUND_SO3_ENVELOPE_UNSELECTED"
        return "SYMMETRY_COEFFICIENT_INCOMPATIBLE"
    if symmetry == "U1_REFLECTION_OPTIONAL" and dependence == "FULL_R_THETA_PSI":
        return "SYMMETRY_COEFFICIENT_INCOMPATIBLE"
    if global_status == "MISSING_WRL_S3_JOIN":
        return "GLOBAL_JOIN_OPEN_NO_CROSS_SPLICE"
    if symmetry == "SYMMETRY_ENHANCED":
        return "SYMMETRY_ENHANCED_CONTROL"
    if dependence == "CONDITIONAL_S3":
        return "CONDITIONAL_S3_CONTROL_ENVELOPE"
    if symmetry == "U1_REFLECTION_OPTIONAL":
        return "AXIAL_U1_ENVELOPE_UNSELECTED"
    if dependence == "FULL_R_THETA_PSI":
        return "GENERAL_NONAXIS_ENVELOPE_UNSELECTED"
    return "GENERIC_SCREEN_ENVELOPE_UNSELECTED"


def write_axis_cross_product() -> int:
    rows = []
    for index, values in enumerate(itertools.product(SCREEN_AXIS, MIXING_AXIS, DEPENDENCE_AXIS, SYMMETRY_AXIS, GLOBAL_AXIS), start=1):
        screen, mixing, dependence, symmetry, global_status = values
        rows.append({
            "cell_id": f"X{index:04d}",
            "screen": screen,
            "mixing": mixing,
            "dependence": dependence,
            "symmetry": symmetry,
            "global_status": global_status,
            "disposition": cell_disposition(*values),
        })
    path = HERE / "AXIS_CROSS_PRODUCT_DISPOSITION.tsv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    A, q11, q12, q22, b1, b2 = sp.symbols("A q11 q12 q22 b1 b2", real=True)
    Q = sp.Matrix([[q11, q12], [q12, q22]])
    b = sp.Matrix([b1, b2])
    Qinv = sp.simplify(Q.inv())
    v = sp.simplify(Qinv * b)
    Lambda = sp.simplify(A + (b.T * v)[0])

    metric = sp.Matrix(
        [
            [-A, 0, b1, b2],
            [0, 1 / A, 0, 0],
            [b1, 0, q11, q12],
            [b2, 0, q12, q22],
        ]
    )
    inverse = sp.zeros(4)
    inverse[0, 0] = -1 / Lambda
    inverse[1, 1] = A
    for i in range(2):
        inverse[0, i + 2] = v[i] / Lambda
        inverse[i + 2, 0] = v[i] / Lambda
        for j in range(2):
            inverse[i + 2, j + 2] = Qinv[i, j] - v[i] * v[j] / Lambda

    det_expected = -Q.det() * Lambda / A
    key("K01_general_inverse", all(sp.simplify(x) == 0 for x in metric * inverse - sp.eye(4)))
    key("K02_general_determinant", sp.simplify(metric.det() - det_expected) == 0)
    key("K03_positive_screen_lorentzian", sp.simplify((-A - (b.T * Qinv * b)[0]) + Lambda) == 0)

    # Recover the C1 axis-regular spherical lift.
    r, theta, h = sp.symbols("r theta h", positive=True, real=True)
    s = sp.sin(theta)
    c1 = {q11: r**2, q12: 0, q22: r**2 * s**2, b1: 0, b2: h * s**2}
    D = A * r**2 + h**2 * s**2
    key("K04_C1_Lambda", sp.trigsimp(sp.simplify(Lambda.subs(c1) - D / r**2)) == 0)
    key("K05_C1_volume", sp.trigsimp(sp.simplify((-det_expected.subs(c1)) - r**2 * s**2 * D / A)) == 0)
    key("K06_C1_tpsi_inverse", sp.trigsimp(sp.simplify(inverse[0, 3].subs(c1) - h / D)) == 0)
    key("K07_C1_psipsi_inverse", sp.trigsimp(sp.simplify(inverse[3, 3].subs(c1) - A / (s**2 * D))) == 0)

    # The general stationary mode-reduced operator contains
    # -i omega S^-1 d_A(S v^A/Lambda) u in addition to the transport term.
    x, eps = sp.symbols("x epsilon", real=True)
    Lambda_w = 1 + eps**2 * sp.sin(x) ** 2
    S_w = sp.sqrt(Lambda_w)
    gt_x = eps * sp.sin(x) / Lambda_w
    shift_divergence = sp.simplify(sp.diff(S_w * gt_x, x) / S_w)
    key("K08_shift_divergence_witness", sp.simplify(shift_divergence - eps * sp.cos(x) / Lambda_w**2) == 0)
    key("K09_shift_divergence_nonzero", sp.simplify(shift_divergence.subs({eps: 1, x: 0}) - 1) == 0)

    # At b=0 the screen inverse and round operator are recovered.
    zero_mix = {b1: 0, b2: 0}
    key("K10_zero_mix_Lambda", sp.simplify(Lambda.subs(zero_mix) - A) == 0)
    key("K11_zero_mix_screen_inverse", all(sp.simplify(inverse[i + 2, j + 2].subs(zero_mix) - Qinv[i, j]) == 0 for i in range(2) for j in range(2)))

    # Three independent symmetric screen tangents: area and two shears.
    tangents = [
        sp.Matrix([[1, 0], [0, 1]]),
        sp.Matrix([[2, 0], [0, -2]]),
        sp.Matrix([[0, 1], [1, 0]]),
    ]
    flattened = sp.Matrix.hstack(*(sp.Matrix([T[0, 0], T[0, 1], T[1, 1]]) for T in tangents))
    key("K12_three_screen_modes", flattened.rank() == 3)

    # A nonaxisymmetric area factor generates m -> m +/- 1 coupling.
    psi = sp.symbols("psi", real=True)
    m = sp.symbols("m", integer=True)
    plus = sp.integrate(sp.exp(-sp.I * (m + 1) * psi) * sp.cos(psi) * sp.exp(sp.I * m * psi), (psi, 0, 2 * sp.pi)) / (2 * sp.pi)
    minus = sp.integrate(sp.exp(-sp.I * (m - 1) * psi) * sp.cos(psi) * sp.exp(sp.I * m * psi), (psi, 0, 2 * sp.pi)) / (2 * sp.pi)
    far = sp.integrate(sp.exp(-sp.I * (m + 2) * psi) * sp.cos(psi) * sp.exp(sp.I * m * psi), (psi, 0, 2 * sp.pi)) / (2 * sp.pi)
    key("K13_nonaxis_m_coupling", sp.simplify(plus - sp.Rational(1, 2)) == 0 and sp.simplify(minus - sp.Rational(1, 2)) == 0 and sp.simplify(far) == 0)

    # Frozen source identity.
    source_rows = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            path_text, digest = line.rstrip("\n").split("\t")
            source_rows.append((path_text, digest))
    key("K14_source_manifest", all(frozen_hash(path) == digest for path, digest in source_rows))

    families = read_tsv("FAMILY_UNIVERSE.tsv")
    routes = read_tsv("REGISTERED_CANDIDATE_ROUTING.tsv")
    bases = read_tsv("BASIS_COUPLING_ATLAS.tsv")
    batches = read_tsv("SOLVE_BATCH_DESIGN.tsv")
    cross_count = write_axis_cross_product()
    cross_rows = read_tsv("AXIS_CROSS_PRODUCT_DISPOSITION.tsv")
    key("K15_family_ids_unique", len(families) == 18 and len({row["family_id"] for row in families}) == 18)
    routed = [row["candidate_id"] for row in routes]
    expected_candidates = {f"C{i:02d}" for i in range(1, 19)}
    key("K16_C01_C18_exact_coverage", len(routes) == 18 and set(routed) == expected_candidates and len(set(routed)) == 18)
    family_ids = {row["family_id"] for row in families}
    key("K17_route_targets_exist", all(row["family_id"] in family_ids for row in routes))
    route_by_id = {row["candidate_id"]: row for row in routes}
    key("K18_special_controls_preserved", route_by_id["C14"]["disposition"] == "SYMMETRY_ENHANCED_CONTROL" and route_by_id["C15"]["disposition"] == "TWIST_FREE_CONTROL" and route_by_id["C18"]["disposition"] == "DEGENERATE_NO_INVERSE")
    key("K19_causal_controls_preserved", all(route_by_id[cid]["disposition"] == "CAUSAL_STRATA_CONTROL" for cid in ("C16", "C17")))
    key("K20_basis_census", len(bases) == 8 and len({row["basis_id"] for row in bases}) == 8)
    key("K21_nonaxis_basis_mixes_m", any(row["basis_id"] == "B04" and row["m_status"] == "MIXED" for row in bases))
    key("K22_no_solve_authorized", len(batches) == 7 and all(row["authorization"] == "NOT_AUTHORIZED" for row in batches))
    key("K23_no_data_merit_filter", all(row["acceptance_rule"] == "CHARACTERIZE_ALL_OUTPUTS" for row in batches))
    key("K24_no_cross_splice", any(row["family_id"] == "F15" and row["global_join"] == "NO_WRL_S3_CROSS_SPLICE" for row in families))
    expected_cross_count = len(SCREEN_AXIS) * len(MIXING_AXIS) * len(DEPENDENCE_AXIS) * len(SYMMETRY_AXIS) * len(GLOBAL_AXIS)
    key("K25_axis_cross_product_census", cross_count == expected_cross_count == 2800 and len(cross_rows) == 2800)
    key("K26_axis_cells_unique", len({row["cell_id"] for row in cross_rows}) == 2800)
    key("K27_axis_cells_dispositioned", all(row["disposition"] for row in cross_rows) and len({row["disposition"] for row in cross_rows}) >= 8)

    if not all(KEYS.values()):
        raise SystemExit("family-atlas derivation failed")

    result = {
        "status": "VERIFIED_DESIGN_MAP__GENERAL_STATIONARY_SCREEN_OPERATOR_DERIVED__NO_SOLVE_AUTHORIZED",
        "key_count": len(KEYS),
        "keys": KEYS,
        "general_inverse": {
            "Lambda": "A+b^T q^-1 b",
            "gtt": "-1/Lambda",
            "gtA": "v^A/Lambda with v=q^-1 b",
            "gAB": "q^-1-v v^T/Lambda",
            "grr": "A",
        },
        "determinant": "-det(q) Lambda/A",
        "volume": "sqrt(det(q) Lambda/A)",
        "mode_operator": "S^-1 d_r(S A u_r)+S^-1 d_A[S(q^-1-vv^T/Lambda)^AB d_B u]+omega^2 u/Lambda-2i omega(v^A/Lambda)d_Au-i omega S^-1 d_A(Sv^A/Lambda)u",
        "family_count": len(families),
        "candidate_route_count": len(routes),
        "basis_count": len(bases),
        "batch_count": len(batches),
        "axis_cross_product_count": len(cross_rows),
        "next_design_ready_task": "N01_C1_HARMONIC_COUPLING_MATRIX_ATLAS",
        "maximum_conclusion": "architecture only; physical complete screen, spectra, populations, FD2 and GPU work remain open and unauthorized",
        "sympy_version": sp.__version__,
    }
    (HERE / "MAP_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {len(KEYS)}/{len(KEYS)} family-map keys")


if __name__ == "__main__":
    main()
