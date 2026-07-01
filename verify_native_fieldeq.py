"""VERIFIER (pure sympy, no solver/solve): dispose Charles's native field-eq derivation.
Check every load-bearing boxed claim. Aim hardest at the GR-collapse-escape step."""
import sympy as sp

r, th, ps, t, c = sp.symbols('r theta psi t c', positive=True)
lam, q, phiinf, C0, C1, Z, K, xi, kap = sp.symbols('lambda q phi_inf C0 C1 Z Kc xi kappa')
phi = sp.Function('phi')

def cov_lap_radial(f, phifun):
    """Box_g f for the canonical metric, radial: (1/(r^2)) d/dr( r^2 e^{-2phi} f' )
    computed from the metric directly to confirm the operator."""
    ph = phifun(r)
    g = sp.diag(-sp.exp(-2*ph)*c**2, sp.exp(2*ph), r**2, (r*sp.sin(th))**2)
    detg = sp.simplify(g.det()); sqrtmg = sp.sqrt(-detg)
    ginv = g.inv()
    # Box f = 1/sqrt(-g) d_mu( sqrt(-g) g^{mu nu} d_nu f ), radial-only f
    fr = sp.diff(f(r), r)
    flux = sqrtmg*ginv[1, 1]*fr
    return sp.simplify(sp.diff(flux, r)/sqrtmg), sqrtmg, ginv

print("=== [0] det & measure: sqrt(-g) should be c r^2 sin(th) (phi-free) ===")
box_phi, sqrtmg, ginv = cov_lap_radial(phi, phi)
print("  sqrt(-g) =", sqrtmg)
print("  Box_g phi =", sp.simplify(box_phi))
print("  matches (1/r^2)(r^2 e^{-2phi} phi')'? ->",
      sp.simplify(box_phi - sp.diff(r**2*sp.exp(-2*phi(r))*sp.diff(phi(r),r), r)/r**2) == 0)

print("\n=== [1] Ricci scalar of canonical metric ===")
ph = phi(r)
g = sp.diag(-sp.exp(-2*ph)*c**2, sp.exp(2*ph), r**2, (r*sp.sin(th))**2)
gi = g.inv()
coords = [t, r, th, ps]
def christ(g, gi, coords):
    n=4; Ga=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s=0
                for d in range(n):
                    s+=gi[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])-sp.diff(g[b,cc],coords[d]))
                Ga[a][b][cc]=sp.simplify(s/2)
    return Ga
Ga=christ(g,gi,coords)
def ricci(Ga,coords):
    n=4; Ric=sp.zeros(n)
    for b in range(n):
        for d in range(n):
            s=0
            for a in range(n):
                s+=sp.diff(Ga[a][b][d],coords[a])-sp.diff(Ga[a][b][a],coords[d])
                for e in range(n):
                    s+=Ga[a][a][e]*Ga[e][b][d]-Ga[a][d][e]*Ga[e][b][a]
            Ric[b,d]=sp.simplify(s)
    return Ric
Ric=ricci(Ga,coords)
Rs=sp.simplify(sum(gi[i,i]*Ric[i,i] for i in range(4)))
R_claim = sp.exp(-2*ph)*(-4*sp.diff(ph,r)**2+2*sp.diff(ph,r,2)+8*sp.diff(ph,r)/r)+2/r**2-2*sp.exp(-2*ph)/r**2
print("  R - R_claim simplifies to 0? ->", sp.simplify(Rs-R_claim)==0)

print("\n=== [2] EH boundary-term identity: r^2 R == d/dr[2r(1-e^{-2phi})+2r^2 e^{-2phi}phi'] ===")
bdy = 2*r*(1-sp.exp(-2*ph))+2*r**2*sp.exp(-2*ph)*sp.diff(ph,r)
print("  r^2 R - d/dr[bdy] = 0? ->", sp.simplify(r**2*Rs - sp.diff(bdy,r))==0)

