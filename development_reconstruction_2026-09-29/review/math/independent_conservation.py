"""Compute curvature/divergence from full diagonal metric components, off shell."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s
out=Path(__file__).resolve().parent
t,x,y,z=s.symbols('t x y z', real=True)
coords=(t,x,y,z)
checks={};values={}
def ck(name,yes):
    checks[name]=bool(yes)
    if not checks[name]:raise AssertionError(name)
def simp(expr):return s.factor(expr)

for label,N in [('source',1+x*x+y**3),('alternate',2+x*x+y**4)]:
    g=s.diag(-N*N,1,1,1);gi=g.inv()
    Gam=[[[simp(sum(gi[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d])) for d in range(4))/2) for c in range(4)] for b in range(4)] for a in range(4)]
    Ric=s.Matrix(4,4,lambda a,b:simp(sum(s.diff(Gam[c][a][b],coords[c])-s.diff(Gam[c][a][c],coords[b])+sum(Gam[c][c][d]*Gam[d][a][b]-Gam[c][b][d]*Gam[d][a][c] for d in range(4)) for c in range(4))))
    R=simp(s.trace(gi*Ric))
    def div(A):
        return s.Matrix([simp(sum(gi[a,c]*(s.diff(A[a,b],coords[c])-sum(Gam[d][c][a]*A[d,b]+Gam[d][c][b]*A[a,d] for d in range(4))) for a in range(4) for c in range(4))) for b in range(4)])
    dR=s.Matrix([s.diff(R,co) for co in coords])
    dric=div(Ric)
    ck(label+'_contracted_Bianchi',all(simp(v)==0 for v in dric-dR/2))
    S=Ric-R*g/4
    ck(label+'_TF_Ricci_divergence',all(simp(v)==0 for v in div(S)-dR/4))
    ck(label+'_Einstein_conserved',all(simp(v)==0 for v in div(Ric-R*g/2)))
    Sq=R*Ric-R*R*g/4
    j=div(Sq)
    ric_grad=Ric*gi*dR
    ck(label+'_quadratic_response_divergence',all(simp(v)==0 for v in j-ric_grad))
    curl=simp(s.diff(j[2],x)-s.diff(j[1],y))
    point=curl.subs({x:1,y:1})
    ck(label+'_nonzero_completion_obstruction',point!=0)
    if label=='source':ck('source_exact_16_over_3',point==s.Rational(16,3))
    values[label]={'R':str(R),'j_x':str(j[1]),'j_y':str(j[2]),'curl_xy_at_1_1':str(point)}

# Same-action covariant/inverse-metric variation must differ by a minus sign.
G=s.diag(-4,2,3,5);Gi=G.inv()
h=s.Matrix([[1,2,0,0],[2,3,1,0],[0,1,-1,2],[0,0,2,4]])
E=s.Matrix([[2,1,0,1],[1,3,2,0],[0,2,4,1],[1,0,1,-2]])
dGi=-Gi*h*Gi
inverse_contraction=sum(E[a,b]*dGi[a,b] for a in range(4) for b in range(4))
upper=Gi*E*Gi
cov_contraction=sum((-upper[a,b])*h[a,b] for a in range(4) for b in range(4))
ck('same_action_variation_minus_sign',inverse_contraction==cov_contraction)
ck('wrong_plus_density_rejected',inverse_contraction!=-cov_contraction)
record={'python':platform.python_version(),'sympy':s.__version__,'checks':checks,'values':values,'passed':sum(checks.values()),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (out/'conservation_results.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps({'passed':record['passed'],'values':values},sort_keys=True))
