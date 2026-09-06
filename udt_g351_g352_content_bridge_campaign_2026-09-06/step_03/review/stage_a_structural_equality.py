"""Metric-derivative reconstruction, authored without Step 3 candidate exposure."""
import itertools, json, platform
import sympy as s
u,v,x,y=s.symbols('u v x y', real=True)
coords=(u,v,x,y); n=range(4)
H=s.Function('H')(u,x,y)
g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
inv=g.inv(); simplify=s.simplify
checks=[]
def require(name, ok):
    assert ok, name
    checks.append(name)
Gamma={}
for a,b,c in itertools.product(n,repeat=3):
    Gamma[a,b,c]=simplify(sum(inv[a,d]*(s.diff(g[d,c],coords[b])+s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in n))
Rup={}
for a,b,c,d in itertools.product(n,repeat=4):
    Rup[a,b,c,d]=simplify(s.diff(Gamma[a,d,b],coords[c])-s.diff(Gamma[a,c,b],coords[d])+sum(Gamma[a,c,e]*Gamma[e,d,b]-Gamma[a,d,e]*Gamma[e,c,b] for e in n))
Ric=s.Matrix(4,4,lambda b,d:simplify(sum(Rup[a,b,a,d] for a in n)))
target=s.zeros(4); target[0,0]=-(s.diff(H,x,2)+s.diff(H,y,2))/2
require('full_Ricci_from_metric',Ric==target)
R={k:simplify(sum(g[k[0],e]*Rup[(e,)+k[1:]] for e in n)) for k in itertools.product(n,repeat=4)}
require('full_Riemann_support',all(z==0 or (k[0:2].count(0)==1 and k[2:4].count(0)==1 and 1 not in k) for k,z in R.items()))
aa,bb=s.symbols('a b',real=True)
harm={s.diff(H,x,2):aa,s.diff(H,x,y):bb,s.diff(H,y,2):-aa}
W={k:simplify(z.xreplace(harm)) for k,z in R.items()}
require('harmonic_Ricci_zero',all(simplify(z.xreplace(harm))==0 for z in Ric))
star={}
for a,b,c,d in itertools.product(n,repeat=4):
    star[a,b,c,d]=simplify(sum(s.LeviCivita(a,b,e,f)*inv[e,i]*inv[f,j]*W[i,j,c,d]/2 for e,f,i,j in itertools.product(n,repeat=4) if inv[e,i]!=0 and inv[f,j]!=0))
nzinv=[(i,j,inv[i,j]) for i,j in itertools.product(n,repeat=2) if inv[i,j]!=0]
B={}
for a,b,c,d in itertools.product(n,repeat=4):
    B[a,b,c,d]=simplify(sum(ij*kl*(W[a,i,c,k]*W[b,j,d,l]+star[a,i,c,k]*star[b,j,d,l]) for i,j,ij in nzinv for k,l,kl in nzinv))
require('full_quadratic_tensor',all(z==(aa**2+bb**2 if k==(0,0,0,0) else 0) for k,z in B.items()))
require('dual_orientation_cancels',all(simplify(sum(ij*kl*(W[a,i,c,k]*W[b,j,d,l]+(-star[a,i,c,k])*(-star[b,j,d,l])) for i,j,ij in nzinv for k,l,kl in nzinv)-B[a,b,c,d])==0 for a,b,c,d in itertools.product(n,repeat=4)))
rho=s.Function('rho')(u,x,y)
beta=s.Matrix([-rho,0,0,0]); C=inv*beta
cov=s.Matrix(4,4,lambda a,b:simplify(s.diff(beta[b],coords[a])-sum(Gamma[c,a,b]*beta[c] for c in n)))
alpha=s.Matrix([s.diff(rho,z)/rho for z in coords])
require('root_recurrence',cov==alpha*beta.T)
db=cov-cov.T
require('ambient_closure_components',db[2,0]==-s.diff(rho,x) and db[3,0]==-s.diff(rho,y) and db[0,1]==0)
q=simplify((alpha.T*inv*alpha)[0])
require('recurrence_norm',q==(s.diff(rho,x)**2+s.diff(rho,y)**2)/rho**2)
div=simplify(sum(s.diff(C[a],coords[a])+sum(Gamma[a,a,b]*C[b] for b in n) for a in n))
acc=s.Matrix([simplify(sum(C[a]*(s.diff(C[b],coords[a])+sum(Gamma[b,a,c]*C[c] for c in n)) for a in n)) for b in n])
require('nonclosed_still_divergence_free',div==0)
require('nonclosed_still_affine',acc==s.zeros(4,1))
require('q_weighted_divergence_free',simplify(sum(s.diff(q*C[a],coords[a]) for a in n))==0)
# Differential algebra behind the transverse classification: harmonic H implies
# a_x=-b_y, a_y=b_x. Laplacian(a^2+b^2)=2|da|^2+2|db|^2.
ax,ay=s.symbols('a_x a_y',real=True)
require('constant_norm_harmonic_hessian_forces_constant',s.expand(2*(ax**2+ay**2+ay**2+ax**2))==4*(ax**2+ay**2))
# Full pullback polynomial checks for arbitrary symmetric trace-free K(u).
A,D=s.symbols('A D',real=True); K=s.Matrix([[A,D],[D,-A]])
p1,p2,d1,d2,e1,e2=s.symbols('p1 p2 d1 d2 e1 e2',real=True)
z=s.Matrix([x,y]); p=s.Matrix([p1,p2]); dp=s.Matrix([d1,d2]); ddp=s.Matrix([e1,e2])
quad=(z.T*K*z)[0]
G=s.Matrix([[quad,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
J=s.Matrix([[1,0,0,0],[(ddp.dot(z)+(dp.dot(dp)+p.dot(ddp))/2),1,d1,d2],[d1,0,1,0],[d2,0,0,1]])
shifted=G.subs({x:x+p1,y:y+p2},simultaneous=True)
def matzero(M):return all(simplify(e)==0 for e in M)
ode={e1:(K*p)[0],e2:(K*p)[1]}
require('arbitrary_profile_full_isometry_pullback',matzero((J.T*shifted*J-G).subs(ode)))
h=s.symbols('h',positive=True); F=s.diag(1,h*h,h,h)
require('arbitrary_profile_full_proper_homothety',matzero(F.T*G.subs({x:h*x,y:h*y},simultaneous=True)*F-h*h*G))
require('isometry_preserves_variable_root',J.T*beta==beta)
require('homothety_preserves_variable_root',F.T*beta==beta)
# Gauge removal with affine transverse terms, differentiated full matrix.
l1,l2,E,tprime=s.symbols('l1 l2 E tprime',real=True); L=s.Matrix([l1,l2])
Ga=G.copy(); Ga[0,0]=quad+L.dot(z)+E
Jg=s.Matrix([[1,0,0,0],[ddp.dot(z)+tprime,1,d1,d2],[d1,0,1,0],[d2,0,0,1]])
odes={e1:(K*p)[0]+l1/2,e2:(K*p)[1]+l2/2,tprime:(dp.dot(dp)+(p.T*K*p)[0]+L.dot(p)+E)/2}
require('full_affine_gauge_removal',matzero((Jg.T*Ga.subs({x:x+p1,y:y+p2},simultaneous=True)*Jg-G).subs(odes)))
require('wrong_translation_ode_is_detected',not matzero((J.T*shifted*J-G).subs({e1:0,e2:0})))
# Exact analytic witnesses, with no root branch division at zero.
Hw=(x**3-3*x*y**2)/3
Sw=s.expand(s.diff(Hw,x,2)**2+s.diff(Hw,x,y)**2)
alphaw=s.Matrix([s.diff(Sw,z)/(4*Sw) for z in coords])
qw=s.factor((alphaw.T*inv*alphaw)[0])
require('cubic_harmonic',s.diff(Hw,x,2)+s.diff(Hw,y,2)==0)
require('cubic_S',Sw==4*(x*x+y*y))
require('cubic_q',qw==1/(4*(x*x+y*y)))
require('cubic_nonclosed_at_regular_point',s.diff(Sw,x).subs({x:1,y:0})!=0)
Hv=(1+u)**2*(x*x-y*y)
Sv=s.expand(s.diff(Hv,x,2)**2+s.diff(Hv,x,y)**2)
require('variable_u_phase_branch',s.factor(Sv)==4*(u+1)**4)
rv=s.sqrt(2)*(u+1) # branch u>-1
require('closed_not_parallel_witness',s.diff(rv,x)==0 and s.diff(rv,y)==0 and s.diff(rv,u)!=0)
require('zero_root_excluded',Sw.subs({x:0,y:0})==0)
def sparse(T):return {''.join(map(str,k)):str(z) for k,z in T.items() if z!=0}
print(json.dumps(dict(versions=dict(python=platform.python_version(),sympy=s.__version__),checks=checks,
    connection=sparse(Gamma),riemann=sparse(R),weyl_harmonic=sparse(W),dual=sparse(star),quadratic=sparse(B),
    recurrence=[str(z) for z in alpha],q=str(q),cubic=dict(H=str(Hw),S=str(Sw),q=str(qw)),
    variable_u=dict(H=str(Hv),S=str(Sv),rho_domain='u>-1',rho=str(rv))),indent=2))
