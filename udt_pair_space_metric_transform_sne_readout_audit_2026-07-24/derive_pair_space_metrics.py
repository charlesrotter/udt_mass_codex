#!/usr/bin/env python3
"""Exact metric-transform algebra for the preregistered pair-space audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "9f34e799388d7b59539f95fc666d0d7aaed2f778"
PREREG_CORRECTION_COMMIT = "9d95652c70a2e43adcd80e3291aa038a2afef27f"


def check(checks: dict[str, str], name: str, condition: object) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(
    filename: str, fieldnames: list[str], rows: list[dict[str, object]]
) -> None:
    with (HERE / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def source_checks(checks: dict[str, str]) -> int:
    rows = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    check(checks, "source_count", len(rows) == 23)
    check(checks, "source_paths_unique", len({row["path"] for row in rows}) == 23)
    for row in rows:
        path = ROOT / row["path"]
        check(checks, f"source_exists_{row['path']}", path.is_file())
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        check(checks, f"source_hash_{row['path']}", digest == row["sha256"])
    return len(rows)


def main() -> None:
    checks: dict[str, str] = {}
    s, x, y = sp.symbols("s x y", nonnegative=True)
    X, kappa = sp.symbols("X kappa", positive=True)

    profiles = {
        "PROJECTIVE_TANH": sp.tanh(s),
        "WRL_PROPER_EXPONENTIAL": 1 - sp.exp(-s),
        "B19_ROUND": sp.Rational(2, 1) / sp.pi * sp.atan(sp.sinh(2 * s)),
    }

    pair_rows: list[dict[str, object]] = []
    for name, profile in profiles.items():
        first = sp.simplify(sp.diff(profile, s))
        second = sp.simplify(sp.diff(profile, s, 2))
        check(checks, f"{name}_origin", profile.subs(s, 0) == 0)
        check(checks, f"{name}_endpoint", sp.limit(profile, s, sp.oo) == 1)
        check(checks, f"{name}_positive_slope", first.subs(s, 1) > 0)
        check(checks, f"{name}_negative_curvature", second.subs(s, 1) < 0)
        check(checks, f"{name}_strict_positive", profile.subs(s, 1) > 0)

        pair_rows.append(
            {
                "candidate": name,
                "normalized_profile": str(profile),
                "first_derivative": str(first),
                "second_derivative": str(second),
                "origin": "0",
                "endpoint_supremum": "1",
                "monotonicity": "STRICTLY_INCREASING",
                "concavity": "STRICTLY_CONCAVE_FOR_s_GT_0",
                "pair_metric_status": "CONDITIONAL_VALID_METRIC_TRANSFORM",
                "local_length_status": "NOT_GENERALLY_INTRINSIC_PATH_LENGTH",
            }
        )

    # The derivatives have simple manifest signs on the nonnegative domain.
    check(
        checks,
        "tanh_first_exact",
        sp.simplify(sp.diff(profiles["PROJECTIVE_TANH"], s) - sp.sech(s) ** 2)
        == 0,
    )
    check(
        checks,
        "tanh_second_exact",
        sp.simplify(
            sp.diff(profiles["PROJECTIVE_TANH"], s, 2)
            + 2 * sp.sech(s) ** 2 * sp.tanh(s)
        )
        == 0,
    )
    check(
        checks,
        "exp_first_exact",
        sp.diff(profiles["WRL_PROPER_EXPONENTIAL"], s) == sp.exp(-s),
    )
    check(
        checks,
        "exp_second_exact",
        sp.diff(profiles["WRL_PROPER_EXPONENTIAL"], s, 2) == -sp.exp(-s),
    )
    check(
        checks,
        "round_first_exact",
        sp.simplify(
            sp.diff(profiles["B19_ROUND"], s)
            - 4 / (sp.pi * sp.cosh(2 * s))
        )
        == 0,
    )
    check(
        checks,
        "round_second_exact",
        sp.simplify(
            sp.diff(profiles["B19_ROUND"], s, 2)
            + 8 * sp.tanh(2 * s) / (sp.pi * sp.cosh(2 * s))
        )
        == 0,
    )

    # Concavity plus f(0)=0 implies subadditivity:
    # f(x)>=x/(x+y)f(x+y), f(y)>=y/(x+y)f(x+y).
    # Exact positive witnesses supplement the theorem.
    for name, profile in profiles.items():
        witness = sp.N(
            profile.subs(s, 1) + profile.subs(s, 2) - profile.subs(s, 3), 50
        )
        check(checks, f"{name}_subadditivity_witness", witness > 0)
        subdivision = sp.N(2 * profile.subs(s, sp.Rational(1, 2)) - profile.subs(s, 1), 50)
        check(checks, f"{name}_non_path_length_witness", subdivision > 0)

    # Normalized collinear composition inherited from additive base depth.
    a, b, c = sp.symbols("a b c", nonnegative=True)
    tanh_comp = (a + b) / (1 + a * b)
    exp_comp = a + b - a * b
    round_aux = a * sp.sqrt(1 + b**2) + b * sp.sqrt(1 + a**2)
    round_comp = sp.Rational(2, 1) / sp.pi * sp.atan(round_aux)

    check(
        checks,
        "tanh_composition_from_addition",
        sp.simplify(
            sp.tanh(x + y)
            - tanh_comp.subs({a: sp.tanh(x), b: sp.tanh(y)})
        )
        == 0,
    )
    check(
        checks,
        "exp_composition_from_addition",
        sp.simplify(
            1
            - sp.exp(-(x + y))
            - exp_comp.subs({a: 1 - sp.exp(-x), b: 1 - sp.exp(-y)})
        )
        == 0,
    )
    round_a = sp.sinh(2 * x)
    round_b = sp.sinh(2 * y)
    check(
        checks,
        "round_aux_from_addition",
        sp.simplify(
            sp.sinh(2 * (x + y))
            - (
                sp.sinh(2 * x) * sp.cosh(2 * y)
                + sp.sinh(2 * y) * sp.cosh(2 * x)
            )
        )
        == 0,
    )
    check(
        checks,
        "round_composition_from_addition",
        sp.simplify(
            sp.tan(
                sp.pi
                * profiles["B19_ROUND"].subs(s, x + y)
                / 2
            )
            - (
                sp.sinh(2 * x) * sp.cosh(2 * y)
                + sp.sinh(2 * y) * sp.cosh(2 * x)
            )
        )
        == 0,
    )

    # Associativity is exact by conjugation with addition; verify the two
    # elementary closed laws symbolically and the round auxiliary law.
    tanh_left = sp.factor(tanh_comp.subs({a: tanh_comp, b: c}))
    tanh_right = sp.factor(tanh_comp.subs({a: a, b: tanh_comp.subs({a: b, b: c})}))
    check(checks, "tanh_associative", sp.simplify(tanh_left - tanh_right) == 0)
    exp_left = sp.expand(exp_comp.subs({a: exp_comp, b: c}))
    exp_right = sp.expand(exp_comp.subs({a: a, b: exp_comp.subs({a: b, b: c})}))
    check(checks, "exp_associative", sp.simplify(exp_left - exp_right) == 0)

    composition_rows = [
        {
            "candidate": "PROJECTIVE_TANH",
            "normalized_pair_inputs": "y1;y2",
            "composition": "(y1+y2)/(1+y1*y2)",
            "inverse_additive_depth": "atanh(y)",
            "associativity": "EXACT_BY_CONJUGATION_WITH_ADDITION",
        },
        {
            "candidate": "WRL_PROPER_EXPONENTIAL",
            "normalized_pair_inputs": "y1;y2",
            "composition": "y1+y2-y1*y2",
            "inverse_additive_depth": "-log(1-y)",
            "associativity": "EXACT_BY_CONJUGATION_WITH_ADDITION",
        },
        {
            "candidate": "B19_ROUND",
            "normalized_pair_inputs": "y1;y2",
            "composition": "(2/pi)*atan(a1*sqrt(1+a2^2)+a2*sqrt(1+a1^2)); ai=tan(pi*yi/2)",
            "inverse_additive_depth": "asinh(tan(pi*y/2))/2",
            "associativity": "EXACT_BY_CONJUGATION_WITH_ADDITION",
        },
    ]

    # A concrete arbitrary metric triangle demonstrates preservation without
    # presuming a radial chart: d12=2, d23=3, d13=4.
    for name, profile in profiles.items():
        lhs = X * profile.subs(s, 4 * kappa)
        rhs = X * (
            profile.subs(s, 2 * kappa) + profile.subs(s, 3 * kappa)
        )
        check(
            checks,
            f"{name}_metric_triangle_witness",
            sp.N((rhs - lhs).subs({X: 7, kappa: sp.Rational(2, 5)}), 50)
            > 0,
        )

    source_count = source_checks(checks)

    readout_rows = [
        {
            "candidate": "PROJECTIVE_PAIR_TRANSFORM",
            "geometric_role": "BOUNDED_PAIR_METRIC_TRANSFORM",
            "redshift_join": "OPEN",
            "areal_or_optical_join": "OPEN",
            "SNe_status": "NOT_EVALUABLE",
            "reason": "pair distance is not automatically D_A or d_L",
        },
        {
            "candidate": "WRL_PROPER_PAIR_TRANSFORM",
            "geometric_role": "LOCAL_PROPER_RADIAL_PROFILE_AND_CONDITIONAL_PAIR_TRANSFORM",
            "redshift_join": "REGISTERED_LOCAL_STATIC",
            "areal_or_optical_join": "NOT_THE_SCORED_D_A",
            "SNe_status": "NOT_EVALUABLE_AS_PAIR_PROFILE",
            "reason": "existing SNe score uses areal r not proper distance",
        },
        {
            "candidate": "B19_ROUND_PAIR_TRANSFORM",
            "geometric_role": "CONDITIONAL_ANGULAR_DEPTH_PAIR_TRANSFORM",
            "redshift_join": "ABSENT_CONSTANT_LAPSE",
            "areal_or_optical_join": "OPEN",
            "SNe_status": "NOT_EVALUABLE",
            "reason": "clock/angular solder and SNe readout absent",
        },
        {
            "candidate": "FC12_OPEN",
            "geometric_role": "FREE_PROFILE_CONTROL",
            "redshift_join": "ABSENT_CONSTANT_LAPSE",
            "areal_or_optical_join": "OPEN",
            "SNe_status": "NOT_EVALUABLE",
            "reason": "A(phi) unselected",
        },
        {
            "candidate": "TEMPORAL_PHI_SEPARATION_FAMILY",
            "geometric_role": "CONDITIONAL_EQUAL_PHI_OBSERVER_DISTANCE",
            "redshift_join": "OPEN",
            "areal_or_optical_join": "OPEN",
            "SNe_status": "NOT_EVALUABLE",
            "reason": "representative and global branch open",
        },
        {
            "candidate": "WRL_AREAL_OPTICAL_READOUT",
            "geometric_role": "STATIC_CENTERED_AREAL_PLUS_CLOCK_PLUS_OPTICS",
            "redshift_join": "1+z=exp(phi)",
            "areal_or_optical_join": "D_A=r=X*(1-exp(-2phi)); d_L=(1+z)^2*D_A",
            "SNe_status": "EVALUABLE_EXISTING",
            "reason": "complete registered conditional readout",
        },
        {
            "candidate": "PROJECTIVE_AREAL_J1_READOUT",
            "geometric_role": "REGISTERED_PROJECTIVE_COMPARATOR",
            "redshift_join": "1+z=exp(phi)",
            "areal_or_optical_join": "D_A=X*tanh(phi); d_L=(1+z)^2*D_A",
            "SNe_status": "EVALUABLE_EXISTING_COMPARATOR",
            "reason": "complete registered conditional comparator",
        },
        {
            "candidate": "RETIRED_P_ELL",
            "geometric_role": "IMPOSED_JOIN",
            "redshift_join": "RETIRED",
            "areal_or_optical_join": "RETIRED",
            "SNe_status": "PROHIBITED",
            "reason": "prior imposition finding",
        },
    ]

    write_tsv(
        "PAIR_METRIC_LEDGER.tsv",
        [
            "candidate",
            "normalized_profile",
            "first_derivative",
            "second_derivative",
            "origin",
            "endpoint_supremum",
            "monotonicity",
            "concavity",
            "pair_metric_status",
            "local_length_status",
        ],
        pair_rows,
    )
    write_tsv(
        "COMPOSITION_LEDGER.tsv",
        [
            "candidate",
            "normalized_pair_inputs",
            "composition",
            "inverse_additive_depth",
            "associativity",
        ],
        composition_rows,
    )
    write_tsv(
        "READOUT_DISPOSITION.tsv",
        [
            "candidate",
            "geometric_role",
            "redshift_join",
            "areal_or_optical_join",
            "SNe_status",
            "reason",
        ],
        readout_rows,
    )
    status_rows = [
        {
            "claim": "three bounded transforms preserve metric axioms",
            "status": "DERIVED_CONDITIONAL_ON_SUPPLIED_BASE_METRIC",
            "scope": "positive X kappa and registered profiles",
        },
        {
            "claim": "transformed distances are local path lengths",
            "status": "REFUTED_IN_GENERAL",
            "scope": "strict concavity makes subdivision sum larger",
        },
        {
            "claim": "profile selected by pair-metric validity",
            "status": "REFUTED",
            "scope": "all three pass",
        },
        {
            "claim": "WR-L proper profile is the successful SNe law",
            "status": "REFUTED_CONFLATION",
            "scope": "SNe uses WR-L areal radius plus clock and optics",
        },
        {
            "claim": "global physical Xmax",
            "status": "OPEN",
            "scope": "base metric event pairing profile and scale unselected",
        },
        {
            "claim": "BAO CMB black-hole consequences",
            "status": "OPEN_OUT_OF_SCOPE",
            "scope": "no inference from this SNe replay",
        },
    ]
    write_tsv(
        "STATUS_LEDGER.tsv", ["claim", "status", "scope"], status_rows
    )

    result = {
        "schema": "udt-pair-space-metric-transform-1.0",
        "result": "PASS",
        "grade": "VERIFIED_WITH_CAVEATS_PENDING_INDEPENDENT_REPLAY",
        "preregistration_commit": PREREG_COMMIT,
        "preregistration_correction_commit": PREREG_CORRECTION_COMMIT,
        "source_count": source_count,
        "check_count": len(checks),
        "checks": checks,
        "pair_metric_theorem": {
            "form": "D_f(p,q)=X*f(kappa*d(p,q))",
            "premises": [
                "d is a metric",
                "X>0",
                "kappa>0",
                "f(0)=0",
                "f strictly increasing",
                "f concave and nonnegative",
            ],
            "accepted_profiles": list(profiles),
            "status": "DERIVED_CONDITIONAL_MATHEMATICAL_FAMILY",
        },
        "diameter": {
            "unbounded_base": "sup(D_f)=X; not attained at finite d",
            "finite_base_Delta": "sup(D_f)=X*f(kappa*Delta)",
            "physical_Xmax": "OPEN",
        },
        "path_length": {
            "status": "NOT_GENERALLY_INTRINSIC",
            "reason": "strict concavity gives n*f(s/n)>f(s) for s>0,n>1",
        },
        "SNe_stage": "FIREWALLED_NOT_YET_RUN",
        "maximum_conclusion": (
            "CONDITIONAL_BOUNDED_PAIR_METRIC_FAMILY_AND_READOUT_TYPE_"
            "DISTINCTION_ONLY;NO_PROFILE_SELECTION_OR_GLOBAL_XMAX"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
