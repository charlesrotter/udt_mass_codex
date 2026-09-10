"""QC2 direct review checks for all formal parameters; no author code import."""

import json
import platform
import sympy as s

x, epsilon, n = s.symbols("x epsilon n", positive=True)
a, b = s.symbols("a b", real=True)
checks = []
negative_controls = []


def eq(actual, expected, label):
    difference = s.simplify(actual-expected)
    assert difference == 0, (label, difference)
    checks.append(label)


def reject(actual, incorrect, label):
    try:
        assert s.simplify(actual-incorrect) == 0
    except AssertionError:
        negative_controls.append(label)
    else:
        raise AssertionError("failed to reject " + label)


def residual(profile):
    return x*x*s.diff(profile, x, 2)/2-profile+1


# Recover zero-data constant-forcing perturbation by solving the two anchor
# coefficients, starting with the Euler homogeneous solutions and -epsilon.
y_general = a*x*x+b/x-epsilon
solved = s.solve([y_general.subs(x, 1), s.diff(y_general, x).subs(x, 1)], (a, b))
y = s.factor(y_general.subs(solved))
w = s.simplify(y/epsilon)
eq(w, (x-1)**2*(x+2)/(3*x), "factorization supplies global positivity")
eq(x*x*s.diff(y, x, 2)/2-y, epsilon, "constant forcing at formal epsilon")
eq(y.subs(x, 1), 0, "derived value data")
eq(s.diff(y, x).subs(x, 1), 0, "derived slope data")

p_grow, q_grow = s.Integer(1), 1+y.subs(epsilon, n**-2)
eq(residual(q_grow), n**-2, "growing continuous residual")
z_grow_squared = s.cancel((q_grow/q_grow.subs(x, 1))/(p_grow/p_grow.subs(x, 1)))
end_grow = s.simplify(z_grow_squared.subs(x, n))
eq(end_grow, s.Rational(4, 3)-n**-2+s.Rational(2, 3)*n**-3,
   "growing endpoint clock square")
eq(s.limit(end_grow, n, s.oo), s.Rational(4, 3), "growing squared clock limit")
eq(s.limit(s.log(end_grow)/2, n, s.oo), s.log(s.Rational(4, 3))/2,
   "growing log clock limit")

p_gap = 1-(s.Rational(1, 2)-epsilon)/x
q_gap = s.factor(p_gap+y)
eq(residual(p_gap), 0, "gap reference balanced for formal epsilon")
eq(residual(q_gap), epsilon, "gap continuous residual for formal epsilon")
eq((q_gap-p_gap).subs(x, 1), 0, "gap value data")
eq(s.diff(q_gap-p_gap, x).subs(x, 1), 0, "gap derivative data")
eq(p_gap.subs(x, s.Rational(1, 2)), 2*epsilon, "gap reference minimum value")
eq(s.diff(p_gap, x), (s.Rational(1, 2)-epsilon)/x**2,
   "gap reference monotonicity expression")
eq(s.diff(p_gap, x).subs(x, s.Rational(1, 2)), 2-4*epsilon,
   "gap maximum reference slope")
z_gap_squared = s.cancel((q_gap/q_gap.subs(x, 1))/(p_gap/p_gap.subs(x, 1)))
eq(z_gap_squared.subs(x, s.Rational(1, 2)), s.Rational(29, 24),
   "gap endpoint relative clock square")
eq(s.limit(p_gap.subs(x, s.Rational(1, 2))/p_gap.subs(x, 1), epsilon, 0, dir="+"),
   0, "reference absolute anchored clock square vanishes")
eq(s.limit(q_gap.subs(x, s.Rational(1, 2))/q_gap.subs(x, 1), epsilon, 0, dir="+"),
   0, "perturbed absolute anchored clock square vanishes")

eq(w.subs(x, s.Rational(1, 2)), s.Rational(5, 12), "gap C0 coefficient")
eq(-s.diff(w, x).subs(x, s.Rational(1, 2)), s.Rational(7, 3), "gap C1 coefficient")
eq(s.diff(w, x, 2).subs(x, s.Rational(1, 2)), s.Rational(34, 3), "gap C2 coefficient")
eq(s.diff(w, x), 2*(x-1)*(x*x+x+1)/(3*x*x),
   "W monotonicity factor about anchor")
eq(s.diff(w, x, 2), (2+4/x**3)/3, "W second derivative positive")
eq(s.diff(w, x, 3), -4/x**4, "W second derivative decreasing")

radial = s.diff(w, x, 2)/2
tangential = s.diff(w, x)/(2*x)
sphere = w/x**2
eq(radial, (1+2/x**3)/3, "radial curvature coefficient")
eq(tangential, (1-x**-3)/3, "tangential curvature coefficient")
eq(sphere, s.Rational(1, 3)+s.Rational(2, 3)/x**3-1/x**2,
   "sphere curvature coefficient")
eq(s.diff(radial, x), -2/x**4, "radial curvature monotonicity")
eq(s.diff(tangential, x), 1/x**4, "tangential curvature monotonicity")
eq(s.diff(sphere, x), 2*(x-1)/x**4, "sphere curvature monotonicity")
eq(radial.subs(x, s.Rational(1, 2)), s.Rational(17, 3), "gap radial maximum")
eq(-tangential.subs(x, s.Rational(1, 2)), s.Rational(7, 3), "gap tangential maximum")
eq(sphere.subs(x, s.Rational(1, 2)), s.Rational(5, 3), "gap sphere maximum")
eq(radial.subs(x, 1), 1, "growing radial maximum")
eq(s.limit(tangential, x, s.oo), s.Rational(1, 3), "growing tangential supremum")
eq(s.limit(sphere, x, s.oo), s.Rational(1, 3), "growing sphere supremum")

reject(end_grow, s.Rational(4, 3)+n**-2+s.Rational(2, 3)*n**-3,
       "wrong growing coefficient")
reject(z_gap_squared.subs(x, s.Rational(1, 2)), s.Rational(29, 12),
       "wrong gap clock normalization")
reject(radial.subs(x, s.Rational(1, 2)), s.Rational(17, 6),
       "wrong radial curvature normalization")

print(json.dumps({"python": platform.python_version(), "sympy": s.__version__,
                  "identity_count": len(checks), "negative_count": len(negative_controls),
                  "identities": checks, "negative_controls": negative_controls,
                  "meaning": "symbolic algebra support; analytic sign/domain proofs reviewed separately"},
                 indent=2, sort_keys=True))
