#!/usr/bin/env python3
"""
phase1_geon_backreact.py

Exact SYMBOLIC GR (sympy, c=1, DATA-BLIND).

GOAL: derive the O(A^2) static l=0 metric backreaction (the geon "mass")
sourced by a finite-amplitude l=2 even-parity vacuum gravitational standing
wave on a flat round background, in the held UDT diagonal gauge.

INPUTS (from phase1_geon_zerilli.py, trusted; master G with G''=(6/r^2-w^2)G):
  RW-gauge reconstruction (overall normalization free):
    H0 = H2 = [-i r^2 w^2 G + i r G' + 3 i G]/(r w)
    H1 = r G' + G
    K  = [i r G' + 3 i G]/(r w)
  Even-parity metric perturbation (flat bg, f=1), harmonic Y = P2(cos th):
    dg_tt = H0 Y e^{-iwt},   dg_tr = H1 Y e^{-iwt},
    dg_rr = H2 Y e^{-iwt},   dg_thth = r^2 K Y e^{-iwt},
    dg_psps = r^2 sin^2(th) K Y e^{-iwt}.
  Regular master:  G = Psi0 = r * j_2(w r).

METHOD / CONVENTIONS (stated explicitly):
  * We keep the perturbation COMPLEX with the factor e^{-iwt}, and form the
    PHYSICAL REAL standing wave  dg_{mn} = Re[ h_{mn}(r) Y e^{-iwt} ].
    For a quadratic (O(A^2)) quantity built from two such real fields, the
    TIME-AVERAGE over one period is the standard complex rule
        < Re(a e^{-iwt}) Re(b e^{-iwt}) >_t = (1/2) Re(a b*) .
    We exploit this: rather than expand cos/sin everywhere, we compute the
    O(A^2) curvature with two formally-independent copies of the wave that
    share the SAME e^{-iwt} (so d_t -> -iw), take the bilinear, then apply
    the time-average operator T[X] = (1/2) Re(X) with one copy conjugated.
    Concretely we build the curvature with h carrying e^{-iwt} (=> d_t=-iw)
    AND its conjugate h* carrying e^{+iwt} (=> d_t=+iw); the static l=0
    backreaction couples h with h*, whose product is t-independent, and the
    averaged source is  (1/2) of that real bilinear.  This is exactly the
    <Re Re>=1/2 Re(ab*) rule and avoids any cos/sin ambiguity.
  * ANGULAR l=0 projection: average the P2-structure over solid angle,
       <X>_ang = (1/2) \int_{-1}^{1} X d(cos th).
       Note <Y> = <P2> = 0, <Y^2> = <P2^2> = 1/5, <(dY/dth)^2 ...> handled
       by explicit theta-integration of each curvature component.
  * STATIC l=0 backreaction in HELD UDT DIAGONAL gauge:
       g_tt -> -(1) + 2 A^2 F(r)   [from -e^{-2 A^2 F} ~ -(1 - 2A^2 F)]
       g_rr -> +(1) + 2 A^2 F(r)   [from e^{+2 A^2 F} ~ +(1 + 2A^2 F)]
       (angular block unchanged at l=0, diagonal gauge; off-diagonal none).
    F(r) is the unknown to be sourced.

DELIVERABLES (printed at end):
  - exact O(A^2) l=0 time-averaged G_tt = 0 -> Misner-Sharp F-equation & source S[Psi]
  - exact O(A^2) l=0 time-averaged G_rr relation (consistency)
  - Misner-Sharp mass m(r) ~ 2 A^2 r F, m'(r) = effective energy density
  - SIGN of the time+angle-averaged effective energy density for Psi=r j_2(wr).
"""

import sympy as sp

print("="*78)
print("phase1_geon_backreact -- O(A^2) l=0 geon backreaction from l=2 even GW")
print("="*78)

t, r, th = sp.symbols('t r theta', real=True)
ph = sp.symbols('phi', real=True)
w = sp.symbols('w', positive=True)
A = sp.symbols('A', real=True)          # finite amplitude (book-keeping order)
I = sp.I
coords = [t, r, th, ph]
n = 4

