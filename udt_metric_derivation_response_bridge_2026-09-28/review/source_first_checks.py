"""Independent exact 4D metric computation; imports no parent package code."""
import json
import platform
import time
import sympy as s

started = time.monotonic()
t, r, th, ph = s.symbols('t r theta phi', real=True)
x = [t, r, th, ph]
f, N = s.Function('f')(r), s.Function('N')(r)
a, b, d, k, c1, c2, eps = s.symbols('a b d k c1 c2 eps', real=True)
checks = []

def zero(name, expression):
    result = s.simplify(expression)
    if result != 0:
        raise AssertionError((name, str(result)))
    checks.append(name)

def true(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)

g = s.diag(-N**2*f, 1/f, r*r, r*r*s.sin(th)**2)
gi = g.inv()
Gamma = [[[s.simplify(sum(gi[i,l]*(s.diff(g[l,j],x[h])+s.diff(g[l,h],x[j])-s.diff(g[j,h],x[l])) for l in range(4))/2)
           for h in range(4)] for j in range(4)] for i in range(4)]
Ric = s.Matrix(4,4,lambda i,j:s.simplify(sum(
    s.diff(Gamma[l][i][j],x[l])-s.diff(Gamma[l][i][l],x[j])+
    sum(Gamma[l][i][j]*Gamma[m][l][m]-Gamma[m][i][l]*Gamma[l][j][m] for m in range(4))
    for l in range(4))))
scalar = s.simplify(s.trace(gi*Ric))
atN1 = {N:1,s.diff(N,r):0,s.diff(N,r,2):0}
primary = s.simplify((gi*Ric).subs(atN1))
P = -s.diff(f,r,2)/2-s.diff(f,r)/r
Q = (1-f-r*s.diff(f,r))/r**2
for i in range(4):
    for j in range(4):
        zero(f'4D_Ric_component_{i}{j}', primary[i,j]-(P if i<2 else Q) if i==j else primary[i,j])
R = s.simplify(scalar.subs(atN1))
zero('primary_scalar',R-(2*P+2*Q))
zero('primary_determinant',g.det().subs(N,1)+r**4*s.sin(th)**2)

p, q, z = [s.Function(v)(r) for v in ['p','q','z']]
gp=g.subs(N,1)
gip=gi.subs(N,1)
Ec=s.diag(*[gp[i,i]*[p,q,z,z][i] for i in range(4)])
gvar=s.diag(-1/(f*s.exp(eps)),f*s.exp(eps),1/r**2,1/(r*r*s.sin(th)**2))
pairing=sum(Ec[i,j]*s.diff(gvar[i,j],eps).subs(eps,0) for i in range(4) for j in range(4))
zero('profile_covector_pairing',pairing-(q-p))

u,v,w=s.symbols('u v w')
gv=s.diag(gp[0,0]*s.exp(eps*u),gp[1,1]*s.exp(eps*v),gp[2,2]*s.exp(eps*w),gp[3,3]*s.exp(eps*w))
pair_cov=sum(gip[i,i]**2*Ec[i,i]*s.diff(gv[i,i],eps).subs(eps,0) for i in range(4))
zero('general_diagonal_pairing',pair_cov-(p*u+q*v+2*z*w))
directions=s.Matrix([[1,-1,0],[1,1,-1],[1,1,1]])
response_map=directions*s.diag(1,1,2)
true('full_diagonal_rank_three',response_map.rank()==3)
true('shape_rank_two',response_map[:2,:].rank()==2)
true('shape_annihilator_pure_trace',response_map[:2,:].nullspace()==[s.Matrix([1,1,1])])
zero('shape_trace_zero',sum(directions[1,j]*[1,1,2][j] for j in range(3)))

GammaP=[[[s.simplify(e.subs(atN1)) for e in row] for row in part] for part in Gamma]
divr=s.simplify(sum(gip[i,i]*(s.diff(Ec[i,1],x[i])-
           sum(GammaP[l][i][i]*Ec[l,1]+GammaP[l][i][1]*Ec[i,l] for l in range(4))) for i in range(4)))
