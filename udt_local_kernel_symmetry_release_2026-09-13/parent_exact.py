"""Original Cartesian metric second-jet checks; analytical proof is separate."""
import json, platform, sys
import sympy as sp

x = sp.Matrix(sp.symbols('x y z', real=True))
c, a, b, d, e, h = sp.symbols('c a b d e h', real=True)
S = sp.Matrix([[a,d,e],[d,b,h],[e,h,-a-b]])
C = sp.Matrix([[0,-x[2],x[1]],[x[2],0,-x[0]],[-x[1],x[0],0]])
D = C.T*S*C
r2 = (x.T*x)[0]
eta = sp.diag(-1,1,1,1)
coords = [sp.Symbol('t',real=True),*x]
metric = sp.diag(-1-c*r2,1,1,1)
metric[1:4,1:4] = sp.eye(3)-c*x*x.T+D
origin = dict.fromkeys(coords,0)
checks = []
def zero(label, expr):
    entries = list(expr) if isinstance(expr,sp.MatrixBase) else [expr]
    residuals = [sp.factor(v) for v in entries]
    if any(v != 0 for v in residuals):
        raise AssertionError((label,[str(v) for v in residuals]))
    checks.append(label)
zero('metric_calibration',metric.subs(origin)-eta)
for k in coords:
    zero('first_derivative_'+str(k),metric.diff(k).subs(origin))
zero('D_radial_annihilation',D*x)
zero('D_trace',sp.trace(D)+(x.T*S*x)[0])
zero('tangent_determinant', (sp.eye(3)+D).det()-(1-(x.T*S*x)[0]+r2*(x.T*S.adjugate()*x)[0]))

# At the verified zero-connection point this follows directly from the declared
# Levi-Civita/Riemann convention, before any claimed tensor coefficient is used.
g2 = {(i,j,k,l):sp.diff(metric[i,j],coords[k],coords[l]).subs(origin)
      for i in range(4) for j in range(4) for k in range(4) for l in range(4)}
R = {(i,j,k,l):sp.expand((g2[i,l,j,k]+g2[j,k,i,l]-g2[i,k,j,l]-g2[j,l,i,k])/2)
     for i in range(4) for j in range(4) for k in range(4) for l in range(4)}
for i in range(4):
 for j in range(4):
  for k in range(4):
   for l in range(4):
    target = -c*(eta[i,k]*eta[j,l]-eta[i,l]*eta[j,k])
    if min(i,j,k,l)>0:
     target -= 3*sum(sp.LeviCivita(i-1,j-1,p)*sp.LeviCivita(k-1,l-1,q)*S[p,q]
                     for p in range(3) for q in range(3))
    zero('R_'+str((i,j,k,l)),R[i,j,k,l]-target)
Ric = sp.Matrix(4,4,lambda j,l:sum(eta[i,i]*R[i,j,i,l] for i in range(4)))
Ric_target = sp.diag(3*c,-3*c,-3*c,-3*c)
Ric_target[1:4,1:4] += 3*S
zero('Ricci',Ric-Ric_target)
scalar = sp.trace(eta*Ric)
zero('scalar',scalar+12*c)
W = {(i,j,k,l):sp.expand(R[i,j,k,l]-(eta[i,k]*Ric[j,l]-eta[i,l]*Ric[j,k]
                  -eta[j,k]*Ric[i,l]+eta[j,l]*Ric[i,k])/2
                  +scalar*(eta[i,k]*eta[j,l]-eta[i,l]*eta[j,k])/6)
     for i,j,k,l in R}
def norm4(tensor):
 return sp.expand(sum(eta[i,i]*eta[j,j]*eta[k,k]*eta[l,l]*v*v
                      for (i,j,k,l),v in tensor.items()))
trS2 = sp.trace(S*S)
zero('Riemann_squared',norm4(R)-24*c*c-36*trS2)
zero('Ricci_squared',sum(eta[i,i]*eta[j,j]*Ric[i,j]**2 for i in range(4) for j in range(4))-36*c*c-9*trS2)
zero('Weyl_squared',norm4(W)-18*trS2)
for i in range(3):
 for j in range(3): zero('Weyl_electric_'+str((i,j)),W[0,i+1,0,j+1]-sp.Rational(3,2)*S[i,j])

