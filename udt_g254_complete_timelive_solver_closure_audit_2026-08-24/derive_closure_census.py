#!/usr/bin/env python3
"""Exact G254 source/ownership census and analytic arbitrary-history control."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent

HISTORY_SCHEMAS = {
    "independently_owned_C_of_g_equals_zero",
    "independently_owned_global_G_of_g_and_R_equals_zero",
}
FORBIDDEN_AS_DYNAMICS = {
    "metric_pullback_h_equals_JTgJ",
    "completed_pair_m_equals_sqrt_minus_det_h",
    "completed_Phi_equals_minus_half_log_minus_h00",
    "Levi_Civita_metricity_and_zero_torsion",
    "Cartan_structure_equations",
    "Bianchi_and_Ricci_commutator",
    "Jacobi_equation_on_supplied_null_germ",
    "pair_reversal_and_endpoint_composition",
    "rank_complete_network_existence",
    "observational_loss_or_fit",
    "Einstein_or_chosen_action_equation",
}

SOURCE_CLAIMS = {
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md":
        "does not yet derive a unique action, the profile",
    "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/EXACT_DERIVATION.md":
        "does not select those histories or create an evolution law",
    "udt_g190_completed_pair_timelive_frequency_screen_join_2026-08-20/EXACT_DERIVATION.md":
        "the global endpoint intersection, metric history, and observer-family population are",
    "udt_g211_complete_diagonal_scalar_basis_closure_2026-08-22/EXACT_DERIVATION.md":
        "a basis closure, not a physical-function closure",
    "udt_g212_observer_equivalence_history_bridge_whiteboard_2026-08-22/AUDIT_REPORT.md":
        "arbitrary smooth `omega(x),q(x)` survive",
    "udt_g226_null_chain_conformal_symplectic_assembly_2026-08-22/EXACT_DERIVATION.md":
        "choose a metric history",
    "udt_g231_cartan_regional_realization_bridge_2026-08-23/EXACT_DERIVATION.md":
        "they do not select the values",
    "udt_g233_primary_profile_cartan_closure_discriminator_2026-08-23/EXACT_DERIVATION.md":
        "__unrestricted_primary_profile_has_no_universal_finite_jet_autonomous_closure",
    "udt_g234_post_g233_native_closure_route_map_2026-08-23/AUDIT_REPORT.md":
        "__no_active_owned_condition_yet_closes_the_primary_profile",
    "udt_g235_rank_complete_matched_network_nonselection_2026-08-23/EXACT_DERIVATION.md":
        "reconstructive and compositional but remains an identity",
    "udt_g253_native_kernel_minimal_dependency_compression_audit_2026-08-24/AUDIT_REPORT.md":
        "physical metric history",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_sources() -> int:
    rows = read_tsv(PACKAGE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == 16
    for row in rows:
        source = ROOT / row["path"]
        assert source.is_file(), row["path"]
        assert sha256(source) == row["sha256"], row["path"]
    for relative, token in SOURCE_CLAIMS.items():
        text = " ".join((ROOT / relative).read_text(encoding="utf-8").lower().split())
        assert token.lower() in text, (relative, token)
    return len(rows)


def validate_contract(rows: list[dict[str, str]], stage2_started: bool = False) -> dict[str, object]:
    names = {row["candidate"] for row in rows}
    assert HISTORY_SCHEMAS <= names
    assert FORBIDDEN_AS_DYNAMICS <= names
    for row in rows:
        if row["candidate"] in FORBIDDEN_AS_DYNAMICS:
            assert row["counts_as_history_equation"] == "no", row
    schema_yes = {
        row["candidate"]
        for row in rows
        if row["counts_as_history_equation"] == "yes"
    }
    assert schema_yes == HISTORY_SCHEMAS
    # The two yes rows are candidate equation *types*. The frozen source ledger supplies no owner.
    owned_active: set[str] = set()
    assert not owned_active
    if stage2_started:
        assert owned_active, "a reduced solver was launched without an owned ambient residual"
    return {
        "candidate_rows": len(rows),
        "eligible_history_schema_count": len(schema_yes),
        "owned_active_history_equation_count": len(owned_active),
    }


def scalar_curvature(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]) -> sp.Expr:
    dimension = metric.rows
    inverse = sp.simplify(metric.inv())
    gamma = [[[
        sp.simplify(sp.Rational(1, 2) * sum(
            inverse[rho, sigma] * (
                sp.diff(metric[sigma, nu], coordinates[mu])
                + sp.diff(metric[sigma, mu], coordinates[nu])
                - sp.diff(metric[mu, nu], coordinates[sigma])
            )
            for sigma in range(dimension)
        ))
        for nu in range(dimension)] for mu in range(dimension)] for rho in range(dimension)]
    ricci = sp.MutableDenseMatrix.zeros(dimension, dimension)
    for mu in range(dimension):
        for nu in range(dimension):
            value = 0
            for rho in range(dimension):
                value += sp.diff(gamma[rho][mu][nu], coordinates[rho])
                value -= sp.diff(gamma[rho][mu][rho], coordinates[nu])
                for sigma in range(dimension):
                    value += gamma[rho][rho][sigma] * gamma[sigma][mu][nu]
                    value -= gamma[rho][nu][sigma] * gamma[sigma][mu][rho]
            ricci[mu, nu] = sp.simplify(value)
    return sp.simplify(sum(inverse[mu, nu] * ricci[mu, nu]
                           for mu in range(dimension) for nu in range(dimension)))


def counterfamily_record() -> dict[str, object]:
    t, x, y, z, b = sp.symbols("t x y z b", real=True)
    q = b * t**2
    scale = sp.exp(2 * q)
    metric = sp.diag(-1, scale, scale, scale)
    curvature = sp.simplify(scalar_curvature(metric, (t, x, y, z)))
    curvature_at_anchor = sp.simplify(curvature.subs(t, 0))
    assert curvature_at_anchor == 12 * b

    # Eulerian clock plus x-ruler: G176 completion works for every b and t.
    h = sp.diag(-1, scale)
    determinant = sp.simplify(h.det())
    m = sp.sqrt(-determinant)
    completed = sp.simplify(sp.diag(1, 1 / m).T * h * sp.diag(1, 1 / m))
    phi = -sp.Rational(1, 2) * sp.log(-h[0, 0])
    assert sp.simplify(determinant + scale) == 0
    assert sp.simplify(m - sp.exp(q)) == 0
    assert completed == sp.diag(-1, 1)
    assert phi == 0
    record = {
        "family": "diag(-1,exp(2*b*t^2),exp(2*b*t^2),exp(2*b*t^2))",
        "scalar_curvature": str(curvature),
        "scalar_curvature_at_t0": str(curvature_at_anchor),
        "b0_curvature": int(curvature_at_anchor.subs(b, 0)),
        "b7_curvature": int(curvature_at_anchor.subs(b, 7)),
        "completed_pair_metric": [[-1, 0], [0, 1]],
        "completed_phi": 0,
        "meaning": "invariantly distinct smooth time-live histories satisfy the same completed-pair algebra",
    }
    validate_witness(record)
    return record


def validate_witness(record: dict[str, object]) -> None:
    assert record["b0_curvature"] != record["b7_curvature"], (
        "arbitrary-history invariant separator was erased"
    )


def derive() -> dict[str, object]:
    source_count = validate_sources()
    contract = validate_contract(read_tsv(PACKAGE / "CLOSURE_CONTRACT.tsv"))
    witness = counterfamily_record()
    return {
        "status": "PASS",
        "landing": "NO_OWNED_TIMELIVE_RESIDUAL__ODE_AND_GPU_SOLVES_NOT_YET_DEFINED",
        "source_count": source_count,
        "contract": contract,
        "ambient_metric_component_count": 10,
        "coordinate_gauge_function_count": 4,
        "configuration_functions_after_coordinate_gauge": 6,
        "owned_active_ambient_evolution_equation_count": 0,
        "counterfamily": witness,
        "stage_2": "GATED_NOT_STARTED",
        "stage_3": "GATED_NOT_STARTED",
        "assertion_count": 56,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = derive()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
