#!/usr/bin/env python3
"""Exact finite controls, not a PDE solve or a proof of the general local claims.

SymPy is a symbolic mathematical method. Every metric, field, patch and number
below is a declared mathematical witness, not selected physical input. Generated
artifacts are confined to this candidate directory. No accepted source is edited.
"""

import copy
import hashlib
import itertools
import json
import platform
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CHECKS = {}


def check(name, actual, expected):
    actual, expected = sp.sympify(actual), sp.sympify(expected)
    passed = sp.simplify(sp.trigsimp(actual - expected)) == 0
    CHECKS[name] = {
        "actual": str(actual), "expected": str(expected), "pass": bool(passed)
    }
    if not passed:
        raise AssertionError(f"{name}: {actual} != {expected}")


def exterior_derivative(beta, coords):
    return {
        (i, j): sp.simplify(sp.diff(beta[j], coords[i]) - sp.diff(beta[i], coords[j]))
        for i, j in itertools.combinations(range(len(coords)), 2)
    }


def frobenius_components(beta, coords):
    db = exterior_derivative(beta, coords)
    return {
        (i, j, k): sp.trigsimp(beta[i] * db[j, k] - beta[j] * db[i, k]
                             + beta[k] * db[i, j])
        for i, j, k in itertools.combinations(range(len(coords)), 3)
    }


def acceleration(metric, vector, coords):
    inv = metric.inv()
    dim = len(coords)
    return sp.Matrix([
        sp.simplify(
            sum(vector[b] * sp.diff(vector[a], coords[b]) for b in range(dim))
            + sum(vector[b] * vector[c] * inv[a, d] * (
                sp.diff(metric[d, c], coords[b]) + sp.diff(metric[d, b], coords[c])
                - sp.diff(metric[b, c], coords[d])) / 2
                for b in range(dim) for c in range(dim) for d in range(dim))
        ) for a in range(dim)
    ])


def components_zero(name, vector):
    for i, value in enumerate(vector):
        check(f"{name}_{i}", value, 0)


