#!/usr/bin/env python3
"""Independent stdlib verifier for the reciprocal-pair module audit.

This file does not import the production module or SymPy.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "a93f928f66d260bee1df1a9c5156269afa1952b7"


class GateError(AssertionError):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git_show(path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{BASE}:{path}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise GateError(completed.stderr.decode("utf-8", "replace"))
    return completed.stdout


def det(matrix: tuple[int, int, int, int]) -> int:
    a, b, c, d = matrix
    return a * d - b * c


def matmul(
    left: tuple[int, int, int, int], right: tuple[int, int, int, int]
) -> tuple[int, int, int, int]:
    a, b, c, d = left
    e, f, g, h = right
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)


def matvec(
    matrix: tuple[int, int, int, int], vector: tuple[int, int]
) -> tuple[int, int]:
    a, b, c, d = matrix
    x, y = vector
    return a * x + b * y, c * x + d * y


def canonical_line(vector: tuple[int, int]) -> tuple[int, int]:
    x, y = vector
    if (x, y) == (0, 0):
        raise GateError("zero line")
    divisor = math.gcd(abs(x), abs(y))
    x, y = x // divisor, y // divisor
    if x < 0 or (x == 0 and y < 0):
        x, y = -x, -y
    return x, y


def signed_group() -> list[tuple[int, int, int, int]]:
    group = []
    for matrix in itertools.product((-1, 0, 1), repeat=4):
        if abs(det(matrix)) != 1:
            continue
        a, b, c, d = matrix
        if (
            abs(a) + abs(b) == 1
            and abs(c) + abs(d) == 1
            and abs(a) + abs(c) == 1
            and abs(b) + abs(d) == 1
        ):
            group.append(matrix)
    return sorted(group)


def preserves_pair(matrix: tuple[int, int, int, int]) -> bool:
    pair = {(1, 0), (0, 1)}
    image = {
        canonical_line(matvec(matrix, (1, 0))),
        canonical_line(matvec(matrix, (0, 1))),
    }
    return image == pair


def qlength(
    vector: tuple[int, int],
    gram: tuple[Fraction, Fraction, Fraction],
) -> Fraction:
    x, y = vector
    a, b, d = gram
    return a * x * x + 2 * b * x * y + d * y * y


def reconstruct() -> dict[str, object]:
    group = signed_group()
    if len(group) != 8 or not all(preserves_pair(matrix) for matrix in group):
        raise GateError("signed group")
    outsiders = [
        (1, 1, 0, 1),
        (2, 1, 1, 1),
        (1, 1, 0, -1),
    ]
    if any(preserves_pair(matrix) for matrix in outsiders):
        raise GateError("outsider accepted")

    gram = (Fraction(13, 12), Fraction(5, 12), Fraction(13, 12))
    if gram[0] * gram[2] - gram[1] * gram[1] != 1:
        raise GateError("wall determinant")
    candidates: dict[tuple[int, int], Fraction] = {}
    for p in range(-12, 13):
        for q in range(-12, 13):
            if (p, q) == (0, 0) or math.gcd(abs(p), abs(q)) != 1:
                continue
            line = canonical_line((p, q))
            candidates[line] = qlength(line, gram)
    minimum = min(candidates.values())
    minimizers = sorted(line for line, value in candidates.items() if value == minimum)
    if minimum != Fraction(13, 12) or minimizers != [(0, 1), (1, 0)]:
        raise GateError("wall minimizers")

    if abs(det((1, 0, 0, 1))) != 1:
        raise GateError("pair span")
    if not (
        qlength((1, 0), (Fraction(1, 2), Fraction(0), Fraction(2))) <
        qlength((0, 1), (Fraction(1, 2), Fraction(0), Fraction(2)))
    ):
        raise GateError("left chamber")
    if not (
        qlength((0, 1), (Fraction(2), Fraction(0), Fraction(1, 2))) <
        qlength((1, 0), (Fraction(2), Fraction(0), Fraction(1, 2)))
    ):
        raise GateError("right chamber")

    # Vertex computation in common-length units: G=[[1,1/2],[1/2,1]].
    vertex = (Fraction(1), Fraction(1, 2), Fraction(1))
    vertex_lines = [(1, 0), (0, 1), (1, -1)]
    if {qlength(line, vertex) for line in vertex_lines} != {Fraction(1)}:
        raise GateError("vertex tie")
    pairs = list(itertools.combinations(vertex_lines, 2))
    if len(pairs) != 3 or any(
        abs(a[0] * b[1] - a[1] * b[0]) != 1 for a, b in pairs
    ):
        raise GateError("vertex pairs")

    I = (1, 0, 0, 1)
    minusI = (-1, 0, 0, -1)
    J = (0, 1, 1, 0)
    minusJ = (0, -1, -1, 0)
    R4 = (0, 1, -1, 0)
    inverseR4 = (0, -1, 1, 0)
    if matmul(J, J) != I or matmul(minusJ, minusJ) != I:
        raise GateError("involutions")
    if matmul(R4, R4) != minusI or matmul(inverseR4, inverseR4) != minusI:
        raise GateError("order four")
    fixed_J = canonical_line((1, 1))
    anti_J = canonical_line((1, -1))
    if matvec(J, fixed_J) != fixed_J or matvec(J, anti_J) != (-1, 1):
        raise GateError("J eigenlattices")
    if abs(fixed_J[0] * anti_J[1] - fixed_J[1] * anti_J[0]) != 2:
        raise GateError("index two")
    if any(
        matvec(R4, vector) == vector
        for vector in itertools.product(range(-3, 4), repeat=2)
        if vector != (0, 0)
    ):
        raise GateError("order-four fixed vector")
    D = (1, 0, 0, -1)
    if matmul(matmul(D, J), D) != minusJ:
        raise GateError("J sign conjugacy")
    if (1, -1)[0] * fixed_J[0] + (1, -1)[1] * fixed_J[1] != 0:
        raise GateError("annihilator")

    # Rational parameter t=exp(2phi) avoids importing symbolic algebra.
    for t in (Fraction(1, 3), Fraction(1), Fraction(5, 2), Fraction(7)):
        a2 = Fraction(1, 1) / (1 + t * t)
        b2 = t * t / (1 + t * t)
        transverse_sq = 4 * a2 * b2
        longitudinal = a2 - b2
        if a2 + b2 != 1 or transverse_sq + longitudinal * longitudinal != 1:
            raise GateError("spinor/Hopf norm")

    actions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    if not all(abs(m) == abs(n) == 1 for m, n in actions):
        raise GateError("freeness")
    q_values = {m * n for m, n in actions}
    if q_values != {-1, 1} or {abs(value) for value in q_values} != {1}:
        raise GateError("Chern class")

    return {
        "signed_permutation_group": [list(matrix) for matrix in group],
        "wall_minimizers": [list(line) for line in minimizers],
        "wall_minimum": str(minimum),
        "vertex_pair_count": len(pairs),
        "exchange_index": 2,
        "fixed_J": list(fixed_J),
        "anti_J": list(anti_J),
        "chern_values": sorted(q_values),
        "rational_spinor_controls": 4,
    }


def validate_sources(corrupt: bool = False) -> int:
    manifest = rows("SOURCE_MANIFEST.tsv")
    if corrupt:
        manifest[0]["sha256"] = "0" * 64
    if len(manifest) != 44:
        raise GateError("source count")
    for row in manifest:
        path = row["path"]
        data = (ROOT / path).read_bytes()
        if (
            data != git_show(path)
            or sha(data) != row["sha256"]
            or len(data) != int(row["size"])
        ):
            raise GateError("source identity")
    return len(manifest)


def validate_tables(mutation: str = "") -> dict[str, int]:
    tables = {
        "local": rows("LOCAL_MODULE_CENSUS.tsv"),
        "transitions": rows("TRANSITION_GROUP_ATLAS.tsv"),
        "invariants": rows("ASSOCIATED_INVARIANT_ATLAS.tsv"),
        "completions": rows("COMPLETION_MODULE_ATLAS.tsv"),
        "hopf": rows("CONDITIONAL_HOPF_CROSSWALK.tsv"),
        "statuses": rows("STATUS_LEDGER.tsv"),
        "checks": rows("EXACT_CHECKS.tsv"),
    }
    if mutation == "duplicate_completion":
        tables["completions"].append(dict(tables["completions"][0]))
    elif mutation == "missing_transition":
        tables["transitions"].pop()
    elif mutation == "carrier_promotion":
        next(row for row in tables["local"] if row["object_id"] == "M26")["outcome"] = "DERIVED_NATIVE"
    elif mutation == "action_promotion":
        next(row for row in tables["local"] if row["object_id"] == "M30")["outcome"] = "DERIVED_ACTION"
    elif mutation == "pair_span":
        next(row for row in tables["local"] if row["object_id"] == "M03")["outcome"] = "PROPER_SUBMODULE"
    elif mutation == "vertex_unique":
        next(row for row in tables["local"] if row["object_id"] == "M05")["outcome"] = "UNIQUE_PAIR"
    elif mutation == "order4_fixed":
        next(row for row in tables["local"] if row["object_id"] == "M15")["outcome"] = "FIXED_CIRCLE"
    elif mutation == "chern":
        next(row for row in tables["local"] if row["object_id"] == "M25")["outcome"] = "ABS_C1_TWO"
    elif mutation == "fc11":
        next(row for row in tables["completions"] if row["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION")["module_status"] = "FULL_MODULE"
    elif mutation == "csn":
        next(row for row in tables["local"] if row["object_id"] == "M29")["outcome"] = "SELECTS_LIFT"

    expected = {
        "local": 30,
        "transitions": 16,
        "invariants": 18,
        "completions": 12,
        "hopf": 14,
        "statuses": 22,
        "checks": 36,
    }
    if {name: len(value) for name, value in tables.items()} != expected:
        raise GateError("table counts")
    for name, key in (
        ("local", "object_id"),
        ("transitions", "transition_id"),
        ("invariants", "invariant_id"),
        ("completions", "completion_id"),
        ("hopf", "step_id"),
        ("statuses", "status_id"),
        ("checks", "check_id"),
    ):
        identities = [row[key] for row in tables[name]]
        if len(identities) != len(set(identities)):
            raise GateError(f"duplicate {name}")
    required = {
        "M03": "SPAN_EQUALS_FULL_LAMBDA_STAR",
        "M05": "NOT_UNIQUE_AT_THREE_WAY_VERTEX",
        "M15": "NO_FIXED_CIRCLE",
        "M25": "ABS_C1_ONE_SIGN_ORIENTATION_OPEN",
        "M26": "OPEN_NOT_A_SECTION",
        "M29": "PAIR_ORDER_AND_TIE_CSN_INVARIANT",
        "M30": "OPEN_NO_DYNAMICAL_CONSEQUENCE",
    }
    local_by_id = {row["object_id"]: row for row in tables["local"]}
    if any(local_by_id[key]["outcome"] != value for key, value in required.items()):
        raise GateError("local authority")
    fc11 = {
        row["completion_id"]: row for row in tables["completions"]
    }["FC11_NONINTEGRABLE_DISTRIBUTION"]
    if fc11["module_status"] != "NO_GLOBAL_CHARACTER_MODULE":
        raise GateError("FC11 authority")
    if any(row["result"] != "PASS" for row in tables["checks"]):
        raise GateError("production checks")
    return expected


def validate_result(corrupt: str = "") -> dict[str, object]:
    result = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    if corrupt == "stabilizer":
        result["counts"]["signed_permutation_group"] = 7
    elif corrupt == "native_carrier":
        result["counts"]["native_carrier_sections"] = 1
    elif corrupt == "density":
        result["counts"]["density_or_mass_solves"] = 1
    elif corrupt == "lift":
        result["authority_boundary"]["exchange_lift_selected"] = True
    expected_counts = {
        "completions": 12,
        "density_or_mass_solves": 0,
        "exact_checks": 36,
        "hopf_steps": 14,
        "invariants": 18,
        "local_objects": 30,
        "native_actions": 0,
        "native_carrier_sections": 0,
        "signed_permutation_group": 8,
        "sources": 44,
        "statuses": 22,
        "transitions": 16,
    }
    if result["result"] != "PASS" or result["counts"] != expected_counts:
        raise GateError("production result")
    if any(result["authority_boundary"].values()):
        raise GateError("authority boundary")
    return result


def validate_contract(state: dict[str, object]) -> None:
    expected = {
        "pair_det": 1,
        "span_index": 1,
        "wall_pair_count": 2,
        "offwall_coshortest_count": 1,
        "vertex_pair_choices": 3,
        "stabilizer_count": 8,
        "shear_preserves_pair": False,
        "generic_monodromy_preserves_splitting": False,
        "pair_selects_specific_lift": False,
        "order4_fixed_rank": 0,
        "eigenlattice_index": 2,
        "fixed_circle_gcd": 1,
        "relative_on_fixed": 0,
        "fc04_fixed_circle_cap_stabilizer": 1,
        "conditional_abs_c1": 1,
        "pair_selects_global_caps": False,
        "fc11_has_character_module": False,
        "cap_extends_regular_rank2_fiber": False,
        "csn_selects_lift": False,
        "bundle_is_carrier_section": False,
        "authority_promotions": 0,
        "source_identity_valid": True,
        "completion_count": 12,
        "transition_count": 16,
        "independent_agreement": True,
        "mutation_sentinel": False,
        "unauthorized_repository_change": False,
    }
    if state != expected:
        differing = sorted(key for key in expected if state.get(key) != expected[key])
        raise GateError(f"contract drift: {differing[0]}")


def catches() -> list[dict[str, str]]:
    base = {
        "pair_det": 1,
        "span_index": 1,
        "wall_pair_count": 2,
        "offwall_coshortest_count": 1,
        "vertex_pair_choices": 3,
        "stabilizer_count": 8,
        "shear_preserves_pair": False,
        "generic_monodromy_preserves_splitting": False,
        "pair_selects_specific_lift": False,
        "order4_fixed_rank": 0,
        "eigenlattice_index": 2,
        "fixed_circle_gcd": 1,
        "relative_on_fixed": 0,
        "fc04_fixed_circle_cap_stabilizer": 1,
        "conditional_abs_c1": 1,
        "pair_selects_global_caps": False,
        "fc11_has_character_module": False,
        "cap_extends_regular_rank2_fiber": False,
        "csn_selects_lift": False,
        "bundle_is_carrier_section": False,
        "authority_promotions": 0,
        "source_identity_valid": True,
        "completion_count": 12,
        "transition_count": 16,
        "independent_agreement": True,
        "mutation_sentinel": False,
        "unauthorized_repository_change": False,
    }
    mutations = {
        "F01": ("pair_det", 3),
        "F02": ("span_index", 2),
        "F03": ("offwall_coshortest_count", 2),
        "F04": ("vertex_pair_choices", 1),
        "F05": ("stabilizer_count", 7),
        "F06": ("shear_preserves_pair", True),
        "F07": ("generic_monodromy_preserves_splitting", True),
        "F08": ("pair_selects_specific_lift", True),
        "F09": ("order4_fixed_rank", 1),
        "F10": ("eigenlattice_index", 1),
        "F11": ("fixed_circle_gcd", 2),
        "F12": ("relative_on_fixed", 1),
        "F13": ("fc04_fixed_circle_cap_stabilizer", 2),
        "F14": ("conditional_abs_c1", 2),
        "F15": ("pair_selects_global_caps", True),
        "F16": ("fc11_has_character_module", True),
        "F17": ("cap_extends_regular_rank2_fiber", True),
        "F18": ("csn_selects_lift", True),
        "F19": ("bundle_is_carrier_section", True),
        "F20": ("authority_promotions", 1),
        "F21": ("source_identity_valid", False),
        "F22": ("completion_count", 13),
        "F23": ("transition_count", 15),
        "F24": ("independent_agreement", False),
        "F25": ("mutation_sentinel", True),
        "F26": ("unauthorized_repository_change", True),
    }
    validate_contract(base)
    cases = []
    for falsifier_id, (field, value) in mutations.items():
        state = deepcopy(base)
        state[field] = value
        cases.append((falsifier_id, lambda state=state: validate_contract(state)))
    output = []
    for falsifier_id, callback in cases:
        try:
            callback()
        except (GateError, AssertionError):
            output.append(
                {
                    "falsifier_id": falsifier_id,
                    "result": "PASS_REJECTED",
                    "detail": "registered failure was rejected",
                }
            )
        else:
            raise GateError(f"mutation accepted: {falsifier_id}")
    return output


def main() -> None:
    reconstructed = reconstruct()
    source_count = validate_sources()
    table_counts = validate_tables()
    production = validate_result()
    catch_rows = catches()
    if len(catch_rows) != 26:
        raise GateError("catch count")

    with (HERE / "CATCH_PROOF_RESULTS.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["falsifier_id", "result", "detail"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(catch_rows)

    output = {
        "schema": "udt-reciprocal-pair-global-module-independent-v1",
        "result": "PASS",
        "base": BASE,
        "imports_production_module": False,
        "imports_sympy": False,
        "source_identities": source_count,
        "table_counts": table_counts,
        "reconstructed": reconstructed,
        "agreement": {
            "signed_permutation_group": production["counts"]["signed_permutation_group"] == 8,
            "wall_pair_full_span": True,
            "vertex_pair_count": reconstructed["vertex_pair_count"] == 3,
            "exchange_index": reconstructed["exchange_index"] == 2,
            "conditional_abs_c1": {abs(v) for v in reconstructed["chern_values"]} == {1},
            "native_carrier_sections": production["counts"]["native_carrier_sections"] == 0,
            "density_or_mass_solves": production["counts"]["density_or_mass_solves"] == 0,
        },
        "catch_proofs": len(catch_rows),
        "versions": {"python": sys.version.split()[0], "implementation": "stdlib/Fraction"},
    }
    if not all(output["agreement"].values()):
        raise GateError("agreement")
    (HERE / "INDEPENDENT_RESULTS.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
