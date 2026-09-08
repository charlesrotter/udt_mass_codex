"""Independent original coordinate-Ricci check; stdlib exact rational 2-jets.

Constructed from source-first requirements without candidate/code exposure.
Only examples/regressions; universal statements are reviewed analytically.
"""
from fractions import Fraction as Q
import json
import platform

N = 4
SIGN = (-1, 1, 1, 1)  # Declared Lorentzian coordinate convention; not physics.

def zeros(shape):
    return Q(0) if not shape else [zeros(shape[1:]) for _ in range(shape[0])]


class Jet:
    def __init__(self, value, grad=None, hess=None):
        self.v = Q(value)
        self.d = [Q(x) for x in grad] if grad is not None else zeros((N,))
        self.h = [[Q(x) for x in row] for row in hess] if hess is not None else zeros((N, N))

    def power(self, exponent):
        n, v = exponent, self.v
        return Jet(v**n, [n*v**(n-1)*x for x in self.d],
                   [[n*v**(n-1)*self.h[i][j] + n*(n-1)*v**(n-2)*self.d[i]*self.d[j]
                     for j in range(N)] for i in range(N)])

    def times(self, other):
        return Jet(self.v*other.v,
                   [self.d[i]*other.v+self.v*other.d[i] for i in range(N)],
                   [[self.h[i][j]*other.v+self.d[i]*other.d[j]+self.d[j]*other.d[i]
                     + self.v*other.h[i][j] for j in range(N)] for i in range(N)])


def conformal_diagonal(s):
    f = s.power(-2)
    g, dg, ddg = zeros((N,N)), zeros((N,N,N)), zeros((N,N,N,N))
    for a in range(N):
        g[a][a] = SIGN[a]*f.v
        for i in range(N):
            dg[i][a][a] = SIGN[a]*f.d[i]
            for j in range(N):
                ddg[i][j][a][a] = SIGN[a]*f.h[i][j]
    return g, dg, ddg


def geometry(g, dg, ddg):
    # The fixtures are diagonal only; the Christoffel and Ricci loops are general.
    inv = zeros((N,N))
    for a in range(N):
        assert g[a][a] != 0 and all(g[a][b] == 0 for b in range(N) if b != a)
        inv[a][a] = 1/g[a][a]
    dinv = zeros((N,N,N))
    for i in range(N):
        for a in range(N):
            for b in range(N):
                dinv[i][a][b] = -sum(inv[a][c]*dg[i][c][d]*inv[d][b]
                                      for c in range(N) for d in range(N))
    gamma, dgamma = zeros((N,N,N)), zeros((N,N,N,N))
    for a in range(N):
        for b in range(N):
            for c in range(N):
                gamma[a][b][c] = sum(inv[a][d]*(dg[b][d][c]+dg[c][d][b]-dg[d][b][c])/2
                                      for d in range(N))
                for i in range(N):
                    dgamma[i][a][b][c] = sum(
                        (dinv[i][a][d]*(dg[b][d][c]+dg[c][d][b]-dg[d][b][c])
                         + inv[a][d]*(ddg[i][b][d][c]+ddg[i][c][d][b]-ddg[i][d][b][c]))/2
                        for d in range(N))
    ric = zeros((N,N))
    for b in range(N):
        for d in range(N):
            ric[b][d] = sum(dgamma[a][a][d][b]-dgamma[d][a][a][b]
                           + sum(gamma[a][a][c]*gamma[c][d][b]
                                 - gamma[a][d][c]*gamma[c][a][b] for c in range(N))
                           for a in range(N))
    scalar = sum(inv[a][b]*ric[a][b] for a in range(N) for b in range(N))
    tf = [[ric[a][b]-scalar*g[a][b]/4 for b in range(N)] for a in range(N)]
    return dict(g=g, inv=inv, gamma=gamma, ric=ric, scalar=scalar, tf=tf)


def residual(geom, lam):
    return [[geom['ric'][a][b]-lam*geom['g'][a][b] for b in range(N)] for a in range(N)]


def allzero(array):
    return all(allzero(x) for x in array) if isinstance(array, list) else array == 0


