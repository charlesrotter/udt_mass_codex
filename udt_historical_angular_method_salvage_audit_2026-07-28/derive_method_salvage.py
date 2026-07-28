#!/usr/bin/env python3
"""Exact algebra and complete historical-method census for the salvage audit."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "fa77ce28c8b5b83e7a6d5a92df2e684b62bb60e6"
DOC = "udt_canonical_geometry.md"
SECTION_RANGES = [
    (2187, 2420, "lepton_angular"),
    (2420, 2564, "hadron_assignment"),
    (2662, 2797, "boson_force_mapping"),
    (2797, 2902, "structural_constants"),
    (3141, 3164, "rank2_qcd_claim"),
    (3164, 3961, "exterior_mixing_quark_nuclear"),
    (3961, 4053, "multiplicity_web"),
    (5875, 6045, "translation_cluster"),
]


def git(*args: str, binary: bool = False):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if result.returncode:
        message = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise RuntimeError(message)
    return result.stdout


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def vec(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(list(matrix))


def rank(matrices: list[sp.Matrix]) -> int:
    return sp.Matrix.hstack(*(vec(matrix) for matrix in matrices)).rank()


def in_span(matrix: sp.Matrix, basis: list[sp.Matrix]) -> bool:
    return rank(basis + [matrix]) == rank(basis)


def commutator(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left * right - right * left


def is_skew(matrix: sp.Matrix) -> bool:
    return matrix.T == -matrix and sp.trace(matrix) == 0


def is_symmetric_traceless(matrix: sp.Matrix) -> bool:
    return matrix.T == matrix and sp.trace(matrix) == 0


def matrix_unit(n: int, i: int, j: int) -> sp.Matrix:
    result = sp.zeros(n)
    result[i, j] = 1
    return result


def real_traceless_basis(n: int) -> tuple[list[sp.Matrix], list[sp.Matrix]]:
    skew = [matrix_unit(n, i, j) - matrix_unit(n, j, i) for i in range(n) for j in range(i + 1, n)]
    symmetric = [matrix_unit(n, i, j) + matrix_unit(n, j, i) for i in range(n) for j in range(i + 1, n)]
    symmetric.extend(
        sp.diag(*([1] * i + [-i] + [0] * (n - i - 1)))
        for i in range(1, n)
    )
    return skew, symmetric


def trace_gram(basis: list[sp.Matrix]) -> sp.Matrix:
    return sp.Matrix([[sp.trace(left * right) for right in basis] for left in basis])


def inertia_symmetric(matrix: sp.Matrix) -> tuple[int, int, int]:
    eigenvalues = matrix.eigenvals()
    positive = negative = zero = 0
    for value, multiplicity in eigenvalues.items():
        sign = sp.signsimp(value)
        if sign.is_positive:
            positive += multiplicity
        elif sign.is_negative:
            negative += multiplicity
        elif sign == 0:
            zero += multiplicity
        else:
            raise AssertionError(f"undetermined sign {value}")
    return positive, negative, zero


def verify_manifest(name: str) -> int:
    rows = list(csv.DictReader((HERE / name).open(encoding="utf-8"), delimiter="\t"))
    for row in rows:
        payload = git("show", f"{BASE}:{row['path']}", binary=True)
        assert str(git("rev-parse", f"{BASE}:{row['path']}")).strip() == row["blob"]
        assert digest(payload) == row["sha256"] and len(payload) == int(row["size_bytes"])
    return len(rows)


def reference_census(document: str) -> list[dict[str, object]]:
    lines = document.splitlines()
    base_paths = str(git("ls-tree", "-r", "--name-only", BASE)).splitlines()
    history_paths = sorted({
        line.split(" ", 1)[1]
        for line in str(git("rev-list", "--objects", "--all")).splitlines()
        if " " in line
    })
    by_basename: dict[str, list[str]] = {}
    for path in base_paths:
        by_basename.setdefault(Path(path).name, []).append(path)
    history_by_basename: dict[str, list[str]] = {}
    for path in history_paths:
        history_by_basename.setdefault(Path(path).name, []).append(path)
    pattern = re.compile(r"[A-Za-z0-9_./-]+\.(?:md|py|json|txt|csv|tsv|npz|ipynb)")
    found: dict[str, dict[str, object]] = {}
    for start, end, section in SECTION_RANGES:
        for line_number in range(start, min(end, len(lines)) + 1):
            for reference in pattern.findall(lines[line_number - 1]):
                item = found.setdefault(reference, {"lines": [], "sections": set()})
                item["lines"].append(line_number)
                item["sections"].add(section)
    rows = []
    for reference, item in sorted(found.items()):
        exact = reference if reference in base_paths else ""
        matches = by_basename.get(Path(reference).name, [])
        if exact:
            base_status, base_resolved = "TRACKED_EXACT", exact
        elif len(matches) == 1:
            base_status, base_resolved = "TRACKED_BASENAME_ONLY", matches[0]
        elif len(matches) > 1:
            base_status, base_resolved = "AMBIGUOUS_BASENAME", ";".join(matches)
        else:
            base_status, base_resolved = "ABSENT_AT_BASE", "-"
        history_exact = reference if reference in history_paths else ""
        history_matches = history_by_basename.get(Path(reference).name, [])
        if history_exact:
            history_status, history_resolved = "TRACKED_EXACT_IN_HISTORY", history_exact
        elif len(history_matches) == 1:
            history_status, history_resolved = "TRACKED_BASENAME_IN_HISTORY", history_matches[0]
        elif len(history_matches) > 1:
            history_status, history_resolved = "AMBIGUOUS_BASENAME_IN_HISTORY", ";".join(history_matches)
        else:
            history_status, history_resolved = "MISSING_FROM_ALL_GIT_HISTORY", "-"
        rows.append({
            "literal_reference": reference,
            "first_line": min(item["lines"]),
            "occurrences": len(item["lines"]),
            "sections": ";".join(sorted(item["sections"])),
            "base_tracking_status": base_status,
            "base_resolved_path": base_resolved,
            "history_resolution_status": history_status,
            "history_resolved_path": history_resolved,
        })
    return rows


def method_rows() -> list[dict[str, object]]:
    raw = [
        ("M01", "13.2", "S2 average <cos^2>=1/3", "round S2 measure", "none", "PURE_MATH_REUSABLE_CONDITIONAL", "valid identity; carrier and physical role supplied"),
        ("M02", "13.2", "multiply S2 average by angular half-period pi to define mu^2", "M01", "choice of half-period and mass interpretation", "EMPIRICAL_NUMEROLOGY", "product is not forced by the average"),
        ("M03", "13.3", "rank-1 tensor matrix elements between spinor harmonics", "round S2 plus spinor harmonics", "Dirac/spinor carrier", "PURE_MATH_REUSABLE_CONDITIONAL", "Wigner-Eckart selection rule is mathematical; UDT carrier is not derived"),
        ("M04", "13.4", "multiply coupling by j-ratio and set equal to 4", "M03", "universal constant 4 and equality criterion", "EMPIRICAL_NUMEROLOGY", "selection equation is imposed rather than metric-selected"),
        ("M05", "13.5", "build A_n from closure number 5 and multiplicities", "small integer labels", "closure-channel assignment", "EMPIRICAL_NUMEROLOGY", "coefficient prescription lacks an operator"),
        ("M06", "13.6", "Gaussian complex-mode measure gives pi^d", "complex amplitudes", "Fock/Gaussian quantization", "IMPORTED_COMPARISON_ONLY", "document itself retracts this as a smuggled import"),
        ("M07", "13.7-13.10", "assign particle-dependent pi powers and coefficients", "M05-M06", "particle labels and exponent assignment", "EMPIRICAL_NUMEROLOGY", "labels choose different rules; computation sources absent"),
        ("M08", "13.10", "symmetric occupation count binomial(9,3)=84", "finite-dimensional combinatorics", "bosonic occupation and physical 7-orbit", "PURE_MATH_REUSABLE_CONDITIONAL", "count is exact but no native operator produces it"),
        ("M09", "13.10;26", "Diophantine equality of two dimension counts", "multiplicity dimensions", "equality/self-consistency criterion", "NATIVE_METHOD_LEAD_REQUIRES_REDERIVATION", "Pell arithmetic is exact; representation decompositions are not isomorphic"),
        ("M10", "13.11", "Brannen/Koide Z3 orbit parametrization", "three-component mass vector", "imported empirical parametrization; phase choice", "IMPORTED_COMPARISON_ONLY", "l=1 degeneracy does not select a unique Z3 orbit or phase"),
        ("M11", "14", "match radial eigenvalue ladders to named hadrons", "chosen Dirac cavity spectrum", "PDG labels; two domains; Neumann boundary", "HISTORICAL_RESULT_ONLY", "document admits density/look-elsewhere and underived mapping"),
        ("M12", "14.9;16.4", "interpret kappa magnitude/sign/step as color/charge/flavor", "Dirac kappa label", "Standard Model role assignment", "IMPORTED_COMPARISON_ONLY", "analogy is not an operator derivation"),
        ("M13", "18.6", "close rank-1 rotations plus rank-2 traceless tensors", "finite-dimensional angular operator space", "complex/Hermitian structure for compact real form", "PURE_MATH_REUSABLE_CONDITIONAL", "exact generated-algebra method; physical gauge interpretation imported"),
        ("M14", "19.1-19.2", "use exterior powers and Hodge duality on R9", "exterior algebra", "9d base; EM and particle channel assignments", "PURE_MATH_REUSABLE_CONDITIONAL", "identities exact; physical channels not derived"),
        ("M15", "19.3-19.5", "recognize numerical radial outputs as simple rational/pi bridge values", "computed eigenvalues and sources", "target algebraic forms", "HISTORICAL_RESULT_ONLY", "near-matches are not established identities; scripts absent"),
        ("M16", "19.5b;19.7-19.8a", "form bilinear and vertex partition fractions", "small multiplicity dimensions", "field-count powers and physical mixing labels", "EMPIRICAL_NUMEROLOGY", "dimension partitions are assigned to desired observables"),
        ("M17", "19.8b", "generate quark ratios from 2pi^2 times rotating sector factors", "small integers and pi", "quark labels and searched prescription", "EMPIRICAL_NUMEROLOGY", "document states coefficients were found by search; Gaussian factor is imported"),
        ("M18", "19.8", "map small rational fractions to CP phases and hierarchy parameters", "M16 fractions", "trigonometric mapping and empirical labels", "EMPIRICAL_NUMEROLOGY", "mapping function is selected after the observable"),
        ("M19", "19.9", "insert angular formulas into nuclear/Goldberger-Treiman/CVC machinery", "historical angular coefficients", "imported nuclear relations and potentials", "IMPORTED_COMPARISON_ONLY", "external dynamics are load-bearing"),
        ("M20", "19.10", "interpret partial radial integral as QCD running and cavity boundary as confinement", "radial integral and boundary", "QCD scale/running interpretation", "IMPORTED_COMPARISON_ONLY", "monotone accumulation is not a beta function"),
        ("M21", "20", "reuse multiplicities 2,3,5,7 across many named observables", "small integer vocabulary", "large target and formula choice space", "EMPIRICAL_NUMEROLOGY", "multiplicity web has severe look-elsewhere exposure"),
        ("M22", "26", "V2+V4+V7 dimension/representation/orbit translation cluster", "endomorphism dimensions and combinatorics", "GR matter substrate and unproved joins", "MIXED_MULTIPLE_METHOD_CLASSES", "valid algebra is combined with open dimension-equality and physical maps"),
        ("M23", "current cross-map", "decompose complete screen endomorphism into trace rotation and shear", "current metric-derived screen plus coframe response", "no physical coefficient or dynamics", "NATIVE_EXACT_REDERIVED_BOUNDED", "current owner reports supply the object; exact algebra below supplies the method"),
    ]
    return [
        {"method_id": row[0], "historical_section": row[1], "operation": row[2],
         "native_or_mathematical_input": row[3], "import_or_free_join": row[4],
         "classification": row[5], "rationale": row[6]}
        for row in raw
    ]


def formula_rows() -> list[dict[str, object]]:
    formulas = [
        ("muon_electron", "20*pi^3/3", 20 * math.pi**3 / 3),
        ("proton_electron", "6*pi^5", 6 * math.pi**5),
        ("proton_muon", "9*pi^2/10", 9 * math.pi**2 / 10),
        ("pion_electron", "84*pi", 84 * math.pi),
        ("strange_down", "2*pi^2", 2 * math.pi**2),
        ("charm_up", "6*pi^4", 6 * math.pi**4),
        ("bottom_strange", "9*pi^2/2", 9 * math.pi**2 / 2),
        ("top_charm", "14*pi^2", 14 * math.pi**2),
        ("pmns_12", "4/13", 4 / 13),
        ("pmns_23", "4/7", 4 / 7),
        ("pmns_13", "1/45", 1 / 45),
        ("weinberg", "3/13", 3 / 13),
        ("cabibbo", "9/40", 9 / 40),
    ]
    return [
        {"historical_label": label, "formula": formula, "numeric_replay": f"{value:.12g}",
         "audit_status": "ARITHMETIC_REPRODUCED_NOT_NATIVE_VALIDATION"}
        for label, formula, value in formulas
    ]


def main() -> None:
    fixed_sources = verify_manifest("SOURCE_MANIFEST.tsv")
    supplemental_sources = verify_manifest("SUPPLEMENTAL_SOURCE_MANIFEST.tsv")
    document_bytes = git("show", f"{BASE}:{DOC}", binary=True)
    document = document_bytes.decode("utf-8")
    write_tsv("SECTION_SCOPE.tsv", [
        {
            "start_line": start,
            "end_line": end,
            "section_key": section,
            "selection_rule": "REGISTERED_ANGULAR_RATIO_HIERARCHY_MULTIPLET_CHARGE_SPECTRUM_QCD_OR_MASS_METHOD_SPAN",
        }
        for start, end, section in SECTION_RANGES
    ])
    references = reference_census(document)
    write_tsv("TRANSITIVE_REFERENCE_CENSUS.tsv", references)
    methods = method_rows()
    write_tsv("HISTORICAL_METHOD_CENSUS.tsv", methods)
    write_tsv("FORMULA_REPLAY.tsv", formula_rows())

    dimension_rows = []
    for n in range(2, 7):
        skew, symmetric = real_traceless_basis(n)
        basis = skew + symmetric
        assert rank(basis) == n * n - 1
        assert all(is_skew(commutator(left, right)) for left in skew for right in skew)
        assert all(is_symmetric_traceless(commutator(left, right)) for left in skew for right in symmetric)
        assert all(is_skew(commutator(left, right)) for left in symmetric for right in symmetric)
        dimension_rows.append({
            "n": n, "rotation_dim": len(skew), "symmetric_traceless_dim": len(symmetric),
            "total_traceless_dim": len(basis), "n_squared_minus_one": n * n - 1,
            "real_algebra": f"sl({n},R)",
        })
    write_tsv("DIMENSION_GENERALIZATION.tsv", dimension_rows)

    r = sp.Matrix([[0, -1], [1, 0]])
    s1 = sp.diag(1, -1)
    s2 = sp.Matrix([[0, 1], [1, 0]])
    screen_basis = [r, s1, s2]
    screen_names = ["R", "S1", "S2"]
    bracket_rows = []
    for i in range(3):
        for j in range(i + 1, 3):
            bracket = commutator(screen_basis[i], screen_basis[j])
            coordinates = sp.Matrix.hstack(*(vec(item) for item in screen_basis)).gauss_jordan_solve(vec(bracket))[0]
            bracket_rows.append({
                "left": screen_names[i], "right": screen_names[j],
                "coefficient_R": coordinates[0], "coefficient_S1": coordinates[1],
                "coefficient_S2": coordinates[2],
            })
    write_tsv("SCREEN_BRACKET_TABLE.tsv", bracket_rows)
    screen_inertia = inertia_symmetric(trace_gram(screen_basis))

    skew3, sym3 = real_traceless_basis(3)
    basis3 = skew3 + sym3
    real_inertia = inertia_symmetric(trace_gram(basis3))
    compact3 = skew3 + [sp.I * item for item in sym3]
    compact_gram = sp.Matrix([[-sp.re(sp.trace(left * right)) for right in compact3] for left in compact3])
    compact_inertia = inertia_symmetric(compact_gram)
    assert rank(basis3) == 8
    assert all(in_span(commutator(left, right), basis3) for left in basis3 for right in basis3)
    assert all(in_span(commutator(left, right), compact3) for left in compact3 for right in compact3)

    tensor_rank_rows = []
    for ell in range(1, 6):
        ranks = list(range(1, 2 * ell + 1))
        total = sum(2 * k + 1 for k in ranks)
        tensor_rank_rows.append({
            "ell": ell, "representation_dimension": 2 * ell + 1,
            "tensor_ranks": ";".join(map(str, ranks)), "traceless_operator_dimension": total,
            "dimension_squared_minus_one": (2 * ell + 1) ** 2 - 1,
        })
    write_tsv("SPHERICAL_TENSOR_GENERALIZATION.tsv", tensor_rank_rows)

    ownership = [
        {"object": "reciprocal_depth", "algebraic_slot": "additive_scalar_cocycle", "owner": "OBSERVER_COMPARISON", "status": "DERIVED_TYPE_PHYSICAL_BASE_OPEN"},
        {"object": "screen_rotation", "algebraic_slot": "so(2)", "owner": "COFRAME_PATH_TRANSPORT", "status": "EXACT_GIVEN_PATH"},
        {"object": "lambda_identity_response", "algebraic_slot": "R_I", "owner": "METRIC_REALIZATION_SCREEN_TRACE", "status": "OPEN_VALUE"},
        {"object": "two_shape_components", "algebraic_slot": "Sym0(2)", "owner": "METRIC_REALIZATION_SCREEN_SHAPE", "status": "OPEN_RESPONSE"},
        {"object": "pair_screen_mixing", "algebraic_slot": "off_diagonal_blocks", "owner": "COMPLETE_METRIC_REALIZATION", "status": "OPEN_RESPONSE"},
        {"object": "complete_screen_generator", "algebraic_slot": "gl(2,R)", "owner": "REALIZATION_PLUS_COFRAME_TRANSPORT", "status": "TYPE_AVAILABLE_NOT_SELECTED"},
        {"object": "action_source_dynamics", "algebraic_slot": "not_fixed_by_closure", "owner": "DOWNSTREAM_PHYSICS", "status": "OPEN"},
    ]
    write_tsv("OWNERSHIP_CROSSWALK.tsv", ownership)

    missing = sum(row["history_resolution_status"] == "MISSING_FROM_ALL_GIT_HISTORY" for row in references)
    reference_status_counts: dict[str, int] = {}
    for row in references:
        status = str(row["history_resolution_status"])
        reference_status_counts[status] = reference_status_counts.get(status, 0) + 1
    classifications: dict[str, int] = {}
    for row in methods:
        classifications[row["classification"]] = classifications.get(row["classification"], 0) + 1
    output = {
        "schema": "udt-historical-angular-method-salvage-1.0",
        "primary_outcome": "MIXED_MULTIPLE_METHOD_CLASSES",
        "method_lead": "CURRENT_SCREEN_OPERATOR_METHOD_LEAD",
        "historical_physics_restored": False,
        "fixed_sources_replayed": fixed_sources,
        "supplemental_sources_replayed": supplemental_sources,
        "historical_document_sha256": digest(document_bytes),
        "historical_methods": len(methods),
        "method_class_counts": classifications,
        "transitive_references": len(references),
        "missing_transitive_references": missing,
        "transitive_reference_status_counts": reference_status_counts,
        "screen_endomorphism_dimension": 4,
        "screen_traceless_algebra": "sl(2,R)",
        "screen_trace_form_inertia": screen_inertia,
        "three_dimensional_real_algebra": "sl(3,R)",
        "three_dimensional_real_trace_form_inertia": real_inertia,
        "three_dimensional_compact_algebra": "su(3)_ONLY_AFTER_COMPLEX_HERMITIAN_CHOICE",
        "three_dimensional_compact_form_inertia": compact_inertia,
        "old_3_plus_5_unique": False,
        "lambda_is_complete_screen_response": False,
        "compute": {"backend": "CPU_SYMBOLIC", "gpu_work_performed": False},
        "authority_boundary": {
            "historical_particle_or_gauge_claim_restored": False,
            "lambda_or_branch_selected": False,
            "action_source_carrier_boundary_or_density_selected": False,
            "ode_pde_time_live_or_gpu_work_launched": False,
            "canon_changed": False,
            "repository_reorganization_performed": False,
        },
        "maximum_conclusion": "OPERATOR_ALGEBRA_METHOD_SALVAGED;_CURRENT_SCREEN_DECOMPOSITION_SHARPENS_OWNERSHIP;_NO_HISTORICAL_PARTICLE_OR_GAUGE_CLAIM_RESTORED",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
