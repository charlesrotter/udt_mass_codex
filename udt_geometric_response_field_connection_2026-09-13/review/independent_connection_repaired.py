"""GFC1 reviewer original connection, exact rational jets; no SymPy imports.

Reuse only inspected NR1 reviewer engine definitions. Values of F from screen
jets are exact at chosen events; no derivatives beyond valid jet order claimed.
"""
import ast,datetime,hashlib,json,os,platform,sys
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
root=Path(__file__).resolve().parents[2]
pkg=root/'udt_geometric_response_field_connection_2026-09-13'
utility=root/'udt_current_native_radiation_feasibility_2026-09-13/review/independent_exact.py'
tree=ast.parse(utility.read_text());nodes=[]
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='checks' for t in node.targets):break
    nodes.append(node)
ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(utility),'exec'),ns)
J,coord,diag,geometry=[ns[n] for n in ('J','coord','diag','geometry')]
checks=[];records=[]
def flatten(x):
    if isinstance(x,(tuple,list)):return [v for y in x for v in flatten(y)]
    return [x.v if isinstance(x,J) else Q(x)]
def equal(name,a,b):
    aa,bb=flatten(a),flatten(b)
    if len(aa)!=len(bb):raise ValueError((name,len(aa),len(bb)))
    rr=[x-y for x,y in zip(aa,bb)]
    checks.append({'name':name,'pass':all(r==0 for r in rr),'entries':len(rr),'nonzero':[str(r) for r in rr if r]})
def zero(name,a):
    aa=flatten(a);equal(name,aa,[0]*len(aa))
def nonzero(name,a):
    aa=flatten(a);checks.append({'name':name,'pass':any(r!=0 for r in aa),'values':list(map(str,aa))})
def gate(name,b):checks.append({'name':name,'pass':bool(b)})
def cast(x):return x if isinstance(x,J) else J(x)
def vec(*x):return list(map(cast,x))
def plus(a,b):return [x+y for x,y in zip(a,b)]
def scale(c,a):return [c*x for x in a]
def dot(g,a,b):return sum(g[i][j]*a[i]*b[j] for i in range(4) for j in range(4))
def deriv(a,k):return [x.d(k) for x in a]
def cov(C,a,k):return [a[i].d(k)+sum(C[i][k][j]*a[j] for j in range(4)) for i in range(4)]
def connection(g,C,a,b):return [dot(g,a,cov(C,b,k)) for k in range(4)]
def exterior(a):return [[a[j].d(i)-a[i].d(j) for j in range(4)] for i in range(4)]
def firstjet(a):return [z for x in a for z in [x]+[x.d(i) for i in range(4)]]
def aligned(ax,ay):
    F=[[J() for _ in range(4)] for _ in range(4)]
    F[0][2]=cast(ax);F[0][3]=cast(ay);F[2][0]=-F[0][2];F[3][0]=-F[0][3]
    return F

def frame_geometry(point):
    u,v,x,y=coord(point);H=2*(x*x-y*y)/(u*u)
    g=diag(H,0,1,1);g[0][1]=g[1][0]=J(-1)
    gi,C,R,Ric=geometry(g)
    return (u,v,x,y,H,g,gi,C,R,Ric,vec(0,1,0,0),vec(1,H/2,0,0),vec(0,0,1,0),vec(0,0,0,1))

def sqrt_at(z,c0):
    assert z.v==c0*c0
    dz=z-z.v
    return c0+dz/(2*c0)-dz*dz/(8*c0**3)

def gauge(g,C,a,b,t):
    co=(1-t*t)/(1+t*t);si=2*t/(1+t*t)
    ar=plus(scale(co,a),scale(-si,b));br=plus(scale(si,a),scale(co,b))
    return ar,br,vec(*[2*t.d(i)/(1+t*t) for i in range(4)])

