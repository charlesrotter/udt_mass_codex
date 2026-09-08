import itertools, json, platform
import sympy as s

checks=[]
def eq(name, actual, expected=0):
    values=list(actual-expected) if isinstance(actual,s.MatrixBase) else [actual-expected]
    assert all(s.simplify(v)==0 for v in values), (name, actual, expected)
    checks.append(name)

p,q=s.symbols('p q', positive=True)
h,epsilon=s.symbols('h epsilon', nonzero=True, real=True)
x,y,z,u,v,w,E=s.symbols('x y z u v w E', real=True)
ix=range(3)
br={}
for a,b,c,t in [(0,1,2,q),(1,2,0,p),(2,0,1,p)]:
    br[a,b,c]=t; br[b,a,c]=-t
C=lambda a,b,c:br.get((a,b,c),s.S.Zero)
G={(a,b,c):s.expand((C(a,b,c)-C(b,c,a)+C(c,a,b))/2)
   for a,b,c in itertools.product(ix,repeat=3)}
K=s.Matrix([[x,u,v],[u,y,w],[v,w,z]])
d={(a,i,j):s.Symbol(f'd{a}{min(i,j)}{max(i,j)}') for a,i,j in itertools.product(ix,repeat=3)}
def derivative(K,d):
    return {(a,i,j):s.expand(d[a,i,j]-sum(G[a,i,r]*K[r,j]+G[a,j,r]*K[i,r] for r in ix))
            for a,i,j in itertools.product(ix,repeat=3)}
DK=derivative(K,d)
mom=s.Matrix([s.expand(sum(DK[j,j,i]-d[i,j,j] for j in ix)) for i in ix])
expected=s.Matrix([-d[0,1,1]-d[0,2,2]+d[1,0,1]+d[2,0,2]+(q-p)*w,
                   d[0,0,1]-d[1,0,0]-d[1,2,2]+d[2,1,2]+(p-q)*v,
                   d[0,0,2]+d[1,1,2]-d[2,0,0]-d[2,1,1]])
eq('all_three_full_momenta_from_Koszul',mom,expected)
Ham=s.trace(K)**2-s.trace(K*K)-2*E
F=(E-x*y+u*u+v*v+w*w)/(x+y)
eq('exact_nonlinear_Hamiltonian_elimination',s.factor(Ham.subs(z,F)))
base={x:h,y:h,u:0,v:0,w:0,E:3*h*h}
eq('baseline_F',F.subs(base),h)
eq('baseline_Fx',s.diff(F,x).subs(base),-1)
n1,n2,n3=s.symbols('n1 n2 n3')
U=(x,v,w)
normal=s.Matrix([[-n1*s.diff(F,x),n3-n1*s.diff(F,v),-n1*s.diff(F,w)],
                 [-n2*(1+s.diff(F,x)),-n2*s.diff(F,v),n3-n2*s.diff(F,w)],
                 [-n3,n1,n2]])
normal0=normal.subs(base).subs({n1:0,n2:0,n3:1})
eq('noncharacteristic_normal_matrix',normal0,s.Matrix([[0,1,0],[0,0,1],[-1,0,0]]))
eq('normal_determinant',normal0.det(),-1)
eq('a_characteristic_surface_is_not_admissible',normal.subs(base).det().subs({n1:0,n2:1,n3:0}),0)

# Solve the differentiated constraint equations, rather than insert the answer.
# y,u have all derivatives zero; x,v,w tangential data are specified.
J={}
for component in ['x','v','w']:
    for a,b in itertools.combinations_with_replacement(ix,2):
        J[component,a,b]=(epsilon if (component,a,b)==('v',1,1) else s.S.Zero) if b<2 else s.Symbol(f'{component}_{a}{b}')
def jet(component,a,b): return J[component,min(a,b),max(a,b)]
equations=[]
for b in ix:
    equations.extend([jet('v',2,b)+jet('x',0,b),jet('w',2,b),
                      jet('x',2,b)-jet('v',0,b)-jet('w',1,b)])
unknowns=sorted(set().union(*(e.free_symbols for e in equations))-{epsilon},key=str)
solutions=s.solve(equations,unknowns,dict=True)
assert len(solutions)==1
for variable in unknowns: eq('CK_jet_'+str(variable),solutions[0][variable])

