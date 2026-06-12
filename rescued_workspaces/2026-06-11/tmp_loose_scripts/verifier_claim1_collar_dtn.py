"""BLIND VERIFIER — Claim 1: collar two-boundary DtN, off-diagonal decay,
diagonal asymptotics, Schur identity. Independent recomputation, mpmath.

Conventions derived from scratch:
  ODE (banked ~248):  a'' + (2 - q/2) a'/y - lam y^(q-2) a = 0,  q = 1/3
  SL form: (w a')' = lam v a,  w = y^(2-q/2) = y^(11/6),  v = y^(q/2)
  beta = q/2 = 1/6, x = sqrt(lam)/beta * y^beta, m = (1-2/q)/2 = -5/2, nu = 5/2
  F = x^m I_nu(x) (regular at y->0), G = x^m K_nu(x)
  Fluxes (outward): p_0 = +w(1) a'(1),  p_c = -w(y_c) a'(y_c)
  DtN matrix Lam: (p_c, p_0)^T = Lam (u_c, u_0)^T
"""
import mpmath as mp

mp.mp.dps = 60

q = mp.mpf(1)/3
beta = q/2
m = (1 - 2/q)/2          # -5/2
nu = abs(m)              # 5/2
P = 2 - q/2              # 11/6  (first-derivative coefficient)

def w(y): return y**(2 - q/2)

def xofy(lam, y): return mp.sqrt(lam)/beta * y**beta

def F(lam, y):
    x = xofy(lam, y)
    return x**m * mp.besseli(nu, x)

def G(lam, y):
    x = xofy(lam, y)
    return x**m * mp.besselk(nu, x)

def dFdy(lam, y):
    return mp.diff(lambda t: F(lam, t), y)

def dGdy(lam, y):
    return mp.diff(lambda t: G(lam, t), y)

def ode_residual(lam, y, f):
    a   = f(lam, y)
    a1  = mp.diff(lambda t: f(lam, t), y)
    a2  = mp.diff(lambda t: f(lam, t), y, 2)
    return a2 + P*a1/y - lam * y**(q-2) * a

print("== 1. ODE residual check (relative) ==")
for lam in [mp.mpf(2), mp.mpf(6), mp.mpf(12)]:
    for y in [mp.mpf('0.3'), mp.mpf('0.7'), mp.mpf(1)]:
        rF = ode_residual(lam, y, F)/F(lam, y)
        rG = ode_residual(lam, y, G)/G(lam, y)
        print(f"  lam={float(lam):4.0f} y={float(y):.2f}  resF={mp.nstr(rF,3)}  resG={mp.nstr(rG,3)}")

print("\n== 2. Banked D(lam) check ==")
def Dlam(lam):
    x1 = 6*mp.sqrt(lam)
    return mp.sqrt(lam)*mp.besseli(mp.mpf(7)/2, x1)/mp.besseli(mp.mpf(5)/2, x1)
D1 = Dlam(2)
print("  D(2) =", mp.nstr(D1, 20), " banked 0.979663326283 -> diff:",
      mp.nstr(D1 - mp.mpf('0.979663326283'), 3))
# independent: log-derivative of F at y=1
ld = dFdy(2, mp.mpf(1))/F(2, mp.mpf(1))
print("  a'(1)/a(1) regular branch =", mp.nstr(ld, 20), " diff vs D(2):", mp.nstr(ld - D1, 3))

print("\n== 3. Wronskian constant W0 = w (F G' - G F') ==")
for lam in [mp.mpf(2), mp.mpf(6)]:
    vals = []
    for y in [mp.mpf('0.05'), mp.mpf('0.4'), mp.mpf(1)]:
        W = w(y)*(F(lam,y)*dGdy(lam,y) - G(lam,y)*dFdy(lam,y))
        vals.append(W)
    pred = -beta * (mp.sqrt(lam)/beta)**(2*m)
    pred_claim = beta * (mp.sqrt(lam)/beta)**(2*m)   # claimed sign
    print(f"  lam={float(lam):4.0f}: W0 sampled {[mp.nstr(v,12) for v in vals]}")
    print(f"     my analytic -beta(sqrt(lam)/beta)^(2m) = {mp.nstr(pred,12)}; claimed +: {mp.nstr(pred_claim,12)}")