try:equal('deliberate_bad_shape',[1,2],[1])
except ValueError:gate('shape_mismatch_rejected',True)
else:gate('shape_mismatch_rejected',False)
u,v,x,y=coord([Q(2),Q(3),Q(4),Q(5)])
equal('jet_inverse_second_derivative',(u**-2).d(0).d(0),Q(3,8))
zero('jet_inverse_algebra',(u*u+x)/(u*u+x)-1)
points=[(Q(1),Q(0),Q(0),Q(0)),(Q(2),Q(1,3),Q(1,2),Q(-2,3)),(Q(3,2),Q(-1),Q(-2,5),Q(4,7))]
for i,point in enumerate(points):
    u,v,x,y,H,g,gi,C,R,Ric,k,n,X,Y=frame_geometry(point)
    tag=f'point{i}'
    zero(tag+'_full_Ricci',Ric)
    zero(tag+'_parallel_null_derivative',[cov(C,k,j) for j in range(4)])
    ntarget=[vec(-H.d(2)/2 if j==0 else 0,0,0,0) for j in range(4)]
    ntarget=[vec(0,0,-H.d(2)/2,-H.d(3)/2) if j==0 else vec(0,0,0,0) for j in range(4)]
    equal(tag+'_other_null_derivative',[cov(C,n,j) for j in range(4)],ntarget)
    naturalA=connection(g,C,X,Y);zero(tag+'_natural_A',firstjet(naturalA));zero(tag+'_natural_F',exterior(naturalA))
    Ruxux=sum(g[0][a].v*R[a][2][0][2].v for a in range(4))
    equal(tag+'_nonflat_Ruxux',Ruxux,-2/u.v**2)
    a=u+x*v+y*y;b=u*u+y*v-x
    E1=plus(X,scale(a,k));E2=plus(Y,scale(b,k))
    equal(tag+'_parallel_lift_Gram',[[dot(g,A,B) for B in (E1,E2)] for A in (E1,E2)],[[1,0],[0,1]])
    Ap=connection(g,C,E1,E2);zero(tag+'_all_coordinate_parallel_lift_A',firstjet(Ap))
    E1r=scale(-1,E1);Ar=connection(g,C,E1r,E2);zero(tag+'_opposite_orientation_F',exterior(Ar))
    t=u+x-v/3+y*y
    G1,G2,dlambda=gauge(g,C,E1,E2,t);Ag=connection(g,C,G1,G2)
    equal(tag+'_SO2_gauge_A',firstjet(Ag),firstjet(dlambda));zero(tag+'_SO2_gauge_curvature',exterior(Ag))
    G1r,G2r,drev=gauge(g,C,E1r,E2,t)
    equal(tag+'_reversed_orientation_gauge_A',firstjet(connection(g,C,G1r,G2r)),firstjet(drev))
    # Other-null compatible screens: arbitrary coordinate dependence retained.
    N1=plus(X,scale(a,n));N2=plus(Y,scale(b,n))
    equal(tag+'_other_null_lift_Gram',[[dot(g,A,B) for B in (N1,N2)] for A in (N1,N2)],[[1,0],[0,1]])
    An=connection(g,C,N1,N2);An_expected=vec((a*H.d(3)-b*H.d(2))/2,0,0,0)
    equal(tag+'_other_null_original_A',firstjet(An),firstjet(An_expected));equal(tag+'_other_null_dA',exterior(An),exterior(An_expected))
    # Prespecified arbitrary profiles with simultaneous zero at u=1.
    ax=u-1;ay=(u-1)**2
    Na=plus(X,scale(u*u*ay/2,n));Nb=plus(Y,scale(u*u*ax/2,n))
    Aaligned=connection(g,C,Na,Nb);targetA=vec(-ax*x-ay*y,0,0,0)
    equal(tag+'_smooth_zero_including_profile_A',firstjet(Aaligned),firstjet(targetA));equal(tag+'_smooth_zero_including_profile_F',exterior(Aaligned),aligned(ax,ay))
    if i==0:
        equal('simultaneous_zero_screen_base',[Na,Nb],[X,Y]);zero('simultaneous_zero_F',exterior(Aaligned));equal('profile_derivative_at_zero',ax.d(0),1)
    # Source-free checks use independently built aligned tensor, not invalid third jet.
    F=aligned(ax,ay);Fu=[[sum(gi[a][c]*gi[b][d]*F[c][d] for c in range(4) for d in range(4)) for b in range(4)] for a in range(4)]
    divergence=[sum(Fu[a][b].d(a)+sum(C[a][a][d]*Fu[d][b]+C[b][a][d]*Fu[a][d] for d in range(4)) for a in range(4)) for b in range(4)]
    zero(tag+'_aligned_full_covariant_divergence',divergence)
    zero(tag+'_aligned_closed',[F[b][c].d(a)+F[c][a].d(b)+F[a][b].d(c) for a,b,c in combinations(range(4),3)])
    zero(tag+'_aligned_null',sum(F[a][b]*Fu[a][b] for a in range(4) for b in range(4)))
    # Rational representation of parent w=sqrt2*z: sqrt2 cancels from screen.
    h=u-u.v
    if i==0:z1=h;z2=h+h*h;c0=Q(1)
    elif i==1:z1=Q(2,3)+h/3+h*h/5;z2=Q(2,3)-h/4+h*h/7;c0=Q(5,3)
    else:z1=Q(2,3)+h/2;z2=-Q(2,3)+h/3;c0=Q(5,3)
    c=sqrt_at(1+2*(z1*z1+z2*z2),c0)
    S11=1+2*z1*z1/(c+1);S12=2*z1*z2/(c+1);S22=1+2*z2*z2/(c+1)
    nk=plus(n,k)
    B1=plus(scale(z1,nk),plus(scale(S11,X),scale(S12,Y)))
    B2=plus(scale(z2,nk),plus(scale(S12,X),scale(S22,Y)))
    equal(tag+'_boost_Gram',[[dot(g,A,B) for B in (B1,B2)] for A in (B1,B2)],[[1,0],[0,1]])
    Bw=2*(z2*z1.d(0)-z1*z2.d(0))/(c+1)
    Ab=connection(g,C,B1,B2);Abe=vec(Bw-2*(z2*x+z1*y)/(u*u),0,0,0)
    equal(tag+'_boost_original_full_A',firstjet(Ab),firstjet(Abe))
    Fb=exterior(Ab);Fbe=aligned(2*z2/(u*u),2*z1/(u*u))
    equal(tag+'_boost_original_dA',Fb,Fbe)
    frame=[plus(scale(c,nk),plus(scale(2*z1,X),scale(2*z2,Y))),plus(n,scale(-1,k)),B1,B2]
    zero(tag+'_full_scaled_frame_connection_off_du',[dot(g,A,cov(C,B,j)) for A in frame for B in frame for j in (1,2,3)])
    ambient=[[sum(dot(g,B1,vec(*[sum(R[p][q][a][b].v*B2[q].v for q in range(4)) for p in range(4)])).v for _ in [0]) for b in range(4)] for a in range(4)]
    equal(tag+'_ambient_R_projection',ambient,Fb)
    if i==1:
        nonzero('catch_omitted_moving_B',[Ab[0]-Abe[0]+Bw]);zero('moving_B_curvature_blindness',exterior(vec(Bw,0,0,0)))
        partialA=[dot(g,B1,deriv(B2,j)) for j in range(4)]
        nonzero('catch_omitted_Christoffel',[p-q for p,q in zip(partialA,Ab)])
        bad1=plus(X,scale(z1,nk));bad2=plus(Y,scale(z2,nk))
        nonzero('catch_omitted_spatial_boost_correction',[dot(g,bad1,bad1)-1,dot(g,bad2,bad2)-1,dot(g,bad1,bad2)])
        nonzero('catch_wrong_curvature_sign',[[Fb[a][b]+Fbe[a][b] for b in range(4)] for a in range(4)])
        nonzero('catch_natural_not_nonzero_target',Fbe)
    # Local Killing ODE jets and exact full-potential gauge (source-first route).
    q0,p0,r0,s0=Q(2),Q(-1),Q(-3),Q(2)
    q=q0+p0*h+q0*h*h/u.v**2;r=r0+s0*h-r0*h*h/u.v**2
    p=p0+2*q0*h/u.v**2+(2*p0/u.v**2-4*q0/u.v**3)*h*h/2
    s0j=s0-2*r0*h/u.v**2+(-2*s0/u.v**2+4*r0/u.v**3)*h*h/2
    K=vec(0,p*x+s0j*y,q,r);Kflat=vec(*[sum(g[a][b]*K[b] for b in range(4)) for a in range(4)])
    C1=plus(X,scale(u*u*s0j,n));C2=plus(Y,scale(u*u*p,n));Ak=connection(g,C,C1,C2)
    lam=q*x+r*y;dlam=vec(*[lam.d(a) for a in range(4)])
    equal(tag+'_general_K_potential_difference',firstjet(plus(Ak,dlam)),firstjet(Kflat))
    equal(tag+'_general_K_screen_curvature',exterior(Ak),exterior(Kflat))
    lt=lam-lam.v;sn=lt;co=1-lt*lt/2
    RG1=plus(scale(co,C1),scale(-sn,C2));RG2=plus(scale(sn,C1),scale(co,C2))
    Arot=connection(g,C,RG1,RG2)
    equal(tag+'_actual_rotated_frame_potential_Kflat',firstjet(Arot),firstjet(Kflat))
    records.append({'point':list(map(str,point)),'A_boost':list(map(str,flatten(Ab))),'B_boost':str(Bw.v),'F_ux':str(Fb[0][2].v),'F_uy':str(Fb[0][3].v),'A_null_lift':list(map(str,flatten(Aaligned)))})

