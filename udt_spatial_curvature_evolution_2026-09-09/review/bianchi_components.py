"""Independent symbolic expansion of projected vacuum Bianchi at a Fermi point.

Algebra check, not realization of arbitrary Weyl/kinematic/spatial-jet arrays.
Conventions match sealed SOURCE_FIRST.md; no author-code imports.
"""
import itertools
import json
import sympy as s

def stf(prefix):
    a,b,c,d,e=s.symbols(prefix+'0:5')
    return s.Matrix([[a,b,c],[b,d,e],[c,e,-a-d]])

E,B=stf('E'),stf('B')
de,db=[stf('de'+str(i)+'_') for i in range(3)],[stf('db'+str(i)+'_') for i in range(3)]
k=s.symbols('k0:6')
K=s.Matrix([[k[0],k[1],k[2]],[k[1],k[3],k[4]],[k[2],k[4],k[5]]])
eps=s.LeviCivita

def curvature(e,b,a,c,d,f):
    if a==c or d==f:return s.Integer(0)
    sign=1
    if a>c:a,c,sign=c,a,-sign
    if d>f:d,f,sign=f,d,-sign
    if a==0 and d==0:return sign*e[c-1,f-1]
    if a==0:return sign*sum(eps(d-1,f-1,j)*b[j,c-1] for j in range(3))
    if d==0:return sign*sum(eps(a-1,c-1,j)*b[j,f-1] for j in range(3))
    return -sign*sum(eps(a-1,c-1,j)*eps(d-1,f-1,l)*e[j,l]
                    for j,l in itertools.product(range(3),repeat=2))

def nabla(p,*abcd):
    result=curvature(de[p-1],db[p-1],*abcd)
    for slot,a in enumerate(abcd):
        if a==0:
            for j in range(1,4):
                ids=list(abcd);ids[slot]=j
                result+=K[p-1,j-1]*curvature(E,B,*ids)
        else:
            ids=list(abcd);ids[slot]=0
            result+=K[p-1,a-1]*curvature(E,B,*ids)
    return result

eraw=s.Matrix(3,3,lambda b,c:-sum(nabla(p,p,b+1,c+1,0) for p in range(1,4)))
braw=s.Matrix(3,3,lambda b,c:sum(eps(b,k,l)*nabla(p,p,c+1,k+1,l+1)/2
    for k,l,p in itertools.product(range(3),range(3),range(1,4))))
edot=(eraw+eraw.T)/2
bdot=(braw+braw.T)/2

def curl(ds):
    return s.Matrix(3,3,lambda i,j:sum((eps(i,k,l)*ds[k][j,l]+eps(j,k,l)*ds[k][i,l])/2
        for k,l in itertools.product(range(3),repeat=2)))

def local(q):
    return 2*s.trace(K)*q-3*(K*q+q*K)/2+s.trace(K*q)*s.eye(3)

electric_defect=(edot+curl(db)-local(E)).applyfunc(s.expand)
magnetic_defect=(bdot-curl(de)-local(B)).applyfunc(s.expand)
assert electric_defect==s.zeros(3),electric_defect
assert magnetic_defect==s.zeros(3),magnetic_defect
assert s.expand(s.trace(edot))==0
assert s.expand(s.trace(bdot))==0
print(json.dumps({'sympy':s.__version__,'electric_defect':str(electric_defect),
    'magnetic_defect':str(magnetic_defect),
    'scope':'Symbolic projected Bianchi identity for arbitrary STF E/B and full symmetric K; no arbitrary-data realization or PDE-existence assertion'},indent=2))
