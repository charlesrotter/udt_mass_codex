import sympy as sp

x, r = sp.symbols('x', real=True), sp.symbols('r', positive=True)
q, s = sp.symbols('q s', real=True)
R, r_in = sp.symbols('R r_in', positive=True)
A, B = sp.symbols('A B', real=True)

print("== CHECK A: demand ==")
fss = sp.exp(-q*x)
res = sp.simplify((sp.diff(fss,x,2)+sp.diff(fss,x)+2*s*fss)/fss)
print("residual:", res, "; s solve:", sp.solve(res, s))

print("\n== CHECK C: supply=demand ==")
print("solutions of q(1-q)/2 = q/3:", sp.solve(sp.Eq(q*(1-q)/2, q/3), q))
print("flow q^2-q+2q/3 =", sp.factor(q**2-q+2*q/3))

print("\n== D1: roots at s=1/9 ==")
m = sp.symbols('m')
print("roots of m^2+m+2/9:", sp.solve(m**2+m+sp.Rational(2,9), m))
fg = A*r**sp.Rational(-1,3)+B*r**sp.Rational(-2,3)
res2 = sp.simplify(r*sp.diff(r*sp.diff(fg,r),r)+r*sp.diff(fg,r)+sp.Rational(2,9)*fg)
print("residual of general sol:", res2)
# cross-check against doc form f'' + 2f'/r + 2sf/r^2 = 0:
res3 = sp.simplify(sp.diff(fg,r,2)+2*sp.diff(fg,r)/r+sp.Rational(2,9)*fg/r**2)
print("residual in doc form f''+2f'/r+2sf/r^2:", res3)
# also: are the two radial forms equivalent? r d/dr(r d/dr f) + r f' = r^2 f'' + 2 r f'
ff = sp.Function('f')(r)
lhs = r*sp.diff(r*sp.diff(ff,r),r) + r*sp.diff(ff,r)
print("collar-eq operator in r:", sp.expand(lhs), " (matches r^2(f''+2f'/r))")

print("\n== D2/D3 ==")
pv = sp.Rational(1,3)
h = sp.expand(fg/(R/r)**pv)
print("h(r) with p=1/3:", h)
Ap, Bp = sp.symbols("Ap Bp", real=True)
sol = sp.solve([sp.Eq(Ap+Bp*R**sp.Rational(-1,3),1), sp.Eq(Ap+Bp*r_in**sp.Rational(-1,3),1)], [Ap,Bp], dict=True)
print("two-end pinning solution (r_in != R):", sol)

print("\n== D4 ==")
p = sp.symbols('p', positive=True)
print("Int_0^1 r^{-4/3} dr =", sp.integrate(r**sp.Rational(-4,3), (r,0,1)))
print("Int_0^1 r^{-2/3} dr =", sp.integrate(r**sp.Rational(-2,3), (r,0,1)))

print("\n== E1 identity ==")
fs, fps, ql = sp.symbols('fs fps ql')
ls = (1-fs-r*fps).subs(fps, -ql*fs/r)
print("local share:", sp.simplify(ls), "; minus q factored:", sp.factor(sp.simplify(ls)-ql))

print("\n== ATTACK C: free-p normalization ==")
# given B != 0, choose p* = ln f(r_in)/ln(R/r_in) with f(R)=1 normalization
# concrete numbers: R=1, r_in=exp(-3), pick B
import math
Rv, riv = 1.0, math.exp(-3.0)
for Bv in [0.2, -0.1, 0.05]:
    Av = 1.0 - Bv          # f(R)=1 with R=1
    fin = Av*riv**(-1/3.) + Bv*riv**(-2/3.)
    pstar = math.log(fin)/math.log(Rv/riv)
    # h(r) = f(r) (r/R)^{p*}; check h at both ends
    hR = (Av*Rv**(-1/3.)+Bv*Rv**(-2/3.))*(Rv/Rv)**pstar
    hin = fin*(riv/Rv)**pstar
    # delta_h = -d ln h/d ln r |_R = q_phi0 - p*
    qphi0 = (Av/3.+2*Bv/3.)/(Av+Bv)   # -r f'/f at r=R=1
    dh = qphi0 - pstar
    print(f"B={Bv:+.2f}: p*={pstar:.6f} (≠1/3), h(R)={hR:.6f}, h(r_in)={hin:.6f}, "
          f"q_phi0={qphi0:.6f}, delta_h={dh:+.6f}")
print("=> y=0 at BOTH ends achievable for ANY on-shell f by choosing p;")
print("   then p≠1/3 and q_phi0=p*+delta_h still carries the B-mode.")
