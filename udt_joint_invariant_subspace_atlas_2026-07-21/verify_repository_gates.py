#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "e237b589d7604426df0a19e1362e2e77387834a2"
PACKAGE = "udt_joint_invariant_subspace_atlas_2026-07-21"
PARENT = ROOT / "udt_chart_coframe_invariance_atlas_2026-07-21"
PARENT_MANIFEST = "082c41bea96e99611d3fc89a135692058e346665b4b1520d7f6d790788a0cf09"
DIRTY = Path("/home/udt-admin/udt_mass_codex")
MAXIMUM = "BOUNDED_POINTWISE_JOINT_INVARIANT_SUBSPACE_ATLAS_CHARACTERIZED"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate_navigation(generic, corrupt: str | None = None) -> dict[str,int]:
    current=tsv(ROOT/"research/_registry/CURRENT_ARTIFACT_PATHS.tsv");current_paths=[row["current_path"] for row in current]
    if corrupt=="current":current_paths=current_paths[:-1]
    if len(current)!=1114 or len(current_paths)!=1114 or len(set(current_paths))!=1114:
        raise generic.GateError("NAVIGATION","current-count")
    if not all((ROOT/path).exists() for path in current_paths):
        raise generic.GateError("NAVIGATION","current-target")
    frontier=tsv(ROOT/"research/_registry/CURRENT_FRONTIER_TARGETS.tsv");targets={row["target_path"].rstrip("/") for row in frontier}
    if corrupt=="frontier":targets.pop()
    if len(frontier)!=306 or len(targets)!=101:
        raise generic.GateError("NAVIGATION","frontier-count")
    if not all((ROOT/path).exists() for path in targets):
        raise generic.GateError("NAVIGATION","frontier-target")
    pattern=re.compile(r"\[[^\]]+\]\(([^)]+)\)");links=[]
    for source in sorted(HERE.glob("*.md")):
        for raw in pattern.findall(source.read_text(encoding="utf-8")):
            target=raw.strip().strip("<>")
            if target.startswith(("http://","https://","mailto:","#")):continue
            target=unquote(target.split("#",1)[0]);path=source.parent.joinpath(target).resolve()
            if not path.exists() and re.search(r":\d+$",str(path)):
                path=Path(re.sub(r":\d+$","",str(path)))
            links.append(path)
    if not all(path.exists() for path in links):
        raise generic.GateError("NAVIGATION","markdown-link")
    return {"current_paths":len(current),"frontier_rows":len(frontier),"frontier_targets":len(targets),"package_links":len(links)}


def scope(generic, inject: str | None = None) -> list[str]:
    changed = set(str(generic.git(ROOT, "diff", "--name-only", BASE)).splitlines())
    changed.update(str(generic.git(ROOT, "ls-files", "--others", "--exclude-standard")).splitlines())
    if inject:
        changed.add(inject)
    bad = sorted(path for path in changed if path and not path.startswith(PACKAGE + "/"))
    if bad:
        raise generic.GateError("SCOPE", bad[0])
    return sorted(
        path for path in changed
        if path != f"{PACKAGE}/REPOSITORY_GATES.json" and "__pycache__" not in path and not path.endswith(".pyc")
    )


