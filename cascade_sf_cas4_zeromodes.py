"""sf_cas4_zeromodes.py -- CAS part 3: zero/soft-mode identities (D4).

 C13 Translation field (u,v) = (phi', rho') solves the Jacobi system EXACTLY on-shell
     (autonomy => translation Jacobi field).
 C14 Homothety map: if (phi,rho) solves the EOMs with potential U, then
     (phi_l, rho_l)(r) = (phi(r/l), l*rho(r/l)) solves them with potential U_l(s) = U(s/l).
 C15 Fixed-U homothety direction h = (u_h, v_h) = (-r phi', rho - r rho') is NOT a Jacobi
     field: J_phi[h] == 0 but J_rho[h] == -(e^{2phi}/4)(rho U''(rho) + U'(rho))
     (the pre-named scale-breaking source; for U = c rho^n it equals -(e^{2phi}/4) c n^2 rho^{n-1}).
 C16 h satisfies the linearized essential constraint with beta_h = r_s (u_h(r_s) = -phi'_s r_s)
     and the even-fold compatibility u_h'(0)=0, v_h'(0) = -r ... -> v_h'(0)=0 with alpha_h = 0
     ONLY IF U'(rho_c)=0; generically v_h(0) = rho_c != 0 (violates inner transversality scalar).
"""
import sympy as sp