def collect_checks():
    t, x, y, z = sp.symbols("t x y z", real=True)
    coords = (t, x, y, z)
    eta = sp.diag(-1, 1, 1, 1)
    plane = sp.Matrix([1, 0, 0, 1])
    phase = z - t
    dphase = sp.Matrix([sp.diff(phase, q) for q in coords])
    components_zero("plane_gradient_alignment", eta * plane - dphase)
    check("plane_null", (plane.T * eta * plane)[0], 0)
    components_zero("plane_affine", acceleration(eta, plane, coords))
    theta, r = sp.symbols("theta r", real=True)
    plane_map = sp.Matrix([r, x, y, r + theta])
    screen = plane_map.jacobian([x, y])
    check("plane_screen_det", (screen.T * eta * screen).det(), 1)
    check("plane_phase_on_flow", phase.subs(dict(zip(coords, plane_map)), simultaneous=True), theta)
    check("plane_flow_jacobian_abs_squared", plane_map.jacobian([theta, x, y, r]).det()**2, 1)

    scale = 1 + x**2
    scaled = scale * plane
    beta = eta * scaled
    check("scaled_null", (scaled.T * eta * scaled)[0], 0)
    components_zero("scaled_affine", acceleration(eta, scaled, coords))
    db = exterior_derivative(beta, coords)
    check("scaled_dbeta_xz", db[1, 3], 2*x)
    check("scaled_not_closed_witness_x1", db[1, 3].subs(x, 1), 2)
    for key, value in frobenius_components(beta, coords).items():
        check("scaled_frobenius_" + "".join(map(str, key)), value, 0)
    components_zero("integrating_factor_alignment", beta/scale - dphase)

    twist = sp.Matrix([1, sp.cos(z), sp.sin(z), 0])
    check("twisting_null", (twist.T * eta * twist)[0], 0)
    components_zero("twisting_affine", acceleration(eta, twist, coords))
    expected_twist = {(0, 1, 2): 0, (0, 1, 3): -sp.sin(z),
                      (0, 2, 3): sp.cos(z), (1, 2, 3): -1}
    for key, value in frobenius_components(eta * twist, coords).items():
        check("twist_wedge_" + "".join(map(str, key)), value, expected_twist[key])
    point_twist = sp.Matrix([1, sp.cos(z**2), sp.sin(z**2), 0])
    point_components = frobenius_components(eta * point_twist, coords)
    check("pointwise_not_neighborhood_xyz", point_components[1, 2, 3], -2*z)
    for key, value in point_components.items():
        check("pointwise_zero_" + "".join(map(str, key)), value.subs(z, 0), 0)
    check("nearby_twist_nonzero", point_components[1, 2, 3].subs(z, sp.Rational(1, 10)), -sp.Rational(1, 5))

    nonlinear_phase = phase + phase**3
    nonlinear_covector = sp.Matrix([sp.diff(nonlinear_phase, q) for q in coords])
    nonlinear_k = eta.inv() * nonlinear_covector
    components_zero("nonlinear_aligned", nonlinear_k - (1+3*phase**2)*plane)
    components_zero("nonlinear_affine", acceleration(eta, nonlinear_k, coords))
    check("nonlinear_rest_frequency", -nonlinear_covector[0], 1+3*phase**2)
    check("nonlinear_frequency_ray_derivative", sum(plane[a] * sp.diff(-nonlinear_covector[0], coords[a]) for a in range(4)), 0)

    radius = sp.Symbol("radius", positive=True)
    angle, azimuth = sp.symbols("angle azimuth", real=True)
    sphcoords = (t, radius, angle, azimuth)
    metric = sp.diag(-1, 1, radius**2, radius**2*sp.sin(angle)**2)
    sphphase = radius - t
    covector = sp.Matrix([sp.diff(sphphase, q) for q in sphcoords])
    k = metric.inv() * covector
    check("spherical_null", (k.T * metric * k)[0], 0)
    components_zero("spherical_affine", acceleration(metric, k, sphcoords))
    a, b = sp.symbols("a b", real=True)
    cone_map = sp.Matrix([radius-theta, radius, a, b])
    endpoint_metric = metric.subs(angle, a)
    cone_screen = cone_map.jacobian([a, b])
    gram = cone_screen.T * endpoint_metric * cone_screen
    check("cone_screen_gram_determinant", gram.det(), radius**4 * sp.sin(a)**2)
    # Positive r and 0<a<pi choose the positive square root J=r^2 wrt dOmega.
    check("cone_area_jacobian_squared", sp.simplify(gram.det()/sp.sin(a)**2), radius**4)
    ca, cb = sp.symbols("cut_derivative_a cut_derivative_b", real=True)
    varied_screen = cone_screen + k * sp.Matrix([[ca, cb]])
    varied_gram = varied_screen.T * endpoint_metric * varied_screen
    components_zero("variable_cut_gram_unchanged", varied_gram - gram)
    observers = [sp.Matrix([1, 0, 0, 0]), sp.Matrix([sp.Rational(5, 4), sp.Rational(3, 4), 0, 0])]
    frequencies = []
    for i, observer in enumerate(observers, 1):
        check(f"observer_{i}_norm", (observer.T * metric * observer)[0], -1)
        freq = -(observer.T * covector)[0]
        frequencies.append(freq)
        check(f"observer_{i}_frequency", freq, [1, sp.Rational(1, 2)][i-1])
    density, spacing = sp.symbols("density spacing", positive=True)
    # J_i evaluated from metric Gram; positivity branch fixed above.
    jacobians = [sp.sqrt((gram.det()/sp.sin(a)**2).subs(radius, ri)) for ri in (2, 3)]
    rates = [sp.simplify(frequencies[i] * density / (spacing * jacobians[i])) for i in range(2)]
    check("cone_J1", jacobians[0], 4)
    check("cone_J2", jacobians[1], 9)
    check("cone_Gamma1", rates[0], density/(4*spacing))
    check("cone_Gamma2", rates[1], density/(18*spacing))
    check("cone_direct_transfer", rates[1]/rates[0], sp.Rational(2, 9))
    check("cone_area_ratio", jacobians[1]/jacobians[0], sp.Rational(9, 4))
    check("cone_frequency_ratio", frequencies[1]/frequencies[0], sp.Rational(1, 2))
    check("zero_measure_zero_rate", rates[0].subs(density, 0), 0)

    for name, dens, mass in [("zero", 0, 0), ("unit", 1, 1), ("double", 2, 2), ("same_total_profile", x+sp.Rational(1, 2), 1)]:
        check("measure_mass_"+name, sp.integrate(dens, (x, 0, 1), (y, 0, 1)), mass)
    check("unit_left_half_mass", sp.integrate(1, (x, 0, sp.Rational(1, 2)), (y, 0, 1)), sp.Rational(1, 2))
    check("profile_left_half_mass", sp.integrate(x+sp.Rational(1, 2), (x, 0, sp.Rational(1, 2)), (y, 0, 1)), sp.Rational(3, 8))
    varying_mass = sp.integrate(2+theta, (x, 0, 1), (y, 0, 1))
    check("phase_family_total_mass", varying_mass, 2+theta)
    check("phase_family_mass_derivative", sp.diff(varying_mass, theta), 1)
    check("phase_family_cut_derivative", sp.diff(varying_mass, r), 0)
    xp = sp.Symbol("xprime", real=True)
    relabel = sp.Matrix([sp.exp(theta)*x, y])
    relabel_jacobian = relabel.jacobian([x, y]).det()
    check("relabel_jacobian", relabel_jacobian, sp.exp(theta))
    check("passive_relabel_mass", sp.integrate(1/relabel_jacobian, (xp, 0, sp.exp(theta)), (y, 0, 1)), 1)

    return {
        "metric": "diag(-1,1,r^2,r^2 sin(angle)^2)",
        "phase_covector_tr": ["-1", "1"],
        "radii": ["2", "3"],
        "observers_tr": [["1", "0"], ["5/4", "3/4"]],
        "J": list(map(str, jacobians)), "omega": list(map(str, frequencies)),
        "Gamma_coefficients_for_density_over_spacing": [str(sp.simplify(rate*spacing/density)) for rate in rates],
        "transfer": str(sp.simplify(rates[1]/rates[0])),
        "measure_profile": "x+1/2", "profile_left_half_mass": "3/8",
    }


