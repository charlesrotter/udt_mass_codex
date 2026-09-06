"""Exact local tensor methods for the frozen mathematical recipe.

Only the supplied metric and standard differential/tensor operations enter.
No physical field equation or interpretation is imported. Sparse dictionaries
store nonzero components, but absent components are explicitly zero in checks.
This is not advertised as a general-purpose verified geometry library.
"""
from itertools import product, permutations
import sympy as S

N = 4
Z = S.Integer(0)


def tidy(value):
    return S.factor(S.cancel(value))


def clean(data):
    return {key: val for key, raw in data.items() if (val := tidy(raw)) != 0}


def geometry(g, coordinates):
    gi = g.inv().applyfunc(tidy)
    gamma = {}
    for a,b,c in product(range(N), repeat=3):
        gamma[a,b,c] = sum(gi[a,d]*(S.diff(g[d,c],coordinates[b])
                              +S.diff(g[d,b],coordinates[c])
                              -S.diff(g[b,c],coordinates[d])) for d in range(N))/2
    gamma = clean(gamma)
    rup = {}
    for a,b,c,d in product(range(N), repeat=4):
        rup[a,b,c,d] = S.diff(gamma.get((a,d,b),Z),coordinates[c]) \
                      -S.diff(gamma.get((a,c,b),Z),coordinates[d]) \
                      +sum(gamma.get((a,c,e),Z)*gamma.get((e,d,b),Z)
                          -gamma.get((a,d,e),Z)*gamma.get((e,c,b),Z)
                          for e in range(N))
    rup = clean(rup)
    ric = S.Matrix(N,N,lambda b,d: tidy(sum(rup.get((a,b,a,d),Z) for a in range(N))))
    scalar = tidy(sum(gi[a,b]*ric[a,b] for a,b in product(range(N),repeat=2)))
    riemann, weyl = {}, {}
    for a,b,c,d in product(range(N), repeat=4):
        rv = sum(g[a,e]*rup.get((e,b,c,d),Z) for e in range(N))
        riemann[a,b,c,d] = rv
        weyl[a,b,c,d] = rv-(g[a,c]*ric[d,b]-g[a,d]*ric[c,b]
                            -g[b,c]*ric[d,a]+g[b,d]*ric[c,a])/2 \
                          +scalar*(g[a,c]*g[d,b]-g[a,d]*g[c,b])/6
    return gi, gamma, clean(riemann), ric, scalar, clean(weyl)


def epsilon_lower(g, orientation=1):
    density = S.sqrt(-tidy(g.det()))
    result = {}
    for p in permutations(range(N)):
        inversions = sum(p[i]>p[j] for i in range(N) for j in range(i+1,N))
        result[p] = orientation*((-1)**inversions)*density
    return result


def hodge_first(g, gi, tensor, orientation=1, mutation=None):
    eps = epsilon_lower(g,orientation)
    half = S.Integer(1) if mutation=='omit_dual_half' else S.Rational(1,2)
    result = {}
    for a,b,c,d in product(range(N), repeat=4):
        result[a,b,c,d] = half*sum(eps.get((a,b,p,q),Z)*gi[p,m]*gi[q,n]*value
                         for (m,n,cc,dd),value in tensor.items() if cc==c and dd==d
                         for p,q in product(range(N),repeat=2))
    return clean(result)


def quadratic(g, gi, weyl, orientation=1, mutation=None):
    dual = hodge_first(g,gi,weyl,orientation,mutation)
    inverse = S.eye(N) if mutation=='euclidean_contraction' else gi
    terms = [weyl] if mutation=='omit_dual' else [weyl,dual]
    result = {}
    for tensor in terms:
        for (a,e,c,h),left in tensor.items():
            for (b,f,d,i),right in tensor.items():
                coefficient = inverse[e,f]*inverse[h,i]
                if coefficient:
                    key = (a,b,c,d)
                    result[key] = result.get(key,Z)+coefficient*left*right
    return dual, clean(result)


def real_future_root(B, auxiliary_future, mutation=None):
    """Extraction on the rank-one positive fourth-power class; verify that class.

The arbitrary timelike vector is only a computational auxiliary. The analytic
argument and tests require its cancellation. No preferred observer is selected.
"""
    U = auxiliary_future
    contraction = tidy(sum(value*U[a]*U[b]*U[c]*U[d] for (a,b,c,d),value in B.items()))
    if contraction == 0:
        if B:
            raise ValueError('zero contraction outside certified pure-power domain')
        return S.zeros(N,1)
    exponent = S.Rational(1,2) if mutation=='wrong_root_degree' else S.Rational(3,4)
    sign = 1 if mutation=='past_root' else -1
    return S.Matrix([S.simplify(sign*sum(value*U[b]*U[c]*U[d]
                              for (aa,b,c,d),value in B.items() if aa==a)
                              /contraction**exponent) for a in range(N)])


def exterior_one(beta, coordinates, mutation=None):
    if mutation=='differentials_zero':
        return S.zeros(N,N)
    return S.Matrix(N,N,lambda a,b: tidy(S.diff(beta[b],coordinates[a])
                                       -S.diff(beta[a],coordinates[b])))


def covariant_one(beta, gamma, coordinates):
    return S.Matrix(N,N,lambda a,b: tidy(S.diff(beta[b],coordinates[a])
                          -sum(gamma.get((c,a,b),Z)*beta[c] for c in range(N))))


def divergence(g, vector, coordinates, mutation=None):
    if mutation=='differentials_zero':
        return Z
    density = S.sqrt(-tidy(g.det()))
    return tidy(sum(S.diff(density*vector[a],coordinates[a]) for a in range(N))/density)


def raised_current(gi, beta, mutation=None, base_inverse=None):
    if mutation=='homothety_inverse_frozen' and base_inverse is not None:
        return (base_inverse*beta).applyfunc(S.simplify)
    return (gi*beta).applyfunc(S.simplify)


def sheet_area(g, tangents, mutation=None):
    metric = S.eye(N) if mutation=='euclidean_cut_area' else g
    return S.sqrt(tidy((tangents.T*metric*tangents).det()))


def product_readout(omega, spacing, s_density, area, mutation=None, new_spacing=None):
    if mutation=='phase_gauge_recreates_mu' and new_spacing is not None:
        s_density *= new_spacing/spacing
    divisor = spacing if new_spacing is None else new_spacing
    return S.simplify(omega*s_density/(divisor*area))
