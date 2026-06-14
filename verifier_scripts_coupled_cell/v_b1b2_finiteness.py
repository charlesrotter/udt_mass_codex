import sympy as sp
r, xi, rs, delta, rc, ri, p, R = sp.symbols('r xi rs delta r_core r_int p R', positive=True)

# ===== CLAIM 1: CELL FINITIZES =====
# rho = xi/r^2 ; bare coordinate measure 4 pi r^2 dr
integrand = (xi/r**2) * 4*sp.pi*r**2
print("CLAIM1 integrand rho*4pi r^2 =", sp.simplify(integrand), " (constant in r?)",
      sp.simplify(sp.diff(integrand, r))==0)
E = sp.integrate(integrand, (r, rc, ri))
print("CLAIM1 E_coord =", sp.simplify(E), " == 4 pi xi (r_int-r_core)?",
      sp.simplify(E - 4*sp.pi*xi*(ri-rc))==0)
# divergence as r_core -> 0 ?
print("CLAIM1 limit r_core->0:", sp.limit(E, rc, 0), " (finite => no 1/r_core div)")

# Misner-Sharp version with bare m(r)=int rho 4pi r^2 dr (G=c=1 schematic)
mMS = sp.integrate((xi/r**2)*4*sp.pi*r**2, (r, rc, r))
print("CLAIM1 m_MS(r) =", sp.simplify(mMS), " finite, linear in width.")

# Proper-volume check with deep log background phi = -p ln(ri/r) => e^{+phi}=(r/ri)^? 
# proper radial measure e^{phi} dr with phi = -p ln(ri/r) => e^{phi}=(ri/r)^{-p}=(r/ri)^p
phi_bg = -p*sp.ln(ri/r)
ephi = sp.exp(phi_bg)
print("e^{phi} =", sp.simplify(ephi))
integ_proper = (xi/r**2)*4*sp.pi*r**2*ephi   # rho * 4pi r^2 * e^{phi}
Eproper = sp.integrate(integ_proper, (r, rc, ri))
print("CLAIM1 E_proper(p) =", sp.simplify(Eproper))
print("   limit r_core->0 (p>0):", sp.limit(Eproper, rc, 0))
print("   p=1 numeric over (1e-3,1), xi=0.1:",
      float(Eproper.subs({p:1, ri:1, rc:sp.Rational(1,1000), xi:sp.Rational(1,10)})),
      " vs E_coord/2 =", float((4*sp.pi*xi*(ri-rc)/2).subs({ri:1,rc:sp.Rational(1,1000),xi:sp.Rational(1,10)})))

print()
# ===== CLAIM 2: PHI ALONE DOES NOT FINITIZE =====
# back-reaction e^{-2phi} = 1 - delta - rs/r ; MS mass m(r)=(r/2)(1-e^{-2phi}) in c^2/G=1,
# study uses m(r)=r(1-e^{-2phi}). Use that convention.
em2phi = 1 - delta - rs/r
mr = r*(1 - em2phi)
print("CLAIM2 m(r)=r(1-e^{-2phi}) =", sp.simplify(mr))
print("   as r->inf, m(r)/r ->", sp.limit(mr/r, r, sp.oo), " (=> diverges linearly if delta>0)")
print("   m(r) leading:", sp.expand(mr), " -> delta*r + rs (linear divergence).")
# sign check: deficit delta>0 => positive growing mass => diverges, not converge
print("   with rs=0: m(r)=delta*r, m(1e6)=", float(mr.subs({rs:0,delta:sp.Rational(1,100),r:10**6})))
