"""Independent verification (Attack A + B).

A: compute sqrt(-g)R for ds^2 = -f dt^2 + f^-1 dr^2 + rho^2 dOmega^2 from
   scratch (own Christoffel/Riemann code, lower-index Riemann route, different
   from the target script's Ricci-direct route), check:
     - rho^2 R = -rho^2 f'' - 4 rho rho' f' + 2 - 2 f rho'^2 - 4 f rho rho''
     - boundary split rho^2 R = -d/dr[rho^2 f' + 2 f rho rho'] + 2 - 2 f rho rho''
     - EL_f = -2 rho rho'',  EL_rho = -(2 rho f'' + 4 rho' f' + 4 f rho'')
     - rho = r  ==> total derivative of 2r(1-f) - r^2 f'
     - cross-check vs warped-product formula R = -f'' + 2/rho^2 - 2 f rho'^2/rho^2
                                                 - (4/rho)(f' rho' + f rho'')
B: physicality of the underdetermination: two extremal members with the SAME
   (C, a): (rho=r, f=C+a/r) vs (rho=r^2, f=C+a/(3r^3)). Compare Ricci scalar
   and Kretschmann as functions of the INVARIANT areal radius rho.
"""
import sympy as sp

t, r, th, ph = sp.symbols("t r theta phi", real=True, positive=True)
f = sp.Function("f", positive=True)(r)
rho = sp.Function("rho", positive=True)(r)
x = [t, r, th, ph]
g = sp.diag(-f, 1/f, rho**2, rho**2*sp.sin(th)**2)
ginv = g.inv()
n = 4

# Christoffel symbols Gamma^a_{bc}
Gam = [[[sp.together(sum(ginv[a, d]*(sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b])
         - sp.diff(g[b, c], x[d]))/2 for d in range(n)))
         for c in range(n)] for b in range(n)] for a in range(n)]

# Riemann R^a_{bcd} = dGam^a_{bd}/dx^c - dGam^a_{bc}/dx^d + G^a_{ce}G^e_{bd} - G^a_{de}G^e_{bc}
def Riem(a, b, c, d):
    return sp.simplify(sp.diff(Gam[a][b][d], x[c]) - sp.diff(Gam[a][b][c], x[d])
        + sum(Gam[a][c][e]*Gam[e][b][d] - Gam[a][d][e]*Gam[e][b][c] for e in range(n)))

Riemann = [[[[Riem(a, b, c, d) for d in range(n)] for c in range(n)]
            for b in range(n)] for a in range(n)]

# Ricci from Riemann contraction (different route than target script)
Ric = [[sp.simplify(sum(Riemann[a][b][a][d] for a in range(n))) for d in range(n)]
       for b in range(n)]
Rs = sp.simplify(sum(ginv[b, d]*Ric[b][d] for b in range(n) for d in range(n)))

fp, fpp = sp.diff(f, r), sp.diff(f, r, 2)
rp, rpp = sp.diff(rho, r), sp.diff(rho, r, 2)

target = -rho**2*fpp - 4*rho*rp*fp + 2 - 2*f*rp**2 - 4*f*rho*rpp
print("A1 rho^2 R == target:", sp.simplify(rho**2*Rs - target) == 0)

warped = -fpp + 2/rho**2 - 2*f*rp**2/rho**2 - (4/rho)*(fp*rp + f*rpp)
print("A2 cross-check warped-product formula:", sp.simplify(Rs - warped) == 0)

bdry = -(rho**2*fp + 2*f*rho*rp)
rem = sp.simplify(rho**2*Rs - sp.diff(bdry, r))
print("A3 boundary split, remainder == 2 - 2 f rho rho'':",
      sp.simplify(rem - (2 - 2*f*rho*rpp)) == 0)
# Is the remainder itself secretly a total derivative? 2 is (d/dr)(2r) but
# -2 f rho rho'' cannot be: check EL derivative of the remainder is nonzero.
def EL(L, u):
    return sp.simplify(L.diff(u) - sp.diff(L.diff(sp.diff(u, r)), r)
                       + sp.diff(L.diff(sp.diff(u, r, 2)), r, 2))
