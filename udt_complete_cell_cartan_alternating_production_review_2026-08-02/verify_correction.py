#!/usr/bin/env python3
"""Independent correction verifier for the cold-reviewed Cartan contact result."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_complete_cell_cartan_alternating_production_audit_2026-08-02"
ETA = (-1, 1, 1, 1)
PAIRS = tuple((i, j) for i in range(4) for j in range(i + 1, 4))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_sources_and_parent() -> dict[str, object]:
    source_rows = rows(HERE / "SOURCE_MANIFEST.tsv")
    assert len(source_rows) == len({row["path"] for row in source_rows}) == 20
    for row in source_rows:
        path = ROOT / row["path"]
        assert path.is_file() and path.stat().st_size == int(row["bytes"])
        assert digest(path) == row["sha256"]
        blob = subprocess.run(
            ["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT,
            text=True, capture_output=True, check=True,
        ).stdout.strip()
        assert blob == row["git_blob"]

    package_entries = []
    for line in (PARENT / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        expected, name = line.split(None, 1)
        target = PARENT / name.strip()
        assert target.is_file() and digest(target) == expected
        package_entries.append(name.strip())
    assert len(package_entries) == len(set(package_entries)) == 43
    parent_sources = rows(PARENT / "SOURCE_MANIFEST.tsv")
    assert len(parent_sources) == len({row["path"] for row in parent_sources}) == 29
    return {
        "review_sources": 20,
        "review_source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
        "parent_package_entries": 43,
        "parent_package_manifest_sha256": digest(PARENT / "PACKAGE_MANIFEST.sha256"),
        "parent_sources": 29,
    }


def corrected_contact_algebra() -> dict[str, object]:
    phi, sigma, B = sp.symbols("phi sigma B", real=True)
    dphi, dsigma = sp.symbols("dphi dsigma")
    v = B + phi - sigma
    dv = dphi - dsigma
    primitive = sp.Matrix([
        sp.expand((v * dphi - phi * dv) / 2).coeff(dphi),
        sp.expand((v * dphi - phi * dv) / 2).coeff(dsigma),
    ])
    expected = sp.Matrix([-sigma / 2 + B / 2, phi / 2])
    assert sp.simplify(primitive - expected) == sp.zeros(2, 1)
    affine = sp.Matrix([[0, 0, -1, 0, 1, 0]])
    assert affine.rank() == 1 and len(affine.nullspace()) == 5
    return {
        "dimensioned_contact_log": "v=log(|t1|/T0)=B+phi-sigma",
        "B": "log(|kappa|/(D0*T0))",
        "differential_identity": "-dphi_wedge_dv=dphi_wedge_dsigma",
        "primitive_difference": "lambda_phi_v-lambda_phi_sigma=d(B*phi/2)",
        "affine_quotient_rank": 1,
        "universally_exact_kernel_dimension": 5,
    }


def gauge_algebra() -> dict[str, str]:
    theta, q, m = sp.symbols("theta q m", real=True)
    c, s = sp.cos(theta), sp.sin(theta)
    O = sp.Matrix([[c, -s], [s, c]])
    R = sp.Matrix([[0, -1], [1, 0]])
    l11, l12, l21, l22 = sp.symbols("l11 l12 l21 l22")
    L = sp.Matrix([[l11, l12], [l21, l22]])
    C = R
    Q = q * R
    Cprime = sp.simplify(O * C * O.T)
    Lprime = sp.simplify(Q + O * L * O.T)
    Aprime_direct = sp.simplify(Q + O * (L + m * C) * O.T)
    Aprime_split = sp.simplify(Lprime + m * Cprime)
    assert sp.simplify(Cprime - C) == sp.zeros(2)
    assert sp.simplify(Aprime_direct - Aprime_split) == sp.zeros(2)
    reflection = sp.diag(1, -1)
    assert reflection.det() == -1
    return {
        "m_transform": "m_prime=m",
        "C_transform": "C_prime=O*C*O^-1",
        "L1_transform": "L1_prime=(E1O)O^-1+O*L1*O^-1",
        "total_transform": "A1_prime=(E1O)O^-1+O*A1*O^-1",
        "ruling": "mC_HOMOGENEOUS_BUT_EXTRACTION_FROM_TOTAL_A1_REQUIRES_SUPPLIED_DECOMPOSITION",
        "t1_transform": "t1_prime=det(O)*t1",
    }


def curvature_census(pivot: str) -> dict[str, object]:
    p1, p2, p3, s1, s2, s3, m, t = sp.symbols("p1 p2 p3 s1 s2 s3 m t", real=True)
    p = (p1, p2, p3)
    s = (s1, s2, s3)
    fields = p + s
    deriv = {
        (direction, field): sp.Symbol(f"{pivot}_E{direction}_{field}", real=True)
        for direction in (1, 2, 3) for field in fields
    }
    A: dict[tuple[int, int, int], sp.Expr] = {}
    for index, value in enumerate(p, start=1):
        A[(0, 0, index)] = value
    A.update({
        (1, 1, 2): -p2, (1, 1, 3): -p3, (1, 2, 3): t,
        (2, 1, 2): s1/2, (2, 1, 3): -m, (2, 2, 3): -s3/2,
        (3, 1, 2): m, (3, 1, 3): s1/2, (3, 2, 3): s2/2,
    })

    def aval(a: int, b: int, c: int) -> sp.Expr:
        if b == c:
            return sp.Integer(0)
        return A.get((a, b, c), 0) if b < c else -A.get((a, c, b), 0)

    def structure(a: int, b: int, c: int) -> sp.Expr:
        return -aval(a, b, c)

    closure: dict[sp.Symbol, sp.Expr] = {}
    for field in (p, s):
        for i, j in ((1, 2), (1, 3), (2, 3)):
            commutator = sum(structure(k, i, j) * field[k-1] for k in (1, 2, 3))
            if pivot == "FORWARD":
                closure[deriv[(i, field[j-1])]] = deriv[(j, field[i-1])] + commutator
            elif pivot == "REVERSE":
                closure[deriv[(j, field[i-1])]] = deriv[(i, field[j-1])] - commutator
            else:
                raise AssertionError(pivot)

    def E(direction: int, expression: sp.Expr) -> sp.Expr:
        if direction == 0:
            return sp.Integer(0)
        value = sum(sp.diff(expression, field) * deriv[(direction, field)] for field in fields)
        value += sp.diff(expression, m) * (-m * p[direction-1])
        value += sp.diff(expression, t) * (t * (p[direction-1] - s[direction-1]))
        return sp.factor(sp.expand(value).subs(closure))

    gamma: dict[tuple[int, int, int], sp.Expr] = {}
    for a in range(4):
        for i in range(4):
            for j in range(4):
                gamma[(a, i, j)] = sp.factor((
                    structure(a, i, j)
                    - ETA[a]*ETA[i]*structure(i, j, a)
                    + ETA[a]*ETA[j]*structure(j, a, i)
                )/2)
    for a in range(4):
        for i, j in PAIRS:
            assert sp.simplify(gamma[(a, i, j)]-gamma[(a, j, i)]-structure(a, i, j)) == 0
    for i in range(4):
        for a in range(4):
            for b in range(4):
                assert sp.simplify(ETA[a]*gamma[(a, i, b)]+ETA[b]*gamma[(b, i, a)]) == 0

    curvature: dict[tuple[int, int, int, int], sp.Expr] = {}
    for a in range(4):
        for b in range(4):
            for c, d in PAIRS:
                value = E(c, gamma[(a, d, b)])-E(d, gamma[(a, c, b)])
                value += sum(
                    gamma[(e, d, b)]*gamma[(a, c, e)]
                    -gamma[(e, c, b)]*gamma[(a, d, e)]
                    -structure(e, c, d)*gamma[(a, e, b)]
                    for e in range(4)
                )
                curvature[(a, b, c, d)] = sp.factor(sp.expand(value).subs(closure))

    mixed_rows = []
    narrow_rows = []
    nonzero_pairs = set()
    for a, b in PAIRS:
        for c, d in PAIRS:
            expression = sp.expand(ETA[a]*curvature[(a, b, c, d)])
            if expression != 0:
                nonzero_pairs.add((a, b))
            has_mixed = False
            monomials = []
            polynomial = sp.Poly(expression, *(fields + tuple(deriv.values()) + (m, t)))
            for powers, coefficient in polynomial.terms():
                if coefficient == 0:
                    continue
                has_p = any(powers[index] for index in range(3))
                has_s = any(powers[index] for index in range(3, 6))
                if has_p and has_s:
                    has_mixed = True
                    monomials.append(str(sp.prod(variable**power for variable, power in zip(polynomial.gens, powers) if power)))
            if has_mixed:
                mixed_rows.append({
                    "pivot": pivot, "curvature_pair": f"Omega{a}{b}", "two_form_leg": f"{c}{d}",
                    "mixed_monomials": ";".join(sorted(set(monomials))),
                    "expression": str(expression),
                })
            if c > 0:
                forward = expression.coeff(p[c-1]*s[d-1])
                reverse = expression.coeff(p[d-1]*s[c-1])
                alt = sp.simplify((forward-reverse)/2)
                sym = sp.simplify((forward+reverse)/2)
                if alt != 0 or sym != 0:
                    narrow_rows.append((a, b, c, d, alt, sym))
    expected_reverse = {
        ("Omega02", "02"), ("Omega02", "03"), ("Omega03", "02"), ("Omega03", "03"),
        ("Omega12", "12"), ("Omega12", "13"), ("Omega12", "23"),
        ("Omega13", "12"), ("Omega13", "13"), ("Omega13", "23"),
        ("Omega23", "12"), ("Omega23", "13"),
    }
    actual = {(row["curvature_pair"], row["two_form_leg"]) for row in mixed_rows}
    if pivot == "REVERSE":
        assert actual == expected_reverse, (pivot, actual ^ expected_reverse)
    assert len(narrow_rows) == 0 and len(nonzero_pairs) == 6
    return {
        "pivot": pivot,
        "nonzero_lower_curvature_pairs": len(nonzero_pairs),
        "mixed_rows": mixed_rows,
        "mixed_row_count": len(mixed_rows),
        "narrow_leg_aligned_nonzero_count": len(narrow_rows),
    }


def semantic_check(state: dict[str, object]) -> None:
    assert state["headline"] == (
        "SPLIT_RELATIVE_FIRST_CARTAN_CONTACT_ENCODING_DERIVED__PRIMITIVE_SELECTION_AND_COMPLETE_FRAME_NATURALITY_OPEN"
    )
    assert state["branch_scope"] == "WITHIN_FROZEN_29_SOURCE_AUTHORITY_SET"
    assert state["contact_log_uses_T0"] is True
    assert state["m_ruling"].startswith("mC_HOMOGENEOUS")
    assert state["forward_mixed_rows"] == state["reverse_mixed_rows"] == 12
    assert state["forward_narrow_rows"] == state["reverse_narrow_rows"] == 0
    assert state["wording"] == "ENCODES_AND_RECONSTRUCTS_NOT_NEW_LAW"


def catch_proofs(base: dict[str, object]) -> list[dict[str, str]]:
    mutations = (
        ("C01", "zero_full_mixed_claim", lambda x: x.update(forward_mixed_rows=0)),
        ("C02", "missing_reverse_pivot", lambda x: x.update(reverse_mixed_rows="UNTESTED")),
        ("C03", "nonzero_narrow_hidden", lambda x: x.update(reverse_narrow_rows=1)),
        ("C04", "m_called_mixed", lambda x: x.update(m_ruling="m_MIXES_WITH_L1")),
        ("C05", "production_law_promotion", lambda x: x.update(wording="PRODUCES_NEW_RESPONSE_LAW")),
        ("C06", "branch_scope_globalized", lambda x: x.update(branch_scope="REPOSITORY_WIDE_EXHAUSTIVE")),
        ("C07", "dimension_reference_removed", lambda x: x.update(contact_log_uses_T0=False)),
        ("C08", "complete_frame_promotion", lambda x: x.update(headline="OBSERVER_NATURAL_RESPONSE_DERIVED")),
    )
    output = []
    for catch_id, name, mutation in mutations:
        state = copy.deepcopy(base)
        mutation(state)
        caught = False
        try:
            semantic_check(state)
        except AssertionError:
            caught = True
        assert caught
        output.append({"catch_id": catch_id, "mutation": name, "result": "PASS_CAUGHT"})
    return output


def main() -> None:
    identity = verify_sources_and_parent()
    contact = corrected_contact_algebra()
    gauge = gauge_algebra()
    forward = curvature_census("FORWARD")
    reverse = curvature_census("REVERSE")
    forward_ids = {(row["curvature_pair"], row["two_form_leg"]) for row in forward["mixed_rows"]}
    reverse_ids = {(row["curvature_pair"], row["two_form_leg"]) for row in reverse["mixed_rows"]}
    assert forward_ids != reverse_ids

    with (HERE / "CORRECTED_CURVATURE_MIXED_CENSUS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, delimiter="\t",
            fieldnames=["pivot", "curvature_pair", "two_form_leg", "mixed_monomials", "expression"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(forward["mixed_rows"] + reverse["mixed_rows"])

    state = {
        "headline": "SPLIT_RELATIVE_FIRST_CARTAN_CONTACT_ENCODING_DERIVED__PRIMITIVE_SELECTION_AND_COMPLETE_FRAME_NATURALITY_OPEN",
        "branch_scope": "WITHIN_FROZEN_29_SOURCE_AUTHORITY_SET",
        "contact_log_uses_T0": True,
        "m_ruling": gauge["ruling"],
        "forward_mixed_rows": forward["mixed_row_count"],
        "reverse_mixed_rows": reverse["mixed_row_count"],
        "forward_narrow_rows": forward["narrow_leg_aligned_nonzero_count"],
        "reverse_narrow_rows": reverse["narrow_leg_aligned_nonzero_count"],
        "wording": "ENCODES_AND_RECONSTRUCTS_NOT_NEW_LAW",
    }
    semantic_check(state)
    catches = catch_proofs(state)
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["catch_id", "mutation", "result"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)

    result = {
        "schema": "udt-complete-cell-cartan-cold-review-correction-1.0",
        "status": "PASS_AFTER_REQUIRED_CORRECTIONS",
        "identity": identity,
        "contact_algebra": contact,
        "gauge_algebra": gauge,
        "curvature": {
            "forward": {key: value for key, value in forward.items() if key != "mixed_rows"},
            "reverse": {key: value for key, value in reverse.items() if key != "mixed_rows"},
            "mixed_identity_set_same": False,
            "forward_mixed_row_identities": [
                f"{row['curvature_pair']}[{row['two_form_leg']}]" for row in forward["mixed_rows"]
            ],
            "reverse_mixed_row_identities": [
                f"{row['curvature_pair']}[{row['two_form_leg']}]" for row in reverse["mixed_rows"]
            ],
            "forward_only_identities": sorted(f"{a}[{b}]" for a, b in forward_ids-reverse_ids),
            "reverse_only_identities": sorted(f"{a}[{b}]" for a, b in reverse_ids-forward_ids),
            "raw_monomial_attribution": "CLOSURE_NORMAL_FORM_DEPENDENT",
            "tensorial_mixed_curvature_nogo": "NOT_DERIVED",
        },
        "corrected_state": state,
        "catch_proofs": len(catches),
        "parent_package_modified": False,
    }
    with (HERE / "CORRECTION_RESULT.json").open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
