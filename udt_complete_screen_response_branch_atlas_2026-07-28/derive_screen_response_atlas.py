#!/usr/bin/env python3
"""Exact bounded screen-response atlas for the frozen complete-branch universe."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def wedge(left: dict[tuple[int, ...], sp.Expr], right: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    result: dict[tuple[int, ...], sp.Expr] = {}
    for a, ca in left.items():
        for b, cb in right.items():
            if set(a) & set(b):
                continue
            inversions = sum(i > j for i in a for j in b)
            key = tuple(sorted(a + b))
            result[key] = sp.simplify(result.get(key, 0) + (-1) ** inversions * ca * cb)
    return {k: v for k, v in result.items() if sp.simplify(v) != 0}


def add(*forms: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    result: dict[tuple[int, ...], sp.Expr] = {}
    for form in forms:
        for key, value in form.items():
            result[key] = sp.simplify(result.get(key, 0) + value)
    return {k: v for k, v in result.items() if sp.simplify(v) != 0}


def scale(value: sp.Expr, form: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    return {key: sp.simplify(value * coefficient) for key, coefficient in form.items()}


def decompose(matrix: sp.Matrix) -> dict[str, sp.Expr]:
    return {
        "a": sp.simplify((matrix[0, 0] + matrix[1, 1]) / 2),
        "w": sp.simplify((matrix[1, 0] - matrix[0, 1]) / 2),
        "s1": sp.simplify((matrix[0, 0] - matrix[1, 1]) / 2),
        "s2": sp.simplify((matrix[0, 1] + matrix[1, 0]) / 2),
    }


def twisted_cartan() -> dict[str, object]:
    lam, p1, p2, p3, shift, kappa, phi = sp.symbols("lambda p1 p2 p3 alpha kappa phi", real=True)
    basis = [{(i,): sp.Integer(1)} for i in range(4)]
    dphi = add(scale(p1, basis[1]), scale(p2, basis[2]), scale(p3, basis[3]))
    at = shift * kappa * sp.exp(-(1 + 2 * lam) * phi)
    bt = kappa * sp.exp((1 - 2 * lam) * phi)
    ct = kappa * sp.exp(-phi)
    de = (
        add(scale(-1, wedge(dphi, basis[0])), scale(at, wedge(basis[2], basis[3]))),
        add(wedge(dphi, basis[1]), scale(bt, wedge(basis[2], basis[3]))),
        add(scale(lam, wedge(dphi, basis[2])), scale(ct, wedge(basis[3], basis[1]))),
        add(scale(lam, wedge(dphi, basis[3])), scale(ct, wedge(basis[1], basis[2]))),
    )
    structure: dict[tuple[int, int, int], sp.Expr] = {}
    for upper, form in enumerate(de):
        for (left, right), coefficient in form.items():
            structure[upper, left, right] = -coefficient
            structure[upper, right, left] = coefficient
    signs = (-1, 1, 1, 1)

    def lower(out: int, left: int, right: int) -> sp.Expr:
        return signs[out] * structure.get((out, left, right), 0)

    def gamma(left: int, middle: int, out: int) -> sp.Expr:
        return sp.simplify((lower(out, left, middle) - lower(left, middle, out) + lower(middle, out, left)) / 2)

    response: dict[str, object] = {}
    omegas: dict[str, sp.Expr] = {}
    for label, sign in (("plus", 1), ("minus", -1)):
        kvec = (1, sign, 0, 0)
        # Congruence screen derivative B_ij=<nabla_{E_j} k,E_i>.
        bmat = sp.Matrix(2, 2, lambda ii, jj: sp.simplify(sum(kvec[m] * gamma(jj + 2, m, ii + 2) for m in range(4))))
        # Coframe connection along k: A_ij=<nabla_k E_j,E_i>.
        amat = sp.Matrix(2, 2, lambda ii, jj: sp.simplify(sum(kvec[left] * gamma(left, jj + 2, ii + 2) for left in range(4))))
        acceleration = [sp.simplify(signs[out] * sum(kvec[l] * kvec[m] * gamma(l, m, out) for l in range(4) for m in range(4))) for out in range(4)]
        bdec = decompose(bmat)
        adec = decompose(amat)
        assert sp.simplify(adec["a"]) == sp.simplify(adec["s1"]) == sp.simplify(adec["s2"]) == 0
        assert sp.simplify(bdec["s1"]) == sp.simplify(bdec["s2"]) == 0
        assert sp.simplify(bdec["a"] - sign * lam * p1) == 0
        assert acceleration == [-sign * p1, -p1, -2 * p2, -2 * p3]
        omegas[label] = adec["w"]
        response[label] = {
            "congruence_matrix": [[str(sp.simplify(v)) for v in bmat.row(i)] for i in range(2)],
            "congruence_decomposition": {k: str(v) for k, v in bdec.items()},
            "path_connection_matrix": [[str(sp.simplify(v)) for v in amat.row(i)] for i in range(2)],
            "path_connection_decomposition": {k: str(v) for k, v in adec.items()},
            "acceleration": [str(v) for v in acceleration],
        }

    omega_plus = omegas["plus"]
    omega_minus = omegas["minus"]
    omega_u = sp.simplify((omega_plus + omega_minus) / 2)
    omega_n = sp.simplify((omega_plus - omega_minus) / 2)
    expected_u = sp.simplify(-shift * kappa * sp.exp(-(1 + 2 * lam) * phi) / 2)
    expected_n = sp.simplify(kappa * (sp.exp(2 * phi) - 2 * sp.exp(2 * lam * phi)) * sp.exp(-(1 + 2 * lam) * phi) / 2)
    assert sp.simplify(omega_u - expected_u) == 0
    assert sp.simplify(omega_n - expected_n) == 0
    return {
        "symbols": {"lambda": lam, "p1": p1, "p2": p2, "p3": p3, "alpha": shift, "kappa": kappa, "phi": phi},
        "ray_response": response,
        "omega_u": omega_u,
        "omega_n": omega_n,
        "omega_plus": omega_plus,
        "omega_minus": omega_minus,
    }


def homogeneous_cartan() -> dict[str, sp.Expr]:
    p, q = sp.symbols("p q", positive=True)
    A = p - q / 2
    return {"p": p, "q": q, "congruence_rotation": q / 2, "path_rotation": A}


def matrix_algebra() -> dict[str, object]:
    I = sp.eye(2)
    R = sp.Matrix([[0, -1], [1, 0]])
    S1 = sp.diag(1, -1)
    S2 = sp.Matrix([[0, 1], [1, 0]])
    bracket = lambda a, b: sp.simplify(a * b - b * a)
    assert bracket(R, S1) == 2 * S2
    assert bracket(R, S2) == -2 * S1
    assert bracket(S1, S2) == -2 * R
    assert all(bracket(I, x) == sp.zeros(2) for x in (R, S1, S2))
    return {"I": I, "R": R, "S1": S1, "S2": S2}


def closure_rows() -> list[dict[str, str]]:
    return [
        {"generator_set": "NONE", "pointwise_span_dim": "0", "generated_lie_dim": "0", "generated_algebra": "ZERO", "exact_reason": "empty"},
        {"generator_set": "I", "pointwise_span_dim": "1", "generated_lie_dim": "1", "generated_algebra": "R_I_ABELIAN", "exact_reason": "I_central"},
        {"generator_set": "R", "pointwise_span_dim": "1", "generated_lie_dim": "1", "generated_algebra": "so2_ABELIAN", "exact_reason": "single_generator"},
        {"generator_set": "I;R", "pointwise_span_dim": "2", "generated_lie_dim": "2", "generated_algebra": "R_I_DIRECT_SUM_so2_ABELIAN", "exact_reason": "[I,R]=0"},
        {"generator_set": "R;S1", "pointwise_span_dim": "2", "generated_lie_dim": "3", "generated_algebra": "sl2R", "exact_reason": "[R,S1]=2S2"},
        {"generator_set": "R;S2", "pointwise_span_dim": "2", "generated_lie_dim": "3", "generated_algebra": "sl2R", "exact_reason": "[R,S2]=-2S1"},
        {"generator_set": "S1;S2", "pointwise_span_dim": "2", "generated_lie_dim": "3", "generated_algebra": "sl2R", "exact_reason": "[S1,S2]=-2R"},
        {"generator_set": "I;R;S1", "pointwise_span_dim": "3", "generated_lie_dim": "4", "generated_algebra": "gl2R", "exact_reason": "I_central_plus_sl2R"},
        {"generator_set": "I;S1;S2", "pointwise_span_dim": "3", "generated_lie_dim": "4", "generated_algebra": "gl2R", "exact_reason": "I_central_plus_[S1,S2]"},
        {"generator_set": "I;R;S1;S2", "pointwise_span_dim": "4", "generated_lie_dim": "4", "generated_algebra": "gl2R", "exact_reason": "complete_End_screen"},
        {"generator_set": "PAIR_SCREEN_MIXING", "pointwise_span_dim": "OUTSIDE_EndS", "generated_lie_dim": "NOT_EVALUATED", "generated_algebra": "SCREEN_BLOCK_NOT_CLOSED", "exact_reason": "off_diagonal_pair_screen_blocks_present"},
    ]


def response_row(record_id: str, parent: str, completion: str, metric_status: str, path_class: str,
                 path_scope: str, screen: str, basis: str, a: str, w: str, s1: str, s2: str,
                 mixing: str, owner: str, algebra: str, degeneracy: str, holonomy: str,
                 ruling: str, source: str) -> dict[str, str]:
    return locals()


def build_branch_rows(twisted: dict[str, object], homogeneous: dict[str, sp.Expr]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    # Completion classes are retained as possibilities but do not silently acquire a metric.
    for fc in read_tsv("COMPLETION_CLASS_UNIVERSE.tsv"):
        cid = fc["completion_id"]
        rows.append(response_row(
            f"{cid}:UNSUPPLIED", cid, cid, "COMPLETION_TAXONOMY_ONLY", "UNSUPPLIED",
            "NO_METRIC_OR_PATH", "UNDEFINED", "UNDEFINED", "UNDEFINED", "UNDEFINED", "UNDEFINED", "UNDEFINED",
            "UNDEFINED", "NONE", "NONE", "CLASS_DEPENDENT", "OPEN_NO_METRIC_HOLONOMY",
            "BLOCKED_NO_ACTUAL_METRIC_REPRESENTATIVE", fc["source_path"],
        ))

    # Homogeneous Q controls.  Keep congruence vorticity and path-frame rotation separate.
    q = str(homogeneous["q"])
    A = str(homogeneous["path_rotation"])
    for rid, status, line, selected in (
        ("Q01_ROUND_S3_B19", "CONDITIONAL_COMPLETE_ON_SHELL_C2_CONTROL", "CHOSEN_HOPF_LINE", "NO_ROUND_ISOTROPY"),
        ("Q02_SQUASHED_S3_OFF_SHELL", "COMPLETE_OFF_SHELL_CONTROL", "METRIC_SELECTED_UNORIENTED_RICCI_LINE", "UNORIENTED_ONLY"),
    ):
        basis = f"CONDITIONAL_ORIENTED_SCREEN;LINE={line};SELECTION={selected}"
        src = "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/EXACT_DERIVATION.md"
        rows.extend([
            response_row(f"{rid}:CLOCK_U", rid, "FC04_TWO_CAP_P1", status, "CLOCK_U", "GLOBAL_HOMOGENEOUS", "POSITIVE_RANK2_CONDITIONAL_PAIR", basis, "0", "0", "0", "0", "0", "CONGRUENCE_PLUS_CONNECTION", "ZERO", "NONE", "FULL_SPATIAL_HOLONOMY_so3_NOT_SCREEN_REDUCED", "EXACT_CONDITIONAL_ZERO_RESPONSE", src),
            response_row(f"{rid}:RULER_CONGRUENCE", rid, "FC04_TWO_CAP_P1", status, "RULER_CONGRUENCE", "GLOBAL_HOMOGENEOUS", "POSITIVE_RANK2_CONDITIONAL_PAIR", basis, "0", f"{q}/2", "0", "0", "0", "CONGRUENCE_VORTICITY", "so2", "NONE", "DISPLAYED_R_DEPENDS_ON_ORIENTATION", "EXACT_PURE_TWIST_CONDITIONAL_PAIR", src),
            response_row(f"{rid}:HOPF_PATH", rid, "FC04_TWO_CAP_P1", status, "HOPF_PATH_FRAME_CONNECTION", "GLOBAL_CLOSED_HOPF_PATHS", "POSITIVE_RANK2_CONDITIONAL_PAIR", basis, "0", A, "0", "0", "0", "COFRAME_CONNECTION", "so2", "NONE", "CLOSED_PATH_HOLONOMY_REQUIRES_PERIOD_NORMALIZATION", "EXACT_LOCAL_CONNECTION_COEFFICIENT", src),
            response_row(f"{rid}:NULL_PLUS", rid, "FC04_TWO_CAP_P1", status, "U_PLUS_N", "GLOBAL_CONDITIONAL_NULL_PATH", "POSITIVE_RANK2_CONDITIONAL_PAIR", basis, "0", A, "0", "0", "0", "COFRAME_CONNECTION", "so2", "NONE", "PATHWISE_ROTATION_GAUGE_DEPENDENT", "EXACT_PURE_ROTATION_CONDITIONAL_PAIR", src),
            response_row(f"{rid}:NULL_MINUS", rid, "FC04_TWO_CAP_P1", status, "U_MINUS_N", "GLOBAL_CONDITIONAL_NULL_PATH", "POSITIVE_RANK2_CONDITIONAL_PAIR", basis, "0", f"-({A})", "0", "0", "0", "COFRAME_CONNECTION", "so2", "NONE", "PATHWISE_ROTATION_GAUGE_DEPENDENT", "EXACT_PURE_ROTATION_CONDITIONAL_PAIR", src),
            response_row(f"{rid}:ARBITRARY_GEODESIC", rid, "FC04_TWO_CAP_P1", status, "ARBITRARY_GEODESIC_JACOBI", "PATH_AND_INITIAL_DATA_UNSUPPLIED", "POSITIVE_RANK2_WHERE_PATH_SCREEN_SUPPLIED", "PATH_SCREEN_UNSUPPLIED", "UNDETERMINED", "GAUGE_DEPENDENT", "UNDETERMINED", "UNDETERMINED", "UNDETERMINED", "OPTICAL_JACOBI_NOT_LOCAL_COFRAME", "UNDETERMINED", "CAUSTICS_RETAINED", "FULL_SPATIAL_HOLONOMY_so3", "BLOCKED_MISSING_PATH_AND_JACOBI_DATA", src),
        ])

    # Incomplete and absent Q rows stay visible.
    rows.append(response_row("Q03_WRL_LOCAL:LOCAL_RADIAL", "Q03_WRL_LOCAL", "NONE", "LOCAL_STATIC_SPHERICAL_INCOMPLETE", "LOCAL_RADIAL", "LOCAL_ONLY", "LOCAL_SCREEN_ONLY", "CENTER_DEPENDENT", "UNDETERMINED", "UNDETERMINED", "UNDETERMINED", "UNDETERMINED", "UNDETERMINED", "NONE", "UNDETERMINED", "GLOBAL_COMPLETION_ABSENT", "NONE", "BLOCKED_COMPLETE_BRANCH_GATE", "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/CONCRETE_REPRESENTATIVE_ATLAS.tsv"))
    rows.append(response_row("Q04_PHYSICAL_XMAX_JOIN:NONE", "Q04_PHYSICAL_XMAX_JOIN", "NONE", "ABSENT", "NONE", "NONE", "UNDEFINED", "UNDEFINED", "UNDEFINED", "UNDEFINED", "UNDEFINED", "UNDEFINED", "UNDEFINED", "NONE", "NONE", "ABSENT", "NONE", "BLOCKED_ABSENT_CONFIGURATION", "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/CONCRETE_REPRESENTATIVE_ATLAS.tsv"))

    # The complete shifted reciprocal S3 family.
    sym = twisted["symbols"]
    p1, p2, p3, lam = (sym["p1"], sym["p2"], sym["p3"], sym["lambda"])
    op = {key: str(sp.simplify(twisted[key])) for key in ("omega_u", "omega_n", "omega_plus", "omega_minus")}
    wsrc = "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/EXACT_DERIVATION.md"
    wbasis = "INTRINSIC_UNORIENTED_SCREEN;DISPLAYED_BASIS_AND_ORIENTATION_CONDITIONAL"
    rows.extend([
        response_row("W01:DEPTH_PARAMETER", "W01_TWISTED_RECIPROCAL_S3", "FC04_TWO_CAP_P1", "COMPLETE_CONFIGURATION_EXISTENCE_NOT_ON_SHELL", "PHI_PARAMETER_RESPONSE", "POINTWISE_COMPLETE_COFRAME", "POSITIVE_RANK2_INTRINSIC", wbasis, str(lam), "0", "0", "0", "0", "SCREEN_METRIC_DEFORMATION", "R_I", "NONE", "NOT_A_PATH_HOLONOMY", "EXACT_EQUAL_WEIGHT_TRACE_ONLY", wsrc),
        response_row("W01:CLOCK_U", "W01_TWISTED_RECIPROCAL_S3", "FC04_TWO_CAP_P1", "COMPLETE_CONFIGURATION_EXISTENCE_NOT_ON_SHELL", "STATIONARY_CLOCK_U", "GLOBAL_STATIONARY", "POSITIVE_RANK2_INTRINSIC", wbasis, "0", op["omega_u"], "0", "0", "0", "COFRAME_CONNECTION", "so2", "NONE", "DISPLAYED_ROTATION_GAUGE_DEPENDENT", "EXACT_PURE_ROTATION", wsrc),
        response_row("W01:RULER_N", "W01_TWISTED_RECIPROCAL_S3", "FC04_TWO_CAP_P1", "COMPLETE_CONFIGURATION_EXISTENCE_NOT_ON_SHELL", "INTRINSIC_RULER_N", "LOCAL_VECTOR_FIELD_NOT_GLOBALLY_ALIGNED_NULL_RAY", "POSITIVE_RANK2_INTRINSIC", wbasis, str(lam*p1), op["omega_n"], "0", "0", "0", "CONGRUENCE_PLUS_CONNECTION", "R_I_DIRECT_SUM_so2", "NONE", "DISPLAYED_ROTATION_GAUGE_DEPENDENT", "EXACT_TRACE_PLUS_ROTATION", wsrc),
        response_row("W01:NULL_PLUS_ALIGNED", "W01_TWISTED_RECIPROCAL_S3", "FC04_TWO_CAP_P1", "COMPLETE_CONFIGURATION_EXISTENCE_NOT_ON_SHELL", "U_PLUS_N_ALIGNED", "LOCAL_WHERE_p2=p3=0", "POSITIVE_RANK2_INTRINSIC", wbasis, str(lam*p1), op["omega_plus"], "0", "0", "0", "CONGRUENCE_PLUS_CONNECTION", "R_I_DIRECT_SUM_so2", "GLOBAL_ALIGNMENT_FORCES_dphi_ZERO", "DISPLAYED_ROTATION_GAUGE_DEPENDENT", "EXACT_LOCAL_TRACE_PLUS_ROTATION", wsrc),
        response_row("W01:NULL_MINUS_ALIGNED", "W01_TWISTED_RECIPROCAL_S3", "FC04_TWO_CAP_P1", "COMPLETE_CONFIGURATION_EXISTENCE_NOT_ON_SHELL", "U_MINUS_N_ALIGNED", "LOCAL_WHERE_p2=p3=0", "POSITIVE_RANK2_INTRINSIC", wbasis, str(-lam*p1), op["omega_minus"], "0", "0", "0", "CONGRUENCE_PLUS_CONNECTION", "R_I_DIRECT_SUM_so2", "GLOBAL_ALIGNMENT_FORCES_dphi_ZERO", "DISPLAYED_ROTATION_GAUGE_DEPENDENT", "EXACT_LOCAL_TRACE_PLUS_ROTATION", wsrc),
        response_row("W01:NULL_GENERIC", "W01_TWISTED_RECIPROCAL_S3", "FC04_TWO_CAP_P1", "COMPLETE_CONFIGURATION_EXISTENCE_NOT_ON_SHELL", "U_PLUS_OR_MINUS_N_GENERIC", "POINTWISE_RAW_NULL_DIRECTION_NOT_PREGEODESIC_IF_SCREEN_GRADIENT_NONZERO", "POSITIVE_RANK2_INTRINSIC", wbasis, "plus_or_minus_lambda*p1", "omega_plus_or_minus", "0", "0", "(-2*p2,-2*p3)", "CONGRUENCE_CONNECTION_AND_OFF_BLOCK_ACCELERATION", "SCREEN_BLOCK_NOT_CLOSED", "MIXING_ZERO_ONLY_IF_p2=p3=0", "NO_GLOBAL_ALIGNED_REDUCTION_FOR_NONCONSTANT_phi", "EXACT_PAIR_SCREEN_MIXING", wsrc),
        response_row("W01:ARBITRARY_GEODESIC", "W01_TWISTED_RECIPROCAL_S3", "FC04_TWO_CAP_P1", "COMPLETE_CONFIGURATION_EXISTENCE_NOT_ON_SHELL", "ARBITRARY_GEODESIC_JACOBI", "PATH_PROFILE_AND_INITIAL_DATA_UNSUPPLIED", "PATH_SCREEN_EXISTS_WHERE_REGULAR", "PATH_SCREEN_FRAME_CONDITIONAL", "UNDETERMINED", "GAUGE_DEPENDENT", "UNDETERMINED", "UNDETERMINED", "GENERIC_INTRINSIC_OPTICAL_SCREEN_MISMATCH", "OPTICAL_JACOBI_NOT_LOCAL_COFRAME", "UNDETERMINED", "CAUSTICS_RETAINED;PROPAGATOR_SYMPLECTIC", "PATH_HOLONOMY_UNCOMPUTED", "BLOCKED_EXPLICIT_NONHOMOGENEOUS_PATH_ATLAS", wsrc),
    ])

    # W02-W06 are controls/strata, not extra fully solved response families.
    control_rows = [
        ("W02", "STATIC_GENERIC_LAPSE_ROUND_S3", "COMPLETE_METRIC_NATIVE_STATIONARY_DEPTH_CONTROL", "NO_INTRINSIC_RULER_OR_TWO_SCREEN", "BLOCKED_SCREEN_SELECTION"),
        ("W03", "ULTRASTATIC_S3", "ULTRASTATIC_ZERO_DEPTH_CONTROL", "CONDITIONAL_CHOSEN_HOPF_SCREEN", "CONDITIONAL_HOMOGENEOUS_TRACE_ZERO"),
        ("W04", "MULTIPLE_KILLING_CONTROL", "LINE_NONUNIQUENESS_CONTROL", "NO_UNIQUE_CLOCK_LINE", "BLOCKED_PAIR_SELECTION"),
        ("W05", "CAUSAL_SLICE_BOUNDARY", "SLICE_STRATUM_BOUNDARY", "SCREEN_CAN_REMAIN_POSITIVE_BUT_SLICE_DEGENERATES", "RETAINED_DEGENERACY_NOT_COMPLETE_PATH"),
        ("W06", "TWIST_FREE_NONCONSTANT_CLOCK", "DEPTH_WITHOUT_TWIST_RULER_CONTROL", "NO_INTRINSIC_RULER_OR_TWO_SCREEN", "BLOCKED_SCREEN_SELECTION"),
    ]
    for wid, name, status, screen, ruling in control_rows:
        rows.append(response_row(f"{wid}:REGISTERED_CONTROL", f"{wid}_{name}", "FC04_TWO_CAP_P1", status, "REGISTERED_CONTROL_SCOPE", "NO_ADDITIONAL_PATH_SUPPLIED", screen, "UNSUPPLIED_OR_CONDITIONAL", "UNDETERMINED", "UNDETERMINED", "UNDETERMINED", "UNDETERMINED", "UNDETERMINED", "NONE", "UNDETERMINED", "CONTROL_SPECIFIC", "UNCOMPUTED", ruling, "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/WITNESS_UNIVERSE.tsv"))

    # Parameter samples are retained separately; they are children of W01, not eight new branches.
    for c in read_tsv("TWISTED_PARAMETER_STRATA.tsv"):
        cid = c["candidate"]
        lv = sp.Rational(c["lambda"])
        eps = sp.Rational(c["epsilon"])
        shift = sp.Rational(c["a"])
        if cid in {f"C{i:02d}" for i in range(1, 7)}:
            p1v, p2v, p3v = 3*eps, eps, 2*eps
            mix = f"({-2*p2v},{-2*p3v})"
            rows.append(response_row(f"{cid}:NORTH_GENERIC_NULL", cid, "FC04_TWO_CAP_P1", "PARAMETER_SAMPLE_OF_W01_NOT_ON_SHELL", "NORTH_EVENT_U_PLUS_N", "POINTWISE_NOT_PREGEODESIC", "POSITIVE_RANK2_INTRINSIC", wbasis, str(lv*p1v), "FORMULA_IN_W01_WITH_PARAMETERS", "0", "0", mix, "CONGRUENCE_CONNECTION_AND_OFF_BLOCK_ACCELERATION", "SCREEN_BLOCK_NOT_CLOSED", "p2_and_p3_nonzero", "NO_ALIGNED_GLOBAL_REDUCTION", "EXACT_SAMPLE_WITH_PAIR_SCREEN_MIXING", wsrc))
            rows.append(response_row(f"{cid}:DEPTH_PARAMETER", cid, "FC04_TWO_CAP_P1", "PARAMETER_SAMPLE_OF_W01_NOT_ON_SHELL", "PHI_PARAMETER_RESPONSE", "POINTWISE_COMPLETE_COFRAME", "POSITIVE_RANK2_INTRINSIC", wbasis, str(lv), "0", "0", "0", "0", "SCREEN_METRIC_DEFORMATION", "ZERO" if lv == 0 else "R_I", "NONE", "NOT_A_PATH_HOLONOMY", "EXACT_EQUAL_WEIGHT_TRACE_ONLY", wsrc))
        elif cid == "C07":
            rows.append(response_row("C07:TWIST_OFF", cid, "FC04_TWO_CAP_P1", "PARAMETER_CONTROL", "TWIST_OFF_CONTROL", "GLOBAL_CONTROL", "NO_INTRINSIC_RULER_SCREEN", "COFRAME_SLOTS_EXIST_NOT_INTRINSIC", "0", "0", "0", "0", "0", "COFRAME_PARAMETER_ONLY", "ZERO", "RULER_SELECTION_LOST", "NONE", "EXPECTED_BLOCK_FULL_PAIR", wsrc))
        else:
            rows.append(response_row("C08:DEPTH_OFF", cid, "FC04_TWO_CAP_P1", "PARAMETER_CONTROL", "CONSTANT_DEPTH_CONTROL", "GLOBAL_CONTROL", "NO_PARENT_INTRINSIC_PAIR", "COFRAME_SLOTS_EXIST_NOT_INTRINSIC", "0", "COFRAME_TWIST_MAY_REMAIN_BUT_PAIR_GATE_FAILS", "0", "0", "0", "CONTROL_ONLY", "UNDETERMINED", "DEPTH_ZERO", "NONE", "EXPECTED_BLOCK_FULL_PAIR", wsrc))
    return rows


def main() -> int:
    twisted = twisted_cartan()
    homogeneous = homogeneous_cartan()
    matrix_algebra()
    rows = build_branch_rows(twisted, homogeneous)
    ids = [r["record_id"] for r in rows]
    assert len(ids) == len(set(ids))
    fields = list(rows[0])
    write_tsv("BRANCH_PATH_RESPONSE_ATLAS.tsv", fields, rows)

    invariant_rows = [
        {"object": "trace_area", "formula": "tr(K)=2a", "frame_behavior": "O2_INVARIANT", "metric_status": "INTRINSIC_GIVEN_SCREEN_AND_DIRECTION"},
        {"object": "determinant", "formula": "det(K)=a^2+w^2-s1^2-s2^2", "frame_behavior": "O2_INVARIANT", "metric_status": "INTRINSIC_FOR_ENDOMORPHISM"},
        {"object": "shear_norm", "formula": "s1^2+s2^2", "frame_behavior": "O2_INVARIANT", "metric_status": "INTRINSIC_SELF_ADJOINT_TRACEFREE_NORM"},
        {"object": "rotation_magnitude", "formula": "w^2", "frame_behavior": "O2_INVARIANT_BUT_SIGN_NEEDS_ORIENTATION", "metric_status": "CONNECTION_PATH_AND_FRAME_REQUIRED"},
        {"object": "shear_components", "formula": "(s1,s2)", "frame_behavior": "ROTATE_BY_DOUBLE_SCREEN_ANGLE", "metric_status": "BASIS_DEPENDENT_COMPONENTS"},
        {"object": "mixing_norm", "formula": "4*(p2^2+p3^2)", "frame_behavior": "O2_INVARIANT", "metric_status": "INTRINSIC_WHEN_PAIR_AND_SCREEN_EXIST"},
        {"object": "screen_rank", "formula": "rank(H)=2", "frame_behavior": "INVARIANT", "metric_status": "ONLY_WHERE_POSITIVE_PAIR_OR_PATH_SCREEN_EXISTS"},
    ]
    write_tsv("INTRINSIC_INVARIANT_ATLAS.tsv", list(invariant_rows[0]), invariant_rows)

    gauge_rows = [
        {"component": "aI", "SO2_change": "unchanged", "O2_reflection": "unchanged", "ownership": "screen_metric_deformation"},
        {"component": "wR", "SO2_change": "coefficient_unchanged_for_oriented_rotation", "O2_reflection": "w_changes_sign", "ownership": "coframe_connection_not_metric_deformation"},
        {"component": "s1S1+s2S2", "SO2_change": "components_rotate_by_2theta", "O2_reflection": "components_reflect", "ownership": "tracefree_screen_metric_deformation"},
        {"component": "pair_screen_vector", "SO2_change": "vector_rotates_by_theta", "O2_reflection": "vector_reflects", "ownership": "off_diagonal_connection_block"},
    ]
    write_tsv("COFRAME_GAUGE_ATLAS.tsv", list(gauge_rows[0]), gauge_rows)

    ray = twisted["ray_response"]
    rotation_rows = [
        {"family_path": "Q01_Q02:RULER_CONGRUENCE", "congruence_vorticity": "q/2", "path_frame_connection": "NOT_THE_SAME_OBJECT", "path_minus_congruence": "N/A", "status": "EXACT_CONDITIONAL_PAIR"},
        {"family_path": "Q01_Q02:HOPF_PATH", "congruence_vorticity": "NOT_THE_SAME_OBJECT", "path_frame_connection": "p-q/2", "path_minus_congruence": "N/A", "status": "EXACT_CONDITIONAL_PAIR"},
        {"family_path": "W01:U_PLUS_N", "congruence_vorticity": ray["plus"]["congruence_decomposition"]["w"], "path_frame_connection": ray["plus"]["path_connection_decomposition"]["w"], "path_minus_congruence": "-kappa*exp(-phi)", "status": "EXACT_DISTINCT_ROTATION_OWNERS"},
        {"family_path": "W01:U_MINUS_N", "congruence_vorticity": ray["minus"]["congruence_decomposition"]["w"], "path_frame_connection": ray["minus"]["path_connection_decomposition"]["w"], "path_minus_congruence": "+kappa*exp(-phi)", "status": "EXACT_DISTINCT_ROTATION_OWNERS"},
        {"family_path": "ALL", "congruence_vorticity": "projected_nabla_of_ray_field", "path_frame_connection": "screen_basis_parallel_transport_along_path", "path_minus_congruence": "OBJECTS_NEED_NOT_AGREE", "status": "DO_NOT_CONFLATE"},
    ]
    write_tsv("ROTATION_OWNERSHIP_ATLAS.tsv", list(rotation_rows[0]), rotation_rows)
    closure = closure_rows()
    write_tsv("GENERATED_ALGEBRA_ATLAS.tsv", list(closure[0]), closure)

    frozen_rows = [
        {"registered_family": "Q01_Q02_HOMOGENEOUS", "frozen_or_missing_component": "a;s1;s2", "exact_reason": "homogeneity_and_ultrastatic_product_make_conditional_pair response pure twist", "allowed_conclusion": "ZERO_IN_THESE_CONTROLS_NOT_UNIVERSAL_NO_GO"},
        {"registered_family": "W01_EQUAL_SCREEN_WEIGHT", "frozen_or_missing_component": "s1;s2_IN_PHI_PARAMETER_RESPONSE", "exact_reason": "theta2_and_theta3_both_carry_exp(lambda*phi)", "allowed_conclusion": "EQUAL_WEIGHT_ANSATZ_TRACE_ONLY"},
        {"registered_family": "W01_GENERIC_PATH", "frozen_or_missing_component": "EXPLICIT_JACOBI_s1;s2", "exact_reason": "path_profile_and_initial_data_not_supplied", "allowed_conclusion": "OPEN_NOT_ZERO"},
        {"registered_family": "COUNTERFACTUAL_INDEPENDENT_WEIGHTS", "frozen_or_missing_component": "NONE_ALGEBRAIC_DIAGNOSTIC_ONLY", "exact_reason": "weights_lambda2_lambda3_give_a=(lambda2+lambda3)/2_and_s1=(lambda2-lambda3)/2", "allowed_conclusion": "SHOWS_EQUAL_WEIGHT_CHOICE_REMOVES_ONE_SHEAR_AXIS;NOT_A_NEW_BRANCH"},
        {"registered_family": "GENERAL_SCREEN_MATRIX", "frozen_or_missing_component": "second_shear_and_rotation", "exact_reason": "requires_general_GL2_screen_coframe_and_connection", "allowed_conclusion": "NOT_PRESENTLY_CONSTRUCTED_OR_SELECTED"},
    ]
    write_tsv("FROZEN_DOF_DIAGNOSTIC.tsv", list(frozen_rows[0]), frozen_rows)

    mixing_rows = [r for r in rows if r["mixing"] not in {"0", "NONE", "UNDEFINED", "UNDETERMINED"}]
    exact_mixing_rows = [r for r in mixing_rows if r["ruling"].startswith("EXACT")]
    write_tsv("PAIR_SCREEN_MIXING_ATLAS.tsv", fields, mixing_rows)
    degeneracy_rows = [r for r in rows if r["degeneracy"] not in {"NONE"}]
    write_tsv("DEGENERACY_ATLAS.tsv", fields, degeneracy_rows)

    holonomy_rows = [
        {"family": "FC01-FC12", "local_reduction": "UNDEFINED_WITHOUT_METRIC", "global_descent": "CLASS_DEPENDENT", "holonomy_status": "OPEN_TAXONOMY_ONLY", "maximum_claim": "NO_BRANCH_HOLONOMY"},
        {"family": "Q01_ROUND_S3_B19", "local_reduction": "CHOSEN_HOPF_PAIR_GIVES_SO2_SCREEN", "global_descent": "PAIR_FIELDS_EXIST_BUT_ROUND_METRIC_SELECTS_NONE", "holonomy_status": "FULL_SPATIAL_so3", "maximum_claim": "PATHWISE_SO2_NOT_GLOBAL_PARALLEL_SCREEN_REDUCTION"},
        {"family": "Q02_SQUASHED_S3_OFF_SHELL", "local_reduction": "UNORIENTED_RICCI_LINE_PLUS_CONDITIONAL_SCREEN_ORIENTATION", "global_descent": "UNORIENTED_LINE_GLOBAL", "holonomy_status": "FULL_SPATIAL_so3_IN_REGISTERED_CONTROL", "maximum_claim": "OFF_SHELL_PATHWISE_REDUCTION_ONLY"},
        {"family": "W01_TWISTED_RECIPROCAL_S3", "local_reduction": "INTRINSIC_PAIR_AND_RANK2_SCREEN", "global_descent": "PROJECTOR_GLOBAL_ON_REGULAR_COMPLETE_CONFIGURATION", "holonomy_status": "FULL_PATH_HOLONOMY_UNCOMPUTED", "maximum_claim": "NONCONSTANT_DEPTH_FORCES_PAIR_SCREEN_MIXING_SOMEWHERE"},
        {"family": "C01-C06", "local_reduction": "PARAMETER_SAMPLES_OF_W01", "global_descent": "SAME_AS_W01", "holonomy_status": "NORTH_EVENT_MIXING_CERTIFICATE_ONLY", "maximum_claim": "NO_GLOBAL_ALIGNED_NULL_REDUCTION"},
        {"family": "W02-W06;C07-C08", "local_reduction": "CONTROL_DEPENDENT_OR_PAIR_GATE_FAILS", "global_descent": "NOT_A_COMMON_REDUCTION", "holonomy_status": "UNCOMPUTED_OR_NOT_DEFINED", "maximum_claim": "CONTROLS_RETAINED_NO_SELECTION"},
        {"family": "ARBITRARY_GEODESIC_JACOBI", "local_reduction": "PATH_OPTICAL_SCREEN", "global_descent": "CAUSTIC_SAFE_ONLY_IN_FULL_SYMPLECTIC_PHASE_SPACE", "holonomy_status": "PATH_PROFILE_AND_INITIAL_DATA_REQUIRED", "maximum_claim": "GENERIC_SHEAR_OPEN_NOT_ZERO"},
    ]
    write_tsv("HOLONOMY_DESCENT_ATLAS.tsv", list(holonomy_rows[0]), holonomy_rows)

    component_rows = [
        {"component": "aI_TRACE", "realized_records": str(sum(r["a"] not in {"0", "UNDEFINED", "UNDETERMINED"} for r in rows)), "exact_zero_records": str(sum(r["a"] == "0" for r in rows)), "blocked_records": str(sum(r["a"] in {"UNDEFINED", "UNDETERMINED"} for r in rows)), "ruling": "REALIZED_IN_W01_AND_C_PARAMETER_RESPONSE_OR_CONGRUENCE"},
        {"component": "wR_ROTATION", "realized_records": str(sum(r["w"] not in {"0", "UNDEFINED", "UNDETERMINED", "GAUGE_DEPENDENT"} for r in rows)), "exact_zero_records": str(sum(r["w"] == "0" for r in rows)), "blocked_records": str(sum(r["w"] in {"UNDEFINED", "UNDETERMINED", "GAUGE_DEPENDENT"} for r in rows)), "ruling": "REALIZED_BUT_DISPLAYED_SIGN_OR_COEFFICIENT_NEEDS_FRAME_OR_PATH"},
        {"component": "s1_SHEAR", "realized_records": "0", "exact_zero_records": str(sum(r["s1"] == "0" for r in rows)), "blocked_records": str(sum(r["s1"] in {"UNDEFINED", "UNDETERMINED"} for r in rows)), "ruling": "ZERO_IN_EVALUATED_REGISTERED_RESPONSES;GENERIC_JACOBI_OPEN"},
        {"component": "s2_SHEAR", "realized_records": "0", "exact_zero_records": str(sum(r["s2"] == "0" for r in rows)), "blocked_records": str(sum(r["s2"] in {"UNDEFINED", "UNDETERMINED"} for r in rows)), "ruling": "ZERO_IN_EVALUATED_REGISTERED_RESPONSES;GENERAL_SCREEN_MATRIX_UNCONSTRUCTED"},
        {"component": "PAIR_SCREEN_MIXING", "realized_records": str(len(exact_mixing_rows)), "exact_zero_records": str(sum(r["mixing"] == "0" for r in rows)), "blocked_records": str(len(rows)-len(exact_mixing_rows)-sum(r["mixing"] == "0" for r in rows)), "ruling": "SEVEN_EXACT_MIXING_ROWS_PLUS_ONE_GENERIC_PATH_MISMATCH_DISCLOSURE"},
    ]
    write_tsv("SCREEN_COMPONENT_COVERAGE.tsv", list(component_rows[0]), component_rows)

    intersection_rows = [
        {"scope": "ALL_52_ROWS", "intersection": "UNDEFINED", "reason": "contains taxonomy-only, absent, incomplete, and blocked rows", "allowed_claim": "NO_NONZERO_COMMON_SUBALGEBRA"},
        {"scope": "ALL_EVALUATED_POINTWISE_RESPONSES", "intersection": "ZERO", "reason": "explicit zero-response rows are included", "allowed_claim": "TRIVIAL_INTERSECTION_ONLY"},
        {"scope": "UNION_OF_EVALUATED_EndS_COMPONENTS", "intersection": "NOT_AN_INTERSECTION", "reason": "nonzero union spans I and R only in current explicit records", "allowed_claim": "OBSERVED_BOUNDED_VOCABULARY_NOT_SELECTION"},
        {"scope": "GENERIC_SCREEN_ALGEBRA", "intersection": "EndS_EQUALS_gl2R", "reason": "mathematical ambient space includes I,R,S1,S2", "allowed_claim": "AMBIENT_IDENTITY_NOT_BRANCH_REALIZATION"},
    ]
    write_tsv("COMMON_INTERSECTION_AUDIT.tsv", list(intersection_rows[0]), intersection_rows)

    parent_counts: dict[str, int] = {}
    for row in rows:
        parent_counts[row["parent"]] = parent_counts.get(row["parent"], 0) + 1
    coverage_summary = [
        {"parent": parent, "response_rows": str(count), "coverage": "EXACTLY_ONCE_PER_REGISTERED_PATH_RECORD", "selection_status": "NOT_SELECTED"}
        for parent, count in sorted(parent_counts.items())
    ]
    write_tsv("BRANCH_PATH_COVERAGE.tsv", list(coverage_summary[0]), coverage_summary)

    completeness = read_tsv("COMPLETENESS_PLAN.tsv")
    coverage_rows = []
    for row in completeness:
        coverage_rows.append({
            "criterion": row["criterion"],
            "audit_stamp": "COVERED_AS_REGISTERED_SCOPE" if row["criterion"] not in {"STABILITY_SPECTRUM"} else "EXPLICITLY_OPEN_NOT_TESTED",
            "evidence": row["covered_now"],
            "remaining_open": row["dropped_or_open"],
        })
    write_tsv("TEN_CRITERION_COVERAGE.tsv", list(coverage_rows[0]), coverage_rows)

    result = {
        "schema": "udt-complete-screen-response-atlas-1.0",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "branch_path_rows": len(rows),
        "unique_record_ids": len(set(ids)),
        "completion_taxonomy_rows": sum(r["metric_status"] == "COMPLETION_TAXONOMY_ONLY" for r in rows),
        "exact_or_conditional_response_rows": sum(r["ruling"].startswith(("EXACT", "CONDITIONAL")) for r in rows),
        "blocked_or_open_rows": sum(r["ruling"].startswith(("BLOCKED", "OPEN")) for r in rows),
        "pair_screen_mixing_rows": len(exact_mixing_rows),
        "mixing_or_mismatch_rows": len(mixing_rows),
        "degeneracy_rows": len(degeneracy_rows),
        "branch_parent_rows": len(parent_counts),
        "complete_screen_basis": "End(S)=R*I+so(2)+Sym0(2);dim=1+1+2=4",
        "observed_common_structure": "REGISTERED_EXPLICIT_RESPONSE_ROWS_USE_ONLY_TRACE_AND_ROTATION_INSIDE_EndS;PAIR_SCREEN_MIXING_OCCURS_ON_GENERIC_NONCONSTANT_TWISTED_DEPTH",
        "critical_caveat": "EXPLICIT_GENERIC_JACOBI_SHEAR_IS_OPEN_NOT_ZERO;CURRENT_EQUAL_WEIGHT_COFAME_FREEZES_SHEAR_ONLY_IN_THE_PHI_PARAMETER_RESPONSE",
        "outcome_class": "MIXED_MULTIPLE_OUTCOMES",
        "maximum_conclusion": "BOUNDED_REGISTERED_BRANCH_ATLAS_NO_PHYSICAL_SELECTION",
    }
    serializable_twisted = {
        k: (str(v) if isinstance(v, sp.Basic) else v)
        for k, v in twisted.items() if k != "symbols"
    }
    result["twisted_exact"] = serializable_twisted
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "twisted_exact"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
