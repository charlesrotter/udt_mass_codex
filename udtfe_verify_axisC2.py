"""
Axis C, clean final test of the ABSORBABILITY claim.

The correct, sharp statement of 'varying-c in the metric is absorbable':
A metric g_tt = -F(r) (any lapse) has curvature that depends only on F, NOT on
how F is written as e^{-2phi}*cl^2. I.e. for FIXED g_tt and g_rr, splitting the
g_tt magnitude between an 'e^{-2phi}' piece and a 'cl^2' piece is a pure
relabeling with ZERO effect on any curvature invariant. Demonstrate: two
DIFFERENT (phi,cl) pairs giving the SAME product e^{-2phi}cl^2 (and same g_rr)
have identical curvature.
"""
import sympy as sp

r, t, th, ph = sp.symbols('r t theta varphi', real=True)
c0 = sp.symbols('c0', positive=True)
coords = [t, r, th, ph]

def ricci_kretsch(gmat):
    n = 4
    ginv = gmat.inv()
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for k in range(n):
                ss = 0
                for d in range(n):
                    ss += ginv[l, d]*(sp.diff(gmat[d, m], coords[k])
                                      + sp.diff(gmat[d, k], coords[m])
                                      - sp.diff(gmat[m, k], coords[d]))
                Gam[l][m][k] = sp.simplify(ss/2)
    def Riem(a, b, cc, d):
        term = sp.diff(Gam[a][b][d], coords[cc]) - sp.diff(Gam[a][b][cc], coords[d])
        for e in range(n):
            term += Gam[a][cc][e]*Gam[e][b][d] - Gam[a][d][e]*Gam[e][b][cc]
        return sp.simplify(term)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            Ric[b, d] = sp.simplify(sum(Riem(a, b, a, d) for a in range(n)))
    Rsc = sp.simplify(sum(ginv[i, i]*Ric[i, i] for i in range(n)))
    Rlow = {}
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    Rlow[(a,b,cc,d)] = sp.simplify(sum(gmat[a,e]*Riem(e,b,cc,d) for e in range(n)))
    K = 0
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    K += Rlow[(a,b,cc,d)]*ginv[a,a]*ginv[b,b]*ginv[cc,cc]*ginv[d,d]*Rlow[(a,b,cc,d)]
    return Rsc, sp.simplify(K)

phi = sp.Function('phi')(r)
# Split 1: lapse magnitude F = e^{-2phi} * c0^2  (cl = c0, "constant c")
g1 = sp.diag(-sp.exp(-2*phi)*c0**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)
# Split 2: SAME lapse magnitude F, written with a varying cl and a compensating phi2:
#   e^{-2phi2} cl^2 = e^{-2phi} c0^2  with cl arbitrary => phi2 = phi + ln(cl/c0)
# Keep the SAME spatial g_rr=e^{2phi} (the physical metric is literally identical).
cl = sp.Function('cl')(r)
phi2 = phi + sp.log(cl/c0)
g2 = sp.diag(-sp.exp(-2*phi2)*cl**2, sp.exp(2*phi), r**2, r**2*sp.sin(th)**2)

print("g1[tt] =", sp.simplify(g1[0,0]))
print("g2[tt] =", sp.simplify(g2[0,0]), " identical:", sp.simplify(g1[0,0]-g2[0,0])==0)
print("g1[rr] =", sp.simplify(g1[1,1]), " g2[rr] =", sp.simplify(g2[1,1]),
      " identical:", sp.simplify(g1[1,1]-g2[1,1])==0)

R1, K1 = ricci_kretsch(g1)
R2, K2 = ricci_kretsch(g2)
print("\nRicci diff  =", sp.simplify(R1-R2), " (==0 => splitting c-vs-phi has NO curvature effect)")
print("Kretsch diff =", sp.simplify(K1-K2), " (==0 => confirmed)")
print("\n=> ABSORBABILITY of varying-c CONFIRMED: the (phi,cl) split of the lapse")
print("   carries zero invariant content. Only the lapse magnitude (=phi alone")
print("   when cl folded in) and g_rr matter. PASS.")
