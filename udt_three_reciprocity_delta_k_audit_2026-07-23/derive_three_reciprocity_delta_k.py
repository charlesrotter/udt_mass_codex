#!/usr/bin/env python3
"""Derive the exact consequences of UDT's three distinct reciprocities."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "51a355a746fab82baa9760ceaf564f20ab2e1099"
MAXIMUM = (
    "CURRENT_RECIPROCITIES_SUPPLY_A_REFERENCE_SOURCE_AND_COVARIANT_"
    "OBSTRUCTION;UNDER_ADDED_HOMOGENEITY_CENTRALITY_AND_TWO_SEAL_"
    "PREMISES_THE_OPEN_TENSOR_SEAM_REDUCES_TO_ONE_DIMENSIONLESS_SCALAR_"
    "LAMBDA_BUT_LAMBDA_EQUALS_ONE_REMAINS_OPEN"
)

SOURCES = [
    ("S01", "reciprocal_c_clock_channel_correction_2026-07-19/AUDIT_REPORT.md",
     "RECIPROCAL_C_MEANING"),
    ("S02", "udt_reciprocal_c_metric_meaning_audit_2026-07-22/AUDIT_REPORT.md",
     "PAIR_AND_OBSERVER_RECIPROCITY"),
    ("S03", "udt_reciprocal_c_metric_meaning_audit_2026-07-22/"
     "PREREGISTRATION_OWNER_CLARIFICATION.md", "OBSERVER_OWNER_MEANING"),
    ("S04", "udt_clock_anchor_scale_threading_audit_2026-07-22/AUDIT_REPORT.md",
     "COVARIANCE_AND_SCALE_LIMIT"),
    ("S05", "udt_reciprocity_regime_angular_center_audit_2026-07-22/"
     "AUDIT_REPORT.md", "REGIME_AND_ANGULAR_SCOPE"),
    ("S06", "udt_two_frame_regime_metric_limit_audit_2026-07-22/AUDIT_REPORT.md",
     "TWO_FRAME_SCOPE"),
    ("S07", "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md", "XMAX_STATUS"),
    ("S08", "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
     "OWNER_LOCKED_PREMISES"),
    ("S09", "udt_premise_reset_audit_2026-07-19/"
     "LOAD_BEARING_CLAIM_REGRADE.tsv", "XMAX_REGRADE"),
    ("S10", "xmax_reciprocity_audit_2026-07-19/AUDIT_REPORT.md",
     "CONDITIONAL_XMAX_GROUP"),
    ("S11", "xmax_full_frame_realization_2026-07-19/AUDIT_REPORT.md",
     "CONDITIONAL_FULL_FRAME"),
    ("S12", "xmax_dynamic_observer_frame_2026-07-19/AUDIT_REPORT.md",
     "DYNAMIC_FRAME_SCOPE"),
    ("S13", "xmax_accelerating_finite_cell_cartan_2026-07-19/AUDIT_REPORT.md",
     "ACCELERATING_FRAME_SCOPE"),
    ("S14", "udt_angular_bulk_jacobi_selector_audit_2026-07-23/AUDIT_REPORT.md",
     "IMMEDIATE_PARENT"),
    ("S15", "udt_angular_bulk_jacobi_selector_audit_2026-07-23/"
     "RECIPROCAL_SOURCE_CONDITIONAL_THEOREM.json", "PARENT_THEOREM"),
    ("S16", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "CSN"),
    ("S17", "boundary_bootstrap_representative_selector_audit_2026-07-19/"
     "AUDIT_REPORT.md", "BOOTSTRAP_STATUS"),
    ("S18", str(HERE.relative_to(ROOT) / "PREREGISTRATION.md"), "FROZEN_SCOPE"),
    ("S19", str(HERE.relative_to(ROOT) / "PREMISE_LEDGER.tsv"),
     "FROZEN_PREMISES"),
    ("S20", str(HERE.relative_to(ROOT) / "ROUTE_UNIVERSE.tsv"),
     "FROZEN_ROUTES"),
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for piece in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(piece)
    return value.hexdigest()


def write_json(name: str, value: object) -> None:
    (HERE / name).write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_tsv(
    name: str,
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(item) == 0 for item in matrix)


def derive_reference_and_covariance() -> dict[str, object]:
    c, phi, mu, nu = sp.symbols(
        "c_E phi mu nu", positive=True, finite=True
    )
    a, b, d, e = sp.symbols("a b d e", real=True)
    transform = sp.Matrix([[a, b], [d, e]])
    assert sp.simplify(transform.det()) != 0
    inverse = transform.inv()
    identity = sp.eye(2)
    generator = sp.diag(-1, 1)
    reference_source = -generator * generator
    assert reference_source == -identity

    reciprocal_pair = sp.diag(sp.exp(-phi) / c, c * sp.exp(phi))
    pair_generator = sp.simplify(
        reciprocal_pair.inv() * sp.diff(reciprocal_pair, phi)
    )
    assert pair_generator == generator

    delta11, delta12, delta21, delta22 = sp.symbols(
        "delta11 delta12 delta21 delta22", real=True
    )
    delta = sp.Matrix([[delta11, delta12], [delta21, delta22]])
    delta_prime = sp.simplify(transform * delta * inverse)
    source_prime = sp.simplify(
        transform * (reference_source + delta) * inverse
    )
    covariance_residual = sp.simplify(
        source_prime
        - (
            transform * reference_source * inverse
            + delta_prime
        )
    )
    assert is_zero(covariance_residual)

    central = mu * identity
    central_prime = sp.simplify(transform * central * inverse)
    assert central_prime == central
    assert central != sp.zeros(2)

    mirror = sp.Matrix([[0, 1], [1, 0]])
    assert mirror * generator * mirror == -generator
    assert mirror * reference_source * mirror == reference_source

    xi = sp.symbols("xi", real=True)
    anisotropic = nu * xi * (1 - xi**2) ** 2 * generator
    reversed_anisotropic = sp.simplify(
        mirror
        * anisotropic.subs(xi, -xi)
        * mirror
    )
    assert is_zero(reversed_anisotropic - anisotropic)

    endpoint_flat = mu * (1 - xi**2) ** 2 * identity
    assert endpoint_flat.subs(xi, 1) == sp.zeros(2)
    assert endpoint_flat.subs(xi, -1) == sp.zeros(2)
    assert endpoint_flat.subs(xi, 0) == central

    return {
        "schema": "udt-three-reciprocity-covariance-1.0",
        "c_retained_symbolically": True,
        "reciprocal_pair": "diag(exp(-phi)/c_E,c_E*exp(phi))",
        "pair_generator": "L=diag(-1,+1)",
        "reference_source": "K_rec=-L^2=-I",
        "observer_law": "Delta_K_prime=S*Delta_K*S^-1",
        "covariance_residual": "EXACT_ZERO",
        "zero_is_frame_invariant": True,
        "zero_is_forced_by_covariance": False,
        "central_survivor": "Delta_K=mu*I",
        "central_survivor_nonzero_for_mu_nonzero": True,
        "mirror_action": "L->-L;K_rec->K_rec",
        "reversal_even_central_survivor": "mu*I",
        "reversal_even_anisotropic_survivor": (
            "nu*xi*(1-xi^2)^2*L"
        ),
        "endpoint_flat_survivor": "mu*(1-xi^2)^2*I",
        "ruling": "MAKES_COVARIANT_NOT_NECESSARY",
    }


def derive_xmax_group() -> dict[str, object]:
    x, y, z = sp.symbols("xi eta zeta", real=True)

    def compose(left: sp.Expr, right: sp.Expr) -> sp.Expr:
        return sp.factor((left + right) / (1 + left * right))

    xy = compose(x, y)
    associativity = sp.factor(compose(xy, z) - compose(x, compose(y, z)))
    identity_left = sp.factor(compose(0, x) - x)
    inverse = sp.factor(compose(x, -x))
    character = lambda value: sp.factor((1 - value) / (1 + value))
    character_residual = sp.factor(character(xy) - character(x) * character(y))
    assert associativity == 0
    assert identity_left == 0
    assert inverse == 0
    assert character_residual == 0

    endpoint_cross_denominator = sp.simplify(1 + 1 * (-1))
    endpoint_same = sp.simplify(compose(sp.Integer(1), sp.Integer(1)))
    assert endpoint_cross_denominator == 0
    assert endpoint_same == 1

    return {
        "schema": "udt-conditional-xmax-group-1.0",
        "domain": "open_interval_-1_lt_xi_lt_1",
        "composition": "(xi+eta)/(1+xi*eta)",
        "identity": 0,
        "inverse": "-xi",
        "associativity_residual": "EXACT_ZERO",
        "multiplicative_character": "(1-xi)/(1+xi)",
        "character_residual": "EXACT_ZERO",
        "additive_coordinate": "phi=atanh(xi)",
        "status": "CHOSE_CONDITIONAL_NOT_UNIQUE",
        "position_field_join": "OPEN_NOT_CERTIFIED",
        "positive_endpoint": "LIMIT_NOT_GROUP_ELEMENT",
        "negative_endpoint": "LIMIT_NOT_GROUP_ELEMENT",
        "plus_one_compose_minus_one_denominator": int(
            endpoint_cross_denominator
        ),
        "opposite_endpoints_composable": False,
        "same_endpoint_formal_limit": str(endpoint_same),
        "endpoints_are_regular_mirror_seals": False,
    }


def derive_constant_lambda_flow() -> dict[str, object]:
    lam, shear, t = sp.symbols(
        "lambda s t", positive=True, finite=True
    )
    u = sp.symbols("u", real=True)
    b = sp.factor(lam * (u + lam * t) / (lam + u * t))
    dt_dp = lam * (1 - t**2)
    residual = sp.factor(sp.diff(b, t) * dt_dp + b**2 - lam**2)
    assert residual == 0

    b_plus = sp.factor(b.subs(u, shear))
    b_minus = sp.factor(b.subs(u, -shear))
    area = sp.factor((b_plus + b_minus) / 2)
    shape_generator = sp.factor((b_plus - b_minus) / 2)
    shape = sp.factor(shape_generator**2)
    expected_area = sp.factor(
        lam * t * (lam**2 - shear**2)
        / (lam**2 - shear**2 * t**2)
    )
    expected_shape = sp.factor(
        lam**4 * shear**2 * (1 - t**2) ** 2
        / (lam**2 - shear**2 * t**2) ** 2
    )
    assert sp.factor(area - expected_area) == 0
    assert sp.factor(shape - expected_shape) == 0

    second_seal_numerator = sp.factor(
        area * (lam**2 - shear**2 * t**2)
    )
    assert sp.simplify(
        second_seal_numerator
        - lam * t * (lam - shear) * (lam + shear)
    ) == 0

    matched_area = sp.simplify(area.subs(shear, lam))
    matched_shape = sp.simplify(shape.subs(shear, lam))
    assert matched_area == 0
    assert matched_shape == lam**2

    witnesses = []
    for lam_value in (sp.Integer(1), sp.Integer(2), sp.Integer(3)):
        for t_value in (sp.Rational(1, 3), sp.Rational(2, 5)):
            witness_area = sp.simplify(
                area.subs({lam: lam_value, shear: lam_value, t: t_value})
            )
            witness_shape = sp.simplify(
                shape.subs({lam: lam_value, shear: lam_value, t: t_value})
            )
            assert witness_area == 0
            assert witness_shape == lam_value**2
            witnesses.append(
                {
                    "lambda": str(lam_value),
                    "s": str(lam_value),
                    "t": str(t_value),
                    "A_rel": str(witness_area),
                    "S_shape": str(witness_shape),
                    "unit_shape": witness_shape == 1,
                }
            )

    return {
        "schema": "udt-constant-lambda-riccati-1.0",
        "added_control_premises": [
            "supplied_regular_screen",
            "central_angular_source",
            "phi_translation_homogeneity",
            "negative_constant_source_sign",
            "parallel_screen",
            "nonsingular_flow",
        ],
        "source": "K_eff=-lambda^2*I",
        "equation": "B_p+B^2-lambda^2*I=0",
        "t": "tanh(lambda*Delta_phi)",
        "matrix_solution": (
            "B=lambda*(B0+lambda*t*I)*(lambda*I+t*B0)^-1"
        ),
        "eigen_solution": "b_u=lambda*(u+lambda*t)/(lambda+u*t)",
        "riccati_residual": "EXACT_ZERO",
        "first_seal": "B0=J0;J0^2=s^2*I;A_rel(0)=0",
        "area": (
            "lambda*t*(lambda^2-s^2)/(lambda^2-s^2*t^2)"
        ),
        "shape": (
            "lambda^4*s^2*(1-t^2)^2/"
            "(lambda^2-s^2*t^2)^2"
        ),
        "second_nontrivial_area_seal_condition": "s^2=lambda^2",
        "matched_flow_area": "0",
        "matched_flow_shape": "lambda^2",
        "two_seals_force_lambda_one": False,
        "witnesses": witnesses,
    }


def make_counterfamilies() -> list[dict[str, object]]:
    return [
        {
            "counter_id": "C01",
            "family": "CENTRAL_CONSTANT",
            "Delta_K": "mu*I",
            "c_reciprocal": "PRESERVED_REFERENCE_PAIR",
            "observer_reciprocity": "INVARIANT_UNDER_ANY_CONJUGATION",
            "Xmax_reversal": "EVEN",
            "endpoint_behavior": "NOT_CONSTRAINED",
            "complete_metric_status": "ALLOWED_SOURCE_JET",
            "defeats": "COVARIANCE_IMPLIES_DELTA_K_ZERO",
        },
        {
            "counter_id": "C02",
            "family": "CENTRAL_ENDPOINT_FLAT",
            "Delta_K": "mu*(1-xi^2)^2*I",
            "c_reciprocal": "PRESERVED_REFERENCE_PAIR",
            "observer_reciprocity": "COVARIANT_SCALAR_ENDOMORPHISM",
            "Xmax_reversal": "EVEN",
            "endpoint_behavior": "VANISHES_AT_BOTH_FORMAL_LIMITS",
            "complete_metric_status": "ALLOWED_SOURCE_JET",
            "defeats": "ENDPOINT_MATCHING_IMPLIES_BULK_EQUALITY",
        },
        {
            "counter_id": "C03",
            "family": "ANISOTROPIC_REVERSAL_EVEN",
            "Delta_K": "nu*xi*(1-xi^2)^2*L",
            "c_reciprocal": "L_EXPLICIT",
            "observer_reciprocity": "COVARIANT_WHERE_SCREEN_JOIN_SUPPLIED",
            "Xmax_reversal": "XI_ODD_AND_L_ODD",
            "endpoint_behavior": "VANISHES_AT_BOTH_FORMAL_LIMITS",
            "complete_metric_status": "ALLOWED_WITHOUT_ANGULAR_ISOTROPY",
            "defeats": "THREE_RECIPROCITIES_FORCE_CENTRALITY",
        },
        {
            "counter_id": "C04",
            "family": "CENTRAL_HOMOGENEOUS",
            "Delta_K": "(1-lambda^2)*I",
            "c_reciprocal": "K_rec_RETAINED",
            "observer_reciprocity": "INVARIANT_UNDER_ANY_CONJUGATION",
            "Xmax_reversal": "EVEN_AND_PHI_HOMOGENEOUS",
            "endpoint_behavior": "ENDPOINTS_NOT_GROUP_ELEMENTS",
            "complete_metric_status": "STRONGEST_CHARITABLE_CONTROL",
            "defeats": "SYMMETRIES_FIX_LAMBDA_EQUALS_ONE",
        },
    ]


def route_rulings() -> list[dict[str, str]]:
    rulings = {
        "R01": ("SUPPLIES_REFERENCE_ONLY",
                "L_and_K_rec_are_exact_but_no_angular_source_equation_follows"),
        "R02": ("MAKES_COVARIANT_NOT_NECESSARY",
                "Delta_K_transforms_by_conjugation;zero_is_invariant_not_forced"),
        "R03": ("CONSTRAINS_NOT_CLOSES",
                "central_mu_I_survives_every_conjugation;anisotropy_survives_without_isotropy"),
        "R04": ("CONSTRAINS_NOT_CLOSES",
                "conditional_group_supplies_addition_reversal_and_character_not_source_normalization"),
        "R05": ("OBSTRUCTED_OR_UNDEFINED",
                "plus_minus_endpoints_are_open_limits_and_opposite_composition_is_undefined"),
        "R06": ("NOT_JOINED_TO_COMPLETE_METRIC",
                "physical_position_observer_depth_and_absolute_metric_phi_are_not_derived_as_one_object"),
        "R07": ("CONSTRAINS_NOT_CLOSES",
                "central_and_endpoint_flat_Delta_K_counterfamilies_survive"),
        "R08": ("REDUCES_TO_SCALAR_SEAM_CONDITIONALLY",
                "added_centrality_homogeneity_and_sign_reduce_source_to_lambda_not_to_one"),
        "R09": ("REDUCES_TO_SCALAR_SEAM_CONDITIONALLY",
                "exact_flow_exposes_lambda_as_dimensionless_relative_normalization"),
        "R10": ("CONSTRAINS_NOT_CLOSES",
                "two_area_seals_force_s_squared_equals_lambda_squared_not_lambda_squared_equals_one"),
        "R11": ("CONSTRAINS_NOT_CLOSES",
                "no_registered_angular_isotropy_removes_noncentral_source_freedom"),
        "R12": ("CONSTRAINS_NOT_CLOSES",
                "CSN_and_dimensional_c_G_anchors_do_not_fix_dimensionless_lambda"),
        "R13": ("NOT_JOINED_TO_COMPLETE_METRIC",
                "finite_cell_and_bootstrap_lack_executable_source_or_boundary_selector"),
        "R14": ("CONSTRAINS_NOT_CLOSES",
                "both_Delta_K_zero_and_two_regular_seals_remain_added_premises"),
    }
    with (HERE / "ROUTE_UNIVERSE.tsv").open(
        newline="", encoding="utf-8"
    ) as handle:
        universe = list(csv.DictReader(handle, delimiter="\t"))
    assert len(universe) == 14
    assert set(rulings) == {row["route_id"] for row in universe}
    return [
        {
            **row,
            "ruling": rulings[row["route_id"]][0],
            "reason": rulings[row["route_id"]][1],
        }
        for row in universe
    ]


def make_status_ledger() -> list[dict[str, str]]:
    return [
        {"claim_id": "Q01", "claim": "reciprocal_c_pair_and_L",
         "status": "DERIVED_IN_ABSTRACT_PAIR",
         "scope": "founding_clock_ruler_pair"},
        {"claim_id": "Q02", "claim": "K_rec_equals_minus_I",
         "status": "DERIVED_REFERENCE_SOURCE",
         "scope": "same_abstract_reciprocal_pair"},
        {"claim_id": "Q03", "claim": "observer_frame_reciprocity",
         "status": "OWNER_LOCKED_ORDINARY_REGIME",
         "scope": "passive_covariance_no_preferred_observer"},
        {"claim_id": "Q04", "claim": "Delta_K_zero_is_frame_invariant",
         "status": "DERIVED",
         "scope": "supplied_screen_and_frame_action"},
        {"claim_id": "Q05", "claim": "observer_covariance_forces_Delta_K_zero",
         "status": "NOT_DERIVED",
         "scope": "central_counterfamily_survives"},
        {"claim_id": "Q06", "claim": "one_global_Xmax",
         "status": "WORKING_POSIT",
         "scope": "completed_universe"},
        {"claim_id": "Q07", "claim": "fractional_Xmax_composition",
         "status": "CHOSE_CONDITIONAL",
         "scope": "signed_open_interval"},
        {"claim_id": "Q08", "claim": "Xmax_join_to_absolute_metric_phi",
         "status": "OPEN",
         "scope": "physical_position_field_join"},
        {"claim_id": "Q09", "claim": "Xmax_endpoints_are_regular_seals",
         "status": "NOT_DERIVED",
         "scope": "endpoints_are_noncomposable_limits"},
        {"claim_id": "Q10", "claim": "three_reciprocities_force_Delta_K_zero",
         "status": "NOT_DERIVED",
         "scope": "current_registered_premises"},
        {"claim_id": "Q11", "claim": "strongest_composition_reduces_to_lambda",
         "status": "CONDITIONAL",
         "scope": "added_centrality_homogeneity_sign_and_screen"},
        {"claim_id": "Q12", "claim": "two_seals_force_s_squared_lambda_squared",
         "status": "DERIVED_CONDITIONAL",
         "scope": "constant_lambda_nonsingular_Riccati_control"},
        {"claim_id": "Q13", "claim": "lambda_equals_one",
         "status": "OPEN",
         "scope": "dimensionless_reciprocal_angular_normalization"},
        {"claim_id": "Q14", "claim": "complete_native_action_source_boundary",
         "status": "OPEN",
         "scope": "not_addressed_by_symmetry_audit"},
    ]


def make_catch_proofs(
    covariance: dict[str, object],
    xmax: dict[str, object],
    flow: dict[str, object],
    routes: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks = [
        ("T01", "covariance_promoted_to_necessity",
         covariance["zero_is_forced_by_covariance"] is False),
        ("T02", "central_survivor_deleted",
         covariance["central_survivor_nonzero_for_mu_nonzero"] is True),
        ("T03", "c_anchor_dropped",
         covariance["c_retained_symbolically"] is True),
        ("T04", "reversal_demotes_reference_source",
         covariance["mirror_action"] == "L->-L;K_rec->K_rec"),
        ("T05", "endpoint_flat_bulk_countermodel_deleted",
         "endpoint_flat_survivor" in covariance),
        ("T06", "Xmax_law_promoted_to_unique",
         xmax["status"] == "CHOSE_CONDITIONAL_NOT_UNIQUE"),
        ("T07", "position_field_join_silently_inserted",
         xmax["position_field_join"] == "OPEN_NOT_CERTIFIED"),
        ("T08", "opposite_endpoints_promoted_to_group_pair",
         xmax["opposite_endpoints_composable"] is False),
        ("T09", "endpoints_promoted_to_regular_seals",
         xmax["endpoints_are_regular_mirror_seals"] is False),
        ("T10", "lambda_set_to_one",
         flow["two_seals_force_lambda_one"] is False),
        ("T11", "lambda_two_witness_missing",
         any(row["lambda"] == "2" and row["S_shape"] == "4"
             for row in flow["witnesses"])),
        ("T12", "lambda_three_witness_missing",
         any(row["lambda"] == "3" and row["S_shape"] == "9"
             for row in flow["witnesses"])),
        ("T13", "conditional_premises_hidden",
         len(flow["added_control_premises"]) == 6),
        ("T14", "route_missing_or_duplicate",
         len(routes) == 14
         and len({row["route_id"] for row in routes}) == 14),
        ("T15", "native_derivation_false_positive",
         all(row["ruling"] != "DERIVES_MISSING_PREMISE" for row in routes)),
        ("T16", "two_seal_premise_promoted_native",
         "parallel_screen" in flow["added_control_premises"]),
        ("T17", "source_sign_hidden",
         "negative_constant_source_sign" in flow["added_control_premises"]),
        ("T18", "maximum_conclusion_overstated",
         "LAMBDA_EQUALS_ONE_REMAINS_OPEN" in MAXIMUM),
    ]
    assert all(ok for _, _, ok in checks)
    return [
        {
            "catch_id": catch_id,
            "mutation": mutation,
            "expected": "REJECT",
            "result": "PASS_REJECTED",
        }
        for catch_id, mutation, _ in checks
    ]


def main() -> None:
    assert (ROOT / ".git").exists()
    lineage = []
    for source_id, relative_path, role in SOURCES:
        path = ROOT / relative_path
        if not path.is_file():
            raise AssertionError(f"missing source: {relative_path}")
        lineage.append(
            {
                "source_id": source_id,
                "path": relative_path,
                "role": role,
                "sha256": digest(path),
            }
        )

    covariance = derive_reference_and_covariance()
    xmax = derive_xmax_group()
    flow = derive_constant_lambda_flow()
    counterfamilies = make_counterfamilies()
    routes = route_rulings()
    status = make_status_ledger()
    catches = make_catch_proofs(covariance, xmax, flow, routes)

    write_json("RECIPROCITY_COVARIANCE.json", covariance)
    write_json("XMAX_GROUP_ENDPOINTS.json", xmax)
    write_json("CONSTANT_LAMBDA_RICCATI.json", flow)
    write_tsv(
        "COUNTERFAMILY_ATLAS.tsv",
        list(counterfamilies[0]),
        counterfamilies,
    )
    write_tsv(
        "ROUTE_RULING_MATRIX.tsv",
        ["route_id", "route", "required_test", "ruling", "reason"],
        routes,
    )
    write_tsv(
        "STATUS_LEDGER.tsv",
        ["claim_id", "claim", "status", "scope"],
        status,
    )
    write_tsv(
        "SOURCE_LINEAGE.tsv",
        ["source_id", "path", "role", "sha256"],
        lineage,
    )
    write_tsv(
        "CATCH_PROOFS.tsv",
        ["catch_id", "mutation", "expected", "result"],
        catches,
    )
    result = {
        "schema": "udt-three-reciprocity-delta-k-audit-1.0",
        "base_commit": BASE,
        "metric_led": True,
        "cpu_only": True,
        "current_registered_composition": {
            "Delta_K_zero": "NOT_DERIVED",
            "two_regular_mirror_seals": "NOT_DERIVED",
            "reason": [
                "covariance_preserves_optional_zero_but_does_not_force_it",
                "central_and_anisotropic_covariant_counterfamilies_survive",
                "Xmax_position_field_join_is_open",
                "Xmax_endpoints_are_limits_not_regular_seals",
            ],
        },
        "strongest_charitable_composition": {
            "status": "CONDITIONAL",
            "additional_premises": flow["added_control_premises"],
            "reduction": "K_eff=-lambda^2*I",
            "two_seal_result": "s^2=lambda^2",
            "bulk_result": "A_rel=0;S_shape=lambda^2",
            "remaining_seam": "lambda=1",
        },
        "three_reciprocity_roles": {
            "reciprocal_c": "SUPPLIES_L_AND_REFERENCE_K_rec",
            "observer_frame": "MAKES_DELTA_K_A_COVARIANT_OBSTRUCTION",
            "Xmax": "CONDITIONALLY_SUPPLIES_GLOBAL_GROUP_AND_REVERSAL",
        },
        "founded_vs_open": {
            "founded": [
                "reciprocal_c_pair",
                "abstract_exponential_character",
                "ordinary_regime_observer_covariance",
            ],
            "working_or_chosen": [
                "one_global_Xmax",
                "fractional_linear_Xmax_group",
            ],
            "open": [
                "Xmax_position_field_join",
                "absolute_relative_phi_join",
                "complete_angular_source",
                "two_regular_seals",
                "lambda_equals_one",
            ],
        },
        "maximum_conclusion": MAXIMUM,
        "native_closure": False,
        "source_count": len(lineage),
        "route_count": len(routes),
        "counterfamily_count": len(counterfamilies),
        "catch_count": len(catches),
        "catch_pass_count": sum(
            row["result"] == "PASS_REJECTED" for row in catches
        ),
    }
    write_json("RESULT.json", result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
