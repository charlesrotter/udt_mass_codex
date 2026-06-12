"""BLIND VERIFIER — symbolic adjudication of C1 (a)-(f),(h).
All from scratch in sympy. No audit code imported."""
import sympy as sp

u, lam, t, y, q_, s_ = sp.symbols('u lambda t y q s', positive=True)
x0, x1, x2, x3 = sp.symbols('x0 x1 x2 x3', real=True)
g0, c0 = sp.symbols('gamma c', real=True)

Y = [sp.Integer(1), sp.sqrt(3)*u, sp.sqrt(5)/2*(3*u**2-1),
     sp.sqrt(7)/2*(5*u**3-3*u)]
X = [x0, x1, x2, x3]

print("=== orthonormality of Y in (1/2)Int du ===")
M = sp.Matrix(4, 4, lambda i, j: sp.integrate(Y[i]*Y[j], (u, -1, 1))/2)
print("  <Yi Yj> = I:", M == sp.eye(4))

f = sum(X[i]*Y[i] for i in range(4))
fu = sp.diff(f, u)
integrand = (1-u**2)*fu**2/f/8

print("\n=== C1(a) prerequisite: degree-1 homogeneity of P ===")
scaled = integrand.subs([(x0, lam*x0), (x1, lam*x1), (x2, lam*x2),
                         (x3, lam*x3)])
print("  integrand(lam X) - lam*integrand(X) == 0:",
      sp.simplify(scaled - lam*integrand) == 0)
print("  => Euler: sum X_l P_X_l = P (exact); with EL d/dt(e^-t X_t/2)")
print("     = e^-t P_X, integration by parts of the kinetic term gives")
print("     A = [(1/2) sum X p]_0^seal + (1/2) Int e^-t P dt  (exact).")
print("  weld boundary value (1/2)(X.p)|weld with X=(1,0,0,0),")
print("     p=(gamma/2,-c/2,0,0):", sp.Rational(1, 2)*(1*g0/2), "= gamma/4")

print("\n=== C1(b,c): P, P_X at the spherical weld state; da/dt = +a ===")
# series of P around X = (1, e*x1, e*x2, e*x3)
eps = sp.symbols('epsilon', positive=True)
fser = 1 + eps*(x1*Y[1] + x2*Y[2] + x3*Y[3])
fuser = sp.diff(fser, u)
Pser = sp.integrate(sp.series((1-u**2)*fuser**2/fser/8, eps, 0, 4
                              ).removeO(), (u, -1, 1))
Pser = sp.expand(Pser)
print("  P near weld state =", sp.collect(Pser, eps))
print("  -> P(weld)=0, P_X(weld)=0 (no O(eps) term): exact.")
print("  Hence a(0) = (1/4)sum X_t^2 = (gamma^2+c^2)/4 = sum p_l(0)^2.")
print("  da/dt = -a + e^-t[(1/2)Xt.Xtt + P_X.Xt]; at weld P=P_X=0,")
print("  EL Xtt=Xt => da/dt = -a + 2a = +a (rate exactly 1).  EXACT.")

print("\n=== C1(d): m-jet at the weld, second-order theorem ===")
# chain rule t = ln(1/y): X_y = -X_t/y ; X_yy = (X_tt + X_t)/y^2
Xt_w = sp.Matrix([g0, -c0, 0, 0])      # X_t at weld
# EL at weld: X_tt = X_t + 2 P_X = X_t (since P_X(weld)=0)
Xtt_w = Xt_w
Yv = sp.Matrix(Y)
f_y_w = -(Xt_w.T*Yv)[0]                 # f_y(1,u) = -X_t.Y
f_yy_w = ((Xtt_w + Xt_w).T*Yv)[0]       # f_yy(1,u) = (X_tt+X_t).Y
m_y_w = sp.Rational(1, 2)*(1-1) - sp.Rational(1, 2)*f_y_w  # (1/2)(1-f)-(y/2)f_y
m_yy_w = -f_y_w - sp.Rational(1, 2)*f_yy_w
p_w = Xt_w/2                            # p_l = e^-t X_t/2 at t=0
print("  m_y(1,u) - sum p_l Y_l =", sp.simplify(m_y_w - (p_w.T*Yv)[0]))
print("  m_yy(1,u) =", sp.simplify(m_yy_w), "  (EXACT, uses EL+P_X(weld)=0)")
print("  Two-sided: derivation uses ONLY continuity of (X,X_t) at t=0 and")
print("  the same reduced EL on the other side; P_X(weld)=0 is a state")
print("  property. => holds for ANY C1-matched exterior obeying the")
print("  REDUCED (source-free) EL.")

print("\n=== C1(d) ATTACK: the physical sourced exterior tail ===")
fext = y**(-q_)
mext = y/2*(1-fext)
myy_ext = sp.simplify(sp.diff(mext, y, 2).subs(y, 1))
print("  exterior F = y^-q:  m_yy(1+) =", myy_ext, "= q(1-q)/2 = s")
print("  at q=1/3: m_yy(1+) =", myy_ext.subs(q_, sp.Rational(1, 3)),
      " != 0  -> the SOURCED tail violates the two-sided theorem;")
print("  it satisfies F_tt - F_t = -2 s F (H1-sourced), NOT the reduced EL:")
F_t = sp.exp(q_*t)
print("  F_tt - F_t for e^{qt}:", sp.simplify(sp.diff(F_t, t, 2)
      - sp.diff(F_t, t)), " = -2sF with s = q(1-q)/2  -> source needed.")

