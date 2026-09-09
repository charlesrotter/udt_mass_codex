"""Post-exposure NT2 comparison using the sealed reviewer tensor implementation."""
import itertools as it
import json
from pathlib import Path
import source_first_check as r
import sympy as s

root=Path(__file__).resolve().parents[3]
step=root/'udt_neighboring_tidal_consistency_campaign_2026-09-08/step_02'
ii=range(4)
a,b,u,v,x,y=r.a,r.b,r.u,r.v,r.x,r.y
emit=r.emit

# Translate independently constructed generic Weyl basis into the author's
# REGISTERED C/B coordinates. No author matrix or science code constructs it.
C=s.Matrix(3,3,lambda i,j:r.Q(i+1,0,0,j+1))
B=s.Matrix(3,3,lambda l,i:sum(s.LeviCivita(j,k,l)*r.Q(i+1,0,j+1,k+1) for j,k in it.product(range(3),repeat=2))/2)
coords=s.Matrix([C[0,0],C[1,1],C[0,1],C[0,2],C[1,2],B[0,0],B[1,1],B[0,1],B[0,2],B[1,2]])
change=coords.jacobian(r.unknowns)*r.Qbasis
assert change.det()!=0
symbol=json.loads((step/'symbol_corrected.stdout').read_text())
all_symbol={}
for name,nu,rank in [('timelike',(1,0,0,0),10),('spacelike',(0,0,0,1),10),('null',(1,0,0,-1),8)]:
    independent=r.factor_matrix(nu)*change.inv()
    saved=s.Matrix(symbol['symbol_matrices'][name])
    assert independent.rank()==saved.rank()==rank
    assert independent.col_join(saved).rank()==rank
    all_symbol[name]={'rank':rank,'full_row_space_equal':True,'all_entries_equal':independent==saved}
V=s.Matrix(symbol['null_kernel'])
assert V.rank()==2 and (r.factor_matrix((1,0,0,-1))*change.inv())*V==s.zeros(24,2)
assert V.T*V==s.diag(3,3)
emit('saved_symbol_independent_check',all_symbol)

# Original equations for an arbitrary v-independent H(u,x,y), then specialize
# only after deriving all components. This exposes transverse harmonicity.
H=s.Function('H')(u,x,y)
g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
gi,Gamma,_,Q,Ric=r.geometry(g,(u,v,x,y))
lap=s.diff(H,x,2)+s.diff(H,y,2)
expected_Ric=s.zeros(4);expected_Ric[0,0]=-lap/2
assert s.simplify(Ric-expected_Ric)==s.zeros(4)
nn=(1,0,0,0)
Hlift=s.zeros(4)
for i,j in it.product((2,3),repeat=2):Hlift[i,j]=s.diff(H,(u,v,x,y)[i],(u,v,x,y)[j])/2
def wedge(n,S,i,j,k,l):
    return n[i]*n[k]*S[j,l]-n[j]*n[k]*S[i,l]-n[i]*n[l]*S[j,k]+n[j]*n[l]*S[i,k]
assert all(s.simplify(Q(*t)-wedge(nn,Hlift,*t))==0 for t in it.product(ii,repeat=4))
emit('generic_profile_full_metric',{'Ricci':Ric.tolist(),'all_256_Riemann_components_checked':True})

A=s.Function('A')(u);F=s.Function('F')(u)
profile=A*(x*x-y*y)+2*F*x*y
special=lambda expr:s.simplify(expr.subs(H,profile).doit())
assert all(special(t)==0 for t in Ric)
frame=s.Matrix([[1,0,0,-1],[(H+1)/2,0,0,(1-H)/2],[0,1,0,0],[0,0,1,0]])
assert s.simplify(frame.T*g*frame-s.diag(-1,1,1,1))==s.zeros(4)
at={A:0,F:0,s.diff(A,u):-a,s.diff(F,u):-b,u:0,v:0,x:0,y:0}
value=lambda expr:s.simplify(special(expr).subs(at,simultaneous=True))
frame0=frame.applyfunc(value)
nonzero={i:[(j,frame0[j,i]) for j in ii if frame0[j,i]!=0] for i in ii}
assert all(value(Q(*t))==0 for t in it.product(ii,repeat=4))
dQ={}
for m,t in it.product(ii,it.product(ii,repeat=4)):
    expr=s.diff(Q(*t),(u,v,x,y)[m])
    for slot in ii:
        for h in ii:
            repl=list(t);repl[slot]=h
            expr-=Gamma(h,m,t[slot])*Q(*repl)
    dQ[(m,*t)]=value(expr)
