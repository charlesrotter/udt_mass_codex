"""Independent FCW fidelity algebra; finite symbolic orders, six families max."""
import json, platform
from pathlib import Path
import sympy as S

L,x,y,v=S.symbols('L x y v', real=True)
R=S.Rational
checks=[]
def zero(name, value):
    value=S.factor(value)
    assert value == 0, (name,str(value))
    checks.append(name)
def ser(value,n):
    return S.series(value,L,0,n).removeO().expand()

# Family 1. Product-null world function from the de Sitter embedding invariant.
# cosh(gamma*(y-x))-cosh(u*(y-x))
# +(cos(L)-1)*cosh(gamma*x)*cosh(gamma*y)=0, gamma^2=1+v,u^2=v.
# Its homogeneous Taylor polynomial is formed without using any FCW formula.
F=0
for n in range(1,5):
    F+=((1+v)**n-v**n)*(y-x)**(2*n)/S.factorial(2*n)
for a in range(1,5):
    for b in range(4):
        for c in range(4):
            if a+b+c<=4:
                F+=(-1)**a*L**(2*a)*(1+v)**(b+c)*x**(2*b)*y**(2*c)/(S.factorial(2*a)*S.factorial(2*b)*S.factorial(2*c))
F=S.expand(F)
zero('null_world_function_symmetric',F-F.xreplace({x:y,y:x}))
b3,b5,b7=S.symbols('b3 b5 b7')
b=L+b3*L**3+b5*L**5+b7*L**7
first=ser(F.subs({x:0,y:b}),9)
bsol={}
for power,var in [(4,b3),(6,b5),(8,b7)]:
    bsol[var]=S.factor(S.solve(first.coeff(L,power).subs(bsol),var)[0])
b=S.expand(b.subs(bsol))
zero('first_arrival_order8',ser(F.subs({x:0,y:b}),9))
a3,a5,a7=S.symbols('a3 a5 a7')
a=2*L+a3*L**3+a5*L**5+a7*L**7
ret=ser(F.subs({x:b,y:a}),9)
asol={}
for power,var in [(4,a3),(6,a5),(8,a7)]:
    asol[var]=S.factor(S.solve(ret.coeff(L,power).subs(asol),var)[0])
a=S.expand(a.subs(asol))
zero('return_arrival_order8',ser(F.subs({x:b,y:a}),9))
Fx,Fy=S.diff(F,x),S.diff(F,y)
pn=ser(-Fx.subs({x:0,y:b}),7)/L
pd=ser(Fy.subs({x:0,y:b}),7)/L
qn=ser(-Fx.subs({x:b,y:a}),7)/L
qd=ser(Fy.subs({x:b,y:a}),7)/L
p=ser(pn/pd,5)
q=ser(qn/qd,5)
res=ser((2-p*p)*q-p,5)
zero('untilted_p_sec',ser(p.subs(v,0)-1/S.cos(L),5))
zero('untilted_echo_identity',res.subs(v,0))
zero('leading_three_to_one',q.coeff(L,2)-3*p.coeff(L,2))
# Match the scalar p to the untilted family: q0(p)=p/(2-p^2).
matched=ser(q-p/(2-p*p),5)
assert S.factor(matched.coeff(L,4)).subs(v,1)!=0
checks.append('tilted_same_p_echo_obstruction_nonzero')

# Family 2. Simple conformal zero and power controls, all symbolic.
d,h,c=S.symbols('d h c',positive=True)
om=h*d+c*d*d
P=1/om
H=S.diff(om,d)
Rscalar=6*(2*S.diff(om,d)**2-om*S.diff(om,d,2))
zero('simple_zero_residue',S.limit(d*P,d,0,dir='+')-1/h)
zero('simple_zero_H',S.limit(H,d,0,dir='+')-h)
zero('simple_zero_R',S.limit(Rscalar,d,0,dir='+')-12*h*h)
power_controls={}
for beta in (R(1,2),S.Integer(1),S.Integer(2)):
    # eta*=1 normalization is FREE; d=1-eta.
    O=d**beta
    PP=1/O
    HH=S.diff(O,d)
    RR=6*(2*S.diff(O,d)**2-O*S.diff(O,d,2))
    power_controls[str(beta)]={'p':str(PP),'H':str(HH),'R':str(S.factor(RR)),
       'proper_time_antiderivative':str(-S.integrate(PP,d))}
    zero('power_H_'+str(beta),HH-beta*d**(beta-1))

# Family 3. Compact positive interior deformation leaves endpoint behavior free.
# A compactly supported smooth bump is justified analytically, not by polynomial
# pretending to have compact support. Its local value is an independent symbol.
eps,B=S.symbols('eps B',real=True)
O=S.symbols('O',positive=True)
deformed=O*S.exp(eps*B)
zero('interior_p_ratio', (1/deformed)/(1/O)-S.exp(-eps*B))
zero('deformation_off_support',deformed.subs(B,0)-O)

# Family 4. Conformal null-affine tangent endpoint frequency cancellation.
# k_tilde=exp(-2psi)k; g_tilde=exp(2psi)g; U_tilde=exp(-psi)U.
psi,omega=S.symbols('psi omega',real=True)
measured=S.exp(2*psi)*S.exp(-2*psi)*S.exp(-psi)*omega
zero('endpoint_conformal_frequency',measured-S.exp(-psi)*omega)
zero('clock_neighborhood_frequency',measured.subs(psi,0)-omega)

result={'scope':'conditional exact finite algebra anchors; analytic proof owns general claims',
 'python':platform.python_version(),'sympy':S.__version__,'symbolic_families':4,
 'checks':checks,'count':len(checks),'b_series':str(S.factor(b)),
 'a_series':str(S.factor(a)),'p_series':str(S.collect(S.factor(p),L)),
 'q_series':str(S.collect(S.factor(q),L)),
 'echo_residual_series':str(S.factor(res)),
 'q_minus_untilted_same_p':str(S.factor(matched)),
 'power_controls':power_controls,'status':'PASS'}
Path(__file__).with_name('SOURCE_FIRST_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
