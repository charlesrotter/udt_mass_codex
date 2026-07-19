#!/usr/bin/env python3
"""Exact Cartan curvature and finite-cell flux for the dynamic reciprocal frame.

The angular seed is locally arbitrary through isothermal coordinates
qbar=exp(2 sigma(u,v))(du^2+dv^2).  This covers an arbitrary smooth local
two-metric, while base-dependent twist/shear remains outside the registered
warped-product representative.
"""

from __future__ import annotations

import json
import platform
from pathlib import Path
from typing import Dict, Tuple

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"
Basis = Tuple[int, ...]
Form = Dict[Basis, sp.Expr]


def simp(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.trigsimp(sp.simplify(value.rewrite(sp.exp))))


def clean(form: Form) -> Form:
    return {basis: value for basis, raw in form.items() if (value := simp(raw)) != 0}


def add(*forms: Form) -> Form:
    result: Form = {}
    for form in forms:
        for basis, value in form.items():
            result[basis] = result.get(basis, sp.S.Zero) + value
    return clean(result)


def scale(value: sp.Expr, form: Form) -> Form:
    return clean({basis: value * coefficient for basis, coefficient in form.items()})


def wedge(left: Form, right: Form) -> Form:
    result: Form = {}
    for a, av in left.items():
        for b, bv in right.items():
            if set(a).intersection(b):
                continue
            inversions = sum(1 for i in a for j in b if i > j)
            basis = tuple(sorted(a + b))
            result[basis] = result.get(basis, sp.S.Zero) + (-1) ** inversions * av * bv
    return clean(result)


def exterior_d(form: Form, coords: tuple[sp.Symbol, ...]) -> Form:
    result: Form = {}
    for basis, coefficient in form.items():
        for index, coordinate in enumerate(coords):
            derivative = sp.diff(coefficient, coordinate)
            if derivative != 0:
                result = add(result, wedge({(index,): derivative}, {basis: sp.S.One}))
    return clean(result)


def require_zero(name: str, value, checks: dict[str, str]) -> None:
    if isinstance(value, dict):
        reduced = clean(value)
        if reduced:
            raise AssertionError(f"{name}: {reduced}")
    elif isinstance(value, sp.MatrixBase):
        reduced = value.applyfunc(simp)
        if any(entry != 0 for entry in reduced):
            raise AssertionError(f"{name}: {reduced}")
    elif simp(value) != 0:
        raise AssertionError(f"{name}: {simp(value)}")
    checks[name] = "PASS"


def form_string(form: Form, coordinate_names: tuple[str, ...] = ("dt", "dphi", "du", "dv")) -> str:
    if not form:
        return "0"
    terms: list[str] = []
    for basis in sorted(form):
        blade = "^".join(coordinate_names[index] for index in basis)
        terms.append(f"({form[basis]})*{blade}")
    return " + ".join(terms)


