#!/usr/bin/env python3
"""Fail-closed independent verifier for the transverse reciprocal selector."""

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


BASE = "4f5cb5d18b4f3658789a0b0e5f88d1f9439e811a"
PREREG = "5becdc107317802cff8aec44948969a317356204"
PREREG_SHA256 = "94a2193d148ec3219666d9368dde30676d8ea3f442628bf2f9cfc60311e671ea"
VERDICT = (
    "EXACT_REPRESENTATION_LEVEL_RECIPROCAL_HOPF_CORRESPONDENCE_"
    "CONDITIONAL_ON_LORENTZ_SPIN_REALIZATION; "
    "PHYSICAL_TRANSVERSE_SPATIAL_PERIODICITY_UNDERDETERMINED; "
    "GLOBAL_UNIT_HOPF_LIFT_AND_SOLDERING_OPEN; "
    "FINITE_CELL_CAP_GATE_NOT_ACTIVATED"
)


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git(repo: pathlib.Path, *args: str, binary: bool = False):
    result = subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if result.returncode:
        error = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise AssertionError(f"git {' '.join(args)} failed: {error}")
    return result.stdout


def rows(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def rows_text(payload: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(payload), delimiter="\t"))


def reject(name: str, callback) -> dict[str, str]:
    try:
        callback()
    except (AssertionError, KeyError, ValueError) as error:
        return {"name": name, "result": "PASS", "caught": type(error).__name__}
    raise AssertionError(f"catch-proof accepted corruption: {name}")


def validate_prereg(repo: pathlib.Path, package: pathlib.Path) -> None:
    assert str(git(repo, "rev-parse", f"{PREREG}^")).strip() == BASE
    changed = str(git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", PREREG)).splitlines()
    assert changed == ["transverse_reciprocal_realization_selector_2026-07-19/PREREGISTRATION.md"]
    assert sha((package / "PREREGISTRATION.md").read_bytes()) == PREREG_SHA256


def validate_sources(repo: pathlib.Path, inventory: list[dict[str, str]]) -> None:
    assert len(inventory) == 13
    paths = [row["current_path"] for row in inventory]
    assert len(paths) == len(set(paths))
    for row in inventory:
        path = row["current_path"]
        payload = bytes(git(repo, "show", f"{BASE}:{path}", binary=True))
        assert row["blob_oid"] == str(git(repo, "rev-parse", f"{BASE}:{path}")).strip()
        assert row["sha256"] == sha(payload)
        assert int(row["size_bytes"]) == len(payload)
        assert row["last_commit"] == str(git(repo, "log", "-1", "--format=%H", BASE, "--", path)).strip()


def source(repo: pathlib.Path, path: str, replacements: dict[str, str] | None = None) -> str:
    replacements = replacements or {}
    if path in replacements:
        return replacements[path]
    return str(git(repo, "show", f"{BASE}:{path}"))


def validate_source_semantics(repo: pathlib.Path, replacements: dict[str, str] | None = None) -> None:
    required = {
        "UDT_NATIVE_ACTION_COLD_PACKET.md": [
            "the transverse spatial block or full time-live geometry",
            "slot identification retain their separately ledgered non-derived statuses",
            "This principle is a global selection requirement, not a ready-made local field equation",
        ],
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": [
            "the unique native action outside a named derivative/minimality class",
            "the matter carrier",
        ],
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": [
            "The full time-live volume and boundary are not yet derived",
            "No nonlocal insertion",
        ],
        "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md": [
            "a sphere fiber is not a chosen field",
            "needs a frame/trivialization",
        ],
        "null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md": [
            "does not put its reciprocal pair into two",
            "needs a soldering/frame",
            "the existing carrier cannot simply be renamed",
        ],
        "angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md": [
            "Only after that first gate passes",
            "FINITE_CELL_CAP_COMPLETION",
        ],
        "reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md": [
            "NO_UNIVERSAL_LOCAL_METRIC_ONLY_SELECTOR_REALIZATION_MAP_OPEN",
            "type gap matters",
        ],
    }
    for path, tokens in required.items():
        payload = source(repo, path, replacements)
        for token in tokens:
            assert token in payload, f"missing source token {path}: {token}"
    cold = source(repo, "UDT_NATIVE_ACTION_COLD_PACKET.md", replacements)
    assert "the selected transverse spatial spin torus" not in cold
    bootstrap = source(repo, "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", replacements)
    assert "bootstrap selects the spin lift" not in bootstrap.lower()


