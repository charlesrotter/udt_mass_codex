#!/usr/bin/env python3
"""Independent, non-importing verifier for the UDT time-live boundary-flux audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
ETA = sp.diag(-1, 1, 1, 1)
COMPONENTS = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3))

SOURCE_HASHES = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "d38232792ac78188687db433a3f60a08c775c46e9ecf5fc42ad7953dc89fadb0",
    "udt_full_equation_variation_p05_2026-07-21/SHA256SUMS.txt": "5c26d4eb97c4dc370e286469c63d662f182a71a94a6e6899131fd6706c4e7f2e",
    "udt_pre_p06_boundary_selector_audit_2026-07-21/SHA256SUMS.txt": "45c239639d999c26f2e574592fafc392fbb7c1e6f20ea92e1d260b4784e00e51",
    "reciprocal_metric_null_line_selector_2026-07-19/SHA256SUMS.txt": "01ed5557bb94a1df99209d37b1eb5e4eefae4486978be34ab09dafb73aeac17b",
    "complete_coframe_seal_involution_2026-07-20/SHA256SUMS.txt": "87d43cb281d236111a8baec4fe7da5686a8043931e6ba0a2715228f7d61f483e",
    "udt_global_kinematic_assembly_p03g_2026-07-21/SHA256SUMS.txt": "62f9b3f33409b62fb841734e8a91e61d9b859247bf808c4a6cf3740b6a54b6c9",
    "udt_founded_constraint_atlas_p03_2026-07-21/SHA256SUMS.txt": "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tensor_matrix(operator: str, covector: tuple[int, int, int, int]) -> sp.Matrix:
    """Build a principal map independently by applying it to ten explicit tensor bases."""
    xi = sp.Matrix(covector)
    xu = ETA * xi
    x2 = (xi.T * xu)[0]
    columns: list[sp.Matrix] = []
    for pair in COMPONENTS:
        h = sp.zeros(4)
        h[pair[0], pair[1]] = 1
        h[pair[1], pair[0]] = 1
        if pair[0] == pair[1]:
            h[pair[0], pair[1]] = 1
        tr = sp.trace(ETA * h)
        ric = sp.zeros(4)
        for aa in range(4):
            for bb in range(4):
                contraction_b = sum(xu[cc] * h[cc, bb] for cc in range(4))
                contraction_a = sum(xu[cc] * h[cc, aa] for cc in range(4))
                ric[aa, bb] = sp.Rational(1, 2) * (
                    xi[aa] * contraction_b
                    + xi[bb] * contraction_a
                    - x2 * h[aa, bb]
                    - xi[aa] * xi[bb] * tr
                )
        scal = sum(xu[aa] * xu[bb] * h[aa, bb] for aa in range(4) for bb in range(4)) - x2 * tr
        out = sp.zeros(4)
        for aa in range(4):
            for bb in range(4):
                if operator == "L02":
                    out[aa, bb] = ric[aa, bb] - ETA[aa, bb] * scal / 2
                elif operator == "L01":
                    out[aa, bb] = x2 * ric[aa, bb] / 2 - xi[aa] * xi[bb] * scal / 6 - ETA[aa, bb] * x2 * scal / 12
                else:
                    raise ValueError(operator)
        columns.append(sp.Matrix([sp.expand(out[aa, bb]) for aa, bb in COMPONENTS]))
    return sp.Matrix.hstack(*columns)


def canonical_j(n: int) -> sp.Matrix:
    return sp.zeros(n).row_join(sp.eye(n)).col_join((-sp.eye(n)).row_join(sp.zeros(n)))


def load_state() -> dict[str, object]:
    return {
        "result": json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "sources": read_tsv("SOURCE_LINEAGE.tsv"),
        "seals": read_tsv("SEAL_CAUSAL_BRANCHES.tsv"),
        "ranks": read_tsv("PRINCIPAL_SYMBOL_RANKS.tsv"),
        "characteristics": read_tsv("CHARACTERISTIC_AND_CONSTRAINTS.tsv"),
        "pairs": read_tsv("SYMPLECTIC_PAIR_CENSUS.tsv"),
        "polarizations": read_tsv("POLARIZATION_WITNESSES.tsv"),
        "fluxes": read_tsv("FLUX_WITNESSES.tsv"),
        "ambiguities": read_tsv("FUNCTIONAL_AMBIGUITY.tsv"),
        "boundaries": read_tsv("BOUNDARY_BRANCH_STATUS.tsv"),
        "fields": read_tsv("FIELD_LANE_CLOSURE.tsv"),
        "status": read_tsv("STATUS_LEDGER.tsv"),
        "graph": json.loads((HERE / "SELECTOR_DEPENDENCY_GRAPH.json").read_text(encoding="utf-8")),
    }


def validate_state(state: dict[str, object]) -> None:
    result = state["result"]
    require(isinstance(result, dict), "result object")
    require(result["classification"] == "TIME_LIVE_REDUCES_BUT_DOES_NOT_SELECT_BOUNDARY_DATA", "classification")
    require(result["maximum_conclusion"] == "TIME_LIVE_CHARACTERISTIC_AND_BOUNDARY_FLUX_SELECTOR_STATUS_CLASSIFIED", "maximum conclusion")
    require(result["P06_ready_pairs"] == 0 and result["solutions_run"] == 0 and result["gpu_used"] is False, "stop gates")
    require(result["epistemic_grade"] == "LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW", "evidence grade")
    require(result["canonical_pair_census"] == {"L01_non_null": "constrained presymplectic; P_K trace-free and CSN-null", "L02_non_null_comparison": 6}, "canonical pair census")

    sources = state["sources"]
    require(isinstance(sources, list) and len(sources) == 7, "source count")
    require(len({row["path"] for row in sources}) == 7, "unique sources")
    require({row["path"]: row["sha256"] for row in sources} == SOURCE_HASHES, "source registry")

    seals = state["seals"]
    require(isinstance(seals, list) and len(seals) == 7 and len({row["id"] for row in seals}) == 7, "seal census")
    seal_map = {row["id"]: row for row in seals}
    require(seal_map["S01"]["boundary_class"] == "spacelike", "spacelike seal witness")
    require(seal_map["S02"]["boundary_class"] == "null", "null seal witness")
    require(seal_map["S03"]["boundary_class"] == "timelike", "timelike seal witness")
    require(seal_map["S07"]["boundary_class"] == "OPEN", "no-extension branch")
    require("v is not selected" in seal_map["S05"]["consequence"], "velocity nonselection")

    ranks = state["ranks"]
    require(isinstance(ranks, list) and len(ranks) == 6, "rank census")
    rank_map = {(row["lane"], row["covector_class"]): (int(row["rank"]), int(row["nullity"])) for row in ranks}
    require(rank_map == {
        ("L01", "TIMELIKE"): (5, 5),
        ("L02", "TIMELIKE"): (6, 4),
        ("L01", "SPACELIKE"): (5, 5),
        ("L02", "SPACELIKE"): (6, 4),
        ("L01", "NULL"): (1, 9),
        ("L02", "NULL"): (4, 6),
    }, "principal ranks")
    require(all(row["matrix_dimension"] == "10x10" for row in ranks), "ten metric components")

    characteristics = state["characteristics"]
    require(isinstance(characteristics, list) and len(characteristics) == 8, "characteristic census")
    c_map = {row["id"]: row for row in characteristics}
    require(c_map["C01"]["exact_result"] == "alpha*(g^ab xi_a xi_b)^2", "L01 double cone")
    require(c_map["C02"]["exact_result"] == "kappa*(g^ab xi_a xi_b)", "L02 simple cone")
    require(c_map["C05"]["status"] == "DERIVED_KINEMATICS_CONDITIONAL_EXTENSION", "conditional seal extension")
    require(c_map["C08"]["status"] == "OPEN_NO_OPERATOR", "bridge no operator")

    pairs = state["pairs"]
    require(isinstance(pairs, list) and len(pairs) == 4, "symplectic pair census")
    pair_map = {row["lane"] + ":" + row["regular_boundary_type"]: row for row in pairs}
    require(pair_map["L01:non-null"]["phase_dimension"] == "OPEN_CONSTRAINED_PRESYMPLECTIC", "L01 constrained phase dimension")
    require(pair_map["L01:non-null"]["symplectic_rank"] == "OPEN_BEFORE_CSN_AND_CONSTRAINT_REDUCTION", "L01 rank not overstated")
    require("trace-free" in pair_map["L01:non-null"]["momentum_slots"], "L01 trace-free momentum")
    require(pair_map["L02:non-null"]["phase_dimension"] == "12", "L02 phase dimension")
    require(pair_map["L01+L02:null"]["symplectic_rank"] == "OPEN", "null completion open")

    pols = state["polarizations"]
    require(isinstance(pols, list) and len(pols) == 5 and len({row["id"] for row in pols}) == 5, "polarization census")
    require(sum(row["lane"] == "L01" for row in pols) == 2, "two explicit L01 polarizations")
    require(sum(row["lane"] == "L02" for row in pols) == 2, "two explicit L02 polarizations")
    require(all(row["flux"].startswith("zero") for row in pols[:4]), "explicit flux-free polarizations")
    require(all(row["scalar_seal"] == "preserved" for row in pols[:4]), "seal-preserving polarizations")
    require(all("normal jet free" in row["normal_phi_jet"] for row in pols if row["lane"] == "L01"), "C2 free normal jet")

    fluxes = state["fluxes"]
    require(isinstance(fluxes, list) and len(fluxes) == 4, "flux witness census")
    require(all("phi" in row["seal"] for row in fluxes), "seal disclosure")
    require(all(row["boundary_flux"] not in {"0", "zero"} for row in fluxes), "nonzero flux witnesses")
    require(all("TT angular-shape" in row["sector"] for row in fluxes if row["id"] in {"F03", "F04"}), "TT wave disclosure")

    ambiguities = state["ambiguities"]
    require(isinstance(ambiguities, list) and len(ambiguities) == 7, "functional ambiguity count")
    require(all(row["removed_by_characteristics"] == "NO" for row in ambiguities), "ambiguities survive characteristics")
    require({row["id"] for row in ambiguities} == {f"A{i:02d}" for i in range(1, 8)}, "ambiguity identities")

    boundaries = state["boundaries"]
    require(isinstance(boundaries, list) and len(boundaries) == 8 and len({row["id"] for row in boundaries}) == 8, "boundary branch census")
    require(all(row["selected"] == "NO" for row in boundaries), "no boundary selected")
    require({row["id"] for row in boundaries} == {f"T{i:02d}" for i in range(1, 9)}, "boundary identities")

    fields = state["fields"]
    require(isinstance(fields, list) and len(fields) == 21, "field pair census")
    require(len({row["pair_id"] for row in fields}) == 21, "unique field pairs")
    require({row["pair_id"] for row in fields} == {f"L{lane:02d}_C{rid:02d}" for lane in range(1, 4) for rid in range(1, 8)}, "complete field pair identities")
    require(all(row["P06_ready"] == "NO" for row in fields), "P06 closed")
    require(sum(row["operator_status"] == "CONDITIONAL_METRIC_BULK_OPERATOR" for row in fields) == 2, "metric operator pairs")
    require(sum(row["operator_status"] == "NO_BRIDGE_OPERATOR" for row in fields) == 7, "bridge pairs")

    status = state["status"]
    require(isinstance(status, list) and len(status) == 14, "status census")
    s_map = {row["id"]: row for row in status}
    require(s_map["R04"]["status"] == "NOT_DERIVED", "null seal not forced")
    require(s_map["R08"]["status"] == "EXCLUDED_BY_EXACT_COUNTERWITNESSES", "seal flux claim excluded")
    require(s_map["R09"]["status"] == "NOT_DERIVED", "polarization not selected")
    require(s_map["R13"]["status"] == result["classification"], "classification ledger")

    graph = state["graph"]
    require(isinstance(graph, dict), "dependency graph")
    require(len(graph["failed_implications"]) == 6, "failed implication census")
    require("metric null cone -> seal is null" in graph["failed_implications"], "cone/seal distinction")
    require("complete coframe action and lift" in graph["open_inputs"], "coframe blocker")


def independent_algebra() -> int:
    checks = 0
    for rel, expected in SOURCE_HASHES.items():
        require(digest(ROOT / rel) == expected, f"source hash {rel}")
        checks += 1

    # Independently invert the angular block and evaluate the complete seal norm.
    aa, bb, dd = sp.symbols("aa bb dd")
    p0, px, py, pz, cc = sp.symbols("p0 px py pz cc", nonzero=True)
    q = sp.Matrix([[aa, bb], [bb, dd]])
    q_inverse = q.inv()
    angular = (sp.Matrix([py, pz]).T * q_inverse * sp.Matrix([py, pz]))[0]
    expected_angular = (dd * py**2 - 2 * bb * py * pz + aa * pz**2) / (aa * dd - bb**2)
    require(sp.factor(angular - expected_angular) == 0, "independent angular inverse")
    seal_norm = -p0**2 / cc**2 + px**2 + angular
    vv = sp.symbols("vv")
    expected_moving = -px**2 * (-cc + vv) * (cc + vv) / cc**2
    require(sp.simplify(seal_norm.subs({p0: -vv * px, py: 0, pz: 0}) - expected_moving) == 0, "independent moving seal")
    checks += 2

    expected_ranks = {
        ("L01", (1, 0, 0, 0)): 5,
        ("L01", (0, 1, 0, 0)): 5,
        ("L01", (1, 1, 0, 0)): 1,
        ("L02", (1, 0, 0, 0)): 6,
        ("L02", (0, 1, 0, 0)): 6,
        ("L02", (1, 1, 0, 0)): 4,
    }
    for key, expected_rank in expected_ranks.items():
        matrix = tensor_matrix(*key)
        require(matrix.shape == (10, 10) and matrix.rank() == expected_rank, f"independent rank {key}")
        checks += 1

    # Independent EH canonical geometry: two Lagrangian subspaces respecting q0=0.
    pair_count = 6
    jj = canonical_j(pair_count)
    require(jj.rank() == 2 * pair_count and jj.T == -jj, "EH canonical form")
    basis_a = sp.zeros(2 * pair_count, pair_count)
    basis_b = sp.zeros(2 * pair_count, pair_count)
    for ii in range(pair_count):
        basis_a[pair_count + ii, ii] = 1
    basis_b[pair_count, 0] = 1
    for ii in range(1, pair_count):
        basis_b[ii, ii] = 1
    require(basis_a.T * jj * basis_a == sp.zeros(pair_count), "EH polarization A")
    require(basis_b.T * jj * basis_b == sp.zeros(pair_count), "EH polarization B")
    require(basis_a != basis_b and basis_a.rank() == basis_b.rank() == pair_count, "inequivalent EH polarizations")
    checks += 3

    # Independently keep the C2 trace-free/CSN constraint visible.  Two exact natural boundary
    # classes cancel Pi_h:dh + P_K:dK without assigning a reduced phase-space rank.
    dh = sp.Matrix(sp.symbols("vh0:6"))
    dk = sp.Matrix(sp.symbols("vk0:6"))
    ph = sp.Matrix(sp.symbols("vph0:6"))
    pk = sp.Matrix(sp.symbols("vpk0:6"))
    raw_flux = (ph.T * dh)[0] + (pk.T * dk)[0]
    rules_a = {**{dh[i]: 0 for i in range(6)}, **{pk[i]: 0 for i in range(6)}}
    rules_b = {dh[0]: 0, **{ph[i]: 0 for i in range(1, 6)}, **{pk[i]: 0 for i in range(6)}}
    require(sp.simplify(raw_flux.subs(rules_a)) == 0, "independent C2 natural class A")
    require(sp.simplify(raw_flux.subs(rules_b)) == 0, "independent C2 natural class B")
    require(not any(dk[i] in rules_a or dk[i] in rules_b for i in range(6)), "independent C2 free K")
    require(dh[1] not in rules_b, "independent C2 transverse h free")
    checks += 4

    # Explicit TT angular-shape waves and fourth-order biwaves.
    tt = sp.zeros(10, 1)
    tt[7], tt[9] = 1, -1
    require(tensor_matrix("L02", (1, -1, 0, 0)) * tt == sp.zeros(10, 1), "independent EH TT null mode")
    require(tensor_matrix("L01", (1, -1, 0, 0)) * tt == sp.zeros(10, 1), "independent C2 TT null mode")
    time, normal = sp.symbols("time normal")
    box = lambda f: sp.diff(f, normal, 2) - sp.diff(f, time, 2)
    e1, e2 = time - normal, (time - normal) ** 2
    require(box(e1) == box(e2) == 0, "independent EH waves")
    eh_flux = e1 * sp.diff(e2, normal) - e2 * sp.diff(e1, normal)
    require(eh_flux.subs({time: 1, normal: 0}) == -1, "independent EH flux")
    b1, b2 = normal**2 + time * normal, time - normal
    require(box(box(b1)) == box(box(b2)) == 0, "independent C2 biwaves")
    s1, s2 = box(b1), box(b2)
    c2_flux = s1 * sp.diff(b2, normal) - sp.diff(s1, normal) * b2 - s2 * sp.diff(b1, normal) + sp.diff(s2, normal) * b1
    require(c2_flux.subs({time: 1, normal: 0}) == -2, "independent C2 flux")
    checks += 6
    return checks


def catch_proofs(original: dict[str, object]) -> int:
    mutations: list[tuple[str, callable]] = []

    def add(name: str, mutate) -> None:
        mutations.append((name, mutate))

    add("classification promotion", lambda s: s["result"].__setitem__("classification", "TIME_LIVE_UNIQUE_BOUNDARY_SELECTOR_DERIVED"))
    add("P06 promotion", lambda s: s["result"].__setitem__("P06_ready_pairs", 1))
    add("solution invented", lambda s: s["result"].__setitem__("solutions_run", 1))
    add("GPU invented", lambda s: s["result"].__setitem__("gpu_used", True))
    add("grade inflated", lambda s: s["result"].__setitem__("epistemic_grade", "DERIVED"))
    add("source removed", lambda s: s["sources"].pop())
    add("source duplicated", lambda s: s["sources"].append(copy.deepcopy(s["sources"][0])))
    add("source hash altered", lambda s: s["sources"][0].__setitem__("sha256", "0" * 64))
    add("seal branch removed", lambda s: s["seals"].pop())
    add("null seal forced", lambda s: s["seals"][0].__setitem__("boundary_class", "null"))
    add("no-extension erased", lambda s: s["seals"][6].__setitem__("boundary_class", "null"))
    add("velocity selected", lambda s: s["seals"][4].__setitem__("consequence", "v=c selected"))
    add("rank row removed", lambda s: s["ranks"].pop())
    add("L01 null rank altered", lambda s: next(r for r in s["ranks"] if r["lane"] == "L01" and r["covector_class"] == "NULL").__setitem__("rank", "2"))
    add("component dimension reduced", lambda s: s["ranks"][0].__setitem__("matrix_dimension", "6x6"))
    add("simple double swap", lambda s: s["characteristics"][0].__setitem__("exact_result", "alpha*(g^ab xi_a xi_b)"))
    add("bridge operator invented", lambda s: s["characteristics"][7].__setitem__("status", "DERIVED"))
    add("conditional seal promoted", lambda s: s["characteristics"][4].__setitem__("status", "DERIVED_NATIVE"))
    add("symplectic census removed", lambda s: s["pairs"].pop())
    add("C2 phase rank invented", lambda s: next(r for r in s["pairs"] if r["lane"] == "L01").__setitem__("phase_dimension", "24"))
    add("C2 trace-free disclosure removed", lambda s: next(r for r in s["pairs"] if r["lane"] == "L01").__setitem__("momentum_slots", "6 unconstrained Pi_K"))
    add("null symplectic rank invented", lambda s: next(r for r in s["pairs"] if r["regular_boundary_type"] == "null").__setitem__("symplectic_rank", "12"))
    add("polarization removed", lambda s: s["polarizations"].pop(1))
    add("polarization duplicated", lambda s: s["polarizations"].append(copy.deepcopy(s["polarizations"][0])))
    add("C2 normal jet fixed", lambda s: next(r for r in s["polarizations"] if r["lane"] == "L01").__setitem__("normal_phi_jet", "fixed"))
    add("polarization flux nonzero", lambda s: s["polarizations"][0].__setitem__("flux", "1"))
    add("seal disclosure lost", lambda s: s["polarizations"][0].__setitem__("scalar_seal", "unspecified"))
    add("flux witness removed", lambda s: s["fluxes"].pop())
    add("flux zeroed", lambda s: s["fluxes"][0].__setitem__("boundary_flux", "0"))
    add("TT disclosure removed", lambda s: s["fluxes"][2].__setitem__("sector", "scalar wave"))
    add("ambiguity removed", lambda s: s["ambiguities"].pop())
    add("Euler ambiguity selected away", lambda s: s["ambiguities"][1].__setitem__("removed_by_characteristics", "YES"))
    add("boundary branch removed", lambda s: s["boundaries"].pop())
    add("boundary selected", lambda s: s["boundaries"][3].__setitem__("selected", "YES"))
    add("boundary duplicate", lambda s: s["boundaries"].append(copy.deepcopy(s["boundaries"][0])))
    add("field pair removed", lambda s: s["fields"].pop())
    add("field pair duplicated", lambda s: s["fields"].append(copy.deepcopy(s["fields"][0])))
    add("field promoted P06", lambda s: s["fields"][0].__setitem__("P06_ready", "YES"))
    add("extra operator invented", lambda s: s["fields"][1].__setitem__("operator_status", "CONDITIONAL_METRIC_BULK_OPERATOR"))
    add("bridge field operator invented", lambda s: s["fields"][14].__setitem__("operator_status", "CONDITIONAL_METRIC_BULK_OPERATOR"))
    add("null seal status promoted", lambda s: next(r for r in s["status"] if r["id"] == "R04").__setitem__("status", "DERIVED"))
    add("polarization status promoted", lambda s: next(r for r in s["status"] if r["id"] == "R09").__setitem__("status", "DERIVED"))
    add("classification ledger mismatch", lambda s: next(r for r in s["status"] if r["id"] == "R13").__setitem__("status", "UNIQUE"))
    add("failed implication removed", lambda s: s["graph"]["failed_implications"].pop())
    add("coframe blocker removed", lambda s: s["graph"]["open_inputs"].remove("complete coframe action and lift"))

    caught = 0
    for name, mutate in mutations:
        trial = copy.deepcopy(original)
        mutate(trial)
        try:
            validate_state(trial)
        except (AssertionError, KeyError, StopIteration, TypeError, ValueError):
            caught += 1
        else:
            raise AssertionError(f"mutation escaped: {name}")
    return caught


def main() -> None:
    state = load_state()
    validate_state(state)
    algebra_checks = independent_algebra()
    catches = catch_proofs(state)
    result_hash = digest(HERE / "DERIVATION_RESULT.json")
    output = {
        "verification": "PASS",
        "generator_imported": False,
        "independent_algebra_checks": algebra_checks,
        "catch_proofs": catches,
        "classification": state["result"]["classification"],
        "principal_ranks": state["result"]["principal_ranks"],
        "boundary_branches": len(state["boundaries"]),
        "field_lane_pairs": len(state["fields"]),
        "P06_ready_pairs": state["result"]["P06_ready_pairs"],
        "main_result_sha256": result_hash,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "UDT_TIME_LIVE_CHARACTERISTIC_FLUX_VERIFICATION=PASS",
        f"independent_algebra_checks={algebra_checks}",
        f"catch_proofs={catches}",
        "generator_imported=NO",
        f"boundary_branches={len(state['boundaries'])}/8",
        f"field_pairs={len(state['fields'])}/21",
        f"P06_ready_pairs={state['result']['P06_ready_pairs']}",
        f"main_result_sha256={result_hash}",
    ]
    (HERE / "VERIFICATION_TRANSCRIPT.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
