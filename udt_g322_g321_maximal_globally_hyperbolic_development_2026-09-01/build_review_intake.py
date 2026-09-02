#!/usr/bin/env python3
"""Build a sealed, self-contained, read-only G322 external-review intake."""

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SOURCE_FILES = (
    "LIVE.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "startup_surface_g310_universal_reciprocity_refresh_2026-08-31/ADOPTION_RECORD.md",
    "startup_surface_g312_two_premise_adoption_refresh_2026-09-01/ADOPTION_RECORD.md",
    "udt_g303_two_class_nonlinear_cauchy_data_classification_2026-08-30/EXACT_DERIVATION.md",
    "udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01/EXACT_DERIVATION.md",
    "udt_g319_ratio_free_noncmc_constraint_descent_2026-09-01/EXACT_DERIVATION.md",
    "udt_g320_g319_physical_initial_geometry_quotient_audit_2026-09-01/EXACT_DERIVATION.md",
    "udt_g321_g320_local_cauchy_development_uniqueness_2026-09-01/EXACT_DERIVATION.md",
    "udt_g321_g320_local_cauchy_development_uniqueness_2026-09-01/EXTERNAL_REPAIR_FOLLOWUP_RESPONSE.md",
    "udt_gr_lorentzian_relational_architecture_audit_2026-07-27/SOURCE_UNIVERSE.tsv",
    "udt_gr_lorentzian_relational_architecture_audit_2026-07-27/SOURCE_VERIFICATION.tsv",
)
EXCLUDED_PACKAGE_NAMES = {
    "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_CLI_FINAL.md",
    "EXTERNAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


intake = Path(tempfile.mkdtemp(prefix="udt_g322_review_", dir="/tmp"))
package_out = intake / "package"
package_out.mkdir()
for path in sorted(HERE.iterdir()):
    if path.is_file() and path.name not in EXCLUDED_PACKAGE_NAMES:
        shutil.copy2(path, package_out / path.name)

sources_out = intake / "sources"
for relative in SOURCE_FILES:
    source = REPO / relative
    if not source.is_file():
        raise FileNotFoundError(relative)
    target = sources_out / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)

scope = {
    "schema": "udt-g322-fresh-review-scope-v1",
    "question": "conditional unique maximal globally hyperbolic development per fixed G321 datum",
    "preregistration_commit": "8bf4aedb0cca3be76536ea69c04d635e678262ae",
    "allowed": [
        "inspect only this sealed intake",
        "copy the entire intake to a writable ephemeral directory",
        "run exactly the four package/REPLAY_COMMANDS.txt commands",
        "perform bounded read-only or ephemeral adversarial checks",
        "write the response only to the designated return directory",
    ],
    "forbidden": [
        "edit intake or evidence files",
        "continue the research or broaden the question",
        "access the repository or protected packages",
        "use internet or unsealed observations",
        "select or canonize a law history datum scale topology population source matter mass or Xmax",
        "promote the imported global theorem into a native UDT derivation",
    ],
    "registered_commands": (HERE / "REPLAY_COMMANDS.txt").read_text(encoding="utf-8").splitlines(),
    "permitted_verdicts": [
        "G322_ACCEPTED__CONDITIONAL_MAXIMAL_GLOBALLY_HYPERBOLIC_DEVELOPMENT_PER_FIXED_DATUM",
        "G322_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED",
        "G322_REFUTED__GLOBAL_CAUCHY_THEOREM_INTERFACE_FAILS",
        "G322_INCONCLUSIVE__SOURCE_OR_IMPLEMENTATION_DISAGREEMENT",
    ],
}
(intake / "REVIEW_SCOPE.json").write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

payloads = sorted(path for path in intake.rglob("*") if path.is_file())
manifest = intake / "REVIEW_MANIFEST.tsv"
with manifest.open("w", encoding="utf-8", newline="") as handle:
    handle.write("sha256\tbytes\tpath\n")
    for path in payloads:
        relative = path.relative_to(intake).as_posix()
        handle.write(f"{sha256(path)}\t{path.stat().st_size}\t{relative}\n")
manifest_hash = sha256(manifest)
seal = intake / "REVIEW_MANIFEST.sha256"
seal.write_text(f"{manifest_hash}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")

result = {
    "intake": str(intake),
    "manifest_payloads": len(payloads),
    "total_files": len(payloads) + 2,
    "scope_sha256": sha256(intake / "REVIEW_SCOPE.json"),
    "manifest_sha256": manifest_hash,
    "seal_sha256": sha256(seal),
}
print(json.dumps(result, indent=2, sort_keys=True))
