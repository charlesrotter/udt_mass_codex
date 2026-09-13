"""NR1 reviewer: exact second-order rational coordinate jets, no scientific imports.

Finite-point checks are equation checks, not an all-function proof. Metric inverse
is Gauss-Jordan over a truncated Taylor algebra. Curvature uses connection jets;
Maxwell divergence uses all connection terms, not the parent's density shortcut.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from pathlib import Path
import datetime
import hashlib
import json
import os
import platform
import sys

D = 4
Z = (0,)*D
UNITS = [tuple(int(i == j) for i in range(D)) for j in range(D)]

class J:
    def __init__(self, x=0):
        self.c = {k: Q(v) for k,v in x.items() if v} if isinstance(x,dict) else ({Z:Q(x)} if x else {})
    @property
    def v(self): return self.c.get(Z,Q(0))
    def __add__(self,b):
        b=cast(b); c=self.c.copy()
        for k,v in b.c.items(): c[k]=c.get(k,Q(0))+v
        return J(c)
    __radd__=__add__
    def __neg__(self): return J({k:-v for k,v in self.c.items()})
    def __sub__(self,b): return self+-cast(b)
    def __rsub__(self,b): return cast(b)+-self
    def __mul__(self,b):
        b=cast(b);c={}
        for i,u in self.c.items():
            for j,v in b.c.items():
                k=tuple(a+b for a,b in zip(i,j))
                if sum(k)<=2:c[k]=c.get(k,Q(0))+u*v
        return J(c)
    __rmul__=__mul__
    def inverse(self):
        assert self.v != 0
        a=self.v;r=(self-a)*(1/a)
        return (1-r+r*r)*(1/a)
    def __truediv__(self,b): return self*cast(b).inverse()
    def __rtruediv__(self,b): return cast(b)*self.inverse()
    def __pow__(self,n):
        assert isinstance(n,int)
        if n<0:return self.inverse()**(-n)
        out=J(1)
        for _ in range(n):out=out*self
        return out
    def d(self,a):
        c={}
        for k,v in self.c.items():
            if k[a]:
                p=list(k);p[a]-=1;c[tuple(p)]=v*k[a]
        return J(c)

def cast(x):return x if isinstance(x,J) else J(x)
def coord(values):return [J({Z:Q(v),UNITS[i]:Q(1)}) for i,v in enumerate(values)]
def matrix(n=D):return [[J() for _ in range(n)] for _ in range(n)]
def diag(*vals):return [[cast(vals[i] if i==j else 0) for j in range(D)] for i in range(D)]
def inverse(g):
    a=[row[:] + [J(int(i==j)) for j in range(D)] for i,row in enumerate(g)]
    for k in range(D):
        p=next(i for i in range(k,D) if a[i][k].v)
        a[k],a[p]=a[p],a[k]
        h=a[k][k];a[k]=[v/h for v in a[k]]
        for i in range(D):
            if i!=k:
                h=a[i][k];a[i]=[v-h*w for v,w in zip(a[i],a[k])]
    return [row[D:] for row in a]

def geometry(g):
    gi=inverse(g)
    C=[[[sum(gi[a][e]*(g[e][b].d(c)+g[e][c].d(b)-g[b][c].d(e))/2 for e in range(D)) for c in range(D)] for b in range(D)] for a in range(D)]
    R=[[[[C[a][d][b].d(c)-C[a][c][b].d(d)+sum(C[a][c][e]*C[e][d][b]-C[a][d][e]*C[e][c][b] for e in range(D)) for d in range(D)] for c in range(D)] for b in range(D)] for a in range(D)]
    Ric=[[sum(R[a][b][a][d].v for a in range(D)) for d in range(D)] for b in range(D)]
    return gi,C,R,Ric

def tensors(g,K):
    gi,C,R,Ric=geometry(g)
    K=[cast(k) for k in K]
    lower=[sum(g[a][b]*K[b] for b in range(D)) for a in range(D)]
    F=[[lower[b].d(a)-lower[a].d(b) for b in range(D)] for a in range(D)]
    Fu=[[sum(gi[a][c]*gi[b][d]*F[c][d] for c in range(D) for d in range(D)) for b in range(D)] for a in range(D)]
    div=[sum(Fu[a][b].d(a)+sum(C[a][a][d]*Fu[d][b]+C[b][a][d]*Fu[a][d] for d in range(D)) for a in range(D)).v for b in range(D)]
    Lie=[[sum(K[c]*g[a][b].d(c)+g[c][b]*K[c].d(a)+g[a][c]*K[c].d(b) for c in range(D)).v for b in range(D)] for a in range(D)]
    closed=[(F[b][c].d(a)+F[c][a].d(b)+F[a][b].d(c)).v for a,b,c in combinations(range(D),3)]
    inv=sum(F[a][b].v*Fu[a][b].v for a in range(D) for b in range(D))
    wedge=(F[0][1]*F[2][3]-F[0][2]*F[1][3]+F[0][3]*F[1][2]).v
    T=[[sum(F[a][c].v*gi[c][d].v*F[b][d].v for c in range(D) for d in range(D))-g[a][b].v*inv/4 for b in range(D)] for a in range(D)]
    rhs=[-2*sum(gi[a][b].v*Ric[b][c]*K[c].v for b in range(D) for c in range(D)) for a in range(D)]
    return dict(gi=gi,C=C,R=R,Ric=Ric,F=F,div=div,Lie=Lie,closed=closed,invariant=inv,wedge=wedge,T=T,rhs=rhs)

checks=[];records=[]
def flat(x):
    if isinstance(x,(list,tuple)):return [v for y in x for v in flat(y)]
    return [x.v if isinstance(x,J) else x]
def zero(name,x):
    vals=flat(x);ok=all(v==0 for v in vals)
    checks.append({'name':name,'pass':ok,'count':len(vals),'nonzero':[str(v) for v in vals if v]})
def equal(name,a,b):zero(name,[x-y for x,y in zip(flat(a),flat(b))])
def nonzero(name,x):
    vals=flat(x);checks.append({'name':name,'pass':any(v!=0 for v in vals),'values':[str(v) for v in vals]})
def pp(values,wrong_trace=False,wrong_k=False,parallel=False,flat_metric=False):
    u,v,x,y=coord(values);H=0 if flat_metric else 2*(x*x+(y*y if wrong_trace else -y*y))/(u*u)
    g=diag(H,0,1,1);g[0][1]=g[1][0]=J(-1)
    K=[0,1,0,0] if parallel else [0,(-2 if wrong_k else 2)*u*x,u*u,0]
    return g,K,tensors(g,K)

# Metadata and source checks are saved with the same bounded capture.
root=Path(__file__).resolve().parents[2]
pkg=root/'udt_current_native_radiation_feasibility_2026-09-13'
pins=json.loads((pkg/'SOURCE_PINS.json').read_text())
source_checks={p:hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in pins['sources'].items()}
freeze=json.loads((pkg/'CANDIDATE_FREEZE.json').read_text())
candidate_checks={p:hashlib.sha256((pkg/p).read_bytes()).hexdigest()==h for p,h in freeze['pins'].items()}
checks.append({'name':'17_exact_source_pins','pass':all(source_checks.values()),'checks':source_checks})
checks.append({'name':'5_candidate_freeze_pins','pass':all(candidate_checks.values()),'checks':candidate_checks})

# Small independent coordinate-jet algebra controls, not substantive theorem proof.
x,y,z,w=coord([Q(2),Q(3),Q(4),Q(5)])
zero('jet_inverse_identity',(x*x+y)/(x*x+y)-1)
equal('jet_second_derivative_rational',(1/(x*x)).d(0).d(0),Q(3,8))
equal('jet_mixed_derivative_product',(x*x*y).d(0).d(1),4)

samples=[(Q(1,2),Q(0),Q(1,3),Q(-2,5)),(Q(1),Q(2),Q(1),Q(1)),(Q(2),Q(-1),Q(-3,4),Q(5,6))]
for i,p in enumerate(samples):
    g,K,s=pp(p);u=p[0]
    zero(f'pp{i}_all_Ricci',s['Ric']);zero(f'pp{i}_all_Killing',s['Lie'])
    zero(f'pp{i}_closed',s['closed']);zero(f'pp{i}_covariant_divergence',s['div'])
    E=[[Q(0) for _ in range(D)] for _ in range(D)];E[0][2]=4*u;E[2][0]=-4*u
    equal(f'pp{i}_F_lower_then_d',s['F'],E)
    zero(f'pp{i}_null_invariant',s['invariant']);zero(f'pp{i}_wedge_square',s['wedge'])
    T=[[Q(0) for _ in range(D)] for _ in range(D)];T[0][0]=16*u*u
    equal(f'pp{i}_quadratic_comparison',s['T'],T)
    Ruxux=sum(g[0][a].v*s['R'][a][2][0][2].v for a in range(D))
    equal(f'pp{i}_nonzero_curvature_value',Ruxux,-2/u**2);nonzero(f'pp{i}_curved',Ruxux)
    zero(f'pp{i}_du_parallel',[s['C'][0][a][b] for a in range(D) for b in range(D)])
    H=g[0][0].v
    # A rational orthonormal coframe distinct from the parent's sqrt(2) display.
    e=[[Q(1,2)*(1-H),1,0,0],[-Q(1,2)*(1+H),1,0,0],[0,0,1,0],[0,0,0,1]]
    reconstructed=[[sum((-1 if a==0 else 1)*e[a][b]*e[a][c] for a in range(D)) for c in range(D)] for b in range(D)]
    equal(f'pp{i}_complete_rational_coframe',reconstructed,g)
    records.append({'type':'q=u^2, u>0','coordinates':list(map(str,p)),'F_ux':str(s['F'][0][2].v),'R_uxux':str(Ruxux),'C_uu':str(s['T'][0][0])})

p=samples[0]
_,_,s=pp(p,parallel=True);zero('curved_parallel_K_zero_F',s['F'])
_,_,s=pp(p,wrong_k=True);nonzero('catch_flipped_Kv_sign',s['Lie'])
_,_,s=pp(p,wrong_trace=True);nonzero('catch_wrong_transverse_trace_Ricci',s['Ric'])

# Independent nonvacuum sign control: Minkowski2 x unit round S2 in stereographic coordinates.
t,v,x,y=coord([Q(3,2),Q(2,3),Q(1,3),Q(2,5)])
b=4/(1+x*x+y*y)**2;g=diag(-1,1,b,b)
s=tensors(g,[0,0,-y,x]);expectedRic=[[Q(0) for _ in range(D)] for _ in range(D)];expectedRic[2][2]=expectedRic[3][3]=b.v
equal('product_sphere_full_Ricci',s['Ric'],expectedRic);zero('product_sphere_rotation_Killing',s['Lie'])
equal('product_sphere_divergence_sign',s['div'],[0,0,2*y.v,-2*x.v])
equal('product_sphere_Ricci_Killing_identity',s['div'],s['rhs']);nonzero('catch_drop_Ricci_K_hypothesis',s['div'])
nonzero('catch_reverse_Ricci_sign',[a+b for a,b in zip(s['div'],s['rhs'])])
records.append({'type':'Minkowski2 x S2 rotation','coordinates':['3/2','2/3','1/3','2/5'],'divergence':list(map(str,s['div']))})
# Ric(K)=0 may hold with nonzero Ricci and nonzero F: a boost in the flat factor.
s=tensors(g,[v,t,0,0]);zero('non_Ricci_flat_boost_Killing',s['Lie']);zero('non_Ricci_flat_boost_divergence',s['div']);nonzero('non_Ricci_flat_boost_F',s['F']);nonzero('non_Ricci_flat_boost_Ricci',s['Ric'])

# Flat null-rotation countercontrol, separately constructed from curved example.
u,v,x,y=coord([Q(2),Q(1),Q(3,5),Q(4,7)]);g=diag(0,0,1,1);g[0][1]=g[1][0]=J(-1)
s=tensors(g,[0,x,u,0]);zero('flat_null_rotation_Ricci',s['Ric']);zero('flat_null_rotation_Killing',s['Lie']);equal('flat_null_rotation_nonzero_Fux',s['F'][0][2],2);zero('flat_null_rotation_invariant',s['invariant'])
# An exact one-form not generated by a Killing field: arbitrary exactness is insufficient.
t,x,y,z=coord([Q(2),Q(1),Q(0),Q(0)]);g=diag(-1,1,1,1)
s=tensors(g,[0,t*t,0,0]);zero('arbitrary_exact_flat_form_closed',s['closed']);equal('arbitrary_exact_flat_form_divergence',s['div'],[0,-2,0,0]);nonzero('arbitrary_exact_flat_form_not_Killing',s['Lie'])

# Full-metric BE1-shaped identity on arbitrary positive rational b=exp(P), w=N^2.
# This off-equation metric is an equation-control, not a BE1 Ricci-flat member.
for i,p in enumerate([(Q(1),Q(1,3),Q(0),Q(0)),(Q(2),Q(-2,5),Q(1),Q(-1))]):
    t,x,y,z=coord(p);b=1+t*t+x*x;w=(1+t+x*x)**2;g=diag(-w,w,t*b,t/b)
    Pt=b.d(0)/b;Px=b.d(1)/b
    op=(Pt+t*Pt.d(0)-t*Px.d(1)).v
    for axis,sign in [(2,1),(3,-1)]:
        K=[0,0,0,0];K[axis]=1;s=tensors(g,K);target=[Q(0)]*D;target[axis]=-sign*op/(w.v*t.v)
        zero(f'be_off{i}_{axis}_Killing',s['Lie']);zero(f'be_off{i}_{axis}_closed',s['closed']);equal(f'be_off{i}_{axis}_full_covariant_identity',s['div'],target)
        nonzero(f'be_off{i}_{axis}_catch_omit_P_equation',s['div'])

# Independent on-equation control P=3log(t), N^2=t^4; no BE1 finite-mode membership claimed.
t,x,y,z=coord([Q(2),Q(1,3),Q(0),Q(0)]);g=diag(-t**4,t**4,t**4,t**-2)
for axis in (2,3):
    K=[0,0,0,0];K[axis]=1;s=tensors(g,K)
    zero(f'be_form_Kasner_{axis}_all_Ricci',s['Ric']);zero(f'be_form_Kasner_{axis}_divergence',s['div']);nonzero(f'be_form_Kasner_{axis}_nonnull',s['invariant'])

# P=0 background with full arbitrary positive lapse; invariant must be negative.
t,x,y,z=coord([Q(2),Q(1,3),Q(0),Q(0)]);w=(1+t+x*x)**2;g=diag(-w,w,t,t)
s=tensors(g,[0,0,1,0]);equal('BE1_P0_nonnull_full_lapse',s['invariant'],-2/(w.v*t.v))

record={'scope':'independent exact rational finite coordinate jets and direct covariant tensors; not all-function proof','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'implementation':'standard library fractions; no SymPy or parent scientific imports','thread_environment':{k:os.environ.get(k) for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')},'checks':checks,'records':records,'count':len(checks),'passed':sum(c['pass'] for c in checks),'all_pass':all(c['pass'] for c in checks),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with Path(sys.argv[1]).open('x') as stream:json.dump(record,stream,indent=2);stream.write('\n')
print(json.dumps({'count':record['count'],'passed':record['passed'],'all_pass':record['all_pass'],'records':records}))
sys.exit(0 if record['all_pass'] else 1)
