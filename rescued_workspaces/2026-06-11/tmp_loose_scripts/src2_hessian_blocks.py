"""SCRIPT 2 (optimized) — exact Hessian blocks of the C1 angular sector on the
ell=1 background, closed form in kappa.  See header of previous version.

H_ij = (1/4) int dOmega [ 2 grad(Yi).grad(Yj)/B
                          - 2 F kap (1-c^2) (Yi_c Yj + Yj_c Yi)/B^2
                          + 2 (1-c^2) F^2 kap^2 Yi Yj / B^3 ],   B = F(1+kap c).
Convention: Q2 = (1/2) sum H_ij x_i x_j  (so H is the literal Hessian of Q2).
"""
import sympy as sp, time

PASS = 0; FAIL = 0
def check(name, expr_zero):
    global PASS, FAIL
    ok = sp.simplify(expr_zero) == 0
    if ok: PASS += 1
    else: FAIL += 1
    print(("PASS " if ok else "FAIL ") + name)
    if not ok: print("   residual:", sp.simplify(expr_zero))

c, ph = sp.symbols('c phi', real=True)
kap = sp.Symbol('kappa', positive=True)
F, a = sp.symbols('F a', positive=True)

Y = {
 'u' : sp.S(1)/sp.sqrt(4*sp.pi) * sp.sqrt(4*sp.pi),  # = 1 (the ell=0 radial fluct enters as u*1)
}
Y['u']  = sp.S(1)
Y['a0'] = sp.sqrt(sp.S(3)/(4*sp.pi))*c
Y['a1'] = sp.sqrt(sp.S(3)/(4*sp.pi))*sp.sqrt(1-c**2)*sp.cos(ph)
Y['g0'] = sp.sqrt(sp.S(5)/(16*sp.pi))*(3*c**2-1)
Y['g1'] = sp.sqrt(sp.S(15)/(4*sp.pi))*c*sp.sqrt(1-c**2)*sp.cos(ph)
Y['g2'] = sp.sqrt(sp.S(15)/(16*sp.pi))*(1-c**2)*sp.cos(2*ph)

B = F*(1+kap*c)

def grad_dot(g, h):
    return (1-c**2)*sp.diff(g, c)*sp.diff(h, c) + sp.diff(g, ph)*sp.diff(h, ph)/(1-c**2)

def Hij(i, j):
    Yi, Yj = Y[i], Y[j]
    integ = ( 2*grad_dot(Yi, Yj)/B
              - 2*F*kap*(1-c**2)*(sp.diff(Yi,c)*Yj + sp.diff(Yj,c)*Yi)/B**2
              + 2*(1-c**2)*F**2*kap**2*Yi*Yj/B**3 )
    integ = sp.expand_trig(sp.expand(integ))
    iphi = sp.integrate(integ, (ph, 0, 2*sp.pi))
    iphi = sp.cancel(sp.expand(iphi))
    val  = sp.integrate(iphi, (c, -1, 1))
    return sp.Rational(1,4)*sp.simplify(sp.factor(sp.cancel(sp.together(val))))

pairs = [('u','u'),('u','a0'),('u','g0'),('a0','a0'),('a0','g0'),
         ('a1','a1'),('a1','g1'),('g0','g0'),('g1','g1'),('g2','g2')]
H = {}
print("== exact closed-form entries (B = F(1+kappa c)) ==")
for (i,j) in pairs:
    t0 = time.time()
    H[(i,j)] = Hij(i,j)
    lead = sp.simplify(sp.series(H[(i,j)], kap, 0, 3).removeO())
    print(f"  H[{i},{j}]: leading = {lead}   ({time.time()-t0:.1f}s)")

print("\n== superselection spot checks (must vanish identically) ==")
for (i,j) in [('u','a1'),('a0','a1'),('a1','g0'),('a1','g2'),('g0','g1'),('g1','g2'),('u','g1'),('u','g2')]:
    v = Hij(i,j)
    check(f"H[{i},{j}] == 0", v)