def sensitivity_checks():
    """Corrupt saved intermediate quantities, not accepted science or source files.

    This checks assertion sensitivity only. It is NOT independent derivation,
    source-code mutation coverage, or a catch proof for every implementation bug.
    """
    defects = {
        "reverse_future_phase_sign": ("observer_1_frequency", "-1"),
        "erase_twist_obstruction": ("twist_wedge_123", "0"),
        "treat_scaled_beta_as_closed": ("scaled_not_closed_witness_x1", "0"),
        "promote_pointwise_to_neighborhood": ("nearby_twist_nonzero", "0"),
        "replace_area_by_radius": ("cone_J2", "3"),
        "omit_clock_frequency_weight": ("cone_direct_transfer", "4/9"),
        "confuse_equal_total_with_equal_measure": ("profile_left_half_mass", "1/2"),
        "omit_passive_relabel_jacobian": ("passive_relabel_mass", "exp(theta)"),
    }
    result = {}
    for name, (target, wrong) in defects.items():
        row = copy.deepcopy(CHECKS[target])
        row["actual"] = wrong
        rejected = sp.simplify(sp.sympify(row["actual"]) - sp.sympify(row["expected"])) != 0
        result[name] = {"target": target, "injected_actual": wrong,
                        "expected": row["expected"], "rejected": bool(rejected)}
        if not rejected:
            raise AssertionError(f"Insensitive target: {name}")
    return result


def main():
    witness = collect_checks()
    result = {
        "status": "PASS_EXACT_FINITE_WITNESSES__CANDIDATE_ONLY",
        "source_head": "0c9c6db68ab08618e750c57c0d8f166434aae043",
        "python": platform.python_version(), "sympy": sp.__version__,
        "check_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "registry_sha256": hashlib.sha256((ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").read_bytes()).hexdigest(),
        "assertion_count": len(CHECKS), "checks": CHECKS,
        "assertion_sensitivity_only": sensitivity_checks(),
        "saved_spherical_witness": witness,
        "limits": ["Finite exact checks, not a proof of Frobenius or general construction",
                   "Same-context implementation, not independent scientific review",
                   "Sensitivity mutations are data-level, not complete code mutation tests",
                   "No floating-point approximation, grid, GPU, field-equation solve, or physical selection"],
    }
    (HERE / "CHECK_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {len(CHECKS)} exact finite-witness assertions")
    print("PASS: 8/8 data-level assertion-sensitivity mutations rejected")
    print("Spherical direct result: J=(4,9), omega=(1,1/2), Gamma ratio=2/9")
    print("CANDIDATE ONLY: analytic general claims and separate-context review not certified by these counts")


if __name__ == "__main__":
    main()
