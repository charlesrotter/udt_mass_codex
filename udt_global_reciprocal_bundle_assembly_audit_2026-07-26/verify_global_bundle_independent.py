#!/usr/bin/env python3
import csv
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent


def rows(name):
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def exact(table, key, expected):
    values = [r[key] for r in table]
    return len(values) == len(expected) and len(values) == len(set(values)) and set(values) == set(expected)


def zeros(n, m):
    return [[F(0) for _ in range(m)] for _ in range(n)]


def identity(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def flatten(a):
    return [x for row in a for x in row]


def rank(matrix):
    a = [row[:] for row in matrix]
    if not a:
        return 0
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col] != 0), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        value = a[r][col]
        a[r] = [x / value for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col] != 0:
                factor = a[i][col]
                a[i] = [a[i][j] - factor * a[r][j] for j in range(len(a[0]))]
        r += 1
    return r


def diag(values):
    output = zeros(len(values), len(values))
    for i, value in enumerate(values):
        output[i][i] = F(value)
    return output


def lorentz_generator(i, j):
    m = zeros(4, 4)
    m[i][j] = F(1)
    m[j][i] = F(1 if i == 0 else -1)
    return m


basis = [lorentz_generator(0, 1), lorentz_generator(0, 2), lorentz_generator(0, 3), lorentz_generator(1, 2), lorentz_generator(1, 3), lorentz_generator(2, 3)]


def centralizer_dim(lam):
    x = diag([-1, 1, lam, lam])
    columns = [flatten(sub(mul(b, x), mul(x, b))) for b in basis]
    matrix = [[columns[j][i] for j in range(6)] for i in range(16)]
    return 6 - rank(matrix)


def spatial_generators():
    j12 = [[F(0), F(1), F(0)], [F(-1), F(0), F(0)], [F(0), F(0), F(0)]]
    j13 = [[F(0), F(0), F(1)], [F(0), F(0), F(0)], [F(-1), F(0), F(0)]]
    j23 = [[F(0), F(0), F(0)], [F(0), F(0), F(1)], [F(0), F(-1), F(0)]]
    return j12, j13, j23


def holonomy_rank(p, q):
    j12, j13, j23 = spatial_generators()
    k12 = p * q - F(3, 4) * q * q
    k13 = F(1, 4) * q * q
    k23 = F(1, 4) * q * q
    curv = [scale(k12, j12), scale(k13, j13), scale(k23, j23)]
    closure = curv + [sub(mul(a, b), mul(b, a)) for a in curv for b in curv]
    columns = [flatten(m) for m in closure]
    matrix = [[columns[j][i] for j in range(len(columns))] for i in range(9)]
    return rank(matrix), (k12, k13, k23)


completion_u = rows("COMPLETION_UNIVERSE.tsv")
controls_u = rows("CONCRETE_CONTROL_UNIVERSE.tsv")
strata_u = rows("LAMBDA_STRATUM_UNIVERSE.tsv")
gates_u = rows("ASSEMBLY_GATE_UNIVERSE.tsv")
completion = rows("COMPLETION_ASSEMBLY_ATLAS.tsv")
controls = rows("CONCRETE_CONTROL_ASSEMBLY.tsv")
strata = rows("LAMBDA_STRATUM_OUTCOMES.tsv")
gates = rows("ASSEMBLY_GATE_OUTCOMES.tsv")
holonomy = rows("HOMOGENEOUS_HOLONOMY_ATLAS.tsv")
variation = rows("VARIATION_CONSEQUENCE_LEDGER.tsv")
production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())

fc_ids = [r["completion_id"] for r in completion_u]
o = {r["control_id"]: r for r in controls}
s = {r["stratum_id"]: r for r in strata}
g = {r["gate_id"]: r for r in gates}
c = {r["completion_id"]: r for r in completion}
v = {r["variation_id"]: r for r in variation}

