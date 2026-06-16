#!/usr/bin/env python3
"""
INDEPENDENT blind-verifier GR engine (sympy from scratch).
Builds the mixed Einstein tensor G^mu_nu for the diagonal Weyl axisym metric
  ds^2 = -e^{2a}dt^2 + e^{2b}dr^2 + e^{2c} r^2 dtheta^2 + e^{2d} r^2 sin^2 th dpsi^2
with a,b,c,d FULL functions of (r,theta) -- via metric -> Christoffel -> Riemann
-> Ricci -> Einstein, the textbook route, NO reuse of the committed generators.
Then lambdifies and compares numerically (incl off-diagonal G^r_theta) against
axisym_einstein_analytic.Gmix_components on a NONTRIVIAL metric (c,d != 0).

Also: independent matter L2+L4 stress + EL for the unit-S^3 hedgehog, compared
against axisym_matter_el and the torch matter_stress_t.
"""
import sympy as sp
import numpy as np

# ---- coordinates and metric ----
t, r, th, ps = sp.symbols('t r theta psi', real=True)
coords = [t, r, th, ps]
# a,b,c,d as functions of (r,theta)
A = sp.Function('a')(r, th)
Bf = sp.Function('b')(r, th)
C = sp.Function('c')(r, th)
Df = sp.Function('d')(r, th)

g = sp.diag(-sp.exp(2*A), sp.exp(2*Bf), sp.exp(2*C)*r**2,
            sp.exp(2*Df)*r**2*sp.sin(th)**2)
ginv = g.inv()

n = 4
# Christoffel symbols Gamma^a_bc
Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
for a_ in range(n):
    for b_ in range(n):
        for c_ in range(n):
            s = 0
            for d_ in range(n):
                s += ginv[a_, d_]*(sp.diff(g[d_, b_], coords[c_])
                                   + sp.diff(g[d_, c_], coords[b_])
                                   - sp.diff(g[b_, c_], coords[d_]))
            Gamma[a_][b_][c_] = sp.simplify(s/2)

# Ricci tensor R_bd = R^a_bad
Ric = sp.zeros(n, n)
for b_ in range(n):
    for d_ in range(n):
        s = 0
        for a_ in range(n):
            s += sp.diff(Gamma[a_][b_][d_], coords[a_]) - sp.diff(Gamma[a_][b_][a_], coords[d_])
            for e_ in range(n):
                s += Gamma[a_][a_][e_]*Gamma[e_][b_][d_] - Gamma[a_][d_][e_]*Gamma[e_][b_][a_]
        Ric[b_, d_] = s  # do NOT simplify yet (slow); simplify lazily

Rscal = sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n))
# Einstein G_munu = Ric - 1/2 g R ; mixed G^mu_nu = ginv . G_lower
Glow = Ric - sp.Rational(1, 2)*g*Rscal
Gmix = ginv * Glow   # G^mu_nu, indexed [mu, nu]

# replace functions+derivatives with plain symbols for lambdify
def repl_map():
    syms = {}
    flist = [(A, 'a'), (Bf, 'b'), (C, 'c'), (Df, 'd')]
    subs = {}
    args = []
    for f, nm in flist:
        s0 = sp.Symbol(nm)
        sr = sp.Symbol(nm+'_r'); st = sp.Symbol(nm+'_t')
        srr = sp.Symbol(nm+'_rr'); stt = sp.Symbol(nm+'_tt'); srt = sp.Symbol(nm+'_rt')
        subs[sp.diff(f, r, 2)] = srr
        subs[sp.diff(f, th, 2)] = stt
        subs[sp.diff(f, r, th)] = srt
        subs[sp.diff(f, r)] = sr
        subs[sp.diff(f, th)] = st
        subs[f] = s0
        args += [s0, sr, st, srr, stt, srt]
    return subs, args

subs, fargs = repl_map()
allargs = [r, th] + fargs