def qform(c, b, a, x):
    value = Q(c)+sum(Q(b[i])*x[i] for i in range(N))+Q(a,2)*sum(SIGN[i]*x[i]**2 for i in range(N))
    grad = [Q(b[i])+a*SIGN[i]*x[i] for i in range(N)]
    hess = [[Q(a*SIGN[i]) if i == j else Q(0) for j in range(N)] for i in range(N)]
    return Jet(value, grad, hess)


results = []
fixtures = [
    ('constant', 2, (0,0,0,0), 0),
    ('timelike_affine', 3, (1,0,0,0), 0),
    ('spacelike_affine', 3, (0,1,0,0), 0),
    ('null_affine', 3, (1,1,0,0), 0),
    ('full_quadratic', 3, (1,2,-1,1), 2),
]
points = [(Q(0),)*4, (Q(1,5),Q(-1,7),Q(2,9),Q(1,6))]
for name,c,b,a in fixtures:
    lam = 6*a*c-3*sum(SIGN[i]*b[i]**2 for i in range(N))
    for x in points:
        s = qform(c,b,a,x)
        assert s.v > 0
        geom = geometry(*conformal_diagonal(s))
        assert allzero(residual(geom,lam)), (name, 'original Ricci residual')
        assert geom['scalar'] == 4*lam
        results.append(dict(case=name, point=[str(z) for z in x], inverse_factor=str(s.v),
                            lambda_hat=str(lam), original_ricci_residual='EXACT_ZERO'))

# A positive metric can satisfy the trace-free equation but have nonzero Ricci.
assert any(item['lambda_hat'] != '0' for item in results)

# Reject a full nonlinear claim that discards the gradient-norm term.
wrong_lam = 0
timelike = geometry(*conformal_diagonal(qform(3,(1,0,0,0),0,points[0])))
wrong_scalar_detected = not allzero(residual(timelike,wrong_lam))
assert wrong_scalar_detected

# Reintroduce an off-equation factor that agrees with a constant through first order.
bad_hess = zeros((N,N)); bad_hess[1][1] = Q(2)
bad = geometry(*conformal_diagonal(Jet(1,hess=bad_hess)))
bad_factor_detected = not allzero(bad['tf'])
assert bad_factor_detected

# A conformally flat nonflat Einstein BASE, s0=t, with sigma=s/s0.
# Reconstruct both Ricci tensors directly; only then compare the claimed general law.
x = (Q(2),Q(1,3),Q(1,4),Q(-1,5))
base_s = Jet(x[0], (1,0,0,0))
target_s = qform(3,(1,2,-1,1),2,x)
assert target_s.v > 0
base, target = geometry(*conformal_diagonal(base_s)), geometry(*conformal_diagonal(target_s))
assert allzero(residual(base,Q(3)))
sigma = target_s.times(base_s.power(-1))
hess = [[sigma.h[a][b]-sum(base['gamma'][c][a][b]*sigma.d[c] for c in range(N))
         for b in range(N)] for a in range(N)]
box = sum(base['inv'][a][b]*hess[a][b] for a in range(N) for b in range(N))
norm = sum(base['inv'][a][b]*sigma.d[a]*sigma.d[b] for a in range(N) for b in range(N))
transformed = [[base['ric'][a][b]+2*hess[a][b]/sigma.v
                +(box/sigma.v-3*norm/sigma.v**2)*base['g'][a][b]
                for b in range(N)] for a in range(N)]
assert transformed == target['ric']
assert all(hess[a][b] == (box/4)*base['g'][a][b] for a in range(N) for b in range(N))
target_lambda = target['scalar']/4
assert target_lambda == 3*sigma.v**2+6*sigma.v*(box/4)-3*norm

print(json.dumps(dict(status='PASS_EXACT_EXAMPLES_AND_HOSTILE_CONTROLS',
    python=platform.python_version(), arithmetic='stdlib fractions.Fraction',
    base_dimension=N, examples=results,
    hostile=dict(gradient_term_omission_detected=wrong_scalar_detected,
                 non_Einstein_positive_profile_detected=bad_factor_detected,
                 bad_factor_tracefree=[[str(z) for z in row] for row in bad['tf']]),
    nonflat_base=dict(lambda_base='3', lambda_target=str(target_lambda),
                      original_transformation_residual='EXACT_ZERO'),
    ceiling='Finite original-equation examples and guards; not a general proof'), indent=2))
