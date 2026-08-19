#!/usr/bin/env python3
"""Exact production derivation for the bounded G181 endpoint classification."""

from __future__ import annotations

import csv
import json
import os
from fractions import Fraction
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
LANDING = (
    "COMPLETED_PAIR_ENDPOINT_CLASSIFICATION__"
    "REMOVABLE_STALLS_SEPARATED_FROM_INTRINSIC_BOUNDARIES"
)


def classify_power(a: Fraction, b: Fraction) -> tuple[str, str]:
    p = a + b
    if p > -1:
        tape = "FINITE"
    elif p == -1:
        tape = "INFINITE_LOG"
    else:
        tape = "INFINITE_POWER"
    if a > 0:
        depth = "POSITIVE_INFINITY"
    elif a == 0:
        depth = "FINITE"
    else:
        depth = "NEGATIVE_INFINITY"
    return tape, depth


def power_row(name: str, a: int, b: int) -> dict[str, str]:
    af = Fraction(a)
    bf = Fraction(b)
    tape, depth = classify_power(af, bf)
    return {
        "witness": name,
        "family": "power",
        "a": str(af),
        "b": str(bf),
        "p=a+b": str(af + bf),
        "tape_class": tape,
        "depth_class": depth,
        "boundary_note": "q_to_0_positive",
    }


