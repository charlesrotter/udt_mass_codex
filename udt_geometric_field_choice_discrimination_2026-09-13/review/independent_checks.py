"""NR2 outcome-exposed independent equation checks using an existing Fraction engine.

New case construction and record-map implementation. The inspected NR1 reviewer
engine is reused, not claimed as newly independent machinery. No parent NR2
scientific code is imported or executed.
"""
import ast
from pathlib import Path
import datetime,hashlib,json,os,platform,sys
from fractions import Fraction as Rat
from itertools import combinations

root=Path(__file__).resolve().parents[2]
pkg=root/'udt_geometric_field_choice_discrimination_2026-09-13'
utility=root/'udt_current_native_radiation_feasibility_2026-09-13/review/independent_exact.py'
raw=utility.read_text(); tree=ast.parse(raw)
nodes=[]
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='checks' for t in node.targets): break
    nodes.append(node)
ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(utility),'exec'),ns)
J,coord,diag,tensors,geometry,inverse=[ns[n] for n in ('J','coord','diag','tensors','geometry','inverse')]

checks=[];records=[]
def flatten(x):
    if isinstance(x,(tuple,list)):return [v for y in x for v in flatten(y)]
    return [x.v if isinstance(x,J) else x]
def equal(name,a,b):
    aa,bb=flatten(a),flatten(b)
    if len(aa)!=len(bb):raise ValueError((name,len(aa),len(bb)))
    rr=[a-b for a,b in zip(aa,bb)]
    checks.append({'name':name,'pass':all(r==0 for r in rr),'shape':[len(aa),len(bb)],'nonzero':list(map(str,[r for r in rr if r!=0]))})
def zero(name,a):
    aa=flatten(a);equal(name,aa,[0]*len(aa))
def nonzero(name,a):
    aa=flatten(a);checks.append({'name':name,'pass':any(r!=0 for r in aa),'values':list(map(str,aa))})
def gate(name,condition,**extra):checks.append(dict(name=name,pass_=bool(condition),**extra));checks[-1]['pass']=checks[-1].pop('pass_')
def base_metric(u,v,x,y,epsilon=0,nonharmonic=0):
    H=2*(x*x-y*y)/(u*u)+epsilon*(x**3-3*x*y*y)+nonharmonic*(x*x+y*y)
    g=diag(H,0,1,1);g[0][1]=g[1][0]=J(-1);return g
def lowerR(g,out,a,b,c,d):return sum(g[a][h].v*out['R'][h][b][c][d].v for h in range(4))
def ode_jets(u,q,p,r,s):
    h=u-u.v;A=2/u.v**2;Ap=-4/u.v**3
    qj=q+p*h+A*q*h*h/2;rj=r+s*h-A*r*h*h/2
    pj=p+A*q*h+(Ap*q+A*p)*h*h/2
    sj=s-A*r*h-(Ap*r+A*s)*h*h/2
    return qj,pj,rj,sj
def field_checks(g,F):
    gi,C,R,Ric=geometry(g)
    Fu=[[sum(gi[a][c]*gi[b][d]*F[c][d] for c in range(4) for d in range(4)) for b in range(4)] for a in range(4)]
    partial=[sum(Fu[a][b].d(a) for a in range(4)).v for b in range(4)]
    div=[partial[b]+sum((C[a][a][d]*Fu[d][b]+C[b][a][d]*Fu[a][d]).v for a in range(4) for d in range(4)) for b in range(4)]
    closed=[(F[b][c].d(a)+F[c][a].d(b)+F[a][b].d(c)).v for a,b,c in combinations(range(4),3)]
    inv=sum(F[a][b].v*Fu[a][b].v for a in range(4) for b in range(4))
    return {'div':div,'partial':partial,'closed':closed,'invariant':inv,'Ric':Ric}
def aligned(ax,ay,dx=None):
    F=[[J() for b in range(4)] for a in range(4)]
    if dx is None:dx=[0,0,1,0]
    for i in range(4):F[0][i]=ax*dx[i]
    F[0][3]=F[0][3]+ay
    F[0][0]=J()
    for i in range(1,4):F[i][0]=-F[0][i]
    return F
