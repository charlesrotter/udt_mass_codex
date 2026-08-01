#!/usr/bin/env python3
"""Independent fail-closed verifier; never imports the primary derivation."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def load_tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(result: dict, conditions: list[dict[str, str]], sources: list[dict[str, str]]) -> None:
    assert result["outcome"] == "CONDITIONAL_NONPERIODIC_F02_DIRICHLET_HESSIAN_SECTOR_POSITIVITY_WITNESS_EXISTS"
    assert result["e0"] == "1/8"
    assert result["candidate_mass_gen"] == "1/4"
    assert result["candidate_mass_density_coordinate"] == "1/4"
    assert result["candidate_mass_density_proper"] == "1/4"
    assert result["candidate_mass_wall"] == "0"
    assert result["native_mass"] is False
    assert result["native_stability"] is False
    assert result["selected_response"] is False
    assert result["time_live"] is False
    assert result["completion"] == "OPEN_ACYCLIC_CONDITIONAL__NO_PHYSICAL_COMPLETION_CLAIM"
    assert result["threshold_residual"] == "pi**4 - 1"
    assert result["external_cold_review"] == "PASS_AFTER_REQUIRED_SCOPE_NARROWING__CLOSED"

    ids = [row["condition_id"] for row in conditions]
    assert ids == [f"C{i:02d}" for i in range(1, 12)]
    assert len(ids) == len(set(ids))
    by_id = {row["condition_id"]: row for row in conditions}
    assert by_id["C05"]["status"] == "CONDITIONAL_FREE"
    assert by_id["C06"]["status"] == "CONDITIONAL_ACYCLIC"
    assert by_id["C07"]["status"] == "NOT_ASSUMED_OPEN"
    assert by_id["C09"]["status"] == "OPEN"
    assert by_id["C10"]["status"] == "CANDIDATE_ONLY"
    assert by_id["C11"]["status"] == "OPEN"

    for row in sources:
        target = ROOT / row["path"]
        assert target.is_file()
        assert str(target.stat().st_size) == row["bytes"]
        assert digest(target) == row["sha256"]

    # Independent algebra: direct background substitution and Fourier-mode determinant.
    x = sp.symbols("x", real=True)
    p, lam, f, h = [sp.Function(name)(x) for name in ("p", "lam", "f", "h")]
    density = sp.exp(2 * lam * p) * (
        sp.diff(p, x) ** 2 / 2
        + sp.diff(f, x) ** 2 / 2
        + sp.diff(h, x) ** 2 / 2
        + sp.diff(lam, x) ** 2 / 2
    )

    def row(q):
        return sp.simplify(sp.diff(density, q) - sp.diff(sp.diff(density, sp.diff(q, x)), x))

    sub = {
        p: 0, sp.diff(p, x): 0, sp.diff(p, x, 2): 0,
        lam: 0, sp.diff(lam, x): 0, sp.diff(lam, x, 2): 0,
        f: x / 2, sp.diff(f, x): sp.Rational(1, 2), sp.diff(f, x, 2): 0,
        h: 0, sp.diff(h, x): 0, sp.diff(h, x, 2): 0,
    }
    assert all(sp.simplify(row(q).subs(sub)) == 0 for q in (p, lam, f, h))
    e0 = sp.Rational(1, 8)
    k = sp.pi / 2
    block = sp.Matrix([[k**2, 2 * e0], [2 * e0, k**2]])
    assert sp.simplify(block.det() - (sp.pi**4 - 1) / 16) == 0
    assert sp.ask(sp.Q.positive(block.det())) is True
    assert sp.integrate(sp.diff(x / 2, x), (x, -1, 1)) == 1


def expect_failure(name: str, mutate, base_result, base_conditions, sources) -> tuple[str, str]:
    result = copy.deepcopy(base_result)
    conditions = copy.deepcopy(base_conditions)
    src = copy.deepcopy(sources)
    mutate(result, conditions, src)
    try:
        validate(result, conditions, src)
    except (AssertionError, KeyError, FileNotFoundError):
        return name, "PASS"
    return name, "FAIL"


def main() -> None:
    result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
    conditions = load_tsv("CONDITION_LEDGER.tsv")
    sources = load_tsv("SOURCE_INVENTORY.tsv")
    validate(result, conditions, sources)
    mutations = [
        ("missing_condition", lambda r, c, s: c.pop()),
        ("duplicate_condition", lambda r, c, s: c.append(copy.deepcopy(c[0]))),
        ("source_mutation", lambda r, c, s: s[0].__setitem__("sha256", "0" * 64)),
        ("mass_promotion", lambda r, c, s: r.__setitem__("native_mass", True)),
        ("stability_promotion", lambda r, c, s: r.__setitem__("native_stability", True)),
        ("response_promotion", lambda r, c, s: r.__setitem__("selected_response", True)),
        ("wall_mass_conflation", lambda r, c, s: r.__setitem__("candidate_mass_wall", "1/4")),
        ("physical_completion_promotion", lambda r, c, s: r.__setitem__("completion", "PHYSICAL_COMPLETE_CELL")),
        ("fold_premise_smuggle", lambda r, c, s: c[6].__setitem__("status", "DERIVED_R_A")),
        ("inherited_as_adjudicated", lambda r, c, s: c[10].__setitem__("status", "NATIVE_STABLE")),
        ("stationary_global_promotion", lambda r, c, s: r.__setitem__("outcome", "CONDITIONAL_F02_STATIONARY_SECTOR_WITNESS_EXISTS")),
    ]
    catches = [expect_failure(name, mutation, result, conditions, sources) for name, mutation in mutations]
    assert all(status == "PASS" for _, status in catches)
    with (PKG / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch", "result"])
        writer.writerows(catches)
    verification = {
        "status": "PASS",
        "independent_rows_recomputed": 4,
        "condition_rows": len(conditions),
        "source_rows": len(sources),
        "catch_proofs_passed": len(catches),
        "catch_proofs_total": len(catches),
        "outcome_checked": result["outcome"],
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    line = json.dumps(verification, sort_keys=True)
    (PKG / "VERIFIER_STDOUT.txt").write_text(line + "\n", encoding="utf-8")
    print(line)


if __name__ == "__main__":
    main()
