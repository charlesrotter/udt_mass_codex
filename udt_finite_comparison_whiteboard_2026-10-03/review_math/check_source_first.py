"""Independent finite source-first FCW1 anchors; six declared control families."""
import hashlib
import json
import platform
from pathlib import Path
import sympy as S
import mpmath as mp

L, s, b, a, v = S.symbols('L s b a v', real=True)
fac = S.factorial
families = []
checks = []
def ck(name, expr):
    value = S.simplify(expr)
    checks.append({'name': name, 'residual': str(value)})
    if value != 0:
        raise AssertionError((name, value))
def trunc(expr, order):
    return S.series(expr, L, 0, order).removeO().expand()

# Family 1: genuine local product incidence; k=1, v=u^2, gamma^2=1+v.
# Exact source F=cosh(gamma*s)cosh(gamma*b)cos(L)
# -sinh(gamma*s)sinh(gamma*b)-cosh(u*(b-s)).
# Equivalent series organization avoids symbolic square roots.
cosg = lambda z: sum((1+v)**j*z**(2*j)/fac(2*j) for j in range(5))
cosu = lambda z: sum(v**j*z**(2*j)/fac(2*j) for j in range(5))
cosL = sum((-1)**j*L**(2*j)/fac(2*j) for j in range(5))
raw = (cosg(b-s)-cosu(b-s)+(cosL-1)*cosg(s)*cosg(b)).expand()
F = S.Add(*(term for term in raw.as_ordered_terms()
            if sum(term.as_powers_dict().get(z,0) for z in (s,b,L)) <= 8))

def solve_arrival(start, leading, label):
    ans = leading*L
    for order in (3,5,7):
        c = S.Symbol(label+str(order))
        test = ans+c*L**order
        coeff = trunc(F.subs({s:start,b:test}, simultaneous=True),order+2).coeff(L,order+1)
        found = S.solve(coeff,c)
        if len(found)!=1: raise AssertionError(('nonunique_coefficient',label,order,found))
        ans += S.factor(found[0])*L**order
    residual = trunc(F.subs({s:start,b:ans}, simultaneous=True),9)
    ck(label+'_incidence_to_L8',residual)
    return ans

B = solve_arrival(S.Integer(0),1,'B')
A = solve_arrival(B,2,'A')
Fs,Fb = S.diff(F,s),S.diff(F,b)
def ratio(start,end):
    num = trunc(-Fs.subs({s:start,b:end}, simultaneous=True),8)/L
    den = trunc(Fb.subs({s:start,b:end}, simultaneous=True),8)/L
    return trunc(num/den,7)
p = ratio(S.Integer(0),B)
q = ratio(B,A)
D = trunc(S.log(q)-S.log(p/(2-p*p)),7)
families.append({'family':'boosted_product_exact_series','v':'u^2, gamma^2=1+v',
                 'B':str(S.collect(B,L)), 'A':str(S.collect(A,L)),
                 'p':str(S.collect(p,L)), 'q':str(S.collect(q,L)),
                 'D':str(S.factor(D)),
                 'D_coefficients':{str(n):str(S.factor(D.coeff(L,n))) for n in (2,4,6)}})

# Family 2: unboosted control from the exact conformal chart, no series matching input.
ck('unboosted_p',trunc(p.subs(v,0)-1/S.cos(L),7))
ck('unboosted_q',trunc(q.subs(v,0)-S.cos(L)/S.cos(2*L),7))
ck('unboosted_exact_identity',S.trigsimp(S.cos(L)/S.cos(2*L)-(1/S.cos(L))/(2-1/S.cos(L)**2)))
families.append({'family':'unboosted_control','scope':'series through L6 and exact trig identity'})

# Family 3: 80-digit actual roots, rational boost gamma=5/4,u=3/4, 5 cases.
mp.mp.dps=80
gam=mp.mpf(5)/4
u=mp.mpf(3)/4
def exact_F(x,y,ell):
    return mp.cosh(gam*(y-x))-mp.cosh(u*(y-x))-2*mp.sin(ell/2)**2*mp.cosh(gam*x)*mp.cosh(gam*y)
def stretch(x,y,ell):
    df=gam*mp.sinh(gam*(y-x))-u*mp.sinh(u*(y-x))
    fs=-df-2*mp.sin(ell/2)**2*gam*mp.sinh(gam*x)*mp.cosh(gam*y)
    fb=df-2*mp.sin(ell/2)**2*gam*mp.cosh(gam*x)*mp.sinh(gam*y)
    return -fs/fb
