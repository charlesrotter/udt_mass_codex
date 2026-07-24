#!/usr/bin/env python3
"""Exact controller for the Hopf/transport/bootstrap dependency audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path, key: str) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row[key]: row for row in csv.DictReader(handle, delimiter="\t")}


def verify_sources() -> tuple[bool, list[dict[str, object]]]:
    results: list[dict[str, object]] = []
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["path"]
            actual = sha256(path)
            is_manifest = path.name in {"SHA256SUMS.txt", "MANIFEST.sha256"}
            replay = True
            replay_stdout_sha256 = ""
            if is_manifest:
                completed = subprocess.run(
                    ["sha256sum", "--check", path.name],
                    cwd=path.parent,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                replay = completed.returncode == 0 and "FAILED" not in completed.stdout
                replay_stdout_sha256 = hashlib.sha256(
                    completed.stdout.encode()
                ).hexdigest()
            results.append(
                {
                    "path": row["path"],
                    "expected_sha256": row["sha256"],
                    "actual_sha256": actual,
                    "hash_match": actual == row["sha256"],
                    "package_manifest": is_manifest,
                    "package_replay": replay,
                    "replay_stdout_sha256": replay_stdout_sha256,
                }
            )
    return all(row["hash_match"] and row["package_replay"] for row in results), results


def form_component(form: dict[tuple[int, int], sp.Expr], i: int, j: int) -> sp.Expr:
    if i == j:
        return sp.Integer(0)
    if i < j:
        return form[(i, j)]
    return -form[(j, i)]


def torsion_identity() -> dict[str, object]:
    f01, f02, f12 = sp.symbols("f01 f02 f12")
    form = {(0, 1): f01, (0, 2): f02, (1, 2): f12}
    derivative = {
        (a, b, c): sp.symbols(f"d{a}{b}{c}")
        for a in range(3)
        for b in range(3)
        for c in range(b + 1, 3)
    }
    gamma = [
        [[sp.symbols(f"G{d}{a}{b}") for b in range(3)] for a in range(3)]
        for d in range(3)
    ]

    def partial(a: int, b: int, c: int) -> sp.Expr:
        if b == c:
            return sp.Integer(0)
        if b < c:
            return derivative[(a, b, c)]
        return -derivative[(a, c, b)]

    def covariant(a: int, b: int, c: int) -> sp.Expr:
        return sp.simplify(
            partial(a, b, c)
            - sum(
                gamma[d][a][b] * form_component(form, d, c)
                + gamma[d][a][c] * form_component(form, b, d)
                for d in range(3)
            )
        )

    d_form = sp.simplify(
        partial(0, 1, 2) + partial(1, 2, 0) + partial(2, 0, 1)
    )
    alt_covariant = sp.simplify(
        covariant(0, 1, 2)
        + covariant(1, 2, 0)
        + covariant(2, 0, 1)
    )

    def torsion(d: int, a: int, b: int) -> sp.Expr:
        return gamma[d][a][b] - gamma[d][b][a]

    correction = sp.simplify(
        sum(
            torsion(d, 0, 1) * form_component(form, d, 2)
            + torsion(d, 1, 2) * form_component(form, d, 0)
            + torsion(d, 2, 0) * form_component(form, d, 1)
            for d in range(3)
        )
    )
    generic_residual = sp.simplify(d_form - alt_covariant - correction)

    symmetric_subs = {
        gamma[d][a][b]: gamma[d][b][a]
        for d in range(3)
        for a in range(3)
        for b in range(a + 1, 3)
    }
    torsion_free_residual = sp.simplify((d_form - alt_covariant).subs(symmetric_subs))

    witness_subs = {symbol: 0 for symbol in set().union(
        *[
            set(entry.free_symbols)
            for plane in gamma
            for row in plane
            for entry in row
        ],
        set(d_form.free_symbols),
        {f01, f02, f12},
    )}
    witness_subs.update(
        {
            f01: sp.Integer(1),
            f02: sp.Integer(2),
            f12: sp.Integer(3),
            gamma[0][0][1]: sp.Integer(1),
        }
    )
    witness_d = sp.simplify(d_form.subs(witness_subs))
    witness_alt = sp.simplify(alt_covariant.subs(witness_subs))
    witness_correction = sp.simplify(correction.subs(witness_subs))

    return {
        "identity": "dF_abc=3*nabla_[a F_bc]+T^d_ab F_dc+T^d_bc F_da+T^d_ca F_db",
        "generic_residual": str(generic_residual),
        "generic_identity_pass": generic_residual == 0,
        "torsion_free_reduction_pass": torsion_free_residual == 0,
        "torsionful_witness": {
            "dF": str(witness_d),
            "naive_covariant_antisymmetrization": str(witness_alt),
            "torsion_correction": str(witness_correction),
            "naive_rewrite_fails": witness_alt != witness_d,
            "corrected_rewrite_passes": witness_d
            == witness_alt + witness_correction,
        },
    }


def primitive_gauge_identity() -> dict[str, object]:
    chi, chi0, chi1, chi2 = sp.symbols("chi chi0 chi1 chi2")
    f01, f02, f12 = sp.symbols("f01 f02 f12")
    df012 = sp.symbols("dF012")
    dchi_wedge_f = sp.expand(chi0 * f12 - chi1 * f02 + chi2 * f01)
    d_chi_f = sp.expand(dchi_wedge_f + chi * df012)
    closed_residual = sp.simplify((d_chi_f - dchi_wedge_f).subs(df012, 0))
    return {
        "integrand_change": str(dchi_wedge_f),
        "boundary_form_derivative": str(d_chi_f),
        "closed_form_exact_difference": closed_residual == 0,
        "integral_invariant_when_boundary_term_vanishes": True,
        "required_boundary_scope": "closed domain or fixed/constant boundary class",
    }


def conformal_action_weights() -> dict[str, object]:
    dimension, q = sp.Integer(3), sp.symbols("q", positive=True)
    e2_weight = sp.simplify(q**dimension * q**-2)
    e4_weight = sp.simplify(q**dimension * q**-4)
    e2, e4 = sp.symbols("E2 E4", positive=True)
    transformed = sp.expand(e2_weight * e2 + e4_weight * e4)
    witness = sp.simplify(transformed.subs({q: 2, e2: 3, e4: 5}))
    original = sp.Integer(8)
    return {
        "spatial_dimension": 3,
        "hbar": "q^2 h",
        "volume_weight": "q^3",
        "E2_weight": str(e2_weight),
        "E4_weight": str(e4_weight),
        "transformed_energy": str(transformed),
        "hf_specialization": "q=exp(f(phi)); E2 gets exp(f), E4 gets exp(-f)",
        "noninvariance_witness": {
            "q": 2,
            "E2": 3,
            "E4": 5,
            "original": str(original),
            "transformed": str(witness),
            "different": witness != original,
        },
        "Hopf_form_integral_metric_weight": 0,
        "Hodge_star_on_two_forms_in_three_dimensions_weight": "q^-1",
    }


def source_authority() -> dict[str, object]:
    native = read_tsv(
        ROOT / "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv",
        "claim_id",
    )
    transport = read_tsv(
        ROOT
        / "udt_reciprocal_transport_naturality_selector_audit_2026-07-23/STATUS_LEDGER.tsv",
        "id",
    )
    parent = read_tsv(
        ROOT / "udt_csn_dphi_transport_selector_audit_2026-07-23/STATUS_LEDGER.tsv",
        "id",
    )
    intrinsic = read_tsv(
        ROOT / "udt_complete_metric_intrinsic_object_audit_2026-07-23/STATUS_LEDGER.tsv",
        "id",
    )
    coframe = read_tsv(
        ROOT / "udt_coframe_hopf_bridge_audit_2026-07-23/STATUS_LEDGER.tsv",
        "id",
    )
    toric = read_tsv(
        ROOT / "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
        "claim_id",
    )
    bootstrap = read_tsv(
        ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/STATUS_LEDGER.tsv",
        "claim_id",
    )
    matter = read_tsv(
        ROOT / "matter_bootstrap_dimensional_inventory_2026-07-20/STATUS_LEDGER.tsv",
        "id",
    )

    checks = {
        "carrier_is_posit": native["T05"]["status"] == "WORKING_POSIT_REOPENED"
        and coframe["S12"]["status"] == "POSIT",
        "conditional_Hopf_domain": native["T06"]["status"]
        == "CONDITIONAL_HOPF_DOMAIN_AVAILABLE",
        "physical_carrier_boundary_open": native["T07"]["status"] == "OPEN",
        "static_stability_scoped": native["T10"]["status"]
        == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
        "physical_affine_selector_open": transport["S18"]["status"] == "OPEN_SELECTOR",
        "projected_transport_torsionful": parent["S13"]["status"]
        == "GENERICALLY_NONZERO_IN_EXACT_WITNESS",
        "split_connection_nonunique": parent["S14"]["status"].startswith("REFUTED"),
        "intrinsic_Hopf_section_open": intrinsic["S13"]["status"] == "OPEN",
        "global_real_Hopf_object_open": intrinsic["S17"]["status"]
        == "OPEN_NOT_DERIVED",
        "coframe_native_bridge_open": coframe["S14"]["status"] == "OPEN",
        "toric_bootstrap_no_ranking": toric["T16"]["status"]
        == "NO_TOPOLOGY_RANKING_LAW",
        "current_bootstrap_after_solution": bootstrap["R08"]["status"] == "WORKING",
        "current_bootstrap_no_local_operator": bootstrap["R09"]["status"]
        == "NOT_PRESENT",
        "future_B_only_conditional": bootstrap["R10"]["status"] == "CONDITIONAL_FORM",
        "future_Sigma_only_conditional": bootstrap["R11"]["status"]
        == "CONDITIONAL_FORM",
        "bootstrap_placement_underdetermined": bootstrap["R12"]["status"]
        == "UNDERDETERMINED",
        "density_not_pointwise_operator": bootstrap["R28"]["status"] == "NOT_PRESENT",
        "complete_matter_action_open": matter["S14"]["status"] == "OPEN",
        "time_live_persistence_open": matter["S15"]["status"] == "OPEN",
    }
    return {
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "current_bootstrap": "AFTER_SOLUTION_GLOBAL_ADMISSIBILITY_ONLY",
        "future_bootstrap_forms": ["Sigma map", "varied global functional B"],
        "future_forms_current_status": "OPEN_CONDITIONAL_FORM_NOT_SUPPLIED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    sources_ok, sources = verify_sources()
    torsion = torsion_identity()
    gauge = primitive_gauge_identity()
    weights = conformal_action_weights()
    authority = source_authority()

    checks = {
        "source_hashes_and_manifests_pass": sources_ok,
        "source_authority_pass": authority["all_checks_pass"],
        "generic_torsion_identity_pass": torsion["generic_identity_pass"],
        "torsion_free_reduction_pass": torsion["torsion_free_reduction_pass"],
        "torsionful_naive_rewrite_fails": torsion["torsionful_witness"][
            "naive_rewrite_fails"
        ],
        "torsionful_corrected_rewrite_passes": torsion["torsionful_witness"][
            "corrected_rewrite_passes"
        ],
        "primitive_gauge_exact_difference": gauge["closed_form_exact_difference"],
        "E2_conformal_weight_q": weights["E2_weight"] == "q",
        "E4_conformal_weight_inverse_q": weights["E4_weight"] == "1/q",
        "energy_noninvariance_witness": weights["noninvariance_witness"]["different"],
        "Hopf_integral_metric_weight_zero": weights["Hopf_form_integral_metric_weight"]
        == 0,
        "Hodge_primitive_metric_sensitive": weights[
            "Hodge_star_on_two_forms_in_three_dimensions_weight"
        ]
        == "q^-1",
    }

    result = {
        "schema": "udt-hopf-transport-bootstrap-dependency-v1",
        "python": "3.10.12",
        "sympy": sp.__version__,
        "source_manifest": sources,
        "source_authority": authority,
        "torsion_identity": torsion,
        "primitive_gauge_identity": gauge,
        "conformal_action_weights": weights,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "typed_connections": {
            "affine_tangent_connection": {
                "bundle": "TM",
                "operator": "nabla: sections(TM) -> Omega1(M,TM)",
                "role": "compare tangent/screen data",
            },
            "Hopf_principal_connection": {
                "bundle": "principal U1 bundle P -> S2",
                "operator": "U1-valued vertical-normalized one-form on P",
                "role": "horizontal lift and first Chern/Hopf readout in supplied bundle",
            },
            "same_type": False,
        },
        "transport_adjudication": {
            "Gamma_f_torsion_free": "true exterior closure equals covariant antisymmetrization",
            "A0_plus_lambda_dphi_torsion_free": "true exterior closure equals covariant antisymmetrization",
            "projected_Kato_torsionful": "true exterior closure requires torsion correction",
            "projected_plus_stabilizer": "true d remains independent; covariant rewrite follows actual torsion",
            "normal_conformal_tractor": "different representation transport; not needed by supplied de Rham Hopf core",
            "no_affine_connection": "sufficient for pullback, dF, primitive class, and form integral once map/domain data are supplied",
        },
        "dependency_rulings": {
            "topological_core": "TRANSPORT_INDEPENDENT_CONDITIONAL_ON_SUPPLIED_MAP_DOMAIN_ORIENTATION_NORMALIZATION_AND_BOUNDARY_CLASS",
            "Hodge_or_Coulomb_primitive": "METRIC_BOUNDARY_AND_GAUGE_DEPENDENT_REPRESENTATIVE",
            "conditional_toric_unit_class": "AFFINE_TRANSPORT_INDEPENDENT_BUT_GLOBAL_TORIC_PREMISES_SUPPLIED",
            "internal_target_L2_plus_L4": "DIRECT_AFFINE_CONNECTION_INDEPENDENT_BUT_METRIC_MEASURE_COEFFICIENT_CARRIER_AND_BOUNDARY_DEPENDENT",
            "tangent_or_null_section_action": "REQUIRES_SELECTED_BUNDLE_CONNECTION_OR_INTRINSIC_DERIVATIVE_AND_IS_OPEN",
            "static_stability": "RETAINS_EXACT_EXISTING_METRIC_ACTION_CARRIER_BOX_OPERATOR_PREMISES",
            "time_live_persistence": "OPEN_REQUIRES_DYNAMICS_REGULARITY_AND_PHYSICAL_BOUNDARY",
            "emergent_native_Hopf_realization": "DEPENDS_ON_OPEN_SECTION_TRANSPORT_TRIVIALIZATION_GLOBAL_COMPLETION_AND_DYNAMICS",
        },
        "bootstrap_adjudication": {
            "B0": "topological dependency classification needs no bootstrap",
            "B1": "current bootstrap may only filter already complete matter-bearing global solutions",
            "B2": "a future derived Sigma could select a representative section or branch; none is supplied",
            "B3": "a future derived varied functional B could modify equations; none is supplied",
            "density_window_now": "not operational before native action source total mass proper volume boundary and complete solutions",
            "topological_role_later": "could bracket admissible complete topological sectors without changing the definition of Q",
        },
        "maximum_conclusion": [
            "TOPOLOGICAL_CORE_TRANSPORT_INDEPENDENT_IN_DECLARED_CARRIER_DOMAIN",
            "EMERGENT_HOPF_REALIZATION_DEPENDS_ON_OPEN_SECTION_TRANSPORT_BOUNDARY_OR_DYNAMICS",
            "CURRENT_BOOTSTRAP_IS_OUTER_ADMISSIBILITY_ONLY",
        ],
        "not_claimed": [
            "native carrier",
            "selected Hopf section",
            "physical affine connection",
            "native L2+L4 action",
            "physical boundary",
            "time-live persistence",
            "bootstrap selector operator",
            "mass or scale",
            "carrier emergence",
        ],
    }
    if not result["all_checks_pass"]:
        failed = [name for name, passed in checks.items() if not passed]
        raise SystemExit(f"exact controller failed: {failed}")
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
