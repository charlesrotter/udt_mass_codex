"""Post-exposure distinct-frame spacetime reconstruction.

Fixed Xi and time-varying diagonal metric, [dt,Xi]=0. Author instead uses
a moving orthonormal frame with time-dependent brackets. No author import.
Shared general Koszul/curvature method and SymPy are explicitly acknowledged.
"""
import json
import platform
import sympy as s

checks=[]
def zero(name,value):
    values=list(value) if isinstance(value,s.MatrixBase) else [value]
    residual=[s.factor(v) for v in values]
    assert all(v==0 for v in residual),(name,residual)
    checks.append(name)

x=s.symbols('x1:4',positive=True)
k=s.symbols('k1:4',real=True)
acc=s.symbols('a1:4',real=True)  # Initially independent derivatives of mixed K.
lam=s.Symbol('Lambda',real=True)
tau=sum(k)
metric=s.diag(-1,*x)
inv=metric.inv()
def dt(expr):
    return sum(-2*x[i]*k[i]*s.diff(expr,x[i])+acc[i]*s.diff(expr,k[i]) for i in range(3))
def direction(a,expr):return dt(expr) if a==0 else s.S.Zero
br=[[[s.S.Zero]*4 for j in range(4)] for i in range(4)]
for i in range(1,4):
    for j in range(1,4):
        for m in range(1,4):br[i][j][m]=2*s.LeviCivita(i-1,j-1,m-1)
connections=[]
for a in range(4):
    matrix=s.zeros(4)
    for c in range(4):
        for b in range(4):
            matrix[c,b]=s.factor((
                direction(a,metric[b,c])+direction(b,metric[c,a])-direction(c,metric[a,b])
                -metric[a,a]*br[b][c][a]+metric[b,b]*br[c][a][b]+metric[c,c]*br[a][b][c]
                )/(2*metric[c,c]))
    connections.append(matrix)
for a in range(4):
    zero('full_metric_compatibility_'+str(a),
         metric.applyfunc(lambda e:direction(a,e))-connections[a].T*metric-metric*connections[a])
    for b in range(4):
        zero('full_torsion_'+str((a,b)),connections[a][:,b]-connections[b][:,a]-s.Matrix(br[a][b]))
curvature=[]
for a in range(4):
    row=[]
    for b in range(4):
        row.append(connections[b].applyfunc(lambda e:direction(a,e))
                   -connections[a].applyfunc(lambda e:direction(b,e))
                   +connections[a]*connections[b]-connections[b]*connections[a]
                   -sum((br[a][b][c]*connections[c] for c in range(4)),s.zeros(4)))
    curvature.append(row)
Ric4=s.Matrix(4,4,lambda b,c:s.factor(sum(curvature[a][b][a,c] for a in range(4))))
rho=[2*(x[i]**2-(x[(i+1)%3]-x[(i+2)%3])**2)/(x[0]*x[1]*x[2]) for i in range(3)]
expected=s.diag(sum(acc[i]-k[i]**2 for i in range(3)),
                *(x[i]*(rho[i]-acc[i]+tau*k[i]) for i in range(3)))
zero('all_16_Ricci_components_before_using_evolution',Ric4-expected)
evolution={acc[i]:rho[i]+tau*k[i]-lam for i in range(3)}
R=sum(rho)
H=R+tau**2-sum(v*v for v in k)-2*lam
solved=Ric4.subs(evolution).applyfunc(s.factor)
zero('original_Einstein_equation_residual_exact',solved-lam*metric-s.diag(H,0,0,0))
zero('Hamiltonian_propagation',dt(H).subs(evolution)-2*tau*H)
zero('scalar_normal_variation',dt(R)-2*sum(k[i]*rho[i] for i in range(3)))
for i in range(3):
    # Negative-K conversion from G315's COVARIANT K evolution.
    zero('original_ADM_to_mixed_rates_'+str(i),
         dt(x[i]*k[i]).subs(evolution)
         -(x[i]*rho[i]+tau*x[i]*k[i]-2*x[i]*k[i]**2-lam*x[i]))
zero('orthonormal_bracket_motion',s.Matrix([
    s.factor(dt(2*s.sqrt(x[i]/(x[(i+1)%3]*x[(i+2)%3])))
             -2*s.sqrt(x[i]/(x[(i+1)%3]*x[(i+2)%3]))*(tau-2*k[i]))
    for i in range(3)]))

# Deliberate semantic defects evaluated against the original unspecialized Ricci.
defects={
    'wrong_Lambda_sign':{acc[i]:rho[i]+tau*k[i]+lam for i in range(3)},
    'drop_tau_ki':{acc[i]:rho[i]-lam for i in range(3)},
    'spuriously_keep_minus_2ki_squared_in_mixed_rates':{
        acc[i]:rho[i]+tau*k[i]-2*k[i]**2-lam for i in range(3)}}
residuals={}
for name,mut in defects.items():
    residual=(Ric4.subs(mut)-lam*metric-s.diag(H,0,0,0)).applyfunc(s.factor)
    assert residual!=s.zeros(4),(name,'false pass')
    residuals[name]=str(residual)

print(json.dumps(dict(status='PASS',python=platform.python_version(),sympy=s.__version__,
    check_count=len(checks),checks=checks,fixed_frame_Ricci4=str(Ric4),
    after_original_evolution=str(solved),Hamiltonian=str(s.factor(H)),
    full_metric=str(metric),defect_residuals=residuals,
    independence='post-exposure; fixed invariant frame and independent k derivatives; shared Koszul method/SymPy',
    omissions='no integration, general Cauchy theorem proof, global/uniform existence or physical stability'),indent=2))
