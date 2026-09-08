"""SM1 reviewer source-first checks; no author code or outputs imported.

This checks exact identities and diagnostic counterexamples, not the universal
theorem. The analytic review supplies the quantifiers. CPU, one process.
"""
import json
import platform
import sympy as sp


checks = []


def require(name, condition, detail):
    passed = bool(condition)
    checks.append({"name": name, "passed": passed, "detail": str(detail)})
    if not passed:
        print(json.dumps({"checks": checks}, indent=2))
        raise AssertionError(name)


H, a, b, q11, q12, q22 = sp.symbols("H a b q11 q12 q22", real=True)
general = sp.Matrix([[H, 1, a, b], [1, 0, 0, 0],
                     [a, 0, q11, q12], [b, 0, q12, q22]])
det = sp.factor(general.det())
require("general_adapted_metric_determinant", det == q12**2-q11*q22, det)

# Outgoing spherical Minkowski tube, theta=r-t and r>0, 0<alpha<pi.
# This has expansion and nonconstant area despite zero ambient curvature.
theta, radius, alpha, beta = sp.symbols("theta radius alpha beta", real=True)
delta = sp.symbols("delta", positive=True)
coordinates = [theta, radius, alpha, beta]
g = sp.Matrix([[-1, 1, 0, 0], [1, 0, 0, 0],
               [0, 0, radius**2, 0],
               [0, 0, 0, radius**2*sp.sin(alpha)**2]])
gi = g.inv()
connection = [[[sp.simplify(sum(gi[i, ell] *
                 (sp.diff(g[ell, k], coordinates[j])
                  + sp.diff(g[ell, j], coordinates[k])
                  - sp.diff(g[j, k], coordinates[ell]))/2
                 for ell in range(4)))
                for k in range(4)] for j in range(4)] for i in range(4)]
k = gi * sp.Matrix([1, 0, 0, 0])
require("future_null_gradient", list(k) == [0, 1, 0, 0]
        and (k.T*g*k)[0] == 0, list(k))
require("affine_generator", all(connection[i][1][1] == 0 for i in range(4)),
        [connection[i][1][1] for i in range(4)])
area = radius**2*sp.sin(alpha)
density = (1+sp.cos(alpha)**2)*(2+sp.sin(beta))**2
current = density/(delta*area)*k


def divergence(vector):
    return sp.simplify(sum(sp.diff(vector[i], coordinates[i])
                           for i in range(4))
                       + sum(connection[i][i][j]*vector[j]
                             for i in range(4) for j in range(4)))


expansion = divergence(k)
div_current = divergence(current)
require("expanding_tube_not_parallel", expansion == 2/radius, expansion)
require("current_covariant_divergence", div_current == 0, div_current)

# Nontrivial angular/radial observer components; t=r-theta.
U = sp.Matrix([-1, sp.Rational(1, 2), 1/radius, 0])
norm = sp.simplify((U.T*g*U)[0])
omega = -(U.T*g*k)[0]
readout = sp.simplify(-(U.T*g*current)[0])
require("future_unit_timelike_observer", norm == -1 and U[1]-U[0] > 0, norm)
require("observer_readout", sp.simplify(readout-density*omega/(delta*area)) == 0,
        readout)

# Screen representative orthogonal to U; additions along k must leave q.
E = [sp.eye(4)[:, 2], sp.eye(4)[:, 3]]
screen = [e+((e.T*g*U)[0]/omega)*k for e in E]
screen_gram = sp.Matrix(2, 2, lambda i, j: (screen[i].T*g*screen[j])[0])
require("observer_screen_metric", sp.simplify(screen_gram.det()-area**2) == 0,
        screen_gram)
require("observer_screen_orthogonality",
        all(sp.simplify((e.T*g*U)[0]) == 0 for e in screen), "zero contractions")

other = (2+theta**2)*current
require("phase_dependent_conserved_control", divergence(other) == 0, divergence(other))
obstruction = sp.simplify(sp.diff(delta*area*other[1], theta))
point = {theta: 1, radius: 3, alpha: sp.pi/2, beta: sp.pi/6, delta: 5}
require("fixed_product_control_actually_fails", obstruction.subs(point) == sp.Rational(25, 2),
        obstruction.subs(point))

wrong = density/delta*k
wrong_div = divergence(wrong)
require("missing_area_mutation_detected", wrong_div.subs(point) == sp.Rational(5, 6),
        wrong_div.subs(point))

scale, label_jacobian = sp.symbols("scale label_jacobian", positive=True)
scaled = density/((scale*delta)*area)*(scale*k)
relabeled = (density/label_jacobian)/(delta*(area/label_jacobian))*k
require("phase_and_spacing_gauge", all(sp.simplify(scaled[i]-current[i]) == 0 for i in range(4)),
        list(scaled))
require("fixed_label_density_gauge", all(sp.simplify(relabeled[i]-current[i]) == 0 for i in range(4)),
        list(relabeled))
require("phase_only_is_not_gauge", sp.simplify((density/(delta*area)*(2*k)-current)[1]).subs(point)
        == sp.Rational(5, 36), "nonzero difference 5/36 at b=2")
require("amplitude_is_not_gauge", sp.simplify((2*current-current)[1]).subs(point)
        == sp.Rational(5, 36), "doubling supplied measure doubles current")

print(json.dumps({"python": platform.python_version(), "sympy": sp.__version__,
                  "method": "full Christoffel contraction on outgoing spherical tube; exact arithmetic",
                  "checks": checks, "passed": sum(c["passed"] for c in checks),
                  "total": len(checks), "interpretation": "finite diagnostic/regression only"}, indent=2))
