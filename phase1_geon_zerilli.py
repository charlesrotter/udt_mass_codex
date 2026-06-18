#!/usr/bin/env python3
"""
phase1_geon_zerilli.py

Exact SYMBOLIC GR: l=2, m=0 EVEN-PARITY (polar) vacuum gravitational-wave
master equation on FLAT round Minkowski background (spherical coords, c=1).

DATA-BLIND. Exact rationals. l=2, m=0 fixed.

Deliverables:
  (A) Full even-parity RW-gauge perturbation set {H0,H1,H2,K} of flat space.
  (B) Linearized vacuum Einstein eqs delta R_{mu nu}=0 -> radial equations.
  (C) RW->Zerilli reduction: algebraic relation (H0=H2), constraints fixing
      H1,K, and the SINGLE master ODE -Psi'' + V Psi = w^2 Psi, V = 6/r^2.
  (D) Confirm Psi = r j_2(w r) is the regular solution.
  (E) Reconstruction map H0,H1,H2,K(Psi,Psi',w,r).
  (F) Over-constraint check: reconstructed {H0..K} -> EVERY delta R = 0 exactly.

IMPLEMENTATION NOTE (avoiding a sympy QQ<I> trigsimp factorization crash):
  We DO NOT carry exp(-i w t) symbolically and we NEVER call sp.simplify /
  trigsimp on mixed complex-trig expressions.  The only t-dependence is the
  common factor e^{-i w t}, so d_t acts as multiplication by (-i w) and
  d_t^2 by (-w^2).  We implement time-derivatives via a REAL placeholder
  symbol 'wt' standing for that factor at the curvature stage; physically
  wt-> -i w, and time-second-derivatives give wt^2 -> -w^2.  Because the
  background is static and the perturbation has a single e^{-iwt}, every
  curvature component carries exactly one power of e^{-iwt}; we strip it and
  keep only powers of (i w) via wt.  We use cancel/expand/together only.
"""

import sympy as sp

print("="*78)
print("phase1_geon_zerilli  --  l=2 even-parity vacuum GW on flat space")
print("="*78)

t, r, th = sp.symbols('t r theta', real=True)
ph = sp.symbols('phi', real=True)
w = sp.symbols('w', positive=True)
eps = sp.symbols('epsilon')
coords = [t, r, th, ph]
n = 4
l = 2

# Angular harmonic m=0: P_2(cos theta)
ct, st = sp.cos(th), sp.sin(th)
Y = sp.Rational(1,2)*(3*ct**2 - 1)

# Radial amplitudes (functions of r only)
H0 = sp.Function('H0')(r)
H1 = sp.Function('H1')(r)
H2 = sp.Function('H2')(r)
K  = sp.Function('K')(r)

# Common time factor handled formally: a function of t, F(t), with the rule
# F'(t) = (-I w) F(t).  We use a symbolic Function and substitute its
# derivatives by the algebraic rule, so no exp() ever enters the CAS.
F = sp.Function('F')(t)
dF = -sp.I*w*F          # F'  = -i w F
d2F = (-sp.I*w)**2 * F  # F'' = -w^2 F

def Tdiff(expr, k):
    """k-th t-derivative of (radial*angular*F), using F'=-iwF rule."""
    # expr is linear in F (and its t-derivatives only through F).
    e = sp.diff(expr, t, k)
    # replace derivatives of F by the algebraic rule, high order first
    e = e.subs(sp.Derivative(F, t, 2), d2F)
    e = e.subs(sp.Derivative(F, t), dF)
    return e

# Background flat metric diag(-1,1,r^2,r^2 sin^2)
g_bg = sp.diag(-1, 1, r**2, r**2*st**2)

# Even-parity RW-gauge perturbation (f=1), each carries Y * F(t):
h = sp.zeros(4,4)
h[0,0] = H0*Y*F
h[0,1] = H1*Y*F;  h[1,0] = H1*Y*F
h[1,1] = H2*Y*F
h[2,2] = r**2*K*Y*F
h[3,3] = r**2*st**2*K*Y*F

g = g_bg + eps*h

