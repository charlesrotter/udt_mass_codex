"""B3/B4/B5: proper-measure lift, hostile recomputation.
Scheme (weld record W1): g_tt=-e^{-2phi}, g_rr=+e^{+2phi}, phi=phi0+eps*dphi*Y,
g_tr=eps*H1*Y, g_thth=r^2(1+eps*K*Y), g_phph=r^2 sin^2(1+eps*K*Y).
Banked H1 sector (weld record, verifier-confirmed): A_C1 = (c/4) f^2 r^2 phi0'^2 (H1^2 coeff),
weld H1 = 2 d_t dphi/(f phi0')  => B = -4A/(f phi0') ;  flip fact B^2/(4A) = 2*gamma.
Source ties to C1 normalization via criticality: c_n = c * J f0^{1-n}/n  (same c).
"""
import sympy as sp

eps, H1, K, Y, r, th, n, q = sp.symbols('epsilon H1 K Y r theta n q', positive=True)
phi = sp.Symbol('phi', real=True)   # full phi (background+pert) -- measure must be phi-free
c = sp.Symbol('c', positive=True)
pp = sp.Symbol('pp', positive=True)     # phi0'
E0s = sp.Symbol('E0', positive=True)    # E0 > 0 on collar
f = sp.Symbol('f', positive=True)

# ---- measure expansion ----
g = sp.Matrix([[-sp.exp(-2*phi), eps*H1*Y, 0, 0],
               [ eps*H1*Y, sp.exp(2*phi), 0, 0],
               [0, 0, r**2*(1+eps*K*Y), 0],
               [0, 0, 0, r**2*sp.sin(th)**2*(1+eps*K*Y)]])
sqrtg = sp.sqrt(-g.det())
ser = sp.series(sqrtg, eps, 0, 3).removeO()
claim = r**2*(1+eps*K*Y)*(1+eps**2*H1**2*Y**2/2)*sp.sin(th)
print("B3 measure: sqrt(-g) to O(e^2) - claim:",
      sp.simplify(sp.expand(ser - sp.expand(claim)).coeff(eps,0)),
      sp.simplify(sp.expand(ser - sp.expand(claim)).coeff(eps,1)),
      sp.simplify(sp.expand(ser - sp.expand(claim)).coeff(eps,2)))
print("B3 measure phi-free:", sp.diff(ser, phi) == 0)

# ---- source O(e^2) loadings under proper measure (collar, criticality-tied c_n) ----
# per solid angle: c_n f^n * (1+eKY)(1+e^2H1^2Y^2/2);  c_n f0^n = c*J*f0/n = -c r^2 f^2 E0/n
cnf0n = -c*r**2*f**2*E0s/n
dphi = sp.Symbol('dphi')
fn_exp = cnf0n*sp.exp(-2*n*eps*dphi)            # f^n expansion around f0 (Y absorbed in dphi)
S2 = sp.expand(sp.series(fn_exp*(1+eps*K)*(1+eps**2*H1**2/2), eps, 0, 3).removeO()).coeff(eps, 2)
print("B3 source O(e^2) content:", sp.collect(S2, [H1**2, K, dphi**2]))
DA = S2.coeff(H1**2)
print("B3 H1^2 weight (true):", DA, "   N3 claim: +c r^2 f^2 E0/(4 n)")
Kcoup = S2.coeff(K)
print("B3 K coupling at O(e^2):", Kcoup)