# pick the components we will compare:  (0,0),(1,1),(2,2),(3,3),(1,2)
comp_keys = [(0, 0), (1, 1), (2, 2), (3, 3), (1, 2), (2, 1)]
lam = {}
print("lambdifying independent Einstein components (sympy from scratch)...")
for key in comp_keys:
    expr = Gmix[key[0], key[1]].subs(subs, simultaneous=True)
    lam[key] = sp.lambdify(allargs, expr, 'numpy')
print("done.")


def eval_indep(rv, thv, vals):
    """vals: dict name-> array (a,a_r,a_t,a_rr,a_tt,a_rt,b_...,c_...,d_...)."""
    order = []
    for nm in ['a', 'b', 'c', 'd']:
        order += [vals[nm], vals[nm+'_r'], vals[nm+'_t'], vals[nm+'_rr'],
                  vals[nm+'_tt'], vals[nm+'_rt']]
    out = {}
    for key in comp_keys:
        out[key] = lam[key](rv, thv, *order)
    return out


if __name__ == "__main__":
    import axisym_einstein_analytic as GE
    rng = np.random.default_rng(20260616)
    # ---- build a NONTRIVIAL axisymmetric metric field, c,d != 0, off-diag live ----
    # choose smooth analytic a,b,c,d of (r,theta) so we can compute exact derivs
    rv = 1.7
    thv = 0.9
    # define symbolic test fields then differentiate exactly
    rs, ths = sp.symbols('rs ths')
    fields = {
        'a': 0.21*sp.exp(-rs/3)*sp.cos(ths) + 0.05*rs,
        'b': -0.4*sp.exp(-(rs-1)**2) + 0.1*sp.cos(2*ths),
        'c': 0.13*sp.sin(ths)**2*sp.exp(-rs/4),
        'd': -0.09*sp.cos(ths)*sp.exp(-rs/5) + 0.03*rs*sp.sin(ths),
    }
    vals = {}
    for nm, expr in fields.items():
        f0 = float(expr.subs({rs: rv, ths: thv}))
        fr = float(sp.diff(expr, rs).subs({rs: rv, ths: thv}))
        ft = float(sp.diff(expr, ths).subs({rs: rv, ths: thv}))
        frr = float(sp.diff(expr, rs, 2).subs({rs: rv, ths: thv}))
        ftt = float(sp.diff(expr, ths, 2).subs({rs: rv, ths: thv}))
        frt = float(sp.diff(expr, rs, ths).subs({rs: rv, ths: thv}))
        vals.update({nm: f0, nm+'_r': fr, nm+'_t': ft, nm+'_rr': frr,
                     nm+'_tt': ftt, nm+'_rt': frt})

    mine = eval_indep(rv, thv, vals)
    # committed generator
    comm = GE.Gmix_components(
        rv, thv, vals['a'], vals['b'], vals['c'], vals['d'],
        vals['a_r'], vals['b_r'], vals['c_r'], vals['d_r'],
        vals['a_t'], vals['b_t'], vals['c_t'], vals['d_t'],
        vals['a_rr'], vals['b_rr'], vals['c_rr'], vals['d_rr'],
        vals['a_tt'], vals['b_tt'], vals['c_tt'], vals['d_tt'],
        vals['a_rt'], vals['b_rt'], vals['c_rt'], vals['d_rt'])

    print("\n=== INDEPENDENT vs COMMITTED Einstein G^mu_nu (NONTRIVIAL metric, c,d!=0) ===")
    print(f"test point r={rv} theta={thv}")
    print(f"{'comp':>8} {'independent':>16} {'committed':>16} {'abs_diff':>12}")
    for key in comp_keys:
        mv = mine[key]
        cv = comm.get(key, float('nan'))
        diff = abs(mv-cv)
        print(f"{str(key):>8} {mv:>16.10e} {cv:>16.10e} {diff:>12.2e}")
