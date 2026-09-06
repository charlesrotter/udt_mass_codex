"""Bounded symbolic representation diagnostic; independent projector route."""
import json
import platform
import sympy as s

y = s.Matrix(s.symbols('y0:3', real=True))
t = s.symbols('t', real=True)
r = s.sqrt(y.dot(y))
radial = y*y.T/(r*r)
projector_J = radial+(1-t/r)*(s.eye(3)-radial)
coordinate_J = ((1-t/r)*y).jacobian(y)
assert all(s.simplify(d)==0 for d in projector_J-coordinate_J)
r0 = s.symbols('r0', positive=True)
axis = {y[0]:r0,y[1]:0,y[2]:0}
actual = s.simplify(coordinate_J.subs(axis))
expected = s.diag(1,1-t/r0,1-t/r0)
structural_equal = actual==expected
entrywise = [s.simplify(d) for d in actual-expected]
assert structural_equal is False
assert all(d==0 for d in entrywise)
wrong_J = s.diag(1,1+t/r0,1+t/r0)
assert any(s.simplify(d)!=0 for d in actual-wrong_J)
normal = s.symbols('normal', real=True)
roots = s.solveset(-normal**2,normal,domain=s.S.Reals)
assert roots==s.FiniteSet(0)
assert (-normal**2).subs(normal,s.Rational(1,7))!=0
print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,
                  'projector_vs_coordinate_differences':[str(s.simplify(d)) for d in projector_J-coordinate_J],
                  'axis_actual':str(actual),'axis_expected':str(expected),
                  'structural_equal':structural_equal,'exact_entrywise_differences':[str(d) for d in entrywise],
                  'critical_point_real_normal_roots':str(roots),
                  'wrong_jacobian_rejected':True,'nonzero_critical_normal_rejected':True,
                  'classification':'representation-only structural-equality defect; exact zero testing is a valid repair'},indent=2))
