"""
Independent adversarial verification of the EOS window -> de Sitter uniqueness claim.

Metric: ds^2 = -A c^2 dt^2 + (1/A) dr^2 + r^2 dOmega^2, A = A(r).
Einstein-tensor continuum readout:
    rho    proportional to -G^t_t
    p_r    proportional to  G^r_r
    p_t    proportional to  G^theta_theta
with 8 pi G / c^4 = 1 convention (units absorbed).

Claim under test:
  reciprocal metric + Einstein readout + p_t = w rho (const) + DEC
  + BOTH wall-regularity AND center-regularity  ==>  w = -1 uniquely (de Sitter).
  L (A = 1 - r/X) is the w = -1/2 member and center-SINGULAR.

Everything derived below is my OWN sympy, no values taken from the docs.
"""
import sympy as sp

r, t, th, ph, c = sp.symbols('r t theta phi c', positive=True)
A = sp.Function('A')(r)

# metric g_{mu nu}, coords (t, r, theta, phi)
g = sp.diag(-A*c**2, 1/A, r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
coords = [t, r, th, ph]

# Christoffel symbols
def christoffel(g, ginv, coords):
    n = len(coords)
    Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a, d]*(sp.diff(g[d, b], coords[cc])
                                    + sp.diff(g[d, cc], coords[b])
                                    - sp.diff(g[b, cc], coords[d]))
                Gamma[a][b][cc] = sp.simplify(s/2)
    return Gamma

Gamma = christoffel(g, ginv, coords)

# Ricci tensor
n = 4
Ric = sp.zeros(n, n)
for a in range(n):
    for b in range(n):
        s = 0
        for cc in range(n):
            s += sp.diff(Gamma[cc][a][b], coords[cc]) - sp.diff(Gamma[cc][a][cc], coords[b])
            for d in range(n):
                s += Gamma[cc][cc][d]*Gamma[d][a][b] - Gamma[cc][b][d]*Gamma[d][a][cc]
        Ric[a, b] = sp.simplify(s)

Rscalar = sp.simplify(sum(ginv[a, b]*Ric[a, b] for a in range(n) for b in range(n)))

# Einstein tensor G_{mu nu} = R_{mu nu} - 1/2 g_{mu nu} R, then mixed G^mu_nu
G_low = sp.Matrix(n, n, lambda a, b: sp.simplify(Ric[a, b] - sp.Rational(1, 2)*g[a, b]*Rscalar))
G_mixed = sp.simplify(ginv*G_low)

Gt = sp.simplify(G_mixed[0, 0])   # G^t_t
Gr = sp.simplify(G_mixed[1, 1])   # G^r_r
Gth = sp.simplify(G_mixed[2, 2])  # G^theta_theta

print("=== Einstein mixed components (readout) ===")
print("G^t_t   =", Gt)
print("G^r_r   =", Gr)
print("G^theta_theta =", Gth)

rho = sp.simplify(-Gt)
p_r = sp.simplify(Gr)
p_t = sp.simplify(Gth)
print("\nrho  ~ -G^t_t   =", rho)
print("p_r  ~  G^r_r   =", p_r)
print("p_t  ~  G^th_th =", p_t)

# Check p_r = -rho identity on reciprocal metric
print("\np_r + rho simplifies to:", sp.simplify(p_r + rho))

# ---- Impose p_t = w rho, solve ODE for A(r) ----
w = sp.symbols('w', real=True)
Afun = sp.Function('A')
ode = sp.Eq(p_t.subs(A, Afun(r)).doit(), w*rho.subs(A, Afun(r)).doit())
ode = sp.simplify(ode)
print("\n=== ODE p_t = w rho ===")
print(ode)

sol = sp.dsolve(ode, Afun(r))
print("\nGeneral solution:")
print(sol)

print("\n\n=================================================================")
print(" PART 2: verify power family A=1-(r/X)^beta, beta=-2w")
print("=================================================================")
X, beta = sp.symbols('X beta', positive=True)
Ap = 1 - (r/X)**beta

