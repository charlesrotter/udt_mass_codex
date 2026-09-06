"""Independent exact 4D coordinate reconstruction; no candidate imports or reads."""
import datetime
import itertools
import json
import platform
import time
import sympy as s

started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t0 = time.monotonic()
u, v, x, y, A = s.symbols('u v x y A', real=True)
coords = (u, v, x, y)
n = range(4)
tuples = list(itertools.product(n, repeat=4))
g = s.Matrix([[A*(x*x-y*y), -1, 0, 0], [-1, 0, 0, 0],
              [0, 0, 1, 0], [0, 0, 0, 1]])
gi = g.inv()
Gamma = {(a,b,c): s.simplify(sum(gi[a,d]*(s.diff(g[d,c],coords[b])
          +s.diff(g[d,b],coords[c])-s.diff(g[b,c],coords[d]))/2 for d in n))
         for a,b,c in itertools.product(n, repeat=3)}
Rup = {(a,b,c,d): s.simplify(s.diff(Gamma[a,d,b],coords[c])
        -s.diff(Gamma[a,c,b],coords[d])
        +sum(Gamma[a,c,e]*Gamma[e,d,b]-Gamma[a,d,e]*Gamma[e,c,b] for e in n))
       for a,b,c,d in tuples}
Ric = s.Matrix(4,4,lambda b,d: s.simplify(sum(Rup[a,b,a,d] for a in n)))
scalar = s.simplify(sum(gi[a,b]*Ric[a,b] for a in n for b in n))
R = {(a,b,c,d): s.simplify(sum(g[a,e]*Rup[e,b,c,d] for e in n))
     for a,b,c,d in tuples}
W = {(a,b,c,d): s.simplify(R[a,b,c,d] - (g[a,c]*Ric[d,b]-g[a,d]*Ric[c,b]
      -g[b,c]*Ric[d,a]+g[b,d]*Ric[c,a])/2
      +scalar*(g[a,c]*g[d,b]-g[a,d]*g[c,b])/6)
     for a,b,c,d in tuples}
eps = lambda a,b,c,d: s.LeviCivita(a,b,c,d)*s.sqrt(-g.det())
star = {(a,b,c,d): s.simplify(sum(eps(a,b,r,t)*gi[r,m]*gi[t,k]*W[m,k,c,d]/2
         for r,t,m,k in tuples)) for a,b,c,d in tuples}
gterms = [(e,f,gi[e,f]) for e in n for f in n if gi[e,f] != 0]
def contraction(T):
    return {(a,b,c,d): s.simplify(sum(ief*ihi*T[a,e,c,h]*T[b,f,d,i]
            for e,f,ief in gterms for h,i,ihi in gterms)) for a,b,c,d in tuples}
plain, dual = contraction(W), contraction(star)
B = {t: s.simplify(plain[t]+dual[t]) for t in tuples}
expected = {t: 4*A*A if t == (0,0,0,0) else s.S.Zero for t in tuples}
assert Ric == s.zeros(4)
assert scalar == 0 and g.det() == -1
assert all(s.simplify(B[t]-expected[t]) == 0 for t in tuples)
assert plain[0,0,0,0] == dual[0,0,0,0] == 2*A*A
assert all(B[t].subs(A,0) == 0 for t in tuples)
assert all(Gamma[0,a,b] == 0 for a in n for b in n)
q = s.symbols('q', positive=True)
beta = s.Matrix([-q,0,0,0])
C = gi*beta
d_beta = {(a,b): s.simplify(s.diff(beta[b],coords[a])-s.diff(beta[a],coords[b]))
          for a in n for b in n}
divC = s.simplify(sum(s.diff(C[a],coords[a]) for a in n)
        +sum(Gamma[a,a,b]*C[b] for a in n for b in n))
bad_beta = (1+v)*beta
bad_C = gi*bad_beta
bad_exterior_uv = s.diff(bad_beta[1],u)-s.diff(bad_beta[0],v)
bad_div = s.simplify(sum(s.diff(bad_C[a],coords[a]) for a in n)
          +sum(Gamma[a,a,b]*bad_C[b] for a in n for b in n))
assert all(value == 0 for value in d_beta.values()) and divC == 0
assert (beta.T*gi*beta)[0] == 0 and C == s.Matrix([0,q,0,0])
assert bad_exterior_uv == q and bad_div == q
# Arbitrary nonconstant v=f(x,y) cut in a fixed-u phase sheet.
fx,fy = s.symbols('fx fy', real=True)
E = s.Matrix([[0,0],[fx,fy],[1,0],[0,1]])
assert E.T*g*E == s.eye(2)
# Three-form contraction checked componentwise.
J = {(a,b,c): s.simplify(sum(C[d]*eps(d,a,b,c) for d in n))
     for a,b,c in itertools.product(n, repeat=3)}
assert J[0,2,3] == -q
# Passive positive null coordinate scaling with its complete tensor Jacobian.
a_scale, h_scale = s.symbols('a_scale h_scale', positive=True)
Jac = s.diag(1/a_scale,a_scale,1,1)
gprime = (Jac.T*g*Jac).subs({u:u/a_scale,v:a_scale*v})
assert gprime[0,0] == A*(x*x-y*y)/a_scale**2
assert Jac.T*beta == s.Matrix([-q/a_scale,0,0,0])
assert Jac.inv()*C == s.Matrix([0,q/a_scale,0,0])
# Exact contractions distinguish recipe factor and orientation controls.
star_reversed = {t:-star[t] for t in tuples}
rev_dual = contraction(star_reversed)
wrong_half_dual = contraction({t:2*star[t] for t in tuples})
assert all(plain[t]+rev_dual[t] == B[t] for t in tuples)
assert plain[0,0,0,0]+wrong_half_dual[0,0,0,0] == 10*A*A
report = {
 'started_utc':started, 'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'elapsed_seconds':time.monotonic()-t0,'python':platform.python_version(),'sympy':s.__version__,
 'domain':'all real constant A; exact symbolic full 4D tensors; q>0 for root identities',
 'metric_det':str(g.det()), 'ricci':str(Ric), 'scalar':str(scalar),
 'weyl_nonzero':{str(t):str(W[t]) for t in tuples if W[t] != 0},
 'first_pair_dual_nonzero':{str(t):str(star[t]) for t in tuples if star[t] != 0},
 'B_nonzero':{str(t):str(B[t]) for t in tuples if B[t] != 0},
 'plain_uuuu':str(plain[0,0,0,0]),'dual_uuuu':str(dual[0,0,0,0]),
 'full_tensor_expected_identity':True, 'flat_all_B_zero':True,
 'beta_components':str(beta),'C_components':str(C),'divC':str(divC),
 'd_beta_all_zero':True, 'bad_d_beta_uv':str(bad_exterior_uv),'bad_divC':str(bad_div),
 'arbitrary_cut_gram':str(E.T*g*E),'J_uxy':str(J[0,2,3]),
 'positive_null_coordinate_covariance':True,'orientation_reversal_B_unchanged':True,
 'omitted_Hodge_half_yields_Buuuu':str(plain[0,0,0,0]+wrong_half_dual[0,0,0,0]),
 'no_candidate_code_imports_or_outputs_read':True,
}
print(json.dumps(report,indent=2,sort_keys=True))
