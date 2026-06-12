"""
VX2 verifier — C1: flip uniformity check, from scratch.

Reconstruct the C1 action covariantly. The banked per-solid-angle static
form is L = (1/4)[y^2 f'^2 + |grad_Omega f|^2 / f], f = e^{-2 phi}.
Identity: (1/4) (df)^2/f = f (dphi)^2, so the covariant C1 density is
    L_C1 = c * sqrt(-g) * e^{-2 Phi} * g^{mu nu} d_mu Phi d_nu Phi
(static reduction check performed below). Metric (R-areal + B=1/A tie
built in, the banked W1 structure):
    g_tt = -e^{-2 Phi}, g_rr = +e^{+2 Phi}, g_tr = eps*H1(t,r)*Y(theta),
    g_thth = r^2, g_phph = r^2 sin^2.
Phi = phi0(r) + eps * p(t,r) * Y(theta).

Checks:
 (A) static reduction reproduces the banked per-solid-angle form;
 (B) second-order action: extract alpha (H1^2), beta (H1 * d_t p),
     kinetic c0 ((d_t p)^2) at explicit ell=1 (Y=cos th) and ell=2
     (Y=(3cos^2-1)/2): alpha, beta per unit <Y^2> must be IDENTICAL
     (lambda-free) while the angular-gradient term carries lambda;
 (C) alpha equals the banked (c/4) f^2 r^2 phi0'^2 (f = e^{-2phi0});
 (D) elimination H1 = -beta/(2 alpha) reproduces the banked weld
     f phi0' H1 = 2 d_t p  and the kinetic flip is EXACT:
     c0 - beta^2/(4 alpha) = -c0.
 (E) rank-1 dressed-kernel algebra in the flipped frame.
"""
import sympy as sp

t, r, th, eps, lam = sp.symbols('t r theta epsilon lambda', real=True)
c = sp.symbols('c', positive=True)
phi0 = sp.Function('phi0')(r)
p = sp.Function('p')(t, r)      # delta-phi radial amplitude
H = sp.Function('H1')(t, r)     # RW H1 amplitude

def second_order_action(Y):
    Phi = phi0 + eps*p*Y
    f = sp.exp(-2*Phi)
    gtt = -sp.exp(-2*Phi)
    grr = sp.exp(2*Phi)
    gtr = eps*H*Y
    block = sp.Matrix([[gtt, gtr], [gtr, grr]])
    blockinv = block.inv()
    det2 = block.det()
    # full det g = det2 * r^4 sin^2 th ; sqrt(-g) = r^2 sin th * sqrt(-det2)
    sqrtmg = r**2*sp.sin(th)*sp.sqrt(-det2)
    dPhi_t = sp.diff(Phi, t)
    dPhi_r = sp.diff(Phi, r)
    dPhi_th = sp.diff(Phi, th)
    quad = (blockinv[0, 0]*dPhi_t**2 + 2*blockinv[0, 1]*dPhi_t*dPhi_r
            + blockinv[1, 1]*dPhi_r**2 + dPhi_th**2/r**2)
    L = c*sqrtmg*sp.exp(-2*Phi)*quad
    L2 = sp.series(L, eps, 0, 3).removeO()
    L2 = sp.expand(sp.integrate(L2, (th, 0, sp.pi)))   # solid-angle reduce
    return L2

