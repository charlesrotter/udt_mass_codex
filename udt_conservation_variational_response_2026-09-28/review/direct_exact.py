"""CRV1 direct checks: matrix curvature, mixed density divergence, variation sign.

Independent implementation after candidate exposure; no producer imports.
Mathematical witness only. One process/exact arithmetic; capture:60s/512MiB.
"""
import hashlib
import json
from pathlib import Path
import platform
import sympy as s

t,x,y,z=s.symbols('t x y z',real=True)
coords=(t,x,y,z)
N=1+x*x+y**3
metric=s.diag(-N*N,1,1,1)
inverse=metric.inv()
reduce=lambda expr:s.factor(s.cancel(expr))
# Connection is a matrix-valued one-form; K[c][a,b]=Gamma^a_cb.
K=[]
for c in range(4):
    K.append(s.Matrix(4,4,lambda a,b:reduce(sum(inverse[a,d]*(
        s.diff(metric[d,b],coords[c])+s.diff(metric[d,c],coords[b])
        -s.diff(metric[c,b],coords[d]))/2 for d in range(4)))))
# Curvature matrix Omega_cd = d_c K_d - d_d K_c + [K_c,K_d].
Omega={}
for c in range(4):
    for d in range(4):
        Omega[c,d]=(K[d].diff(coords[c])-K[c].diff(coords[d])
                    +K[c]*K[d]-K[d]*K[c]).applyfunc(reduce)
Ric=s.Matrix(4,4,lambda b,d:reduce(sum(Omega[a,d][a,b] for a in range(4))))
R=reduce(s.trace(inverse*Ric))
S=R*(Ric-R*metric/4)
mixed=inverse*S
# For the positive-lapse patch sqrt(abs(det g))=N.
j=s.Matrix([reduce(sum(s.diff(N*mixed[a,b],coords[a])/N
    -sum(K[a][c,b]*mixed[a,c] for c in range(4)) for a in range(4))) for b in range(4)])
curl=reduce(s.diff(j[2],x)-s.diff(j[1],y))
point={x:s.Integer(1),y:s.Integer(1)}
tests={}
def zero(name,value):
    entries=list(value) if isinstance(value,s.MatrixBase) else [value]
    tests[name]=all(reduce(v)==0 for v in entries)
    assert tests[name],(name,entries)
def nonzero(name,value):
    tests[name]=reduce(value)!=0
    assert tests[name],(name,value)

zero('Ricci_matrix_curvature',Ric-s.diag(N*(2+6*y),-2/N,-6*y/N,0))
zero('scalar_curvature',R+4*(3*y+1)/N)
zero('trace_free',s.trace(inverse*S))
zero('j_vs_Ric_grad_R',j-Ric*inverse*s.Matrix([s.diff(R,c) for c in coords]))
zero('author_j_x',j[1]+16*x*(3*y+1)/N**3)
zero('author_j_y',j[2]-72*y*(x*x-2*y**3-y*y+1)/N**3)
zero('author_curl_value',curl.subs(point)-s.Rational(16,3))
nonzero('nontrivial_curl',curl.subs(point))
nonzero('curl_wrong_zero_rejected',curl.subs(point))
nonzero('curl_wrong_orientation_rejected',-curl.subs(point)-s.Rational(16,3))
# Test variation conversion with a full symmetric tangent and concrete E.
g0=metric.subs(point)
gi0=g0.inv()
h=s.Matrix([[1,2,0,1],[2,3,1,0],[0,1,2,1],[1,0,1,-2]])
eps=s.symbols('eps')
dg_inverse=(g0+eps*h).inv().diff(eps).subs(eps,0)
zero('inverse_metric_tangent',dg_inverse+gi0*h*gi0)
E=Ric.subs(point)
volume=N.subs(point)
inverse_pair=reduce(volume*s.trace(E*dg_inverse))
Tminus=-volume*gi0*E*gi0
Tplus=-Tminus
zero('same_action_covariant_density_minus',inverse_pair-s.trace(Tminus*h))
nonzero('same_action_plus_density_rejected',inverse_pair-s.trace(Tplus*h))
dvolume=s.diff(s.sqrt(-(g0+eps*h).det()),eps).subs(eps,0)
zero('volume_derivative',dvolume-volume*s.trace(gi0*h)/2)
zero('minus_two_C_action_gives_plus_Cg_inverse_response',-2*dvolume-volume*s.trace(g0*dg_inverse))
# Direct density divergence conversion for the nonconserved E=Ric.
raised=inverse*Ric*inverse
density=N*raised
density_div=s.Matrix([reduce(sum(s.diff(density[a,b],coords[b])
    +sum(K[b][a,c]*density[c,b] for c in range(4)) for b in range(4))) for a in range(4)])
zero('density_divergence_conversion',density_div-N*inverse*s.Matrix([s.diff(R,c)/2 for c in coords]))
nonzero('density_divergence_control_nonzero',density_div[1].subs(point))

out={'scope':'Direct independent metric witness/convention checks after candidate exposure',
     'python':platform.python_version(),'sympy':s.__version__,
     'method':'Matrix-valued connection curvature and mixed-index density divergence; no producer imports',
     'j':[str(v) for v in j],'curl':str(curl),'curl_at_1_1':str(curl.subs(point)),
     'same_action_inverse_pair':str(inverse_pair),
     'same_action_covariant_plus_sign_defect':str(reduce(inverse_pair-s.trace(Tplus*h))),
     'checks':tests,'passed':sum(tests.values()),
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with Path(__file__).with_name('direct_exact_result.json').open('x') as f:
    json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
