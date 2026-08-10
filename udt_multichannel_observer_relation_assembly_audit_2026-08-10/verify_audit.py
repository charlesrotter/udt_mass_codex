#!/usr/bin/env python3
"""Fail-closed verification of the multi-channel observer-relation assembly audit."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PREREG_COMMIT = "08c0838e"
EXPECTED_BASE = "3330601b9fd04adc9a9f78e13e5756bd868ba146"
EXTERNAL_SHA256 = "ddb5952742dc050f70d14fccfb6fe5550525dee8a64508ce73647053e6008865"
TRANSCRIPT_SHA256 = "01ec9e11434103d085e43236585bcf9d7462a223970a3ec5e37ba7a3f8e7e415"
PREREG_FILES = (
    "PREREGISTRATION.md",
    "PONDER_MAP.md",
    "PREMISE_LEDGER.tsv",
    "CHANNEL_UNIVERSE.tsv",
    "EQUIVALENCE_CONTRACT.tsv",
    "REGIME_AXIS.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "SOURCE_MANIFEST.tsv",
    "verify_preregistration.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    base = subprocess.check_output(
        ["git", "rev-parse", f"{PREREG_COMMIT}^"], cwd=ROOT, text=True
    ).strip()
    require(base == EXPECTED_BASE, "preregistration base changed")
    for name in PREREG_FILES:
        relative = f"{HERE.name}/{name}"
        result = subprocess.run(
            ["git", "diff", "--quiet", PREREG_COMMIT, "--", relative], cwd=ROOT, check=False
        )
        require(result.returncode == 0, f"preregistered file changed: {name}")

    sources = table(HERE / "SOURCE_MANIFEST.tsv")
    require(len(sources) == 19, "source manifest must contain exactly 19 rows")
    require([row["source_id"] for row in sources] == [f"S{i:02d}" for i in range(1, 20)],
            "source ids changed")
    for row in sources:
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        require(len(data) == int(row["size"]), f"source size changed: {row['path']}")
        require(hashlib.sha256(data).hexdigest() == row["sha256"],
                f"source hash changed: {row['path']}")
        blob = subprocess.check_output(
            ["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True
        ).strip()
        require(blob == row["git_blob"], f"source blob changed: {row['path']}")

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8")
    )
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    require(result["status"] == "PASS" and result["passed"] == result["total"] == 23,
            "production derivation is not 23/23 PASS")
    require(independent["status"] == "PASS" and independent["passed"] == independent["total"] == 27,
            "independent verification is not 27/27 PASS")
    require(catches["status"] == "PASS" and catches["rejected"] == catches["total"] == 21,
            "catch proofs are not 21/21 PASS")

    require(result["pair_metric_coordinates"] == "UNIQUE_TRIPLE_kappa_phi_beta",
            "pair-metric coordinate result changed")
    require(result["matched_arrow_characters"] == "Delta_kappa_and_Delta_phi",
            "matched density characters changed")
    require(result["path_arrow"] == "U_gamma_IN_ORIENTED_NORMAL_ISOMETRY_GROUPOID",
            "angular path arrow changed")
    require("DECLARED_PAIR_MAP_CURVE" in result["minimal_banked_assembly"],
            "common query/path scope lost")
    require(result["physical_regime_map"] is None, "physical regimes were assigned")
    require(result["conductor_owner"] is None, "a conductor was invented")
    require(result["observational_calibration"]["c_E"] == "ACTIVE_PAIR_TAPE_CALIBRATION_ONLY",
            "c_E was promoted to a selector")
    require(result["observational_calibration"]["G_obs"] == "INACTIVE_WITHOUT_NATIVE_MASS_READOUT",
            "G_obs was activated without a mass readout")
    require(result["observational_calibration"]["m_e"] == "UNAPPLIED_FUTURE_CALIBRATION_CANDIDATE",
            "electron mass was activated")
    require(result["observational_calibration"]["hbar"] == "EXCLUDED", "hbar was imported")

    require(len(table(HERE / "CHANNEL_CLASSIFICATION.tsv")) == 16, "channel census changed")
    require(len(table(HERE / "ASSEMBLED_CHANNELS.tsv")) == 6, "assembly census changed")
    require(len(table(HERE / "GEOMETRIC_REGIME_ATLAS.tsv")) == 10, "regime census changed")
    require(all(row["physical_regime"].startswith("OPEN")
                for row in table(HERE / "GEOMETRIC_REGIME_ATLAS.tsv")),
            "geometric strata received physical labels")

    require(digest(HERE / "EXTERNAL_REVIEW_RAW.md") == EXTERNAL_SHA256,
            "external raw review hash changed")
    transcript = gzip.decompress((HERE / "EXTERNAL_REVIEW_TRANSCRIPT.log.gz").read_bytes())
    require(hashlib.sha256(transcript).hexdigest() == TRANSCRIPT_SHA256,
            "external transcript hash changed after lossless decompression")
    external = (HERE / "EXTERNAL_REVIEW.md").read_text(encoding="utf-8")
    require("CONDITIONAL_MULTICHANNEL_ASSEMBLY_ONLY" in external, "external grade missing")
    require("ordered observer-query / measurement-projection" in external,
            "smallest remaining owner missing")
    require("not a selected physical observer-relation theorem" in external,
            "conditional scope correction missing")

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    for text, name in ((report, "report"), (exact, "exact derivation")):
        flat = " ".join(text.split())
        require("supplied calibrated pair" in flat, f"supplied-pair scope missing: {name}")
        require(
            "physical observer arrow" in flat or "complete observer arrow" in flat,
            f"physical-arrow boundary missing: {name}",
        )
        require(
            "physical regime" in flat or "activity stratum" in flat,
            f"physical-regime boundary missing: {name}",
        )
    forbidden = (
        "COMPLETE_PHYSICAL_OBSERVER_ARROW_DERIVED",
        "PHYSICAL_REGIME_MAP_DERIVED",
        "UNIVERSAL_C_EFF_DERIVED",
        "NATIVE_ACTION_DERIVED",
        "BOOTSTRAP_CLOSED",
    )
    corpus = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in HERE.iterdir() if path.is_file() and path.suffix in {".md", ".tsv", ".json"}
    )
    for token in forbidden:
        require(token not in corpus, f"forbidden downstream promotion: {token}")

    print(
        "PASS: preregistration immutable; 19/19 sources pinned; production 23/23; "
        "independent 27/27; catches 21/21; external grade conditional-multichannel-only; "
        "query projection, path, regime map, conductor, and downstream physics remain open"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
