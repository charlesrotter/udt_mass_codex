#!/usr/bin/env python3
"""Fail-closed deterministic verifier for the null-section / Hopfion metric audit."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import io
import json
import pathlib
import platform
import subprocess
import sys
import tempfile

import sympy as sp


BASE = "715fa57767ecc2ec370599ad18cd9f87911798d8"
PREREG_COMMIT = "3588962"
PREREG_SHA256 = "ad46dc61f5b10f560f615b607b9053acb10f2908d28949fdc0ac0598b302a2c5"
VERDICT = (
    "EXACT_RECIPROCAL_HOPF_ORBIT_BLOCK_COMPATIBILITY_WITNESS; "
    "CONDITIONAL_UNIT_HOPF_CONNECTION_AFTER_TORIC_S3_COMPLETION; "
    "ANGULAR_SLOTS_GLOBAL_CLOSURE_BOUNDARY_CONFIGURATION_SPACE_AND_ACTION_OPEN; "
    "DIRECT_CELESTIAL_CARRIER_IDENTITY_BLOCKED_WITHOUT_SOLDERING"
)


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git(repo: pathlib.Path, *args: str, binary: bool = False):
    completed = subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if completed.returncode:
        error = completed.stderr if not binary else completed.stderr.decode("utf-8", "replace")
        raise AssertionError(f"git {' '.join(args)} failed: {error}")
    return completed.stdout


def rows_from_text(payload: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(payload), delimiter="\t"))


def rows(path: pathlib.Path) -> list[dict[str, str]]:
    return rows_from_text(path.read_text(encoding="utf-8"))


def reject(name: str, callback) -> dict[str, str]:
    try:
        callback()
    except (AssertionError, KeyError, ValueError) as exc:
        return {"name": name, "result": "PASS", "caught": type(exc).__name__}
    raise AssertionError(f"catch-proof accepted corruption: {name}")


def validate_prereg(repo: pathlib.Path, package: pathlib.Path) -> None:
    parent = str(git(repo, "rev-parse", f"{PREREG_COMMIT}^")).strip()
    changed = str(
        git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", PREREG_COMMIT)
    ).splitlines()
    expected = ["null_section_hopfion_metric_audit_2026-07-19/PREREGISTRATION.md"]
    assert parent == BASE, (parent, BASE)
    assert changed == expected, changed
    assert sha((package / "PREREGISTRATION.md").read_bytes()) == PREREG_SHA256


def validate_sources(
    repo: pathlib.Path,
    inventory: list[dict[str, str]],
    replacements: dict[str, bytes] | None = None,
) -> None:
    replacements = replacements or {}
    assert len(inventory) == 15
    paths = [row["current_path"] for row in inventory]
    assert len(set(paths)) == 15
    for row in inventory:
        path = row["current_path"]
        payload = replacements.get(path)
        if payload is None:
            payload = bytes(git(repo, "show", f"{BASE}:{path}", binary=True))
        assert row["blob_oid"] == str(git(repo, "rev-parse", f"{BASE}:{path}")).strip()
        assert row["sha256"] == sha(payload)
        assert int(row["size_bytes"]) == len(payload)
        assert row["last_commit"] == str(
            git(repo, "log", "-1", "--format=%H", BASE, "--", path)
        ).strip()


def validate_source_semantics(repo: pathlib.Path, replacements: dict[str, str] | None = None) -> None:
    replacements = replacements or {}

    def text(path: str) -> str:
        if path in replacements:
            return replacements[path]
        return str(git(repo, "show", f"{BASE}:{path}"))

    required = {
        "UDT_NATIVE_ACTION_COLD_PACKET.md": [
            "any slot identification retain their separately ledgered non-derived statuses",
            "the transverse spatial block or full time-live geometry",
            "a matter carrier",
        ],
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": [
            "D(\\phi)=\\operatorname{diag}(e^{-\\phi},e^\\phi)",
            "the matter carrier",
        ],
        "reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md": [
            "metric-only timelike, spacelike, or null line selector exists",
            "A metric does not uniquely factor into a coframe",
        ],
        "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md": [
            "a sphere fiber is not a chosen field",
            "This is not UDT-unique yet",
        ],
        "hopfion_arc_scripts_2026-07-05/fs_hopfion.py": [
            "torch.stack([n1, n2, n3], 0)",
            "dn = grads(n, h)",
            "Q_H = (1/16pi^2)",
        ],
        "noNull_energy.py": [
            "same continuum functional",
            "dn = [_dop(n, 1",
        ],
        "simple_metric_angular_on_solution_space_MAP.md": [
            "phi=\\phi(r,\\vartheta,\\varphi)",
            "Christoffel symbols involve",
        ],
        "simple_metric_angular_on_L_multipole_results.md": [
            "wall-loud",
            "not full Einstein backreaction",
        ],
        "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md": [
            "whole-solution event-domain",
            "Co-presence is not zero-time separation",
        ],
    }
    for path, tokens in required.items():
        payload = text(path)
        for token in tokens:
            assert token in payload, f"missing source token {path}: {token}"


def validate_ledger(ledger: list[dict[str, str]]) -> None:
    assert len(ledger) == 22
    ids = [row["claim_id"] for row in ledger]
    assert ids == [f"N{number:02d}" for number in range(1, 23)]
    assert len(set(ids)) == 22
    by_id = {row["claim_id"]: row for row in ledger}
    expected = {
        "N02": "OPEN",
        "N04": "DIRECT_UNFRAMED_IDENTITY_BLOCKED",
        "N05": "NOT_FRAME_INVARIANT",
        "N06": "NOT_LOCALLY_FRAME_COVARIANT",
        "N07": "GENERIC_RECIPROCAL_NORMAL_FORM",
        "N08": "EXACT_ALGEBRAIC_MATCH",
        "N10": "CONDITIONAL_COMPLETION",
        "N11": "CONDITIONAL_CSN_INVARIANT_CONNECTION",
        "N12": "CONDITIONAL_UNIT_CLASS",
        "N14": "UNDERDETERMINED",
        "N15": "WORKING_CANDIDATE",
        "N16": "NO_DIRECTION_SELECTOR",
        "N18": "GEOMETRIC_COUPLING_NOT_HOPF_SELECTION",
        "N20": "CONCEPTUALLY_COMPATIBLE_NOT_SELECTED",
        "N21": "OPEN",
        "N22": "PROMISING_STRONGER_CONDITIONAL_ROUTE",
    }
    for claim_id, status in expected.items():
        assert by_id[claim_id]["status"] == status, (claim_id, by_id[claim_id]["status"])
    assert "compatibility, not uniqueness" in by_id["N07"]["maximum_claim"]
    assert "not derived boundary physics" in by_id["N15"]["maximum_claim"]
    assert "separate preregistered derivation" in by_id["N21"]["maximum_claim"]
    assert "canonical unit-class compatibility witness" in by_id["N22"]["maximum_claim"]


def validate_algebra(result: dict) -> None:
    assert result["status"] == "PASS"
    assert result["check_count"] == 32
    assert len(result["checks"]) == 32 and set(result["checks"].values()) == {"PASS"}
    exact = result["exact_identities"]
    assert exact["null_lift_norm"] == "n_x**2 + n_y**2 + n_z**2 - 1"
    assert exact["positive_conformal_null_lift_norm"] == "Omega_c**2*(n_x**2 + n_y**2 + n_z**2 - 1)"
    assert exact["integral_A_wedge_dA"] == "-4*pi**2"
    assert exact["registered_hopf_charge"] == "1"
    assert exact["doubled_connection_integral"] == "-16*pi**2"
    assert exact["doubled_connection_charge_1_over_16pi2"] == "1"
    assert exact["diagonal_and_antidiagonal_charges"] == ["1", "-1"]
    assert exact["anti_diagonal_connection_density"] == "cosh(2*phi)**(-2)"
    assert exact["constant_map_registered_hopf_charge"] == "0"
    assert exact["constant_map_pullback_curvature"] == ["0", "0", "0"]
    assert exact["aberration_pair_dot_product_before"] == "0"
    assert exact["aberration_pair_dot_product_after"] == "beta**2"
    assert exact["winding_frame_standard_hopf_map"] == [
        "sin(2*eta_h)*cos(xi1 - xi2)",
        "sin(2*eta_h)*sin(xi1 - xi2)",
        "cos(2*eta_h)",
    ]
    assert exact["normalized_hopf_torus_block"] == "Matrix([[exp(-2*phi), 0], [0, exp(2*phi)]])"
    assert exact["round_mixed_tracefree"] == "Matrix([[0, 0], [0, 0]])"
    assert exact["reciprocal_mixed_tracefree"] == "Matrix([[-1, 0], [0, 1]])"
    assert exact["rotating_round_dyad_covariant_derivative"] == "Matrix([[0, 0], [0, 0]])"
    assert exact["geometric_type_shapes"] == {
        "internal_target_map": [3, 1],
        "spacetime_null_lift": [4, 1],
    }
    assert exact["angular_phi_frobenius_coefficients"] == [
        "A_theta/A**2", "A_varphi/A**2",
    ]
    assert exact["spatial_slice_pullback_of_ell_wedge_dell"] == "0"
    assert exact["round_completion_endpoint_limits"] == {
        "Omega_minus_infinity": "0",
        "Omega_plus_infinity": "0",
        "f_minus_infinity": "1",
        "f_plus_infinity": "0",
        "g_minus_infinity": "0",
        "g_plus_infinity": "1",
    }
    structural = result["structural_readout"]
    assert "Every positive diagonal two-block" in structural["genericity_caveat"]
    assert "does not place the reciprocal pair" in structural["not_selected"]
    assert "Omega>0 holds on the open principal-orbit region" in structural["csn_endpoint_caveat"]
    assert result["maximum_verdict"] == VERDICT


def validate_report(report: str) -> None:
    required = [
        "Every positive diagonal two-block has a reciprocal determinant-one normal form",
        "compatibility theorem, not a uniqueness theorem",
        "does not put its reciprocal pair into two",
        "periodic spatial angular slots",
        "admit lens-space",
        "No physical time direction was compactified",
        "normalized reciprocal orbit block and the",
        "positively conformally related on the open principal-orbit region",
        "full three-metric additionally requires the independently supplied radial",
        "DIRECT_CELESTIAL_CARRIER_IDENTITY_BLOCKED_WITHOUT_SOLDERING",
        "Its pullback to a constant-`t` spatial slice vanishes",
        "No existing action is derived by this audit",
        "one canonical `Q=+/-1` witness",
        "not the full carrier configuration space `Map(S3,S2)`",
        "WORKING_CANDIDATE",
    ]
    for token in required:
        assert token in report, token
    forbidden = [
        "reciprocity proves S3",
        "carrier is derived from the metric",
        "co-presence selects the construction",
        "time-live stability is established",
    ]
    lower = report.lower()
    for token in forbidden:
        assert token not in lower, token


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    package = pathlib.Path(__file__).resolve().parent
    repo = package.parent
    validate_prereg(repo, package)

    inventory = rows(package / "SOURCE_INVENTORY.tsv")
    ledger = rows(package / "STATUS_LEDGER.tsv")
    derivation = json.loads((package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    report = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")

    validate_sources(repo, inventory)
    validate_source_semantics(repo)
    validate_ledger(ledger)
    validate_algebra(derivation)
    validate_report(report)

    with tempfile.TemporaryDirectory(prefix="null_section_hopf_replay_") as temp:
        replay = pathlib.Path(temp) / "DERIVATION_RESULT.json"
        completed = subprocess.run(
            [sys.executable, str(package / "derive_null_section_hopfion.py"), "--output", str(replay)],
            cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
        )
        assert completed.returncode == 0, completed.stderr
        assert completed.stderr == ""
        assert replay.read_bytes() == (package / "DERIVATION_RESULT.json").read_bytes()

    catches: list[dict[str, str]] = []
    for claim_id, bad_status, name in [
        ("N02", "DERIVED_ANGULAR_BLOCK", "open_angular_block_promoted"),
        ("N04", "DIRECT_IDENTITY_DERIVED", "celestial_identity_promoted"),
        ("N05", "FRAME_INVARIANT", "frame_winding_ignored"),
        ("N06", "LOCALLY_COVARIANT", "ordinary_energy_mislabeled_covariant"),
        ("N07", "UNIQUE_HOPF_SIGNATURE", "generic_normal_form_ignored"),
        ("N10", "UNIQUE_ROUND_S3", "round_completion_promoted"),
        ("N12", "UNCONDITIONAL_UNIT_CHARGE", "conditional_charge_promoted"),
        ("N14", "S3_UNIQUELY_SELECTED", "lens_space_countermodels_removed"),
        ("N16", "DIRECTION_SELECTED", "round_warp_promoted"),
        ("N18", "HOPF_CHARGE_DERIVED", "angular_phi_coupling_overclaimed"),
        ("N20", "COPRESENCE_SELECTS_SECTION", "copresence_semantics_promoted"),
        ("N21", "ACTION_DERIVED", "open_action_promoted"),
    ]:
        mutated = copy.deepcopy(ledger)
        next(row for row in mutated if row["claim_id"] == claim_id)["status"] = bad_status
        catches.append(reject(name, lambda data=mutated: validate_ledger(data)))

    bad_derivation = copy.deepcopy(derivation)
    bad_derivation["exact_identities"]["registered_hopf_charge"] = "2"
    catches.append(reject("hopf_charge_mutation", lambda: validate_algebra(bad_derivation)))

    for field, value, name in [
        ("positive_conformal_null_lift_norm", "0", "conformal_null_anchor_deleted"),
        ("constant_map_registered_hopf_charge", "1", "constant_map_zero_charge_deleted"),
        ("aberration_pair_dot_product_after", "0", "aberration_mislabeled_fixed_rotation"),
        ("angular_phi_frobenius_coefficients", ["0", "0"], "frobenius_derivation_deleted"),
    ]:
        bad_anchor = copy.deepcopy(derivation)
        bad_anchor["exact_identities"][field] = value
        catches.append(reject(name, lambda data=bad_anchor: validate_algebra(data)))

    bad_derivation = copy.deepcopy(derivation)
    bad_derivation["structural_readout"]["genericity_caveat"] = "S3 is unique"
    catches.append(reject("genericity_caveat_deleted", lambda: validate_algebra(bad_derivation)))

    bad_inventory = copy.deepcopy(inventory)
    bad_inventory[0]["sha256"] = "0" * 64
    catches.append(reject("source_hash_mutation", lambda: validate_sources(repo, bad_inventory)))

    c1_path = "UDT_NATIVE_ACTION_COLD_PACKET.md"
    c1 = str(git(repo, "show", f"{BASE}:{c1_path}"))
    bad_c1 = c1.replace("the transverse spatial block or full time-live geometry", "the selected transverse spatial block")
    catches.append(reject(
        "transverse_open_disclosure_removed",
        lambda: validate_source_semantics(repo, {c1_path: bad_c1}),
    ))

    bad_report = report.replace(
        "compatibility theorem, not a uniqueness theorem",
        "proof that reciprocity uniquely selects S3",
    )
    catches.append(reject("report_uniqueness_overclaim", lambda: validate_report(bad_report)))

    bad_report = report.replace(
        "normalized reciprocal orbit block and the\nround metric's orbit block",
        "normalized reciprocal block and the\nround metric",
    ).replace(
        "The full three-metric additionally requires the independently supplied radial\ncoefficient `g_phiphi=sech^2(2phi)`. ",
        "",
    )
    catches.append(reject("orbit_block_promoted_to_full_metric", lambda: validate_report(bad_report)))

    result = {
        "status": "PASS_SELF_CONSISTENCY",
        "verification_class": "DETERMINISTIC_REPLAY_SOURCE_SNAPSHOT_AND_CATCH_PROOFS; EXTERNAL_SEMANTIC_REVIEW_SEPARATE",
        "base": BASE,
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "source_rows": len(inventory),
        "ledger_rows": len(ledger),
        "algebra_checks": derivation["check_count"],
        "derivation_replay": "PASS_BYTE_IDENTICAL",
        "catch_proof_count": len(catches),
        "catch_proofs": catches,
        "preregistration_sha256": sha((package / "PREREGISTRATION.md").read_bytes()),
        "source_inventory_sha256": sha((package / "SOURCE_INVENTORY.tsv").read_bytes()),
        "derivation_result_sha256": sha((package / "DERIVATION_RESULT.json").read_bytes()),
        "status_ledger_sha256": sha((package / "STATUS_LEDGER.tsv").read_bytes()),
        "audit_report_sha256": sha((package / "AUDIT_REPORT.md").read_bytes()),
        "verdict": VERDICT,
    }
    output = pathlib.Path(args.output)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"VERIFIER PASS sources={len(inventory)}/15 ledger={len(ledger)}/22 "
        f"algebra={derivation['check_count']}/32 catches={len(catches)}/{len(catches)}"
    )
    print(VERDICT)


if __name__ == "__main__":
    main()
