#!/usr/bin/env python3
"""Verify package identity and final FC07 Cartan/response gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}
MAXIMUM = (
    "FC07_FULL_SCREEN_CARTAN_AND_CURVATURE_DERIVED__ALL_NONCONSTANT_REGISTERED_INTERPOLATIONS_HAVE_"
    "NONZERO_BUNDLE_RELATIVE_PROJECTOR_RESPONSE__THREE_VARYING_UNIQUE_H1_CLASSES_HAVE_A_METRIC_"
    "INTRINSIC_GLOBAL_HARMONIC_RULER_CHANNEL__ONE_FORCED_HYPERBOLIC_INSTANCE__THREE_CONSTANT_"
    "SUBFAMILIES_HAVE_A_HOLONOMY_FIXED_RECIPROCAL_PLANE_WITHOUT_SELECTED_AXES__NO_UNIVERSAL_"
    "PROJECTOR_BOOTSTRAP_CLOSURE_XMAX_SELECTION_DYNAMICS_OR_MATTER"
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
    actual = {path.name for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDE}
    assert set(manifest) == actual

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    gates = json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    assert derivation["status"] == independent["status"] == verification["status"] == gates["status"] == "PASS"
    assert derivation["maximum_conclusion"] == verification["maximum_conclusion"] == MAXIMUM
    assert derivation["exact_checks"] == 69
    assert independent["check_count"] == 155
    assert verification["semantic_mutations"] == verification["semantic_mutations_caught"] == 25
    assert verification["source_identities"] == 23 and verification["source_anchors"] == 15
    assert derivation["varying_unique_H1_intrinsic_ruler_channels"] == 3
    assert derivation["constant_subfamily_unique_reciprocal_pair_planes"] == 3
    assert derivation["universal_metric_ruler_projector"] is False
    assert derivation["native_bootstrap_return"] is False
    assert derivation["Xmax_derived"] is False
    output = {
        "schema": "udt.fc07_cartan_response_return.package.v1",
        "status": "PASS",
        "manifest_files": len(manifest),
        "manifest_sha256": hashlib.sha256((HERE / "PACKAGE_MANIFEST.sha256").read_bytes()).hexdigest(),
        "scientific_grade": "VERIFIED_WITH_CAVEATS",
        "maximum_conclusion": MAXIMUM,
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