def dtn_matrix(lam, yc):
    """exact 2x2 DtN from Bessel solutions"""
    Fc, F0 = F(lam,yc), F(lam,mp.mpf(1))
    Gc, G0 = G(lam,yc), G(lam,mp.mpf(1))
    dFc, dF0 = dFdy(lam,yc), dFdy(lam,mp.mpf(1))
    dGc, dG0 = dGdy(lam,yc), dGdy(lam,mp.mpf(1))
    Delta = Fc*G0 - Gc*F0
    # solution a = [u_c (G0 F - F0 G) + u_0 (Fc G - Gc F)] / Delta
    L00 = w(1)*(Fc*dG0 - Gc*dF0)/Delta              # coeff of u_0 in p_0
    b0c = w(1)*(G0*dF0 - F0*dG0)/Delta              # coeff of u_c in p_0
    Lcc = -w(yc)*(G0*dFc - F0*dGc)/Delta            # coeff of u_c in p_c
    bc0 = -w(yc)*(Fc*dGc - Gc*dFc)/Delta            # coeff of u_0 in p_c
    return Lcc, b0c, bc0, L00, Delta

print("\n== 4. Symmetry + independent ODE-shooting cross-check ==")
lam = mp.mpf(2); yc = mp.mpf('0.2')
Lcc, b1, b2, L00, Delta = dtn_matrix(lam, yc)
print("  Bessel DtN (l=1, yc=0.2): Lcc=%s b(p0<-uc)=%s b(pc<-u0)=%s L00=%s" %
      (mp.nstr(Lcc,15), mp.nstr(b1,15), mp.nstr(b2,15), mp.nstr(L00,15)))
print("  symmetry b-b' =", mp.nstr(b1-b2, 3))
# Independent: integrate ODE numerically from yc with two ICs (Taylor via odefun)
def shoot(lam, yc, a0, ap0):
    f = mp.odefun(lambda y, Y: [Y[1], -P*Y[1]/y + lam*y**(q-2)*Y[0]],
                  yc, [a0, ap0], tol=mp.mpf(10)**(-40))
    return f
s1 = shoot(lam, yc, mp.mpf(1), mp.mpf(0))
s2 = shoot(lam, yc, mp.mpf(0), mp.mpf(1))
# solution with u_c=1,u_0=0: a = s1 + c s2 with s1(1)+c s2(1)=0
v11, v12 = s1(mp.mpf(1)); v21, v22 = s2(mp.mpf(1))
c = -v11/v21
Lcc_num = -w(yc)*(0 + c*1)          # p_c = -w(yc) a'(yc), a'(yc)=0 + c*1
b1_num  = w(1)*(v12 + c*v22)        # p_0 coeff of u_c
# u_c=0,u_0=1: a = d s2 with d s2(1)=1... need also s1 comb: a = e s1 + d s2, a(yc)=e=0
d = 1/v21
b2_num  = -w(yc)*d                  # p_c = -w(yc) a'(yc) = -w(yc)*d
L00_num = w(1)*d*v22
print("  ODE-shoot   DtN:          Lcc=%s b=%s b'=%s L00=%s" %
      (mp.nstr(Lcc_num,15), mp.nstr(b1_num,15), mp.nstr(b2_num,15), mp.nstr(L00_num,15)))
print("  max |Bessel - shoot| =", mp.nstr(max(abs(Lcc-Lcc_num), abs(b1-b1_num),
                                              abs(b2-b2_num), abs(L00-L00_num)), 3))

