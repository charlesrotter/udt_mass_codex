"""CD2 author exact diagnostics: NOT CK existence/uniqueness certification."""
import ast
from fractions import Fraction as F
import hashlib
import json
import pathlib
import platform
import sympy as S

old=pathlib.Path('udt_source_metric_connection_campaign_2026-09-08/step_03/review/independent_interface_check.py')
pin='06c96d1df44bc67f697ebbe9a6100cdc0f281e20d68161fdb7ed7c423cb8071'
# Exact retained source pin; inspected pure functions only, no prior assertions.
pin='06c96d1df44bc67f697ebbe9a6100cdc0f281e20d681e61fdb7ed7c423cb8071'
raw=old.read_bytes()
assert hashlib.sha256(raw).hexdigest()==pin
nodes=[n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef)
       and n.name in ('zeros','curvature')]
assert len(nodes)==2
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(old),'exec'))
checks,reds,values=[],[],{}
def flat(x):
    if isinstance(x,(list,tuple)): return [v for y in x for v in flat(y)]
    if isinstance(x,S.MatrixBase): return list(x)
    return [x]
def check(name,items):
    residues=[S.simplify(i) for i in flat(items)]
    assert all(i==0 for i in residues),(name,residues)
    checks.append(name)
def red(name,items):
    residues=[S.simplify(i) for i in flat(items)]
    assert any(i!=0 for i in residues),(name,'false pass')
    assert all(not getattr(i,'free_symbols',set()) for i in residues),(name,residues)
    reds.append({'name':name,'exact_nonzero_residuals':[str(i) for i in residues if i!=0]})

# General lapse/shift null branch, not only a zero-shift or unit-rate example.
N=S.symbols('N',positive=True)
r1,r2,r3=S.symbols('r1 r2 r3',positive=True)
p=S.Matrix(S.symbols('p1 p2 p3',real=True))
shift=S.Matrix(S.symbols('b1 b2 b3',real=True))
sp=S.diag(r1**-2,r2**-2,r3**-2)
energy=S.sqrt((p.T*sp*p)[0])
gi=S.zeros(4)
gi[0,0]=-1/N**2
for i in range(3):
    gi[0,i+1]=gi[i+1,0]=shift[i]/N**2
    for j in range(3):
        gi[i+1,j+1]=sp[i,j]-shift[i]*shift[j]/N**2
Q=(shift.T*p)[0]-N*energy
q=S.Matrix([Q,*p])
ell=S.simplify(gi*q)
check('general_null_root',(q.T*ell)[0])
check('general_future_time_component',ell[0]-energy/N)
b=(gi[0,1:4]*p)[0]
disc=S.simplify(b*b-gi[0,0]*(p.T*gi[1:4,1:4]*p)[0])
check('discriminant_positive_domain',disc-energy**2/N**2)
check('displayed_root_branch',Q-(-b+S.sqrt(disc))/gi[0,0])
V=[S.simplify(ell[i+1]/ell[0]) for i in range(3)]
check('Hamiltonian_derivative_equals_minus_velocity',
      [S.diff(Q,p[i])+V[i] for i in range(3)])
anchor={N:S.Rational(3,2),r1:1,r2:2,r3:3,
        p[0]:2,p[1]:2,p[2]:3,shift[0]:S.Rational(1,3),shift[1]:0,shift[2]:0}
red('wrong_null_root_is_past',[-(energy/N).subs(anchor)])

# Variable change keeps the entire continuity equation, with nonconstant factors.
t,x,y,z=S.symbols('t x y z')
coords=(t,x,y,z)
m,W,L=[S.Function(k)(*coords) for k in ('m','W','L')]
vel=[S.Function('V'+str(i))(*coords) for i in range(3)]
n=m/(W*L)
div=S.diff(W*n*L,t)+sum(S.diff(W*n*L*vel[i],coords[i+1]) for i in range(3))
check('full_continuity_variable_change',
      div-S.diff(m,t)-sum(S.diff(m*vel[i],coords[i+1]) for i in range(3)))

def gauge(gi,first,second):
    conn,ric,scalar=curvature(gi,first,second)
    H=[sum(gi[c][d]*(first[c][b][d]-first[b][c][d]/2)
           for c in range(4) for d in range(4)) for b in range(4)]
    dinv=[[[-sum(gi[c][i]*first[a][i][j]*gi[j][d]
                for i in range(4) for j in range(4))
             for d in range(4)] for c in range(4)] for a in range(4)]
    DH=[[sum(dinv[a][c][d]*(first[c][b][d]-first[b][c][d]/2)+
             gi[c][d]*(second[a][c][b][d]-second[a][b][c][d]/2)
             for c in range(4) for d in range(4))-
          sum(conn[e][a][b]*H[e] for e in range(4))
          for b in range(4)] for a in range(4)]
    reduced=[[ric[a][b]-(DH[a][b]+DH[b][a])/2 for b in range(4)] for a in range(4)]
    return H,DH,reduced,ric

