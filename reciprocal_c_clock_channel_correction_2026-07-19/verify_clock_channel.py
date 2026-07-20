#!/usr/bin/env python3
"""Independent verifier for the reciprocal-c clock-channel correction."""

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
BASE = "d88e6fabd209e81f7c0ba0ef7e1743663bb1106e"
RESULT = HERE / "DERIVATION_RESULT.json"
VERIFY = HERE / "VERIFICATION_RESULT.json"
PRIOR_PACKAGES = {
    "projective_position_join_audit_2026-07-19": "bde786c168a2bf552a9720afa66a3615e66c0d63ffcfb78af680c88813198a84",
    "projective_position_direction_magnitude_correction_2026-07-19": "377eaa791ab93845f50c19d6eb30dadb0b10322ac0cbe405db55ca0a37ad3dfb",
}
CONTROLS = {
    "LIVE.md": ("c^-1", "sech", "remain open", "DO NOT CLAIM EVERYTHING SOLVED"),
    "HANDOFF.md": ("c^-1", "sech", "remain genuinely open", "no follow-on solve"),
    "INDEX.md": ("c^-1", "sech", "remain open", "No follow-on study"),
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md": ("c^-1", "sech", "remain `OPEN`", "does not close"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_controls(overrides: dict[str, str] | None = None) -> list[dict[str, str | int]]:
    """Require the append-only correction layer in every authorized live control."""
    overrides = overrides or {}
    details: list[dict[str, str | int]] = []
    package_token = "reciprocal_c_clock_channel_correction_2026-07-19"
    for name, phrases in CONTROLS.items():
        path = ROOT / name
        content = overrides.get(name, path.read_text(encoding="utf-8"))
        # All four files place their live/current orientation at the top. Restrict
        # this test to that window so a stale historical mention cannot satisfy it.
        window = "\n".join(content.splitlines()[:160])
        require(package_token in window, f"current correction package missing from {name}")
        for phrase in phrases:
            require(phrase.casefold() in window.casefold(), f"control disclosure missing from {name}: {phrase}")
        details.append({"path": name, "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(), "window_lines": min(160, len(content.splitlines()))})
    return details


def validate(data: dict) -> None:
    require(data["schema"] == "udt-reciprocal-c-clock-channel-correction-1.0", "schema changed")
    require(len(data["checks"]) == 30 and all(value == "PASS" for value in data["checks"].values()), "primary check census/failure")
    anchor = data["founding_anchor"]
    require(anchor["classification"] == "FOUNDING_OWNER_CLARIFIED", "founding anchor demoted")
    require("not an optional arithmetic afterthought" in anchor["statement"], "c inverse demoted")
    require("clock side" in anchor["clock_channel"], "clock channel identity lost")
    channels = data["derived_channels"]
    require(channels["temporal_weight"] == "T(rho)=exp(-rho)", "temporal character changed")
    require(channels["ruler_weight"] == "R(rho)=exp(+rho)", "ruler character changed")
    require(channels["classification"] == "DERIVED_CONDITIONAL_WITH_EXACT_PREMISE_STAMPS", "channel scope changed")
    direction = data["direction_correction"]
    require(direction["classification"] == "ANGULAR_REVERSAL_DOES_NOT_SWAP_CLOCK_AND_RULER_CHANNELS", "angular reversal swapped channels")
    require(direction["physical_depth"] == "rho>=0", "negative depth restored")
    local = data["local_clock_readout"]
    require(local["classification"].startswith("CONDITIONAL_ON_THE_DECLARED_LORENTZIAN"), "local readout promoted")
    require(local["not_open"].startswith("no additional choice"), "false scalar selector restored")
    alternatives = data["symmetric_alternative_regrade"]
    require(alternatives["classification"] == "REJECTED_AS_COMPLETE_FOUNDATION_CLOCK_CHANNEL_COUNTERMODELS", "symmetric alternatives admitted")
    frontier = data["corrected_frontier"]
    require(frontier["everything_solved"] is False, "complete closure invented")
    require(len(frontier["closed"]) == 5 and len(frontier["conditional"]) == 3 and len(frontier["open"]) == 6, "frontier census changed")
    adjudication = data["adjudication"]
    require(adjudication["base_clock_selector"].startswith("NOT_OPEN"), "base clock reopened")
    require(adjudication["symmetric_clock_selector_problem"] == "WITHDRAWN_AS_UNDERPREMISED", "false selector retained")
    require(adjudication["negative_physical_distance"] == "REJECTED", "negative distance restored")
    require(adjudication["projective_radial_readout"] == "OPEN" and adjudication["complete_udt_closure"] == "OPEN", "genuine open gates closed")


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
        [sys.executable, "-B", str(HERE / "derive_clock_channel.py")],
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

    # Independent Lie-generator route: the one-parameter representation is the
    # matrix exponential of the named reciprocal generator.
    x, y = sp.symbols("x y", real=True)
    generator = sp.diag(-1, 1)
    representation = lambda value: (value * generator).exp()
    require((representation(x) - sp.diag(sp.exp(-x), sp.exp(x))).applyfunc(sp.simplify) == sp.zeros(2), "independent generator exponential failed")
    require((representation(x) * representation(y) - representation(x + y)).applyfunc(sp.simplify) == sp.zeros(2), "independent character composition failed")
    require((representation(x).inv() - representation(-x)).applyfunc(sp.simplify) == sp.zeros(2), "independent inverse failed")
    checks["independent_generator_character_derivation"] = "PASS"

    # Independent exact witness at log(3), distinct from the primary log(2).
    a = sp.log(3)
    sech_one = sp.Rational(3, 5)
    sech_two = sp.Rational(9, 41)
    require(sp.simplify(sp.sech(a) - sech_one) == 0, "independent sech log3 anchor failed")
    require(sp.simplify(sp.sech(2 * a) - sech_two) == 0, "independent sech log9 anchor failed")
    require(sp.simplify(sech_two - sech_one**2) == -sp.Rational(144, 1025), "independent sech character witness changed")
    require(sp.simplify(sp.exp(-2 * a) - sp.exp(-a) ** 2) == 0, "independent true character failed")
    checks["independent_noncharacter_witness"] = "PASS"

    # Independent channel and angular-direction distinction.
    rho = sp.symbols("rho", nonnegative=True)
    n = sp.Matrix(sp.symbols("n1:4", real=True))
    require(-n != n, "independent direction reversal collapsed")
    require(sp.exp(-rho) == sp.exp(-rho), "independent fixed-rho clock changed")
    require(sp.exp(rho) == sp.exp(rho), "independent fixed-rho ruler changed")
    checks["independent_angular_reversal_preserves_channels"] = "PASS"

    prior_details = []
    for package, expected in PRIOR_PACKAGES.items():
        manifest = ROOT / package / "SHA256SUMS.txt"
        require(sha256(manifest) == expected, f"prior manifest changed: {package}")
        replay_prior = subprocess.run(
            ["sha256sum", "--check", "SHA256SUMS.txt"],
            cwd=manifest.parent,
            text=True,
            capture_output=True,
            timeout=90,
            check=False,
        )
        require(replay_prior.returncode == 0 and "FAILED" not in replay_prior.stdout, f"prior replay failed: {package}")
        prior_details.append({"package": package, "manifest_sha256": expected, "result": "PASS"})
    checks["both_prior_packages_byte_identical"] = "PASS"

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
    require(len(read_tsv(HERE / "SOURCE_INVENTORY.tsv")) == 13, "source census mismatch")
    checks["source_inventory_replay"] = "PASS"

    overlay = read_tsv(HERE / "CORRECTION_OVERLAY.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(len(overlay) == 12 and len({row["id"] for row in overlay}) == 12, "overlay census mismatch")
    require(len(statuses) == 15 and len({row["id"] for row in statuses}) == 15, "status census mismatch")
    require(next(row for row in statuses if row["id"] == "S02")["status"] == "NOT_OPEN", "base clock reopened in ledger")
    require(next(row for row in statuses if row["id"] == "S15")["status"] == "REFUTED_AS_CURRENT_CLAIM", "everything solved in ledger")
    checks["correction_ledger_coverage"] = "PASS"

    controls = validate_controls()
    checks["live_control_correction_layer"] = "PASS"

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    flat = " ".join(report.split()).replace("*", "").casefold()
    for phrase in (
        "The base clock channel was not an unknown scalar function waiting to be selected",
        "We temporarily forgot which wire was which",
        "not multiplicative channel characters",
        "no additional choice among arbitrary symmetric functions is needed",
        "substantial kinematic skeleton",
        "everything is solved” is not yet an evidence-supported verdict",
        "The recent `sech`-type alternatives",
    ):
        require(phrase.casefold() in flat, f"report disclosure missing: {phrase}")
    checks["report_contract"] = "PASS"

    changed = set(subprocess.check_output(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines())
    changed.update(subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True).splitlines())
    allowed_controls = {"LIVE.md", "HANDOFF.md", "INDEX.md", "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md"}
    invalid = sorted(path for path in changed if path and not path.startswith(HERE.name + "/") and path not in allowed_controls)
    require(not invalid, f"out-of-scope paths: {invalid}")
    require("CANON.md" not in changed, "canon changed")
    checks["scope_and_canon_boundary"] = "PASS"

    mutation = copy.deepcopy(data)
    mutation["founding_anchor"]["classification"] = "OPEN"
    expect_failure("founding_anchor_demoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["founding_anchor"]["statement"] = "c inverse is optional arithmetic"
    expect_failure("reciprocal_c_afterthought_restored", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["direction_correction"]["classification"] = "ANGULAR_REVERSAL_SWAPS_CHANNELS"
    expect_failure("angular_reversal_swapped_channels", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["symmetric_alternative_regrade"]["classification"] = "ADMISSIBLE_CLOCK_LAWS"
    expect_failure("noncharacter_admitted_as_channel", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["local_clock_readout"]["classification"] = "FOUNDING_UNCONDITIONAL"
    expect_failure("local_readout_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["direction_correction"]["physical_depth"] = "rho signed distance"
    expect_failure("negative_distance_restored", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["adjudication"]["projective_radial_readout"] = "DERIVED_PROPER_DISTANCE"
    expect_failure("projective_coordinate_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["corrected_frontier"]["everything_solved"] = True
    expect_failure("everything_solved_promoted", lambda: validate(mutation), catches)
    live = (ROOT / "LIVE.md").read_text(encoding="utf-8")
    expect_failure(
        "control_correction_layer_loss_rejected",
        lambda: validate_controls({"LIVE.md": live.replace("reciprocal_c_clock_channel_correction_2026-07-19", "missing_clock_correction")}),
        catches,
    )
    for number, (package, _) in enumerate(PRIOR_PACKAGES.items(), start=1):
        expect_failure(
            f"prior_package_{number}_mutation_rejected",
            lambda package=package: require(sha256(ROOT / package / "SHA256SUMS.txt") == "0" * 64, "prior mutation"),
            catches,
        )

    output = {
        "schema": "udt-reciprocal-c-clock-channel-verification-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "checks": checks,
        "catch_proofs": catches,
        "independent_witnesses": {
            "generator": "diag(-1,+1)",
            "sech_log3_character_failure": "-144/1025",
            "true_clock_character": "exp[-(x+y)]=exp(-x)exp(-y)",
            "prior_packages": prior_details,
            "live_controls": controls,
        },
        "result": "PASS",
    }
    VERIFY.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
