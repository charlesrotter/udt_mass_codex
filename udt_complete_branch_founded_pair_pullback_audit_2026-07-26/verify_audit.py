#!/usr/bin/env python3
import copy
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FC_IDS = {
    "FC01_BOUNDARY_BOUNDARY", "FC02_ONE_CAP_BOUNDARY", "FC03_TWO_CAP_P0",
    "FC04_TWO_CAP_P1", "FC05_TWO_CAP_P_GT1", "FC06_NONPRIMITIVE_CAP",
    "FC07_PERIODIC_TORUS_BUNDLE", "FC08_MIRROR_DOUBLE", "FC09_NONORIENTABLE_GLUE",
    "FC10_STRATIFIED_PROJECTOR", "FC11_NONINTEGRABLE_DISTRIBUTION",
    "FC12_RECIPROCAL_TORIC_DIAGONAL",
}
Q_IDS = {"Q01_ROUND_S3_B19", "Q02_SQUASHED_S3_OFF_SHELL", "Q03_WRL_LOCAL", "Q04_PHYSICAL_XMAX_JOIN"}
B_IDS = {
    "B19_ROUND_S3", "SQUASHED_S3_OFF_SHELL", "WRL_LOCAL_RESIDUAL",
    "TEMPORAL_PHI_SLICE_FAMILY", "CONSTANT_SPATIAL_CURVATURE_STATIC_CONTROL",
    "UNIVERSAL_PHYSICAL_UDT",
}
MOTIF_IDS = {f"W{i:02d}" for i in range(1, 7)} | {f"U{i:02d}" for i in range(1, 9)} | {f"N{i:02d}" for i in range(1, 9)}


def rows(name):
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def exact(values, key, identities):
    actual = [row[key] for row in values]
    if len(actual) != len(set(actual)) or set(actual) != identities:
        raise AssertionError(f"identity coverage:{key}")


