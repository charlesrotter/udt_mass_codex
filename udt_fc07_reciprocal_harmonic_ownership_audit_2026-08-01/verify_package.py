#!/usr/bin/env python3
"""Verify final package identity and load-bearing gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}
MAXIMUM = (
    "FOUR_UNIQUE_H1_FC07_COMPLETIONS_HAVE_EXACT_RECIPROCAL_HARMONIC_LINE_OWNERSHIP_FOR_ARBITRARY_"
    "SMOOTH_FINITE_DESCENDING_PHI_AND_EVERY_DESCENDING_MEMBER_OF_A_BOUNDED_LOWER_TRIANGULAR_"
    "PAIR_SCREEN_MIXING_CLASS_CONTAINING_THE_REGISTERED_E02_MEMBERS__ANGULAR_AREA_MODULATES_THE_"
    "LOCAL_HARMONIC_AMPLITUDE_THROUGH_A_"
    "COMPLETE_CELL_NORMALIZATION__THE_UNRESCALED_RULER_IS_HARMONIC_IFF_ANGULAR_AREA_IS_CONSTANT__"
    "NO_NONTRIVIAL_BACKGROUND_CURVATURE_WINDOW_NATIVE_RETURN_EQUATION_DENSITY_BRIDGE_XMAX_OR_MATTER"
)


def main() -> int:
    manifest = {}
    for line in (HERE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        expected, name = line.split(None, 1)
        name = name.strip()
        path = HERE / name
        assert name not in manifest and path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
        manifest[name] = expected
    actual = {p.name for p in HERE.iterdir() if p.is_file() and p.name not in EXCLUDE}
    assert set(manifest) == actual

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    gates = json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    assert verification["status"] == gates["status"] == "PASS"
    assert derivation["all_checks_pass"] and independent["all_checks_pass"]
    assert derivation["checks"] == verification["production_checks"] == 45
    assert independent["checks"] == verification["independent_checks"] == 68
    assert verification["semantic_mutations"] == verification["semantic_mutations_caught"] == 20
    assert verification["source_identities"] == 16 and verification["source_anchors"] == 13
    assert derivation["maximum_conclusion"] == verification["maximum_conclusion"] == MAXIMUM
    for field in (
        "nontrivial_background_window_derived", "native_return_equation_derived",
        "density_curvature_bridge_derived", "physical_completion_selected",
        "matter_or_source_derived", "mixing_descent_law_derived",
    ):
        assert derivation[field] is False
    result = {
        "schema": "udt.fc07.reciprocal_harmonic_ownership.package.v1",
        "status": "PASS",
        "manifest_files": len(manifest),
        "manifest_sha256": hashlib.sha256(
            (HERE / "PACKAGE_MANIFEST.sha256").read_bytes()
        ).hexdigest(),
        "scientific_grade": "VERIFIED_WITH_CAVEATS",
        "maximum_conclusion": MAXIMUM,
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