# linearized inverse g^{ab} = eta^{ab} - eps h^{ab}
eta_inv = g_bg.inv()
hup = eta_inv*h*eta_inv
ginv = eta_inv - eps*hup

# derivative helper that applies the F-rule whenever d/dt is taken
def D(expr, x):
    e = sp.diff(expr, x)
    if x is t:
        e = e.subs(sp.Derivative(F, t, 2), d2F).subs(sp.Derivative(F, t), dF)
    return e

print("\n[1] Christoffels...")
def dch(a,b,c):
    s = sp.S.Zero
    for d in range(n):
        s += ginv[a,d]*(D(g[d,b],coords[c]) + D(g[d,c],coords[b]) - D(g[b,c],coords[d]))
    return sp.Rational(1,2)*s
Gamma = [[[dch(a,b,c) for c in range(n)] for b in range(n)] for a in range(n)]

print("[2] Ricci...")
def ricci_comp(b,c):
    s = sp.S.Zero
    for a in range(n):
        s += D(Gamma[a][b][c], coords[a])
        s -= D(Gamma[a][b][a], coords[c])
        for d in range(n):
            s += Gamma[a][a][d]*Gamma[d][b][c]
            s -= Gamma[a][c][d]*Gamma[d][b][a]
    return s

print("[3] Linearize in eps (coeff of eps^1)...")
def lin(expr):
    e = sp.expand(expr)
    # coefficient of eps^1: differentiate once in eps, set eps=0
    return sp.expand(sp.diff(e, eps).subs(eps, 0))

comps = [(0,0),(0,1),(1,1),(0,2),(1,2),(2,2),(3,3)]
labels = {(0,0):'tt',(0,1):'tr',(1,1):'rr',(0,2):'t_th',
          (1,2):'r_th',(2,2):'thth',(3,3):'phph'}

dR = {}
for (a,b) in comps:
    val = lin(ricci_comp(a,b))
    # strip the common F(t): every term has exactly one F. divide out.
    val = sp.expand(val)
    # substitute F -> 1 after factoring (each term linear in F and its t-derivs
    # already replaced); replace any residual derivative of F too.
    val = val.subs(sp.Derivative(F, t, 2), d2F).subs(sp.Derivative(F, t), dF)
    val = sp.expand(val).subs(F, 1)
    dR[(a,b)] = sp.cancel(val)
print("    vacuum field eqs: delta R_{ab} = 0 (background R=0). F stripped.")

# ----------------------------------------------------------------------
# Angular separation. Replace cos->c, sin->s, reduce s^2->1-c^2, collect.
# ----------------------------------------------------------------------
print("\n[4] Angular projection -> radial equations...")
c, s = sp.symbols('c s', real=True)
def angproj(expr):
    e = sp.expand(expr)
    e = e.subs({sp.sin(th): s, sp.cos(th): c})
    e = sp.expand(e)
    e = sp.expand(e.subs(s**2, 1 - c**2))
    return e

radeqs = []
for (a,b) in comps:
    e = angproj(dR[(a,b)])
    poly_s = sp.Poly(e, s)
    for monom, coeff_s in poly_s.terms():
        sdeg = monom[0]
        pc = sp.Poly(sp.expand(coeff_s), c)
        for cm, rad in pc.terms():
            cdeg = cm[0]
            rad = sp.cancel(rad)
            if rad != 0:
                radeqs.append((labels[(a,b)], (sdeg, cdeg), rad))

def same(e1, e2):
    if e2 == 0:
        return e1 == 0
    ratio = sp.cancel(e1/e2)
    return ratio.free_symbols.isdisjoint({r}) and sp.cancel(sp.diff(ratio, r)) == 0

distinct = []
for lab, key, rad in radeqs:
    if not any(same(rad, d[2]) for d in distinct):
        distinct.append((lab, key, rad))

print(f"    {len(radeqs)} raw coeff-eqs, {len(distinct)} distinct.")
print("\n    Distinct radial equations (each = 0):")
for i,(lab,key,rad) in enumerate(distinct):
    print(f"      [{i}] from {lab} (s^{key[0]} c^{key[1]}):  0 = {sp.cancel(rad)}")

