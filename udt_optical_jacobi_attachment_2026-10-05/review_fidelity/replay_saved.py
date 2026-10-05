"""OJM1 independent reciprocal-radius replay, no parent code imported."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
import resource
resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
import json
from pathlib import Path
import mpmath as mp
mp.mp.dps=60
rows=[]
def compute(a,H,R,b=None,E=mp.mpf(1)):
    a,H,R,E=map(mp.mpf,(a,H,R,E))
    x=1/R
    m=mp.mpf(1)
    omega=mp.sqrt(m/a**3-H**2)
    h=1-3*m/a
    def s(w,b): return mp.sqrt(1+H*H*b*b-b*b*w*w+2*m*b*b*w**3)
    def P(b): return mp.quad(lambda w:b/s(w,b),[x,1/a])
    def U(b): return mp.quad(lambda w:b*b/(s(w,b)*(1+s(w,b))),[x,1/a])
    t_e=None; residual=None
    if b is None:
        def tail(w):
            V=mp.sqrt(H*H+(E*E-1)*w*w+2*m*w**3)
            return 1/(V*(E*w+V))
        d=mp.quad(tail,[0,x])
        bmax=a/s(1/a,mp.mpf(0)) # temporary overwritten with actual launch bound
        bmax=a/mp.sqrt(1-2*m/a-H*H*a*a)
        b=mp.findroot(lambda v:P(v)-omega*U(v)-omega*d,(mp.mpf(0),bmax/2))
        t_e=-d-U(b)
        residual=abs(omega*t_e+P(b))
        assert abs(mp.im(b))<mp.mpf('1e-50') and residual<mp.mpf('1e-45')
    b=mp.mpf(b)
    sa,so=s(1/a,b),s(x,b)
    assert sa>0
    I=mp.quad(lambda w:1/s(w,b)**3,[x,1/a])
    bp=a*sa*R*so*I
    bt=a*R*mp.sin(P(b))/b if b else R-a
    v=mp.sqrt(E*E-1+2*m/R+H*H*R*R)
    A=1/(E+v)+v*b*b/(R*R*(1+so))
    L=mp.quad(lambda w:1/(w*w*s(w,b)),[x,1/a])
    Z=(1-omega*b)/(mp.sqrt(h)*A)
    vals=dict(m=m,a=a,H=H,R=R,E=E,b=b,P=P(b),I=I,B_parallel=bp,B_perp=bt,
              j_parallel=A*bp,j_perp=A*bt,D_A=A*mp.sqrt(abs(bp*bt)),D_o=A*L,Z=Z)
    if t_e is not None: vals.update(t_e=t_e,incidence_residual=residual)
    return {k:mp.nstr(v,58) for k,v in vals.items()}

H=mp.sqrt(mp.mpf('.0001')/3)
for E in ['1','10']:
    for R in ['1000','1000000']:
        row=compute('10',H,R,E=E)
        row['label']=f'actual_E{E}_R{R}'
        rows.append(row)
for R,b in [('50','2'),('1000','-3')]:
    row=compute('10',H,R,mp.mpf(b))
    row['label']=f'ray_R{R}_b{b}'
    rows.append(row)
a=mp.mpf('3.001'); H=mp.mpf('.18')
b=-mp.mpf('.999')*a/mp.sqrt(1-2/a-H*H*a*a)
row=compute(a,H,'10000',b)
row['label']='strong_ray'
rows.append(row)
result=dict(dps=mp.mp.dps,case_count=len(rows),cumulative_case_count=23,records=rows)
text=json.dumps(result,indent=2)+'\n'
(Path(__file__).parent/'REPLAY_RESULT.json').write_text(text)
print(text,end='')
