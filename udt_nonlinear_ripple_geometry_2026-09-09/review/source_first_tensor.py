"""Source-first full-coordinate Ricci check; no author candidate/code imported.

FREE supplied unit initial metric, axial period 2*pi, transverse markings,
plus polarization, and amplitude. The rational 3/4 follows from matching
the existing SE1 normal expansion; not a physical constant.
METHOD: exact SymPy coordinate differentiation, all 16 Ricci components.
Resources enforced externally: 512 MiB, 60 seconds, one thread.
"""
import json
import platform
import sympy as s

t = s.symbols('t', positive=True)
x, y, z = s.symbols('x y z', real=True)
coords = (t, x, y, z)
P, L = (s.Function(n)(t, x) for n in ('P', 'L'))
b = s.Rational(3, 4)
A = s.exp(L / 2) / s.sqrt(t)
g = s.diag(-b*b*A, A, t*s.exp(P), t*s.exp(-P))
gi = g.inv()

def connection(metric, inverse, variables):
    n = len(variables)
    return [[[s.simplify(sum(inverse[a,d]*(
        s.diff(metric[d,c], variables[b0])
        + s.diff(metric[d,b0], variables[c])
        - s.diff(metric[b0,c], variables[d])) for d in range(n))/2)
        for c in range(n)] for b0 in range(n)] for a in range(n)]

def ricci(ch, variables):
    n = len(variables)
    return s.Matrix(n,n,lambda i,j:s.simplify(sum(
        s.diff(ch[a][i][j],variables[a])-s.diff(ch[a][i][a],variables[j])
        + sum(ch[a][a][d]*ch[d][i][j]-ch[a][j][d]*ch[d][i][a]
              for d in range(n)) for a in range(n))))

ch = connection(g,gi,coords)
R = ricci(ch,coords)
pt,px=s.diff(P,t),s.diff(P,x)
ptt=b*b*s.diff(P,x,2)-pt/t
lt=t*(pt*pt+b*b*px*px)
lx=2*t*pt*px
rules={s.diff(L,t,2):s.diff(lt,t).subs(s.diff(P,t,2),ptt),
       s.diff(L,t,x):s.diff(lx,t).subs(s.diff(P,t,2),ptt),
       s.diff(L,x,2):s.diff(lx,x),
       s.diff(L,t):lt,s.diff(L,x):lx,s.diff(P,t,2):ptt}
Ron=R.applyfunc(lambda q:s.simplify(q.subs(rules, simultaneous=True)))
assert Ron == s.zeros(4), ('original_Ricci',Ron)

# All components of induced initial gamma and future-normal K.
e=s.symbols('e',real=True)
initial={P:0,L:0,pt:s.Rational(3,2)*e*s.cos(x),px:0,t:1}
N=b*s.exp(L/4)*t**(-s.Rational(1,4))
gamma=g[1:4,1:4]
K=-gamma.diff(t)/(2*N)
gamma1=gamma.subs(initial, simultaneous=True)
K1=K.subs(s.diff(L,t),lt).subs(initial, simultaneous=True).applyfunc(s.simplify)
expected=s.diag(s.Rational(1,3)-s.Rational(3,4)*e**2*s.cos(x)**2,
                -s.Rational(2,3)-e*s.cos(x),-s.Rational(2,3)+e*s.cos(x))
assert gamma1 == s.eye(3)
assert K1 == expected, ('initial_K',K1)
assert s.simplify(s.trace(K1)**2-s.trace(K1*K1))==0
assert s.simplify(s.diff(K1[1,1]+K1[2,2],x))==0

# Direct intrinsic Ricci, distinct from the spacetime constraint projection.
R3tensor=ricci(connection(gamma,gamma.inv(),coords[1:]),coords[1:])
R3=s.simplify(s.trace(gamma.inv()*R3tensor))
assert s.simplify(R3+px**2/(2*A))==0
area_rate=1/(t*N)
normalized=s.simplify(R3/area_rate**2)
assert normalized == -s.Rational(9,32)*t*t*px*px

# Exact single-mode constraint antiderivative using arbitrary f solving ODE.
f=s.Function('f')(t)
fp=s.diff(f,t)
fpp=-fp/t-b*b*f
Pmode=e*f*s.cos(x)
Lmode=e*e/2*(t*t*(fp*fp+b*b*f*f)+t*f*fp*(1+s.cos(2*x))-s.Rational(9,4))
Lt=s.simplify(s.diff(Lmode,t).subs(s.diff(f,t,2),fpp))
Lx=s.diff(Lmode,x)
assert s.trigsimp(Lt-t*(s.diff(Pmode,t)**2+b*b*s.diff(Pmode,x)**2))==0
assert s.simplify(Lx-2*t*s.diff(Pmode,t)*s.diff(Pmode,x))==0
assert s.simplify(Lmode.subs({f:0,fp:s.Rational(3,2),t:1}, simultaneous=True))==0
assert s.simplify(s.integrate(Lx,(x,0,2*s.pi)))==0

# Original-equation adverse control: holding longitudinal response at zero
# is not a solution for the nontrivial initial polarization rate.
no_L={L:0,s.diff(L,t):0,s.diff(L,x):0,s.diff(L,t,2):0,
      s.diff(L,t,x):0,s.diff(L,x,2):0}
broken=R.subs(no_L, simultaneous=True).subs(s.diff(P,t,2),ptt)
probe={P:0,pt:s.Rational(1,4),px:0,s.diff(P,x,2):0,
       s.diff(P,t,x):0,t:1}
broken_probe=broken.subs(probe, simultaneous=True).applyfunc(s.simplify)
assert broken_probe != s.zeros(4)

# G327 time equation follows at first order with T=t^(3/4).
T=s.symbols('T',positive=True)
h=s.Function('h')(T)
dTdt=s.Rational(3,4)*T**(-s.Rational(1,3))
chain=s.simplify(dTdt*s.diff(dTdt*s.diff(h,T),T)
                  +T**(-s.Rational(4,3))*dTdt*s.diff(h,T)+b*b*h)
claimed=b*b*T**(-s.Rational(2,3))*(s.diff(h,T,2)+s.diff(h,T)/T+T**(s.Rational(2,3))*h)
assert s.simplify(chain-claimed)==0

print(json.dumps(dict(python=platform.python_version(),sympy=s.__version__,
    metric=[str(g[i,i]) for i in range(4)],
    original_Ricci=[[str(R[i,j]) for j in range(4)] for i in range(4)],
    on_shell_Ricci=[[str(Ron[i,j]) for j in range(4)] for i in range(4)],
    initial_gamma=str(gamma1),initial_K=str(K1),
    spatial_scalar=str(R3),area_rate=str(area_rate),normalized_curvature=str(normalized),
    explicit_L=str(Lmode),zero_response_defect=str(broken_probe),
    result='PASS_EXACT_BOUNDED_IDENTITIES'),indent=2))
