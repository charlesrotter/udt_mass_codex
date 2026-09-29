from fractions import Fraction as F
import json
import platform
import sympy as s

records = {}
def check(name, value):
    if not value:
        raise AssertionError(name)
    records[name] = True

def eye(n): return [[F(i == j) for j in range(n)] for i in range(n)]
def mm(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def tr(a): return [list(x) for x in zip(*a)]
def mv(a,b): return [sum(x*y for x,y in zip(row,b)) for row in a]
def diag(v): return [[v[i] if i==j else F(0) for j in range(len(v))] for i in range(len(v))]
eta=diag([F(-1),F(1),F(1),F(1)])
def inv_l(a): return mm(mm(eta,tr(a)),eta)
def boost(q):
    r=sum(x*x for x in q); d=1-r
    if not d > 0: raise ValueError('regular rational boost required')
    g=(1+r)/d; v=[2*x/d for x in q]
    return [[g,*v], *[[v[i], *[F(i==j)+2*q[i]*q[j]/d for j in range(3)]] for i in range(3)]]
def freq(a,n):
    v=mv(a,[F(1),*n]); f=v[0]
    if not f > 0: raise ValueError('future null required')
    return f,[x/f for x in v[1:]]

# Separate pairings are checked without identifying their physical vector spaces.
a=F(3,2); D=diag([1/a,a]); K=[[F(0),F(1)],[F(1),F(0)]]; eta2=diag([F(-1),F(1)])
N=[[F(1),F(-1)],[F(-1),F(-1)]]; Ni=[[x/2 for x in row] for row in N]
B=mm(mm(Ni,D),N)
check('reciprocal_pairing',mm(mm(tr(D),K),D)==K)
check('not_same_eta_isometry',mm(mm(tr(D),eta2),D)!=eta2)
check('abstract_null_basis_conjugacy',mm(mm(tr(B),eta2),B)==eta2)
check('boost_signed_parameter',B==[[(a+1/a)/2,(a-1/a)/2],[(a-1/a)/2,(a+1/a)/2]])
R=[[F(1),F(0),F(0),F(0)],[F(0),F(0),F(-1),F(0)],[F(0),F(1),F(0),F(0)],[F(0),F(0),F(0),F(1)]]
L1=mm(boost([F(1,3),F(0),F(0)]),R)
L2=boost([F(0),F(1,4),F(1,5)])
C=mm(boost([F(0),F(0),F(1,6)]),R)
n=[F(2,3),F(1,3),F(2,3)]
for name,M in [('L1',L1),('L2',L2),('C',C)]:
    check(name+'_lorentz',mm(mm(tr(M),eta),M)==eta)
f1,n1=freq(L1,n); f2,n2=freq(L2,n1); ft,nt=freq(mm(L2,L1),n)
check('direction_carried_cocycle',ft==f1*f2 and nt==n2)
naive=freq(L2,n)[0]*f1
check('direction_drop_separated',naive!=ft)
fr,nr=freq(inv_l(L1),n1)
check('same_arrow_inverse',fr*f1==1 and nr==n)
L1c=mm(inv_l(C),L1); L2c=mm(L2,C)
fc1,nc1=freq(L1c,n); fc2,nc2=freq(L2c,nc1)
check('intermediate_frame_cancels',fc1*fc2==ft and nc2==nt)
col=[row[0] for row in mm(L2,L1)]
Z=col[0]-sum(x*y for x,y in zip(col[1:],nt))
check('clock_column_directional_identity',Z==1/ft)
check('rotation_zero_frequency_nontrivial',freq(R,n)[0]==1 and R!=eye(4))
for p,q in [(F(2),F(3)),(F(2),F(1,2)),(F(3),F(1,2))]:
    beta=(p*q-1)/(p*q+1)
    check('radar_'+str(p)+'_'+str(q),beta==((q-1/p)/(q+1/p)))
check('future_return_not_inverse_control',F(2)*F(3)!=1)
check('positive_radar_not_both_redshift',F(3)*F(1,2)>1 and not F(1,2)>1)

# Independent coordinate Christoffels, then frame transform, rather than
# entering a Cartan connection and checking its own asserted formula.
t,x=s.symbols('t x',real=True); phi=s.Function('phi')(t,x)
coords=[t,x]; g=s.diag(-s.exp(-2*phi),s.exp(2*phi)); gi=g.inv()
Gamma=[[[s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in range(2))) for c in range(2)] for b in range(2)] for a in range(2)]
E=s.diag(s.exp(phi),s.exp(-phi)); Ei=E.inv()
J=s.Matrix([[0,1],[1,0]])
coeff=[-s.exp(-2*phi)*s.diff(phi,x),s.exp(2*phi)*s.diff(phi,t)]
for b in range(2):
    Gb=s.Matrix([[Gamma[a][b][c] for c in range(2)] for a in range(2)])
    W=s.simplify(Ei*(E.diff(coords[b])+Gb*E))
    check('christoffel_frame_connection_'+str(b),s.simplify(W-coeff[b]*J)==s.zeros(2))
for sign in [-1,1]:
    v=sign*s.exp(-2*phi)
    # omega=e^-phi*k^t, geodesic k derivative, divided by dt/dlambda.
    dlogw=-s.diff(phi,t)-v*s.diff(phi,x)-Gamma[0][0][0]-2*Gamma[0][0][1]*v-Gamma[0][1][1]*v*v
    expected=-s.diff(phi,t)+v*s.diff(phi,x)
    check('null_log_frequency_'+str(sign),s.simplify(dlogw-expected)==0)
    transport_depth=-sign*(coeff[0]+coeff[1]*v)
    check('null_transport_depth_'+str(sign),s.simplify(transport_depth-expected)==0)
    check('stationary_depth_sign_'+str(sign),s.simplify(expected.subs(s.diff(phi,t),0)-v*s.diff(phi,x))==0)
    check('time_only_depth_sign_'+str(sign),s.simplify(expected.subs(s.diff(phi,x),0)+s.diff(phi,t))==0)
# alpha = -phi_t dt + phi_x dx has d alpha = 2 phi_tx dt wedge dx.
check('restricted_one_form_curvature',s.simplify(s.diff(s.diff(phi,x),t)-s.diff(-s.diff(phi,t),x)-2*s.diff(phi,t,x))==0)
print(json.dumps({'status':'PASS','checks':records,'count':len(records),'fraction_example':{'f1':str(f1),'f2_carried':str(f2),'f_total':str(ft),'wrong_direction_total':str(naive),'Z':str(Z)},'python':platform.python_version(),'sympy':s.__version__},indent=2))
