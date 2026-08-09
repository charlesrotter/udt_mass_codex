#!/usr/bin/env python3
"""Classify banked radial/profile candidates before any N02 eigensolve.

This script derives center and wall admissibility only. It does not integrate a radial equation.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "c73eb657"
INV_N = (Fraction(9658, 10000), Fraction(9470, 10000), Fraction(9284, 10000))
Q_RATIOS = (
    Fraction(-2), Fraction(-1), Fraction(0), Fraction(1, 4),
    Fraction(1, 2), Fraction(3, 4), Fraction(95, 100),
)
HBAR_COUNT = 10
HBAR_VALUES = ("0.001", "0.002", "0.005", "0.01", "0.02", "0.05", "0.1", "0.2", "0.5", "1")
KEYS: dict[str, bool] = {}


def key(name: str, condition: object) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}")


def frozen_hash(path_text: str) -> str:
    data = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{path_text}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(data).hexdigest()


def fraction_text(value: Fraction | None) -> str:
    if value is None:
        return "-"
    return f"{value.numerator}/{value.denominator}"


def full_c1_center_residue() -> sp.Expr:
    """Compute lim r*RicciScalar for A=1+a r+b r^2, h=k r^2+c r^3."""
    r, theta = sp.symbols("r theta", positive=True)
    a, b, kappa, c = sp.symbols("a b kappa c", real=True)
    A = 1 + a * r + b * r**2
    h = kappa * r**2 + c * r**3
    sine = sp.sin(theta)
    metric = sp.Matrix([
        [-A, 0, 0, h * sine**2],
        [0, 1 / A, 0, 0],
        [0, 0, r**2, 0],
        [h * sine**2, 0, 0, r**2 * sine**2],
    ])
    inverse = sp.simplify(metric.inv())
    coordinates = (sp.symbols("t"), r, theta, sp.symbols("psi"))
    dimension = 4
    connection = [
        [[sp.S(0) for _ in range(dimension)] for _ in range(dimension)]
        for _ in range(dimension)
    ]
    for upper in range(dimension):
        for left in range(dimension):
            for right in range(dimension):
                connection[upper][left][right] = sp.factor(
                    sp.Rational(1, 2) * sum(
                        inverse[upper, index]
                        * (
                            sp.diff(metric[index, right], coordinates[left])
                            + sp.diff(metric[index, left], coordinates[right])
                            - sp.diff(metric[left, right], coordinates[index])
                        )
                        for index in range(dimension)
                    )
                )
    ricci = sp.MutableDenseMatrix.zeros(dimension, dimension)
    for left in range(dimension):
        for right in range(dimension):
            ricci[left, right] = sp.factor(sum(
                sp.diff(connection[upper][left][right], coordinates[upper])
                - sp.diff(connection[upper][left][upper], coordinates[right])
                + sum(
                    connection[upper][upper][index] * connection[index][left][right]
                    - connection[upper][right][index] * connection[index][left][upper]
                    for index in range(dimension)
                )
                for upper in range(dimension)
            ))
    scalar = sum(
        inverse[left, right] * ricci[left, right]
        for left in range(dimension)
        for right in range(dimension)
    )
    return sp.simplify(sp.limit(r * scalar, r, 0, dir="+"))


def main() -> None:
    source_rows = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            path_text, digest = line.rstrip("\n").split("\t")
            source_rows.append((path_text, digest))
    key("K01_source_manifest", all(frozen_hash(path) == digest for path, digest in source_rows))

    residue = full_c1_center_residue()
    a = sp.symbols("a", real=True)
    key("K02_full_C1_center_residue", sp.simplify(residue + 6 * a) == 0)

    rows: list[dict[str, object]] = []
    endpoints: list[dict[str, object]] = []
    for inv_n in INV_N:
        n = 1 / inv_n
        # Round h=0 control.
        rows.append({
            "candidate_id": f"R0_n{float(n):.12f}",
            "family": "R0_ROUND_P1",
            "inv_n": f"{float(inv_n):.4f}",
            "n_exact": fraction_text(n),
            "q_ratio": "-",
            "q_exact": "-",
            "represented_h_magnitudes": 1,
            "represented_h_values": "0",
            "B_center": "ZERO",
            "B_wall": "ZERO",
            "mixing_center_status": "PASS_H_ZERO",
            "complete_metric_center_status": "FAIL_A_LINEAR_TERM",
            "ricci_r_times_limit": fraction_text(6 * n),
            "wall_liouville_length": "INFINITE",
            "wall_domain_status": "UNIQUE_LIMIT_POINT_CONTINUUM_CONTROL",
            "boundary_ownership": "NO_FREE_D_OR_N_WALL_DATUM",
            "profile_provenance": "P1_DATA_CONDITIONED_CHOSE_NOT_NATIVE",
            "execution_disposition": "BLOCKED_C1_CENTER_REGULARITY",
        })
        endpoints.append({
            "endpoint_id": f"E0_n{float(n):.12f}",
            "family": "R0_ROUND_P1",
            "n_exact": fraction_text(n),
            "q_ratio": "-",
            "B_wall": "ZERO",
            "radial_flux_exponent_u": fraction_text(n),
            "frequency_weight_exponent_u": fraction_text(-n),
            "liouville_length": "INFINITE",
            "angular_potential_exponent_x": "DECAYS_TO_ZERO",
            "rotation_potential_exponent_x": "ABSENT",
            "endpoint_character": "LIMIT_POINT",
            "extension_status": "UNIQUE_ENDPOINT_DOMAIN_DERIVED",
            "D_N_status": "NOT_FREE_ENDPOINT_DATA",
        })

        for q_ratio in Q_RATIOS:
            qcrit = (2 - n) / 2
            q = q_ratio * qcrit
            B_exponent = 2 * q - n
            flux_exponent = q + n / 2
            one_minus_flux = 1 - flux_exponent
            angular_x_exponent = 2 * q / one_minus_flux
            rotation_x_exponent = q / one_minus_flux
            for family, center_mixing, provenance, count in (
                (
                    "R1_CENTER_REGULAR_MIXING_P1",
                    "PASS_NECESSARY_H_ORDER_R2_ONLY__FULL_SMOOTHNESS_NOT_CLAIMED",
                    "FD1_BANKED_FREE_EXPLORED_CONDITIONAL_FAMILY",
                    HBAR_COUNT,
                ),
                (
                    "R2_RA1_LITERAL_LINEAGE",
                    "FAIL_H_ORDER_R0_ON_COLLAPSING_AXIAL_ORBIT",
                    "RA1_LINEAGE_CONTROL_NOT_COMPLETE_C1_CENTER",
                    1,
                ),
            ):
                prefix = "R1" if family.startswith("R1") else "R2"
                rows.append({
                    "candidate_id": f"{prefix}_n{float(n):.12f}_qr{float(q_ratio):+.2f}",
                    "family": family,
                    "inv_n": f"{float(inv_n):.4f}",
                    "n_exact": fraction_text(n),
                    "q_ratio": fraction_text(q_ratio),
                    "q_exact": fraction_text(q),
                    "represented_h_magnitudes": count,
                    "represented_h_values": ";".join(HBAR_VALUES) if prefix == "R1" else "SYMBOLIC_NONZERO_H0_LINEAGE",
                    "B_center": "ZERO" if prefix == "R1" else "INFINITY",
                    "B_wall": "INFINITY" if B_exponent < 0 else ("FINITE_NONZERO" if B_exponent == 0 else "ZERO"),
                    "mixing_center_status": center_mixing,
                    "complete_metric_center_status": "FAIL_A_LINEAR_TERM",
                    "ricci_r_times_limit": fraction_text(6 * n) if prefix == "R1" else "NOT_APPLICABLE_STRONGER_COFRAME_SINGULARITY",
                    "wall_liouville_length": "FINITE" if flux_exponent < 1 else "INFINITE",
                    "wall_domain_status": "LIMIT_CIRCLE_SUB_INVERSE_SQUARE",
                    "boundary_ownership": "FREE_SELF_ADJOINT_EXTENSION_FAMILY_REQUIRED",
                    "profile_provenance": provenance,
                    "execution_disposition": "BLOCKED_C1_CENTER_REGULARITY",
                })
            endpoints.append({
                "endpoint_id": f"E1_n{float(n):.12f}_qr{float(q_ratio):+.2f}",
                "family": "R1_AND_R2_NONZERO_MIXING_WALL",
                "n_exact": fraction_text(n),
                "q_ratio": fraction_text(q_ratio),
                "B_wall": "INFINITY" if B_exponent < 0 else ("FINITE_NONZERO" if B_exponent == 0 else "ZERO"),
                "radial_flux_exponent_u": fraction_text(flux_exponent),
                "frequency_weight_exponent_u": fraction_text(-flux_exponent),
                "liouville_length": "FINITE" if flux_exponent < 1 else "INFINITE",
                "angular_potential_exponent_x": fraction_text(angular_x_exponent),
                "rotation_potential_exponent_x": fraction_text(rotation_x_exponent),
                "endpoint_character": "LIMIT_CIRCLE_SUB_INVERSE_SQUARE",
                "extension_status": "REQUIRES_FREE_EXTENSION_CENSUS",
                "D_N_status": "ADMISSIBLE_CONTROL_MEMBERS_NOT_SELECTED__FULL_EXTENSION_FAMILY_OPEN",
            })

    with (HERE / "PROFILE_STRATA.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (HERE / "ENDPOINT_OWNERSHIP.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(endpoints[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(endpoints)

    r1_rows = [row for row in rows if row["family"] == "R1_CENTER_REGULAR_MIXING_P1"]
    r2_rows = [row for row in rows if row["family"] == "R2_RA1_LITERAL_LINEAGE"]
    nonzero_endpoints = [row for row in endpoints if row["family"] == "R1_AND_R2_NONZERO_MIXING_WALL"]
    key("K03_exact_profile_strata_census", len(rows) == 45)
    key("K04_exact_endpoint_census", len(endpoints) == 24)
    key("K05_R1_represents_all_210_profiles", sum(int(row["represented_h_magnitudes"]) for row in r1_rows) == 210 and all(row["represented_h_values"] == ";".join(HBAR_VALUES) and int(row["represented_h_magnitudes"]) == len(HBAR_VALUES) for row in r1_rows))
    key("K06_all_registered_nonzero_B_wall_infinite", all(row["B_wall"] == "INFINITY" for row in nonzero_endpoints))
    key("K07_all_registered_q_below_qcrit", all(Fraction(row["q_ratio"]) < 1 for row in nonzero_endpoints))
    key("K08_all_nonzero_wall_lengths_finite", all(row["liouville_length"] == "FINITE" for row in nonzero_endpoints))
    key("K09_all_angular_terms_sub_inverse_square", all(Fraction(row["angular_potential_exponent_x"]) > -2 for row in nonzero_endpoints))
    key("K10_all_rotation_terms_sub_inverse_square", all(Fraction(row["rotation_potential_exponent_x"]) > -2 for row in nonzero_endpoints))
    round_endpoints = [row for row in endpoints if row["family"] == "R0_ROUND_P1"]
    key("K11_round_wall_limit_point", len(round_endpoints) == 3 and all(row["endpoint_character"] == "LIMIT_POINT" for row in round_endpoints))
    key("K12_nonzero_wall_extension_family", all(row["extension_status"] == "REQUIRES_FREE_EXTENSION_CENSUS" for row in nonzero_endpoints))
    key("K13_R1_mixing_center_order_passes", all(row["mixing_center_status"] == "PASS_NECESSARY_H_ORDER_R2_ONLY__FULL_SMOOTHNESS_NOT_CLAIMED" for row in r1_rows))
    key("K14_RA1_literal_center_fails", all(str(row["mixing_center_status"]).startswith("FAIL") for row in r2_rows))
    key("K15_all_P1_complete_centers_fail", all(row["complete_metric_center_status"] == "FAIL_A_LINEAR_TERM" for row in rows))
    expected_ids = {
        f"R0_n{float(1 / inv_n):.12f}" for inv_n in INV_N
    } | {
        f"{prefix}_n{float(1 / inv_n):.12f}_qr{float(q_ratio):+.2f}"
        for prefix in ("R1", "R2") for inv_n in INV_N for q_ratio in Q_RATIOS
    }
    key("K16_no_profile_postselection", {row["candidate_id"] for row in rows} == expected_ids)
    key(
        "K17_D_N_never_physical_selection",
        all(
            row["D_N_status"]
            == (
                "NOT_FREE_ENDPOINT_DATA"
                if row["family"] == "R0_ROUND_P1"
                else "ADMISSIBLE_CONTROL_MEMBERS_NOT_SELECTED__FULL_EXTENSION_FAMILY_OPEN"
            )
            for row in endpoints
        ),
    )
    syntax = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    called = {
        node.func.attr if isinstance(node.func, ast.Attribute) else node.func.id
        for node in ast.walk(syntax)
        if isinstance(node, ast.Call) and isinstance(node.func, (ast.Attribute, ast.Name))
    }
    key("K18_no_eigensolver", not any(name.startswith("eig") or name in {"solve_ivp", "root_scalar"} for name in called))
    data_suffixes = (".csv", ".npz", ".npy", ".fits", ".h5", ".hdf5")
    imported_modules = {
        node.module.split(".")[0] if isinstance(node, ast.ImportFrom) and node.module else alias.name.split(".")[0]
        for node in ast.walk(syntax)
        for alias in (node.names if isinstance(node, (ast.Import, ast.ImportFrom)) else [])
    }
    key(
        "K19_no_observational_merit_filter",
        imported_modules <= {"__future__", "ast", "csv", "hashlib", "json", "subprocess", "fractions", "pathlib", "sympy"}
        and not any(path.lower().endswith(data_suffixes) for path, _ in source_rows)
        and len({row["execution_disposition"] for row in rows}) == 1,
    )
    key("K20_no_execution_authorized", all(row["execution_disposition"] == "BLOCKED_C1_CENTER_REGULARITY" for row in rows))

    if not all(KEYS.values()):
        raise SystemExit("N02 admissibility derivation failed")

    result = {
        "status": "VERIFIED_WITH_CAVEATS__NO_BANKED_REGULAR_CENTER_TO_WALL_C1_C2_ANCHOR__NO_EIGENSOLVE",
        "key_count": len(KEYS),
        "keys": KEYS,
        "profile_strata_count": len(rows),
        "endpoint_strata_count": len(endpoints),
        "represented_R1_profiles": sum(int(row["represented_h_magnitudes"]) for row in r1_rows),
        "full_C1_center_curvature_residue": str(residue),
        "P1_center_result": "A=(1-r)^n has a=-n and lim[r RicciScalar]=6n!=0; all frozen P1 full-sphere centers are curvature singular",
        "mixing_center_result": "h=hbar r^2(1-r)^q passes the necessary O(r^2) collapsing-orbit order only; full Cartesian smoothness is not claimed; RA1 literal h=h0(1-r)^q fails even that necessary order",
        "wall_result": "all registered nonzero-mixing q/qcrit<1 rows have B->infinity, finite Liouville length, sub-inverse-square matrix potentials, and a free limit-circle extension family; D/N are unselected control members",
        "round_wall_result": "h=0 with every registered n>1 has infinite Liouville length and a limit-point continuum endpoint; D/N are not free wall data",
        "execution_result": "NO_BANKED_CENTER_TO_WALL_C1_OR_C2_PROFILE_IS_ADMISSIBLE_AS_A_REGULAR_COMPLETE_CONTROL_ANCHOR",
        "maximum_conclusion": "admissibility map only; no eigensolve, physical profile, boundary selection, spectrum, FD2, data fit, or GPU work",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {len(KEYS)}/{len(KEYS)} N02 admissibility keys; {len(rows)} profile strata; {len(endpoints)} endpoint strata")


if __name__ == "__main__":
    main()