print("\n== 5. b = W0/Delta exact identity check ==")
for lam, yc in [(mp.mpf(2), mp.mpf('0.2')), (mp.mpf(6), mp.mpf('0.05')), (mp.mpf(12), mp.mpf('0.5'))]:
    Lcc, b1, b2, L00, Delta = dtn_matrix(lam, yc)
    W0 = w(mp.mpf(1))*(F(lam,1)*dGdy(lam,mp.mpf(1)) - G(lam,1)*dFdy(lam,mp.mpf(1)))
    print(f"  lam={float(lam):4.0f} yc={float(yc):5.2f}:  b={mp.nstr(b1,15)}  -W0/Delta={mp.nstr(-W0/Delta,15)}"
          f"  +W0/Delta={mp.nstr(W0/Delta,15)}")

print("\n== 6. Asymptotics yc->0:  b*yc^(-5/6), Lcc*yc^(-5/6), L00-D(lam) ==")
claim = {1: mp.mpf('-0.0203697387'), 2: mp.mpf('-0.000180418048')}
for ell in [1, 2, 3]:
    lam = mp.mpf(ell*(ell+1))
    print(f"  ell={ell} (lam={int(lam)}):")
    for k in [3, 6, 9, 12, 15]:
        yc = mp.mpf(10)**(-k)
        Lcc, b1, b2, L00, Delta = dtn_matrix(lam, yc)
        print(f"    yc=1e-{k:02d}: b*yc^(-5/6) = {mp.nstr(b1*yc**(mp.mpf(-5)/6), 12)}"
              f"   Lcc*yc^(-5/6) = {mp.nstr(Lcc*yc**(mp.mpf(-5)/6), 12)}"
              f"   L00-D = {mp.nstr(L00 - Dlam(lam), 3)}")
    # analytic limit: -1/(6 Gamma(5/2) 2^(3/2) F(1))
    lim = -1/(6*mp.gamma(mp.mpf(5)/2)*2**mp.mpf(1.5)*F(lam, mp.mpf(1)))
    print(f"    analytic limit -1/(6 G(5/2) 2^(3/2) F_l(1)) = {mp.nstr(lim, 12)}")
    if ell in claim:
        print(f"    claimed constant: {mp.nstr(claim[ell],12)}  diff: {mp.nstr(lim-claim[ell],3)}")

print("\n== 7. ratio b/Lcc as yc->0 (flat-direction diagnostic) ==")
for ell in [1, 2]:
    lam = mp.mpf(ell*(ell+1))
    for k in [6, 12]:
        yc = mp.mpf(10)**(-k)
        Lcc, b1, _, L00, _ = dtn_matrix(lam, yc)
        corr2 = b1*b1/(Lcc*L00)
        print(f"  ell={ell} yc=1e-{k:02d}: b/Lcc = {mp.nstr(b1/Lcc,10)}  b^2/(Lcc*L00) = {mp.nstr(corr2,6)}"
              f"  schur-shift b^2/Lcc = {mp.nstr(b1*b1/Lcc,6)}")

print("\n== 8. Schur identity: L00 - b^2/Lcc == Neumann-inner DtN (exact at finite yc) ==")
for lam, yc in [(mp.mpf(2), mp.mpf('0.3')), (mp.mpf(2), mp.mpf('0.05')),
                (mp.mpf(6), mp.mpf('0.3')), (mp.mpf(12), mp.mpf('0.1'))]:
    Lcc, b1, b2, L00, Delta = dtn_matrix(lam, yc)
    schur = L00 - b1*b2/Lcc
    # Neumann at yc: a = alpha F + gamma G with a'(yc)=0 -> alpha dFc + gamma dGc = 0
    dFc, dGc = dFdy(lam, yc), dGdy(lam, yc)
    alpha, gamma_ = dGc, -dFc
    aN  = alpha*F(lam,1) + gamma_*G(lam,1)
    aNp = alpha*dFdy(lam,mp.mpf(1)) + gamma_*dGdy(lam,mp.mpf(1))
    DN = w(1)*aNp/aN
    print(f"  lam={float(lam):4.0f} yc={float(yc):5.2f}: Schur={mp.nstr(schur,25)}  D_Neu={mp.nstr(DN,25)}"
          f"  diff={mp.nstr(schur-DN,3)}")
