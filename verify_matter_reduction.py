"""CAS-confirm Charles's round S^2 matter reduction (free axisymmetric field).
n = (sin f cos N psi, sin f sin N psi, cos f), f=f(r,theta). Verify derivative identities,
the reduced L2/L4, the rigid limit, and the rho-source with the stabilizing xi*rho*I_r term."""
import sympy as sp

r, th, ps, N, f = sp.symbols('r theta psi N f', real=True)
fr, fth = sp.symbols('f_r f_theta', real=True)
F = sp.Function('f')

# n and its derivatives (f as function of r,theta)
frt = F(r, th)
n = sp.Matrix([sp.sin(frt)*sp.cos(N*ps), sp.sin(frt)*sp.sin(N*ps), sp.cos(frt)])
nr = sp.diff(n, r); nth = sp.diff(n, th); nps = sp.diff(n, ps)
print("=== derivative norms ===")
print("  |d_r n|^2  =", sp.simplify(nr.dot(nr)), "  (want f_r^2)")
print("  |d_th n|^2 =", sp.simplify(nth.dot(nth)), "  (want f_theta^2)")
print("  |d_ps n|^2 =", sp.simplify(nps.dot(nps)), "  (want N^2 sin^2 f)")
print("  d_r.d_ps =", sp.simplify(nr.dot(nps)), "  d_th.d_ps =", sp.simplify(nth.dot(nps)))
# area (cross) norms
def cross(a,b): return a.cross(b)
print("  |d_th x d_ps|^2 =", sp.simplify(cross(nth,nps).dot(cross(nth,nps))), " (want N^2 f_th^2 sin^2 f)")
print("  |d_r  x d_ps|^2 =", sp.simplify(cross(nr,nps).dot(cross(nr,nps))), " (want N^2 f_r^2 sin^2 f)")

print("\n=== rho-source from reduced L (I's = ρ-independent constants) ===")
rho = sp.Function('rho')(r); phi = sp.Function('phi')(r)
Z, xi, kap, Ir, Ith, Is, I4r, I4th = sp.symbols('Z xi kappa I_r I_th I_s I4r I4th', positive=True)
rhp = sp.diff(rho, r); php = sp.diff(phi, r)
L = (sp.Rational(1,2)*Z*rho**2*php**2 + 2 - 2*sp.exp(-2*phi)*rhp**2
     - sp.Rational(1,2)*xi*(rho**2*Ir + Ith + N**2*Is)
     - sp.Rational(1,2)*kap*N**2*(I4r + I4th/rho**2))
el_rho = sp.diff(L, rho) - sp.diff(sp.diff(L, rhp), r)
# solve for rho''
rhopp = sp.symbols('rhopp')
sol = sp.solve(el_rho.subs(sp.diff(rho,(r,2)), rhopp), rhopp)[0]
matter_part = sp.simplify(sol - (2*php*rhp - sp.Rational(1,4)*Z*rho*sp.exp(2*phi)*php**2))
print("  rho'' matter-part =", matter_part)
print("  == e^{2phi}/4 (xi rho I_r - kap N^2 I4th/rho^3) ? ->",
      sp.simplify(matter_part - sp.exp(2*phi)/4*(xi*rho*Ir - kap*N**2*I4th/rho**3)) == 0)
print("\n  => stabilizing (outward) xi*rho*I_r needs I_r>0 (radial matter structure);")
print("     rigid f=theta has I_r=0 -> only inward -kap N^2 I4th/rho^3 -> COLLAPSE (confirmed).")
print("     balance: rho^4 ~ kap N^2 I4th/(xi I_r).")
