"""Independent source-first symbolic regression; no candidate imports or reads."""
import json
import platform
import sympy as sp

checks = {}

# Coordinate order (r, theta, x, y), k = partial_r, k_flat = dtheta.
a, bx, by, q11, q12, q22 = sp.symbols("a bx by q11 q12 q22", real=True)
g = sp.Matrix([[0, 1, 0, 0], [1, a, bx, by],
               [0, bx, q11, q12], [0, by, q12, q22]])
q = sp.Matrix([[q11, q12], [q12, q22]])
checks["generic_volume_screen_determinant"] = sp.expand(g.det() + q.det()) == 0
checks["exact_gradient_is_ray_coordinate_vector"] = g.inv()[:, 1] == sp.Matrix([1, 0, 0, 0])

# Variable-cut tangents on a fixed phase sheet, including arbitrary cut gradients.
tx, ty = sp.symbols("tx ty", real=True)
e = sp.Matrix([[tx, ty], [0, 0], [1, 0], [0, 1]])
checks["variable_cut_gradient_cancels"] = e.T * g * e == q

# Curved/expanding local flowbox: J depends on all coordinates.
r, theta, x, y = sp.symbols("r theta x y", real=True)
J = sp.exp(r * theta + x) * (1 + r**2 + y**2)
F = 2 + theta**2 + x**2 + y**2
rho = F / J
checks["phase_dependent_conserved_data"] = sp.simplify(sp.diff(J * rho, r) / J) == 0
checks["phase_dependent_not_fixed_product"] = sp.diff(F, theta) == 2 * theta

# Counterexample in Minkowski coordinates (t,z,x,y).
t, z = sp.symbols("t z", real=True)
phase = z - t
profile = 2 + phase**2 + x**2 + y**2
divergence = sp.diff(profile, t) + sp.diff(profile, z)
checks["minkowski_counterexample_divergence"] = divergence == 0
checks["minkowski_counterexample_phase_values_differ"] = (
    profile.subs({t: 0, z: 0}) != profile.subs({t: 0, z: 1})
)

# Positive affine phase normalization changes rho inversely and keeps C fixed.
b, delta, density, jac = sp.symbols("b delta density jac", positive=True)
checks["affine_phase_normalization"] = sp.simplify(b * density / (b * delta * jac) - density / (delta * jac)) == 0
checks["zero_density_no_division_by_content"] = sp.simplify((density / (delta * jac)).subs(density, 0)) == 0

# Passive phase-dependent relabeling x'=exp(theta)*x introduces a density
# Jacobian despite representing the same measure and same vector field.
xp = sp.symbols("xp", real=True)
passive_F = sp.exp(-theta)
passive_J = jac * sp.exp(-theta)
checks["passive_relabel_density_ratio_invariant"] = sp.simplify(passive_F / passive_J - 1 / jac) == 0
checks["passive_density_looks_phase_dependent"] = sp.diff(passive_F, theta) != 0

print(json.dumps({"python": platform.python_version(), "sympy": sp.__version__,
                  "evidence_type": "exact_symbolic_regression_not_general_proof",
                  "checks": checks, "passed": sum(checks.values()),
                  "total": len(checks), "all_passed": all(checks.values())}, indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
