"""Bounded exact algebra support for NR1; no physical inputs or source edits."""
import argparse
import json
import sys
import sympy as s

parser = argparse.ArgumentParser()
parser.add_argument('--mutant', choices=['plus', 'omit_cross', 'omit_sine_velocity'])
args = parser.parse_args()
checks = []

def gate(expr, name):
    assert s.simplify(expr) == 0, name
    checks.append(name)

e, a, b, T = s.symbols('e a b T', positive=True)
u, w, p, r = s.symbols('u w p r', real=True)
H = s.Matrix([[u,w],[w,-u]])
P = s.Matrix([[p,r],[r,-p]])
gamma = s.diag(a*a,b*b,b*b)
h = s.zeros(3); h[1:3,1:3] = 2*b*b*H
K = s.diag(a*a/(3*T),-2*b*b/(3*T),-2*b*b/(3*T))
dK = s.zeros(3); dK[1:3,1:3] = -b*b*(P+4*H/(3*T))
ge = gamma+e*h; ke = K+e*dK; inv = ge.inv()
tau = s.trace(inv*ke)
pie = s.sqrt(ge.det())*(inv*ke*inv-tau*inv)
pi1 = pie.diff(e).subs(e,0).applyfunc(s.simplify)
expected = s.zeros(3); expected[1:3,1:3] = a*(-P-2*H/(3*T))
for i in range(3):
    for j in range(3): gate(pi1[i,j]-expected[i,j], f'full_density_variation_{i}{j}')
gate(tau.diff(e).subs(e,0),'trace_variation_zero')
gate(s.diff(s.sqrt(ge.det()),e).subs(e,0),'volume_variation_zero')

uc1,uc2,us1,us2,vc1,vc2,vs1,vs2=s.symbols('uc1 uc2 us1 us2 vc1 vc2 vs1 vs2',real=True)
theta=s.symbols('theta',real=True)
uc=s.Matrix([uc1,uc2]); us=s.Matrix([us1,us2]); vc=s.Matrix([vc1,vc2]); vs=s.Matrix([vs1,vs2])
q=uc*s.cos(theta)+us*s.sin(theta); v=vc*s.cos(theta)+vs*s.sin(theta)
HH=s.Matrix([[q[0],q[1]],[q[1],-q[0]]]); VV=s.Matrix([[v[0],v[1]],[v[1],-v[0]]])
integral=s.integrate(s.expand_trig(s.trace(VV*HH.diff(theta))),(theta,0,2*s.pi))
def candidate_Q():
    if args.mutant=='plus': return vc.dot(us)+vs.dot(uc)
    if args.mutant=='omit_cross': return vc1*us1-vs1*uc1
    if args.mutant=='omit_sine_velocity': return vc.dot(us)
    return vc.dot(us)-vs.dot(uc)
Q=candidate_Q()
gate(integral-2*s.pi*Q,'full_fourier_integral_matches_candidate')
gate(s.integrate(s.trace(HH*HH.diff(theta)),(theta,0,2*s.pi)),'background_density_term_is_total_derivative')

# Coefficient independence from arbitrary periodic second-order metric entries.
# This finite Fourier polynomial supports (does not replace) the integration proof.
z0,z1,z2=s.symbols('z0 z1 z2')
arbitrary=z0+z1*s.cos(3*theta)+z2*s.sin(5*theta)
gate(s.integrate(s.diff(arbitrary,theta),(theta,0,2*s.pi)),'periodic_second_order_term_integrates_zero')

freq=s.symbols('freq',positive=True)
variables=list(uc)+list(us)+list(vc)+list(vs)
derivatives=list(vc)+list(vs)+list(-vc/T-freq*uc)+list(-vs/T-freq*us)
gate(sum(s.diff(Q,z)*dz for z,dz in zip(variables,derivatives))+Q/T,'ode_preserves_TQ')
Ac=s.Matrix(s.symbols('Ac1 Ac2')); Bc=s.Matrix(s.symbols('Bc1 Bc2'))
As=s.Matrix(s.symbols('As1 As2')); Bs=s.Matrix(s.symbols('Bs1 Bs2'))
J,Y,dJ,dY=s.symbols('J Y dJ dY')
replacement=dict(zip(variables,list(Ac*J+Bc*Y)+list(As*J+Bs*Y)+list(Ac*dJ+Bc*dY)+list(As*dJ+Bs*dY)))
gate(Q.subs(replacement,simultaneous=True)-(J*dY-dJ*Y)*(Bc.dot(As)-Ac.dot(Bs)),'bessel_coefficient_form')

cases=[([1,0,0,0,0,0,1,0],-1),
       ([1,0,0,1,0,1,1,0],0),
       ([1,2,0,0,3,4,0,0],0),
       ([0]*8,0)]
for n,(vals,want) in enumerate(cases): gate(Q.subs(dict(zip(variables,vals)))-want,f'nonzero_or_surviving_control_{n}')
print(json.dumps({'status':'PASS_EXACT_ALGEBRA_SUPPORT_NOT_EXISTENCE','checks':checks,'count':len(checks),'pi1_transverse':str(expected[1:3,1:3]),'fourier_integral':str(integral),'candidate_Q':str(Q),'python':sys.version,'sympy':s.__version__,'mutant':args.mutant},indent=2))