EXPECTED_CANDIDATES = {
    "F01": ("TANGENT_VECTOR_EXTENSION", "NOT_SELECTED"),
    "F02": ("VOLUME_HODGE_ORIENTATION", "NOT_SELECTED"),
    "F03": ("METRIC_DERIVATIVE_NATURAL_TENSORS", "CONDITIONAL_STRATIFIED"),
    "F04": ("GLOBAL_TRANSVERSE_SURFACES", "UNDERDETERMINED_GLOBAL"),
    "F05": ("CONFORMAL_SPIN_REPRESENTATION", "REPRESENTATION_ONLY_CONDITIONAL"),
    "F06": ("SELF_DUAL_BIVECTOR_OR_FRAME", "NOT_PHYSICAL_SPATIAL_SELECTION"),
    "F07": ("FINITE_CELL_BOOTSTRAP", "NOT_SELECTED"),
}


def validate_candidates(candidates: list[dict[str, str]]) -> None:
    assert len(candidates) == 7
    assert {row["family_id"] for row in candidates} == set(EXPECTED_CANDIDATES)
    assert len({row["family_id"] for row in candidates}) == len(candidates)
    for row in candidates:
        expected = EXPECTED_CANDIDATES[row["family_id"]]
        assert (row["family"], row["physical_spatial_status"]) == expected
    assert next(row for row in candidates if row["family_id"] == "F05")["disposition"] == "RETAINED_POSITIVE_CONDITIONAL"
    global_family = next(row for row in candidates if row["family_id"] == "F04")
    assert global_family["disposition"] == "RETAINED_COUNTERFAMILY"
    assert "irrational-slope" in global_family["counterexample_or_limit"]


EXPECTED_LEDGER = {
    "R01": "DERIVED_CONDITIONAL",
    "R02": "TRANSVERSE_IDENTITY",
    "R03": "NO_NONZERO_EQUIVARIANT_TF_TENSOR",
    "R04": "AREA_ONLY",
    "R05": "CONDITIONAL_STRATIFIED",
    "R06": "NOT_LOCAL_METRIC_DATA",
    "R07": "KINEMATICALLY_COMPATIBLE",
    "R08": "KINEMATICALLY_COMPATIBLE",
    "R09": "CONDITIONAL_DERIVED_FIBER",
    "R10": "EXACT_CONDITIONAL_CORRESPONDENCE",
    "R11": "S3_REPRESENTATIVE_CONDITIONAL",
    "R12": "CP1_EQUALS_S2_CONDITIONAL",
    "R13": "PERIODIC_WITH_DISTINCT_ROLES",
    "R14": "EXACT_RECIPROCAL_MATCH",
    "R15": "UNIT_CLASS_CONDITIONAL",
    "R16": "OPEN_TYPE_GATE",
    "R17": "OPEN",
    "R18": "INSUFFICIENT_FOR_REALIZATION",
    "R19": "NO_CURRENT_RANKING_OPERATOR",
    "R20": "NOT_ACTIVATED",
    "R21": "OPEN",
    "R22": "TWO_LEVEL_RESULT",
}


