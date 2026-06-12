"""Attack B: independent derivation of G^th_th and the C1 scalar stress."""
import sympy as sp

t, r, th, ph = sp.symbols("t r theta varphi", real=True)
a, c = sp.symbols("a c", real=True)
C = sp.Symbol("C", positive=True)
f = sp.Function("f", positive=True)(r)
coords = [t, r, th, ph]

g = sp.diag(-f, 1/f, r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
n = 4
Gam = [[[sp.simplify(sum(ginv[l, m]*(sp.diff(g[m, i], coords[j])
        + sp.diff(g[m, j], coords[i]) - sp.diff(g[i, j], coords[m]))
        for m in range(n))/2) for j in range(n)] for i in range(n)] for l in range(n)]
Ric = sp.zeros(n, n)
for i in range(n):
    for j in range(n):
        e = sum(sp.diff(Gam[l][i][j], coords[l]) - sp.diff(Gam[l][i][l], coords[j])
                for l in range(n))
        e += sum(Gam[l][l][m]*Gam[m][i][j] - Gam[l][j][m]*Gam[m][i][l]
                 for l in range(n) for m in range(n))
        Ric[i, j] = sp.simplify(e)
Rs = sp.simplify(sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n)))
Gmix = sp.simplify(ginv*(Ric - Rs/2*g))
fp = f.diff(r)
print("G^th_th - [f''/2 + f'/r] =", sp.simplify(Gmix[2, 2] - (f.diff(r, 2)/2 + fp/r)))
print("G^th_th - (r^2 f')'/(2r^2) =", sp.simplify(Gmix[2, 2] - sp.diff(r**2*fp, r)/(2*r**2)))
print("G^t_t - (r f' + f - 1)/r^2 =", sp.simplify(Gmix[0, 0] - (r*fp + f - 1)/r**2))
print("G^th_th on f=C+a/r:", sp.simplify(Gmix[2, 2].subs(f, C + a/r).doit()))

# de Sitter convention anchor
lam = sp.Symbol("Lambda", positive=True)
print("G^th_th(f=1-Lam r^2/3) =", sp.simplify(Gmix[2, 2].subs(f, 1 - lam*r**2/3).doit()))

# --- stress tensor: T_mn = -2 dL/dg^mn + g_mn L for L = -(c/2) e^{-2phi} g^{ab} d_a phi d_b phi
phi = sp.Function("phi", real=True)(r)
# dL/dg^{mn} = -(c/2) e^{-2phi} d_m phi d_n phi  (only rr nonzero)
dphi = [0, phi.diff(r), 0, 0]
Lval = -sp.Rational(1, 2)*c*sp.exp(-2*phi)*ginv[1, 1]*phi.diff(r)**2
T = sp.zeros(4, 4)
for m in range(4):
    for nn in range(4):
        T[m, nn] = sp.simplify(-2*(-sp.Rational(1,2)*c*sp.exp(-2*phi)*dphi[m]*dphi[nn]) + g[m, nn]*Lval)
Tmix = sp.simplify(ginv*T)
gr = c*sp.exp(-2*phi)*f*phi.diff(r)**2/2
print("\nT^t_t + (c/2)e^{-2phi} f phi'^2 =", sp.simplify(Tmix[0, 0] + gr))
print("T^r_r - (c/2)e^{-2phi} f phi'^2 =", sp.simplify(Tmix[1, 1] - gr))
print("T^th_th + (c/2)e^{-2phi} f phi'^2 =", sp.simplify(Tmix[2, 2] + gr))
print("T^th_th - L_value =", sp.simplify(Tmix[2, 2] - Lval))
# repo lock phi = -(1/2) ln f
Th_lock = sp.simplify(Tmix[2, 2].subs(phi, -sp.log(f)/2).doit())
print("T^th_th|lock + (c/8) f'^2 =", sp.simplify(Th_lock + c*fp**2/8))
Delta = sp.simplify(Gmix[2, 2] - 8*sp.pi*Th_lock)
Db = sp.simplify(Delta.subs(f, C + a/r).doit())
print("Delta|banked - pi c a^2/r^4 =", sp.simplify(Db - sp.pi*c*a**2/r**4),
      "| C-independent:", C not in Db.free_symbols)

# cross-check T^th_th via FULL variational machinery incl. sqrt(-g) weight
# (T_mn = -(2/sqrt(-g)) d(sqrt(-g) L)/d g^mn): the sqrt(-g) term gives
# -2*(-1/2) g_mn L = +g_mn L -- same as above; verify with explicit symbols
att, arr2, ahh, app = sp.symbols("Att Arr Ahh App", real=True)
sqrtg = 1/sp.sqrt(-att*arr2*ahh*app)
Lm = -sp.Rational(1,2)*c*sp.exp(-2*phi)*arr2*phi.diff(r)**2
vals = {att: -1/f, arr2: f, ahh: 1/r**2, app: 1/(r**2*sp.sin(th)**2)}
T_hh_low = sp.simplify((-2/sqrtg*sp.diff(sqrtg*Lm, ahh)).subs(vals))
print("full-machinery T^th_th matches:", sp.simplify(T_hh_low/r**2 - Tmix[2, 2]) == 0)

# conservation extra
Tlock = sp.diag(*[sp.simplify(Tmix[i, i].subs(phi, -sp.log(f)/2).doit()) for i in range(4)])
div_r = sp.simplify(
    sum(sp.diff(Tlock[m, 1], coords[m]) for m in range(4))
    + sum(Gam[m][m][l]*Tlock[l, 1] for m in range(4) for l in range(4))
    - sum(Gam[l][m][1]*Tlock[m, l] for m in range(4) for l in range(4)))
print("(div T)_r - [(c/4)f'(f''+2f'/r) + (c/8)f'^3/f] =",
      sp.simplify(div_r - (c/4*fp*(f.diff(r,2) + 2*fp/r) + c/8*fp**3/f)))
print("(div T)_r |banked =", sp.simplify(div_r.subs(f, C + a/r).doit()))