# ---- H1 elimination with the banked C1 sector ----
A = (c/4)*f**2*r**2*pp**2
B = -4*A/(f*pp)              # reproduces banked weld H1 = 2 dt dphi/(f pp)
gam = B**2/(8*A)             # flip fact: B^2/(4A) = 2 gamma  => gamma = c r^2/2
print("B3 gamma from flip fact:", sp.simplify(gam), " (record: +(c/2) r^2)")
v = sp.Symbol('v')           # v := d_t dphi
Lh = A*H1**2 + B*H1*v + DA*H1**2
H1star = sp.solve(sp.diff(Lh, H1), H1)[0]
print("B3 H1* (true):", sp.simplify(H1star/v), "* d_t dphi")
H1_N3 = 2*pp/(f*(pp**2 + E0s/n))
print("B3 H1* N3 claim:", H1_N3, "* d_t dphi   (e^{2phi0}=1/f)")
print("B3 H1* ratio true/N3:", sp.simplify((H1star/v)/H1_N3))
# post-elimination kinetic coefficient
gam_eff = sp.simplify(gam - B**2/(4*(A+DA)))
print("B3 gamma_eff:", sp.factor(gam_eff))
zer = sp.solve(sp.Eq(gam_eff, 0), n)
print("B3 kinetic-coefficient zero at n =", zer, " ; on collar E0/pp^2 = 2(1-q)/q ->",
      [sp.simplify(z.subs(E0s, 2*(1-q)/q*pp**2)) for z in zer], "-> at q=1/3:",
      [sp.simplify(z.subs(E0s, 2*(1-q)/q*pp**2)).subs(q, sp.Rational(1,3)) for z in zer])
pole = sp.solve(sp.Eq(sp.together(A+DA), 0), n)
print("B3 H1*-pole (A+DA=0) at n =", pole, "-> collar:",
      [sp.simplify(z.subs(E0s, 2*(1-q)/q*pp**2)).subs(q, sp.Rational(1,3)) for z in pole])
# N3's claimed coincidence point:
print("B3 N3 claimed n* = E0/pp'^2 -> collar 2(1-q)/q at q=1/3 =",
      sp.simplify((2*(1-q)/q).subs(q, sp.Rational(1,3))), "(arithmetic only)")
# n->0 obstruction:
print("B3 n->0: H1^2 and K loadings ~ 1/n diverge:",
      sp.limit(DA, n, 0, '+'), ",", sp.limit(cnf0n, n, 0, '+'))

# ---- contravariant vs covariant delta T^{tr} ----
gtt, grr = -sp.exp(-2*phi), sp.exp(2*phi)
blk = sp.Matrix([[gtt, eps*H1], [eps*H1, grr]])
inv = blk.inv()
dg_tr_up = sp.series(inv[0,1], eps, 0, 2).removeO().coeff(eps, 1)
Ttt, Trr, dTtr = sp.symbols('T_tt T_rr dT_tr')
T = sp.Matrix([[Ttt, eps*dTtr], [eps*dTtr, Trr]])
Tup = inv*T*inv     # T^{ab} = g^{ac} g^{bd} T_cd
dT_up = sp.expand(sp.series(Tup[0,1], eps, 0, 2).removeO()).coeff(eps, 1)
print("B4/B3 split: dT^{tr} =", sp.simplify(dT_up))
X = sp.Symbol('X', positive=True)  # scalar kinetic: T^t_t = -X, T^r_r = +X
scalar = dT_up.subs({Ttt: -X*gtt, Trr: X*grr})
print("B3 split for C1 scalar-type bg (T^t_t=-T^r_r):", sp.simplify(scalar))
V = sp.Symbol('V', positive=True)  # potential: T^t_t = T^r_r = -V
pot = dT_up.subs({Ttt: -V*gtt, Trr: -V*grr})
print("B3 split for potential-type bg (T^t_t=T^r_r=-V):", sp.simplify(pot))

# ---- B4: dT^t_theta at first order ----
# even-parity scheme: no g_{t theta}, no g_{r theta} perturbation; bg T diagonal;
# T^t_th = g^{ta} T_{a th}: a=t -> dT_{t th}; a=r -> dg^{tr} * T_{r th}[bg](=0)
# potential source: T_{t th} = g_{t th} * (-V) = 0 at first order. Coordinate measure: no theta row at all.
print("B4: dT^t_theta[src] = g^{tt}*dT_{t th} + dg^{tr}*T_{r th}[bg] = g^{tt}*(-V*dg_{t th}) + 0 = 0  (dg_{t th}=0 in scheme)")

# ---- B5 flag-level ----
W = sp.Symbol('W')
print("B5 identity W^2/(1-W) == 1/(1-W) - 1 - W:",
      sp.simplify(W**2/(1-W) - (1/(1-W) - 1 - W)) == 0)
print("B5 series of W^2/(1-W):", sp.series(W**2/(1-W), W, 0, 5))
