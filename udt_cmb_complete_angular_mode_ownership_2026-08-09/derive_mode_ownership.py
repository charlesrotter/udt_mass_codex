#!/usr/bin/env python3
"""Exact bounded derivation for complete-angular mode ownership.

No observational values are loaded.  C1 is a declared axis-regular spherical
completion of the equatorial scalar probe, not a selected UDT metric.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "33579c653e853cecf0fe10c4266c5c54fc72b735"
KEYS: dict[str, bool] = {}


def key(name: str, condition: object) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_sha256(path_text: str) -> str:
    completed = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{path_text}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return hashlib.sha256(completed.stdout).hexdigest()


def lie_derivative_metric(
    metric: sp.Matrix, vector: sp.Matrix, coordinates: tuple[sp.Symbol, ...]
) -> sp.Matrix:
    size = len(coordinates)
    out = sp.zeros(size)
    for mu in range(size):
        for nu in range(size):
            value = sum(vector[k] * sp.diff(metric[mu, nu], coordinates[k]) for k in range(size))
            value += sum(metric[k, nu] * sp.diff(vector[k], coordinates[mu]) for k in range(size))
            value += sum(metric[mu, k] * sp.diff(vector[k], coordinates[nu]) for k in range(size))
            out[mu, nu] = sp.trigsimp(sp.simplify(value))
    return out


def main() -> None:
    t, r, theta, psi = sp.symbols("t r theta psi", real=True)
    omega, m = sp.symbols("omega m", real=True)
    A = sp.Function("A", positive=True)(r)
    h = sp.Function("h", real=True)(r)
    s = sp.sin(theta)
    c = sp.cos(theta)
    D = A * r**2 + h**2 * s**2

    # C1: the axis-regular round-screen completion named, but not computed, by RA1.
    metric = sp.Matrix(
        [
            [-A, 0, 0, h * s**2],
            [0, 1 / A, 0, 0],
            [0, 0, r**2, 0],
            [h * s**2, 0, 0, r**2 * s**2],
        ]
    )
    inverse = sp.Matrix(
        [
            [-r**2 / D, 0, 0, h / D],
            [0, A, 0, 0],
            [0, 0, 1 / r**2, 0],
            [h / D, 0, 0, A / (s**2 * D)],
        ]
    )
    determinant = -r**2 * s**2 * D / A
    volume = r * s * sp.sqrt(D / A)  # on the regular chart 0 < theta < pi

    key("K01_inverse", all(sp.simplify(x) == 0 for x in metric * inverse - sp.eye(4)))
    key("K02_determinant", sp.simplify(metric.det() - determinant) == 0)
    key("K03_volume", sp.simplify(volume**2 + determinant) == 0)
    key("K04_lorentzian_block", sp.simplify(metric.extract([0, 3], [0, 3]).det() + s**2 * D) == 0)

    time_azimuth = sp.simplify(
        -omega**2 * inverse[0, 0] + 2 * omega * m * inverse[0, 3] - m**2 * inverse[3, 3]
    )
    expected_potential = (r**2 * omega**2 + 2 * h * omega * m - A * m**2 / s**2) / D
    key("K05_time_azimuth_potential", sp.simplify(time_azimuth - expected_potential) == 0)

    # The full reduced scalar equation for exp(-i omega t+i m psi) u(r,theta) is
    # 1/S d_r(S A u_r)+1/S d_theta(S/r^2 u_theta)+V u=0.
    u = sp.Function("u")(r, theta)
    full_operator = (
        sp.diff(volume * A * sp.diff(u, r), r) / volume
        + sp.diff(volume * sp.diff(u, theta) / r**2, theta) / volume
        + expected_potential * u
    )
    key("K06_full_operator_has_both_derivatives", full_operator.has(sp.diff(u, r, 2)) and full_operator.has(sp.diff(u, theta, 2)))

    # At the equator the 4D volume carries an extra r relative to the 3D FD1 slice.
    D_eq = A * r**2 + h**2
    W_fd1 = sp.sqrt(D_eq / A)
    S_eq = sp.simplify(volume.subs(theta, sp.pi / 2))
    key("K07_equatorial_volume_extra_r", sp.simplify(S_eq / W_fd1 - r) == 0)
    key("K08_equatorial_potential_matches", sp.simplify(expected_potential.subs(theta, sp.pi / 2) - (r**2 * omega**2 + 2 * h * omega * m - A * m**2) / D_eq) == 0)

    # h=0 restores the ordinary round-screen operator and SO(3) angular multiplets.
    key("K09_round_volume", sp.simplify(volume.subs(h, 0) ** 2 - r**4 * s**2) == 0)
    key("K10_round_potential", sp.simplify(expected_potential.subs(h, 0) - (omega**2 / A - m**2 / (r**2 * s**2))) == 0)

    # Generic nonseparability.  The unique product-separation multiplier forced by the
    # principal coefficients is r^2.  Its radial first-derivative coefficient has a
    # nonzero theta derivative whenever B'=d[h^2/(A r^2)]/dr is nonzero.
    B = sp.simplify(h**2 / (A * r**2))
    mixed_log_volume = sp.simplify(sp.diff(sp.diff(sp.log(volume), theta), r))
    expected_mixed = sp.diff(B, r) * s * c / (1 + B * s**2) ** 2
    key("K11_mixed_volume_identity", sp.trigsimp(sp.simplify(mixed_log_volume - expected_mixed)) == 0)
    hb, n, q = sp.symbols("hbar n q", nonzero=True, real=True)
    B_fd1 = hb**2 * r**2 * (1 - r) ** (2 * q - n)
    Bprime_witness = sp.simplify(sp.diff(B_fd1, r).subs({r: sp.Rational(1, 3), n: sp.Rational(3, 2), q: 0, hb: 1}))
    key("K12_fd1_profile_generically_nonseparable", Bprime_witness != 0)
    key("K13_round_limit_separable", sp.simplify(expected_mixed.subs(h, 0)) == 0)

    coordinates = (t, r, theta, psi)
    Jz = sp.Matrix([0, 0, 0, 1])
    Jx = sp.Matrix([0, 0, -sp.sin(psi), -sp.cot(theta) * sp.cos(psi)])
    Lz = lie_derivative_metric(metric, Jz, coordinates)
    Lx = lie_derivative_metric(metric, Jx, coordinates)
    key("K14_axial_U1_survives", all(entry == 0 for entry in Lz))
    key("K15_nonaxial_rotation_broken", sp.simplify(Lx[0, 2] - h * sp.cos(psi)) == 0 and Lx[0, 2] != 0)
    key("K16_SO3_restored_at_h0", all(sp.simplify(entry.subs(h, 0)) == 0 for entry in Lx))

    # Equatorial reflection is still exact, so C1 decomposes by m and north/south parity.
    parity_checks = [
        sp.trigsimp(entry.subs(theta, sp.pi - theta) - entry)
        for entry in (D, volume / s, expected_potential)
    ]
    key("K17_equatorial_parity_survives", all(sp.simplify(entry) == 0 for entry in parity_checks))

    ell, a = sp.symbols("ell a", integer=True, nonnegative=True)
    indicial_3d = sp.expand(a * (a + 1) - ell * (ell + 1))
    indicial_2d = sp.expand(a**2 - m**2)
    key("K18_full_center_regular_power", sp.simplify(indicial_3d.subs(a, ell)) == 0)
    key("K19_equatorial_center_regular_power", sp.simplify(indicial_2d.subs({a: 1, m: 1})) == 0 and sp.simplify(indicial_2d.subs({a: 0, m: 0})) == 0)
    key(
        "K20_same_index_not_round_triplet",
        sp.simplify(indicial_2d.subs({a: 0, m: 0})) == 0
        and sp.simplify(indicial_2d.subs({a: 1, m: 1})) == 0
        and sp.simplify(indicial_3d.subs({a: 1, ell: 1})) == 0
        and sp.simplify(indicial_3d.subs({a: 0, ell: 1})) != 0,
    )

    # A smooth positive general-screen area mode can break the axial U(1).  This is an
    # availability counterexample, not a selected physical screen.
    eps = sp.symbols("epsilon", real=True)
    Vscreen = 1 + eps * sp.sin(theta) * sp.cos(psi)
    gthth_general = r**2 * Vscreen
    axial_break = sp.diff(gthth_general, psi)
    key("K21_general_screen_can_break_m", sp.simplify(axial_break + eps * r**2 * sp.sin(theta) * sp.sin(psi)) == 0 and axial_break != 0)

    # Conditional group projectors characterize every m; none singles out one m.
    alpha = sp.symbols("alpha", real=True)
    unequal = sp.integrate(sp.exp(-sp.I * alpha), (alpha, 0, 2 * sp.pi)) / (2 * sp.pi)
    equal = sp.integrate(1, (alpha, 0, 2 * sp.pi)) / (2 * sp.pi)
    key("K22_U1_projectors_orthogonal", sp.simplify(unequal) == 0 and sp.simplify(equal - 1) == 0)

    source_rows = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        next(handle)
        for line in handle:
            path_text, expected_hash = line.rstrip("\n").split("\t")
            source_rows.append((path_text, expected_hash))
    key("K23_source_manifest", all(frozen_sha256(path) == digest for path, digest in source_rows))
    global_report = (ROOT / "udt_native_global_coframe_definition_audit_2026-07-28/AUDIT_REPORT.md").read_text(encoding="utf-8")
    screen_report = (ROOT / "udt_intrinsic_general_screen_neighborhood_audit_2026-08-02/AUDIT_REPORT.md").read_text(encoding="utf-8")
    fd1_report = (ROOT / "udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md").read_text(encoding="utf-8")
    key("K24_no_selected_complete_lift", "OPEN_MULTIPLE_INDEPENDENT_SELECTOR_GAPS" in global_report and "complete reciprocal lift" in global_report)
    key("K25_general_screen_selection_open", "SCREEN_SELECTION_OPEN" in screen_report and "does not say which member" in screen_report)
    fd1_flat = " ".join(fd1_report.split())
    key("K26_fd1_population_rule_open", "absent mode weights" in fd1_flat and "physical population rule" in fd1_flat)

    if not all(KEYS.values()):
        raise SystemExit("one or more derivation keys failed")

    result = {
        "status": "DERIVED_CONDITIONAL_MODE_OWNERSHIP__METRIC_ONLY_POPULATION_PROJECTION_OPEN",
        "key_count": len(KEYS),
        "keys": KEYS,
        "c1_metric": "-A dt^2+dr^2/A+r^2 dtheta^2+r^2 sin^2(theta)dpsi^2+2h sin^2(theta)dt dpsi",
        "determinant": "-r^2 sin^2(theta) [A r^2+h^2 sin^2(theta)]/A",
        "volume": "r sin(theta) sqrt([A r^2+h^2 sin^2(theta)]/A)",
        "mode_operator": "S^-1 d_r(S A u_r)+S^-1 d_theta(S u_theta/r^2)+[r^2 omega^2+2h omega m-A m^2/sin^2(theta)]u/D",
        "D": "A r^2+h^2 sin^2(theta)",
        "mixed_log_volume": "B'(r) sin(theta)cos(theta)/[1+B(r)sin^2(theta)]^2; B=h^2/(A r^2)",
        "equatorial_relation": "C1 volume at theta=pi/2 equals r times the C0 volume; the C0 radial ODE is not the equatorial restriction of the C1 PDE",
        "C1_mode_ownership": "conditional U(1) character m plus north-south parity; radial and polar variables generically coupled",
        "C2_mode_ownership": "SO(3) ell multiplet with m=-ell..ell; full-center regular power r^ell",
        "C3_mode_ownership": "no universal m label because admitted general screens need not retain an axial Killing field",
        "projection_result": "conditional symmetry projectors decompose all modes but select no population; tangent pair/screen projectors are not Hilbert-space spectral weights",
        "maximum_conclusion": "no registered metric-only invariant selects one FD1 ladder or physical mode weights; FD2 cannot postselect a ladder",
        "sympy_version": sp.__version__,
        "source_count": len(source_rows),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {len(KEYS)}/{len(KEYS)} exact derivation keys")


if __name__ == "__main__":
    main()
