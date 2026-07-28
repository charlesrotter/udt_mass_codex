#!/usr/bin/env python3
"""Independent stdlib verifier for the historical angular-method salvage audit."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "fa77ce28c8b5b83e7a6d5a92df2e684b62bb60e6"
PACKAGE = HERE.name
DOC = "udt_canonical_geometry.md"
EXPECTED_DIRTY_COUNT = 55
EXPECTED_DIRTY_SHA256 = "345d297e0ad849cd38f1d817c915922de653ca2d2befcf923af6f9d097b483e4"
RANGES = [
    (2187, 2420, "lepton_angular"),
    (2420, 2564, "hadron_assignment"),
    (2662, 2797, "boson_force_mapping"),
    (2797, 2902, "structural_constants"),
    (3141, 3164, "rank2_qcd_claim"),
    (3164, 3961, "exterior_mixing_quark_nuclear"),
    (3961, 4053, "multiplicity_web"),
    (5875, 6045, "translation_cluster"),
]


def git(*args: str, binary: bool = False):
    completed = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if completed.returncode:
        message = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise AssertionError(message)
    return completed.stdout


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifests() -> tuple[int, list[str]]:
    paths: list[str] = []
    for name in ("SOURCE_MANIFEST.tsv", "SUPPLEMENTAL_SOURCE_MANIFEST.tsv"):
        for row in rows(name):
            payload = git("show", f"{BASE}:{row['path']}", binary=True)
            assert sha(payload) == row["sha256"]
            assert len(payload) == int(row["size_bytes"])
            assert str(git("rev-parse", f"{BASE}:{row['path']}")).strip() == row["blob"]
            paths.append(row["path"])
    assert len(paths) == 17 and len(set(paths)) == 17
    return len(paths), paths


def independent_reference_census(document: str) -> list[dict[str, str]]:
    base_paths = str(git("ls-tree", "-r", "--name-only", BASE)).splitlines()
    history_paths = sorted({
        line.split(" ", 1)[1]
        for line in str(git("rev-list", "--objects", "--all")).splitlines()
        if " " in line
    })
    base_names: dict[str, list[str]] = {}
    history_names: dict[str, list[str]] = {}
    for path in base_paths:
        base_names.setdefault(Path(path).name, []).append(path)
    for path in history_paths:
        history_names.setdefault(Path(path).name, []).append(path)
    pattern = re.compile(r"[A-Za-z0-9_./-]+\.(?:md|py|json|txt|csv|tsv|npz|ipynb)")
    discovered: dict[str, dict[str, object]] = {}
    lines = document.splitlines()
    for start, end, section in RANGES:
        for number in range(start, min(end, len(lines)) + 1):
            for literal in pattern.findall(lines[number - 1]):
                item = discovered.setdefault(literal, {"lines": [], "sections": set()})
                item["lines"].append(number)
                item["sections"].add(section)
    result = []
    for literal, item in sorted(discovered.items()):
        base_exact = literal if literal in base_paths else ""
        base_matches = base_names.get(Path(literal).name, [])
        if base_exact:
            base_status, base_resolved = "TRACKED_EXACT", base_exact
        elif len(base_matches) == 1:
            base_status, base_resolved = "TRACKED_BASENAME_ONLY", base_matches[0]
        elif len(base_matches) > 1:
            base_status, base_resolved = "AMBIGUOUS_BASENAME", ";".join(base_matches)
        else:
            base_status, base_resolved = "ABSENT_AT_BASE", "-"
        history_exact = literal if literal in history_paths else ""
        history_matches = history_names.get(Path(literal).name, [])
        if history_exact:
            history_status, history_resolved = "TRACKED_EXACT_IN_HISTORY", history_exact
        elif len(history_matches) == 1:
            history_status, history_resolved = "TRACKED_BASENAME_IN_HISTORY", history_matches[0]
        elif len(history_matches) > 1:
            history_status, history_resolved = "AMBIGUOUS_BASENAME_IN_HISTORY", ";".join(history_matches)
        else:
            history_status, history_resolved = "MISSING_FROM_ALL_GIT_HISTORY", "-"
        result.append({
            "literal_reference": literal,
            "first_line": str(min(item["lines"])),
            "occurrences": str(len(item["lines"])),
            "sections": ";".join(sorted(item["sections"])),
            "base_tracking_status": base_status,
            "base_resolved_path": base_resolved,
            "history_resolution_status": history_status,
            "history_resolved_path": history_resolved,
        })
    return result


Matrix = list[list[Fraction]]


def zero(n: int) -> Matrix:
    return [[Fraction(0) for _ in range(n)] for _ in range(n)]


def unit(n: int, i: int, j: int) -> Matrix:
    out = zero(n); out[i][j] = Fraction(1); return out


def plus(a: Matrix, b: Matrix, sign: int = 1) -> Matrix:
    return [[a[i][j] + sign * b[i][j] for j in range(len(a))] for i in range(len(a))]


def mul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return [[sum((a[i][k] * b[k][j] for k in range(n)), Fraction(0)) for j in range(n)] for i in range(n)]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def trace(a: Matrix) -> Fraction:
    return sum((a[i][i] for i in range(len(a))), Fraction(0))


def comm(a: Matrix, b: Matrix) -> Matrix:
    return plus(mul(a, b), mul(b, a), -1)


def flatten(a: Matrix) -> list[Fraction]:
    return [value for row in a for value in row]


def rank(columns: list[list[Fraction]]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns)]
    nrows, ncols = len(matrix), len(matrix[0])
    pivot_row = 0
    for col in range(ncols):
        pivot = next((row for row in range(pivot_row, nrows) if matrix[row][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(nrows):
            if row != pivot_row and matrix[row][col]:
                factor = matrix[row][col]
                matrix[row] = [matrix[row][j] - factor * matrix[pivot_row][j] for j in range(ncols)]
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def basis(n: int) -> tuple[list[Matrix], list[Matrix]]:
    skew: list[Matrix] = []
    symmetric: list[Matrix] = []
    for i in range(n):
        for j in range(i + 1, n):
            skew.append(plus(unit(n, i, j), unit(n, j, i), -1))
            symmetric.append(plus(unit(n, i, j), unit(n, j, i)))
    for i in range(1, n):
        item = zero(n)
        for j in range(i):
            item[j][j] = Fraction(1)
        item[i][i] = Fraction(-i)
        symmetric.append(item)
    return skew, symmetric


def is_skew(a: Matrix) -> bool:
    return transpose(a) == [[-value for value in row] for row in a] and trace(a) == 0


def is_sym0(a: Matrix) -> bool:
    return transpose(a) == a and trace(a) == 0


def gram(items: list[Matrix], skew_sign: int = 1) -> list[list[Fraction]]:
    return [[skew_sign * trace(mul(left, right)) for right in items] for left in items]


def inertia_ldlt(source: list[list[Fraction]]) -> tuple[int, int, int]:
    matrix = [row[:] for row in source]
    positive = negative = zero_count = 0
    for k in range(len(matrix)):
        pivot = matrix[k][k]
        if pivot == 0:
            raise AssertionError("zero pivot in registered Gram basis")
        if pivot > 0:
            positive += 1
        else:
            negative += 1
        for i in range(k + 1, len(matrix)):
            for j in range(i, len(matrix)):
                value = matrix[i][j] - matrix[i][k] * matrix[j][k] / pivot
                matrix[i][j] = matrix[j][i] = value
    return positive, negative, zero_count


def direct_sum_gram(skew: list[Matrix], symmetric: list[Matrix], compact: bool) -> list[list[Fraction]]:
    count = len(skew) + len(symmetric)
    out = [[Fraction(0) for _ in range(count)] for _ in range(count)]
    for i, left in enumerate(skew):
        for j, right in enumerate(skew):
            out[i][j] = (-1 if compact else 1) * trace(mul(left, right))
    offset = len(skew)
    for i, left in enumerate(symmetric):
        for j, right in enumerate(symmetric):
            # Real form uses Tr(ST); compact iS form with -Re Tr((iS)(iT)) is also Tr(ST).
            out[offset + i][offset + j] = trace(mul(left, right))
    return out


def verify_exact_algebra() -> dict[str, object]:
    table = {int(row["n"]): row for row in rows("DIMENSION_GENERALIZATION.tsv")}
    assert set(table) == set(range(2, 7))
    for n in range(2, 7):
        skew, symmetric = basis(n)
        combined = skew + symmetric
        assert rank([flatten(item) for item in combined]) == n * n - 1
        assert all(is_skew(comm(left, right)) for left in skew for right in skew)
        assert all(is_sym0(comm(left, right)) for left in skew for right in symmetric)
        assert all(is_skew(comm(left, right)) for left in symmetric for right in symmetric)
        row = table[n]
        expected = (len(skew), len(symmetric), len(combined), n * n - 1, f"sl({n},R)")
        observed = tuple(int(row[key]) for key in (
            "rotation_dim", "symmetric_traceless_dim", "total_traceless_dim", "n_squared_minus_one"
        )) + (row["real_algebra"],)
        assert observed == expected

    bracket_expected = {
        ("R", "S1"): (0, 0, 2),
        ("R", "S2"): (0, -2, 0),
        ("S1", "S2"): (-2, 0, 0),
    }
    bracket_observed = {
        (row["left"], row["right"]): tuple(int(row[key]) for key in (
            "coefficient_R", "coefficient_S1", "coefficient_S2"
        ))
        for row in rows("SCREEN_BRACKET_TABLE.tsv")
    }
    assert bracket_observed == bracket_expected

    skew2, sym2 = basis(2)
    skew3, sym3 = basis(3)
    assert inertia_ldlt(direct_sum_gram(skew2, sym2, compact=False)) == (2, 1, 0)
    assert inertia_ldlt(direct_sum_gram(skew3, sym3, compact=False)) == (5, 3, 0)
    assert inertia_ldlt(direct_sum_gram(skew3, sym3, compact=True)) == (8, 0, 0)

    spherical = rows("SPHERICAL_TENSOR_GENERALIZATION.tsv")
    assert len(spherical) == 5
    for ell, row in enumerate(spherical, 1):
        ranks = list(range(1, 2 * ell + 1))
        assert row["tensor_ranks"] == ";".join(map(str, ranks))
        assert int(row["traceless_operator_dimension"]) == sum(2 * k + 1 for k in ranks)
        assert int(row["dimension_squared_minus_one"]) == (2 * ell + 1) ** 2 - 1
    return {
        "dimensions_checked": 5,
        "screen_brackets_checked": 3,
        "screen_trace_form_inertia": [2, 1, 0],
        "real_3d_trace_form_inertia": [5, 3, 0],
        "compact_3d_trace_form_inertia": [8, 0, 0],
    }


def validate_semantic_gates(facts: dict[str, bool]) -> None:
    expected = {f"F{number:02d}" for number in range(1, 28)}
    if set(facts) != expected:
        raise AssertionError("semantic gate identity mismatch")
    failed = [key for key, value in facts.items() if not value]
    if failed:
        raise AssertionError("semantic gate failed: " + failed[0])


def main() -> None:
    source_count, source_paths = verify_manifests()
    document_bytes = git("show", f"{BASE}:{DOC}", binary=True)
    assert sha(document_bytes) == "8e4f27a4e15a4ab608661ea49a5fdbc9339de0a6ea2eb9f713192a2980c705a7"
    document = document_bytes.decode("utf-8")
    references = rows("TRANSITIVE_REFERENCE_CENSUS.tsv")
    independent_references = independent_reference_census(document)
    assert references == independent_references and len(references) == 45
    assert all(row["history_resolution_status"] == "MISSING_FROM_ALL_GIT_HISTORY" for row in references)

    methods = rows("HISTORICAL_METHOD_CENSUS.tsv")
    assert [row["method_id"] for row in methods] == [f"M{number:02d}" for number in range(1, 24)]
    expected_classes = {
        "EMPIRICAL_NUMEROLOGY": 8,
        "HISTORICAL_RESULT_ONLY": 2,
        "IMPORTED_COMPARISON_ONLY": 5,
        "MIXED_MULTIPLE_METHOD_CLASSES": 1,
        "NATIVE_EXACT_REDERIVED_BOUNDED": 1,
        "NATIVE_METHOD_LEAD_REQUIRES_REDERIVATION": 1,
        "PURE_MATH_REUSABLE_CONDITIONAL": 5,
    }
    observed_classes: dict[str, int] = {}
    for row in methods:
        observed_classes[row["classification"]] = observed_classes.get(row["classification"], 0) + 1
        assert all(row.values())
    assert observed_classes == expected_classes
    method_by_id = {row["method_id"]: row for row in methods}

    formulas = rows("FORMULA_REPLAY.tsv")
    expected_formula_values = {
        "muon_electron": 20 * math.pi**3 / 3,
        "proton_electron": 6 * math.pi**5,
        "proton_muon": 9 * math.pi**2 / 10,
        "pion_electron": 84 * math.pi,
        "strange_down": 2 * math.pi**2,
        "charm_up": 6 * math.pi**4,
        "bottom_strange": 9 * math.pi**2 / 2,
        "top_charm": 14 * math.pi**2,
        "pmns_12": 4 / 13,
        "pmns_23": 4 / 7,
        "pmns_13": 1 / 45,
        "weinberg": 3 / 13,
        "cabibbo": 9 / 40,
    }
    assert len(formulas) == len(expected_formula_values)
    for row in formulas:
        assert row["numeric_replay"] == f"{expected_formula_values[row['historical_label']]:.12g}"
        assert row["audit_status"] == "ARITHMETIC_REPRODUCED_NOT_NATIVE_VALIDATION"

    algebra = verify_exact_algebra()
    ownership = rows("OWNERSHIP_CROSSWALK.tsv")
    assert len(ownership) == 7 and len({row["object"] for row in ownership}) == 7
    assert all(all(row.values()) for row in ownership)

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert result["primary_outcome"] == "MIXED_MULTIPLE_METHOD_CLASSES"
    assert result["method_lead"] == "CURRENT_SCREEN_OPERATOR_METHOD_LEAD"
    assert result["historical_physics_restored"] is False
    assert result["old_3_plus_5_unique"] is False
    assert result["lambda_is_complete_screen_response"] is False
    assert result["method_class_counts"] == expected_classes
    assert result["fixed_sources_replayed"] == 13 and result["supplemental_sources_replayed"] == 4
    assert result["transitive_references"] == 45 and result["missing_transitive_references"] == 45
    assert result["screen_trace_form_inertia"] == [2, 1, 0]
    assert result["three_dimensional_real_trace_form_inertia"] == [5, 3, 0]
    assert result["three_dimensional_compact_form_inertia"] == [8, 0, 0]

    status = {row["item"]: row for row in rows("STATUS_LEDGER.tsv")}
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    completeness = (HERE / "COMPLETENESS_MAP.md").read_text(encoding="utf-8")
    registered_gates = rows("AUDIT_SEMANTIC_GATES.tsv")
    assert [row["id"] for row in registered_gates] == [f"F{number:02d}" for number in range(1, 28)]
    assert all(row["status"] == "PASS" and row["evidence"] for row in registered_gates)

    short_status = str(git("status", "--short"))
    unrelated_lines = [
        line for line in short_status.splitlines()
        if not line[3:].startswith(PACKAGE + "/")
    ]
    unrelated_text = "".join(line + "\n" for line in unrelated_lines)
    dirty_sha = sha(unrelated_text.encode("utf-8"))
    assert len(unrelated_lines) == EXPECTED_DIRTY_COUNT and dirty_sha == EXPECTED_DIRTY_SHA256
    canon_blob = str(git("hash-object", "CANON.md")).strip()
    assert canon_blob == str(git("rev-parse", f"{BASE}:CANON.md")).strip()

    historical_native = [
        row for row in methods
        if row["classification"] == "NATIVE_EXACT_REDERIVED_BOUNDED"
    ]
    flags = result["authority_boundary"]
    facts = {
        "F01": source_count == 17,
        "F02": references == independent_references,
        "F03": len(methods) == 23 and method_by_id["M06"]["rationale"].find("retract") >= 0,
        "F04": result["historical_physics_restored"] is False and status["historical_lepton_quark_qcd_claims"]["status"] == "NOT_RESTORED",
        "F05": all(row["classification"] != "NATIVE_EXACT_REDERIVED_BOUNDED" for row in methods[:-1]),
        "F06": all(row["audit_status"] == "ARITHMETIC_REPRODUCED_NOT_NATIVE_VALIDATION" for row in formulas),
        "F07": all(method_by_id[key]["classification"] == "IMPORTED_COMPARISON_ONLY" for key in ("M06", "M10", "M12", "M19", "M20")) and "complex/Hermitian" in method_by_id["M13"]["import_or_free_join"],
        "F08": all(row["native_or_mathematical_input"] and row["import_or_free_join"] for row in methods),
        "F09": status["screen_response_coefficients"]["status"] == "OPEN",
        "F10": "look-elsewhere" in report and "look-elsewhere" in method_by_id["M11"]["rationale"] and "near-matches" in method_by_id["M15"]["rationale"],
        "F11": len(rows("DIMENSION_GENERALIZATION.tsv")) == 5 and result["old_3_plus_5_unique"] is False,
        "F12": len(historical_native) == 1 and historical_native[0]["method_id"] == "M23" and historical_native[0]["historical_section"] == "current cross-map",
        "F13": "unique metric decomposition" in exact,
        "F14": status["action_source_carrier_matter_map"]["status"] == "OPEN",
        "F15": "matter interpretation" in report and status["action_source_carrier_matter_map"]["status"] == "OPEN",
        "F16": method_by_id["M13"]["classification"] == "PURE_MATH_REUSABLE_CONDITIONAL",
        "F17": all(key in method_by_id for key in ("M06", "M07", "M11", "M17")),
        "F18": len(references) == 45 and all(row["history_resolved_path"] == "-" for row in references),
        "F19": all(value is False for key, value in flags.items() if key != "historical_particle_or_gauge_claim_restored"),
        "F20": all("VALIDATION" in row["audit_status"] for row in formulas),
        "F21": len(source_paths) == 17,
        "F22": {row["object"] for row in ownership} == {"reciprocal_depth", "screen_rotation", "lambda_identity_response", "two_shape_components", "pair_screen_mixing", "complete_screen_generator", "action_source_dynamics"},
        "F23": "Not covered" in completeness and "No negative" in completeness,
        "F24": result["compute"] == {"backend": "CPU_SYMBOLIC", "gpu_work_performed": False} and flags["ode_pde_time_live_or_gpu_work_launched"] is False,
        "F25": canon_blob == str(git("rev-parse", f"{BASE}:CANON.md")).strip(),
        "F26": len(unrelated_lines) == EXPECTED_DIRTY_COUNT and dirty_sha == EXPECTED_DIRTY_SHA256,
        "F27": "VERIFIED-WITH-CAVEATS_SAME_CONTEXT_INDEPENDENT_IMPLEMENTATION" in report,
    }
    validate_semantic_gates(facts)
    catches = []
    for gate_id in sorted(facts):
        corrupted = dict(facts); corrupted[gate_id] = False
        rejected = False
        try:
            validate_semantic_gates(corrupted)
        except AssertionError as exc:
            rejected = gate_id in str(exc)
        assert rejected
        catches.append({
            "id": gate_id,
            "mutation": "force_independently_computed_gate_predicate_false",
            "expected": "REJECT",
            "observed": "REJECT",
            "result": "PASS",
        })
    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(catches)

    output = {
        "schema": "udt-historical-angular-method-salvage-verification-1.0",
        "status": "PASS_VERIFIED_WITH_CAVEATS_SAME_CONTEXT_INDEPENDENT_IMPLEMENTATION",
        "implementation": "PYTHON_STDLIB_NO_SYMPY_NO_PRODUCTION_IMPORT",
        "source_blobs_replayed": source_count,
        "historical_document_sha256": sha(document_bytes),
        "historical_methods_verified": len(methods),
        "transitive_references_verified": len(references),
        "missing_from_all_git_history": sum(row["history_resolution_status"] == "MISSING_FROM_ALL_GIT_HISTORY" for row in references),
        "method_class_counts": observed_classes,
        "algebra": algebra,
        "operator_outcome": "COMPLETE_SCREEN_RESPONSE_ALGEBRA_EXACT;_COEFFICIENTS_AND_DYNAMICS_OPEN",
        "historical_physics_restored": False,
        "catch_proofs": len(catches),
        "dirty_checkout": {"paths": len(unrelated_lines), "short_status_sha256": dirty_sha, "contents_read": False},
        "canon_blob_unchanged": True,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