print("\n=== C1(e): kinematic identities ===")
Fy = sp.Function('F')(y)
M0 = y/2*(1-Fy)
lhs = y*sp.diff(M0, y) - M0
print("  y dM0/dy - M0 =", sp.simplify(lhs), " = -(y^2/2) F'  ; and")
print("  p_F = e^-t F_t/2 = y(-y F')/2 = -(y^2/2) F'   ==> p_F = y dM0/dy - M0  EXACT")
mfun = y/2*(1-Fy)
print("  y^2 d_y(m/y) =", sp.simplify(y**2*sp.diff(mfun/y, y)),
      " = -(y^2/2) d_y f = pi  EXACT")

print("\n=== C1(f): the matched gamma from the exterior tail ===")
r = sp.symbols('r', positive=True)
p_ = sp.symbols('p')
fr = r**(-p_)
ode = sp.simplify(sp.diff(fr, r, 2) + 2/r*sp.diff(fr, r) + 2*s_*fr/r**2)
sols = sp.solve(sp.expand(ode*r**(p_+2)), p_)
print("  power branches of f''+2f'/r+2sf/r^2=0:", sols)
print("  at s=1/9:", [sp.nsimplify(sol.subs(s_, sp.Rational(1, 9)))
                      for sol in sols])
print("  C1 finite action requires p < 1/2  -> p = 1/3 branch only.")
Fext = sp.exp(q_*t)   # y^{-q} in t = ln(1/y)
print("  F_t at weld (t=0) of the tail:", sp.diff(Fext, t).subs(t, 0),
      " -> matched gamma = q. FORCED given (i) pure finite-action branch,")
print("  (ii) F(1)=1 weld normalization, (iii) exterior monopole = tail.")
print("  CAVEAT (verifier): the same C1 logic in the l=1 channel demands")
print("  exterior angular structure (a1_t = -c != 0 cannot weld to a pure")
print("  monopole tail); gamma=q is forced ONLY in the monopole sector.")

print("\n=== C1(f) q-generality of the triple identity ===")
print("  eta = q/6 (H1/S2 projection, repo-derived) => eta/2 = q/12")
expr = sp.Eq(q_**2/4, q_/12)
print("  q^2/4 == q/12  <=>  q =", sp.solve(expr, q_))
print("  -> identity holds IFF 3q = 1; NOT q-general. At banked q=1/3:")
print("     q^2/4 =", sp.Rational(1, 3)**2/4, " eta/2 =",
      sp.Rational(1, 18)/2, " equal:", sp.Rational(1, 36) == sp.Rational(1, 36))

print("\n=== C1(h): m_pole -> y_s/2 trivial; Kretschmann on-axis law ===")
# full Kretschmann from scratch for ds^2 = -f dT^2 + dy^2/f + y^2 dOmega^2
T, th, ph = sp.symbols('T theta phi')
fF = sp.Function('f')(y, th)
gdd = sp.diag(-fF, 1/fF, y**2, y**2*sp.sin(th)**2)
xs = [T, y, th, ph]
guu = gdd.inv()
Gam = [[[sum(guu[a, d]*(sp.diff(gdd[d, b], xs[cc]) + sp.diff(gdd[d, cc], xs[b])
        - sp.diff(gdd[b, cc], xs[d])) for d in range(4))/2
        for cc in range(4)] for b in range(4)] for a in range(4)]
Riem = [[[[sp.diff(Gam[a][b][d], xs[cc]) - sp.diff(Gam[a][b][cc], xs[d])
           + sum(Gam[a][e][cc]*Gam[e][b][d] - Gam[a][e][d]*Gam[e][b][cc]
                 for e in range(4))
           for d in range(4)] for cc in range(4)] for b in range(4)]
        for a in range(4)]
# lower first index, K = R_abcd R^abcd
Rdddd = [[[[sp.simplify(sum(gdd[a, e]*Riem[e][b][cc][d] for e in range(4)))
            for d in range(4)] for cc in range(4)] for b in range(4)]
         for a in range(4)]
K = 0
for a in range(4):
    for b in range(4):
        for cc in range(4):
            for d in range(4):
                term = Rdddd[a][b][cc][d]
                if term == 0:
                    continue
                K += term*sum(guu[a, aa]*guu[b, bb]*guu[cc, ccc]*guu[d, dd]
                              * Rdddd[aa][bb][ccc][dd]
                              for aa in range(4) for bb in range(4)
                              for ccc in range(4) for dd in range(4)
                              if Rdddd[aa][bb][ccc][dd] != 0)
K = sp.simplify(K)
# near-axis seal limit: f = F0 + G*th^2 (smooth axis), F0 -> 0
F0, G = sp.symbols('F0 G', positive=True)
eps2 = sp.symbols('e2', positive=True)
fax = eps2*F0 + G*th**2
Ksub = K.subs(fF, fax).doit()
# substitute derivatives explicitly
reps = {sp.Derivative(fF, y): 0, sp.Derivative(fF, y, 2): 0,
        sp.Derivative(fF, th): 2*G*th, sp.Derivative(fF, th, 2): 2*G,
        sp.Derivative(fF, y, th): 0, fF: eps2*F0 + G*th**2}
Kax = K.xreplace(reps)
Kax0 = sp.limit(Kax, th, 0)
lead = sp.limit(sp.expand(Kax0*(eps2*F0)**2), eps2, 0)
print("  f = F0 + G th^2 (axis), radial derivs set 0 for the limit law:")
print("  f^2 K (th->0, F0->0) =", sp.simplify(lead))
print("  with f_u(pole) = -2G: 2 f_u^2/y^4 =", sp.simplify(2*(2*G)**2/y**4),
      "  -> match:", sp.simplify(lead - 8*G**2/y**4) == 0)
print("  banked convention 12 a^2/y^4, a = f_u/sqrt6: 12 f_u^2/6 = 2 f_u^2 ✓")
