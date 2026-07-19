#!/usr/bin/env python3
"""Independent fail-closed verifier for the reciprocal metric null-line selector."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import pathlib
import platform
import subprocess
import tempfile

import sympy as sp


BASE = "e76d748881e6a091ce367a4c11db640700724bfb"
PREREG = "9fc890a5074f016917272b1b37b3681cedff2d53"
VERDICT = (
    "NONTRIVIAL_STATIC_NULL_DPHI_EXCLUDED_WITHIN_POSITIVE_SPATIAL_STATIC_SUBFAMILY; "
    "TIME_LIVE_NULL_DPHI_OPTIONAL_EIKONAL_BRANCH; "
    "ROUND_ANGULAR_WARPED_FAMILY_PETROV_D_OR_O_CONDITIONAL; "
    "RECIPROCAL_ANISOTROPIC_PETROV_I_COUNTERFAMILY_EXISTS; "
    "UNIQUE_REPEATED_PND_UNDERDETERMINED; "
    "GLOBAL_CONFORMAL_NULL_LINE_NOT_DERIVED"
)

EXPECTED_SOURCES = {
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
    "CANON.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "projective_transport_section_selector_2026-07-19/AUDIT_REPORT.md",
    "projective_transport_section_selector_2026-07-19/STATUS_LEDGER.tsv",
    "projective_transport_section_selector_2026-07-19/DERIVATION_RESULT.json",
    "transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md",
    "transverse_reciprocal_realization_selector_2026-07-19/STATUS_LEDGER.tsv",
    "null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md",
    "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv",
    "angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md",
    "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
    "reciprocal_clock_optical_scale_selector_2026-07-19/DERIVATION_REPORT.md",
    "reciprocal_clock_optical_scale_selector_2026-07-19/STATUS_LEDGER.tsv",
}

EXPECTED_CANDIDATES = {
    "N01": ("STATIC_GENERAL_ANGULAR_DPHI", "EXCLUDED_NONTRIVIAL_NULL"),
    "N02": ("TIME_LIVE_RADIAL_EIKONAL", "OPTIONAL_BRANCH"),
    "N03": ("TIME_LIVE_ANGULAR_EIKONAL", "OPTIONAL_BRANCH"),
    "N04": ("ROUND_ANGULAR_WARPED_PETROV", "PAIR_OR_NONE_CONDITIONAL"),
    "N05": ("ANISOTROPIC_TRANSVERSE_PETROV", "COUNTERFAMILY"),
    "N06": ("ALGEBRAICALLY_SPECIAL_UNIQUE_PND", "CONDITIONAL_LOCAL_SELECTOR"),
    "N07": ("SEAL_AND_GLOBAL_CONTINUATION", "GLOBAL_GATE_OPEN"),
    "N08": ("FINITE_CELL_BOOTSTRAP_ACTION", "NO_CURRENT_OPERATOR"),
}

EXPECTED_LEDGER = {
    "R01": "DERIVED_CONDITIONAL",
    "R02": "DERIVED_CONDITIONAL",
    "R03": "DERIVED_CONDITIONAL",
    "R04": "DERIVED_WITHIN_SUBFAMILY",
    "R05": "EXCLUDED_WITHIN_SUBFAMILY",
    "R06": "OPTIONAL_EIKONAL_BRANCH",
    "R07": "OBSERVED_EXACT",
    "R08": "DERIVED_CONDITIONAL",
    "R09": "OPTIONAL_EIKONAL_BRANCH",
    "R10": "DERIVED_WITHIN_STATIC_SEAL",
    "R11": "NOT_DERIVED",
    "R12": "DERIVED_CONDITIONAL",
    "R13": "PETROV_D_CONDITIONAL",
    "R14": "PETROV_O_CONDITIONAL",
    "R15": "EXCLUDED_WITHIN_SUBFAMILY",
    "R16": "EXACT_COUNTERFAMILY",
    "R17": "OBSERVED_EXACT",
    "R18": "PETROV_I_EXACT_COUNTERFAMILY",
    "R19": "REFUTED_AT_KINEMATIC_LEVEL",
    "R20": "CONDITIONAL_LOCAL_SELECTOR",
    "R21": "EXCLUDED_NOT_IMPORTED",
    "R22": "DERIVED_CONDITIONAL",
    "R23": "NOT_DERIVED",
    "R24": "NO_CURRENT_OPERATOR",
    "R25": "OPEN_NOT_ACTIVATED",
    "R26": "OPEN_NOT_ACTIVATED",
    "R27": "NOT_CLAIMED",
    "R28": "UNDERDETERMINED_NOT_DERIVED",
}


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def run(repo: pathlib.Path, *command: str, binary: bool = False):
    result = subprocess.run(
        list(command), cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if result.returncode:
        stderr = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise AssertionError(f"command failed {command}: {stderr}")
    return result.stdout


def git(repo: pathlib.Path, *args: str, binary: bool = False):
    return run(repo, "git", *args, binary=binary)


def table(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def base_text(repo: pathlib.Path, path: str) -> str:
    return str(git(repo, "show", f"{BASE}:{path}"))


def reject(name: str, callback) -> dict[str, str]:
    try:
        callback()
    except (AssertionError, KeyError, ValueError):
        return {"name": name, "result": "PASS_REJECTED"}
    raise AssertionError(f"catch-proof accepted corruption: {name}")


def validate_prereg(repo: pathlib.Path, package: pathlib.Path) -> None:
    registered = bytes(git(repo, "show", f"{PREREG}:reciprocal_metric_null_line_selector_2026-07-19/PREREGISTRATION.md", binary=True))
    assert package.joinpath("PREREGISTRATION.md").read_bytes() == registered
    text = registered.decode("utf-8")
    assert BASE in text
    assert "**OBSERVING.**" in text
    assert "STATIC_GENERAL_ANGULAR_DPHI" in text
    assert "ANISOTROPIC_TRANSVERSE_PETROV" in text
    assert "No carrier adoption" in text


def validate_sources(repo: pathlib.Path, inventory: list[dict[str, str]]) -> None:
    assert len(inventory) == 16
    assert len({row["current_path"] for row in inventory}) == 16
    assert {row["current_path"] for row in inventory} == EXPECTED_SOURCES
    for row in inventory:
        path = row["current_path"]
        payload = bytes(git(repo, "show", f"{BASE}:{path}", binary=True))
        assert row["blob_oid"] == str(git(repo, "rev-parse", f"{BASE}:{path}")).strip()
        assert row["sha256"] == sha(payload)
        assert int(row["size_bytes"]) == len(payload)
        assert row["last_commit"] == str(git(repo, "log", "-1", "--format=%H", BASE, "--", path)).strip()


def validate_source_semantics(repo: pathlib.Path, overrides: dict[str, str] | None = None) -> None:
    overrides = overrides or {}
    texts = {path: overrides.get(path, base_text(repo, path)) for path in EXPECTED_SOURCES}
    assert "the transverse spatial block or full time-live geometry" in texts["UDT_NATIVE_ACTION_COLD_PACKET.md"]
    assert "spatial-depth mirror makes `phi` odd" in texts["UDT_NATIVE_ACTION_COLD_PACKET.md"]
    assert "\\Omega(x)^2g_{\\mu\\nu}:\\Omega(x)>0" in texts["UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md"]
    assert "not silently inferred from the word “bootstraps.”" in texts["UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md"]
    assert "Petrov types II, III, and N" in texts["projective_transport_section_selector_2026-07-19/AUDIT_REPORT.md"]
    assert "Is the physical first gate passed? | `NO`" in texts["transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md"]
    assert "Fiber topology does not supply a frame-invariant carrier field" in texts["null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md"]


def validate_candidates(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 8
    assert len({row["family_id"] for row in rows}) == 8
    assert {row["family_id"] for row in rows} == set(EXPECTED_CANDIDATES)
    for row in rows:
        assert (row["family"], row["selector_status"]) == EXPECTED_CANDIDATES[row["family_id"]]
    assert "two sign branches" in next(row for row in rows if row["family_id"] == "N02")["obstruction_or_limit"]
    assert "four simple PNDs" in next(row for row in rows if row["family_id"] == "N05")["exact_positive_result"]
    assert "no action" in next(row for row in rows if row["family_id"] == "N08")["obstruction_or_limit"]


def validate_ledger(rows: list[dict[str, str]]) -> None:
    assert len(rows) == 28
    assert len({row["claim_id"] for row in rows}) == 28
    assert {row["claim_id"] for row in rows} == set(EXPECTED_LEDGER)
    for row in rows:
        assert row["status"] == EXPECTED_LEDGER[row["claim_id"]]
    assert "dphi=0" in next(row for row in rows if row["claim_id"] == "R05")["basis"]
    assert "two and O gives none" in next(row for row in rows if row["claim_id"] == "R15")["basis"]
    assert "not certified on shell" in next(row for row in rows if row["claim_id"] == "R16")["dependency_or_limit"]
    assert "geodesicity" in next(row for row in rows if row["claim_id"] == "R21")["dependency_or_limit"]
    assert "not yet a section" in next(row for row in rows if row["claim_id"] == "R25")["basis"]


def validate_algebra(data: dict) -> None:
    assert data["status"] == "PASS"
    assert data["check_count"] == 32
    assert len(data["checks"]) == 32
    assert set(data["checks"].values()) == {"PASS"}
    assert data["verdict"] == VERDICT
    exact = data["exact_identities"]
    assert "c_light**2" in exact["general_dphi_norm"]
    assert "qnorm" in exact["general_dphi_norm"]
    assert exact["explicit_angular_inverse_norm"] == "(px**2*qd - 2*px*py*qb + py**2*qa)/(qa*qd - qb**2)"
    assert "px**2/qa" in exact["angular_complete_square_decomposition"]
    assert "(-px*qb + py*qa)**2" in exact["angular_complete_square_decomposition"]
    assert exact["anisotropic_np_at_k1_ay2_az3_r0"] == {
        "psi0": "-5/4", "psi1": "0", "psi2": "-13/12", "psi3": "0", "psi4": "-5/4"
    }
    assert exact["anisotropic_pnd_polynomial"] == "-(z**2 + 5)*(5*z**2 + 1)/4"
    assert exact["anisotropic_pnd_discriminant"] == "32400"
    assert exact["anisotropic_petrov_I"] == "61/12"
    assert exact["anisotropic_petrov_J"] == "-91/216"
    assert exact["anisotropic_speciality_discriminant"] == "2025/16"
    classification = data["classification"]
    assert classification["static_positive_spatial_dphi"].startswith("SPACELIKE_OR_ZERO")
    assert classification["time_live_radial_dphi"] == "NULL_IS_OPTIONAL_EIKONAL_PDE_NOT_RECIPROCITY_IDENTITY"
    assert classification["round_angular_warped_petrov"] == "D_IF_PSI2_NONZERO; O_IF_PSI2_ZERO; TWO_OR_NO_PNDS"
    assert classification["anisotropic_reciprocal_counterfamily"] == "PETROV_I_WITH_FOUR_SIMPLE_PNDS"
    assert classification["global_conformal_null_line"] == "NOT_DERIVED"
    assert set(data["counterfamilies"]) == {
        "static_nonzero_phi_spacelike_gradient",
        "explicit_time_live_null_gradient",
        "round_angular_petrov_d_or_o",
        "anisotropic_reciprocal_petrov_i",
    }


def validate_report(report: str) -> None:
    normalized = " ".join(report.split())
    required = [
        VERDICT,
        "The angular sector is decisive rather than decorative",
        "smooth positive nondegenerate Common-Scale change",
        "P_{\\rm seal}",
        "These are eikonal equations, not identities",
        "two distinct double base-null directions",
        "second double root at infinity",
        "I^3-27J^2",
        "A principal null direction is not automatically geodesic",
        "strong kinematic underdetermination, not a complete-dynamics no-go",
        "No further derivation",
    ]
    for token in required:
        assert token in normalized, token
    forbidden = [
        "the carrier is derived",
        "petrov ii is forced",
        "global conformal null line derived",
        "counterfamilies are complete udt universes",
        "finite-cell cap gate passed",
        "goldberg-sachs was applied",
    ]
    lower = report.lower()
    for token in forbidden:
        assert token not in lower, token


def direct_np(metric: sp.Matrix, coords: tuple[sp.Symbol, ...], tetrad: tuple[sp.Matrix, ...], at: dict) -> dict[str, sp.Expr]:
    """Fresh coordinate implementation, intentionally independent of the derivation module."""
    dim = 4
    inverse = metric.inv()
    connection = [[[
        sp.simplify(sum(inverse[a, e] * (
            sp.diff(metric[e, b], coords[c]) + sp.diff(metric[e, c], coords[b])
            - sp.diff(metric[b, c], coords[e])
        ) for e in range(dim)) / 2)
        for c in range(dim)] for b in range(dim)] for a in range(dim)]
    riemann_up = [[[[
        sp.simplify(
            sp.diff(connection[a][b][d], coords[c])
            - sp.diff(connection[a][b][c], coords[d])
            + sum(connection[a][e][c] * connection[e][b][d]
                  - connection[a][e][d] * connection[e][b][c] for e in range(dim))
        )
        for d in range(dim)] for c in range(dim)] for b in range(dim)] for a in range(dim)]
    ricci = [[sp.simplify(sum(riemann_up[a][b][a][d] for a in range(dim))) for d in range(dim)] for b in range(dim)]
    scalar = sp.simplify(sum(inverse[a, b] * ricci[a][b] for a in range(dim) for b in range(dim)))

    def weyl(a: int, b: int, c: int, d: int):
        rlow = sum(metric[a, e] * riemann_up[e][b][c][d] for e in range(dim))
        value = rlow - (
            metric[a, c] * ricci[b][d] - metric[a, d] * ricci[b][c]
            - metric[b, c] * ricci[a][d] + metric[b, d] * ricci[a][c]
        ) / 2 + scalar * (metric[a, c] * metric[b, d] - metric[a, d] * metric[b, c]) / 6
        return sp.simplify(value.subs(at))

    vectors = [vector.applyfunc(lambda value: sp.simplify(value.subs(at))) for vector in tetrad]
    lvec, nvec, mvec, mbvec = vectors

    def contract(v1, v2, v3, v4):
        return sp.simplify(-sum(
            weyl(a, b, c, d) * v1[a] * v2[b] * v3[c] * v4[d]
            for a in range(dim) for b in range(dim) for c in range(dim) for d in range(dim)
        ))

    return {
        "psi0": contract(lvec, mvec, lvec, mvec),
        "psi1": contract(lvec, nvec, lvec, mvec),
        "psi2": contract(lvec, mvec, mbvec, nvec),
        "psi3": contract(lvec, nvec, mbvec, nvec),
        "psi4": contract(nvec, mbvec, nvec, mbvec),
    }


def independent_exact() -> dict[str, str]:
    phi, pt, pr, c0 = sp.symbols("phi pt pr c0", real=True, positive=True)
    a, b, d, px, py = sp.symbols("a b d px py", real=True)
    determinant = a * d - b**2
    q_inverse_norm = sp.factor((d * px**2 - 2 * b * px * py + a * py**2) / determinant)
    expected = sp.Matrix([px, py]).dot(sp.Matrix([[a, b], [b, d]]).inv() * sp.Matrix([px, py]))
    assert sp.simplify(q_inverse_norm - expected) == 0
    P = -sp.exp(2 * phi) * pt**2 / c0**2 + sp.exp(-2 * phi) * pr**2 + q_inverse_norm
    assert sp.simplify(P.subs({pt: c0 * sp.exp(-2 * phi) * pr, px: 0, py: 0})) == 0
    assert sp.simplify(P.subs({pt: 0, px: 0, py: 0}) - sp.exp(-2 * phi) * pr**2) == 0

    t, r, rate, A, B = sp.symbols("t r rate A B", real=True)
    wave = sp.log((A + 2 * c0 * rate * t) / (B - 2 * rate * r)) / 2
    wave_norm = -sp.exp(2 * wave) * sp.diff(wave, t)**2 / c0**2 + sp.exp(-2 * wave) * sp.diff(wave, r)**2
    assert sp.simplify(wave_norm) == 0

    tt, rr, xx, yy = sp.symbols("tt rr xx yy", real=True)
    root2 = sp.sqrt(2)
    anisotropic = sp.diag(-sp.exp(-2 * rr), sp.exp(2 * rr), sp.exp(4 * rr), sp.exp(6 * rr))
    lvec = sp.Matrix([sp.exp(rr), sp.exp(-rr), 0, 0]) / root2
    nvec = sp.Matrix([sp.exp(rr), -sp.exp(-rr), 0, 0]) / root2
    mvec = sp.Matrix([0, 0, sp.exp(-2 * rr), sp.I * sp.exp(-3 * rr)]) / root2
    anis_np = direct_np(anisotropic, (tt, rr, xx, yy), (lvec, nvec, mvec, sp.conjugate(mvec)), {rr: 0})
    assert anis_np == {"psi0": -sp.Rational(5, 4), "psi1": 0, "psi2": -sp.Rational(13, 12), "psi3": 0, "psi4": -sp.Rational(5, 4)}
    z = sp.symbols("z")
    polynomial = sp.factor(anis_np["psi0"] + 4*anis_np["psi1"]*z + 6*anis_np["psi2"]*z**2 + 4*anis_np["psi3"]*z**3 + anis_np["psi4"]*z**4)
    assert sp.expand(polynomial + (z**2 + 5) * (5*z**2 + 1) / 4) == 0
    assert sp.discriminant(polynomial, z) == 32400

    theta, varphi = sp.symbols("theta varphi", real=True)
    pfun = rr
    radius = 1 + rr
    spherical = sp.diag(-sp.exp(-2*pfun), sp.exp(2*pfun), radius**2, radius**2*sp.sin(theta)**2)
    ls = sp.Matrix([sp.exp(pfun), sp.exp(-pfun), 0, 0]) / root2
    ns = sp.Matrix([sp.exp(pfun), -sp.exp(-pfun), 0, 0]) / root2
    ms = sp.Matrix([0, 0, 1/radius, sp.I/(radius*sp.sin(theta))]) / root2
    spherical_np = direct_np(spherical, (tt, rr, theta, varphi), (ls, ns, ms, sp.conjugate(ms)), {rr: 0, theta: sp.pi/2})
    assert spherical_np["psi0"] == spherical_np["psi1"] == spherical_np["psi3"] == spherical_np["psi4"] == 0
    assert spherical_np["psi2"] != 0

    bvar = sp.symbols("bvar")
    assert sorted(sp.roots(bvar**2*(bvar-1)*(bvar+1), bvar).values()) == [1, 1, 2]
    assert sorted(sp.roots(bvar**3*(bvar-1), bvar).values()) == [1, 3]
    assert sp.roots(bvar**4, bvar) == {0: 4}
    return {
        "general_positive_angular_norm": "PASS",
        "static_causal_class": "PASS",
        "radial_eikonal_relation": "PASS",
        "explicit_time_live_solution": "PASS",
        "independent_anisotropic_weyl": "PASS",
        "independent_petrov_i_quartic": "PASS",
        "independent_round_warped_d_witness": "PASS",
        "special_pnd_multiplicities": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    package = pathlib.Path(__file__).resolve().parent
    repo = package.parent

    inventory = table(package / "SOURCE_INVENTORY.tsv")
    candidates = table(package / "CANDIDATE_FAMILY.tsv")
    ledger = table(package / "STATUS_LEDGER.tsv")
    algebra = json.loads((package / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    report = (package / "AUDIT_REPORT.md").read_text(encoding="utf-8")

    validate_prereg(repo, package)
    validate_sources(repo, inventory)
    validate_source_semantics(repo)
    validate_candidates(candidates)
    validate_ledger(ledger)
    validate_algebra(algebra)
    validate_report(report)

    with tempfile.TemporaryDirectory(prefix="udt-null-line-replay-") as directory:
        replay = pathlib.Path(directory) / "result.json"
        subprocess.run(
            ["python3", str(package / "derive_reciprocal_null_line_selector.py"), "--output", str(replay)],
            cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        assert replay.read_bytes() == (package / "DERIVATION_RESULT.json").read_bytes()

    independent = independent_exact()

    catches: list[dict[str, str]] = []
    missing_source = copy.deepcopy(inventory[:-1])
    catches.append(reject("missing_source", lambda: validate_sources(repo, missing_source)))
    duplicate_candidate = copy.deepcopy(candidates)
    duplicate_candidate[-1]["family_id"] = "N01"
    catches.append(reject("duplicate_candidate", lambda: validate_candidates(duplicate_candidate)))
    dropped_angular = copy.deepcopy(algebra)
    dropped_angular["exact_identities"]["general_dphi_norm"] = "-pt**2*exp(2*phi)/c_light**2 + pr**2*exp(-2*phi)"
    catches.append(reject("dropped_positive_angular_term", lambda: validate_algebra(dropped_angular)))
    static_promoted = copy.deepcopy(ledger)
    next(row for row in static_promoted if row["claim_id"] == "R05")["status"] = "DERIVED"
    catches.append(reject("static_nonzero_gradient_called_null", lambda: validate_ledger(static_promoted)))
    eikonal_promoted = copy.deepcopy(ledger)
    next(row for row in eikonal_promoted if row["claim_id"] == "R06")["status"] = "FOUNDING_IDENTITY"
    catches.append(reject("eikonal_promoted_to_reciprocity", lambda: validate_ledger(eikonal_promoted)))
    d_unique = copy.deepcopy(ledger)
    next(row for row in d_unique if row["claim_id"] == "R15")["status"] = "UNIQUE_PND"
    catches.append(reject("petrov_d_pair_called_unique", lambda: validate_ledger(d_unique)))
    o_selected = copy.deepcopy(ledger)
    next(row for row in o_selected if row["claim_id"] == "R14")["status"] = "SELECTED_RAY"
    catches.append(reject("petrov_o_called_selector", lambda: validate_ledger(o_selected)))
    no_type_i = copy.deepcopy(algebra)
    del no_type_i["counterfamilies"]["anisotropic_reciprocal_petrov_i"]
    catches.append(reject("deleted_petrov_i_counterfamily", lambda: validate_algebra(no_type_i)))
    gr_geodesic = copy.deepcopy(ledger)
    next(row for row in gr_geodesic if row["claim_id"] == "R21")["status"] = "IMPORTED_GR_CLOSURE"
    catches.append(reject("imported_gr_geodesicity", lambda: validate_ledger(gr_geodesic)))
    no_transition = copy.deepcopy(candidates)
    next(row for row in no_transition if row["family_id"] == "N07")["selector_status"] = "GLOBAL_PASS"
    catches.append(reject("skipped_seal_type_transition", lambda: validate_candidates(no_transition)))
    carrier_claim = report.replace("No further derivation", "The carrier is derived. No further derivation")
    catches.append(reject("claimed_carrier_closure", lambda: validate_report(carrier_claim)))
    complete_universe = report.replace("they are not certified solutions", "counterfamilies are complete UDT universes; they are certified solutions")
    catches.append(reject("claimed_complete_on_shell_countermodel", lambda: validate_report(complete_universe)))
    source_mutation = {"UDT_NATIVE_ACTION_COLD_PACKET.md": base_text(repo, "UDT_NATIVE_ACTION_COLD_PACKET.md").replace("the transverse spatial block or full time-live geometry", "nothing remains open")}
    catches.append(reject("mutated_open_transverse_source", lambda: validate_source_semantics(repo, source_mutation)))

    result = {
        "status": "PASS",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "base": BASE,
        "preregistration": PREREG,
        "source_rows": len(inventory),
        "candidate_rows": len(candidates),
        "ledger_rows": len(ledger),
        "controller_checks": algebra["check_count"],
        "byte_identical_derivation_replay": "PASS",
        "independent_exact_checks": independent,
        "catch_proofs": catches,
        "catch_proof_count": len(catches),
        "verdict": VERDICT,
    }
    pathlib.Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"VERIFICATION PASS catches={len(catches)}/{len(catches)} independent={len(independent)}/{len(independent)}")


if __name__ == "__main__":
    main()
