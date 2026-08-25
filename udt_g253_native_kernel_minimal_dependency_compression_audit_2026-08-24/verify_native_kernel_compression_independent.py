#!/usr/bin/env python3
"""Independent source-first replay for G253; imports no production module or output."""

from __future__ import annotations

import hashlib
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_source(path: str, expected_sha256: str) -> Path:
    """Independently resolve repository and sealed-intake source layouts."""
    candidates = (ROOT / path, ROOT / "sources" / path)
    existing = [candidate for candidate in candidates if candidate.is_file()]
    assert existing, ("missing_source", path)
    actual = {candidate: digest(candidate) for candidate in existing}
    assert all(value == expected_sha256 for value in actual.values()), (
        "source_hash_mismatch",
        path,
        {str(candidate): value for candidate, value in actual.items()},
    )
    return existing[0]


def parse_manifest() -> list[tuple[str, str]]:
    rows = []
    for line in (PKG / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        path, expected, _role = line.split("\t")
        rows.append((path, expected))
    return rows


def source_has(
    path: str,
    expected_sha256: str,
    all_terms: tuple[str, ...],
    no_terms: tuple[str, ...] = (),
) -> int:
    text = resolve_source(path, expected_sha256).read_text(encoding="utf-8")
    assert all(term in text for term in all_terms)
    assert all(term not in text for term in no_terms)
    return len(all_terms) + len(no_terms)


def independent_math() -> tuple[int, int]:
    rng = random.Random(9253)
    assertions = 0
    trials = 12000
    for _ in range(trials):
        t = Fraction(rng.randrange(1, 150), rng.randrange(1, 150))
        l = Fraction(rng.randrange(1, 150), rng.randrange(1, 150))
        b = Fraction(rng.randrange(-149, 150), rng.randrange(1, 150))
        matrix = ((-t * t, -t * t * b), (-t * t * b, l * l - t * t * b * b))
        determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        assert determinant == -(t * l) ** 2
        assertions += 1
        density = t * l
        assert l / density == 1 / t
        assertions += 1
        # Homothety cancels from a pair clock ratio but not from proper time or Jacobi area.
        ell = Fraction(rng.randrange(1, 150), rng.randrange(1, 150))
        ta = Fraction(rng.randrange(1, 150), rng.randrange(1, 150))
        tb = Fraction(rng.randrange(1, 150), rng.randrange(1, 150))
        assert (ell * tb) / (ell * ta) == tb / ta
        assertions += 1
        area = Fraction(rng.randrange(1, 150), rng.randrange(1, 150))
        assert ell * ell * area != area or ell == 1
        assertions += 1
    for signed_n in range(-400, 401):
        delta = signed_n / 80
        clock = math.exp(-delta)
        ruler = math.exp(delta)
        assert abs(clock * ruler - 1) < 3e-14
        assert abs(-math.log(clock) - delta) < 3e-14
        assertions += 2
    return trials, assertions


def main() -> None:
    manifest = parse_manifest()
    assert len(manifest) == 21
    manifest_hashes = dict(manifest)
    assert len(manifest_hashes) == len(manifest)
    assert all(resolve_source(path, expected) for path, expected in manifest)

    source_assertions = 0
    source_assertions += source_has(
        "udt_g197_native_kernel_provenance_and_startup_integrity_audit_2026-08-21/AUDIT_REPORT.md",
        manifest_hashes["udt_g197_native_kernel_provenance_and_startup_integrity_audit_2026-08-21/AUDIT_REPORT.md"],
        ("No P1 profile", "G176 is the sole active non-metric selection premise", "Deleting G176 removes"),
    )
    source_assertions += source_has(
        "udt_g215_completed_scalar_shared_clock_incidence_descent_2026-08-22/EXACT_DERIVATION.md",
        manifest_hashes["udt_g215_completed_scalar_shared_clock_incidence_descent_2026-08-22/EXACT_DERIVATION.md"],
        ("incident ruler directions, angular components", "not this endpoint scalar", "Phi_s=\\phi"),
    )
    source_assertions += source_has(
        "udt_g244_metric_native_observer_sky_response_query_2026-08-24/EXACT_DERIVATION.md",
        manifest_hashes["udt_g244_metric_native_observer_sky_response_query_2026-08-24/EXACT_DERIVATION.md"],
        ("Separation from reciprocal redshift", "neither generates nor", "The SNe endpoint relation remains"),
    )
    source_assertions += source_has(
        "udt_g249_reciprocal_angular_absolute_scale_ownership_2026-08-24/EXACT_DERIVATION.md",
        manifest_hashes["udt_g249_reciprocal_angular_absolute_scale_ownership_2026-08-24/EXACT_DERIVATION.md"],
        ("equal redshift depth does not fix", "complete dimensionless metric history", "conditional calibration theorem"),
    )
    source_assertions += source_has(
        "udt_g251_same_object_metric_attachment_ownership_2026-08-24/EXACT_DERIVATION.md",
        manifest_hashes["udt_g251_same_object_metric_attachment_ownership_2026-08-24/EXACT_DERIVATION.md"],
        ("ordinary empirical step", "not a request for a new kernel term", "Metric self-evaluation is circular"),
    )

    trials, assertions = independent_math()
    result = {
        "verdict": "INDEPENDENT_REPLAY_PASS",
        "manifest_sources": len(manifest),
        "source_assertions": source_assertions,
        "independent_trials": trials,
        "independent_assertions": assertions,
        "production_module_imported": False,
        "production_output_read": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--no-write" not in sys.argv[1:]:
        (PKG / "INDEPENDENT_VERIFICATION.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
