#!/usr/bin/env python3
"""Cold independent verifier for the conditional F01 inverse wall surface.

This verifier does not import or execute any primary package code.  It checks
the frozen Git objects, reconstructs the response problems by DOP853 shooting,
and corroborates the rank-one inertia transition with a separate linear-FEM
assembly.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import subprocess
from pathlib import Path

import mpmath as mp
import numpy as np
import scipy
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.linalg import eigvalsh
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
BASE = "46c763770f3f71376a0e57338c276ed3981ce36b"
SOURCE_ROOTS = (
    "udt_f01_lambda_schur_check_2026-08-01/",
    "udt_p4_stability_slice_2026-07-30/",
    "udt_p4_boundary_action_gate_2026-07-30/",
    "udt_stability_derivation_closure_sweep_2026-08-01/",
    "udt_stability_action_boundary_bridge_audit_2026-08-01/",
)
SOURCE_FILES = {
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "PONDER_MATH_ELEGANCE_2026-07-31.md",
}
ALPHAS = (0.25, 0.5, 0.75, 1.0)
FEM_ELEMENTS = 600
COMMAND = (
    "python3 "
    "udt_f01_second_wall_inverse_stability_2026-08-01/"
    "cold_verify_inverse_surface.py"
)


def run_git(*args: str, binary: bool = False):
    completed = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True,
        text=not binary,
    )
    return completed.stdout


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def decimal(value: float, digits: int = 17) -> str:
    return format(float(value), f".{digits}g")


def selected_source_paths() -> list[str]:
    raw = run_git("ls-tree", "-r", "--name-only", "-z", BASE, binary=True)
    paths = [token.decode("utf-8") for token in raw.split(b"\0") if token]
    return sorted(
        path for path in paths
        if path in SOURCE_FILES or any(path.startswith(root) for root in SOURCE_ROOTS)
    )


def verify_frozen_sources() -> dict[str, object]:
    selected = selected_source_paths()
    if len(selected) != 135:
        raise AssertionError(f"expected 135 frozen sources, found {len(selected)}")

    with (PKG / "SOURCE_INVENTORY.tsv").open(encoding="utf-8", newline="") as handle:
        inventory = list(csv.DictReader(handle, delimiter="\t"))
    inventory_paths = [row["path"] for row in inventory]
    if inventory_paths != selected:
        raise AssertionError("source inventory does not equal independent Git-tree selection")

    total_bytes = 0
    checked = 0
    for row in inventory:
        path = row["path"]
        blob = run_git("rev-parse", f"{BASE}:{path}").strip()
        payload = run_git("cat-file", "blob", blob, binary=True)
        digest = sha256(payload)
        if (
            blob != row["git_blob"]
            or len(payload) != int(row["bytes"])
            or digest != row["sha256"]
        ):
            raise AssertionError(f"frozen source identity mismatch: {path}")
        working_payload = (ROOT / path).read_bytes()
        if sha256(working_payload) != digest:
            raise AssertionError(f"working source differs from frozen source: {path}")
        checked += 1
        total_bytes += len(payload)

    manifest = (PKG / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    expected_manifest = [f"{row['sha256']}  {row['path']}" for row in inventory]
    if manifest != expected_manifest:
        raise AssertionError("source manifest differs from independent inventory check")

    return {
        "base_commit": BASE,
        "selected_paths": len(selected),
        "identities_checked": checked,
        "bytes_checked": total_bytes,
        "inventory_matches_git_tree": True,
        "git_blobs_bytes_sha256_match": True,
        "working_tree_bytes_match_frozen_base": True,
        "manifest_matches_inventory": True,
    }


def w_value(x, s):
    return 0.5 * s * s * x * x + (s * s - s) * x + 1 + 0.5 * s * s - s


def wp_value(x, s):
    return s * s * x + s * s - s


def root_function(s: float) -> float:
    return quad(
        lambda x: np.log(w_value(x, s)), -1.0, 1.0,
        epsabs=2.0e-13, epsrel=2.0e-13, limit=300,
    )[0]


def symbolic_cold_controls() -> dict[str, bool]:
    beta, j, s, tau = sp.symbols("beta j s tau", positive=True)
    tau_beta = s**2 * beta / (1 + beta * j)
    beta_inverse = tau / (s**2 - tau * j)
    controls = {
        "tau_beta_zero": sp.simplify(tau_beta.subs(beta, 0)) == 0,
        "tau_beta_derivative_positive_form": (
            sp.simplify(sp.diff(tau_beta, beta) - s**2 / (1 + beta * j) ** 2) == 0
        ),
        "tau_beta_hard_pin_limit": sp.simplify(sp.limit(tau_beta, beta, sp.oo) - s**2 / j) == 0,
        "tau_beta_inverse": sp.simplify(tau_beta.subs(beta, beta_inverse) - tau) == 0,
    }
    if not all(controls.values()):
        raise AssertionError(controls)
    return controls


def shoot_response(s: float, domain: str, response: str):
    if response not in {"u", "phi"}:
        raise ValueError(response)

    def ode(x, y, forced: bool):
        w = w_value(x, s)
        if forced and response == "u":
            source = s * s * (1 - (1 - np.log(w)) / w)
        elif forced:
            source = 1 / w
        else:
            source = 0.0
        return np.asarray((y[1] / w, -s * s * y[0] / w - source))

    options = {
        "rtol": 2.0e-13,
        "atol": 2.0e-14,
        "method": "DOP853",
        "dense_output": True,
        "max_step": 0.01,
    }
    particular = solve_ivp(
        lambda x, y: ode(x, y, True), (-1.0, 1.0), (0.0, 0.0), **options
    )
    homogeneous = solve_ivp(
        lambda x, y: ode(x, y, False), (-1.0, 1.0), (0.0, 1.0), **options
    )
    if not particular.success or not homogeneous.success:
        raise AssertionError("DOP853 shooting integration failed")

    right_w = w_value(1.0, s)
    right_wp = wp_value(1.0, s)
    if domain == "DIRICHLET":
        scale = -particular.y[0, -1] / homogeneous.y[0, -1]
    elif domain == "FREE":
        extra = np.log(right_w) * right_wp if response == "u" else 0.0
        numerator = particular.y[1, -1] + right_wp * particular.y[0, -1] + extra
        denominator = homogeneous.y[1, -1] + right_wp * homogeneous.y[0, -1]
        scale = -numerator / denominator
    else:
        raise ValueError(domain)

    def solution(x):
        return particular.sol(x) + scale * homogeneous.sol(x)

    left_residual = float(solution(-1.0)[0])
    if domain == "DIRICHLET":
        right_residual = float(solution(1.0)[0])
    else:
        value = solution(1.0)
        extra = np.log(right_w) * right_wp if response == "u" else 0.0
        right_residual = float(value[1] + right_wp * value[0] + extra)

    return solution, {
        "particular_nfev": particular.nfev,
        "homogeneous_nfev": homogeneous.nfev,
        "left_boundary_residual": decimal(left_residual),
        "right_boundary_residual": decimal(right_residual),
    }


def ell_density(x: float, s: float, state) -> float:
    w = w_value(x, s)
    logw = np.log(w)
    value = state[0]
    derivative = state[1] / w
    return (
        s * s * value * (1 + logw * (1 - 1 / w))
        + logw * wp_value(x, s) * derivative
    )


def reconstruct_branch(s: float, j_value: float, c_value: float, domain: str) -> dict[str, object]:
    u, u_meta = shoot_response(s, domain, "u")
    phi, phi_meta = shoot_response(s, domain, "phi")
    integrate = lambda function: quad(
        function, -1.0, 1.0, epsabs=2.0e-12, epsrel=2.0e-12, limit=300
    )[0]

    n_green = integrate(lambda x: -u(x)[0] / w_value(x, s))
    n_direct = integrate(lambda x: ell_density(x, s, phi(x)))
    m_direct = integrate(lambda x: phi(x)[0] / w_value(x, s))
    ell_u = integrate(lambda x: ell_density(x, s, u(x)))
    s_zero = c_value + ell_u

    right_w = w_value(1.0, s)
    if domain == "DIRICHLET":
        d_value = 2 / (s - 1)
    else:
        d_value = 2 * (4 * s * s - 3 * s + 1) / ((2 * s - 1) * right_w)
    m_formula = -(j_value + d_value) / (s * s)
    tau_infinity = s * s / j_value
    tau_critical = -1 / m_formula
    t_critical = tau_critical / tau_infinity

    samples = {}
    for alpha in ALPHAS:
        t_value = t_critical + alpha * (1 - t_critical)
        tau = t_value * tau_infinity
        schur = s_zero + tau * n_green * n_green / (1 + tau * m_formula)
        alpha_label = {0.25: "1/4", 0.5: "1/2", 0.75: "3/4", 1.0: "1/1"}[alpha]
        samples[alpha_label] = {
            "t": decimal(t_value),
            "tau": decimal(tau),
            "S_nu": decimal(schur),
            "eta_critical": decimal(-schur),
            "representative_eta_mu_critical": decimal(-schur / 4),
        }

    if abs(n_direct - n_green) > 2.0e-10:
        raise AssertionError(f"direct/Green n disagreement: {domain}")
    if abs(m_direct - m_formula) > 2.0e-10:
        raise AssertionError(f"direct/formula m disagreement: {domain}")
    if not (0 < t_critical < 1 and n_green < 0 and s_zero > 0):
        raise AssertionError(f"branch sign/crossing failure: {domain}")

    crossing_determinant = -(n_green * n_green)
    if crossing_determinant >= 0:
        raise AssertionError(f"finite-eta crossing obstruction lost: {domain}")

    return {
        "DOP853": {"u": u_meta, "phi": phi_meta},
        "d": decimal(d_value),
        "m_direct": decimal(m_direct),
        "m_formula": decimal(m_formula),
        "m_absolute_difference": decimal(abs(m_direct - m_formula)),
        "n_green": decimal(n_green),
        "n_direct": decimal(n_direct),
        "n_absolute_difference": decimal(abs(n_green - n_direct)),
        "S0": decimal(s_zero),
        "tau_critical": decimal(tau_critical),
        "tau_infinity": decimal(tau_infinity),
        "t_critical": decimal(t_critical),
        "crossing_two_by_two_determinant": decimal(crossing_determinant),
        "finite_eta_crossing_obstruction": True,
        "samples": samples,
    }


def assemble_fem(s: float, domain: str):
    nodes = np.linspace(-1.0, 1.0, FEM_ELEMENTS + 1)
    width = nodes[1] - nodes[0]
    matrix = np.zeros((FEM_ELEMENTS + 1, FEM_ELEMENTS + 1))
    g_vector = np.zeros(FEM_ELEMENTS + 1)
    quad_nodes, quad_weights = np.polynomial.legendre.leggauss(5)

    for element in range(FEM_ELEMENTS):
        left = nodes[element]
        right = nodes[element + 1]
        midpoint = (left + right) / 2
        jacobian = width / 2
        local_matrix = np.zeros((2, 2))
        local_g = np.zeros(2)
        for point, weight in zip(quad_nodes, quad_weights):
            x = midpoint + jacobian * point
            basis = np.asarray(((right - x) / width, (x - left) / width))
            derivative = np.asarray((-1 / width, 1 / width))
            w = w_value(x, s)
            local_matrix += weight * jacobian * (
                w * np.outer(derivative, derivative)
                - (s * s / w) * np.outer(basis, basis)
            )
            local_g += weight * jacobian * basis / w
        matrix[element:element + 2, element:element + 2] += local_matrix
        g_vector[element:element + 2] += local_g

    if domain == "FREE":
        matrix[-1, -1] += wp_value(1.0, s)
        retained = np.arange(1, FEM_ELEMENTS + 1)
    else:
        retained = np.arange(1, FEM_ELEMENTS)
    return matrix[np.ix_(retained, retained)], g_vector[retained]


def fem_inertia_checks(s: float, domain: str, tau_critical: float, tau_infinity: float):
    matrix, g_vector = assemble_fem(s, domain)
    points = {
        "below": 0.9 * tau_critical,
        "near_below": (1 - 1.0e-3) * tau_critical,
        "near_above": tau_critical + 1.0e-3 * (tau_infinity - tau_critical),
        "above": 0.5 * (tau_critical + tau_infinity),
        "R06_endpoint": tau_infinity,
    }
    rows = {}
    for name, tau in points.items():
        values = eigvalsh(
            matrix + tau * np.outer(g_vector, g_vector),
            subset_by_index=(0, 2), driver="evr",
        )
        negative_count = int(np.count_nonzero(values < 0))
        expected = 1 if name in {"below", "near_below"} else 0
        if negative_count != expected:
            raise AssertionError(
                f"FEM inertia mismatch: {domain} {name}: {negative_count} != {expected}"
            )
        rows[name] = {
            "tau": decimal(tau),
            "lowest_three_matrix_eigenvalues": [decimal(value) for value in values],
            "negative_count": negative_count,
            "expected_negative_count": expected,
        }
    return {
        "elements": FEM_ELEMENTS,
        "quadrature_points_per_element": 5,
        "role": "independent corroboration; analytic rank-one inertia is load-bearing",
        "points": rows,
    }


def interval_contains(value: float, interval) -> bool:
    number = mp.mpf(decimal(value))
    return mp.mpf(interval[0]) <= number <= mp.mpf(interval[1])


def compare_primary(cold: dict[str, object]) -> dict[str, object]:
    certificate = json.loads((PKG / "PRIMARY_CERTIFICATE.json").read_text(encoding="utf-8"))
    result = json.loads((PKG / "RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((PKG / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    checks: dict[str, bool] = {
        "repaired_control_count_15": result.get("computed_controls_passed") == 15,
        "repaired_semantic_catch_count_at_least_11": (
            isinstance(verification.get("semantic_catches_passed"), int)
            and verification["semantic_catches_passed"] >= 11
            and verification.get("semantic_catches_total") == verification["semantic_catches_passed"]
        ),
        "primary_outcome_unchanged": (
            result.get("primary_outcome")
            == "TWO_PARAMETER_CONDITIONAL_STABILITY_THRESHOLD_SURFACE_DERIVED"
        ),
        "tau_eta_not_selected": result.get("tau_eta_selected") is False,
        "complete_hessian_not_claimed": result.get("complete_wall_hessian_covered") is False,
    }
    for domain in ("DIRICHLET", "FREE"):
        cold_branch = cold["branches"][domain]
        primary_branch = certificate["branches"][domain]
        prefix = domain.lower()
        checks[f"{prefix}_J_in_primary_interval"] = interval_contains(
            float(cold["J_closed"]), primary_branch["fine"]["J"]
        )
        checks[f"{prefix}_S0_in_primary_interval"] = interval_contains(
            float(cold_branch["S0"]), primary_branch["fine"]["S0"]
        )
        checks[f"{prefix}_n_in_primary_interval"] = interval_contains(
            float(cold_branch["n_green"]), primary_branch["fine"]["n_green"]
        )
        checks[f"{prefix}_tcrit_in_primary_interval"] = interval_contains(
            float(cold_branch["t_critical"]), primary_branch["t_critical_interval"]
        )
        checks[f"{prefix}_taucrit_in_primary_interval"] = interval_contains(
            float(cold_branch["tau_critical"]), primary_branch["tau_critical_interval"]
        )
        checks[f"{prefix}_tauinf_in_primary_interval"] = interval_contains(
            float(cold_branch["tau_infinity"]), primary_branch["tau_infinity_interval"]
        )
        primary_samples = {row["alpha"]: row for row in primary_branch["samples"]}
        for alpha, cold_sample in cold_branch["samples"].items():
            checks[f"{prefix}_eta_{alpha}_in_primary_interval"] = interval_contains(
                float(cold_sample["eta_critical"]),
                primary_samples[alpha]["eta_critical_interval"],
            )
    if not all(checks.values()):
        failed = [name for name, value in checks.items() if not value]
        raise AssertionError(f"cold/primary disagreement: {failed}")
    return {
        "all_checks_pass": True,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "checks": checks,
        "primary_code_imported_or_executed": False,
        "independence_caveat": (
            "Primary midpoint verification is a separately coded same-formula reconstruction; "
            "the DOP853/FEM cold paths supply the distinct-method check."
        ),
    }


def main() -> None:
    sources = verify_frozen_sources()
    controls = symbolic_cold_controls()
    left_value = root_function(1.68102)
    right_value = root_function(1.68103)
    if not (left_value < 0 < right_value):
        raise AssertionError("root bracket sign lost")
    s = brentq(root_function, 1.68102, 1.68103, xtol=5.0e-15)
    j_closed = 2 / s * (np.arctan(2 * s - 1) + np.pi / 4)
    j_quadrature = quad(
        lambda x: 1 / w_value(x, s), -1.0, 1.0,
        epsabs=2.0e-13, epsrel=2.0e-13,
    )[0]
    c_value = quad(
        lambda x: s * s * np.log(w_value(x, s)) ** 2 * (1 - 1 / w_value(x, s)),
        -1.0, 1.0, epsabs=2.0e-12, epsrel=2.0e-12,
    )[0]

    branches = {
        domain: reconstruct_branch(s, j_closed, c_value, domain)
        for domain in ("DIRICHLET", "FREE")
    }
    for domain, branch in branches.items():
        branch["FEM"] = fem_inertia_checks(
            s, domain, float(branch["tau_critical"]), float(branch["tau_infinity"])
        )

    raw: dict[str, object] = {
        "command": COMMAND,
        "scope": (
            "conditional F01 local massive crease root; both owned p endpoint domains; "
            "trace-aligned beta/tau and eta slice only"
        ),
        "method": {
            "source_identity": "independent Git tree/blob/byte/SHA-256 reconstruction",
            "root": "SciPy adaptive quadrature plus Brent bracket solve",
            "responses": "independent first-order DOP853 particular-plus-homogeneous shooting",
            "overlaps": "adaptive quadrature; n evaluated by direct ell(phi) and Green -int(u/w)",
            "inertia": "piecewise-linear FEM with five-point Gauss element quadrature",
            "symbolic": "independent SymPy beta/tau endpoint, monotonicity, limit, and inverse checks",
        },
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
            "mpmath": mp.__version__,
        },
        "sources": sources,
        "symbolic_controls": controls,
        "root_bracket": {
            "interval": ["1.68102", "1.68103"],
            "left_value": decimal(left_value),
            "right_value": decimal(right_value),
            "central_root": decimal(s),
        },
        "J_closed": decimal(j_closed),
        "J_quadrature": decimal(j_quadrature),
        "J_absolute_difference": decimal(abs(j_closed - j_quadrature)),
        "C": decimal(c_value),
        "formulas": {
            "tau_beta": "s^2*beta/(1+beta*J)",
            "tau_infinity": "s^2/J",
            "tau_critical": "-1/m",
            "S_nu": "S0+tau*n^2/(1+tau*m)",
            "eta_critical": "-S_nu",
            "representative_eta_mu": "eta/4 for a_F=a_Fprime=2",
            "crossing_block_determinant": "-n^2",
        },
        "branches": branches,
        "conclusion_ceiling": (
            "conditional inverse target in one trace-aligned wall-Hessian slice only; "
            "no wall response, boundary, action, carrier, source, matter, persistence, mass, "
            "or bootstrap law selected"
        ),
    }
    raw["primary_agreement"] = compare_primary(raw)

    historical_repairs = [
        "derive the finite aligned beta elimination and tau(beta), rather than merely drawing an interpolation",
        "state that the penalized angular object is a trace difference so an absolute one-wall shift is not mistaken for a penalty",
        "record the cold distinct-method m, n, crossing, threshold, and FEM checks",
        "describe primary mutation catches as semantic/schema checks rather than raw-Hessian independence",
        "add cold artifacts before building the final package manifest",
    ]
    result = {
        "status": "PASS-WITH-CAVEATS",
        "mathematical_status_after_beta_repair": "PASS",
        "historical_verdict_preserved": True,
        "source_identity": "PASS_135_OF_135",
        "symbolic_controls": f"PASS_{len(controls)}_OF_{len(controls)}",
        "DOP853_BVP_and_overlap_checks": "PASS_BOTH_DOMAINS",
        "FEM_inertia_checks": "PASS_BELOW_NEAR_ABOVE_BOTH_DOMAINS",
        "current_repaired_primary_evidence_agrees": True,
        "primary_agreement_checks": raw["primary_agreement"]["checks_passed"],
        "primary_code_imported_or_executed": False,
        "historical_repairs_requested": historical_repairs,
        "remaining_before_bank_at_cold_return": [
            "link this cold review/result from the package report and replace future-tense wording",
            "build and verify the package manifest only after all cold/repair artifacts are final",
        ],
        "conclusion_ceiling": raw["conclusion_ceiling"],
    }

    (PKG / "COLD_RAW.json").write_text(
        json.dumps(raw, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (PKG / "COLD_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": result["status"],
        "mathematical_status_after_beta_repair": result["mathematical_status_after_beta_repair"],
        "sources": result["source_identity"],
        "primary_agreement_checks": result["primary_agreement_checks"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
