#!/usr/bin/env python3
"""Fail-closed verifier for the stability/action boundary-bridge audit."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from copy import deepcopy
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
BASE = "3d136a8"
OUTCOME = "PARTIAL_ANALOGIES_ONLY__F01_BOUNDARY_BRIDGE_OPEN"
SOURCE_ROOTS = (
    "native_action_final_adjudication_2026-07-18/",
    "native_action_arm_c_2026-07-18/",
    "native_action_stage1_2026-07-18/",
    "native_action_stage2_2026-07-18/",
    "native_action_external_verifier_2026-07-18/",
    "udt_native_stability_configuration_space_audit_2026-08-01/",
    "udt_f01_lambda_schur_check_2026-08-01/",
    "udt_stability_derivation_closure_sweep_2026-08-01/",
    "udt_p4_boundary_action_gate_2026-07-30/",
    "udt_p4_stability_slice_2026-07-30/",
)
SOURCE_FILES = {
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md",
    "UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md",
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "PONDER_MATH_ELEGANCE_2026-07-31.md",
}


def table(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git_blob(path: str) -> tuple[str, bytes]:
    blob = subprocess.run(
        ["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()
    data = subprocess.run(
        ["git", "cat-file", "blob", blob], cwd=ROOT, check=True, capture_output=True
    ).stdout
    return blob, data


def selected_base_paths() -> list[str]:
    raw = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "-z", BASE],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    paths = [token.decode("utf-8") for token in raw.split(b"\0") if token]
    return sorted(
        path for path in paths
        if path in SOURCE_FILES or any(path.startswith(root) for root in SOURCE_ROOTS)
    )


def literal_search(payloads: dict[str, bytes]) -> list[dict[str, str]]:
    groups = {
        "ACTION_CORPUS": [p for p in payloads if p.startswith(("native_action_", "UDT_GR_TO_UDT"))],
        "P4_F01_CORPUS": [p for p in payloads if p.startswith(("udt_p4_", "udt_f01_"))],
    }
    patterns = [
        ("F01", r"\bF01\b"),
        ("R05", r"\bR05\b"),
        ("R06", r"\bR06\b"),
        ("second_wall_germ", r"second wall germ"),
        ("Bach", r"\bBach\b"),
        ("EH_or_Einstein_Hilbert", r"\bEH\b|Einstein[- ]Hilbert"),
        ("p_f_h_lambda_tuple", r"p\s*,\s*f\s*,\s*h\s*,\s*lambda"),
    ]
    rows: list[dict[str, str]] = []
    for group, paths in groups.items():
        for label, pattern in patterns:
            regex = re.compile(pattern, re.IGNORECASE)
            hits: list[str] = []
            occurrences = 0
            for path in sorted(paths):
                count = len(regex.findall(payloads[path].decode("utf-8", errors="replace")))
                if count:
                    occurrences += count
                    hits.append(path)
            rows.append({
                "corpus": group,
                "token": label,
                "occurrences": str(occurrences),
                "source_count": str(len(hits)),
                "paths": ";".join(hits),
            })
    return rows


def validate(data: dict[str, object]) -> None:
    result = data["result"]
    assert isinstance(result, dict)
    if result.get("primary_outcome") != OUTCOME:
        raise AssertionError("outcome promotion or mutation")
    if result.get("exact_map_count_from_action_routes") != 0:
        raise AssertionError("invented action-route map")
    if result.get("second_wall_germ_owner") != "OPEN":
        raise AssertionError("invented second-germ owner")
    if result.get("c2_bach_current_applicability") != "INACTIVE_WITHOUT_STRONG_CSN_PREMISE__COUNTERFACTUAL_ONLY":
        raise AssertionError("inactive C2/Bach route promoted")

    gates = data["gates"]
    assert isinstance(gates, list)
    if len(gates) != 36:
        raise AssertionError("route/gate census mismatch")
    keyed = {(r["route"], r["gate"]): r for r in gates}
    if len(keyed) != 36:
        raise AssertionError("missing or duplicate route/gate")
    for route in ("C2_BACH_PRE_SCALE", "EH_POST_SCALE", "TWO_STAGE_BRIDGE"):
        rows = [r for r in gates if r["route"] == route]
        if len(rows) != 12:
            raise AssertionError(f"route gate mismatch: {route}")
        if not any(r["status"] == "BLOCK" for r in rows):
            raise AssertionError(f"route improperly promoted: {route}")
    route_status = {
        "C2_BACH_PRE_SCALE": "INACTIVE_WITHOUT_STRONG_CSN_PREMISE__COUNTERFACTUAL_ONLY",
        "EH_POST_SCALE": "CONDITIONAL_NOT_SELECTED",
        "TWO_STAGE_BRIDGE": "OPEN_UNDERIVED",
    }
    for row in gates:
        if row["route_current_status"] != route_status[row["route"]]:
            raise AssertionError(f"route applicability stamp lost: {row['route']}")
    for route in ("C2_BACH_PRE_SCALE", "EH_POST_SCALE"):
        row = keyed[(route, "derivative_order_and_principal_symbol")]
        if row["status"] != "CONDITIONAL_ANALOGY_ONLY":
            raise AssertionError("derivative order promoted from analogy")
    if keyed[("C2_BACH_PRE_SCALE", "boundary_functional_and_charge")]["status"] != "BLOCK":
        raise AssertionError("C2 boundary completion invented")
    if keyed[("EH_POST_SCALE", "scale_ordering_and_bootstrap_dependence")]["status"] != "BLOCK":
        raise AssertionError("EH representative invented")
    for route in ("C2_BACH_PRE_SCALE", "EH_POST_SCALE", "TWO_STAGE_BRIDGE"):
        if keyed[(route, "preservation_of_R05_R06_trace_fork")]["status"] != "BLOCK":
            raise AssertionError(f"trace-domain map invented: {route}")
        if keyed[(route, "ownership_of_second_wall_germ")]["status"] != "BLOCK":
            raise AssertionError(f"second-germ ownership invented: {route}")

    maps = data["maps"]
    assert isinstance(maps, list)
    if len(maps) != 4 or len({r["id"] for r in maps}) != 4:
        raise AssertionError("map ledger census")
    for row in maps[:3]:
        if row["exact_map_exists"] != "NO":
            raise AssertionError("candidate action map invented")
    if maps[3]["exact_map_exists"] != "YES_CONDITIONAL_ONLY":
        raise AssertionError("internal P4 map stamp lost")

    premises = {r["id"]: r for r in data["premises"]}  # type: ignore[index]
    required = {
        "P02": ("UNIQUE_CONDITIONAL_INACTIVE_WITHOUT_STRONG_CSN", "counterfactual compatibility audit only; not active candidate"),
        "P03": ("CONDITIONAL", "tested only as registered conditional route"),
        "P04": ("OPEN", "not assumed"),
        "P05": ("CONDITIONAL", "exact target; not promoted"),
        "P07": ("OPEN", "ownership is the tested join"),
        "P08": ("WORKING_POSIT_WITHOUT_OPERATION", "not assumed"),
        "P10": ("WORKING_LEAD_ONLY", "never affirmative authority"),
    }
    for pid, pair in required.items():
        row = premises.get(pid)
        if not row or (row["entry_status"], row["audit_treatment"]) != pair:
            raise AssertionError(f"premise lost or promoted: {pid}")

    controls_rows = data["controls"]
    assert isinstance(controls_rows, list)
    expected_constructions = {
        "C01": "delta integral(1/2 u_prime^2) = integral(-u_doubleprime v) + [u_prime v]",
        "C02": "delta integral(1/2 u_doubleprime^2) = integral(u_fourth v) + [u_doubleprime v_prime-u_tripleprime v]",
        "C03": "L_tilde=L+d(kappa u^2/2)/dx",
        "C04": "second variation of [kappa u^2/2] along v is [kappa v^2]",
        "C05": "bulk equation equality != action reduction != boundary one-form pullback != boundary Hessian identity",
    }
    if len(controls_rows) != 5 or len({r["id"] for r in controls_rows}) != 5:
        raise AssertionError("control census")
    for row in controls_rows:
        if row["construction"] != expected_constructions.get(row["id"]) or row["status"] != "PASS":
            raise AssertionError(f"control ledger mutation: {row['id']}")


def controls() -> list[tuple[str, bool]]:
    x, eps, kappa = sp.symbols("x eps kappa")
    u = sp.Function("u")(x)
    v = sp.Function("v")(x)
    ue = u + eps * v
    d = lambda expr, n=1: sp.diff(expr, x, n)
    var = lambda expr: sp.diff(expr, eps).subs(eps, 0)

    l2_var = var(d(ue) ** 2 / 2)
    c01 = sp.simplify(l2_var - (-d(u, 2) * v + d(d(u) * v))) == 0
    l4_var = var(d(ue, 2) ** 2 / 2)
    c02 = sp.simplify(l4_var - (d(u, 4) * v + d(d(u, 2) * d(v) - d(u, 3) * v))) == 0
    added_density = d(kappa * ue**2 / 2)
    c03 = sp.simplify(var(added_density) - d(kappa * u * v)) == 0
    c04 = sp.simplify(sp.diff(kappa * ue**2 / 2, eps, 2).subs(eps, 0) - kappa * v**2) == 0
    # Distinct typed objects are intentionally not equated.
    typed = {"bulk_euler", "action_reduction", "boundary_one_form", "boundary_hessian"}
    c05 = len(typed) == 4
    return [("C01", c01), ("C02", c02), ("C03", c03), ("C04", c04), ("C05", c05)]


def catches(base: dict[str, object]) -> list[list[str]]:
    rows: list[list[str]] = []

    def expect(name: str, mutation) -> None:
        trial = deepcopy(base)
        mutation(trial)
        caught = False
        try:
            validate(trial)
        except (AssertionError, KeyError, IndexError):
            caught = True
        rows.append([name, "PASS" if caught else "FAIL"])

    expect("invent_C2_map", lambda d: d["maps"][0].update(exact_map_exists="YES"))
    expect("invent_EH_map", lambda d: d["maps"][1].update(exact_map_exists="YES"))
    expect("invent_two_stage_map", lambda d: d["maps"][2].update(exact_map_exists="YES"))
    expect("promote_derivative_order_to_map", lambda d: d["gates"][3].update(status="PASS_MAP"))
    expect("invent_C2_boundary", lambda d: d["gates"][5].update(status="PASS"))
    expect("invent_EH_representative", lambda d: d["gates"][21].update(status="PASS"))
    expect("erase_R05_R06_block", lambda d: d["gates"][7].update(status="PASS"))
    expect("assign_second_germ_owner", lambda d: d["result"].update(second_wall_germ_owner="C2"))
    expect("promote_P4_response", lambda d: d["premises"][4].update(entry_status="DERIVED_NATIVE"))
    expect("adopt_bootstrap_operation", lambda d: d["premises"][7].update(audit_treatment="DERIVED"))
    expect("promote_PONDER", lambda d: d["premises"][9].update(entry_status="DERIVED"))
    expect("drop_route_gate", lambda d: d["gates"].pop())
    expect("duplicate_map", lambda d: d["maps"].append(deepcopy(d["maps"][0])))
    expect("promote_primary_outcome", lambda d: d["result"].update(primary_outcome="EXACT_C2_BACH_TO_F01_BOUNDARY_MAP_DERIVED"))
    expect("activate_C2_without_strong_CSN", lambda d: d["gates"][0].update(route_current_status="ACTIVE"))
    expect("mutate_control_to_false_identity", lambda d: d["controls"][0].update(construction="FALSE_IDENTITY"))
    return rows


def main() -> None:
    sources = table("SOURCE_INVENTORY.tsv")
    if not sources or len({row["path"] for row in sources}) != len(sources):
        raise AssertionError("source inventory missing/duplicate")
    if [row["path"] for row in sources] != selected_base_paths():
        raise AssertionError("source inventory does not exactly cover preregistered roots")
    payloads: dict[str, bytes] = {}
    for row in sources:
        blob, payload = git_blob(row["path"])
        payloads[row["path"]] = payload
        if blob != row["git_blob"] or str(len(payload)) != row["bytes"]:
            raise AssertionError(f"source identity mismatch: {row['path']}")
        if hashlib.sha256(payload).hexdigest() != row["sha256"]:
            raise AssertionError(f"source sha mismatch: {row['path']}")
    manifest = (PKG / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    if manifest != [f"{r['sha256']}  {r['path']}" for r in sources]:
        raise AssertionError("source manifest mismatch")
    if table("LITERAL_MAP_SEARCH.tsv") != literal_search(payloads):
        raise AssertionError("literal cross-corpus census mismatch")

    authorities = table("SOURCE_AUTHORITY_LEDGER.tsv")
    by_path = {row["path"]: row for row in sources}
    if len(authorities) != 14 or len({row["id"] for row in authorities}) != 14:
        raise AssertionError("authority census")
    for row in authorities:
        src = by_path.get(row["path"])
        if not src or row["git_blob"] != src["git_blob"] or row["sha256"] != src["sha256"]:
            raise AssertionError(f"authority identity mismatch: {row['id']}")

    data: dict[str, object] = {
        "result": json.loads((PKG / "RESULT.json").read_text(encoding="utf-8")),
        "gates": table("ROUTE_GATE_MATRIX.tsv"),
        "maps": table("EXACT_MAP_LEDGER.tsv"),
        "premises": table("PREMISE_LEDGER.tsv"),
        "controls": table("EXACT_CONTROL_LEDGER.tsv"),
    }
    validate(data)
    if len(table("OBSTRUCTION_LEDGER.tsv")) != 8:
        raise AssertionError("obstruction census")
    control_results = controls()
    ledger = {r["id"]: r for r in data["controls"]}  # type: ignore[index]
    if len(ledger) != 5 or not all(ok and ledger[cid]["status"] == "PASS" for cid, ok in control_results):
        raise AssertionError("exact controls")
    catch_rows = catches(data)
    if not all(row[1] == "PASS" for row in catch_rows):
        raise AssertionError("mutation catch failure")
    with (PKG / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["mutation", "caught"])
        writer.writerows(catch_rows)

    report = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    derivation = (PKG / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (PKG / "LAY_REPORT.md").read_text(encoding="utf-8")
    for token in (OUTCOME, "bounded no-bridge result", "second wall germ remains open"):
        if token not in report:
            raise AssertionError(f"audit-report token missing: {token}")
    for token in ("kappa u v", "kappa v^2", "Zero exact action-route maps"):
        if token not in derivation:
            raise AssertionError(f"exact-derivation token missing: {token}")
    if "leaves the stability hypothesis alive" not in lay:
        raise AssertionError("lay scope statement missing")

    result = {
        "status": "PASS",
        "base_commit": BASE,
        "source_count": len(sources),
        "authority_count": len(authorities),
        "routes": 3,
        "gates_per_route": 12,
        "exact_controls_passed": 5,
        "semantic_catches_passed": len(catch_rows),
        "semantic_catches_total": len(catch_rows),
        "primary_outcome": OUTCOME,
        "action_route_exact_map_count": 0,
        "second_wall_germ_owner": "OPEN",
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
