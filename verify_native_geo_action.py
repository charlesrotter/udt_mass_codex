"""VERIFIER (sympy, no solver): dispose Charles's native geometric action derivation.
Native action S = int c sqrt(h) [ (Z/2)phi'^2 + R^(2)[h] + W_chi(phi) K ],  K = K_AB K^AB - K^2,
K_AB = 1/2 e^{-phi} d_r h_AB.  W_chi = e^{2phi} (G) or 1 (P). Aim hardest at:
 (i) G/P round cancellations; (ii) the GATING question: is K genuinely BULK in the sqrt(h)-measure
 action while EH (measure sqrt(-g) or sqrt(g3)) hides it as a boundary term?"""
import sympy as sp

r, th, ps, c, Z, lam = sp.symbols('r theta psi c Z lambda', positive=True)
phi = sp.Function('phi')
ph = phi(r); phr = sp.diff(ph, r)

# transverse round 2-metric h and its curvature; extrinsic K_AB = 1/2 e^{-phi} d_r h_AB
R2 = 2/r**2
Kcal = -2*sp.exp(-2*ph)/r**2                 # K_AB K^AB - K^2 (round), from earlier verification
sqh = r**2*sp.sin(th)

print("=== G/P round combinations ===")
G_comb = sp.simplify(R2 + sp.exp(2*ph)*Kcal)
P_comb = sp.simplify(R2 + Kcal)
print("  R^(2) + e^{2phi} K  =", G_comb, "   (G: angular sector CANCELS, any phi)")
print("  R^(2) + K           =", sp.simplify(P_comb), " = (2/r^2)(1-e^{-2phi})  (P source)")
print("  flat phi=0: R^(2)+K =", P_comb.subs(ph, 0), " (flat angular foliation cancels)")
print("  e^{2phi}K =", sp.simplify(sp.exp(2*ph)*Kcal), " -> phi-FREE (so G's K-term gives NO phi-EL)")

print("\n=== EL with the phi-FREE measure sqrt(h) (round) ===")
def phi_EL(Ldens):
    # EL: d/dphi - d/dr d/dphi'  of a density Ldens(phi,phi',r)
    return sp.simplify(sp.diff(Ldens, ph) - sp.diff(sp.diff(Ldens, phr), r))
LG = sqh*(Z*sp.Rational(1,2)*phr**2 + R2 + sp.exp(2*ph)*Kcal)
LP = sqh*(Z*sp.Rational(1,2)*phr**2 + R2 + Kcal)
elG = phi_EL(LG); elP = phi_EL(LP)
print("  S_G phi-EL /(-sin th) =", sp.simplify(-elG/sp.sin(th)),
      " == Z(r^2 phi')' ? ->", sp.simplify(-elG/sp.sin(th) - Z*sp.diff(r**2*phr, r))==0)
print("  S_P phi-EL /(sin th)  =", sp.simplify(elP/sp.sin(th)),
      " == Z(r^2 phi')' - 4e^{-2phi} ? ->",
      sp.simplify(elP/sp.sin(th) - (Z*sp.diff(r**2*phr, r) - 4*sp.exp(-2*ph)))==0)

print("\n=== GATING: is K BULK in the sqrt(h) action, while EH hides it? ===")
# native P angular density with phi-free measure:
densP = sp.simplify(sqh*P_comb)
print("  sqrt(h)(R^(2)+K) =", densP, " ; the R^(2) piece sqrt(h)R^(2) =", sp.simplify(sqh*R2),
      "-> d/dr(2r sin th) (boundary); the K piece = -2 e^{-2phi} sin th is NOT a total d/dr(local F) -> BULK")

# 3D spatial metric g3 = e^{2phi} dr^2 + r^2 Omega ; compute R^(3) and check EH-3D density total-deriv
g3 = sp.diag(sp.exp(2*ph), r**2, (r*sp.sin(th))**2)
gi3 = g3.inv(); coords3 = [r, th, ps]
def ricci_scalar(g, gi, coords):
    n = 3
    Ga = [[[sp.simplify(sum(gi[a,d]*(sp.diff(g[d,b],coords[cc])+sp.diff(g[d,cc],coords[b])
             -sp.diff(g[b,cc],coords[d])) for d in range(n))/2) for cc in range(n)]
           for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n)
    for b in range(n):
        for d in range(n):
            s = 0
            for a in range(n):
                s += sp.diff(Ga[a][b][d], coords[a]) - sp.diff(Ga[a][b][a], coords[d])
                for e in range(n):
                    s += Ga[a][a][e]*Ga[e][b][d] - Ga[a][d][e]*Ga[e][b][a]
            Ric[b,d] = sp.simplify(s)
    return sp.simplify(sum(gi[i,i]*Ric[i,i] for i in range(n)))
R3 = ricci_scalar(g3, gi3, coords3)
print("  R^(3) of (e^{2phi}dr^2 + r^2 Omega) =", R3)
print("  R^(3) vs R^(2)+/-K:  R^(3)-(R^(2)-K) =", sp.simplify(R3-(R2-Kcal)),
      " ;  R^(3)-(R^(2)+K) =", sp.simplify(R3-(R2+Kcal)))
sqg3 = sp.sqrt(g3.det())
# is sqrt(g3) R^(3) a total r-derivative?  try F(r) with dF/dr = sqrt(g3)R3 / sin th
dens3 = sp.simplify(sqg3*R3/sp.sin(th))
F3 = sp.integrate(dens3, r)
print("  sqrt(g3) R^(3)/sin th =", dens3, " ; integral_r =", sp.simplify(F3),
      " -> total derivative? ", not F3.has(sp.Integral))