checks = {}
checks["completion_universe"] = exact(completion_u, "completion_id", fc_ids) and len(fc_ids) == 12
checks["control_universe"] = exact(controls_u, "control_id", [f"Q{i:02d}" for i in range(1, 5)])
checks["stratum_universe"] = exact(strata_u, "stratum_id", [f"L{i:02d}" for i in range(1, 5)])
checks["gate_universe"] = exact(gates_u, "gate_id", [f"G{i:02d}" for i in range(1, 13)])
checks["completion_outcomes"] = exact(completion, "completion_id", fc_ids)
checks["control_outcomes"] = exact(controls, "control_id", [f"Q{i:02d}" for i in range(1, 5)])
checks["stratum_outcomes"] = exact(strata, "stratum_id", [f"L{i:02d}" for i in range(1, 5)])
checks["gate_outcomes"] = exact(gates, "gate_id", [f"G{i:02d}" for i in range(1, 13)])
checks["variation_outcomes"] = exact(variation, "variation_id", [f"V{i:02d}" for i in range(1, 9)])
checks["centralizer_generic"] = centralizer_dim(F(2)) == 1
checks["centralizer_minus_one"] = centralizer_dim(F(-1)) == 3
checks["centralizer_zero"] = centralizer_dim(F(0)) == 1
checks["centralizer_plus_one"] = centralizer_dim(F(1)) == 3
checks["centralizer_table_generic"] = s["L01"]["connected_lorentz_centralizer_dimension"] == "1"
checks["centralizer_table_minus_one"] = s["L02"]["connected_lorentz_centralizer_dimension"] == "3"
checks["centralizer_table_zero"] = s["L03"]["connected_lorentz_centralizer_dimension"] == "1"
checks["centralizer_table_plus_one"] = s["L04"]["connected_lorentz_centralizer_dimension"] == "3"

x_plus = diag([-1, 1, 1, 1])
x_clock = sub(identity(4), scale(F(2), diag([1, 0, 0, 0])))
x_minus = diag([-1, 1, -1, -1])
x_ruler = sub(scale(F(2), diag([0, 1, 0, 0])), identity(4))
checks["clock_collapse"] = x_plus == x_clock
checks["ruler_collapse"] = x_minus == x_ruler
checks["trace_plus_one"] = sum(x_plus[i][i] for i in range(4)) == 2
checks["trace_zero"] = sum(diag([-1, 1, 0, 0])[i][i] for i in range(4)) == 0

round_rank, round_k = holonomy_rank(F(1), F(1))
squashed_rank, squashed_k = holonomy_rank(F(2), F(1))
checks["round_K"] = round_k == (F(1, 4), F(1, 4), F(1, 4))
checks["squashed_K"] = squashed_k == (F(5, 4), F(1, 4), F(1, 4))
checks["round_holonomy"] = round_rank == 3
checks["squashed_holonomy"] = squashed_rank == 3
checks["holonomy_table"] = [r["spatial_holonomy_lie_rank"] for r in holonomy[:2]] == ["3", "3"]

q = F(2)


def dX_nonzero(lam):
    factor = (F(1) - lam) * q / 2
    return factor != 0


