#!/usr/bin/env python3
"""Exercise fail-closed mutations against the G68 package verifier."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path

from verify_package import verify_documents, verify_payload


HERE = Path(__file__).resolve().parent


def load() -> tuple[dict, dict, list[dict[str, str]], str]:
    payload = json.loads((HERE / "FINITE_PATH_RESULT.json").read_text(encoding="utf-8"))
    bundle = json.loads((HERE / "BUNDLE_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    with (HERE / "PROFILE_UNIVERSE.tsv").open(newline="", encoding="utf-8") as stream:
        profiles = list(csv.DictReader(stream, delimiter="\t"))
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    return payload, bundle, profiles, prereg


def main() -> None:
    base_payload, base_bundle, base_profiles, base_prereg = load()
    mutations = []

    def add(name, mutate):
        mutations.append((name, mutate))

    add("G01_missing_profile", lambda p, b, r, d: p["profiles"].pop())
    add("G02_duplicate_profile", lambda p, b, r, d: p["profiles"].__setitem__(1, copy.deepcopy(p["profiles"][0])))
    add("G05_hidden_outcome", lambda p, b, r, d: p.__setitem__("status_counts", {"ENDPOINT_REGULAR_NO_CAUSTIC": 20, "TURNING_NO_ENDPOINT": 1}))
    add("G06_null_residual", lambda p, b, r, d: p["profiles"][0]["residuals"].__setitem__("null", 1.0))
    add("G07_wronskian", lambda p, b, r, d: p["profiles"][0]["residuals"].__setitem__("wronskian", 1.0))
    add("G08_method_mismatch", lambda p, b, r, d: p["profiles"][0]["convergence"].__setitem__("refined_second_D_relative", 1.0))
    add("G09_bundle_missing", lambda p, b, r, d: b["rows"].pop())
    add("G10_F01_mutated", lambda p, b, r, d: p["profiles"][0]["endpoint_D"][0].__setitem__(0, 99.0))
    add("G11_reflection_mutated", lambda p, b, r, d: next(iter(p["reflection_checks"].values())).__setitem__("D_conjugation_relative", 1.0))
    add("epsilon_nonconvergence", lambda p, b, r, d: p["epsilon_limit_checks"][0].__setitem__("nonincrease_or_below_floor", False))
    add("rotation_promoted", lambda p, b, r, d: p["profiles"][3].__setitem__("polar_rotation", 0.1))
    add("profile_effect_zeroed", lambda p, b, r, d: [row.__setitem__("endpoint_D", copy.deepcopy(p["profiles"][1]["endpoint_D"])) for row in p["profiles"] if row["family"] == "F02"])
    add("G12_scope_promoted", lambda p, b, r, d: p.__setitem__("maximum_conclusion", "physical CMB profile selected"))
    add("G14_control_promoted", lambda p, b, r, d: r[0].__setitem__("profile_status", "PHYSICAL"))
    add("bounded_scope_deleted", lambda p, b, r, d: None)

    caught = {}
    for name, mutation in mutations:
        payload = copy.deepcopy(base_payload)
        bundle = copy.deepcopy(base_bundle)
        profiles = copy.deepcopy(base_profiles)
        prereg = base_prereg
        if name == "bounded_scope_deleted":
            prereg = prereg.replace("bounded slice of function space", "profile census")
        else:
            mutation(payload, bundle, profiles, prereg)
        try:
            verify_payload(payload, bundle, profiles, prereg)
            caught[name] = False
        except (AssertionError, KeyError, IndexError):
            caught[name] = True

    if not all(caught.values()):
        raise AssertionError({key: value for key, value in caught.items() if not value})

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    completeness = (HERE / "COMPLETENESS_SCOPE.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    document_mutations = {
        "exact_landing_deleted": (exact.replace("FINITE_PATH_CONTROL_ATLAS_REGULAR_WITH_PROFILE_DEPENDENCE", "CMB_PROFILE_SELECTED"), report, completeness, lay),
        "postreview_gate_demoted": (exact, report.replace("VERIFIED_WITH_CAVEATS", "LEAD_PENDING_REVIEW"), completeness, lay),
        "caustic_caveat_deleted": (exact.replace("even-multiplicity tangential zero", "zero"), report, completeness, lay),
        "bundle_caveat_deleted": (exact, report.replace("does not independently certify screen transport or endpoint selection", "fully independent"), completeness, lay),
        "completeness_time_live_promoted": (exact, report, completeness.replace("no time-live\n   metric", "time-live metric derived"), lay),
        "lay_control_scope_deleted": (exact, report, completeness, lay.replace("controls, not candidate universes", "candidate universes")),
    }
    for name, docs in document_mutations.items():
        try:
            verify_documents(*docs)
            caught[name] = False
        except AssertionError:
            caught[name] = True

    if not all(caught.values()):
        raise AssertionError({key: value for key, value in caught.items() if not value})
    result = {"caught": caught, "passed": sum(caught.values()), "total": len(caught)}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(rendered, encoding="utf-8")
    (HERE / "CATCH_PROOF_STDOUT.txt").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