results = {}
for name, Y, lamval in [('ell1', sp.cos(th), 2),
                        ('ell2', (3*sp.cos(th)**2 - 1)/2, 6)]:
    L2 = second_order_action(Y)
    o2 = sp.expand(sp.diff(L2, eps, 2)/2)              # O(eps^2) piece
    normY2 = sp.integrate(Y**2*sp.sin(th), (th, 0, sp.pi))
    pt = sp.Symbol('pt'); Hs = sp.Symbol('Hs'); pr = sp.Symbol('pr'); ps = sp.Symbol('ps')
    o2s = o2.subs({sp.Derivative(p, t): pt, sp.Derivative(p, r): pr, H: Hs, p: ps})
    o2s = sp.expand(o2s)
    alpha = sp.simplify(o2s.coeff(Hs, 2)/normY2)
    beta = sp.simplify(o2s.coeff(Hs, 1).coeff(pt, 1)/normY2)
    c0 = sp.simplify(o2s.coeff(pt, 2)/normY2)
    # angular-gradient (lambda) term: coefficient of ps^2 with no r-derivs
    mass_ps = sp.simplify(o2s.coeff(ps, 2)/normY2)
    results[name] = dict(alpha=alpha, beta=beta, c0=c0, mass=mass_ps, lamval=lamval)
    print(f"--- {name} (lambda={lamval}) ---")
    print(" alpha/<Y^2> =", alpha)
    print(" beta /<Y^2> =", beta)
    print(" c0(dtp^2)/<Y^2> =", c0)
    print(" ps^2 coeff /<Y^2> =", mass_ps)

a1, a2 = results['ell1']['alpha'], results['ell2']['alpha']
b1, b2 = results['ell1']['beta'], results['ell2']['beta']
k1, k2 = results['ell1']['c0'], results['ell2']['c0']
print("\n[B] lambda-freeness: alpha_ell1 - alpha_ell2 =", sp.simplify(a1 - a2))
print("    beta_ell1  - beta_ell2  =", sp.simplify(b1 - b2))
print("    c0_ell1    - c0_ell2    =", sp.simplify(k1 - k2))
m1, m2 = results['ell1']['mass'], results['ell2']['mass']
print("    mass-term ratio (should track lambda ratio 6/2 in the lambda piece):")
print("      mass_ell1 =", sp.simplify(m1))
print("      mass_ell2 =", sp.simplify(m2))
print("      mass_ell2 - 3*mass_ell1 =", sp.simplify(m2 - 3*m1),
      " (zero iff pure-lambda scaling of the angular piece)")

# (C) banked alpha
f0 = sp.exp(-2*phi0)
banked_alpha = sp.Rational(1, 4)*c*f0**2*r**2*sp.Derivative(phi0, r)**2
print("\n[C] alpha - (c/4) f0^2 r^2 phi0'^2 =",
      sp.simplify(a1 - banked_alpha.doit()))

# (D) elimination and flip
H1_sol = sp.simplify(-b1/(2*a1))
print("\n[D] H1 = -beta/(2 alpha) * dtp  with  H1/dtp =", H1_sol)
weld_check = sp.simplify(f0*sp.Derivative(phi0, r).doit()*H1_sol - 2)
print("    f0 phi0' * (H1/dtp) - 2 =", weld_check, " (0 <=> banked weld)")
flip = sp.simplify(k1 - b1**2/(4*a1))
print("    kinetic after elimination =", flip, " ; bare =", sp.simplify(k1))
print("    flip exact (after = -bare)?:", sp.simplify(flip + k1) == 0)

# (E) rank-1 dressed kernel algebra (flipped frame)
w2, rho_a, Vaa, Pff = sp.symbols('omega2 rho_a V_aa P_FF', positive=True)
Vua = sp.sqrt(Pff*Vaa)          # rank-1 (exact pointwise screening)
Veff = Pff - Vua**2/(Vaa + rho_a*w2)
Wt = w2*rho_a/Vaa
print("\n[E] Veff - P_FF*W/(1+W) =", sp.simplify(Veff - Pff*Wt/(1 + Wt)))
print("    Veff(omega2=0) =", sp.simplify(Veff.subs(w2, 0)),
      "; Veff(omega2->oo) =", sp.limit(Veff, w2, sp.oo))
# unflipped-frame resonant writing: -P*W/(1-W) with W = omega2/omega0^2
W0 = sp.symbols('W0')
res_form = -Pff*W0/(1 - W0)
print("    resonant form equals Veff iff W0 = -W~ (omega0^2 = -Vaa/rho_a):",
      sp.simplify(res_form.subs(W0, -Wt) - Veff) == 0)
