#!/usr/bin/env python3
"""Fresh-seed equivalence census for the G194 write-free autodiff repair."""

from __future__ import annotations

import json
import os
import random
from types import SimpleNamespace
from pathlib import Path

import numpy as np

import verify_general_symmetric_screen_mixing_independent as base


SEED = 1940821
PROFILE_COUNT = 32
POINTS = (-0.23, 0.11, 0.47)
CEILING = 2.0e-8
PACKAGE = Path(__file__).resolve().parent
torch = base.torch


def profiles():
    generator = random.Random(SEED)
    result = []
    for index in range(PROFILE_COUNT):
        log_scale = base.series(
            c1=generator.uniform(-0.25, 0.25),
            c2=generator.uniform(-0.20, 0.20),
            sin_amp=generator.uniform(-0.08, 0.08),
            cos_amp=generator.uniform(-0.05, 0.05),
            frequency=float(generator.choice((1, 2, 3))),
        )

        def random_entry():
            return base.series(
                c0=generator.uniform(-0.25, 0.25),
                c1=generator.uniform(-0.25, 0.25),
                c2=generator.uniform(-0.12, 0.12),
                sin_amp=generator.uniform(-0.10, 0.10),
                cos_amp=generator.uniform(-0.10, 0.10),
                frequency=float(generator.choice((1, 2, 3))),
            )

        result.append(
            base.Profile(
                f"equivalence_{index:02d}",
                log_scale,
                random_entry(),
                random_entry(),
                random_entry(),
            )
        )
    return result


def original_forward_jets(profile, eta_value):
    point = torch.tensor([eta_value, eta_value, 0.0, 0.0], dtype=base.DTYPE)
    metric_function = lambda argument: base.coframe_metric(profile, argument)

    # torch.func.jacfwd consults torch._dynamo only to decide whether to attach
    # functools metadata to the returned wrapper.  Supplying this local
    # is_compiling=False sentinel avoids importing unrelated distributed/JIT
    # helpers; it does not alter the forward-AD transform or tensor operations.
    sentinel = object()
    previous = torch.__dict__.get("_dynamo", sentinel)
    torch.__dict__["_dynamo"] = SimpleNamespace(is_compiling=lambda: False)
    try:
        first_function = torch.func.jacfwd(metric_function)
        second_function = torch.func.jacfwd(torch.func.jacfwd(metric_function))
    finally:
        if previous is sentinel:
            del torch.__dict__["_dynamo"]
        else:
            torch.__dict__["_dynamo"] = previous

    metric = metric_function(point)
    first = first_function(point)
    second = second_function(point)
    return metric.detach().numpy(), first.detach().numpy(), second.detach().numpy()


def tide_from_jets(profile, eta_value, metric, first, second):
    riemann = base.curvature_from_jets(metric, first, second)
    scale = profile.values(eta_value)[0]
    ray = np.array([scale**-2, scale**-2, 0.0, 0.0])
    screens = (
        np.array([0.0, 0.0, scale**-1, 0.0]),
        np.array([0.0, 0.0, 0.0, scale**-1]),
    )
    tide = np.zeros((2, 2), dtype=float)
    for left_index, left in enumerate(screens):
        for right_index, right in enumerate(screens):
            curvature_vector = np.zeros(4, dtype=float)
            for aa in range(4):
                curvature_vector[aa] = sum(
                    riemann[aa, bb, cc, dd] * ray[bb] * right[cc] * ray[dd]
                    for bb in (0, 1)
                    for cc in (2, 3)
                    for dd in (0, 1)
                )
            tide[left_index, right_index] = left @ metric @ curvature_vector
    return tide


def maximum_error(left, right):
    return float(np.max(np.abs(np.asarray(left) - np.asarray(right))))


def main():
    maxima = {"metric": 0.0, "first_jet": 0.0, "second_jet": 0.0, "tide": 0.0}
    assertions = 0
    for profile in profiles():
        for eta_value in POINTS:
            reference = original_forward_jets(profile, eta_value)
            candidate = base.metric_jets(profile, eta_value)
            for name, old, new in zip(("metric", "first_jet", "second_jet"), reference, candidate):
                error = maximum_error(old, new)
                maxima[name] = max(maxima[name], error)
                assert error < CEILING
                assertions += 1
            reference_tide = tide_from_jets(profile, eta_value, *reference)
            candidate_tide = tide_from_jets(profile, eta_value, *candidate)
            tide_error = maximum_error(reference_tide, candidate_tide)
            maxima["tide"] = max(maxima["tide"], tide_error)
            assert tide_error < CEILING
            assertions += 1

    result = {
        "status": "PASS",
        "seed": SEED,
        "profile_count": PROFILE_COUNT,
        "points": list(POINTS),
        "assertion_count": assertions,
        "ceiling": CEILING,
        "maximum_errors": maxima,
        "role": "VERIFIER_ONLY_AUTODIFF_EQUIVALENCE__NOT_SCIENTIFIC_CENSUS",
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G194_NO_WRITE") != "1":
        (PACKAGE / "AUTODIFF_EQUIVALENCE_RESULT.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