# Full metric-jet initial gauge and original equations after reduced acceleration.
# rho jets are supplied first; the CD1 constraint formulas solve A,Bprime.
for case,(a,rho,rp,rpp,E,beta,lam,B) in enumerate([
    (F(2,3),F(9,4),F(2,5),F(-1,3),F(5,3),F(-4,7),F(0),F(7,5)),
    (F(5,4),F(16,25),F(-3,7),F(2,9),F(3,2),F(5,8),F(-2),F(-3,4)),
    (F(1),F(2),F(0),F(1,5),F(4,3),F(-1),F(3,2),F(1)),
]):
    h=-rp/(2*rho); ap=a*h
    app=a*(3*rp*rp/(4*rho*rho)-rpp/(2*rho))
    hp=app/a-h*h
    T=beta*rho*E*E
    R3=-4*app/a-2*h*h
    A=(2*lam+2*T-R3-2*B*B)/(4*B)
    Bp=h*(A-B)-T/2
    Ap=F(17,13) # unconstrained diagnostic higher density/phase jet, not a solve
    g=[[F(0) for _ in range(4)] for _ in range(4)]
    gi=[[F(0) for _ in range(4)] for _ in range(4)]
    for i,c in enumerate((F(-1),F(1),a*a,a*a)):
        g[i][i]=c; gi[i][i]=1/c
    first= zeros(4,4,4); second=zeros(4,4,4,4)
    first[0][0][0]=2*(A+2*B)
    first[0][0][1]=first[0][1][0]=-2*h
    first[0][1][1]=-2*A
    second[0][1][0][0]=second[1][0][0][0]=2*(Ap+2*Bp)
    second[0][1][0][1]=second[0][1][1][0]=-2*hp
    second[1][0][0][1]=second[1][0][1][0]=-2*hp
    second[0][1][1][1]=second[1][0][1][1]=-2*Ap
    for i in (2,3):
        first[0][i][i]=-2*a*a*B
        first[1][i][i]=2*a*ap
        second[1][1][i][i]=2*(ap*ap+a*app)
        second[0][1][i][i]=second[1][0][i][i]=-4*a*ap*B-2*a*a*Bp
    H,DH,reduced,ric=gauge(gi,first,second)
    check('initial_full_H_'+str(case),H)
    check('initial_tangential_DH_'+str(case),DH[1:])
    qq=[-E,E,F(0),F(0)]
    target=[[lam*g[i][j]+beta*rho*qq[i]*qq[j] for j in range(4)] for i in range(4)]
    # With g^00=-1, reduced Ricci acceleration coefficient is +1/2.
    for i in range(4):
        for j in range(4):
            second[0][0][i][j]=2*(target[i][j]-reduced[i][j])
    H,DH,reduced,ric=gauge(gi,first,second)
    check('reduced_equations_all_components_'+str(case),
          [[reduced[i][j]-target[i][j] for j in range(4)] for i in range(4)])
    check('normal_gauge_derivative_'+str(case),DH[0])
    check('ORIGINAL_equations_all_components_'+str(case),
          [[ric[i][j]-target[i][j] for j in range(4)] for i in range(4)])
    check('initial_independent_density_product_'+str(case),rho*a*a*E-(rho*a*a)*E)
    values['metric_jet_'+str(case)]={'beta':str(beta),'Lambda':str(lam),
        'E':str(E),'rho':str(rho),'A':str(A),'B':str(B),
        'original_Ric00':str(ric[0][0]),'original_Ric01':str(ric[0][1])}
    if case==0:
        badfirst=[[[v for v in row] for row in slab] for slab in first]
        badfirst[0][0][0]*=-1
        badH,_,_,_=gauge(gi,badfirst,second)
        red('wrong_lapse_rate_does_not_set_H_zero',badH)
        wrong=[[target[i][j]+(DH[i][j]+DH[j][i]) for j in range(4)] for i in range(4)]
        red('erasing_nonzero_source_term',target[0][1])

# Gauge Cauchy data: H initially0, tangential derivatives0; map normal derivative.
ac=S.Matrix(S.symbols('a0:4',real=True))
dh=S.zeros(4); dh[0,:]=ac.T
eta=S.diag(-1,1,1,1)
err=(dh+dh.T)/2-eta*S.trace(eta*dh)/2
check('subsidiary_normal_projection',err[0,0]-ac[0]/2)
check('subsidiary_mixed_projection',[err[0,i]-ac[i]/2 for i in range(1,4)])
red('initial_H_alone_not_zero_normal_data',err[0,1].subs(ac[1],2))

# Actual constrained transverse principal block; not an evolution/no-go theorem.
eps,py,E0,m0=S.symbols('eps py E0 m0',positive=True)
vv=S.Matrix([E0,eps*py,0])/S.sqrt(E0**2+eps**2*py**2)
dVy=S.diff(vv[1],eps).subs(eps,0)
check('transverse_velocity_linearization',dVy-py/E0)
J=S.Matrix([[0,0],[m0/E0,0]])
check('principal_block_square',J*J)
assert J.rank()==1 and len(J.nullspace())==1
checks.append('nonzero_Jordan_block_not_diagonalizable')
red('treat_repeated_real_eigenvalues_as_full_eigenbasis',J.subs({m0:3,E0:2}))
tt,yy,k=S.symbols('tt yy k',real=True)
dm=tt*m0*k*S.sin(k*yy)/E0
dp=S.cos(k*yy)
check('Jordan_mode_transport_residual',S.diff(dm,tt)+(m0/E0)*S.diff(dp,yy))
red('omit_full_initial_phase_factor',F(3,2)*F(4,3)-F(3,2))
print(json.dumps({'python':platform.python_version(),'sympy':S.__version__,
 'arithmetic':'exact symbolic/rational; no production PDE or time truncation',
 'shared_geometry_utility':str(old),'shared_geometry_sha256':pin,
 'checks':checks,'passed':len(checks),'red_controls':reds,'values':values,
 'ceiling':'diagnostics only; general analytic normal-form/gauge/product proof requires review'},indent=2))