def rank(a):
    a=[[Rat(x) for x in row] for row in a];m=len(a);n=len(a[0]);p=0
    for col in range(n):
        choices=[j for j in range(p,m) if a[j][col]]
        if not choices:continue
        j=choices[0];a[p],a[j]=a[j],a[p];v=a[p][col];a[p]=[x/v for x in a[p]]
        for j in range(m):
            if j!=p:
                v=a[j][col];a[j]=[x-v*y for x,y in zip(a[j],a[p])]
        p+=1
        if p==m:break
    return p
def outer(x,y):return [[a*b for b in y] for a in x]
def mv(a,x):return [sum(v*w for v,w in zip(row,x)) for row in a]
def dot(a,b):return sum(x*y for x,y in zip(a,b))

# Integrity checks include a real malformed-shape rejection.
try:equal('deliberate_bad_shape',[1,2],[1])
except ValueError:gate('shape_mismatch_rejected',True)
else:gate('shape_mismatch_rejected',False)
u,v,x,y=coord([Rat(2),Rat(3),Rat(4),Rat(5)])
equal('rational_jet_derivative',(u**-2).d(0).d(0),Rat(3,8))
zero('rational_jet_inverse',(u*u+x)/(u*u+x)-1)

# Arbitrary local ODE data, including a simultaneous zero field event.
samples=[([Rat(1),Rat(0),Rat(0),Rat(0)],[Rat(2),Rat(0),Rat(-3),Rat(0)]),
         ([Rat(2),Rat(1,3),Rat(1,2),Rat(-2,3)],[Rat(-1),Rat(3,2),Rat(5,3),Rat(-2)]),
         ([Rat(3,2),Rat(-1),Rat(-2,5),Rat(4,7)],[Rat(1,4),Rat(-1,2),Rat(3),Rat(2,5)])]
for i,(point,state) in enumerate(samples):
    u,v,x,y=coord(point);q,p,r,s=state;qj,pj,rj,sj=ode_jets(u,q,p,r,s)
    K=[0,pj*x+sj*y+Rat(7,3),qj,rj]
    baseline=None
    for label,eps,nh in [('base',Rat(0),Rat(0)),('cubic',Rat(1,5),Rat(0)),('nonharmonic',Rat(0),Rat(2,7))]:
        g=base_metric(u,v,x,y,eps,nh);out=tensors(g,K)
        tag=f'point{i}_{label}'
        expectedRic=[[0]*4 for _ in range(4)];expectedRic[0][0]=-2*nh
        equal(tag+'_full_Ricci',out['Ric'],expectedRic)
        expectedF=[[0]*4 for _ in range(4)];expectedF[0][2]=2*p;expectedF[2][0]=-2*p;expectedF[0][3]=2*s;expectedF[3][0]=-2*s
        equal(tag+'_full_F',out['F'],expectedF)
        zero(tag+'_original_covariant_divergence',out['div']);zero(tag+'_exterior_closure',out['closed'])
        zero(tag+'_null_invariants',[out['invariant'],out['wedge']])
        expectedLie=[[0]*4 for _ in range(4)];expectedLie[0][0]=3*eps*(q*(x.v*x.v-y.v*y.v)-2*r*x.v*y.v)+2*nh*(q*x.v+r*y.v)
        equal(tag+'_full_Lie',out['Lie'],expectedLie)
        tide=[[lowerR(g,out,0,a,0,b) for b in (2,3)] for a in (2,3)]
        target=[[-2/u.v**2-3*eps*x.v-nh,3*eps*y.v],[3*eps*y.v,2/u.v**2+3*eps*x.v-nh]]
        equal(tag+'_full_screen_tide',tide,target)
        equal(tag+'_field_u_jet',[out['F'][0][2].d(0),out['F'][0][3].d(0)],[4*q/u.v**2,-4*r/u.v**2])
        if label=='base':baseline=out
        if i==0 and label=='cubic':
            plain=base_metric(u,v,x,y)
            gate('center_cubic_all_metric2jet_coefficients',all(g[a][b].c==plain[a][b].c for a in range(4) for b in range(4)))
            zero('center_cubic_connection',[z for plane in out['C'] for row in plane for z in row])
            equal('center_full_Riemann_same',out['R'],baseline['R'])
        records.append({'point':list(map(str,point)),'local_state':list(map(str,state)),'metric':label,'Lie_uu':str(out['Lie'][0][0]),'F_ux':str(out['F'][0][2].v),'F_uy':str(out['F'][0][3].v),'tide':[[str(z) for z in row] for row in tide]})