nonzero=[n for n in (2,4,6) if S.simplify(D.coeff(L,n))!=0]
if not nonzero: raise AssertionError('no_nonzero_through_L6')
power=min(nonzero)
lead=S.factor(D.coeff(L,power).subs(v,S.Rational(9,16)))
rows=[]
for denom in (10,20,40,80,160):
    ell=mp.mpf(1)/denom
    beta=mp.findroot(lambda z:exact_F(0,z,ell),(ell,ell*mp.mpf('1.1')),solver='secant',maxsteps=80)
    ret=mp.findroot(lambda z:exact_F(beta,z,ell),(2*ell,2*ell*mp.mpf('1.1')),solver='secant',maxsteps=80)
    residual=max(abs(exact_F(0,beta,ell)),abs(exact_F(beta,ret,ell)))
    if residual>mp.mpf('1e-70'): raise AssertionError(('incidence_residual',residual))
    pp,qq=stretch(0,beta,ell),stretch(beta,ret,ell)
    if not (0<beta<ret and 0<pp<mp.sqrt(2) and qq>0):raise AssertionError('branch')
    dd=mp.log(qq)-mp.log(pp/(2-pp*pp))
    rows.append({key:mp.nstr(value,45) for key,value in {
        'L':ell,'b':beta,'a':ret,'p':pp,'q':qq,'D':dd,'D_over_L_power':dd/ell**power,
        'incidence_residual':residual}.items()})
families.append({'family':'independent_actual_root_control','precision_dps':80,
                 'root_tolerance':'1e-70','expected_leading_power':power,
                 'exact_leading_coefficient':str(lead),'rows':rows})

# Family 4: four-dimensional metric Christoffels/Ricci, no response equation.
eta=S.symbols('eta',real=True)
O=S.Function('Omega')(eta)
coords=(eta,S.Symbol('x'),S.Symbol('y'),S.Symbol('z'))
g=S.diag(-1,1,1,1)/O**2
gi=S.diag(-1,1,1,1)*O**2
d=lambda expr,j:S.diff(expr,coords[j])
Gamma=[[[S.simplify(sum(gi[i,m]*(d(g[m,k],j)+d(g[m,j],k)-d(g[j,k],m))/2 for m in range(4)))
          for k in range(4)] for j in range(4)] for i in range(4)]
Ric=S.Matrix(4,4,lambda i,j:S.simplify(sum(d(Gamma[k][i][j],k)-d(Gamma[k][i][k],j)
    +sum(Gamma[k][k][m]*Gamma[m][i][j]-Gamma[k][j][m]*Gamma[m][i][k] for m in range(4)) for k in range(4))))
R=S.simplify(sum(gi[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
R_expected=12*S.diff(O,eta)**2-6*O*S.diff(O,eta,2)
ck('original_metric_scalar',R-R_expected)
pOmega=1/O
ck('clock_curve_scalar_identity',6*S.diff(pOmega,eta,2)/pOmega**3-R)
families.append({'family':'conformal_metric_original_tensor','R':str(R),
                 'Ric_diagonal':[str(Ric[i,i]) for i in range(4)],'p':'1/Omega(L)'})

# Family 5: exact exponent controls, endpoint at E>0.
E=S.symbols('E',positive=True)
powerrows=[]
for exponent in (1,2):
    oo=(1-eta/E)**exponent
    rr=S.simplify(R_expected.subs(O,oo).doit())
    powerrows.append({'beta':exponent,'Omega':str(oo),'R':str(rr),
                      'endpoint_R':str(S.limit(rr,eta,E,dir='-')),
                      'endpoint_dOmega':str(S.diff(oo,eta).subs(eta,E))})
families.append({'family':'power_controls','rows':powerrows})

# Family 6: compact C-infinity interior deformation, a chosen mathematical example.
# eta in (E/4,3E/4); exp(-1/(1-z^2)) there, zero outside. It and all
# derivatives vanish at support endpoints, so the simple endpoint data match.
z=4*(eta-E/2)/E
bump=S.exp(-1/(1-z*z))
eps=S.symbols('epsilon',real=True)
deformed=(1-eta/E)*(1+eps*bump)
center=S.simplify(deformed.subs(eta,E/2))
center_R=S.simplify((12*S.diff(deformed,eta)**2-6*deformed*S.diff(deformed,eta,2)).subs(eta,E/2))
families.append({'family':'compact_interior_deformation',
                 'support':'E/4 < eta < 3E/4','epsilon_domain':'0 < epsilon < 1',
                 'Omega_center':str(center),'R_center':str(center_R),
                 'p_center':'1/Omega_center differs from 2 when epsilon!=0',
                 'endpoint_R':'12/E^2 unchanged: deformation identically zero near E'})

out={'context':'fresh source-first; no FCW1 candidate/code/results',
     'versions':{'python':platform.python_version(),'sympy':S.__version__,'mpmath':mp.__version__},
     'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'families':families,'zero_checks':checks,'status':'PASS'}
dest=Path(__file__).with_name('SOURCE_FIRST_CHECKS.json')
with dest.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