print("\n[5] Algebraic relations (no derivatives):")
alg = []
for lab, key, rad in distinct:
    if rad.atoms(sp.Derivative) == set():
        r0 = sp.cancel(rad)
        if r0 != 0 and not any(same(r0, a) for a in alg):
            alg.append(r0)
            print("      0 =", r0)
            sol = sp.solve(sp.Eq(r0, 0), H0, dict=True)
            if sol:
                print("        -> H0 =", sp.cancel(sol[0][H0]))
if not alg:
    print("      (none purely algebraic)")

# ----------------------------------------------------------------------
# Master operator + reconstruction. Verify with explicit regular solution.
# ----------------------------------------------------------------------
print("\n[6] Master ODE & regular solution check.")
print("    Target master eq:  Psi'' + (w^2 - 6/r^2) Psi = 0   (V = 6/r^2).")
xw = w*r
j2 = (3/xw**3 - 1/xw)*sp.sin(xw) - (3/xw**2)*sp.cos(xw)
Psi0 = sp.cancel(sp.expand(r*j2))
mres = sp.expand(sp.diff(Psi0, r, 2) + (w**2 - 6/r**2)*Psi0)
mres = sp.cancel(sp.together(mres))
print("    Psi = r*j_2(wr); master residual Psi''+(w^2-6/r^2)Psi =", mres)

# ----------------------------------------------------------------------
# Build the reconstruction by SOLVING the radial system directly with the
# explicit Psi0, then verify EVERY dR component vanishes (over-constraint
# test). We solve the radial system for {H0,H1,H2,K} as functions of r by
# expressing them through Psi.  Concretely:
#   * use H0 = H2 (algebraic),
#   * solve remaining ODEs/constraints for K and H1 in terms of one master.
# We carry this out by treating the distinct equations as a linear system
# in the metric functions & derivatives and reducing with sympy.solve.
# ----------------------------------------------------------------------
print("\n[7] Solve radial system for metric functions (reduction)...")
eqs = [sp.Eq(sp.cancel(rad), 0) for (_,_,rad) in distinct]
funcs = [H0, H1, H2, K]
unknowns = (funcs
            + [sp.Derivative(f, r) for f in funcs]
            + [sp.Derivative(f, r, 2) for f in funcs])
try:
    sol = sp.solve([e.lhs for e in eqs], unknowns, dict=True)
    print("    solve returned", len(sol), "branch(es).")
    if sol:
        for kk, vv in sol[0].items():
            print("      ", kk, "=", sp.cancel(vv))
except Exception as ex:
    print("    full linear solve failed:", repr(ex))

# ----------------------------------------------------------------------
# OVER-CONSTRAINT VERIFICATION (the key deliverable).
# We construct an explicit even-parity reconstruction from a master G(r)
# with G'' = (6/r^2 - w^2) G, plug into ALL dR components, and show every
# residual reduces to 0 (using G''-rule). The reconstruction is determined
# from the radial equations above; we use the standard flat even-parity map:
#       H1 = (-i w) * ( G' - G/r ) ... etc.
# We DERIVE the exact map from the equations and then verify.
# ----------------------------------------------------------------------
print("\n[8] Over-constraint verification via master substitution.")
G = sp.Function('G')(r)
Gp = sp.Derivative(G, r)
Gpp_rule = (6/r**2 - w**2)*G
# G''' = d/dr[(6/r^2 - w^2)G] = (6/r^2 - w^2)G' - (12/r^3) G
Gppp_rule = (6/r**2 - w**2)*Gp - (12/r**3)*G
def applyGrule(e):
    """Reduce all G-derivatives of order>=2 to {G, G'} using the master eq."""
    e = sp.expand(e)
    for _ in range(6):
        e = e.subs(sp.Derivative(G, r, 4),
                   sp.diff(Gppp_rule, r))   # will re-reduce next pass
        e = e.subs(sp.Derivative(G, r, 3), Gppp_rule)
        e = e.subs(sp.Derivative(G, r, 2), Gpp_rule)
        e = sp.expand(e)
    return e

