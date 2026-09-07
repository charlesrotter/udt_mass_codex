"""Exposed independent recomputation from coordinate embeddings, stdout only."""
import hashlib
import json
import pathlib
import platform
import sympy as S

root=pathlib.Path(__file__).resolve().parents[3]
step=root/'udt_phase_current_product_persistence_campaign_2026-09-07/step_03'
saved=json.loads((step/'author_exact.stdout').read_text())
checks={}

def eq(name,a,b):
    delta=a-b
    entries=list(delta) if isinstance(delta,S.MatrixBase) else [delta]
    residuals=[S.simplify(x) for x in entries]
    assert all(x==0 for x in residuals),(name,residuals)
    checks[name]='PASS'

u,v,x,y,flow,theta,z2=S.symbols('u v x y flow theta z2',real=True)
h,c,A,B,Lshear=S.symbols('h c A B Lshear',real=True)
kappa,z1,w,Delta,au=S.symbols('kappa z1 w Delta au',positive=True)
px,py=S.symbols('px py',real=True)
g=S.Matrix([[h,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
# Differentiate the actual coordinate maps, rather than inserting their
# asserted tangents/Jacobians. The metric value h is used pointwise only.
graph=S.Matrix([u,-c*u+A*x+B*y,x,y])
graph_jac=graph.jacobian([u,x,y])
gamma=graph_jac.T*g*graph_jac
mapping=S.Matrix([-theta/kappa,
                 flow+c*theta/kappa+A*z1**2+B*(z2+Lshear*z1),
                 z1**2,z2+Lshear*z1])
jac=mapping.jacobian([flow,theta,z1,z2])
full=S.simplify(jac.T*g*jac)
gamma_phase=full[1:,1:]
L=h+2*c-A*A-B*B
J2=S.sqrt(S.factor(gamma_phase[1:,1:].det()))
J3=2*z1*S.sqrt(L)/kappa
eq('volume_from_full_minor',gamma_phase.det(),J3**2)
nflat=S.Matrix([-1/S.sqrt(L),0,0,0])
normal=full.inv()*nflat
eq('full_normal_unit',(normal.T*full*normal)[0],-1)
current=S.Matrix([w,0,0,0])
flux=S.simplify(-(current.T*full*normal)[0]*J3)
phase=S.Matrix([0,1,0,0])
Uold=S.Matrix([au,(1+h*au**2+px**2+py**2)/(2*au),px,py])
U=jac.inv()*Uold
omega=-(phase.T*U)[0]
rate=-(U.T*full*current)[0]
local={str(symbol):symbol for symbol in [u,v,x,y,flow,theta,z2,h,c,A,B,Lshear,kappa,z1,w,Delta,au,px,py]}
local['Matrix']=S.Matrix
parse=lambda key:S.sympify(saved[key],locals=local)
for key,actual in [('gamma_graph',gamma),('gamma_phase',gamma_phase),
                   ('J2',J2),('J3',J3),('initial_flux',flux),('Gamma',rate),
                   ('nonproduct_derivative',S.diff(S.exp(theta*z1),theta))]:
    eq('saved_'+key,actual,parse(key))
eq('coarea_from_inverse',gamma_phase.inv()[0,0],J2**2/J3**2)
eq('flux_vs_metric_volume',flux,w*J2/kappa)
eq('full_future_normalization',(phase.T*normal)[0],-kappa/S.sqrt(L))
eq('full_observer_frequency',omega,kappa*au)

# Nonconstant positive phase normalization: this is an independent control
# of the full covector theorem, not a new metric or product construction.
coords=[u,v,x,y]
Theta=-u-u**3
k=S.Matrix([S.diff(Theta,t) for t in coords])
lam=1+3*u*u
eq('variable_phase_raises_to_same_ray',g.inv()*k,lam*S.Matrix([0,1,0,0]))
eq('variable_phase_full_null',(k.T*g.inv()*k)[0],0)
closure=S.Matrix(4,4,lambda i,j:S.diff(k[j],coords[i])-S.diff(k[i],coords[j]))
eq('variable_phase_full_closure',closure,S.zeros(4))
eq('variable_phase_flow_normalization',S.diff(lam,v),0)
eq('variable_phase_nonconstant_control',S.diff(lam,u),6*u)

# Verify frozen input bytes. This authenticates all entries, including
# auxiliary source entries not re-proved by this bounded review.
manifests={}
for name in ['FREEZE_SHA256SUMS','SOURCE_SHA256SUMS','review/STAGE_A_SHA256SUMS']:
    lines=(step/name).read_text().splitlines()
    for line in lines:
        digest,relative=line.split(None,1)
        actual=hashlib.sha256((root/relative).read_bytes()).hexdigest()
        assert actual==digest,(name,relative,actual,digest)
    manifests[name]=dict(count=len(lines),sha256=hashlib.sha256((step/name).read_bytes()).hexdigest())
stage_a=json.loads((step/'review/source_first.stdout').read_text())
for relative,digest in stage_a['source_sha256'].items():
    assert hashlib.sha256((root/relative).read_bytes()).hexdigest()==digest,relative
print(json.dumps(dict(checks=checks,outputs=dict(gamma_graph=gamma.tolist(),
    gamma_phase=gamma_phase.tolist(),J2=J2,J3=J3,flux=flux,rate=rate,
    variable_phase=Theta,variable_lambda=lam),manifests=manifests,
    stage_a_source_count=len(stage_a['source_sha256']),python=platform.python_version(),
    sympy=S.__version__),indent=2,sort_keys=True,default=str))
