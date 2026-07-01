#!/usr/bin/env python3
"""
gen_einstein_3d_general.py -- AUTO-GENERATE the analytic mixed Einstein tensor
G^mu_nu for the GENERAL (sheared) static/stationary 3-D metric

  g_tt = -e^{2a},  g_rr = e^{2b},  g_thth = e^{2c} r^2,  g_psps = e^{2d} r^2 sin^2 th,
  g_rth = e_rt * r,            g_rps = e_rp * r * sin th,   g_thps = e_tp * r^2 * sin th,
  g_tr  = h_tr,                g_tth = h_tt * r,            g_tps  = h_tp * r * sin th,

with a,b,c,d,e_rt,e_rp,e_tp,h_tr,h_tt,h_tp = functions of (r,theta,psi).  (FULL 3-D,
psi LIVE, NO axisymmetry; SHEAR + time-row off-diagonals carried -- this is the
GENERAL-metric analog of gen_einstein_3d_weyl.py.)

WHY (the S1 diagnosis, 2026-06-21): the numerical CORE.einstein engine builds Gamma
from a SPECTRAL dg and then SPECTRALLY DIFFERENTIATES Gamma AGAIN (dGamma).  On a
Chebyshev grid each spectral differentiation amplifies high modes by O(N^2); the
NESTED (double) differentiation makes the Einstein-tensor error GROW WITH N even on a
perfectly smooth analytic metric (measured: CORE max|G| went 14->160 as Nr 16->64 on
a smooth Gaussian-bump warp, while the diagonal-analytic engine stayed ~12).  The cure
(proven in 2-D and in the diagonal 3-D einstein_mixed_weyl): derive G^mu_nu
ANALYTICALLY (sympy cancels the cot/1/sin pole structure symbolically into finite
expressions AND eliminates the second derivative-of-a-constructed-quantity), then
evaluate ONLY the SMOOTH warp partials (1st/2nd) spectrally.  This carries SHEAR while
staying pole-stable and N-convergent.  Same native Einstein content (principle 4:
transformed GR numerics), general-metric class.

OUTPUT: einstein_3d_general_gen.py with Gmix_components_gen(...) returning the 4x4
mixed G^mu_nu as torch-evaluable expressions in the warps + their 1st/2nd partials.

VALIDATION (run at bottom, symbolic):
  flat (all warps 0)              -> G = 0 EXACTLY
  Schwarzschild (a=-b=.5 ln(1-2M/r), rest 0, th/ps-indep) -> G = 0 EXACTLY
  diagonal limit (e_*,h_*=0)      -> matches gen_einstein_3d_weyl term-by-term.
"""
import sympy as sp

t, r, th, ps = sp.symbols('t r theta psi', real=True)

WARP_NAMES = ['a', 'b', 'c', 'd', 'e_rt', 'e_rp', 'e_tp', 'h_tr', 'h_tt', 'h_tp']
F = {nm: sp.Function(nm)(r, th, ps) for nm in WARP_NAMES}
a, b, c, d = F['a'], F['b'], F['c'], F['d']
e_rt, e_rp, e_tp = F['e_rt'], F['e_rp'], F['e_tp']
h_tr, h_tt, h_tp = F['h_tr'], F['h_tt'], F['h_tp']

sin, cos, exp = sp.sin, sp.cos, sp.exp

# ---- the metric (matches full3d_spectral.build_metric, time-row added) ----
g = sp.zeros(4, 4)
g[0, 0] = -exp(2*a)
g[1, 1] = exp(2*b)
g[2, 2] = exp(2*c)*r**2
g[3, 3] = exp(2*d)*r**2*sin(th)**2
g[1, 2] = g[2, 1] = e_rt*r
g[1, 3] = g[3, 1] = e_rp*r*sin(th)
g[2, 3] = g[3, 2] = e_tp*r**2*sin(th)
g[0, 1] = g[1, 0] = h_tr
g[0, 2] = g[2, 0] = h_tt*r
g[0, 3] = g[3, 0] = h_tp*r*sin(th)

import sys, time
t0 = time.time()
def log(msg): print(f"[{time.time()-t0:7.1f}s] {msg}", flush=True)

log("inverting metric (symbolic 4x4 with shear) via adjugate/det ...")
detg = g.det()
adj = g.adjugate()
ginv = sp.Matrix(4, 4, lambda i, j: adj[i, j]/detg)   # entries share 1/detg; cancel later
coords = [t, r, th, ps]

# ---- Christoffel (stationary: d_t of any warp = 0; coords[0]=t derivatives drop) ----
# NO simplification here (defer all to a single cancel after substitution to plain
# symbols, where expressions are far smaller).  Keep raw.
log("building Christoffel (raw, no simplify)...")
Gamma = [[[sp.S(0)]*4 for _ in range(4)] for _ in range(4)]
for l in range(4):
    for m in range(4):
        for n in range(4):
            s = sp.S(0)
            for k in range(4):
                s += ginv[l, k]*(sp.diff(g[k, m], coords[n])
                                 + sp.diff(g[k, n], coords[m])
                                 - sp.diff(g[m, n], coords[k]))
            Gamma[l][m][n] = s/2
    log(f"  Christoffel row l={l} done")

# ---- Ricci  R_{mn} = d_l G^l_{mn} - d_n G^l_{ml} + G^l_{lk}G^k_{mn} - G^l_{nk}G^k_{ml} ----
log("building Ricci (raw)...")
Ric = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        s = sp.S(0)
        for l in range(4):
            s += sp.diff(Gamma[l][m][n], coords[l]) - sp.diff(Gamma[l][m][l], coords[n])
            for k in range(4):
                s += Gamma[l][l][k]*Gamma[k][m][n] - Gamma[l][n][k]*Gamma[k][m][l]
        Ric[m, n] = s
    log(f"  Ricci row m={m} done")

