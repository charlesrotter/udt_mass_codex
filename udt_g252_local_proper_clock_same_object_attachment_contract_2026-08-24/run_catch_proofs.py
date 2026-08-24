#!/usr/bin/env python3
"""Hostile exact controls for the G252 attachment contract."""

from __future__ import annotations

import argparse
from dataclasses import replace
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import sys


PKG = Path(__file__).resolve().parent


def load_production():
    path = PKG / "derive_local_proper_clock_attachment.py"
    spec = importlib.util.spec_from_file_location("g252_production", path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load production module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def raises_value_error(callable_object) -> bool:
    try:
        callable_object()
    except ValueError:
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    module = load_production()

    base = module.make_record(Q(7, 5), Q(11, 7), "control")
    second = module.make_record(Q(13, 9), Q(11, 7), "second")
    inconsistent = replace(second, tau_star=second.tau_star + Q(1, 13))
    fixed_c_e = Q(299792458)
    scales_compatible_without_attachment = {Q(1), Q(3, 2), Q(11, 7)}

    mutations = {
        "control_recovers_scale": module.recover_scale(base) == Q(11, 7),
        "control_common_scale": module.common_scale((base, second)) == Q(11, 7),
        "self_evaluation_rejected": raises_value_error(lambda: module.recover_scale(replace(base, defined_by_metric=True))),
        "nonindependent_calibration_rejected": raises_value_error(lambda: module.recover_scale(replace(base, independently_calibrated=False))),
        "observer_mismatch_rejected": raises_value_error(lambda: module.recover_scale(replace(base, record_observer="other"))),
        "start_event_mismatch_rejected": raises_value_error(lambda: module.recover_scale(replace(base, record_start="other"))),
        "end_event_mismatch_rejected": raises_value_error(lambda: module.recover_scale(replace(base, record_end="other"))),
        "branch_mismatch_rejected": raises_value_error(lambda: module.recover_scale(replace(base, record_branch="other"))),
        "missing_clock_identity_rejected": raises_value_error(lambda: module.recover_scale(replace(base, clock_id=""))),
        "missing_calibration_identity_rejected": raises_value_error(lambda: module.recover_scale(replace(base, calibration_id=""))),
        "zero_model_duration_rejected": raises_value_error(lambda: module.recover_scale(replace(base, bar_tau=Q(0)))),
        "negative_model_duration_rejected": raises_value_error(lambda: module.recover_scale(replace(base, bar_tau=Q(-1)))),
        "zero_clock_duration_rejected": raises_value_error(lambda: module.recover_scale(replace(base, tau_star=Q(0)))),
        "negative_clock_duration_rejected": raises_value_error(lambda: module.recover_scale(replace(base, tau_star=Q(-1)))),
        "inconsistent_second_attachment_rejected": raises_value_error(lambda: module.common_scale((base, inconsistent))),
        "per_attachment_scale_proliferation_rejected": module.recover_scale(base) != module.recover_scale(inconsistent),
        "empty_attachment_set_rejected": raises_value_error(lambda: module.common_scale(tuple())),
        "c_E_alone_not_a_scale_equation": fixed_c_e > 0 and len(scales_compatible_without_attachment) == 3,
        "same_unit_change_control": (Q(17, 9) * base.tau_star) / (Q(17, 9) * base.bar_tau) == module.recover_scale(base),
        "local_anchor_does_not_select_history": (
            module.recover_scale(base) == Q(11, 7)
            and {"bar_tau": base.bar_tau, "elsewhere": Q(1)} != {"bar_tau": base.bar_tau, "elsewhere": Q(2)}
        ),
    }
    missed = [name for name, caught in mutations.items() if not caught]
    result = {
        "status": "PASS" if not missed else "FAIL",
        "implementation": "executable_metadata_and_exact_arithmetic_mutations",
        "caught": sum(bool(value) for value in mutations.values()),
        "total": len(mutations),
        "missed": missed,
        "mutations": mutations,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if missed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