def validate_ledger(ledger: list[dict[str, str]]) -> None:
    assert len(ledger) == 22
    assert len({row["claim_id"] for row in ledger}) == 22
    assert {row["claim_id"] for row in ledger} == set(EXPECTED_LEDGER)
    for row in ledger:
        assert row["status"] == EXPECTED_LEDGER[row["claim_id"]]
    assert "not a physical spatial universe" in next(row for row in ledger if row["claim_id"] == "R11")["maximum_claim"]
    assert "neither role is a second physical transverse spatial direction" in next(row for row in ledger if row["claim_id"] == "R13")["dependency_or_limit"]
    assert "irrational-slope" in next(row for row in ledger if row["claim_id"] == "R06")["basis"]
    assert "equal component magnitudes" in next(row for row in ledger if row["claim_id"] == "R14")["dependency_or_limit"]
    assert "SU2 to S2 gives S3" in next(row for row in ledger if row["claim_id"] == "R16")["basis"]
    assert next(row for row in ledger if row["claim_id"] == "R20")["status"] == "NOT_ACTIVATED"


def validate_algebra(algebra: dict) -> None:
    assert algebra["status"] == "PASS"
    assert algebra["check_count"] == 40
    assert len(algebra["checks"]) == 40
    assert set(algebra["checks"].values()) == {"PASS"}
    assert algebra["verdict"] == VERDICT
    classification = algebra["classification"]
    assert classification["direct_tangent_vector_route"] == "TRANSVERSE_IDENTITY_NOT_RECIPROCAL_PAIR"
    assert classification["physical_transverse_spatial_periodicity"] == "UNDERDETERMINED_NOT_DERIVED"
    assert classification["global_unit_hopf_lift"] == "OPEN_WITHOUT_GLOBAL_SPIN_LIFT_AND_NORM_FRAME_DATA"
    assert classification["finite_cell_cap_gate"] == "NOT_ACTIVATED"
    assert "PHASE_TWIST_ALPHA" in classification["spin_embedding_uniqueness"]
    assert "EQUAL_COMPONENT_MAGNITUDES" in classification["balanced_reference_ray"]
    topology = algebra["topological_classification"]
    assert "RP3" in topology["metric_rotation_frame_bundle_over_S2"]
    assert "S3" in topology["spin_lift_bundle_over_S2"]
    assert topology["common_phase_role"] == "HOPF_FIBER_GAUGE_NOT_SECOND_PHYSICAL_SPATIAL_DIRECTION"
    assert algebra["exact_identities"]["hopf_unit_class"] == "1"
    assert algebra["exact_identities"]["fubini_study_boost_factor_at_lambda2_rho1"] == "16/25"
    assert set(algebra["counterfamilies"]) == {
        "finite_disk_transverse", "finite_sphere_transverse", "local_plane_vs_torus",
        "irrational_torus_eigenflow", "spin_representation_only"
    }


def validate_report(report: str) -> None:
    required = [
        VERDICT,
        "not a random resemblance",
        "relative phase is celestial azimuth",
        "common phase is the projective/Hopf fiber gauge",
        "SO(3) ≅ RP3",
        "requires the `SU(2)` spin double cover",
        "A_alpha(phi)",
        "16/25",
        "balanced-reference premise",
        "irrational slope `sqrt(2)`",
        "kinematic foundation-compatible counterfamilies",
        "FINITE_CELL_CAP_GATE_NOT_ACTIVATED",
        "No matter spinor",
        "native realization/soldering rule",
    ]
    for token in required:
        assert token in report, token
    forbidden = [
        "the physical transverse torus is derived",
        "the carrier is derived",
        "bootstrap selects the spin lift",
        "the finite cell selects s3",
        "udt derives a quantum spinor",
    ]
    lower = report.lower()
    for token in forbidden:
        assert token not in lower, token


