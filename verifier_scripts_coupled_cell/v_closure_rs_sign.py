# CLAIM 4 ATTACK: is rs<0 forced, or a BC artifact of phi(r_int)=0?
# And CLAIM 3 continued: does requiring core-regularity + seal BC overdetermine
# the static coupled solution (-> discrete params) or leave a free family?
import sympy as sp
r, xi, rs, delta, rc, ri, p = sp.symbols('r xi rs delta r_core r_int p', positive=True)

# Static coupled t-equation integrates to areal mass:
#   m_areal(r) = delta*(r - r_core) + r_core*(1 - e^{-2p}) + rs
# with e^{-2phi}(r) = 1 - m_areal(r)/r.
e2p = sp.exp(-2*p)
m_areal = delta*(r-rc) + rc*(1-e2p) + rs

# core depth BC: e^{-2phi}(rc) = e^{-2p}  =>  1 - m_areal(rc)/rc = e^{-2p}
core_cond = sp.simplify( (1 - m_areal.subs(r,rc)/rc) - e2p )
print("Core-depth BC residual (should fix nothing extra):", sp.simplify(core_cond))
# solve for rs from core condition:
rs_core = sp.solve(sp.Eq(1 - m_areal.subs(r,rc)/rc, e2p), rs)
print("rs from core BC:", rs_core)   # => rs = 0 ? check

# interface BC: phi(r_int)=0 => e^{-2phi}(ri)=1 => m_areal(ri)=0
rs_int = sp.solve(sp.Eq(m_areal.subs(r,ri), 0), rs)[0]
print("rs forced by phi(r_int)=0 :", sp.simplify(rs_int))
print("  sign: delta>0,p>0 => m without rs at r_int =",
      sp.simplify(delta*(ri-rc)+rc*(1-e2p)), " >0 => rs<0 forced. CONFIRM rs<0.")

# --- Test ALTERNATIVE native closures (BC-dependence of rs<0) ---
print()
print("=== Alternative seal: mirror-fold NEUMANN on phi (dphi/dr=0 at r_int), rs free ===")
# e^{-2phi}=1-m_areal/r ; dphi/dr=0  <=> d/dr(e^{-2phi})=0
em2 = 1 - m_areal/r
dem2 = sp.diff(em2, r)
neu = sp.solve(sp.Eq(dem2.subs(r,ri),0), rs)
print(" d(e^{-2phi})/dr=0 at r_int -> rs =", [sp.simplify(s) for s in neu])
# evaluate its sign
if neu:
    rsN=sp.simplify(neu[0])
    print("   rs(Neumann) =", rsN, " sign for delta,p>0, ri>rc:",
          sp.simplify(rsN.subs({delta:sp.Rational(1,10),p:1,rc:sp.Rational(1,1000),ri:1,xi:sp.Rational(1,10)})))

print()
print("=== No interface pin at all (rs=0, just truncate at r_int) ===")
print(" m_areal(ri) with rs=0 =", sp.simplify(m_areal.subs(rs,0)),
      " >0 => phi(r_int)<0 (deficit persists). rs<0 only needed IF you demand phi=0.")
