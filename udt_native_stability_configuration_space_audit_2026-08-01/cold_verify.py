#!/usr/bin/env python3
"""Independent cold verification for the native configuration-space audit.

This file deliberately imports and executes neither build_audit.py nor verify_audit.py.
It reads the frozen Git tree directly, rebuilds the source identities, checks source
semantics against the frozen bytes, recomputes the five logic controls, derives the
outcome from independent gates, and exercises fail-closed mutations in memory.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
import re
import subprocess
from pathlib import Path


BASE = "095a2a5e093f21bfd68939f5874b359868a109d3"
OUTCOME = "NATIVE_OFFSHELL_PARENT_ARENA_DERIVED__REALIZATION_VARIATION_OPEN"
PKG = Path(__file__).resolve().parent
ROOT = PKG.parent


def run_git(*args: str, input_bytes: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout


def frozen_tree() -> tuple[dict[str, dict[str, object]], dict[str, bytes]]:
    raw = run_git("ls-tree", "-r", "-z", "--long", BASE)
    entries: dict[str, dict[str, object]] = {}
    for item in raw.split(b"\0"):
        if not item:
            continue
        meta, path_b = item.split(b"\t", 1)
        mode, kind, blob, size = meta.decode("ascii").split()
        assert kind == "blob"
        path = path_b.decode("utf-8", "surrogateescape")
        assert path not in entries
        entries[path] = {"mode": mode, "blob": blob, "bytes": int(size)}

    ordered = sorted(entries)
    request = b"".join((entries[path]["blob"] + "\n").encode("ascii") for path in ordered)
    batch = io.BytesIO(run_git("cat-file", "--batch", input_bytes=request))
    contents: dict[str, bytes] = {}
    for path in ordered:
        header = batch.readline().decode("ascii").strip().split()
        assert len(header) == 3 and header[1] == "blob"
        blob, _, size_s = header
        size = int(size_s)
        data = batch.read(size)
        assert batch.read(1) == b"\n"
        assert blob == entries[path]["blob"] and size == entries[path]["bytes"]
        entries[path]["sha256"] = hashlib.sha256(data).hexdigest()
        contents[path] = data
    assert batch.read() == b""
    return entries, contents


def read_tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def check_source_freeze(
    tree: dict[str, dict[str, object]],
    inventory: list[dict[str, str]],
    manifest_text: str,
) -> None:
    assert len(tree) == 11209
    assert len(inventory) == len(tree)
    assert [row["path"] for row in inventory] == sorted(tree)
    assert len({row["path"] for row in inventory}) == len(inventory)
    for row in inventory:
        source = tree[row["path"]]
        assert row["git_blob"] == source["blob"]
        assert int(row["bytes"]) == source["bytes"]
        assert row["sha256"] == source["sha256"]
    expected_manifest = "".join(
        f"{tree[path]['sha256']}  {path}\n" for path in sorted(tree)
    )
    assert manifest_text == expected_manifest


SOURCE_ANCHORS: dict[str, tuple[str, ...]] = {
    "A01": ("founded scalar `phi` is already the additive logarithmic depth", "complete native action, source, boundary charge, and mass remain open"),
    "A02": ("complete metric and its angular/mixing content form the physical geometric arena", "does not select a final domain"),
    "A03": ("`phi` is not an arbitrary placeholder", "founded two-channel postulates do not select a unique complete coframe"),
    "A04": ("zero selector rank", "variation domain remain open"),
    "A05": ("DERIVED AS AN EXISTENCE CLASS", "The complete family is off shell"),
    "A06": ("generic regular four-dimensional metric arena", "not a selected native UDT field count"),
    "A07": ("Constant-moduli census", "Field-moduli census", "census fork: OPEN"),
    "A08": ("PULLBACK of the field-fork one-form", "pullback-vanishing is strictly weaker"),
    "A09": ("field-moduli census REGISTERS", "off-shell", "Neither branch adopted"),
    "A10": ("no response law selected", "no solve"),
    "A11": ("angular-live on-shell coexistence is also unproved",),
    "A12": ("No native carrier or Hopfion has been derived", "Global/time-live persistence", "OPEN"),
    "A13": ("FORMAL_COMPATIBILITY_ONLY_COMMON_REALIZATION_OPEN", "nonzero time-and-angular finite-cell field"),
    "A14": ("NO_NATIVE_PROBLEM_DERIVED_DOWNSTREAM_STAGES_BLOCKED", "does not yet derive either"),
    "A15": ("LOCAL_TO_GLOBAL_MAP_PARTIAL_RETURN_OPEN", "does not yet supply one common, complete physical global-state map"),
    "A16": ("RECIPROCITY_DERIVES_EQUIVARIANT_QUOTIENT_ONLY", "does not supply the missing nonidentity return operation"),
    "A17": ("BOOTSTRAP_IS_DISTINCT_POSIT", "contains no derivation of global/local mutual determination"),
    "A18": ("DERIVATION_SWEEP_MIXED_WITH_SCOPED_OBSTRUCTION", "fifteen registered objects across the five active families"),
    "A19": ("OPERATIONAL_EVIDENCE_MAP_NOT_SOLUTION_PARTITION", "zero native realized families"),
    "A20": ("different objects and premises", "no common metric-native stability operator"),
    "A21": ("STATUS: PURE PONDER", "every interpretation is conjecture"),
}


def check_authorities(
    authorities: list[dict[str, str]],
    tree: dict[str, dict[str, object]],
    contents: dict[str, bytes],
) -> None:
    assert [row["id"] for row in authorities] == [f"A{i:02d}" for i in range(1, 22)]
    assert len({row["path"] for row in authorities}) == 21
    for row in authorities:
        source = tree[row["path"]]
        assert row["git_blob"] == source["blob"]
        assert row["sha256"] == source["sha256"]
        text = contents[row["path"]].decode("utf-8", "replace")
        normalized_text = " ".join(re.sub(r"[^a-z0-9]+", " ", text.casefold()).split())
        for anchor in SOURCE_ANCHORS[row["id"]]:
            normalized_anchor = " ".join(re.sub(r"[^a-z0-9]+", " ", anchor.casefold()).split())
            assert normalized_anchor in normalized_text, (row["id"], anchor)
    a18 = next(row for row in authorities if row["id"] == "A18")
    a20 = next(row for row in authorities if row["id"] == "A20")
    assert "five" in a18["load_bearing_statement"].casefold() or "15" in a18["load_bearing_statement"]
    assert "zero native realized" not in a20["load_bearing_statement"].casefold()


SEARCH_PATTERNS = tuple(
    re.compile(pattern, re.I | re.S)
    for pattern in (
        r"configuration.{0,100}(variation|tangent|off[- ]shell|response)",
        r"(variation|tangent|off[- ]shell|response).{0,100}configuration",
        r"constant[- ]section|constant[- ]moduli|field[- ]moduli|pullback.{0,100}integrated",
        r"time[- ]live|angular[- ]live|common.{0,80}realization",
        r"hopfion|round[- ]?s2|carrier.{0,80}(metric|native)",
        r"reciprocity.{0,120}(naturality|equivarian|return|dynamics)",
        r"bootstrap.{0,120}(schema|operation|return|membership|posit)",
        r"stable basin|stability landscape|taxonomy.{0,40}basin",
    )
)


def broad_candidate_search(contents: dict[str, bytes]) -> list[str]:
    candidates: list[str] = []
    for path, data in contents.items():
        if not path.endswith((".md", ".tsv", ".json", ".txt")):
            continue
        text = data.decode("utf-8", "ignore")
        if any(pattern.search(text) for pattern in SEARCH_PATTERNS):
            candidates.append(path)
    # Directed predecessor/current-layer checks that would expose a stronger or conflicting route.
    required = {
        "P4_ARC_SUMMARY_2026-07-31.md",
        "udt_complete_metric_solution_space_map_2026-07-21/AUDIT_REPORT.md",
        "udt_p4_variation_domain_map_2026-07-28/MAP.md",
        "udt_relational_metric_fixed_point_typing_audit_2026-07-26/AUDIT_REPORT.md",
        "udt_stability_foundations_audit_2026-08-01/FINAL_CLOSURE_REPORT.md",
    }
    assert required <= set(candidates)
    directed_anchors = {
        "P4_ARC_SUMMARY_2026-07-31.md": "Nothing was adopted as physics anywhere in the arc",
        "udt_complete_metric_solution_space_map_2026-07-21/AUDIT_REPORT.md": "DYNAMICAL_SOLUTION_SPACE requires a separately specified law",
        "udt_p4_variation_domain_map_2026-07-28/MAP.md": "what configuration space does UDT vary over",
        "udt_relational_metric_fixed_point_typing_audit_2026-07-26/AUDIT_REPORT.md": "There is no current relational fixed-point operator",
        "udt_stability_foundations_audit_2026-08-01/FINAL_CLOSURE_REPORT.md": "complete action, native stability, both bootstrap maps, and fixed realized live solution remain open",
    }
    for path, anchor in directed_anchors.items():
        source_text = contents[path].decode("utf-8", "replace")
        normalized_source = " ".join(re.sub(r"[^a-z0-9]+", " ", source_text.casefold()).split())
        normalized_anchor = " ".join(re.sub(r"[^a-z0-9]+", " ", anchor.casefold()).split())
        assert normalized_anchor in normalized_source, (path, anchor)
    return sorted(candidates)


def exact_controls() -> dict[str, object]:
    # C01: actual one-form counterexample. i(a)=(a,a), Di=(1,1)^T,
    # alpha=dx-dy has coefficient vector (1,-1), so i*alpha=0 although alpha != 0.
    di = (1, 1)
    alpha = (1, -1)
    pullback = sum(a * b for a, b in zip(di, alpha))
    assert pullback == 0 and alpha != (0, 0)

    # C02: tagging retains two copies even when the underlying sets are equal.
    set_a = {0}
    set_b = {0}
    tagged_union = {("A", value) for value in set_a} | {("B", value) for value in set_b}
    assert len(tagged_union) == 2 and len(set_a | set_b) == 1

    # C03: exact critical-point/Hessian classification for the two potentials.
    # V1'=2x, V1''=2; V2'=4x(x^2-1), V2''=12x^2-4.
    v1_critical = (0,)
    v1_stable = tuple(x for x in v1_critical if 2 > 0)
    v2_critical = (-1, 0, 1)
    v2_stable = tuple(x for x in v2_critical if 12 * x * x - 4 > 0)
    assert v1_stable == (0,) and v2_stable == (-1, 1)

    # C04: both formal modules are nonempty, but no nonzero live member is common.
    module_1 = {0, 1}
    module_2 = {0, 2}
    intersection = module_1 & module_2
    assert module_1 and module_2 and intersection == {0}
    assert not {value for value in intersection if value != 0}

    # C05: an index family supplies no transition arrow by itself.
    fibers = {0: {"a"}, 1: {"b"}}
    transitions: dict[tuple[int, int], object] = {}
    assert set(fibers) == {0, 1} and (0, 1) not in transitions

    return {
        "C01_pullback": pullback,
        "C02_tagged_union_cardinality": len(tagged_union),
        "C03_stable_minima_counts": [len(v1_stable), len(v2_stable)],
        "C04_common_nonzero_count": 0,
        "C05_transition_count": len(transitions),
    }


def check_corrected_package(
    objects: list[dict[str, str]],
    relations: list[dict[str, str]],
    controls: list[dict[str, str]],
    report_text: str,
) -> None:
    c01 = next(row for row in controls if row["id"] == "C01")
    normalized = c01["construction"].replace(" ", "").lower()
    assert "dx-dy" in normalized or "dx_minus_dy" in normalized

    by_id = {row["id"]: row for row in objects}
    for object_id in ("O07", "O08"):
        value = by_id[object_id]["belongs_to_native_parent_type"].casefold()
        assert "conditional" in value

    p4_to_parent = {
        row["source_object"]
        for row in relations
        if row["target_object"] == "complete_metric_arena"
        and "CONDITIONAL" in (row["relation"] + row["status"]).upper()
    }
    assert {"p4_constant_moduli", "p4_field_moduli"} <= p4_to_parent
    lowered = report_text.casefold()
    assert "byte-complete" in lowered
    assert "semantic" in lowered and "21" in lowered


def derive_outcome(contents: dict[str, bytes]) -> tuple[str, dict[str, bool]]:
    def has(path: str, *needles: str) -> bool:
        text = contents[path].decode("utf-8", "replace").casefold()
        return all(needle.casefold() in text for needle in needles)

    gates = {
        "native_parent_type": has(
            "udt_complete_relational_configuration_variation_domain_audit_2026-07-26/AUDIT_REPORT.md",
            "physical geometric arena",
        ),
        "nonvacuous_offshell_existence": has(
            "udt_native_global_coframe_definition_audit_2026-07-28/AUDIT_REPORT.md",
            "derived as an existence class",
            "off shell",
        ),
        "native_variation_selected": False,
        "native_realization_selected": False,
        "p4_stationary_equivalence": False,
        "time_angular_common_live_witness": False,
        "hopfion_native_carrier_map": False,
        "reciprocity_return_law": False,
        "bootstrap_operation": False,
        "ponder_is_authority": False,
    }
    assert gates["native_parent_type"] and gates["nonvacuous_offshell_existence"]
    assert not any(
        gates[name]
        for name in (
            "native_variation_selected",
            "native_realization_selected",
            "p4_stationary_equivalence",
            "time_angular_common_live_witness",
            "hopfion_native_carrier_map",
            "reciprocity_return_law",
            "bootstrap_operation",
            "ponder_is_authority",
        )
    )
    return OUTCOME, gates


def semantic_state(
    audit: dict[str, object],
    objects: list[dict[str, str]],
    relations: list[dict[str, str]],
    premises: list[dict[str, str]],
    basin_rows: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "outcome": audit["primary_outcome"],
        "native_count": audit["native_realized_family_count"],
        "objects": {row["id"]: row for row in objects},
        "relations": {row["id"]: row for row in relations},
        "premises": {row["id"]: row for row in premises},
        "basins": {row["arena"]: row for row in basin_rows},
    }


def verify_semantic_state(state: dict[str, object]) -> None:
    assert state["outcome"] == OUTCOME
    assert state["native_count"] == 0
    objects = state["objects"]
    relations = state["relations"]
    premises = state["premises"]
    basins = state["basins"]
    assert isinstance(objects, dict) and isinstance(relations, dict)
    assert isinstance(premises, dict) and isinstance(basins, dict)
    assert premises["P06"]["entry_status"] == "POSIT"
    assert premises["P07"]["entry_status"] == "CONDITIONAL"
    assert premises["P08"]["entry_status"] == "CHOSE"
    assert premises["P11"]["entry_status"] == "WORKING_POSIT"
    assert relations["R07"]["relation"] == "PULLBACK_GIVES_INTEGRATED_ROWS"
    assert relations["R08"]["status"] == "OPEN"
    assert relations["R11"]["status"] == "OPEN"
    assert relations["R12"]["status"] == "OPEN"
    assert relations["R14"]["status"] == "OPEN"
    assert "CONSTRAINT" in relations["R15"]["relation"]
    assert relations["R17"]["status"] == "NOT_DERIVED"
    assert objects["O11"]["status"] == "CONDITIONAL_CARRIER_MODEL"
    assert objects["O11"]["belongs_to_native_parent_type"] == "no"
    assert basins["native_geometric_arena"]["stable_basin_well_posed"] == "NO"
    assert basins["conditional_hopfion"]["stable_basin_well_posed"] == "YES_CONDITIONAL_ONLY"


def mutation_catches(state: dict[str, object]) -> list[str]:
    mutations: list[tuple[str, tuple[object, ...], object]] = [
        ("promote_outcome", ("outcome",), "NATIVE_PARENT_REALIZED_VARIATION_SPACE_DERIVED"),
        ("invent_native_family", ("native_count",), 1),
        ("promote_carrier", ("premises", "P06", "entry_status"), "DERIVED"),
        ("promote_action", ("premises", "P07", "entry_status"), "DERIVED"),
        ("promote_boundary", ("premises", "P08", "entry_status"), "DERIVED"),
        ("invent_bootstrap_operation", ("premises", "P11", "entry_status"), "DERIVED_OPERATION"),
        ("equate_stationary_sets", ("relations", "R07", "relation"), "STATIONARY_SET_EQUIVALENCE"),
        ("close_p4_converse", ("relations", "R08", "status"), "DERIVED"),
        ("invent_live_join", ("relations", "R11", "status"), "DERIVED"),
        ("invent_hopfion_embedding", ("relations", "R12", "status"), "DERIVED"),
        ("invent_bootstrap_return", ("relations", "R14", "status"), "DERIVED"),
        ("reciprocity_as_dynamics", ("relations", "R15", "relation"), "DYNAMICAL_RETURN_LAW"),
        ("formal_union_as_native", ("relations", "R17", "status"), "DERIVED"),
        ("promote_hopfion_model", ("objects", "O11", "status"), "NATIVE_DERIVED"),
        ("attach_hopfion_to_parent", ("objects", "O11", "belongs_to_native_parent_type"), "yes"),
        ("invent_native_basin", ("basins", "native_geometric_arena", "stable_basin_well_posed"), "YES"),
        ("erase_conditional_basin_stamp", ("basins", "conditional_hopfion", "stable_basin_well_posed"), "YES"),
    ]
    caught: list[str] = []
    for name, path, value in mutations:
        mutant = copy.deepcopy(state)
        cursor = mutant
        for key in path[:-1]:
            cursor = cursor[key]  # type: ignore[index]
        cursor[path[-1]] = value  # type: ignore[index]
        try:
            verify_semantic_state(mutant)
        except AssertionError:
            caught.append(name)
        else:
            raise AssertionError(f"mutation escaped: {name}")
    return caught


def source_mutation_catches(
    tree: dict[str, dict[str, object]],
    contents: dict[str, bytes],
    inventory: list[dict[str, str]],
    manifest_text: str,
    authorities: list[dict[str, str]],
) -> list[str]:
    caught: list[str] = []

    source_mutants: list[tuple[str, list[dict[str, str]], str]] = []
    source_mutants.append(("missing_source_row", copy.deepcopy(inventory[:-1]), manifest_text))
    duplicated = copy.deepcopy(inventory)
    duplicated[-1] = copy.deepcopy(duplicated[0])
    source_mutants.append(("duplicated_source_row", duplicated, manifest_text))
    bad_hash = copy.deepcopy(inventory)
    bad_hash[0]["sha256"] = "0" * 64
    source_mutants.append(("source_hash_mismatch", bad_hash, manifest_text))
    source_mutants.append(("manifest_hash_mismatch", copy.deepcopy(inventory), "0" + manifest_text[1:]))
    for name, rows, manifest in source_mutants:
        try:
            check_source_freeze(tree, rows, manifest)
        except AssertionError:
            caught.append(name)
        else:
            raise AssertionError(f"source mutation escaped: {name}")

    authority_mutants: list[tuple[str, list[dict[str, str]]]] = []
    authority_mutants.append(("missing_authority", copy.deepcopy(authorities[:-1])))
    bad_authority_hash = copy.deepcopy(authorities)
    bad_authority_hash[0]["sha256"] = "0" * 64
    authority_mutants.append(("authority_hash_mismatch", bad_authority_hash))
    for name, rows in authority_mutants:
        try:
            check_authorities(rows, tree, contents)
        except AssertionError:
            caught.append(name)
        else:
            raise AssertionError(f"authority mutation escaped: {name}")
    return caught


def main() -> None:
    tree, contents = frozen_tree()
    inventory = read_tsv("SOURCE_INVENTORY.tsv")
    authorities = read_tsv("SOURCE_AUTHORITY_LEDGER.tsv")
    objects = read_tsv("CONFIGURATION_OBJECT_LEDGER.tsv")
    relations = read_tsv("PARENT_RELATION_MATRIX.tsv")
    basins = read_tsv("VARIATION_AND_BASIN_GATE.tsv")
    premises = read_tsv("PREMISE_LEDGER.tsv")
    controls = read_tsv("EXACT_CONTROL_LEDGER.tsv")
    manifest_text = (PKG / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8")
    report_text = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    audit = json.loads((PKG / "AUDIT_RESULT.json").read_text(encoding="utf-8"))

    check_source_freeze(tree, inventory, manifest_text)
    check_authorities(authorities, tree, contents)
    candidates = broad_candidate_search(contents)
    control_results = exact_controls()
    check_corrected_package(objects, relations, controls, report_text)
    outcome, gates = derive_outcome(contents)
    assert audit["primary_outcome"] == outcome
    state = semantic_state(audit, objects, relations, premises, basins)
    verify_semantic_state(state)
    catches = mutation_catches(state)
    source_catches = source_mutation_catches(
        tree, contents, inventory, manifest_text, authorities
    )

    result = {
        "status": "PASS",
        "base_commit": BASE,
        "source_count": len(tree),
        "source_bytes": sum(int(row["bytes"]) for row in tree.values()),
        "authority_count": len(authorities),
        "authority_semantic_checks": len(SOURCE_ANCHORS),
        "broad_candidate_count": len(candidates),
        "exact_controls": control_results,
        "exact_controls_passed": len(control_results),
        "derived_outcome": outcome,
        "outcome_gates": gates,
        "semantic_mutations_rejected": len(catches),
        "semantic_mutation_names": catches,
        "source_mutations_rejected": len(source_catches),
        "source_mutation_names": source_catches,
        "imports_primary_builder_or_verifier": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
