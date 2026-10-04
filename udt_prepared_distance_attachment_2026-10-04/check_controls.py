"""Finite exact controls; not certification of the generic conditional theorem."""
import json, platform
import sympy as s

checks=[]
def zero(name, expr):
    value=s.simplify(expr)
    assert value == 0, (name, str(value))
    checks.append(name)

x=s.symbols('x', positive=True)
p,q,r=s.symbols('p q r', real=True)
coords=(x,)+s.symbols('y z w', real=True)
g=s.diag(-1,1,1,1)/x**2
inv=g.inv()
Gamma=[[[s.simplify(sum(inv[i,l]*(s.diff(g[l,k],coords[j])+
    s.diff(g[l,j],coords[k])-s.diff(g[j,k],coords[l]))/2
    for l in range(4))) for k in range(4)] for j in range(4)] for i in range(4)]
gam=s.sqrt(1+(p*p+q*q+r*r)*x*x)
u=s.Matrix([-x*gam,x*x*p,x*x*q,x*x*r])
zero('original metric unit normalization',(u.T*g*u)[0]+1)
for i in range(4):
    zero(f'original Christoffel geodesic {i}',u[0]*s.diff(u[i],x)+
         sum(Gamma[i][j][k]*u[j]*u[k] for j in range(4) for k in range(4)))
gam1=gam.subs(x,1)
for i,P in enumerate((p,q,r)):
    displacement=(1-x*x)*P/(gam1+gam)
    zero(f'position derivative {i}',s.diff(displacement,x)-u[i+1]/u[0])

gp=s.sqrt(1+p*p*x*x)
D=p*(1-x*x)/(s.sqrt(1+p*p)+gp)
L=1-x-D
Lstar=1-p/(s.sqrt(1+p*p)+1)
B=gp-p*x
Z=1/(x*B)
zero('initial L zero',L.subs(x,1))
zero('radial incidence',L+D-(1-x))
zero('L derivative',s.diff(L,x)-(-1+p*x/gp))
zero('radial endpoint',s.limit(L,x,0,dir='+')-Lstar)
zero('radial pole residue',s.limit((Lstar-L)*Z,x,0,dir='+')-1)
zero('normal distance law',(Z*(1-L)-1).subs(p,0))

# Original vector flow for the deliberately degenerate label preparation.
# r,v are label offsets, x is the reception parameter; no label jet is imposed.
rr,v,w=s.symbols('rr v w', real=True)
a=s.Matrix([1+rr,v,w]); F=s.Matrix([1-v,rr+v*v,w])
d=F-a; d2=(d.T*d)[0]; P=2*d/(1-d2)
ga=s.sqrt(1+(P.T*P)[0]*x*x)
Y=F-P*x*x/(ga+1)
base={rr:0,v:0,w:0}
labels=(rr,v,w)
J=F.jacobian(labels).subs(base)
zero('endpoint Jacobian det',J.det()-1)
A=s.simplify(Y.jacobian(labels).subs(base))
for i in range(3):
    for j in range(3):
        zero(f'base flow Jacobian {i}{j}',A[i,j]-(x*x*s.eye(3)+(1-x*x)*J)[i,j])
zero('base Jacobian determinant',A.det()-(x**4+(1-x*x)**2))
zero('determinant lower bound identity',x**4+(1-x*x)**2-s.Rational(1,2)-2*(x*x-s.Rational(1,2))**2)
# sqrt(1+|P|^2)=(1+|d|^2)/(1-|d|^2) on the stated |d|<1 domain.
gd=(1+d2)/(1-d2)
zero('momentum inverse normalization',gd*gd-1-(P.T*P)[0])
for i in range(3): zero(f'endpoint inverse identity {i}',P[i]/(gd+1)-d[i])
H=Y-s.Matrix([1-x,0,0])
origin={x:0,**base}
Hx=H.diff(x).subs(origin)
first=-J.inv()*Hx
for i,expected in enumerate((0,1,0)):zero(f'implicit first {i}',first[i]-expected)
second_forcing=[]
for h in H:
    val=s.diff(h,x,2).subs(origin)
    val+=2*sum(s.diff(h,x,b).subs(origin)*first[j] for j,b in enumerate(labels))
    val+=sum(s.diff(h,b,c).subs(origin)*first[j]*first[k]
             for j,b in enumerate(labels) for k,c in enumerate(labels))
    second_forcing.append(s.simplify(val))
second=-J.inv()*s.Matrix(second_forcing)
for i,expected in enumerate((-2,0,0)):zero(f'implicit second {i}',second[i]-expected)
dist=s.sqrt((a.T*a)[0])
grad=s.Matrix([s.diff(dist,b) for b in labels]).subs(base)
hes=s.hessian(dist,labels).subs(base)
zero('distance first derivative',(grad.T*first)[0])
zero('distance second derivative',(grad.T*second)[0]+(first.T*hes*first)[0]+1)
zero('endpoint frequency coefficient',(ga-P[0]*x).subs(origin)-1)

# Actual straight return null leg: from (x,1-x) to (xa,0), future decreasing x.
xa=s.symbols('xa', real=True)
return_solution=s.solve(s.Eq(1-x,x-xa),xa)
assert return_solution == [2*x-1]
checks.append('return null equation gives xa=2x-1; physical iff x>1/2')
t=s.symbols('t',real=True)
U=s.Matrix([-s.cosh(t),-s.sinh(t),0,0])
for i in range(4):
    zero(f'ambient parallel transport {i}',s.diff(U[i],t)+sum(Gamma[i][1][j].subs(x,1)*U[j] for j in range(4)))
oldP=(1-x**-2)/2
assert s.limit(oldP,x,0,dir='+') == -s.oo
checks.append('CCW initial momentum unbounded')
assert len(checks)<100
print(json.dumps(dict(status='PASS',python=platform.python_version(),sympy=s.__version__,
    families=5,exact_checks=len(checks),checks=checks,
    critical_first=list(map(str,first)),critical_second=list(map(str,second)),
    distance_second='-1',critical_B_limit='1',
    limits='Analytic hypotheses and stated real domains are not certified by finite controls'),indent=2))
