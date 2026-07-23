#!/usr/bin/env python3
"""Exact metric-led coframe-to-Hopf bridge algebra."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE_MANIFEST = HERE / "SOURCE_MANIFEST.sha256"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def verify_sources() -> int:
    count = 0
    for line in SOURCE_MANIFEST.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        path = ROOT / relative
        if not path.is_file() or digest(path) != expected:
            raise AssertionError(f"source mismatch: {relative}")
        count += 1
    return count


def write_tsv(name: str, rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def coframe(a: sp.Matrix, d: sp.Matrix, s: sp.Matrix) -> sp.Matrix:
    zero = sp.zeros(2)
    return a.row_join(zero).col_join((d * s).row_join(d))


def exact_algebra() -> dict[str, object]:
    # Independent reconstruction of the complete triangular chart group.
    a1, c1, r1, t1, b1, e1 = sp.symbols(
        "a1 c1 r1 t1 b1 e1", nonzero=True
    )
    a2, c2, r2, t2, b2, e2 = sp.symbols(
        "a2 c2 r2 t2 b2 e2", nonzero=True
    )
    p11, p12, p21, p22 = sp.symbols("p11 p12 p21 p22")
    q11, q12, q21, q22 = sp.symbols("q11 q12 q21 q22")
    a_one = sp.Matrix([[a1, b1], [0, c1]])
    a_two = sp.Matrix([[a2, b2], [0, c2]])
    d_one = sp.Matrix([[r1, e1], [0, t1]])
    d_two = sp.Matrix([[r2, e2], [0, t2]])
    s_one = sp.Matrix([[p11, p12], [p21, p22]])
    s_two = sp.Matrix([[q11, q12], [q21, q22]])
    first = coframe(a_one, d_one, s_one)
    second = coframe(a_two, d_two, s_two)
    s_product = sp.simplify(d_two.inv() * s_one * a_two + s_two)
    predicted = coframe(a_one * a_two, d_one * d_two, s_product)
    product_residual = sp.simplify(first * second - predicted)
    inverse_s = sp.simplify(-d_one * s_one * a_one.inv())
    inverse_residual = sp.simplify(
        first.inv() - coframe(a_one.inv(), d_one.inv(), inverse_s)
    )
    if product_residual != sp.zeros(4) or inverse_residual != sp.zeros(4):
        raise AssertionError("complete chart-group reconstruction failed")

    # The base and angular positive upper-triangular blocks each carry an
    # additive scale-free diagonal character, regardless of their shear.
    sigma_a1, alpha1, sigma_a2, alpha2 = sp.symbols(
        "sigma_a1 alpha1 sigma_a2 alpha2", real=True
    )
    sigma_d1, phi1, sigma_d2, phi2 = sp.symbols(
        "sigma_d1 phi1 sigma_d2 phi2", real=True
    )
    h_a1, h_a2, h_d1, h_d2 = sp.symbols("h_a1 h_a2 h_d1 h_d2")
    abase_one = sp.Matrix(
        [[sp.exp(sigma_a1 - alpha1), h_a1], [0, sp.exp(sigma_a1 + alpha1)]]
    )
    abase_two = sp.Matrix(
        [[sp.exp(sigma_a2 - alpha2), h_a2], [0, sp.exp(sigma_a2 + alpha2)]]
    )
    dbase_one = sp.Matrix(
        [[sp.exp(sigma_d1 - phi1), h_d1], [0, sp.exp(sigma_d1 + phi1)]]
    )
    dbase_two = sp.Matrix(
        [[sp.exp(sigma_d2 - phi2), h_d2], [0, sp.exp(sigma_d2 + phi2)]]
    )
    a_product = abase_one * abase_two
    d_product = dbase_one * dbase_two
    expected_a_diagonal = (
        sp.exp(sigma_a1 + sigma_a2 - alpha1 - alpha2),
        sp.exp(sigma_a1 + sigma_a2 + alpha1 + alpha2),
    )
    expected_d_diagonal = (
        sp.exp(sigma_d1 + sigma_d2 - phi1 - phi2),
        sp.exp(sigma_d1 + sigma_d2 + phi1 + phi2),
    )
    if (
        sp.simplify(a_product[0, 0] - expected_a_diagonal[0]) != 0
        or sp.simplify(a_product[1, 1] - expected_a_diagonal[1]) != 0
        or sp.simplify(d_product[0, 0] - expected_d_diagonal[0]) != 0
        or sp.simplify(d_product[1, 1] - expected_d_diagonal[1]) != 0
    ):
        raise AssertionError("upper-triangular characters failed")

    # The Hopf-compatible reciprocal-diagonal angular family is a subgroup,
    # but not a normal/invariant part of the complete angular group.
    omega1, omega2 = sp.symbols("Omega1 Omega2", positive=True)

    def reciprocal_angular(omega: sp.Expr, depth: sp.Expr) -> sp.Matrix:
        return omega * sp.diag(sp.exp(-depth), sp.exp(depth))

    reciprocal_product = sp.simplify(
        reciprocal_angular(omega1, phi1)
        * reciprocal_angular(omega2, phi2)
        - reciprocal_angular(omega1 * omega2, phi1 + phi2)
    )
    reciprocal_inverse = sp.simplify(
        reciprocal_angular(omega1, phi1).inv()
        - reciprocal_angular(1 / omega1, -phi1)
    )
    if reciprocal_product != sp.zeros(2) or reciprocal_inverse != sp.zeros(2):
        raise AssertionError("reciprocal angular subgroup failed")
    shear = sp.symbols("shear", nonzero=True)
    unipotent = sp.Matrix([[1, shear], [0, 1]])
    reciprocal_unit = reciprocal_angular(1, phi1)
    conjugated = sp.simplify(unipotent * reciprocal_unit * unipotent.inv())
    conjugate_off_diagonal = sp.simplify(conjugated[0, 1])
    if conjugate_off_diagonal == 0:
        raise AssertionError("diagonal subgroup falsely appeared normal")

    # Induced conditional toric connection-weight and Hopf-latitude laws.
    f1, f2, f3 = sp.symbols("f1 f2 f3", positive=True)

    def f_compose(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        return sp.factor(
            left
            * right
            / (left * right + (1 - left) * (1 - right))
        )

    f_phi = sp.simplify(1 / (1 + sp.exp(4 * phi1)))
    f_phi_two = sp.simplify(1 / (1 + sp.exp(4 * phi2)))
    f_phi_sum = sp.simplify(1 / (1 + sp.exp(4 * (phi1 + phi2))))
    if sp.simplify(f_compose(f_phi, f_phi_two) - f_phi_sum) != 0:
        raise AssertionError("connection-weight composition failed")
    if sp.simplify(f_compose(f1, sp.Rational(1, 2)) - f1) != 0:
        raise AssertionError("connection-weight identity failed")
    if sp.simplify(f_compose(f1, 1 - f1) - sp.Rational(1, 2)) != 0:
        raise AssertionError("connection-weight inverse failed")
    associator = sp.factor(
        f_compose(f_compose(f1, f2), f3)
        - f_compose(f1, f_compose(f2, f3))
    )
    if associator != 0:
        raise AssertionError("connection-weight associativity failed")

    z1, z2 = sp.symbols("z1 z2", real=True)
    z_compose = sp.factor((z1 + z2) / (1 + z1 * z2))
    z_phi = -sp.tanh(2 * phi1)
    z_phi_two = -sp.tanh(2 * phi2)
    z_phi_sum = -sp.tanh(2 * (phi1 + phi2))
    if (
        sp.simplify(
            (z_phi + z_phi_two) / (1 + z_phi * z_phi_two) - z_phi_sum
        ).rewrite(sp.exp)
        != 0
    ):
        raise AssertionError("Hopf-latitude composition failed")
    rho_law_residual = sp.simplify(
        sp.sech(2 * (phi1 + phi2))
        - sp.sech(2 * phi1)
        * sp.sech(2 * phi2)
        / (1 + z_phi * z_phi_two)
    ).rewrite(sp.exp)
    if sp.simplify(rho_law_residual) != 0:
        raise AssertionError("Hopf transverse-amplitude composition failed")

    delta = sp.symbols("delta", real=True)
    quotient = sp.Matrix(
        [
            sp.sech(2 * phi1) * sp.cos(delta),
            sp.sech(2 * phi1) * sp.sin(delta),
            -sp.tanh(2 * phi1),
        ]
    )
    quotient_norm = sp.simplify((quotient.dot(quotient)).rewrite(sp.exp))
    eta = sp.diag(-1, 1, 1, 1)
    null_lift = sp.Matrix([1, quotient[0], quotient[1], quotient[2]])
    null_norm = sp.simplify((null_lift.T * eta * null_lift)[0].rewrite(sp.exp))
    conformal = sp.symbols("conformal", positive=True)
    conformal_null_norm = sp.simplify(
        (null_lift.T * (conformal**2 * eta) * null_lift)[0].rewrite(sp.exp)
    )
    if quotient_norm != 1 or null_norm != 0 or conformal_null_norm != 0:
        raise AssertionError("conditional Hopf/null-section lift failed")

    # The pointwise group law does not define a homomorphism on the
    # finite-endpoint Hopf readout. Two pairs with the same separate endpoint
    # differences give distinct composed differences.
    first_minus, first_plus = sp.Rational(3, 4), sp.Rational(1, 4)
    second_a_minus, second_a_plus = sp.Rational(3, 4), sp.Rational(1, 4)
    second_b_minus, second_b_plus = sp.Rational(2, 3), sp.Rational(1, 6)
    q_first = first_minus - first_plus
    q_second_a = second_a_minus - second_a_plus
    q_second_b = second_b_minus - second_b_plus
    q_composed_a = sp.factor(
        f_compose(first_minus, second_a_minus)
        - f_compose(first_plus, second_a_plus)
    )
    q_composed_b = sp.factor(
        f_compose(first_minus, second_b_minus)
        - f_compose(first_plus, second_b_plus)
    )
    if (
        q_first != sp.Rational(1, 2)
        or q_second_a != q_second_b
        or q_composed_a == q_composed_b
    ):
        raise AssertionError("finite-endpoint charge non-homomorphism catch failed")

    return {
        "complete_chart_group": {
            "product_residual": "ZERO_4X4",
            "inverse_residual": "ZERO_4X4",
            "zero_shift_subset_closed": True,
            "angular_factor_independent_of_base_and_shift": True,
        },
        "upper_triangular_characters": {
            "base_depth": "alpha12=alpha1+alpha2",
            "angular_depth": "phiD12=phiD1+phiD2",
            "base_scale": "sigmaA12=sigmaA1+sigmaA2",
            "angular_scale": "sigmaD12=sigmaD1+sigmaD2",
            "survive_shear": True,
            "physical_owner_selected": False,
            "scalar_phi_identification_selected": False,
        },
        "reciprocal_angular_subgroup": {
            "product": "D(Omega1,phi1)D(Omega2,phi2)=D(Omega1*Omega2,phi1+phi2)",
            "inverse": "D(Omega,phi)^-1=D(Omega^-1,-phi)",
            "common_scale_cancels_from_ratio": True,
            "diagonal_subset_is_subgroup": True,
            "diagonal_subset_is_normal_in_upper_triangular_group": False,
            "shear_conjugate_off_diagonal": str(conjugate_off_diagonal),
        },
        "conditional_toric_composition": {
            "weight": "f=1/(1+exp(4*phiD))",
            "weight_operation": "f1*f2/(f1*f2+(1-f1)*(1-f2))",
            "identity": "1/2",
            "inverse": "1-f",
            "associative": True,
            "latitude": "z=2*f-1=-tanh(2*phiD)",
            "latitude_operation": str(z_compose),
            "transverse_amplitude": "rho12=rho1*rho2/(1+z1*z2)",
            "phase_delta_composition": "NOT_PRESENT_IN_POINTWISE_COFRAME_GROUP",
            "scalar_dphi_rule": (
                "dphi12=dphi1+dphi2 ONLY_IF scalar phi is CHOSEN to equal "
                "the angular depth character"
            ),
        },
        "conditional_null_section": {
            "quotient_norm": str(quotient_norm),
            "null_lift_norm": str(null_norm),
            "csn_scaled_null_lift_norm": str(conformal_null_norm),
            "status": (
                "EXACT_AFTER_TORIC_PHI_DELTA_AND_A_COFRAME_REPRESENTATIVE_ARE_"
                "SUPPLIED"
            ),
        },
        "finite_endpoint_readout": {
            "q_first": str(q_first),
            "q_second_a": str(q_second_a),
            "q_second_b": str(q_second_b),
            "q_composed_a": str(q_composed_a),
            "q_composed_b": str(q_composed_b),
            "same_input_q_different_composed_q": True,
            "pointwise_group_law_is_hopf_charge_homomorphism": False,
        },
    }


def subgroup_rows() -> list[dict[str, str]]:
    return [
        {
            "candidate": "FULL_POSITIVE_TRIANGULAR_TEN_FIELD_GROUP",
            "closure": "PRODUCT_AND_INVERSE",
            "invariance": "CHART_LEVEL_ONLY",
            "hopf_relation": "CONTAINS_ANGULAR_FACTOR_BUT_NO_SELECTED_AXES_OR_PHASE",
            "status": "DERIVED_CHART_GROUP",
        },
        {
            "candidate": "ZERO_SHIFT_BLOCK_DIAGONAL",
            "closure": "SUBGROUP",
            "invariance": "NOT_SELECTED_AND_NOT_GENERIC_UNDER_SHIFTED_CONJUGATION",
            "hopf_relation": "REMOVES_BASE_ANGULAR_SHIFT_WITHOUT_DERIVING_ITS_ABSENCE",
            "status": "DERIVED_SUBGROUP_CHOSE_AS_PHYSICAL_SLICE",
        },
        {
            "candidate": "POSITIVE_UPPER_TRIANGULAR_ANGULAR_FACTOR",
            "closure": "PRODUCT_AND_INVERSE",
            "invariance": "FACTOR_OF_REGISTERED_CHART_GROUP",
            "hopf_relation": "CARRIES_SCALE_AND_RECIPROCAL_DEPTH_CHARACTERS_DESPITE_SHEAR",
            "status": "DERIVED_CHART_FACTOR",
        },
        {
            "candidate": "POSITIVE_DIAGONAL_ANGULAR_SUBSET",
            "closure": "SUBGROUP",
            "invariance": "NOT_NORMAL_UNDER_ANGULAR_SHEAR",
            "hopf_relation": "SUPPLIES_ALIGNED_TORIC_AXES_ONLY_AFTER_SHEAR_IS_SET_ZERO",
            "status": "DERIVED_SUBGROUP_NOT_SELECTED",
        },
        {
            "candidate": "COMMON_SCALE_TIMES_RECIPROCAL_DIAGONAL",
            "closure": "COMMUTATIVE_SUBGROUP",
            "invariance": "CSN_RATIO_INVARIANT_BUT FRAME_AND_AXIS_DEPENDENT",
            "hopf_relation": "INDUCES_EXACT_LOGISTIC_WEIGHT_AND_LATITUDE_LAWS",
            "status": "DERIVED_CONDITIONAL_ALIGNED_SUBGROUP",
        },
        {
            "candidate": "RECIPROCAL_TORIC_CONNECTION_AND_QUOTIENT",
            "closure": "WEIGHT_AND_LATITUDE_CLOSE_ON_OPEN_INTERVAL",
            "invariance": "COMMON_SCALE_INDEPENDENT; PHASE_GLOBAL_DATA_AND_GAUGE_OPEN",
            "hopf_relation": "EXACT_SEED_LEVEL_COMPATIBILITY",
            "status": "EXACT_CONDITIONAL_WITNESS",
        },
        {
            "candidate": "PROJECTIVE_NULL_DIRECTION_S2_FIBER",
            "closure": "NOT_A_COFAME_GROUP_SUBGROUP",
            "invariance": "CONFORMAL_FIBER_NATURAL; SECTION_AND_TRANSPORT_OPEN",
            "hopf_relation": "TORIC_QUOTIENT_LIFTS_TO_NULL_SECTION_IN_CHOSEN_FRAME",
            "status": "CONDITIONAL_DERIVED_FIBER_OPEN_SECTION",
        },
        {
            "candidate": "POSITED_MAP_S3_S2_CARRIER_AND_RELAXED_HOPFION",
            "closure": "INDEPENDENT_CONFIGURATION_SPACE",
            "invariance": "CARRIER_ACTION_BOX_AND_BOUNDARY_CONDITIONAL",
            "hopf_relation": "SEED_MATCH_ONLY_NOT_RELAXED_FIELD_EQUALITY",
            "status": "OBSERVED_AND_SETTLED_WITH_EXISTING_PREMISES_NOT_NATIVE_JOIN",
        },
    ]


def dependency_rows() -> list[dict[str, str]]:
    return [
        {
            "object": "descent of chart multiplication to physical coframe/metric classes",
            "metric_or_group_supply": "FAILS_UNDER_INDEPENDENT_LOCAL_LORENTZ_REPRESENTATIVES",
            "extra_premise": "type-correct soldering plus selected section or Lorentz-equivariant quotient operation",
            "hopf_role": "makes the composition frame-independent",
            "ruling": "OPEN",
        },
        {
            "object": "angular reciprocal depth character",
            "metric_or_group_supply": "DERIVED_IN_POSITIVE_TRIANGULAR_CHART",
            "extra_premise": "physical owner and representative",
            "hopf_role": "latitude parameter",
            "ruling": "DERIVED_CHART_CHARACTER_PHYSICAL_OWNERSHIP_OPEN",
        },
        {
            "object": "identification of positional scalar phi with angular depth",
            "metric_or_group_supply": "NOT_SELECTED_IN_COMPLETE_TEN_FIELD_PLUS_SCALAR_SPACE",
            "extra_premise": "conditional reciprocal-toric identification",
            "hopf_role": "ties positional depth to latitude",
            "ruling": "CHOSE_IN_EXISTING_WITNESS",
        },
        {
            "object": "connection weight f",
            "metric_or_group_supply": "DERIVED_FROM_ALIGNED_RECIPROCAL_ANGULAR_RATIO",
            "extra_premise": "diagonal axes and toric circle coordinates",
            "hopf_role": "Hopf connection coefficient",
            "ruling": "DERIVED_CONDITIONAL",
        },
        {
            "object": "transverse phase delta",
            "metric_or_group_supply": "NOT_COMPOSED_OR_SELECTED",
            "extra_premise": "two periodic axes and their difference",
            "hopf_role": "azimuth on target S2",
            "ruling": "OPEN",
        },
        {
            "object": "S2-valued quotient/null section",
            "metric_or_group_supply": "EXACT_UNIT_AND_NULL LIFT AFTER PHI_DELTA_FRAME",
            "extra_premise": "toric phi delta and representative coframe",
            "hopf_role": "seed-level section",
            "ruling": "CONDITIONAL_EXACT_SECTION_WITNESS",
        },
        {
            "object": "periods circle action caps orientation full range",
            "metric_or_group_supply": "NOT_SELECTED",
            "extra_premise": "existing toric global completion",
            "hopf_role": "turns continuous endpoint readout into integer class",
            "ruling": "CONDITIONAL_GLOBAL_DATA",
        },
        {
            "object": "finite-endpoint Hopf readout under composition",
            "metric_or_group_supply": "NOT_A_HOMOMORPHISM_OF_SEPARATE_Q_VALUES",
            "extra_premise": "complete endpoint profiles",
            "hopf_role": "boundary-dependent diagnostic",
            "ruling": "DERIVED_OBSTRUCTION_TO_CHARGE_COMPOSITION",
        },
        {
            "object": "deformation from exact seed to relaxed field",
            "metric_or_group_supply": "NOT_SUPPLIED",
            "extra_premise": "independent Map(S3,S2) carrier configuration space",
            "hopf_role": "existing stable configuration",
            "ruling": "POSIT_CONDITIONAL",
        },
        {
            "object": "L2+L4 action and static stability",
            "metric_or_group_supply": "NOT_DERIVED_BY_POINTWISE_GROUP",
            "extra_premise": "existing carrier functional box boundary operator",
            "hopf_role": "stabilizes relaxed Hopfion",
            "ruling": "SETTLED_STATIC_FINITE_BOX_CONDITIONAL_UNCHANGED",
        },
        {
            "object": "time-live persistence source mass",
            "metric_or_group_supply": "ABSENT",
            "extra_premise": "native dynamics boundary source and scale",
            "hopf_role": "physical matter completion",
            "ruling": "OPEN",
        },
    ]


def status_rows() -> list[dict[str, str]]:
    return [
        {
            "id": "S01",
            "status": "DERIVED",
            "claim": "The complete triangular chart group has independent additive base and angular diagonal-depth characters.",
            "scope": "Chosen positive triangular coordinate/internal section; characters survive shear algebraically.",
        },
        {
            "id": "S02",
            "status": "OPEN",
            "claim": "Current UDT selects which chart character, if either, physically owns positional phi.",
            "scope": "Controlling reciprocal-subbundle ownership audit remains unchanged.",
        },
        {
            "id": "S03",
            "status": "DERIVED_CONDITIONAL",
            "claim": "Common-scale times reciprocal-diagonal angular coframes form a commutative subgroup.",
            "scope": "Aligned diagonal angular axes in the chosen chart.",
        },
        {
            "id": "S04",
            "status": "DERIVED",
            "claim": "The diagonal Hopf-compatible angular subgroup is not normal under the full upper-triangular angular group.",
            "scope": "Exact shear conjugation; no claim about a future physical quotient.",
        },
        {
            "id": "S05",
            "status": "DERIVED_CONDITIONAL_CHART_IDENTITY",
            "claim": "Within the toric identification, chosen chart multiplication induces exact logistic connection-weight and hyperbolic Hopf-latitude formulas.",
            "scope": "Chosen triangular trivialization, chosen chart composition, aligned axes, common domain, and phiD=scalar phi are supplied.",
        },
        {
            "id": "S06",
            "status": "OPEN",
            "claim": "The coframe group selects or composes the transverse phase delta.",
            "scope": "Delta is coordinate/global circle data absent from the pointwise group law.",
        },
        {
            "id": "S07",
            "status": "CONDITIONAL",
            "claim": "The reciprocal-toric quotient is a unit S2 field and a null-direction section.",
            "scope": "Requires toric phi/delta and a chosen Lorentzian coframe representative.",
        },
        {
            "id": "S08",
            "status": "DERIVED",
            "claim": "CSN removes common angular scale from the toric connection weight.",
            "scope": "It does not select axes, section, phase, or physical reciprocal subbundle.",
        },
        {
            "id": "S09",
            "status": "DERIVED",
            "claim": "The composed finite-endpoint readout does not factor through the two separate endpoint-readout values, so no binary operation on Q alone is induced.",
            "scope": "Exact same-input-readout counterexample; no target operation is presumed and global full-range topology remains conditional.",
        },
        {
            "id": "S10",
            "status": "CONDITIONAL",
            "claim": "Full reciprocal range plus supplied periods, circle action, caps, orientation, and normalization gives unit Hopf class.",
            "scope": "Existing reciprocal-toric control; none of the global data is newly derived.",
        },
        {
            "id": "S11",
            "status": "EXACT_CONDITIONAL",
            "claim": "The toric quotient formula exactly matches the existing degree-one Hopf seed.",
            "scope": "Exact seed-level correspondence, not equality to the relaxed field.",
        },
        {
            "id": "S12",
            "status": "POSIT",
            "claim": "The relaxed Hopfion lives in an independent round-S2 carrier configuration space.",
            "scope": "Carrier emergence remains open.",
        },
        {
            "id": "S13",
            "status": "CONDITIONAL",
            "claim": "Existing Hopfion stability remains settled in its static finite-box carrier/action premises.",
            "scope": "No time-live, boundary, source, mass, or native-emergence upgrade.",
        },
        {
            "id": "S14",
            "status": "OPEN",
            "claim": "A native coframe-to-Hopf carrier bridge is derived.",
            "scope": "Missing physical ownership/gauge descent, phase, global completion, deformation space, and action.",
        },
    ]


def main() -> None:
    source_count = verify_sources()
    algebra = exact_algebra()
    subgroups = subgroup_rows()
    dependencies = dependency_rows()
    statuses = status_rows()
    write_tsv("SUBGROUP_CENSUS.tsv", subgroups)
    write_tsv("BRIDGE_DEPENDENCY_MATRIX.tsv", dependencies)
    write_tsv("STATUS_LEDGER.tsv", statuses)
    result = {
        "schema": "udt-coframe-hopf-bridge-audit-v1",
        "source_count": source_count,
        "algebra": algebra,
        "counts": {
            "registered_candidates": len(subgroups),
            "bridge_dependencies": len(dependencies),
            "status_rows": len(statuses),
            "native_carrier_bridges_derived": 0,
            "exact_conditional_seed_bridges": 1,
            "independent_additive_chart_depth_characters": 2,
        },
        "rulings": {
            "new_exact_structure": (
                "THE_CHOSEN_COMPLETE_TRIANGULAR_CHART_GROUP_CARRIES_AN_ANGULAR_"
                "RECIPROCAL_DEPTH_CHARACTER_WHOSE_ALIGNED_TORIC_SUBGROUP_"
                "INDUCES_EXACT_HOPF_CONNECTION_WEIGHT_AND_LATITUDE_FORMULAS"
            ),
            "physical_limit": (
                "CURRENT_UDT_DOES_NOT_SELECT_THE_CHARACTERS_PHYSICAL_OWNER_"
                "TORIC_AXES_PHASE_GLOBAL_COMPLETION_DEFORMATION_SPACE_OR_ACTION"
            ),
            "hopfion_status": (
                "EXISTING_FULL_3D_HOPFION_REMAINS_STATIC_FINITE_BOX_"
                "CARRIER_AND_ACTION_CONDITIONAL"
            ),
        },
        "maximum_conclusion": (
            "EXACT_CONDITIONAL_CHART_LEVEL_ANGULAR_CHARACTER_TO_HOPF_WEIGHT_"
            "AND_LATITUDE_CROSSWALK_IDENTIFIED__FRAME_INDEPENDENT_KINEMATIC_"
            "LAW_NATIVE_CARRIER_AND_HOPFION_EMERGENCE_REMAIN_OPEN"
        ),
    }
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
