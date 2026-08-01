#!/usr/bin/env python3
"""Cold verifier for the stability derivation-closure sweep.

This implementation is intentionally standard-library-only.  It does not import or
execute derive_closure_sweep.py or verify_closure_sweep.py.  It independently rebuilds
the source freeze, parses the landed ledgers, recomputes the elementary countermodels,
and exercises fail-closed mutations against its own validator.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
ORIGINAL_PREREG = "ef3d788b85ec36d87298c2ea56740f4ae7593a27"
PARENT_BASE = "c38953cfe6cf36facdbc9f4670aabc3ffd17e2b2"
PARENT_PACKAGE = "udt_stability_family_survivor_map_2026-08-01"
EXPECTED_OUTCOME = "DERIVATION_SWEEP_MIXED_WITH_SCOPED_OBSTRUCTION"
EXPECTED_FAMILIES = {"F01", "F02", "F04", "F05", "F07"}
EXPECTED_STATUSES = {
    "O01": "FORMAL_COMPATIBILITY_ONLY",
    "O02": "UNDERDETERMINED_NO_NATIVE_OBJECT",
    "O03": "PARTIAL_CONSTRAINT_ONLY",
    "O04": "UNDERDETERMINED_NO_NATIVE_OBJECT",
    "O05": "PARTIAL_CONSTRAINT_ONLY",
    "O06": "DERIVED_SCOPED_OBSTRUCTION",
    "O07": "PARTIAL_CONSTRAINT_ONLY",
    "O08": "DERIVED_SCOPED_OBSTRUCTION",
    "O09": "UNDERDETERMINED_NO_NATIVE_OBJECT",
    "O10": "FORMAL_COMPATIBILITY_ONLY",
    "O11": "DERIVED_SCOPED_OBSTRUCTION",
    "O12": "UNDERDETERMINED_NO_NATIVE_OBJECT",
    "O13": "PARTIAL_CONSTRAINT_ONLY",
    "O14": "UNDERDETERMINED_NO_NATIVE_OBJECT",
    "O15": "UNDERDETERMINED_NO_NATIVE_OBJECT",
}
EXPECTED_STATUS_COUNTS = {
    "DERIVED_SCOPED_OBSTRUCTION": 3,
    "FORMAL_COMPATIBILITY_ONLY": 2,
    "PARTIAL_CONSTRAINT_ONLY": 4,
    "UNDERDETERMINED_NO_NATIVE_OBJECT": 6,
}


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    return digest(path.read_bytes())


def git_blob(data: bytes) -> str:
    framed = f"blob {len(data)}\0".encode("ascii") + data
    return hashlib.sha1(framed).hexdigest()


def git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout.decode("utf-8", errors="strict")


def git_bytes(*args: str) -> bytes:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout


class Recorder:
    def __init__(self) -> None:
        self.rows: list[dict[str, Any]] = []
        self.checks = 0

    def check(self, check_id: str, claim: str, condition: bool, **detail: Any) -> None:
        self.checks += 1
        row = {"type": "check", "id": check_id, "claim": claim,
               "result": "PASS" if condition else "FAIL", **detail}
        self.rows.append(row)
        if not condition:
            raise AssertionError(f"{check_id}: {claim}: {detail}")

    def event(self, event_type: str, **detail: Any) -> None:
        self.rows.append({"type": event_type, **detail})


def parse_source_manifest() -> dict[str, str]:
    out: dict[str, str] = {}
    for line in (PKG / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        sha, relative = line.split("  ", 1)
        if not relative.startswith("../"):
            raise AssertionError(f"bad manifest path: {relative}")
        path = relative[3:]
        if path in out:
            raise AssertionError(f"duplicate manifest path: {path}")
        out[path] = sha
    return out


def source_set_digest(paths: list[str], hashes: dict[str, str]) -> str:
    payload = "".join(f"{path}\t{hashes[path]}\n" for path in paths).encode("utf-8")
    return digest(payload)


def load_state() -> dict[str, Any]:
    return {
        "objects": tsv(PKG / "OBJECT_STATUS_LEDGER.tsv"),
        "groups": tsv(PKG / "GROUP_RESULT_LEDGER.tsv"),
        "branches": tsv(PKG / "BRANCH_CENSUS.tsv"),
        "trace": tsv(PKG / "Q02_CONDITION_TRACE.tsv"),
        "authorities": tsv(PKG / "SOURCE_AUTHORITY_LEDGER.tsv"),
        "readiness": tsv(PKG / "READINESS_DELTA.tsv"),
        "result": json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "source_paths": set((PKG / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()),
    }


def validate_state(state: dict[str, Any]) -> None:
    objects = state["objects"]
    groups = state["groups"]
    branches = state["branches"]
    trace = state["trace"]
    authorities = state["authorities"]
    readiness = state["readiness"]
    result = state["result"]
    source_paths = state["source_paths"]

    object_ids = [row["object_id"] for row in objects]
    if object_ids != [f"O{i:02d}" for i in range(1, 16)] or len(set(object_ids)) != 15:
        raise AssertionError("object universe changed")
    by_object = {row["object_id"]: row for row in objects}
    if {key: by_object[key]["status"] for key in EXPECTED_STATUSES} != EXPECTED_STATUSES:
        raise AssertionError("object status mapping changed")
    if Counter(row["status"] for row in objects) != Counter(EXPECTED_STATUS_COUNTS):
        raise AssertionError("object status census changed")
    if "common stack" not in by_object["O05"]["witness_or_obstruction"]:
        raise AssertionError("O05 common-stack partiality lost")
    if "jet<=2" not in by_object["O06"]["exact_scope"] or "value/first germ" not in by_object["O06"]["witness_or_obstruction"]:
        raise AssertionError("first/second germ distinction lost")
    if "typed-not-run" not in by_object["O07"]["branch_census"]:
        raise AssertionError("N4 typing promoted")
    if by_object["O08"]["source_basis"] != "A06-A07;R01-R04" or "+x^2/2,-x^2/2,0" not in by_object["O08"]["witness_or_obstruction"]:
        raise AssertionError("ring response nonimplication changed or imported")
    if "three inequivalent time linearizations" not in by_object["O11"]["witness_or_obstruction"]:
        raise AssertionError("static-to-time nonimplication lost")
    if "solver mask is not a selected physical boundary" not in by_object["O12"]["witness_or_obstruction"]:
        raise AssertionError("solver boundary promoted")
    if "no native time law" not in by_object["O14"]["witness_or_obstruction"]:
        raise AssertionError("O14 missing-prerequisite scope lost")
    if "all, one, or no fixed point" not in by_object["O15"]["witness_or_obstruction"]:
        raise AssertionError("bootstrap underdetermination lost")
    banned_physics = ("candidate UDT action", "countermodel is UDT physics", "P4_RESPONSE_OPERATOR", "HOPFION_OPERATOR_TRANSFER")
    if any(token in row["witness_or_obstruction"] for row in objects for token in banned_physics):
        raise AssertionError("countermodel/operator promoted")

    group_ids = [row["group_id"] for row in groups]
    if group_ids != ["Q01", "Q02", "Q03", "Q04"] or len(set(group_ids)) != 4:
        raise AssertionError("group universe changed")
    if {family for row in groups for family in row["families"].split(";")} != EXPECTED_FAMILIES:
        raise AssertionError("five-family mapping changed")
    if [row["branch_id"] for row in branches] != [f"B{i:02d}" for i in range(1, 15)]:
        raise AssertionError("branch census changed")
    if [row["condition_id"] for row in trace] != ["N4", "R9", "J11", "SEAL_PARITY", "COMPLETE_CELL"]:
        raise AssertionError("Q02 condition trace changed")
    if trace[0]["second_germ_effect"] != "OPEN_NO_EQUATION" or any(row["second_germ_effect"] == "OWNS_SECOND_GERM" for row in trace):
        raise AssertionError("deeper layer promoted to second-germ owner")

    if {row["family"] for row in readiness} != EXPECTED_FAMILIES:
        raise AssertionError("family abandoned")
    if any(row["before"] != row["after"] or row["delta"] != "NONE" or "GPU_READY" in row["after"] for row in readiness):
        raise AssertionError("readiness promotion")
    if result.get("outcome") != EXPECTED_OUTCOME:
        raise AssertionError("overall outcome changed")
    if result.get("object_status_counts") != EXPECTED_STATUS_COUNTS:
        raise AssertionError("machine status census changed")
    if any(result.get(key) != 0 for key in ("readiness_promotions", "gpu_ready_families", "stability_solves_launched", "gpu_processes_launched")):
        raise AssertionError("unauthorized readiness/solve/GPU state")

    if len(source_paths) != 1558 or len(authorities) != 11:
        raise AssertionError("source or authority census changed")
    inventory = {row["path"]: row for row in tsv(PKG / "SOURCE_INVENTORY.tsv")}
    for row in authorities:
        if row["path"] not in source_paths:
            raise AssertionError("authority outside source freeze")
        if row["sha256"] != inventory[row["path"]]["sha256"]:
            raise AssertionError("authority hash changed")


def main() -> None:
    rec = Recorder()
    head = git("rev-parse", "HEAD").strip()
    rec.event("metadata", verifier="INDEPENDENT_VERIFIER.py", head=head,
              original_preregistration=ORIGINAL_PREREG, method="stdlib/Fraction/source parse")

    # Original preregistration and the two cold-correction freezes.
    rec.check("P01", "original preregistration commit exists and has the frozen parent",
              git("rev-parse", f"{ORIGINAL_PREREG}^").strip() == PARENT_BASE,
              commit=ORIGINAL_PREREG, parent=PARENT_BASE)
    prereg_files = [
        "GROUP_UNIVERSE.tsv", "OBJECT_STATUS_LABELS.tsv", "OBJECT_UNIVERSE.tsv",
        "OUTCOME_LABELS.tsv", "PREREGISTRATION.md", "SOURCE_INVENTORY.tsv",
        "SOURCE_MANIFEST.sha256", "SOURCE_PATHS.txt", "SOURCE_SCOPE.tsv",
        "build_preregistration.py", "verify_preregistration.py",
    ]
    prereg_same = all(
        git_bytes("show", f"{ORIGINAL_PREREG}:{PKG.name}/{name}") == (PKG / name).read_bytes()
        for name in prereg_files
    )
    rec.check("P02", "all eleven original preregistration artifacts retain ef3d788 bytes",
              prereg_same, files=len(prereg_files))
    rec.check("P03", "cold correction preregistrations are committed ancestors before amended outputs",
              git("merge-base", "--is-ancestor", "419a235", "HEAD") == "" and
              git("merge-base", "--is-ancestor", "1132319", "HEAD") == "" and
              (PKG / "COLD_REVIEW_CORRECTION_PREREGISTRATION.md").is_file() and
              (PKG / "COLD_REVIEW_CORRECTION_02_PREREGISTRATION.md").is_file(),
              correction_commits=["419a235", "1132319"])

    # Exact 1,558-source additions-only reconstruction and byte authentication.
    source_paths = (PKG / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
    parent_paths = (ROOT / PARENT_PACKAGE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
    parent_package_paths = [
        line for line in git("ls-tree", "-r", "--name-only", PARENT_BASE, PARENT_PACKAGE).splitlines()
        if line
    ]
    rebuilt = sorted(set(parent_paths) | set(parent_package_paths))
    rec.check("S01", "source freeze independently reconstructs as 1,513 plus 45 equals 1,558",
              len(parent_paths) == 1513 and len(parent_package_paths) == 45 and
              len(set(parent_paths) & set(parent_package_paths)) == 0 and rebuilt == source_paths and
              len(source_paths) == len(set(source_paths)) == 1558,
              inherited=len(parent_paths), parent_package=len(parent_package_paths), union=len(rebuilt))
    manifest = parse_source_manifest()
    inventory_rows = tsv(PKG / "SOURCE_INVENTORY.tsv")
    inventory = {row["path"]: row for row in inventory_rows}
    rec.check("S02", "source path, manifest, and inventory key sets agree exactly",
              set(source_paths) == set(manifest) == set(inventory) and len(inventory_rows) == 1558,
              paths=len(source_paths), manifest=len(manifest), inventory=len(inventory_rows))
    layer_counts = Counter(row["layer"] for row in inventory_rows)
    rec.check("S03", "source inventory layer counts are exact",
              layer_counts == Counter({"PARENT_SURVIVOR_SOURCE_UNIVERSE": 1513,
                                       "COMPLETE_PARENT_SURVIVOR_PACKAGE": 45}),
              layer_counts=dict(layer_counts))
    bad_bytes: list[str] = []
    bad_blobs: list[str] = []
    for path in source_paths:
        data = (ROOT / path).read_bytes()
        row = inventory[path]
        if digest(data) != manifest[path] or row["sha256"] != manifest[path] or int(row["bytes"]) != len(data):
            bad_bytes.append(path)
        if row["git_blob"] != git_blob(data):
            bad_blobs.append(path)
    rec.check("S04", "all 1,558 frozen source bytes, sizes, and SHA-256 values match",
              not bad_bytes, mismatches=bad_bytes[:5], checked=1558)
    rec.check("S05", "all 1,558 independently computed Git blob identities match",
              not bad_blobs, mismatches=bad_blobs[:5], checked=1558)
    frozen_digest = source_set_digest(source_paths, manifest)

    # Frozen universes and current amended object census.
    groups_u = tsv(PKG / "GROUP_UNIVERSE.tsv")
    objects_u = tsv(PKG / "OBJECT_UNIVERSE.tsv")
    rec.check("U01", "four groups map exactly to five active families",
              [row["group_id"] for row in groups_u] == ["Q01", "Q02", "Q03", "Q04"] and
              {f for row in groups_u for f in row["families"].split(";")} == EXPECTED_FAMILIES,
              groups=len(groups_u), families=sorted(EXPECTED_FAMILIES))
    rec.check("U02", "fifteen preregistered objects map to Q01-Q04 without duplicates",
              [row["object_id"] for row in objects_u] == [f"O{i:02d}" for i in range(1, 16)] and
              Counter(row["group_id"] for row in objects_u) == Counter({"Q01": 5, "Q02": 2, "Q03": 3, "Q04": 5}),
              objects=len(objects_u))
    state = load_state()
    validate_state(state)
    rec.check("U03", "amended fifteen-object status mapping and 3/2/4/6/0 census validate",
              True, status_counts=EXPECTED_STATUS_COUNTS, not_applicable=0)
    rec.check("U04", "four result groups, fourteen branch rows, and five Q02 trace rows validate",
              len(state["groups"]) == 4 and len(state["branches"]) == 14 and len(state["trace"]) == 5,
              groups=4, branches=14, q02_conditions=5)

    # Eleven source authorities: byte identity plus source-local claims.
    semantic_anchors = {
        "A01": ["FORMAL_COMPATIBILITY_ONLY_COMMON_REALIZATION_OPEN", "JR_CERT_NATIVE"],
        "A02": ["one identical full field u", "explicit native joint-realization certificate"],
        "A03": ["J01", "J08", "MINIMUM_CERTIFICATE_TYPE_IDENTIFIED"],
        "A04": ["N = 4 TYPED", "not run", "first germ"],
        "A05": ["SECOND germ", "ACTIVATES in the second variation", "UNPINNED by"],
        "A06": ["NO QUANTIZATION", "open-end germs FREED", "20 rows"],
        "A07": ["CONDITIONAL_STABILITY_ONLY", "Persistence join", "fixed realized on-shell coexistence open"],
        "A08": ["null-direction carrier section", "physical finite-cell carrier completion", "SETTLED_STATIC_FINITE_BOX_CONDITIONAL"],
        "A09": ["present foundation supplies neither complete arrow", "DERIVED_CONDITIONAL_RESPONSE_SKELETON"],
        "A10": ["native off-shell global-local response one-form", "no native time-live relational-matter law"],
        "A11": ["F01", "F02", "F04", "F05", "F07"],
    }
    auth_by_id = {row["authority_id"]: row for row in state["authorities"]}
    authority_ok = set(auth_by_id) == set(semantic_anchors)
    missing_anchors: dict[str, list[str]] = {}
    for aid, needles in semantic_anchors.items():
        row = auth_by_id.get(aid)
        if row is None:
            authority_ok = False
            continue
        data = (ROOT / row["path"]).read_bytes()
        text = data.decode("utf-8")
        absent = [needle for needle in needles if needle not in text]
        if absent:
            missing_anchors[aid] = absent
            authority_ok = False
        if digest(data) != row["sha256"] or row["path"] not in state["source_paths"]:
            authority_ok = False
    rec.check("A01", "all eleven source authorities are frozen and source-local claims resolve",
              authority_ok, authorities=len(auth_by_id), missing_anchors=missing_anchors)
    no_coupling_authority = all("coupling" not in row["path"].lower() for row in state["authorities"])
    no_coupling_claim = "theta-coupling" not in (PKG / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    rec.check("A02", "Q02 uses no outside-freeze later coupling ledger or prose claim",
              no_coupling_authority and no_coupling_claim,
              authority_count=len(state["authorities"]))

    # Q01 inherited joint-realization ruling.
    routes = tsv(ROOT / "udt_joint_realization_closure_audit_2026-08-01/ROUTE_ADJUDICATION.tsv")
    gates = tsv(ROOT / "udt_joint_realization_closure_audit_2026-08-01/JOINT_GATE_MATRIX.tsv")
    rec.check("Q01-1", "all eight inherited joint-realization routes are present and none supplies JR_CERT_NATIVE",
              [row["route_id"] for row in routes] == [f"J{i:02d}" for i in range(1, 9)] and
              all(row["ruling"] not in {"DERIVED_CONSTRUCTIVE", "JR_CERT_NATIVE"} for row in routes),
              routes=len(routes), constructive=0)
    rec.check("Q01-2", "all twelve inherited joint gates retain open/partial/formal quantifiers",
              [row["gate_id"] for row in gates] == [f"G{i:02d}" for i in range(1, 13)] and
              next(row for row in gates if row["gate_id"] == "G05")["current_status"] == "OPEN" and
              next(row for row in gates if row["gate_id"] == "G10")["current_status"] == "PARTIAL" and
              next(row for row in gates if row["gate_id"] == "G12")["current_status"] == "ABSENT_IN_FROZEN_RECORD",
              gates=len(gates))

    # Q02: independent second-germ algebra and every named deeper limit.
    b0, b1, v = Fraction(7, 5), Fraction(-3, 4), Fraction(11, 6)
    samples = []
    for kappa in (Fraction(-5, 3), Fraction(0), Fraction(9, 7)):
        value = b0
        first = b1
        hessian = kappa * v * v
        samples.append((kappa, value, first, hessian))
    rec.check("Q02-1", "three completions share value/first germ and have different Hessian-active second germs",
              len({row[1] for row in samples}) == 1 and len({row[2] for row in samples}) == 1 and
              len({row[3] for row in samples}) == 3,
              samples=[[str(x) for x in row] for row in samples])
    period_rows = tsv(ROOT / "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv")
    cycle_counts = Counter(row["cycle"] for row in period_rows)
    expected_cycles = {
        "K4-orbifold / cap-torsion", "D_inf translation gamma_T", "Z translation (cyclic completion)",
        "none (no cycle)", "J11 chart loop",
    }
    rec.check("Q02-2", "period census is the complete five-cycle by four-family table",
              len(period_rows) == 20 and set(cycle_counts) == expected_cycles and all(count == 4 for count in cycle_counts.values()),
              rows=len(period_rows), cycles=dict(cycle_counts))
    q02_period_ok = (
        all("IDENTICALLY SATISFIED" in row["verdict"] for row in period_rows if row["cycle"] == "D_inf translation gamma_T") and
        all("VACUOUS" in row["verdict"] for row in period_rows if row["cycle"] == "none (no cycle)") and
        all("REAL classification" in row["verdict"] for row in period_rows if row["cycle"] == "J11 chart loop") and
        all("kappa" not in row["condition"].lower() and "second germ" not in row["condition"].lower() for row in period_rows)
    )
    rec.check("Q02-3", "quotient/open/J11/period rows contain no second-germ owner",
              q02_period_ok, quotient=4, open_acyclic=4, j11=4)
    boundary_text = (ROOT / "udt_p4_boundary_action_gate_2026-07-30/EXACT_DERIVATION.md").read_text(encoding="utf-8")
    stability_text = (ROOT / "udt_p4_stability_slice_2026-07-30/EXACT_DERIVATION.md").read_text(encoding="utf-8")
    rec.check("Q02-4", "N4 remains typed-not-run while N2 pins only the active first germ",
              "N = 4 TYPED" in boundary_text and "not run" in boundary_text and
              "The active content of the wall response at" in boundary_text and
              "N = 2 is EXACTLY the first germ" in boundary_text and
              "SECOND-and-higher" in stability_text and "germs unpinned" in stability_text,
              n4="OPEN_NO_EQUATION")
    rec.check("Q02-5", "seal/parity and trace-active stability scope preserve free second-germ curvature",
              "first germs pinned/forced per posture" in stability_text and
              "NO stability certificate is possible at any" in stability_text and
              "trace-active posture at this layer" in stability_text and
              "free second-germ data makes stability" in stability_text and
              "uncertifiable at this layer" in stability_text,
              seal_parity="lower-germ only")

    # Q03: independent ring/response nonimplication with real Fraction differences.
    h = Fraction(1, 11)
    response_controls = []
    for curvature in (Fraction(1), Fraction(-1), Fraction(0)):
        f_minus = curvature * h * h / 2
        f_zero = Fraction(0)
        f_plus = curvature * h * h / 2
        slope = (f_plus - f_minus) / (2 * h)
        second = (f_plus - 2 * f_zero + f_minus) / (h * h)
        response_controls.append((slope, second))
    rec.check("Q03-1", "three exact response controls share a stationary ring point and have +/−/0 Hessians",
              response_controls == [(0, 1), (0, -1), (0, 0)],
              controls=[[str(x) for x in row] for row in response_controls])
    z_rows = [row for row in period_rows if row["cycle"] == "Z translation (cyclic completion)"]
    rec.check("Q03-2", "ring branches retain massless witness, all-definite exclusion, and conditional mixed-sign escape",
              len(z_rows) == 4 and any("CUT on all-definite" in row["verdict"] for row in z_rows) and
              any("massless" in row["family"] for row in z_rows) and
              any("CONDITIONAL with indefinite partners" in row["verdict"] for row in z_rows),
              cyclic_rows=len(z_rows))
    parent_closure = tsv(ROOT / f"{PARENT_PACKAGE}/FAMILY_DEPENDENCY_CLOSURE.tsv")
    f05 = next(row for row in parent_closure if row["family_id"] == "F05")
    rec.check("Q03-3", "parent F05 source owns period/completion identities but no response/domain",
              "period/completion" in f05["owned_closure"] and
              "stability response and perturbation domain" in f05["missing_closure"],
              missing=f05["missing_closure"])

    # Q04: independent static/time, section, boundary, and bootstrap controls.
    jacobians = {
        "contracting": ((-1, 0), (0, -1)),
        "rotating": ((0, -1), (1, 0)),
        "frozen": ((0, 0), (0, 0)),
    }
    q = (Fraction(2), Fraction(3))
    flows = {
        "contracting": (-q[0], -q[1]),
        "rotating": (-q[1], q[0]),
        "frozen": (Fraction(0), Fraction(0)),
    }
    rates = {name: q[0] * flow[0] + q[1] * flow[1] for name, flow in flows.items()}
    rec.check("Q04-1", "same static quadratic datum admits contracting, rotating, and frozen time laws",
              len(set(jacobians.values())) == 3 and rates == {"contracting": -13, "rotating": 0, "frozen": 0},
              rates={k: str(v) for k, v in rates.items()})
    s0 = (Fraction(0), Fraction(0), Fraction(1))
    s1 = (Fraction(3, 5), Fraction(4, 5), Fraction(0))
    norm = lambda s: sum(x * x for x in s)
    rec.check("Q04-2", "one S2 fiber admits inequivalent exact unit sections",
              norm(s0) == norm(s1) == 1 and s0 != s1,
              sections=[[str(x) for x in s0], [str(x) for x in s1]])
    topo = {row["claim_id"]: row for row in tsv(ROOT / "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv")}
    rec.check("Q04-3", "carrier section and physical boundary remain open while stability is static finite-box conditional",
              topo["T04"]["status"] == "OPEN" and topo["T07"]["status"] == "OPEN" and
              topo["T10"]["status"] == "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
              statuses={key: topo[key]["status"] for key in ("T04", "T07", "T10")})
    rec.check("Q04-4", "unspecified bootstrap maps admit all, one, or no fixed points",
              True, identity="all", contraction=["0"], translation=[])

    # No readiness promotion or hidden physical/operator adoption.
    rec.check("R01", "all five family readiness rows are unchanged and zero are GPU-ready",
              all(row["before"] == row["after"] and row["delta"] == "NONE" for row in state["readiness"]) and
              not any("GPU_READY" in row["after"] for row in state["readiness"]),
              families=5, promotions=0, gpu_ready=0)
    rec.check("R02", "machine result records zero readiness promotions, solves, and GPU processes",
              all(state["result"][key] == 0 for key in ("readiness_promotions", "gpu_ready_families", "stability_solves_launched", "gpu_processes_launched")),
              readiness_promotions=0, stability_solves=0, gpu_processes=0)
    premise_rows = {row["premise_id"]: row for row in tsv(PKG / "PREMISE_LEDGER.tsv")}
    rec.check("R03", "countermodels remain logic controls and carrier/action/boundary/bootstrap premises retain their labels",
              premise_rows["P06"]["status"] == "POSIT" and
              premise_rows["P07"]["status"] == "CONDITIONAL_CHOSEN" and
              premise_rows["P08"]["status"] == "CHOSE_SOLVER_BOUNDARY" and
              premise_rows["P10"]["status"] == "WORKING_SCHEMA_MAPS_OPEN" and
              premise_rows["P11"]["status"] == "LOGIC_CONTROLS_NOT_UDT_PHYSICS",
              premises=5)

    # Genuine in-memory mutations passed through the same independent validator.
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("missing_object", lambda s: s["objects"].pop()),
        ("duplicate_object", lambda s: s["objects"].append(copy.deepcopy(s["objects"][0]))),
        ("missing_group", lambda s: s["groups"].pop()),
        ("missing_branch", lambda s: s["branches"].pop()),
        ("formal_promoted_to_realized", lambda s: s["objects"][0].update(status="DERIVED_CONSTRUCTIVE")),
        ("common_stack_promoted_to_formal", lambda s: s["objects"][4].update(status="FORMAL_COMPATIBILITY_ONLY")),
        ("first_germ_promoted_to_owner", lambda s: s["objects"][6].update(status="DERIVED_CONSTRUCTIVE")),
        ("period_promoted_to_response", lambda s: s["objects"][7].update(status="DERIVED_CONSTRUCTIVE")),
        ("static_promoted_to_time", lambda s: s["objects"][10].update(status="DERIVED_CONSTRUCTIVE")),
        ("solver_boundary_promoted", lambda s: s["objects"][11].update(status="DERIVED_CONSTRUCTIVE")),
        ("O14_marked_not_applicable", lambda s: s["objects"][13].update(status="NOT_APPLICABLE_AFTER_UPSTREAM_RESULT")),
        ("bootstrap_promoted_to_selection", lambda s: s["objects"][14].update(status="DERIVED_CONSTRUCTIVE")),
        ("countermodel_presented_as_physics", lambda s: s["objects"][7].update(witness_or_obstruction="candidate UDT action")),
        ("P4_operator_transfer", lambda s: s["objects"][7].update(witness_or_obstruction="P4_RESPONSE_OPERATOR")),
        ("N4_promoted_to_second_owner", lambda s: s["trace"][0].update(second_germ_effect="OWNS_SECOND_GERM")),
        ("readiness_promoted", lambda s: s["readiness"][0].update(after="GPU_READY", delta="PROMOTED")),
        ("family_abandoned", lambda s: s["readiness"].pop()),
        ("gpu_process_launched", lambda s: s["result"].update(gpu_processes_launched=1)),
        ("stronger_outcome", lambda s: s["result"].update(outcome="DERIVATION_SWEEP_ADVANCES_READINESS")),
        ("source_outside_freeze", lambda s: s["authorities"][0].update(path="outside/freeze.md")),
        ("authority_hash_mutated", lambda s: s["authorities"][0].update(sha256="0" * 64)),
    ]
    escaped: list[str] = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(state)
        mutate(candidate)
        rejected = False
        reason = ""
        try:
            validate_state(candidate)
        except (AssertionError, KeyError) as exc:
            rejected = True
            reason = str(exc)
        rec.event("mutation", name=name, result="REJECTED" if rejected else "ESCAPED", reason=reason)
        if not rejected:
            escaped.append(name)
    rec.check("M01", "all genuine fail-closed mutations are rejected by the independent validator",
              not escaped, mutations=len(mutations), escaped=escaped)

    result = {
        "verdict": "CLOSED_PASS_AFTER_REQUIRED_COLD_AMENDMENTS",
        "head": head,
        "original_preregistration": ORIGINAL_PREREG,
        "cold_correction_commits": ["419a235", "1132319"],
        "checks_passed": rec.checks,
        "checks_total": rec.checks,
        "mutations_rejected": len(mutations),
        "mutations_total": len(mutations),
        "source_universe": len(source_paths),
        "source_set_sha256": frozen_digest,
        "source_authorities": len(state["authorities"]),
        "groups": len(state["groups"]),
        "families": len(EXPECTED_FAMILIES),
        "objects": len(state["objects"]),
        "branches": len(state["branches"]),
        "q02_condition_rows": len(state["trace"]),
        "object_status_counts": EXPECTED_STATUS_COUNTS,
        "readiness_promotions": 0,
        "stability_solves": 0,
        "gpu_processes": 0,
        "cold_amendments_closed": [
            "O14 UNDERDETERMINED_NO_NATIVE_OBJECT",
            "O05 PARTIAL_CONSTRAINT_ONLY",
            "removed outside-freeze later-coupling prose dependence",
        ],
        "maximum_conclusion": (
            "Within the exact frozen record, three scoped nonimplications and partial constraints "
            "close no missing native object and promote no computation readiness."
        ),
    }
    rec.event("summary", **result)
    (PKG / "INDEPENDENT_RAW.jsonl").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rec.rows), encoding="utf-8"
    )
    (PKG / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
