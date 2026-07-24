#!/usr/bin/env python3
"""Independent stdlib verification and exercised semantic catch-proofs."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path(__file__).resolve().parent


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")

def rows(name: str) -> list[dict[str, str]]:
    with (OUT / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def verify(data: dict) -> None:
    rulings = data["rulings"]
    algebra = data["algebra"]
    assert data["status"] == "PASS"
    assert data["production_check_count"] == 20
    assert all(data["production_checks"].values())

    # Independent fixed-number reconstruction: A=3 and exp(phi)=2.
    # D=diag(1/2,2), so D^T K D=K; (3D)^T K (3D)=9K.
    D = ((1 / 2, 0), (0, 2))
    K = ((0, 1), (1, 0))
    P = ((3 / 2, 0), (0, 6))

    def mt(a):
        return tuple(zip(*a))

    def mm(a, b):
        bt = mt(b)
        return tuple(
            tuple(sum(x * y for x, y in zip(row, col)) for col in bt)
            for row in a
        )

    assert mm(mm(mt(D), K), D) == K
    assert mm(mm(mt(P), K), P) == ((0, 9), (9, 0))
    assert algebra["P_transpose_K_P"] == "A^2*K"
    assert algebra["fixed_K_positive_A"] == "1"
    assert algebra["length_from_c_and_G_alone"] == "NO_MONOMIAL_SOLUTION"

    # c remains invariant under simultaneous clock/ruler unit scaling.
    dtau, dell, omega = 7, 11, 13
    assert (omega * dtau) / (omega * dell) == dtau / dell

    # Nonconstant conformal witness is nonzero for k=x=1.
    assert -6 * (2.718281828459045 ** -2) != 0

    assert rulings["strong_local_CSN"] == (
        "OWNER_POSTULATE_NOT_DERIVED_FROM_RECIPROCITY_CURRENTLY_CHALLENGED"
    )
    assert rulings["common_factor_from_reciprocity"] == (
        "FIXED_IN_EXACT_K_PRESERVING_COMPARISON_NOT_GAUGE_DERIVED"
    )
    assert rulings["physical_representative"] == "OPEN_SELECTOR"
    assert rulings["C2_Bach"] == (
        "UNIQUE_CONDITIONAL_IF_STRONG_LOCAL_CSN_IS_RETAINED"
    )
    assert rulings["EH"] == "CONDITIONAL_NOT_SELECTED"

    postulate = read("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md")
    reciprocal = read("UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md")
    selector = read(
        "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md"
    )
    assert "FOUNDATIONAL POSTULATE" in postulate
    assert "declares the first factor calibrational" in postulate
    assert r"\Omega(x)^2g_{\mu\nu}" in postulate
    assert r"\boxed{u(\Delta)v(\Delta)=1.}" in reciprocal
    assert "SELECTOR_NOT_FOUND_IN_CURRENT_FOUNDATION" in selector

    census = rows("SOURCE_CENSUS.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    assert len(census) == 1421
    assert len(manifest) == 1421
    assert len({r["path"] for r in census}) == 1421
    assert len({r["path"] for r in manifest}) == 1421
    assert sum(r["mandatory"] == "YES" for r in census) == 29
    assert sum(r["role"] == "LOAD_BEARING" for r in census) == 29
    assert sum(int(r["query_hits"]) for r in census) == 18612
    assert {
        (r["path"], r["blob"], r["sha256"], r["bytes"]) for r in manifest
    } == {
        (r["path"], r["blob"], r["sha256"], r["bytes"]) for r in census
    }

    status = rows("STATUS_LEDGER.tsv")
    impact = rows("DOWNSTREAM_IMPACT_LEDGER.tsv")
    load_bearing = rows("LOAD_BEARING_SOURCE_LEDGER.tsv")
    assert len(status) == 24
    assert len({r["id"] for r in status}) == 24
    assert len(impact) == 15
    assert len(load_bearing) == 23
    strong = next(r for r in status if r["id"] == "S08")
    assert strong["current_audit_status"] == (
        "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED"
    )
    c2 = next(r for r in status if r["id"] == "S12")
    assert c2["current_audit_status"] == (
        "UNIQUE_CONDITIONAL_ONLY_IF_STRONG_CSN_RETAINED"
    )
    eh = next(r for r in status if r["id"] == "S13")
    assert eh["current_audit_status"] == "CONDITIONAL_NOT_SELECTED"


def mutate(data: dict, name: str) -> dict:
    bad = copy.deepcopy(data)
    if name == "postulate_promoted_to_derived":
        bad["rulings"]["strong_local_CSN"] = "DERIVED"
    elif name == "fixed_K_allows_arbitrary_A":
        bad["algebra"]["fixed_K_positive_A"] = "ARBITRARY"
    elif name == "c_claimed_to_select_length":
        bad["algebra"]["length_from_c_and_G_alone"] = "UNIQUE_LENGTH"
    elif name == "representative_claimed_selected":
        bad["rulings"]["physical_representative"] = "DERIVED"
    elif name == "C2_premise_dropped":
        bad["rulings"]["C2_Bach"] = "UNIQUE_UNCONDITIONAL"
    elif name == "EH_promoted":
        bad["rulings"]["EH"] = "DERIVED"
    elif name == "source_check_removed":
        bad["production_checks"]["S02_CSN_declares_factor_calibrational"] = False
    elif name == "production_count_corrupted":
        bad["production_check_count"] = 19
    elif name == "strong_CSN_left_unchallenged":
        bad["rulings"]["strong_local_CSN"] = "FOUNDING_LOCKED"
    elif name == "common_factor_called_gauge_derived":
        bad["rulings"]["common_factor_from_reciprocity"] = "GAUGE_DERIVED"
    else:
        raise KeyError(name)
    return bad


def main() -> None:
    data = json.loads((OUT / "RESULTS.json").read_text(encoding="utf-8"))
    verify(data)
    names = [
        "postulate_promoted_to_derived",
        "fixed_K_allows_arbitrary_A",
        "c_claimed_to_select_length",
        "representative_claimed_selected",
        "C2_premise_dropped",
        "EH_promoted",
        "source_check_removed",
        "production_count_corrupted",
        "strong_CSN_left_unchallenged",
        "common_factor_called_gauge_derived",
    ]
    catches = []
    for name in names:
        caught = False
        try:
            verify(mutate(data, name))
        except (AssertionError, KeyError):
            caught = True
        assert caught, f"mutation escaped: {name}"
        catches.append({"catch": name, "result": "PASS_REJECTED"})

    result = {
        "status": "PASS",
        "independent_method": "stdlib fixed-number matrix and dimensional reconstruction",
        "production_result_sha256": hashlib.sha256(
            (OUT / "RESULTS.json").read_bytes()
        ).hexdigest(),
        "catch_count": len(catches),
        "catches": catches,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (OUT / "INDEPENDENT_RESULTS.json").write_text(payload, encoding="utf-8")
    with (OUT / "CATCH_PROOF_RESULTS.tsv").open("w", encoding="utf-8") as f:
        f.write("catch\tresult\n")
        for row in catches:
            f.write(f"{row['catch']}\t{row['result']}\n")
    print(payload, end="")


if __name__ == "__main__":
    main()