def scientific_verification() -> dict[str, object]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    main = subprocess.run(
        [sys.executable, "-B", str(HERE / "build_joint_atlas.py")], cwd=ROOT, env=env,
        text=True, capture_output=True, timeout=1800, check=False,
    )
    if main.returncode or main.stderr:
        raise AssertionError(main.stdout + main.stderr)
    independent = subprocess.run(
        [sys.executable, "-B", str(HERE / "verify_joint_atlas.py")], cwd=ROOT, env=env,
        text=True, capture_output=True, timeout=600, check=False,
    )
    if independent.returncode or independent.stderr:
        raise AssertionError(independent.stdout + independent.stderr)
    result = json.loads((HERE / "ATLAS_RESULT.json").read_text(encoding="utf-8"))
    verify = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    margins = tsv(HERE / "NUMERIC_MARGIN_LEDGER.tsv")
    catches = tsv(HERE / "CATCH_PROOFS.tsv")
    if (
        result["status"] != "PASS" or result["maximum_conclusion"] != MAXIMUM
        or result["configurations"] != 6144 or result["family_rows"] != 55296
        or result["nonlinear_configuration_rows"] != 12288 or result["nonlinear_family_rows"] != 110592
        or result["unique_central_2plus2_rows"] != 11983 or result["multiple_central_2plus2_rows"] != 2225
        or result["gradient_generated_plane_rows"] != 0 or result["unique_bivector_complementary_split_rows"] != 0
        or result["nonlinear_classification_discordances"] != 0 or result["nonlinear_uncertain_comparisons"] != 24
        or result["discarded_rows"] != 0 or len(margins) != 24
        or result["supplied_split_loaded"] is not False or result["action_or_equation_loaded"] is not False
        or result["physical_split_selected"] is not False or result["global_distribution_claimed"] is not False
        or result["full_group_claimed"] is not False or result["gpu_used"] is not False
        or verify["status"] != "PASS" or verify["anchors"] != 480 or verify["nonlinear_anchors"] != 960
        or verify["family_classifications"] != 12960 or verify["anchor_uncertain_comparisons"] != 4
        or verify["catch_proofs"] != 10 or len(catches) != 10
        or any(row["result"] != "REJECTED_AS_REQUIRED" for row in catches)
    ):
        raise AssertionError("scientific verification")
    if digest(HERE / "PRECORRECTION_ATLAS_RESULT.json") != "bf73dbdfd12c9b07bd167725c0f9086bdd9f9539b3c034793a4fca2ff5d6a93e":
        raise AssertionError("precorrection result changed")
    if digest(HERE / "PRECORRECTION_ATLAS_TRANSCRIPT.txt") != "975299fabd703fd34e6461c96c0502a8d63634250188f800a9ff4a822e3d07ef":
        raise AssertionError("precorrection transcript changed")
    preserved = {
        "PRE_REAL_SPECTRAL_CORRECTION_ATLAS_RESULT.json": "2d87656d1cb62e51e35ee5203d11189ce44773a7b31fa7114c97b036378c7cbc",
        "PRE_REAL_SPECTRAL_CORRECTION_ATLAS_TRANSCRIPT.txt": "efb8d2c0642ce80d149d55187cf3525cee0ec78d31a36afaeebeeae7d44f8bfc",
        "PRE_REAL_SPECTRAL_CORRECTION_FAMILY_CLASS_CENSUS.tsv": "845bfd3cd5c18175085fc33f43fafaec2ee9d8fa06417224d26f4da137f6d82b",
        "PRE_REAL_SPECTRAL_CORRECTION_VERIFICATION_RESULT.json": "ba96cf770d96ce606f3ffbf678422d2c8097b5d2ecf4cfca9423ead13b82fb66",
        "FRESH_ADVERSARIAL_REVIEW.md": "c4a4b5734d5ae04cf53ba7461889d80daf74d295503fa587819e5d8a54f8ba61",
        "FRESH_ADVERSARIAL_REVIEW_TRANSCRIPT.txt": "f2a53ab5228a90b7c8cadaa574f40bb135f16bf741e29a9c1b265a5cbc8b4277",
        "FRESH_ADVERSARIAL_CORRECTION_REVIEW.md": "e84f326340a94ce9598f46dc485459d82ce9c64f4aa7e673757060763c1c9c05",
        "FRESH_ADVERSARIAL_CORRECTION_REVIEW_TRANSCRIPT.txt": "6b6c2f945754b8232e953bf064aad1d3d6b18a71f4c384bf75520a1c8c9bcef5",
        "JORDAN_FAIL_CLOSURE_CORRECTION.md": "5ea4d6f3e403f2782089c0e1a05718fb665670112caf1aee0fb65308ec46f7a7",
        "PRE_JORDAN_FAIL_CLOSURE_ATLAS_RESULT.json": "0d05664c6c9a139b234ae7a6316988351a52ef7854ef1b089b4d9f15619d8e8d",
        "PRE_JORDAN_FAIL_CLOSURE_ATLAS_TRANSCRIPT.txt": "1dac58d65e5b976fdf6c56ab38c4277605acd555026e1bcb87787c8ea517857b",
        "PRE_JORDAN_FAIL_CLOSURE_CATCH_PROOFS.tsv": "f82504da9197e28c8174ce70960b8edb6d720f1894e81097e719d8063102d978",
        "PRE_JORDAN_FAIL_CLOSURE_REPOSITORY_GATES.json": "a711c674a04a5bc659113f0f5850bce4f0a6490795e6e06c1fedd627d878a929",
        "PRE_JORDAN_FAIL_CLOSURE_SHA256SUMS.txt": "7ab1b2b77e098c1d692e5dec018409f69b6a83e5797486c872583da445cfbff6",
        "PRE_JORDAN_FAIL_CLOSURE_VERIFICATION_RESULT.json": "823dac5a942b5514b1b8793f7e73e7903766e7c95a3ce9b7b9799db5fa1d7bf3",
        "PRE_JORDAN_FAIL_CLOSURE_VERIFICATION_TRANSCRIPT.txt": "7ad8ffac24b28fdfa1207f1873d477f789bd00b081f4aed766e47dde1486ea6a",
        "FRESH_ADVERSARIAL_FINAL_REQUEST.md": "aff5ae9ae2a69a3286300eac13c7fc7e99fa502c0ed670eeda58ed1d035bd3d9",
        "FRESH_ADVERSARIAL_FINAL_REVIEW.md": "59e992665968ecc5e0a3b811488dc02dfa2295032a0c031ee3232d1cb38f786f",
        "FRESH_ADVERSARIAL_FINAL_REVIEW_TRANSCRIPT.txt": "d3ec743c4480b893ec71048a30a11edbb1c08f53779e3ea453bd45d86afabe1b",
        "BIVECTOR_TOLERANCE_CORRECTION.md": "da0d111cd8ebc650c1be88a5a12acbd9eb53b0d74d0812fb7661646d41885c4a",
        "FRESH_ADVERSARIAL_POST_TOLERANCE_REQUEST.md": "6b9e233be95054cd4dd72191bbc0da0a1172b7a59b17d02b611bfe3fd98ddb96",
        "FRESH_ADVERSARIAL_POST_TOLERANCE_REVIEW.md": "476e27ccb6c678f7d298d18b0409e5e1c945b4f7a1a1443d044cc670644c418b",
        "FRESH_ADVERSARIAL_POST_TOLERANCE_REVIEW_TRANSCRIPT.txt": "5b3a1de391d5e474bee07202c903aede551a1698438c3eb32ef81c15195ad61a",
    }
    if any(digest(HERE / name) != expected for name, expected in preserved.items()):
        raise AssertionError("real-spectral correction history changed")
    escalation = tsv(HERE / "UNIQUE_SPLIT_ESCALATION_CENSUS.tsv")
    if {(row["source_family"], row["full_riemann_joint_class"], row["full_weyl_joint_class"], int(row["configurations"])) for row in escalation} != {
        ("F01_RICCI", "FULL_MATRIX_ALGEBRA_IRREDUCIBLE", "FULL_MATRIX_ALGEBRA_IRREDUCIBLE", 4298),
        ("F02_PHI_HESSIAN", "FULL_MATRIX_ALGEBRA_IRREDUCIBLE", "FULL_MATRIX_ALGEBRA_IRREDUCIBLE", 3003),
        ("F04_RICCI_HESSIAN", "FULL_MATRIX_ALGEBRA_IRREDUCIBLE", "FULL_MATRIX_ALGEBRA_IRREDUCIBLE", 2533),
        ("F05_RICCI_HESSIAN_DYAD", "FULL_MATRIX_ALGEBRA_IRREDUCIBLE", "FULL_MATRIX_ALGEBRA_IRREDUCIBLE", 2149),
    }:
        raise AssertionError("unique-split escalation census")
    return {
        "status": "PASS", "configurations": result["configurations"], "family_rows": result["family_rows"],
        "nonlinear_family_rows": result["nonlinear_family_rows"], "independent_anchors": verify["anchors"],
        "independent_nonlinear_anchors": verify["nonlinear_anchors"],
        "independent_family_classifications": verify["family_classifications"],
        "catch_proofs": verify["catch_proofs"], "uncertain_comparisons": len(margins),
        "main_result_sha256": digest(HERE / "ATLAS_RESULT.json"),
        "verification_result_sha256": digest(HERE / "VERIFICATION_RESULT.json"),
        "margin_ledger_sha256": digest(HERE / "NUMERIC_MARGIN_LEDGER.tsv"),
        "maximum_conclusion": result["maximum_conclusion"],
    }