zero('direct_full_divergence_formula',divr-(s.diff(q,r)+s.diff(f,r)*(q-p)/(2*f)+2*(q-z)/r))
replace={p:a*P+b*R,q:a*P+b*R,z:a*Q+b*R}
zero('G301_full_divergence',divr.subs(replace).doit()-(a/s.Integer(2)+b)*s.diff(R,r))
zero('G301_profile_projection',pairing.subs(replace))
zero('G301_second_shape', (p+q-2*z).subs(replace)-a*(-s.diff(f,r,2)+2*(f-1)/r**2))
zero('DDR_known_family',(-s.diff(f,r,2)+2*(f-1)/r**2).subs(f,1+c1*r**2+c2/r).doit())
zero('DDR_constant_scalar',R.subs(f,1+c1*r**2+c2/r).doit()+12*c1)
zero('nonidentity_control_P',P.subs(f,1+k*r**4).doit()+10*k*r**2)
zero('nonidentity_control_Q',Q.subs(f,1+k*r**4).doit()+5*k*r**2)
zero('nonidentity_control_Rprime',s.diff(R,r).subs(f,1+k*r**4).doit()+60*k*r)
true('nonidentity_control_shape_catch',s.simplify((P-Q).subs(f,1+r**4).doit())!=0)
true('divergence_rejects_wrong_coefficient',s.simplify(divr.subs(replace).subs({a:1,b:0,f:1+r**4}).doit())!=0)
zero('scalar_only_shape_degeneracy',(p+q-2*z).subs(replace).subs(a,0))

Rf=-s.diff(f,r,2)-4*s.diff(f,r)/r+2*(1-f)/r**2
zero('general_lapse_curvature',scalar-(Rf-2*f*s.diff(N,r,2)/N-(3*s.diff(f,r)+4*f/r)*s.diff(N,r)/N))
zero('Hilbert_primary_total_derivative',r**2*R-s.diff(-r**2*s.diff(f,r)-2*r*(f-1),r))
L=s.expand(N*r**2*(a*scalar-2*d))
B=-a*N*r**2*s.diff(f,r)-2*a*r**2*f*s.diff(N,r)
L1=2*a*N*(1-f-r*s.diff(f,r))-2*d*N*r**2
zero('Hilbert_lapse_boundary_decomposition',L-L1-s.diff(B,r))

def el(expr,y):
    return s.simplify(s.diff(expr,y)-s.diff(s.diff(expr,s.diff(y,r)),r)+s.diff(s.diff(expr,s.diff(y,r,2)),r,2))

zero('primary_Hilbert_EL_identity',el((a*R-2*d)*r**2,f))
zero('full_lapse_EL_N',el(L,N)-(2*a*(1-f-r*s.diff(f,r))-2*d*r**2))
zero('full_lapse_EL_f',el(L,f)-2*a*r*s.diff(N,r))
zero('lapse_EL_recovers_full_clock',el(L,N).subs(atN1)+2*r**2*(a*(P-R/2)+d))
true('lapse_constraint_not_identity',s.simplify(el(L,N).subs({a:1,d:0,f:1+r**4}).doit())!=0)
zero('fixed_trace_solution',el(L,N).subs(f,1-d*r**2/(3*a)+c2/r).doit())
true('constant_volume_term_hidden_control',el((a*R-2*d)*r**2,f)==0 and s.simplify(el(L,N).subs(a,0))==-2*d*r**2)
true('angular_omission_catch',s.simplify(R-2*P)!=0)

print(json.dumps({'status':'PASS','checks':checks,'count':len(checks),'python':platform.python_version(),'sympy':s.__version__,'elapsed_s':time.monotonic()-started,'method':'Direct full 4D metric connection and Ricci; no parent imports; exact symbolic arithmetic','expressions':{'primary_R':str(R),'general_lapse_R':str(scalar),'divergence':str(divr),'lapse_EL_N':str(el(L,N)),'lapse_EL_f':str(el(L,f))}},indent=2))
