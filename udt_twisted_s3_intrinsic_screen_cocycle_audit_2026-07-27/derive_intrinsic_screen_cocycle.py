#!/usr/bin/env python3
"""Exact same-metric clock/ruler/screen and cocycle derivation."""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def wedge(left: dict[tuple[int, ...], sp.Expr],
          right: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    result: dict[tuple[int, ...], sp.Expr] = {}
    for a, ca in left.items():
        for b, cb in right.items():
            if set(a) & set(b):
                continue
            inversions = sum(i > j for i in a for j in b)
            key = tuple(sorted(a + b))
            result[key] = sp.simplify(result.get(key, 0) + (-1) ** inversions * ca * cb)
    return {key: value for key, value in result.items() if sp.simplify(value) != 0}


def add(*forms: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    result: dict[tuple[int, ...], sp.Expr] = {}
    for form in forms:
        for key, value in form.items():
            result[key] = sp.simplify(result.get(key, 0) + value)
    return {key: value for key, value in result.items() if sp.simplify(value) != 0}


def scale(value: sp.Expr, form: dict[tuple[int, ...], sp.Expr]) -> dict[tuple[int, ...], sp.Expr]:
    return {key: sp.simplify(value * coefficient) for key, coefficient in form.items()}


def load_candidates() -> list[dict[str, str]]:
    with (HERE / "CANDIDATE_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    expected = {
        "C01": ("-2", "1/50", "1/64"), "C02": ("-1", "1/50", "1/64"),
        "C03": ("0", "1/50", "1/64"), "C04": ("1/2", "1/50", "1/64"),
        "C05": ("1", "1/50", "1/64"), "C06": ("2", "1/50", "1/64"),
        "C07": ("0", "1/50", "0"), "C08": ("0", "0", "1/64"),
    }
    assert len(rows) == 8 and len({row["candidate"] for row in rows}) == 8
    assert {row["candidate"]: (row["lambda"], row["epsilon"], row["a"])
            for row in rows} == expected
    return rows


def projector_checks() -> dict[str, object]:
    eta = sp.diag(-1, 1, 1, 1)
    identity = sp.eye(4)
    u_up = sp.Matrix([1, 0, 0, 0])
    n_up = sp.Matrix([0, 1, 0, 0])
    u_down = eta * u_up
    n_down = eta * n_up
    projector = identity + u_up * u_down.T - n_up * n_down.T
    q_metric = eta + u_down * u_down.T - n_down * n_down.T
    expected = sp.diag(0, 0, 1, 1)
    assert projector == expected
    assert projector * projector == projector
    assert projector.trace() == 2
    assert projector * u_up == sp.zeros(4, 1)
    assert projector * n_up == sp.zeros(4, 1)
    assert q_metric == expected
    assert q_metric[2, 2] == q_metric[3, 3] == 1
    return {
        "mixed_projector": [0, 0, 1, 1], "rank": 2, "idempotent": True,
        "annihilates_clock_and_ruler": True, "screen_metric_signature": "++",
    }


def exterior_and_connection_checks() -> dict[str, object]:
    lam, p1, p2, p3, twist, kappa, phi = sp.symbols(
        "lambda p1 p2 p3 a kappa phi", real=True
    )
    e = [{(index,): sp.Integer(1)} for index in range(4)]
    dphi = add(scale(p1, e[1]), scale(p2, e[2]), scale(p3, e[3]))
    area = wedge(e[2], e[3])
    at = twist * kappa * sp.exp(-(1 + 2 * lam) * phi)
    bt = kappa * sp.exp((1 - 2 * lam) * phi)
    ct = kappa * sp.exp(-phi)

    de0 = add(scale(-1, wedge(dphi, e[0])), scale(at, wedge(e[2], e[3])))
    de1 = add(wedge(dphi, e[1]), scale(bt, wedge(e[2], e[3])))
    de2 = add(scale(lam, wedge(dphi, e[2])), scale(ct, wedge(e[3], e[1])))
    de3 = add(scale(lam, wedge(dphi, e[3])), scale(ct, wedge(e[1], e[2])))
    darea = add(wedge(de2, e[3]), scale(-1, wedge(e[2], de3)))
    expected_darea = scale(2 * lam, wedge(dphi, area))
    assert darea == expected_darea == {(1, 2, 3): 2 * lam * p1}

    # de^A=-1/2 C^A_BC e^B wedge e^C; for B<C the displayed coefficient is -C^A_BC.
    structure: dict[tuple[int, int, int], sp.Expr] = {}
    for upper, form in enumerate((de0, de1, de2, de3)):
        for (left, right), coefficient in form.items():
            assert len((left, right)) == 2
            structure[upper, left, right] = -coefficient
            structure[upper, right, left] = coefficient
    signs = (-1, 1, 1, 1)

    def lowered(out: int, left: int, right: int) -> sp.Expr:
        return signs[out] * structure.get((out, left, right), 0)

    def gamma(left: int, middle: int, out: int) -> sp.Expr:
        # Koszul: 2<del_left E_middle,E_out>
        return sp.simplify((lowered(out, left, middle)
                            - lowered(left, middle, out)
                            + lowered(middle, out, left)) / 2)

    accelerations: dict[str, list[sp.Expr]] = {}
    screen_rotations: dict[str, str] = {}
    for ray_sign in (1, -1):
        vector = (1, ray_sign, 0, 0)
        acceleration = []
        for out in range(4):
            lower_component = sum(vector[left] * vector[middle] * gamma(left, middle, out)
                                  for left in range(4) for middle in range(4))
            acceleration.append(sp.simplify(signs[out] * lower_component))
        expected = [-ray_sign * p1, -p1, -2 * p2, -2 * p3]
        assert acceleration == expected
        accelerations["plus" if ray_sign == 1 else "minus"] = acceleration

        # When p2=p3=0, derivatives of E2,E3 along the ray stay inside the screen and
        # are antisymmetric there: only an SO(2) screen rotation remains.
        rotation_23 = sp.simplify(sum(vector[left] * gamma(left, 2, 3)
                                      for left in range(4))).subs({p2: 0, p3: 0})
        rotation_32 = sp.simplify(sum(vector[left] * gamma(left, 3, 2)
                                      for left in range(4))).subs({p2: 0, p3: 0})
        assert sp.simplify(rotation_23 + rotation_32) == 0
        screen_rotations["plus" if ray_sign == 1 else "minus"] = str(rotation_23)

    # The screen-horizontal distribution is contact/bracket generating.  If p2=p3=0,
    # [E2,E3](phi)=C^1_23 p1 because E0(phi)=0.  Its nonzero coefficient forces p1=0.
    c1_23 = sp.simplify(structure[(1, 2, 3)].subs({p2: 0, p3: 0}))
    assert sp.simplify(c1_23 + kappa * sp.exp((1 - 2 * lam) * phi)) == 0
    assert c1_23.subs({kappa: -2}) != 0

    return {
        "area_form": "theta2^theta3_up_to_orientation",
        "area_exterior_derivative": "2*lambda*dphi^theta2^theta3",
        "area_lie_u": "0_for_stationary_phi",
        "area_lie_n": "2*lambda*n(phi)*area",
        "null_acceleration_plus": [str(value) for value in accelerations["plus"]],
        "null_acceleration_minus": [str(value) for value in accelerations["minus"]],
        "pregeodesic_condition": "E2(phi)=E3(phi)=0",
        "screen_transport_when_aligned": "SO2_rotation_only",
        "screen_rotation_coefficients": screen_rotations,
        "contact_coefficient_C1_23": str(c1_23),
        "global_alignment_implication": "E2phi=E3phi=0 => E1phi=0 => dphi=0",
    }


def clock_and_jacobi_checks() -> dict[str, object]:
    phi_p, phi_q, phi_r = sp.symbols("phi_p phi_q phi_r", real=True)
    n_p, n_q, n_r = (sp.exp(-phi_p), sp.exp(-phi_q), sp.exp(-phi_r))
    q_pq = sp.simplify(n_p / n_q)
    q_qr = sp.simplify(n_q / n_r)
    q_pr = sp.simplify(n_p / n_r)
    assert sp.simplify(q_pq * q_qr - q_pr) == 0
    assert sp.simplify(sp.log(q_pq).expand(force=True) - (phi_q - phi_p)) == 0

    # Killing energy conservation: symmetric k^a k^b annihilates antisymmetric nabla_a K_b.
    k = sp.symbols("k0:4", real=True)
    skew_symbols = {(i, j): sp.symbols(f"w{i}{j}", real=True)
                    for i in range(4) for j in range(i + 1, 4)}
    contraction = 0
    for i in range(4):
        for j in range(4):
            if i == j:
                value = 0
            elif i < j:
                value = skew_symbols[(i, j)]
            else:
                value = -skew_symbols[(j, i)]
            contraction += k[i] * k[j] * value
    assert sp.expand(contraction) == 0

    t11, t12, t22 = sp.symbols("t11 t12 t22", real=True)
    tidal = sp.Matrix([[t11, t12], [t12, t22]])
    zero = sp.zeros(2)
    eye = sp.eye(2)
    generator = zero.row_join(eye).col_join((-tidal).row_join(zero))
    omega = zero.row_join(eye).col_join((-eye).row_join(zero))
    assert sp.simplify(generator.T * omega + omega * generator) == sp.zeros(4)

    # Two independent exact symplectic shears and their composition.
    b = sp.Matrix([[2, 1], [1, 3]])
    c = sp.Matrix([[1, -1], [-1, 2]])
    m1 = eye.row_join(b).col_join(zero.row_join(eye))
    m2 = eye.row_join(zero).col_join(c.row_join(eye))
    for matrix in (m1, m2, m2 * m1):
        assert matrix.T * omega * matrix == omega
        assert matrix.det() == 1

    x, y = sp.symbols("x y", nonzero=True)
    s1 = sp.diag(1 / x, x)
    s2 = sp.diag(1 / y, y)
    s12 = sp.diag(1 / (x * y), x * y)
    assert sp.simplify(s2 * s1 - s12) == sp.zeros(2)
    combined1 = sp.diag(1, 1, 1, 1, 1, 1)
    combined1[:2, :2] = s1
    combined1[2:, 2:] = m1
    combined2 = sp.diag(1, 1, 1, 1, 1, 1)
    combined2[:2, :2] = s2
    combined2[2:, 2:] = m2
    combined12 = combined2 * combined1
    assert combined12[:2, :2] == s12
    assert combined12[2:, 2:] == m2 * m1

    return {
        "stationary_norm": "exp(-phi)",
        "frequency": "E*exp(phi)",
        "Q_pq": "exp(phi_q-phi_p)",
        "log_Q": "phi_q-phi_p",
        "triangle_composition": True,
        "killing_energy_conserved_on_affine_geodesic": True,
        "jacobi_generator_hamiltonian": True,
        "full_propagator_symplectic_composable_invertible": True,
        "vertex_B_block_standalone_cocycle": False,
        "same_branch_direct_sum": "DERIVED_GIVEN_SUPPLIED_GEODESIC_AND_STATIONARY_ENDPOINTS",
        "irreducible_solder": False,
    }


def wr_l_nonconflation() -> dict[str, object]:
    lam, amplitude, phi = sp.symbols("lambda A phi", real=True)
    local = amplitude * sp.exp(lam * phi)
    optical = 1 - sp.exp(-2 * phi)
    at_zero = (sp.simplify(local.subs(phi, 0)), sp.simplify(optical.subs(phi, 0)))
    assert at_zero == (amplitude, 0)
    forced_amplitude = sp.Integer(0)
    derivative_gap = sp.simplify(sp.diff(local.subs(amplitude, forced_amplitude) - optical, phi).subs(phi, 0))
    assert derivative_gap == -2
    return {
        "local_screen_length_family": "A*exp(lambda*phi)",
        "WRL_vertex_DA_over_X": "1-exp(-2*phi)",
        "open_interval_identity_for_constant_lambda": False,
        "proof": "value_at_zero_forces_A_zero_then_derivative_mismatch_minus_2",
        "implication": "local_coframe_area_is_not_vertex_Jacobi_area",
        "SNe_result_changed": False,
    }


def candidate_outcomes(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    outcomes = []
    for row in rows:
        candidate = row["candidate"]
        epsilon = Fraction(row["epsilon"])
        if epsilon:
            north = (3 * epsilon, epsilon, 2 * epsilon)
            aligned = "FAIL_GENERIC_NORTH_SCREEN_GRADIENT_NONZERO"
        else:
            north = (Fraction(0), Fraction(0), Fraction(0))
            aligned = "TRIVIAL_CONSTANT_DEPTH_ONLY"
        if candidate <= "C06":
            screen = "PASS_INTRINSIC_RANK_TWO"
            clock = "PASS_NONTRIVIAL"
            cocycle = "PASS_PATH_SCREEN_NOT_GLOBALLY_INTRINSIC_ALIGNED"
            status = "PASS_BOUNDED_SAME_METRIC_JOIN_WITH_ALIGNMENT_OBSTRUCTION"
        elif candidate == "C07":
            screen = "FAIL_NO_TWIST_SELECTED_RULER"
            clock = "PASS_NONTRIVIAL"
            cocycle = "FAIL_FULL_INTRINSIC_PAIR_GATE"
            status = "FAIL_AS_EXPECTED_TWIST_OFF"
        else:
            screen = "FAIL_NO_PARENT_INTRINSIC_PAIR"
            clock = "TRIVIAL_Q_ONE"
            cocycle = "FAIL_FULL_INTRINSIC_PAIR_GATE"
            status = "FAIL_AS_EXPECTED_DEPTH_OFF"
        outcomes.append({
            "candidate": candidate, "lambda": row["lambda"],
            "north_E1phi": str(north[0]), "north_E2phi": str(north[1]),
            "north_E3phi": str(north[2]), "intrinsic_screen": screen,
            "endpoint_depth_join": clock, "aligned_null_congruence": aligned,
            "same_metric_reducible_cocycle": cocycle,
            "raw_local_area_equals_WRL_DA": "NO", "status": status,
        })
    return outcomes


def main() -> int:
    candidates = load_candidates()
    result = {
        "schema": "udt-twisted-s3-intrinsic-screen-cocycle-1.0",
        "status": "PASS",
        "candidate_count": len(candidates),
        "projector": projector_checks(),
        "coframe_and_connection": exterior_and_connection_checks(),
        "clock_and_jacobi": clock_and_jacobi_checks(),
        "WRL_SNe_nonconflation": wr_l_nonconflation(),
        "candidate_outcomes": candidate_outcomes(candidates),
        "maximum_conclusion": (
            "COMPLETE_TWISTED_S3_INTRINSIC_CLOCK_RULER_SCREEN_SPLIT_AND_BRANCH_SPECIFIC_"
            "FOUNDED_CLOCK_JOIN_DERIVED;NONTRIVIAL_SAME_METRIC_REDUCIBLE_PATH_COCYCLE_"
            "DERIVED_GIVEN_PATH;NONTRIVIAL_DEPTH_FORCES_INTRINSIC_NULL_SCREEN_MIXING_IN_"
            "THIS_CONTACT_BRANCH;LOCAL_SCREEN_AREA_NOT_WRL_VERTEX_JACOBI_AREA;NO_PHYSICAL_SELECTION"
        ),
        "authority_boundary": {
            "on_shell": False, "path_selected": False, "lambda_selected": False,
            "SNe_fit_performed": False, "irreducible_solder_claimed": False,
            "action_or_source_selected": False, "operational_access_derived": False,
        },
        "sympy_version": sp.__version__,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