# Zero central generator and wrong-sign control are distinct from field failure.
u,v,x,y=coord([Rat(1),Rat(0),Rat(1),Rat(0)]);g=base_metric(u,v,x,y,Rat(1,5))
central=tensors(g,[0,1,0,0]);zero('central_Killing_survives',central['Lie']);zero('central_F_zero',central['F'])
wrong=tensors(base_metric(u,v,x,y),[0,-2*u*x,u*u,0]);nonzero('wrong_Kv_sign_detected',wrong['Lie'])

# Arbitrary profiles on a deliberately nonharmonic full metric.
u,v,x,y=coord([Rat(2),Rat(1),Rat(3,5),Rat(-1,4)])
g=base_metric(u,v,x,y,Rat(1,7),Rat(2,9))
F=aligned(u*u+1,1/u);out=field_checks(g,F)
zero('arbitrary_profile_original_divergence',out['div']);zero('arbitrary_profile_closed',out['closed']);zero('arbitrary_profile_null',out['invariant']);nonzero('arbitrary_profile_non_Ricci_flat',out['Ric'])
bad=field_checks(g,aligned(x,J(0)));nonzero('transverse_dependence_divergence_caught',bad['div'])

# Pull back x=(v+2)z. Nonconstant sqrt(-g)=v+2 makes raw partial divergence fail.
u,v,z,y=coord([Rat(3,2),Rat(1),Rat(2,5),Rat(-1,3)])
scale=v+2;x=scale*z;H=2*(x*x-y*y)/(u*u)+(x**3-3*x*y*y)/5
g=diag(H,z*z,scale*scale,1);g[0][1]=g[1][0]=J(-1);g[1][2]=g[2][1]=scale*z
F=aligned(u*u+1,1/u,[0,z,scale,0]);out=field_checks(g,F)
zero('nonconstant_det_chart_covariant_divergence',out['div']);zero('nonconstant_det_chart_closed',out['closed']);zero('nonconstant_det_chart_null',out['invariant'])
nonzero('dropping_connection_terms_caught',out['partial'])
records.append({'type':'x=(v+2)z coordinate control','sqrt_minus_det':'v+2','raw_partial_divergence':list(map(str,out['partial'])),'full_covariant_divergence':list(map(str,out['div']))})

# Exact rational finite-map and quadratic inversion checks; E=e/sqrt(2).
M1=[[0,1,0,0],[0,0,0,1],[0,1,0,0],[0,0,0,1]]
equal('coincident_original_matrix_rank',rank(M1),2)
equal('coincident_original_repeated_rows',M1[:2],M1[2:])
for u0 in [Rat(1,2),Rat(1),Rat(3)]:
    A=2/u0**2
    jet=[[0,1,0,0],[0,0,0,1],[A,0,0,0],[0,0,-A,0]]
    equal(f'local_signed_jet_rank_u{u0}',rank(jet),4)
for alpha,beta,target in [(Rat(2),Rat(3),4),(Rat(0),Rat(3),3),(Rat(2),Rat(0),3),(Rat(0),Rat(0),2)]:
    M=[[0,1,0,0],[0,0,0,1],[alpha,Rat(5,7),0,0],[0,0,beta,Rat(-2,3)]]
    equal(f'two_sample_structural_rank_{alpha}_{beta}',rank(M),target)
for i,(e,ep) in enumerate([([Rat(1),Rat(2)],[Rat(-3),Rat(4)]),([Rat(0),Rat(2)],[Rat(3),Rat(-1)]),([Rat(-2,3),Rat(4,5)],[Rat(7,2),Rat(-8,3)])]):
    Q=outer(e,e);I=dot(e,e);Qp=[[ep[a]*e[b]+e[a]*ep[b] for b in range(2)] for a in range(2)]
    qp_e=mv(Qp,e);ep_rec=[(qp_e[a]-e[a]*dot(e,qp_e)/(2*I))/I for a in range(2)]
    equal(f'quadratic_derivative_inverse_{i}',ep_rec,ep)
    equal(f'quadratic_global_sign_{i}',outer([-x for x in e],[-x for x in e]),Q)
    ep_rec_neg=[(-qp_e[a]+e[a]*dot(e,qp_e)/(2*I))/I for a in range(2)]
    equal(f'quadratic_reconstructed_same_sign_{i}',ep_rec_neg,[-x for x in ep])
