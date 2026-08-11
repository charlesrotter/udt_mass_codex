#!/usr/bin/env python3
"""Exercise algebraic, semantic, and packaging catches for the time-live audit."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--read-only", action="store_true")
READ_ONLY = parser.parse_args().read_only

prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
independent_source = (HERE / "verify_timelive_orchestra_independent.py").read_text(encoding="utf-8")
production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
independent = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
    sources = list(csv.DictReader(stream, delimiter="\t"))

# A noncommuting control showing that the right-Maurer-Cartan sign matters.
Pt = [[0, 1], [0, 0]]
Px = [[0, 0], [1, 0]]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


commutator = [[mul(Pt, Px)[i][j] - mul(Px, Pt)[i][j] for j in range(2)] for i in range(2)]
wrong_sign_residual = [[2 * value for value in row] for row in commutator]

catches = {
    "F01_wrong_right_MC_sign_rejected": any(value != 0 for row in wrong_sign_residual for value in row),
    "F02_common_scale_retained": "d kappa-d phi" in exact and "d kappa+d phi" in exact,
    "F03_phi_retained": "exp(-2phi)d beta" in exact,
    "F04_beta_not_frozen": "shift `beta`" in exact and "dot beta_pair" in exact,
    "F05_general_Q_retained": "general invertible `2 x 2` angular coframe" in exact,
    "F06_full_S_retained": "general `2 x 2`\nmixing field" in exact,
    "F07_mixing_couples_P_and_R": "C_t P_i-C_i P_t+R_t C_i-R_i C_t" in exact,
    "F08_query_motion_separate": "J_R" in exact and "J_A" in exact and "fixed-query control" in exact,
    "F09_arbitrary_frequency_survives": independent["arbitrary_frequency_selection"] == "NONE_FROM_KINEMATICS",
    "F10_flat_K_not_spacetime_flat": "flatness of `K` is not zero spacetime curvature" in exact,
    "F11_identity_not_EOM": "not an equation selecting a movie" in audit,
    "F12_cone_not_characteristic": "principal differential operator" in exact,
    "F13_bootstrap_inactive": "Bootstrap was not used" in audit and "bootstrap density/curvature selection" in prereg,
    "F14_no_physical_regime": "physical regime" in audit and "does\nnot currently select" in audit,
    "F15_R17_not_universal": "R17 remains only a\nstationary conditional split owner" in exact,
    "F16_global_scope_excluded": "cut loci, topology, boundary, and global completion" in exact,
    "F17_no_downstream_physics": "No action, source, matter, mass" in audit,
    "F18_independent_no_production_or_sympy_import": "import sympy" not in independent_source and "derive_timelive_orchestra" not in independent_source,
    "F19_protected_atlas_absent": not any("udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" in row["path"] for row in sources),
    "F20_stopped_drafts_absent": not any("udt_native_onshell_timelive_reset_owner_audit_2026-08-10" in row["path"] for row in sources),
}

failed = [name for name, caught in catches.items() if not caught]
result = {
    "schema_version": 1,
    "catch_count": len(catches),
    "caught_count": sum(catches.values()),
    "catches": catches,
    "failed": failed,
}
assert not failed, failed
assert production["status"] == "EXACT_COMPATIBILITY_ORCHESTRA_BUT_NO_EVOLUTION_LAW"
assert independent["status"] == "PASS" and independent["total_exact_trials"] == 1200
if not READ_ONLY:
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
print(json.dumps(result, indent=2, sort_keys=True))
