#!/usr/bin/env python3
"""Fail closed on the final intrinsic-contact evidence package."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


entries = []
for line in (HERE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    expected, name = line.split(None, 1)
    target = HERE / name.strip()
    assert target.is_file() and digest(target) == expected
    entries.append(name.strip())
assert len(entries) == len(set(entries))
assert digest(HERE / "PREREGISTRATION.md") == "2535d0be7eca5213afb83210adebde2820da502e35baeee6d14eac1bf007144c"
assert digest(HERE / "SOURCE_MANIFEST.tsv") == "b0ea71998dc5e0cb1c2e1aebe4f256c541863e062ceaf30625e304e80765ad4d"
assert digest(HERE / "derive_intrinsic_descent.py") == "4aa861f2d9baf3c1fc74afc2dbd9c7463bb46da40564243fdeefff0b03c47684"
assert digest(HERE / "DERIVATION_RESULT.json") == "cc49a65de1d888b01d19f66e6ff069e8eaf3d101505ffb3b4c59dd346af5b724"
assert digest(HERE / "ADJUDICATION_RESULT.json") == "d64eeef26f7e53dcdb3ec151446889b1bb6fe2c596b36becad0fd2e469da46a6"
assert digest(HERE / "DESCENT_ATLAS.tsv") == "4b03f0206f5d9b9e3921e074eb67db765ab46be2b6c6fbf059a8d801da86fa8a"
assert digest(HERE / "O13_SUBCLASSIFICATION.tsv") == "432c2fb49934d2f0d884cc58a67a80afa183d1ea9ca894ec692a9fa0b2f00a42"
assert digest(HERE / "CATCH_PROOFS.tsv") == "35047e72d558b61a179b031600062796b063d511ba8c13e52520f959015c39a5"

review = HERE / "independent_review"
assert digest(review / "verify_intrinsic_contact_coordinate.py") == "60ab5a11767dcefa60a7178c991b5294ac16263c4c720317d5902d37e5f739f1"
assert digest(review / "coordinate.stdout.txt") == "b504e07557d02b5cb35e19b9f71a4279ac502f96c75c8a6160b88a642b4fef74"
assert digest(review / "exact_contact_values.py") == "2a9b924f330f312f799d023cdb3d633c4cd083cec99077ad3c4fa9b59ae2b603"
assert digest(review / "exact_values.stdout.txt") == "79306ac13c5a137d9611b47af91ed2fedead1551994cf1948a07b82fbd2abf28"
assert digest(review / "verify_intrinsic_contact_manifest.py") == "69fdeee14ce22e42c50f3cc2bf51ebba3af470627b278a7a43cf8f1d5902fdc3"
assert digest(review / "environment.json") == "4cb272087b81beb2de39bb9964baef8ee3699fc3035144ea7f1659f7bd54744d"

adjudication = json.loads((HERE / "ADJUDICATION_RESULT.json").read_text(encoding="utf-8"))
gates = json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
assert adjudication["status"] == "PASS_VERIFIED_FRESH_COLD_REVIEW"
assert adjudication["four_gates"] == "PASS_ALL_FOUR"
assert adjudication["parent_objects"] == 22 and adjudication["O13_subclassifications"] == 2
assert adjudication["lambda_certificates"] == 3 and adjudication["catches"] == 24
assert adjudication["contact_stratum"] == "Q_POSITIVE_ONLY_ON_WITNESS"
assert adjudication["absolute_Phi_contact"] == "DERIVED_METRIC_SCALAR_ON_FROZEN_a_EQUALS_R_EQUALS_ONE_WITNESS"
assert adjudication["absolute_sigma"] == "REFERENCE_DEPENDENT__DSIGMA_INTRINSIC"
assert adjudication["alternating_contact_two_form"] == "DERIVED_IDENTICALLY_ZERO_ON_WITNESS"
assert adjudication["full_GL2_neighborhood"] == "OPEN_NOT_TESTED"
assert adjudication["on_shell_selection"] == adjudication["universal_selection"] == "OPEN_NOT_CLAIMED"
assert adjudication["physics_promoted"] is False
assert gates["status"] == "PASS" and gates["tests"] == "70 passed, 1 xfailed"

verification = {
    "status": adjudication["status"],
    "entries": len(entries),
    "package_manifest_sha256": digest(HERE / "PACKAGE_MANIFEST.sha256"),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
    "derivation_result_sha256": digest(HERE / "DERIVATION_RESULT.json"),
    "adjudication_result_sha256": digest(HERE / "ADJUDICATION_RESULT.json"),
    "headline": adjudication["headline"],
}
(HERE / "PACKAGE_VERIFICATION.json").write_text(
    json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(verification, sort_keys=True))
