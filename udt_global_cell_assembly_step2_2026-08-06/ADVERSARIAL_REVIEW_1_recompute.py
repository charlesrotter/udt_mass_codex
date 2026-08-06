"""ADVERSARIAL REVIEW 1 — fresh independent recompute. No step-2 code imported.
Everything re-derived from the source-doc Lagrangian L = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2.
"""
import sympy as sp

x, Zc, cc, Xc, mm, W = sp.symbols('x Zc cc Xc mm W', positive=True)
f = sp.Function('f')(x)      # phi
g = sp.Function('g')(x)      # rho
fp, gp = sp.diff(f, x), sp.diff(g, x)
res = []

Lag = (Zc/2)*g**2*fp**2 - 2*sp.exp(-2*f)*gp**2 + 2

def euler(Lg, h):
    return sp.diff(sp.diff(Lg, sp.diff(h, x)), x) - sp.diff(Lg, h)

ELf = euler(Lag, f)          # phi-EL
ELg = euler(Lag, g)          # rho-EL

# A1: flux identity re-derived: with F := Zc*g^2*f', is F' - 4 e^{-2f} g'^2 == ELf identically?
F = Zc*g**2*fp
res.append(('A1 flux identity (F\' - 4e^{-2phi}rho\'^2) == phi-EL, rho\'\'-free',
            sp.simplify(sp.diff(F, x) - 4*sp.exp(-2*f)*gp**2 - ELf) == 0))

# A2: source-blindness — a matter term Lm(g, g', x) with NO f or f' dependence leaves phi-EL
#     untouched (symbolic: EL of Lm w.r.t. f is identically 0)
Lm = sp.Function('Lm')(g, gp, x)
res.append(('A2 phi-blind matter never enters the phi-EL (identity)',
            sp.simplify(euler(Lm, f)) == 0))

# A2b: the banked EOM forms (from the derivation notes / cell_solver_round) re-derived
fpp_sol = sp.solve(sp.Eq(ELf, 0), sp.diff(f, x, 2))[0]
gpp_sol = sp.solve(sp.Eq(ELg, 0), sp.diff(g, x, 2))[0]
res.append(('A2b phi\'\' = 4e^{-2phi}rho\'^2/(Z rho^2) - 2phi\'rho\'/rho',
            sp.simplify(fpp_sol - (4*sp.exp(-2*f)*gp**2/(Zc*g**2) - 2*fp*gp/g)) == 0))
res.append(('A2c rho\'\' = 2phi\'rho\' - (Z/4)rho e^{2phi}phi\'^2',
            sp.simplify(gpp_sol - (2*fp*gp - (Zc/4)*g*sp.exp(2*f)*fp**2)) == 0))

# A3: shift/Z-rescale lemma re-derived independently
psi = f - cc
Z2 = Zc*sp.exp(2*cc)
ELf_sh = sp.diff(Z2*g**2*sp.diff(psi, x), x) - 4*sp.exp(-2*psi)*gp**2
res.append(('A3a shift: phi-EL maps to e^{2c} x itself', sp.simplify(ELf_sh - sp.exp(2*cc)*ELf) == 0))
Lag_sh = (Z2/2)*g**2*sp.diff(psi, x)**2 - 2*sp.exp(-2*psi)*gp**2 + 2
ELg_sh = euler(Lag_sh, g)
res.append(('A3b shift: rho-EL maps to e^{2c} x itself', sp.simplify(ELg_sh - sp.exp(2*cc)*ELg) == 0))

# A4: Route-B object (regrade C6: mixing term 4 rho rho' phi'; general Z)
LagB = Lag + 4*g*gp*fp
ELfB = euler(LagB, f)
FB = Zc*g**2*fp + 4*g*gp
res.append(('A4 Route-B: (Z rho^2 phi\' + 4 rho rho\')\' - 4e^{-2phi}rho\'^2 == RouteB phi-EL (same nonneg RHS)',
            sp.simplify(sp.diff(FB, x) - 4*sp.exp(-2*f)*gp**2 - ELfB) == 0))

# A5: L-lead exact violations, all re-derived
fL = -sp.Rational(1,2)*sp.log(1 - x/Xc)
fLp = sp.simplify(sp.diff(fL, x))
res.append(('A5a phi_L\'(r) = 1/(2(X-r)) never zero for finite X',
            sp.simplify(fLp - 1/(2*(Xc - x))) == 0))
# flux-identity residual under phi_L at a point where rho'=0 (rho'' arbitrary):
FL = Zc*g**2*sp.diff(fL, x)
residL = sp.diff(FL, x) - 4*sp.exp(-2*fL)*gp**2
rpp = sp.Symbol('rpp')
residL_at = residL.subs(sp.diff(g, x, 2), rpp).subs(sp.diff(g, x), 0)
res.append(('A5b residual at any rho\'=0 point = Z rho^2/(2(X-r)^2) != 0',
            sp.simplify(residL_at - Zc*g**2/(2*(Xc - x)**2)) == 0))

