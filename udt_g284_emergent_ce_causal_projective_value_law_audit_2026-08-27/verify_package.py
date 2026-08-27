#!/usr/bin/env python3
"""Fail-closed internal package verifier for G284."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LANDING = (
    "EMERGENT_CE_CAUSAL_PROJECTIVE_NETWORK_RECONSTRUCTS_BUT_DOES_NOT_SELECT_"
    "TIDAL_HISTORY"
)


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run_replays(
    manifest_rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], bool]:
    """Execute the four registered computations in an exact ephemeral source copy."""

    expected = (
        ("verify_preregistration.py", "PASS: G284 preregistration"),
        ("derive_causal_projective.py", '"status": "PASS"'),
        ("verify_independent.py", '"status": "PASS"'),
        ("run_catch_proofs.py", '"status": "PASS"'),
    )
    records: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="g284_package_replay_") as temporary:
        replay_root = Path(temporary)
        replay_package = replay_root / PACKAGE.name
        shutil.copytree(PACKAGE, replay_package)
        for row in manifest_rows:
            source = ROOT / row["path"]
            target = replay_root / row["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        for script, expected_token in expected:
            command = [sys.executable, "-S", str(replay_package / script)]
            completed = subprocess.run(
                command,
                cwd=replay_root,
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
            token_found = expected_token in completed.stdout
            records.append(
                {
                    "script": script,
                    "interpreter_mode": "python_-S_no_site_packages",
                    "exit_code": completed.returncode,
                    "expected_token_found": token_found,
                }
            )
            if completed.returncode != 0 or not token_found:
                raise AssertionError(
                    {
                        "failed_replay": script,
                        "exit_code": completed.returncode,
                        "expected_token_found": token_found,
                        "stdout_tail": completed.stdout[-1000:],
                        "stderr_tail": completed.stderr[-1000:],
                    }
                )

        # Artifact-level hostile catch: a broken registered derivation in the
        # disposable copy must fail the same runner that certified the baseline.
        mutant = replay_package / "derive_causal_projective.py"
        text = mutant.read_text(encoding="utf-8")
        needle = "def main() -> None:\n"
        if needle not in text:
            raise AssertionError("mutation anchor absent")
        mutant.write_text(
            text.replace(needle, needle + '    raise SystemExit("hostile replay mutation")\n', 1),
            encoding="utf-8",
        )
        broken = subprocess.run(
            [sys.executable, "-S", str(mutant)],
            cwd=replay_root,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        mutation_caught = broken.returncode != 0 and '"status": "PASS"' not in broken.stdout
        if not mutation_caught:
            raise AssertionError("broken registered replay was not caught")
    return records, mutation_caught


def main() -> None:
    source_scope = rows("SOURCE_SCOPE.tsv")
    manifest_rows = rows("SOURCE_MANIFEST.tsv")
    manifest = {row["path"]: row for row in manifest_rows}
    premises = rows("PREMISE_LEDGER.tsv")
    status_rows = rows("STATUS_LEDGER.tsv")
    status = {row["id"]: row for row in status_rows}
    replay_records, broken_replay_mutation_caught = run_replays(manifest_rows)
    derivation = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((PACKAGE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    audit = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    required = (
        "MAP.md",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_SCOPE.tsv",
        "SOURCE_MANIFEST.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "COMMANDS.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "VERIFICATION_RESULT.json",
        "verify_preregistration.py",
        "derive_causal_projective.py",
        "derive_causal_projective_sympy.py",
        "verify_independent.py",
        "run_catch_proofs.py",
        "verify_package.py",
        "EXTERNAL_REVIEW_GPT54.md",
        "EXTERNAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_TRANSMISSION.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_RESULT.json",
        "EXTERNAL_REPAIR_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md",
        "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md",
        "build_repair_followup_intake.py",
    )
    protected = (
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
    )
    checks = {
        "all_required_files_present": all((PACKAGE / name).is_file() for name in required),
        "source_count_15": len(source_scope) == len(manifest_rows) == 15,
        "source_scope_manifest_exact": {row["path"] for row in source_scope} == set(manifest),
        "all_source_hashes_and_sizes_exact": all(
            (ROOT / path).is_file()
            and sha256(ROOT / path) == manifest[path]["sha256"]
            and str((ROOT / path).stat().st_size) == manifest[path]["bytes"]
            for path in manifest
        ),
        "protected_sources_excluded": not any(
            fragment in path for fragment in protected for path in manifest
        ),
        "premise_rows_16": len(premises) == 16,
        "status_rows_10": len(status_rows) == 10,
        "external_review_and_repairs_confirmed": status["S10"]["status"]
        == "PASS_ACCEPTED_REPAIRS_CONFIRMED",
        "registered_replays_4_of_4": (
            len(replay_records) == 4
            and all(record["exit_code"] == 0 for record in replay_records)
            and all(record["expected_token_found"] for record in replay_records)
        ),
        "registered_replays_use_no_site_packages": all(
            record["interpreter_mode"] == "python_-S_no_site_packages"
            for record in replay_records
        ),
        "broken_registered_replay_mutation_caught": broken_replay_mutation_caught,
        "derivation_20_of_20": (
            derivation["status"] == "PASS"
            and derivation["landing"] == LANDING
            and derivation["exact_checks"] == len(derivation["checks"]) == 20
            and all(derivation["checks"].values())
        ),
        "three_arbitrary_tidal_functions_retained": len(
            derivation["arbitrary_tidal_functions_retained"]
        )
        == 3,
        "no_value_selecting_constraint_found": derivation["value_selecting_constraints_found"]
        == 0,
        "independent_512_cases_7168_assertions": (
            independent["status"] == "PASS"
            and independent["exact_cases"] == 512
            and independent["exact_assertions"] == 7168
            and independent["network_cases"] == 64
            and independent["different_area_cases"] == 64
            and all(independent["checks"].values())
        ),
        "claim_schema_catches_9_of_9": (
            catches["status"] == "PASS"
            and catches["caught_count"] == catches["mutation_count"] == 9
            and catches["certification_scope"]
            == "in_memory_boolean_claim_schema_only__not_artifact_level_mutation_replay"
            and all(catches["caught"].values())
        ),
        "landing_exact_and_externally_accepted": (
            verification["status"] == "PASS_EXTERNAL_REVIEW_COMPLETE"
            and verification["landing"] == LANDING
            and verification["external_review"] == "ACCEPTED_REPAIRS_CONFIRMED"
            and "R1_R2_EXTERNALLY_CONFIRMED" in verification["grade"]
            and LANDING in audit
        ),
        "causal_tape_type_stated_without_formula_promotion": (
            "curvature of the causal tape" in exact
            and "G284 derives its mathematical type but not its formula" in exact
        ),
        "stronger_premises_not_imported": all(
            token in exact
            for token in (
                "endpoint-only or path-independent tape law",
                "zero holonomy or all-germ isotropy",
                "none follows from the\ntested conjunction",
            )
        ),
        "no_imports_or_outcomes": not any(derivation["imports"].values()),
    }
    if not all(checks.values()):
        raise AssertionError({name: value for name, value in checks.items() if not value})
    print(
        json.dumps(
            {
                "audit": "G284_PACKAGE_AND_EXECUTABLE_REPLAY_VERIFICATION",
                "status": "PASS_EXTERNAL_REVIEW_COMPLETE",
                "landing": LANDING,
                "counts": verification["counts"],
                "replay_commands": replay_records,
                "broken_replay_mutation_caught": broken_replay_mutation_caught,
                "checks": checks,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