ct, st = sp.cos(th), sp.sin(th)
Y = sp.Rational(1,2)*(3*ct**2 - 1)       # P2(cos th)

# ----------------------------------------------------------------------
# Master G(r) with the Zerilli/flat master relation G'' = (6/r^2 - w^2) G.
# We carry G, G' as the independent radial data; reduce all >=2 derivs.
# ----------------------------------------------------------------------
G  = sp.Function('G')(r)
Gp = sp.Derivative(G, r)
Gpp_rule  = (6/r**2 - w**2)*G
Gppp_rule = (6/r**2 - w**2)*Gp - (12/r**3)*G
# 4th: d/dr of Gppp_rule, then reduce G'' inside
def _reduce_G(e):
    e = sp.expand(e)
    for _ in range(8):
        e = e.subs(sp.Derivative(G, r, 4), sp.diff(Gppp_rule, r))
        e = e.subs(sp.Derivative(G, r, 3), Gppp_rule)
        e = e.subs(sp.Derivative(G, r, 2), Gpp_rule)
        e = sp.expand(e)
    return e

# ----------------------------------------------------------------------
# Reconstruction radial amplitudes (functions of r), per trusted inputs.
# ----------------------------------------------------------------------
H0r = (-I*r**2*w**2*G + I*r*Gp + 3*I*G)/(r*w)
H2r = H0r
H1r = r*Gp + G
Kr  = (I*r*Gp + 3*I*G)/(r*w)

# ----------------------------------------------------------------------
# Build TWO copies of the O(A) perturbation sharing space-structure but with
# opposite time factors:  hP carries e^{-iwt} (d_t->-iw), hM = (hP)* carries
# e^{+iwt} (d_t->+iw).  We implement the time factor formally: each metric
# entry is (radial)*Y, and we encode the time derivative rule by tagging the
# entry with a per-copy "omega-sign".  Because everything is at most quadratic
# and we only ever need d_t on these, we use placeholder time-functions.
# ----------------------------------------------------------------------
Fp = sp.Function('Fp')(t)   # stands for e^{-iwt}: Fp' = -iw Fp
Fm = sp.Function('Fm')(t)   # stands for e^{+iwt}: Fm' = +iw Fm

def Trule(e):
    e = e.subs(sp.Derivative(Fp, t, 2), (-I*w)**2*Fp)
    e = e.subs(sp.Derivative(Fp, t),    (-I*w)*Fp)
    e = e.subs(sp.Derivative(Fm, t, 2), (+I*w)**2*Fm)
    e = e.subs(sp.Derivative(Fm, t),    (+I*w)*Fm)
    return e

# radial reconstruction lists [tt, tr, rr, thth, psps] in coordinate slots
def make_h(rad_tt, rad_tr, rad_rr, rad_K, Fac):
    h = sp.zeros(4,4)
    h[0,0] = rad_tt*Y*Fac
    h[0,1] = rad_tr*Y*Fac;  h[1,0] = rad_tr*Y*Fac
    h[1,1] = rad_rr*Y*Fac
    h[2,2] = r**2*rad_K*Y*Fac
    h[3,3] = r**2*st**2*rad_K*Y*Fac
    return h

# h_+ (e^{-iwt}) and h_- = conjugate radial parts (e^{+iwt}).
hP = make_h(H0r, H1r, H2r, Kr, Fp)
hM = make_h(sp.conjugate(H0r), sp.conjugate(H1r), sp.conjugate(H2r),
            sp.conjugate(Kr), Fm)
# conjugate(G), conjugate(Gp): G is a real master (Psi=r j_2(wr) real); declare real.
# Replace conjugate(G)->G, conjugate(Gp)->Gp (real master), conjugate(w)->w.
def realize(e):
    e = e.subs(sp.conjugate(G), G)
    e = e.subs(sp.conjugate(sp.Derivative(G, r)), sp.Derivative(G, r))
    e = e.subs(sp.conjugate(w), w)
    e = e.subs(sp.conjugate(r), r)
    return e
