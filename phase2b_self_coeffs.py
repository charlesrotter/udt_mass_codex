#!/usr/bin/env python3
"""
phase2b_self_coeffs.py -- EXACT per-l self-source coefficients for the O(A^2)
time+angle-averaged static l=0 G_tt GW-stress source S_self[Psi;l], l=2,3,4.

Reuses the VERIFIED method of phase1_geon_backreact.py / phase2b_cross_stress.py
(complex double-copy time-average + l=0 angle projection), but extracts the
NUMERATOR COEFFICIENTS as exact integers so the numeric solver
(phase2b_ensemble_solve.py) can hard-code them with an assert against this.

DATA-BLIND. Exact sympy. c=1.

This is the SINGLE-MODE diagonal source per l; the l=2 result MUST equal phase1.
"""
import sympy as sp

t, r, th = sp.symbols('t r theta', real=True)
w = sp.symbols('w', positive=True)
A = sp.symbols('A', real=True)
I = sp.I
coords = [t, r, th, sp.symbols('psi', real=True)]
n = 4
ct, st = sp.cos(th), sp.sin(th)


def self_source_for_l(l):
    Lc = sp.Integer(l*(l+1))
    half = Lc/2
    Y = sp.legendre(l, ct)
    G = sp.Function('G')(r); Gp = sp.Derivative(G, r)
    Gpp = (Lc/r**2 - w**2)*G
    Gppp = (Lc/r**2 - w**2)*Gp - (2*Lc/r**3)*G

    def reduceG(e):
        e = sp.expand(e)
        for _ in range(8):
            e = e.subs(sp.Derivative(G, r, 4), sp.diff(Gppp, r))
            e = e.subs(sp.Derivative(G, r, 3), Gppp)
            e = e.subs(sp.Derivative(G, r, 2), Gpp)
            e = sp.expand(e)
        return e

    # general-l even-parity reconstruction (verified phase2b_cross_stress.py)
    H0r = (-I*r**2*w**2*G + I*r*Gp + I*half*G)/(r*w)
    H2r = H0r
    H1r = r*Gp + G
    Kr  = (I*r*Gp + I*half*G)/(r*w)

    Fp = sp.Function('Fp')(t); Fm = sp.Function('Fm')(t)
    def Trule(e):
        e = e.subs(sp.Derivative(Fp, t, 2), (-I*w)**2*Fp)
        e = e.subs(sp.Derivative(Fp, t),    (-I*w)*Fp)
        e = e.subs(sp.Derivative(Fm, t, 2), (+I*w)**2*Fm)
        e = e.subs(sp.Derivative(Fm, t),    (+I*w)*Fm)
        return e

    def make_h(tt_, tr_, rr_, K_, Fac):
        h = sp.zeros(4, 4)
        h[0,0] = tt_*Y*Fac
        h[0,1] = tr_*Y*Fac; h[1,0] = tr_*Y*Fac
        h[1,1] = rr_*Y*Fac
        h[2,2] = r**2*K_*Y*Fac
        h[3,3] = r**2*st**2*K_*Y*Fac
        return h
    hP = make_h(H0r, H1r, H2r, Kr, Fp)
    hM = make_h(sp.conjugate(H0r), sp.conjugate(H1r), sp.conjugate(H2r),
                sp.conjugate(Kr), Fm)
    def realize(e):
        e = e.subs(sp.conjugate(G), G)
        e = e.subs(sp.conjugate(sp.Derivative(G, r)), sp.Derivative(G, r))
        e = e.subs(sp.conjugate(w), w).subs(sp.conjugate(r), r)
        return e
    hM = hM.applyfunc(realize)

    F = sp.Function('F')(r)
    hS = sp.zeros(4, 4); hS[0,0] = 2*F; hS[1,1] = 2*F

    g_bg = sp.diag(-1, 1, r**2, r**2*st**2)
    hWave = (hP + hM)/2
    g = g_bg + A*hWave + A**2*hS
    bgi = g_bg.inv()
    M1 = bgi*hWave*bgi
    M2 = bgi*hWave*bgi*hWave*bgi - bgi*hS*bgi
    ginv = bgi - A*M1 + A**2*M2

    def D(expr, x):
        e = sp.diff(expr, x)
        if x is t:
            e = Trule(e)
        return e
    def dch(a, b, c):
        s = sp.S.Zero
        for d in range(n):
            s += ginv[a,d]*(D(g[d,b],coords[c]) + D(g[d,c],coords[b]) - D(g[b,c],coords[d]))
        return sp.Rational(1,2)*s
    def trunc_A(e, order=2):
        e = sp.expand(e)
        if not e.has(A):
            return e
        p = sp.Poly(e, A)
        out = sp.S.Zero
        for (k,), co in p.terms():
            if k <= order:
                out += co*A**k
        return out
    Gamma = [[[None]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(b, n):
                v = trunc_A(dch(a, b, c)); Gamma[a][b][c] = v; Gamma[a][c][b] = v
    def ricci(b, c):
        s = sp.S.Zero
        for a in range(n):
            s += D(Gamma[a][b][c], coords[a]); s -= D(Gamma[a][b][a], coords[c])
            for d in range(n):
                s += Gamma[a][a][d]*Gamma[d][b][c]; s -= Gamma[a][c][d]*Gamma[d][b][a]
        return trunc_A(s)
    Ric = {}
    for ab in [(0,0),(1,1),(2,2),(3,3),(0,1)]:
        Ric[ab] = ricci(*ab)
    Rsc = sp.S.Zero
    for a in range(n):
        for b in range(n):
            if a == b: Rab = Ric[(a,a)]
            elif {a,b} == {0,1}: Rab = Ric[(0,1)]
            else: Rab = sp.S.Zero
            Rsc += ginv[a,b]*Rab
    Rsc = trunc_A(Rsc)
    Gtt = trunc_A(Ric[(0,0)] - sp.Rational(1,2)*g[0,0]*Rsc)

    def A2(e):
        e = sp.expand(e)
        return sp.expand(e.coeff(A, 2)) if e.has(A) else sp.S.Zero
    def time_avg(e):
        es = sp.expand(e.subs({Fp: sp.Symbol('Fp_'), Fm: sp.Symbol('Fm_')}))
        fp = sp.Symbol('Fp_'); fm = sp.Symbol('Fm_')
        out = sp.S.Zero
        for term in sp.Add.make_args(es):
            cfp = sp.degree(sp.Poly(term, fp), fp) if term.has(fp) else 0
            cfm = sp.degree(sp.Poly(term, fm), fm) if term.has(fm) else 0
            co = term
            if term.has(fp): co = co.subs(fp, 1)
            if term.has(fm): co = co.subs(fm, 1)
            if cfp == 0 and cfm == 0: out += co
            elif cfp == 1 and cfm == 1: out += co
        return sp.expand(out)
    def angle_avg(e):
        u = sp.Symbol('u', real=True)
        expr = sp.expand(e).subs(sp.sin(th)**2, 1 - sp.cos(th)**2)
        expr = sp.expand(expr).subs(sp.cos(th), u)
        if expr.has(sp.sin(th)):
            expr = expr.subs(sp.sin(th), sp.sqrt(1-u**2))
        return sp.Rational(1,2)*sp.cancel(sp.integrate(expr, (u, -1, 1)))

    g2 = A2(Gtt); g2 = time_avg(g2); g2 = reduceG(g2)
    g2 = angle_avg(g2); g2 = sp.cancel(sp.together(reduceG(g2)))
    # split F-part from source
    Spart = sp.S.Zero
    for term in sp.Add.make_args(sp.expand(g2)):
        if not (term.has(F) or term.has(sp.Derivative(F, r)) or term.has(sp.Derivative(F, r, 2))):
            Spart += term
    Spart = sp.cancel(sp.together(Spart))
    # the F-eqn is Fpart = -Spart => (rF)' = -(r^2/2) S means source S = -Spart*(2/r^2)/...
    # phase1 uses S with (rF)' + (r^2/2) S = 0, and S = SpartTT/... Let's match the
    # phase1 convention: phase1 Src S is the pure-G part with G_tt = Fpart + Spart = 0
    # => Fpart = -Spart; phase1 then writes (rF)'=-(r^2/2)S with S the source such
    # that Fpart=(2/r^2)(rF)'. We just report Spart and the numerator coeffs.
    return sp.cancel(sp.together(Spart)), G, Gp


def extract_coeffs(Spart, G, Gp):
    """Express Spart = num / (40 r^4 w^2) and read integer coeffs of the 8 terms."""
    num = sp.expand(sp.cancel(Spart * (40*r**4*w**2)))
    # the phase1 source S = (num_phase1)/(40 r^4 w^2); but Spart sign/normalization
    # may differ. We report the numerator as-is and the 8 monomial coefficients.
    terms = {
        'c0': G**2, 'c1': r**2*w**2*G**2, 'c2': r**4*w**4*G**2,
        'd0': r*G*Gp, 'd1': r**3*w**2*G*Gp, 'd2': r**5*w**4*G*Gp,
        'e0': r**2*Gp**2, 'e1': r**4*w**2*Gp**2,
    }
    out = {}
    rem = num
    for k, mon in terms.items():
        co = rem.coeff(mon)
        # coeff on a product needs care: use Poly over G,Gp then match powers
        out[k] = co
    return num, out


if __name__ == "__main__":
    # Cleaner extraction: build polynomial in G,Gp and read coefficients.
    Gs, Gps = sp.symbols('Gs Gps')
    for l in (2, 3, 4):
        Spart, G, Gp = self_source_for_l(l)
        num = sp.expand(sp.cancel(Spart * (40*r**4*w**2)))
        num = num.subs({G: Gs, Gp: Gps})
        num = sp.expand(num)
        p = sp.Poly(num, Gs, Gps)
        # map (deg_Gs, deg_Gps) -> coefficient (a polynomial in r,w)
        print(f"\n=== l={l} : S_self numerator over (40 r^4 w^2) ===")
        coeffmap = {}
        for (dG, dGp), co in p.terms():
            co = sp.expand(co)
            # co is a monomial(s) in r,w; print
            coeffmap[(dG, dGp)] = co
            print(f"   G^{dG} Gp^{dGp} : {co}")
        # Extract the 8 named coefficients for the solver
        def pick(dG, dGp, rpow, wpow):
            co = coeffmap.get((dG, dGp), sp.S.Zero)
            return sp.expand(co).coeff(r, rpow).coeff(w, wpow)
        named = dict(
            c0=pick(2,0,0,0), c1=pick(2,0,2,2), c2=pick(2,0,4,4),
            d0=pick(1,1,1,0), d1=pick(1,1,3,2), d2=pick(1,1,5,4),
            e0=pick(0,2,2,0), e1=pick(0,2,4,2),
        )
        print(f"   NAMED COEFFS: {named}")
