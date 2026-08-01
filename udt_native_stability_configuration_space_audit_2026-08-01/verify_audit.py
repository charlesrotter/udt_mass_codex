#!/usr/bin/env python3
"""Independent fail-closed verifier for the native configuration-space audit."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
import tarfile
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
BASE = "095a2a5e093f21bfd68939f5874b359868a109d3"
OUTCOME = "NATIVE_OFFSHELL_PARENT_ARENA_DERIVED__REALIZATION_VARIATION_OPEN"


def run_git(*args: str, binary: bool = False):
    proc = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return proc.stdout if binary else proc.stdout.decode()


def table(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def base_tree_independent() -> list[dict[str, str]]:
    listing = run_git("ls-tree", "-r", "-z", "--long", BASE, binary=True)
    meta: dict[str, tuple[str, int]] = {}
    for token in listing.split(b"\0"):
        if not token:
            continue
        left, right = token.split(b"\t", 1)
        _mode, kind, blob, size = left.decode().split()
        if kind != "blob":
            raise AssertionError("tracked non-blob encountered")
        meta[right.decode()] = (blob, int(size))

    tar_bytes = run_git("archive", BASE, binary=True)
    payload: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            fd = archive.extractfile(member)
            if fd:
                payload[member.name] = fd.read()

    result = []
    for path in sorted(meta):
        blob, size = meta[path]
        data = payload.get(path)
        if data is None:
            data = run_git("cat-file", "blob", blob, binary=True)
        if len(data) != size:
            raise AssertionError(f"base byte count mismatch: {path}")
        result.append({"path": path, "git_blob": blob, "bytes": str(size), "sha256": hashlib.sha256(data).hexdigest()})
    return result


def indexed(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    values = [row[field] for row in rows]
    if len(values) != len(set(values)):
        raise AssertionError(f"duplicate {field}")
    return {row[field]: row for row in rows}


def validate_semantics(data: dict[str, object]) -> None:
    result = data["result"]
    assert isinstance(result, dict)
    if result.get("primary_outcome") != OUTCOME:
        raise AssertionError("wrong or promoted primary outcome")
    if result.get("native_realized_family_count") != 0:
        raise AssertionError("native realized family promotion")
    if result.get("conditional_stability_scope_count") != 1 or "conditional_stable_basin_count" in result:
        raise AssertionError("conditional stability scope mislabeled as a basin count")

    premises = indexed(data["premises"], "id")  # type: ignore[arg-type]
    expected_premises = {
        "P03": ("OPEN", "NOT_PROMOTED"),
        "P04": ("OPEN", "NOT_PROMOTED"),
        "P05": ("CONDITIONAL", "NOT_SELECTED"),
        "P06": ("POSIT", "NOT_PROMOTED"),
        "P07": ("CONDITIONAL", "NOT_PROMOTED"),
        "P08": ("CHOSE", "NOT_PROMOTED"),
        "P10": ("DERIVED_NATURALITY_IN_SCOPE", "NOT_USED_AS_DYNAMICS"),
        "P11": ("WORKING_POSIT", "NO_OPERATION_INVENTED"),
        "P12": ("OPEN", "NOT_PROMOTED"),
        "P13": ("WORKING_LEAD", "INTERPRETATION_ONLY"),
    }
    for pid, pair in expected_premises.items():
        row = premises.get(pid)
        if not row or (row["entry_status"], row["audit_treatment"]) != pair:
            raise AssertionError(f"premise promotion or loss: {pid}")

    rel = indexed(data["relations"], "id")  # type: ignore[arg-type]
    exact_relations = {
        "R06": ("CONSTANT_SECTION_EMBEDDING", "EXACT_CONDITIONAL"),
        "R07": ("PULLBACK_GIVES_INTEGRATED_ROWS", "EXACT_CONDITIONAL"),
        "R08": ("NO_EQUIVALENCE_DERIVED", "OPEN"),
        "R11": ("COMMON_REALIZED_INTERSECTION", "OPEN"),
        "R12": ("CARRIER_EMBEDDING", "OPEN"),
        "R14": ("RETURN_MAP", "OPEN"),
        "R15": ("NATURALITY_CONSTRAINT", "DERIVED_IN_SCOPE"),
        "R16": ("NATIVE_PARTITION", "NOT_DERIVED"),
        "R17": ("NATIVE_PARENT_SELECTION", "NOT_DERIVED"),
        "R19": ("CONDITIONAL_SUBDOMAIN", "CONDITIONAL"),
        "R20": ("CONDITIONAL_SUBDOMAIN", "CONDITIONAL"),
    }
    for rid, pair in exact_relations.items():
        row = rel.get(rid)
        if not row or (row["relation"], row["status"]) != pair:
            raise AssertionError(f"relation promotion or loss: {rid}")

    objects = indexed(data["objects"], "id")  # type: ignore[arg-type]
    if objects["O02"]["status"] != "NATIVE_OFFSHELL_ARENA_DERIVED_AS_TYPE":
        raise AssertionError("native off-shell arena lost or promoted")
    if objects["O11"]["status"] != "CONDITIONAL_CARRIER_MODEL":
        raise AssertionError("Hopfion carrier promotion")
    if objects["O14"]["status"] != "BOOKKEEPING_CONTROL_ONLY":
        raise AssertionError("formal union promoted")
    for oid in ("O07", "O08"):
        if objects[oid]["belongs_to_native_parent_type"] != "conditional_only":
            raise AssertionError(f"P4 parent relation lost or promoted: {oid}")

    gates = indexed(data["gates"], "arena")  # type: ignore[arg-type]
    required = {
        "native_geometric_arena": "NO",
        "conditional_hopfion": "YES_CONDITIONAL_ONLY",
        "bootstrap_global_local": "NO",
        "F01_F07_catalogue": "NO_GLOBAL_BASIN",
    }
    for arena, basin in required.items():
        if arena not in gates or gates[arena]["stable_basin_well_posed"] != basin:
            raise AssertionError(f"basin gate promoted or missing: {arena}")
    if gates["native_geometric_arena"]["bootstrap_return"] != "OPEN":
        raise AssertionError("bootstrap return invented")


def exact_controls() -> list[tuple[str, bool, str]]:
    # C01: alpha1=dx-dy has coefficient vector (1,-1). The derivative of
    # i(a)=(a,a) is (1,1), so its pullback coefficient is 1-1=0 even
    # though the ambient covector is nonzero.
    alpha1_coefficients = (1, -1)
    di_da = (1, 1)
    pullback_coefficient = sum(a * b for a, b in zip(alpha1_coefficients, di_da))
    ambient_nonzero = any(alpha1_coefficients)
    c01 = pullback_coefficient == 0 and ambient_nonzero

    # C02: tagged union exists without any relation between the sets.
    a = {0}
    b = {0}
    tagged = {("A", x) for x in a} | {("B", x) for x in b}
    c02 = len(tagged) == 2 and a == b

    # C03: the same sampled set has one versus two strict minima.
    xs = [-2, -1, 0, 1, 2]
    v1 = [x * x for x in xs]
    v2 = [(x * x - 1) ** 2 for x in xs]
    minima1 = [xs[i] for i in range(1, 4) if v1[i] < v1[i - 1] and v1[i] < v1[i + 1]]
    minima2 = [xs[i] for i in range(1, 4) if v2[i] < v2[i - 1] and v2[i] < v2[i + 1]]
    c03 = minima1 == [0] and minima2 == [-1, 1]

    # C04: nonempty modules have only a zero intersection.
    m1, m2 = {0, 1}, {0, 2}
    c04 = bool(m1) and bool(m2) and m1.intersection(m2) == {0}

    # C05: labels and fibers do not construct a transition map.
    labels = {0, 1}
    fibers = {0: {"a"}, 1: {"b"}}
    transitions: dict[tuple[int, int], object] = {}
    c05 = set(fibers) == labels and (0, 1) not in transitions
    return [
        ("C01", c01, "one-way pullback implication and failed converse"),
        ("C02", c02, "formal tagged union is selector-free"),
        ("C03", c03, "same set admits different stable-minimum counts"),
        ("C04", c04, "nonempty modules lack nonzero common witness"),
        ("C05", c05, "fiber labels do not generate gluing"),
    ]


def mutation_catches(base: dict[str, object]) -> list[list[str]]:
    cases = []

    def expect(name: str, mutate) -> None:
        trial = deepcopy(base)
        mutate(trial)
        caught = False
        try:
            validate_semantics(trial)
        except (AssertionError, KeyError):
            caught = True
        cases.append([name, "PASS" if caught else "FAIL"])

    expect("promoted_primary_outcome", lambda d: d["result"].update(primary_outcome="NATIVE_PARENT_REALIZED_VARIATION_SPACE_DERIVED"))
    expect("invented_native_realized_family", lambda d: d["result"].update(native_realized_family_count=1))
    expect("carrier_posit_promoted", lambda d: d["premises"][5].update(entry_status="DERIVED"))
    expect("conditional_action_promoted", lambda d: d["premises"][6].update(entry_status="DERIVED"))
    expect("chosen_boundary_promoted", lambda d: d["premises"][7].update(entry_status="DERIVED"))
    expect("bootstrap_operation_invented", lambda d: d["premises"][10].update(audit_treatment="DERIVED_RETURN"))
    expect("reciprocity_used_as_dynamics", lambda d: d["premises"][9].update(audit_treatment="FLOW"))
    expect("working_lead_promoted", lambda d: d["premises"][12].update(entry_status="DERIVED"))
    expect("pullback_made_stationary_equivalence", lambda d: d["relations"][7].update(relation="EQUAL_STATIONARY_SETS", status="DERIVED"))
    expect("live_modules_declared_realized", lambda d: d["relations"][10].update(status="DERIVED_NONZERO"))
    expect("Hopfion_embedding_invented", lambda d: d["relations"][11].update(status="DERIVED"))
    expect("bootstrap_return_invented", lambda d: d["relations"][13].update(status="DERIVED"))
    expect("formal_union_promoted", lambda d: d["objects"][13].update(status="NATIVE_PARENT"))
    expect("Hopfion_model_promoted", lambda d: d["objects"][10].update(status="NATIVE_DERIVED"))
    expect("native_basin_declared", lambda d: d["gates"][0].update(stable_basin_well_posed="YES"))
    expect("conditional_stamp_removed", lambda d: d["gates"][5].update(stable_basin_well_posed="YES_NATIVE"))
    expect("missing_native_gate", lambda d: d["gates"].pop(0))
    expect("catalogue_made_solution_partition", lambda d: d["relations"][15].update(status="DERIVED"))
    expect("P4_parent_relation_erased", lambda d: d["objects"][6].update(belongs_to_native_parent_type="no"))
    expect("P4_conditional_subdomain_promoted", lambda d: d["objects"][7].update(belongs_to_native_parent_type="yes_native"))
    expect("P4_parent_relation_promoted", lambda d: d["relations"][18].update(status="DERIVED_NATIVE"))
    return cases


def main() -> None:
    expected_sources = base_tree_independent()
    actual_sources = table("SOURCE_INVENTORY.tsv")
    if actual_sources != expected_sources:
        raise AssertionError("SOURCE_INVENTORY does not exactly reproduce frozen base tree")
    manifest_lines = (PKG / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    expected_manifest = [f"{r['sha256']}  {r['path']}" for r in expected_sources]
    if manifest_lines != expected_manifest:
        raise AssertionError("source manifest mismatch")

    authorities = table("SOURCE_AUTHORITY_LEDGER.tsv")
    source_by_path = indexed(actual_sources, "path")
    if len(authorities) != 21:
        raise AssertionError("authority census mismatch")
    indexed(authorities, "id")
    for row in authorities:
        source = source_by_path.get(row["path"])
        if not source or row["git_blob"] != source["git_blob"] or row["sha256"] != source["sha256"]:
            raise AssertionError(f"authority source identity mismatch: {row['path']}")

    data: dict[str, object] = {
        "result": json.loads((PKG / "AUDIT_RESULT.json").read_text()),
        "premises": table("PREMISE_LEDGER.tsv"),
        "relations": table("PARENT_RELATION_MATRIX.tsv"),
        "objects": table("CONFIGURATION_OBJECT_LEDGER.tsv"),
        "gates": table("VARIATION_AND_BASIN_GATE.tsv"),
    }
    counts = {"premises": 13, "relations": 20, "objects": 14, "gates": 8}
    for key, count in counts.items():
        if len(data[key]) != count:  # type: ignore[arg-type]
            raise AssertionError(f"{key} census mismatch")
    validate_semantics(data)

    controls = exact_controls()
    ledger_controls = indexed(table("EXACT_CONTROL_LEDGER.tsv"), "id")
    if len(ledger_controls) != 5 or not all(ok for _, ok, _ in controls):
        raise AssertionError("exact control failure")
    for cid, _ok, _detail in controls:
        if ledger_controls[cid]["status"] != "PASS":
            raise AssertionError(f"control ledger failure: {cid}")

    catches = mutation_catches(data)
    if not all(row[1] == "PASS" for row in catches):
        raise AssertionError("one or more semantic mutation catches failed")
    with (PKG / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["mutation", "caught"])
        writer.writerows(catches)

    report = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    derivation = (PKG / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    for required in (OUTCOME, "native typed off-shell geometric parent arena", "zero native realized families"):
        if required not in report:
            raise AssertionError(f"report token missing: {required}")
    for required in ("alpha0 = i* alpha1", "The converse is false", "WORKING POSIT"):
        if required not in derivation:
            raise AssertionError(f"derivation token missing: {required}")

    result = {
        "status": "PASS",
        "base_commit": BASE,
        "source_count": len(expected_sources),
        "authority_count": len(authorities),
        "semantic_catches_passed": len(catches),
        "semantic_catches_total": len(catches),
        "exact_controls_passed": len(controls),
        "exact_controls_total": len(controls),
        "primary_outcome": OUTCOME,
        "native_realized_family_count": 0,
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
