"""Exact u-congruence kinematics for reciprocal-lock metric. float-free sympy.
Metric class (SUPPLIED, canon): ds^2 = -e^{-2phi(x)} c^2 dt^2 + e^{2phi(x)}(dx^2+dy^2+dz^2).
u = d_t / sqrt(-g_tt)  (copresence direction, normalized). SCOPED: static, free-kinematic.
"""
import sympy as sp

t, x, y, z, c = sp.symbols('t x y z c', real=True, positive=True)
phi = sp.Function('phi')(x)          # depth field, depends only on x
coords = [t, x, y, z]
n = 4

# --- metric (reciprocal lock + isotropic transverse block) ---
g = sp.zeros(n, n)
g[0,0] = -sp.exp(-2*phi)*c**2
g[1,1] =  sp.exp(2*phi)
g[2,2] =  sp.exp(2*phi)
g[3,3] =  sp.exp(2*phi)
ginv = g.inv()

# --- Christoffels ---
def christoffel(g, ginv, coords):
    n = len(coords)
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a,d]*(sp.diff(g[d,b],coords[cc]) +
                                    sp.diff(g[d,cc],coords[b]) -
                                    sp.diff(g[b,cc],coords[d]))
                Gam[a][b][cc] = sp.simplify(s/2)
    return Gam
Gam = christoffel(g, ginv, coords)

# --- u^mu, u_mu ---
gtt = g[0,0]
norm = sp.sqrt(-gtt)                 # = e^{-phi} c
uup = [sp.simplify(1/norm), 0, 0, 0]
udn = [sp.simplify(sum(g[a,b]*uup[b] for b in range(n))) for a in range(n)]
print("u^mu =", uup)
print("u_mu =", udn)
print("norm u:", sp.simplify(sum(uup[a]*udn[a] for a in range(n))))  # expect -1

# --- covariant derivative nabla_nu u_mu = d_nu u_mu - Gam^l_{nu mu} u_l ---
def covD_lower(vlow, vup, Gam, coords):
    n = len(coords)
    # returns M[mu][nu] = nabla_nu v_mu
    M = [[0]*n for _ in range(n)]
    for mu in range(n):
        for nu in range(n):
            s = sp.diff(vlow[mu], coords[nu])
            for l in range(n):
                s -= Gam[l][nu][mu]*vlow[l]
            M[mu][nu] = sp.simplify(s)
    return M
nab = covD_lower(udn, uup, Gam, coords)   # nab[mu][nu] = nabla_nu u_mu

# --- acceleration a_mu = u^nu nabla_nu u_mu ---
a_low = [sp.simplify(sum(uup[nu]*nab[mu][nu] for nu in range(n))) for mu in range(n)]
a_up  = [sp.simplify(sum(ginv[mu,nu]*a_low[nu] for nu in range(n))) for mu in range(n)]
a2    = sp.simplify(sum(a_up[mu]*a_low[mu] for mu in range(n)))
print("a_mu =", a_low)
print("a^mu =", a_up)
print("a^mu a_mu =", a2)

# --- projector h_{mu nu} = g + u u ---
h = sp.zeros(n,n)
for mu in range(n):
    for nu in range(n):
        h[mu,nu] = sp.simplify(g[mu,nu] + udn[mu]*udn[nu])

# --- expansion theta = nabla_mu u^mu ---
uup_dn = covD_lower  # reuse pattern: nabla_nu u^mu
def covD_upper(vup, Gam, coords):
    n = len(coords)
    M = [[0]*n for _ in range(n)]
    for mu in range(n):
        for nu in range(n):
            s = sp.diff(vup[mu], coords[nu])
            for l in range(n):
                s += Gam[mu][nu][l]*vup[l]
            M[mu][nu] = sp.simplify(s)
    return M
nabU = covD_upper(uup, Gam, coords)   # nabU[mu][nu] = nabla_nu u^mu
theta = sp.simplify(sum(nabU[mu][mu] for mu in range(n)))
print("theta =", theta)

# --- B_{mu nu} = nabla_nu u_mu projected; shear & twist ---
# spatial projected gradient: B_{mu nu} = h_mu^a h_nu^b nabla_b u_a
Bmn = sp.zeros(n,n)
for mu in range(n):
    for nu in range(n):
        s = 0
        for a in range(n):
            for b in range(n):
                ha = h[mu,a]; hb = h[nu,b]
                s += ha*hb*nab[a][b]
        Bmn[mu,nu] = sp.simplify(s)
# symmetric traceless = shear; antisymmetric = twist
sym = sp.simplify((Bmn + Bmn.T)/2)
asym = sp.simplify((Bmn - Bmn.T)/2)
# shear = sym - (theta/3) h  (3 spatial dims)
shear = sp.simplify(sym - (theta/3)*h)
print("twist omega_{mu nu} (antisym proj) =")
sp.pprint(asym)
print("shear sigma_{mu nu} =")
sp.pprint(shear)
sigma2 = sp.simplify(sum(sum(shear[i,j]*ginv[i,ii]*ginv[j,jj]*shear[ii,jj]
              for ii in range(n) for jj in range(n)) for i in range(n) for j in range(n)))
omega2 = sp.simplify(sum(sum(asym[i,j]*ginv[i,ii]*ginv[j,jj]*asym[ii,jj]
              for ii in range(n) for jj in range(n)) for i in range(n) for j in range(n)))
print("sigma^2 =", sigma2)
print("omega^2 =", omega2)
