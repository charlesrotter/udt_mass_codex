#!/usr/bin/env python3
"""Independent, fail-closed verifier for the finite-cell audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
EXPECTED_IDS = {
    "FC01_BOUNDARY_BOUNDARY",
    "FC02_ONE_CAP_BOUNDARY",
    "FC03_TWO_CAP_P0",
    "FC04_TWO_CAP_P1",
    "FC05_TWO_CAP_P_GT1",
    "FC06_NONPRIMITIVE_CAP",
    "FC07_PERIODIC_TORUS_BUNDLE",
    "FC08_MIRROR_DOUBLE",
    "FC09_NONORIENTABLE_GLUE",
    "FC10_STRATIFIED_PROJECTOR",
    "FC11_NONINTEGRABLE_DISTRIBUTION",
    "FC12_RECIPROCAL_TORIC_DIAGONAL",
}
STATIC_COMPACT_IDS = {
    "FC03_TWO_CAP_P0",
    "FC04_TWO_CAP_P1",
    "FC05_TWO_CAP_P_GT1",
    "FC07_PERIODIC_TORUS_BUNDLE",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def exterior_action(endomorphism: sp.Matrix) -> sp.Matrix:
    """Build F -> P^T F + F P from antisymmetric-matrix basis."""
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    columns = []
    for i, j in pairs:
        two_form = sp.zeros(4)
        two_form[i, j] = 1
        two_form[j, i] = -1
        image = endomorphism.T * two_form + two_form * endomorphism
        columns.append(sp.Matrix([image[a, b] for a, b in pairs]))
    return sp.Matrix.hstack(*columns)


def independent_algebra() -> dict[str, object]:
    metric_inverse = sp.diag(-1, 1, 1, 1)
    results: dict[str, object] = {}
    for label, alpha in {
        "timelike": sp.Matrix([1, 0, 0, 0]),
        "spacelike": sp.Matrix([0, 1, 0, 0]),
    }.items():
        raised = metric_inverse * alpha
        norm = (alpha.T * raised)[0]
        projector = raised * alpha.T / norm
        two_form = exterior_action(projector)
        complement = sp.eye(6) - two_form
        results[label] = {
            "norm": str(norm),
            "tangent_rank": projector.rank(),
            "parallel_rank": two_form.rank(),
            "transverse_rank": complement.rank(),
            "idempotent": projector**2 == projector
            and two_form**2 == two_form
            and complement**2 == complement,
            "complementary": two_form * complement == sp.zeros(6),
        }
    alpha_null = sp.Matrix([1, 1, 0, 0])
    nilpotent = metric_inverse * alpha_null * alpha_null.T
    exterior_nilpotent = exterior_action(nilpotent)
    results["null"] = {
        "norm": str((alpha_null.T * metric_inverse * alpha_null)[0]),
        "tangent_rank": nilpotent.rank(),
        "tangent_nilpotent": nilpotent**2 == sp.zeros(4),
        "two_form_rank": exterior_nilpotent.rank(),
        "two_form_nilpotent": exterior_nilpotent**2 == sp.zeros(6),
    }
    return results


def validate(
    result: dict[str, object],
    atlas: list[dict[str, str]],
    bracket: list[dict[str, str]],
    theorems: list[dict[str, str]],
    lineage: list[dict[str, str]],
) -> None:
    if result["schema"] != "udt-finite-cell-reciprocal-survival-density-1.0":
        raise AssertionError("schema")
    if result["sympy_version"] != "1.14.0":
        raise AssertionError("pinned SymPy")
    if result["base_commit"] != "67553529e79514aa79607dee859ae7d084ea37d6":
        raise AssertionError("base")

    ids = [row["completion_id"] for row in atlas]
    if len(ids) != 12 or len(set(ids)) != 12 or set(ids) != EXPECTED_IDS:
        raise AssertionError("missing or duplicate completion")
    if any(
        row["global_data_level"] == "COMPLETE_G_PHI_FIELD_WITNESS"
        for row in atlas
    ):
        raise AssertionError("invented complete witness")
    if sum(
        row["global_data_level"]
        == "PARAMETRIC_COMPLETION_TYPE_NO_COMPLETE_G_PHI_FIELD_WITNESS"
        for row in atlas
    ) != 11:
        raise AssertionError("type-only count")
    if sum(
        row["global_data_level"]
        == "CONDITIONAL_CONTROL_NO_COMPLETE_PROFILE_OR_ENDPOINT_SOLUTION"
        for row in atlas
    ) != 1:
        raise AssertionError("conditional control count")
    if any(
        row["selection_ruling"]
        != "REGISTERED_ALTERNATIVE_NOT_SELECTED_BY_THIS_AUDIT"
        for row in atlas
    ):
        raise AssertionError("selection promotion")
    if any(
        row["density_response"]
        != "UNDEFINED_NO_NATIVE_DENSITY_TO_BRANCH_INTERFACE"
        for row in atlas
    ):
        raise AssertionError("invented density response")

    by_id = {row["completion_id"]: row for row in atlas}
    for completion_id in STATIC_COMPACT_IDS:
        row = by_id[completion_id]
        if (
            row["static_spatial_phi"]
            != "STATIC_COMPACT_REAL_PHI_HAS_AT_LEAST_ONE_CRITICAL_POINT"
            or row["projector_survival"]
            != "OBSTRUCTED_FOR_STATIC_REAL_PHI__CONDITIONAL_TIME_LIVE"
        ):
            raise AssertionError("compact static obstruction")
        if "MAY_EVADE" not in row["time_live_phi"]:
            raise AssertionError("time-live wrongly obstructed")
    if "ORDINARY_GLOBAL_HODGE_ENDOMORPHISM_FAILS" not in by_id[
        "FC09_NONORIENTABLE_GLUE"
    ]["hodge_exchange"]:
        raise AssertionError("nonorientable Hodge")
    if "UNDEFINED_AT_TRUE_METRIC_OR_MANIFOLD_SINGULARITY" not in by_id[
        "FC06_NONPRIMITIVE_CAP"
    ]["hodge_exchange"]:
        raise AssertionError("singular extension")
    if "NOT_DESCEND_AS_ORDINARY_QUOTIENT_SCALAR" not in by_id[
        "FC08_MIRROR_DOUBLE"
    ]["global_behavior"]:
        raise AssertionError("odd quotient descent")
    if "NEITHER_SELECTS_NOR_REFUTES" not in by_id[
        "FC10_STRATIFIED_PROJECTOR"
    ]["global_behavior"]:
        raise AssertionError("projector conflation")
    if "NOT_A_DPHI_OBSTRUCTION" not in by_id[
        "FC11_NONINTEGRABLE_DISTRIBUTION"
    ]["global_behavior"]:
        raise AssertionError("distribution conflation")
    if "CONDITIONAL_CONTROL" not in by_id[
        "FC12_RECIPROCAL_TORIC_DIAGONAL"
    ]["global_behavior"]:
        raise AssertionError("toric promotion")

    gate = result["density_interface_gate"]
    if gate["gate_pass"] or gate["numeric_density_sweep_run"]:
        raise AssertionError("density gate")
    if gate["formal_bracket"] != "rho_tot in [0,infinity)":
        raise AssertionError("density bracket")
    if (
        gate["native_route_status"] != "OPEN_NATIVE_OBJECT_REQUIRED"
        or gate["native_route_missing_object"]
        != "off-shell native mass functional plus varied global closure and response map"
    ):
        raise AssertionError("density missing objects")
    if len(bracket) != 4:
        raise AssertionError("density domains")
    if any(
        "DENSITY_DRIVEN" in row["branch_response"]
        or "BRANCH_APPEARS" in row["branch_response"]
        for row in bracket
    ):
        raise AssertionError("fabricated density event")
    if not any(
        row["rho_tot_domain"] == "FORMAL_POSITIVE_EXTENDED_DOMAIN_[0,INFINITY)"
        and row["interface_status"] == "GATE_FAILED__NO_NUMERICAL_SWEEP_AUTHORIZED"
        for row in bracket
    ):
        raise AssertionError("formal density gate row")

    theorem_ids = [row["theorem_id"] for row in theorems]
    if len(theorem_ids) != 12 or len(set(theorem_ids)) != 12:
        raise AssertionError("theorem coverage")
    theorem_by_id = {row["theorem_id"]: row for row in theorems}
    if theorem_by_id["G11_SEAL_VALUE"]["scope_guard"] != (
        "PHI_ZERO_DOES_NOT_IMPLY_DPHI_ZERO"
    ):
        raise AssertionError("seal derivative conflation")
    if theorem_by_id["G03_COMPACT_STATIC_REAL_SCALAR"]["scope_guard"] != (
        "DOES_NOT_APPLY_TO_UNCONSTRAINED_TIME_LIVE_PHI"
    ):
        raise AssertionError("static theorem overscope")

    counts = result["counts"]
    expected_counts = {
        "registered_completion_families": 12,
        "complete_g_phi_field_witnesses": 0,
        "parametric_type_only": 11,
        "conditional_controls": 1,
        "static_compact_completion_rows_obstructed": 4,
        "mirror_fixed_seam_rows_with_static_normal_obstruction": 1,
        "global_theorems": 12,
        "density_source_routes": 5,
        "density_numeric_runs": 0,
    }
    if counts != expected_counts:
        raise AssertionError(f"counts: {counts}")
    if result["geometry_stopping_gate"]["status"] != "REACHED":
        raise AssertionError("geometry stopping gate")

    source_paths = [row["path"] for row in lineage]
    if len(source_paths) != 14 or len(set(source_paths)) != 14:
        raise AssertionError("source lineage coverage")
    for row in lineage:
        path = ROOT / row["path"]
        if not path.is_file():
            raise AssertionError("source missing")
        if sha256(path) != row["sha256"] or path.stat().st_size != int(row["size"]):
            raise AssertionError("source identity")

    source_density = read_tsv(
        ROOT
        / "udt_global_metric_assembly_atlas_2026-07-22"
        / "DENSITY_BOOTSTRAP_CIRCULARITY_LEDGER.tsv"
    )
    d03 = {row["route_id"]: row for row in source_density}[
        "D03_NATIVE_SIMULTANEOUS_FIXED_POINT"
    ]
    if (
        d03["mass_status"] != "OPEN_NATIVE_OBJECT_REQUIRED"
        or d03["selection_authority"] != "POTENTIAL_FUTURE_EIGENVALUE_OR_BRANCH_SELECTOR"
    ):
        raise AssertionError("native density source replay")

    algebra = independent_algebra()
    for label, norm in {"timelike": "-1", "spacelike": "1"}.items():
        row = algebra[label]
        if row != {
            "norm": norm,
            "tangent_rank": 1,
            "parallel_rank": 3,
            "transverse_rank": 3,
            "idempotent": True,
            "complementary": True,
        }:
            raise AssertionError(f"independent {label} algebra")
    if algebra["null"] != {
        "norm": "0",
        "tangent_rank": 1,
        "tangent_nilpotent": True,
        "two_form_rank": 2,
        "two_form_nilpotent": True,
    }:
        raise AssertionError("independent null algebra")


def main() -> None:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    atlas = read_tsv(HERE / "FINITE_CELL_BRANCH_ATLAS.tsv")
    bracket = read_tsv(HERE / "DENSITY_BRACKET.tsv")
    theorems = read_tsv(HERE / "GLOBAL_SURVIVAL_THEOREMS.tsv")
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")

    validate(result, atlas, bracket, theorems, lineage)

    catches: list[dict[str, str]] = []

    def catch(
        catch_id: str,
        name: str,
        mutator,
    ) -> None:
        mutated = (
            copy.deepcopy(result),
            copy.deepcopy(atlas),
            copy.deepcopy(bracket),
            copy.deepcopy(theorems),
            copy.deepcopy(lineage),
        )
        mutator(*mutated)
        try:
            validate(*mutated)
        except AssertionError:
            catches.append(
                {"catch_id": catch_id, "mutation": name, "status": "CAUGHT"}
            )
            return
        raise AssertionError(f"uncaught mutation {catch_id}: {name}")

    catch("C01", "remove_completion", lambda r, a, b, t, l: a.pop())
    catch("C02", "duplicate_completion", lambda r, a, b, t, l: a.append(copy.deepcopy(a[0])))
    catch(
        "C03",
        "promote_complete_witness",
        lambda r, a, b, t, l: a[0].update(global_data_level="COMPLETE_G_PHI_FIELD_WITNESS"),
    )
    catch(
        "C04",
        "promote_static_compact_split",
        lambda r, a, b, t, l: next(
            row for row in a if row["completion_id"] == "FC04_TWO_CAP_P1"
        ).update(projector_survival="GLOBAL_NONNULL_SPACELIKE"),
    )
    catch(
        "C05",
        "apply_static_obstruction_to_time_live",
        lambda r, a, b, t, l: next(
            row for row in a if row["completion_id"] == "FC03_TWO_CAP_P0"
        ).update(time_live_phi="OBSTRUCTED_BY_EXTREME_VALUE_THEOREM"),
    )
    catch(
        "C06",
        "ordinary_Hodge_on_nonorientable",
        lambda r, a, b, t, l: next(
            row for row in a if row["completion_id"] == "FC09_NONORIENTABLE_GLUE"
        ).update(hodge_exchange="GLOBAL_ORDINARY_HODGE_EXCHANGE"),
    )
    catch(
        "C07",
        "extend_through_singularity",
        lambda r, a, b, t, l: next(
            row for row in a if row["completion_id"] == "FC06_NONPRIMITIVE_CAP"
        ).update(hodge_exchange="GLOBAL_THROUGH_SINGULARITY"),
    )
    catch(
        "C08",
        "equate_phi_zero_with_dphi_zero",
        lambda r, a, b, t, l: next(
            row for row in t if row["theorem_id"] == "G11_SEAL_VALUE"
        ).update(scope_guard="PHI_ZERO_IMPLIES_DPHI_ZERO"),
    )
    catch(
        "C09",
        "descend_odd_scalar_to_quotient",
        lambda r, a, b, t, l: next(
            row for row in a if row["completion_id"] == "FC08_MIRROR_DOUBLE"
        ).update(global_behavior="ODD_PHI_DESCENDS_AS_ORDINARY_QUOTIENT_SCALAR"),
    )
    catch(
        "C10",
        "conflate_stratified_projector",
        lambda r, a, b, t, l: next(
            row for row in a if row["completion_id"] == "FC10_STRATIFIED_PROJECTOR"
        ).update(global_behavior="DPHI_SPLIT_OBSTRUCTED"),
    )
    catch(
        "C11",
        "activate_density_gate",
        lambda r, a, b, t, l: r["density_interface_gate"].update(gate_pass=True),
    )
    catch(
        "C12",
        "claim_numeric_density_sweep",
        lambda r, a, b, t, l: r["density_interface_gate"].update(
            numeric_density_sweep_run=True
        ),
    )
    catch(
        "C13",
        "insert_density_branch_event",
        lambda r, a, b, t, l: b[1].update(branch_response="BRANCH_APPEARS"),
    )
    catch(
        "C14",
        "erase_missing_native_objects",
        lambda r, a, b, t, l: r["density_interface_gate"].update(
            native_route_missing_object="-"
        ),
    )
    catch(
        "C15",
        "select_topology",
        lambda r, a, b, t, l: a[3].update(selection_ruling="SELECTED_S3"),
    )
    catch(
        "C16",
        "promote_toric_control",
        lambda r, a, b, t, l: next(
            row for row in a
            if row["completion_id"] == "FC12_RECIPROCAL_TORIC_DIAGONAL"
        ).update(global_behavior="COMPLETE_SELECTED_FIELD_SOLUTION"),
    )
    catch(
        "C17",
        "drop_formal_density_domain",
        lambda r, a, b, t, l: b.pop(),
    )
    catch(
        "C18",
        "mutate_source_hash",
        lambda r, a, b, t, l: l[0].update(sha256="0" * 64),
    )
    catch(
        "C19",
        "miscount_static_compact_rows",
        lambda r, a, b, t, l: r["counts"].update(
            static_compact_completion_rows_obstructed=5
        ),
    )
    catch(
        "C20",
        "treat_other_distribution_as_dphi",
        lambda r, a, b, t, l: next(
            row for row in a
            if row["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION"
        ).update(global_behavior="REGISTERED_PLANE_IS_DPHI_KERNEL"),
    )

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["catch_id", "mutation", "status"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(catches)

    independent = {
        "schema": "udt-finite-cell-reciprocal-survival-density-independent-1.0",
        "sympy_version": sp.__version__,
        "status": "PASS",
        "independent_algebra": independent_algebra(),
        "completion_rows": len(atlas),
        "global_theorem_rows": len(theorems),
        "density_bracket_rows": len(bracket),
        "source_rows_replayed": len(lineage),
        "catch_proofs": {
            "expected": 20,
            "caught": len(catches),
            "all_caught": len(catches) == 20,
        },
        "verdict": "VERIFIED_BOUNDED__NO_COMPLETE_FIELD_WITNESSES_AND_NO_NATIVE_DENSITY_RESPONSE_INTERFACE",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(independent, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(independent, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