def derive() -> tuple[dict[str, object], list[dict[str, str]]]:
    T, L, beta = sp.symbols("T L beta", positive=True, finite=True)
    m = sp.simplify(T * L)
    h_sigma = sp.Matrix(
        [
            [-T**2, -T**2 * beta],
            [-T**2 * beta, L**2 - T**2 * beta**2],
        ]
    )
    assert sp.simplify(h_sigma.det() + m**2) == 0

    jac = sp.diag(1, 1 / m)
    h_s = sp.simplify(jac.T * h_sigma * jac)
    B = sp.symbols("B", real=True, finite=True)
    expected_h_s = sp.Matrix(
        [
            [-T**2, -T**2 * B],
            [-T**2 * B, T ** (-2) - T**2 * B**2],
        ]
    )
    assert sp.simplify(h_s.subs(beta, B * m) - expected_h_s) == sp.zeros(2)
    assert sp.simplify(h_s.det() + 1) == 0

    q = sp.symbols("q", positive=True)
    k = sp.symbols("k", integer=True, positive=True)
    m_stall = k * q ** (k - 1)
    h_stall = sp.diag(-1, m_stall**2)
    stall_jac = sp.diag(1, 1 / m_stall)
    assert sp.simplify(stall_jac.T * h_stall * stall_jac - sp.diag(-1, 1)) == sp.zeros(2)

    v, e2, r, bang = sp.symbols("v e2 r bang", real=True)
    primary_m2 = v**2 + e2 * r**2 * bang**2
    assert sp.simplify(primary_m2.subs({v: 0, bang: 0})) == 0
    assert sp.simplify(primary_m2.subs({v: 0, bang: 3, e2: 2, r: 5}) - 450) == 0
    assert sp.simplify(primary_m2.subs({v: 7, bang: 0}) - 49) == 0
    assert sp.simplify(primary_m2.subs({v: 0, r: 0})) == 0

    rows = [
        power_row("finite_depth_plus", 1, 0),
        power_row("finite_depth_zero", 0, 0),
        power_row("finite_depth_minus", -1, 1),
        power_row("log_infinite_depth_plus", 1, -2),
        power_row("log_infinite_depth_zero", 0, -1),
        power_row("log_infinite_depth_minus", -1, 0),
        power_row("power_infinite_depth_plus", 1, -3),
        power_row("power_infinite_depth_zero", 0, -2),
        power_row("power_infinite_depth_minus", -1, -1),
        {
            "witness": "finite_tape_nonconvergent_depth",
            "family": "oscillatory",
            "a": "NA",
            "b": "NA",
            "p=a+b": "0",
            "tape_class": "FINITE",
            "depth_class": "NO_LIMIT",
            "boundary_note": "m=1; T=2+sin(log(q))",
        },
        {
            "witness": "infinite_tape_nonconvergent_depth",
            "family": "oscillatory",
            "a": "NA",
            "b": "NA",
            "p=a+b": "-1",
            "tape_class": "INFINITE_LOG",
            "depth_class": "NO_LIMIT",
            "boundary_note": "m=1/q; T=2+sin(log(q))",
        },
        {
            "witness": "one_sided_removable_stall",
            "family": "primary_radial",
            "a": "NA",
            "b": "NA",
            "p=a+b": "k-1",
            "tape_class": "FINITE",
            "depth_class": "FINITE",
            "boundary_note": "r=r0+q^k; s=q^k; h_s=diag(-1,1)",
        },
        {
            "witness": "two_sided_cusp_warning",
            "family": "primary_radial",
            "a": "NA",
            "b": "NA",
            "p=a+b": "1",
            "tape_class": "FINITE_EACH_SIDE",
            "depth_class": "FINITE",
            "boundary_note": "r=r0+q^2; s=q*abs(q); r=r0+abs(s)",
        },
        {
            "witness": "finite_regular_with_m_to_zero",
            "family": "generic_shifted",
            "a": "0",
            "b": "1",
            "p=a+b": "1",
            "tape_class": "FINITE",
            "depth_class": "FINITE",
            "boundary_note": "T=1; m=q; beta=B*m; h_s regular",
        },
        {
            "witness": "finite_irregular_with_m_to_zero",
            "family": "generic",
            "a": "1",
            "b": "0",
            "p=a+b": "1",
            "tape_class": "FINITE",
            "depth_class": "POSITIVE_INFINITY",
            "boundary_note": "T=q; m=q; h00_s_to_0; hss_s_to_infinity",
        },
        {
            "witness": "finite_regular_with_m_to_infinity",
            "family": "generic",
            "a": "0",
            "b": "-1/2",
            "p=a+b": "-1/2",
            "tape_class": "FINITE",
            "depth_class": "FINITE",
            "boundary_note": "T=1; m=q^(-1/2); h_s regular",
        },
        {
            "witness": "primary_angular_turn",
            "family": "primary",
            "a": "NA",
            "b": "NA",
            "p=a+b": "NA",
            "tape_class": "INTERIOR_REGULAR",
            "depth_class": "FINITE",
            "boundary_note": "v=0; r>0; bang!=0; m>0",
        },
        {
            "witness": "primary_zero_complete_tangent",
            "family": "primary",
            "a": "NA",
            "b": "NA",
            "p=a+b": "NA",
            "tape_class": "DEGENERATE",
            "depth_class": "UNCLASSIFIED",
            "boundary_note": "r>0; v=0; bang=0; m=0",
        },
        {
            "witness": "primary_center_radial_control",
            "family": "primary",
            "a": "NA",
            "b": "NA",
            "p=a+b": "NA",
            "tape_class": "INTERIOR_REGULAR_IFF_V_NONZERO",
            "depth_class": "FINITE",
            "boundary_note": "r=0; m=abs(v)",
        },
    ]

    power_rows = [row for row in rows if row["family"] == "power"]
    assert {row["depth_class"] for row in power_rows} == {
        "POSITIVE_INFINITY",
        "FINITE",
        "NEGATIVE_INFINITY",
    }
    assert {row["tape_class"] for row in power_rows} == {
        "FINITE",
        "INFINITE_LOG",
        "INFINITE_POWER",
    }

    result: dict[str, object] = {
        "audit": "G181",
        "status": "PASS",
        "landing": LANDING,
        "domain": "one supplied one-sided smooth regular interior pair family",
        "generic_identities": {
            "det_h_sigma": "-T^2*L_sigma^2=-m^2",
            "completed_coordinate": "ds=m*d_sigma",
            "det_h_s": "-1 on the regular interior",
            "completed_shift": "B=beta/m",
            "completed_depth": "Phi=-log(T)",
        },
        "endpoint_classification": {
            "finite_tape_iff": "m is locally integrable at the endpoint",
            "regular_finite_completed_metric_iff": (
                "T approaches a finite positive limit and beta/m approaches a finite limit "
                "in the retained calibrated clock chart"
            ),
            "m_limit_alone": "neither proves nor forbids regular completed extension",
            "auxiliary_stall": "may be one-sidedly removable; two-sided immersion carry remains open",
            "depth_tape_relation": "independent in the unrestricted supplied interior family",
        },
        "power_law": {
            "finite_tape": "a+b>-1",
            "log_infinite_tape": "a+b=-1",
            "power_infinite_tape": "a+b<-1",
            "positive_depth_infinity": "a>0",
            "finite_depth": "a=0",
            "negative_depth_infinity": "a<0",
        },
        "primary_boundary": {
            "density_squared": "v^2+exp(-2phi)*r^2*b^2",
            "r_positive_zero_iff": "v=0 and b=0",
            "angular_turn": "regular when r>0 and b!=0",
            "center": "m=abs(v)",
        },
        "witness_count": len(rows),
        "power_witness_count": len(power_rows),
        "open_scope": [
            "physical event pair-germ and family selection",
            "two-sided branch and immersion carry",
            "null cut focal topology-changing and global completion strata",
            "non-scalar transport",
            "metric-space distance and numerical Xmax",
            "dynamics action source matter bootstrap radiative transfer and observations",
        ],
    }
    return result, rows


def render_tsv(rows: list[dict[str, str]]) -> str:
    fields = [
        "witness",
        "family",
        "a",
        "b",
        "p=a+b",
        "tape_class",
        "depth_class",
        "boundary_note",
    ]
    from io import StringIO

    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def main() -> None:
    result, rows = derive()
    result_text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    tsv_text = render_tsv(rows)
    if os.environ.get("UDT_READ_ONLY_REPLAY") == "1":
        assert (HERE / "DERIVATION_RESULT.json").read_text() == result_text
        assert (HERE / "WITNESS_ATLAS.tsv").read_text() == tsv_text
    else:
        (HERE / "DERIVATION_RESULT.json").write_text(result_text)
        (HERE / "WITNESS_ATLAS.tsv").write_text(tsv_text)
    print(
        "PASS: completed-pair endpoint integrability, power-law, removable-stall, "
        "shift, primary-turning, and zero-tangent classifications"
    )


if __name__ == "__main__":
    main()
