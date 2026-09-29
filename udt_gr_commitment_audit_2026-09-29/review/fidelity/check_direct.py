import hashlib
import json
import pathlib
import platform
import sympy as s

root=pathlib.Path.cwd()
base=root/'udt_gr_commitment_audit_2026-09-29'
freeze={}
for name in ['DIRECT_FREEZE.json','CANDIDATE_FREEZE.json']:
    pins=json.loads((base/name).read_text())['sha256']
    for p,h in pins.items():
        actual=hashlib.sha256((root/p).read_bytes()).hexdigest()
        assert actual==h, (p,h,actual)
    freeze[name]={'sha256':hashlib.sha256((base/name).read_bytes()).hexdigest(),
                  'verified_entries':len(pins)}

checks=[]
def eq(name,actual,expected):
    delta=actual-expected
    if isinstance(delta,s.MatrixBase):
        assert delta.applyfunc(s.simplify)==s.zeros(*delta.shape),(name,delta)
    else:
        assert s.simplify(delta)==0,(name,delta)
    checks.append(name)

t,x,y,z=s.symbols('t x y z',real=True)
r=s.symbols('r',positive=True)
alpha=s.symbols('alpha',real=True)
coords=(t,x,y,z)

def geometry(g):
    gi=g.inv()
    # Connection one-form matrices: Gamma_c[a,b]=Gamma^a_cb.
    Gam=[s.Matrix(4,4,lambda a,b:s.simplify(sum(gi[a,k]*(
        s.diff(g[k,b],coords[c])+s.diff(g[k,c],coords[b])-s.diff(g[c,b],coords[k]))/2
        for k in range(4)))) for c in range(4)]
    # R^a_bcd from the curvature of these matrices.
    curv=[[ (Gam[j].diff(coords[i])-Gam[i].diff(coords[j])
              +Gam[i]*Gam[j]-Gam[j]*Gam[i]).applyfunc(s.simplify)
           for j in range(4)] for i in range(4)]
    Ric=s.Matrix(4,4,lambda b,d:s.simplify(sum(curv[a][d][a,b] for a in range(4))))
    def trace(T):
        return s.simplify(s.trace(gi*T))
    R=trace(Ric)
    def TF(T):
        return (T-trace(T)*g/4).applyfunc(s.simplify)
    def div(T):
        derivatives=[T.diff(coords[c])-Gam[c].T*T-T*Gam[c] for c in range(4)]
        return s.Matrix([s.simplify(sum(gi[a,c]*derivatives[c][a,b]
                           for a in range(4) for c in range(4))) for b in range(4)])
    H=s.Matrix(4,4,lambda a,b:s.simplify(s.diff(R,coords[a],coords[b])
             -sum(Gam[a][k,b]*s.diff(R,coords[k]) for k in range(4))))
    Qalg=2*R*Ric-R**2*g/2
    Q=(Qalg+2*(g*trace(H)-H)).applyfunc(s.simplify)
    G=(Ric-R*g/2).applyfunc(s.simplify)
    return dict(g=g,Ric=Ric,R=R,TF=TF,div=div,H=H,Q=Q,Qalg=Qalg,G=G)

p=geometry(s.diag(-1,1,r**2/y**2,r**2/y**2))
eq('Negative-curvature product Ricci',p['Ric'],s.diag(0,0,-1/y**2,-1/y**2))
eq('Negative-curvature product scalar',p['R'],-2/r**2)
eq('Product Hessian scalar vanishes',p['H'],s.zeros(4))
E=p['G']+r**2*p['Q']/4
eq('Positive-alpha product response is pure trace',E,p['g']/(2*r**2))
eq('Positive-alpha product DDR',p['TF'](E),s.zeros(4))
eq('Product response covariant divergence',p['div'](E),s.zeros(4,1))
assert p['TF'](p['Ric'])!=s.zeros(4) and E!=s.zeros(4)
checks.append('Nonzero controls: Einstein shape and full equation remain distinct')

q=geometry(s.diag(-1,t**6,t**6,t**6))
eq('Independent nonconstant scalar',q['R'],90/t**2)
eq('Full R-squared response divergence',q['div'](q['Q']),s.zeros(4,1))
eq('Mixed action response divergence',q['div'](q['G']+alpha*q['Q']),s.zeros(4,1))
wrong=q['div'](q['Qalg'])
assert wrong[0]!=0
eq('Omitted-Hessian control from Ricci gradient',wrong[0],-2*q['Ric'][0,0]*s.diff(q['R'],t))
checks.append('Derivative omission is detected on nonconstant curvature')

# Fixed-metric coefficient equality for a general constant-curvature product.
k1,k2=s.symbols('k1 k2',real=True)
eta=s.diag(-1,1,1,1)
Rp=2*(k1+k2)
Ricp=s.diag(-k1,k1,k2,k2)
Sp=Ricp-Rp*eta/4
Ep=Ricp-Rp*eta/2+alpha*(2*Rp*Ricp-Rp**2*eta/2)
TFp=Ep-s.trace(eta*Ep)*eta/4
eq('General two-factor shape response multiplier',TFp,(1+4*alpha*(k1+k2))*Sp)

print(json.dumps({'freeze':freeze,'python':platform.python_version(),'sympy':s.__version__,
 'checks':checks,'count':len(checks),'product_scalar':str(p['R']),
 'product_E_alpha':str(E),'product_TF_Ric':str(p['TF'](p['Ric'])),
 'nonconstant_R':str(q['R']),'nonconstant_Q':str(q['Q']),
 'div_algebraic_Q':str(wrong),'arithmetic':'exact; no tolerance',
 'scope':'mathematical comparison only; no physical/model/filter/stability claim'},indent=2))
