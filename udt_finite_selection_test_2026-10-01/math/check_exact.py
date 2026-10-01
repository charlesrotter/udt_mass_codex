"""Independent exact algebra anchors for FST1; no scientific source code imported."""
from fractions import Fraction as F
import json
import platform

pairs = [(i, j) for i in range(4) for j in range(i, 4)]
eta = [-1, 1, 1, 1]
checks = 0

def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(label)

def matrix():
    return [[F(0) for _ in range(4)] for _ in range(4)]

def identity():
    return [[F(i == j) for j in range(4)] for i in range(4)]

def conjugate(E, A):
    return [[sum(A[k][i]*E[k][l]*A[l][j] for k in range(4) for l in range(4))
             for j in range(4)] for i in range(4)]

def rref(rows):
    a = [[F(x) for x in row] for row in rows]
    pivots, r = [], 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [x / scale for x in a[r]]
        for i in range(len(a)):
            if i != r:
                scale = a[i][c]
                a[i] = [x - scale*y for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    return a, pivots

def nullspace(rows):
    a, pivots = rref(rows)
    basis = []
    for free in set(range(len(a[0]))) - set(pivots):
        v = [F(0)] * len(a[0])
        v[free] = F(1)
        for r, p in enumerate(pivots):
            v[p] = -a[r][free]
        basis.append(v)
    return pivots, basis

g = matrix()
for i in range(4):
    g[i][i] = F(eta[i])
gvec = [g[i][j] for i, j in pairs]
tensor_basis = []
for i, j in pairs:
    E = matrix()
    E[i][j] = E[j][i] = F(1)
    tensor_basis.append(E)

# Isotropy: two independent spatial quarter-turns and a rational finite boost.
group = []
for i, j in [(1, 2), (2, 3)]:
    A = identity()
    A[i][i] = A[j][j] = F(0)
    A[i][j], A[j][i] = F(-1), F(1)
    group.append(A)
A = identity()
A[0][0] = A[1][1] = F(5, 3)
A[0][1] = A[1][0] = F(4, 3)
group.append(A)
invariance = []
for A in group:
    require(conjugate(g, A) == g, 'actual Lorentz matrix')
    images = [conjugate(E, A) for E in tensor_basis]
    for i, j in pairs:
        invariance.append([image[i][j] - E[i][j]
                           for image, E in zip(images, tensor_basis)])
irank, ibasis = nullspace(invariance)
require(len(irank) == 9, 'isotropy rank')
require(ibasis == [gvec], 'isotropy nullspace is metric line')

# Separately, actual all-pair DDR strains with rational rotated and boosted pairs.
e = [[F(i == j) for j in range(4)] for i in range(4)]
orthopairs = [(e[0], e[i]) for i in (1, 2, 3)]
for i, j in [(1, 2), (1, 3), (2, 3)]:
    orthopairs.append((e[0], [(3*e[i][a]+4*e[j][a])/5 for a in range(4)]))
for i in (1, 2, 3):
    orthopairs.append(([(5*e[0][a]+4*e[i][a])/3 for a in range(4)],
                      [(4*e[0][a]+5*e[i][a])/3 for a in range(4)]))
dot = lambda u,v: sum(eta[a]*u[a]*v[a] for a in range(4))
ddr = []
for u, n in orthopairs:
    require((dot(u,u), dot(n,n), dot(u,n)) == (-1, 1, 0), 'orthonormal pair')
    H = [[2*eta[i]*eta[j]*(u[i]*u[j]+n[i]*n[j]) for j in range(4)] for i in range(4)]
    require(sum(eta[i]*H[i][i] for i in range(4)) == 0, 'strain trace zero')
    ddr.append([sum(eta[i]*eta[j]*E[i][j]*H[i][j]
                    for i in range(4) for j in range(4)) for E in tensor_basis])
drank, dbasis = nullspace(ddr)
require(len(drank) == 9, 'all-pair DDR rank')
require(dbasis == [gvec], 'DDR nullspace is metric line')
# Negative anchors distinguish each result from unrestricted component arithmetic.
rank_spatial, _ = nullspace(invariance[:20])
rank_one, _ = nullspace(ddr[:1])
require(len(rank_spatial) == 8, 'without boost an extra scalar survives')
require(len(rank_one) == 1, 'one pair leaves rank one only')
require(any(sum(row[i]*int(i == 0) for i in range(10)) != 0 for row in ddr),
        'nonmetric time-only tensor rejected')

curvature_rows = []
for kappa in [F(-7,3), F(-1), F(0), F(2,5), F(3)]:
    # R(e_c,e_d)e_b = κ (g_db e_c - g_cb e_d), convention matching T=-κI.
    curvature = lambda a,b,c,d: kappa*((a == c)*g[d][b] - (a == d)*g[c][b])
    Ric = [[sum(curvature(a,b,a,d) for a in range(4)) for d in range(4)] for b in range(4)]
    require(Ric == [[3*kappa*g[i][j] for j in range(4)] for i in range(4)], 'full Ricci contraction')
    R = sum(eta[i]*Ric[i][i] for i in range(4))
    require(R == 12*kappa, 'full scalar contraction')
    for a,b in [(F(1), F(0)), (F(1), F(-1,4)), (F(0), F(2)), (F(-2,3), F(4,7))]:
        E = [[a*Ric[i][j]+b*R*g[i][j] for j in range(4)] for i in range(4)]
        trace = sum(eta[i]*E[i][i] for i in range(4))
        require(E == [[(3*a+12*b)*kappa*g[i][j] for j in range(4)] for i in range(4)], 'response trace coefficient')
        require(all(E[i][j] - trace*g[i][j]/4 == 0 for i in range(4) for j in range(4)), 'response tracefree zero')
        Evec = [E[i][j] for i,j in pairs]
        require(all(sum(x*y for x,y in zip(row,Evec)) == 0 for row in ddr), 'direct DDR balance')
    curvature_rows.append({'kappa': str(kappa), 'R': str(R), 'Ric00': str(Ric[0][0])})

cosh_log = lambda q: (q + 1/q)/2
c1, c2, c4 = [cosh_log(F(2)**n) for n in (1, 2, 4)]
p, p0, q, q0 = 1/c1, 1/c2, c1/c2, c2/c4
require((p,p0,q,q0) == (F(4,5), F(8,17), F(10,17), F(68,257)), 'hyperbolic exact values')
require(0 < p0 < p < 1 and 0 < q0 < q < 1, 'both net blue yet positive contrasts')
require((p/p0, q/q0) == (F(17,10), F(1285,578)), 'exact contrast ratios')

print(json.dumps({'status':'PASS','checks':checks,'python':platform.python_version(),
 'arithmetic':'fractions.Fraction; exact rational anchors, no continuum sampling claim',
 'isotropy_rank':len(irank),'DDR_rank':len(drank),'common_nullspace':[[str(x) for x in gvec]],
 'spatial_only_rank':len(rank_spatial),'single_pair_rank':len(rank_one),
 'curvature_rows':curvature_rows,'contrast':{'p':str(p),'p0':str(p0),'q':str(q),'q0':str(q0),
 'p_ratio':str(p/p0),'q_ratio':str(q/q0)}}, indent=2))
