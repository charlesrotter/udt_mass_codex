#!/usr/bin/env python3
"""Exact G166 primary-metric ordered-pair kernel derivation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def source_hashes() -> tuple[int, list[str]]:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    failures: list[str] = []
    for row in rows:
        payload = (ROOT / row["path"]).read_bytes()
        actual = hashlib.sha256(payload).hexdigest()
        if actual != row["sha256"]:
            failures.append(row["path"])
    return len(rows), failures


def main() -> None:
    T, L, beta = sp.symbols("T L beta", positive=True, real=True)
    Omega = sp.symbols("Omega", positive=True, real=True)
    delta = sp.symbols("delta", real=True)
    x, y, z = sp.symbols("x y z", real=True)
    q1, q2 = sp.symbols("q1 q2", positive=True, real=True)

    h = sp.Matrix(
        [
            [-T**2, -T**2 * beta],
            [-T**2 * beta, L**2 - T**2 * beta**2],
        ]
    )
    det_h = sp.factor(h.det())
    beta_read = sp.simplify(h[0, 1] / h[0, 0])
    L2_read = sp.factor(h[1, 1] - h[0, 1] ** 2 / h[0, 0])
    reciprocal_ratio_squared = sp.factor((-det_h) / h[0, 0] ** 2)
    q_squared = sp.factor(h[0, 0] ** 2 / (-det_h))
    chi = sp.factor((L - T) / (L + T))
    chi_from_q = sp.factor((1 - T / L) / (1 + T / L))

    primary = sp.diag(-sp.exp(-2 * delta), sp.exp(2 * delta))
    primary_det = sp.simplify(primary.det())
    primary_ratio = sp.simplify((-primary.det()) / primary[0, 0] ** 2)
    primary_q = sp.simplify((-primary[0, 0]) / sp.sqrt(-primary.det()))

    q = sp.symbols("q", positive=True, real=True)
    chi_q = (1 - q) / (1 + q)
    reverse_identity = sp.factor(chi_q.subs(q, 1 / q) + chi_q)
    identity_value = sp.simplify(chi_q.subs(q, 1))
    chi1 = (1 - q1) / (1 + q1)
    chi2 = (1 - q2) / (1 + q2)
    composed = sp.factor((1 - q1 * q2) / (1 + q1 * q2))
    mobius = sp.factor((chi1 + chi2) / (1 + chi1 * chi2))

    conformal_h = sp.simplify(Omega**2 * h)
    conformal_ratio_squared = sp.factor(
        (-conformal_h.det()) / conformal_h[0, 0] ** 2
    )
    scaled_primary_det = sp.factor((Omega**2 * primary).det())

    orchestra = sp.Matrix([[x, z], [z, y]])
    h_complete = h + orchestra
    minus_det_complete = sp.factor(-h_complete.det())
    registered_minus_det = sp.expand(
        (T**2 - x) * (L**2 + y)
        + x * T**2 * beta**2
        - 2 * T**2 * beta * z
        + z**2
    )
    complete_q_squared = sp.factor(
        h_complete[0, 0] ** 2 / (-h_complete.det())
    )

    core_h00, core_h01, core_h11 = sp.symbols("h00 h01 h11", real=True)
    core_det = core_h00 * core_h11 - core_h01**2
    core_q_squared = sp.factor(core_h00**2 / (-core_det))

    checks = {
        "pair_det_is_minus_T2L2": sp.simplify(det_h + T**2 * L**2) == 0,
        "clock_density_reads_from_h00": sp.simplify(-h[0, 0] - T**2) == 0,
        "shift_reads_algebraically": sp.simplify(beta_read - beta) == 0,
        "ruler_density_reads_algebraically": sp.simplify(L2_read - L**2) == 0,
        "depth_ratio_is_L_over_T_squared": sp.simplify(
            reciprocal_ratio_squared - (L / T) ** 2
        )
        == 0,
        "conditional_ceff_ratio_is_T_over_L_squared": sp.simplify(
            q_squared - (T / L) ** 2
        )
        == 0,
        "chi_is_pair_density_contrast": sp.simplify(chi - chi_from_q) == 0,
        "primary_reciprocal_block_det_minus_one": primary_det == -1,
        "primary_block_returns_delta_ratio": sp.simplify(
            primary_ratio - sp.exp(4 * delta)
        )
        == 0,
        "primary_block_returns_ceff_ratio": sp.simplify(
            primary_q - sp.exp(-2 * delta)
        )
        == 0,
        "coincidence_is_identity": identity_value == 0,
        "observer_reversal_negates_chi": reverse_identity == 0,
        "matched_depths_compose_mobius": sp.simplify(composed - mobius) == 0,
        "common_scale_cancels_from_kernel": sp.simplify(
            conformal_ratio_squared - reciprocal_ratio_squared
        )
        == 0,
        "arbitrary_common_scale_leaves_founded_det_one_family": sp.simplify(
            scaled_primary_det + 1
        )
        == 1 - Omega**4,
        "orchestra_enters_complete_pair_before_readout": sp.simplify(
            minus_det_complete - registered_minus_det
        )
        == 0,
        "orchestra_clock_entry_changes_terminal_ratio": sp.diff(
            complete_q_squared, x
        )
        != 0,
        "orchestra_ruler_entry_changes_terminal_ratio": sp.diff(
            complete_q_squared, y
        )
        != 0,
        "orchestra_shift_entry_changes_terminal_ratio": sp.diff(
            complete_q_squared, z
        )
        != 0,
        "native_core_has_no_path_symbol": all(
            str(s) not in {"path", "gamma"} for s in core_q_squared.free_symbols
        ),
        "native_core_has_no_xmax_symbol": all(
            str(s) not in {"Xmax", "X_max"} for s in core_q_squared.free_symbols
        ),
    }

    source_count, source_failures = source_hashes()
    checks["source_hashes_match"] = source_count == 13 and not source_failures

    source_classes = [
        ("S01", "founded reciprocal representation", "PRIMARY_UDT_METRIC_INPUT"),
        ("S02", "declared Lorentzian pair readout", "PRIMARY_UDT_METRIC_INPUT"),
        ("S03", "recorded static spherical metric", "DERIVED_CONDITIONAL_REALIZATION"),
        ("S04", "regular pair density decomposition", "ALGEBRAIC_KERNEL_DESCENT"),
        ("S05", "terminal reciprocal c_E ratio", "ALGEBRAIC_KERNEL_DESCENT"),
        ("S06", "normalized chi chart", "WORKING_POSITION_CONSTITUTION"),
        ("S07", "orchestra-before-readout", "CONDITIONAL_COMPLETE_ASSEMBLY"),
        ("S08", "uncompressed E and J envelope", "CONDITIONAL_CONFIGURATION_ENVELOPE"),
        ("S09", "arbitrary pair realization", "NOT_REQUIRED_AS_A_FIXED_PATH_FOR_LOCAL_KERNEL"),
        ("S10", "general observer network calibration carry", "OPEN_GLOBAL_EXTENSION"),
        ("S11", "X_max", "DOWNSTREAM_GLOBAL_CONSEQUENCE_TARGET"),
        ("S12", "G164 scaffold subtraction", "PONDER_PARENT"),
        ("S13", "G165 conformal family", "BROADER_ENVELOPE_CONTROL_NOT_FOUNDED_FREEDOM"),
    ]
    with (HERE / "SOURCE_CLASSIFICATION.tsv").open("w", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
        writer.writerow(["id", "object", "g166_class"])
        writer.writerows(source_classes)

    result = {
        "primary_landing": (
            "PRIMARY_UDT_ORDERED_PAIR_KERNEL_DESCENDS_ALGEBRAICALLY"
            "__GENERAL_3PLUS1_ASSEMBLY_CONDITIONAL"
        ),
        "checks_passed": sum(bool(v) for v in checks.values()),
        "checks_total": len(checks),
        "checks": checks,
        "source_count": source_count,
        "source_failures": source_failures,
        "source_classes": len(source_classes),
        "exact_core": {
            "phi_pair": "(1/4) log((-det h)/h00^2)",
            "q_pair": "(-h00)/sqrt(-det h) = T/L",
            "chi_pair": "(L-T)/(L+T) = (1-q)/(1+q)",
        },
        "scope": (
            "Founded ordered-pair radial metric and algebraic terminal kernel; complete "
            "nonspherical, mixing, time-live metric assembly remains conditional."
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    if not all(checks.values()):
        failed = [name for name, value in checks.items() if not value]
        raise SystemExit(f"FAIL: {failed}")
    print(
        f"PASS: {len(checks)} exact G166 checks; {source_count} frozen sources; "
        f"{len(source_classes)} classified objects"
    )


if __name__ == "__main__":
    main()
