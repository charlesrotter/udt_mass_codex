#!/usr/bin/env python3
"""Fail-closed verifier for the bounded post-July response availability audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
GATES = [
    "G1_complete_variation_domain",
    "G2_off_shell_local_response",
    "G3_tracefree_angular_response",
    "G4_same_solution_mass_volume_density",
    "G5_finite_cell_boundary_global_variation",
    "G6_native_provenance",
]
ALLOWED_GATE_VALUES = {
    "PASS", "CONDITIONAL", "ABSENT", "INCOMPATIBLE", "OUT_OF_SCOPE",
    "PROVENANCE_BLOCKED",
}
ALLOWED_DISPOSITIONS = {
    "COMPLETE_RESPONSE_SURVIVOR", "PARTIAL_NATIVE_INTERFACE",
    "CONDITIONAL_IMPORTED_OR_POSITED", "ON_SHELL_ONLY", "GEOMETRY_ONLY",
    "PROVENANCE_BLOCKED", "NO_RESPONSE_ROLE",
}
EXPECTED_IDS = [f"B{i:02d}" for i in range(1, 26)] + ["B27", "B28", "B29", "B30", "B31"]
PINNED_HASHES = {
    "udt_bootstrap_clock_angular_closure_audit_2026-07-24/EQUATION_FAMILY_GATE_MATRIX.tsv":
        "9ff6b8d1005964ee0721440779e07a78165b47a52a0bcac275b221733ce4fac1",
    "udt_global_local_relational_closure_audit_2026-07-25/SHA256SUMS.txt":
        "7571a85c60da8edb7f5160063538d0f1261acb29380428eb2e46515530cc4872",
    "udt_founded_phi_complete_coframe_extension_audit_2026-07-25/SHA256SUMS.txt":
        "b9c09d4b661303fd091ecc6995ad62da3b81799f2e7771b43fb172725efc63d7",
    "udt_macro_phi_angular_xmax_extension_atlas_2026-07-25/SHA256SUMS.txt":
        "c4cd2aee0db110d2f15aa56a1c14fa5a589cb2dc555b3003d8d179fc625c8342",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_source_closure(rows: list[dict[str, str]], closure: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    if len(closure) != len(rows):
        return [f"source-closure cardinality mismatch: {len(closure)}"]
    by_id = {row.get("candidate_id", ""): row for row in closure}
    if len(by_id) != len(closure):
        errors.append("duplicate source-closure identity")
    for row in rows:
        cid = row["candidate_id"]
        item = by_id.get(cid)
        if item is None:
            errors.append(f"missing source-closure row: {cid}")
            continue
        citation = row["load_bearing_evidence"]
        source_path = citation.split(":", 1)[0]
        source = ROOT / source_path
        if item.get("citation") != citation or item.get("source_path") != source_path:
            errors.append(f"source-closure citation mismatch: {cid}")
            continue
        if item.get("sha256") != sha256(source):
            errors.append(f"source-closure SHA-256 mismatch: {cid}")
        blob = subprocess.run(
            ["git", "rev-parse", f"HEAD:{source_path}"], cwd=ROOT,
            check=True, text=True, capture_output=True,
        ).stdout.strip()
        if item.get("git_blob") != blob or item.get("tracked") != "YES":
            errors.append(f"source-closure Git identity mismatch: {cid}")
    return errors


def validate(rows: list[dict[str, str]], prereg: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    ids = [row.get("candidate_id", "") for row in rows]
    prereg_primary = [row["candidate_id"] for row in prereg if row["eligibility"] == "PRIMARY"]
    if ids != EXPECTED_IDS:
        errors.append(f"candidate order/set mismatch: {ids}")
    if prereg_primary != EXPECTED_IDS:
        errors.append("preregistered universe does not equal the pinned 30-family identity list")
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate identity")
    if "B26" in ids:
        errors.append("legacy B26 negative control entered the affirmative universe")
    prereg_by_id = {row["candidate_id"]: row for row in prereg}
    for row in rows:
        cid = row.get("candidate_id", "")
        if cid not in prereg_by_id:
            errors.append(f"unregistered/generated candidate: {cid}")
            continue
        if row.get("family_label") != prereg_by_id[cid]["family_label"]:
            errors.append(f"family label mismatch: {cid}")
        invalid = {row.get(gate, "") for gate in GATES} - ALLOWED_GATE_VALUES
        if invalid:
            errors.append(f"invalid gate value for {cid}: {sorted(invalid)}")
        disposition = row.get("disposition", "")
        if disposition not in ALLOWED_DISPOSITIONS:
            errors.append(f"invalid disposition for {cid}: {disposition}")
        all_pass = all(row.get(gate) == "PASS" for gate in GATES)
        if (disposition == "COMPLETE_RESPONSE_SURVIVOR") != all_pass:
            errors.append(f"survivor equivalence violation: {cid}")
        if disposition in {"ON_SHELL_ONLY", "GEOMETRY_ONLY", "NO_RESPONSE_ROLE"} and row.get("G2_off_shell_local_response") == "PASS":
            errors.append(f"non-response family promoted to off-shell response: {cid}")
        if row.get("G3_tracefree_angular_response") == "PASS" and row.get("G2_off_shell_local_response") != "PASS":
            errors.append(f"angular response credited without an off-shell response: {cid}")
        if row.get("G2_off_shell_local_response") == "ABSENT" and row.get("G6_native_provenance") != "OUT_OF_SCOPE":
            errors.append(f"vacuous response-provenance ruling: {cid}")
        if row.get("G2_off_shell_local_response") == "ABSENT" and row.get("G5_finite_cell_boundary_global_variation") != "ABSENT":
            errors.append(f"boundary geometry credited as response variation: {cid}")
        if row.get("G4_same_solution_mass_volume_density") == "PASS":
            errors.append(f"unregistered native same-solution mass promotion: {cid}")
        if row.get("G5_finite_cell_boundary_global_variation") == "PASS":
            errors.append(f"unregistered complete finite-cell variation promotion: {cid}")
        if disposition == "CONDITIONAL_IMPORTED_OR_POSITED" and row.get("G6_native_provenance") != "CONDITIONAL":
            errors.append(f"conditional/imported family has invalid provenance grade: {cid}")
        citation = row.get("load_bearing_evidence", "")
        match = re.fullmatch(r"([^:]+):(\d+)(?:-(\d+))?(?:;(\d+)-(\d+))?", citation)
        if not match:
            errors.append(f"malformed citation: {cid}: {citation}")
        else:
            source = ROOT / match.group(1)
            if not source.is_file():
                errors.append(f"missing cited source: {cid}: {source.relative_to(ROOT)}")
            else:
                line_count = sum(1 for _ in source.open(encoding="utf-8"))
                cited_lines = [int(value) for value in match.groups()[1:] if value]
                if any(line < 1 or line > line_count for line in cited_lines):
                    errors.append(f"citation outside source: {cid}: {citation} has {line_count} lines")
        if not row.get("ruling", "").strip():
            errors.append(f"empty ruling: {cid}")
    for relpath, expected in PINNED_HASHES.items():
        path = ROOT / relpath
        if not path.is_file():
            errors.append(f"missing pinned source: {relpath}")
        elif sha256(path) != expected:
            errors.append(f"pinned source hash mismatch: {relpath}")
    negative = read_tsv(PKG / "PREREGISTERED_NEGATIVE_CONTROL.tsv")
    if (len(negative) != 1 or negative[0].get("registry_row") != "B26"
            or negative[0].get("allowed_role") != "NEGATIVE_OR_COUNTEREXAMPLE_ONLY"):
        errors.append("B26 negative-control registration invalid")
    return errors


def expect_failure(name: str, rows: list[dict[str, str]], prereg: list[dict[str, str]], mutate) -> dict[str, object]:
    changed = deepcopy(rows)
    mutate(changed)
    errors = validate(changed, prereg)
    return {"name": name, "rejected": bool(errors), "first_error": errors[0] if errors else ""}


def run_catch_proofs(rows: list[dict[str, str]], prereg: list[dict[str, str]]) -> list[dict[str, object]]:
    def row(cid: str, data: list[dict[str, str]]) -> dict[str, str]:
        return next(item for item in data if item["candidate_id"] == cid)

    proofs = []
    proofs.append(expect_failure("missing_candidate", rows, prereg, lambda d: d.pop()))
    proofs.append(expect_failure("duplicate_candidate", rows, prereg, lambda d: d.append(deepcopy(d[0]))))
    proofs.append(expect_failure("legacy_control_promoted", rows, prereg, lambda d: d.__setitem__(0, {**d[0], "candidate_id": "B26"})))
    proofs.append(expect_failure("partial_family_called_survivor", rows, prereg, lambda d: row("B19", d).__setitem__("disposition", "COMPLETE_RESPONSE_SURVIVOR")))
    proofs.append(expect_failure("on_shell_called_off_shell", rows, prereg, lambda d: row("B23", d).__setitem__("G2_off_shell_local_response", "PASS")))
    proofs.append(expect_failure("volume_called_angular_response", rows, prereg, lambda d: row("B23", d).__setitem__("G3_tracefree_angular_response", "PASS")))
    proofs.append(expect_failure("external_mass_called_native", rows, prereg, lambda d: row("B22", d).__setitem__("G4_same_solution_mass_volume_density", "PASS")))
    proofs.append(expect_failure("gluing_called_boundary_variation", rows, prereg, lambda d: row("B16", d).__setitem__("G5_finite_cell_boundary_global_variation", "CONDITIONAL")))
    proofs.append(expect_failure("imported_route_called_native", rows, prereg, lambda d: row("B20", d).__setitem__("G6_native_provenance", "PASS")))
    proofs.append(expect_failure("vacuous_native_provenance_pass", rows, prereg, lambda d: row("B25", d).__setitem__("G6_native_provenance", "PASS")))
    proofs.append(expect_failure("generated_candidate", rows, prereg, lambda d: d.__setitem__(0, {**d[0], "candidate_id": "B32"})))
    proofs.append(expect_failure("missing_source_citation", rows, prereg, lambda d: row("B01", d).__setitem__("load_bearing_evidence", "missing.md:1-2")))
    return proofs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = read_tsv(PKG / "CANDIDATE_RESPONSE_GATE_MATRIX.tsv")
    prereg = read_tsv(PKG / "PREREGISTERED_CANDIDATE_UNIVERSE.tsv")
    closure = read_tsv(PKG / "FAMILY_SOURCE_CLOSURE.tsv")
    errors = validate(rows, prereg)
    errors.extend(validate_source_closure(rows, closure))
    proofs = run_catch_proofs(rows, prereg)
    bad_closure = deepcopy(closure)
    bad_closure[0]["sha256"] = "0" * 64
    closure_errors = validate_source_closure(rows, bad_closure)
    proofs.append({
        "name": "source_closure_hash_corruption",
        "rejected": bool(closure_errors),
        "first_error": closure_errors[0] if closure_errors else "",
    })
    if any(not proof["rejected"] for proof in proofs):
        errors.append("one or more catch-proofs did not fail closed")
    dispositions = Counter(row["disposition"] for row in rows)
    gate_counts = {gate: dict(sorted(Counter(row[gate] for row in rows).items())) for gate in GATES}
    survivors = [row["candidate_id"] for row in rows if row["disposition"] == "COMPLETE_RESPONSE_SURVIVOR"]
    result = {
        "status": "PASS" if not errors else "FAIL",
        "maximum_conclusion": "NO_COMPLETE_RESPONSE_IN_FROZEN_30_FAMILY_UNIVERSE" if not survivors else "COMPLETE_RESPONSE_SURVIVORS_PRESENT",
        "candidate_count": len(rows),
        "candidate_identity_sha256": hashlib.sha256(("\n".join(row["candidate_id"] for row in rows) + "\n").encode()).hexdigest(),
        "survivors": survivors,
        "disposition_counts": dict(sorted(dispositions.items())),
        "gate_counts": gate_counts,
        "pinned_hashes": {path: sha256(ROOT / path) for path in PINNED_HASHES},
        "catch_proofs": proofs,
        "errors": errors,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
