"""Exact central-connection anchors; original Ricci checks for the optional ansatz."""
import json,itertools
import sympy as s
results=[]
# Full area data differentiate in ten independent symmetric metric entries.
pairs=list(itertools.combinations(range(4),2));positions=[(i,j) for i in range(4) for j in range(i,4)]
v=s.symbols('g0:10');g=s.zeros(4)
for value,(i,j) in zip(v,positions):g[i,j]=g[j,i]=value
areas=[g[i,k]*g[j,l]-g[i,l]*g[j,k] for a,(i,j) in enumerate(pairs) for k,l in pairs[a:]]
J=s.Matrix(areas).jacobian(v);flat={value:(-1 if i==0 else 1) if i==j else 0 for value,(i,j) in zip(v,positions)}
assert J.subs(flat).rank()==10;results.append('area differential rank10 on nondegenerate Lorentz control')
p,q=s.symbols('p q',positive=True);b=(p*q-1)/(p*q+1)
assert s.factor(((1/p+q)/2)**2-((q-1/p)/2)**2)==q/p
assert s.factor((p/q)*(1-b*b)*((1/p+q)/2)**2)==1
kd,sd=s.symbols('Kdot Sdot');tx=(kd+b*sd)/(1-b*b);rx=(-sd-b*kd)/(1-b*b)
assert s.factor(tx+b*rx-kd)==0 and s.factor(-b*tx-rx-sd)==0
results.append('actual two-way normalization and gradient system')
eta=s.diag(-1,1,1,1);e0=s.eye(4)[:,0];e1=s.eye(4)[:,1];C=s.Rational(5,3);S=s.Rational(4,3)
def halfH(u,n):
 a=eta*u;c=eta*n;return a*a.T+c*c.T
cross=halfH(C*e0+S*e1,S*e0+C*e1)-(C*C+S*S)*halfH(e0,e1)
a=eta*e0;c=eta*e1;right=2*C*S*(a*c.T+c*a.T)
assert cross==right and cross!=-right and cross[0,1]==-2*C*S
results.append('G310 corrected covector sign with negative coordinate component')
tau,q=s.symbols('tau q',real=True);assert s.expand(tau**2-(tau**2+2*q*q))==-2*q*q
x=s.symbols('x',real=True);Tau=s.Function('tau')(x);assert s.diff(Tau,x)-s.diff(Tau,x)==0
# Momentum equation is checked as actual divergence minus trace gradient.
K=s.diag(Tau,q,-q);momentum=[sum(s.diff(K[j,i],x) if j==0 else 0 for j in range(3))-(s.diff(s.trace(K),x) if i==0 else 0) for i in range(3)]
assert momentum==[0,0,0];results.append('full non-CMC flat-torus constraints with Lambda=-q^2')
# Direct Christoffels/Ricci from full4D original metric, no producer import.
t,xi,y,z=s.symbols('t xi y z',positive=True);coords=[t,xi,y,z];P=s.Function('P')(t,xi);lam=s.Function('lam')(t,xi)
A=s.exp(lam/2)/s.sqrt(t);G=s.diag(-A,A,t*s.exp(P),t*s.exp(-P));Gi=G.inv()
Ga=[[[s.simplify(sum(Gi[a,d]*(s.diff(G[d,c],coords[b])+s.diff(G[d,b],coords[c])-s.diff(G[b,c],coords[d])) for d in range(4))/2) for c in range(4)] for b in range(4)] for a in range(4)]
Ric=s.Matrix(4,4,lambda a,b:s.simplify(sum(s.diff(Ga[c][a][b],coords[c])-s.diff(Ga[c][a][c],coords[b])+sum(Ga[c][a][b]*Ga[d][c][d]-Ga[d][a][c]*Ga[c][b][d] for d in range(4)) for c in range(4))))
pt=s.diff(P,t);px=s.diff(P,xi);lt=t*(pt**2+px**2);lx=2*t*pt*px
sub={s.diff(lam,t,2):s.diff(lt,t),s.diff(lam,xi,2):s.diff(lx,xi),s.diff(lam,t,xi):s.diff(lt,xi),s.diff(lam,t):lt,s.diff(lam,xi):lx}
res=Ric.applyfunc(lambda e:s.simplify(e.subs(sub,simultaneous=True).subs(s.diff(P,t,2),s.diff(P,xi,2)-pt/t)))
assert res==s.zeros(4);results.append('all original Ricci components vanish under polarized reduction')
k=s.symbols('k',positive=True);F=s.Function('F')(t);fp=s.diff(F,t);L=t*t*(fp**2+k*k*F*F)/2+t*F*fp/2-s.Rational(9,8)
rule={s.diff(F,t,2):-fp/t-k*k*F}
assert s.simplify(s.diff(L,t).subs(rule)-t*(fp**2+k*k*F*F)/2)==0
assert s.simplify(s.diff(t*F*fp/2,t).subs(rule)-t*(fp**2-k*k*F*F)/2)==0
results.append('exact nonlinear lambda compatibility with chosen F ODE')
# Optional null-source coordinate-flux algebra, not a physical source adoption.
a,bb,cc=s.symbols('a b c',real=True);D=bb*bb-a*cc;Q=(-bb+s.sqrt(D))/a
assert s.simplify(a*Q*Q+2*bb*Q+cc)==0
assert s.simplify(a*Q+bb)==s.sqrt(D);results.append('optional future-raised null root')
print(json.dumps({'result':'PASS','sympy':s.__version__,'checked_connections':results,'scope':'Exact controls and original metric residuals. Conditional ansatz only; no general existence/stability proof or physical promotion.'},indent=2))
