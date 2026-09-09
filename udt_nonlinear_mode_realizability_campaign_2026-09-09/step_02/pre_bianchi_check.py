"""Full spatial coordinate constraints and tangent checks for NR2 (not a PDE proof)."""
import argparse
import json
import sys
import sympy as S

parser=argparse.ArgumentParser()
parser.add_argument('--mutant',choices=['mean_sign','hamiltonian_denominator','cross_velocity'])
args=parser.parse_args()
checks=[]
def simp(v): return S.simplify(S.expand(v))
def gate(expr,name):
    assert simp(expr)==0,name
    checks.append(name)

x=S.symbols('x',real=True)
a,b,T=S.symbols('a b T',positive=True)
u,v,pu,pv,s,kappa=[S.Function(n)(x) for n in ['u','v','pu','pv','s','kappa']]
M=S.Matrix([[S.exp(2*u),S.exp(2*u)*v],[S.exp(2*u)*v,S.exp(-2*u)+S.exp(2*u)*v*v]])
mi=M.inv().applyfunc(simp)
uu,vv=S.symbols('uu vv')
mm=M.subs({u:uu,v:vv})
Eu=(mm.inv()*mm.diff(uu)).subs({uu:u,vv:v}).applyfunc(simp)
Ev=(mm.inv()*mm.diff(vv)).subs({uu:u,vv:v}).applyfunc(simp)
V=(pu*Eu/4+pv*S.exp(-4*u)*Ev).applyfunc(simp)
gate(M.det()-1,'determinant_one_metric_chart')
for E,n in [(Eu,'u'),(Ev,'v')]:
    gate(S.trace(E),'tracefree_coordinate_basis_'+n)
    for i in range(2):
        for j in range(i+1,2): gate((M*E)[i,j]-(M*E)[j,i],'selfadjoint_coordinate_basis_'+n)
gate(S.trace(Eu*Eu)/2-4,'gram_uu')
gate(S.trace(Eu*Ev),'gram_uv')
gate(S.trace(Ev*Ev)/2-S.exp(4*u),'gram_vv')
U=(mi*M.diff(x)).applyfunc(simp)
gate(S.trace(U*V)-2*(pu*S.diff(u,x)+pv*S.diff(v,x)),'exact_coordinate_momentum_pairing')
gate(S.trace(V*V)-(pu*pu/2+2*pv*pv*S.exp(-4*u)),'exact_traceless_norm')

g=S.zeros(3);g[0,0]=a*a;g[1:3,1:3]=b*b*M
gi=g.inv().applyfunc(simp)
K=S.zeros(3);K[0,0]=a*a*kappa;K[1:3,1:3]=b*b*M*(s*S.eye(2)+V)
K=K.applyfunc(simp); L=(gi*K).applyfunc(simp);tau=simp(S.trace(L))
def d(expr,i):return S.diff(expr,x) if i==0 else S.Integer(0)
C=[[[simp(sum(gi[k,l]*(d(g[l,j],i)+d(g[l,i],j)-d(g[i,j],l)) for l in range(3))/2) for j in range(3)] for i in range(3)] for k in range(3)]
Ric=S.zeros(3)
for i in range(3):
    for j in range(3):
        Ric[i,j]=simp(sum(d(C[k][i][j],k)-d(C[k][i][k],j)+sum(C[k][i][j]*C[l][k][l]-C[l][i][k]*C[k][j][l] for l in range(3)) for k in range(3)))
R=simp(S.trace(gi*Ric))
expected_R=-(4*S.diff(u,x)**2+S.exp(4*u)*S.diff(v,x)**2)/(2*a*a)
gate(R-expected_R,'full_coordinate_scalar_curvature')
mom=[]
for i in range(3):
    mom.append(simp(sum(d(L[j,i],j)+sum(C[j][j][m]*L[m,i]-C[m][j][i]*L[j,m] for m in range(3)) for j in range(3))-d(tau,i)))