checks["parallel_plus_one"] = not dX_nonzero(F(1))
checks["nonparallel_generic"] = dX_nonzero(F(2))
checks["nonparallel_minus_one"] = dX_nonzero(F(-1))
checks["nonparallel_zero"] = dX_nonzero(F(0))
checks["parallel_table_plus_one"] = s["L04"]["parallel_endpoint_on_concrete_S3_controls"] == "YES_ON_Q01_Q02"
checks["parallel_table_others"] = all(s[x]["parallel_endpoint_on_concrete_S3_controls"] == "NO_ON_Q01_Q02" for x in ["L01", "L02", "L03"])
checks["all_lambda_overlap"] = all(row["pair_bundle_overlap"] == "YES" for row in strata)
checks["all_lambda_path_groupoid"] = all(row["typed_path_groupoid"] == "YES" for row in strata)
checks["no_lambda_depth"] = all(row["signed_depth"] == "NO_FOUNDED_DEPTH" for row in strata)
checks["round_metric_natural_only_plus_one"] = o["Q01"]["metric_natural_X"].startswith("L04_ONLY")
checks["round_ruler_not_selected"] = "CHOSEN_NOT_SELECTED" in o["Q01"]["chosen_global_section"]
checks["squashed_metric_natural_all"] = o["Q02"]["metric_natural_X"].startswith("ALL_LAMBDA")
checks["squashed_off_shell"] = o["Q02"]["scope"] == "OFF_SHELL_CONTROL"
checks["wrl_incomplete"] = o["Q03"]["scope"] == "INCOMPLETE_DO_NOT_SPLICE"
checks["xmax_absent"] = o["Q04"]["pair_frame_bundle"] == "ABSENT"
checks["only_FC04_concrete"] = c["FC04_TWO_CAP_P1"]["pair_bundle_status"] == "PASS_FOR_Q01_Q02_PAIR_FRAME_BUNDLE" and sum(row["pair_bundle_status"].startswith("PASS_") for row in completion) == 1
checks["FC06_regular_strata"] = c["FC06_NONPRIMITIVE_CAP"]["pair_bundle_status"] == "REGULAR_STRATUM_ONLY"
checks["FC07_monodromy_open"] = "MONODROMY" in c["FC07_PERIODIC_TORUS_BUNDLE"]["global_join_status"]
checks["FC08_lift_open"] = "UNSELECTED_LIFT" in c["FC08_MIRROR_DOUBLE"]["global_join_status"]
checks["FC10_rank_transition_open"] = "RANK_CHANGE" in c["FC10_STRATIFIED_PROJECTOR"]["global_join_status"]
checks["FC11_no_orbit_needed"] = c["FC11_NONINTEGRABLE_DISTRIBUTION"]["pair_bundle_status"] == "PAIR_FRAME_BUNDLE_DOES_NOT_REQUIRE_ORBIT_SURFACE"
checks["depth_gate_open"] = g["G11"]["status"] == "OPEN_ABSENT"
checks["variation_gate_open"] = g["G12"]["status"] == "OPEN_UNSELECTED"
checks["causal_type_scoped"] = "NOT_APPLICABLE_UNLESS_PAIR_DERIVED_FROM_DPHI" == g["G10"]["status"]
checks["full_delta_g_retained"] = v["V01"]["status"] == "RETAIN_OPEN_CANDIDATE"
checks["parallelism_extra"] = v["V05"]["status"] == "CONDITIONAL_EXTRA_RESTRICTION"
checks["lambda_not_field"] = v["V03"]["status"] == "NOT_AUTHORIZED"
checks["authority_closed"] = not any(production["authority_boundary"].values())
checks["production_counts"] = production["counts"]["completion_classes"] == 12 and production["counts"]["lambda_strata"] == 4
checks["production_algebra"] = production["algebra"]["centralizer_dimensions"] == {"L01": 1, "L02": 3, "L03": 1, "L04": 3}
checks["maximum_scoped"] = "CONDITIONAL_ON_ENDPOINT_ONLY_REQUIREMENT" in production["maximum_conclusion"] and "LAMBDA_SELECTED" not in production["maximum_conclusion"]

if not all(checks.values()):
    raise AssertionError(sorted(key for key, value in checks.items() if not value))

result = {
    "schema": "udt-global-reciprocal-bundle-assembly-independent-1.0",
    "result": "PASS",
    "counts": {"checks": len(checks), "completion_classes": len(completion), "lambda_strata": len(strata), "assembly_gates": len(gates)},
    "algebra": {"centralizer_dimensions": {str(value): centralizer_dim(F(value)) for value in [2, -1, 0, 1]}, "round_holonomy_rank": round_rank, "squashed_holonomy_rank": squashed_rank, "parallel_lambda": 1},
    "rulings": {"query_bundle": "ALL_LAMBDA", "parallel_endpoint": "LAMBDA_ONE_ONLY_Q01_Q02", "endpoint_requirement": "CONDITIONAL_NOT_SELECTED", "depth": "OPEN"},
    "checks": {key: "PASS" for key in sorted(checks)},
}
(HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
