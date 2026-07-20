#!/usr/bin/env python3
"""Independent verifier for the direction–magnitude correction."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "86874cb8482fc2a29bfc53251c3bcf4160eda4ed"
PRIOR = ROOT / "projective_position_join_audit_2026-07-19"
PRIOR_MANIFEST_SHA = "bde786c168a2bf552a9720afa66a3615e66c0d63ffcfb78af680c88813198a84"
RESULT = HERE / "DERIVATION_RESULT.json"
VERIFY = HERE / "VERIFICATION_RESULT.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(data: dict) -> None:
    require(data["schema"] == "udt-projective-direction-magnitude-correction-1.0", "schema changed")
    require(len(data["checks"]) == 39 and all(value == "PASS" for value in data["checks"].values()), "primary check census/failure")
    objects = data["conceptual_objects"]
    require(objects["ordered_comparison"]["classification"].endswith("NOT_DISTANCE"), "ordered comparison promoted to distance")
    require(objects["separation"]["classification"] == "CANDIDATE_NOT_A_DERIVED_GLOBAL_METRIC_DISTANCE", "magnitude candidate promoted")
    require(objects["separation"]["properties"] == "nonnegative symmetric and zero at coincidence", "separation symmetry changed")
    require("ANGULAR_SECTOR" in objects["direction"]["classification"], "angular direction dropped")
    require(objects["direction"]["reversal"] == "n_hat -> -n_hat while rho is unchanged", "direction reversal changed magnitude")
    require(objects["projective_imbalance"]["classification"] == "ORIENTED_PROJECTIVE_COORDINATE_NOT_PHYSICAL_DISTANCE", "projective chart promoted")
    require(objects["projective_imbalance"]["readout_status"].startswith("radial chart remains OPEN"), "radial chart selected")
    clock = objects["clock_scalar"]
    require(clock["classification"].startswith("UNCONDITIONAL_NATIVE_SCALAR_OPEN"), "unconditional clock scalar promoted")
    require("ordered observer-comparison reversal" in clock["ordered_weights"], "ordered comparison distinction lost")
    require(clock["conditional_status"] == "CONDITIONAL_IN_THE_CHOSEN_LOCAL_LORENTZIAN_TEMPORAL_SLOT", "chosen-slot scope changed")
    require("exp(-rho)" in clock["conditional_chosen_slot"], "chosen-slot clock branch lost")
    require(data["coframe_regrade"]["does_not_follow"] == "inverse ordered comparison is not a physical clock-speed-up theorem", "inverse comparison promoted")
    require(data["seal_regrade"]["separation_candidate"] == "rho_candidate(S,O)=abs(Phi(O))", "seal magnitude correction lost")
    adjudication = data["adjudication"]
    require(adjudication["physical_signed_position"].startswith("WITHDRAWN"), "signed distance retained")
    require(adjudication["negative_observer_distance"] == "REJECTED", "negative distance admitted")
    require(adjudication["direction_induced_clock_speedup"].startswith("REJECTED"), "direction speed-up admitted")
    require(adjudication["global_distance"] == "OPEN", "global distance promoted")
    require(adjudication["scalar_clock_dilation"] == "CONDITIONAL_IN_CHOSEN_TEMPORAL_SLOT; UNCONDITIONAL_NATIVE_READOUT_OPEN", "clock scope changed")
    require(data["revised_missing_maps"]["status"] == "ALL_OPEN; IDENTIFIED_NOT_ADOPTED", "missing maps adopted")


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation unexpectedly passed: {name}")


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""

    before = sha256(RESULT)
    replay = subprocess.run(
        [sys.executable, "-B", str(HERE / "derive_direction_magnitude.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=180,
        check=False,
    )
    require(replay.returncode == 0 and not replay.stderr, f"primary replay failed: {replay.stderr}")
    require(sha256(RESULT) == before, "primary replay changed result")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    validate(data)
    checks["deterministic_primary_replay_and_contract"] = "PASS"

    # Independent observer-swap and magnitude calculation.
    a, b = sp.symbols("a b", real=True)
    ordered = a - b
    require(sp.simplify(ordered + ordered.xreplace({a: b, b: a})) == 0, "independent antisymmetry failed")
    require(sp.simplify(sp.Abs(ordered) - sp.Abs(ordered.xreplace({a: b, b: a}))) == 0, "independent magnitude symmetry failed")
    checks["independent_ordered_vs_nonnegative_separation"] = "PASS"

    # Radial difference alone cannot be a complete 3D distance: a transverse
    # displacement can have zero depth difference and nonzero metric length.
    dphi, dtheta, L, H = sp.symbols("dphi dtheta L H", real=True)
    length_squared = L**2 * dphi**2 + H * dtheta**2
    witness = length_squared.subs({dphi: 0, dtheta: 1, L: 1, H: 1})
    require(witness == 1 and sp.Abs(dphi).subs(dphi, 0) == 0, "independent angular-distance witness failed")
    checks["independent_complete_metric_requires_angular_path_data"] = "PASS"

    # Independent direction vector reversal.
    r = sp.symbols("r", nonnegative=True)
    nx, ny, nz = sp.symbols("nx ny nz", real=True)
    vector = r * sp.Matrix([nx, ny, nz])
    reversed_vector = r * sp.Matrix([-nx, -ny, -nz])
    require(reversed_vector == -vector, "independent direction reversal failed")
    require(sp.simplify(reversed_vector.dot(reversed_vector) - vector.dot(vector)) == 0, "independent magnitude reversal failed")
    checks["independent_direction_magnitude_split"] = "PASS"

    # A third scalar readout, not used by the primary derivation.
    U, V, s = sp.symbols("U V s", positive=True)
    clock_alt = 2 * U * V / (U**2 + V**2)
    require(sp.simplify(clock_alt.subs({U: s * U, V: s * V}, simultaneous=True) - clock_alt) == 0, "independent clock CSN failed")
    require(sp.simplify(clock_alt.xreplace({U: V, V: U}) - clock_alt) == 0, "independent clock exchange failed")
    require(clock_alt.subs({U: 1, V: 1}) == 1, "independent clock normalization failed")
    require(clock_alt.subs({U: sp.Rational(1, 2), V: 2}) == sp.Rational(8, 17), "independent clock witness failed")
    depth = sp.symbols("depth", real=True)
    depth_alt = sp.sech(2 * depth)
    require(sp.simplify(depth_alt.subs(depth, -depth) - depth_alt) == 0, "independent clock direction evenness failed")
    checks["independent_third_clock_counterexample"] = "PASS"

    # Prior package is historical evidence and must remain byte-identical.
    require(sha256(PRIOR / "SHA256SUMS.txt") == PRIOR_MANIFEST_SHA, "prior manifest identity changed")
    prior_replay = subprocess.run(
        ["sha256sum", "--check", "SHA256SUMS.txt"],
        cwd=PRIOR,
        text=True,
        capture_output=True,
        timeout=90,
        check=False,
    )
    require(prior_replay.returncode == 0 and "FAILED" not in prior_replay.stdout, "prior package replay failed")
    checks["prior_package_byte_identity"] = "PASS"

    inventory_before = sha256(HERE / "SOURCE_INVENTORY.tsv")
    inventory_run = subprocess.run(
        [sys.executable, "-B", str(HERE / "build_source_inventory.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=90,
        check=False,
    )
    require(inventory_run.returncode == 0 and not inventory_run.stderr, "source replay failed")
    require(sha256(HERE / "SOURCE_INVENTORY.tsv") == inventory_before, "source inventory changed")
    require(len(read_tsv(HERE / "SOURCE_INVENTORY.tsv")) == 12, "source census mismatch")
    checks["source_inventory_replay"] = "PASS"

    overlay = read_tsv(HERE / "CORRECTION_OVERLAY.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(len(overlay) == 18 and len({row["id"] for row in overlay}) == 18, "overlay coverage mismatch")
    require(len(statuses) == 12 and len({row["id"] for row in statuses}) == 12, "status coverage mismatch")
    require(next(row for row in overlay if row["id"] == "C01")["correction_disposition"] == "WITHDRAWN", "signed-position overlay lost")
    require(next(row for row in statuses if row["id"] == "S10")["status"] == "OPEN", "clock status promoted")
    checks["correction_ledger_coverage"] = "PASS"

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    flat = " ".join(report.split()).replace("*", "").casefold()
    for phrase in (
        "The prior phrase “physical signed position” was therefore a category error",
        "an ordered reciprocal comparison",
        "magnitude and direction separate",
        "Two operations that had been conflated must be separated",
        "the conditional clock factor `exp(-rho)`",
        "These are countermodels to unrestricted uniqueness, not proposed UDT clock laws",
        "a bounded coordinate need not equal proper length",
        "The former single “projective-position join” splits into three distinct questions",
        "The prior package remains byte-identical",
    ):
        require(phrase.casefold() in flat, f"report disclosure missing: {phrase}")
    checks["report_contract"] = "PASS"

    changed = subprocess.check_output(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines()
    forbidden = {"LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md", "CANON.md"}
    require(not forbidden.intersection(changed), f"forbidden controls changed: {forbidden.intersection(changed)}")
    checks["no_control_canon_or_prior_edits"] = "PASS"

    mutation = copy.deepcopy(data)
    mutation["conceptual_objects"]["ordered_comparison"]["classification"] = "PHYSICAL_DISTANCE"
    expect_failure("signed_comparison_called_distance", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["conceptual_objects"]["separation"]["classification"] = "DERIVED_GLOBAL_DISTANCE"
    expect_failure("magnitude_promoted_to_global_distance", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["conceptual_objects"]["direction"]["classification"] = "SIGN_ALONE"
    expect_failure("angular_direction_dropped", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["conceptual_objects"]["direction"]["reversal"] = "n_hat -> -n_hat and rho -> -rho"
    expect_failure("direction_reversal_changed_distance_magnitude", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["conceptual_objects"]["projective_imbalance"]["classification"] = "PHYSICAL_DISTANCE"
    expect_failure("projective_chart_promoted_to_distance", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["conceptual_objects"]["clock_scalar"]["classification"] = "DERIVED_SECH"
    expect_failure("clock_candidate_promoted_without_selector", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["conceptual_objects"]["clock_scalar"]["ordered_weights"] = "angular reversal and observer exchange are identical"
    expect_failure("ordered_weight_called_clock_scalar", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["conceptual_objects"]["clock_scalar"]["conditional_status"] = "UNCONDITIONAL"
    expect_failure("chosen_temporal_slot_scope_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["coframe_regrade"]["does_not_follow"] = "inverse comparison means clock speed-up"
    expect_failure("inverse_comparison_promoted_to_speedup", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["seal_regrade"]["separation_candidate"] = "rho_candidate(S,O)=0=X_max"
    expect_failure("seal_identified_with_coincidence_or_endpoint", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["revised_missing_maps"]["status"] = "ADOPTED"
    expect_failure("open_maps_adopted", lambda: validate(mutation), catches)
    expect_failure(
        "prior_package_mutation_rejected",
        lambda: require(sha256(PRIOR / "SHA256SUMS.txt") == "0" * 64, "prior package mutation"),
        catches,
    )

    output = {
        "schema": "udt-projective-direction-magnitude-verification-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "checks": checks,
        "catch_proofs": catches,
        "independent_witnesses": {
            "observer_swap": "delta flips sign while abs(delta) is invariant",
            "angular_path": "dphi=0,dtheta=1,L=H=1 gives metric length squared 1 while radial difference is zero",
            "clock_counterexample": "2uv/(u^2+v^2)=sech(2delta)",
            "clock_witness_u_half_v_two": "8/17",
            "prior_manifest_sha256": PRIOR_MANIFEST_SHA,
        },
        "result": "PASS",
    }
    VERIFY.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
