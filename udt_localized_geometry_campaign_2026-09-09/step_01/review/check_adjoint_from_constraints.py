"""Recover the flat constant-K full linear momentum constraint from index calculus.

Independent formula construction: vary the mixed-index divergence and trace,
then integrate the resulting differential polynomial by parts formally.
"""
import json
import sympy as s

T = s.Symbol('T', positive=True)
ks = [1/(3*T),-2/(3*T),-2/(3*T)]
tau = sum(ks)
pairs = [(i,j) for i in range(3) for j in range(i,3)]
def symmetric(prefix):
    d = {(i,j):s.Symbol(f'{prefix}_{i}{j}') for i,j in pairs}
    return s.Matrix(3,3,lambda i,j:d[tuple(sorted((i,j)))])
h, q = symmetric('h'), symmetric('q')
dh, dq = [symmetric(f'dh{a}') for a in range(3)], [symmetric(f'dq{a}') for a in range(3)]
Y = s.symbols('Y0:3')
dY = s.Matrix(3,3,lambda a,i:s.Symbol(f'dY{a}_{i}'))
N = s.Symbol('N')
dGamma = [[[s.Rational(1,2)*(dh[j][i,m]+dh[m][i,j]-dh[i][j,m])
            for m in range(3)] for j in range(3)] for i in range(3)]
# delta[D_j K^j_i - D_i tr(K)] using K^j_i variation q_ji-k_i h_ji.
M = []
for i in range(3):
    mixed_div = sum(dq[j][j,i]-ks[i]*dh[j][j,i] for j in range(3))
    connection = sum((ks[i]-ks[j])*dGamma[j][j][i] for j in range(3))
    dtrace = sum(dq[i][j,j]-ks[j]*dh[i][j,j] for j in range(3))
    M.append(s.expand(mixed_div+connection-dtrace))
    closed = sum(dq[j][i,j] for j in range(3))-sum(dq[i][j,j] for j in range(3))
    closed += -ks[i]*sum(dh[j][i,j] for j in range(3))
    closed += sum((ks[i]+ks[j])*dh[i][j,j]/2 for j in range(3))
    assert s.expand(M[i]-closed)==0

integrand = s.expand(sum(-2*Y[i]*M[i] for i in range(3)))
adjh, adjq = s.zeros(3), s.zeros(3)
for i,j in pairs:
    ah = aq = 0
    for a in range(3):
        ch, cq = s.diff(integrand,dh[a][i,j]), s.diff(integrand,dq[a][i,j])
        ah -= sum(s.diff(ch,Y[b])*dY[a,b] for b in range(3))
        aq -= sum(s.diff(cq,Y[b])*dY[a,b] for b in range(3))
    # Symmetric tensor contraction has two copies of each off-diagonal slot.
    weight = 1 if i==j else 2
    adjh[i,j]=adjh[j,i]=s.expand(ah/weight)
    adjq[i,j]=adjq[j,i]=s.expand(aq/weight)
divY = s.trace(dY)
expected_q = s.Matrix(3,3,lambda i,j:dY[i,j]+dY[j,i]-(2*divY if i==j else 0))
expected_h = s.Matrix(3,3,lambda i,j:-ks[i]*dY[j,i]-ks[j]*dY[i,j]
                     +(sum((ks[i]+ks[a])*dY[a,a] for a in range(3)) if i==j else 0))
assert (adjq-expected_q).applyfunc(s.simplify)==s.zeros(3)
assert (adjh-expected_h).applyfunc(s.simplify)==s.zeros(3)

# Hamiltonian K-sector is differentiated directly from inverse metric series.
eps = s.Symbol('eps')
K = s.diag(*ks)
kinv = (s.eye(3)-eps*h)*(K+eps*q)
quadratic = s.trace(kinv)**2-s.trace(kinv*kinv)
deltaH_K = s.expand(s.diff(quadratic,eps).subs(eps,0))
expected_H_K = 2*sum((ks[i]**2-tau*ks[i])*h[i,i]+(tau-ks[i])*q[i,i] for i in range(3))
assert s.expand(deltaH_K-expected_H_K)==0
assert s.diff(deltaH_K,h[0,0]) != 0
print(json.dumps({'status':'PASS_EXACT_SYMBOLIC_SCOPED','sympy':s.__version__,
                  'checks':['All three mixed-index momentum variations agree',
                            'Six metric adjoint coefficients agree',
                            'Six K adjoint coefficients agree',
                            'Hamiltonian inverse-metric/trace variation agrees'],
                  'zero_residuals':18,
                  'limitations':['Flat constant-K background only',
                                 'Scalar-curvature adjoint uses the analytic Hessian-minus-trace identity',
                                 'No nonlinear solve or gluing theorem']},indent=2))
