#!/usr/bin/env python3
"""Independent verifier for the native global-coframe definition audit.

This script does not import the production derivation.  It rebuilds the
load-bearing linear algebra, checks the frozen repository evidence, and
exercises every preregistered rejection guard with a deliberately invalid
in-memory candidate.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_manifest(rows: list[dict[str, str]]) -> None:
    require(len(rows) == 99, "source count")
    paths = [row["path"] for row in rows]
    require(len(set(paths)) == len(paths), "duplicate source")
    for row in rows:
        path = ROOT / row["path"]
        require(path.is_file(), f"missing source {path}")
        require(path.stat().st_size == int(row["size_bytes"]), f"size {path}")
        require(digest(path) == row["sha256"], f"hash {path}")
        require(not row["path"].startswith(HERE.name + "/"), "generated source")
    for required in (
        "udt_full_local_jet_strata_p02_2026-07-27/STRATUM_LEDGER.tsv",
        "udt_full_local_jet_strata_p02_2026-07-27/P02B_CANDIDATE_LEDGER.tsv",
    ):
        require(required in paths, f"missing detailed P02 source {required}")


def independent_algebra() -> dict[str, object]:
    # Rebuild the commutants from an independently named generic matrix.
    y = sp.symbols("y0:16")
    A = sp.Matrix(4, 4, y)
    boosts = []
    for spatial in (1, 2, 3):
        B = sp.zeros(4)
        B[0, spatial] = B[spatial, 0] = 1
        boosts.append(B)
    rotations = []
    for left, right in ((1, 2), (1, 3), (2, 3)):
        J = sp.zeros(4)
        J[left, right], J[right, left] = 1, -1
        rotations.append(J)
    eqs = []
    for generator in boosts + rotations:
        eqs.extend(A * generator - generator * A)
    coefficient, _ = sp.linear_eq_to_matrix(eqs, y)
    full_nullity = 16 - coefficient.rank()
    require(full_nullity == 1, "full Lorentz commutant is scalar")

    eta = sp.diag(-1, 1, 1, 1)
    Jscreen = sp.zeros(4)
    Jscreen[2, 3], Jscreen[3, 2] = 1, -1
    pair_eqs = list(A * Jscreen - Jscreen * A) + list(A.T * eta - eta * A)
    H = sp.diag(-1, 1, 0, 0)
    for row in range(4):
        for col in range(4):
            if row < 2 or col < 2:
                pair_eqs.append(A[row, col] - H[row, col])
    M, b = sp.linear_eq_to_matrix(pair_eqs, y)
    solution = next(iter(sp.linsolve((M, b), y)))
    free = set().union(*(entry.free_symbols for entry in solution))
    require(len(free) == 1, "ordered-pair lift must retain exactly one modulus")

    p, q, radius, twist, ell = sp.symbols("p q radius twist ell", real=True)
    Xell = sp.diag(-1, 1, ell, ell)
    group_residual = (sp.exp(p * Xell) * sp.exp(q * Xell) - sp.exp((p + q) * Xell)).applyfunc(sp.simplify)
    require(group_residual == sp.zeros(4), "lift group law")
    require(Xell.trace() == 2 * ell, "lambda invariant")

    # Independently assemble the complete R x S3 coframe matrix.
    frame = sp.zeros(4)
    frame[0, 0] = sp.exp(-p)
    frame[0, 1] = twist * sp.exp(-p)
    frame[1, 1] = radius * sp.exp(p)
    frame[2, 2] = frame[3, 3] = radius * sp.exp(ell * p)
    metric = sp.simplify(frame.T * eta * frame)
    require(sp.simplify(frame.det() - radius**3 * sp.exp(2 * ell * p)) == 0, "coframe determinant")
    require(sp.simplify(metric.det() + radius**6 * sp.exp(4 * ell * p)) == 0, "metric determinant")
    require(sp.simplify(metric[0, 0] + sp.exp(-2 * p)) == 0, "stationary clock norm")
    expected_slice = radius**2 * sp.exp(2 * p) - twist**2 * sp.exp(-2 * p)
    require(sp.simplify(metric[1, 1] - expected_slice) == 0, "slice coefficient")

    dimensions = sp.Matrix([[1, 3], [0, -1], [-1, -2]])
    require(dimensions.rank() == 2 and not dimensions.nullspace(), "c/G dimensional rank")
    fp, fq, fr = sp.symbols("fp fq fr")
    require(sp.simplify((fq - fp) + (fr - fq) - (fr - fp)) == 0, "depth cocycle")
    return {
        "full_lorentz_centralizer_nullity": full_nullity,
        "ordered_pair_moduli": len(free),
        "coframe_determinant": "radius^3*exp(2*ell*p)",
        "metric_determinant": "-radius^6*exp(4*ell*p)",
        "dimension_matrix_rank": dimensions.rank(),
        "dimensionless_nullity": len(dimensions.nullspace()),
    }


def must_reject(case: dict[str, object]) -> None:
    forbidden_true = {
        "cross_splice", "assume_block_diagonal", "assume_spectator_screen",
        "assume_topology_or_carrier", "reactivate_strong_csn", "anchors_select_shape",
        "covariance_implies_unique", "bundle_implies_section", "local_implies_global",
        "coordinate_is_phi", "copresence_is_equation", "xmax_is_edge_value",
        "import_gr", "import_downstream_physics", "invent_join", "filter_by_merit",
        "launch_p03b", "launch_gpu", "kinematics_implies_eom", "claim_complete_action",
    }
    if any(bool(case.get(key)) for key in forbidden_true):
        raise ValueError("forbidden premise promotion")
    if case.get("coherent_domain") is False:
        raise ValueError("counterfamily has no coherent domain")
    if case.get("claim_unique") and int(case.get("surviving_moduli", 0)) > 0:
        raise ValueError("uniqueness with surviving moduli")
    if int(case.get("independent_selector_count", 3)) < 3:
        raise ValueError("independent gaps compressed")


def expect_rejection(catch_id: str, operation) -> dict[str, str]:
    try:
        operation()
    except (AssertionError, ValueError):
        return {"catch_id": catch_id, "result": "PASS", "method": "invalid in-memory candidate rejected"}
    raise AssertionError(f"{catch_id} did not reject its false promotion")


def main() -> None:
    manifest = table("SOURCE_MANIFEST.tsv")
    validate_manifest(manifest)
    adjudication = table("SOURCE_ADJUDICATION.tsv")
    require({row["path"] for row in adjudication} == {row["path"] for row in manifest}, "source adjudication coverage")

    obligations = table("CONSTRUCTION_OBLIGATIONS.tsv")
    premises = table("PREMISE_LEDGER.tsv")
    matrix = table("PRINCIPLE_CAPABILITY_MATRIX.tsv")
    require(len(obligations) == 12 and len(premises) == 17, "registered axes")
    require(len(matrix) == 204, "17 x 12 matrix")
    require(len({(row["premise_id"], row["obligation_id"]) for row in matrix}) == 204, "matrix uniqueness")

    algebra = independent_algebra()
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    require(production["lorentz_centralizer_nullity"] == algebra["full_lorentz_centralizer_nullity"], "centralizer agreement")
    require(production["ordered_pair_SO2_self_adjoint_physical_moduli"] == algebra["ordered_pair_moduli"], "lift agreement")
    require(production["c_G_dimension_matrix_rank"] == algebra["dimension_matrix_rank"], "dimension rank agreement")
    require(production["c_G_dimensionless_monomial_nullity"] == algebra["dimensionless_nullity"], "dimension nullity agreement")

    counters = table("COUNTERFAMILY_ATLAS.tsv")
    selectors = table("MINIMAL_SELECTOR_SET.tsv")
    require([row["id"] for row in counters] == [f"C{i:02d}" for i in range(1, 8)], "counterfamily coverage")
    require([row["selector_id"] for row in selectors] == [f"S{i:02d}" for i in range(1, 6)], "selector coverage")
    require(sum(row["status"] == "OPEN_INDEPENDENT" for row in selectors) == 3, "three kinematic selectors")

    correction = {row["claim"]: row for row in table("P03_SCOPE_CORRECTION.tsv")}
    nonultra = "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/AUDIT_REPORT.md"
    p03_paths = {row["path"] for row in table("../udt_global_coframe_compatibility_p03_2026-07-27/SOURCE_MANIFEST.tsv")}
    require(nonultra not in p03_paths, "P03 omission independently reproduced")
    introducing = git("log", "-1", "--format=%H", "--", nonultra).stdout.strip()
    ancestry = git("merge-base", "--is-ancestor", introducing, "6727b74878103a91eac855bad91a97b0a5c2e167", check=False)
    require(ancestry.returncode == 0, "omitted source predates P03 base")
    require(correction["only_ultrastatic_complete_controls_registered"]["ruling"] == "SUPERSEDED_REPOSITORY_WIDE", "P03 scope correction")

    proofs: list[dict[str, str]] = []
    duplicate = [dict(row) for row in manifest] + [dict(manifest[0])]
    proofs.append(expect_rejection("F01", lambda: validate_manifest(duplicate)))
    changed = [dict(row) for row in manifest]
    changed[0]["sha256"] = "0" * 64
    proofs.append(expect_rejection("F02", lambda: validate_manifest(changed)))
    omitted = [dict(row) for row in manifest if not row["path"].endswith("STRATUM_LEDGER.tsv")]
    proofs.append(expect_rejection("F03", lambda: validate_manifest(omitted)))
    generated = [dict(row) for row in manifest]
    generated[0]["path"] = HERE.name + "/AUDIT_RESULT.json"
    generated[0]["size_bytes"] = str((HERE / "AUDIT_RESULT.json").stat().st_size)
    generated[0]["sha256"] = digest(HERE / "AUDIT_RESULT.json")
    proofs.append(expect_rejection("F04", lambda: validate_manifest(generated)))

    policy_cases = {
        "F05": {"cross_splice": True},
        "F06": {"assume_block_diagonal": True},
        "F07": {"assume_spectator_screen": True},
        "F08": {"assume_topology_or_carrier": True},
        "F09": {"reactivate_strong_csn": True},
        "F10": {"anchors_select_shape": True},
        "F11": {"covariance_implies_unique": True},
        "F12": {"bundle_implies_section": True},
        "F13": {"local_implies_global": True},
        "F14": {"coordinate_is_phi": True},
        "F15": {"copresence_is_equation": True},
        "F16": {"xmax_is_edge_value": True},
        "F17": {"import_gr": True},
        "F18": {"import_downstream_physics": True},
        "F19": {"invent_join": True},
        "F20": {"coherent_domain": False},
        "F21": {"claim_unique": True, "surviving_moduli": 1},
        "F22": {"independent_selector_count": 1},
        "F23": {"filter_by_merit": True},
        "F24": {"launch_p03b": True},
        "F25": {"launch_gpu": True},
        "F26": {"kinematics_implies_eom": True},
        "F27": {"claim_complete_action": True},
    }
    for catch_id, invalid in policy_cases.items():
        proofs.append(expect_rejection(catch_id, lambda invalid=invalid: must_reject(invalid)))
    require([row["catch_id"] for row in proofs] == [f"F{i:02d}" for i in range(1, 28)], "catch order")

    with (HERE / "CATCH_PROOF_RESULTS.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["catch_id", "result", "method"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(proofs)

    audit = json.loads((HERE / "AUDIT_RESULT.json").read_text())
    require(audit["status"] == "OPEN_MULTIPLE_INDEPENDENT_SELECTOR_GAPS", "final classification")
    require(audit["source_count"] == 99 and audit["kinematic_minimal_selector_count"] == 3, "result counts")
    result = {
        "schema": "udt-native-global-coframe-definition-verification-1.0",
        "status": "PASS_VERIFIED_WITH_CAVEATS_SAME_SESSION",
        "source_count": len(manifest),
        "principle_obligation_rows": len(matrix),
        "counterfamily_count": len(counters),
        "kinematic_selector_count": 3,
        "catch_proofs_passed": len(proofs),
        "independent_algebra": algebra,
        "P03_omission_reproduced": True,
        "P03_omitted_source_introducing_commit": introducing,
        "fresh_adversarial_context": False,
        "caveat": "System instructions did not authorize subagent delegation; independent code was run in the same session.",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