gate(mom[0]+2*S.diff(s,x)+pu*S.diff(u,x)+pv*S.diff(v,x),'full_axial_momentum_identity')
gate(mom[1],'transverse_momentum_y_structural')
gate(mom[2],'transverse_momentum_z_structural')
Ham=simp(R+tau*tau-S.trace(L*L))
gate(Ham-(R+4*s*kappa+2*s*s-S.trace(V*V)),'full_hamiltonian_identity')
Lam=S.symbols('Lambda',real=True)
den=2 if args.mutant=='hamiltonian_denominator' else 4
kap=(2*Lam-R-2*s*s+S.trace(V*V))/(den*s)
gate(Ham.subs(kappa,kap)-2*Lam,'completed_hamiltonian_constraint')

e=S.symbols('epsilon',real=True)
f,w,p,r,Psi=[S.Function(n)(x) for n in ['f','w','p','r','Psi']]
lambda2,mean2=S.symbols('lambda2 mean2',real=True)
sgn=-1 if args.mutant=='mean_sign' else 1
crossfactor=S.Rational(1,2) if args.mutant=='cross_velocity' else S.Integer(1)
sub={u:e*f,v:2*e*w,pu:-2*e*p,pv:-crossfactor*e*r,s:-2/(3*T)+e*e*(sgn*Psi+mean2)}
se=mom[0].subs(sub).doit().subs(S.diff(Psi,x),p*S.diff(f,x)+r*S.diff(w,x))
gate(se,'completed_pointwise_momentum_constraint')
ge=g.subs(sub);ke=K.subs(kappa,kap).subs(Lam,e*e*lambda2).subs(sub).doit()
dge=ge.diff(e).subs(e,0).applyfunc(simp);dke=ke.diff(e).subs(e,0).applyfunc(simp)
HH=S.Matrix([[f,w],[w,-f]]);PP=S.Matrix([[p,r],[r,-p]])
expected_dg=S.zeros(3);expected_dg[1:3,1:3]=2*b*b*HH
expected_dk=S.zeros(3);expected_dk[1:3,1:3]=-b*b*(PP+4*HH/(3*T))
for i,j in [(0,0),(1,1),(1,2),(2,2)]:
    gate(dge[i,j]-expected_dg[i,j],f'prescribed_metric_tangent_{i}{j}')
    gate(dke[i,j]-expected_dk[i,j],f'prescribed_K_tangent_{i}{j}')
gate(ke[0,0].subs(e,0)-a*a/(3*T),'background_K_axial')
gate(ke[1,1].subs(e,0)+2*b*b/(3*T),'background_K_transverse')

fc,fs,wc,ws,pc,ps,rc,rs=S.symbols('fc fs wc ws pc ps rc rs')
f0=fc*S.cos(x)+fs*S.sin(x);w0=wc*S.cos(x)+ws*S.sin(x)
p0=pc*S.cos(x)+ps*S.sin(x);r0=rc*S.cos(x)+rs*S.sin(x)
primitive_integrand=S.expand_trig(p0*S.diff(f0,x)+r0*S.diff(w0,x))
period=S.integrate(primitive_integrand,(x,0,2*S.pi))
gate(period-S.pi*(pc*fs-ps*fc+rc*ws-rs*wc),'periodic_primitive_iff_NR1_charge')
# Both nonzero polarization charges may cancel; this is not a single-mode-only check.
balance={fc:1,fs:0,pc:0,ps:1,wc:0,ws:1,rc:1,rs:0}
gate(period.subs(balance),'balanced_two_polarization_periodic_primitive')
unbalance={fc:1,fs:0,pc:0,ps:1,wc:0,ws:0,rc:0,rs:0}
gate(period.subs(unbalance)+S.pi,'excluded_single_polarization_nonzero_period')

print(json.dumps({'status':'PASS_EXACT_FULL_SPATIAL_CONSTRAINTS_AND_TANGENT_NOT_PDE_PROOF','checks':checks,'count':len(checks),'M':str(M),'V':str(V),'R3':str(R),'momentum':[str(m) for m in mom],'hamiltonian':str(Ham),'primitive_period':str(period),'python':sys.version,'sympy':S.__version__,'mutant':args.mutant},indent=2))