def independent_exact() -> dict[str, str]:
    p, alpha, eta, delta, rho = sp.symbols("p alpha eta delta rho", real=True)
    t = sp.symbols("t", positive=True)
    I = sp.I
    K = sp.Matrix([[0, 1], [1, 0]])
    P = sp.diag(sp.exp(-p), sp.exp(p))
    assert sp.simplify(P.T * K * P - K) == sp.zeros(2)

    x0, x1, x2, x3 = sp.symbols("x0 x1 x2 x3", real=True)
    X = sp.Matrix([[x0 + x3, x1 - I * x2], [x1 + I * x2, x0 - x3]])
    A = sp.diag(sp.exp(-p), sp.exp(p))
    transformed = sp.simplify(A * X * A.conjugate().T)
    assert sp.simplify(transformed.det() - X.det()) == 0
    assert sp.simplify(transformed[0, 1] - X[0, 1]) == 0
    assert sp.simplify(transformed[1, 0] - X[1, 0]) == 0

    twisted = sp.diag(sp.exp((-1 + I * alpha) * p), sp.exp((1 - I * alpha) * p))
    assert sp.simplify(twisted.det() - 1) == 0
    assert sp.simplify(twisted.conjugate().T * twisted - sp.diag(sp.exp(-2 * p), sp.exp(2 * p))) == sp.zeros(2)

    u, v = sp.symbols("u v", real=True)
    tracefree = sp.Matrix([[u, v], [v, -u]])
    rotation = sp.Matrix([[0, -1], [1, 0]])
    rotation45 = sp.sqrt(2) / 2 * sp.Matrix([[1, -1], [1, 1]])
    equations = list(rotation.T * tracefree * rotation - tracefree) + list(rotation45.T * tracefree * rotation45 - tracefree)
    assert sp.solve(equations, (u, v), dict=True) == [{u: 0, v: 0}]

    orbit = sp.diag(1 / (1 + t**2), t**2 / (1 + t**2))
    normalized = sp.simplify(orbit / (t / (1 + t**2)))
    assert sp.simplify(normalized - sp.diag(1 / t, t)) == sp.zeros(2)
    assert sp.simplify(normalized.subs(t, sp.exp(2 * p)) - sp.diag(sp.exp(-2 * p), sp.exp(2 * p))) == sp.zeros(2)
    seed_a, seed_b = sp.symbols("seed_a seed_b", positive=True)
    generic_seed = sp.diag(seed_a * sp.exp(-2 * p) / seed_b, seed_b * sp.exp(2 * p) / seed_a)
    assert sp.solve(sp.Eq(generic_seed[0, 0].subs(p, 0), 1), seed_a, dict=True) == [{seed_a: seed_b}]
    assert sp.sqrt(2).is_irrational is True
    assert (-1 / sp.sqrt(2)).is_irrational is True

    n = sp.Matrix([2 * t * sp.cos(delta) / (1 + t**2), 2 * t * sp.sin(delta) / (1 + t**2), (1 - t**2) / (1 + t**2)])
    assert sp.simplify((n.T * n)[0] - 1) == 0
    nphi = n.subs(t, sp.exp(2 * p))
    expected = sp.Matrix([sp.sech(2 * p) * sp.cos(delta), sp.sech(2 * p) * sp.sin(delta), -sp.tanh(2 * p)])
    assert all(sp.simplify(entry.rewrite(sp.exp)) == 0 for entry in nphi - expected)

    fs = 4 * (1 + rho**2) ** 2 / (1 + 4 * rho**2) ** 2
    assert sp.simplify(fs.subs(rho, 1) - sp.Rational(16, 25)) == 0
    density = -sp.sin(2 * eta)
    integral = sp.integrate(density, (eta, 0, sp.pi / 2)) * (2 * sp.pi) ** 2
    assert sp.simplify(integral + 4 * sp.pi**2) == 0
    return {
        "founding_pairing": "PASS",
        "induced_vector_transverse_invariance": "PASS",
        "phase_twisted_embedding": "PASS",
        "so2_equivariance": "PASS",
        "normalized_orbit": "PASS",
        "balanced_reference_ray": "PASS",
        "irrational_torus_nonperiodicity": "PASS",
        "cp1_unit_sphere": "PASS",
        "fubini_study_nonisometry": "PASS",
        "hopf_integral": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    package = pathlib.Path(__file__).resolve().parent
    repo = package.parent

    validate_prereg(repo, package)
    inventory = rows(package / "SOURCE_INVENTORY.tsv")
    candidates = rows(package / "CANDIDATE_FAMILY.tsv")
    ledger = rows(package / "STATUS_LEDGER.tsv")
    algebra = json.loads((package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    report = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    validate_sources(repo, inventory)
    validate_source_semantics(repo)
    validate_candidates(candidates)
    validate_ledger(ledger)
    validate_algebra(algebra)
    validate_report(report)
    independent = independent_exact()

    with tempfile.TemporaryDirectory(prefix="transverse_selector_replay_") as temp:
        replay = pathlib.Path(temp) / "DERIVATION_RESULT.json"
        process = subprocess.run(
            [sys.executable, str(package / "derive_transverse_reciprocal_selector.py"), "--output", str(replay)],
            cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False,
        )
        assert process.returncode == 0, process.stderr
        assert process.stderr == ""
        assert replay.read_bytes() == (package / "DERIVATION_RESULT.json").read_bytes()

    catches: list[dict[str, str]] = []
    ledger_mutations = [
        ("R02", "PHYSICAL_TRANSVERSE_PAIR_DERIVED", "direct_extension_promotion"),
        ("R03", "NONZERO_SCALAR_SHEAR", "so2_obstruction_removed"),
        ("R04", "TWO_LINES_SELECTED", "hodge_area_promoted"),
        ("R06", "PERIODS_LOCALLY_DERIVED", "global_periodicity_promoted"),
        ("R07", "EXCLUDED", "finite_disk_counterfamily_deleted"),
        ("R08", "EXCLUDED", "finite_sphere_counterfamily_deleted"),
        ("R10", "FOUNDATION_LEVEL_SPIN_REALIZATION", "spin_embedding_promotion"),
        ("R11", "PHYSICAL_SPATIAL_S3", "representation_s3_promoted"),
        ("R13", "TWO_PHYSICAL_SPATIAL_CIRCLES", "phase_roles_conflated"),
        ("R16", "GLOBAL_SPIN_DERIVED", "global_spin_promotion"),
        ("R17", "SOLDERING_DERIVED", "soldering_promotion"),
        ("R19", "BOOTSTRAP_SELECTS_SPIN_LIFT", "bootstrap_scope_inflation"),
        ("R20", "ACTIVATED", "cap_gate_activated"),
        ("R21", "ACTION_DERIVED", "action_promotion"),
    ]
    for claim_id, status, name in ledger_mutations:
        changed = copy.deepcopy(ledger)
        next(row for row in changed if row["claim_id"] == claim_id)["status"] = status
        catches.append(reject(name, lambda data=changed: validate_ledger(data)))

    missing = [row for row in candidates if row["family_id"] != "F04"]
    catches.append(reject("missing_global_counterfamily", lambda: validate_candidates(missing)))
    duplicate = copy.deepcopy(candidates) + [copy.deepcopy(candidates[0])]
    catches.append(reject("duplicate_candidate", lambda: validate_candidates(duplicate)))
    promoted_spin = copy.deepcopy(candidates)
    next(row for row in promoted_spin if row["family_id"] == "F05")["physical_spatial_status"] = "PHYSICAL_TORUS_DERIVED"
    catches.append(reject("representation_promoted_to_spacetime", lambda: validate_candidates(promoted_spin)))
    lost_irrational_family = copy.deepcopy(candidates)
    next(row for row in lost_irrational_family if row["family_id"] == "F04")["counterexample_or_limit"] = "all reciprocal torus axes close"
    catches.append(reject("irrational_torus_counterexample_removed", lambda: validate_candidates(lost_irrational_family)))

    lost_irrational_ledger = copy.deepcopy(ledger)
    next(row for row in lost_irrational_ledger if row["claim_id"] == "R06")["basis"] = "all reciprocal torus axes close"
    catches.append(reject("irrational_torus_basis_removed", lambda: validate_ledger(lost_irrational_ledger)))
    lost_balanced_reference = copy.deepcopy(ledger)
    next(row for row in lost_balanced_reference if row["claim_id"] == "R14")["dependency_or_limit"] = "no reference-ray premise"
    catches.append(reject("balanced_reference_premise_removed", lambda: validate_ledger(lost_balanced_reference)))

    bad_source = copy.deepcopy(inventory)
    bad_source[0]["sha256"] = "0" * 64
    catches.append(reject("source_hash_mutation", lambda: validate_sources(repo, bad_source)))
    cold_path = "UDT_NATIVE_ACTION_COLD_PACKET.md"
    cold = source(repo, cold_path)
    catches.append(reject(
        "transverse_open_disclosure_removed",
        lambda: validate_source_semantics(repo, {cold_path: cold.replace("the transverse spatial block or full time-live geometry", "the selected transverse spatial spin torus")}),
    ))
    bootstrap_path = "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md"
    bootstrap = source(repo, bootstrap_path)
    catches.append(reject(
        "bootstrap_contradiction_rejected",
        lambda: validate_source_semantics(repo, {bootstrap_path: bootstrap + "\nbootstrap selects the spin lift\n"}),
    ))

    bad_algebra = copy.deepcopy(algebra)
    bad_algebra["classification"]["physical_transverse_spatial_periodicity"] = "DERIVED"
    catches.append(reject("algebra_physical_promotion", lambda: validate_algebra(bad_algebra)))
    bad_algebra = copy.deepcopy(algebra)
    bad_algebra["topological_classification"]["common_phase_role"] = "SECOND_PHYSICAL_SPATIAL_DIRECTION"
    catches.append(reject("algebra_common_phase_conflation", lambda: validate_algebra(bad_algebra)))
    bad_algebra = copy.deepcopy(algebra)
    bad_algebra["classification"]["finite_cell_cap_gate"] = "ACTIVATED"
    catches.append(reject("algebra_cap_activation", lambda: validate_algebra(bad_algebra)))
    bad_report = report.replace("not a random resemblance", "the physical transverse torus is derived")
    catches.append(reject("report_overclaim", lambda: validate_report(bad_report)))

    result = {
        "status": "PASS_SELF_CONSISTENCY",
        "verification_class": "BASE_PINNED_SOURCES; BYTE_IDENTICAL_REPLAY; INDEPENDENT_SPIN_PROJECTIVE_ALGEBRA; CATCH_PROOFS; FRESH_SEMANTIC_REVIEW_SEPARATE",
        "base": BASE,
        "preregistration_commit": PREREG,
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "source_rows": len(inventory),
        "candidate_rows": len(candidates),
        "ledger_rows": len(ledger),
        "algebra_checks": algebra["check_count"],
        "derivation_replay": "PASS_BYTE_IDENTICAL",
        "independent_exact": independent,
        "catch_proof_count": len(catches),
        "catch_proofs": catches,
        "preregistration_sha256": sha((package / "PREREGISTRATION.md").read_bytes()),
        "source_inventory_sha256": sha((package / "SOURCE_INVENTORY.tsv").read_bytes()),
        "derivation_result_sha256": sha((package / "DERIVATION_RESULT.json").read_bytes()),
        "candidate_family_sha256": sha((package / "CANDIDATE_FAMILY.tsv").read_bytes()),
        "status_ledger_sha256": sha((package / "STATUS_LEDGER.tsv").read_bytes()),
        "audit_report_sha256": sha((package / "AUDIT_REPORT.md").read_bytes()),
        "verdict": VERDICT,
    }
    pathlib.Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"VERIFIER PASS sources={len(inventory)}/13 candidates={len(candidates)}/7 "
        f"ledger={len(ledger)}/22 algebra={algebra['check_count']}/40 catches={len(catches)}/{len(catches)}"
    )
    print(VERDICT)


if __name__ == "__main__":
    main()
