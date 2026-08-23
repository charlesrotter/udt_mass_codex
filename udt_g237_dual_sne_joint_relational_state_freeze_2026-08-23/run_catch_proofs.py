#!/usr/bin/env python3
"""Mutation and hostile algebra catches for G237."""

from __future__ import annotations

import copy
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
RESULT = PACKAGE / "JOINT_STATE_RESULT.json"
VERIFICATION = PACKAGE / "VERIFICATION_RESULT.json"
OUT = PACKAGE / "CATCH_PROOF_RESULT.json"


def validate(production: dict, verification: dict) -> None:
    if production["primary_resolution"] != 12:
        raise AssertionError("primary resolution")
    if production["state_rows"] != 56:
        raise AssertionError("state row count")
    if production["cross_release_covariance"] != (
        "CHOSE_ZERO_AFTER_EXACT_CID_DEOVERLAP__UNKNOWN_SHARED_SYSTEMATICS_OPEN"
    ):
        raise AssertionError("cross-release covariance premise")
    if verification["status"] != "PASS":
        raise AssertionError("package verification")
    if not verification["checks"]["theta_cross_tolerance"]:
        raise AssertionError("independent theta mismatch")


def catches() -> list[str]:
    production = json.loads(RESULT.read_text())
    verification = json.loads(VERIFICATION.read_text())
    mutations = []
    for name, mutate in (
        ("primary_K", lambda p, v: p.__setitem__("primary_resolution", 16)),
        ("state_rows", lambda p, v: p.__setitem__("state_rows", 55)),
        ("covariance_premise", lambda p, v: p.__setitem__("cross_release_covariance", "DERIVED_INDEPENDENT")),
        ("verification_status", lambda p, v: v.__setitem__("status", "FAIL")),
        ("theta_tolerance", lambda p, v: v["checks"].__setitem__("theta_cross_tolerance", False)),
    ):
        p = copy.deepcopy(production)
        v = copy.deepcopy(verification)
        mutate(p, v)
        try:
            validate(p, v)
        except AssertionError:
            mutations.append(name)
        else:
            raise AssertionError(f"mutation escaped: {name}")
    return mutations


def main() -> None:
    mutations = catches()
    result = {"audit": "G237_CATCH_PROOFS", "status": "PASS", "caught": mutations}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
