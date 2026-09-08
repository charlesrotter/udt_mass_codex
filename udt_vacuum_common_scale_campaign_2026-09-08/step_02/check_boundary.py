"""VS2 exact algebra and actual local metrics; finite checks are not a proof.

FREE diagnostic coordinates/values, not physical selection. AST reuse of one
SHA-pinned Christoffel/Ricci method; no old optional-source controls executed.
"""
import ast
import hashlib
import itertools
import json
import platform
from pathlib import Path
import sympy as S

root = Path(__file__).resolve().parents[2]
method = root / 'udt_source_metric_connection_campaign_2026-09-08/step_03/check_interface.py'
assert hashlib.sha256(method.read_bytes()).hexdigest() == '8a34a9e57a2b5fab7f67586e6bff6398f76effe4b8f68407fa43f124ca40a416'
nodes = [n for n in ast.parse(method.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'geometry']
assert len(nodes) == 1
namespace = {'S': S}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(method), 'exec'), namespace)
geometry = namespace['geometry']
checks, catches, values = {}, {}, {}

def equal(name, actual, expected):
    residual = (S.Matrix(actual)-S.Matrix(expected)).applyfunc(S.simplify)
    if residual != S.zeros(*residual.shape):
        raise AssertionError(name+': nonzero residual '+str(residual))
    checks[name] = True

def reject(name, actual, expected):
    try:
        equal(name, actual, expected)
    except AssertionError as error:
        catches[name] = str(error)
    else:
        raise AssertionError('false pass: '+name)

# General algebraic Weyl tensor, represented by a symmetric bivector matrix.
pairs = list(itertools.combinations(range(4),2))
variables = S.symbols('w0:21')
M = S.zeros(6)
idx = 0
for i in range(6):
    for j in range(i,6):
        M[i,j] = M[j,i] = variables[idx]
        idx += 1

def component(a,b,c,d):
    if a==b or c==d:
        return S.Integer(0)
    sign = (1 if a<b else -1)*(1 if c<d else -1)
    return sign*M[pairs.index(tuple(sorted((a,b)))),pairs.index(tuple(sorted((c,d))))]

eta = S.diag(-1,1,1,1)
equations = []
for a,b,c,d in itertools.product(range(4), repeat=4):
    equations.append(component(a,b,c,d)+component(a,c,d,b)+component(a,d,b,c))
for b,d in itertools.product(range(4),repeat=2):
    equations.append(sum(eta[a,a]*component(a,b,a,d) for a in range(4)))

def dimension(extra):
    A,_ = S.linear_eq_to_matrix(equations+extra, variables)
    return len(variables)-A.rank()

equal('unrestricted_algebraic_Weyl_dimension',[dimension([])],[10])
for label,V,expected in [('timelike',(1,0,0,0),0),('spacelike',(0,1,0,0),0),('null',(1,1,0,0),2)]:
    contracted = [sum(component(a,b,c,d)*V[d] for d in range(4))
                  for a,b,c in itertools.product(range(4),repeat=3)]
    dim = dimension(contracted)
    equal(label+'_annihilator_tensor_dimension',[dim],[expected])
    values[label+'_annihilator_tensor_dimension']=dim
    if label=='null':
        reject('discarding_nonzero_null_Weyl_sector',[dim],[0])

def lower_riemann(metric, connection, coords, a,b,c,d):
    return S.simplify(sum(metric[a,e]*(S.diff(connection[e][d][b],coords[c])
        -S.diff(connection[e][c][b],coords[d])
        +sum(connection[e][c][h]*connection[h][d][b]
             -connection[e][d][h]*connection[h][c][b] for h in range(4))) for e in range(4)))

def hessian(profile, connection, coords):
    return S.Matrix(4,4,lambda a,b:S.diff(profile,coords[a],coords[b])
                    -sum(connection[d][a][b]*S.diff(profile,coords[d]) for d in range(4)))

r,v,x,y = coords = S.symbols('r v x y',real=True)
H = r*(x*x-y*y)
g = S.Matrix([[H,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]])
conn,ric,scalar = geometry(g,coords)
equal('pp_wave_original_Ricci',ric,S.zeros(4))
equal('pp_wave_determinant',[g.det()],[-1])
equal('parallel_null_dr_hessian',hessian(r,conn,coords),S.zeros(4))
equal('dr_is_null',[g.inv()[0,0]],[0])
Rrxrx = lower_riemann(g,conn,coords,0,2,0,2)
equal('nonzero_pp_wave_curvature',[Rrxrx],[-r])
u = 1+r
connhat,richat,scalarhat = geometry(g/u**2,coords)
equal('actual_rescaled_pp_wave_original_Ricci',richat,S.zeros(4))
values['positive_domain']='r>-1, restricted to small connected chart'

origin = {r:0,v:0,x:0,y:0}
all_curvature = [lower_riemann(g,conn,coords,a,b,c,d) for a,b,c,d in itertools.product(range(4),repeat=4)]
equal('all_curvature_zero_at_origin',[z.subs(origin) for z in all_curvature],[0]*256)
equal('all_connection_zero_at_origin',[z.subs(origin) for plane in conn for row in plane for z in row],[0]*64)
derivative = S.diff(Rrxrx,r).subs(origin)
equal('differentiated_compatibility_obstruction',[derivative],[-1])
reject('pointwise_Weyl_pass_is_not_extension',[derivative],[0])
# This original metric residual is additional evidence, not the proof that
# EVERY extension with u(p)=1,du(p)=dx is obstructed.
bad = 1+x
connbad,ricbad,scalarbad = geometry(g/bad**2,coords)
tfbad = (ricbad-scalarbad*g/bad**2/4).applyfunc(S.simplify)
reject('affine_coordinate_profile_not_automatically_vacuum',tfbad,S.zeros(4))
values['trial_bad_tf_rr']=str(tfbad[0,0])

t,z = S.symbols('t z',real=True)
theta,phi = S.symbols('theta phi',real=True)
coords2=(t,z,theta,phi)
product=S.diag(-1,S.cosh(t)**2,1,S.sin(theta)**2)
conn2,ric2,scalar2=geometry(product,coords2)
equal('product_development_original_Ricci',ric2,product)
equal('product_scalar',[scalar2],[4])
R0101=lower_riemann(product,conn2,coords2,0,1,0,1)
W0101=S.simplify(R0101-(product[0,0]*product[1,1]-product[0,1]*product[1,0])/3)
equal('nonzero_product_Weyl',[W0101],[-S.Rational(2,3)*S.cosh(t)**2])
reject('Einstein_is_not_necessarily_constant_curvature',[W0101],[0])
values['product_domain']='0<theta<pi; no global sphere-coordinate assertion'

print(json.dumps({'kind':'VS2 exact finite algebra and original-coordinate Ricci controls, NOT general-proof ownership',
    'python':platform.python_version(),'sympy':S.__version__,'checks':checks,
    'actual_rejection_paths':catches,'values':values,
    'tensor_shapes':'general Weyl: symmetric6x6 bivector matrix/21 variables then Bianchi+trace; metric4x4; full Riemann4^4',
    'shared_method':'SHA-pinned geometry function only; no optional-source tests run'},indent=2,sort_keys=True))
