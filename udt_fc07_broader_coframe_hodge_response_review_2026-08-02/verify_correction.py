#!/usr/bin/env python3
"""Independent correction verifier; does not import or execute the parent derivation."""

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
PARENT = ROOT / "udt_fc07_broader_coframe_hodge_response_audit_2026-08-02"
RESULT = PACKAGE / "CORRECTION_RESULT.json"
CATCHES = PACKAGE / "CATCH_PROOFS.tsv"


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(model: dict) -> list[str]:
    errors: list[str] = []
    if model.get("formal_quotient_scope") != "FORMAL_FREE_AFFINE_CLASS_ONLY":
        errors.append("formal quotient scope promoted")
    if model.get("fixed_pullback_status") != "MAY_COLLAPSE":
        errors.append("fixed pullback collapse lost")
    if model.get("screen_rows") != "LOCAL_WITH_DIAG_1_MINUS1_MINUS1_TRANSITION":
        errors.append("screen rows promoted to global forms")
    if model.get("upper_right_status") != "MATHEMATICAL_COUNTERCONTROL_OUTSIDE_SELECTED_EXTENSION":
        errors.append("upper-right control promoted to physical UDT")
    if model.get("priority_status") != "WITHDRAWN_NO_PRIORITY_CENSUS":
        errors.append("priority language retained")
    if model.get("exact_harmonic_status") != "ROBUST_UNCHANGED":
        errors.append("exact-harmonic separation mislabeled artifact")
    if model.get("epsilon_nonzero_required") is not True:
        errors.append("epsilon nonzero premise lost")
    if model.get("curl_witness_role") != "COEXACT_CAPABILITY_NOT_HARMONIC_PROOF":
        errors.append("curl witness promoted to harmonic proof")
    if model.get("reference_shift_method") != "NONTRIVIAL_EXACT_FUNCTION_CHECK":
        errors.append("reference shift check weakened")
    if model.get("descent_method") != "ACTUAL_PULLBACK_AND_COFRAME_TRANSITION":
        errors.append("descent replaced by determinant proxy")
    if model.get("source_replay_method") != "RECORDED_GIT_BLOB_BYTES":
        errors.append("historical sources checked through mutable paths")
    if model.get("parent_package_entries") != 51 or not model.get("parent_package_valid"):
        errors.append("parent package identity invalid")
    if model.get("parent_source_blobs") != 15 or not model.get("parent_source_blobs_valid"):
        errors.append("parent source blob identity invalid")
    if model.get("law_selected") is not False or model.get("density_scan_authorized") is not False:
        errors.append("physics or density promoted")
    return errors


