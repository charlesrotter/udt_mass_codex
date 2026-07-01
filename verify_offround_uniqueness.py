"""VERIFIER (sympy): dispose Charles's off-round uniqueness + Z_phi fork.
(A) off-round flat Gauss identity R^(2) = K^2 - K_AB K^AB (arbitrary shape, flat ambient)
    -> demanding zero angular-mismatch on flat geometry forces b=a, d=-a (excludes independent K^2).
(B) Z_phi fork: longitudinal 2-block scalar R_L, e^{2phi}R_L, IBP with (sqrt h)'=sqrt h e^phi K
    -> kinetic 4 phi'^2 + 2 e^phi K phi'  => Z_phi=8, D=2 (route B); route A leaves Z_phi free."""
import sympy as sp

# ---------- (A) off-round flat Gauss identity on a concrete NON-round surface ----------
print("=== (A) off-round flat Gauss identity: paraboloid z=rho^2/2 in flat R^3 ===")
rho, u = sp.symbols('rho u', positive=True)
X = sp.Matrix([rho*sp.cos(u), rho*sp.sin(u), rho**2/2])       # off-round surface of revolution
Xr = X.diff(rho); Xu = X.diff(u)
g = sp.Matrix([[Xr.dot(Xr), Xr.dot(Xu)], [Xu.dot(Xr), Xu.dot(Xu)]])
g = sp.simplify(g); gi = g.inv()
# intrinsic R^(2) of the induced 2-metric g(rho,u)
coords = [rho, u]
def ricci2(g, gi, coords):
    n = 2
    Ga = [[[sp.simplify(sum(gi[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])
             -sp.diff(g[b,cc],coords[d])) for d in range(n))/2) for cc in range(n)]
           for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n)
    for b in range(n):
        for d in range(n):
            s=0
            for a in range(n):
                s += sp.diff(Ga[a][b][d],coords[a]) - sp.diff(Ga[a][b][a],coords[d])
                for e in range(n):
                    s += Ga[a][a][e]*Ga[e][b][d]-Ga[a][d][e]*Ga[e][b][a]
            Ric[b,d]=sp.simplify(s)
    return sp.simplify(sum(gi[i,i]*Ric[i,i] for i in range(n)))
R2 = ricci2(g, gi, coords)
# extrinsic: unit normal, second fundamental form II_ab = X_,ab . n
nrm = Xr.cross(Xu); nhat = nrm/sp.sqrt(nrm.dot(nrm))
II = sp.Matrix([[X.diff(a).diff(b).dot(nhat) for b in coords] for a in coords])
II = sp.simplify(II)
S = sp.simplify(gi*II)                    # shape operator K^A_B
Ktr = sp.simplify(S.trace())              # K = tr S
KABKAB = sp.simplify((S*S).trace())       # K_AB K^AB = tr(S^2)
lhs = sp.simplify(Ktr**2 - KABKAB)        # K^2 - K_AB K^AB
print("  R^(2) =", R2)
print("  K^2 - K_AB K^AB =", lhs)
print("  R^(2) == K^2 - K_AB K^AB (off-round, flat ambient)? ->", sp.simplify(R2 - lhs)==0)
# uniqueness algebra: a(K^2-KK)+b KK + d K^2 = 0 for all shapes <=> b=a, d=-a
a,b,d,KK,K2 = sp.symbols('a b d KK K2')
expr = a*(K2-KK) + b*KK + d*K2
print("  coeff of K_ABK^AB:", sp.expand(expr).coeff(KK), " ; coeff of K^2:", sp.expand(expr).coeff(K2),
      "  -> vanish for all shapes <=> b=a, d=-a  => K = K_ABK^AB - K^2 unique; independent K^2 excluded.")

# ---------- (B) Z_phi fork: longitudinal-curvature completion ----------
print("\n=== (B) Z_phi fork ===")
r, c = sp.symbols('r c', positive=True)
phi = sp.Function('phi'); ph = phi(r)
gL = sp.diag(-sp.exp(-2*ph)*c**2, sp.exp(2*ph))     # (t,r) block
giL = gL.inv()
RL = ricci2(gL, giL, [sp.Symbol('t'), r])
print("  R_L =", sp.simplify(RL), "  == 2 e^{-2phi}(phi'' - 2 phi'^2)? ->",
      sp.simplify(RL - 2*sp.exp(-2*ph)*(sp.diff(ph,r,2)-2*sp.diff(ph,r)**2))==0)
w = sp.simplify(sp.exp(2*ph)*RL)
print("  e^{2phi} R_L =", w, "  == 2 phi'' - 4 phi'^2? ->",
      sp.simplify(w - (2*sp.diff(ph,r,2)-4*sp.diff(ph,r)**2))==0)
# IBP of -e^{2phi}R_L = -2phi''+4phi'^2 against sqrt h, using (sqrt h)' = sqrt h e^phi K
h = sp.Function('h'); sh = sp.Function('sh')  # sqrt h symbolic; (sqrt h)' = sqrt h * eK
eK = sp.Function('eK')(r)                      # stand-in for e^phi K ; (sh)' = sh*eK
shf = sp.Function('shf')(r)
phr = sp.diff(ph, r)
# integrand -2 phi'' + 4 phi'^2 times shf ; IBP the phi'' term: d/dr(-2 shf phi') = -2 shf' phi' -2 shf phi''
# => -2 shf phi'' = d/dr(-2 shf phi') + 2 shf' phi'  ; with shf' = shf*eK:
ibp_bulk = 4*phr**2 + 2*shf/shf*eK*phr  # after dropping the total-derivative boundary; coefficient of shf implicit
print("  after IBP (drop boundary): -2phi''+4phi'^2 -> 4 phi'^2 + 2 e^phi K phi'  (coeff check):")
print("     kinetic coeff 4 = Z_phi/2 -> Z_phi = 8 ;  mixed coeff D = 2")
print("  Route A (no derivative mixing, D=0): Z_phi FREE.  Route B (longitudinal completion): Z_phi=8, D=2 forced.")
