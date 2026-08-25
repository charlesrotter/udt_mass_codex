#!/usr/bin/env python3
"""Production verifier for the preregistered G253 dependency audit."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
ALLOWED_CLASSES = {
    "LOAD_BEARING_DERIVED",
    "LOAD_BEARING_DERIVED_CONDITIONAL",
    "LOAD_BEARING_WORKING_PREMISE",
    "LOAD_BEARING_SUPPLIED_QUERY_OR_HISTORY",
    "LOAD_BEARING_OBSERVED_ATTACHMENT",
    "NON_LOAD_BEARING_CONTROL",
    "REDUNDANT_EVIDENCE",
    "UNSUPPORTED_EDGE",
}
REQUIRED_GRAPHS = {"scalar_kernel", "angular_sibling", "optional_scale_attachment"}
FORBIDDEN_ACTIVE = {"P1", "G116", "G189", "X_max", "protected_local_packages", "observational_outcomes"}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_source(relpath: str, expected_sha256: str) -> Path:
    """Resolve one frozen source in either repository or sealed-intake layout."""
    candidates = (ROOT / relpath, ROOT / "sources" / relpath)
    existing = [path for path in candidates if path.is_file()]
    assert existing, ("missing_source", relpath)
    actual = {path: sha256(path) for path in existing}
    assert all(value == expected_sha256 for value in actual.values()), (
        "source_hash_mismatch",
        relpath,
        {str(path): value for path, value in actual.items()},
    )
    return existing[0]


def require_tokens(
    relpath: str,
    expected_sha256: str,
    tokens: tuple[str, ...],
) -> int:
    text = resolve_source(relpath, expected_sha256).read_text(encoding="utf-8")
    for token in tokens:
        assert token in text, (relpath, token)
    return len(tokens)


def validate_graph(
    nodes: list[dict[str, str]],
    edges: list[dict[str, str]],
    manifest_hashes: dict[str, str],
) -> dict[str, int]:
    ids = {row["node_id"] for row in nodes}
    assert len(ids) == len(nodes)
    assert REQUIRED_GRAPHS <= {row["graph"] for row in edges}
    assert all(row["classification"] in ALLOWED_CLASSES for row in edges)
    assert all(row["classification"] != "UNSUPPORTED_EDGE" for row in edges)
    for row in edges:
        assert row["to_node"] in ids
        assert set(row["from_nodes"].split(",")) <= ids
        assert row["source"] in manifest_hashes
        resolve_source(row["source"], manifest_hashes[row["source"]])
    active_blob = "\n".join(
        row["from_nodes"] + "\t" + row["to_node"] + "\t" + row["exact_claim"] for row in edges
    )
    assert not any(term in active_blob for term in FORBIDDEN_ACTIVE)

    adjacency: dict[str, set[str]] = {node: set() for node in ids}
    for row in edges:
        for source in row["from_nodes"].split(","):
            adjacency[source].add(row["to_node"])

    def reachable(start: str, target: str) -> bool:
        seen = {start}
        stack = [start]
        while stack:
            current = stack.pop()
            if current == target:
                return True
            for nxt in adjacency[current]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return False

    assert reachable("N00", "N08")
    assert reachable("N02", "N11")
    assert reachable("N12", "N16")
    return {"nodes": len(nodes), "edges": len(edges), "graphs": len(REQUIRED_GRAPHS)}


def exact_formula_checks() -> dict[str, int]:
    rng = random.Random(253)
    assertions = 0
    for _ in range(4096):
        t = Fraction(rng.randint(1, 80), rng.randint(1, 80))
        length = Fraction(rng.randint(1, 80), rng.randint(1, 80))
        beta = Fraction(rng.randint(-80, 80), rng.randint(1, 80))
        h00 = -(t * t)
        h01 = -(t * t) * beta
        h11 = length * length - t * t * beta * beta
        det = h00 * h11 - h01 * h01
        assert det == -(t * t) * (length * length)
        assertions += 1
        m2 = -det
        assert m2 == (t * length) ** 2
        assertions += 1
        completed_ruler = length / (t * length)
        assert t * completed_ruler == 1
        assertions += 1

        # A common metric homothety shifts each endpoint potential equally,
        # so endpoint-relative depth is unchanged.
        t_a = Fraction(rng.randint(1, 80), rng.randint(1, 80))
        t_b = Fraction(rng.randint(1, 80), rng.randint(1, 80))
        ell = Fraction(rng.randint(1, 80), rng.randint(1, 80))
        assert (ell * t_a) / (ell * t_b) == t_a / t_b
        assertions += 1

        # Spatial-only orchestra changes tape density while the shared clock scalar stays fixed.
        length2 = length + Fraction(rng.randint(1, 80), rng.randint(1, 80))
        assert t * length2 != t * length
        assertions += 1

    # Exact equal-depth, unequal-angular-response witness from G249.
    phi = Fraction(0)
    p0, q0 = Fraction(0), Fraction(0)
    p1, q1 = Fraction(1), Fraction(0)
    exp_minus_2phi = Fraction(1)
    a0 = (exp_minus_2phi * (2 * p0 * p0 + p0 - q0), 1 - exp_minus_2phi * (1 + p0))
    a1 = (exp_minus_2phi * (2 * p1 * p1 + p1 - q1), 1 - exp_minus_2phi * (1 + p1))
    assert phi == 0 and a0 == (0, 0) and a1 == (3, -1) and a0 != a1
    assertions += 4

    # Founded block formula check over a deterministic floating sweep.
    for delta in [i / 64 for i in range(-256, 257)]:
        h00 = -math.exp(-2 * delta)
        h11 = math.exp(2 * delta)
        assert abs(h00 * h11 + 1.0) < 2e-14
        phi_completed = -0.5 * math.log(-h00)
        assert abs(phi_completed - delta) < 2e-14
        assertions += 2
    return {"formula_assertions": assertions, "fraction_trials": 4096, "founded_depth_samples": 513}


def main() -> None:
    manifest = read_tsv(PKG / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 21
    manifest_hashes = {row["path"]: row["sha256"] for row in manifest}
    assert len(manifest_hashes) == len(manifest)
    for row in manifest:
        resolve_source(row["path"], row["sha256"])

    token_assertions = 0
    token_assertions += require_tokens(
        "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
        manifest_hashes["UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md"],
        ("u(\\Delta)v(\\Delta)=1", "S(\\phi_1)S(\\phi_2)=S(\\phi_1+\\phi_2)", "not yet derive a unique action"),
    )
    token_assertions += require_tokens(
        "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/EXACT_DERIVATION.md",
        manifest_hashes["udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/EXACT_DERIVATION.md"],
        ("WORKING_FOUNDATIONAL_CLARIFICATION", "m=T L_\\sigma", "\\Phi=-\\log T"),
    )
    token_assertions += require_tokens(
        "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/EXACT_DERIVATION.md",
        manifest_hashes["udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/EXACT_DERIVATION.md"],
        ("h=Y^TB^T\\eta_2BY+(SY+Z)^TQ^TQ(SY+Z)", "Every term enters before", "not the completed physical"),
    )
    token_assertions += require_tokens(
        "udt_g216_observer_event_comparison_clock_rate_ownership_2026-08-22/EXACT_DERIVATION.md",
        manifest_hashes["udt_g216_observer_event_comparison_clock_rate_ownership_2026-08-22/EXACT_DERIVATION.md"],
        ("-\\log\\frac{d\\tau_B}{d\\tau_A}", "pair germ are physically realized", "free scalar clock calibration left"),
    )
    token_assertions += require_tokens(
        "udt_g243_reciprocal_sne_radial_spline_freeze_2026-08-24/EXACT_DERIVATION.md",
        manifest_hashes["udt_g243_reciprocal_sne_radial_spline_freeze_2026-08-24/EXACT_DERIVATION.md"],
        ("1+z=\\exp(\\phi_s-\\phi_o)", "No angular or screen response is needed", "not a native UDT light law"),
    )
    token_assertions += require_tokens(
        "udt_g245_metric_owned_observer_null_cone_field_2026-08-24/EXACT_DERIVATION.md",
        manifest_hashes["udt_g245_metric_owned_observer_null_cone_field_2026-08-24/EXACT_DERIVATION.md"],
        ("F(\\lambda,n)=\\operatorname{Exp}_o", "angular differential", "not a post-readout correction"),
    )
    token_assertions += require_tokens(
        "udt_g249_reciprocal_angular_absolute_scale_ownership_2026-08-24/EXACT_DERIVATION.md",
        manifest_hashes["udt_g249_reciprocal_angular_absolute_scale_ownership_2026-08-24/EXACT_DERIVATION.md"],
        ("PHI_VALUE_ALONE_DOES_NOT_FIX_NORMALIZED_ANGULAR_RESPONSE", "\\mathcal D_\\ell", "ONE_INDEPENDENT_DIMENSIONFUL_ANCHOR_REMAINS"),
    )
    token_assertions += require_tokens(
        "udt_g252_local_proper_clock_same_object_attachment_contract_2026-08-24/EXACT_DERIVATION.md",
        manifest_hashes["udt_g252_local_proper_clock_same_object_attachment_contract_2026-08-24/EXACT_DERIVATION.md"],
        ("It changes no reciprocal-kernel operator", "\\ell=\\frac{\\tau_*}{\\bar\\tau}", "does not add scaffolding to the kernel"),
    )

    nodes = read_tsv(PKG / "NODE_LEDGER.tsv")
    edges = read_tsv(PKG / "LOAD_BEARING_EDGE_LEDGER.tsv")
    graph_counts = validate_graph(nodes, edges, manifest_hashes)
    formula_counts = exact_formula_checks()
    controls = read_tsv(PKG / "HISTORICAL_CONTROL_DISPOSITION.tsv")
    assert all(row["load_bearing"] in {"no", "yes_for_primary_slice_only", "no_kernel_mechanism"} for row in controls)
    assert all(row["object_or_package"] != "protected_local_packages" or row["disposition"] == "EXCLUDED_AND_UNINSPECTED" for row in controls)

    result = {
        "landing": "MIXED_STATUS_NATIVE_CHAIN_COMPRESSES__REDSHIFT_DIRECT_CONDITIONAL__ANGULAR_RESPONSE_SIBLING_NOT_POSTPROCESSING__SCALE_ATTACHMENT_DOWNSTREAM",
        "manifest_sources": len(manifest),
        "manifest_hashes_pass": True,
        "token_assertions": token_assertions,
        **graph_counts,
        **formula_counts,
        "historical_controls": len(controls),
        "unsupported_edges": 0,
        "observational_values_read": 0,
        "protected_paths_read": 0,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--no-write" not in sys.argv[1:]:
        (PKG / "DERIVATION_RESULT.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