def source_immutability() -> dict[str, object]:
    observed = {}
    for row in tsv(HERE / "SOURCE_LINEAGE.tsv"):
        relative, expected, role = row["path"], row["sha256"], row["role"]
        path = HERE / relative if role == "PREREGISTRATION" else ROOT / relative
        if digest(path) != expected:
            raise AssertionError(f"source hash {relative}")
        if role == "IMMUTABLE_SOURCE" and subprocess.run(
            ["git", "diff", "--quiet", BASE, "--", relative], cwd=ROOT, check=False
        ).returncode:
            raise AssertionError(f"source changed {relative}")
        observed[relative] = expected
    if len(observed) != 5:
        raise AssertionError("source count")
    return {"status": "PASS", "count": len(observed), "sources": observed}


def prior_packages() -> dict[str, str]:
    record = json.loads((PARENT / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    prior = {row["package"]: row["manifest_sha256"] for row in record["prior_scientific_packages"]["packages"]}
    prior[PARENT.name] = PARENT_MANIFEST
    return prior


def validate_package_manifest(generic, corrupt: bool = False) -> dict[str, object]:
    manifest = HERE / "SHA256SUMS.txt"
    replay = subprocess.run(
        ["sha256sum", "--check", manifest.name], cwd=HERE,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False,
    )
    if corrupt or replay.returncode or "FAILED" in replay.stdout:
        raise generic.GateError("PACKAGE", "hash-replay")
    entries = [line.split("  ", 1)[1] for line in manifest.read_text(encoding="utf-8").splitlines() if line]
    excluded = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    actual = sorted(
        path.relative_to(HERE).as_posix() for path in HERE.rglob("*")
        if path.is_file() and path.relative_to(HERE).as_posix() not in excluded
        and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )
    if sorted(entries) != actual or len(entries) != len(set(entries)):
        raise generic.GateError("PACKAGE", "recursive coverage")
    return {"entries": len(entries), "sha256": digest(manifest), "result": "PASS"}


def main() -> None:
    generic = load(ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/verify_repository_gates.py", "joint_generic")
    generic.BASE = BASE
    generic.PACKAGE = PACKAGE
    changed = scope(generic)
    scientific = scientific_verification()
    sources = source_immutability()
    frozen = generic.validate_frozen(ROOT)
    prior = prior_packages()
    replay = generic.replay_packages(ROOT, prior, "PRIOR")
    if len(prior) != 67 or replay["entries"] != 1731:
        raise generic.GateError("PRIOR", f"{len(prior)}:{replay['entries']}")
    navigation = validate_navigation(generic)
    dirty = generic.validate_dirty(ROOT, DIRTY)
    tests = generic.validate_tests(ROOT)
    tests.pop("stdout_sha256", None)
    signature = f"{tests['passed']}|{tests['failed']}|{tests['xfailed']}|{tests['failure']}"
    tests["result_signature_sha256"] = hashlib.sha256(signature.encode()).hexdigest()
    package = validate_package_manifest(generic)
    catches = {
        "scope": generic.expect("SCOPE", lambda: scope(generic, "LIVE.md")),
        "frozen": generic.expect("FROZEN", lambda: generic.validate_frozen(ROOT, True)),
        "prior": generic.expect("PRIOR", lambda: generic.replay_packages(ROOT, prior, "PRIOR", True)),
        "current": generic.expect("NAVIGATION", lambda: validate_navigation(generic, "current")),
        "frontier": generic.expect("NAVIGATION", lambda: validate_navigation(generic, "frontier")),
        "dirty": generic.expect("DIRTY", lambda: generic.validate_dirty(ROOT, DIRTY, True)),
        "package": generic.expect("PACKAGE", lambda: validate_package_manifest(generic, True)),
    }
    output = {
        "schema": "udt-joint-invariant-subspace-atlas-repository-gates-1.0", "base": BASE, "result": "PASS",
        "scope_paths": changed, "scientific_verifier": scientific, "source_immutability": sources,
        "frozen": frozen, "prior_scientific_packages": replay, "navigation": navigation,
        "dirty_checkout": dirty, "tests": tests, "package_manifest": package, "catch_proofs": catches,
        "compute": {"cpu_only": True, "gpu_work_performed": False, "ODE_or_PDE_run": False},
        "authority_boundary": {
            "startup_controls_changed": False, "canon_changed": False, "action_or_equations_loaded": False,
            "physical_interaction_claimed": False, "physical_split_selected": False,
            "physics_ranked": False, "physical_evolution_launched": False,
            "boundary_topology_or_scale_selected": False, "carrier_or_matter_adopted": False,
            "repository_reorganization_performed": False,
        },
    }
    (HERE / "REPOSITORY_GATES.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("repository_gates=PASS")
    print(f"scientific={scientific['configurations']} configurations/{scientific['independent_family_classifications']} independent classifications/{scientific['catch_proofs']} catches")
    print(f"sources={sources['count']} frozen_manifests=6 entries={frozen['entries']} paths={frozen['tracked_paths']}")
    print(f"prior_packages={len(prior)} entries={replay['entries']}")
    print(f"tests={tests['passed']} passed/{tests['failed']} known failed/{tests['xfailed']} xfailed")
    print(f"dirty_metadata_paths={dirty['paths']} hash={dirty['metadata_sha256']}")
    print(f"package_manifest={package['sha256']} entries={package['entries']}")


if __name__ == "__main__":
    main()
