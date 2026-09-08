"""CD1 exact symbolic author checks; general existence is not a test count."""
import hashlib
import json
import platform
import sympy as S

x, y, z = coords = S.symbols('x y z', real=True)
a, A, B, rho, Phi = [S.Function(k)(x) for k in ('a','A','B','rho','Phi')]
lam, beta, s0 = S.symbols('Lambda beta s0', real=True, nonzero=True)
metric = S.diag(1,a*a,a*a)
inv = metric.inv()
Gamma = [[[sum(inv[i,k]*(S.diff(metric[k,j],coords[l])+
             S.diff(metric[k,l],coords[j])-S.diff(metric[j,l],coords[k]))
             for k in range(3))/2 for l in range(3)] for j in range(3)]
             for i in range(3)]
Ric = S.Matrix(3,3,lambda i,j:sum(S.diff(Gamma[k][i][j],coords[k])-
       S.diff(Gamma[k][i][k],coords[j])+sum(Gamma[k][k][l]*Gamma[l][i][j]-
       Gamma[k][j][l]*Gamma[l][i][k] for l in range(3)) for k in range(3)))
scalar = S.simplify(S.trace(inv*Ric))
K = S.diag(A,a*a*B,a*a*B)
mixed = inv*K
trace = S.trace(mixed)
P = mixed-trace*S.eye(3)
momentum = [S.simplify(sum(S.diff(P[j,i],coords[j])+sum(
    Gamma[j][j][k]*P[k,i]-Gamma[k][j][i]*P[j,k] for k in range(3))
    for j in range(3))) for i in range(3)]
H = S.simplify(scalar+trace**2-S.trace(mixed*mixed))
checks, rejected = [], []
def zero(name, expr):
    result=S.simplify(expr)
    assert result==0, (name,str(result))
    checks.append(name)
def red(name, expr, point):
    result=S.simplify(expr.subs(point).doit())
    assert result!=0 and not result.free_symbols, (name,str(result))
    rejected.append({'name':name,'nonzero_exact_residual':str(result)})

h=S.diff(a,x)/a
R_expected=-4*S.diff(a,x,2)/a-2*h*h
T=beta*rho*S.diff(Phi,x)**2
Af=(2*lam+2*T-R_expected-2*B*B)/(4*B)
Bf=h*(Af-B)-T/2
zero('full_intrinsic_R3',scalar-R_expected)
zero('full_H',H-(R_expected+4*A*B+2*B*B))
zero('full_Mx',momentum[0]-(-2*S.diff(B,x)+2*h*(A-B)))
zero('full_My',momentum[1])
zero('full_Mz',momentum[2])
zero('joint_H',H.subs(A,Af)-2*lam-2*T)
zero('joint_Mx',(momentum[0]-T).subs({S.diff(B,x):Bf,A:Af},simultaneous=True))
zero('symmetric_covariant_K',(K-K.T).norm())
E=S.symbols('E',positive=True)
g4=S.diag(-1,1,a*a,a*a)
q=S.Matrix([-E,E,0,0]); ell=g4.inv()*q
zero('initial_eikonal',(q.T*ell)[0])
zero('future_normal_raised',ell[0]-E)
zero('initial_screen_area',S.det(metric[1:3,1:3])-a**4)
zero('initial_product',(rho*a*a-s0).subs(a*a,s0/rho))
zero('full_initial_flux',(rho*E*a*a-s0*E).subs(a*a,s0/rho))
point={a:S.Rational(3,2),S.diff(a,x):S.Rational(2,3),
       S.diff(a,x,2):S.Rational(-1,5),B:S.Rational(7,4),
       rho:S.Rational(5,3),S.diff(Phi,x):S.Rational(4,3),
       beta:S.Rational(-2,5),lam:S.Rational(3,7)}
for sign in (-1,1):
    pp={**point,beta:sign*S.Rational(2,5)}
    zero('rational_H_beta_'+str(sign),(H.subs(A,Af)-2*lam-2*T).subs(pp))
    zero('rational_M_beta_'+str(sign),
         (momentum[0]-T).subs({S.diff(B,x):Bf,A:Af},simultaneous=True).subs(pp))
red('wrong_momentum_source_sign',
    (momentum[0]-T).subs({S.diff(B,x):h*(Af-B)+T/2,A:Af},simultaneous=True),point)
red('omit_warp_connection',
    (momentum[0]-T).subs({S.diff(B,x):-T/2,A:Af},simultaneous=True),point)
red('wrong_intrinsic_scalar_sign',
    H.subs(A,(2*lam+2*T+R_expected-2*B*B)/(4*B))-2*lam-2*T,point)
red('omit_phase_intensity_from_three_form',s0*E-s0,{s0:S.Rational(3,2),E:S.Rational(4,3)})
red('arbitrary_density_with_fixed_area_fails_product',rho*a*a-s0,
    {rho:S.Rational(5,3),a:S.Rational(3,2),s0:S.Rational(1,1)})
print(json.dumps({'python':platform.python_version(),'sympy':S.__version__,
 'shape':'3x3 intrinsic metric, covariant K and all three momentum components',
 'arithmetic':'exact symbolic/rational; no discretization or fitted data',
 'checks':checks,'passed':len(checks),'red_controls':rejected,
 'ceiling':'regression/algebra diagnostics, not local ODE or PDE theorem'},indent=2))
