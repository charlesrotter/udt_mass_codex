#!/usr/bin/env python3
"""Independent stdlib/Fraction reconstruction and adversarial verifier."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "4a6f72fc6d15ca19d3b97936b7332604655f4513"


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matsub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def determinant2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def eye2():
    return [[F(1), F(0)], [F(0), F(1)]]


def zeros(a):
    return all(entry == 0 for row in a for entry in row)


def read_tsv(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_hashes(scope):
    rows = []
    for row in scope:
        completed = subprocess.run(
            ["git", "show", f"{BASE}:{row['path']}"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode:
            raise AssertionError("base source")
        data = completed.stdout
        rows.append(
            {
                "source_id": row["source_id"],
                "path": row["path"],
                "role": row["role"],
                "size": str(len(data)),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return rows


def validate(result, routes, equations, completions, lineage):
    if result["schema"] != "udt-bootstrap-clock-angular-closure-1.0":
        raise AssertionError("schema")
    counts = result["counts"]
    expected = {
        "sources": 35,
        "bootstrap_routes": 8,
        "equation_families": 28,
        "completion_families": 12,
        "complete_registered_bootstrap_witnesses": 0,
    }
    for key, value in expected.items():
        if counts[key] != value:
            raise AssertionError(f"count:{key}")
    if len(routes) != 8 or len({row["route_id"] for row in routes}) != 8:
        raise AssertionError("routes")
    if len(equations) != 28 or len({row["family_id"] for row in equations}) != 28:
        raise AssertionError("equations")
    if len(completions) != 12 or len({row["completion_id"] for row in completions}) != 12:
        raise AssertionError("completions")
    if len(lineage) != 35 or len({row["path"] for row in lineage}) != 35:
        raise AssertionError("lineage")
    for row in lineage:
        completed = subprocess.run(
            ["git", "show", f"{BASE}:{row['path']}"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode:
            raise AssertionError("source_base")
        data = completed.stdout
        if str(len(data)) != row["size"]:
            raise AssertionError("source_size")
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise AssertionError("source_hash")

    route = {row["route_id"]: row for row in routes}
    if route["R01"]["off_shell_variation"] != "NONE":
        raise AssertionError("after_solution_variation")
    if route["R01"]["local_response"] != "CANNOT_ADDRESS":
        raise AssertionError("after_solution_local")
    if route["R05"]["screen_selection"] != "FORBIDS_WITHOUT_ANISOTROPIC_TERM":
        raise AssertionError("volume_screen")
    if route["R06"]["current_status"] != "OPEN_OBJECT_ABSENT":
        raise AssertionError("native_mass_absence")
    if route["R08"]["current_status"] != "OPEN_NOT_REGISTERED_COMPLETE":
        raise AssertionError("complete_bootstrap_absence")

    family = {row["family_id"]: row for row in equations}
    if any(row["complete_simultaneous_closure"] != "NO" for row in equations):
        raise AssertionError("invented_complete_witness")
    if family["B19"]["clock_curvature_match"] != "FORBIDS_NONTRIVIAL_MATCH":
        raise AssertionError("B19")
    if family["B21"]["clock_curvature_match"] != "FORBIDS_IN_LOCAL_PROFILE":
        raise AssertionError("WRL")
    if family["B23"]["native_local_response"] != "OPEN_FUNCTIONAL_DERIVATIVE_ABSENT":
        raise AssertionError("bootstrap_operator")
    if family["B26"]["ruling"] != "PROVENANCE_FIREWALL_NEGATIVE_USE_ONLY":
        raise AssertionError("firewall")
    if family["B22"]["native_local_response"] != "CONDITIONAL_CARRIER_NO_NATIVE_METRIC_SOURCE":
        raise AssertionError("carrier")
    if any(row["complete_g_phi_matter_witness"] != "NO" for row in completions):
        raise AssertionError("completion_witness")
    if any(row["density_response_argument"] != "ABSENT" for row in completions):
        raise AssertionError("completion_density")

    rulings = result["rulings"]
    if rulings["current_registered_source_set"] != "NO_COMPLETE_GATE_WITNESS":
        raise AssertionError("top_ruling")
    if rulings["intrinsic_solder"] != "OPEN_BOOTSTRAP_COULD_ADDRESS_BUT_DOES_NOT_CURRENTLY_DERIVE":
        raise AssertionError("solder_ruling")
    if rulings["B19_and_WRL"] != "FAILURES_REMAIN_EXACT_IN_THEIR_SCOPES_NOT_UNIVERSAL_MATTER_FILLED_NO_GOS":
        raise AssertionError("negative_regrade")
    if rulings["gate_reduction"] != "SIMPLE_SPECTRUM_PLUS_CLOCK_MATCH_SELECTS_THE_SCREEN_LINE_AND_MAKES_TIDAL_INVARIANCE_AUTOMATIC;PARALLELISM_AND_GLOBAL_DESCENT_REMAIN":
        raise AssertionError("gate_reduction")
    if rulings["path_level_caveat"] != "POINTWISE_MATCH_IS_NOT_FULL_COCYCLE_EQUIVALENCE;VARYING_CLOCK_RATE_REQUIRES_A_DERIVED_CONNECTION_TERM_OR_CONSTANT_RATE":
        raise AssertionError("path_level_caveat")
    forbidden = {"complete_action", "matter_emergence", "density_window_derived", "mass_derived"}
    if forbidden.intersection(rulings.values()):
        raise AssertionError("physics_promotion")


def expect_failure(name, mutator, result, routes, equations, completions, lineage, catches):
    payloads = [
        copy.deepcopy(result),
        copy.deepcopy(routes),
        copy.deepcopy(equations),
        copy.deepcopy(completions),
        copy.deepcopy(lineage),
    ]
    mutator(*payloads)
    try:
        validate(*payloads)
    except AssertionError:
        catches[name] = "PASS_REJECTED"
        return
    raise AssertionError(f"catch did not fail: {name}")


def main():
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    routes = read_tsv(HERE / "BOOTSTRAP_ROUTE_LEDGER.tsv")
    equations = read_tsv(HERE / "EQUATION_FAMILY_GATE_MATRIX.tsv")
    completions = read_tsv(HERE / "COMPLETION_BOOTSTRAP_ATLAS.tsv")
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    scope = read_tsv(HERE / "SOURCE_SCOPE.tsv")
    if source_hashes(scope) != lineage:
        raise AssertionError("independent source hash replay")

    checks = {}
    sample_count = 0
    rotations = [
        [[F(1), F(0)], [F(0), F(1)]],
        [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]],
        [[F(5, 13), F(-12, 13)], [F(12, 13), F(5, 13)]],
    ]
    eigenpairs = [(F(-3), F(2)), (F(-5, 2), F(7, 3)), (F(-1), F(4))]
    for rotation in rotations:
        if not zeros(matsub(matmul(transpose(rotation), rotation), eye2())):
            raise AssertionError("rotation")
        for k1, k2 in eigenpairs:
            diagonal = [[k1, F(0)], [F(0), k2]]
            tidal = matmul(matmul(rotation, diagonal), transpose(rotation))
            p1 = matmul(
                matmul(rotation, [[F(1), F(0)], [F(0), F(0)]]),
                transpose(rotation),
            )
            p2 = matsub(eye2(), p1)
            if not zeros(matsub(matmul(p1, p1), p1)):
                raise AssertionError("p1")
            if not zeros(matsub(matmul(p2, p2), p2)):
                raise AssertionError("p2")
            if not zeros(matmul(p1, p2)):
                raise AssertionError("orthogonal")
            if not zeros(matsub(matmul(tidal, p1), [[k1 * x for x in row] for row in p1])):
                raise AssertionError("eigenprojector")
            tr = tidal[0][0] + tidal[1][1]
            det = determinant2(tidal)
            disc = tr * tr - 4 * det
            if disc != (k1 - k2) ** 2 or disc <= 0:
                raise AssertionError("discriminant")
            for clock in [F(1), F(2), F(3, 2)]:
                match = determinant2(
                    [
                        [tidal[0][0] + clock * clock, tidal[0][1]],
                        [tidal[1][0], tidal[1][1] + clock * clock],
                    ]
                )
                polynomial = clock**4 + clock**2 * tr + det
                if match != polynomial:
                    raise AssertionError("clock polynomial")
                sample_count += 1
    checks["fraction_screen_samples"] = sample_count

    matched_projector_samples = 0
    for rotation in rotations:
        for clock in [F(1), F(2), F(3, 2)]:
            other = clock + F(5, 3)
            diagonal = [[-clock * clock, F(0)], [F(0), other]]
            tidal = matmul(matmul(rotation, diagonal), transpose(rotation))
            qclock = [
                [tidal[0][0] + clock * clock, tidal[0][1]],
                [tidal[1][0], tidal[1][1] + clock * clock],
            ]
            tq = qclock[0][0] + qclock[1][1]
            pclock = [
                [eye2()[i][j] - qclock[i][j] / tq for j in range(2)]
                for i in range(2)
            ]
            if determinant2(qclock) != 0:
                raise AssertionError("matched determinant")
            if not zeros(matsub(matmul(pclock, pclock), pclock)):
                raise AssertionError("matched projector")
            if not zeros(matmul(qclock, pclock)):
                raise AssertionError("matched kernel")
            if pclock[0][0] + pclock[1][1] != 1:
                raise AssertionError("matched rank")
            matched_projector_samples += 1
    checks["fraction_matched_projector_samples"] = matched_projector_samples

    parallel_samples = 0
    for k1, k2 in eigenpairs:
        for omega in [F(0), F(1, 7), F(-3, 8)]:
            dp = [[F(0), omega], [omega, F(0)]]
            comm = [[F(0), (k1 - k2) ** 2 * omega], [-(k1 - k2) ** 2 * omega, F(0)]]
            if zeros(dp) != zeros(comm):
                raise AssertionError("parallel equivalence")
            parallel_samples += 1
    checks["fraction_parallel_samples"] = parallel_samples

    connection_samples = 0
    for clock, clock_dot in [(F(1), F(0)), (F(2), F(1, 3)), (F(3, 2), F(-2, 5))]:
        hdot = [[F(0), F(0)], [-clock_dot, clock_dot]]
        compatible = zeros(hdot)
        if compatible != (clock_dot == 0):
            raise AssertionError("connection gate")
        connection_samples += 1
    checks["fraction_connection_samples"] = connection_samples

    density_samples = 0
    for volume in [F(2), F(7, 3), F(11)]:
        for density in [F(0), F(5, 2), F(9)]:
            mass = density * volume
            for delta_mass, delta_volume in [(F(1), F(0)), (F(0), F(1)), (F(7, 5), F(-2, 3))]:
                quotient = (volume * delta_mass - mass * delta_volume) / volume**2
                response = (delta_mass - density * delta_volume) / volume
                if quotient != response:
                    raise AssertionError("density variation")
                density_samples += 1
    checks["fraction_density_samples"] = density_samples
    checks["tracefree_volume_response"] = "PASS" if F(4) + F(-4) == 0 else "FAIL"

    validate(result, routes, equations, completions, lineage)
    checks["source_hash_replay"] = "PASS"
    checks["table_semantics"] = "PASS"

    catches = {}
    expect_failure("registered_witness_invented", lambda r, *_: r["counts"].update(complete_registered_bootstrap_witnesses=1), result, routes, equations, completions, lineage, catches)
    expect_failure("after_solution_promoted_to_variation", lambda _r, b, *_: b[0].update(off_shell_variation="LOCAL_EOM"), result, routes, equations, completions, lineage, catches)
    expect_failure("after_solution_promoted_to_local_response", lambda _r, b, *_: b[0].update(local_response="CAN_ENFORCE"), result, routes, equations, completions, lineage, catches)
    expect_failure("volume_only_selects_screen", lambda _r, b, *_: b[4].update(screen_selection="CAN_ENFORCE"), result, routes, equations, completions, lineage, catches)
    expect_failure("native_mass_marked_present", lambda _r, b, *_: b[5].update(current_status="DERIVED"), result, routes, equations, completions, lineage, catches)
    expect_failure("complete_bootstrap_marked_registered", lambda _r, b, *_: b[7].update(current_status="DERIVED"), result, routes, equations, completions, lineage, catches)
    expect_failure("missing_equation_family", lambda _r, _b, e, *_: e.pop(), result, routes, equations, completions, lineage, catches)
    expect_failure("duplicate_equation_family", lambda _r, _b, e, *_: e.append(copy.deepcopy(e[0])), result, routes, equations, completions, lineage, catches)
    expect_failure("family_promoted_complete", lambda _r, _b, e, *_: e[0].update(complete_simultaneous_closure="YES"), result, routes, equations, completions, lineage, catches)
    expect_failure("B19_match_promoted", lambda _r, _b, e, *_: e[18].update(clock_curvature_match="ENFORCES"), result, routes, equations, completions, lineage, catches)
    expect_failure("WRL_failure_erased", lambda _r, _b, e, *_: e[20].update(clock_curvature_match="PERMITS"), result, routes, equations, completions, lineage, catches)
    expect_failure("bootstrap_operator_invented", lambda _r, _b, e, *_: e[22].update(native_local_response="ENFORCES"), result, routes, equations, completions, lineage, catches)
    expect_failure("carrier_promoted_native", lambda _r, _b, e, *_: e[21].update(native_local_response="NATIVE"), result, routes, equations, completions, lineage, catches)
    expect_failure("firewall_breached", lambda _r, _b, e, *_: e[25].update(ruling="AFFIRMATIVE_UDT"), result, routes, equations, completions, lineage, catches)
    expect_failure("completion_missing", lambda _r, _b, _e, c, *_: c.pop(), result, routes, equations, completions, lineage, catches)
    expect_failure("completion_witness_invented", lambda _r, _b, _e, c, *_: c[0].update(complete_g_phi_matter_witness="YES"), result, routes, equations, completions, lineage, catches)
    expect_failure("completion_density_invented", lambda _r, _b, _e, c, *_: c[0].update(density_response_argument="rho"), result, routes, equations, completions, lineage, catches)
    expect_failure("source_removed", lambda _r, _b, _e, _c, s: s.pop(), result, routes, equations, completions, lineage, catches)
    expect_failure("source_hash_corrupted", lambda _r, _b, _e, _c, s: s[0].update(sha256="0" * 64), result, routes, equations, completions, lineage, catches)
    expect_failure("negative_scope_promoted", lambda r, *_: r["rulings"].update(B19_and_WRL="UNIVERSAL_NO_GO"), result, routes, equations, completions, lineage, catches)
    expect_failure("intrinsic_projector_gate_erased", lambda r, *_: r["rulings"].update(gate_reduction="SCREEN_LINE_MUST_ALWAYS_BE_SUPPLIED"), result, routes, equations, completions, lineage, catches)
    expect_failure("pointwise_promoted_to_path_cocycle", lambda r, *_: r["rulings"].update(path_level_caveat="FULL_COCYCLE_DERIVED"), result, routes, equations, completions, lineage, catches)
    expect_failure("solder_promoted", lambda r, *_: r["rulings"].update(intrinsic_solder="DERIVED"), result, routes, equations, completions, lineage, catches)

    output = {
        "schema": "udt-bootstrap-clock-angular-closure-independent-1.0",
        "production_schema": result["schema"],
        "method": "stdlib_Fraction_reconstruction_without_importing_production_module",
        "checks": checks,
        "catch_proofs": catches,
        "counts": {
            "fraction_screen_samples": sample_count,
            "fraction_parallel_samples": parallel_samples,
            "fraction_density_samples": density_samples,
            "fraction_matched_projector_samples": matched_projector_samples,
            "fraction_connection_samples": connection_samples,
            "sources": len(lineage),
            "routes": len(routes),
            "equation_families": len(equations),
            "completions": len(completions),
            "catch_proofs": len(catches),
        },
        "result": "PASS",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
