"""Exact symbolic/coordinate controls for VS1, not universal-proof substitutes.

All constants below are FREE diagnostic values/charts, not physical data.
The sole reused geometry function is AST-extracted from the pinned SM3 method;
no optional source model, old test body or prior output is executed.
"""
import ast
import hashlib
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
    residual = S.Matrix(actual) - S.Matrix(expected)
    reduced = residual.applyfunc(S.simplify)
    if reduced != S.zeros(*reduced.shape):
        raise AssertionError(name + ': nonzero residual ' + str(reduced))
    checks[name] = True

def reject(name, actual, expected):
    try:
        equal(name, actual, expected)
    except AssertionError as error:
        catches[name] = str(error)
    else:
        raise AssertionError('false pass: ' + name)

eta = S.diag(-1, 1, 1, 1)
inv = eta
u = S.symbols('u', positive=True)
mu = S.Matrix(S.symbols('m0:4'))
hs = S.symbols('h0:10')
H = S.zeros(4)
index = 0
for i in range(4):
    for j in range(i, 4):
        H[i,j] = H[j,i] = hs[index]
        index += 1
raised = inv * mu
C = [[[ -(int(a==b)*mu[c]+int(a==c)*mu[b]-eta[b,c]*raised[a])/u
         for c in range(4)] for b in range(4)] for a in range(4)]
def nabla(expr, direction):
    return S.diff(expr,u)*mu[direction]+sum(S.diff(expr,mu[j])*H[direction,j] for j in range(4))
delta_ric = S.Matrix(4,4,lambda b,d: S.simplify(sum(
    nabla(C[a][d][b],a)-nabla(C[a][a][b],d)+sum(
    C[a][a][e]*C[e][d][b]-C[a][d][e]*C[e][a][b] for e in range(4)) for a in range(4))))
q = (mu.T*inv*mu)[0]
expected = 2*H/u + (S.trace(inv*H)/u-3*q/u**2)*eta
equal('general_normal_jet_connection_to_ricci',delta_ric,expected)
reject('missing_quadratic_gradient_term',delta_ric,2*H/u+S.trace(inv*H)*eta/u)
tf = lambda tensor, metric: tensor-S.trace(metric.inv()*tensor)*metric/4
equal('conformal_tracefree_covariant_type',tf(delta_ric,eta/u**2),tf(delta_ric,eta))
equal('full_tf_condition',tf(delta_ric,eta),2*tf(H,eta)/u)

k,c = S.symbols('k c',real=True)
f = c-k*u
Hsub = {H[i,j]:f*eta[i,j] for i in range(4) for j in range(i,4)}
Q = q+k*u**2-2*c*u
for a in range(4):
    derivative = S.diff(Q,u)*mu[a]+sum(S.diff(Q,mu[j])*f*eta[a,j] for j in range(4))
    equal('conserved_Q_direction_'+str(a),[derivative],[0])
lamhat = 3*k*u**2+6*u*f-3*q
equal('target_scalar', [lamhat],[-3*Q])
reject('wrong_target_scalar_sign',[lamhat],[3*Q])

t,x,y,z = coords = S.symbols('t x y z',real=True)
def ricci_anchor(name, profile, target):
    metric=eta/profile**2
    conn,ric,scalar=geometry(metric,coords)
    equal(name,ric,target*metric)
    equal(name+'_scalar',[scalar],[4*target])
    return ric,metric

profile=1+t+2*x+3*y+4*z-t*t+x*x+y*y+z*z
ric,metric=ricci_anchor('six_nonzero_data_flat_quadratic',profile,-72)
reject('fixed_wrong_target_scalar',ric,-71*metric)
values['quadratic_u_at_origin']='1; positive on a sufficiently small neighborhood'
values['quadratic_target_Lambda']='-72'
ricci_anchor('nonconstant_null_affine',1+t+x,0)

bad=1+x*x
conn_bad,ric_bad,r_bad=geometry(eta/bad**2,coords)
reject('arbitrary_positive_profile_is_not_vacuum',tf(ric_bad,eta/bad**2),S.zeros(4))
values['failed_profile_tf_00']=str(S.simplify(tf(ric_bad,eta/bad**2)[0,0]))

base=eta/t**2  # FREE chart t>0, exact Lambda=3 control, no chosen physical scale.
connection,ricbase,scalarbase=geometry(base,coords)
equal('nonzero_scalar_base_original_ricci',ricbase,3*base)
rescale=1/t
Hess=S.Matrix(4,4,lambda a,b:S.diff(rescale,coords[a],coords[b])-sum(connection[d][a][b]*S.diff(rescale,coords[d]) for d in range(4)))
equal('nonzero_base_hessian_sign',Hess,-rescale*base)
conn_flat,ric_flat,r_flat=geometry(base/rescale**2,coords)
equal('nonzero_base_to_zero_scalar_target',ric_flat,S.zeros(4))
reject('silently_equal_base_and_target_scalar',ric_flat,3*eta)

# Six independent initial data are reconstructed, including the trace Hessian.
A,B0,B1,B2,B3,C0=S.symbols('A B0 B1 B2 B3 C0',real=True)
general=A+B0*t+B1*x+B2*y+B3*z+C0*(-t*t+x*x+y*y+z*z)/2
at0={v:0 for v in coords}
data=S.Matrix([general.subs(at0)]+[S.diff(general,v).subs(at0) for v in coords]+[S.trace(eta*S.hessian(general,coords))/4])
equal('six_data_injective_flat_reconstruction',data,S.Matrix([A,B0,B1,B2,B3,C0]))
reject('dropping_trace_hessian_datum',data,S.Matrix([A,B0,B1,B2,B3,0]))
s=S.symbols('s',real=True)
null_line={t:s,x:s,y:0,z:0}
equal('general_flat_u_affine_on_null_line',[S.diff(general.subs(null_line),s,2)],[0])
reject('bad_profile_not_null_affine',[S.diff(bad.subs(null_line),s,2)],[0])

T,L,beta=S.symbols('T L beta',positive=True)
h=S.Matrix([[-T*T,-T*T*beta],[-T*T*beta,L*L-T*T*beta*beta]])
equal('completed_tape_squared_weight',[(h/u**2).det()],[h.det()/u**4])
equal('reduced_control_invariant',[-(h/u**2).det()/(h[0,0]/u**2)**2],[-h.det()/h[0,0]**2])
values['completed_depth_shift']='log(u), with positive T,u and fixed auxiliary embedding'

print(json.dumps({'kind':'same-author exact symbolic and coordinate checks, NOT a holonomy/proof substitute',
    'python':platform.python_version(),'sympy':S.__version__,'checks':checks,
    'actual_rejection_paths':catches,'values':values,
    'proof_quantifiers':'general candidate argument, not finite pass count',
    'shared_method':'SHA-pinned geometry function only; no prior source-law code/output executed'},indent=2,sort_keys=True))
