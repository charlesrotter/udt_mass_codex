"""Exact, bounded author checks; independent review is a separate artifact."""
import json
import platform
import sympy as s

T = s.symbols('T', positive=True)
coords = (T, *s.symbols('X y z'))
g = s.diag(-1, T**(-s.Rational(2, 3)), T**s.Rational(4, 3), T**s.Rational(4, 3))
gi = g.inv()
C = [[[s.simplify(sum(gi[i, l]*(s.diff(g[l, k], coords[j]) + s.diff(g[l, j], coords[k]) - s.diff(g[j, k], coords[l])) for l in range(4))/2) for k in range(4)] for j in range(4)] for i in range(4)]
R = [[[[s.simplify(s.diff(C[i][j][l], coords[k])-s.diff(C[i][j][k], coords[l])+sum(C[i][m][k]*C[m][j][l]-C[i][m][l]*C[m][j][k] for m in range(4))) for l in range(4)] for k in range(4)] for j in range(4)] for i in range(4)]
ric = s.Matrix(4, 4, lambda j,l: s.simplify(sum(R[i][j][i][l] for i in range(4))))
kretsch = s.simplify(sum(g[i,i]**2*gi[i,i]*gi[j,j]*gi[k,k]*gi[l,l]*R[i][j][k][l]**2 for i in range(4) for j in range(4) for k in range(4) for l in range(4)))
assert ric == s.zeros(4)
assert s.simplify(kretsch-64/(27*T**4)) == 0
assert s.diff(kretsch,T) == -s.Rational(256,27)/T**5
a = s.symbols('a', positive=True)
K = s.diag(a,-2*a,-2*a)
tau = s.trace(K)
rxy,rxz,ryz = s.symbols('rxy rxz ryz')
A = s.Matrix([[0,-rxy,-rxz],[rxy,0,-ryz],[rxz,ryz,0]])
comm = K*A-A*K
sol = s.linsolve(list(comm), (rxy,rxz,ryz))
assert sol == s.FiniteSet((0,0,ryz))

# Density variation in arbitrary symmetric h and q=dK (six independent entries).
h = s.Matrix([[2,3,5],[3,7,11],[5,11,13]])
q = s.Matrix([[17,19,23],[19,29,31],[23,31,37]])
# Recompute by formal first-order inverse/determinant contractions rather than
# importing campaign formulas or any predecessor's implementation.
eps=s.symbols('eps')
iv=s.eye(3)-eps*h
tau_eps=s.trace(iv*(K+eps*q))
pi_eps=(1+eps*s.trace(h)/2)*(iv*(K+eps*q)*iv-tau_eps*iv)
v=pi_eps.diff(eps).subs(eps,0)
expected=q-h*K-K*h-(s.trace(q)-s.trace(h*K))*s.eye(3)+tau*h+s.trace(h)*(K-tau*s.eye(3))/2
assert s.simplify(v-expected)==s.zeros(3)
assert v != q

# Deliberate invalid-data false-pass control: all finite charges zero if h=0.
b=s.symbols('b', real=True)
badK=K+eps*b*s.eye(3)
badH=s.expand(s.trace(badK)**2-s.trace(badK*badK))
assert badH == -12*a*b*eps+6*b*b*eps*eps
assert badH.subs({a:1,b:1,eps:s.Rational(1,10)}) != 0
assert not (K*s.Matrix([[0,-1,0],[1,0,0],[0,0,0]])-s.Matrix([[0,-1,0],[1,0,0],[0,0,0]])*K).is_zero_matrix
print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,'status':'PASS',
 'kind':'exact symbolic author checks; not independent proof review',
 'Ricci_zero':True,'Kretschmann':str(kretsch),'Kretschmann_derivative':str(s.diff(kretsch,T)),
 'rotation_solution':str(sol),'density_variation_checked':True,
 'invalid_data_charge_false_pass_exposed':str(badH),
 'omissions':['no numerical constraint solver','no sufficiency theorem','no full365 pass']},indent=2))
