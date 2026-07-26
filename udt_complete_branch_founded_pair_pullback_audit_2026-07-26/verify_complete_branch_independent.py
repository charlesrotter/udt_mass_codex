#!/usr/bin/env python3
import csv
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


checks = {}


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    r = c = 0
    while r < m and c < n:
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            c += 1
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [v / scale for v in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                factor = a[i][c]
                a[i] = [a[i][j] - factor * a[r][j] for j in range(n)]
        r += 1
        c += 1
    return r


completion = rows(ROOT / "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv")
configs = rows(ROOT / "udt_directional_observer_pair_distance_audit_2026-07-24/CORRECTED_CONFIGURATION_REGISTRY.tsv")
branches = rows(ROOT / "udt_observer_longitudinal_transverse_cocycle_audit_2026-07-24/BRANCH_COCYCLE_ATLAS.tsv")
basis = rows(ROOT / "udt_founded_pair_first_jet_one_form_atlas_2026-07-26/ONE_FORM_BASIS.tsv")
outcomes = {r["id"]: r for r in rows(ROOT / "udt_founded_pair_first_jet_one_form_atlas_2026-07-26/ONE_FORM_OUTCOMES.tsv")}
equations = rows(ROOT / "udt_directional_observer_pair_distance_audit_2026-07-24/EQUATION_FAMILY_PAIR_DISTANCE_SCREEN.tsv")
bootstrap_equations = rows(ROOT / "udt_bootstrap_clock_angular_closure_audit_2026-07-24/EQUATION_FAMILY_GATE_MATRIX.tsv")
generated_completion = rows(HERE / "COMPLETION_PULLBACK_ATLAS.tsv")
generated_concrete = rows(HERE / "CONCRETE_REPRESENTATIVE_ATLAS.tsv")
generated_motifs = rows(HERE / "HOMOGENEOUS_MOTIF_PULLBACK.tsv")
generated_branches = rows(HERE / "BRANCH_PULLBACK_ATLAS.tsv")
generated_gates = rows(HERE / "EIGHT_GATE_MATRIX.tsv")

check("completion_count", len(completion) == len(generated_completion) == 12)
check("completion_identity", [r["completion_id"] for r in completion] == [r["completion_id"] for r in generated_completion])
check("configuration_count", len(configs) == len(generated_concrete) == 4)
check("gate_matrix_count", len(generated_gates) == 4)
check("branch_count", len(branches) == len(generated_branches) == 6)
check("basis_count", len(basis) == len(generated_motifs) == 22)
check("only_FC04_concrete", [r["completion_id"] for r in generated_completion if r["registered_concrete_representatives"] != "-"] == ["FC04_TWO_CAP_P1"])
check("B19_only_complete_equation_family", [r["family_id"] for r in equations if r["complete_spatial_metric"] != "NO"] == ["B19"])
check("zero_complete_simultaneous_closure", len(bootstrap_equations) == 28 and all(r["complete_simultaneous_closure"] == "NO" for r in bootstrap_equations))

# Independent numeric rational controls for three distinct nonround Berger choices and the round case.
# Reconstruct the connection from the left-invariant brackets with the Koszul formula rather than
# importing the production Cartan solve. Curvature and Ricci are then contracted directly.
for label, p, q in [
    ("round", Fraction(3), Fraction(3)),
    ("squash_1", Fraction(2), Fraction(5)),
    ("squash_2", Fraction(7, 3), Fraction(4, 5)),
    ("squash_3", Fraction(-2), Fraction(3)),
]:
    # Spatial order (s1,s2,n). de1=p e2^n, de2=p n^e1, dn=q e1^e2.
    bracket = [[[Fraction(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for i, j, k, value in [
        (1, 2, 0, -p),
        (2, 0, 1, -p),
        (0, 1, 2, -q),
    ]:
        bracket[i][j][k] = value
        bracket[j][i][k] = -value

    gamma = [[[Fraction(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                gamma[i][j][k] = (
                    bracket[i][j][k] - bracket[j][k][i] + bracket[k][i][j]
                ) / 2

    check(f"koszul_nabla_s1_n_{label}", gamma[0][2][1] == q / 2)
    check(f"koszul_nabla_s2_n_{label}", gamma[1][2][0] == -q / 2)
    check(f"koszul_nabla_n_n_{label}", all(gamma[2][2][k] == 0 for k in range(3)))

    curvature = [[[[Fraction(0) for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for ell in range(3):
                    curvature[i][j][k][ell] = sum(
                        gamma[j][k][m] * gamma[i][m][ell]
                        - gamma[i][k][m] * gamma[j][m][ell]
                        - bracket[i][j][m] * gamma[m][k][ell]
                        for m in range(3)
                    )
    ricci = [[sum(curvature[i][j][k][i] for i in range(3)) for k in range(3)] for j in range(3)]
    ric_screen = p * q - q * q / 2
    ric_hopf = q * q / 2
    check(f"ricci_screen_1_{label}", ricci[0][0] == ric_screen)
    check(f"ricci_screen_2_{label}", ricci[1][1] == ric_screen)
    check(f"ricci_hopf_{label}", ricci[2][2] == ric_hopf)
    check(f"ricci_offdiagonal_{label}", all(ricci[i][j] == 0 for i in range(3) for j in range(3) if i != j))
    check(f"ricci_gap_{label}", ricci[2][2] - ricci[0][0] == q * (q - p))
    check(f"isotropy_class_{label}", (ricci[2][2] == ricci[0][0]) == (p == q))

ids = [r["id"] for r in basis]
cols = []
dcols = []
for mid in ids:
    if mid == "N07":
        cols.append([-1, 0, 0, 0])
        dcols.append([0, 0, 0, 0, 0, 0])
    elif mid == "N08":
        cols.append([0, 1, 0, 0])
        dcols.append([0, 0, 0, 0, 0, 1])
    else:
        cols.append([0, 0, 0, 0])
        dcols.append([0, 0, 0, 0, 0, 0])

image = [[cols[j][i] for j in range(len(cols))] for i in range(4)]
derivative = [[dcols[j][i] for j in range(len(dcols))] for i in range(6)]
check("image_rank_two", rank(image) == 2)
check("exterior_rank_one", rank(derivative) == 1)

o2_indices = [i for i, r in enumerate(basis) if r["uses_screen_orientation"] == "NO"]
n_even_indices = [i for i, r in enumerate(basis) if outcomes[r["id"]]["n_flip_parity"] == "EVEN"]

def selected_rank(indices):
    return rank([[cols[j][i] for j in indices] for i in range(4)])

check("O2_rank_zero", selected_rank(o2_indices) == 0)
check("n_even_rank_one", selected_rank(n_even_indices) == 1)
check("O2_n_even_rank_zero", selected_rank([i for i in o2_indices if i in n_even_indices]) == 0)

motif_by_id = {r["id"]: r for r in generated_motifs}
check("only_N07_N08_nonzero", {i for i, r in motif_by_id.items() if r["homogeneous_pair_pullback"] != "0"} == {"N07", "N08"})
check("N07_time_not_depth", motif_by_id["N07"]["founded_depth_status"] == "NO_COORDINATE_TIME_NOT_RECIPROCAL_DEPTH")
check("N08_nonclosed", motif_by_id["N08"]["closed"].startswith("NO_"))

concrete = {r["representative_id"]: r for r in generated_concrete}
check("B19_not_intrinsic", "NONE_METRIC_SELECTED" in concrete["Q01_ROUND_S3_B19"]["n_status"])
check("squashed_off_shell", concrete["Q02_SQUASHED_S3_OFF_SHELL"]["metric_status"] == "COMPLETE_HOMOGENEOUS_OFF_SHELL_CONTROL")
check("WRL_local", concrete["Q03_WRL_LOCAL"]["ruling"] == "FAIL_COMPLETE_REPRESENTATIVE_GATE")
check("Xmax_absent", concrete["Q04_PHYSICAL_XMAX_JOIN"]["ruling"] == "FAIL_ABSENT_REPRESENTATIVE")
check("zero_full_witness", not any(r["ruling"] == "PASS_ALL_EIGHT_GATES" for r in generated_concrete))
check("zero_eight_gate_pass", all(r["all_gates"] == "NO" for r in generated_gates))

result = {
    "result": "PASS",
    "checks": checks,
    "counts": {
        "checks": len(checks),
        "completion_classes": len(completion),
        "configurations": len(configs),
        "branches": len(branches),
        "basis": len(basis),
        "rational_controls": 4,
        "full_witnesses": 0,
    },
    "maximum_conclusion": "NO_REGISTERED_COMPLETE_PULLBACK_WITNESS",
}
(HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
