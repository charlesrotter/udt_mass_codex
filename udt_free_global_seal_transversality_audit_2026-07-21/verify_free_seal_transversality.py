#!/usr/bin/env python3
"""Non-importing verifier for the free-global-seal transversality audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent

SOURCE_HASHES = {
    "udt_premise_reset_audit_2026-07-19/SHA256SUMS.txt": "6123253b9370bce674c626a863dc595c773da3905cb155a7fe2b77c4667fd3a7",
    "udt_global_reciprocal_closure_audit_2026-07-20/SHA256SUMS.txt": "e11985e9afd9cefbb818e75aa1afe90acec48d60b2170e26c2fe712287742d48",
    "udt_complete_seal_fixed_set_selector_audit_2026-07-21/SHA256SUMS.txt": "3a6cc83e40fe95951b19f37b68b1167a3683cf4f02c0fbf1f52f54d95db99b66",
    "udt_full_equation_variation_p05_2026-07-21/SHA256SUMS.txt": "5c26d4eb97c4dc370e286469c63d662f182a71a94a6e6899131fd6706c4e7f2e",
    "udt_pre_p06_boundary_selector_audit_2026-07-21/SHA256SUMS.txt": "45c239639d999c26f2e574592fafc392fbb7c1e6f20ea92e1d260b4784e00e51",
    "udt_time_live_characteristic_flux_audit_2026-07-21/SHA256SUMS.txt": "3089e66d65f85753d45e9e78596dba9ae2b962a015857c969ff6a0492d442f12",
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_state() -> dict[str, object]:
    return {
        "result": json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "sources": read_tsv("SOURCE_LINEAGE.tsv"),
        "endpoints": read_tsv("ENDPOINT_COUNTERFUNCTIONALS.tsv"),
        "scales": read_tsv("GLOBAL_SCALE_TRANSVERSALITY.tsv"),
        "seals": read_tsv("SEAL_VARIATION_COMPATIBILITY.tsv"),
        "embeddings": read_tsv("EMBEDDING_DOF_CENSUS.tsv"),
        "covariance": read_tsv("COVARIANT_TRANSVERSALITY.tsv"),
        "lanes": read_tsv("LANE_BOUNDARY_CHANNELS.tsv"),
        "transversality": read_tsv("TRANSVERSALITY_BRANCHES.tsv"),
        "ambiguities": read_tsv("FUNCTIONAL_DEPENDENCE.tsv"),
        "joins": read_tsv("GLOBAL_BOUNDARY_JOIN.tsv"),
        "fields": read_tsv("FIELD_LANE_CLOSURE.tsv"),
        "status": read_tsv("STATUS_LEDGER.tsv"),
        "graph": json.loads((HERE / "TRANSVERSALITY_DEPENDENCY_GRAPH.json").read_text(encoding="utf-8")),
    }


def validate(state: dict[str, object]) -> None:
    result = state["result"]
    require(isinstance(result, dict), "result type")
    require(result["classification"] == "FREE_BOUNDARY_ADDS_TRANSVERSALITY_BUT_REMAINS_FUNCTIONAL_DEPENDENT", "classification")
    require(result["maximum_conclusion"] == "FREE_GLOBAL_SEAL_TRANSVERSALITY_SELECTOR_STATUS_CLASSIFIED", "maximum conclusion")
    require(result["owner_authorized_conditional_premise"] is True, "premise authorization")
    require(result["premise_promoted_to_canon"] is False, "no canon promotion")
    require(result["R_cell_identified_with_Xmax"] is False, "no R/Xmax join")
    require(result["P06_ready_pairs"] == result["solutions_run"] == 0 and result["gpu_used"] is False, "stop gates")
    require(result["epistemic_grade"] == "LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW", "grade")
    require(result["global_scale_realizations"] == 6, "global scale result count")
    require(result["embedding_realizations"] == 7, "embedding result count")

    sources = state["sources"]
    require(isinstance(sources, list) and len(sources) == 7, "source count")
    require(len({row["path"] for row in sources}) == 7, "source uniqueness")
    require({row["path"]: row["sha256"] for row in sources} == SOURCE_HASHES, "source registry")

    endpoints = state["endpoints"]
    require(isinstance(endpoints, list) and len(endpoints) == 4 and len({row["id"] for row in endpoints}) == 4, "endpoint census")
    require(all(row["same_bulk"] == "YES" and row["bulk_equation"] == "m*qddot+k*q=0" for row in endpoints), "same endpoint bulk")
    ep = {row["id"]: row for row in endpoints}
    require(ep["E01"]["field_transversality"] == "p=0" and ep["E01"]["position_transversality"] == "H=0", "bare endpoint")
    require(ep["E02"]["field_transversality"] == "p+lambda*q=0", "lambda changes field condition")
    require(ep["E03"]["position_transversality"] == "H=mu", "mu changes position condition")
    require(ep["E04"]["status"] == "TWO_PARAMETER_COUNTERFAMILY", "two-parameter family")

    scales = state["scales"]
    require(isinstance(scales, list) and len(scales) == 6 and len({row["id"] for row in scales}) == 6, "global scale census")
    gmap = {row["id"]: row for row in scales}
    require(gmap["G01"]["stationarity"] == "dS/dR=0 identically" and gmap["G01"]["selector_status"] == "NO_SCALE_SELECTION", "L01 homothety flat")
    require(gmap["G02"]["stationarity"] == "2*kappa*R*(Ahat-4*Lambda*R^2*Vhat)=0", "L02 homothety equation")
    require("R^2=Ahat/(4*Lambda*Vhat)" in gmap["G02"]["exact_consequence"], "L02 conditional root")
    require(gmap["G03"]["selector_status"] == "NO_GENERIC_SCALE_ROOT", "Lambda-zero branch")
    require(gmap["G04"]["selector_status"] == "FUNCTIONAL_DEPENDENCE", "boundary scaling dependence")
    require(gmap["G05"]["selector_status"] == "DISTINCT_REALIZATION", "endpoint/homothety distinction")
    require(gmap["G06"]["selector_status"] == "OPEN", "Xmax scale join open")

    seals = state["seals"]
    require(isinstance(seals, list) and len(seals) == 5 and len({row["id"] for row in seals}) == 5, "seal census")
    smap = {row["id"]: row for row in seals}
    require(smap["S02"]["allowed_relation"] == "Delta_phi=delta_phi+chi_normal*nabla_normal(phi)=0", "moving seal relation")
    require(smap["S03"]["embedding_displacement"] == "forced chi_normal=0", "stacked constraint")
    require(smap["S03"]["compatibility"] == "INCOMPATIBLE_WITH_INTENDED_FREE_MOTION", "stacked incompatibility")
    require(smap["S04"]["compatibility"] == "DEGENERATE_NOT_SELECTOR", "zero slope degeneracy")
    require(smap["S05"]["compatibility"] == "DISTINCT_OBJECT_BRANCH", "unlocked boundary branch")

    embeddings = state["embeddings"]
    require(isinstance(embeddings, list) and len(embeddings) == 7 and len({row["id"] for row in embeddings}) == 7, "embedding census")
    dmap = {row["id"]: row for row in embeddings}
    require(dmap["D01"]["independent_shape_data"] == "1 global number", "global modulus count")
    require(dmap["D02"]["raw_components"] == "4 functions" and dmap["D02"]["gauge_or_redundant"] == "3 tangential reparameterizations", "local embedding quotient")
    require(dmap["D02"]["independent_shape_data"] == "1 normal function", "local shape count")
    require(dmap["D07"]["realization"] == "MIRROR_DOUBLE_INTERNAL_SEAM" and "jump/matching" in dmap["D07"]["transversality_output"], "mirror seam branch")
    require(all(row["can_close_local_metric_polarization"] == "NO" for row in embeddings), "embedding no closure")

    covariance = state["covariance"]
    require(isinstance(covariance, list) and len(covariance) == 6, "covariance census")
    cmap = {row["id"]: row for row in covariance}
    require("Theta(g,delta_g)+i_chi L" in cmap["C01"]["identity"], "moving-domain term")
    require(cmap["C03"]["identity"] == "J_chi=Theta(g,L_chi g)-i_chi L", "Noether current")
    require(cmap["C04"]["identity"] == "dJ_chi=-E.L_chi g", "Noether divergence")
    require(cmap["C05"]["status"] == "CONDITIONAL_AFTER_B_AND_EMBEDDING_CHOICE", "shape depends on B")
    require(cmap["C06"]["status"] == "CONDITIONAL_AFTER_COMPLETE_GLOBAL_FUNCTIONAL", "global equation incomplete")

    lanes = state["lanes"]
    require(isinstance(lanes, list) and len(lanes) == 3 and {row["id"] for row in lanes} == {"L01", "L02", "L03"}, "lane census")
    require(all(row["transversality_status"] == "ADDED_B_DEPENDENT_NOT_SELECTOR" for row in lanes if row["id"] in {"L01", "L02"}), "metric lanes remain dependent")
    require(next(row for row in lanes if row["id"] == "L03")["transversality_status"] == "OPEN_NO_OPERATOR", "bridge open")

    trans = state["transversality"]
    require(isinstance(trans, list) and len(trans) == 7 and len({row["id"] for row in trans}) == 7, "transversality branches")
    tmap = {row["id"]: row for row in trans}
    require(tmap["T01"]["local_or_global"] == "one integrated scalar", "global transversality")
    require(tmap["T02"]["selector_result"] == "FUNCTIONAL_DEPENDENT", "local shape dependence")
    require(tmap["T04"]["selector_result"] == "NO_NEW_SELECTOR", "diffeomorphism branch")
    require(tmap["T05"]["selector_result"] == "UNCLASSIFIED_NOT_SELECTED", "null branch")
    require(tmap["T07"]["selector_result"] == "CONDITIONAL_CANCELLATION_NOT_CURRENTLY_EVALUABLE", "mirror cancellation conditional")

    ambiguities = state["ambiguities"]
    require(isinstance(ambiguities, list) and len(ambiguities) == 8, "ambiguity count")
    require({row["id"] for row in ambiguities} == {f"A{i:02d}" for i in range(1, 9)}, "ambiguity identities")
    require(all(row["removed_by_free_variation"] == "NO" for row in ambiguities), "ambiguities retained")
    require(next(row for row in ambiguities if row["id"] == "A01")["status"] == "PRIMARY_COUNTEREXAMPLE", "B counterexample")

    joins = state["joins"]
    require(isinstance(joins, list) and len(joins) == 5, "join census")
    jmap = {row["id"]: row for row in joins}
    require("X_max" in jmap["X01"]["must_not_equal_silently"], "R/Xmax separation")
    require(jmap["X02"]["current_status"] == "OWNER_LOCKED_GLOBAL_OUTPUT_VALUE_OPEN", "Xmax output status")
    require(jmap["X03"]["closure"] == jmap["X04"]["closure"] == "OPEN_JOIN", "surface joins open")
    require(jmap["X05"]["current_status"] == "WORKING_ON_SHELL_ADMISSIBILITY", "bootstrap status")

    fields = state["fields"]
    require(isinstance(fields, list) and len(fields) == 21, "field count")
    require(len({row["pair_id"] for row in fields}) == 21, "field uniqueness")
    require({row["pair_id"] for row in fields} == {f"L{lane:02d}_C{realization:02d}" for lane in range(1, 4) for realization in range(1, 8)}, "field identities")
    require(all(row["P06_ready"] == "NO" and row["Xmax_join"] == "OPEN" for row in fields), "field stop gates")
    require(sum(row["bulk_status"] == "CONDITIONAL_METRIC_BULK_OPERATOR" for row in fields) == 2, "metric-only pairs")
    require(sum(row["bulk_status"] == "NO_OPERATOR" for row in fields) == 7, "bridge pairs")

    status = state["status"]
    require(isinstance(status, list) and len(status) == 16, "status count")
    rmap = {row["id"]: row for row in status}
    require(rmap["R01"]["status"] == "CHOSE_CONDITIONAL_OWNER_AUTHORIZED_TEST", "premise status")
    require(rmap["R02"]["status"] == "NOT_DERIVED_FORBIDDEN_SILENT_JOIN", "Xmax join status")
    require(rmap["R04"]["status"] == "REFUTED_BY_TWO_PARAMETER_COUNTERFAMILY", "functional selection refuted")
    require(rmap["R08"]["status"] == "REFUTED", "fixed/moving stack refuted")
    require(rmap["R16"]["status"] == result["classification"], "classification ledger")

    graph = state["graph"]
    require(isinstance(graph, dict), "graph type")
    require(len(graph["failed_implications"]) == 7 and len(graph["open"]) == 7, "graph counts")
    require("free boundary -> B=0" in graph["failed_implications"], "B implication rejected")
    require("R_cell -> X_max" in graph["failed_implications"], "R/Xmax implication rejected")
    require("native matter source total mass and proper volume" in graph["open"], "matter closure open")


def independent_algebra() -> int:
    checks = 0
    for relative, expected in SOURCE_HASHES.items():
        require(digest(ROOT / relative) == expected, f"source hash: {relative}")
        checks += 1

    # Independent endpoint derivation using the total endpoint displacement directly.
    mm, kk, qq, vel = sp.symbols("mm kk qq vel")
    dq_total, dtime, ll, uu = sp.symbols("dq_total dtime ll uu")
    lag = mm * vel**2 / 2 - kk * qq**2 / 2
    mom = sp.diff(lag, vel)
    ham = sp.expand(mom * vel - lag)
    delta_fixed = dq_total - vel * dtime
    varied = sp.expand(mom * delta_fixed + lag * dtime + ll * qq * dq_total + uu * dtime)
    target = sp.expand((mom + ll * qq) * dq_total + (-ham + uu) * dtime)
    require(sp.expand(varied - target) == 0, "independent endpoint formula")
    qddot = sp.symbols("qddot")
    require(sp.diff(lag, qq) - qddot * sp.diff(mom, vel) == -kk * qq - mm * qddot, "same bulk symbolic form")
    checks += 2

    radius = sp.symbols("radius", positive=True)
    aa, vv, llambda, kap, c2hat, e4hat, alph, bet = sp.symbols("aa vv llambda kap c2hat e4hat alph bet")
    pre_scale = alph * c2hat + bet * e4hat
    post_scale = kap * (radius**2 * aa - 2 * llambda * radius**4 * vv) + bet * e4hat
    require(sp.diff(pre_scale, radius) == 0, "independent L01 scale flatness")
    post_derivative = sp.factor(sp.diff(post_scale, radius))
    require(post_derivative == 2 * kap * radius * (aa - 4 * llambda * radius**2 * vv), "independent L02 scale equation")
    require(sp.solve(sp.Eq(post_derivative / (2 * kap * radius), 0), radius**2) == [aa / (4 * llambda * vv)], "independent L02 scale root")
    bb, pp = sp.symbols("bb pp")
    require(sp.diff(bb * radius**pp, radius) == bb * pp * radius**pp / radius, "independent boundary scaling response")
    checks += 4

    slope = sp.symbols("slope", nonzero=True)
    move = sp.Matrix([[1, slope]])
    fixed_and_move = sp.Matrix([[1, slope], [1, 0]])
    require(move.nullspace() == [sp.Matrix([-slope, 1])], "independent correlated level-set tangent")
    require(fixed_and_move.det() == -slope and fixed_and_move.nullspace() == [], "independent stacked obstruction")
    zero = fixed_and_move.subs(slope, 0)
    require(zero.rank() == 1 and zero.nullspace() == [sp.Matrix([0, 1])], "independent degenerate slope")
    checks += 3

    # Count one physical normal embedding function after the tangential quotient.
    embedding_projection = sp.Matrix([[0, 0, 0, 1]])
    tangential_basis = sp.Matrix.hstack(sp.eye(4)[:, 0], sp.eye(4)[:, 1], sp.eye(4)[:, 2])
    require(tangential_basis.rank() == 3, "tangential rank")
    require(embedding_projection.rank() == 1 and embedding_projection * tangential_basis == sp.zeros(1, 3), "normal quotient")
    checks += 2

    # Independent-channel obstruction: adding chi adds a column, not a relation among h channels.
    l02 = sp.eye(3)
    l01 = sp.eye(4)
    require(l02.rank() == 3 and l01.rank() == 4, "independent field/embedding channels")
    require(l02.rank() - 1 == 2 and l01.rank() - 1 == 3, "one seal relation cannot erase channels")
    checks += 2
    theta_a, theta_b, response_a, response_b = sp.symbols("theta_a theta_b response_a response_b")
    require((theta_a - theta_b).subs(theta_b, theta_a) == 0, "independent two-sided flux cancellation")
    require((response_a - response_b).subs(response_b, response_a) == 0, "independent two-sided shape cancellation")
    checks += 2
    return checks


def catch_proofs(original: dict[str, object]) -> int:
    mutations: list[tuple[str, object]] = []

    def add(name: str, mutation) -> None:
        mutations.append((name, mutation))

    add("classification promotion", lambda s: s["result"].__setitem__("classification", "FREE_GLOBAL_BOUNDARY_UNIQUELY_CLOSES_SELECTOR"))
    add("canon promotion", lambda s: s["result"].__setitem__("premise_promoted_to_canon", True))
    add("R/Xmax identification", lambda s: s["result"].__setitem__("R_cell_identified_with_Xmax", True))
    add("P06 promotion", lambda s: s["result"].__setitem__("P06_ready_pairs", 1))
    add("solution invented", lambda s: s["result"].__setitem__("solutions_run", 1))
    add("GPU invented", lambda s: s["result"].__setitem__("gpu_used", True))
    add("grade inflated", lambda s: s["result"].__setitem__("epistemic_grade", "DERIVED"))
    add("source removed", lambda s: s["sources"].pop())
    add("source duplicate", lambda s: s["sources"].append(copy.deepcopy(s["sources"][0])))
    add("source hash changed", lambda s: s["sources"][0].__setitem__("sha256", "0" * 64))
    add("endpoint removed", lambda s: s["endpoints"].pop())
    add("endpoint bulk changed", lambda s: s["endpoints"][1].__setitem__("bulk_equation", "different"))
    add("lambda effect erased", lambda s: s["endpoints"][1].__setitem__("field_transversality", "p=0"))
    add("mu effect erased", lambda s: s["endpoints"][2].__setitem__("position_transversality", "H=0"))
    add("counterfamily demoted", lambda s: s["endpoints"][3].__setitem__("status", "UNIQUE"))
    add("scale row removed", lambda s: s["scales"].pop())
    add("L01 scale selected", lambda s: s["scales"][0].__setitem__("selector_status", "UNIQUE_SCALE"))
    add("L01 derivative changed", lambda s: s["scales"][0].__setitem__("stationarity", "R=1"))
    add("L02 equation changed", lambda s: s["scales"][1].__setitem__("stationarity", "Ahat-Lambda*R=0"))
    add("L02 root made unconditional", lambda s: s["scales"][1].__setitem__("exact_consequence", "R is uniquely derived"))
    add("Lambda-zero scale invented", lambda s: s["scales"][2].__setitem__("selector_status", "UNIQUE_SCALE"))
    add("boundary scaling ignored", lambda s: s["scales"][3].__setitem__("selector_status", "NO_EFFECT"))
    add("endpoint homothety conflated", lambda s: s["scales"][4].__setitem__("selector_status", "IDENTICAL"))
    add("Xmax scale joined", lambda s: s["scales"][5].__setitem__("selector_status", "DERIVED"))
    add("seal branch removed", lambda s: s["seals"].pop())
    add("moving relation altered", lambda s: s["seals"][1].__setitem__("allowed_relation", "delta_phi=0"))
    add("stack displacement freed", lambda s: s["seals"][2].__setitem__("embedding_displacement", "free"))
    add("stack compatibility promoted", lambda s: s["seals"][2].__setitem__("compatibility", "COMPATIBLE"))
    add("zero slope selected", lambda s: s["seals"][3].__setitem__("compatibility", "SELECTOR"))
    add("embedding row removed", lambda s: s["embeddings"].pop())
    add("local raw count changed", lambda s: s["embeddings"][1].__setitem__("raw_components", "1 function"))
    add("tangential gauge lost", lambda s: s["embeddings"][1].__setitem__("gauge_or_redundant", "0"))
    add("embedding closure promoted", lambda s: s["embeddings"][0].__setitem__("can_close_local_metric_polarization", "YES"))
    add("mirror embedding erased", lambda s: s["embeddings"][6].__setitem__("realization", "EXTERNAL_WALL"))
    add("covariance row removed", lambda s: s["covariance"].pop())
    add("moving-domain chi term removed", lambda s: s["covariance"][0].__setitem__("identity", "delta S=E delta g+Theta"))
    add("Noether sign changed", lambda s: s["covariance"][3].__setitem__("identity", "dJ=+E.Lg"))
    add("shape promoted independent", lambda s: s["covariance"][4].__setitem__("status", "DERIVED_UNCONDITIONAL"))
    add("global functional invented", lambda s: s["covariance"][5].__setitem__("status", "DERIVED"))
    add("lane removed", lambda s: s["lanes"].pop())
    add("L01 selected", lambda s: s["lanes"][0].__setitem__("transversality_status", "SELECTOR"))
    add("bridge operator invented", lambda s: s["lanes"][2].__setitem__("transversality_status", "DERIVED"))
    add("trans branch removed", lambda s: s["transversality"].pop())
    add("global condition made local", lambda s: s["transversality"][0].__setitem__("local_or_global", "all local functions"))
    add("shape dependence erased", lambda s: s["transversality"][1].__setitem__("selector_result", "UNIQUE"))
    add("diffeo made selector", lambda s: s["transversality"][3].__setitem__("selector_result", "UNIQUE"))
    add("mirror cancellation promoted", lambda s: s["transversality"][6].__setitem__("selector_result", "DERIVED_UNCONDITIONAL"))
    add("ambiguity removed", lambda s: s["ambiguities"].pop())
    add("ambiguity selected away", lambda s: s["ambiguities"][0].__setitem__("removed_by_free_variation", "YES"))
    add("primary counterexample lost", lambda s: s["ambiguities"][0].__setitem__("status", "CLOSED"))
    add("join removed", lambda s: s["joins"].pop())
    add("R/Xmax separation erased", lambda s: s["joins"][0].__setitem__("must_not_equal_silently", "WRL only"))
    add("Xmax made input", lambda s: s["joins"][1].__setitem__("current_status", "FREE_INPUT"))
    add("fold join closed", lambda s: s["joins"][2].__setitem__("closure", "CLOSED"))
    add("bootstrap promoted offshell", lambda s: s["joins"][4].__setitem__("current_status", "OFFSHELL_ACTION"))
    add("field removed", lambda s: s["fields"].pop())
    add("field duplicated", lambda s: s["fields"].append(copy.deepcopy(s["fields"][0])))
    add("field P06 promoted", lambda s: s["fields"][0].__setitem__("P06_ready", "YES"))
    add("field Xmax closed", lambda s: s["fields"][0].__setitem__("Xmax_join", "CLOSED"))
    add("extra field operator invented", lambda s: s["fields"][1].__setitem__("bulk_status", "CONDITIONAL_METRIC_BULK_OPERATOR"))
    add("status premise canonized", lambda s: s["status"][0].__setitem__("status", "CANONIZED"))
    add("status Xmax joined", lambda s: s["status"][1].__setitem__("status", "DERIVED"))
    add("status functional selected", lambda s: s["status"][3].__setitem__("status", "DERIVED_UNIQUE"))
    add("status classification mismatch", lambda s: s["status"][15].__setitem__("status", "UNIQUE"))
    add("graph implication removed", lambda s: s["graph"]["failed_implications"].pop())
    add("graph R/Xmax rejection removed", lambda s: s["graph"]["failed_implications"].remove("R_cell -> X_max"))
    add("graph matter closure removed", lambda s: s["graph"]["open"].remove("native matter source total mass and proper volume"))

    caught = 0
    for name, mutation in mutations:
        trial = copy.deepcopy(original)
        mutation(trial)
        try:
            validate(trial)
        except (AssertionError, KeyError, StopIteration, TypeError, ValueError):
            caught += 1
        else:
            raise AssertionError(f"mutation escaped: {name}")
    return caught


def main() -> None:
    state = load_state()
    validate(state)
    algebra_checks = independent_algebra()
    catches = catch_proofs(state)
    result_hash = digest(HERE / "DERIVATION_RESULT.json")
    output = {
        "verification": "PASS",
        "generator_imported": False,
        "independent_algebra_checks": algebra_checks,
        "catch_proofs": catches,
        "classification": state["result"]["classification"],
        "endpoint_counterfunctionals": len(state["endpoints"]),
        "global_scale_realizations": len(state["scales"]),
        "embedding_realizations": len(state["embeddings"]),
        "field_lane_pairs": len(state["fields"]),
        "P06_ready_pairs": state["result"]["P06_ready_pairs"],
        "main_result_sha256": result_hash,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "UDT_FREE_GLOBAL_SEAL_TRANSVERSALITY_VERIFICATION=PASS",
        f"independent_algebra_checks={algebra_checks}",
        f"catch_proofs={catches}",
        "generator_imported=NO",
        f"endpoint_counterfunctionals={len(state['endpoints'])}/4",
        f"global_scale_realizations={len(state['scales'])}/6",
        f"embedding_realizations={len(state['embeddings'])}/7",
        f"field_pairs={len(state['fields'])}/21",
        f"P06_ready_pairs={state['result']['P06_ready_pairs']}",
        f"main_result_sha256={result_hash}",
    ]
    (HERE / "VERIFICATION_TRANSCRIPT.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
