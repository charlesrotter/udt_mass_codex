"""Finite original-geometric controls; see CHECK_PLAN.md, no numerical solve."""
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp

l, lam, c, d, a = sp.symbols('l lam c d a', real=True)


def jet(expr, variable, order):
    return sp.series(expr, variable, 0, order).removeO().expand()


def zero(expr, name):
    residual = sp.simplify(expr)
    if residual != 0:
        raise AssertionError((name, residual))
    return str(residual)


# The original dS2(1) x R2 metric has conserved spatial ray momenta.
t_lam = lam - c**2 * lam**3 / 6
x_lam = c * (lam - lam**3 / 3)
rho_lam = sp.sqrt(1-c**2) * lam
checks = {}
checks['t_geodesic_jet'] = zero(
    jet(sp.diff(t_lam, lam) - sp.sqrt(c**2 / sp.cosh(t_lam)**2 + 1-c**2), lam, 3),
    't original null-geodesic jet')
checks['x_geodesic_jet'] = zero(
    jet(sp.diff(x_lam, lam) - c / sp.cosh(t_lam)**2, lam, 3),
    'x original null-geodesic jet')

# Product null incidence: the proper timelike dS2 separation equals rho.
cut_lam = l + d*l**3
t_cut = jet(t_lam.subs(lam, cut_lam), l, 4)
x_cut = jet(x_lam.subs(lam, cut_lam), l, 4)
rho_cut = jet(rho_lam.subs(lam, cut_lam), l, 4)
invariant = (-sp.sinh(t_cut)*sp.sinh(2*l)
             + sp.cosh(t_cut)*sp.cosh(2*l)*sp.cos(x_cut)
             - sp.cosh(rho_cut))
incidence_coefficient = sp.simplify(jet(invariant, l, 5).coeff(l, 4))
d_solution = sp.solve(incidence_coefficient, d)
assert len(d_solution) == 1
d_value = d_solution[0]
checks['null_incidence_l4'] = zero(incidence_coefficient.subs(d, d_value), 'cut incidence')
t_cut = t_cut.subs(d, d_value)
x_cut = x_cut.subs(d, d_value)
rho_cut = rho_cut.subs(d, d_value)

# Coordinates (c,phi) have dOmega=dc dphi. This is the actual induced cut metric.
gcc = (-sp.diff(t_cut, c)**2
       + sp.cosh(t_cut)**2 * sp.diff(x_cut, c)**2
       + sp.diff(rho_cut, c)**2)
gpp = rho_cut**2
det_normalized = jet(jet(gcc, l, 5)*jet(gpp, l, 5)/l**4, l, 3)
density_coefficient = sp.simplify(det_normalized.coeff(l, 2)/2)
expected = (1-5*c**2)/6
checks['directional_density_comparison'] = zero(density_coefficient-expected, 'directional cut area')
angular_mean = sp.integrate(density_coefficient, (c, -1, 1))/2
checks['scalar_mean_comparison'] = zero(angular_mean + sp.Rational(1, 9), 'R=2 area mean')

# Accelerated central clock in exactly flat geometry, no curvature formula used.
qt = sp.sinh(2*a*l)/a
qx = (sp.cosh(2*a*l)-1)/a
affine_from_null = (qt**2-qx**2)/(2*(qt-c*qx))
affine_exact = sp.sinh(a*l)/(a*(sp.cosh(a*l)-c*sp.sinh(a*l)))
checks['accelerated_null_root'] = zero(sp.trigsimp(affine_from_null-affine_exact), 'flat cut root')
accelerated_density = jet((affine_exact/l)**2, l, 3)
acc_linear = sp.simplify(accelerated_density.coeff(l, 1))
acc_quadratic = sp.simplify(accelerated_density.coeff(l, 2))
checks['accelerated_linear'] = zero(acc_linear-2*a*c, 'accelerated linear')
checks['accelerated_quadratic'] = zero(acc_quadratic-a**2*(3*c**2-sp.Rational(2, 3)), 'accelerated quadratic')
acc_mean = sp.integrate(acc_quadratic, (c, -1, 1))/2
checks['accelerated_angular_mean'] = zero(acc_mean-a**2/3, 'accelerated mean')

result = {
    'python': platform.python_version(), 'sympy': sp.__version__,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'scope': 'Exact Taylor coefficients of two supplied original-metric controls; no general numerical certificate',
    'dS2_product': {'affine_cut_cubic': str(d_value),
                    'directional_density_l2': str(density_coefficient),
                    'mean_density_l2': str(angular_mean),
                    'axis_density_l2': str(density_coefficient.subs(c, 1)),
                    'transverse_density_l2': str(density_coefficient.subs(c, 0))},
    'flat_accelerated': {'density_l1': str(acc_linear), 'density_l2': str(acc_quadratic),
                         'mean_density_l2': str(acc_mean)},
    'zero_residual_checks': checks,
}
print(json.dumps(result, indent=2))
