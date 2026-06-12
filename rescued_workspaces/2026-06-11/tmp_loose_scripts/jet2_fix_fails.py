"""Repair harness artifacts for S6, S9, S10 (independent re-checks)."""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40
PASS=[];FAIL=[]
def check(name, ok):
    (PASS if ok else FAIL).append(name); print(("PASS " if ok else "FAIL ")+name)

# ---- S6 numeric: u = y^{-1/2} I_nu((2 sqrt(lam)/q) y^{q/2}) solves (y^2 u')' = (lam y^q + mu) u,
#      nu = sqrt(1+4mu)/q ; random q, n, lam, y at 40 digits.
def resid(qv, nv, lmv, yv):
    sv = qv*(1-qv)/2
    muv = 2*(1-nv)*sv
    nuv = mp.sqrt(1+4*muv)/qv
    u  = lambda yy: yy**mp.mpf('-0.5') * mp.besseli(nuv, (2*mp.sqrt(lmv)/qv)*yy**(qv/2))
    # (y^2 u')' - (lam y^q + mu) u  via high-precision numeric differentiation
    g  = lambda yy: yy**2 * mp.diff(u, yy)
    return mp.diff(g, yv) - (lmv*yv**qv + muv)*u(yv)
ok = True
for (qv,nv,lmv,yv) in [(mp.mpf(1)/3, 1, 2, mp.mpf('0.41')),
                        (mp.mpf(1)/3, 0, mp.mpf(1)/2, mp.mpf('0.73')),
                        (mp.mpf(1)/3, -1, 2, mp.mpf('0.59')),
                        (mp.mpf('0.4'), mp.mpf('0.27'), mp.mpf('1.7'), mp.mpf('0.66'))]:
    r = resid(qv,nv,lmv,yv)
    ok = ok and abs(r) < mp.mpf('1e-25')
check("S6' Bessel solution of sourced f-form EL, nu = sqrt(1+4mu)/q (4 random configs, <1e-25)", ok)

# ---- S9 symbolic redo with proper Euler operator
y,q,e,lam = sp.symbols('y q epsilon lamda', positive=True)
A = sp.Function('A')(y)
f0 = y**(-q); phi0 = q*sp.log(y)/2; s = q*(1-q)/2; K = 2*s*y**(-2*q)
phi_e = phi0 + e*A
L_hyb = sp.exp(-2*phi_e)*(f0*sp.diff(phi_e,y)**2)*y**2
tot1 = sp.expand(sp.diff(L_hyb + K*phi_e, e).subs(e,0))
res_hyb = sp.simplify(tot1.diff(A) - sp.diff(tot1.diff(sp.diff(A,y)), y))
print("    hybrid jet-1 bulk residual (n=0 completion) =", sp.simplify(res_hyb))
check("S9' hybrid residual = (q^2/2) y^{-2q} != 0  (hybrid off-shell under n=0 completion)",
      sp.simplify(res_hyb - q**2*y**(-2*q)/2) == 0)
# n=1 completion: source = c1*f = J*f0*e^{-2 e A} contributes d/de at 0: -2 J f0 A = +2 s y^{-2q} A
tot1b = sp.expand(sp.diff(L_hyb + (-s*y**(-q))*f0*sp.exp(-2*e*A), e).subs(e,0))
res_hyb_f = sp.simplify(tot1b.diff(A) - sp.diff(tot1b.diff(sp.diff(A,y)), y))
check("S9'' hybrid residual under n=1 completion also != 0", sp.simplify(res_hyb_f) != 0)
print("    hybrid jet-1 bulk residual (n=1 completion) =", sp.simplify(res_hyb_f))

# ---- S10 with unrestricted symbol
qq = sp.Symbol('q')
sols = sorted(sp.solve(sp.Eq(qq*(1-qq)/2, qq/3), qq))
check("S10' q(1-q)/2 = q/3 iff q in {0, 1/3}", sols == [0, sp.Rational(1,3)])

print("TOTAL: %d PASS, %d FAIL" % (len(PASS), len(FAIL)))
if FAIL: print("FAILED:", FAIL)
