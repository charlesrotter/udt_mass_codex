"""Q1c: copresence congruence kinematics, TIME-LIVE, full 3+1 isotropic reciprocal lock.
u = d_t/sqrt(-g_tt). Compute acceleration a, expansion theta, shear sigma^2, twist omega^2.
A hypersurface-orthogonal timelike KV would force theta=sigma=omega=0; nonzero theta => un-pinned.
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
c = sp.symbols('c', positive=True)
phi = sp.Function('phi')(t, x, y, z)
coords = [t, x, y, z]
g = sp.diag(-sp.exp(-2*phi)*c**2, sp.exp(2*phi), sp.exp(2*phi), sp.exp(2*phi))
ginv = g.inv()

def christoffel(g, ginv, coords):
    n = len(coords); G = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = sum(ginv[a, d]*(sp.diff(g[d, b], coords[cc]) + sp.diff(g[d, cc], coords[b])
                        - sp.diff(g[b, cc], coords[d])) for d in range(n))
                G[a][b][cc] = sp.simplify(s/2)
    return G
G = christoffel(g, ginv, coords)

# u: u^t = e^{phi}/c, others 0 ; u_a
uup = [sp.exp(phi)/c, 0, 0, 0]
ulow = [sp.simplify(sum(g[a, b]*uup[b] for b in range(4))) for a in range(4)]
print("u^a =", uup); print("u_a =", ulow)
print("norm u.u =", sp.simplify(sum(ulow[a]*uup[a] for a in range(4))))

def nabla_u_low(a, b):  # nabla_a u_b
    return sp.diff(ulow[b], coords[a]) - sum(G[cc][a][b]*ulow[cc] for cc in range(4))
Nab = sp.Matrix(4, 4, lambda a, b: sp.simplify(nabla_u_low(a, b)))

# acceleration a_b = u^a nabla_a u_b
acc = [sp.simplify(sum(uup[a]*Nab[a, b] for a in range(4))) for b in range(4)]
accup = [sp.simplify(sum(ginv[b, d]*acc[d] for d in range(4))) for b in range(4)]
a2 = sp.simplify(sum(acc[b]*accup[b] for b in range(4)))
print("\nacceleration a_b =", acc)
print("a^2 =", a2)

# projector h_ab = g_ab + u_a u_b
h = sp.Matrix(4, 4, lambda a, b: sp.simplify(g[a, b] + ulow[a]*ulow[b]))
# B_ab = h_a^c h_b^d nabla_c u_d  (purely spatial velocity gradient)
hmix = sp.Matrix(4, 4, lambda a, b: sp.simplify(sum(ginv[a, cc]*h[cc, b] for cc in range(4))))  # h^a_b
B = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        B[a, b] = sp.simplify(sum(hmix[cc, a]*hmix[d, b]*Nab[cc, d] for cc in range(4) for d in range(4)))
theta = sp.simplify(sum(ginv[a, b]*B[a, b] for a in range(4) for b in range(4)))
print("\nexpansion theta =", theta)

# shear sigma_ab = B_(ab) - (1/3) theta h_ab ; twist omega_ab = B_[ab]
sig = sp.Matrix(4, 4, lambda a, b: sp.simplify((B[a, b]+B[b, a])/2 - theta*h[a, b]/3))
om = sp.Matrix(4, 4, lambda a, b: sp.simplify((B[a, b]-B[b, a])/2))
sig2 = sp.simplify(sum(ginv[a, cc]*ginv[b, d]*sig[a, b]*sig[cc, d]
                       for a in range(4) for b in range(4) for cc in range(4) for d in range(4)))
om2 = sp.simplify(sum(ginv[a, cc]*ginv[b, d]*om[a, b]*om[cc, d]
                      for a in range(4) for b in range(4) for cc in range(4) for d in range(4)))
print("shear^2 sigma_ab sigma^ab =", sig2)
print("twist^2 omega_ab omega^ab =", om2)