n = sp.Matrix(sp.symbols('n1 n2 n3',real=True))
v = sp.Matrix(sp.symbols('v1 v2 v3',real=True))
w = sp.Matrix(sp.symbols('w1 w2 w3',real=True))
k4 = [1,*n]; v4=[0,*v]; w4=[0,*w]
tide = sp.expand(sum(v4[i]*k4[j]*w4[k]*k4[l]*R[i,j,k,l] for i,j,k,l in R))
# Identity before imposing unit/null/screen constraints; the c term must be
# retained here rather than incorrectly cancelling for arbitrary input vectors.
target_tide = c*((1-n.dot(n))*v.dot(w)+v.dot(n)*w.dot(n))-3*(v.cross(n).T*S*w.cross(n))[0]
zero('full_screen_polynomial_identity',tide-target_tide)
ss=sp.Symbol('s',real=True)
diag={a:ss,b:2*ss,d:0,e:0,h:0}
screen_entries=[]
for i in [1,2]:
 for j in [1,2]:
  val=sp.expand(R[i,0,j,0]+R[i,3,j,3]+R[i,0,j,3]+R[i,3,j,0]).subs(diag)
  expected={ (1,1):-6*ss,(2,2):-3*ss,(1,2):0,(2,1):0}[i,j]
  zero('signed_witness_'+str((i,j)),val-expected)
  screen_entries.append(str(val))

def sphere_average(poly):
    total=0
    for powers,coef in sp.Poly(sp.expand(poly),*x).terms():
        if any(p%2 for p in powers): continue
        m=[p//2 for p in powers]
        total += coef*sp.prod(sp.factorial2(2*t-1) for t in m)/sp.factorial2(2*sum(m)+1)
    return sp.factor(total)
u=(x.T*S*x)[0]; adj=(x.T*S.adjugate()*x)[0]
zero('sphere_first_moment',sphere_average(u))
zero('sphere_adjugate',sphere_average(adj)+trS2/6)
zero('sphere_second_moment',sphere_average(u*u)-2*trS2/15)
m4=sp.factor(sphere_average(adj)/2-sphere_average(u*u)/8)
zero('area_normalization_coefficient',m4+trS2/10)

f=1+c*r2; q=sp.Symbol('q',positive=True)
gamma=x*x.T/(r2*f)+q*(sp.eye(3)-x*x.T/r2+D)
zero('exact_radial_metric',gamma*x-x/f)
zero('spherical_source_recovery',gamma.subs({a:0,b:0,d:0,e:0,h:0,q:1})-(sp.eye(3)-c*x*x.T/f))
gamma2=sp.eye(3)-c*x*x.T+D
rho2=sp.expand((v.T*gamma2*v)[0]+c*r2*v.dot(v))
zero('directional_density_second_jet',rho2-(v.dot(v)+c*(r2*v.dot(v)-(x.dot(v))**2)+(v.T*D*v)[0]))

# Recompute erroneous hypotheses against the original metric outputs. These are
# hostile checks, not additional independent derivations.
hostile={
 'omit_D_predicts_quiet': sp.expand(R[1,3,1,3]+R[1,0,1,0]).subs(diag).subs(ss,1)!=0,
 'reverse_D_tide_sign': sp.expand(R[1,3,1,3]+R[1,0,1,0]).subs(diag).subs(ss,1)!=6,
 'omit_q_area_correction':m4.subs(diag).subs(ss,1)!=0,
 'normalized_only_erases_density':sp.expand((x.T*D*x)[0])==0 and D[2,2].subs(diag).subs({x[0]:sp.Rational(1,10),x[1]:0,x[2]:0,ss:1})!=0,
 'raw_scaled_order_confusion':sp.expand((R[1,3,1,3]+R[1,0,1,0]).subs(diag)*sp.Symbol('r')**2).coeff(sp.Symbol('r'),2)!=0,
}
assert all(hostile.values()),hostile
result={'status':'PASS','python':platform.python_version(),'sympy':sp.__version__,
 'argv':sys.argv,'checks':checks,'check_count':len(checks),'hostile_recomputations':hostile,
 'signed_witness_screen':screen_entries,'trace_S_squared':str(trS2),
 'sphere_M_r4':str(m4),'R_scalar':str(scalar),'Weyl_squared':str(sp.factor(norm4(W))),
 'epistemic_scope':'exact symbolic identities from original Cartesian second jet; analytical full-metric existence proof separate; not native admission'}
print(json.dumps(result,indent=2))
