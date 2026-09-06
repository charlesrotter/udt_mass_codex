"""Independent Stage A exact controls; no repository imports or candidate exposure.

Question: a regular flat source cone with its fixed affine tangent admits distinct
ambient null scalar extensions agreeing in the full covector on that cone;
nonaffine rescaling is incompatible with being an exact null gradient.
Regime: local r > 0 in spherical Minkowski coordinates; angular entries vanish.
Controls: exact SymPy algebra, CPU only, no grid, no floating-point tolerance.
The free parameter a is mathematical continuation freedom, not physical input.
"""
import json
import platform
import sympy as sp

t, r, a, eta = sp.symbols("t r a eta", real=True)
theta = r-t
alternate = theta+a*theta**2
eta_inverse = sp.diag(-1, 1)
def covector(f):
    return sp.Matrix([sp.diff(f, t), sp.diff(f, r)])
def norm(p):
    return sp.simplify((p.T*eta_inverse*p)[0])
p = covector(theta)
p_alt = covector(alternate)
fixed_k = sp.Matrix([1, 1])
cone_match = [sp.simplify(v.subs(t,r)) for v in p_alt-p]
observer = sp.Matrix([sp.cosh(eta), sp.sinh(eta)])
omega = sp.simplify(-(observer.T*p)[0])
omega_alt = sp.simplify(-(observer.T*p_alt)[0])
omega_difference_on_cone = sp.simplify((omega_alt-omega).subs(t,r))
assert norm(p) == 0 and norm(p_alt) == 0
assert eta_inverse*p == fixed_k
assert all(v == 0 for v in cone_match)
assert omega_difference_on_cone == 0
assert sp.simplify(alternate.subs(t,r)) == 0
# At a != 0 the transverse second derivative is different, even on N.
second_jet_difference = sp.diff(alternate-theta, t, 2)
assert second_jet_difference == 2*a
# In (t,r), K=t*(partial_t+partial_r) is a positive nonaffine normal
# to t=r>0. Its radial Christoffel contributions vanish in Minkowski.
nonaffine = t*fixed_k
acceleration = sp.Matrix([
    sp.simplify(sum(nonaffine[j]*sp.diff(nonaffine[i], (t,r)[j])
                    for j in range(2))) for i in range(2)])
assert acceleration == t*fixed_k
results = {
    "evidence_type": "exact_symbolic_finite_witness_and_obstruction_control",
    "python": platform.python_version(),
    "sympy": sp.__version__,
    "coordinates": "(t,r), zero angular covector entries, r>0",
    "metric_radial_block": "diag(-1,1)",
    "theta": str(theta),
    "alternate": str(alternate),
    "null_norms": [str(norm(p)), str(norm(p_alt))],
    "ambient_covector_difference_on_cone": [str(v) for v in cone_match],
    "future_domain": "1+2*a*(r-t)>0; shrink about the cone",
    "omega": str(omega),
    "omega_difference_on_cone": str(omega_difference_on_cone),
    "transverse_second_jet_difference": str(second_jet_difference),
    "nonaffine_tangent": [str(v) for v in nonaffine],
    "nonaffine_acceleration": [str(v) for v in acceleration],
    "ceiling": "These finite controls do not prove the general local theorem."
}
print(json.dumps(results, indent=2, sort_keys=True))
