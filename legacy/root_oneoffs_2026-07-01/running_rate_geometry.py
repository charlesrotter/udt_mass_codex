"""
running_rate_geometry.py  (agent, 2026-06-18)  MODE: OBSERVE
Task 1 + Task 4 symbolic backbone.

Candidate UDT field equation (Charles frame, 2026-06-18):
    G_mu^nu = kappa(phi) T_mu^nu ,   kappa(phi) = (8 pi G / c0^4) e^{8 phi}
LEFT side = STANDARD Einstein tensor of the UDT metric (no f(phi)R, no Brans-Dicke
(g box - nabla nabla)f terms).  We VERIFY the left side here.

Metric (CANON C-2026-06-18-1; static/spherical/diagonal/areal-r are CHOSEN):
    ds^2 = -e^{-2phi} c0^2 dt^2 + e^{2phi} dr^2 + r^2 dOmega^2
phi = phi(r) (single slaved function).

Outputs:
  - Einstein tensor G^mu_nu (mixed) for general phi(r)
  - vacuum check: set G=0 and confirm solution is Schwarzschild-de-Sitter-free / Schwarzschild
  - identity Box_g phi vs -G^theta_theta
"""
import sympy as sp

t, r, th, ph, c0 = sp.symbols('t r theta phi_ang c0', positive=True)
phi = sp.Function('phi')(r)

# metric (mostly-plus spatial), signature (-,+,+,+)
gtt = -sp.exp(-2*phi)*c0**2
grr =  sp.exp(2*phi)
gthth = r**2
gphph = r**2*sp.sin(th)**2
g = sp.diag(gtt, grr, gthth, gphph)
ginv = g.inv()
x = [t, r, th, ph]

# Christoffels
def christoffel(g, ginv, x):
    n = len(x)
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cidx in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, b], x[cidx]) +
                                     sp.diff(g[d, cidx], x[b]) -
                                     sp.diff(g[b, cidx], x[d]))
                Gam[a][b][cidx] = sp.simplify(sp.Rational(1, 2)*s)
    return Gam

Gam = christoffel(g, ginv, x)

# Ricci tensor
def ricci(Gam, x):
    n = len(x)
    Ric = sp.zeros(n, n)
    for a in range(n):
        for b in range(n):
            s = 0
            for cidx in range(n):
                s += sp.diff(Gam[cidx][a][b], x[cidx]) - sp.diff(Gam[cidx][a][cidx], x[b])
                for d in range(n):
                    s += Gam[cidx][cidx][d]*Gam[d][a][b] - Gam[cidx][b][d]*Gam[d][a][cidx]
            Ric[a, b] = sp.simplify(s)
    return Ric

Ric = ricci(Gam, x)
Rscalar = sp.simplify(sum(ginv[i, j]*Ric[i, j] for i in range(4) for j in range(4)))

# Einstein tensor mixed G^mu_nu
Gmixed = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        Gab = Ric[a, b] - sp.Rational(1, 2)*g[a, b]*Rscalar
        # raise first index
    # raise after
for a in range(4):
    for b in range(4):
        s = 0
        for cidx in range(4):
            Gcb = Ric[cidx, b] - sp.Rational(1, 2)*g[cidx, b]*Rscalar
            s += ginv[a, cidx]*Gcb
        Gmixed[a, b] = sp.simplify(s)

print("=== Einstein tensor G^mu_nu (mixed), metric ds^2=-e^{-2phi}c0^2 dt^2+e^{2phi}dr^2+r^2 dOmega^2 ===")
labels = ['t', 'r', 'th', 'ph']
for a in range(4):
    print(f"G^{labels[a]}_{labels[a]} =", sp.simplify(Gmixed[a, a]))

# Box_g phi  vs -G^theta_theta  (geometry identity claimed in the prompt)
sqrtg = sp.sqrt(-g.det())
Box_phi = 0
for a in range(4):
    Box_phi += sp.diff(sqrtg*ginv[a, a]*sp.diff(phi, x[a]), x[a])/sqrtg
Box_phi = sp.simplify(Box_phi)
print("\n=== Box_g phi ===")
print("Box_g phi =", Box_phi)
print("\n=== -G^theta_theta ===")
print("-G^th_th  =", sp.simplify(-Gmixed[2, 2]))
print("\nBox_g phi - ( -G^th_th ) =", sp.simplify(Box_phi - (-Gmixed[2, 2])))

# VACUUM: solve G^t_t = 0 for phi(r)
print("\n=== VACUUM (G^t_t = 0) ===")
Gtt_eq = sp.simplify(Gmixed[0, 0])
print("G^t_t =", Gtt_eq)
# substitute u = e^{2 phi} ?  Let f = e^{-2phi} = -g_tt/c0^2 (the lapse^2). Schwarzschild: f=1-2GM/(rc^2)
# Check Schwarzschild: e^{-2phi} = 1 - rs/r , so phi = -1/2 ln(1-rs/r)
rs = sp.symbols('r_s', positive=True)
phi_schw = -sp.Rational(1, 2)*sp.log(1 - rs/r)
checks = {}
for a in range(4):
    expr = Gmixed[a, a].subs(phi, phi_schw).doit()
    # need to substitute derivatives properly: rebuild with explicit function
    checks[labels[a]] = expr
# Better: substitute the function then simplify
phi_s = sp.Function('phi')
sub = {phi.diff(r, 2): sp.diff(phi_schw, r, 2),
       phi.diff(r): sp.diff(phi_schw, r),
       phi: phi_schw}
print("\nSchwarzschild test  phi=-1/2 ln(1-rs/r):")
for a in range(4):
    val = sp.simplify(Gmixed[a, a].subs(sub))
    print(f"  G^{labels[a]}_{labels[a]} =", val)
