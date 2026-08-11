#!/usr/bin/env python3
"""Fail-closed checks for the additions-only G74 external-review adjudication."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    raw = HERE / "EXTERNAL_REVIEW_RAW.md"
    transcript = HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt"
    adjudication = HERE / "EXTERNAL_REVIEW_ADJUDICATION.md"
    correction = HERE / "EXTERNAL_REVIEW_CORRECTION_PREREGISTRATION.md"

    checks = {
        "raw_hash": digest(raw)
        == "ab76e853842442289ea0296866687c9be00bb6522f0754cc645f46ce6f89a9dd",
        "transcript_hash": digest(transcript)
        == "c00b1ebd1496e25b277d7c5cf2bcea4acf8ea2fc577d43f74618cb83909620a8",
    }
    raw_text = raw.read_text(encoding="utf-8")
    adjudication_text = adjudication.read_text(encoding="utf-8")
    correction_text = correction.read_text(encoding="utf-8")
    required_raw = [
        "VERIFIED_WITH_CAVEATS",
        "MIXED_GLOBAL_COMPLETION_CLASSES",
        "All 34 manifest hashes matched",
        "3` F01 controls",
        "6` persistent controls",
        "12` tapered/sign-changing controls",
        "only partially independent",
    ]
    required_adjudication = [
        "EXTERNALLY_VERIFIED_WITH_METHOD_INDEPENDENCE_AND_PREREG_WORDING_CAVEATS",
        "SEPARATE_EQUATION_CROSS_CHECK_WITH_SHARED_PROFILE_AND_MESH_HELPERS",
        "OBSERVED_SAMPLED_REGULAR_NOT_GLOBAL_PROOF",
        "BLOCKED_SUPPLIED_PROFILE_NOT_C2_AT_CENTER",
        "Do not fit peaks",
    ]
    checks["raw_required_statements"] = all(token in raw_text for token in required_raw)
    checks["adjudication_required_statements"] = all(
        token in adjudication_text or token in correction_text for token in required_adjudication
    )
    checks["no_clean_room_promotion"] = "not clean-room independent" in adjudication_text
    checks["historical_prereg_preserved"] = "Preserve `PREREGISTRATION.md`" in correction_text
    checks["physical_scope_open"] = all(
        token in adjudication_text
        for token in ("physical CMB metric", "`X_max`", "bootstrap law", "matter source")
    )
    assert all(checks.values()), [name for name, value in checks.items() if not value]
    payload = {
        "schema": "udt-cmb-g74-external-adjudication-v1",
        "status": "PASS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "raw_sha256": digest(raw),
        "transcript_sha256": digest(transcript),
    }
    (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