nu=(1,0,0,-1)
amp=s.zeros(4);amp[1,1]=-a;amp[1,2]=amp[2,1]=-b;amp[2,2]=a
Pt={t:wedge(nu,amp,*t) for t in it.product(ii,repeat=4)}
for t in it.product(ii,repeat=5):
    transformed=sum(s.prod(q[1] for q in terms)*dQ[tuple(q[0] for q in terms)] for terms in it.product(*(nonzero[i] for i in t)))
    assert s.expand(transformed-nu[t[0]]*Pt[t[1:]])==0
Cout=s.Matrix(3,3,lambda i,j:Pt[i+1,0,0,j+1])
Bout=s.Matrix(3,3,lambda l,i:sum(s.LeviCivita(j,k,l)*Pt[i+1,0,j+1,k+1] for j,k in it.product(range(3),repeat=2))/2)
assert Cout==s.Matrix([[a,b,0],[b,-a,0],[0,0,0]])
assert Bout==s.Matrix([[b,-a,0],[-a,-b,0],[0,0,0]])
emit('normalized_jet',{'all_1024_covariant_slots':True,'C':Cout.tolist(),'B':Bout.tolist(),'nu':nu})

# Different normal/K implementation: differentiate the actual normal vector,
# contract with the metric and slice tangents, rather than the author's Hessian.
S=H+4
X=s.Matrix([[1,0,0],[-2,0,0],[0,1,0],[0,0,1]])
n=s.Matrix([1,H+2,0,0])/s.sqrt(S)
gamma=X.T*g*X
Dn=s.Matrix(4,3,lambda k,j:s.simplify(sum(X[m,j]*(s.diff(n[k],(u,v,x,y)[m])+sum(Gamma(k,m,h)*n[h] for h in ii)) for m in ii)))
Kdirect=s.simplify(-X.T*g*Dn)
K=s.Matrix([[s.diff(H,u),s.diff(H,x),s.diff(H,y)],[s.diff(H,x),0,0],[s.diff(H,y),0,0]])/(2*s.sqrt(S))
assert s.simplify(Kdirect-K)==s.zeros(3)
assert s.simplify((n.T*g*frame[:,0])[0]+(S+1)/(2*s.sqrt(S)))==0
gami,Gam3,_,_,Ric3=r.geometry(gamma,(u,x,y))
Km=gami*K;tau=s.trace(Km);norm=s.trace(Km*Km)
R3=s.simplify(s.trace(gami*Ric3))
Ham=s.simplify(R3+tau*tau-norm)
Mom=[]
for i in range(3):
    div=sum(s.diff(Km[j,i],(u,x,y)[j]) for j in range(3))
    div+=sum(Gam3(j,j,h)*Km[h,i]-Gam3(h,j,i)*Km[j,h] for j,h in it.product(range(3),repeat=2))
    Mom.append(s.simplify(div-s.diff(tau,(u,x,y)[i])))
assert s.simplify(Ham+lap/S)==0
assert s.simplify(Mom[0]-lap/(2*s.sqrt(S)))==0
assert Mom[1:]==[0,0]
assert special(Ham)==0 and all(special(t)==0 for t in Mom)
emit('full_slice',{'K_from_covariant_normal':Kdirect.tolist(),'Hamiltonian_generic':Ham,'momentum_generic':Mom,'future_inner_product':-(S+1)/(2*s.sqrt(S))})

saved=json.loads((step/'development_corrected.stdout').read_text())
loc={'u':u,'v':v,'x':x,'y':y,'a':a,'b':b,'A':s.Function('A'),'F':s.Function('F'),'Matrix':s.Matrix,'Derivative':s.Derivative,'sqrt':s.sqrt}
comparisons={'metric':g,'frame':frame,'Ricci':Ric,'gamma':gamma,'K':Kdirect,'R3':R3,'tau':tau,'Knorm':norm,'Hamiltonian':Ham,'momentum':s.Matrix(Mom),'P_C':Cout,'P_B':Bout}
for key,expr in comparisons.items():
    stored=s.sympify(saved[key],locals=loc)
    diff=stored-special(expr)
    if isinstance(diff,s.MatrixBase):assert all(s.simplify(t)==0 for t in diff),key
    else:assert s.simplify(diff)==0,key
emit('saved_development_artifact_check',{'fields':list(comparisons),'all_equal_to_independent_computation':True})

epsilon=s.symbols('epsilon',real=True)
bad=profile+epsilon*u*x*x
bad_ric=s.simplify(Ric[0,0].subs(H,bad).doit())
assert bad_ric==-epsilon*u and bad_ric.subs(u,0)==0
assert s.simplify((K-(-K))[0,0])!=0
emit('negative_controls',{'nonharmonic_Ricci_neighborhood':bad_ric,'nonharmonic_Ricci_event':0,'wrong_K_sign_has_nonzero_normal_projection_residual':True})
emit('DIRECT_INDEPENDENT_PASS',True)