try:sqrt_at(J(17),Q(3))
except AssertionError:gate('catch_original_invalid_rational_sqrt_input',True)
else:gate('catch_original_invalid_rational_sqrt_input',False)

sources=json.loads((pkg/'SOURCE_PINS.json').read_text())['sources']
gate('all18_source_pins',all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in sources.items()))
freeze=json.loads((pkg/'CANDIDATE_FREEZE.json').read_text())['pins']
gate('all6_initial_candidate_pins',all(hashlib.sha256((pkg/p).read_bytes()).hexdigest()==h for p,h in freeze.items()))
result={'kind':'outcome-exposed exact finite rational coordinate-jet checks with source-first analytic reconstruction','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'engine':str(utility.relative_to(root)),'engine_sha256':hashlib.sha256(utility.read_bytes()).hexdigest(),'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'thread_environment':{k:os.environ.get(k) for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')},'jet_order':2,'limitations':'F values valid; its further derivatives from these frame jets not used. All-function scope belongs to analytic proof, not finite samples.','checks':checks,'records':records,'count':len(checks),'passed':sum(c['pass'] for c in checks),'all_pass':all(c['pass'] for c in checks)}
with Path(sys.argv[1]).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'count':result['count'],'passed':result['passed'],'all_pass':result['all_pass'],'failed':[c for c in checks if not c['pass']],'records':records}))
sys.exit(0 if result['all_pass'] else 1)