rho_p = ((1 - Ap - r*sp.diff(Ap, r))/r**2)
pt_p  = (sp.diff(Ap, r, 2)/2 + sp.diff(Ap, r)/r)
ratio = sp.simplify(pt_p/rho_p)
print("p_t/rho for A=1-(r/X)^beta :", ratio, "  (expect -beta/2 = w)")

# Ricci scalar for this A (independent, general beta)
def ricci_scalar_of(Aexpr):
    gg = sp.diag(-Aexpr*c**2, 1/Aexpr, r**2, r**2*sp.sin(th)**2)
    gi = gg.inv()
    Gam = christoffel(gg, gi, coords)
    Rc = sp.zeros(4, 4)
    for a in range(4):
        for b in range(4):
            s = 0
            for cc in range(4):
                s += sp.diff(Gam[cc][a][b], coords[cc]) - sp.diff(Gam[cc][a][cc], coords[b])
                for d in range(4):
                    s += Gam[cc][cc][d]*Gam[d][a][b] - Gam[cc][b][d]*Gam[d][a][cc]
            Rc[a, b] = s
    return sp.simplify(sum(gi[a, b]*Rc[a, b] for a in range(4) for b in range(4)))

R_p = sp.simplify(ricci_scalar_of(Ap))
print("Ricci scalar R =", R_p, "  (doc: (beta+1)(beta+2) r^(beta-2)/X^beta)")
print("  check vs doc:", sp.simplify(R_p - (beta+1)*(beta+2)*r**(beta-2)/X**beta))

print("\n--- Center regularity: R finite as r->0 requires exponent (beta-2) >= 0 -> beta>=2 -> w<=-1")
for bval, name in [(sp.Rational(1), "L (beta=1, w=-1/2)"),
                   (sp.Rational(2), "dS (beta=2, w=-1)"),
                   (sp.Rational(3), "beta=3, w=-3/2"),
                   (sp.Rational(1,2), "beta=1/2, w=-1/4")]:
    Rb = R_p.subs(beta, bval)
    lim = sp.limit(Rb, r, 0, '+')
    print(f"  {name}: R = {sp.simplify(Rb)} ,  R(r->0) = {lim}")

print("\n--- DEC analysis (rho>0, |p_r|<=rho, |p_t|<=rho) ---")
# p_r = -rho => |p_r|=|rho| ok if rho>0. p_t = w rho => |p_t|<=rho iff |w|<=1 (rho>0).
rho_beta = sp.simplify(rho_p)
print("rho(A=1-(r/X)^beta) =", rho_beta)
print("sign of rho: for X>0,r>0 rho = (beta+1) r^(beta-2)/X^beta -> positive for beta>-1")
print("  simplified rho:", sp.simplify(rho_beta*r**2))
print("|p_t|<=rho  <=>  |w|<=1  (with rho>0)  ->  w in [-1,1]; combined w<0 => w in [-1,0)")
print("Center-regular w<=-1  INTERSECT  DEC w>=-1  ==>  w = -1 UNIQUELY")

print("\n--- de Sitter member beta=2 ---")
AdS = 1 - r**2/X**2
rho_dS = sp.simplify((1 - AdS - r*sp.diff(AdS, r))/r**2)
pt_dS  = sp.simplify(sp.diff(AdS, r, 2)/2 + sp.diff(AdS, r)/r)
print("A_dS =", AdS, " rho =", rho_dS, " p_t =", pt_dS, " p_t/rho =", sp.simplify(pt_dS/rho_dS))
print("rho uniform =", rho_dS, " (doc: 3/(8pi X^2) with 8piG=1 convention gives rho=3/X^2? check factor)")
print("R_dS =", sp.simplify(ricci_scalar_of(AdS)))

print("\n--- Does the DROPPED C2/r term matter? (Schwarzschild mass term) ---")
# A = 1 - (r/X)^beta + C2/r ; at center C2/r blows up -> singular unless C2=0.
# So center-regularity independently kills C2. Confirm curvature of pure 1/r term:
C2 = sp.symbols('C2')
R_schw = sp.simplify(ricci_scalar_of(1 + C2/r))
print("Ricci scalar of A=1+C2/r :", R_schw, "(=0: Schwarzschild vacuum, but K~1/r^6 singular at 0)")