def main() -> None:
    checks: dict[str, str] = {}
    t, phi, u, v = sp.symbols("t phi u v", real=True)
    coords = (t, phi, u, v)
    c0, L = sp.symbols("c L", positive=True)
    beta = sp.Function("beta")(t)
    sigma = sp.Function("sigma")(u, v)
    psi = phi - beta
    beta_dot = sp.diff(beta, t)

    theta: list[Form] = [
        {(0,): c0 * sp.exp(-(phi + beta))},
        {(0,): -L * sp.exp(psi) * beta_dot, (1,): L * sp.exp(psi)},
        {(2,): sp.exp(psi + sigma)},
        {(3,): sp.exp(psi + sigma)},
    ]
    f = sp.exp(-psi) / L
    bar_omega: Form = {(2,): sp.diff(sigma, v), (3,): -sp.diff(sigma, u)}

    omega: list[list[Form]] = [[{} for _ in range(4)] for _ in range(4)]
    omega[0][1] = scale(-f, theta[0])
    omega[1][0] = scale(-f, theta[0])
    omega[2][1] = scale(f, theta[2])
    omega[1][2] = scale(-f, theta[2])
    omega[3][1] = scale(f, theta[3])
    omega[1][3] = scale(-f, theta[3])
    omega[2][3] = bar_omega
    omega[3][2] = scale(-1, bar_omega)

    for frame_index in range(4):
        torsion = exterior_d(theta[frame_index], coords)
        for other in range(4):
            torsion = add(torsion, wedge(omega[frame_index][other], theta[other]))
        require_zero(f"torsion_{frame_index}", torsion, checks)

    expected_connection = {
        (0, 1): {(0,): -c0 * sp.exp(-2 * phi) / L},
        (1, 2): {(2,): -sp.exp(sigma) / L},
        (1, 3): {(3,): -sp.exp(sigma) / L},
        (2, 3): bar_omega,
    }
    for pair, expected in expected_connection.items():
        require_zero(f"coordinate_spin_connection_{pair[0]}{pair[1]}", add(omega[pair[0]][pair[1]], scale(-1, expected)), checks)

    curvature: list[list[Form]] = [[{} for _ in range(4)] for _ in range(4)]
    for first in range(4):
        for second in range(4):
            value = exterior_d(omega[first][second], coords)
            for middle in range(4):
                value = add(value, wedge(omega[first][middle], omega[middle][second]))
            curvature[first][second] = clean(value)

    angular_laplacian = sp.diff(sigma, u, 2) + sp.diff(sigma, v, 2)
    Kbar = -sp.exp(-2 * sigma) * angular_laplacian
    expected_curvature = {
        (0, 1): {(0, 1): -2 * c0 * sp.exp(-2 * phi) / L},
        (0, 2): {(0, 2): c0 * sp.exp(-2 * phi + sigma) / L**2},
        (0, 3): {(0, 3): c0 * sp.exp(-2 * phi + sigma) / L**2},
        (1, 2): {},
        (1, 3): {},
        (2, 3): {(2, 3): -angular_laplacian - sp.exp(2 * sigma) / L**2},
    }
    for pair, expected in expected_curvature.items():
        require_zero(f"coordinate_curvature_{pair[0]}{pair[1]}", add(curvature[pair[0]][pair[1]], scale(-1, expected)), checks)

    # Equivalent orthonormal-frame expressions.  These show explicitly how
    # reciprocal and intrinsic angular curvature enter the six planes.
    expected_frame_curvature = {
        "Omega01": "-2 f^2 theta0^theta1",
        "Omega02": "+f^2 theta0^theta2",
        "Omega03": "+f^2 theta0^theta3",
        "Omega12": "0",
        "Omega13": "0",
        "Omega23": "exp(-2psi)(Kbar-1/L^2) theta2^theta3",
    }

    # The first Bianchi identity is checked in the pulled-back dynamic frame.
    for first in range(4):
        bianchi: Form = {}
        for second in range(4):
            bianchi = add(bianchi, wedge(curvature[first][second], theta[second]))
        require_zero(f"first_bianchi_{first}", bianchi, checks)

    # The covariant second Bianchi identity is also exact in this arbitrary
    # beta(t), sigma(u,v) representative.
    for first in range(4):
        for second in range(4):
            bianchi = exterior_d(curvature[first][second], coords)
            for middle in range(4):
                bianchi = add(
                    bianchi,
                    wedge(omega[first][middle], curvature[middle][second]),
                    scale(-1, wedge(curvature[first][middle], omega[middle][second])),
                )
            require_zero(f"second_bianchi_{first}{second}", bianchi, checks)

    beta_atoms = {beta, sp.diff(beta, t), sp.diff(beta, t, 2)}
    for pair in expected_connection:
        if any(coefficient.has(*beta_atoms) for coefficient in omega[pair[0]][pair[1]].values()):
            raise AssertionError(f"beta dependence survived in spin connection {pair}")
        checks[f"beta_and_derivatives_cancel_from_coordinate_connection_{pair[0]}{pair[1]}"] = "PASS"
    for pair in expected_curvature:
        if any(coefficient.has(*beta_atoms) for coefficient in curvature[pair[0]][pair[1]].values()):
            raise AssertionError(f"beta dependence survived in curvature {pair}")
        checks[f"beta_and_derivatives_cancel_from_coordinate_curvature_{pair[0]}{pair[1]}"] = "PASS"

    t0, t1, phi0, phi1 = sp.symbols("t0 t1 phi0 phi1", real=True)
    omega01_coefficient = omega[0][1][(0,)]
    curvature01_coefficient = curvature[0][1][(0, 1)]
    boundary_connection_integral = simp(
        (t1 - t0) * omega01_coefficient.subs(phi, phi0)
        - (t1 - t0) * omega01_coefficient.subs(phi, phi1)
    )
    flux01 = simp(sp.integrate(curvature01_coefficient, (phi, phi0, phi1)) * (t1 - t0))
    require_zero("exact_tphi_stokes", boundary_connection_integral - flux01, checks)
    expected_flux01 = c0 * (t1 - t0) * (sp.exp(-2 * phi1) - sp.exp(-2 * phi0)) / L
    require_zero("exact_tphi_flux", flux01 - expected_flux01, checks)

    rapidity = flux01
    # With parallel transport dV+omega V=0 and J01=[[0,1],[1,0]],
    # H=P exp(-integral omega)=exp(-Phi01 J01) on this commuting face.
    boost = sp.Matrix([[sp.cosh(rapidity), -sp.sinh(rapidity)], [-sp.sinh(rapidity), sp.cosh(rapidity)]])
    lorentz_eta = sp.diag(-1, 1)
    require_zero("exact_tphi_holonomy_lorentz", boost.T * lorentz_eta * boost - lorentz_eta, checks)
    require_zero("exact_tphi_holonomy_unit_determinant", boost.det() - 1, checks)

    delta_t, ell2, ell3, phi_star = sp.symbols("Delta_t ell2 ell3 phi_star", real=True)
    time_angular_fluxes = {
        "Phi02_fixed_coframe_gauge": c0 * sp.exp(-2 * phi_star) * delta_t * ell2 / L**2,
        "Phi03_fixed_coframe_gauge": c0 * sp.exp(-2 * phi_star) * delta_t * ell3 / L**2,
    }
    angular_area, euler_chi = sp.symbols("Abar chi", real=True)
    closed_angular_flux = 2 * sp.pi * euler_chi - angular_area / L**2
    zero_flux_area = simp(sp.solve(sp.Eq(closed_angular_flux, 0), angular_area)[0])
    require_zero("closed_angular_zero_flux_area", zero_flux_area - 2 * sp.pi * euler_chi * L**2, checks)

    result = {
        "schema": "udt-accelerating-finite-cell-cartan-1.0",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "checks": checks,
        "representative": {
            "psi": "phi-beta(t)",
            "coframe": {
                "theta0": "c exp(-(phi+beta)) dt",
                "theta1": "L exp(phi-beta)(dphi-beta_dot dt)",
                "theta2": "exp(phi-beta+sigma(u,v)) du",
                "theta3": "exp(phi-beta+sigma(u,v)) dv",
            },
            "angular_seed": "qbar=exp(2sigma(u,v))(du^2+dv^2); Kbar=-exp(-2sigma)(sigma_uu+sigma_vv)",
            "scope": "full six-plane Cartan curvature of the conditional four-dimensional reciprocal warped-product representative; base-dependent angular twist/shear excluded",
        },
        "spin_connection_coordinate_basis": {
            "omega01": form_string(omega[0][1]),
            "omega12": form_string(omega[1][2]),
            "omega13": form_string(omega[1][3]),
            "omega23": form_string(omega[2][3]),
            "beta_dependence": "IN THE CHOSEN PULLED-BACK COFRAME GAUGE, beta and all time derivatives cancel from the fully expanded coordinate one-forms; spin connection coefficients are gauge-dependent",
        },
        "cartan_curvature": {
            "orthonormal_frame": expected_frame_curvature,
            "coordinate_basis": {f"Omega{a}{b}": form_string(curvature[a][b]) for a, b in expected_curvature},
            "beta_dependence": "NO beta_dot OR beta_double_dot CREATES CURVATURE; fully expanded unprimed coordinate two-forms also contain no beta, while orthonormal coefficients and basis separately depend on psi=phi-beta",
            "angular_interaction": "Omega23 combines intrinsic Kbar with the reciprocal warp contribution -1/L^2; Omega02 and Omega03 couple reciprocal time to each angular direction",
            "identities": "TORSION_ZERO; FIRST_BIANCHI_ZERO; SECOND_BIANCHI_ZERO",
        },
        "finite_cell": {
            "tphi_flux_Phi01": "(c/L)(t1-t0)(exp(-2phi1)-exp(-2phi0))",
            "tphi_boundary_connection_integral": "(c/L)(t1-t0)(exp(-2phi1)-exp(-2phi0))",
            "tphi_exact_holonomy": "H01=exp(-Phi01 J01) for dV+omega V=0 and the registered loop orientation; reversing orientation or generator sign reverses the rapidity sign",
            "tphi_holonomy_matrix": [["cosh(Phi01)", "-sinh(Phi01)"], ["-sinh(Phi01)", "cosh(Phi01)"]],
            "time_angular_fluxes": {key: str(value) for key, value in time_angular_fluxes.items()},
            "radial_angular_fluxes": "Phi12=Phi13=0 in this representative",
            "angular_patch_flux": "Phi23=integral_Sigma (Kbar-1/L^2) dAbar",
            "closed_angular_flux": "Phi23=2*pi*chi(Sigma)-Abar/L^2",
            "zero_closed_angular_flux_condition": "Abar=2*pi*chi*L^2; for topology S2 this is Abar=4*pi*L^2",
            "zero_flux_not_imposed": True,
            "beta_dependence": "NONE FOR THE REGISTERED FIXED UNPRIMED COORDINATE FACES; a same-physical-cell comparison must transform the boundaries and preserves holonomy by pullback naturality",
            "cell_semantics": "coordinate faces are symbolic integration domains, not a bootstrap-selected physical UDT cell",
        },
        "holonomy_scope": {
            "exact": "t-phi face only, because its restricted connection uses one commuting boost generator",
            "not_exactly_flux": "generic time-angular and angular finite holonomies require path ordering/non-Abelian Stokes data; raw curvature flux is not a gauge-invariant replacement",
            "small_loop": "H=I+Omega(area bivector)+higher-order terms in a fixed local trivialization",
        },
        "equivalence_adjudication": {
            "acceleration": "PURE_FRAME_IN_THIS_REPRESENTATIVE; beta_dot and beta_double_dot do not generate Cartan curvature or registered fixed-face flux; beta may label the shifted position psi in orthonormal components",
            "finite_cell": "NONZERO CURVATURE/HOLONOMY CAN DISTINGUISH THE UNDERLYING GEOMETRY FROM A PURE FRAME CHANGE",
            "derived_dimensionless_tphi_defect": "Phi01=(c/L)(t1-t0)(exp(-2phi1)-exp(-2phi0))",
            "physical_crossover": "OPEN; no physical cell size, invariant multi-plane norm, or bootstrap-selected threshold is supplied",
            "gr_equivalence": "NOT_ADOPTED_OR_DERIVED",
        },
        "maximum_conclusion": "IN_THE_DECLARED_CONDITIONAL_FOUR_DIMENSIONAL_RECIPROCAL_WARPED_PRODUCT_REPRESENTATIVE_THE_ACCELERATING_FRAME_IS_AN_EXACT_PULLBACK; BETA_DOT_AND_BETA_DOUBLE_DOT_GENERATE_NO_CURVATURE_IN_THE_FULL_SIX_PLANE_CARTAN_CENSUS_OR_REGISTERED_FIXED_FACE_FLUXES; BETA_CAN_STILL_LABEL_SHIFTED_POSITION_IN_ORTHONORMAL_COMPONENTS; THE_TPHI_COORDINATE_CELL_HAS_AN_EXACT_SO11_HOLONOMY_AND_THE_ANGULAR_FLUX_EXACTLY_COMBINES_INTRINSIC_CURVATURE_WITH_MINUS_ONE_OVER_L_SQUARED; A_PHYSICAL_EQUIVALENCE_WINDOW_REMAINS_OPEN_BECAUSE_PHYSICAL_CELL_SIZE_NORM_THRESHOLD_AND_OMITTED_TWIST_SHEAR_SECTORS_ARE_NOT_SELECTED",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