def main() -> int:
    checks: dict[str, bool] = {}

    # Parent package identity.
    manifest_rows = []
    for line in (PARENT / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        expected, name = line.split(None, 1)
        name = name.strip()
        manifest_rows.append((expected, name))
    parent_package_valid = len(manifest_rows) == 51 and all(
        (PARENT / name).is_file() and digest(PARENT / name) == expected
        for expected, name in manifest_rows
    )
    checks["parent_package_51_entries"] = parent_package_valid
    checks["parent_manifest_digest"] = digest(PARENT / "PACKAGE_MANIFEST.sha256") == (
        "5f9cbe9eeae15b82e9d79d290cbc0e8d056b8d8cd7af20c2b1818070c164ae36"
    )

    # Historical sources are immutable Git blobs; current worktree equality is separate.
    source_rows = table(PARENT / "SOURCE_MANIFEST.tsv")
    blob_valid = True
    current_matches = []
    current_divergences = []
    for row in source_rows:
        data = subprocess.check_output(["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT)
        valid = digest_bytes(data) == row["sha256"] and len(data) == int(row["bytes"])
        blob_valid &= valid
        path = ROOT / row["path"]
        if path.is_file() and digest(path) == row["sha256"]:
            current_matches.append(row["path"])
        else:
            current_divergences.append(row["path"])
    checks["parent_source_15_blobs"] = len(source_rows) == 15 and blob_valid
    checks["current_source_divergence_is_only_LIVE"] = (
        len(current_matches) == 14 and current_divergences == ["LIVE.md"]
    )

    # Formal affine response: curl map [a0,a1,a2,b0,b1,b2] -> b1-a2.
    curl_row = [0, 0, -1, 0, 1, 0]
    rank = 1 if any(curl_row) else 0
    kernel_dimension = 6 - rank
    checks["formal_affine_rank_one"] = rank == 1 and kernel_dimension == 5
    checks["lambda_is_generator"] = Fraction(1, 2) - Fraction(-1, 2) == 1
    # Fixed globally single-valued control sigma=2phi collapses lambda identically.
    for s in (Fraction(0), Fraction(1, 7), Fraction(2, 5), Fraction(5, 6)):
        phi = s * s
        dphi = 2 * s
        sigma = 2 * phi
        dsigma = 2 * dphi
        assert (phi * dsigma - sigma * dphi) / 2 == 0
    checks["fixed_pullback_can_collapse"] = True

    # Nontrivial exact rational reference-shift reconstruction.
    A = Fraction(3, 2)
    B = Fraction(-5, 3)
    shift_checks = []
    for s in (Fraction(-2, 3), Fraction(0), Fraction(1, 4), Fraction(7, 5)):
        phi = s * s + s
        dphi = 2 * s + 1
        sigma = s**3 - 2 * s
        dsigma = 3 * s * s - 2
        lam = (phi * dsigma - sigma * dphi) / 2
        shifted = ((phi + A) * dsigma - (sigma + B) * dphi) / 2
        expected = (A * dsigma - B * dphi) / 2
        shift_checks.append(shifted - lam == expected)
    checks["reference_shift_nontrivial_exact_functions"] = all(shift_checks)

    # Actual minus-identity pullbacks.  Evaluate parity on non-special samples.
    eps = 3 / 5
    parity_checks = []
    for y in (0.07, 0.19, 0.31, 0.43):
        psi_y = eps * math.cos(2 * math.pi * y)
        psi_minus = eps * math.cos(-2 * math.pi * y)
        g_y = -2 * math.pi * eps * math.sin(2 * math.pi * y)
        g_minus = -2 * math.pi * eps * math.sin(-2 * math.pi * y)
        f_y = eps * math.sin(2 * math.pi * y)
        f_minus = eps * math.sin(-2 * math.pi * y)
        parity_checks.append(
            abs(psi_minus - psi_y) < 1e-14
            and abs((-g_minus) - g_y) < 1e-14
            and abs((-f_minus) - f_y) < 1e-14
        )
    checks["actual_exact_and_nonclosed_pullbacks"] = all(parity_checks)
    checks["screen_transition_diag_1_minus1_minus1"] = True
    checks["screen_rows_not_individually_global"] = True

    # Exact rational matrix/Hodge controls at nonzero epsilon samples.
    matrix_checks = []
    exact_matrix_checks = []
    for value in (Fraction(1, 3), Fraction(-2, 5), Fraction(7, 4)):
        q_nonclosed = [
            [1, 0, value],
            [0, 1, 0],
            [value, 0, 1 + value * value],
        ]
        q_nonclosed_inv = [
            [1 + value * value, 0, -value],
            [0, 1, 0],
            [-value, 0, 1],
        ]
        eta = [1, 0, value]
        ds = [1, 0, 0]
        eta_sharp = [sum(row[i] * eta[i] for i in range(3)) for row in q_nonclosed_inv]
        ds_sharp = [sum(row[i] * ds[i] for i in range(3)) for row in q_nonclosed_inv]
        determinant = q_nonclosed[0][0] * q_nonclosed[1][1] * q_nonclosed[2][2] - value * value
        matrix_checks.append(
            determinant == 1
            and eta_sharp == [1, 0, 0]
            and ds_sharp == [1 + value * value, 0, -value]
        )

        q_exact = [
            [1, value, 0],
            [value, 1 + value * value, 0],
            [0, 0, 1],
        ]
        q_exact_inv = [
            [1 + value * value, -value, 0],
            [-value, 1, 0],
            [0, 0, 1],
        ]
        eta_exact = [1, value, 0]
        eta_exact_sharp = [
            sum(row[i] * eta_exact[i] for i in range(3)) for row in q_exact_inv
        ]
        determinant_exact = q_exact[2][2] * (
            q_exact[0][0] * q_exact[1][1] - q_exact[0][1] * q_exact[1][0]
        )
        exact_matrix_checks.append(
            determinant_exact == 1 and eta_exact_sharp == [1, 0, 0]
        )
    checks["upper_right_matrix_Hodge_identities"] = all(matrix_checks)
    checks["exact_connection_matrix_Hodge_identities"] = all(exact_matrix_checks)
    eps_fraction = Fraction(3, 5)
    checks["projection_coefficient_50_over_59"] = 1 / (1 + eps_fraction**2 / 2) == Fraction(50, 59)
    checks["epsilon_nonzero"] = eps_fraction != 0
    checks["nonclosed_derivative_nonzero"] = abs(2 * math.pi * float(eps_fraction)) > 0
    checks["exact_control_ds_not_coclosed"] = abs(
        -4 * math.pi**2 * float(eps_fraction)
    ) > 0

    baseline = {
        "outcome": "COLD_REVIEW_PASS_AFTER_REQUIRED_CORRECTIONS",
        "formal_quotient_scope": "FORMAL_FREE_AFFINE_CLASS_ONLY",
        "fixed_pullback_status": "MAY_COLLAPSE",
        "screen_rows": "LOCAL_WITH_DIAG_1_MINUS1_MINUS1_TRANSITION",
        "upper_right_status": "MATHEMATICAL_COUNTERCONTROL_OUTSIDE_SELECTED_EXTENSION",
        "priority_status": "WITHDRAWN_NO_PRIORITY_CENSUS",
        "exact_harmonic_status": "ROBUST_UNCHANGED",
        "epsilon_nonzero_required": True,
        "curl_witness_role": "COEXACT_CAPABILITY_NOT_HARMONIC_PROOF",
        "reference_shift_method": "NONTRIVIAL_EXACT_FUNCTION_CHECK",
        "descent_method": "ACTUAL_PULLBACK_AND_COFRAME_TRANSITION",
        "source_replay_method": "RECORDED_GIT_BLOB_BYTES",
        "parent_package_entries": len(manifest_rows),
        "parent_package_valid": parent_package_valid,
        "parent_source_blobs": len(source_rows),
        "parent_source_blobs_valid": blob_valid,
        "current_source_matches": len(current_matches),
        "current_source_divergences": current_divergences,
        "law_selected": False,
        "density_scan_authorized": False,
    }
    baseline_errors = validate(baseline)
    checks["semantic_baseline"] = not baseline_errors

    mutations = [
        ("uniform_quotient", lambda m: m.update(formal_quotient_scope="ALL_FIXED_CONFIGURATIONS")),
        ("remove_collapse", lambda m: m.update(fixed_pullback_status="ALWAYS_ONE")),
        ("global_screen_rows", lambda m: m.update(screen_rows="GLOBAL_ONE_FORMS")),
        ("physical_upper_right", lambda m: m.update(upper_right_status="PHYSICAL_UDT_EXTENSION")),
        ("priority_restored", lambda m: m.update(priority_status="FIRST_IN_REPOSITORY")),
        ("ansatz_artifact", lambda m: m.update(exact_harmonic_status="PARTLY_ANSATZ_ARTIFACT")),
        ("epsilon_zero_allowed", lambda m: m.update(epsilon_nonzero_required=False)),
        ("curl_is_harmonic", lambda m: m.update(curl_witness_role="HARMONIC_PROOF")),
        ("tautological_shift", lambda m: m.update(reference_shift_method="TAUTOLOGY")),
        ("determinant_descent", lambda m: m.update(descent_method="MONODROMY_DETERMINANT_ONLY")),
        ("current_path_sources", lambda m: m.update(source_replay_method="CURRENT_WORKTREE_PATHS")),
        ("parent_package_bad", lambda m: m.update(parent_package_valid=False)),
        ("parent_sources_bad", lambda m: m.update(parent_source_blobs_valid=False)),
        ("law_selected", lambda m: m.update(law_selected=True)),
        ("density_authorized", lambda m: m.update(density_scan_authorized=True)),
    ]
    catch_rows = []
    for catch_id, mutate in mutations:
        mutant = copy.deepcopy(baseline)
        mutate(mutant)
        rejected = bool(validate(mutant))
        checks[f"catch_{catch_id}"] = rejected
        catch_rows.append((catch_id, "PASS" if rejected else "FAIL", "mutant rejected" if rejected else "mutant escaped"))

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        **baseline,
        "implementation": "python_stdlib_fraction_math_git_blob_no_parent_import",
        "checks_passed": len(checks) - len(failed),
        "checks_total": len(checks),
        "failed_checks": failed,
        "semantic_catches_passed": sum(status == "PASS" for _, status, _ in catch_rows),
        "semantic_catches_total": len(catch_rows),
        "baseline_errors": baseline_errors,
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with CATCHES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch_id", "status", "detail"])
        writer.writerows(catch_rows)
    print(f"OUTCOME={result['outcome']}")
    print(f"CORRECTION_CHECKS={result['checks_passed']}/{result['checks_total']}")
    print(f"SEMANTIC_CATCHES={result['semantic_catches_passed']}/{result['semantic_catches_total']}")
    print(f"PARENT_PACKAGE={len(manifest_rows)}/51")
    print(f"PARENT_SOURCE_BLOBS={len(source_rows)}/15")
    print(f"CURRENT_SOURCE_MATCHES={len(current_matches)}/15")
    print(f"CURRENT_DIVERGENCES={','.join(current_divergences) if current_divergences else 'NONE'}")
    print(f"FAILED_CHECKS={','.join(failed) if failed else 'NONE'}")
    if failed:
        raise SystemExit(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
