#!/usr/bin/env python3
"""Exact G171 primary-metric multi-pair response derivation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "d9e2d54f"
checks: list[dict[str, object]] = []


def check(name: str, condition: object, detail: object = "") -> None:
    passed = bool(condition)
    checks.append({"name": name, "passed": passed, "detail": str(detail)})
    if not passed:
        raise AssertionError(f"{name}: {detail}")


def source_hashes() -> tuple[int, list[str]]:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    failures: list[str] = []
    for row in rows:
        sealed_source = ROOT / "sources" / row["path"]
        if sealed_source.is_file():
            frozen = sealed_source.read_bytes()
        else:
            frozen = subprocess.run(
                ["git", "show", f"{FROZEN_SOURCE_COMMIT}:{row['path']}"],
                cwd=ROOT,
                capture_output=True,
                check=True,
            ).stdout
        if hashlib.sha256(frozen).hexdigest() != row["sha256"]:
            failures.append(row["path"])
    return len(rows), failures


def pullback(metric: sp.Matrix, u: sp.Matrix, s: sp.Matrix) -> sp.Matrix:
    J = sp.Matrix.hstack(u, s)
    return sp.simplify(J.T * metric * J)


def q2(h: sp.Matrix) -> sp.Expr:
    return sp.factor(h[0, 0] ** 2 / (-h.det()))


def phi(h: sp.Matrix) -> sp.Expr:
    return sp.log((-h.det()) / h[0, 0] ** 2) / 4


# 1. Pair-indexed endpoint algebra.
Phi_A_AB, Phi_B_AB = sp.symbols("Phi_A_AB Phi_B_AB", real=True)
Phi_B_BC, Phi_C_BC = sp.symbols("Phi_B_BC Phi_C_BC", real=True)
Phi_A_AC, Phi_C_AC = sp.symbols("Phi_A_AC Phi_C_AC", real=True)

delta_AB = Phi_B_AB - Phi_A_AB
delta_BA = Phi_A_AB - Phi_B_AB
delta_BC = Phi_C_BC - Phi_B_BC
delta_AC = Phi_C_AC - Phi_A_AC
omega = sp.expand(delta_AB + delta_BC - delta_AC)
omega_expected = sp.expand(
    (Phi_B_AB - Phi_B_BC)
    + (Phi_C_BC - Phi_C_AC)
    + (Phi_A_AC - Phi_A_AB)
)

check("same_pair_reversal", sp.simplify(delta_AB + delta_BA) == 0)
check("three_pair_defect_identity", sp.simplify(omega - omega_expected) == 0, omega)

varphi_A, varphi_B, varphi_C = sp.symbols("varphi_A varphi_B varphi_C", real=True)
observer_only = {
    Phi_A_AB: varphi_A,
    Phi_A_AC: varphi_A,
    Phi_B_AB: varphi_B,
    Phi_B_BC: varphi_B,
    Phi_C_BC: varphi_C,
    Phi_C_AC: varphi_C,
}
check("observer_only_is_sufficient_for_zero_defect", sp.simplify(omega.subs(observer_only)) == 0)

# Matching only B is insufficient to close an independently evaluated AC edge.
matched_B = sp.simplify(omega.subs(Phi_B_BC, Phi_B_AB))
check(
    "middle_match_alone_not_full_triangle_closure",
    matched_B
    == sp.expand((Phi_C_BC - Phi_C_AC) + (Phi_A_AC - Phi_A_AB)),
    matched_B,
)
check("middle_match_alone_not_identically_zero", matched_B != 0)

# 2. Exact primary-metric witness. Same event, metric, clock, and base pair components;
# only the angular components of the second pair germ change.
g = sp.diag(sp.Rational(-1, 4), 4, 9, sp.Rational(144, 25))
u = sp.Matrix([2, 0, 0, 0])
s_radial = sp.Matrix([1, sp.Rational(1, 2), 0, 0])
s_angular = sp.Matrix([1, sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 4)])

h_radial = pullback(g, u, s_radial)
h_angular = pullback(g, u, s_angular)
angular_gram = sp.simplify(h_angular - h_radial)

check("same_metric", g == sp.diag(sp.Rational(-1, 4), 4, 9, sp.Rational(144, 25)))
check("same_clock_tangent", pullback(g, u, s_radial)[0, 0] == pullback(g, u, s_angular)[0, 0])
check("same_base_pair_components", s_radial[:2, :] == s_angular[:2, :])
check("radial_metric_exact", h_radial == sp.Matrix([[-1, sp.Rational(-1, 2)], [sp.Rational(-1, 2), sp.Rational(3, 4)]]), h_radial)
check("angular_metric_exact", h_angular == sp.Matrix([[-1, sp.Rational(-1, 2)], [sp.Rational(-1, 2), sp.Rational(211, 100)]]), h_angular)
check("angular_gram_exact", angular_gram == sp.Matrix([[0, 0], [0, sp.Rational(34, 25)]]), angular_gram)
check("radial_regular", h_radial[0, 0] < 0 and h_radial.det() < 0)
check("angular_regular", h_angular[0, 0] < 0 and h_angular.det() < 0)
check("radial_determinant", h_radial.det() == -1)
check("angular_determinant", h_angular.det() == sp.Rational(-59, 25))
check("radial_q2", q2(h_radial) == 1)
check("angular_q2", q2(h_angular) == sp.Rational(25, 59))
check("radial_phi", sp.simplify(phi(h_radial)) == 0)
check("angular_phi", sp.simplify(phi(h_angular) - sp.log(sp.Rational(59, 25)) / 4) == 0)
check("shared_observer_not_observer_only", sp.simplify(phi(h_angular) - phi(h_radial)) != 0)
check("angular_data_precedes_readout", q2(h_angular) != q2(h_radial))

# 3. A local three-pair network assembled only from primary-metric endpoint witnesses.
p = sp.log(sp.Rational(59, 25)) / 4
network_subs = {
    Phi_A_AB: 0,
    Phi_B_AB: 0,
    Phi_B_BC: p,
    Phi_C_BC: 0,
    Phi_A_AC: 0,
    Phi_C_AC: 0,
}
network_deltas = {
    "delta_AB": sp.simplify(delta_AB.subs(network_subs)),
    "delta_BC": sp.simplify(delta_BC.subs(network_subs)),
    "delta_AC": sp.simplify(delta_AC.subs(network_subs)),
    "omega": sp.simplify(omega.subs(network_subs)),
}
check("network_AB_zero", network_deltas["delta_AB"] == 0)
check(
    "network_BC_nonzero",
    sp.simplify(sp.expand_log(network_deltas["delta_BC"] + p, force=True)) == 0,
)
check("network_AC_zero", network_deltas["delta_AC"] == 0)
check(
    "network_triangle_defect_nonzero",
    sp.simplify(sp.expand_log(network_deltas["omega"] + p, force=True)) == 0 and p != 0,
)

# Reversal remains exact on every edge when the same edge endpoint data are swapped.
check("network_BC_reverse", sp.simplify((Phi_B_BC - Phi_C_BC) + delta_BC) == 0)

# 4. Native pair-chart scope. A shared positive upper-triangular pair rechart shifts both
# endpoint densities equally, so one pair difference is unchanged. Independent recharting is not.
a, d, n = sp.symbols("a d n", positive=True)
T, L, beta = sp.symbols("T L beta", positive=True)
h_generic = sp.Matrix([[-T**2, -T**2 * beta], [-T**2 * beta, L**2 - T**2 * beta**2]])
P = sp.Matrix([[a, n], [0, d]])
h_rechart = sp.simplify(P.T * h_generic * P)
phi_shift = sp.simplify(sp.expand_log(phi(h_rechart) - phi(h_generic), force=True))
check(
    "shared_pair_rechart_shift",
    sp.simplify(sp.expand_log(phi_shift - sp.log(d / a) / 2, force=True)) == 0,
    phi_shift,
)

shift = sp.symbols("shift", real=True)
check(
    "shared_pair_rechart_cancels_in_delta",
    sp.simplify(((Phi_B_AB + shift) - (Phi_A_AB + shift)) - delta_AB) == 0,
)
shift_A, shift_B = sp.symbols("shift_A shift_B", real=True)
check(
    "independent_pair_rechart_exposed",
    sp.simplify(((Phi_B_AB + shift_B) - (Phi_A_AB + shift_A)) - delta_AB)
    == shift_B - shift_A,
)

# 5. Confirm the source universe and exclude scaffolded packages mechanically.
source_count, source_failures = source_hashes()
manifest_text = (HERE / "SOURCE_MANIFEST.tsv").read_text()
check("source_hashes_match", source_count == 12 and not source_failures, source_failures)
check("scaffolded_sources_excluded", all(f"udt_g{i}" not in manifest_text for i in range(142, 161)))

landing = (
    "PRIMARY_METRIC_PAIR_GERM_RELATIVE_NETWORK"
    "__EACH_ORDERED_PAIR_RESPONSE_NATIVE_FROM_ITS_COMPLETE_PULLBACK"
    "__SAME_PAIR_REVERSAL_AUTOMATIC"
    "__SHARED_OBSERVER_DOES_NOT_FORCE_PAIR_INDEPENDENT_ENDPOINT_DENSITY"
    "__GENERAL_TRIANGLE_ADDITIVITY_NOT_DERIVED_OR_REQUIRED"
    "__MATCHED_ENDPOINT_READOUT_SUBFAMILY_TELESCOPES"
    "__NO_SCAFFOLDED_CARRY_KERNEL"
)

result = {
    "landing": landing,
    "status": "DERIVED_BOUNDED_AWAITING_INDEPENDENT_AND_EXTERNAL_REVIEW",
    "checks_passed": sum(int(row["passed"]) for row in checks),
    "checks_total": len(checks),
    "checks": checks,
    "same_observer_witness": {
        "h_radial": [[str(v) for v in row] for row in h_radial.tolist()],
        "h_angular": [[str(v) for v in row] for row in h_angular.tolist()],
        "angular_gram": [[str(v) for v in row] for row in angular_gram.tolist()],
        "q2_radial": str(q2(h_radial)),
        "q2_angular": str(q2(h_angular)),
        "phi_radial": str(phi(h_radial)),
        "phi_angular": str(phi(h_angular)),
    },
    "three_pair_defect": str(omega),
    "network_deltas": {key: str(value) for key, value in network_deltas.items()},
    "pair_rechart_phi_shift": str(phi_shift),
    "source_count": source_count,
    "source_failures": source_failures,
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({key: result[key] for key in ("landing", "checks_passed", "checks_total")}, sort_keys=True))
