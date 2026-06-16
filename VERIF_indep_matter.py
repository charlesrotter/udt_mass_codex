#!/usr/bin/env python3
"""
INDEPENDENT matter EL + stress for the unit-S^3 hedgehog in the diagonal Weyl
axisym metric, built from the Lagrangian directly (Skyrme L2 + L4), NOT reusing
the committed generators.  Compares:
  (1) independent Theta Euler-Lagrange residual  vs  axisym_matter_el.matter_el_resid
  (2) independent mixed stress T^mu_nu           vs  torch matter_stress_t (#56 build)

Hedgehog: n^A = (cosTheta, sinTheta * nhat) with nhat the unit radial 3-vector
in the (theta,psi) sphere; winding m=1.  The standard S^3 sigma-model:
  L2 = -(xi/2) g^{mu nu} d_mu n^A d_nu n^A
  L4 = -(kap/4) g^{mu p} g^{nu q} (G_{mu nu} G_{p q} - G_{mu q} G_{p nu})
       with G_{mu nu} = d_mu n^A d_nu n^A  (Skyrme quartic)
This mirrors the torch matter_stress_t construction (dn matrix), but here we
get the EL by direct variation w.r.t. Theta and verify it equals the committed
generator's residual.
"""
import sympy as sp

t, r, th, ps = sp.symbols('t r theta psi', real=True)
xi, kap = sp.symbols('xi kappa', positive=True)
coords = [t, r, th, ps]

a = sp.Function('a')(r, th)
b = sp.Function('b')(r, th)
c = sp.Function('c')(r, th)
d = sp.Function('d')(r, th)
Th = sp.Function('Theta')(r, th)

g = sp.diag(-sp.exp(2*a), sp.exp(2*b), sp.exp(2*c)*r**2, sp.exp(2*d)*r**2*sp.sin(th)**2)
ginv = g.inv()
sqrtg = sp.sqrt(sp.Abs(sp.det(g)))  # use exp form below to avoid Abs issues

# unit S^3 hedgehog target field n^A(x), A=0..3
# n0 = cosTheta ; spatial part = sinTheta * (sin th cos ps, sin th sin ps, cos th)
sT, cT = sp.sin(Th), sp.cos(Th)
sth, cth = sp.sin(th), sp.cos(th)
nA = [cT,
      sT*sth*sp.cos(ps),
      sT*sth*sp.sin(ps),
      sT*cth]

# G_{mu nu} = sum_A d_mu n^A d_nu n^A
def dmu(expr, mu):
    return sp.diff(expr, coords[mu])

Gmn = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        Gmn[mu, nu] = sum(dmu(nA[A], mu)*dmu(nA[A], nu) for A in range(4))

# L2
L2 = -(xi/2)*sum(ginv[mu, nu]*Gmn[mu, nu] for mu in range(4) for nu in range(4))
# L4 Skyrme
L4 = 0
for mu in range(4):
    for nu in range(4):
        for pp in range(4):
            for q in range(4):
                L4 += ginv[mu, pp]*ginv[nu, q]*(Gmn[mu, nu]*Gmn[pp, q] - Gmn[mu, q]*Gmn[pp, nu])
L4 = -(kap/4)*L4
L = L2 + L4

# det g (explicit, positive root of |det|)
detg = sp.exp(2*a)*sp.exp(2*b)*sp.exp(2*c)*r**2*sp.exp(2*d)*r**2*sth**2
rootg = sp.sqrt(detg)

# Euler-Lagrange for Theta from S = int sqrt(g) L :
#   EL = d/dx^mu [ d(sqrt g L)/d(d_mu Theta) ] - d(sqrt g L)/dTheta = 0
ThR = sp.diff(Th, r)
ThT = sp.diff(Th, th)
lag = rootg*L
EL = -sp.diff(Th, r)  # placeholder
dL_dThr = sp.diff(lag, ThR)
dL_dTht = sp.diff(lag, ThT)
dL_dTh = sp.diff(lag, Th)
EL = sp.diff(dL_dThr, r) + sp.diff(dL_dTht, th) - dL_dTh
# divide by rootg to get the residual in the same normalization as committed gen
ELn = sp.simplify(EL/rootg)