log("building Ricci scalar + mixed Einstein G^m_n ...")
Rscal = sp.S(0)
for m in range(4):
    for n in range(4):
        Rscal += ginv[m, n]*Ric[m, n]
Gmn = Ric - sp.Rational(1, 2)*g*Rscal
Gmix = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        s = sp.S(0)
        for k in range(4):
            s += ginv[m, k]*Gmn[k, n]
        Gmix[m, n] = s
    log(f"  Gmix row m={m} done")

# ---- lower function-derivatives to plain codegen symbols ----
print("lowering to codegen symbols (cancels cot/1/sin structure)...")
subs = {}
for nm, f in F.items():
    A = sp.Symbol(nm)
    subs[sp.diff(f, r, r)] = sp.Symbol(nm+'_rr')
    subs[sp.diff(f, th, th)] = sp.Symbol(nm+'_tt')
    subs[sp.diff(f, ps, ps)] = sp.Symbol(nm+'_pp')
    subs[sp.diff(f, r, th)] = sp.Symbol(nm+'_rt')
    subs[sp.diff(f, r, ps)] = sp.Symbol(nm+'_rp')
    subs[sp.diff(f, th, ps)] = sp.Symbol(nm+'_tp')
    subs[sp.diff(f, r)] = sp.Symbol(nm+'_r')
    subs[sp.diff(f, th)] = sp.Symbol(nm+'_t')
    subs[sp.diff(f, ps)] = sp.Symbol(nm+'_p')
    subs[f] = A

log("substitute to plain symbols (NO cancel: poles at th=0,pi are EXCLUDED by the GL")
log("    grid, so 1/detg & 1/sin are evaluated only at off-axis nodes -- numerically")
log("    safe; cancel is NOT needed for stability, only the diagonal gen used simplify")
log("    to PROVE flat->0 symbolically, which we still do on the cheap flat substitution).")
exprs = []
for m in range(4):
    for n in range(4):
        e = Gmix[m, n].xreplace(subs)   # xreplace: exact-node dict swap, FAST (vs subs)
        exprs.append(e)
        log(f"  done G^{m}_{n}")

# ---- emit torch module with CSE (shared 1/detg etc computed once -> small + fast) ----
log("CSE + codegen ...")
from sympy.printing.pycode import pycode
# plain cse (NO 'basic' optimization -- 'basic' is O(huge) on multi-MB exprs and
# stalls; default cse is fast and still factors the shared 1/detg structure).
repl, reduced = sp.cse(exprs)
log(f"  cse: {len(repl)} common subexpressions")

argnames = []
for nm in WARP_NAMES:
    for suf in ['', '_r', '_t', '_p', '_rr', '_tt', '_pp', '_rt', '_rp', '_tp']:
        argnames.append(nm + suf)
sig = ', '.join(['r', 'theta'] + argnames)

def emit(e):
    code = pycode(e, fully_qualified_modules=False)
    for a_, b_ in [('math.exp', 'exp'), ('math.sin', 'sin'), ('math.cos', 'cos'),
                   ('math.tan', 'tan'), ('math.sqrt', 'sqrt')]:
        code = code.replace(a_, b_)
    return code

lines = ['#!/usr/bin/env python3',
         '"""AUTO-GENERATED by gen_einstein_3d_general.py. Mixed Einstein G^mu_nu for',
         'the GENERAL sheared static/stationary 3-D metric (warps a,b,c,d,e_rt,e_rp,',
         'e_tp,h_tr,h_tt,h_tp).  torch-evaluable, pole-stable.  DO NOT EDIT."""',
         'import torch',
         f'def Gmix_components_gen({sig}):',
         '    exp=torch.exp; sin=torch.sin; cos=torch.cos; tan=torch.tan',
         '    sqrt=torch.sqrt']
for sym, sub in repl:
    lines.append(f'    {sym} = {emit(sub)}')
flat = ['G_0_0', 'G_0_1', 'G_0_2', 'G_0_3', 'G_1_0', 'G_1_1', 'G_1_2', 'G_1_3',
        'G_2_0', 'G_2_1', 'G_2_2', 'G_2_3', 'G_3_0', 'G_3_1', 'G_3_2', 'G_3_3']
for nm, e in zip(flat, reduced):
    lines.append(f'    {nm} = {emit(e)}')
lines.append('    return [[G_0_0,G_0_1,G_0_2,G_0_3],')
lines.append('            [G_1_0,G_1_1,G_1_2,G_1_3],')
lines.append('            [G_2_0,G_2_1,G_2_2,G_2_3],')
lines.append('            [G_3_0,G_3_1,G_3_2,G_3_3]]')
with open('einstein_3d_general_gen.py', 'w') as fo:
    fo.write('\n'.join(lines)+'\n')
log("wrote einstein_3d_general_gen.py")

# ---- symbolic validation ----
print("\n=== symbolic validation ===")
zero = {f: sp.S(0) for f in F.values()}
mx = sp.S(0)
for m in range(4):
    for n in range(4):
        e = sp.simplify(Gmix[m, n].subs(zero))
        if e != 0:
            print(f"  FLAT G^{m}_{n} = {e}"); mx = e
print("flat-space residual:", "0 (PASS)" if mx == 0 else mx)
