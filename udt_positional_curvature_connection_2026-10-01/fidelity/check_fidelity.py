"""Independent source-first exact controls; not a field-equation solver."""
from pathlib import Path
import json, platform
import sympy as s

checks = []
def check(name, expr):
    residual = s.simplify(s.trigsimp(expr))
    checks.append({'name': name, 'residual': str(residual), 'pass': residual == 0})
    if residual != 0:
        raise AssertionError((name, residual))

# FREE supplied family/reference/matching; symbolic choices are not UDT premises.
t, r, th, ph = s.symbols('t r theta phi', real=True)
m, k, b, L = s.symbols('m k b L', real=True)
x = [t, r, th, ph]
f = 1 - 2*m/r - k*r*r
metric = s.diag(-f, 1/f, r*r, r*r*s.sin(th)**2)
inv = metric.inv()
Gamma = [[[s.simplify(sum(inv[a,d]*(s.diff(metric[d,c],x[q])+s.diff(metric[d,q],x[c])-s.diff(metric[q,c],x[d])) for d in range(4))/2) for c in range(4)] for q in range(4)] for a in range(4)]
# R^a_{c i j}: R(partial_i,partial_j)partial_c.
def R_up(a,c,i,j):
    return s.simplify(s.diff(Gamma[a][j][c],x[i])-s.diff(Gamma[a][i][c],x[j])+sum(Gamma[a][i][z]*Gamma[z][j][c]-Gamma[a][j][z]*Gamma[z][i][c] for z in range(4)))
frame = [1/s.sqrt(f), s.sqrt(f), 1/r, 1/(r*s.sin(th))]
eta = [-1,1,1,1]
R = {}
for i in range(4):
    for j in range(4):
        for c in range(4):
            for d in range(4):
                R[i,j,c,d] = s.simplify(metric[d,d]*R_up(d,c,i,j)*frame[i]*frame[j]*frame[c]*frame[d])
                G = (eta[j]*eta[i] if j==c and i==d else 0) - (eta[i]*eta[j] if i==c and j==d else 0)
                check(f'original_connection_delta_{i}{j}{c}{d}', R[i,j,c,d]-R[i,j,c,d].subs(k,0)-k*G)
sections = {f'{i}{j}': s.factor(R[i,j,j,i]) for i in range(4) for j in range(i+1,4)}
expected = [-2*m/r**3-k,m/r**3-k,m/r**3-k,-m/r**3+k,-m/r**3+k,2*m/r**3+k]
for (ij,val), want in zip(sections.items(),expected):
    check('section_'+ij,val-want)
check('nonzero_anisotropy', (R[1,0,0,1]-R[2,0,0,2])+3*m/r**3)
# Contractions recomputed from the saved full frame tensor, not an inserted Ricci law.
Ric = s.Matrix(4,4,lambda j,c: s.simplify(sum(eta[i]*R[i,j,c,i] for i in range(4))))
for j in range(4):
    for c in range(4):
        check(f'ricci_{j}{c}', Ric[j,c]-3*k*(eta[j] if j==c else 0))
check('scalar',sum(eta[i]*Ric[i,i] for i in range(4))-12*k)
# One-rest-frame false pass: spatial 12 curvature invisible for e0.
def spatial(a,q,c,d):
    return ((1 if q==c and a==d else 0)-(1 if a==c and q==d else 0)) if all(z in (1,2) for z in (a,q,c,d)) else 0
U=[s.Rational(5,4),s.Rational(3,4),0,0]
def tide(n,u):
    return sum(n[a]*u[q]*u[c]*n[d]*spatial(a,q,c,d) for a in range(4) for q in range(4) for c in range(4) for d in range(4))
check('rest_invisible',tide([0,0,1,0],[1,0,0,0]))
check('boosted_e2',tide([0,0,1,0],U)-s.Rational(9,16))
check('boosted_e3',tide([0,0,0,1],U))
assert tide([0,0,1,0],U)!=tide([0,0,0,1],U)
# Different reference-frame match in anisotropic background changes the comparison.
check('rotation_match_changes_radial_tide', (R[1,0,0,1]-R[2,0,0,2]).subs(k,0)+3*m/r**3)
assert s.simplify((R[1,0,0,1]-R[2,0,0,2]).subs(k,0)) != 0
# Cubic time-dependent scale factor: exact series inversion of conformal incidence.
a=1+b*t**3
eta_t=s.integrate(s.series(1/a,t,0,7).removeO(),t)
tb=L+b*L**4/4
tr=2*L+4*b*L**4
check('outgoing_incidence_to_order6',s.series(eta_t.subs(t,tb)-L,L,0,7).removeO())
check('return_incidence_to_order6',s.series(eta_t.subs(t,tr)-2*L,L,0,7).removeO())
check('curvature_at_origin_time',(-s.diff(a,t,2)/a).subs(t,0))
check('curvature_at_origin_space',(s.diff(a,t)/a).subs(t,0)**2)
p=a.subs(t,tb)
q=a.subs(t,tr)/a.subs(t,tb)
check('cubic_log_p',s.series(s.log(p),L,0,6).removeO()-b*L**3)
check('cubic_log_q',s.series(s.log(q),L,0,6).removeO()-7*b*L**3)
# An explicit common regular point; positivity extends to a neighborhood by continuity.
point={r:s.Integer(10),m:s.Integer(1),k:s.Rational(1,10000)}
assert f.subs(point)==s.Rational(79,100)
assert f.subs(k,0).subs(point)==s.Rational(4,5)
result={'kind':'independent exact finite controls, not general proof',
        'python':platform.python_version(),'sympy':s.__version__,
        'checks':checks,'assertion_count':len(checks)+4,
        'sections':{key:str(v) for key,v in sections.items()},
        'ricci':[[str(Ric[i,j]) for j in range(4)] for i in range(4)],
        'regular_point':{'r':'10','m':'1','k':'1/10000','f':'79/100','f0':'4/5'},
        'cubic_coefficients':{'outgoing':'b','return':'7*b'},
        'status':'PASS'}
out=Path(__file__).with_name('EXACT_CONTROLS.json')
with out.open('x') as fh:
    json.dump(result,fh,indent=2);fh.write('\n')
print(json.dumps({'status':result['status'],'assertion_count':result['assertion_count'],'sections':result['sections'],'python':result['python'],'sympy':result['sympy']}))
