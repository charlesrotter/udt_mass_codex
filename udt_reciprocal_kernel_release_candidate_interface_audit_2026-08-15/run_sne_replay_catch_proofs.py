#!/usr/bin/env python3
"""Exercise scope/consistency guards; this is not a numerical tamper harness."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile

from verify_sne_replay_package import build_checks


HERE = Path(__file__).resolve().parent


def copy_required(destination: Path) -> None:
    for path in HERE.iterdir():
        if path.is_file():
            shutil.copy2(path, destination / path.name)


def main() -> None:
    catches: dict[str, bool] = {}
    with tempfile.TemporaryDirectory(prefix="udt_sne_replay_catch_") as tmp:
        root = Path(tmp)
        copy_required(root)
        result_path = root / "SNE_COMPLETE_GEOMETRY_RESULT.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        result["authority"]["shape_parameter_fitted"] = True
        result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        catches["fitted_geometry_shape"] = not build_checks(root)["shape_not_fitted"]

    with tempfile.TemporaryDirectory(prefix="udt_sne_replay_catch_") as tmp:
        root = Path(tmp)
        copy_required(root)
        result_path = root / "SNE_COMPLETE_GEOMETRY_RESULT.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        result["authority"]["native_radiative_law_derived"] = True
        result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        catches["transfer_promotion"] = not build_checks(root)["native_transfer_open"]

    with tempfile.TemporaryDirectory(prefix="udt_sne_replay_catch_") as tmp:
        root = Path(tmp)
        copy_required(root)
        result_path = root / "SNE_COMPLETE_GEOMETRY_RESULT.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        result["provisional_transfer"]["eta"] = None
        result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        catches["eta_premise_removed"] = not build_checks(root)["eta_provisional"]

    with tempfile.TemporaryDirectory(prefix="udt_sne_replay_catch_") as tmp:
        root = Path(tmp)
        copy_required(root)
        result_path = root / "SNE_COMPLETE_GEOMETRY_RESULT.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        result["provisional_transfer"]["epsilon"] = "UNSUPPLIED"
        result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        catches["epsilon_premise_removed"] = not build_checks(root)["epsilon_provisional"]

    with tempfile.TemporaryDirectory(prefix="udt_sne_replay_catch_") as tmp:
        root = Path(tmp)
        copy_required(root)
        report = root / "SNE_REPLAY_REPORT.md"
        report.write_text(report.read_text(encoding="utf-8").replace("STRONGLY_INCOMPATIBLE", "GOOD_FIT"), encoding="utf-8")
        catches["bad_fit_erasure"] = not build_checks(root)["bad_fit_recorded"]

    with tempfile.TemporaryDirectory(prefix="udt_sne_replay_catch_") as tmp:
        root = Path(tmp)
        copy_required(root)
        (root / "SNE_REPLAY_PREREGISTRATION.md").unlink()
        catches["missing_preregistration"] = not build_checks(root)["exists:SNE_REPLAY_PREREGISTRATION.md"]

    output = {
        "verifier_role": "scope_and_metadata_consistency_guards_not_independent_numerical_evidence",
        "catches": catches,
        "all_pass": all(catches.values()),
    }
    (HERE / "SNE_REPLAY_CATCH_PROOF.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    if not output["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
