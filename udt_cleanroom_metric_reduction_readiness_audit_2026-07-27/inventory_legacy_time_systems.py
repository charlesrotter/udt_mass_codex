#!/usr/bin/env python3
"""Post-verdict, non-executing provenance inventory of named time/evolution scripts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path


FAMILIES = {
    "F01_GR_S2_COUPLED": {
        "paths": {
            "legacy/root_oneoffs_2026-07-01/coupled_tl_timelive.py",
            "legacy/root_oneoffs_2026-07-01/p4_time_live.py",
            "legacy/root_oneoffs_2026-07-01/p5d_timelive.py",
        },
        "operator": "IMPORTED_GR_EINSTEIN_EOM_PLUS_POSIT_S2_L2L4_ACTION",
        "choices": "harmonic_balance;S2_carrier;L2+L4;Einstein_closure;reduced_or_frozen_background",
        "disposition": "HISTORICAL_BLOCKED_CURRENT_NATIVE_BACKGROUND_SOLVE",
    },
    "F02_LEGACY_SCALAR_SOURCE": {
        "paths": {
            "legacy/root_oneoffs_2026-07-01/dyn1_evolve.py",
            "legacy/root_oneoffs_2026-07-01/dyn1_evolve2.py",
            "legacy/root_oneoffs_2026-07-01/dyn1_evolve3.py",
            "legacy/root_oneoffs_2026-07-01/dyn1_evolve_implicit.py",
            "legacy/root_oneoffs_2026-07-01/ns_scan_evolve.py",
        },
        "operator": "LEGACY_INDEPENDENT_SCALAR_PROFILE_EQUATION_WITH_CHOSEN_SOURCE_POTENTIAL",
        "choices": "independent_phi_or_v;two_exponential_source;radial_or_spherical_slice;Neumann_BC",
        "disposition": "HISTORICAL_BLOCKED_CURRENT_NATIVE_BACKGROUND_SOLVE",
    },
    "F03_S2_STRESS_PROBE": {
        "paths": {"legacy/root_oneoffs_2026-07-01/native_matter_timelive_probe.py"},
        "operator": "POSIT_S2_L2L4_STRESS_KINEMATICS",
        "choices": "S2_hedgehog;L2+L4;diagonal_spherical_metric",
        "disposition": "RETAINED_CONDITIONAL_CARRIER_STRESS_CHECK_NOT_NATIVE_BACKGROUND",
    },
    "F04_NONROUND_SL_PROXY": {
        "paths": {
            "legacy/root_oneoffs_2026-07-01/timelive_nonround_numeric.py",
            "legacy/root_oneoffs_2026-07-01/timelive_nonround_structural.py",
            "legacy/root_oneoffs_2026-07-01/timelive_nonround_verif_claim1.py",
            "legacy/root_oneoffs_2026-07-01/timelive_nonround_verif_claim2.py",
            "legacy/root_oneoffs_2026-07-01/timelive_nonround_verif_claim3.py",
        },
        "operator": "CHOSEN_SCALAR_STURM_LIOUVILLE_PROXY_AND_BOUNDARY_DATA",
        "choices": "legacy_scalar_equation;linearization;chosen_profiles;Dirichlet_or_Neumann;finite_box",
        "disposition": "HISTORICAL_SCOPED_PROXY_NOT_CURRENT_NATIVE_BACKGROUND",
    },
    "F05_W_CHANNEL_ACTION": {
        "paths": {
            "legacy/root_oneoffs_2026-07-01/w4b_evolib.py",
            "legacy/root_oneoffs_2026-07-01/w5_arm2_p3_evolve.py",
        },
        "operator": "SUPPLIED_W_CHANNEL_ACTION_ON_FROZEN_OR_QUASISTATIC_BACKGROUND",
        "choices": "W_wave_action;source_branch;kappa;frozen_geometry;boundary_classifier",
        "disposition": "HISTORICAL_BLOCKED_CURRENT_NATIVE_BACKGROUND_SOLVE",
    },
    "F06_SIMPLE_L_SPECTRUM": {
        "paths": {"simple_metric_angular_timelive_L.py"},
        "operator": "CHOSEN_L_BACKGROUND_SPECTRAL_OPERATOR_AND_CUTOFF",
        "choices": "fixed_L_background;spherical_harmonic_ell;Dirichlet_endpoints;epsilon_cutoff",
        "disposition": "HISTORICAL_CONDITIONAL_SPECTRAL_READOUT_NOT_BACKGROUND_DYNAMICS",
    },
    "F07_C2_EH_FLUX": {
        "paths": {
            "udt_time_live_characteristic_flux_audit_2026-07-21/derive_time_live_flux.py",
            "udt_time_live_characteristic_flux_audit_2026-07-21/verify_time_live_flux.py",
        },
        "operator": "CONDITIONAL_C2_BACH_AND_EH_PRINCIPAL_BOUNDARY_COMPARISON",
        "choices": "conditional_C2_lane;conditional_EH_lane;flat_principal_symbol;candidate_polarizations",
        "disposition": "RETAINED_CONDITIONAL_OPERATOR_COMPARISON_NOT_SELECTED_DYNAMICS",
    },
    "F08_SPHERICAL_AREAL_KINEMATICS": {
        "paths": {
            "udt_timelive_spherical_areal_polarization_audit_2026-07-22/derive_timelive_areal_polarization.py",
            "udt_timelive_spherical_areal_polarization_audit_2026-07-22/verify_timelive_areal_polarization.py",
        },
        "operator": "METRIC_KINEMATIC_SPHERICAL_AREAL_IDENTITIES",
        "choices": "spherical_orbit_reduction;conditional_physical_representative;areal_scalar",
        "disposition": "RETAINED_CONDITIONAL_KINEMATICS_NOT_BACKGROUND_DYNAMICS",
    },
}


def run(repo: Path, *args: str) -> str:
    return subprocess.check_output(args, cwd=repo, text=True).strip()


def history(repo: Path, path: str) -> tuple[str, str, str, str]:
    lines = run(repo, "git", "log", "--follow", "--format=%H%x09%cI", "--", path).splitlines()
    newest_hash, newest_date = lines[0].split("\t")
    oldest_hash, oldest_date = lines[-1].split("\t")
    return oldest_hash, oldest_date, newest_hash, newest_date


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    outdir = args.output_dir.resolve()
    repo = outdir.parent
    expected = set().union(*(row["paths"] for row in FAMILIES.values()))
    tracked = set(run(repo, "git", "ls-files", "*.py").splitlines())
    named = {path for path in tracked if any(token in Path(path).name.lower() for token in ("time_live", "timelive", "evol"))}
    if named != expected:
        raise SystemExit(json.dumps({"missing": sorted(named - expected), "extra": sorted(expected - named)}, indent=2))

    inverse = {}
    for family, meta in FAMILIES.items():
        for path in meta["paths"]:
            inverse[path] = (family, meta)

    rows = []
    for path in sorted(expected):
        source = repo / path
        family, meta = inverse[path]
        first_commit, first_date, last_commit, last_date = history(repo, path)
        text = source.read_text(encoding="utf-8", errors="replace").lower()
        rows.append({
            "path": path,
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "git_blob": run(repo, "git", "rev-parse", f"HEAD:{path}"),
            "first_commit": first_commit,
            "first_date": first_date,
            "last_commit": last_commit,
            "last_date": last_date,
            "family": family,
            "operator_provenance": meta["operator"],
            "physical_choices": meta["choices"],
            "current_disposition": meta["disposition"],
            "current_background_solve_authorized": "NO",
            "contains_einstein_token": str("einstein" in text).upper(),
            "contains_carrier_or_l2l4_token": str(any(token in text for token in ("carrier", "l2+l4", "s^2"))).upper(),
            "contains_chosen_or_proxy_token": str(any(token in text for token in ("chosen", "proxy", "shortcut"))).upper(),
            "contains_boundary_pin_token": str(any(token in text for token in ("dirichlet", "neumann", "cutoff"))).upper(),
        })

    fields = list(rows[0])
    with (outdir / "LEGACY_TIME_SYSTEMS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "schema": "udt-cleanroom-postverdict-legacy-time-provenance-1.0",
        "result": "PASS",
        "scripts": len(rows),
        "families": {family: len(meta["paths"]) for family, meta in FAMILIES.items()},
        "background_solve_authorized": 0,
        "retained_conditional_nonbackground_scripts": sum(row["current_disposition"].startswith("RETAINED_") for row in rows),
        "historical_or_blocked_scripts": sum(not row["current_disposition"].startswith("RETAINED_") for row in rows),
        "cleanroom_verdict_commit": "6c89b7a",
        "legacy_content_inspected_only_after_cleanroom_commit": True,
    }
    (outdir / "LEGACY_PROVENANCE_RESULT.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
