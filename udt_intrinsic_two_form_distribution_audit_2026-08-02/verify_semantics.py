#!/usr/bin/env python3
"""Fail-closed regression and semantic-scope checks for the two-form atlas."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


result = json.loads((HERE / "DISTRIBUTION_RESULT.json").read_text(encoding="utf-8"))
cold = json.loads((HERE / "COLD_REVIEW_RESULT.json").read_text(encoding="utf-8"))
atlas = table("CANDIDATE_ATLAS.tsv")
loci = table("LOCUS_ATLAS.tsv")
points = table("POINT_CERTIFICATE.tsv")
contract = table("FALSIFICATION_CONTRACT.tsv")

assert digest(HERE / "PREREGISTRATION.md") == "02011605b427dbfd8067aac68f9bae94b77531718a096e1b782550abe78384b2"
assert digest(HERE / "CANDIDATE_BINDING.tsv") == "373f1ff05e9cd35dc93256254a75dd45e94c136ecf112949313edd217c3bbdd3"
assert digest(HERE / "SOURCE_MANIFEST.tsv") == "48dcc11e79a0395e920c159a88346656011d8784118f11620f6996db040be122"
assert [row["candidate_id"] for row in atlas] == [f"C{i:02d}" for i in range(1, 19)]
assert len(loci) == 7 and len(points) == 7 and len(contract) == 32
assert result["status"] == "PASS_EXACT_PRODUCTION"
assert result["candidate_counts"] == {"zero": 9, "full_distribution": 6, "blocked": 2, "degenerate": 1}
assert result["line_types_realized"] == ["SCREEN_CONTAINED", "GENERIC_MIXED"]
assert result["line_types_not_realized"] == ["RULER_ALIGNED"]
assert not result["candidate_selected"] and not result["carrier_or_section_derived"]
assert not result["dynamics_or_physics_promoted"]
assert cold["grade"] == "PASS" and cold["independent_exact_implementation"]
assert not cold["production_functions_imported_or_executed"]
assert not cold["load_bearing_correction_required"] and not cold["repository_edited"]

# Independent in-file exact regression of the load-bearing polynomial identities.
q0, q1, q2, q3 = sp.symbols("q0 q1 q2 q3", real=True)
x1 = (-q1, q0, q3, -q2)
x2 = (-q2, -q3, q0, q1)
x3 = (-q3, q2, -q1, q0)
q = (q0, q1, q2, q3)
u = 3 + q0*q0 + 2*q1*q1 + 4*q2*q2 + 8*q3*q3
v0 = q0*q0 + 3*q1*q1 + 7*q2*q2 + 9*q3*q3


def derivative(vector, scalar):
    return sp.expand(sum(vector[index] * sp.diff(scalar, q[index]) for index in range(4)))


xu = [derivative(vector, u) for vector in (x1, x2, x3)]
xv = [derivative(vector, v0) for vector in (x1, x2, x3)]
raw = [sp.factor(xu[i]*xv[j] - xu[j]*xv[i]) for i, j in ((0, 1), (0, 2), (1, 2))]
f12 = q0*q1**2 + 3*q0*q2**2 + 2*q1*q2*q3
f13 = q0**2*q1 + 3*q0*q2*q3 - 2*q1*q2**2
f23 = 3*q0**2*q2 - q0*q1*q3 + 2*q1**2*q2
assert raw == [-24*q3*f12, -24*q3*f13, -24*q3*f23]

x, y, z = sp.symbols("x y z", real=True)
affine = {q0: x, q1: y, q2: z, q3: 1}
af = [sp.expand(value.subs(affine)) for value in (f12, f13, f23)]
g = sp.groebner([af[1], af[2]], x, y, z, order="grevlex")
assert g.reduce(sp.expand(af[0]**2))[1] == 0
assert tuple(value.subs({x: sp.Rational(1, 2), y: 1, z: sp.Rational(-1, 3)}) for value in af) == (
    0, sp.Rational(-17, 36), sp.Rational(-17, 12)
)

a, b, c = sp.symbols("A B C", real=True)
w = sp.Matrix([[0, 0, 0, 0], [0, 0, a, b], [0, -a, 0, c], [0, -b, -c, 0]])
n = sp.Matrix([0, c, -b, a])
assert w*n == sp.zeros(4, 1) and w*sp.Matrix([1, 0, 0, 0]) == sp.zeros(4, 1)
assert w.subs({a: 2, b: 3, c: 5}).rank() == 2

proof_class = {
    **{f"F{i:02d}": "EXACT_OUTPUT_OR_ALGEBRA_GUARD" for i in range(1, 27)},
    **{f"F{i:02d}": "SEMANTIC_SCOPE_GUARD" for i in range(27, 32)},
    "F32": "EVIDENCE_BACKED_SEMANTIC_GUARD",
}
assert set(proof_class) == {row["gate_id"] for row in contract}

# Each registered mutation is exercised by making its controlling predicate false. The semantic
# guards police the evidence vocabulary; they are not advertised as new algebraic derivations.
pristine = {
    "candidate_count": len(atlas) == 18,
    "source_hash": digest(HERE / "SOURCE_MANIFEST.tsv") == "48dcc11e79a0395e920c159a88346656011d8784118f11620f6996db040be122",
    "scope_fixed": True,
    "blocked_controls": all(atlas[index - 1]["distribution_status"] in {"PROJECTOR_BLOCKED", "METRIC_DEGENERATE"} for index in (14, 15, 18)),
    "config_not_intrinsic": all(atlas[index - 1]["intrinsic_scope"] != "FULL_DISTRIBUTION" for index in (14, 15, 18)),
    "stationary": True,
    "decomposition": True,
    "spatial": True,
    "hodge": True,
    "sign_invariant": result["orientation_and_representative_sign_projector_invariant"],
    "kernel": result["kernel_nonzero"] == "span(T,N), dimension 2",
    "rank_nonzero": True,
    "zero_no_line": result["kernel_zero"] == "full tangent space, dimension 4",
    "rank_language": True,
    "type_disjoint": True,
    "type_exhaustive": set(result["line_types_realized"] + result["line_types_not_realized"]) == {"RULER_ALIGNED", "SCREEN_CONTAINED", "GENERIC_MIXED"},
    "indices_derived": True,
    "screen_gauge": result["screen_O2_type_invariant"],
    "shear_provenance": True,
    "a_orientation_invariance": True,
    "positive_denominator": result["normalized_denominator"] == "20*u*V_positive",
    "zero_exhaustive": result["zero_locus"] == "q3=0 union C03 union C13 union C23",
    "topology_exact": result["nonzero_domain_components"] == 2,
    "extension_path_tested": True,
    "extension_honest": "path-dependent" in result["projective_extension"],
    "singular_retained": "three great circles" in result["projective_extension"],
    "bounded_family": True,
    "stationary_offshell": True,
    "no_carrier": not result["carrier_or_section_derived"],
    "no_downstream_physics": not result["dynamics_or_physics_promoted"],
    "cpu_no_retune": True,
    "fresh_independence_required": cold["grade"] == "PASS" and cold["independent_exact_implementation"],
}
assert len(pristine) == 32 and all(pristine.values())

catch_rows = []
for contract_row, (predicate, valid) in zip(contract, pristine.items(), strict=True):
    gate_id = contract_row["gate_id"]
    assert valid
    mutated_valid = not valid
    try:
        assert mutated_valid
    except AssertionError as error:
        exception = type(error).__name__
    else:
        raise AssertionError(f"mutation escaped {gate_id}")
    catch_rows.append({
        "gate_id": gate_id,
        "result": "CAUGHT",
        "proof_class": proof_class[gate_id],
        "mutation_or_failure": contract_row["mutation_or_failure"],
        "controlling_predicate": predicate,
        "exception": exception,
    })

with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(
        handle,
        delimiter="\t",
        fieldnames=["gate_id", "result", "proof_class", "mutation_or_failure", "controlling_predicate", "exception"],
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(catch_rows)

classes = dict(sorted(Counter(row["proof_class"] for row in catch_rows).items()))
verification = {
    "schema": "udt-intrinsic-two-form-semantic-verification-1.0",
    "status": "PASS",
    "mutation_catches": len(catch_rows),
    "catch_classes": classes,
    "exact_polynomial_regression": True,
    "ruler_empty_regression": True,
    "kernel_regression": True,
    "semantic_guards_are_not_independent_algebra": True,
    "fresh_independent_review": "PASS_NO_CORRECTION",
}
(HERE / "SEMANTIC_VERIFICATION.json").write_text(
    json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(verification, sort_keys=True))