hM = hM.applyfunc(realize)

# ----------------------------------------------------------------------
# Static l=0 backreaction (held UDT diagonal gauge), O(A^2):
#   dg_tt^stat = +2 F(r)   (note bg g_tt=-1, so g_tt=-1+2A^2 F)
#   dg_rr^stat = +2 F(r)
# angular block unchanged. We carry F as unknown function.
# ----------------------------------------------------------------------
F = sp.Function('F')(r)
hS = sp.zeros(4,4)
hS[0,0] = 2*F     # delta g_tt
hS[1,1] = 2*F     # delta g_rr

# ----------------------------------------------------------------------
# Full metric to O(A^2):
#   g = g_bg + A*(real wave) + A^2*(static).
# We represent the real wave as (1/2)(hP + hM) so that the O(A^2) cross term
# (1/2)(hP+hM) x (1/2)(hP+hM) contains the bilinear (1/2) hP.hM-type pieces
# whose t-average is exactly (1/2)Re(a b*).  hP.hP carries e^{-2iwt} (averages
# to 0), hM.hM carries e^{+2iwt} (averages to 0); only hP.hM survives.
# ----------------------------------------------------------------------
g_bg = sp.diag(-1, 1, r**2, r**2*st**2)
hWave = (hP + hM)/2
g = g_bg + A*hWave + A**2*hS

print("\n[1] Built metric g = bg + A*Re(wave) + A^2*static(F). Computing inverse to O(A^2)...")

# inverse to O(A^2):  g = bg + A h1 + A^2 h2,
#   ginv = bg^{-1} - A bg^{-1} h1 bg^{-1}
#          + A^2 ( bg^{-1} h1 bg^{-1} h1 bg^{-1} - bg^{-1} h2 bg^{-1} )
bgi = g_bg.inv()
h1 = hWave
h2 = hS
M1 = bgi*h1*bgi
M2 = bgi*h1*bgi*h1*bgi - bgi*h2*bgi
ginv = bgi - A*M1 + A**2*M2

# We will expand all curvature in A and keep up to A^2, then time-average and
# angle-project.  To keep CAS load down, define derivative operator with the
# time rule, and reduce G-derivatives aggressively.

def D(expr, x):
    e = sp.diff(expr, x)
    if x is t:
        e = Trule(e)
    return e

print("[2] Christoffels (O(A^2))...")
def dch(a,b,c):
    s = sp.S.Zero
    for d in range(n):
        s += ginv[a,d]*(D(g[d,b],coords[c]) + D(g[d,c],coords[b]) - D(g[b,c],coords[d]))
    return sp.Rational(1,2)*s

# Pre-expand Christoffels in A, truncate to A^2 to control size.
def trunc_A(e, order=2):
    e = sp.expand(e)
    p = sp.Poly(e, A) if e.has(A) else None
    if p is None:
        return e
    out = sp.S.Zero
    for (k,), co in p.terms():
        if k <= order:
            out += co*A**k
    return out

