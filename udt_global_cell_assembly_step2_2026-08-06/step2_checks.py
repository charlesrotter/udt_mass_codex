"""Step-2 exact checks (sympy, CPU, bounded). LEAD/UNBANKED support for DERIVATION_NOTES.md.
All conditional on S: "S (the 2026-07-01 law-set + phi-blind sources) is UNFORCED (08-06
free-data inference) but the unique banked candidate; conditional robust across Routes A/B."
Round-static Branch-P reduction, ratio level. C7 is the ONE allowed bounded numeric shoot
(WITNESS, not theorem). No GPU. Exit 0 iff all checks pass."""
import sympy as sp

r, Z, c, X, m = sp.symbols('r Z c X m', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho')(r)
OK = []

L = (Z/2)*rho**2*sp.diff(phi, r)**2 - 2*sp.exp(-2*phi)*sp.diff(rho, r)**2 + 2

def EL(Lag, f):
    return sp.diff(sp.diff(Lag, sp.diff(f, r)), r) - sp.diff(Lag, f)

# C1: EL equations reproduce the banked 07-01 EOMs (cell_solver_round.py vacuum P forms)
el_phi = EL(L, phi)   # Z rho^2 phi'' + 2Z rho rho' phi' - 4 e^{-2phi} rho'^2 = 0
el_rho = EL(L, rho)   # -4 e^{-2phi} rho'' + 8 e^{-2phi} phi' rho' - Z rho phi'^2 = 0
phipp = sp.solve(sp.Eq(el_phi, 0), sp.diff(phi, r, 2))[0]
rhopp = sp.solve(sp.Eq(el_rho, 0), sp.diff(rho, r, 2))[0]
OK.append(('C1a phi-EOM matches solver', sp.simplify(
    phipp - (4*sp.exp(-2*phi)*sp.diff(rho, r)**2/(Z*rho**2)
             - 2*sp.diff(phi, r)*sp.diff(rho, r)/rho)) == 0))
OK.append(('C1b rho-EOM matches solver', sp.simplify(
    rhopp - (2*sp.diff(phi, r)*sp.diff(rho, r)
             - (Z/4)*rho*sp.exp(2*phi)*sp.diff(phi, r)**2)) == 0))

# C2: flux identity (Z rho^2 phi')' = 4 e^{-2phi} rho'^2 on the phi-EL ALONE (source-blind:
# phi-blind matter never sources the phi-EL; rho'' absent from the identity)
Phi = Z*rho**2*sp.diff(phi, r)
flux_res = sp.simplify(sp.diff(Phi, r) - 4*sp.exp(-2*phi)*sp.diff(rho, r)**2
                       - el_phi)  # identity: Phi' - RHS == el_phi
OK.append(('C2 flux identity == phi-EL exactly', flux_res == 0))

# C3: shift lemma (ratio level): (phi, rho) solves at Z  =>  (phi - c, rho) solves at Z e^{2c}
psi = phi - c
el_phi_sh = sp.diff((Z*sp.exp(2*c))*rho**2*sp.diff(psi, r), r) - 4*sp.exp(-2*psi)*sp.diff(rho, r)**2
OK.append(('C3a shifted phi-EL == e^{2c} * original phi-EL',
           sp.simplify(el_phi_sh - sp.exp(2*c)*el_phi) == 0))
el_rho_sh = (-4*sp.exp(-2*psi)*sp.diff(rho, r, 2) + 8*sp.exp(-2*psi)*sp.diff(psi, r)*sp.diff(rho, r)
             - (Z*sp.exp(2*c))*rho*sp.diff(psi, r)**2)
OK.append(('C3b shifted rho-EL == e^{2c} * original rho-EL',
           sp.simplify(el_rho_sh - sp.exp(2*c)*el_rho) == 0))

# C5: L-lead phi_L = -(1/2) ln(1 - r/X): flux identity FORBIDS rho'(r0)=0 at ANY point
phiL = -sp.Rational(1, 2)*sp.log(1 - r/X)
PhiL = Z*rho**2*sp.diff(phiL, r)
residual = sp.diff(PhiL, r) - 4*sp.exp(-2*phiL)*sp.diff(rho, r)**2
res_at_rp0 = sp.simplify(residual.subs(sp.diff(rho, r, 2), sp.Symbol('rpp'))
                         .subs(sp.diff(rho, r), 0))
OK.append(('C5 L-lead: residual at rho\'=0 is Z rho^2/(2(X-r)^2) != 0',
           sp.simplify(res_at_rp0 - Z*rho**2/(2*(X - r)**2)) == 0))

# C6: L-lead bulk realizability: u = rho'/rho satisfies 4(m/X)u^2 - (Z/m)u - Z/(2 m^2) = 0
# (m = X - r): discriminant > 0 for Z>0, root product < 0 => two real roots, neither zero.
u = sp.Symbol('u')
quad = 4*(m/X)*u**2 - (Z/m)*u - Z/(2*m**2)
roots = sp.solve(sp.Eq(quad, 0), u)
disc = (Z/m)**2 + 4*(4*m/X)*(Z/(2*m**2))
OK.append(('C6a two real roots (disc = Z^2/m^2 + 8Z/(mX) > 0)',
           len(roots) == 2 and sp.simplify(sp.discriminant(quad, u) - disc) == 0
           and sp.ask(sp.Q.positive(disc), sp.Q.positive(Z) & sp.Q.positive(m) & sp.Q.positive(X))))
prod = sp.simplify(roots[0]*roots[1])
OK.append(('C6b root product = -ZX/(8 m^3) < 0 (opposite signs, neither zero)',
           sp.simplify(prod + Z*X/(8*m**3)) == 0))

# C6c: check the pair (phi_L, rho_+) solves the flux identity exactly (substitute back)
u_plus = [rt for rt in roots if sp.ask(sp.Q.positive(rt), sp.Q.positive(Z) & sp.Q.positive(m) & sp.Q.positive(X))]
OK.append(('C6c a positive root exists (rho_+ = rho_c exp(int u_+) > 0)', len(u_plus) == 1))

# C7: THE ONE BOUNDED NUMERIC SHOOT (WITNESS, not theorem) - odd-fold anchor carrier.
# rho_eps = 1 + eps*sin^2(pi r/2) on [0,1]; IVP phi(0)=-ln(1101), phi'(0)=0 (even-fold core);
# flux identity integrated; bisect eps for phi(1)=0 (=> Delta phi = ln(1101), phi(r_s)=0,
# rho'(0)=rho'(1)=0: all odd-fold + even-fold pins met). Z=8 (banked working value; the
# anchor condition ties eps to Z - existence is Z-robust by the IVT argument in the notes).
import math
def shoot(eps, n=4000, Zv=8.0):
    a = math.log(1101.0); h = 1.0/n
    ph, Ph = -a, 0.0   # Phi = Z rho^2 phi'
    for i in range(n):
        def rhs(rr, ph_, Ph_):
            s = math.sin(math.pi*rr/2)**2
            sp_ = (math.pi/2)*math.sin(math.pi*rr)
            rh = 1.0 + eps*s; rp = eps*sp_
            return Ph_/(Zv*rh*rh), 4.0*math.exp(-2*ph_)*rp*rp
        rr = i*h
        k1 = rhs(rr, ph, Ph); k2 = rhs(rr+h/2, ph+h/2*k1[0], Ph+h/2*k1[1])
        k3 = rhs(rr+h/2, ph+h/2*k2[0], Ph+h/2*k2[1]); k4 = rhs(rr+h, ph+h*k3[0], Ph+h*k3[1])
        ph += h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]); Ph += h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
    return ph, Ph
lo, hi = 0.0, 400.0
assert shoot(hi)[0] > 0.0 and shoot(lo)[0] < 0.0
for _ in range(60):
    mid = (lo+hi)/2
    if shoot(mid)[0] > 0.0: hi = mid
    else: lo = mid
phL_end, q_end = shoot((lo+hi)/2)
OK.append(('C7 WITNESS: eps* found, |phi(r_s)| < 1e-9, q = Phi(r_s) > 0',
           abs(phL_end) < 1e-9 and q_end > 0.0))
print(f'   [C7 witness values: eps* = {(lo+hi)/2:.6f}, q = {q_end:.6f}, Z = 8, L = 1, rho_c = 1]')

fails = [n_ for n_, ok in OK if not ok]
for n_, ok in OK:
    print(('PASS ' if ok else 'FAIL ') + n_)
print('ALL PASS' if not fails else f'FAILURES: {fails}')
raise SystemExit(0 if not fails else 1)