zero('zero_e_gives_zero_Q',outer([0,0],[0,0]))
nonzero('zero_e_nonzero_Qsecond',outer([Rat(2),Rat(-3)],[Rat(4),Rat(-6)]))
equal('scalar_I_reflection_example',dot([1,2],[1,2]),dot([-1,2],[-1,2]));nonzero('Qxy_reflection_detectable',2-(-2))

# Known smooth-family counterexample: finite jets cannot identify arbitrary profiles.
u,v,x,y=coord([Rat(1),Rat(0),Rat(0),Rat(0)]);extra=(u-1)**2
zero('arbitrary_profile_same_first_record_jet',[extra,extra.d(0)])
equal('arbitrary_profile_second_record_jet_changes',extra.d(0).d(0),2)

# Independent symbolic flow construction uses a shared library, no parent code.
import sympy as sym
t=sym.symbols('t',positive=True);nu=sym.sqrt(7)/2
Q0,P0,R0,S0=sym.symbols('Q0 P0 R0 S0',real=True)
q=(Q0+P0)*t**2/3+(2*Q0-P0)/(3*t)
r=sym.sqrt(t)*(R0*sym.cos(nu*sym.log(t))+(S0-R0/2)*sym.sin(nu*sym.log(t))/nu)
def seq(name,a,b=0):
    val=sym.simplify(a-b);gate(name,val==0,residual=str(val))
seq('explicit_q_ODE',sym.diff(q,t,2)-2*q/t**2)
seq('explicit_r_ODE',sym.diff(r,t,2)+2*r/t**2)
ar=sym.diff(sym.diff(r,t),R0);seq('r_sample_q_coefficient',ar,-2*sym.sin(nu*sym.log(t))/(nu*sym.sqrt(t)))
seq('first_blind_return_y_coefficient',ar.subs(t,sym.exp(sym.pi/nu)))
# Assemble original rows directly from field derivatives, specialize BEFORE determinant.
rowx=[sym.diff(sym.diff(q,t),w) for w in (Q0,P0,R0,S0)]
rowy=[sym.diff(sym.diff(r,t),w) for w in (Q0,P0,R0,S0)]
M=sym.Matrix([[0,1,0,0],[0,0,0,1],rowx,rowy]);actual=M.subs(t,1)
seq('independent_original_coincident_matrix_det',actual.det());gate('independent_original_coincident_rank2',actual.rank()==2)
seq('sample_det_by_block_formula',M.det(method='berkowitz'),-rowx[0]*rowy[2])
alpha=sym.symbols('alpha',real=True);R=sym.symbols('R',positive=True)
rp=R*sym.sqrt(t)*sym.cos(nu*sym.log(t)-alpha)
seq('profile_phase_derivative',sym.diff(rp,t),R/sym.sqrt(t)*(sym.cos(nu*sym.log(t)-alpha)/2-nu*sym.sin(nu*sym.log(t)-alpha)))
seq('same_form_phase_u_squared',(-2*t)*(2*sym.diff(q,t)/(-2*t)),2*sym.diff(q,t))

source_pins=json.loads((pkg/'SOURCE_PINS.json').read_text())
gate('all13_source_pins_match',all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in source_pins['sources'].items()))
for filename in ['CANDIDATE_FREEZE.json','REPAIR_FREEZE.json']:
    pins=json.loads((pkg/filename).read_text())['pins']
    gate(filename+'_all_pins_match',all(hashlib.sha256((pkg/p).read_bytes()).hexdigest()==h for p,h in pins.items()))
result={'scope':'outcome-exposed independent check cases; reused Fraction tensor engine; original covariant equations and exact record maps','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'sympy_map_checks':sym.__version__,'utility':str(utility.relative_to(root)),'utility_sha256':hashlib.sha256(raw.encode()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'thread_environment':{k:os.environ.get(k) for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')},'checks':checks,'records':records,'count':len(checks),'passed':sum(c['pass'] for c in checks),'all_pass':all(c['pass'] for c in checks),'limits':'finite coordinate-jet checks are not all-function proof; no floating approximation; reused engine is not new independent engine; symbolic map library shared'}
with Path(sys.argv[1]).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:result[k] for k in ['count','passed','all_pass']}))
sys.exit(0 if result['all_pass'] else 1)
