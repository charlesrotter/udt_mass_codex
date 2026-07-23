#!/usr/bin/env python3
"""Repository gates for the angular bulk Jacobi/selector audit."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE.name
BASE = "1844bdf884b2cbeb8be7dda0aa81689c249cbc68"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
PREVIOUS = "udt_relative_angular_area_shape_selector_audit_2026-07-23"
PREVIOUS_MANIFEST = (
    "2c72943cfaba0df88f96182c796a51fc3653fec6cbddb7198897d104470d7db8"
)
MAXIMUM = (
    "COMPLETE_METRIC_DERIVES_THE_COVARIANT_ANGULAR_JACOBI_TRANSPORT_"
    "OBJECT_BUT_CURRENT_UDT_PREMISES_DO_NOT_SUPPLY_ITS_INDEPENDENT_"
    "CURVATURE_CLOSURE"
)


def load(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def replay_prior(generic, corrupt: bool = False) -> dict[str, object]:
    previous = load(
        ROOT / PREVIOUS / "verify_repository_gates.py",
        "bulk_jacobi_previous_gate_chain",
    )
    result = previous.replay_prior(generic, corrupt)
    details = list(result["packages"])
    entries = int(result["entries"])
    manifest = ROOT / PREVIOUS / "MANIFEST.sha256"
    observed = digest(manifest)
    if corrupt:
        observed = "0" * 64
    if observed != PREVIOUS_MANIFEST:
        raise generic.GateError("PRIOR", PREVIOUS + ":manifest")
    replay = generic.run(
        manifest.parent, ["sha256sum", "--check", manifest.name]
    )
    if replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PRIOR", PREVIOUS + ":replay")
    count = len([line for line in manifest.read_text().splitlines() if line])
    details.append(
        {
            "package": PREVIOUS,
            "manifest": manifest.name,
            "manifest_sha256": observed,
            "entries": count,
            "result": "PASS",
        }
    )
    entries += count
    if len(details) != 97:
        raise generic.GateError("PRIOR", f"package-count:{len(details)}")
    return {"packages": details, "entries": entries, "result": "PASS"}


def validate_package(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "MANIFEST.sha256"
    replay = generic.run(HERE, ["sha256sum", "--check", manifest.name])
    if corrupt or replay.returncode or "FAILED" in str(replay.stdout):
        raise generic.GateError("PACKAGE", "manifest-replay")
    entries = [
        line.split("  ", 1)[1]
        for line in manifest.read_text().splitlines()
        if line
    ]
    excluded = {"MANIFEST.sha256", "REPOSITORY_GATES.json"}
    actual = sorted(
        path.name
        for path in HERE.iterdir()
        if path.is_file() and path.name not in excluded
    )
    if sorted(entries) != actual:
        raise generic.GateError("PACKAGE", "manifest-coverage")
    return {
        "entries": len(entries),
        "manifest_sha256": digest(manifest),
        "result": "PASS",
    }


def validate_navigation(generic) -> dict[str, int]:
    saved = generic.PACKAGE
    generic.PACKAGE = "__NO_PACKAGE_MARKDOWN__"
    try:
        result = generic.validate_navigation(ROOT)
    finally:
        generic.PACKAGE = saved

    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    links = 0
    for source in sorted(HERE.glob("*.md")):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target = unquote(raw.strip().strip("<>").split("#", 1)[0])
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = re.sub(r":\d+$", "", target)
            destination = source.parent.joinpath(target).resolve()
            links += 1
            if not destination.exists():
                raise generic.GateError(
                    "NAVIGATION", f"{source.name}:{raw}"
                )
    result["package_links"] = links
    return result


def validate_dirty_head(generic) -> dict[str, str]:
    head = subprocess.check_output(
        ["git", "-C", str(DIRTY), "rev-parse", "HEAD"], text=True
    ).strip()
    branch = subprocess.check_output(
        ["git", "-C", str(DIRTY), "branch", "--show-current"], text=True
    ).strip()
    if (
        head != "adf8f92d95c387cc647f04b16f1f3b17e1e670d2"
        or branch != "grok"
    ):
        raise generic.GateError("DIRTY", f"{head}:{branch}")
    return {"head": head, "branch": branch}


def validate_science() -> dict[str, object]:
    result = json.loads((HERE / "RESULT.json").read_text())
    projected = json.loads(
        (HERE / "FULL_PROJECTED_JACOBI_FORMULA.json").read_text()
    )
    generic = json.loads(
        (HERE / "GENERIC_REDUCED_RICCATI_FORMULA.json").read_text()
    )
    trace_shape = json.loads(
        (HERE / "TRACE_SHAPE_TWIST_EVOLUTION.json").read_text()
    )
    csn = json.loads(
        (HERE / "CSN_NORMALIZED_REPRESENTATIVE.json").read_text()
    )
    theorem = json.loads(
        (HERE / "RECIPROCAL_SOURCE_CONDITIONAL_THEOREM.json").read_text()
    )
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text()
    )
    tests = json.loads((HERE / "FULL_TEST_RESULT.json").read_text())
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    routes = read_tsv(HERE / "ROUTE_RULING_MATRIX.tsv")
    universe = read_tsv(HERE / "ROUTE_UNIVERSE.tsv")
    controls = read_tsv(HERE / "CONTROL_ATLAS.tsv")
    nonblock = read_tsv(HERE / "NONBLOCK_CONTROLS.tsv")
    freedoms = read_tsv(HERE / "SOURCE_TERM_FREEDOM.tsv")
    boundaries = read_tsv(HERE / "BOUNDARY_PROPAGATION_ATLAS.tsv")
    flows = read_tsv(HERE / "CONDITIONAL_TWO_SEAL_FLOW.tsv")
    joins = read_tsv(HERE / "JOIN_LEDGER.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")

    for row in lineage:
        source = ROOT / row["path"]
        if (
            not source.is_file()
            or digest(source) != row["sha256"]
            or source.stat().st_size != int(row["size"])
        ):
            raise AssertionError("source lineage changed")

    counts = result["counts"]
    route_ids = [row["route_id"] for row in routes]
    if (
        result["maximum_conclusion"] != MAXIMUM
        or result["sympy_version"] != "1.14.0"
        or result["smallest_missing_join"]
        != "Delta_K=K_eff_angular-K_rec=0"
        or projected["projected_identity"]
        != "D_T(B)+B^2+K_eff=0"
        or projected["effective_source"]
        != "K_eff=P*R_T*P+X*Y-U*Y-X*V-P*nabla(a)*P"
        or not projected["nonblock_terms_retained"]
        or generic["same_q_qp_arbitrary_qpp_tidal_rank"] != 3
        or trace_shape["trace_equation"]
        != (
            "D_T(A_rel)+A_rel^2+S_shape-omega^2"
            "+(1/2)tr(K_eff)=0"
        )
        or trace_shape["target_requires"]["twistfree_trace_source"]
        != "tr(K_eff)=-2"
        or csn["reciprocal_determinant"] != "det(h_star)=-c^2"
        or theorem["transport_residual"] != "EXACT_ZERO"
        or theorem["missing_join_status"] != "UNREGISTERED_NOT_DERIVED"
        or theorem["native_status"] != "NOT_A_CURRENT_UDT_DERIVATION"
        or counts["routes"] != 12
        or counts["native_bulk_law_derivations"] != 0
        or counts["conditional_bulk_law_derivations"] != 0
        or counts["unregistered_conditional_closure_theorems"] != 1
        or counts["controls"] != 19
        or counts["nonblock_controls"] != 3
        or counts["source_freedoms"] != 10
        or counts["boundary_rows"] != 7
        or counts["joins"] != 11
        or counts["sources"] != 20
        or counts["catch_proofs"] != 27
        or counts["complete_on_shell_g_phi_branches"] != 0
        or counts["q_second_jet_tidal_rank"] != 3
        or len(routes) != 12
        or len(universe) != 12
        or route_ids != [row["route_id"] for row in universe]
        or any(
            row["ruling"]
            in {"DERIVES_NATIVE_BULK_LAW", "DERIVES_CONDITIONAL_BULK_LAW"}
            for row in routes
        )
        or routes[9]["ruling"] != "NOT_AN_EXECUTABLE_EQUATION"
        or len(controls) != 19
        or len(nonblock) != 3
        or len(freedoms) != 10
        or len(boundaries) != 7
        or boundaries[-1]["J_amplitude"] != "FORCED_SQUARED_ONE"
        or boundaries[-1]["K_eff"]
        != "PINNED_BY_EXTRA_UNDERIVED_TENSOR_JOIN"
        or len(flows) != 4
        or [row["second_seal_condition_met"] for row in flows]
        != ["NO", "NO", "YES", "NO"]
        or [row["bulk_target"] for row in flows]
        != ["NO", "NO", "YES", "NO"]
        or len(joins) != 11
        or len(catches) != 27
        or len(statuses) != 10
        or len(lineage) != 20
        or any(row["status"] != "CAUGHT" for row in catches)
        or independent["status"] != "PASS"
        or independent["mutation_catches"] != 27
        or independent["q_second_jet_tidal_rank"] != 3
        or independent["conditional_two_seal_controls"] != 4
        or independent["source_hashes_replayed"] != 20
        or (tests["passed"], tests["failed"], tests["xfailed"])
        != (70, 0, 1)
        or "Grade: `VERIFIED-WITH-CAVEATS`" not in report
        or "Delta_K = K_eff_angular - K_rec" not in report
        or "CONDITIONAL_THEOREM_ON_AN_UNREGISTERED_PREMISE"
        not in report
    ):
        raise AssertionError("angular bulk-Jacobi science contract")
    return {
        "maximum_conclusion": MAXIMUM,
        "routes": len(routes),
        "native_bulk_law_derivations": 0,
        "conditional_bulk_law_derivations": 0,
        "unregistered_conditional_closure_theorems": 1,
        "q_second_jet_tidal_rank": 3,
        "smallest_missing_join": result["smallest_missing_join"],
        "complete_on_shell_g_phi_branches": 0,
        "source_files": len(lineage),
        "production_mutation_catches": len(catches),
        "independent_mutation_catches": independent["mutation_catches"],
        "grade": "VERIFIED-WITH-CAVEATS",
        "result": "PASS",
    }


def main() -> None:
    generic = load(
        ROOT
        / "bootstrap_csn_phi_angular_selector_2026-07-19"
        / "verify_repository_gates.py",
        "bulk_jacobi_generic_gates",
    )
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE

    scope = [
        path
        for path in generic.validate_scope(ROOT)
        if path != f"{PACKAGE}/REPOSITORY_GATES.json"
    ]
    frozen = generic.validate_frozen(ROOT)
    prior = replay_prior(generic)
    navigation = validate_navigation(generic)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    dirty.update(validate_dirty_head(generic))
    tests = load(
        ROOT
        / "hygiene_baseline_correction_2026-07-23"
        / "verify_repository_gates.py",
        "bulk_jacobi_hygiene_gates",
    ).validate_tests(generic)
    science = validate_science()
    package = validate_package(generic)
    catches = {
        "scope": generic.expect(
            "SCOPE", lambda: generic.validate_scope(ROOT, "LIVE.md")
        ),
        "frozen": generic.expect(
            "FROZEN", lambda: generic.validate_frozen(ROOT, True)
        ),
        "prior": generic.expect(
            "PRIOR", lambda: replay_prior(generic, True)
        ),
        "current_paths": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, "current"),
        ),
        "frontier": generic.expect(
            "NAVIGATION",
            lambda: generic.validate_navigation(ROOT, "frontier"),
        ),
        "dirty": generic.expect(
            "DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)
        ),
        "package": generic.expect(
            "PACKAGE", lambda: validate_package(generic, True)
        ),
    }
    output = {
        "schema": "udt-angular-bulk-jacobi-repository-gates-1.0",
        "result": "PASS",
        "base": BASE,
        "scope_paths": scope,
        "science": science,
        "frozen": frozen,
        "prior_scientific_packages": prior,
        "navigation": navigation,
        "dirty_checkout": dirty,
        "tests": tests,
        "package_manifest": package,
        "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False},
        "authority_boundary": MAXIMUM,
    }
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
