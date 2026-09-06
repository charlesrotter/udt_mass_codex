"""Independent parametric-coordinate reconstruction of the foliation witness.

Uses the Cartesian embedding and its pulled-back metric instead of the
candidate's implicit differentiation. Exact rational symbolic algebra only.
No candidate module imported; no stored candidate output enters this calculation.
"""
import json
import platform
import sympy as s

c, R, v, w, a = s.symbols('c R v w a', real=True)
L = 1+v*v+w*w
m = s.Matrix([2*v/L, (1-v*v-w*w)/L, 2*w/L])
embedding = s.Matrix([R-c, a*c*c+R*m[0], R*m[1], R*m[2]])
coordinates = (c, R, v, w)
eta = s.diag(-1,1,1,1)
Jac = embedding.jacobian(coordinates)
gram = (Jac.T*eta*Jac).applyfunc(s.factor)
D = 1+2*a*c*m[0]
determinant = s.factor(Jac.det())
assert s.factor(determinant-4*R*R*D/L**2) == 0
assert gram[1,1] == 0 and gram[1,2] == 0 and gram[1,3] == 0
assert s.factor(gram[1,0]-D) == 0
# This is solved from the R row of the metric, not imported from the implicit F.
raised_dc_coordinates = s.Matrix([0,1/D,0,0])
assert (gram*raised_dc_coordinates-s.Matrix([1,0,0,0])).applyfunc(s.factor) == s.zeros(4,1)
raised_dc_cartesian = (Jac*raised_dc_coordinates).applyfunc(s.factor)
covector_dc_cartesian = eta*raised_dc_cartesian
assert s.factor((raised_dc_cartesian.T*eta*raised_dc_cartesian)[0]) == 0
cone_vector_difference = (raised_dc_cartesian.subs(c,0)-s.Matrix([1,*m])).applyfunc(s.factor)
assert cone_vector_difference == s.zeros(4,1)
witness_subs = {a:1, c:s.Rational(1,10), R:1, v:0, w:0}
witness = embedding.subs(witness_subs)
witness_covector = covector_dc_cartesian.subs(witness_subs)
assert witness == s.Matrix([s.Rational(9,10),s.Rational(1,100),1,0])
assert witness_covector == s.Matrix([-1,0,1,0])
base_radius = s.sqrt(sum(witness[i]**2 for i in (1,2,3)))
base_covector = s.Matrix([-1,*(witness[i]/base_radius for i in (1,2,3))])
normal_wedge_tx = s.simplify(witness_covector[0]*base_covector[1]
                             -witness_covector[1]*base_covector[0])
assert normal_wedge_tx != 0
print(json.dumps({
    'python':platform.python_version(), 'sympy':s.__version__,
    'method':'Parametric Cartesian embedding, pullback metric, direct metric-duality solve',
    'domain':'R>0, stereographic chart L=1+v^2+w^2, D=1+2*a*c*m_x>0',
    'embedding':[str(z) for z in embedding],
    'jacobian_determinant':str(determinant),
    'canonical_determinant':'4*R^2*D/L^2',
    'R_row_of_metric':[str(gram[1,j]) for j in range(4)],
    'raised_dc_in_parameter_coordinates':[str(z) for z in raised_dc_coordinates],
    'raised_dc_in_cartesian_coordinates':[str(z) for z in raised_dc_cartesian],
    'cone_vector_difference':[str(z) for z in cone_vector_difference],
    'witness_point':[str(z) for z in witness],
    'witness_covector':[str(z) for z in witness_covector],
    'base_covector':[str(z) for z in base_covector],
    'normal_wedge_tx':str(normal_wedge_tx),
    'ceiling':'Exact distinct-foliation witness and local Jacobian; not the general smooth theorem'
},indent=2))
