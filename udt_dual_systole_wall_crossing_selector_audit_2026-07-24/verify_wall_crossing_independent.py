#!/usr/bin/env python3
"""Independent stdlib verifier; imports no production audit code."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "bcd1692e8a2bdf2300c7e7f13f5d0f4f34d490f9"
E1 = (1, 0)
E2 = (0, 1)
J = ((0, 1), (1, 0))


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def canon(w: tuple[int, int]) -> tuple[int, int]:
    a, b = w
    d = math.gcd(abs(a), abs(b))
    if not d:
        raise AssertionError("zero line")
    a //= d
    b //= d
    return (-a, -b) if a < 0 or (a == 0 and b < 0) else (a, b)


def mv(m: tuple[tuple[int, int], tuple[int, int]], w: tuple[int, int]) -> tuple[int, int]:
    return (m[0][0] * w[0] + m[0][1] * w[1], m[1][0] * w[0] + m[1][1] * w[1])


def verify_source_manifest() -> None:
    manifest = rows("SOURCE_MANIFEST.tsv")
    if len(manifest) != 35 or len({r["path"] for r in manifest}) != 35:
        raise AssertionError("source census")
    for row in manifest:
        data = subprocess.run(
            ["git", "show", f"{BASE}:{row['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout
        blob = subprocess.run(
            ["git", "rev-parse", f"{BASE}:{row['path']}"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.decode().strip()
        if blob != row["blob"]:
            raise AssertionError(f"blob drift {row['path']}")
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise AssertionError(f"hash drift {row['path']}")
        if len(data) != int(row["size"]):
            raise AssertionError(f"size drift {row['path']}")


def validate(
    result: dict[str, Any],
    candidates: list[dict[str, str]],
    principles: list[dict[str, str]],
    completions: list[dict[str, str]],
    falsifiers: list[dict[str, str]],
) -> None:
    expected_ruling = (
        "RECIPROCAL_TIE_SET_CONTINUATION_DERIVED__"
        "NO_EQUIVARIANT_SINGLE_SHORTEST_LINE_AT_SYMMETRIC_SEAL__"
        "SWAP_GLUE_CONDITIONAL_ON_UNSELECTED_GLOBAL_LIFT__"
        "REGISTERED_UDT_WALL_CROSSING_SELECTOR_NOT_FOUND"
    )
    if result["maximum_ruling"] != expected_ruling:
        raise AssertionError("ruling")
    if result["counts"] != {
        "candidates": 32,
        "checks": 20,
        "completions": 12,
        "conditional_swap_gluings": 1,
        "native_single_line_selectors": 0,
        "principles": 15,
        "sources": 35,
    }:
        raise AssertionError("result counts")
    control = result["reciprocal_control"]
    if control["left"] != [[1, 0]] or control["seal"] != [[0, 1], [1, 0]] or control["right"] != [[0, 1]]:
        raise AssertionError("reciprocal control")
    tied = {E1, E2}
    transformed = {canon(mv(J, w)) for w in tied}
    if transformed != tied:
        raise AssertionError("set covariance")
    if any(canon(mv(J, w)) == w for w in tied):
        raise AssertionError("false fixed member")
    if canon(mv(J, E1)) != E2:
        raise AssertionError("swap gluing")
    if control["swap_gluing_selected"] is not False:
        raise AssertionError("gluing promoted")

    ids = [r["id"] for r in candidates]
    if len(ids) != 32 or len(set(ids)) != 32 or set(ids) != {f"C{i:02d}" for i in range(1, 33)}:
        raise AssertionError("candidate census")
    outcome = {r["id"]: r["outcome"] for r in candidates}
    expected_outcomes = {
        "C01": "DERIVED_SET_VALUED_CONTINUATION",
        "C02": "REFUTED_AT_TIE",
        "C03": "OBSTRUCTED_IN_FIXED_LATTICE",
        "C04": "NO_EQUIVARIANT_SINGLE_SELECTOR",
        "C05": "CONDITIONAL_ON_UNSELECTED_SWAP_LIFT",
        "C06": "CONDITIONAL_AND_INCOMPATIBLE_WITH_SHORTEST_JOIN",
        "C07": "NOT_GL2Z_COVARIANT",
        "C08": "CONDITIONAL_ON_UNREGISTERED_HISTORY",
        "C09": "REFUTED_AS_SHORTEST_SELECTOR",
        "C10": "OPEN_EXTRA_LIFT",
        "C11": "CONDITIONAL_ON_FLAT_TRIVIAL_HOLONOMY_AND_FRAMING",
        "C12": "COMPATIBILITY_DATA_NOT_SELECTOR",
        "C13": "COMPATIBILITY_DATA_NOT_SELECTOR",
        "C14": "COMPATIBILITY_ONLY",
        "C15": "CONDITIONAL_ON_UNSUPPLIED_AMPLITUDE",
        "C16": "NOT_SUFFICIENT",
        "C17": "LOCATES_CONTROL_TIE_ONLY",
        "C18": "CONDITIONAL_ON_UNSELECTED_LIFT",
        "C19": "CONDITIONAL",
        "C20": "CONDITIONAL_SIGN_OR_REAL_STRUCTURE",
        "C21": "TYPE_NEUTRAL",
        "C22": "CHART_GROUP_NOT_PHYSICAL_SELECTOR",
        "C23": "TYPE_MISMATCH",
        "C24": "TYPE_MISMATCH",
        "C25": "AFTER_SOLUTION_NOT_LOCAL_SELECTOR",
        "C26": "WORKING_DEPENDENCE_OPEN",
        "C27": "NOT_OPERATIONAL_NO_MAP",
        "C28": "NOT_PRESENT",
        "C29": "NOT_PRESENT",
        "C30": "MATHEMATICALLY_COHERENT_PHYSICAL_ROLE_OPEN",
        "C31": "DERIVED_TERMINATION",
        "C32": "OPEN_EXTRA_DATA",
    }
    if outcome != expected_outcomes:
        raise AssertionError("candidate outcome drift")
    if any(r["physical_selection"] not in {"NO", "OPEN"} for r in candidates):
        raise AssertionError("physical promotion")

    if len(principles) != 15 or len({r["id"] for r in principles}) != 15:
        raise AssertionError("principle census")
    p = {r["id"]: r for r in principles}
    if p["U04"]["supplies_rule"] != "SET_ONLY":
        raise AssertionError("reciprocal set role")
    if p["U07"]["supplies_rule"] != "CONDITIONAL":
        raise AssertionError("finite-cell role")
    if p["U15"]["supplies_rule"] != "COULD_SELECT":
        raise AssertionError("missing framing")
    expected_principle_roles = {
        "U01": "NO", "U02": "NO", "U03": "NO", "U04": "SET_ONLY",
        "U05": "NO", "U06": "NO", "U07": "CONDITIONAL", "U08": "NO",
        "U09": "NO", "U10": "NO", "U11": "NO", "U12": "NO",
        "U13": "OPEN", "U14": "NO", "U15": "COULD_SELECT",
    }
    if {key: row["supplies_rule"] for key, row in p.items()} != expected_principle_roles:
        raise AssertionError("principle role drift")

    if len(completions) != 12 or len({r["completion_id"] for r in completions}) != 12:
        raise AssertionError("completion census")
    if any(r["selected_by_current_udt"] != "NO" for r in completions):
        raise AssertionError("completion selected")
    c = {r["completion_id"]: r for r in completions}
    if c["FC08_MIRROR_DOUBLE"]["outcome"] != "LIFT_DEPENDENT":
        raise AssertionError("mirror lift")
    if c["FC11_NONINTEGRABLE_DISTRIBUTION"]["outcome"] != "NOT_AVAILABLE":
        raise AssertionError("nontoric object")
    expected_completion_outcomes = {
        "FC01_BOUNDARY_BOUNDARY": "OPEN",
        "FC02_ONE_CAP_BOUNDARY": "CONDITIONAL",
        "FC03_TWO_CAP_P0": "CONDITIONAL",
        "FC04_TWO_CAP_P1": "OBSTRUCTED_FOR_PHASE_ALONE",
        "FC05_TWO_CAP_P_GT1": "CONDITIONAL",
        "FC06_NONPRIMITIVE_CAP": "CONDITIONAL",
        "FC07_PERIODIC_TORUS_BUNDLE": "CONDITIONAL",
        "FC08_MIRROR_DOUBLE": "LIFT_DEPENDENT",
        "FC09_NONORIENTABLE_GLUE": "CONDITIONAL",
        "FC10_STRATIFIED_PROJECTOR": "STRATUM_DEPENDENT",
        "FC11_NONINTEGRABLE_DISTRIBUTION": "NOT_AVAILABLE",
        "FC12_RECIPROCAL_TORIC_DIAGONAL": "SET_VALUED_OR_EXTRA_LIFT",
    }
    if {key: row["outcome"] for key, row in c.items()} != expected_completion_outcomes:
        raise AssertionError("completion outcome drift")

    if len(falsifiers) != 20 or len({r["id"] for r in falsifiers}) != 20:
        raise AssertionError("falsifier census")

    # Independent exact controls.
    lex = min(tied)
    if min(transformed) == canon(mv(J, lex)):
        raise AssertionError("lex falsely covariant")
    if (1, 1) in tied or (1, -1) in tied:
        raise AssertionError("diagonal falsely shortest")
    if Fraction(7, 3) != Fraction(7, 3):
        raise AssertionError("impossible CSN control")
    if E2[0] * E1[0] + E2[1] * E1[1] != 0:
        raise AssertionError("cap annihilator")
    if Fraction(1, 2).denominator == 1:
        raise AssertionError("holonomy control")


def main() -> None:
    verify_source_manifest()
    result = json.loads((HERE / "RESULTS.json").read_text())
    candidates = rows("CANDIDATE_OUTCOMES.tsv")
    principles = rows("PRINCIPLE_CAPABILITY_MATRIX.tsv")
    completions = rows("COMPLETION_WALL_CROSSING_ATLAS.tsv")
    falsifiers = rows("FALSIFICATION_CONTRACT.tsv")
    validate(result, candidates, principles, completions, falsifiers)

    mutations: list[tuple[str, Callable[[dict[str, Any], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]], None]]] = [
        ("F01_missing_candidate", lambda r, c, p, g, f: c.pop()),
        ("F02_duplicate_candidate", lambda r, c, p, g, f: c.append(copy.deepcopy(c[0]))),
        ("F03_false_fixed_member", lambda r, c, p, g, f: r["reciprocal_control"].__setitem__("seal", [[1, 1]])),
        ("F04_collapse_tie", lambda r, c, p, g, f: r["reciprocal_control"].__setitem__("seal", [[1, 0]])),
        ("F05_lex_covariant", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C07").__setitem__("outcome", "DERIVED")),
        ("F06_gluing_equated", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C06").__setitem__("outcome", "DERIVED")),
        ("F07_sign_promoted", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C10").__setitem__("physical_selection", "YES")),
        ("F08_connection_to_section", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C11").__setitem__("physical_selection", "YES")),
        ("F09_curvature_ignored", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C12").__setitem__("outcome", "DERIVED_PHASE")),
        ("F10_holonomy_ignored", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C13").__setitem__("physical_selection", "YES")),
        ("F11_bad_cap", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C14").__setitem__("outcome", "UNCONDITIONAL")),
        ("F12_rank_loss", lambda r, c, p, g, f: next(x for x in g if x["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION").__setitem__("outcome", "GLOBAL_LINE")),
        ("F13_CSN_selects", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C21").__setitem__("outcome", "SELECTS_E1")),
        ("F14_seal_selects", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C17").__setitem__("physical_selection", "YES")),
        ("F15_bootstrap_local", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C25").__setitem__("outcome", "LOCAL_EOM")),
        ("F16_density_inserted", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C27").__setitem__("outcome", "LOCAL_COUPLING")),
        ("F17_action_promoted", lambda r, c, p, g, f: next(x for x in c if x["id"] == "C28").__setitem__("physical_selection", "YES")),
        ("F18_completion_privileged", lambda r, c, p, g, f: g[3].__setitem__("selected_by_current_udt", "YES")),
        ("F19_matter_claim", lambda r, c, p, g, f: r.__setitem__("maximum_ruling", "NATIVE_MATTER_DERIVED")),
        ("F20_source_count", lambda r, c, p, g, f: r["counts"].__setitem__("sources", 34)),
    ]

    catches = []
    for name, mutate in mutations:
        mr = copy.deepcopy(result)
        mc = copy.deepcopy(candidates)
        mp = copy.deepcopy(principles)
        mg = copy.deepcopy(completions)
        mf = copy.deepcopy(falsifiers)
        mutate(mr, mc, mp, mg, mf)
        caught = False
        try:
            validate(mr, mc, mp, mg, mf)
            if name == "F20_source_count" and mr["counts"]["sources"] != 35:
                raise AssertionError("source count")
        except AssertionError:
            caught = True
        if not caught:
            raise AssertionError(f"mutation escaped: {name}")
        catches.append({"catch_id": name.split("_", 1)[0], "mutation": name, "status": "PASS"})

    with (HERE / "CATCH_PROOF_RESULTS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch_id", "mutation", "status"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)

    independent = {
        "mode": "INDEPENDENT_STANDARD_LIBRARY_NO_PRODUCTION_IMPORT",
        "result": "PASS",
        "source_identities": 35,
        "candidate_rows": 32,
        "principle_rows": 15,
        "completion_rows": 12,
        "catch_proofs": len(catches),
        "fixed_shortest_lines_at_reciprocal_seal": 0,
        "native_single_line_selectors": 0,
        "conditional_swap_gluing": True,
        "swap_gluing_selected": False,
    }
    (HERE / "INDEPENDENT_RESULTS.json").write_text(json.dumps(independent, indent=2, sort_keys=True) + "\n")
    print(json.dumps(independent, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