r, Z, lam, eps = sp.symbols('r Z lambda epsilon', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho')(r)
Uf = sp.Function('U')

phipp = 4*sp.exp(-2*phi)*sp.diff(rho,r)**2/(Z*rho**2) - 2*sp.diff(phi,r)*sp.diff(rho,r)/rho
rhopp = (2*sp.diff(phi,r)*sp.diff(rho,r) - sp.Rational(1,4)*Z*rho*sp.exp(2*phi)*sp.diff(phi,r)**2
         + sp.exp(2*phi)/4*sp.diff(Uf(rho), rho))
EOM_phi = sp.diff(phi, r, 2) - phipp
EOM_rho = sp.diff(rho, r, 2) - rhopp

def onshell(expr):
    """Substitute EOMs for 2nd (and induced 3rd) derivatives."""
    e = expr
    # 3rd derivatives first: differentiate EOMs
    p3 = sp.diff(phipp, r); r3 = sp.diff(rhopp, r)
    e = e.subs({sp.diff(phi, r, 3): p3, sp.diff(rho, r, 3): r3})
    for _ in range(3):
        e = e.subs({sp.diff(phi, r, 2): phipp, sp.diff(rho, r, 2): rhopp})
    return sp.simplify(e)

# Jacobi system (from CAS1: Ju == linearized phi-EOM form, Jv == linearized rho-EOM form).
u = sp.Function('u')(r); v = sp.Function('v')(r)
Jphi = sp.diff((EOM_phi).subs({phi: phi+eps*u, rho: rho+eps*v}, simultaneous=True), eps).subs(eps, 0)
Jrho = sp.diff((EOM_rho).subs({phi: phi+eps*u, rho: rho+eps*v}, simultaneous=True), eps).subs(eps, 0)

# C13 translation
sub_t = {u: sp.diff(phi, r), v: sp.diff(rho, r)}
Jphi_t = onshell(Jphi.subs({sp.diff(u,r,2): sp.diff(phi,r,3), sp.diff(u,r): sp.diff(phi,r,2),
                            sp.diff(v,r,2): sp.diff(rho,r,3), sp.diff(v,r): sp.diff(rho,r,2),
                            u: sp.diff(phi,r), v: sp.diff(rho,r)}))
Jrho_t = onshell(Jrho.subs({sp.diff(u,r,2): sp.diff(phi,r,3), sp.diff(u,r): sp.diff(phi,r,2),
                            sp.diff(v,r,2): sp.diff(rho,r,3), sp.diff(v,r): sp.diff(rho,r,2),
                            u: sp.diff(phi,r), v: sp.diff(rho,r)}))
print("C13 translation Jacobi: J_phi[(phi',rho')] == 0:", Jphi_t == 0)
print("C13 translation Jacobi: J_rho[(phi',rho')] == 0:", Jrho_t == 0)

# C14 homothety covariance (check as identity in functions of s = r/lam)
s = sp.symbols('s', positive=True)
f = sp.Function('f')(s); g = sp.Function('g')(s)   # a U-solution in variable s
# EOM residuals for (f,g) with potential U, as expressions in s:
fpp = 4*sp.exp(-2*f)*sp.diff(g,s)**2/(Z*g**2) - 2*sp.diff(f,s)*sp.diff(g,s)/g
gpp = (2*sp.diff(f,s)*sp.diff(g,s) - sp.Rational(1,4)*Z*g*sp.exp(2*f)*sp.diff(f,s)**2
       + sp.exp(2*f)/4*sp.diff(Uf(g), g))
# mapped fields at r = lam*s (chain rule by hand): phi_l = f(s), rho_l = lam*g(s);
# d/dr = (1/lam) d/ds  =>  phi_l' = f'/lam, phi_l'' = f''/lam^2, rho_l' = g', rho_l'' = g''/lam.
# potential U_l(x) = U(x/lam)  =>  U_l'(rho_l) = U'(g)/lam.
philp = sp.diff(f, s)/lam; philpp = sp.diff(f, s, 2)/lam**2
rholp = sp.diff(g, s);     rholpp = sp.diff(g, s, 2)/lam
phil = f; rhol = lam*g
Ul_prime_at = sp.diff(Uf(g), g)/lam
res_phi = philpp - (4*sp.exp(-2*phil)*rholp**2/(Z*rhol**2) - 2*philp*rholp/rhol)
res_rho = rholpp - (2*philp*rholp - sp.Rational(1,4)*Z*rhol*sp.exp(2*phil)*philp**2
                    + sp.exp(2*phil)/4*Ul_prime_at)
sub_fg = {sp.diff(f, s, 2): fpp, sp.diff(g, s, 2): gpp}
print("C14 homothety maps U-solutions to U(./lam)-solutions:",
      sp.simplify(res_phi.subs(sub_fg)) == 0, sp.simplify(res_rho.subs(sub_fg)) == 0)

# C15 fixed-U homothety direction: h = d/dlam|_1 (phil, rhol) with f,g -> the background (phi,rho)
u_h = sp.diff(phi, r)*(-r)            # d/dlam phi(r/lam)|_1 = -r/1 * phi'(r) ... = -r phi'
v_h = rho - r*sp.diff(rho, r)         # d/dlam lam*rho(r/lam)|_1
def J_apply(uu, vv):
    subs_ = {sp.diff(u,r,2): sp.diff(uu,r,2), sp.diff(u,r): sp.diff(uu,r), u: uu,
             sp.diff(v,r,2): sp.diff(vv,r,2), sp.diff(v,r): sp.diff(vv,r), v: vv}
    return onshell(Jphi.subs(subs_)), onshell(Jrho.subs(subs_))
Jp_h, Jr_h = J_apply(u_h, v_h)
src = -sp.exp(2*phi)/4*(rho*sp.diff(Uf(rho), rho, 2) + sp.diff(Uf(rho), rho))
print("C15 J_phi[h] == 0:", sp.simplify(Jp_h) == 0)
print("C15 J_rho[h] == -(e^{2phi}/4)(rho U'' + U'):", sp.simplify(Jr_h - src) == 0)
# power-law check
n, c = sp.symbols('n c')
print("C15 power-law source == -(e^{2phi}/4) c n^2 rho^(n-1):",
      sp.simplify(src.replace(Uf(rho), c*rho**n).doit()
                  - (-sp.exp(2*phi)/4*c*n**2*rho**(n-1))) == 0)
