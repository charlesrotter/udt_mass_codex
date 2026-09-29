"""Direct-stage independent coordinate calculation before producer code exposure."""
import datetime
import hashlib
import json
from pathlib import Path
import platform
import sympy as s

root=Path.cwd()
here=Path(__file__).resolve().parent
pins={}
for filename in ['DIRECT_FREEZE.json','CANDIDATE_FREEZE.json']:
    p=root/'udt_gr_commitment_audit_2026-09-29'/filename
    pmap=json.loads(p.read_text())['sha256']
    actual={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in pmap}
    assert actual==pmap, (filename,[n for n in pmap if actual[n]!=pmap[n]])
    pins[filename]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'entries':actual}
seal_path=here/'SOURCE_FIRST_SEAL.json'
seal=json.loads(seal_path.read_text())
assert all(hashlib.sha256((root/n).read_bytes()).hexdigest()==h for n,h in seal['files'].items())

t,x,y,z=s.symbols('t x y z', real=True)
r=s.symbols('r',positive=True)
alpha=s.symbols('alpha',real=True)
coords=(t,x,y,z)
checks=[]
def clean(e):return s.factor(s.trigsimp(s.simplify(e)))
def equal(name,a,b=0):
    d=a-b
    components=list(d) if isinstance(d,s.MatrixBase) else [d]
    rem=[clean(c) for c in components]
    assert all(c==0 for c in rem),(name,rem)
    checks.append(name)
def nonzero(name,e):
    assert clean(e)!=0,(name,e)
    checks.append(name)

def tensors(g):
    iv=g.inv()
    # Connection one-form matrices: A_i^a_b=Gamma^a_ib.
    A=[s.Matrix(4,4,lambda a,b:clean(sum(iv[a,k]*(s.diff(g[k,b],coords[i])+
       s.diff(g[k,i],coords[b])-s.diff(g[i,b],coords[k])) for k in range(4))/2))
       for i in range(4)]
    curvature=[[ (A[j].diff(coords[i])-A[i].diff(coords[j])+A[i]*A[j]-A[j]*A[i]).applyfunc(clean)
                  for j in range(4)] for i in range(4)]
    Ric=s.Matrix(4,4,lambda a,b:clean(sum(curvature[i][b][i,a] for i in range(4))))
    R=clean(s.trace(iv*Ric))
    def div(B):
        mixed=iv*B
        return s.Matrix([clean(sum(s.diff(mixed[a,b],coords[a])+
            sum(A[a][a,c]*mixed[c,b]-A[a][c,b]*mixed[a,c] for c in range(4))
            for a in range(4))) for b in range(4)])
    Hess=s.Matrix(4,4,lambda a,b:clean(s.diff(R,coords[a],coords[b])-
                    sum(A[a][c,b]*s.diff(R,coords[c]) for c in range(4))))
    box=clean(s.trace(iv*Hess))
    Q=(2*R*Ric-R*R*g/2+2*(g*box-Hess)).applyfunc(clean)
    G=Ric-R*g/2
    return {'Ric':Ric,'R':R,'Q':Q,'G':G,'box':box,'div':div,'inverse':iv}

g=s.diag(-1,1,r*r,r*r*s.sin(y)**2)
product=tensors(g)
equal('product_Ricci',product['Ric'],s.diag(0,0,1,s.sin(y)**2))
equal('product_R',product['R'],2/r**2)
E=product['G']+alpha*product['Q']
shape=lambda B,g:B-s.trace(g.inv()*B)*g/4
equal('product_general_shape',shape(E,g),(1+4*alpha/r**2)*shape(product['Ric'],g))
equal('product_divergence_all_alpha',product['div'](E),s.zeros(4,1))
selected=E.subs(alpha,-r*r/4)
equal('product_pure_trace',selected,-g/(2*r*r))
equal('product_DDR_shape',shape(selected,g),s.zeros(4))
nonzero('product_not_E_zero',selected[0,0])
nonzero('product_not_Ricci_shape_zero',shape(product['Ric'],g)[0,0])
equal('product_alpha_zero_shape',shape(E.subs(alpha,0),g),shape(product['Ric'],g))

gm=s.diag(-1,t**4,t**4,t**4)
control=tensors(gm)
equal('variable_R',control['R'],36/t**2)
equal('variable_boxR',control['box'],216/t**4)
equal('variable_R_squared_response',control['Q'],s.diag(-648/t**4,216,216,216))
equal('variable_divG',control['div'](control['G']),s.zeros(4,1))
equal('variable_divQ',control['div'](control['Q']),s.zeros(4,1))
equal('variable_divE_all_alpha',control['div'](control['G']+alpha*control['Q']),s.zeros(4,1))
algebraic=2*control['R']*control['Ric']-control['R']**2*gm/2
wrongdiv=control['div'](algebraic)
equal('wrong_algebraic_time_divergence',wrongdiv[0],-864/t**5)
nonzero('omitted_derivatives_rejected',wrongdiv[0])

scaled=tensors(9*gm)
equal('homothety_G_weight_zero',scaled['G'],control['G'])
equal('homothety_Q_weight_minus_two',scaled['Q'],control['Q']/9)
nonzero('fixed_alpha_full_E_not_weight_zero',
        (scaled['G']+scaled['Q']-control['G']-control['Q'])[0,0])

# Explicit matter comparison fixes the Noether convention without adopting a field.
eta=s.diag(-1,1,1,1)
psi=t*t+x**3/3
gradient=s.Matrix([s.diff(psi,c) for c in coords])
V=psi**3/3
T=gradient*gradient.T-eta*((gradient.T*eta*gradient)[0]/2+V)
Em=-T/2
P=sum(eta[a,a]*s.diff(psi,coords[a],coords[a]) for a in range(4))-psi**2
divEm=s.Matrix([sum(eta[a,a]*s.diff(Em[a,b],coords[a]) for a in range(4)) for b in range(4)])
equal('candidate_scalar_Noether_sign',2*divEm+P*gradient,s.zeros(4,1))
nonzero('wrong_scalar_Noether_sign_rejected',(2*divEm-P*gradient)[0].subs({t:1,x:1}))

report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python':platform.python_version(),'sympy':s.__version__,
        'exposure':'candidate prose and freezes read; producer code/output/repair not yet read',
        'freeze_verification':pins,
        'source_first_seal_verified':hashlib.sha256(seal_path.read_bytes()).hexdigest(),
        'check_count':len(checks),'checks':checks,
        'observations':{'product_E_selected_diagonal':[str(selected[i,i]) for i in range(4)],
           'product_shape_Ricci_diagonal':[str(clean(shape(product["Ric"],g)[i,i])) for i in range(4)],
           'control_Q_diagonal':[str(control['Q'][i,i]) for i in range(4)],
           'wrong_algebraic_time_divergence':str(wrongdiv[0])}}
with (here/'DIRECT_INDEPENDENT_RESULTS.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps(report,sort_keys=True,indent=2))
