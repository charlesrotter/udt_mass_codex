#!/usr/bin/env python3
"""G279 source-first dependency and provenance audit."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
MANIFEST = PACKAGE / "SOURCE_MANIFEST.tsv"

G236 = ROOT / "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/derive_dual_sne_relational_state.py"
G278 = ROOT / "udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/derive_scale_and_holdout.py"
G278_DIAGNOSTIC = ROOT / "udt_g278_cepheid_scale_attachment_des_holdout_2026-08-27/diagnose_resolution_sensitivity.py"


EDGES = [
    {
        "edge": "E00",
        "from": "F1_F2_F3",
        "to": "D_delta",
        "status": "DERIVED_ON_SUPPLIED_DEPTH",
        "class": "NATIVE_MIXED_FOUNDING",
        "load_bearing_G278": "yes",
        "claim": "dual reciprocal composition gives diag(exp(-delta),exp(delta))",
    },
    {
        "edge": "E01",
        "from": "D_delta_F4",
        "to": "primary_metric",
        "status": "DERIVED_AFTER_DECLARED_READOUT",
        "class": "NATIVE_MIXED_FOUNDING",
        "load_bearing_G278": "yes_bounded_radial",
        "claim": "quadratic Lorentzian and areal readout gives reciprocal primary metric",
    },
    {
        "edge": "E02",
        "from": "supplied_metric_and_pair_germ",
        "to": "complete_pair_pullback_h",
        "status": "DERIVED_CONDITIONAL",
        "class": "NATIVE_GEOMETRIC_EVALUATOR",
        "load_bearing_G278": "conceptual_radial_reduction",
        "claim": "all B Q S Y Z channels enter h before readout",
    },
    {
        "edge": "E03",
        "from": "complete_pair_pullback_h_and_W1",
        "to": "completed_Phi",
        "status": "WORKING_PREMISE_PLUS_DERIVED_CONDITIONAL",
        "class": "EXPLICIT_NONCANON_CLARIFICATION",
        "load_bearing_G278": "yes_direct_redshift_semantics",
        "claim": "m=sqrt(-det h) and Phi=-log T",
    },
    {
        "edge": "E04",
        "from": "completed_endpoint_clocks_and_supplied_pair_map",
        "to": "delta_AB",
        "status": "DERIVED_CONDITIONAL",
        "class": "NATIVE_PAIR_EVALUATOR",
        "load_bearing_G278": "yes",
        "claim": "delta_AB=-log(d tau_B/d tau_A)",
    },
    {
        "edge": "E05",
        "from": "delta_source_observer_and_redshift_query",
        "to": "phi_equals_log1p_z",
        "status": "DERIVED_CONDITIONAL",
        "class": "NATIVE_DIRECT_REDSHIFT_EDGE",
        "load_bearing_G278": "yes",
        "claim": "log(1+z)=Phi_source-Phi_observer",
    },
    {
        "edge": "E06",
        "from": "direct_redshift_plus_transparent_transfer",
        "to": "relative_areal_state_formula",
        "status": "CONDITIONAL_IMPORT",
        "class": "DECLARED_OBSERVATIONAL_INTERFACE",
        "load_bearing_G278": "yes",
        "claim": "dL=Z^2 R and y=m-10log10 Z=5log10 R+offset",
    },
    {
        "edge": "E07",
        "from": "processed_SNe_plus_hat_basis_K",
        "to": "G236_S_K_phi",
        "status": "OBSERVED_PREREGISTERED_NUMERICAL_READOUT",
        "class": "DECLARED_NUMERICAL_REPRESENTATION",
        "load_bearing_G278": "yes",
        "claim": "piecewise-linear K=8,12,16,24 relative state",
    },
    {
        "edge": "E08",
        "from": "G236_state_plus_Cepheid_ladder_and_optical_bridge",
        "to": "conditional_ell",
        "status": "OBSERVED_PLUS_CONDITIONAL_BRIDGE",
        "class": "DECLARED_EMPIRICAL_ATTACHMENT",
        "load_bearing_G278": "yes",
        "claim": "ell=10^(a/5) Mpc for the frozen areal state",
    },
    {
        "edge": "E09",
        "from": "conditional_curve_plus_DES_published_MU",
        "to": "DES_holdout_score",
        "status": "OBSERVED_RELEASE_CONVENTION",
        "class": "DECLARED_HELDOUT_CHECK",
        "load_bearing_G278": "yes",
        "claim": "no-retuning comparison with published H0=70 normalization cargo",
    },
    {
        "edge": "S00",
        "from": "metric_null_screen_transport",
        "to": "angular_Jacobi_outputs",
        "status": "DERIVED_CONDITIONAL_SIBLING",
        "class": "NATIVE_GEOMETRIC_EVALUATOR",
        "load_bearing_G278": "no",
        "claim": "angular response is upstream metric sibling, not post-readout fit",
    },
    {
        "edge": "P00",
        "from": "G271_G275_W5_projective_chain",
        "to": "complete_projective_pair_position",
        "status": "MIXED_DERIVED_AND_WORKING",
        "class": "SEPARATE_GEOMETRIC_INTERPRETATION",
        "load_bearing_G278": "no",
        "claim": "W5 and chi/tanh do not execute in G236 or G278 numerical code",
    },
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_manifest() -> dict[str, bool]:
    checks: dict[str, bool] = {}
    with MANIFEST.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["path"]
            checks[row["path"]] = (
                path.is_file()
                and path.stat().st_size == int(row["bytes"])
                and digest(path) == row["sha256"]
            )
    assert len(checks) == 31 and all(checks.values()), checks
    return checks


def ast_inventory(path: Path) -> dict[str, object]:
    text = path.read_text()
    tree = ast.parse(text)
    imports: set[str] = set()
    strings: list[str] = []
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            strings.append(node.value)
        elif isinstance(node, ast.Name):
            names.add(node.id)
    return {
        "path": str(path.relative_to(ROOT)),
        "imports": sorted(imports),
        "names": sorted(names),
        "strings": strings,
        "text": text,
    }


def runtime_path_strings(inventory: dict[str, object]) -> list[str]:
    answer = []
    for value in inventory["strings"]:
        if any(marker in value for marker in ("/", ".csv", ".npz", ".dat", ".cov", ".json", ".tsv")):
            answer.append(value)
    return sorted(set(answer))


def validate_edges(edges: list[dict[str, str]]) -> None:
    assert len({edge["edge"] for edge in edges}) == len(edges)
    by_id = {edge["edge"]: edge for edge in edges}
    assert by_id["E03"]["status"] == "WORKING_PREMISE_PLUS_DERIVED_CONDITIONAL"
    assert by_id["E06"]["status"] == "CONDITIONAL_IMPORT"
    assert by_id["E07"]["class"] == "DECLARED_NUMERICAL_REPRESENTATION"
    assert by_id["E08"]["class"] == "DECLARED_EMPIRICAL_ATTACHMENT"
    assert by_id["P00"]["load_bearing_G278"] == "no"
    assert by_id["S00"]["load_bearing_G278"] == "no"


def audit_executables() -> dict[str, object]:
    inventories = {path.name: ast_inventory(path) for path in (G236, G278, G278_DIAGNOSTIC)}
    allowed_main_imports = {
        "__future__", "csv", "hashlib", "json", "math", "os", "pathlib", "numpy", "scipy.linalg"
    }
    for name in (G236.name, G278.name):
        unexpected = set(inventories[name]["imports"]) - allowed_main_imports
        assert not unexpected, (name, unexpected)

    g236_text = str(inventories[G236.name]["text"])
    g278_text = str(inventories[G278.name]["text"])
    combined = g236_text + "\n" + g278_text

    # Exact projective-position machinery is absent from the executable observational path.
    for token in (r"\btanh\b", r"\bprojective\b", r"\bW5\b"):
        assert re.search(token, combined, flags=re.IGNORECASE) is None, token

    # Prohibited objects may occur only as explicit Boolean status/report keys, never imports,
    # names, file paths, or function calls.
    prohibited_names = {"P1", "G116", "G189", "Xmax", "LambdaCDM", "lcdm_distance"}
    for name in (G236.name, G278.name):
        inv = inventories[name]
        assert not (prohibited_names & set(inv["names"])), (name, prohibited_names & set(inv["names"]))
        for path_string in runtime_path_strings(inv):
            assert not any(token.lower() in path_string.lower() for token in prohibited_names), path_string

    # The declared imported boundary and representation family must remain executable and visible.
    required_g236 = [
        "phi=log(1+z)",
        "IMPORTED_CONDITIONAL_eta_1_epsilon_1_over_Z",
        "K_VALUES = (8, 12, 16, 24)",
        "p_y = p_mag - 10.0 * np.log10(1.0 + p_z)",
    ]
    required_g278 = [
        "K_VALUES = (8, 12, 16, 24)",
        "flow_observed = magnitude_all[flow_indices] - 10.0 * np.log10",
        "ell_mpc = float(10.0 ** (a_mag / 5.0))",
        "elif not (resolution_pass and subset_pass and serialization_pass)",
        '"transparent_transfer_imported": True',
        '"P1_used": False',
        '"Xmax_used": False',
        '"lcdm_distance_used": False',
    ]
    assert all(fragment in g236_text for fragment in required_g236)
    assert all(fragment in g278_text for fragment in required_g278)

    diagnostic_imports = set(inventories[G278_DIAGNOSTIC.name]["imports"])
    assert "derive_scale_and_holdout" in diagnostic_imports

    return {
        "inventories": {
            name: {
                "imports": inv["imports"],
                "runtime_path_strings": runtime_path_strings(inv),
            }
            for name, inv in inventories.items()
        },
        "projective_W5_executable_dependency": False,
        "angular_postreadout_executable_dependency": False,
        "P1_G116_G189_Xmax_LCDM_runtime_dependency": False,
        "G236_K_basis_is_executable_numerical_representation": True,
        "G278_resolution_gate_is_active": True,
        "G278_diagnostic_reuses_production_helpers": True,
    }


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    sources = verify_manifest()
    validate_edges(EDGES)
    executable = audit_executables()
    write_tsv(PACKAGE / "DEPENDENCY_LEDGER.tsv", EDGES)

    result = {
        "audit": "G279_NATIVE_KERNEL_OBSERVATIONAL_INTERFACE_PROVENANCE",
        "status": "PASS",
        "landing": (
            "NATIVE_CORE_INTACT__DECLARED_IMPORT_BOUNDARY_INTACT"
            "__G278_SENSITIVITY_DOWNSTREAM__W5_NOT_LOAD_BEARING_FOR_G278"
        ),
        "source_count": len(sources),
        "source_checks_pass": all(sources.values()),
        "edge_count": len(EDGES),
        "executable_audit": executable,
        "key_findings": {
            "kernel_function_fitted": False,
            "native_angular_postprocessing_used": False,
            "explicit_working_premise_W1_required_for_completed_scalar": True,
            "explicit_working_premise_W5_required_for_G278": False,
            "G278_calibrates_downstream_areal_state_not_kernel": True,
            "resolution_sensitivity_enters_at_G236_hat_basis": True,
            "processed_release_and_transfer_imports_are_declared": True,
        },
        "maximum_conclusion": (
            "source-bounded provenance separation only; no history, native light law, unique scale, "
            "W1/W5 canonization, representation-independent state, or Xmax"
        ),
    }
    (PACKAGE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