# We determine the reconstruction coefficients by undetermined-coefficient
# fit: ansatz with rational-in-r coefficients times (G, G').
A0,A1 = sp.symbols('A0 A1')      # placeholders not used; we fit functions
def fit_and_verify():
    # RICH ansatz: coefficients of (G, G') are general Laurent polynomials in
    # r (degrees -3..+3) with constant-in-r coefficients that may depend on w.
    # Even-parity l=2 reconstruction needs several r-powers (cf. step [7],
    # which shows r^5 w^4 structure), so a too-small basis collapses to 0.
    rpows = [r**k for k in range(-3, 4)]   # r^-3 .. r^3
    def mkfun(tag):
        cG  = [sp.Symbol(f'{tag}_G_{i}') for i in range(len(rpows))]
        cGp = [sp.Symbol(f'{tag}_Gp_{i}') for i in range(len(rpows))]
        expr = sum(cG[i]*rpows[i] for i in range(len(rpows)))*G \
             + sum(cGp[i]*rpows[i] for i in range(len(rpows)))*Gp
        return expr, cG + cGp
    Kx,  ckK  = mkfun('K')
    H2x, ckH2 = mkfun('H2')
    H1x, ckH1 = mkfun('H1')
    H0x = H2x                       # impose H0 = H2 (even-parity, vacuum)
    subs_map = {H0: H0x, H2: H2x, K: Kx, H1: H1x}
    fit_consts = ckK + ckH2 + ckH1
    def reduce_expr(expr):
        e = expr
        # substitute functions & their derivatives (up to 2nd)
        for fn, fx in subs_map.items():
            e = e.subs(sp.Derivative(fn, r, 2), sp.diff(fx, r, 2))
        for fn, fx in subs_map.items():
            e = e.subs(sp.Derivative(fn, r), sp.diff(fx, r))
        for fn, fx in subs_map.items():
            e = e.subs(fn, fx)
        e = applyGrule(e)
        return e
    allcoeff_eqs = set()
    for (_,_,rad) in distinct:
        red = reduce_expr(rad)
        # collect on G and G' with rational-in-r coefficients -> require 0
        cGp = sp.cancel(red.coeff(Gp, 1))
        cG  = sp.cancel((red - cGp*Gp).coeff(G, 1))
        rem = sp.cancel(red - cGp*Gp - cG*G)
        for term in (cGp, cG, rem):
            term = sp.together(term)
            num = sp.numer(term)
            if num == 0:
                continue
            pol = sp.Poly(sp.expand(num), r)
            for co in pol.all_coeffs():
                if co != 0:
                    allcoeff_eqs.add(sp.expand(co))
    allcoeff_eqs = list({x for x in allcoeff_eqs if x != 0})
    fit = sp.solve(allcoeff_eqs, fit_consts, dict=True)
    return fit, (Kx, H2x, H1x), fit_consts, subs_map

fit, recon, csyms, _ = fit_and_verify()
Kx, H2x, H1x = recon
print("    undetermined-coefficient fit solutions:", len(fit))

