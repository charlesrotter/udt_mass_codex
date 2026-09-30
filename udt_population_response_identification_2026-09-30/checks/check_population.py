"""Exact PRI1 algebra anchors. Supplied beam/boost values are FREE controls."""
import json
import platform
import sympy as s

identities = {}
rejections = {}
def eq(name, value):
    value = s.simplify(value)
    assert value == 0, (name, value)
    identities[name] = str(value)
def matrix_eq(name, value):
    residual = value.applyfunc(s.simplify)
    assert residual == s.zeros(*value.shape), (name, residual)
    identities[name] = 'zero matrix'
def wrong(name, value):
    value = s.simplify(value)
    assert value != 0, (name, value)
    rejections[name] = str(value)

g = s.diag(-1, 1, 1, 1)
dot = lambda a,b: (a.T*g*b)[0]
moment = lambda population: sum((w*(g*k)*(g*k).T for w,k in population), s.zeros(4))
energy = lambda M,u: (u.T*M*u)[0]
H = lambda u,n: 2*((g*u)*(g*u).T+(g*n)*(g*n).T)
pairing = lambda M,h: s.trace(g*M*g*h)
e0=s.Matrix([1,0,0,0])
axes=[s.Matrix([0,int(j==0),int(j==1),int(j==2)]) for j in range(3)]
pop=[(s.Integer(j+1),e0+sign*n) for j,n in enumerate(axes) for sign in (-1,1)]
assert all(dot(k,k)==0 for _,k in pop)
M0=moment(pop)
matrix_eq('anisotropic rest moment from six rays',M0-s.diag(12,2,4,6))
b=s.Matrix([s.Rational(1,3),s.Rational(2,3),0]); gamma=s.Rational(3,2)
L=s.zeros(4); L[0,0]=gamma
for j in range(3):
    L[0,j+1]=L[j+1,0]=gamma*b[j]
for i in range(3):
    for j in range(3):L[i+1,j+1]=int(i==j)+(gamma-1)*b[i]*b[j]/(b.dot(b))
matrix_eq('nonaxial Lorentz boost',L.T*g*L-g)
boosted=[(w,L*k) for w,k in pop]; M=moment(boosted); u=L*e0; n=L*axes[0]
eq('boosted observer norm',dot(u,u)+1)
eq('boosted moment Lorentz trace',s.trace(g*M))
matrix_eq('boosted observer mixed eigenvector',g*M*u+12*u)
eq('boosted eigenvalue from original beam sum',energy(M,u)-12)
eq('boosted reciprocal contraction',pairing(M,H(u,n))-28)
eq('independent beam reciprocal contraction',pairing(M,H(u,n))-2*sum(w*(dot(k,u)**2+dot(k,n)**2) for w,k in boosted))
wrong('wrong Euclidean eigenvector identification',(M*u+12*u)[0])

z,c=s.symbols('z c',real=True,positive=True)
co=(z+1/z)/2; si=(z-1/z)/2
eq('coercivity integrand expansion',(co-si*c)**2-(z*z*(1-c)**2/4+(1-c*c)/2+(1+c)**2/(4*z*z)))
t,a,b0,c0=s.symbols('t a b c',real=True)
ct=s.cosh(t);st=s.sinh(t)
q=a*ct**2+2*b0*ct*st+c0*st**2
v=a*st**2+2*b0*ct*st+c0*ct**2
eq('hyperbolic geodesic Hessian',s.diff(q,t,2)-2*(q+v))
A,B=s.symbols('A B',positive=True)
qbeam=A/z**2+B*z**2;zstar=(A/B)**s.Rational(1,4)
eq('two-beam critical rapidity',(z*s.diff(qbeam,z)).subs(z,zstar))
eq('two-beam minimum value',qbeam.subs(z,zstar)-2*s.sqrt(A*B))
eq('single-beam unattained infimum',s.limit(A/z**2,z,s.oo))
wrong('single-beam finite minimum at unit boost',(z*s.diff(A/z**2,z)).subs(z,1))

kp=e0+axes[0];km=e0-axes[0];two=[(s.Integer(4),kp),(s.Integer(1),km)]
T=moment(two); J=sum((w*k for w,k in two),s.zeros(4,1))
uJ=J/s.sqrt(-dot(J,J));uM=s.Matrix([3,1,0,0])/(2*s.sqrt(2))
eq('first-moment observer norm',dot(uJ,uJ)+1)
eq('second-moment observer norm',dot(uM,uM)+1)
matrix_eq('second-moment observer original eigenvector',g*T*uM+4*uM)
eq('first-moment velocity',uJ[1]/uJ[0]-s.Rational(3,5))
eq('second-moment velocity',uM[1]/uM[0]-s.Rational(1,3))
wrong('one population does not force same moment frames',uJ[1]/uJ[0]-uM[1]/uM[0])
nJ=s.Matrix([3,5,0,0])/4
eq('nonzero energy flux in current frame',(uJ.T*T*nJ)[0]-3)
wrong('current observer is not second-moment eigenvector',(uJ.T*T*nJ)[0])

rho,lam=s.symbols('rho lambda',positive=True)
iso=s.diag(rho,rho/3,rho/3,rho/3)
eq('isotropic null trace',s.trace(g*iso))
eq('isotropic reciprocal response',pairing(iso,H(e0,axes[0]))-8*rho/3)
eq('pure trace invisible to reciprocal tangent',pairing(lam*g,H(e0,axes[0])))
wrong('isotropic population is not DDR balanced',pairing(iso,H(e0,axes[0])))
wrong('adding pure trace cannot rescue moment',pairing(iso+lam*g,H(e0,axes[0])))

x=s.symbols('x',real=True);P4=(35*x**4-30*x*x+3)/8
for power in (0,1,2):eq(f'P4 low moment {power}',s.integrate(x**power*P4,(x,-1,1)))
eq('P4 fourth moment',s.integrate(x**4*P4,(x,-1,1))-s.Rational(16,315))
eq('P4 critical factorization',s.diff(P4,x)-s.Rational(5,2)*x*(7*x*x-3))
eq('P4 interior minimum',P4.subs(x,s.sqrt(s.Rational(3,7)))+s.Rational(3,7))
eq('P4 endpoint maximum',P4.subs(x,1)-1)
eq('P4 central critical value',P4.subs(x,0)-s.Rational(3,8))
wrong('isotropic low moments do not erase fourth anisotropy',s.integrate(x**4*P4,(x,-1,1)))

print(json.dumps({'status':'PASS','python':platform.python_version(),'sympy':s.__version__,
 'identities':identities,'wrong_nonidentities_rejected':rejections,
 'scope':'Exact finite controls only; coercivity/uniqueness/smoothness and physical interpretation remain analytic and conditional.'},indent=2))
