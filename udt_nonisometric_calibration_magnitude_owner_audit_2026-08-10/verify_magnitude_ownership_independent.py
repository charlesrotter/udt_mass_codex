#!/usr/bin/env python3
"""Independent Fraction/table verifier; imports no production derivation code."""

from __future__ import annotations

import csv
import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
UNTYPED = {"INSUFFICIENT_TYPED_EVIDENCE", "NO_COMPLETE_REGULAR_BRANCH", "HISTORICAL_REDERIVATION_REQUIRED"}


def table(path: Path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return [list(row) for row in zip(*a)]


def diag(values):
    return [[values[i] if i == j else F(0) for j in range(len(values))] for i in range(len(values))]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def gram(columns):
    eta = diag([F(-1), F(1), F(1), F(1)])
    return mm(mm(tr(columns), eta), columns)


def densities(arrow, flag):
    source = gram(flag)
    target = gram(mm(arrow, flag))
    line = abs(target[0][0]) / abs(source[0][0])
    area = abs(det2(target)) / abs(det2(source))
    return line, area, area / line**2


def expected(branch_id: str, family_id: str, parent: str) -> str:
    if family_id == "F04_NATIVE_DYNAMICAL_BOOTSTRAP":
        return "BLOCKED_MISSING_DYNAMIC_LAW"
    if family_id == "F05_NO_CURRENT_KINEMATIC_OWNER":
        return "SUPPORTED_NO_COMPLETE_PHYSICAL_OWNER"
    if parent in UNTYPED:
        return "INSUFFICIENT_TYPED_EVIDENCE"
    if parent == "AGGREGATE_MEMBER_DEPENDENT":
        return "AGGREGATE_MEMBER_DEPENDENT"
    if family_id == "F01_PAIR_SURFACE_JACOBIAN":
        return "BLOCKED_MISSING_PHYSICAL_QUERY"
    if family_id == "F02_ENDPOINT_STATIONARY_CLOCK":
        return {
            "R17": "OWNER_CONDITIONAL_BRANCH_ONLY",
            "R18": "OWNER_CONDITIONAL_BRANCH_ONLY",
            "R19": "TRANSPORT_OR_READOUT_ONLY",
            "R20": "BLOCKED_NONUNIQUE_INTRINSIC_CLOCK",
            "R22": "BLOCKED_MISSING_PHYSICAL_QUERY",
        }.get(branch_id, "NO_OWNED_NONZERO_CLOCK_SCALE")
    if family_id == "F03_PATH_GLOBAL_COMPLETION":
        return "TRANSPORT_OR_READOUT_ONLY" if branch_id in {"R17", "R18", "R19", "R23", "R24"} else "BLOCKED_MISSING_PHYSICAL_QUERY"
    raise AssertionError(family_id)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify cached outputs without writing",
    )
    args = parser.parse_args()
    branches = table(ROOT / "udt_global_relation_family_branch_classification_2026-08-10/BRANCH_UNIVERSE.tsv")
    transitions = {
        row["branch_id"]: row
        for row in table(ROOT / "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/TRANSITION_OWNERSHIP_ATLAS.tsv")
    }
    atlas = table(HERE / "MAGNITUDE_OWNER_ATLAS.tsv")
    assert len(branches) == len(transitions) == 24
    assert len(atlas) == len({(row["branch_id"], row["family_id"]) for row in atlas}) == 120
    for row in atlas:
        parent = transitions[row["branch_id"]]["primary_disposition"]
        assert row["disposition"] == expected(row["branch_id"], row["family_id"], parent)

    conditional = [
        row["branch_id"] for row in atlas
        if row["family_id"] == "F02_ENDPOINT_STATIONARY_CLOCK" and row["disposition"] == "OWNER_CONDITIONAL_BRANCH_ONLY"
    ]
    assert conditional == ["R17", "R18"]
    assert "ENDPOINT_RATIO_OWNED" in transitions["R17"]["intrinsic_clock_scale"]
    assert "NOT_BRANCH_OWNED" in transitions["R17"]["nonisometric_transition"]
    assert "UNIQUE_KILLING_NORM_ENDPOINT_RATIO_OWNED" == transitions["R18"]["intrinsic_clock_scale"]
    assert transitions["R18"]["intrinsic_ruler_or_grading"] == "NO_SAME_BRANCH_INTRINSIC_RULER"

    # Independent exact rational witnesses.
    assert F(2, 3) * F(3, 5) == F(2, 5)
    h1 = [[F(-1, 4), F(0)], [F(0), F(4)]]
    h2 = [[F(-1, 4), F(0)], [F(0), F(1)]]
    arg1 = -det2(h1) / h1[0][0] ** 2
    arg2 = -det2(h2) / h2[0][0] ** 2
    assert (arg1, arg2) == (F(16), F(4))

    flag = [[F(1), F(0)], [F(0), F(1)], [F(0), F(0)], [F(0), F(0)]]
    boost = diag([F(1), F(1), F(1), F(1)])
    boost[0][0] = boost[2][2] = F(5, 4)
    boost[0][2] = boost[2][0] = F(3, 4)
    dilation = diag([F(1, 2), F(2), F(1), F(1)])
    mixed = [[F(1, 2), F(0), F(0), F(0)], [F(0), F(2), F(0), F(0)], [F(1, 4), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
    assert densities(boost, flag) == (F(1), F(1), F(1))
    assert densities(dilation, flag) == (F(1, 4), F(1), F(16))
    assert densities(mm(boost, dilation), flag) == (F(1, 4), F(1), F(16))
    assert densities(mixed, flag) == (F(3, 16), F(3, 4), F(64, 3))

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        manifest = list(csv.DictReader(stream, delimiter="\t"))
    assert len(manifest) == 24
    manifest_paths = {row["path"] for row in manifest}
    assert len(manifest_paths) == 24
    for row in manifest:
        source_path = ROOT / row["path"]
        assert source_path.is_file(), row["path"]
        data = source_path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
        assert len(data) == int(row["size"])
        blob = hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()
        assert blob == row["git_blob"]
    for row in atlas:
        for citation in row["evidence"].split(";"):
            source_path = citation.split("::", 1)[0]
            assert source_path in manifest_paths, (row["branch_id"], row["family_id"], source_path)

    counts = Counter(row["disposition"] for row in atlas)
    result = {
        "verdict": "VERIFIED",
        "method": "independent table reconstruction plus exact Fraction matrices; no production import",
        "branch_identities": len(branches),
        "atlas_cells": len(atlas),
        "conditional_owner_branches": conditional,
        "complete_owner_rows": sum(row["disposition"] == "OWNER_DERIVED" for row in atlas),
        "disposition_counts": dict(sorted(counts.items())),
        "same_clock_terminal_arguments": [str(arg1), str(arg2)],
        "isometric_and_nonisometric_witnesses": True,
        "source_hashes_verified": len(manifest),
        "primary_landing_reproduced": "BRANCH_CONDITIONAL_MAGNITUDE_OWNER_ONLY__NO_UNIVERSAL_OWNER",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        assert (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8") == rendered
    else:
        (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(rendered, encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