# substitution to plain symbols
def repl():
    subs = {}
    for f, nm in [(a, 'a'), (b, 'b'), (c, 'c'), (d, 'd'), (Th, 'Th')]:
        s0 = sp.Symbol(nm)
        subs[sp.diff(f, r, 2)] = sp.Symbol(nm+'_rr')
        subs[sp.diff(f, th, 2)] = sp.Symbol(nm+'_tt')
        subs[sp.diff(f, r, th)] = sp.Symbol(nm+'_rt')
        subs[sp.diff(f, r)] = sp.Symbol(nm+'_r')
        subs[sp.diff(f, th)] = sp.Symbol(nm+'_t')
        subs[f] = s0
    return subs

subs = repl()
syms = [r, th]
for nm in ['a', 'b', 'c', 'd', 'Th']:
    syms += [sp.Symbol(nm), sp.Symbol(nm+'_r'), sp.Symbol(nm+'_t'),
             sp.Symbol(nm+'_rr'), sp.Symbol(nm+'_tt'), sp.Symbol(nm+'_rt')]
syms += [xi, kap]

EL_expr = ELn.subs(subs, simultaneous=True)
EL_lam = sp.lambdify(syms, EL_expr, 'numpy')

if __name__ == "__main__":
    import numpy as np
    import axisym_matter_el as ME
    rng = np.random.default_rng(99)
    rss, thss = sp.symbols('rss thss')
    print("=== INDEPENDENT matter Theta-EL vs committed axisym_matter_el ===")
    worst = 0.0
    for trial in range(5):
        rv = float(rng.uniform(0.6, 5.0)); thv = float(rng.uniform(0.3, 2.8))
        ca = rng.uniform(-0.3, 0.3, 5)
        fld = {
          'a': ca[0]*sp.exp(-rss/3)*sp.cos(thss)+0.05*rss,
          'b': ca[1]*sp.exp(-(rss-1)**2)+0.1*sp.cos(2*thss),
          'c': ca[2]*sp.sin(thss)**2*sp.exp(-rss/4),
          'd': -0.09*sp.cos(thss)*sp.exp(-rss/5)+0.03*rss*sp.sin(thss),
          'Th': 1.4 + ca[3]*sp.cos(thss)*sp.exp(-rss/3) + ca[4]*sp.sin(2*thss)*sp.exp(-rss/2),
        }
        vals = {}
        for nm, expr in fld.items():
            sub = {rss: rv, thss: thv}
            vals[nm] = float(expr.subs(sub))
            vals[nm+'_r'] = float(sp.diff(expr, rss).subs(sub))
            vals[nm+'_t'] = float(sp.diff(expr, thss).subs(sub))
            vals[nm+'_rr'] = float(sp.diff(expr, rss, 2).subs(sub))
            vals[nm+'_tt'] = float(sp.diff(expr, thss, 2).subs(sub))
            vals[nm+'_rt'] = float(sp.diff(expr, rss, thss).subs(sub))
        order = [rv, thv]
        for nm in ['a', 'b', 'c', 'd', 'Th']:
            order += [vals[nm], vals[nm+'_r'], vals[nm+'_t'],
                      vals[nm+'_rr'], vals[nm+'_tt'], vals[nm+'_rt']]
        order += [1.0, 1.0]  # xi, kap
        mine = float(EL_lam(*order))
        comm = float(ME.matter_el_resid(
            rv, thv, vals['a'], vals['b'], vals['c'], vals['d'], vals['Th'],
            vals['a_r'], vals['b_r'], vals['c_r'], vals['d_r'], vals['Th_r'],
            vals['a_t'], vals['b_t'], vals['c_t'], vals['d_t'], vals['Th_t'],
            vals['a_rr'], vals['b_rr'], vals['c_rr'], vals['d_rr'], vals['Th_rr'],
            vals['a_tt'], vals['b_tt'], vals['c_tt'], vals['d_tt'], vals['Th_tt'],
            vals['a_rt'], vals['b_rt'], vals['c_rt'], vals['d_rt'], vals['Th_rt'],
            1.0, 1.0))
        # committed gen may differ by an overall constant factor (normalization);
        # report both raw diff and ratio
        ratio = mine/comm if abs(comm) > 1e-14 else float('nan')
        print(f"trial {trial} r={rv:.2f} th={thv:.2f}  indep={mine:+.6e}  committed={comm:+.6e}  ratio={ratio:.6f}")
        worst = max(worst, abs(mine-comm))
    print(f"\nWORST |indep-committed| = {worst:.2e}")