print("\n[9] Final residual check: plug the fitted reconstruction into all dR.")
if fit:
    f0 = fit[0]
    # The homogeneous system's general solution has FREE parameters (the
    # nontrivial nullspace = the physical mode). Pin solved consts from f0;
    # for the remaining free consts pick a definite nonzero pattern so we get
    # a CONCRETE nonzero even-parity reconstruction, then verify residuals.
    free = [sc for sc in csyms if sc not in f0]
    # try several seeds until a nonzero reconstruction is obtained
    import itertools
    def build(valmap):
        K2  = sp.expand(Kx.subs(valmap))
        H22 = sp.expand(H2x.subs(valmap))
        H12 = sp.expand(H1x.subs(valmap))
        return K2, H22, H12
    chosen = None
    for seedvals in itertools.product([1, 0, -1], repeat=min(len(free), 6)):
        valmap = dict(f0)
        for sc, sv in zip(free, seedvals):
            valmap[sc] = sp.Integer(sv)
        for sc in free[len(seedvals):]:
            valmap[sc] = sp.Integer(0)
        # resolve any consts still symbolic (appear in f0 RHS) by the seeds
        for k in list(valmap.keys()):
            valmap[k] = sp.expand(valmap[k].subs(valmap)) if hasattr(valmap[k], 'subs') else valmap[k]
        K2, H22, H12 = build(valmap)
        if not (K2 == 0 and H22 == 0 and H12 == 0):
            chosen = (valmap, K2, H22, H12)
            break
    if chosen is None:
        valmap = dict(f0)
        for sc in free: valmap[sc] = sp.Integer(1)
        K2, H22, H12 = build(valmap)
        chosen = (valmap, K2, H22, H12)
    valmap, K2, H22, H12 = chosen
    subs_map2 = {H0: H22, H2: H22, K: K2, H1: H12}
    def reduce2(expr):
        e = expr
        for fn, fx in subs_map2.items():
            e = e.subs(sp.Derivative(fn, r, 2), sp.diff(fx, r, 2))
        for fn, fx in subs_map2.items():
            e = e.subs(sp.Derivative(fn, r), sp.diff(fx, r))
        for fn, fx in subs_map2.items():
            e = e.subs(fn, fx)
        e = applyGrule(e)
        return sp.cancel(sp.together(e))
    print("    Concrete nonzero reconstruction (master G; G''=(6/r^2-w^2)G):")
    print("       H0 = H2 =", sp.cancel(H22))
    print("       H1      =", sp.cancel(H12))
    print("       K       =", sp.cancel(K2))
    print("    Residuals of EVERY distinct delta-R radial equation:")
    allzero = True
    for i,(lab,key,rad) in enumerate(distinct):
        res = reduce2(rad)
        if res != 0:
            allzero = False
        print(f"      [{i}] {lab} (s^{key[0]} c^{key[1]}) residual = {res}")
    print("    ALL RESIDUALS ZERO:", allzero)
    print("    Reconstruction is nonzero:",
          not (K2 == 0 and H22 == 0 and H12 == 0))
else:
    print("    no fit found; reconstruction undetermined.")

print("\n[10] Master operator identification + regular-solution plug-in.")
if fit:
    # The reconstruction used G with G''=(6/r^2 - w^2)G, i.e. the master eq
    #     -G'' + (6/r^2) G = w^2 G   <=>   master operator  L = -d^2/dr^2 + 6/r^2.
    print("    Master operator:  L = -d^2/dr^2 + V_Z,   V_Z(r) = l(l+1)/r^2 = 6/r^2")
    print("    Master equation:  -Psi'' + (6/r^2) Psi = w^2 Psi   (r_* = r on flat).")
    # plug the explicit regular master Psi0 = r j_2(wr) into the reconstruction
    G_loc = sp.Symbol('Gtmp')
    rep = {G: Psi0, sp.Derivative(G, r): sp.diff(Psi0, r)}
    H_recon = sp.cancel(sp.together(H22.subs(rep)))
    H1_recon = sp.cancel(sp.together(H12.subs(rep)))
    K_recon = sp.cancel(sp.together(K2.subs(rep)))
    def safe(x):
        try:
            return sp.expand_trig(sp.cancel(x))
        except Exception:
            return sp.cancel(x)
    print("    With Psi = r*j_2(wr), reconstructed metric functions (finite, regular):")
    print("       H0=H2 =", safe(H_recon))
    print("       H1    =", safe(H1_recon))
    print("       K     =", safe(K_recon))
    # regularity at r->0: numeric evaluation at a few small r (w=1) to show finiteness
    print("    numeric check (w=1) K(r) at small r [finite => regular]:")
    for rv in [sp.Rational(1,2), sp.Rational(1,5), sp.Rational(1,10)]:
        try:
            kv = sp.N(K_recon.subs({w: 1, r: rv}))
            print(f"        K(r={float(rv)}) = {kv}")
        except Exception as ex:
            print("        eval failed:", ex)

print("\nDONE.")