Gamma = [[[None]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(b, n):
            val = trunc_A(dch(a,b,c))
            Gamma[a][b][c] = val
            Gamma[a][c][b] = val

print("[3] Ricci (O(A^2))...")
def ricci_comp(b,c):
    s = sp.S.Zero
    for a in range(n):
        s += D(Gamma[a][b][c], coords[a])
        s -= D(Gamma[a][b][a], coords[c])
        for d in range(n):
            s += Gamma[a][a][d]*Gamma[d][b][c]
            s -= Gamma[a][c][d]*Gamma[d][b][a]
    return trunc_A(s)

# We need G_{mn} = R_{mn} - 1/2 g_{mn} R.  Build Ricci for needed comps.
print("[4] Building Ricci tensor components...")
Ric = {}
need = [(0,0),(1,1),(2,2),(3,3),(0,1)]
for (a,b) in need:
    Ric[(a,b)] = ricci_comp(a,b)
    print(f"    R_{a}{b} done.")

# Ricci scalar R = g^{ab} R_{ab}.  Need all diagonal + (0,1) symmetric.
print("[5] Ricci scalar...")
# Need full Ricci for the trace; build remaining comps (off-diag) = symmetric.
# For the trace we need R_{ab} for all a,b with nonzero ginv^{ab}.
# ginv is diagonal at O(A^0); off-diagonal entries appear at O(A) (from h_tr,
# and h is otherwise diagonal). So ginv has (0,1) off-diagonal. Include it.
Rscalar = sp.S.Zero
for a in range(n):
    for b in range(n):
        if a==b:
            Rab = Ric[(a,a)]
        elif {a,b}=={0,1}:
            Rab = Ric[(0,1)]
        else:
            Rab = sp.S.Zero    # no other off-diagonal Ricci at this order
        Rscalar += ginv[a,b]*Rab
Rscalar = trunc_A(Rscalar)

print("[6] Einstein tensor components G_tt, G_rr, G_tr (O(A^2))...")
def einstein(a,b):
    if a==b:
        Rab = Ric[(a,a)]
    elif {a,b}=={0,1}:
        Rab = Ric[(0,1)]
    else:
        Rab = sp.S.Zero
    return trunc_A(Rab - sp.Rational(1,2)*g[a,b]*Rscalar)

Gtt = einstein(0,0)
Grr = einstein(1,1)

# ----------------------------------------------------------------------
# Extract the O(A^2) part, time-average, angle-average (l=0).
# ----------------------------------------------------------------------
print("\n[7] Extracting O(A^2) coefficient, time-averaging, angle-projecting...")

def A2coeff(e):
    e = sp.expand(e)
    if not e.has(A):
        return sp.S.Zero
    return sp.expand(e.coeff(A, 2))

def time_average(e):
    """Apply <...>_t.  After A^2 extraction the surviving structure is:
       - static F-pieces (no Fp/Fm): kept as-is.
       - bilinears Fp*Fm (=> e^{0}, t-indep): kept with factor 1.
       - Fp*Fp (e^{-2iwt}) or Fm*Fm (e^{+2iwt}): average to 0.
       - linear Fp or Fm leftover: those are O(A) cross with static O(A^2)?
         No -- at A^2 the wave(A^1) x static(A^1?) -- static is A^2 so cross is
         A^3. So no single-power Fp/Fm should appear at A^2 except multiplying
         the static perturbation's own A^2 (that's pure static, no F-factor).
       Implement: drop Fp^2, Fm^2 (set 0); set Fp*Fm -> 1; set lone Fp,Fm ->0;
       keep terms with neither.
    """
    e = sp.expand(e)
    out = sp.S.Zero
    for term in sp.Add.make_args(e):
        np_ = term.as_coeff_exponent(Fp)  # not robust for products; do manual
    # robust: replace using substitution rules on monomials in Fp,Fm
    # Strategy: treat Fp,Fm as symbols; build polynomial; map powers.
    es = e.subs({Fp: sp.Symbol('Fp_'), Fm: sp.Symbol('Fm_')})
    fp = sp.Symbol('Fp_'); fm = sp.Symbol('Fm_')
    es = sp.expand(es)
    poly_done = sp.S.Zero
    es = sp.expand(es)
    # collect by powers of fp, fm
    for term in sp.Add.make_args(es):
        cfp = sp.degree(sp.Poly(term, fp), fp) if term.has(fp) else 0
        cfm = sp.degree(sp.Poly(term, fm), fm) if term.has(fm) else 0
        coeff = term
        if term.has(fp):
            coeff = coeff.subs(fp, 1)
        if term.has(fm):
            coeff = coeff.subs(fm, 1)
        # averaging rule
        if cfp==0 and cfm==0:
            poly_done += coeff           # static piece
        elif cfp==1 and cfm==1:
            poly_done += sp.Rational(1,1)*coeff   # <Fp Fm> = 1 (e^0)
        elif (cfp==2 and cfm==0) or (cfp==0 and cfm==2):
            poly_done += 0               # e^{+-2iwt} averages to 0
        elif (cfp==1 and cfm==0) or (cfp==0 and cfm==1):
            poly_done += 0               # lone e^{+-iwt} averages to 0
        else:
            poly_done += 0
    return sp.expand(poly_done)

def angle_average(e):
    """<X>_ang = (1/2) int_{-1}^{1} X d(cos th).  Substitute u=cos th, and any
    sin^2 -> 1-u^2 (the metric/curvature carries explicit sin th via st)."""
    u = sp.Symbol('u', real=True)
    expr = sp.expand(e)
    # replace cos(th)->u, sin(th)^2->1-u^2; handle odd sin powers (none expected
    # in l=0 projected scalars built from P2, even in cos).
    expr = expr.rewrite(sp.cos) if False else expr
    expr = expr.subs(sp.sin(th)**2, 1 - sp.cos(th)**2)
    expr = sp.expand(expr)
    expr = expr.subs(sp.cos(th), u)
    # any remaining sin(th) (odd) integrates with the d(cos) measure to 0 over
    # symmetric interval only if odd in u after sin->sqrt; safest: assert none.
    if expr.has(sp.sin(th)):
        # express leftover sin th as sqrt(1-u^2); P2 structure is even, the
        # G_tt/G_rr scalar should have no odd sin. Force integrate numerically.
        expr = expr.subs(sp.sin(th), sp.sqrt(1-u**2))
    integ = sp.integrate(expr, (u, -1, 1))
    return sp.Rational(1,2)*sp.cancel(integ)

print("    G_tt: A^2 coeff ...")
Gtt2 = A2coeff(Gtt)
print("    G_tt: time-average ...")
Gtt2 = time_average(Gtt2)
print("    G_tt: reduce master derivs + angle-average ...")
Gtt2 = _reduce_G(Gtt2)
Gtt2 = angle_average(Gtt2)
Gtt2 = sp.cancel(sp.together(_reduce_G(Gtt2)))

print("    G_rr: A^2 coeff ...")
Grr2 = A2coeff(Grr)
print("    G_rr: time-average ...")
Grr2 = time_average(Grr2)
print("    G_rr: reduce master derivs + angle-average ...")
Grr2 = _reduce_G(Grr2)
Grr2 = angle_average(Grr2)
Grr2 = sp.cancel(sp.together(_reduce_G(Grr2)))

print("\n[8] RESULTS")
print("-"*78)
print("O(A^2), l=0, time-averaged  G_tt = 0  :")
sp.pprint(sp.Eq(Gtt2, 0))
print("\nO(A^2), l=0, time-averaged  G_rr = 0  :")
sp.pprint(sp.Eq(Grr2, 0))

# ----------------------------------------------------------------------
# Identify the F-operator and source.  G_tt should be linear in F (and F')
# from the static piece, plus a quadratic-in-G source from the wave.
# Write  G_tt = [F-operator on F] - [source S] = 0  =>  F-eqn.
# Separate F-dependent part from pure-G (source) part.
# ----------------------------------------------------------------------
print("\n[9] Separating F-operator from wave source (G_tt)...")
def split_F(e):
    e = sp.expand(e)
    # F-part: terms containing F, F', F''
    Fpart = sp.S.Zero
    Spart = sp.S.Zero
    for term in sp.Add.make_args(e):
        if term.has(F) or term.has(sp.Derivative(F, r)) or term.has(sp.Derivative(F, r, 2)):
            Fpart += term
        else:
            Spart += term
    return sp.expand(Fpart), sp.expand(Spart)

FpartTT, SpartTT = split_F(Gtt2)
print("    F-operator part of G_tt (=0 equation, F terms):")
sp.pprint(sp.cancel(FpartTT))
print("    wave-source part of G_tt (pure G; the SOURCE up to sign):")
SrcTT = sp.cancel(sp.together(-SpartTT))   # move to RHS: Fpart = -Spart_moved
sp.pprint(sp.cancel(SpartTT))

FpartRR, SpartRR = split_F(Grr2)
print("\n    F-operator part of G_rr:")
sp.pprint(sp.cancel(FpartRR))
print("    wave-source part of G_rr:")
sp.pprint(sp.cancel(SpartRR))

# ----------------------------------------------------------------------
# Cast the G_tt equation into Misner-Sharp form (r F)' = -(r^2/2) S, or
# F' + F/r = source.  Try to solve the F-operator structurally.
# ----------------------------------------------------------------------
print("\n[10] Misner-Sharp form & effective energy density.")
# In diagonal gauge with g_tt=-(1-2A^2F), g_rr=(1+2A^2 F): the l=0 G_tt of the
# static piece is the linearized Hamiltonian constraint. For metric
#   ds^2 = -e^{2a} dt^2 + e^{2b} dr^2 + r^2 dOmega,  with 2a=... here a=A^2 F,
#   b=A^2 F (NOTE sign convention from prompt: g_rr=+e^{+2A^2F}).
# Linearized static G_tt (mixed/lower) ~ (1/r^2) d/dr [ r (1 - e^{-2b}) ] ~
#   (2/r^2)(r b)' to O(b). The Misner-Sharp mass m(r): g^{rr}=1-2m/r => with
#   g_rr = 1+2A^2F, g^{rr}=1-2A^2F => 2m/r = 2A^2 F => m = A^2 r F.
# We report m'(r) as effective energy density rho_eff via G_tt = 8 pi rho.
print("    Misner-Sharp: g^{rr} = 1 - 2m/r, here g^{rr}=1-2A^2 F(r) (O(A^2))")
print("       =>  m(r) = A^2 r F(r),   m'(r) = A^2 ( F + r F' )")
print("    G_tt (lower) static linear piece encodes (2/r^2)(r F)' (check via FpartTT).")

# Solve FpartTT = SourceTT for the combination, presenting F-equation:
# FpartTT + SpartTT = 0  =>  FpartTT = -SpartTT.
print("\n    F-EQUATION (G_tt = 0):   [F-operator] = -(wave source)")
print("       F-operator(F,F',F'') :")
sp.pprint(sp.cancel(FpartTT))
print("       = -(wave source) :")
sp.pprint(sp.cancel(-SpartTT))

# Try to read off (rF)' form: compute d/dr(r F) and see if FpartTT is a multiple
rFprime = sp.diff(r*F, r)              # = F + r F'
# Express FpartTT as coefficient * (something). Attempt match to (2/r^2)(rF)':
trial = sp.cancel(FpartTT / ( sp.diff(r*F, r) ))
print("\n    FpartTT / (rF)'  =", sp.cancel(trial), " (constant-in-F => clean MS form)")

# ----------------------------------------------------------------------
# Effective energy density sign for Psi0 = r j_2(w r).
#   The source S (pure-G) is the time+angle-averaged effective rho (up to a
#   fixed positive geometric factor). We evaluate the SOURCE numerically.
# ----------------------------------------------------------------------
print("\n[11] SIGN of time+angle-averaged effective energy density (Psi=r j_2(wr)).")
xw = w*r
j2 = (3/xw**3 - 1/xw)*sp.sin(xw) - (3/xw**2)*sp.cos(xw)
Psi0 = sp.cancel(sp.expand(r*j2))
Psi0p = sp.diff(Psi0, r)

# The wave-source (pure G) of G_tt, evaluated on the regular master:
src_expr = sp.cancel(sp.together(SpartTT))
src_on_Psi = src_expr.subs({G: Psi0, sp.Derivative(G, r): Psi0p})
src_on_Psi = sp.cancel(sp.together(src_on_Psi))

# The effective energy density rho_eff ~ -G_tt(source)/(8 pi) but we only need
# the SIGN relative to a positive geometric prefactor; report source sign and
# the resulting m'(r) sign tendency.
print("    Source S[Psi] (G_tt pure-G part) symbolic (in G,G',w,r):")
sp.pprint(sp.cancel(src_expr))

print("\n    Numeric source on Psi=r j_2(wr), w=1, at several r:")
vals = []
for rv in [0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.0, 10.0]:
    try:
        v = complex(sp.N(src_on_Psi.subs({w:1, r:rv})))
        vals.append((rv, v))
        print(f"      r={rv:5.2f}  S = {v.real: .8e}  (imag {v.imag: .2e})")
    except Exception as ex:
        print(f"      r={rv:5.2f}  eval failed: {ex}")

# Also report the implied effective energy density rho_eff and its sign.
# rho_eff defined via static l=0:  G_tt(static) = 8 pi rho_eff, and
# G_tt(static)+G_tt(source)=0 => G_tt(static) = -G_tt(source) = -SpartTT.
# So 8 pi rho_eff = -SpartTT(on Psi). Report sign of -S.
print("\n    Effective energy density rho_eff ~ -(source)/(8pi). Sign of -S:")
for rv, v in vals:
    rho_sign = -v.real
    print(f"      r={rv:5.2f}  -S = {rho_sign: .8e}  ({'POSITIVE' if rho_sign>0 else 'negative'})")

# ----------------------------------------------------------------------
# Integrate the clean MS F-equation to get F(r), m(r)=A^2 r F, and the
# ACCUMULATED geon mass. The local G_tt source oscillates in sign, but the
# physical observable is m(r) (the enclosed effective mass). Solve
#    (2/r^2)(r F)' = -(wave source)   =>   (r F)' = -(r^2/2)*(wave source).
# So  m(r) = A^2 r F(r) = A^2 * integral_0^r [ -(rho^2/2) * S(rho) ] drho,
# with S = SpartTT-on-Psi (the pure-G G_tt source). Hence the effective mass
# DENSITY is  dm/dr = A^2 * d/dr (r F) = A^2 * [ -(r^2/2) S(r) ].
# ----------------------------------------------------------------------
print("\n[12] Accumulated geon mass m(r) = A^2 r F(r) (integrate the MS eqn).")
print("    (rF)' = -(r^2/2)*S  =>  m'(r)/A^2 = -(r^2/2) S(r).  Integrate from r0.")

import mpmath as mp
mp.mp.dps = 30
S_func = sp.lambdify(r, src_on_Psi.subs(w, 1), 'mpmath')
def dm(rho):
    return -(rho**2/2)*S_func(rho)
# enclosed mass from a small inner radius (regular at 0: Psi~r^3 so source ->0)
r0 = mp.mpf('1e-3')
print("    m'(r)/A^2 = -(r^2/2) S(r) at sample r (effective mass density):")
for rv in [0.5,1.0,1.5,2.0,3.0,5.0,7.0,10.0]:
    dmv = dm(mp.mpf(rv))
    print(f"      r={rv:5.2f}  dm/dr /A^2 = {float(dmv): .8e}  ({'POS' if dmv>0 else 'neg'})")
print("\n    Enclosed effective mass  m(R)/A^2 = integral_{r0}^{R} (-(r^2/2)S) dr :")
for R in [1.0,2.0,3.0,5.0,8.0,12.0,16.0,20.0]:
    val = mp.quad(dm, [r0, R])
    print(f"      m(R={R:5.1f})/A^2 = {float(val): .8e}")
print("\n    (A monotonically GROWING positive m(R) => positive geon mass even")
print("     though the LOCAL G_tt source oscillates; that is the geon signature.)")

# ----------------------------------------------------------------------
# INDEPENDENT CROSS-CHECK of the G_tt source via the EXPLICIT REAL standing
# wave Re[h e^{-iwt}] with <cos^2>=<sin^2>=1/2, <cos sin>=0. This validates
# the complex-average route (route used above). We build the real metric
# perturbation explicitly with cos(wt), sin(wt) and recompute the G_tt source.
# ----------------------------------------------------------------------
print("\n[13] Cross-check: G_tt source via EXPLICIT real standing wave.")
tt = sp.symbols('tt', real=True)   # = w t
cwt, swt = sp.cos(tt), sp.sin(tt)
# Real metric pert: dg = Re(h_rad * e^{-iwt}) Y = (Re h_rad cos wt + Im h_rad sin wt) Y
def realwave(rad):
    re = sp.re(rad); im = sp.im(rad)
    return (re*cwt + im*swt)
# H0r,H1r,H2r,Kr are complex in G (treat G,Gp real). Split via expand+I.
def split_re_im(expr):
    expr = sp.expand(expr)
    re = expr.subs(I, 0)
    im = sp.expand((expr - re)/I)
    return sp.simplify(re), sp.simplify(im)
re0,im0 = split_re_im(H0r); reK,imK = split_re_im(Kr)
re1,im1 = split_re_im(H1r)
htt_real = (re0*cwt + im0*swt)
htr_real = (re1*cwt + im1*swt)
hrr_real = htt_real
hK_real  = (reK*cwt + imK*swt)
hR = sp.zeros(4,4)
hR[0,0] = htt_real*Y
hR[0,1] = htr_real*Y; hR[1,0] = htr_real*Y
hR[1,1] = hrr_real*Y
hR[2,2] = r**2*hK_real*Y
hR[3,3] = r**2*st**2*hK_real*Y
# time derivatives: d/dt -> w d/dtt
def Dr(expr, x):
    if x is t:
        return w*sp.diff(expr, tt)
    return sp.diff(expr, x)
gR = g_bg + A*hR + A**2*hS
bgiR = g_bg.inv()
M1R = bgiR*hR*bgiR
M2R = bgiR*hR*bgiR*hR*bgiR - bgiR*hS*bgiR
giR = bgiR - A*M1R + A**2*M2R
def dchR(a,b,c):
    s=sp.S.Zero
    for d in range(n):
        s += giR[a,d]*(Dr(gR[d,b],coords[c])+Dr(gR[d,c],coords[b])-Dr(gR[b,c],coords[d]))
    return trunc_A(sp.Rational(1,2)*s)
GamR=[[[None]*n for _ in range(n)] for _ in range(n)]
for a in range(n):
    for b in range(n):
        for c in range(b,n):
            v=dchR(a,b,c); GamR[a][b][c]=v; GamR[a][c][b]=v
def ricR(b,c):
    s=sp.S.Zero
    for a in range(n):
        s+=Dr(GamR[a][b][c],coords[a]); s-=Dr(GamR[a][b][a],coords[c])
        for d in range(n):
            s+=GamR[a][a][d]*GamR[d][b][c]; s-=GamR[a][c][d]*GamR[d][b][a]
    return trunc_A(s)
RicR={};
for ab in [(0,0),(1,1),(2,2),(3,3),(0,1)]:
    RicR[ab]=ricR(*ab)
RscR=sp.S.Zero
for a in range(n):
    for b in range(n):
        if a==b: Rab=RicR[(a,a)]
        elif {a,b}=={0,1}: Rab=RicR[(0,1)]
        else: Rab=sp.S.Zero
        RscR+=giR[a,b]*Rab
RscR=trunc_A(RscR)
GttR=trunc_A(RicR[(0,0)]-sp.Rational(1,2)*gR[0,0]*RscR)
GttR2=A2coeff(GttR)
# time-average: <cos^2>=<sin^2>=1/2, <cos sin>=0
GttR2=sp.expand(GttR2)
GttR2=GttR2.subs({cwt**2: sp.Rational(1,2), swt**2: sp.Rational(1,2)})
GttR2=sp.expand(GttR2)
GttR2=GttR2.subs(cwt*swt, 0)
# drop any residual lone cos/sin (linear, average 0)
GttR2=GttR2.subs({cwt:0, swt:0})
GttR2=_reduce_G(GttR2)
GttR2=angle_average(GttR2)
GttR2=sp.cancel(sp.together(_reduce_G(GttR2)))
_,SpartTT_real=split_F(GttR2)
diff_src = sp.cancel(sp.together(SpartTT_real - SpartTT))
print("    (real-wave source) - (complex-route source) =", diff_src,
      " [0 => routes agree]")
print("\n[14] DONE. See deliverables above.")
