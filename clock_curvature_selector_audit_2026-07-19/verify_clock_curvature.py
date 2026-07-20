#!/usr/bin/env python3
"""Independent tensor replay and fail-closed verifier for the clock-curvature audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def need(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def one(items: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    found = [row for row in items if row[key] == value]
    need(len(found) == 1, f"one:{key}:{value}")
    return found[0]


def scalar_curvature(metric: sp.Matrix, coords: tuple[sp.Symbol, ...]) -> tuple[sp.Expr, list[list[sp.Expr]]]:
    n = len(coords)
    inverse = sp.simplify(metric.inv())
    gamma = [[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for upper in range(n):
        for left in range(n):
            for right in range(n):
                gamma[upper][left][right] = sp.simplify(
                    sum(
                        inverse[upper, d]
                        * (sp.diff(metric[d, right], coords[left]) + sp.diff(metric[d, left], coords[right]) - sp.diff(metric[left, right], coords[d]))
                        / 2
                        for d in range(n)
                    )
                )
    ricci = [[sp.S.Zero for _ in range(n)] for _ in range(n)]
    for left in range(n):
        for right in range(n):
            ricci[left][right] = sp.simplify(
                sum(
                    sp.diff(gamma[a][left][right], coords[a])
                    - sp.diff(gamma[a][left][a], coords[right])
                    + sum(gamma[a][a][b] * gamma[b][left][right] - gamma[a][right][b] * gamma[b][left][a] for b in range(n))
                    for a in range(n)
                )
            )
    scalar = sp.simplify(sum(inverse[i, j] * ricci[i][j] for i in range(n) for j in range(n)))
    return scalar, ricci


def independent_tensor_algebra() -> dict[str, str]:
    t, r, theta, azimuth, X, epsilon = sp.symbols("t r theta azimuth X epsilon", positive=True)
    A = sp.Function("Q")(r)  # Deliberately different profile symbol from the derivation script.
    metric4 = sp.diag(-A, 1 / A, r**2, r**2 * sp.sin(theta) ** 2)
    R4, ricci4 = scalar_curvature(metric4, (t, r, theta, azimuth))
    expected_R4 = -sp.diff(A, r, 2) - 4 * sp.diff(A, r) / r + 2 * (1 - A) / r**2
    need(sp.simplify(R4 - expected_R4) == 0, "direct-R4")

    metric3 = sp.diag(1 / A, r**2, r**2 * sp.sin(theta) ** 2)
    R3, _ = scalar_curvature(metric3, (r, theta, azimuth))
    expected_R3 = -2 * sp.diff(A, r) / r + 2 * (1 - A) / r**2
    need(sp.simplify(R3 - expected_R3) == 0, "direct-R3")

    N = sp.sqrt(A)
    determinant3 = sp.simplify(metric3.det())
    inverse3 = sp.simplify(metric3.inv())
    laplace = sp.simplify(
        sum(
            sp.diff(sp.sqrt(determinant3) * inverse3[i, j] * sp.diff(N, (r, theta, azimuth)[j]), (r, theta, azimuth)[i])
            for i in range(3)
            for j in range(3)
        )
        / sp.sqrt(determinant3)
    )
    expected_laplace = N * (sp.diff(A, r, 2) / 2 + sp.diff(A, r) / r)
    need(sp.simplify(laplace - expected_laplace) == 0, "direct-laplacian")
    need(sp.simplify(ricci4[0][0] - N * laplace) == 0, "direct-Rtt")

    operator = sp.diff(A, r, 2) + sp.diff(A, r) / r + (1 - A) / r**2
    need(sp.simplify(laplace + R4 * N / 6 - N * operator / 3) == 0, "direct-E4")
    need(sp.simplify(laplace + R3 * N / 4 - N * operator / 2) == 0, "direct-E3")

    y = r / X
    deformation = (1 - y) * (1 + epsilon * y * (1 - y))
    residual = sp.factor(operator.subs(A, deformation).doit())
    need(sp.simplify(residual - 2 * epsilon * (4 * r - 3 * X) / X**3) == 0, "direct-countermetric")
    return {
        "R4": str(expected_R4),
        "R3": str(expected_R3),
        "laplace_N": str(expected_laplace),
        "countermetric_residual": str(residual),
    }


def validate_premises(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 12 and len({row["id"] for row in items}) == 12, "premise-census")
    need(one(items, "id", "P03")["status"] == "PINNED_BY_THEORY", "CSN-premise")
    need(one(items, "id", "P06")["status"] == "OPEN_CANDIDATE", "selector-open")
    need(one(items, "id", "P08")["status"] == "WORKING", "bootstrap-working")
    need(one(items, "id", "P12")["status"] == "NOT_AUTHORIZED", "review-caveat")
    return {"rows": len(items)}


def validate_profiles(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 4 and len({row["id"] for row in items}) == 4, "profile-census")
    need(one(items, "id", "F03")["clock_curvature_equation"] == "YES", "WRL-control")
    counter = one(items, "id", "F04")
    need(counter["reciprocal_block"] == "YES" and counter["clock_curvature_equation"] == "NO", "countermetric")
    need(counter["classification"] == "BOUNDED_NON_ENTAILMENT_COUNTERMETRIC", "countermetric-scope")
    return {"rows": len(items), "countermetrics": 1}


def validate_status(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 12 and len({row["id"] for row in items}) == 12, "status-census")
    expected = {
        "S03": "UNIQUE_CONDITIONAL",
        "S04": "NOT_DERIVED",
        "S05": "NOT_DERIVED",
        "S06": "REFUTED_AS_WRITTEN",
        "S07": "REFUTED",
        "S08": "CONDITIONAL",
        "S09": "OPEN_NOT_SUPPLIED",
        "S10": "OPEN_NOT_CLAIMED",
        "S11": "CONDITIONAL_LEAD",
        "S12": "OPEN",
    }
    for identity, status in expected.items():
        need(one(items, "id", identity)["status"] == status, f"status:{identity}")
    return {"rows": len(items), "rulings_checked": len(expected)}


def validate_sources(items: list[dict[str, str]]) -> dict[str, object]:
    need(len(items) == 8 and len({row["path"] for row in items}) == 8, "source-census")
    for row in items:
        need((ROOT / row["path"]).is_file(), f"missing-source:{row['path']}")
    csn = (ROOT / "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md").read_text(encoding="utf-8")
    bootstrap = (ROOT / "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md").read_text(encoding="utf-8")
    frontier = (ROOT / "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md").read_text(encoding="utf-8")
    offshell = (ROOT / "reciprocity_offshell_constraint_selector_2026-07-18/DERIVATION_REPORT.md").read_text(encoding="utf-8")
    need(r"g_{\mu\nu}" in csn and "Omega^2g" in csn.replace("\\", "") and "pre-scale bulk law" in csn, "CSN-source")
    need("ON_SHELL_CLOSURE_OR_ADMISSIBILITY" in frontier, "bootstrap-frontier")
    need("No nonlocal insertion" in bootstrap and "center and width" in bootstrap, "bootstrap-source")
    need("gauge" in offshell.lower() and "off-shell" in offshell.lower(), "reciprocity-source")
    return {"rows": len(items), "text_checks": 4}


def validate_derivation(result: dict[str, object]) -> dict[str, object]:
    need(result["result"] == "PASS" and len(result["checks"]) == 23, "derivation-checks")
    need(result["general_family"]["E4"].endswith("/3"), "general-E4")
    need(result["selector_solution"]["conditional_result"] == "A=1-r/X (WR-L)", "conditional-WRL")
    need(result["countermetric"]["profile_residual"] == "2*epsilon*(4*r-3*X)/X^3", "counter-residual")
    need("general local common scale does not" in result["common_scale"]["ruling"], "local-CSN-ruling")
    need("NOT_FORCED_BY_CURRENT" in result["maximum_conclusion"], "maximum")
    return {"checks": len(result["checks"]), "maximum": result["maximum_conclusion"]}


def expect_failure(label: str, function) -> str:
    try:
        function()
    except AssertionError:
        return "PASS"
    raise AssertionError(f"catch-did-not-fail:{label}")


def main() -> None:
    premises = rows("PREMISE_LEDGER.tsv")
    profiles = rows("PROFILE_FAMILY_LEDGER.tsv")
    statuses = rows("STATUS_LEDGER.tsv")
    sources = rows("SOURCE_LEDGER.tsv")
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    groups = {
        "premises": validate_premises(premises),
        "profiles": validate_profiles(profiles),
        "statuses": validate_status(statuses),
        "sources": validate_sources(sources),
        "derivation": validate_derivation(derivation),
        "independent_tensor_algebra": independent_tensor_algebra(),
    }

    catches: dict[str, str] = {}
    catches["missing_premise_rejected"] = expect_failure("premise", lambda: validate_premises(premises[:-1]))
    catches["missing_profile_rejected"] = expect_failure("profile", lambda: validate_profiles(profiles[:-1]))
    mutated = copy.deepcopy(profiles); one(mutated, "id", "F04")["clock_curvature_equation"] = "YES"
    catches["countermetric_erasure_rejected"] = expect_failure("countermetric", lambda: validate_profiles(mutated))
    mutated = copy.deepcopy(statuses); one(mutated, "id", "S03")["status"] = "DERIVED_UNCONDITIONAL"
    catches["conditional_selector_promotion_rejected"] = expect_failure("conditional", lambda: validate_status(mutated))
    mutated = copy.deepcopy(statuses); one(mutated, "id", "S04")["status"] = "DERIVED"
    catches["reciprocity_forcing_promotion_rejected"] = expect_failure("reciprocity", lambda: validate_status(mutated))
    mutated = copy.deepcopy(statuses); one(mutated, "id", "S06")["status"] = "DERIVED_CSN_COVARIANT"
    catches["local_CSN_failure_erasure_rejected"] = expect_failure("CSN", lambda: validate_status(mutated))
    mutated = copy.deepcopy(statuses); one(mutated, "id", "S09")["status"] = "DERIVED_BOOTSTRAP_SELECTOR"
    catches["bootstrap_equation_invention_rejected"] = expect_failure("bootstrap", lambda: validate_status(mutated))
    mutated = copy.deepcopy(statuses); one(mutated, "id", "S10")["status"] = "COMPLETE_FOUNDATION_COUNTEREXAMPLE"
    catches["countermodel_completeness_overstatement_rejected"] = expect_failure("completeness", lambda: validate_status(mutated))
    mutated = copy.deepcopy(statuses); one(mutated, "id", "S12")["status"] = "DERIVED_COMPLETE_ACTION"
    catches["complete_action_promotion_rejected"] = expect_failure("action", lambda: validate_status(mutated))
    altered = copy.deepcopy(derivation); altered["countermetric"]["profile_residual"] = "0"
    catches["algebra_mutation_rejected"] = expect_failure("algebra", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["common_scale"]["ruling"] = "local scale preserves zero"
    catches["CSN_algebra_mutation_rejected"] = expect_failure("CSN-algebra", lambda: validate_derivation(altered))
    altered = copy.deepcopy(derivation); altered["maximum_conclusion"] = "UNCONDITIONAL_NATIVE_FIELD_EQUATION"
    catches["maximum_conclusion_promotion_rejected"] = expect_failure("maximum", lambda: validate_derivation(altered))

    output = {
        "schema": "udt-clock-curvature-selector-verification-1.0",
        "result": "PASS",
        "groups": groups,
        "catch_proofs": catches,
        "counts": {"premises": len(premises), "profiles": len(profiles), "statuses": len(statuses), "sources": len(sources), "catch_proofs": len(catches)},
        "derivation_sha256": hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest(),
        "verdict": "UNIQUE_CONDITIONAL_PROFILE_SELECTOR; CURRENT_NATIVE_FOUNDATION_DOES_NOT_FORCE_IT",
        "certification": "VERIFIED-WITH-CAVEATS: independent in-package tensor replay; no fresh external-model review",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "groups": len(groups), "catch_proofs": len(catches), "verdict": output["verdict"]}, sort_keys=True))


if __name__ == "__main__":
    main()