def validate_sources(corrupt=False):
    scope = rows("SOURCE_SCOPE.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    if [r["source_path"] for r in scope] != [r["source_path"] for r in manifest]:
        raise AssertionError("source order")
    for index, row in enumerate(manifest):
        path = ROOT / row["source_path"]
        expected = "0" * 64 if corrupt and index == 0 else row["sha256"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected or path.stat().st_size != int(row["size"]):
            raise AssertionError("source identity")


def validate_model(completions, concrete, branches, motifs, gates, production, independent):
    exact(completions, "completion_id", FC_IDS)
    exact(concrete, "representative_id", Q_IDS)
    exact(branches, "branch", B_IDS)
    exact(motifs, "id", MOTIF_IDS)
    exact(gates, "representative_id", Q_IDS)

    c = {r["completion_id"]: r for r in completions}
    q = {r["representative_id"]: r for r in concrete}
    b = {r["branch"]: r for r in branches}
    m = {r["id"]: r for r in motifs}
    g = {r["representative_id"]: r for r in gates}

    if [r["completion_id"] for r in completions if r["registered_concrete_representatives"] != "-"] != ["FC04_TWO_CAP_P1"]:
        raise AssertionError("taxonomy promoted")
    if c["FC12_RECIPROCAL_TORIC_DIAGONAL"]["metric_witness_status"] != "PARAMETRIC_METRIC_ANSATZ_PROFILE_AND_ENDPOINT_OPEN":
        raise AssertionError("FC12 promoted")
    if "NONE_METRIC_SELECTED" not in q["Q01_ROUND_S3_B19"]["n_status"]:
        raise AssertionError("B19 axis promoted")
    if q["Q02_SQUASHED_S3_OFF_SHELL"]["metric_status"] != "COMPLETE_HOMOGENEOUS_OFF_SHELL_CONTROL":
        raise AssertionError("squashed promoted")
    if q["Q03_WRL_LOCAL"]["ruling"] != "FAIL_COMPLETE_REPRESENTATIVE_GATE":
        raise AssertionError("WRL spliced")
    if q["Q04_PHYSICAL_XMAX_JOIN"]["ruling"] != "FAIL_ABSENT_REPRESENTATIVE":
        raise AssertionError("absent join promoted")
    if b["CONSTANT_SPATIAL_CURVATURE_STATIC_CONTROL"]["pullback_ruling"] != "COMPARISON_NOT_REGISTERED_UDT_BRANCH":
        raise AssertionError("comparison promoted")

    nonzero = {mid for mid, row in m.items() if row["homogeneous_pair_pullback"] != "0"}
    if nonzero != {"N07", "N08"}:
        raise AssertionError("motif pullback")
    if m["N07"]["closed"] != "YES" or m["N07"]["founded_depth_status"] != "NO_COORDINATE_TIME_NOT_RECIPROCAL_DEPTH":
        raise AssertionError("time line promoted")
    if not m["N08"]["closed"].startswith("NO_") or m["N08"]["n_flip_parity"] != "ODD":
        raise AssertionError("fiber line promoted")
    if q["Q01_ROUND_S3_B19"]["orientation_free_rank"] != "0" or q["Q02_SQUASHED_S3_OFF_SHELL"]["orientation_free_rank"] != "0":
        raise AssertionError("orientation hidden")
    if g["Q01_ROUND_S3_B19"]["G4_metric_selected_n"] != "FAIL_ROUND_ISOTROPY":
        raise AssertionError("global vector mistaken for selection")
    if any(row["all_gates"] != "NO" for row in gates):
        raise AssertionError("full witness promoted")

    if production.get("result") != "PASS" or production.get("grade") != "VERIFIED_WITH_CAVEATS_REGISTERED_COMPLETE_BRANCH_PULLBACK":
        raise AssertionError("production status")
    expected_counts = {
        "source_rows": 18, "completion_classes": 12, "corrected_configurations": 4,
        "branch_rows": 6, "equation_families": 28, "first_jet_basis": 22,
        "completion_classes_with_concrete_representatives": 1,
        "concrete_complete_metric_configurations": 2, "conditional_or_on_shell_complete": 1,
        "off_shell_complete_controls": 1, "full_founded_depth_witnesses": 0,
    }
    if production.get("counts") != expected_counts or set(production.get("checks", {}).values()) != {"PASS"}:
        raise AssertionError("production counts")
    h = production.get("homogeneous_control", {})
    if (h.get("conditional_motif_rank"), h.get("orientation_free_rank"), h.get("n_even_rank"), h.get("orientation_free_n_even_rank"), h.get("exterior_rank")) != (2, 0, 1, 0, 1):
        raise AssertionError("homogeneous ranks")
    if any(production.get("authority_boundary", {}).values()):
        raise AssertionError("authority exceeded")
    if "HIGHER_JET" in production.get("maximum_conclusion", "") or not production.get("maximum_conclusion", "").endswith("NO_REGISTERED_COMPLETE_PULLBACK_WITNESS"):
        raise AssertionError("maximum conclusion")

    if independent.get("result") != "PASS" or independent.get("maximum_conclusion") != "NO_REGISTERED_COMPLETE_PULLBACK_WITNESS":
        raise AssertionError("independent status")
    if independent.get("counts", {}).get("full_witnesses") != 0 or independent.get("counts", {}).get("rational_controls") != 4:
        raise AssertionError("independent counts")
    if set(independent.get("checks", {}).values()) != {"PASS"}:
        raise AssertionError("independent checks")


def changed(table, key, identity, field, value):
    output = copy.deepcopy(table)
    next(row for row in output if row[key] == identity)[field] = value
    return output


def expect_failure(callback):
    try:
        callback()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main():
    completions = rows("COMPLETION_PULLBACK_ATLAS.tsv")
    concrete = rows("CONCRETE_REPRESENTATIVE_ATLAS.tsv")
    branches = rows("BRANCH_PULLBACK_ATLAS.tsv")
    motifs = rows("HOMOGENEOUS_MOTIF_PULLBACK.tsv")
    gates = rows("EIGHT_GATE_MATRIX.tsv")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    validate_model(completions, concrete, branches, motifs, gates, production, independent)
    validate_sources()

    def model(c=completions, q=concrete, b=branches, m=motifs, g=gates, p=production, i=independent):
        return lambda: validate_model(c, q, b, m, g, p, i)

    catches = {}
    catches["missing_completion"] = expect_failure(model(c=completions[:-1]))
    catches["duplicate_configuration"] = expect_failure(model(q=concrete + [copy.deepcopy(concrete[0])]))
    catches["missing_branch"] = expect_failure(model(b=branches[:-1]))
    catches["taxonomy_as_metric"] = expect_failure(model(c=changed(completions, "completion_id", "FC01_BOUNDARY_BOUNDARY", "registered_concrete_representatives", "INVENTED")))
    catches["B19_axis_promotion"] = expect_failure(model(q=changed(concrete, "representative_id", "Q01_ROUND_S3_B19", "n_status", "METRIC_SELECTED")))
    catches["squashed_on_shell_promotion"] = expect_failure(model(q=changed(concrete, "representative_id", "Q02_SQUASHED_S3_OFF_SHELL", "metric_status", "ON_SHELL_NATIVE")))
    catches["WRL_splice"] = expect_failure(model(q=changed(concrete, "representative_id", "Q03_WRL_LOCAL", "ruling", "PASS_COMPLETE")))
    catches["time_as_founded_depth"] = expect_failure(model(m=changed(motifs, "id", "N07", "founded_depth_status", "DERIVED_FOUNDED_DEPTH")))
    catches["nonclosed_as_exact"] = expect_failure(model(m=changed(motifs, "id", "N08", "closed", "YES")))
    catches["orientation_hidden"] = expect_failure(model(q=changed(concrete, "representative_id", "Q02_SQUASHED_S3_OFF_SHELL", "orientation_free_rank", "1")))
    catches["ruler_sign_hidden"] = expect_failure(model(m=changed(motifs, "id", "N08", "n_flip_parity", "EVEN")))
    catches["global_vector_as_selection"] = expect_failure(model(g=changed(gates, "representative_id", "Q01_ROUND_S3_B19", "G4_metric_selected_n", "PASS")))
    bad_independent = copy.deepcopy(independent)
    bad_independent["counts"]["full_witnesses"] = 1
    catches["independent_recomputation"] = expect_failure(model(i=bad_independent))
    bad_higher = copy.deepcopy(production)
    bad_higher["maximum_conclusion"] += ";HIGHER_JET_RULE"
    catches["higher_jet_escape"] = expect_failure(model(p=bad_higher))
    bad_physics = copy.deepcopy(production)
    bad_physics["authority_boundary"]["action_selected"] = True
    catches["physics_promotion"] = expect_failure(model(p=bad_physics))
    catches["source_identity"] = expect_failure(lambda: validate_sources(True))

    if len(catches) != 16 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch coverage")
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch", "result"])
        writer.writerows(sorted(catches.items()))
    result = {
        "schema": "udt-complete-branch-founded-pair-pullback-verification-1.0",
        "result": "PASS",
        "grade": production["grade"],
        "completion_rows": len(completions),
        "concrete_rows": len(concrete),
        "branch_rows": len(branches),
        "motif_rows": len(motifs),
        "gate_rows": len(gates),
        "production_checks": len(production["checks"]),
        "independent_checks": len(independent["checks"]),
        "catch_count": len(catches),
        "catch_proofs": catches,
        "full_witnesses": 0,
        "maximum_conclusion": production["maximum_conclusion"],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