# A6: bulk quadrature — derive the u-quadratic FROM SCRATCH (not copied):
# substitute phi_L, set u = rho'/rho, m = X - r; flux identity is 1st-order in rho.
u = sp.Symbol('u', real=True)
eq = (residL.subs(sp.diff(g, x), u*g) / g**2)          # divide by rho^2
eq = sp.simplify(eq.subs(x, Xc - mm))                   # in terms of m
# my derived form:  Z u/m + Z/(2 m^2) - 4 (m/X) u^2  (should equal -(their quadratic))
mine = Zc*u/mm + Zc/(2*mm**2) - 4*(mm/Xc)*u**2
res.append(('A6a from-scratch quadratic matches notes\' 4(m/X)u^2-(Z/m)u-Z/(2m^2)=0',
            sp.simplify(eq - mine) == 0))
quad = sp.expand(-mine)
rts = sp.solve(sp.Eq(quad, 0), u)
disc = sp.discriminant(sp.Poly(quad, u))
res.append(('A6b discriminant = Z^2/m^2 + 8Z/(mX) > 0 (Z>0)',
            sp.simplify(disc - (Zc**2/mm**2 + 8*Zc/(mm*Xc))) == 0))
res.append(('A6c root product = -ZX/(8m^3) < 0 => two real roots, opposite sign, neither 0',
            sp.simplify(rts[0]*rts[1] + Zc*Xc/(8*mm**3)) == 0))
# A6d substitute u_plus back: residual vanishes identically (exact bulk solution)
up = [rt for rt in rts if sp.simplify(sp.limit(rt*mm, mm, 0)) is not None]
subs_ok = [sp.simplify(quad.subs(u, rt)) == 0 for rt in rts]
res.append(('A6d both roots satisfy the quadratic exactly (bulk solution by quadrature)',
            all(subs_ok)))
# A6e Delta phi_L = (1/2) ln((X-r_c)/(X-r_s))
rc_, rs_ = sp.symbols('rc_ rs_', positive=True)
dphiL = sp.simplify(fL.subs(x, rs_) - fL.subs(x, rc_))
res.append(('A6e Delta phi_L = (1/2)ln((X-rc)/(X-rs)) exactly',
            sp.simplify(dphiL - sp.Rational(1,2)*sp.log((Xc - rc_)/(Xc - rs_))) == 0))
# A6f Z<0 branch: discriminant Z^2/m^2 + 8Z/(mX) can go negative (phi_L bulk-unrealizable there)
dneg = (disc.subs({Zc: -1, mm: sp.Rational(1,2), Xc: 1}))
res.append(('A6f Z<0: discriminant can be negative (e.g. Z=-1,m=1/2,X=1 -> ' + str(sp.simplify(dneg)) + ')',
            sp.simplify(dneg) < 0))

for name, ok in res:
    print(('PASS ' if ok else 'FAIL ') + name)

# ---------------- A7: WITNESS re-shoot, own integrator (scipy RK45 + brentq) ----------------
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
A = float(np.log(1101.0))

def endstate(eps, Zv=8.0, fam='sin2', rtol=1e-11, atol=1e-13):
    if fam == 'sin2':
        rho  = lambda r: 1.0 + eps*np.sin(np.pi*r/2)**2
        rhop = lambda r: eps*(np.pi/2)*np.sin(np.pi*r)
    else:  # smoothstep r^2(3-2r): s'(0)=s'(1)=0
        rho  = lambda r: 1.0 + eps*(r*r*(3-2*r))
        rhop = lambda r: eps*(6*r - 6*r*r)
    def rhs(r, y):
        ph, Ph = y
        return [Ph/(Zv*rho(r)**2), 4.0*np.exp(-2*ph)*rhop(r)**2]
    sol = solve_ivp(rhs, (0.0, 1.0), [-A, 0.0], rtol=rtol, atol=atol, method='RK45')
    return sol.y[0, -1], sol.y[1, -1]

# monotonicity probe of D(eps)
probes = [0.001, 0.005, 0.011, 0.02, 0.05, 0.2, 1.0]
Dv = [endstate(e)[0] for e in probes]
print('A7 D(eps)=phi(1) probes:', [f'{e}:{d:+.4f}' for e, d in zip(probes, Dv)])
eps_star = brentq(lambda e: endstate(e)[0], 1e-4, 1.0, xtol=1e-12)
phL, qv = endstate(eps_star)
print(f'A7 WITNESS(own): eps* = {eps_star:.6f}, q = {qv:.6f}, |phi(1)| = {abs(phL):.2e}')
print('PASS A7 witness reproduces eps*~0.011, q~73.7' if (abs(eps_star-0.011032) < 5e-4 and abs(qv-73.69) < 0.5)
      else f'FAIL A7 mismatch: eps*={eps_star}, q={qv}')
# tighter-tolerance cross-check
e2 = brentq(lambda e: endstate(e, rtol=1e-9, atol=1e-11)[0], 1e-4, 1.0, xtol=1e-12)
print(f'A7b tolerance-robustness: eps*(rtol 1e-9) = {e2:.6f} (delta {abs(e2-eps_star):.2e})')
# independent profile family: existence is not tuned to sin^2
eps_ss = brentq(lambda e: endstate(e, fam='ss')[0], 1e-4, 1.0, xtol=1e-12)
ph2, q2 = endstate(eps_ss, fam='ss')
print(f'A7c second family (smoothstep): eps* = {eps_ss:.6f}, q = {q2:.6f} -> anchor-carrier exists (genericity)')
# A7d check claimed pins at witness: rho'(0)=rho'(1)=0 by construction; q>0; phi(0)=-ln(1101)
print('PASS A7d q>0 and Delta phi = ln(1101) at witness' if (qv > 0 and abs(phL) < 1e-8) else 'FAIL A7d')
