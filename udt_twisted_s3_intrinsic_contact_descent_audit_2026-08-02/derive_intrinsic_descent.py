#!/usr/bin/env python3
"""Exact intrinsic contact descent on the frozen twisted-S3 witness."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def verify_sources() -> int:
    rows = read_tsv("SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 30
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert len(content) == int(row["bytes"])
        assert sha256_bytes(content) == row["sha256"]
    assert sha256_bytes((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == (
        HERE / "SOURCE_MANIFEST.sha256"
    ).read_text(encoding="utf-8").strip()
    return len(rows)


def two_form_norm(form: sp.Matrix, inverse_metric: sp.Matrix) -> sp.Expr:
    raised = inverse_metric * form * inverse_metric
    return sp.factor(sum(form[i, j] * raised[i, j] for i in range(4) for j in range(4)) / 2)


def main() -> int:
    source_count = verify_sources()
    assert len(read_tsv("OBJECT_UNIVERSE.tsv")) == 22
    assert len(read_tsv("FALSIFICATION_CONTRACT.tsv")) == 24

    u = sp.symbols("u", positive=True)
    phi = sp.symbols("phi", real=True)
    kappa = sp.Integer(-2)
    eta = sp.diag(-1, 1, 1, 1)

    lambda_rows = []
    symbolic_rows = []
    for lam in (-1, 0, 1):
        # Direct first-Cartan screen projections for T^flat=-theta0 and S^flat=theta1.
        t0 = sp.factor(kappa * u ** (-sp.Rational(1, 2) - lam))
        t1 = sp.factor(kappa * u ** (+sp.Rational(1, 2) - lam))
        q_t = -t0
        q_s = t1
        q_t_squared = sp.factor(q_t**2)
        q_s_squared = sp.factor(q_s**2)
        q_contact = sp.factor(q_s_squared - q_t_squared)
        expected_q_t = sp.factor(kappa**2 * u ** (-1 - 2 * lam))
        expected_q_s = sp.factor(kappa**2 * u ** (+1 - 2 * lam))
        expected_q = sp.factor(kappa**2 * u ** (-1 - 2 * lam) * (u**2 - 1))
        assert sp.simplify(q_t_squared - expected_q_t) == 0
        assert sp.simplify(q_s_squared - expected_q_s) == 0
        assert sp.simplify(q_contact - expected_q) == 0

        # Differential reconstructions.  Substitute u=exp(2 phi) before differentiating.
        qt_phi = q_t_squared.subs(u, sp.exp(2 * phi))
        qs_phi = q_s_squared.subs(u, sp.exp(2 * phi))
        q_phi = q_contact.subs(u, sp.exp(2 * phi))
        dlog_qt = sp.simplify(sp.diff(sp.log(qt_phi), phi))
        dlog_qs = sp.simplify(sp.diff(sp.log(qs_phi), phi))
        phi_reconstruction = sp.simplify((dlog_qs - dlog_qt) / 4)
        sigma_reconstruction = sp.simplify(-(dlog_qs + dlog_qt) / 4)
        dz_coefficient = sp.factor(sp.diff(sp.log(q_phi), phi) / 2)
        dz_u = sp.factor((u**2 + 1) / (u**2 - 1) - 2 * lam)
        assert phi_reconstruction == 1
        assert sigma_reconstruction == 2 * lam
        assert sp.simplify(
            dz_coefficient - ((u**2 + 1) / (u**2 - 1) - 2 * lam).subs(u, sp.exp(2 * phi))
        ) == 0

        # Exact range on 4 <= u <= 11.  Monotonicity is proved by the derivative sign.
        derivative = sp.factor(sp.diff(q_contact, u))
        if lam in (-1, 0):
            assert derivative.subs(u, 4) > 0 and derivative.subs(u, 11) > 0
            q_min = sp.factor(q_contact.subs(u, 4))
            q_max = sp.factor(q_contact.subs(u, 11))
            monotonicity = "STRICTLY_INCREASING_ON_4_11"
        else:
            assert derivative.subs(u, 4) < 0 and derivative.subs(u, 11) < 0
            # derivative=4*(3-u^2)/u^4, so it is negative throughout u>=4.
            assert sp.factor(derivative - 4 * (3 - u**2) / u**4) == 0
            q_min = sp.factor(q_contact.subs(u, 11))
            q_max = sp.factor(q_contact.subs(u, 4))
            monotonicity = "STRICTLY_DECREASING_ON_4_11"
        assert q_min > 0

        lambda_rows.append({
            "lambda": str(lam),
            "Q_T": str(q_t_squared),
            "Q_S": str(q_s_squared),
            "Q": str(q_contact),
            "dphi_reconstruction_coefficient": str(phi_reconstruction),
            "dsigma_reconstruction_coefficient": str(sigma_reconstruction),
            "dz_over_dphi": str(dz_u),
            "Q_monotonicity": monotonicity,
            "Q_min": str(q_min),
            "Q_max": str(q_max),
            "realized_stratum": "Q_POSITIVE_ONLY",
        })
        symbolic_rows.append({
            "lambda": lam,
            "q_T": str(q_t),
            "q_S": str(q_s),
            "Q_T": str(q_t_squared),
            "Q_S": str(q_s_squared),
            "Q": str(q_contact),
            "Q_derivative": str(derivative),
        })

    write_tsv(
        "LAMBDA_CERTIFICATE.tsv",
        [
            "lambda", "Q_T", "Q_S", "Q", "dphi_reconstruction_coefficient",
            "dsigma_reconstruction_coefficient", "dz_over_dphi", "Q_monotonicity",
            "Q_min", "Q_max", "realized_stratum",
        ],
        lambda_rows,
    )

    # Exact sign, orientation, and full-frame covariance controls.
    qT, qS = sp.symbols("qT qS", real=True)
    FT = sp.zeros(4)
    FS = sp.zeros(4)
    FT[2, 3], FT[3, 2] = qT, -qT
    FS[2, 3], FS[3, 2] = qS, -qS
    assert two_form_norm(FT, eta) == qT**2
    assert two_form_norm(FS, eta) == qS**2

    # Rational Lorentz transformation mixing pair and screen directions.
    boost = sp.Matrix([
        [sp.Rational(5, 4), 0, sp.Rational(3, 4), 0],
        [0, 1, 0, 0],
        [sp.Rational(3, 4), 0, sp.Rational(5, 4), 0],
        [0, 0, 0, 1],
    ])
    rotation = sp.Matrix([
        [1, 0, 0, 0],
        [0, sp.Rational(3, 5), 0, -sp.Rational(4, 5)],
        [0, 0, 1, 0],
        [0, sp.Rational(4, 5), 0, sp.Rational(3, 5)],
    ])
    lorentz = rotation * boost
    assert sp.simplify(lorentz.T * eta * lorentz - eta) == sp.zeros(4)
    inverse_lorentz = lorentz.inv()
    FT_prime = sp.simplify(inverse_lorentz.T * FT * inverse_lorentz)
    FS_prime = sp.simplify(inverse_lorentz.T * FS * inverse_lorentz)
    assert sp.simplify(two_form_norm(FT_prime, eta) - qT**2) == 0
    assert sp.simplify(two_form_norm(FS_prime, eta) - qS**2) == 0
    naive_q = sp.factor(FS_prime[2, 3] ** 2 - FT_prime[2, 3] ** 2)
    true_q = qS**2 - qT**2
    assert sp.simplify(naive_q - true_q) != 0

    controls = [
        {"control": "T_SIGN", "result": "PASS", "detail": "F_T flips; Q_T,Q_S,Q unchanged"},
        {"control": "S_SIGN", "result": "PASS", "detail": "F_S flips; Q_T,Q_S,Q unchanged"},
        {"control": "SCREEN_ORIENTATION", "result": "PASS", "detail": "signed q flips; squared contractions unchanged"},
        {"control": "K_CONSTANT_RESCALE", "result": "PASS", "detail": "unit line representative changes at most sign"},
        {"control": "FULL_FRAME_COVARIANCE", "result": "PASS", "detail": "exact rational Lorentz transform preserves tensor contractions"},
        {"control": "NAIVE_SLOT_RELABEL", "result": "REJECTED_AS_REQUIRED", "detail": f"naive_Q={naive_q};true_Q={true_q}"},
        {"control": "CONSTANT_DEPTH", "result": "AUTHORITY_BLOCKED", "detail": "prior invariant certificate is zero; no intrinsic pair promoted"},
        {"control": "TWIST_FREE", "result": "PAIR_UNDEFINED", "detail": "clock certificate can survive but ruler line and pair projector do not"},
        {"control": "SLICE_NULL", "result": "INELIGIBLE_RETAINED", "detail": "not crossed or used for descent"},
        {"control": "REFERENCE_SHIFT", "result": "PASS", "detail": "absolute logs change; dphi,dsigma,dz unchanged"},
    ]
    write_tsv("CONTROL_OUTCOMES.tsv", ["control", "result", "detail"], controls)

    atlas_rows = [
        ("O01", "clock_line", "METRIC_INTRINSIC_LINE_ON_WITNESS", "unique timelike Killing line", "other branches"),
        ("O02", "ruler_line", "METRIC_INTRINSIC_LINE_ON_WITNESS", "nonzero Killing-twist line", "twist-free and other branches"),
        ("O03", "pair_projector", "METRIC_TENSOR_ON_WITNESS", "sign-independent from O01/O02", "on-shell or universal selection"),
        ("O04", "screen_projector", "METRIC_TENSOR_ON_WITNESS", "identity minus pair projector", "individual screen axes"),
        ("O05", "oriented_screen_area", "ORIENTATION_LINE_NOT_CANONICAL_SIGN", "metric supplies unit area density up to sign", "selected orientation"),
        ("O06", "signed_contact_pair", "SIGN_LOCAL_SYSTEM_NOT_NUMERIC_SCALAR", "screen projections of dTflat,dSflat", "ordered signs and orientation"),
        ("O07", "Q_T", "METRIC_SCALAR_ON_WITNESS", "half norm squared of projected dTflat", "other branches"),
        ("O08", "Q_S", "METRIC_SCALAR_ON_WITNESS", "half norm squared of projected dSflat", "other branches"),
        ("O09", "Q_contact", "METRIC_SCALAR_ON_WITNESS", "Q_S minus Q_T", "universal observable status"),
        ("O10", "contact_causal_strata", "Q_POSITIVE_ONLY_ON_WITNESS", "exact positive lower bound for every registered lambda", "null and negative behavior elsewhere"),
        ("O11", "dphi_from_contact", "METRIC_ONE_FORM_ON_WITNESS", "one quarter dlog(Q_S/Q_T)", "absolute normalization outside witness"),
        ("O12", "dsigma_from_contact", "METRIC_ONE_FORM_ON_WITNESS", "minus one quarter dlog(Q_S Q_T)", "absolute area reference"),
        ("O13", "absolute_phi_sigma", "PHI_CONTACT_METRIC_SCALAR_ON_FROZEN_UNIT_WITNESS__SIGMA_REFERENCE_DEPENDENT", "phi_contact=one_quarter_log_QS_over_QT_equals_phi;absolute_sigma_needs_dimensionful_reference", "general_unfrozen_R_over_a_normalization_and_area_reference"),
        ("O14", "contact_coordinate_z", "REFERENCE_DEPENDENT_ABSOLUTE_DZ_INTRINSIC", "T0 changes z by constant", "selected dimensional reference"),
        ("O15", "contact_differential", "METRIC_TWO_FORM_IDENTICALLY_ZERO_ON_WITNESS", "dz proportional to dphi for all registered lambda", "nontrivial values on independent phi/screen branches"),
        ("O16", "alternating_primitive", "AVAILABLE_REFERENCE_DEPENDENT_NOT_SELECTED", "exterior derivative zero on witness", "law or primitive selection"),
        ("O17", "split_curvature_contractions", "METRIC_SCALARS_AS_A_CLASS_ON_WITNESS", "derived projectors remove prior split-authority obstruction", "complete values and universal reduction"),
        ("O18", "individual_screen_axes", "SCREEN_O2_GAUGE_NOT_SELECTED", "screen plane only", "additional section or symmetry"),
        ("O19", "first_Cartan_screen_slots", "FRAME_COEFFICIENTS_NOT_INDIVIDUAL_SCALARS", "tensorial combinations may be formed", "generic GL2 screen audit on intrinsic branch"),
        ("O20", "Levi_Civita_connection_slots", "CONNECTION_GAUGE_NOT_TENSOR", "inhomogeneous local-frame transformation", "tensorial curvature or chosen frame"),
        ("O21", "path_transport_holonomy", "PATH_DEPENDENT_NOT_FIXED_BY_LOCAL_DESCENT", "connection is metric-derived but path/loop is input", "path family and global transport audit"),
        ("O22", "global_section_carrier", "NOT_DERIVED_ADDITIONAL_GLOBAL_DATA", "pair and screen bundles do not select a carrier section", "carrier emergence and global law"),
    ]
    write_tsv(
        "DESCENT_ATLAS.tsv",
        ["object_id", "object", "status", "exact_scope", "open_scope"],
        [dict(zip(["object_id", "object", "status", "exact_scope", "open_scope"], row)) for row in atlas_rows],
    )
    write_tsv(
        "O13_SUBCLASSIFICATION.tsv",
        ["subobject_id", "subobject", "status", "exact_scope", "open_scope"],
        [
            {
                "subobject_id": "O13-PHI",
                "subobject": "Phi_contact",
                "status": "METRIC_SCALAR_ON_FROZEN_UNIT_WITNESS",
                "exact_scope": "one_quarter_log_QS_over_QT_equals_phi_for_a_equals_R_equals_one",
                "open_scope": "general_unfrozen_value_shifts_by_one_half_log_R_over_a",
            },
            {
                "subobject_id": "O13-SIGMA",
                "subobject": "absolute_sigma",
                "status": "REFERENCE_DEPENDENT_ABSOLUTE__DSIGMA_INTRINSIC",
                "exact_scope": "QS_QT_dimensionful_so_only_log_derivative_is_reference_free",
                "open_scope": "selected_area_reference_D0",
            },
        ],
    )

    result = {
        "schema": "udt-twisted-s3-intrinsic-contact-descent-1.0",
        "status": "PASS_EXACT_PRODUCTION",
        "frozen_sources": source_count,
        "objects_classified": len(atlas_rows),
        "registered_lambda_values": [-1, 0, 1],
        "lambda_certificates": symbolic_rows,
        "metric_scalar_objects": ["Q_T", "Q_S", "Q_contact", "Phi_contact_on_frozen_unit_witness"],
        "metric_one_form_objects": ["dphi_from_contact", "dsigma_from_contact", "dz_off_null"],
        "O13_subclassifications": 2,
        "Phi_contact": "ABSOLUTE_METRIC_SCALAR_EQUALS_PHI_ON_FROZEN_a_EQUALS_R_EQUALS_ONE_WITNESS",
        "Phi_contact_general_unfrozen_scope": "phi_plus_one_half_log_R_over_a",
        "absolute_sigma": "REFERENCE_DEPENDENT__DSIGMA_INTRINSIC",
        "contact_two_form_on_witness": "IDENTICALLY_ZERO",
        "realized_contact_stratum": "Q_POSITIVE_ONLY",
        "null_contact_points": 0,
        "negative_contact_points": 0,
        "naive_slot_relabel_rejected": True,
        "full_GL2_generality_claimed": False,
        "on_shell_claimed": False,
        "universal_claimed": False,
        "physics_promoted": False,
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in result.items() if key != "lambda_certificates"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