print("\n== kappa->0 limits ==")
check("H[u,u](0)=0", H[('u','u')].subs(kap,0))
check("H[a0,a0](0)=1/F", sp.simplify(H[('a0','a0')].subs(kap,0)-1/F))
check("H[a1,a1](0)=1/F", sp.simplify(H[('a1','a1')].subs(kap,0)-1/F))
check("H[g0,g0](0)=3/F", sp.simplify(H[('g0','g0')].subs(kap,0)-3/F))
check("H[g1,g1](0)=3/F", sp.simplify(H[('g1','g1')].subs(kap,0)-3/F))
check("H[g2,g2](0)=3/F", sp.simplify(H[('g2','g2')].subs(kap,0)-3/F))

print("\n== exact identities against the background potential P(F,a) ==")
G1 = (2*kap + (kap-1)*(kap+1)*(sp.log(1+kap)-sp.log(1-kap)))/kap**3
kap_def = a*sp.sqrt(3/(4*sp.pi))/F
P = 3*a**2/(2*F) * G1.subs(kap, kap_def)
check("H[a1,a1] == (1/4)(dP/da)/a   [rotation zero-mode identity, EXACT]",
      sp.simplify(H[('a1','a1')].subs(kap, kap_def) - sp.Rational(1,4)*sp.diff(P, a)/a))
check("H[a0,a0] == (1/4) d2P/da2   [longitudinal]",
      sp.simplify(H[('a0','a0')].subs(kap, kap_def) - sp.Rational(1,4)*sp.diff(P, a, 2)))
check("H[u,a0]  == (1/4) d2P/dFda  [q-amplitude cross]",
      sp.simplify(H[('u','a0')].subs(kap, kap_def) - sp.Rational(1,4)*sp.diff(P, F, a)))
check("H[u,u]   == (1/4) d2P/dF2   [radial from angular sector]",
      sp.simplify(H[('u','u')].subs(kap, kap_def) - sp.Rational(1,4)*sp.diff(P, F, 2)))

print("\n== gamma0 tadpole (ell=2 demand of the truncated background) ==")
g0s = sp.Symbol('g0s')
fB2 = B + g0s*Y['g0']
numfull = grad_dot(fB2, fB2)/fB2
num1 = sp.expand(sp.diff(numfull, g0s).subs(g0s, 0))
iphi = sp.integrate(num1, (ph, 0, 2*sp.pi))
Tg0 = sp.Rational(1,4)*sp.factor(sp.cancel(sp.together(sp.integrate(sp.cancel(sp.expand(iphi)), (c, -1, 1)))))
print("  T_g0 exact:", Tg0)
print("  T_g0 leading kappa:", sp.simplify(sp.series(Tg0, kap, 0, 4).removeO()))

print("\n== demanded-background evaluation (q=1/3, lam=2, s=1/9, eta=1/18) ==")
y = sp.Symbol('y', positive=True)
Fy  = y**(-sp.Rational(1,3))
ay  = 2*sp.sqrt(sp.Rational(1,18))*y**(-sp.Rational(1,2))
kapy = sp.simplify(ay*sp.sqrt(3/(4*sp.pi))/Fy)
k1 = float(kapy.subs(y,1)); ystar = float(sp.solve(sp.Eq(kapy,1), y)[0])
print(f"  kappa(y) = {float(sp.simplify(kapy/y**(-sp.Rational(1,6)))):.6f} * y^(-1/6);  kappa(1)={k1:.6f};  y_*(kappa=1)={ystar:.3e};  ln y_* = {sp.log(sp.Symbol('x')).subs(sp.Symbol('x'),ystar):.4f}")
subs_bg = [(kap, kapy), (F, Fy)]
import math
print(f"  ln y_* = {math.log(ystar):.4f}")
for (i,j) in pairs:
    prof = H[(i,j)].subs(subs_bg)
    v1 = float(prof.subs(y, 1))
    vh = float(prof.subs(y, sp.Rational(1,10)))
    print(f"  V[{i},{j}](y=1) = {v1:+.6f}    V(y=0.1) = {vh:+.6f}")

print("\n== leading kappa-Taylor on background, symbolic y ==")
for (i,j) in pairs:
    lead = sp.expand(sp.series(H[(i,j)], kap, 0, 3).removeO())
    prof = sp.simplify(lead.subs(subs_bg))
    print(f"  V[{i},{j}] ~ {prof}")

print(f"\nTOTALS: PASS={PASS} FAIL={FAIL}")