remL = 2 - 2*f*rho*rpp
print("A4 remainder NOT a null Lagrangian: EL_f[rem] =", EL(remL, f),
      "| EL_rho[rem] =", EL(remL, rho))

ELf = EL(rho**2*Rs, f)
ELrho = EL(rho**2*Rs, rho)
print("A5 EL_f[rho^2 R] == -2 rho rho'':", sp.simplify(ELf + 2*rho*rpp) == 0)
print("A6 EL_rho[rho^2 R] == -(2 rho f'' + 4 rho' f' + 4 f rho''):",
      sp.simplify(ELrho + 2*rho*fpp + 4*rp*fp + 4*f*rpp) == 0)

at_r = sp.simplify((rho**2*Rs).subs(rho, r).doit())
print("A7 rho=r collapse to d/dr[2r(1-f) - r^2 f']:",
      sp.simplify(at_r - sp.diff(2*r*(1-f) - r**2*fp, r)) == 0)

# ---------------- B: physicality of underdetermination --------------------
print()
C, a = sp.symbols("C a", positive=True)

def invariants(f_expr, rho_expr):
    sub = [(f, f_expr), (rho, rho_expr)]
    R_v = sp.simplify(Rs.subs(sub).doit())
    # Kretschmann: K = R_{abcd} R^{abcd}
    Rdown = [[[[sp.simplify(sum(g[a_i, e]*Riemann[e][b][c][d] for e in range(n))).subs(sub).doit()
               for d in range(n)] for c in range(n)] for b in range(n)] for a_i in range(n)]
    gi = [[ginv[i, j].subs(sub).doit() for j in range(n)] for i in range(n)]
    K_v = 0
    for A in range(n):
     for B in range(n):
      for Cc in range(n):
       for D in range(n):
        if Rdown[A][B][Cc][D] == 0:
            continue
        # diagonal metric: raising trivial
        K_v += Rdown[A][B][Cc][D]**2 * gi[A][A]*gi[B][B]*gi[Cc][Cc]*gi[D][D]
    return sp.simplify(R_v), sp.simplify(K_v)

# member 1: rho = r, f = C + a/r  (rho^2 f' = -a, satisfies the lock)
R1, K1 = invariants(C + a/r, r)
# member 2: rho = r^2, f = C + a/(3 r^3)  (rho^2 f' = r^4 * (-a/r^4) = -a)
R2, K2 = invariants(C + a/(3*r**3), r**2)
print("member1 (rho=r):    R =", R1)
print("member1 Kretschmann:", K1)
print("member2 (rho=r^2):  R =", R2)
print("member2 Kretschmann:", K2)

# express as functions of areal radius P (invariant): member1 P=r; member2 P=r^2
P = sp.symbols("P", positive=True)
R1P = sp.simplify(R1.subs(r, P))
R2P = sp.simplify(R2.subs(r, sp.sqrt(P)))
K1P = sp.simplify(K1.subs(r, P))
K2P = sp.simplify(K2.subs(r, sp.sqrt(P)))
print("R as function of areal radius:  member1:", R1P, " member2:", sp.expand(R2P))
print("B1 R(P) differ identically:", sp.simplify(R1P - R2P) != 0)
print("B2 K(P) differ identically:", sp.simplify(K1P - K2P) != 0)
# decisive special case C=1: member1 is Schwarzschild-like (R=0), member2 has R != 0
print("B3 C=1: member1 R =", R1P.subs(C, 1), "; member2 R =", sp.simplify(R2P.subs(C, 1)))

# gauge claim: g_tt g_rr = -1 fixes r up to translation/reflection
rt = sp.Function("rt", positive=True)(r)  # r = rt(r~) reparam; need (dr/dr~)^2 = 1
print("B4 form-preservation condition (dr/dr~)^2 = 1 -> r~ = +-r + const (by inspection)")