print("\n=== [3] R1-WEIGHTED kinetic density is phi-free (only phi'): resolves probe/self-consistent ===")
# density = sqrt(-g) * e^{2phi} * g^{rr} * (phi')^2
dens = sqrtmg*sp.exp(2*ph)*gi[1,1]*sp.diff(ph,r)**2
print("  weighted kinetic density =", sp.simplify(dens), " (no explicit phi, only phi' -> probe==self-consistent)")
# EL of L = r^2 phi'^2 (drop c sin th): d/dr(2 r^2 phi') = 0 -> (r^2 phi')'=0
phi_sol = phiinf - q/r
print("  EL (r^2 phi')'=0 ; solution phi=phi_inf - q/r satisfies it? ->",
      sp.simplify(sp.diff(r**2*sp.diff(phi_sol,r),r))==0)
gtt = -sp.exp(-2*phi_sol)
print("  g_tt = ", sp.simplify(gtt), "  (exponential lapse e^{2q/r}, NOT Schwarzschild -(1-2M/r))")

print("\n=== [4] UNWEIGHTED self-consistent: Box phi + e^{-2phi}phi'^2=0 -> e^{-phi}=C0+C1/r ===")
lhs = box_phi + sp.exp(-2*phi(r))*sp.diff(phi(r),r)**2
y_sol = C0 + C1/r          # e^{-phi} = C0 + C1/r  => phi = -ln(C0+C1/r)
phi_uw = -sp.log(C0+C1/r)
chk = lhs.subs(phi(r), phi_uw).doit()
print("  residual at e^{-phi}=C0+C1/r ->", sp.simplify(chk))

print("\n=== [5] Constrained-two-player: h_AB=r^2 Omega -> K_AB K^AB - K^2 = -2 e^{-2phi}/r^2 ===")
# transverse 2-metric h = diag(r^2, r^2 sin^2 th); normal n = e^{-phi} d_r
h = sp.diag(r**2, (r*sp.sin(th))**2); hinv = h.inv()
KAB = sp.zeros(2)
for A in range(2):
    for B in range(2):
        KAB[A,B] = sp.Rational(1,2)*sp.exp(-ph)*sp.diff(h[A,B], r)
Kmix = sp.simplify(hinv*KAB)           # K^A_B
Ktr = sp.simplify(Kmix.trace())
KABKAB = sp.simplify(sum(Kmix[i,j]*Kmix[j,i] for i in range(2) for j in range(2)))
Kcal = sp.simplify(KABKAB - Ktr**2)
print("  K (trace) =", Ktr, "  K_ABK^AB - K^2 =", Kcal,
      "  == -2 e^{-2phi}/r^2? ->", sp.simplify(Kcal + 2*sp.exp(-2*ph)/r**2)==0)
print("  sqrt(-g) for constrained metric = c*sqrt(h) (phi-free)? det check ->",
      sp.simplify(sp.sqrt(-sp.diag(-sp.exp(-2*ph)*c**2, sp.exp(2*ph), r**2, (r*sp.sin(th))**2).det())
                  - c*sp.sqrt(h.det()))==0)

print("\n=== [6] Branch P eq: Z(r^2 phi')' - 4 e^{-2phi} = 0 (from d/dr(Z sqrt h phi')+2 sqrt h K=0) ===")
sh = r**2*sp.sin(th)   # sqrt(h)
branchP = sp.diff(Z*sh*sp.diff(ph,r), r) + 2*sh*Kcal
print("  d/dr(Z sqrt(h) phi') + 2 sqrt(h) K  = ", sp.simplify(branchP/sp.sin(th)),
      "  == Z(r^2phi')' - 4e^{-2phi} ->",
      sp.simplify(branchP/sp.sin(th) - (Z*sp.diff(r**2*sp.diff(ph,r),r) - 4*sp.exp(-2*ph)))==0)