K0=h*s.eye(3)
zero1={a:s.S.Zero for a in itertools.product(ix,repeat=3)}
H={a:s.S.Zero for a in itertools.product(ix,repeat=4)}
H[1,1,0,2]=H[1,1,2,0]=epsilon
def ricci_variation(K,d,H,drop_derivative_connection=False):
    D1=derivative(K,d)
    D2={}
    for a,b,i,j in itertools.product(ix,repeat=4):
        partial=H[a,b,i,j]-sum(G[b,i,r]*d[a,r,j]+G[b,j,r]*d[a,i,r] for r in ix)
        D2[a,b,i,j]=s.expand(partial-sum(
            (0 if drop_derivative_connection else G[a,b,r]*D1[r,i,j])+
            G[a,i,r]*D1[b,r,j]+G[a,j,r]*D1[b,i,r] for r in ix))
    traceH={(i,j):sum(H[i,j,k,k]-sum(G[i,j,r]*d[r,k,k] for r in ix) for k in ix)
            for i,j in itertools.product(ix,repeat=2)}
    S=s.Matrix(3,3,lambda i,j:s.expand(sum(-D2[k,i,k,j]-D2[k,j,k,i]+D2[k,k,i,j] for k in ix)+traceH[i,j]))
    return S
S=ricci_variation(K0,zero1,H)
expectedS=s.Matrix([[0,0,epsilon],[0,0,0],[epsilon,0,0]])
eq('full_covariant_Ricci_tensor_of_matching_jet',S,expectedS)
eq('pure_trace_homothety_covariant_Ricci_rate',ricci_variation(K0,zero1,{a:0 for a in H}),s.zeros(3))

# Separate direct connection-variation contraction in normal coordinates.
# This specialization is exact because L=DL=0 at the point.
dGamma={(a,k,i,j): -H[a,i,j,k]-H[a,j,i,k]+H[a,k,i,j]
        for a,k,i,j in itertools.product(ix,repeat=4)}
direct=s.Matrix(3,3,lambda i,j:sum(dGamma[k,k,i,j]-dGamma[j,k,i,k] for k in ix))
eq('direct_connection_variation_full_tensor',direct,S)
B=s.diag(p*q-q*q/2,p*q-q*q/2,q*q/2)
Bdot=S+2*K0*B
gap=q*(q-p)
Pdot=s.zeros(3)
for i in [0,1]:
    Pdot[i,2]=s.factor(Bdot[i,2]/gap)
    Pdot[2,i]=s.factor(Bdot[2,i]/gap)
eq('full_inverse_metric_term_retained',Bdot-S,2*h*B)
eq('image_drift_nonzero_coefficient',Pdot[0,2],epsilon/gap)
eq('full_projector_mixed_blocks',Pdot,expectedS/gap)
P=s.diag(0,0,1)
eq('projector_idempotence_derivative',Pdot*P+P*Pdot-Pdot,s.zeros(3))
eq('spectral_commutation_derivative',Bdot*P+B*Pdot-Pdot*B-P*Bdot,s.zeros(3))

# Full connection-slot control from reviewed BI1, outside the special lower-jet match.
Sgeneric=ricci_variation(K,zero1,{a:0 for a in H})
eq('homogeneous_full_covariant_mixed13',Sgeneric[0,2],-(2*p*q+q*q)*v)
eq('homogeneous_full_covariant_mixed23',Sgeneric[1,2],-(2*p*q+q*q)*w)
badS=ricci_variation(K,zero1,{a:0 for a in H},True)
assert any(s.simplify(t)!=0 for t in badS-Sgeneric)

t=s.symbols('t',real=True)
naive=Ham.subs({x:h,y:h,z:h,u:0,v:epsilon*t*t/2,w:0,E:3*h*h})
eq('bare_polynomial_has_exact_nonlinear_defect',naive,-epsilon**2*t**4/2)
correctedF=F.subs({x:h,y:h,u:0,v:epsilon*t*t/2,w:0,E:3*h*h})
eq('surface_algebraic_correction_is_quartic',correctedF,h+epsilon**2*t**4/(8*h))

mutations={}
def reject(name, thunk):
    try: thunk()
    except AssertionError: mutations[name]='REJECTED'; return
    raise AssertionError(('mutant survived',name))
reject('reverse_Ricci_variation_sign',lambda:eq('mutant_sign',-S,expectedS))
reject('delete_spatial_second_jet',lambda:eq('mutant_no_hessian',s.zeros(3),expectedS))
reject('claim_bare_jet_exact_Hamiltonian',lambda:eq('mutant_formal_exact',naive))
reject('drop_derivative_index_connection',lambda:eq('mutant_connection',badS,Sgeneric))
reject('drop_inverse_metric_variation',lambda:eq('mutant_raising',S,S+2*K0*B))
print(json.dumps(dict(status='PASS',python=platform.python_version(),sympy=s.__version__,
    checks=checks,number_of_checks=len(checks),normal_matrix=str(normal),
    normal_determinant_at_base=str(normal0.det()),solved_CK_second_jet={str(k):str(val) for k,val in solutions[0].items()},
    full_S=str(S),full_Bdot=str(Bdot),full_Pdot=str(Pdot),
    naive_polynomial_Hamiltonian_residual=str(naive),mutations=mutations,
    conclusion_scope='Exact symbolic algebra; actual analytic realizability rests on the explicit noncharacteristic CK argument, not finite jets.'),indent=2))
