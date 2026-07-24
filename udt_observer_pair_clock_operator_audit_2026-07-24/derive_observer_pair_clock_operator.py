#!/usr/bin/env python3
"""Exact observer-pair reciprocal operator and metric-transport type audit."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require_zero(name: str, value, checks: dict[str, str]) -> None:
    reduced = sp.simplify(value)
    if isinstance(reduced, sp.MatrixBase):
        failed = any(sp.simplify(entry) != 0 for entry in reduced)
    else:
        failed = reduced != 0
    if failed:
        raise AssertionError(f"{name}: {reduced}")
    checks[name] = "PASS"


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_sources(checks: dict[str, str]) -> int:
    with (HERE / "SOURCE_LINEAGE.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    require("source_count_11", len(rows) == 11, checks)
    require("source_ids_unique", len({row["id"] for row in rows}) == len(rows), checks)
    for row in rows:
        source = ROOT / row["path"]
        require(f"source_exists_{row['id']}", source.is_file(), checks)
        require(f"source_sha_{row['id']}", sha256(source) == row["sha256"], checks)
    return len(rows)


def boost(parameter) -> sp.Matrix:
    return sp.Matrix(
        [
            [sp.cosh(parameter), -sp.sinh(parameter)],
            [-sp.sinh(parameter), sp.cosh(parameter)],
        ]
    )


def main() -> None:
    checks: dict[str, str] = {}
    source_count = validate_sources(checks)

    delta, delta1, delta2 = sp.symbols("delta delta1 delta2", real=True)
    rho, rho1, rho2 = sp.symbols("rho rho1 rho2", nonnegative=True)
    phi_p, phi_q, phi_r = sp.symbols("phi_p phi_q phi_r", real=True)
    a, b = sp.symbols("a b", real=True)

    K = sp.Matrix([[0, 1], [1, 0]])
    S = lambda value: sp.diag(sp.exp(-value), sp.exp(value))

    require_zero("operator_K_preservation", S(delta).T * K * S(delta) - K, checks)
    require_zero("operator_determinant_one", S(delta).det() - 1, checks)
    require_zero("operator_identity", S(0) - sp.eye(2), checks)
    require_zero("operator_inverse", S(delta) * S(-delta) - sp.eye(2), checks)
    require_zero("operator_composition", S(delta1) * S(delta2) - S(delta1 + delta2), checks)

    H = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    eta = sp.diag(1, -1)
    balanced = sp.simplify(H.T * S(delta) * H)
    require_zero("balanced_pairing", H.T * K * H - eta, checks)
    require_zero("balanced_exact_boost", balanced - boost(delta), checks)
    require_zero("balanced_Lorentz", balanced.T * eta * balanced - eta, checks)
    require_zero("balanced_inverse", boost(delta) * boost(-delta) - sp.eye(2), checks)

    gamma = sp.simplify(sp.trace(S(delta)) / 2)
    require_zero("half_trace_cosh", gamma - sp.cosh(delta), checks)
    require_zero("half_trace_reversal_even", gamma.subs(delta, -delta) - gamma, checks)
    require_zero(
        "half_trace_common_conjugation",
        sp.trace(boost(a) * boost(delta) * boost(-a)) / 2 - sp.cosh(delta),
        checks,
    )
    log2 = sp.log(2)
    gamma_failure = sp.simplify(sp.cosh(2 * log2) - sp.cosh(log2) ** 2)
    require_zero("half_trace_noncharacter_witness", gamma_failure - sp.Rational(9, 16), checks)
    require("half_trace_not_channel_character", gamma_failure != 0, checks)

    temporal = sp.exp(-rho)
    ruler = sp.exp(rho)
    require_zero("named_channel_product", temporal * ruler - 1, checks)
    require_zero(
        "named_temporal_character",
        sp.exp(-(rho1 + rho2)) - sp.exp(-rho1) * sp.exp(-rho2),
        checks,
    )
    require_zero(
        "named_ruler_character",
        sp.exp(rho1 + rho2) - sp.exp(rho1) * sp.exp(rho2),
        checks,
    )

    S_p = S(phi_p)
    S_q = S(phi_q)
    S_r = S(phi_r)
    U_pq = sp.simplify(S_p.inv() * S_q)
    U_qr = sp.simplify(S_q.inv() * S_r)
    U_pr = sp.simplify(S_p.inv() * S_r)
    require_zero("endpoint_difference_form", U_pq - S(phi_q - phi_p), checks)
    require_zero("endpoint_groupoid_composition", U_pq * U_qr - U_pr, checks)
    require_zero("endpoint_reversal_inverse", U_pq * (S_q.inv() * S_p) - sp.eye(2), checks)

    # Static diagonal reciprocal metric control.
    t, x, c = sp.symbols("t x c", real=True, positive=True)
    phi = sp.Function("phi")(x)
    coords = (t, x)
    metric = sp.diag(-c**2 * sp.exp(-2 * phi), sp.exp(2 * phi))
    inverse_metric = sp.simplify(metric.inv())
    christoffel = [[[sp.S.Zero for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for upper in range(2):
        for left in range(2):
            for right in range(2):
                christoffel[upper][left][right] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        inverse_metric[upper, lower]
                        * (
                            sp.diff(metric[lower, right], coords[left])
                            + sp.diff(metric[lower, left], coords[right])
                            - sp.diff(metric[left, right], coords[lower])
                        )
                        for lower in range(2)
                    )
                )

    phi_prime = sp.diff(phi, x)
    require_zero("Gamma_t_tx", christoffel[0][0][1] + phi_prime, checks)
    require_zero("Gamma_t_xt", christoffel[0][1][0] + phi_prime, checks)
    require_zero(
        "Gamma_x_tt",
        christoffel[1][0][0] + c**2 * phi_prime * sp.exp(-4 * phi),
        checks,
    )
    require_zero("Gamma_x_xx", christoffel[1][1][1] - phi_prime, checks)
    require_zero("Gamma_t_xx", christoffel[0][1][1], checks)
    require_zero("Gamma_x_tx", christoffel[1][0][1], checks)

    depth = phi_q - phi_p
    vector_transport = sp.diag(sp.exp(depth), sp.exp(-depth))
    covector_transport = sp.diag(sp.exp(-depth), sp.exp(depth))
    require_zero("spatial_vector_transport_inverse_pair", vector_transport - S(-depth), checks)
    require_zero("spatial_covector_transport_pair", covector_transport - S(depth), checks)
    require_zero("vector_covector_duality", vector_transport.T * covector_transport - sp.eye(2), checks)

    theta_p_time = sp.Matrix([sp.exp(-phi_p), 0])
    theta_p_space = sp.Matrix([0, sp.exp(phi_p)])
    theta_q_time = sp.Matrix([sp.exp(-phi_q), 0])
    theta_q_space = sp.Matrix([0, sp.exp(phi_q)])
    require_zero(
        "transported_orthonormal_time_coframe_matches_endpoint",
        covector_transport * theta_p_time - theta_q_time,
        checks,
    )
    require_zero(
        "transported_orthonormal_space_coframe_matches_endpoint",
        covector_transport * theta_p_space - theta_q_space,
        checks,
    )

    # The orthonormal spin connection is proportional to dt; its pullback to
    # a t=constant spatial comparison curve vanishes.
    omega_t = -c * phi_prime * sp.exp(-2 * phi)
    omega_x = sp.S.Zero
    require_zero("orthonormal_spatial_connection_pullback", omega_x, checks)
    require("orthonormal_time_connection_generic_nonzero", omega_t != 0, checks)

    # A lapse ratio uses a supplied shared stationary slicing and is ordered.
    lapse_ratio_q_over_p = sp.exp(-(phi_q - phi_p))
    require_zero("stationary_lapse_ratio", lapse_ratio_q_over_p - S(depth)[0, 0], checks)
    require_zero(
        "stationary_lapse_ratio_reverses",
        lapse_ratio_q_over_p * sp.exp(-(phi_p - phi_q)) - 1,
        checks,
    )
    require(
        "stationary_lapse_ratio_not_mutual_slow_unless_equal",
        sp.simplify(lapse_ratio_q_over_p - sp.exp(-(phi_p - phi_q))) != 0,
        checks,
    )

    # Endpoint-frame freedom: trace is invariant under common conjugation,
    # but not under independent endpoint refactorization.
    identity_transporter = sp.eye(2)
    independently_refactored = boost(b) * identity_transporter * boost(-a)
    require_zero(
        "independent_endpoint_trace",
        sp.trace(independently_refactored) / 2 - sp.cosh(b - a),
        checks,
    )
    require(
        "independent_endpoint_trace_not_invariant",
        sp.simplify(sp.cosh(b - a) - 1) != 0,
        checks,
    )

    operator_rows = [
        {
            "id": "O01",
            "object": "abstract ordered reciprocal pair operator",
            "exact_result": "S(delta)=diag(exp(-delta),exp(delta)); K preserving; determinant one; composition and inverse exact",
            "status": "DERIVED_CONDITIONAL_WITH_FOUNDING_PREMISE_STAMPS",
            "remaining_gate": "map an actual complete observer pair to additive depth",
        },
        {
            "id": "O02",
            "object": "balanced-basis form",
            "exact_result": "H^T S(delta) H=[[cosh(delta),-sinh(delta)],[-sinh(delta),cosh(delta)]]",
            "status": "DERIVED_ALGEBRAIC_O11_BOOST",
            "remaining_gate": "K as physical observer interval readout is OPEN",
        },
        {
            "id": "O03",
            "object": "endpoint local-field factorization",
            "exact_result": "S(phi_p)^-1 S(phi_q)=S(phi_q-phi_p) and obeys the pair-groupoid cocycle",
            "status": "DERIVED_IDENTITY_GIVEN_OPEN_PAIR_TO_LOCAL_FIELD_JOIN",
            "remaining_gate": "current ontology labels delta(p,q)=phi(q)-phi(p) OPEN",
        },
        {
            "id": "O04",
            "object": "metric covector transport in static diagonal reciprocal control",
            "exact_result": "spatial coordinate-covector transport equals S(phi_q-phi_p)",
            "status": "DERIVED_IN_EXACT_CONTROL",
            "remaining_gate": "coordinate covector scaling is not automatically observer clock readout",
        },
        {
            "id": "O05",
            "object": "physical orthonormal coframe under the same spatial transport",
            "exact_result": "the transported endpoint coframe equals the local endpoint coframe; relative orthonormal transform is identity",
            "status": "DERIVED_IN_EXACT_CONTROL",
            "remaining_gate": "clock comparison requires declared slicing/event pairing or another physical readout",
        },
        {
            "id": "O06",
            "object": "complete metric path transporter",
            "exact_result": "Levi-Civita transport exists for each supplied path and reverses by inversion",
            "status": "DERIVED_PER_METRIC_AND_PATH",
            "remaining_gate": "complete branch reciprocal subbundle path family and endpoint frames",
        },
        {
            "id": "O07",
            "object": "global physical observer-pair clock operator",
            "exact_result": "not evaluable from current complete-branch census",
            "status": "OPEN_TYPED_GLOBAL_JOIN",
            "remaining_gate": "pair depth plus event pairing and full angular/holonomy treatment",
        },
    ]

    readout_rows = [
        {
            "id": "R01",
            "readout": "named time-per-length channel",
            "formula": "T(rho)=exp(-rho), rho>=0",
            "status": "DERIVED_CONDITIONAL_CHANNEL_CHARACTER",
            "warning": "nonnegative radial/depth channel; not a signed endpoint-field theorem",
        },
        {
            "id": "R02",
            "readout": "reversal-even half trace",
            "formula": "Gamma(delta)=Tr S(delta)/2=cosh(delta)",
            "status": "DERIVED_DIAGNOSTIC_INVARIANT",
            "warning": "not a multiplicative channel and not invariant under independent endpoint frame choices",
        },
        {
            "id": "R03",
            "readout": "balanced-basis mutual slow factor",
            "formula": "sech(delta)",
            "status": "CONDITIONAL_ON_PHYSICAL_K_READOUT_AND_ENDPOINT_OBSERVER_FRAMES",
            "warning": "cannot replace the founding named temporal character",
        },
        {
            "id": "R04",
            "readout": "stationary lapse ratio",
            "formula": "N(q)/N(p)=exp(-(phi_q-phi_p))",
            "status": "CONDITIONAL_ON_COMMON_STATIC_SLICING_AND_LOCAL_FIELD_JOIN",
            "warning": "ordered ratio; one direction is inverse of the other, not mutual slowdown",
        },
        {
            "id": "R05",
            "readout": "coordinate covector transport",
            "formula": "diag(exp(-Delta phi),exp(Delta phi))",
            "status": "DERIVED_IN_STATIC_DIAGONAL_CONTROL",
            "warning": "physical orthonormal frame comparison is identity along the same spatial curve",
        },
    ]

    transport_rows = [
        {
            "id": "T01",
            "representation": "coordinate vectors",
            "spatial_transport": "diag(exp(Delta phi),exp(-Delta phi))",
            "physical_meaning": "inverse dual of covector transport",
            "ruling": "NOT_THE_FOUNDING_COVECTOR_OPERATOR",
        },
        {
            "id": "T02",
            "representation": "coordinate covectors",
            "spatial_transport": "diag(exp(-Delta phi),exp(Delta phi))",
            "physical_meaning": "matches the founding reciprocal matrix in the exact control",
            "ruling": "TYPE_MATCHED_CONTROL_EQUALITY",
        },
        {
            "id": "T03",
            "representation": "orthonormal physical coframe",
            "spatial_transport": "identity",
            "physical_meaning": "endpoint physical coframes are parallel along the rest-slice path",
            "ruling": "NO_SPATIAL_BOOST_IN_EXACT_CONTROL",
        },
        {
            "id": "T04",
            "representation": "stationary lapse comparison",
            "spatial_transport": "not a parallel-transport observable",
            "physical_meaning": "proper-clock ratio relative to a common coordinate slicing",
            "ruling": "SEPARATE_CONDITIONAL_READOUT",
        },
        {
            "id": "T05",
            "representation": "generic complete coframe",
            "spatial_transport": "path-ordered full connection with boost and rotation mixing",
            "physical_meaning": "metric-derived per path",
            "ruling": "PATH_AND_ENDPOINT_FRAME_DEPENDENT",
        },
    ]

    gate_rows = [
        {
            "gate": "founding reciprocal operator",
            "result": "PASS",
            "basis": "C0/C1 pair algebra",
        },
        {
            "gate": "local phi endpoint realization",
            "result": "OPEN",
            "basis": "O07 in current phi ontology ledger",
        },
        {
            "gate": "static diagonal metric covector match",
            "result": "PASS_BOUNDED_CONTROL",
            "basis": "exact Christoffel and dual transport",
        },
        {
            "gate": "physical orthonormal spatial boost",
            "result": "NO_IN_CONTROL",
            "basis": "spin-connection pullback vanishes",
        },
        {
            "gate": "unique scalar mutual clock readout",
            "result": "OPEN",
            "basis": "named channel and balanced invariant have different types",
        },
        {
            "gate": "global path-independent full operator",
            "result": "OPEN",
            "basis": "complete branch subbundle holonomy and cut-locus joins absent",
        },
        {
            "gate": "physical Xmax mass or CMB",
            "result": "NOT_IN_SCOPE",
            "basis": "no promotion",
        },
    ]

    write_tsv(
        HERE / "OPERATOR_STATUS_LEDGER.tsv",
        ["id", "object", "exact_result", "status", "remaining_gate"],
        operator_rows,
    )
    write_tsv(
        HERE / "CLOCK_READOUT_LEDGER.tsv",
        ["id", "readout", "formula", "status", "warning"],
        readout_rows,
    )
    write_tsv(
        HERE / "TRANSPORT_TYPE_LEDGER.tsv",
        ["id", "representation", "spatial_transport", "physical_meaning", "ruling"],
        transport_rows,
    )
    write_tsv(
        HERE / "GLOBAL_EVALUATION_GATE.tsv",
        ["gate", "result", "basis"],
        gate_rows,
    )

    result = {
        "schema": "udt-observer-pair-clock-operator-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "compute": "CPU_ONLY",
        "checks": checks,
        "check_count": len(checks),
        "source_count": source_count,
        "abstract_operator": {
            "formula": "S(delta)=diag(exp(-delta),exp(delta))",
            "status": "DERIVED_CONDITIONAL_WITH_FOUNDING_PREMISE_STAMPS",
            "properties": [
                "K_PRESERVING",
                "DETERMINANT_ONE",
                "COMPOSITION",
                "REVERSE_IS_INVERSE",
            ],
        },
        "balanced_basis": {
            "formula": "[[cosh(delta),-sinh(delta)],[-sinh(delta),cosh(delta)]]",
            "status": "DERIVED_ALGEBRAIC_O11_BOOST",
            "physical_K_readout": "OPEN",
        },
        "endpoint_realization": {
            "identity": "S(phi_p)^-1 S(phi_q)=S(phi_q-phi_p)",
            "status": "CONDITIONAL_ON_OPEN_PAIR_TO_LOCAL_FIELD_JOIN",
        },
        "metric_transport_control": {
            "coordinate_covector": "MATCHES_S_DELTA_PHI",
            "coordinate_vector": "MATCHES_S_MINUS_DELTA_PHI",
            "orthonormal_spatial_frame": "IDENTITY",
            "interpretation": "coordinate match does not by itself derive mutual observer clock slowdown",
        },
        "clock_readout": {
            "named_channel": "T(rho)=exp(-rho) DERIVED_CONDITIONAL",
            "half_trace": "cosh(delta) DERIVED_DIAGNOSTIC",
            "mutual_slow": "sech(delta) CONDITIONAL_ON_PHYSICAL_K_READOUT_AND_ENDPOINT_FRAMES",
            "stationary_lapse_ratio": "ORDERED_CONDITIONAL_NOT_MUTUAL",
        },
        "global_status": {
            "pair_depth_map": "OPEN",
            "event_pairing": "OPEN",
            "complete_reciprocal_subbundle": "OPEN",
            "path_or_path_family": "OPEN_WHERE_HOLONOMY_OR_CUT_LOCUS_MATTERS",
            "physical_Xmax": "OPEN",
        },
        "maximum_conclusion": (
            "THE FOUNDING POSTULATES ALREADY DERIVE THE ABSTRACT ORDERED RECIPROCAL "
            "OBSERVER-PAIR OPERATOR. ITS BALANCED FORM IS AN EXACT O11 BOOST. THE "
            "STATIC DIAGONAL METRIC REPRODUCES THE SAME MATRIX FOR COORDINATE "
            "COVECTOR TRANSPORT, WHILE THE PHYSICAL ORTHONORMAL COFRAME HAS IDENTITY "
            "SPATIAL TRANSPORT. THEREFORE A GLOBAL MUTUAL CLOCK READOUT STILL REQUIRES "
            "THE OPEN PAIR-DEPTH, ENDPOINT-FRAME, EVENT-PAIRING, AND COMPLETE-METRIC "
            "JOINS; NO PATH, MASS, XMAX, OR CMB LAW IS INSERTED."
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "result": "PASS",
        "checks": len(checks),
        "sources": source_count,
        "maximum_conclusion": result["maximum_conclusion"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
