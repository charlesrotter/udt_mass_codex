#!/usr/bin/env python3
"""Fail-closed primary verifier for the staged JR_CERT_NATIVE derivation."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "686336343878e8a9e39a4b72df08d23754243631"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(
    equation_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    stage_rows: list[dict[str, str]],
    status_rows: list[dict[str, str]],
    result: dict[str, object],
) -> None:
    assert [row["route_id"] for row in equation_rows] == [f"E{i:02d}" for i in range(1, 9)]
    assert len({row["route_id"] for row in equation_rows}) == 8
    assert [row["route_id"] for row in boundary_rows] == [f"B{i:02d}" for i in range(1, 7)]
    assert len({row["route_id"] for row in boundary_rows}) == 6
    assert all(row["pass"] in {"YES", "NO"} for row in equation_rows + boundary_rows)
    e_pass = any(row["pass"] == "YES" for row in equation_rows)
    b_route_pass = any(row["pass"] == "YES" for row in boundary_rows)
    b_pass = e_pass and b_route_pass
    solve_allowed = e_pass and b_pass
    assert [row["stage"] for row in stage_rows] == ["1", "2", "3", "4"]
    assert stage_rows[0]["gate_pass"] == ("YES" if e_pass else "NO")
    assert stage_rows[1]["gate_pass"] == ("YES" if b_pass else "NO")
    assert stage_rows[2]["gate_pass"] == ("YES" if solve_allowed else "NO")
    assert result["stage1_pass"] is e_pass
    assert result["stage2_pass"] is b_pass
    assert result["stage3_solve_allowed"] is solve_allowed
    assert result["stage3_launched"] is False
    assert result["stage3_solution_certified"] is False
    assert result["stage4_certificate_assembled"] is False
    assert result["stage4_certificate_allowed"] is False
    assert result["equation_routes"] == 8 and result["boundary_routes"] == 6
    assert result["equation_routes_passing"] == sum(row["pass"] == "YES" for row in equation_rows)
    assert result["boundary_routes_passing"] == sum(row["pass"] == "YES" for row in boundary_rows)
    assert result["governing_source_count"] == 586
    overall = {row["object"]: row for row in status_rows}["overall"]
    assert overall["status"] == result["outcome"]
    if not solve_allowed:
        assert stage_rows[2]["status"] == "NOT_LAUNCHED_FAIL_CLOSED"
        assert stage_rows[3]["status"].startswith("WITHHELD_")
    identity_text = (HERE / "IDENTITY_VS_EQUATION_LEDGER.tsv").read_text(encoding="utf-8")
    assert "IDENTITY_RECONSTRUCTION_NOT_EOM" in identity_text
    assert "ZERO_DYNAMICAL_RANK" in identity_text


equations = read_tsv("EQUATION_ROUTE_ADJUDICATION.tsv")
boundaries = read_tsv("BOUNDARY_ROUTE_ADJUDICATION.tsv")
stages = read_tsv("STAGE_GATE_LEDGER.tsv")
statuses = read_tsv("STATUS_LEDGER.tsv")
anchors = read_tsv("SOURCE_ANCHOR_LEDGER.tsv")
catch_rows = read_tsv("CATCH_PROOFS.tsv")
result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
algebra = json.loads((HERE / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))

validate(equations, boundaries, stages, statuses, result)
assert len(anchors) == 14 and len({row["anchor_id"] for row in anchors}) == 14
assert all((ROOT / row["path"]).is_file() and sha256(ROOT / row["path"]) == row["sha256"] for row in anchors)
assert all(row["result"] == "PASS" for row in catch_rows) and len(catch_rows) == 4

# Independent formulas, without importing the production module.
x = sp.symbols("x", real=True)
p = sp.Function("phi")(x)
expected_scalar = 2 * (sp.diff(p, x, 2) - 2 * sp.diff(p, x) ** 2) * sp.exp(-2 * p)
assert sp.simplify(sp.sympify(algebra["scalar_curvature"], locals={"phi": sp.Function("phi"), "x": x}) - expected_scalar) == 0
assert algebra["metric_determinant"] == "-1"
assert algebra["metric_compatibility_zero_count"] == algebra["metric_compatibility_total"] == 64
assert algebra["torsion_zero_count"] == algebra["torsion_total"] == 64
assert algebra["contracted_bianchi_divergence"] == ["0", "0", "0", "0"]
assert algebra["seal_family"] == {
    "normal_derivative_at_seal": "a",
    "phi_at_seal": "0",
    "scalar_curvature_at_seal": "-4*a**2",
}
assert algebra["second_order_variation_identity"] == "0"
assert algebra["fourth_order_variation_identity"] == "0"

# Verify both source freezes and their exact union.
original = read_tsv("SOURCE_INVENTORY.tsv")
transitive = read_tsv("TRANSITIVE_SOURCE_INVENTORY.tsv")
combined = [line for line in (HERE / "COMBINED_SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines() if line]
assert len(original) == 172 and len(transitive) == 414 and len(combined) == 586
assert not ({row["path"] for row in original} & {row["path"] for row in transitive})
assert combined == sorted({row["path"] for row in original} | {row["path"] for row in transitive})
assert all((ROOT / row["path"]).is_file() and sha256(ROOT / row["path"]) == row["sha256"] for row in original + transitive)

# Mutations must be rejected.  Each mutation changes one load-bearing gate while leaving the other
# records untouched, so failure demonstrates that the verifier is not merely replaying the outcome.
mutation_results: list[dict[str, str]] = []


def expect_reject(name: str, e=None, b=None, s=None, st=None, r=None) -> None:
    try:
        validate(
            copy.deepcopy(e if e is not None else equations),
            copy.deepcopy(b if b is not None else boundaries),
            copy.deepcopy(s if s is not None else stages),
            copy.deepcopy(st if st is not None else statuses),
            copy.deepcopy(r if r is not None else result),
        )
    except (AssertionError, KeyError):
        mutation_results.append({"mutation": name, "result": "PASS_REJECTED"})
    else:
        raise AssertionError(f"mutation escaped: {name}")


mut = copy.deepcopy(equations); mut.pop(); expect_reject("missing_equation_route", e=mut)
mut = copy.deepcopy(equations); mut[1]["route_id"] = "E01"; expect_reject("duplicate_equation_route", e=mut)
mut = copy.deepcopy(boundaries); mut.pop(); expect_reject("missing_boundary_route", b=mut)
mut = copy.deepcopy(boundaries); mut[1]["route_id"] = "B01"; expect_reject("duplicate_boundary_route", b=mut)
mut = copy.deepcopy(stages); mut[0]["gate_pass"] = "YES"; expect_reject("false_stage1_pass", s=mut)
mut = copy.deepcopy(stages); mut[1]["gate_pass"] = "YES"; expect_reject("false_stage2_pass", s=mut)
mut = copy.deepcopy(stages); mut[2]["gate_pass"] = "YES"; expect_reject("unauthorized_solve", s=mut)
mut = copy.deepcopy(stages); mut[2]["status"] = "LAUNCHED"; expect_reject("solve_status_promotion", s=mut)
mut = copy.deepcopy(stages); mut[3]["status"] = "ASSEMBLED"; expect_reject("certificate_status_promotion", s=mut)
mut = copy.deepcopy(result); mut["stage3_launched"] = True; expect_reject("result_solve_promotion", r=mut)
mut = copy.deepcopy(result); mut["stage4_certificate_assembled"] = True; expect_reject("result_certificate_promotion", r=mut)
mut = copy.deepcopy(result); mut["governing_source_count"] = 585; expect_reject("source_count_loss", r=mut)
mut = copy.deepcopy(result); mut["outcome"] = "NATIVE_JR_CERT_ASSEMBLED"; expect_reject("outcome_promotion", r=mut)
mut = copy.deepcopy(statuses); {row["object"]: row for row in mut}["overall"]["status"] = "NATIVE_JR_CERT_ASSEMBLED"; expect_reject("ledger_promotion", st=mut)

verification = {
    "base": BASE,
    "status": "PASS",
    "equation_routes": len(equations),
    "boundary_routes": len(boundaries),
    "source_anchors": len(anchors),
    "source_files_verified": len(original) + len(transitive),
    "production_catch_proofs": len(catch_rows),
    "verifier_mutations_rejected": len(mutation_results),
    "outcome": result["outcome"],
}
(HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
with (HERE / "VERIFIER_CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=["mutation", "result"], delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(mutation_results)
print(
    "PASS primary verification: "
    f"sources={verification['source_files_verified']} routes=8+6 "
    f"mutations={verification['verifier_mutations_rejected']} outcome={verification['outcome']}"
)
