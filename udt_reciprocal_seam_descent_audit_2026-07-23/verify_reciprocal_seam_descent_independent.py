#!/usr/bin/env python3
"""Independent fail-closed verifier for reciprocal seam descent."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "67ac641e3bf764c2d4b43ddf79df7ef24a1ff429"
EXPECTED_IDS = {f"FC{i:02d}_" for i in range(1, 13)}
MAXIMUM = (
    "RECIPROCAL_VALUE_CHARACTER_HAS_EXACT_Z2_GRADED_SEAM_DESCENT_AND_"
    "CAN_SURVIVE_DPHI_DEGENERATION__COMPLETE_PHYSICAL_GLUE_STILL_"
    "REQUIRES_UNSUPPLIED_COVER_EQUIVARIANCE_ANGULAR_SOLDERING_METRIC_"
    "JETS_AND_CONNECTION_DATA__NO_REALIZATION_RELATION_OR_COMPLETION_"
    "SELECTOR_DERIVED"
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def independent_algebra() -> dict[str, object]:
    x, z = sp.symbols("x z", real=True)

    def d(value: sp.Expr) -> sp.Matrix:
        return sp.Matrix([[sp.exp(-value), 0], [0, sp.exp(value)]])

    f = sp.Matrix([[0, sp.Integer(2)], [sp.Rational(1, 2), 0]])
    g = sp.diag(sp.Integer(3), sp.Rational(1, 3))

    angular_controls = [
        sp.Matrix([[1, 1], [0, 1]]),
        sp.Matrix([[0, -1], [1, 0]]),
    ]
    angular_pass = []
    for angular in angular_controls:
        transition = sp.diag(1, 1, 1, 1)
        transition[:2, :2] = f
        transition[2:, 2:] = angular
        d4 = sp.diag(sp.exp(-z), sp.exp(z), 1, 1)
        expected = sp.diag(sp.exp(z), sp.exp(-z), 1, 1)
        angular_pass.append(
            sp.simplify(transition * d4 * transition.inv() - expected)
            == sp.zeros(4)
        )

    profile_results = {}
    for label, phi in {
        "linear": x,
        "cubic": x**3,
        "mixed": x + x**3,
    }.items():
        pulled = sp.simplify(f * d(phi.subs(x, -x)) * f.inv())
        difference = sp.simplify(pulled - d(phi))
        profile_results[label] = {
            "odd": sp.simplify(phi.subs(x, -x) + phi) == 0,
            "value_match": difference == sp.zeros(2),
            "first_match": difference.diff(x).applyfunc(sp.simplify)
            == sp.zeros(2),
            "second_match": difference.diff(x, 2).applyfunc(sp.simplify)
            == sp.zeros(2),
            "dphi_at_seal": str(sp.diff(phi, x).subs(x, 0)),
            "D_at_seal": str(d(phi).subs(x, 0).tolist()),
        }
    return {
        "det_D": str(sp.simplify(d(z).det())),
        "F_squared": f * f == sp.eye(2),
        "F_inverts_D": sp.simplify(f * d(z) * f.inv() - d(-z))
        == sp.zeros(2),
        "G_preserves_D": sp.simplify(g * d(z) * g.inv() - d(z))
        == sp.zeros(2),
        "two_distinct_angular_controls": len(angular_controls),
        "angular_controls_pass": all(angular_pass),
        "profiles": profile_results,
    }


def validate(
    result: dict[str, object],
    atlas: list[dict[str, str]],
    profiles: list[dict[str, str]],
    theorems: list[dict[str, str]],
    joins: list[dict[str, str]],
    status: list[dict[str, str]],
    lineage: list[dict[str, str]],
) -> None:
    if result["schema"] != "udt-reciprocal-seam-descent-1.0":
        raise AssertionError("schema")
    if result["base_commit"] != BASE or result["sympy_version"] != "1.14.0":
        raise AssertionError("environment")
    if result["maximum_conclusion"] != MAXIMUM:
        raise AssertionError("maximum")

    ids = [row["completion_id"] for row in atlas]
    if len(ids) != 12 or len(set(ids)) != 12:
        raise AssertionError("completion coverage")
    if {value.split("_", 1)[0] + "_" for value in ids} != EXPECTED_IDS:
        raise AssertionError("completion identities")
    by_id = {row["completion_id"]: row for row in atlas}
    if any(
        row["selection_ruling"]
        != "REGISTERED_ALTERNATIVE_NOT_SELECTED_BY_DESCENT"
        for row in atlas
    ):
        raise AssertionError("selection promotion")
    if any("COMPLETE_G_PHI_WITNESS" not in row["data_level"] for row in atlas):
        raise AssertionError("data level label")
    if sum(
        row["data_level"]
        == "CONDITIONAL_CONTROL_NO_COMPLETE_G_PHI_WITNESS"
        for row in atlas
    ) != 1:
        raise AssertionError("conditional control count")
    if sum(
        row["data_level"] == "PARAMETRIC_TYPE_NO_COMPLETE_G_PHI_WITNESS"
        for row in atlas
    ) != 11:
        raise AssertionError("parametric type count")

    mirror = by_id["FC08_MIRROR_DOUBLE"]
    if (
        mirror["value_character_status"]
        != "EXACT_STATIC_Z2_GRADED_SEAM_DESCENT"
        or "VALUE_FIRST_AND_SECOND_PULLBACK_JETS_MATCH"
        not in mirror["jet_status"]
        or "CUBIC_CRITICAL_CONTROL_PASSES"
        not in mirror["dphi_degeneracy_effect"]
        or mirror["angular_coupling"]
        != "ANGULAR_LIFT_REMAINS_ARBITRARY_AND_UNSELECTED"
        or "STILL_UNSUPPLIED" not in mirror["connection_status"]
    ):
        raise AssertionError("mirror ruling")
    if "PHI_GRADING_EQUIVARIANCE" not in by_id[
        "FC07_PERIODIC_TORUS_BUNDLE"
    ]["required_global_data"]:
        raise AssertionError("periodic equivariance")
    if by_id["FC09_NONORIENTABLE_GLUE"]["value_character_status"] != (
        "CONDITIONAL_TWISTED_DESCENT_WITHOUT_ORIENTATION"
    ):
        raise AssertionError("orientation")
    if "UNDEFINED_AT_TRUE_METRIC_OR_MANIFOLD_SINGULARITY" != by_id[
        "FC06_NONPRIMITIVE_CAP"
    ]["connection_status"]:
        raise AssertionError("singular extension")
    if "D_REMAINS_DEFINED" not in by_id["FC10_STRATIFIED_PROJECTOR"][
        "dphi_degeneracy_effect"
    ]:
        raise AssertionError("stratified value character")
    if "INDEPENDENT_OF_DISTRIBUTION_INTEGRABILITY" != by_id[
        "FC11_NONINTEGRABLE_DISTRIBUTION"
    ]["value_character_status"]:
        raise AssertionError("integrability conflation")
    if "NOT_NATIVE_SOLDERING" not in by_id[
        "FC12_RECIPROCAL_TORIC_DIAGONAL"
    ]["angular_coupling"]:
        raise AssertionError("toric promotion")

    profile_ids = [row["profile_id"] for row in profiles]
    if len(profile_ids) != 3 or len(set(profile_ids)) != 3:
        raise AssertionError("profile coverage")
    if any(
        row["value_pullback_match"] != "True"
        or row["first_jet_pullback_match"] != "True"
        or row["second_jet_pullback_match"] != "True"
        for row in profiles
    ):
        raise AssertionError("mirror jets")
    cubic = next(row for row in profiles if row["profile_id"] == "M02_CUBIC_CRITICAL")
    if (
        cubic["dphi_at_seal"] != "0"
        or cubic["derivative_3plus3_available_at_seal"] != "False"
        or cubic["D_at_seal"] != "[[1, 0], [0, 1]]"
        or cubic["scope"] != "STATIC_MIRROR_CONTROL_NOT_COMPLETE_FIELD_SOLUTION"
    ):
        raise AssertionError("critical profile")

    theorem_ids = [row["theorem_id"] for row in theorems]
    if len(theorem_ids) != 12 or len(set(theorem_ids)) != 12:
        raise AssertionError("theorem coverage")
    by_theorem = {row["theorem_id"]: row for row in theorems}
    if (
        by_theorem["T05"]["result"]
        != "ARBITRARY_ANGULAR_TRANSITION_CANCELS_BLOCKWISE"
        or by_theorem["T08"]["status"] != "OPEN"
        or by_theorem["T09"]["status"] != "OPEN"
        or by_theorem["T11"]["status"] != "OPEN_NOT_DERIVED"
        or by_theorem["T12"]["status"] != "OPEN_NOT_DERIVED"
    ):
        raise AssertionError("theorem scope")

    join_ids = [row["join_id"] for row in joins]
    if len(join_ids) != 7 or len(set(join_ids)) != 7:
        raise AssertionError("join coverage")
    by_join = {row["join_id"]: row for row in joins}
    if (
        by_join["J02"]["status"] != "CONDITIONAL"
        or by_join["J03"]["status"] != "OPEN_NOT_DERIVED"
        or by_join["J04"]["status"] != "OPEN_NOT_DERIVED"
        or by_join["J05"]["status"] != "OPEN_NOT_DERIVED"
        or by_join["J06"]["status"] != "OPEN_NOT_DERIVED"
        or by_join["J07"]["status"] != "OPEN_NOT_ACTIVATED"
    ):
        raise AssertionError("join promotion")

    by_status = {row["object"]: row for row in status}
    if len(status) != 8 or len(by_status) != 8:
        raise AssertionError("status coverage")
    for key in {
        "reciprocal_angular_soldering",
        "full_metric_and_connection_glue",
        "completion_selector",
    }:
        if by_status[key]["status"] != "OPEN_NOT_DERIVED":
            raise AssertionError("status promotion")
    if by_status["density_response"]["status"] != "OPEN_NOT_ACTIVATED":
        raise AssertionError("density activation")

    if len(lineage) != 22 or len({row["path"] for row in lineage}) != 22:
        raise AssertionError("source coverage")
    for row in lineage:
        path = ROOT / row["path"]
        if (
            not path.is_file()
            or sha256(path) != row["sha256"]
            or path.stat().st_size != int(row["size"])
        ):
            raise AssertionError("source identity")

    expected_counts = {
        "completion_rows": 12,
        "parametric_type_rows": 11,
        "conditional_control_rows": 1,
        "complete_g_phi_witnesses": 0,
        "mirror_profiles": 3,
        "mirror_profiles_value_first_second_jet_pass": 3,
        "critical_dphi_mirror_profiles": 1,
        "global_theorems": 12,
        "joins": 7,
        "sources": 22,
        "selected_completions": 0,
    }
    if result["counts"] != expected_counts:
        raise AssertionError("counts")
    if result["angular_ruling"] != (
        "ARBITRARY_ANGULAR_TRANSITION_CANCELS_BLOCKWISE__DESCENT_DOES_NOT_"
        "SELECT_RECIPROCAL_ANGULAR_SOLDERING"
    ):
        raise AssertionError("angular ruling")
    if result["new_positive_result"] != (
        "STATIC_ODD_PHI_PLUS_RECIPROCAL_INVERTING_TRANSITION_GIVES_EXACT_"
        "VALUE_AND_JET_SEAM_DESCENT_EVEN_WHEN_DPHI_VANISHES"
    ):
        raise AssertionError("positive ruling")
    if result["exact_algebra"] != {
        "D_zero": "[[1, 0], [0, 1]]",
        "F_inverts_D": True,
        "F_squared": True,
        "G_preserves_D": True,
        "angular_symbol": "A",
        "arbitrary_angular_factor_cancels_blockwise": True,
        "block_conjugation_with_angular_identity": True,
        "det_D": "1",
        "normalizer_result_replayed_not_new_credit": True,
    }:
        raise AssertionError("recorded algebra")

    algebra = independent_algebra()
    if not (
        algebra["det_D"] == "1"
        and algebra["F_squared"]
        and algebra["F_inverts_D"]
        and algebra["G_preserves_D"]
        and algebra["two_distinct_angular_controls"] == 2
        and algebra["angular_controls_pass"]
        and all(
            values["odd"]
            and values["value_match"]
            and values["first_match"]
            and values["second_match"]
            and values["D_at_seal"] == "[[1, 0], [0, 1]]"
            for values in algebra["profiles"].values()
        )
        and algebra["profiles"]["cubic"]["dphi_at_seal"] == "0"
    ):
        raise AssertionError(f"independent algebra: {algebra}")

    source_registry = read_tsv(
        ROOT
        / "udt_global_metric_assembly_atlas_2026-07-22"
        / "COMPLETION_CLASS_REGISTRY.tsv"
    )
    if {row["completion_id"] for row in source_registry} != set(ids):
        raise AssertionError("source registry replay")


def main() -> None:
    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    atlas = read_tsv(HERE / "COMPLETION_DESCENT_ATLAS.tsv")
    profiles = read_tsv(HERE / "MIRROR_JET_CONTROLS.tsv")
    theorems = read_tsv(HERE / "GLOBAL_DESCENT_THEOREMS.tsv")
    joins = read_tsv(HERE / "JOIN_LEDGER.tsv")
    status = read_tsv(HERE / "STATUS_LEDGER.tsv")
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    validate(result, atlas, profiles, theorems, joins, status, lineage)

    catches: list[dict[str, str]] = []

    def catch(catch_id: str, mutation: str, mutator) -> None:
        values = [
            copy.deepcopy(result),
            copy.deepcopy(atlas),
            copy.deepcopy(profiles),
            copy.deepcopy(theorems),
            copy.deepcopy(joins),
            copy.deepcopy(status),
            copy.deepcopy(lineage),
        ]
        mutator(*values)
        try:
            validate(*values)
        except AssertionError:
            catches.append(
                {"catch_id": catch_id, "mutation": mutation, "status": "CAUGHT"}
            )
            return
        raise AssertionError(f"uncaught mutation {catch_id}: {mutation}")

    catch("C01", "remove_completion", lambda r, a, p, t, j, s, l: a.pop())
    catch(
        "C02",
        "duplicate_completion",
        lambda r, a, p, t, j, s, l: a.append(copy.deepcopy(a[0])),
    )
    catch(
        "C03",
        "promote_complete_witness",
        lambda r, a, p, t, j, s, l: a[0].update(
            data_level="COMPLETE_G_PHI_WITNESS"
        ),
    )
    catch(
        "C04",
        "select_S3",
        lambda r, a, p, t, j, s, l: next(
            row for row in a if row["completion_id"] == "FC04_TWO_CAP_P1"
        ).update(selection_ruling="SELECTED"),
    )
    catch(
        "C05",
        "break_mirror_value_descent",
        lambda r, a, p, t, j, s, l: p[0].update(value_pullback_match="False"),
    )
    catch(
        "C06",
        "erase_cubic_criticality",
        lambda r, a, p, t, j, s, l: p[1].update(dphi_at_seal="1"),
    )
    catch(
        "C07",
        "claim_cubic_complete_solution",
        lambda r, a, p, t, j, s, l: p[1].update(
            scope="COMPLETE_ON_SHELL_FIELD_SOLUTION"
        ),
    )
    catch(
        "C08",
        "select_mirror_angular_lift",
        lambda r, a, p, t, j, s, l: next(
            row for row in a if row["completion_id"] == "FC08_MIRROR_DOUBLE"
        ).update(angular_coupling="ANGULAR_PLUS_IDENTITY_SELECTED"),
    )
    catch(
        "C09",
        "promote_toric_soldering",
        lambda r, a, p, t, j, s, l: next(
            row
            for row in a
            if row["completion_id"] == "FC12_RECIPROCAL_TORIC_DIAGONAL"
        ).update(angular_coupling="NATIVE_SOLDERING_DERIVED"),
    )
    catch(
        "C10",
        "extend_connection_through_singularity",
        lambda r, a, p, t, j, s, l: next(
            row for row in a if row["completion_id"] == "FC06_NONPRIMITIVE_CAP"
        ).update(connection_status="GLOBAL_SMOOTH_CONNECTION"),
    )
    catch(
        "C11",
        "require_orientation_for_value_character",
        lambda r, a, p, t, j, s, l: next(
            row for row in a if row["completion_id"] == "FC09_NONORIENTABLE_GLUE"
        ).update(value_character_status="OBSTRUCTED_WITHOUT_ORIENTATION"),
    )
    catch(
        "C12",
        "remove_periodic_phi_equivariance",
        lambda r, a, p, t, j, s, l: next(
            row
            for row in a
            if row["completion_id"] == "FC07_PERIODIC_TORUS_BUNDLE"
        ).update(required_global_data="GL2Z_ONLY"),
    )
    catch(
        "C13",
        "make_projector_degeneracy_destroy_D",
        lambda r, a, p, t, j, s, l: next(
            row for row in a if row["completion_id"] == "FC10_STRATIFIED_PROJECTOR"
        ).update(dphi_degeneracy_effect="D_UNDEFINED"),
    )
    catch(
        "C14",
        "conflate_nonintegrability_with_D_obstruction",
        lambda r, a, p, t, j, s, l: next(
            row
            for row in a
            if row["completion_id"] == "FC11_NONINTEGRABLE_DISTRIBUTION"
        ).update(value_character_status="OBSTRUCTED"),
    )
    catch(
        "C15",
        "derive_physical_metric_glue",
        lambda r, a, p, t, j, s, l: next(
            row for row in t if row["theorem_id"] == "T08"
        ).update(status="DERIVED"),
    )
    catch(
        "C16",
        "derive_connection_glue",
        lambda r, a, p, t, j, s, l: next(
            row for row in t if row["theorem_id"] == "T09"
        ).update(status="DERIVED"),
    )
    catch(
        "C17",
        "derive_reciprocal_angular_join",
        lambda r, a, p, t, j, s, l: next(
            row for row in t if row["theorem_id"] == "T11"
        ).update(status="DERIVED"),
    )
    catch(
        "C18",
        "derive_realization_selector",
        lambda r, a, p, t, j, s, l: next(
            row for row in t if row["theorem_id"] == "T12"
        ).update(status="DERIVED"),
    )
    catch("C19", "remove_theorem", lambda r, a, p, t, j, s, l: t.pop())
    catch(
        "C20",
        "promote_global_descent_without_cocycle",
        lambda r, a, p, t, j, s, l: next(
            row for row in j if row["join_id"] == "J02"
        ).update(status="DERIVED"),
    )
    catch(
        "C21",
        "activate_density",
        lambda r, a, p, t, j, s, l: next(
            row for row in s if row["object"] == "density_response"
        ).update(status="DERIVED"),
    )
    catch("C22", "remove_source", lambda r, a, p, t, j, s, l: l.pop())
    catch(
        "C23",
        "change_maximum",
        lambda r, a, p, t, j, s, l: r.update(
            maximum_conclusion="COMPLETE_REALIZATION_DERIVED"
        ),
    )
    catch(
        "C24",
        "set_selected_completion_count",
        lambda r, a, p, t, j, s, l: r["counts"].update(
            selected_completions=1
        ),
    )
    catch(
        "C25",
        "credit_prior_normalizer_as_new",
        lambda r, a, p, t, j, s, l: r["exact_algebra"].update(
            normalizer_result_replayed_not_new_credit=False
        ),
    )

    if len(catches) != 25 or any(row["status"] != "CAUGHT" for row in catches):
        raise AssertionError("catch proof count")
    with (HERE / "CATCH_PROOFS.tsv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["catch_id", "mutation", "status"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(catches)

    verification = {
        "schema": "udt-reciprocal-seam-descent-independent-1.0",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "independent_algebra": independent_algebra(),
        "completion_rows": len(atlas),
        "source_hashes_replayed": len(lineage),
        "catch_proofs": len(catches),
        "catch_proofs_passed": len(catches),
        "maximum_conclusion": MAXIMUM,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(verification, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
