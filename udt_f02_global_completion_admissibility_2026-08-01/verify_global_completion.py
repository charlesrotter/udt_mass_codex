#!/usr/bin/env python3
"""Independent fail-closed verification; does not import the primary derivation."""

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
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def table(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(result: dict, rows: list[dict[str, str]], sources: list[dict[str, str]]) -> None:
    assert result["outcome"] == "OPEN_INCOMPLETE_REGISTERED_CLOSURE_DATA"
    assert result["candidate_rows"] == 9
    assert result["nonzero_complete_witness_found"] is False
    assert result["exhaustive_no_witness_proved"] is False
    assert result["native_mass"] is False
    assert result["native_stability"] is False
    assert result["selected_completion"] is False
    assert result["candidate_mass_readings"] == "THREE_NONZERO_LABELS_REMAIN_LOCAL_CANDIDATES__M_WALL_ZERO__NONE_PROMOTED"
    ids = [row["candidate_id"] for row in rows]
    assert ids == [f"G{i:02d}" for i in range(1, 10)] and len(set(ids)) == 9
    by_id = {row["candidate_id"]: row for row in rows}
    assert by_id["G04"]["f02_status"] == "OPEN_INCOMPLETE_TRANSITION_DATA"
    assert by_id["G05"]["f02_status"] == "LOCAL_WITNESS_SURVIVES__NO_COMPLETE_GLOBAL_WITNESS"
    assert by_id["G07"]["f02_status"] == "NO_NONZERO_F02_FROM_CAP_REGULARITY"
    assert by_id["G07"]["source"] == "cap-gluing; D06-D07"
    assert by_id["G03"]["reason"] == "one common nondegenerate response matrix plus momentum and field-period closure forces every slope to zero; heterogeneous positive blocks obey the same theorem"
    assert by_id["G08"]["f02_status"] == "OPEN_INCOMPLETE_JOIN_DATA"
    assert by_id["G09"]["registration"] == "UNREGISTERED_EXCLUDED"
    assert "OPEN" in by_id["G01"]["f02_status"]
    for row in sources:
        target = ROOT / row["path"]
        assert target.is_file() and str(target.stat().st_size) == row["bytes"]
        assert digest(target) == row["sha256"]

    # Fresh algebra. Untwisted positive cells: c^T(sum L_i G_i^-1)c > 0 for c != 0.
    L1, L2 = sp.symbols("L1 L2", positive=True)
    q, r = sp.symbols("q r", real=True)
    c = sp.Matrix([q, r])
    G1 = sp.diag(2, 3)
    G2 = sp.Matrix([[2, 1], [1, 2]])
    A = L1 * G1.inv() + L2 * G2.inv()
    assert A[0, 0].is_positive is True and sp.ask(sp.Q.positive(A.det())) is True
    assert sp.solve(list(A * c), [q, r], dict=True) == [{q: 0, r: 0}]

    # Two-cell raw cancellation fails ordinary momentum matching, while T=-I transports it.
    a, b = sp.symbols("a b", real=True)
    v = sp.Matrix([a, b])
    G = sp.Matrix([[4, 1], [1, 2]])
    assert sp.simplify(G * (-v) - G * v) == -2 * G * v
    assert sp.simplify((-sp.eye(2)).inv().T * (G * v)) == G * (-v)
    Gplus = sp.diag(1, -1)
    Gminus = -Gplus
    c0 = sp.Matrix([1, 0])
    ap, am = Gplus.inv() * c0, Gminus.inv() * c0
    assert ap + am == sp.zeros(2, 1)
    assert Gplus * ap == Gminus * am == c0
    assert ((ap.T * Gplus * ap)[0] / 2, (am.T * Gminus * am)[0] / 2) == (sp.Rational(1, 2), sp.Rational(-1, 2))

    # A regular cap requires zero first jets; affine plus opposite cap values is inconsistent.
    x, f0, slope = sp.symbols("x f0 slope", real=True)
    ell = sp.symbols("ell", positive=True)
    f = f0 + slope * x
    assert sp.solve([sp.Eq(sp.diff(f, x), 0)], [slope], dict=True) == [{slope: 0}]
    assert sp.solve(
        [sp.Eq(f.subs(x, -ell), -1), sp.Eq(f.subs(x, ell), 1), sp.Eq(sp.diff(f, x), 0)],
        [f0, slope], dict=True,
    ) == []


def catch(name, mutation, result, rows, sources):
    r, c, s = copy.deepcopy(result), copy.deepcopy(rows), copy.deepcopy(sources)
    mutation(r, c, s)
    try:
        validate(r, c, s)
    except (AssertionError, KeyError, FileNotFoundError):
        return name, "PASS"
    return name, "FAIL"


def main() -> None:
    result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
    rows = table("COMPLETION_CENSUS.tsv")
    sources = table("SOURCE_INVENTORY.tsv")
    validate(result, rows, sources)
    mutations = [
        ("missing_candidate", lambda r, c, s: c.pop()),
        ("duplicate_candidate", lambda r, c, s: c.append(copy.deepcopy(c[0]))),
        ("unregistered_same_closer_witness", lambda r, c, s: c[8].__setitem__("registration", "REGISTERED_WITNESS")),
        ("open_endpoint_promoted", lambda r, c, s: c[4].__setitem__("f02_status", "COMPLETE_GLOBAL_WITNESS")),
        ("RA_smuggled_into_no_RA", lambda r, c, s: c[6].__setitem__("source", "R-A_ASSUMED")),
        ("onecell_as_multicell", lambda r, c, s: c[2].__setitem__("reason", "one-cell proof copied")),
        ("twist_ignored", lambda r, c, s: c[3].__setitem__("f02_status", "NO_NONZERO_F02")),
        ("mixed_join_silently_closed", lambda r, c, s: c[7].__setitem__("f02_status", "NO_NONZERO_F02")),
        ("wall_reading_lost", lambda r, c, s: r.__setitem__("candidate_mass_readings", "ALL_NONZERO_AGREE")),
        ("native_mass_promotion", lambda r, c, s: r.__setitem__("native_mass", True)),
        ("global_stability_promotion", lambda r, c, s: r.__setitem__("native_stability", True)),
        ("false_exhaustive_nogo", lambda r, c, s: r.__setitem__("outcome", "NO_REGISTERED_COMPLETE_F02_WITNESS_IN_EXHAUSTED_CENSUS")),
        ("source_mutation", lambda r, c, s: s[0].__setitem__("sha256", "0" * 64)),
    ]
    catches = [catch(name, mutate, result, rows, sources) for name, mutate in mutations]
    for name, status in catches:
        print(f"[{status}] catch {name}")
    assert all(status == "PASS" for _, status in catches)
    with (PKG / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch", "result"])
        writer.writerows(catches)
    verification = {
        "status": "PASS",
        "candidate_rows": len(rows),
        "source_rows": len(sources),
        "catch_proofs_passed": len(catches),
        "catch_proofs_total": len(catches),
        "independent_algebra": "UNTWISTED_MULTICELL_NO_GO__TWIST_REQUIRES_DATA__REGULAR_CAP_NO_GO",
        "outcome": result["outcome"],
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    line = json.dumps(verification, sort_keys=True)
    (PKG / "VERIFIER_STDOUT.txt").write_text(line + "\n", encoding="utf-8")
    print(line)


if __name__ == "__main__":
    main()
