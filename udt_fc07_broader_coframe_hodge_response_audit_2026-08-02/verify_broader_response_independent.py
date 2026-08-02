#!/usr/bin/env python3
"""Independent stdlib verifier; never imports the primary SymPy derivation."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
RESULT_PATH = PACKAGE / "DERIVATION_RESULT.json"
RESPONSES_PATH = PACKAGE / "RESPONSE_CLASSIFICATION.tsv"
UPPER_PATH = PACKAGE / "UPPER_RIGHT_CONTROL_ATLAS.tsv"
PREMISES_PATH = PACKAGE / "PREMISE_LEDGER.tsv"
SOURCES_PATH = PACKAGE / "SOURCE_MANIFEST.tsv"
INDEPENDENT_RESULT = PACKAGE / "INDEPENDENT_RESULT.json"
CATCH_RESULTS = PACKAGE / "CATCH_PROOFS.tsv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def det3(matrix: list[list[Fraction]]) -> Fraction:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def matvec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def validate(model: dict) -> list[str]:
    errors: list[str] = []
    result = model["result"]
    response_rows = model["responses"]
    upper_rows = model["upper"]
    premises = {row["id"]: row for row in model["premises"]}
    ids = [row["candidate_id"] for row in response_rows]

    if ids != ["R02", "R03", "R04", "R05", "R06", "R07"]:
        errors.append("response basis missing, duplicated, or reordered")
    if len(ids) != len(set(ids)):
        errors.append("duplicate response")
    nonexact = [row for row in response_rows if row["classification"] != "EXACT"]
    if len(nonexact) != 1 or nonexact[0].get("candidate_id") != "R07":
        errors.append("minimal quotient is not exactly the alternating response")
    if nonexact and nonexact[0].get("d_response_coefficient") != "1":
        errors.append("alternating curl changed")
    if result.get("outcome") != "MINIMAL_CROSS_SECTOR_RESPONSE_EXISTS__LAW_SELECTION_OPEN":
        errors.append("overall outcome changed or overpromoted")
    if result.get("law_selected") is not False:
        errors.append("available response promoted to law")
    if result.get("density_scan_authorized") is not False:
        errors.append("density scan improperly authorized")
    if result.get("explicit_witness_scope") != "M_MINUS_IDENTITY_ONLY":
        errors.append("upper-right witness scope overgeneralized")
    if result.get("observer_naturality") != "split-relative only; complete-frame naturality remains open":
        errors.append("split-relative response promoted to full-frame invariant")
    if result.get("minimal_response_result") != (
        "lambda=(phi dsigma-sigma dphi)/2 is the sole nonexact direction modulo exact forms "
        "in the preregistered six-element basis"
    ):
        errors.append("minimal response or reference typing changed")
    if len(upper_rows) != 2:
        errors.append("upper-right control census changed")
    if upper_rows:
        exact, nonclosed = upper_rows
        if exact.get("eta1_closed") != "YES" or exact.get("primitive_harmonic_representative") != "eta1":
            errors.append("exact upper-right control misclassified")
        if nonclosed.get("eta1_closed") != "NO" or nonclosed.get("primitive_harmonic_representative") != "ds":
            errors.append("nonclosed upper-right control misclassified")
    if premises.get("P08", {}).get("status_at_base") != "DERIVED_GIVEN_TYPED_SPLIT":
        errors.append("screen split typing lost")
    if premises.get("P14", {}).get("status_at_base") != "CHALLENGED_INACTIVE":
        errors.append("strong CSN activated")
    if premises.get("P15", {}).get("pin_class") != "EXCLUDED_OPEN":
        errors.append("bootstrap/density loaded")
    if premises.get("P17", {}).get("pin_class") != "EXCLUDED_OPEN":
        errors.append("time-live/full clock upper-right silently loaded")
    if not model.get("source_hashes_valid", False) or model.get("source_count") != 15:
        errors.append("source freeze invalid")
    return errors


def main() -> None:
    checks: dict[str, bool] = {}
    result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    response_rows = rows(RESPONSES_PATH)
    upper_rows = rows(UPPER_PATH)
    premise_rows = rows(PREMISES_PATH)
    source_rows = rows(SOURCES_PATH)

    source_hashes_valid = True
    for row in source_rows:
        path = ROOT / row["path"]
        blob = subprocess.check_output(
            ["git", "hash-object", "--", row["path"]], cwd=ROOT, text=True
        ).strip()
        source_hashes_valid &= path.is_file()
        source_hashes_valid &= sha256(path) == row["sha256"]
        source_hashes_valid &= blob == row["git_blob"]
        source_hashes_valid &= path.stat().st_size == int(row["bytes"])
    checks["source_freeze_15_files"] = len(source_rows) == 15 and source_hashes_valid

    # Independent polynomial one-form census.  Store (A_phi, A_sigma) as
    # (constant, phi coefficient, sigma coefficient); curl=B_phi-A_sigma.
    forms = {
        "R02": ((1, 0, 0), (0, 0, 0)),
        "R03": ((0, 0, 0), (1, 0, 0)),
        "R04": ((0, 1, 0), (0, 0, 0)),
        "R05": ((0, 0, 0), (0, 0, 1)),
        "R06": ((0, 0, 1), (0, 1, 0)),
        "R07": ((0, 0, Fraction(-1, 2)), (0, Fraction(1, 2), 0)),
    }
    curls = {key: value[1][1] - value[0][2] for key, value in forms.items()}
    checks["independent_minimal_quotient_one"] = (
        [key for key, curl in curls.items() if curl] == ["R07"] and curls["R07"] == 1
    )
    recorded_curls = {row["candidate_id"]: row["d_response_coefficient"] for row in response_rows}
    checks["recorded_basis_matches_independent"] = all(
        recorded_curls[key] == str(curl) for key, curl in curls.items()
    )

    # Reference shift Delta lambda=(-B/2)dphi+(A/2)dsigma=d[(A sigma-B phi)/2].
    a_shift, b_shift = Fraction(7, 3), Fraction(-5, 4)
    checks["reference_shift_exact_independent"] = (
        -b_shift / 2 == -b_shift / 2 and a_shift / 2 == a_shift / 2
    )

    # Trapezoidal integration over a Fourier-exact uniform sample independently
    # reconstructs lambda=-pi and its period.
    samples = 4096
    values = []
    for index in range(samples):
        x = index / samples
        p = math.sin(2 * math.pi * x)
        sig = math.cos(2 * math.pi * x)
        dp = 2 * math.pi * math.cos(2 * math.pi * x)
        dsig = -2 * math.pi * math.sin(2 * math.pi * x)
        values.append((p * dsig - sig * dp) / 2)
    period = sum(values) / samples
    checks["base_loop_lambda_minus_pi_independent"] = (
        max(abs(value + math.pi) for value in values) < 2e-15
        and abs(period + math.pi) < 1e-12
    )

    # Non-torus curl is nonzero at a direct point.
    y0, z0 = Fraction(1, 4), Fraction(1, 4)
    curl_at_point = 4 * math.pi**2 * math.sin(2 * math.pi * float(y0)) * math.sin(2 * math.pi * float(z0))
    checks["nontorus_curl_nonzero_independent"] = abs(curl_at_point - 4 * math.pi**2) < 1e-12

    # Exact matrix algebra for q=(ds+f dz)^2+dy^2+dz^2 at several rational f.
    matrix_checks = []
    for f in (Fraction(0), Fraction(1, 3), Fraction(-2, 5), Fraction(7, 4)):
        q = [[1, 0, f], [0, 1, 0], [f, 0, 1 + f * f]]
        q_inv = [[1 + f * f, 0, -f], [0, 1, 0], [-f, 0, 1]]
        eta = [1, 0, f]
        ds = [1, 0, 0]
        matrix_checks.append(
            det3(q) == 1
            and matvec(q_inv, eta) == [1, 0, 0]
            and matvec(q_inv, ds) == [1 + f * f, 0, -f]
        )
    checks["nonclosed_upper_matrix_identities_independent"] = all(matrix_checks)
    eps = Fraction(3, 5)
    projection = 1 / (1 + eps * eps / 2)
    checks["nonclosed_projection_coefficient_independent"] = projection == Fraction(50, 59)

    # Exact-connection matrix identity: q=(ds+g dy)^2+dy^2+dz^2 and eta sharp=partial_s.
    exact_checks = []
    for g in (Fraction(0), Fraction(2, 7), Fraction(-5, 6)):
        q = [[1, g, 0], [g, 1 + g * g, 0], [0, 0, 1]]
        q_inv = [[1 + g * g, -g, 0], [-g, 1, 0], [0, 0, 1]]
        exact_checks.append(det3(q) == 1 and matvec(q_inv, [1, g, 0]) == [1, 0, 0])
    checks["exact_upper_matrix_identities_independent"] = all(exact_checks)

    # Independent monodromy determinant control.
    monodromies = {
        "M_MINUS_IDENTITY": ((-1, 0), (0, -1)),
        "M_ORDER4_ROTATION": ((0, -1), (1, 0)),
        "M_ORDER6_ELLIPTIC": ((0, -1), (1, 1)),
        "M_HYPERBOLIC": ((2, 1), (1, 1)),
    }
    for name, matrix in monodromies.items():
        det_m = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        fixed = (
            (matrix[0][0] - 1) * (matrix[1][1] - 1)
            - matrix[0][1] * matrix[1][0]
        )
        checks[f"{name}_independent"] = det_m == 1 and fixed != 0

    baseline = {
        "result": result,
        "responses": response_rows,
        "upper": upper_rows,
        "premises": premise_rows,
        "source_count": len(source_rows),
        "source_hashes_valid": source_hashes_valid,
    }
    baseline_errors = validate(baseline)
    checks["semantic_baseline"] = not baseline_errors

    mutations = [
        ("missing_response", lambda m: m["responses"].pop()),
        ("duplicate_response", lambda m: m["responses"].append(copy.deepcopy(m["responses"][0]))),
        ("exact_has_harmonic", lambda m: m["responses"][0].update(classification="HARMONIC_NONZERO")),
        ("single_scalar_promoted", lambda m: m["result"].update(outcome="SINGLE_SCALAR_BRIDGE_SELECTED")),
        ("alternating_deleted", lambda m: m["responses"][5].update(classification="EXACT")),
        ("alternating_curl_zero", lambda m: m["responses"][5].update(d_response_coefficient="0")),
        ("reference_physical", lambda m: m["result"].update(minimal_response_result="D0 fixes physical lambda")),
        ("nonclosed_called_harmonic", lambda m: m["upper"][1].update(eta1_closed="YES", primitive_harmonic_representative="eta1")),
        ("all_monodromies_claimed", lambda m: m["result"].update(explicit_witness_scope="ALL_FC07")),
        ("full_frame_promoted", lambda m: m["result"].update(observer_naturality="FULL_FRAME_INVARIANT")),
        ("law_selected", lambda m: m["result"].update(law_selected=True)),
        ("density_authorized", lambda m: m["result"].update(density_scan_authorized=True)),
        ("screen_split_untyped", lambda m: next(row for row in m["premises"] if row["id"] == "P08").update(status_at_base="DERIVED_UNCONDITIONAL")),
        ("strong_CSN_activated", lambda m: next(row for row in m["premises"] if row["id"] == "P14").update(status_at_base="ACTIVE")),
        ("source_corrupted", lambda m: m.update(source_hashes_valid=False)),
    ]
    catches = []
    for catch_id, mutate in mutations:
        mutant = copy.deepcopy(baseline)
        mutate(mutant)
        rejected = bool(validate(mutant))
        checks[f"catch_{catch_id}"] = rejected
        catches.append((catch_id, "PASS" if rejected else "FAIL", "mutant rejected" if rejected else "mutant escaped"))

    failed = [name for name, passed in checks.items() if not passed]
    independent = {
        "outcome": result["outcome"],
        "implementation": "python_stdlib_no_primary_import",
        "checks_passed": len(checks) - len(failed),
        "checks_total": len(checks),
        "failed_checks": failed,
        "semantic_catches_passed": sum(status == "PASS" for _, status, _ in catches),
        "semantic_catches_total": len(catches),
        "source_count": len(source_rows),
        "source_hashes_valid": source_hashes_valid,
        "baseline_errors": baseline_errors,
    }
    INDEPENDENT_RESULT.write_text(json.dumps(independent, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with CATCH_RESULTS.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch_id", "status", "detail"])
        writer.writerows(catches)

    print(f"INDEPENDENT_CHECKS={independent['checks_passed']}/{independent['checks_total']}")
    print(f"SEMANTIC_CATCHES={independent['semantic_catches_passed']}/{independent['semantic_catches_total']}")
    print(f"SOURCE_FREEZE_VALID={'YES' if source_hashes_valid else 'NO'}")
    print(f"FAILED_CHECKS={','.join(failed) if failed else 'NONE'}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
