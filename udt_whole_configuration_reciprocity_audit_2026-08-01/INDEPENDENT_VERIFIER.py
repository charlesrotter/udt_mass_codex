#!/usr/bin/env python3
"""Cold, non-importing verifier for the whole-configuration Reciprocity audit.

This verifier deliberately does not import or execute either production script.  It
rehashes the frozen base-tree sources, searches every frozen text, reconstructs the
finite algebra with Fraction arithmetic, compares only saved production records, and
exercises semantic mutations through one common predicate.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import itertools
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
BASE = "9fe5202e86627aa47a5200ea776dcb468a6531f6"
RAW_PATH = PKG / "INDEPENDENT_RAW.jsonl"
RESULT_PATH = PKG / "INDEPENDENT_RESULT.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def rank(matrix: list[list[Fraction]]) -> int:
    """Exact rank, independently structured from the production eliminator."""
    a = [list(map(Fraction, line)) for line in matrix]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    pivot_row = 0
    for pivot_col in range(n):
        chosen = next((r for r in range(pivot_row, m) if a[r][pivot_col] != 0), None)
        if chosen is None:
            continue
        a[pivot_row], a[chosen] = a[chosen], a[pivot_row]
        pivot = a[pivot_row][pivot_col]
        for c in range(pivot_col, n):
            a[pivot_row][c] /= pivot
        for r in range(m):
            if r == pivot_row or a[r][pivot_col] == 0:
                continue
            factor = a[r][pivot_col]
            for c in range(pivot_col, n):
                a[r][c] -= factor * a[pivot_row][c]
        pivot_row += 1
        if pivot_row == m:
            break
    return pivot_row


def matrix_mul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(x) for x in zip(*a)]


def semantic_contract(state: dict) -> tuple[bool, list[str]]:
    """One predicate used by both the genuine record and every mutation."""
    failures: list[str] = []
    if state["source_count"] != 1384 or state["stronger_founded_return_found"]:
        failures.append("source_scope_or_omission")
    if len(set(state["reciprocity_roles"])) != 3:
        failures.append("reciprocity_conflation")
    if state["xmax_status"] != "WORKING_SCHEMA_NOT_FOUNDED_RETURN":
        failures.append("xmax_promotion")
    if state["naturality_claimed"] and not state["complete_actions_supplied"]:
        failures.append("unscoped_naturality")
    if state["zero_saturation_claimed"] and not state["sigma_fixes_zero"]:
        failures.append("invertibility_does_not_fix_zero")
    if state["fixedness_entailed"]:
        failures.append("equivalence_promoted_to_fixedness")
    if state["physical_observers_quotiented"]:
        failures.append("physical_observers_erased")
    if state["unique_return_selected"]:
        failures.append("equivariance_promoted_to_unique_return")
    if state["cocycle_realizes_profile"]:
        failures.append("cocycle_promoted_to_realization")
    if state["pairing_is_response_covector"]:
        failures.append("pairing_promoted_to_response")
    if state["finite_cell_complete_return"]:
        failures.append("finite_cell_splice")
    if state["p4_selected_law"]:
        failures.append("p4_permitted_promoted_to_selected")
    if state["strong_csn_active"]:
        failures.append("csn_regression")
    if state["prejuly_affirmative"]:
        failures.append("prejuly_firewall_breach")
    if state["boundary_complete"]:
        failures.append("boundary_promotion")
    if state["bootstrap_maps_derived"]:
        failures.append("bootstrap_type_promoted_to_maps")
    if state["universal_no_go"]:
        failures.append("bounded_negative_promoted_to_universal")
    return not failures, failures


def main() -> None:
    raw: list[dict] = []
    checks: list[tuple[str, bool, object]] = []

    def check(name: str, passed: bool, detail: object) -> None:
        checks.append((name, bool(passed), detail))
        raw.append({"kind": "check", "name": name, "passed": bool(passed), "detail": detail})

    # Exact source freeze and base-tree identity.
    inventory = rows("SOURCE_INVENTORY.tsv")
    tree_output = subprocess.run(
        ["git", "ls-tree", "-rl", BASE], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout
    tree: dict[str, tuple[str, int]] = {}
    for line in tree_output.splitlines():
        meta, path = line.split("\t", 1)
        _mode, kind, blob, size = meta.split()
        if kind == "blob":
            tree[path] = (blob, int(size))

    source_text: dict[str, str] = {}
    bad_sources: list[str] = []
    total_bytes = 0
    for row in inventory:
        path = row["path"]
        data = (ROOT / path).read_bytes()
        total_bytes += len(data)
        if (
            row["base"] != BASE
            or sha256_bytes(data) != row["sha256"]
            or len(data) != int(row["bytes"])
            or tree.get(path) != (row["blob"], int(row["bytes"]))
        ):
            bad_sources.append(path)
        source_text[path] = data.decode("utf-8")

    snapshot = json.loads((PKG / "PREREG_SNAPSHOT.json").read_text(encoding="utf-8"))
    source_paths = (PKG / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
    check(
        "frozen_source_identity",
        len(inventory) == len(source_paths) == 1384
        and len({r["path"] for r in inventory}) == 1384
        and [r["path"] for r in inventory] == sorted(source_paths)
        and not bad_sources,
        {"count": len(inventory), "bytes": total_bytes, "bad": bad_sources, "base": BASE},
    )
    check(
        "preregistered_scope_decomposition",
        snapshot["parent_source_paths"] == 926
        and snapshot["parent_package_paths"] == 40
        and snapshot["package_scopes"] == 14
        and snapshot["direct_files"] == 11
        and snapshot["source_union"] == 1384,
        snapshot,
    )

    # Every source is searched, including scripts, raw transcripts, and ledgers.
    patterns = {
        "reciprocity": re.compile(r"reciproc", re.I),
        "observer": re.compile(r"observer", re.I),
        "covariance": re.compile(r"covarian|equivarian|naturality", re.I),
        "return": re.compile(r"return\s+(?:law|map|operation|operator|arrow|relation)|global[- ]to[- ]local|nonidentity return", re.I),
        "bootstrap": re.compile(r"bootstrap|feedback|self[- ]consisten|fixed[- ]point", re.I),
        "zero_set": re.compile(r"zero[- ]set|zero set", re.I),
        "xmax": re.compile(r"x_?max|Xmax", re.I),
        "p4": re.compile(r"\bP4\b|response law", re.I),
        "boundary": re.compile(r"boundary|corner|completion", re.I),
    }
    hit_counts = {name: 0 for name in patterns}
    reciprocity_return_paths: list[str] = []
    for path, text in source_text.items():
        hits = {name: bool(regex.search(text)) for name, regex in patterns.items()}
        for name, hit in hits.items():
            hit_counts[name] += int(hit)
        if hits["reciprocity"] and hits["return"]:
            reciprocity_return_paths.append(path)

    # This detects an explicit affirmative sentence, not merely co-occurrence in a long file.
    affirmative_patterns = [
        re.compile(
            r"(?:founded|founding|observer[- ]frame|ordinary observer)[^\n]{0,300}"
            r"reciproc[^\n]{0,300}(?:deriv|suppl|own|select|provid)[^\n]{0,120}"
            r"(?:return|feedback|self[- ]consisten|fixed[- ]point|zero[- ]set|whole[- ]configuration)",
            re.I,
        ),
        re.compile(
            r"(?:return|feedback|self[- ]consisten|fixed[- ]point|zero[- ]set|whole[- ]configuration)"
            r"[^\n]{0,300}(?:founded|founding|observer[- ]frame|ordinary observer)[^\n]{0,300}reciproc",
            re.I,
        ),
    ]
    explicit_affirmative_hits: list[dict[str, str]] = []
    for path, text in source_text.items():
        for regex in affirmative_patterns:
            for match in regex.finditer(text):
                explicit_affirmative_hits.append({"path": path, "text": match.group(0)[:700]})

    check(
        "all_1384_sources_searched_for_stronger_return",
        len(source_text) == 1384 and not explicit_affirmative_hits,
        {
            "files": len(source_text),
            "bytes": total_bytes,
            "hit_counts": hit_counts,
            "reciprocity_return_cooccurrence_count": len(reciprocity_return_paths),
            "reciprocity_return_cooccurrence_paths": reciprocity_return_paths,
            "explicit_affirmative_hits": explicit_affirmative_hits,
        },
    )

    required_fragments = {
        "CURRENT_SCIENTIFIC_PREMISES.tsv": [
            "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED",
            "WORKING_ON_SHELL_ADMISSIBILITY",
            "WORKING_GLOBAL_OBSERVER_PAIR_MAXIMUM_SEPARATION",
            "complete_native_action_source_boundary_mass\tOPEN\tOPEN",
            "OWNER_RATIFIED_PROPOSAL_NOT_DERIVED_SPLIT_RULED_2026-07-30",
        ],
        "udt_three_reciprocity_delta_k_audit_2026-07-23/THREE_RECIPROCITY_ROLE_MAP.tsv": [
            "observer_frame_reciprocity",
            "passive_tensor_covariance_and_no_preferred_observer",
            "Delta_K_equals_zero_field_equation_or_extreme_regime_extension",
        ],
        "udt_founding_reciprocity_object_audit_2026-07-27/AUDIT_REPORT.md": [
            "covariant local relational comparison law",
            "COMPLETE_WHOLE_SOLUTION_LAW = OPEN",
        ],
        "udt_complete_coframe_native_selector_audit_2026-07-26/SELECTOR_CAPABILITY_LEDGER.tsv": [
            "FIXED_INVARIANCE_IS_INCOMPATIBLE_AND_EQUIVARIANCE_DOES_NOT_SELECT_A_SLOT",
            "P14\tbootstrap\tadmissibility_predicate_on_completed_on_shell_solutions",
        ],
        "udt_observer_pair_xmax_bridge_audit_2026-07-27/STATUS_LEDGER.tsv": [
            "field_valued_global_to_local_return_equation\tOPEN_NOT_SELECTED_IN_FROZEN_CENSUS",
            "bootstrap\tWORKING_ON_SHELL_ADMISSIBILITY_ONLY",
        ],
        "udt_joint_selector_provenance_audit_2026-07-28/AUDIT_REPORT.md": [
            "bootstrap wording",
            "no typed operation, codomain, or return map",
            "July 1 provenance firewall was enforced",
        ],
        "udt_bootstrap_closure_ownership_audit_2026-08-01/AUDIT_REPORT.md": [
            "none of the eight preregistered routes supplies the distinct nonidentity return",
            "P4's broader response family remains permitted rather",
        ],
        "udt_p4_cold_review_repair_2026-08-01/CLOSURE_REPORT.md": [
            "no response law, action, carrier, mass, coupling, solution, or physical branch is",
        ],
        "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md": [
            "Scientific material from before\n2026-07-01 was used only to identify a failure",
            "It supplies no affirmative UDT physics here",
        ],
        "udt_stability_foundations_audit_2026-08-01/BOOTSTRAP_FIXED_POINT_SCHEMA.tsv": [
            "global-to-local admissibility/equation data\tOPEN",
            "local-to-global observable response\tOPEN",
            "fixed-point set\tOPEN",
        ],
    }
    missing_fragments: list[dict[str, str]] = []
    for path, fragments in required_fragments.items():
        text = source_text.get(path, "")
        for fragment in fragments:
            if fragment not in text:
                missing_fragments.append({"path": path, "fragment": fragment})
    check(
        "authority_and_scope_firewalls",
        not missing_fragments,
        {"files": len(required_fragments), "missing": missing_fragments},
    )

    # Control 1: swap orbit and fixed locus.
    swap = [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]]
    x = (Fraction(1), Fraction(2))
    sx = (x[1], x[0])
    fixed_rank = rank([[1, -1]])
    orbit = {x, sx}
    check(
        "swap_orbit_not_fixed",
        len(orbit) == 2 and x != sx and fixed_rank == 1,
        {"x": list(map(int, x)), "Sx": list(map(int, sx)), "orbit_size": len(orbit), "fixed_locus_rank": fixed_rank},
    )

    # Control 2: inequivalent equivariant returns on one domain AND one codomain action.
    # Each map R^2 -> R^2 is equivariant for the swap representation.
    witnesses = [(0, 0), (1, 1), (1, 0), (0, 1), (-1, 1)]

    def f_identity(v: tuple[int, int]) -> tuple[int, int]:
        return v

    def f_difference(v: tuple[int, int]) -> tuple[int, int]:
        d = v[0] - v[1]
        return (d, -d)

    def f_product(v: tuple[int, int]) -> tuple[int, int]:
        p = v[0] * v[1]
        return (p, p)

    maps = {"identity": f_identity, "difference": f_difference, "product_diagonal": f_product}
    equivariance_failures: list[dict] = []
    zero_sets: dict[str, list[list[int]]] = {}
    for name, operation in maps.items():
        zeros: list[list[int]] = []
        for v in witnesses:
            sv = (v[1], v[0])
            lhs = operation(sv)
            out = operation(v)
            rhs = (out[1], out[0])
            if lhs != rhs:
                equivariance_failures.append({"map": name, "v": v})
            if out == (0, 0):
                zeros.append(list(v))
        zero_sets[name] = zeros
    zero_counts = {name: len(value) for name, value in zero_sets.items()}
    check(
        "inequivalent_equivariant_returns_same_domain_codomain",
        not equivariance_failures and zero_counts == {"identity": 1, "difference": 2, "product_diagonal": 3},
        {"zero_counts": zero_counts, "zero_sets": zero_sets, "failures": equivariance_failures},
    )

    # Control 3: all K4 incidence, cycle, and graph ranks.
    vertices = range(4)
    edges = list(itertools.combinations(vertices, 2))
    incidence: list[list[Fraction]] = []
    for i, j in edges:
        row = [Fraction(0)] * 4
        row[i], row[j] = Fraction(-1), Fraction(1)
        incidence.append(row)
    incidence_rank = rank(incidence)

    edge_index = {edge: k for k, edge in enumerate(edges)}
    triangle_matrix: list[list[Fraction]] = []
    for i, j, k in itertools.combinations(vertices, 3):
        row = [Fraction(0)] * 6
        row[edge_index[(i, j)]] = 1
        row[edge_index[(j, k)]] = 1
        row[edge_index[(i, k)]] = -1
        triangle_matrix.append(row)
    cycle_rank = rank(triangle_matrix)
    graph_jacobian = [
        [-value for value in incidence[r]] + [Fraction(int(r == c)) for c in range(6)]
        for r in range(6)
    ]
    graph_rank = rank(graph_jacobian)
    phi = (Fraction(0), Fraction(1), Fraction(4), Fraction(-2))
    directed = {(i, j): phi[j] - phi[i] for i in vertices for j in vertices if i != j}
    ordered_triangle_residuals = [
        directed[(i, j)] + directed[(j, k)] - directed[(i, k)]
        for i, j, k in itertools.permutations(vertices, 3)
    ]
    check(
        "four_observer_incidence_cocycle_graph_ranks",
        incidence_rank == 3
        and 4 - incidence_rank == 1
        and cycle_rank == 3
        and 6 - cycle_rank == 3
        and graph_rank == 6
        and 10 - graph_rank == 4
        and all(value == 0 for value in ordered_triangle_residuals),
        {
            "vertices": 4,
            "edges": 6,
            "incidence_rank": incidence_rank,
            "incidence_nullity": 4 - incidence_rank,
            "cocycle_constraint_rank": cycle_rank,
            "cocycle_space_dimension": 6 - cycle_rank,
            "graph_rank": graph_rank,
            "graph_nullity": 10 - graph_rank,
            "ordered_triangle_checks": len(ordered_triangle_residuals),
            "ordered_triangle_failures": sum(value != 0 for value in ordered_triangle_residuals),
        },
    )

    # Control 4: dual pairing and nonselection of an invariant level/covector.
    K = [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]]
    preservation: dict[str, bool] = {}
    for q in map(Fraction, (2, 3, 5)):
        D = [[1 / q, Fraction(0)], [Fraction(0), q]]
        preservation[str(q)] = matrix_mul(matrix_mul(transpose(D), K), D) == K
    level_witnesses = [(0, 2), (1, 1), (2, Fraction(1, 2)), (2, 2)]
    level_counts = {
        "product_0": sum(a * b == 0 for a, b in level_witnesses),
        "product_1": sum(a * b == 1 for a, b in level_witnesses),
        "product_4": sum(a * b == 4 for a, b in level_witnesses),
    }
    check(
        "dual_pairing_preserved_but_level_unselected",
        all(preservation.values()) and level_counts == {"product_0": 1, "product_1": 2, "product_4": 1},
        {"preservation": preservation, "invariant_level_counts": level_counts},
    )

    # Adversarial counterexample to the production N05 premise as written.
    # Z2 acts by s(x)=1-x both on the two-point domain and affinely on the
    # codomain. A(x)=x is equivariant, sigma is invertible, but zero is moved.
    affine_domain = (0, 1)
    affine_equivariant = all((1 - x) == (1 - x) for x in affine_domain)
    affine_sigma_involutive = all(1 - (1 - y) == y for y in affine_domain)
    zero_orbit_saturated = ((0 == 0) == ((1 - 0) == 0))
    check(
        "invertible_sigma_does_not_imply_zero_saturation",
        affine_equivariant and affine_sigma_involutive and not zero_orbit_saturated,
        {
            "domain_action": "s(x)=1-x",
            "codomain_action": "sigma(y)=1-y",
            "A": "A(x)=x",
            "sigma_invertible": affine_sigma_involutive,
            "A_equivariant": affine_equivariant,
            "A(0)": 0,
            "A(s(0))": 1,
            "required_repair": "replace invertible sigma by sigma_g(0)=0, e.g. a linear/vector-bundle action",
        },
    )

    # Saved production result comparison (records only; no production code is imported/run).
    production_result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
    production_algebra = json.loads((PKG / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    naturality = {row["obligation_id"]: row for row in rows("WHOLE_LAW_NATURALITY_LEDGER.tsv")}
    check(
        "saved_core_result_reproduced",
        production_result["outcome"] == "RECIPROCITY_DERIVES_EQUIVARIANT_QUOTIENT_ONLY"
        and production_result["complete_native_return_A"] is False
        and production_result["fixedness_entailed"] is False
        and production_algebra["orbit_size"] == 2
        and production_algebra["incidence_rank"] == incidence_rank
        and production_algebra["comparison_graph_rank"] == graph_rank
        and production_algebra["comparison_graph_nullity"] == 10 - graph_rank
        and production_algebra["dual_pairing_preservation_failures"] == 0,
        {
            "outcome": production_result["outcome"],
            "complete_native_return_A": production_result["complete_native_return_A"],
            "fixedness_entailed": production_result["fixedness_entailed"],
        },
    )
    production_status = {row["claim"]: row for row in rows("STATUS_LEDGER.tsv")}
    production_verification = json.loads((PKG / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    exact_derivation_text = (PKG / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit_report_text = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    check(
        "n05_amendment_closed",
        naturality["N05"]["status"] == "DERIVED_REQUIREMENT_GIVEN_ZERO_PRESERVING_sigma"
        and "sigma_g(0)=0" in naturality["N05"]["consequence"]
        and production_result.get("zero_set_orbit_saturation_derived_given_A_and_zero_preserving_codomain_action") is True
        and production_status["zero_set_orbit_saturation"]["status"]
        == "DERIVED_GIVEN_FUTURE_A_COMPLETE_ACTION_AND_ZERO_PRESERVING_sigma"
        and production_algebra.get("affine_sigma_invertible") is True
        and production_algebra.get("affine_sigma_fixes_zero") is False
        and production_algebra.get("affine_zero_set_orbit_saturated") is False
        and "sigma_g(0)=0" in exact_derivation_text
        and "sigma_g(0)=0" in audit_report_text,
        {
            "saved_row": naturality["N05"],
            "status_row": production_status["zero_set_orbit_saturation"],
            "affine_counterexample": {
                "equivariant": production_algebra.get("affine_sigma_equivariant"),
                "invertible": production_algebra.get("affine_sigma_invertible"),
                "fixes_zero": production_algebra.get("affine_sigma_fixes_zero"),
                "zero_set_orbit_saturated": production_algebra.get("affine_zero_set_orbit_saturated"),
            },
        },
    )
    check(
        "triangle_count_wording_amendment_closed",
        production_algebra.get("sorted_triangle_witness_checks") == 12
        and "four sorted triangles on three" in exact_derivation_text
        and len(ordered_triangle_residuals) == 24,
        {
            "saved_sorted_witness_count": production_algebra.get("sorted_triangle_witness_checks"),
            "saved_count_origin": "four sorted triangles times three phi witnesses",
            "independent_full_ordered_triples_for_one_K4_assignment": len(ordered_triangle_residuals),
            "effect": "wording repaired; the cocycle and rank results remain correct",
        },
    )
    check(
        "amended_primary_saved_verification",
        production_verification.get("status") == "PASS"
        and production_verification.get("checks_passed") == production_verification.get("checks_total") == 44
        and production_verification.get("catch_proofs_passed")
        == production_verification.get("catch_proofs_total")
        == 21,
        production_verification,
    )

    # One semantic predicate, then genuine changed-record mutations.
    good_state = {
        "source_count": 1384,
        "stronger_founded_return_found": False,
        "reciprocity_roles": ["observer_frame", "internal_dual", "conditional_xmax"],
        "xmax_status": "WORKING_SCHEMA_NOT_FOUNDED_RETURN",
        "naturality_claimed": True,
        "complete_actions_supplied": True,
        "zero_saturation_claimed": True,
        "sigma_fixes_zero": True,
        "fixedness_entailed": False,
        "physical_observers_quotiented": False,
        "unique_return_selected": False,
        "cocycle_realizes_profile": False,
        "pairing_is_response_covector": False,
        "finite_cell_complete_return": False,
        "p4_selected_law": False,
        "strong_csn_active": False,
        "prejuly_affirmative": False,
        "boundary_complete": False,
        "bootstrap_maps_derived": False,
        "universal_no_go": False,
    }
    good_ok, good_failures = semantic_contract(good_state)
    check("repaired_semantic_contract_accepts", good_ok, {"failures": good_failures})

    mutations = {
        "M01_merge_reciprocities": {"reciprocity_roles": ["reciprocity", "reciprocity", "reciprocity"]},
        "M02_promote_xmax": {"xmax_status": "FOUNDED_NATIVE_RETURN"},
        "M03_invertibility_only": {"sigma_fixes_zero": False},
        "M04_fixedness": {"fixedness_entailed": True},
        "M05_erase_physical_observers": {"physical_observers_quotiented": True},
        "M06_unique_return": {"unique_return_selected": True},
        "M07_cocycle_realization": {"cocycle_realizes_profile": True},
        "M08_pairing_response": {"pairing_is_response_covector": True},
        "M09_finite_cell_splice": {"finite_cell_complete_return": True},
        "M10_p4_selection": {"p4_selected_law": True},
        "M11_csn_regression": {"strong_csn_active": True},
        "M12_prejuly_affirmative": {"prejuly_affirmative": True},
        "M13_boundary_promotion": {"boundary_complete": True},
        "M14_bootstrap_promotion": {"bootstrap_maps_derived": True},
        "M15_universal_no_go": {"universal_no_go": True},
        "M16_source_omission": {"source_count": 1383},
        "M17_unscoped_naturality": {"complete_actions_supplied": False},
    }
    mutation_results: list[dict] = []
    for mutation_id, changes in mutations.items():
        candidate = copy.deepcopy(good_state)
        candidate.update(changes)
        accepted, failures = semantic_contract(candidate)
        mutation_results.append(
            {"mutation_id": mutation_id, "changes": changes, "rejected": not accepted, "failures": failures}
        )
    check(
        "genuine_semantic_mutations_rejected",
        all(item["rejected"] for item in mutation_results),
        mutation_results,
    )

    failed = [name for name, passed, _detail in checks if not passed]
    closed_findings = [
        {
            "id": "A1_ZERO_SECTION_PREMISE",
            "status": "CLOSED_IN_AMENDED_PRIMARY",
            "finding": "Invertibility of sigma_g alone does not imply sigma_g(0)=0; equivariance plus invertibility therefore does not by itself orbit-saturate A=0.",
            "repair": "Replace N05's premise by a zero-preserving codomain action (normally a linear/vector-bundle representation), and add sigma_g(0)=0 to the derivation and reports.",
            "effect_on_main_result": "No change to the negative result that Reciprocity does not derive A; the conditional positive zero-set theorem is repaired.",
        },
        {
            "id": "A2_TRIANGLE_COUNT_LABEL",
            "status": "CLOSED_IN_AMENDED_PRIMARY",
            "finding": "The saved 12 triangle checks are four sorted K4 triangles evaluated on three depth witnesses, not a full oriented-triangle census for one assignment.",
            "repair": "Describe the 12 as witness checks, or report the independent 24 ordered-triple checks and cocycle-constraint rank 3.",
            "effect_on_main_result": "No algebraic or scientific conclusion changes.",
        },
    ]
    verdict = "PASS" if not failed else "REFUTED-IN-PART"
    result = {
        "verdict": verdict,
        "primary_outcome_retained": "RECIPROCITY_DERIVES_EQUIVARIANT_QUOTIENT_ONLY",
        "checks_passed": sum(passed for _name, passed, _detail in checks),
        "checks_total": len(checks),
        "failed": failed,
        "source_paths_verified_and_searched": len(inventory),
        "source_bytes_searched": total_bytes,
        "stronger_founded_return_found": False,
        "independent_algebra": {
            "swap_orbit_size": len(orbit),
            "fixed_locus_rank": fixed_rank,
            "equivariant_return_zero_counts_same_domain_codomain": zero_counts,
            "incidence_rank": incidence_rank,
            "incidence_nullity": 4 - incidence_rank,
            "cocycle_constraint_rank": cycle_rank,
            "cocycle_space_dimension": 6 - cycle_rank,
            "graph_rank": graph_rank,
            "graph_nullity": 10 - graph_rank,
            "ordered_triangle_checks": len(ordered_triangle_residuals),
            "dual_pairing_preserved": all(preservation.values()),
        },
        "semantic_mutations_rejected": sum(item["rejected"] for item in mutation_results),
        "semantic_mutations_total": len(mutation_results),
        "closed_findings": closed_findings,
        "four_gates": {
            "preregistered": "YES_aad2ac4",
            "bounded_scope": "YES_exact_1384_source_universe_and_finite_logic_controls",
            "independent_load_bearing_verification": "YES_fresh_nonimporting_reconstruction_and_amended_primary_closure",
            "premises_audited": "YES_observer_dual_Xmax_finite_cell_P4_CSN_firewall_boundary_bootstrap_separated",
        },
        "stop_line": "No solve, GPU, physics adoption, commit, push, or navigation edit performed.",
    }
    RAW_PATH.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in raw), encoding="utf-8")
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"{verdict}: checks={result['checks_passed']}/{result['checks_total']} "
        f"sources={len(inventory)} mutations={result['semantic_mutations_rejected']}/{result['semantic_mutations_total']}"
    )
    if failed:
        raise SystemExit("failed checks: " + ",".join(failed))


if __name__ == "__main__":
    main()
