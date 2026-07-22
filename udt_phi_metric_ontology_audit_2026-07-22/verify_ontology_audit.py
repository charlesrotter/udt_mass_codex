#!/usr/bin/env python3
"""Independent mechanical verifier for the phi–metric ontology audit.

The verifier imports neither production audit script. It reads frozen Git blobs
through cat-file, independently reconstructs the literal census and exact
algebra, checks cross-table logic, and exercises fail-closed mutations.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

import sympy as sp


BASE = "e06fb57b3e13a398289ec687a89cfd46b3728635"
ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
TEXT_SUFFIXES = {".md", ".tsv", ".txt", ".py", ".json", ".yaml", ".yml", ".tex", ".csv"}
TOKEN = re.compile(r"(?<![A-Za-z])(?:phi)(?![A-Za-z])|φ", re.IGNORECASE)


class ContractError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ContractError(label)


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def rows(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tree_entries() -> list[tuple[str, str]]:
    raw = subprocess.check_output(["git", "ls-tree", "-r", "-z", BASE], cwd=ROOT)
    result: list[tuple[str, str]] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        _mode, kind, blob = meta.decode().split()
        if kind == "blob":
            result.append((path.decode(), blob))
    return result


def cat_blobs(entries: list[tuple[str, str]]) -> dict[str, bytes]:
    proc = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=ROOT,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None and proc.stdout is not None
    result: dict[str, bytes] = {}
    for path, blob in entries:
        proc.stdin.write(blob.encode() + b"\n")
        proc.stdin.flush()
        header = proc.stdout.readline().decode().strip().split()
        require(len(header) == 3 and header[1] == "blob", f"cat_file_header:{path}")
        size = int(header[2])
        data = proc.stdout.read(size)
        require(proc.stdout.read(1) == b"\n", f"cat_file_separator:{path}")
        result[path] = data
    proc.stdin.close()
    return_code = proc.wait(timeout=60)
    require(return_code == 0, "cat_file_exit")
    return result


def independently_reconstruct_census() -> dict[str, dict[str, str]]:
    eligible = [
        item for item in tree_entries()
        if Path(item[0]).suffix.lower() in TEXT_SUFFIXES
        or Path(item[0]).name in {"LIVE.md", "HANDOFF.md", "INDEX.md", "MEMORY.md", "AGENTS.md", "CLAUDE.md", "CANON.md"}
    ]
    blobs = cat_blobs(eligible)
    result: dict[str, dict[str, str]] = {}
    for path, blob in eligible:
        data = blobs[path]
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        count = len(TOKEN.findall(text))
        if count:
            result[path] = {
                "git_blob": blob,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": str(len(data)),
                "phi_token_occurrences": str(count),
            }
    return result


def verify_census(census: list[dict[str, str]], summary: dict[str, object]) -> dict[str, object]:
    require(len(census) == len({row["path"] for row in census}), "census_unique_paths")
    rebuilt = independently_reconstruct_census()
    require(set(rebuilt) == {row["path"] for row in census}, "census_complete_path_set")
    for row in census:
        for field in ("git_blob", "sha256", "bytes", "phi_token_occurrences"):
            require(row[field] == rebuilt[row["path"]][field], f"census_field:{row['path']}:{field}")
    require(int(summary["candidate_files"]) == len(census), "summary_candidate_files")
    total = sum(int(row["phi_token_occurrences"]) for row in census)
    require(int(summary["literal_token_occurrences"]) == total, "summary_occurrences")
    require(summary["base"] == BASE, "summary_base")
    require(summary["generated_records_excluded_from_selection"] is True, "generated_exclusion")
    routing = dict(sorted(Counter(row["routing"] for row in census).items()))
    require(summary["routing_counts"] == routing, "summary_routing")
    return {"candidate_files": len(census), "literal_token_occurrences": total}


def first_last(path: str) -> tuple[str, str, str, str]:
    history = run("git", "log", "--follow", "--format=%H%x09%aI", "--", path).splitlines()
    require(bool(history), f"history_present:{path}")
    last_commit, last_date = history[0].split("\t", 1)
    first_commit, first_date = history[-1].split("\t", 1)
    return first_commit, first_date, last_commit, last_date


def verify_lineage(lineage: list[dict[str, str]], *, mutate_ok: bool = False) -> None:
    require(len(lineage) == 19, "lineage_count_19")
    require({row["source_id"] for row in lineage} == {f"S{i:02d}" for i in range(1, 20)}, "lineage_ids")
    require(len({row["path"] for row in lineage}) == 19, "lineage_unique_paths")
    tree = dict(tree_entries())
    selected = [(row["path"], tree[row["path"]]) for row in lineage]
    blobs = cat_blobs(selected)
    for row in lineage:
        path = row["path"]
        data = blobs[path]
        require(row["git_blob"] == tree[path], f"lineage_blob:{path}")
        require(row["sha256"] == hashlib.sha256(data).hexdigest(), f"lineage_sha:{path}")
        require(row["bytes"] == str(len(data)), f"lineage_size:{path}")
        fc, fd, lc, ld = first_last(path)
        require((row["first_commit"], row["first_commit_date"], row["last_commit"], row["last_commit_date"]) == (fc, fd, lc, ld), f"lineage_history:{path}")
        line_field = row["anchor_lines"]
        require(bool(re.fullmatch(r"\d+(?:-\d+)?", line_field)), f"anchor_line_syntax:{path}")
    s19 = next(row for row in lineage if row["source_id"] == "S19")
    require(s19["firewall"] == "MIXED_DATE__PRE_JULY_CONTENT_NEGATIVE_OR_LINEAGE_ONLY", "prefirewall_control_not_affirmative")
    for row in lineage:
        if row["source_id"] != "S19":
            require(row["firewall"] == "POST_FIREWALL_AFFIRMATIVE_ELIGIBLE", f"postfirewall:{row['source_id']}")


EXPECTED_RULINGS = {
    "O01": "DERIVED_EXACT_DECOMPOSITION",
    "O04": "OWNER_LOCKED_FOR_AUDIT",
    "O05": "NOT_DERIVED",
    "O08": "DERIVED_EXACT",
    "O09": "REFUTED_AS_STATED",
    "O10": "DERIVED_CONDITIONAL",
    "O11": "NOT_DERIVED",
    "O13": "OPEN",
    "O14": "OPEN",
    "O15": "CANONIZED_BINDING_STATIC_SCOPE",
    "O16": "NOT_DERIVED",
    "O17": "NOT_PRESENT_IN_CURRENT_FOUNDATION",
    "O18": "OPEN_NOT_DERIVED",
    "O19": "CHOSE_OPEN_CONFIGURATION_BRANCH_NOT_PHYSICS",
    "O20": "REFUTED_AS_OVERSTATEMENT",
    "O21": "DIMENSIONAL_CATEGORY_ERROR_AND_NOT_REGISTERED",
    "O22": "NOT_WELL_POSED_FROM_CURRENT_FOUNDATION",
    "O23": "OPEN_PRECISELY_IDENTIFIED",
}


def validate_contract(
    ontology: list[dict[str, str]],
    models: list[dict[str, str]],
    lineage: list[dict[str, str]],
    census: list[dict[str, str]],
) -> None:
    require(len(ontology) == 23, "ontology_count_23")
    require(len({row["id"] for row in ontology}) == 23, "ontology_unique_ids")
    by_id = {row["id"]: row for row in ontology}
    require(set(EXPECTED_RULINGS).issubset(by_id), "ontology_required_ids")
    for oid, ruling in EXPECTED_RULINGS.items():
        require(by_id[oid]["ruling"] == ruling, f"ruling:{oid}")
    source_ids = {row["source_id"] for row in lineage}
    for row in ontology:
        refs = {part for part in row["sources"].split(";") if part}
        require(bool(refs), f"ontology_sources_nonempty:{row['id']}")
        require(refs.issubset(source_ids), f"ontology_sources_valid:{row['id']}")
        require("S19" not in refs, f"no_prefirewall_affirmative_use:{row['id']}")

    require(len(models) == 5, "model_count_5")
    require(len({row["model_id"] for row in models}) == 5, "model_unique_ids")
    for row in models:
        require(row["foundation_gate"].startswith("FOUNDATION_COMPATIBLE"), f"model_gate:{row['model_id']}")
        limit = row["limit"].lower()
        require(
            bool(limit) and any(
                phrase in limit
                for phrase in ("not a complete", "not a selected", "no native", "unselected", "conditional control")
            ),
            f"model_limit:{row['model_id']}",
        )

    adjudicated = {row["path"] for row in census if row["review_status"] == "INDIVIDUALLY_ADJUDICATED"}
    require(adjudicated == {row["path"] for row in lineage}, "adjudicated_exactly_lineage")


def verify_algebra() -> dict[str, object]:
    p = sp.symbols("p", real=True)
    u, v, omega, c_e = sp.symbols("u v omega c_E", positive=True)
    A, B, b = sp.symbols("A B b", real=True, nonzero=True)
    ratio_phi = sp.log(v / u) / 2
    diag_diff = sp.diag(u, v) - sp.sqrt(u * v) * sp.diag(sp.exp(-ratio_phi), sp.exp(ratio_phi))
    decomp = all(sp.simplify(sp.powdenest(e, force=True)) == 0 for e in diag_diff)
    csn = sp.simplify(sp.expand_log(sp.log((omega*v)/(omega*u))/2, force=True) - sp.expand_log(ratio_phi, force=True)) == 0
    P = sp.diag(sp.exp(-p), sp.exp(p))
    K = sp.Matrix([[0, 1], [1, 0]])
    dual = all(sp.simplify(e) == 0 for e in P.T*K*P-K)
    Omega = sp.symbols("Omega", positive=True)
    g = Omega**2 * sp.diag(-sp.exp(-2*p)*c_e**2, sp.exp(2*p))
    recovered = sp.expand_log(sp.log(g[1,1]/(-g[0,0]/c_e**2))/4, force=True)
    reconstruction = sp.simplify(recovered-p) == 0 and not recovered.has(Omega)
    F = sp.Matrix([[0,b],[1/b,0]])
    H = sp.Matrix([[A,B],[B,A*b**2]])
    g_plus = sp.simplify(P.T*H*P)
    Pm = sp.diag(sp.exp(p), sp.exp(-p))
    g_minus = sp.simplify(Pm.T*H*Pm)
    mirror = all(sp.simplify(e) == 0 for e in F.T*g_minus*F-g_plus)
    independent = {
        "positive_pair_decomposition": decomp,
        "common_scale_phi_invariance": csn,
        "dual_pairing_invariance": dual,
        "diagonal_block_phi_reconstruction": reconstruction,
        "K_readout_phi_invisible": dual and not (P.T*K*P).has(p),
        "mixed_readout_phi_visible": g_plus.has(p),
        "mixed_readout_seal_identity": mirror,
    }
    require(all(independent.values()), "independent_algebra")
    production = json.loads((PKG / "ONTOLOGY_ALGEBRA_RESULT.json").read_text())
    require(production["all_pass"] is True and len(production["checks"]) == 9, "production_algebra_9_of_9")
    for key, value in independent.items():
        require(production["checks"][key] is value, f"algebra_agreement:{key}")
    return {"independent_checks": len(independent), "production_checks": len(production["checks"])}


def mutation_catches(
    ontology: list[dict[str, str]],
    models: list[dict[str, str]],
    lineage: list[dict[str, str]],
    census: list[dict[str, str]],
) -> list[dict[str, str]]:
    catches: list[dict[str, str]] = []

    def expect(label: str, mutate) -> None:
        o, m, l, c = copy.deepcopy(ontology), copy.deepcopy(models), copy.deepcopy(lineage), copy.deepcopy(census)
        mutate(o, m, l, c)
        try:
            validate_contract(o, m, l, c)
        except ContractError as exc:
            catches.append({"catch_id": label, "result": "PASS_REJECTED", "caught_by": str(exc)})
        else:
            raise ContractError(f"mutation_false_pass:{label}")

    expect("C01_MISSING_ONTOLOGY_ROW", lambda o,m,l,c: o.pop())
    expect("C02_DUPLICATE_ONTOLOGY_ID", lambda o,m,l,c: o.append(copy.deepcopy(o[0])))
    expect("C03_PROMOTE_INDEPENDENT_PHI", lambda o,m,l,c: next(r for r in o if r["id"]=="O13").update(ruling="DERIVED"))
    expect("C04_PROMOTE_COMPLETE_METRIC_RECONSTRUCTION", lambda o,m,l,c: next(r for r in o if r["id"]=="O11").update(ruling="DERIVED"))
    expect("C05_PROMOTE_PLANCK_ENDPOINT", lambda o,m,l,c: next(r for r in o if r["id"]=="O21").update(ruling="DERIVED_NATIVE_ENDPOINT"))
    expect("C06_MISLABEL_PHI_AS_CSN_GAUGE", lambda o,m,l,c: next(r for r in o if r["id"]=="O09").update(ruling="DERIVED_CSN_GAUGE"))
    expect("C07_REMOVE_REQUIRED_SOURCE", lambda o,m,l,c: next(r for r in o if r["id"]=="O10").update(sources=""))
    expect("C08_USE_PREFIREWALL_AFFIRMATIVELY", lambda o,m,l,c: next(r for r in o if r["id"]=="O01").update(sources="S19"))
    expect("C09_PROMOTE_ATLAS_BRANCH_TO_PHYSICS", lambda o,m,l,c: next(r for r in o if r["id"]=="O19").update(ruling="DERIVED_PHYSICS"))
    expect("C10_PROMOTE_SEAL_TO_EOM", lambda o,m,l,c: next(r for r in o if r["id"]=="O16").update(ruling="DERIVED_EOM"))
    expect("C11_DELETE_MODEL_LIMIT", lambda o,m,l,c: m[0].update(limit=""))
    expect("C12_MISSING_CONFIGURATION_MODEL", lambda o,m,l,c: m.pop())
    expect("C13_DUPLICATE_CONFIGURATION_MODEL", lambda o,m,l,c: m.append(copy.deepcopy(m[0])))
    expect("C14_PROMOTE_UNREVIEWED_CENSUS_ROW", lambda o,m,l,c: next(r for r in c if r["review_status"]!="INDIVIDUALLY_ADJUDICATED").update(review_status="INDIVIDUALLY_ADJUDICATED"))
    expect("C15_PROMOTE_TIME_LIVE_READY", lambda o,m,l,c: next(r for r in o if r["id"]=="O22").update(ruling="WELL_POSED"))

    # Two catches use the independent source/algebra gates rather than table logic.
    lbad = copy.deepcopy(lineage)
    lbad[0]["sha256"] = "0" * 64
    try:
        verify_lineage(lbad, mutate_ok=True)
    except ContractError as exc:
        catches.append({"catch_id": "C16_SOURCE_HASH_MUTATION", "result": "PASS_REJECTED", "caught_by": str(exc)})
    else:
        raise ContractError("mutation_false_pass:C16_SOURCE_HASH_MUTATION")

    p = sp.symbols("p", real=True)
    broken = sp.diag(sp.exp(-p), sp.exp(2*p))
    K = sp.Matrix([[0,1],[1,0]])
    if any(sp.simplify(e) != 0 for e in broken.T*K*broken-K):
        catches.append({"catch_id": "C17_BROKEN_RECIPROCAL_PAIR", "result": "PASS_REJECTED", "caught_by": "dual_pairing_invariance"})
    else:
        raise ContractError("mutation_false_pass:C17_BROKEN_RECIPROCAL_PAIR")
    return catches


def verify_scope_only_package_changes() -> list[str]:
    changed = run("git", "status", "--porcelain").splitlines()
    paths: list[str] = []
    for line in changed:
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        require(path.startswith("udt_phi_metric_ontology_audit_2026-07-22/"), f"out_of_scope_change:{path}")
        paths.append(path)
    require(run("git", "merge-base", BASE, "HEAD") == BASE, "branch_base_ancestry")
    prereg_paths = run("git", "diff-tree", "--no-commit-id", "--name-only", "-r", "3e25ae2").splitlines()
    require(prereg_paths == ["udt_phi_metric_ontology_audit_2026-07-22/PREREGISTRATION.md"], "prereg_commit_scope")
    return paths


def main() -> None:
    require(run("git", "rev-parse", BASE) == BASE, "base_resolves")
    ontology = rows("PHI_ONTOLOGY_LEDGER.tsv")
    models = rows("CONFIGURATION_MODEL_LEDGER.tsv")
    lineage = rows("LOAD_BEARING_SOURCE_LINEAGE.tsv")
    census = rows("FORENSIC_PHI_SOURCE_CENSUS.tsv")
    summary = json.loads((PKG / "FORENSIC_CENSUS_SUMMARY.json").read_text())

    census_result = verify_census(census, summary)
    verify_lineage(lineage)
    validate_contract(ontology, models, lineage, census)
    algebra_result = verify_algebra()
    changed_paths = verify_scope_only_package_changes()
    catches = mutation_catches(ontology, models, lineage, census)
    require(len(catches) == 17 and all(row["result"] == "PASS_REJECTED" for row in catches), "all_17_catches")

    with (PKG / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch_id", "result", "caught_by"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)

    result = {
        "base": BASE,
        "status": "PASS",
        "grade_ceiling": "VERIFIED-WITH-CAVEATS_NO_FRESH_EXTERNAL_SEMANTIC_REVIEW",
        "ontology_rows": len(ontology),
        "configuration_models": len(models),
        "load_bearing_sources": len(lineage),
        "census": census_result,
        "algebra": algebra_result,
        "catch_proofs": {"passed": len(catches), "total": 17},
        "scope_only_package_changes": True,
        "changed_paths_observed": len(changed_paths),
        "claims_not_made": [
            "complete_metric_to_phi_map", "independent_off_shell_phi", "native_action",
            "time_live_law", "Planck_endpoint", "matter", "mass", "scale", "topology_selection",
        ],
    }
    (PKG / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
