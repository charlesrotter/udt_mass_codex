#!/usr/bin/env python3
"""Independent stdlib verification and exercised corruption catches."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
import subprocess
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "5457a36f96e46424032899dcb1a1a0874f273c58"


class Failure(RuntimeError):
    pass


def need(value: bool, message: str) -> None:
    if not value:
        raise Failure(message)


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def direct_algebra() -> dict[str, bool]:
    checks: dict[str, bool] = {}
    for i, (n, h, b, c) in enumerate([
        (Q(3), Q(5, 2), Q(1, 7), Q(11, 3)),
        (Q(8, 3), Q(9, 4), Q(-2, 9), Q(7, 2)),
    ]):
        g00 = c * c * (-n * n + h * h * b * b)
        g01 = c * h * h * b
        g11 = h * h
        checks[f"direct_det_{i}"] = g00 * g11 - g01 * g01 == -c * c * n * n * h * h
        roots = [c * (-b - n / h), c * (-b + n / h)]
        for j, root in enumerate(roots):
            checks[f"direct_root_{i}_{j}"] = g00 + 2 * g01 * root + g11 * root * root == 0

    # Derive path times directly as sums, without importing production code.
    weights = [Q(2), Q(3), Q(5)]
    lapses = [Q(7), Q(7), Q(7)]
    length = sum(weights)
    optical = sum(w / n for w, n in zip(weights, lapses))
    checks["direct_uniform_path"] = length / optical == 7
    changed = sum(weights) / sum(w / n for w, n in zip(weights, [Q(2), Q(7), Q(11)]))
    changed2 = sum([Q(4), Q(3), Q(5)]) / sum(w / n for w, n in zip([Q(4), Q(3), Q(5)], [Q(2), Q(7), Q(11)]))
    checks["direct_weight_dependence"] = changed != changed2

    d = Q(10**5)
    h = 1 / d
    n_two = Q(1) * d
    n_cancel = (1 / d) * d
    n_reverse = (1 / (d * d)) * d
    checks["cf01_two_ended"] = n_two == d and n_two / h == d * d
    checks["cf02_cancelled"] = n_cancel == 1 and n_cancel / h == d
    checks["cf03_reversed"] = n_reverse == 1 / d and n_reverse / h == 1
    checks["cf04_oscillatory"] = abs((2 + math.sin(0)) - (2 + math.sin(math.pi / 2))) > 0.9
    hb = d - 1
    checks["cf05_shift_oneway"] = d - hb == 1 and d + hb == 2 * d - 1
    checks["cf05_shift_roundtrip"] = Q(2) / (1 / (d - hb) + 1 / (d + hb)) < 2
    checks["cf05_shift_timelike"] = hb < d
    checks["cf06_uniform_path"] = length / optical == 7
    checks["cf07_nonuniform_path"] = changed != changed2
    checks["cf08_bottleneck"] = Q(3) / (Q(2) / d + 1) < 3
    return checks


def validate(
    payload: dict,
    sources: list[dict[str, str]],
    candidates: list[dict[str, str]],
    branches: list[dict[str, str]],
    summaries: list[dict[str, str]],
    counters: list[dict[str, str]],
    selectors: list[dict[str, str]],
    overlaps: list[dict[str, str]],
) -> None:
    need(payload["base"] == BASE, "wrong base")
    need(len(sources) == 25, "source file count")
    need(sum(row["source_kind"] == "CANDIDATE_REGISTRY" for row in sources) == 23, "source registry count")
    need(sum(row["source_kind"] == "LOAD_BEARING_SUPPORT" for row in sources) == 2, "support source count")
    need({row["source_id"] for row in sources if row["source_kind"] == "LOAD_BEARING_SUPPORT"} == {"SUP01", "SUP02"}, "support identities")
    need(sum(int(row["row_count"]) for row in sources) == 380, "source row total")
    for row in sources:
        path = ROOT / row["path"]
        need(path.exists(), "missing source " + row["source_id"])
        base_bytes = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
        base_blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{row['path']}"], cwd=ROOT, text=True).strip()
        need(path.read_bytes() == base_bytes, "working source differs from base " + row["source_id"])
        need(hashlib.sha256(base_bytes).hexdigest() == row["sha256"], "source hash " + row["source_id"])
        need(base_blob == row["git_blob"], "source blob " + row["source_id"])
    toric_source = json.loads((ROOT / next(row["path"] for row in sources if row["source_id"] == "SUP01")).read_text(encoding="utf-8"))
    connector_source = json.loads((ROOT / next(row["path"] for row in sources if row["source_id"] == "SUP02")).read_text(encoding="utf-8"))
    need(toric_source["metric"] == "-dt^2 + A(phi)^2 dphi^2 + Omega(phi)^2[exp(-2phi)dxi1^2+exp(2phi)dxi2^2]", "toric metric provenance")
    need(toric_source["reflection_status"] == "CONDITIONAL_NOT_FORCED_FOR_ARBITRARY_A_OMEGA", "toric global guard")
    need(connector_source["formulas"]["stationary_connector_metric"] == "ds^2=-c_E^2*N^2*dt^2+H^2*(dlambda+c_E*B*dt)^2", "connector metric provenance")
    need(connector_source["bounded_classifications"]["material_information_transfer"] == "NOT_TESTED", "connector information guard")
    need(len(candidates) == 380, "candidate row count")
    need(len({row["candidate_row_id"] for row in candidates}) == 380, "candidate ids")
    need(all(
        row["identity_relation"] == "CROSS_PRODUCT_PRESENTATION_NOT_SOLVED_UNIVERSE"
        for row in candidates if row["source_id"] == "SRC02"
    ), "motif cross rows promoted to universes")
    need(len(branches) == 84, "branch cross rows")
    need(len({row["assembly_id"] for row in branches}) == 84, "branch ids")
    motifs = {row["motif"] for row in branches}
    completions = {row["completion_id"] for row in branches}
    need(len(motifs) == 7 and len(completions) == 12, "cross axes")
    need({(m, c) for m in motifs for c in completions} == {(r["motif"], r["completion_id"]) for r in branches}, "full cross product")
    control_rows = [row for row in branches if row["data_sufficiency"] == "CONNECTOR_CONDITIONAL"]
    need(len(control_rows) == 12, "conditional control presentations")
    need({row["metric_control_identity"] for row in control_rows} == {"TC01_RECIPROCAL_TORIC_STATIC_METRIC"}, "unique control identity")
    need(sum(row["accessibility_class"] == "UNDEFINED_MISSING_CONNECTOR_DATA" for row in branches) == 72, "undefined rows")
    need(sum(row["accessibility_class"] == "FINITE_OR_CANCELLED" for row in branches) == 12, "finite interior presentations")
    need(not any(row["global_connector_status"] == "SUPPLIED" for row in branches), "invented complete global connector")
    for row in branches:
        if row["data_sufficiency"] != "CONNECTOR_CONDITIONAL":
            need(row["accessibility_class"] == "UNDEFINED_MISSING_CONNECTOR_DATA", "promoted incomplete row")
        if row["motif"] == "RECIPROCAL_TORIC_CONTROL":
            need(row["time_threading"] == "N=1_IN_DECLARED_REPRESENTATIVE", "toric lapse")
            need(row["shift"] == "B=0", "toric shift")
            need("PATH" in row["spatial_or_angular_connector"], "toric path weight dropped")
            need(row["global_connector_status"] == "NOT_SUPPLIED__LOCAL_CONTROL_PRESENTATION_ONLY", "global connector promotion")
    compatibility_counts = {
        key: sum(row["global_compatibility_class"] == key for row in control_rows)
        for key in ["CONDITIONAL", "CONDITIONAL_SINGULAR", "RESTRICTED_SUBSET", "OPEN_CHECK_REQUIRED", "INCOMPATIBLE_AS_SAME_DISTRIBUTION"]
    }
    need(compatibility_counts == {"CONDITIONAL": 6, "CONDITIONAL_SINGULAR": 1, "RESTRICTED_SUBSET": 1, "OPEN_CHECK_REQUIRED": 3, "INCOMPATIBLE_AS_SAME_DISTRIBUTION": 1}, "control compatibility counts")
    fc11 = next(row for row in control_rows if row["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION")
    need(fc11["global_compatibility_class"] == "INCOMPATIBLE_AS_SAME_DISTRIBUTION", "FC11 false compatibility")
    fc06 = next(row for row in control_rows if row["completion_id"] == "FC06_NONPRIMITIVE_CAP")
    need(fc06["global_completion_status"] == "GLOBAL_ORBIFOLD_OR_SINGULAR_COMPLETION", "FC06 global status")
    need(fc06["interior_optical_class"] == "FINITE_OR_CANCELLED", "FC06 optical status")
    need(len(summaries) == 12 and all(row["completion_level_ruling"] == "ACCESSIBILITY_NOT_SELECTED" for row in summaries), "completion summaries")
    need(all(row["undefined_connector_rows"] == "6" and row["conditional_control_presentations"] == "1" for row in summaries), "summary coverage")
    need({row["unique_control_identity"] for row in summaries} == {"TC01_RECIPROCAL_TORIC_STATIC_METRIC_SHARED_ACROSS_12_PRESENTATIONS"}, "summary control inflation")
    need(len(counters) == 8 and len({row["id"] for row in counters}) == 8, "counterfamilies")
    need({row["class"] for row in counters} >= {"FINITE_OR_CANCELLED", "REVERSED", "OSCILLATORY_OR_NO_LIMIT"}, "counter classes")
    need(all(row["global_extension_status"] == "UNPROVED" for row in counters), "global branch-preserving overclaim")
    need(len(selectors) == 7, "selector axes")
    need(not any(row["audit_class"] == "SELECTS" for row in selectors), "invented selecting premise")
    need(any(row["selector"] == "BOOTSTRAP" and row["audit_class"] == "OPEN" for row in selectors), "bootstrap grade")
    need(payload["information_transfer"] == "OPEN_NOT_TESTED", "information overclaim")
    need(len(overlaps) == 6 and {row["equivalence_id"] for row in overlaps} == {f"EQ{i:02d}" for i in range(1, 7)}, "overlap map")
    eq03 = next(row for row in overlaps if row["equivalence_id"] == "EQ03")
    need(eq03["unique_identity_count"] == "1" and eq03["presentation_count"] == "12", "control overlap identity")
    need(payload["source_files"] == 25 and payload["source_registries"] == 23 and payload["supporting_sources"] == 2, "payload source counts")
    need(payload["conditional_control_presentations"] == 12, "payload control presentations")
    need(payload["unique_conditional_metric_controls"] == 1, "payload unique control")
    need(payload["undefined_connector_rows"] == 72, "payload undefined")
    need(payload["finite_or_cancelled_control_presentations"] == 12, "payload finite")
    need(payload["complete_global_connectors"] == 0, "payload global connector")
    need(payload["control_global_compatibility_counts"] == compatibility_counts, "payload compatibility")
    need(payload["overlap_equivalence_rows"] == 6, "payload overlap count")
    need(payload["formulas"]["toric_control"].startswith("N=1;B=0"), "toric formula")
    need(all(payload["checks"].values()), "production algebra")


def catches(original: dict[str, object]) -> list[dict[str, str]]:
    cases = []

    def exercise(name: str, mutate) -> None:
        state = copy.deepcopy(original)
        mutate(state)
        caught = False
        try:
            validate(**state)
        except (Failure, KeyError, ValueError, TypeError):
            caught = True
        cases.append({"catch_id": name, "result": "PASS" if caught else "FAIL"})

    exercise("C01_MISSING_CANDIDATE", lambda s: s["candidates"].pop())
    exercise("C02_DUPLICATE_CANDIDATE", lambda s: s["candidates"].append(copy.deepcopy(s["candidates"][0])))
    exercise("C03_MISSING_BRANCH", lambda s: s["branches"].pop())
    exercise("C04_DUPLICATE_BRANCH", lambda s: s["branches"].append(copy.deepcopy(s["branches"][0])))
    exercise("C05_BREAK_CROSS_PRODUCT", lambda s: s["branches"][0].update({"completion_id": s["branches"][1]["completion_id"]}))
    exercise("C06_PROMOTE_DISTRIBUTION", lambda s: next(r for r in s["branches"] if r["data_sufficiency"] == "DISTRIBUTION_ONLY").update({"accessibility_class": "FORCED_TWO_ENDED"}))
    exercise("C07_DROP_TORIC_LAPSE", lambda s: next(r for r in s["branches"] if r["motif"] == "RECIPROCAL_TORIC_CONTROL").update({"time_threading": "NOT_SUPPLIED"}))
    exercise("C08_ADD_TORIC_SHIFT", lambda s: next(r for r in s["branches"] if r["motif"] == "RECIPROCAL_TORIC_CONTROL").update({"shift": "B=1"}))
    exercise("C09_INVENT_SELECTOR", lambda s: s["selectors"][0].update({"audit_class": "SELECTS"}))
    exercise("C10_BOOTSTRAP_OVERCLAIM", lambda s: next(r for r in s["selectors"] if r["selector"] == "BOOTSTRAP").update({"audit_class": "SELECTS"}))
    exercise("C11_INFORMATION_OVERCLAIM", lambda s: s["payload"].update({"information_transfer": "DERIVED"}))
    exercise("C12_INFLATE_PRESENTATIONS_TO_UNIQUE_CONTROLS", lambda s: s["payload"].update({"unique_conditional_metric_controls": 12}))
    exercise("C13_WRONG_UNDEFINED_COUNT", lambda s: s["payload"].update({"undefined_connector_rows": 71}))
    exercise("C14_DROP_COUNTERFAMILY", lambda s: s["counters"].pop())
    exercise("C15_SOURCE_HASH_MUTATION", lambda s: s["sources"][0].update({"sha256": "0" * 64}))
    exercise("C16_OVERLAP_AS_UNIVERSE", lambda s: s["candidates"][12].update({"identity_relation": "INDEPENDENT_COMPLETE_UNIVERSE"}))
    exercise("C17_FC06_GLOBAL_OPTICAL_CONFLATION", lambda s: next(r for r in s["branches"] if r["completion_id"] == "FC06_NONPRIMITIVE_CAP" and r["motif"] == "RECIPROCAL_TORIC_CONTROL").update({"global_completion_status": "FINITE_OR_CANCELLED"}))
    exercise("C18_TREAT_12_COMPLETIONS_AS_SELECTED", lambda s: s["summaries"][0].update({"completion_level_ruling": "SELECTED"}))
    exercise("C19_DROP_PATH_WEIGHT", lambda s: next(r for r in s["branches"] if r["motif"] == "RECIPROCAL_TORIC_CONTROL").update({"spatial_or_angular_connector": "IRRELEVANT"}))
    exercise("C20_TORIC_FORMULA_MUTATION", lambda s: s["payload"]["formulas"].update({"toric_control": "N=D;B=0"}))
    exercise("C21_MISSING_CONTROL_PROVENANCE", lambda s: s["sources"].pop(next(i for i, r in enumerate(s["sources"]) if r["source_id"] == "SUP01")))
    exercise("C22_FC11_FALSE_COMPATIBILITY", lambda s: next(r for r in s["branches"] if r["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION" and r["motif"] == "RECIPROCAL_TORIC_CONTROL").update({"global_compatibility_class": "CONDITIONAL"}))
    exercise("C23_BRANCH_PRESERVING_OVERCLAIM", lambda s: s["counters"][0].update({"global_extension_status": "PROVED"}))
    exercise("C24_MISSING_OVERLAP_MAP", lambda s: s["overlaps"].pop())
    exercise("C25_DUPLICATE_CONTROL_ID", lambda s: s["branches"][next(i for i, r in enumerate(s["branches"]) if r["motif"] == "RECIPROCAL_TORIC_CONTROL")].update({"metric_control_identity": "TC02_FALSE_SECOND_CONTROL"}))
    exercise("C26_GLOBAL_CONNECTOR_PROMOTION", lambda s: next(r for r in s["branches"] if r["motif"] == "RECIPROCAL_TORIC_CONTROL").update({"global_connector_status": "SUPPLIED"}))
    return cases


def main() -> None:
    payload = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    state = {
        "payload": payload,
        "sources": table("SOURCE_CENSUS.tsv"),
        "candidates": table("CANDIDATE_ROW_LEDGER.tsv"),
        "branches": table("ASSEMBLED_BRANCH_ATLAS.tsv"),
        "summaries": table("COMPLETION_SUMMARY.tsv"),
        "counters": table("COUNTERFAMILY_ATLAS.tsv"),
        "selectors": table("SELECTOR_EFFECT_ATLAS.tsv"),
        "overlaps": table("IDENTITY_EQUIVALENCE_MAP.tsv"),
    }
    validate(**state)
    independent = direct_algebra()
    need(all(independent.values()), "independent algebra")
    catch_rows = catches(state)
    need(all(row["result"] == "PASS" for row in catch_rows), "catch proofs")
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch_id", "result"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catch_rows)
    result = {
        "status": "PASS",
        "base": BASE,
        "independent_checks": independent,
        "independent_check_count": len(independent),
        "catch_proofs": len(catch_rows),
        "candidate_rows": len(state["candidates"]),
        "assembled_cross_rows": len(state["branches"]),
        "conditional_control_presentations": 12,
        "unique_conditional_metric_controls": 1,
        "undefined_rows": 72,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "VERIFICATION_RESULT.json").write_text(rendered, encoding="utf-8")
    (HERE / "VERIFY_STDOUT.txt").write_text(rendered, encoding="utf-8")
    (HERE / "VERIFY_STDERR.txt").write_text("", encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
