#!/usr/bin/env python3
"""Independent coordinate-Riemann verifier and fail-closed semantic catches."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "9f12b97349b09f7392edb4bd7204c52cbc597d10"
RESULT = HERE / "DERIVATION_RESULT.json"
VERIFY = HERE / "VERIFICATION_RESULT.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def validate(data: dict) -> None:
    require(data["schema"] == "udt-accelerating-finite-cell-cartan-1.0", "schema changed")
    require(len(data["checks"]) == 49 and all(value == "PASS" for value in data["checks"].values()), "primary check census/failure")
    representative = data["representative"]
    require("full six-plane Cartan curvature" in representative["scope"], "six-plane scope lost")
    require("twist/shear excluded" in representative["scope"], "scope promoted to complete metric")
    connection = data["spin_connection_coordinate_basis"]
    require(connection["beta_dependence"].startswith("IN THE CHOSEN PULLED-BACK COFRAME GAUGE"), "connection gauge scope lost")
    curvature = data["cartan_curvature"]
    require(curvature["beta_dependence"].startswith("NO beta_dot OR beta_double_dot CREATES CURVATURE"), "acceleration curvature invented")
    require("orthonormal coefficients and basis separately depend on psi=phi-beta" in curvature["beta_dependence"], "positional beta dependence hidden")
    require(curvature["orthonormal_frame"]["Omega12"] == "0" and curvature["orthonormal_frame"]["Omega13"] == "0", "zero mixed planes changed")
    require("Kbar-1/L^2" in curvature["orthonormal_frame"]["Omega23"], "angular reciprocal interaction lost")
    cell = data["finite_cell"]
    require(cell["tphi_flux_Phi01"] == "(c/L)(t1-t0)(exp(-2phi1)-exp(-2phi0))", "t-phi flux changed")
    require(cell["beta_dependence"].startswith("NONE FOR THE REGISTERED FIXED UNPRIMED COORDINATE FACES"), "fixed-face beta scope changed")
    require(cell["tphi_exact_holonomy"].startswith("H01=exp(-Phi01 J01)"), "exact commuting holonomy sign/scope lost")
    require(cell["tphi_holonomy_matrix"] == [["cosh(Phi01)", "-sinh(Phi01)"], ["-sinh(Phi01)", "cosh(Phi01)"]], "holonomy matrix sign changed")
    require(cell["cell_semantics"].endswith("not a bootstrap-selected physical UDT cell"), "coordinate cell promoted to physical cell")
    require(cell["closed_angular_flux"] == "Phi23=2*pi*chi(Sigma)-Abar/L^2", "closed angular flux changed")
    require(cell["zero_flux_not_imposed"] is True, "zero angular flux imposed")
    holonomy = data["holonomy_scope"]
    require("require path ordering" in holonomy["not_exactly_flux"], "generic flux promoted to holonomy")
    adjudication = data["equivalence_adjudication"]
    require(adjudication["physical_crossover"].startswith("OPEN"), "physical crossover invented")
    require(adjudication["gr_equivalence"] == "NOT_ADOPTED_OR_DERIVED", "GR equivalence imported")
    require("cell size, invariant multi-plane norm, or bootstrap-selected threshold" in adjudication["physical_crossover"], "missing crossover inputs hidden")


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation unexpectedly passed: {name}")


def main() -> None:
    checks: dict[str, str] = {}
    catches: dict[str, str] = {}
    before = sha256(RESULT)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    replay = subprocess.run(
        [sys.executable, "-B", str(HERE / "derive_finite_cell_cartan.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=240,
        check=False,
    )
    require(replay.returncode == 0, f"primary replay failed: {replay.stderr}")
    require(not replay.stderr, "primary replay emitted stderr")
    require(sha256(RESULT) == before, "primary replay changed result")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    validate(data)
    checks["deterministic_primary_replay_and_contract"] = "PASS"

    # Independent implementation: build a coordinate metric for explicit
    # accelerated beta and non-flat angular sigma, compute Christoffels and
    # Riemann directly, then project Riemann into the orthonormal frame.  This
    # does not use the primary exterior-form connection.
    t, phi, u, v = sp.symbols("t phi u v", real=True)
    coords = (t, phi, u, v)
    c0, L = sp.symbols("c L", positive=True)
    accel, p, q = sp.symbols("accel p q", real=True)
    beta = accel * t**2 / 2
    beta_dot = sp.diff(beta, t)
    sigma = p * u**2 + q * v**2
    psi = phi - beta
    coframe = sp.Matrix([
        [c0 * sp.exp(-(phi + beta)), 0, 0, 0],
        [-L * sp.exp(psi) * beta_dot, L * sp.exp(psi), 0, 0],
        [0, 0, sp.exp(psi + sigma), 0],
        [0, 0, 0, sp.exp(psi + sigma)],
    ])
    lorentz_eta = sp.diag(-1, 1, 1, 1)
    metric = sp.simplify(coframe.T * lorentz_eta * coframe)
    inverse_metric = sp.simplify(metric.inv())
    frame = sp.simplify(coframe.inv())

    gamma = [[[
        sp.simplify(sum(
            inverse_metric[rho, lam] * (
                sp.diff(metric[lam, nu], coords[mu])
                + sp.diff(metric[lam, mu], coords[nu])
                - sp.diff(metric[mu, nu], coords[lam])
            )
            for lam in range(4)
        ) / 2)
        for nu in range(4)] for mu in range(4)] for rho in range(4)]

    riemann_cache: dict[tuple[int, int, int, int], sp.Expr] = {}

    def riemann(rho: int, sig: int, mu: int, nu: int) -> sp.Expr:
        key = (rho, sig, mu, nu)
        if key not in riemann_cache:
            riemann_cache[key] = sp.simplify(
                sp.diff(gamma[rho][nu][sig], coords[mu])
                - sp.diff(gamma[rho][mu][sig], coords[nu])
                + sum(
                    gamma[rho][mu][lam] * gamma[lam][nu][sig]
                    - gamma[rho][nu][lam] * gamma[lam][mu][sig]
                    for lam in range(4)
                )
            )
        return riemann_cache[key]

    def projected(frame_i: int, frame_j: int, mu: int, nu: int) -> sp.Expr:
        return sp.simplify(sum(
            coframe[frame_i, rho] * frame[sig, frame_j] * riemann(rho, sig, mu, nu)
            for rho in range(4)
            for sig in range(4)
        ))

    angular_laplacian = sp.diff(sigma, u, 2) + sp.diff(sigma, v, 2)
    expected = {
        (0, 1, 0, 1): -2 * c0 * sp.exp(-2 * phi) / L,
        (0, 2, 0, 2): c0 * sp.exp(-2 * phi + sigma) / L**2,
        (0, 3, 0, 3): c0 * sp.exp(-2 * phi + sigma) / L**2,
        (2, 3, 2, 3): -angular_laplacian - sp.exp(2 * sigma) / L**2,
    }
    for indices, target in expected.items():
        require(sp.simplify(projected(*indices) - target) == 0, f"independent Riemann projection mismatch {indices}")
    for indices in ((1, 2, 1, 2), (1, 3, 1, 3), (0, 1, 0, 2), (0, 2, 0, 3)):
        require(sp.simplify(projected(*indices)) == 0, f"independent unexpected curvature {indices}")
    checks["independent_accelerated_coordinate_riemann_projection"] = "PASS"

    # Explicitly differentiate the independent Riemann projections with
    # respect to the acceleration parameter.  Zero proves that this witness's
    # velocity/acceleration dependence has cancelled rather than merely being
    # hidden by a numerical substitution.
    for indices in expected:
        require(sp.simplify(sp.diff(projected(*indices), accel)) == 0, f"acceleration survived in independent curvature {indices}")
    checks["independent_acceleration_parameter_cancellation"] = "PASS"

    # Independent finite t-phi Stokes/holonomy computation.
    t0, t1, phi0, phi1 = sp.symbols("t0 t1 phi0 phi1", real=True)
    omega01 = -c0 * sp.exp(-2 * phi) / L
    boundary = sp.simplify((t1 - t0) * (omega01.subs(phi, phi0) - omega01.subs(phi, phi1)))
    # d(omega01 dt)=-partial_phi(omega01) dt^dphi.
    flux = sp.simplify(sp.integrate(-sp.diff(omega01, phi), (phi, phi0, phi1)) * (t1 - t0))
    require(sp.simplify(boundary - flux) == 0, "independent t-phi Stokes mismatch")
    boost = sp.Matrix([[sp.cosh(flux), -sp.sinh(flux)], [-sp.sinh(flux), sp.cosh(flux)]])
    require(sp.simplify(boost.T * sp.diag(-1, 1) * boost - sp.diag(-1, 1)) == sp.zeros(2), "independent exact boost holonomy failed")
    checks["independent_exact_commuting_tphi_holonomy"] = "PASS"

    # Independent angular flux algebra and non-uniqueness of zero integrated
    # flux: zero fixes area-average curvature, not pointwise roundness.
    area, chi = sp.symbols("A chi", real=True)
    closed_flux = 2 * sp.pi * chi - area / L**2
    require(sp.solve(sp.Eq(closed_flux, 0), area) == [2 * sp.pi * L**2 * chi], "independent closed angular flux mismatch")
    # Take any nonround S2 seed with area A0 and a nonzero difference deltaK
    # between two Gaussian-curvature values. A constant rescaling to area
    # 4*pi*L^2 makes Phi23 zero, while the curvature difference remains
    # nonzero. Hence the integrated condition cannot enforce roundness.
    area0 = sp.symbols("A0", positive=True)
    delta_k = sp.symbols("deltaK", nonzero=True)
    scale_sq = 4 * sp.pi * L**2 / area0
    require(sp.simplify(4 * sp.pi - scale_sq * area0 / L**2) == 0, "scaled nonround S2 zero-flux witness failed")
    require(sp.simplify(delta_k / scale_sq) != 0, "nonround curvature contrast vanished under scaling")
    checks["independent_angular_flux_and_nonuniqueness"] = "PASS"

    inventory_before = sha256(HERE / "SOURCE_INVENTORY.tsv")
    inventory_run = subprocess.run(
        [sys.executable, "-B", str(HERE / "build_source_inventory.py")],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=90,
        check=False,
    )
    require(inventory_run.returncode == 0, f"source replay failed: {inventory_run.stderr}")
    require(sha256(HERE / "SOURCE_INVENTORY.tsv") == inventory_before, "source inventory changed")
    sources = read_tsv(HERE / "SOURCE_INVENTORY.tsv")
    require(len(sources) == 13 and len({row["path"] for row in sources}) == 13, "source census mismatch")
    checks["source_inventory_replay"] = "PASS"

    components = read_tsv(HERE / "CARTAN_CELL_LEDGER.tsv")
    statuses = read_tsv(HERE / "STATUS_LEDGER.tsv")
    require(len(components) == 18 and len({row["id"] for row in components}) == 18, "component ledger mismatch")
    require(len(statuses) == 14 and len({row["id"] for row in statuses}) == 14, "status ledger mismatch")
    require(next(row for row in statuses if row["id"] == "S11")["status"] == "OPEN", "crossover promoted")
    checks["ledger_coverage"] = "PASS"

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    flat_report = " ".join(report.split()).casefold()
    for phrase in (
        "acceleration disappears even more completely",
        "all six independent Cartan curvature planes",
        "The signed rapidity is",
        "does not select a physical cell size",
        "zero integrated angular flux does not select a round sphere",
        "not generally the finite holonomy",
        "base-dependent angular twist and shear remain outside",
        "No GR equivalence principle was used",
    ):
        require(phrase.casefold() in flat_report, f"report disclosure missing: {phrase}")
    for forbidden in (
        "UDT equivalence principle is derived",
        "gravity and acceleration are globally identical",
        "L is X_max",
        "the angular sector must be a round sphere",
        "curvature flux equals holonomy in every cell",
        "the complete UDT metric",
        "the action is selected",
    ):
        require(forbidden not in report, f"forbidden promotion: {forbidden}")
    checks["report_contract"] = "PASS"

    adversarial = (HERE / "INTERNAL_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    for phrase in (
        "Review status: `REVISE`, then corrected.",
        "H_{01}=\\exp(-\\Phi_{01}J_{01})",
        "positional beta versus beta derivatives",
        "coordinate cell versus physical UDT cell",
        "fresh external context was not authorized or run",
    ):
        require(phrase.casefold() in adversarial.casefold(), f"adversarial correction missing: {phrase}")
    checks["internal_adversarial_corrections_recorded"] = "PASS"

    changed = subprocess.check_output(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, text=True).splitlines()
    forbidden_controls = {"LIVE.md", "HANDOFF.md", "INDEX.md", "README.md", "MEMORY.md", "CANON.md"}
    require(not forbidden_controls.intersection(changed), f"forbidden controls changed: {forbidden_controls.intersection(changed)}")
    checks["no_control_or_canon_edits"] = "PASS"

    mutation = copy.deepcopy(data)
    mutation["spin_connection_coordinate_basis"]["beta_dependence"] = "beta_double_dot survives"
    expect_failure("acceleration_connection_invariant_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["cartan_curvature"]["beta_dependence"] = "beta_double_dot curvature"
    expect_failure("acceleration_curvature_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["cartan_curvature"]["orthonormal_frame"]["Omega23"] = "Kbar only"
    expect_failure("reciprocal_angular_interaction_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["cartan_curvature"]["orthonormal_frame"]["Omega12"] = "nonzero"
    expect_failure("zero_mixed_plane_changed", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["finite_cell"]["beta_dependence"] = "depends on beta_double_dot"
    expect_failure("beta_dependent_flux_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["finite_cell"]["zero_flux_not_imposed"] = False
    expect_failure("zero_angular_flux_imposed", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["holonomy_scope"]["not_exactly_flux"] = "all fluxes equal holonomy"
    expect_failure("generic_flux_promoted_to_holonomy", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["equivalence_adjudication"]["physical_crossover"] = "DERIVED"
    expect_failure("crossover_formula_invented", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["equivalence_adjudication"]["gr_equivalence"] = "ADOPTED"
    expect_failure("gr_equivalence_imported", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["representative"]["scope"] = "the complete UDT metric"
    expect_failure("warped_product_scope_promoted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["finite_cell"]["closed_angular_flux"] = "Phi23=0"
    expect_failure("angular_flux_formula_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["finite_cell"]["tphi_exact_holonomy"] = "unknown"
    expect_failure("exact_commuting_holonomy_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["finite_cell"]["tphi_flux_Phi01"] = "0"
    expect_failure("tphi_flux_deleted", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["finite_cell"]["tphi_holonomy_matrix"] = [["cosh(Phi01)", "sinh(Phi01)"], ["sinh(Phi01)", "cosh(Phi01)"]]
    expect_failure("parallel_transport_sign_reversed", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["finite_cell"]["cell_semantics"] = "the physical UDT cell"
    expect_failure("coordinate_cell_promoted_to_physical", lambda: validate(mutation), catches)
    mutation = copy.deepcopy(data)
    mutation["cartan_curvature"]["beta_dependence"] = "NO beta_dot OR beta_double_dot CREATES CURVATURE; beta itself is absent from every orthonormal coefficient"
    expect_failure("positional_beta_dependence_hidden", lambda: validate(mutation), catches)

    output = {
        "schema": "udt-accelerating-finite-cell-cartan-verification-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "checks": checks,
        "catch_proofs": catches,
        "independent_witnesses": {
            "beta": "accel*t^2/2",
            "sigma": "p*u^2+q*v^2",
            "riemann_projection": "direct coordinate Christoffel/Riemann then tetrad projection",
            "acceleration_derivative_of_curvature": "0",
            "tphi_stokes_flux": str(flux),
            "tphi_holonomy_group": "SO(1,1)",
            "closed_angular_flux": str(closed_flux),
            "zero_flux_area": "2*pi*chi*L^2",
            "zero_flux_nonround_witness": "any nonround S2 metric rescaled to area 4*pi*L^2 retains nonconstant K and has Phi23=0",
        },
        "result": "PASS",
    }
    VERIFY.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
