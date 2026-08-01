#!/usr/bin/env python3
"""Cold verifier for the global/local premise audit.

This implementation imports neither producer nor primary verifier.  It reads and
hashes every frozen source, rebuilds the finite logic controls, checks the amended
epistemic ceiling, and exercises semantic mutations through the same predicates.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import itertools
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
RAW = PKG / "INDEPENDENT_RAW.jsonl"
RESULT = PKG / "INDEPENDENT_RESULT.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(name: str):
    return json.loads((PKG / name).read_text(encoding="utf-8"))


def read_tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def emit(handle, kind: str, **payload) -> None:
    handle.write(json.dumps({"kind": kind, **payload}, sort_keys=True) + "\n")


def load_inventory() -> tuple[list[dict[str, str]], dict[str, str], list[str]]:
    rows = read_tsv("SOURCE_INVENTORY.tsv")
    manifest: dict[str, str] = {}
    for line in (PKG / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        digest, path = line.split("  ", 1)
        manifest[path] = digest
    paths = (PKG / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
    return rows, manifest, paths


TERM_PATTERNS = {
    "bootstrap": re.compile(r"\bbootstrap\b", re.I),
    "global_local": re.compile(r"global[- /]local|global[- ]to[- ]local|local[- ]to[- ]global", re.I),
    "self_consistency": re.compile(r"self[- ]?consisten", re.I),
    "mutual": re.compile(r"mutual(?:ly)?\s+(?:determin|admiss|tun|consisten)", re.I),
    "fixed_point": re.compile(r"fixed[- ]?point", re.I),
    "return": re.compile(r"nonidentity return|return (?:law|map|operation|operator|arrow|relation)", re.I),
    "metric_ontology": re.compile(r"metric is the theory|complete metric", re.I),
    "reciprocity": re.compile(r"\breciproc", re.I),
}

DECISIVE = re.compile(
    r"DERIVED|NOT_DERIVED|OPEN|WORKING|CONDITIONAL|POSIT|select|entail|"
    r"return|operation|relation|admissib|equation|fixed[- ]?point",
    re.I,
)


def source_census(raw_handle):
    rows, manifest, paths = load_inventory()
    failures: list[str] = []
    term_paths = Counter()
    term_hits = Counter()
    decisive_snippets: list[dict[str, object]] = []
    total_bytes = 0
    decoded = 0
    layers = Counter()

    if len(rows) != 1424 or len(paths) != 1424 or len(manifest) != 1424:
        failures.append("source cardinality is not 1424 across all three freezes")
    row_paths = [row["path"] for row in rows]
    if row_paths != paths or sorted(paths) != paths or len(set(paths)) != 1424:
        failures.append("source path freeze ordering/uniqueness mismatch")

    for row in rows:
        rel = row["path"]
        target = ROOT / rel
        data = target.read_bytes()
        total_bytes += len(data)
        digest = sha(data)
        git_blob = hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()
        if digest != row["sha256"] or digest != manifest.get(rel):
            failures.append(f"source hash mismatch: {rel}")
        if git_blob != row["git_blob"]:
            failures.append(f"source git-blob mismatch: {rel}")
        if len(data) != int(row["bytes"]):
            failures.append(f"source byte-count mismatch: {rel}")
        layers[row["layer"]] += 1
        try:
            text = data.decode("utf-8")
            decoded += 1
        except UnicodeDecodeError:
            text = data.decode("utf-8", errors="replace")
            failures.append(f"non-UTF8 frozen source: {rel}")
        counts = {name: len(regex.findall(text)) for name, regex in TERM_PATTERNS.items()}
        for name, count in counts.items():
            term_hits[name] += count
            if count:
                term_paths[name] += 1
        high = []
        for number, line in enumerate(text.splitlines(), 1):
            if DECISIVE.search(line) and any(regex.search(line) for regex in TERM_PATTERNS.values()):
                high.append({"line": number, "text": line.strip()[:500]})
        if high:
            decisive_snippets.extend({"path": rel, **item} for item in high[:12])
        emit(raw_handle, "source", path=rel, sha256=digest, git_blob=git_blob,
             bytes=len(data), terms=counts,
             decisive_lines=len(high), layer=row["layer"])

    if layers != Counter({"PARENT_1384_SOURCE_UNIVERSE": 1384,
                          "WHOLE_RECIPROCITY_PARENT_PACKAGE": 40}):
        failures.append(f"source layer census mismatch: {dict(layers)}")

    return {
        "failures": failures,
        "rows": len(rows),
        "decoded": decoded,
        "total_bytes": total_bytes,
        "term_paths": dict(term_paths),
        "term_hits": dict(term_hits),
        "layers": dict(layers),
        "decisive_snippets": decisive_snippets,
    }


def orbit_partition(states, generators):
    unseen = set(states)
    orbits = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        frontier = [seed]
        while frontier:
            item = frontier.pop()
            for generator in generators:
                nxt = generator[item]
                if nxt not in orbit:
                    orbit.add(nxt)
                    frontier.append(nxt)
        unseen -= orbit
        orbits.append(frozenset(orbit))
    return sorted(orbits, key=lambda item: tuple(sorted(item)))


def logic_controls():
    states = tuple(range(4))
    outputs = (0, 1)
    readout = {0: 0, 1: 0, 2: 1, 3: 1}
    graph = frozenset((x, readout[x]) for x in states)
    sections = []
    for low in (0, 1):
        for high in (2, 3):
            section = {0: low, 1: high}
            assert all(readout[section[o]] == o for o in outputs)
            sections.append(section)
    fixed_sets = {
        frozenset(x for x in states if sections[index][readout[x]] == x)
        for index in range(len(sections))
    }
    within_fiber_swap = {0: 1, 1: 0, 2: 3, 3: 2}
    orbits = orbit_partition(states, [within_fiber_swap])
    saturated = []
    for mask in range(1 << len(orbits)):
        subset = frozenset().union(*(orbits[i] for i in range(len(orbits)) if mask & (1 << i)))
        saturated.append(subset)
    proper = [item for item in saturated if item and item != frozenset(states)]

    # An equally equivariant larger observer action can be transitive.  This does
    # not refute the chosen countermodel; it proves its orbit count is control-local.
    cross_fiber_swap = {0: 2, 2: 0, 1: 3, 3: 1}
    transitive_orbits = orbit_partition(states, [within_fiber_swap, cross_fiber_swap])
    transitive_proper_count = 2 ** len(transitive_orbits) - 2

    return {
        "complete_state_count": len(states),
        "readout_state_count": len(outputs),
        "readout_graph_size": len(graph),
        "readout_graph_configuration_survivors": len({x for x, _ in graph}),
        "readout_is_surjective": set(readout.values()) == set(outputs),
        "readout_is_injective": len(set(readout.values())) == len(states),
        "right_inverse_section_count": len(sections),
        "distinct_section_image_count": len(fixed_sets),
        "section_fixed_set_sizes": sorted(len(item) for item in fixed_sets),
        "finite_admissibility_predicate_count": 2 ** len(states),
        "observer_orbit_count": len(orbits),
        "observer_saturated_relation_count": len(saturated),
        "nonempty_proper_observer_saturated_relation_count": len(proper),
        "proper_saturated_relations_disjoint": proper[0].isdisjoint(proper[1]),
        "proper_saturated_relation_sizes": sorted(len(item) for item in proper),
        "transitive_equivariant_control_orbit_count": len(transitive_orbits),
        "transitive_equivariant_control_nonempty_proper_saturated_count": transitive_proper_count,
        "orbit_count_is_control_local": True,
    }


EXPECTED_LOGIC = {
    "complete_state_count": 4,
    "readout_state_count": 2,
    "readout_graph_size": 4,
    "readout_graph_configuration_survivors": 4,
    "readout_is_surjective": True,
    "readout_is_injective": False,
    "right_inverse_section_count": 4,
    "distinct_section_image_count": 4,
    "section_fixed_set_sizes": [2, 2, 2, 2],
    "finite_admissibility_predicate_count": 16,
    "observer_orbit_count": 2,
    "observer_saturated_relation_count": 4,
    "nonempty_proper_observer_saturated_relation_count": 2,
    "proper_saturated_relations_disjoint": True,
    "proper_saturated_relation_sizes": [2, 2],
}


def package_state():
    premises = {row["premise_id"]: row for row in read_tsv("PREMISE_LEDGER.tsv")}
    minima = {row["level_id"]: row for row in read_tsv("MINIMUM_LEVEL_LEDGER.tsv")}
    current = {
        row["premise_id"]: row
        for row in csv.DictReader((ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").open(encoding="utf-8"), delimiter="\t")
    }
    return {
        "result": read_json("RESULT.json"),
        "algebra": read_json("ALGEBRA_RESULT.json"),
        "premises": premises,
        "minima": minima,
        "current": current,
        "report": (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8"),
        "derivation": (PKG / "EXACT_DERIVATION.md").read_text(encoding="utf-8"),
        "interpretations": read_tsv("INTERPRETATION_OUTCOMES.tsv"),
        "returns": read_tsv("RETURN_TYPE_OUTCOMES.tsv"),
    }


def evaluate(state, logic):
    result = state["result"]
    premises = state["premises"]
    minima = state["minima"]
    current = state["current"]
    report = state["report"]
    derivation = state["derivation"]
    checks = {}
    checks["logic_exact"] = all(logic.get(key) == value for key, value in EXPECTED_LOGIC.items())
    checks["emitted_algebra_matches_independent"] = all(
        state["algebra"].get(key) == value for key, value in EXPECTED_LOGIC.items()
    )
    checks["result_ceiling"] = (
        result.get("outcome") == "BOOTSTRAP_IS_DISTINCT_POSIT"
        and result.get("frozen_record_derivation_found") is False
        and result.get("deductive_independence_proved") is False
        and result.get("future_same_premise_metric_theorem_excluded") is False
        and result.get("bootstrap_adopted_by_audit") is False
        and result.get("candidate_formula_constructed") is False
        and result.get("solve_authorized") is False
        and result.get("gpu_used") is False
    )
    checks["frozen_counts"] = (
        result.get("source_paths_verified") == 1424
        and result.get("premises") == 18
        and result.get("interpretations") == 12
        and result.get("return_types") == 8
        and len(state["interpretations"]) == 12
        and len(state["returns"]) == 8
    )
    checks["bootstrap_working"] = (
        current["G12"]["epistemic_label"] == "WORKING"
        and current["G12"]["active_use"] == "ON_SHELL_ADMISSIBILITY_ONLY"
        and premises["GLP-P10"]["current_status"] == "WORKING_LENS_AND_TYPE_ARCHITECTURE"
    )
    checks["preserved_high_risk_scopes"] = (
        current["G09"]["epistemic_label"] == "POSIT"
        and current["G14"]["epistemic_label"] == "WORKING"
        and current["G15"]["active_use"] == "STATIC_FINITE_BOX_AND_CARRIER_CONDITIONAL"
        and current["G16"]["current_status"] == "OPEN"
        and current["G04"]["active_use"] == "INACTIVE_UNLESS_CHARLES_EXPLICITLY_REAUTHORIZES"
        and premises["GLP-P09"]["current_status"] == "RATIFIED_PROGRAM_CONSTRUCTION_SPLIT_STATUS"
        and premises["GLP-P12"]["current_status"] == "OPEN_OR_CONDITIONAL_BY_BRANCH"
        and premises["GLP-P13"]["current_status"] == "OPEN"
        and premises["GLP-P14"]["current_status"] == "POSIT_OR_CONDITIONAL_BY_LANE"
        and premises["GLP-P15"]["current_status"] == "OPEN_OR_OBSERVED_INPUT_BY_SCOPE"
        and premises["GLP-P17"]["current_status"] == "INACTIVE_CHALLENGED"
        and premises["GLP-P18"]["current_status"] == "POST_JULY_CPU_EXACT_ONLY"
    )
    checks["minimum_level_separation"] = (
        minima["M02"]["level"] == "NONTRIVIAL_ADMISSIBILITY_ONLY"
        and minima["M02"]["status"] == "TYPE_IDENTIFIED_INSUFFICIENT_FOR_MUTUAL_DETERMINATION"
        and "independent X times O" in minima["M03"]["minimum_object"]
        and "nontrivial dependence on both" in minima["M03"]["minimum_object"]
        and "nonempty proper intersection" in minima["M03"]["minimum_object"]
        and minima["M03"]["status"] == "MINIMUM_EXTRA_POSIT_TYPE_NOT_DERIVED_OR_ADOPTED_HERE"
        and minima["M04"]["level"] == "OPERATIONAL_MEMBERSHIP_RULE"
        and minima["M05"]["level"] == "DIFFERENTIAL_RESPONSE"
        and minima["M06"]["level"] == "VARIATIONAL_REALIZATION"
        and minima["M07"]["level"] == "DYNAMICAL_OR_STABILITY_REALIZATION"
        and result.get("minimum_extra_logical_type") ==
            "OBSERVER_NATURAL_RELATION_ON_INDEPENDENT_X_TIMES_O_WITH_NONTRIVIAL_DEPENDENCE_ON_BOTH_AND_NONEMPTY_PROPER_GRAPH_INTERSECTION"
        and result.get("minimum_type_derived") is False
    )
    checks["epistemic_wording"] = (
        "not a proof of deductive independence" in report
        and re.search(r"new\s+theorem from the same founding metric premises remains possible", report, re.I)
        and re.search(r"not\*\* a theorem that no future derivation|not a theorem that no future derivation",
                      derivation, re.I)
        and "Repeating algebra under the unchanged premise set cannot derive" not in derivation
    )
    # Proper subsets of Graph(R) are exactly predicates on X; this structure alone
    # cannot establish that O is a load-bearing return argument.  The report must
    # state that M02 is semantic nontriviality, while operational return is M03+.
    semantics = (report + "\n" + derivation).lower()
    checks["m02_not_misnamed_operational_return"] = (
        "operational mutual-determination type" in semantics
        and re.search(r"explicit.{0,30}membership rule", semantics, re.S)
        and (
            re.search(r"does not by itself (?:encode|show|make|establish).{0,50}global.{0,50}(?:return|load-bearing|feed back)",
                      semantics, re.S)
        )
        and "independently varied `x` and `o`" in semantics
        and "nontrivial dependence on" in semantics
    )
    checks["observer_orbit_scope"] = (
        logic["transitive_equivariant_control_nonempty_proper_saturated_count"] == 0
        and (
            "two-orbit control" in semantics
            or "complete observer action" in semantics and "open" in semantics
        )
    )
    return checks


SOURCE_RULINGS = {
    "udt_global_local_relational_closure_audit_2026-07-25/AUDIT_REPORT.md":
        r"joined closure is not currently derived",
    "udt_bootstrap_to_local_response_map_audit_2026-07-25/AUDIT_REPORT.md":
        r"supplies neither complete arrow",
    "udt_native_global_observable_closure_census_2026-07-26/AUDIT_REPORT.md":
        r"do not yet turn that vocabulary into one\s+complete differentiable physical state vector",
    "udt_stability_foundations_audit_2026-08-01/BOOTSTRAP_FIXED_POINT_SCHEMA.tsv":
        r"DERIVED_AS_TYPE_SCHEMA_ONLY",
    "udt_joint_realization_closure_audit_2026-08-01/AUDIT_REPORT.md":
        r"Bootstrap diagram is not bootstrap closure",
    "udt_jr_cert_native_derivation_2026-08-01/EQUATION_ROUTE_ADJUDICATION.tsv":
        r"TWO_ARROW_TYPE_DERIVED_MAPS_AND_FIXED_POINT_OPEN",
    "udt_bootstrap_closure_ownership_audit_2026-08-01/AUDIT_REPORT.md":
        r"none of the eight preregistered routes supplies the distinct nonidentity return",
    "udt_whole_configuration_reciprocity_audit_2026-08-01/AUDIT_REPORT.md":
        r"does not supply the missing nonidentity return operation",
    "udt_p4_routeA_slice2_solution_legs_2026-07-29/EXACT_DERIVATION.md":
        r"bootstrap-shaped structure is pairing-branch-RELATIVE",
    "udt_p4_routeA_stage2_pointwise_reduction_2026-07-29/EXACT_DERIVATION.md":
        r"NO\s+member of.*selected or privileged",
    "bootstrap_variation_selector_2026-07-18/STATUS_LEDGER.tsv":
        r"OWNER_STATED_WORKING",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv":
        r"OPEN",
}


def source_ruling_checks():
    checks = {}
    for path, pattern in SOURCE_RULINGS.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        checks[path] = re.search(pattern, text, re.I | re.S) is not None
    return checks


def run_mutations(state, logic):
    mutations = []

    def add(name, target, mutate_state=None, mutate_logic=None):
        trial_state = copy.deepcopy(state)
        trial_logic = copy.deepcopy(logic)
        if mutate_state:
            mutate_state(trial_state)
        if mutate_logic:
            mutate_logic(trial_logic)
        before = evaluate(state, logic)[target]
        after = evaluate(trial_state, trial_logic)[target]
        mutations.append({"name": name, "target": target, "baseline": before,
                          "mutant": after, "rejected": before is True and after is False})

    add("bootstrap_promoted_to_derived", "bootstrap_working",
        lambda s: s["current"]["G12"].update(epistemic_label="DERIVED"))
    add("bootstrap_adopted", "result_ceiling",
        lambda s: s["result"].update(bootstrap_adopted_by_audit=True))
    add("candidate_formula_smuggled", "result_ceiling",
        lambda s: s["result"].update(candidate_formula_constructed=True))
    add("same_premise_theorem_universally_excluded", "result_ceiling",
        lambda s: s["result"].update(future_same_premise_metric_theorem_excluded=True))
    add("minimum_type_promoted", "minimum_level_separation",
        lambda s: s["minima"]["M03"].update(status="DERIVED_AND_ADOPTED"))
    add("nonempty_removed_from_minimum", "minimum_level_separation",
        lambda s: s["minima"]["M03"].update(
            minimum_object=s["minima"]["M03"]["minimum_object"].replace("nonempty ", "")))
    add("response_one_form_collapsed_to_premise_minimum", "minimum_level_separation",
        lambda s: s["minima"]["M05"].update(level="OPERATIONAL_MUTUAL_DETERMINATION_TYPE"))
    add("carrier_promoted", "preserved_high_risk_scopes",
        lambda s: s["current"]["G09"].update(epistemic_label="DERIVED"))
    add("strong_CSN_reactivated", "preserved_high_risk_scopes",
        lambda s: s["current"]["G04"].update(active_use="ACTIVE_GAUGE"))
    add("finite_cell_misattributed_as_owner_bedrock", "preserved_high_risk_scopes",
        lambda s: s["premises"]["GLP-P09"].update(current_status="OWNER_BEDROCK"))
    add("pre_july_affirmative_use_enabled", "preserved_high_risk_scopes",
        lambda s: s["premises"]["GLP-P18"].update(current_status="PRE_JULY_AFFIRMATIVE_ALLOWED"))
    add("readout_made_injective", "logic_exact",
        mutate_logic=lambda value: value.update(readout_is_injective=True))
    add("section_count_falsified", "logic_exact",
        mutate_logic=lambda value: value.update(right_inverse_section_count=1))
    add("observer_saturation_count_falsified", "logic_exact",
        mutate_logic=lambda value: value.update(
            nonempty_proper_observer_saturated_relation_count=1))
    add("deductive_independence_phrase_restored", "epistemic_wording",
        lambda s: s.update(derivation=s["derivation"] +
                           "\nRepeating algebra under the unchanged premise set cannot derive membership.\n"))
    return mutations


def main() -> int:
    with RAW.open("w", encoding="utf-8") as raw_handle:
        census = source_census(raw_handle)
        logic = logic_controls()
        state = package_state()
        checks = evaluate(state, logic)
        source_checks = source_ruling_checks()
        mutations = run_mutations(state, logic)
        emit(raw_handle, "source_summary", **{k: v for k, v in census.items()
                                               if k != "decisive_snippets"})
        for snippet in census["decisive_snippets"]:
            emit(raw_handle, "decisive_source_line", **snippet)
        emit(raw_handle, "logic", **logic)
        for name, passed in checks.items():
            emit(raw_handle, "package_check", name=name, passed=passed)
        for path, passed in source_checks.items():
            emit(raw_handle, "source_ruling", path=path, passed=passed)
        for mutation in mutations:
            emit(raw_handle, "mutation", **mutation)

    failed_checks = [name for name, passed in checks.items() if not passed]
    failed_sources = [path for path, passed in source_checks.items() if not passed]
    failed_mutations = [item["name"] for item in mutations if not item["rejected"]]
    core_failures = census["failures"] + failed_sources + failed_mutations
    if core_failures:
        verdict = "REFUTED_IN_PART"
    elif failed_checks:
        verdict = "PASS_WITH_REQUIRED_AMENDMENTS"
    else:
        verdict = "PASS"
    result = {
        "verdict": verdict,
        "source_paths_read_and_hashed": census["rows"],
        "source_bytes_read": census["total_bytes"],
        "source_utf8_decoded": census["decoded"],
        "source_layers": census["layers"],
        "source_term_paths": census["term_paths"],
        "logic": logic,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "failed_checks": failed_checks,
        "source_rulings_passed": sum(source_checks.values()),
        "source_rulings_total": len(source_checks),
        "failed_source_rulings": failed_sources,
        "mutations_rejected": sum(item["rejected"] for item in mutations),
        "mutations_total": len(mutations),
        "failed_mutations": failed_mutations,
        "core_outcome_retained": not core_failures,
        "deductive_independence_proved": False,
        "m02_graph_relation_encodes_return": False,
        "m02_graph_relation_encodes_nontrivial_admissibility": True,
        "m03_independent_xo_mutual_determination_type_passes":
            checks.get("m02_not_misnamed_operational_return", False),
        "observer_saturation_count_is_control_local": True,
        "gpu_used": False,
        "producer_or_primary_verifier_imported": False,
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
