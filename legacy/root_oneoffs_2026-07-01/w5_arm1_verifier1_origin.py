"""W5 ARM-1 BLIND VERIFIER — SCRIPT 1: THE -2/f ORIGIN AND THE q=0
SPECIES EL MAP (attacks claims (i)/(ii) of w5_arm1_results.md).

Date: 2026-06-12.  Blind adversarial verifier (independent machinery;
no code shared with w5_arm1_*.py; different seed; symbolic closures
where the arm used rational spot points).

ATTACK LIST COVERED HERE:
  A-1 (their V-1): close the div-V EL-invisibility SYMBOLICALLY in the
      w-channel AND the f-channel (the arm had 5 rational points,
      w-channel only); verify the GG split identity sq*R = LGG + divV
      symbolically; re-derive the relation by my own route (full
      second-order jet EL of the COMPLETE density sqrt(-g)R — no GG
      split, no Einstein tensor in the w-channel).
  A-2 (their V-2): the tie-deformation engine — full COMPLETENESS
      census of the algebraic w-EL at symbolic (a,b) (the arm never
      asserted the two-slot completeness: linear slots and cubic+
      monomials were unchecked); the unimodular line; the
      integer-exponent ties (2,0)/(0,2)/(0,0) (tadpole-free) and
      (2,-2)/(1,1) by an INDEPENDENT route (full density jet EL on
      explicit integer metrics — no symbolic exponents, no Einstein
      route).
  A-3 the weight-stripping identity and slot localization (own LGG).
  A-4 claim (ii): the E_f map — note the w==0 macro gate is
      STRUCTURALLY TRIVIAL for any density (EL commutes with setting a
      field+jets to zero); the nontrivial content (no w-second-jets at
      linearized order; shaped-only O(w) source; spherical content ==
      dL_Wwave/df) is re-derived on the FULL EH density (not the GG
      bulk) with my own machinery.
  A-5 the doc's guardrail-softening sentence "any curvature-grade
      scalar built on the tie carries this channel" — TESTED on
      sqrt(-g) R^2 (static q=0 class): does its algebraic w-channel
      exist and localize?

FAILURE CRITERIA (pre-stated): any symbolic residual != 0 in A-1/A-3
kills the corresponding claim; a nonzero unchecked slot in A-2 kills
the "only the normalization is EH-specific" headline; A-5 either way
is reported (the sentence is the arm's, not a banked claim).

Log: /tmp/w5_arm1_ver1.log
"""
import random
import time
import sympy as sp
from sympy import Rational as Ra

random.seed(987654321)          # verifier's own seed
t0 = time.time()
PASS, FAIL = [], []


def check(label, ok):
    ok = bool(ok)
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)


T, r, th, ph = sp.symbols('T r theta varphi', real=True)


# ---------------------------------------------------------- own engine
def geom(g, xs):
    """Christoffel (2nd kind), inverse, Ricci tensor, Ricci scalar.
    Own implementation (single pass, cancel per entry)."""
    n = len(xs)
    gi = g.inv()
    Gam = {}
    for c in range(n):
        for a in range(n):
            for b in range(a, n):
                e = sum(gi[c, d] * (sp.diff(g[d, a], xs[b])
                                    + sp.diff(g[d, b], xs[a])
                                    - sp.diff(g[a, b], xs[d]))
                        for d in range(n)) / 2
                Gam[(c, a, b)] = Gam[(c, b, a)] = sp.cancel(e)
    Ric = sp.zeros(n, n)
    for a in range(n):
        for b in range(a, n):
            e = sp.S(0)
            for c in range(n):
                e += sp.diff(Gam[(c, a, b)], xs[c]) \
                    - sp.diff(Gam[(c, a, c)], xs[b])
                for d in range(n):
                    e += Gam[(c, c, d)] * Gam[(d, a, b)] \
                        - Gam[(c, b, d)] * Gam[(d, a, c)]
            Ric[a, b] = Ric[b, a] = e
    Rs = sum(gi[a, b] * Ric[a, b] for a in range(n) for b in range(n))
    return Gam, gi, Ric, Rs


def gg_split(g, xs, sq):
    """sqrt(-g) R = LGG + div V with
    V^c = sq (g^{ab} Gam^c_ab - g^{cb} Gam^a_ab),
    LGG = sq g^{ab} (Gam^c_ad Gam^d_bc - Gam^c_ab Gam^d_dc)."""
    n = len(xs)
    Gam, gi, _, _ = geom(g, xs)
    V = []
    for c in range(n):
        V.append(sq * sum(gi[a, b] * Gam[(c, a, b)]
                          - (gi[c, b] * Gam[(a, a, b)] if True else 0)
                          for a in range(n) for b in range(n)))
    LGG = sq * sum(gi[a, b] * (Gam[(c, a, d)] * Gam[(d, b, c)]
                               - Gam[(c, a, b)] * Gam[(d, d, c)])
                   for a in range(n) for b in range(n)
                   for c in range(n) for d in range(n))
    return LGG, V


# --------------------------------------------------- own jet machinery
class Jets:
    def __init__(self, fields, coords, tags):
        self.fields = fields      # {Function: 'name'}
        self.coords = coords
        self.tags = tags          # e.g. 'Trh'
        self.J = {}

    def sym(self, name, mi):
        mi = tuple(sorted(mi))
        k = (name, mi)
        if k not in self.J:
            suff = ''.join(self.tags[i] for i in mi)
            self.J[k] = sp.Symbol(name + ('_' + suff if suff else ''),
                                  real=True)
        return self.J[k]

    def to_jets(self, e):
        sub = {}
        for d in e.atoms(sp.Derivative):
            if d.expr in self.fields:
                mi = []
                for v, k in d.variable_count:
                    mi += [self.coords.index(v)] * int(k)
                sub[d] = self.sym(self.fields[d.expr], tuple(mi))
        return e.subs(sub).subs({F: self.sym(nm, ())
                                 for F, nm in self.fields.items()})

    def D(self, e, i):
        out = sp.diff(e, self.coords[i])
        for (nm, mi), s in list(self.J.items()):
            if e.has(s):
                out += sp.diff(e, s) * self.sym(nm, mi + (i,))
        return out

    def EL2(self, L, name):
        """full EL for densities of jet order <= 2."""
        res = sp.diff(L, self.sym(name, ()))
        nc = len(self.coords)
        for i in range(nc):
            res -= self.D(sp.diff(L, self.sym(name, (i,))), i)
        for i in range(nc):
            for j in range(i, nc):
                c = sp.diff(L, self.sym(name, tuple(sorted((i, j)))))
                if c != 0:
                    res += self.D(self.D(c, i), j)
        return res

    def rand_zero(self, e, npts, extra=None):
        """exact rational identity test; hostile draws (w<0 included)."""
        tp = sp.Symbol('t_par', real=True)
        e = e.subs({sp.sin(th): 2 * tp / (1 + tp**2),
                    sp.cos(th): (1 - tp**2) / (1 + tp**2)})
        syms = sorted(e.free_symbols, key=str)
        ok = True
        for _ in range(npts):
            sub = {}
            for s in syms:
                if s == r:
                    sub[s] = Ra(random.randint(1, 11),
                                random.randint(1, 6))
                elif s == tp:
                    sub[s] = Ra(random.randint(1, 9),
                                random.randint(2, 11))
                elif str(s) == 'f':
                    sub[s] = Ra(random.randint(1, 11),
                                random.randint(1, 5))
                elif str(s) == 'w':
                    sub[s] = Ra(random.randint(-3, 8), 9)
                else:
                    sub[s] = Ra(random.randint(-11, 11),
                                random.randint(1, 8))
            if extra:
                sub.update(extra)
            v = sp.cancel(e.subs(sub))
            ok = ok and (v == 0)
        return ok


# =====================================================================
print("=" * 72)
print("PART 0 — ENGINE SANITY (own anchors)")
print("=" * 72)
m_, H_ = sp.symbols('m H', positive=True)
gS = sp.diag(-(1 - 2 * m_ / r), 1 / (1 - 2 * m_ / r), r**2,
             r**2 * sp.sin(th)**2)
_, _, RicS, RS = geom(gS, [T, r, th, ph])
gdS = sp.diag(-(1 - H_**2 * r**2), 1 / (1 - H_**2 * r**2), r**2,
              r**2 * sp.sin(th)**2)
_, _, _, RdS = geom(gdS, [T, r, th, ph])
check("V1-00 engine: Schwarzschild Ricci == 0 AND static de Sitter "
      "R == 12 H^2 (two independent anchors)",
      all(sp.simplify(RicS[i, j]) == 0 for i in range(4)
          for j in range(4)) and sp.simplify(RdS - 12 * H_**2) == 0)

# =====================================================================
print()
print("=" * 72)
print("PART 1 — A-1: THE RELATION BY MY OWN ROUTE + SYMBOLIC div-V")
print("=" * 72)
f = sp.Function('f')(T, r, th)
w = sp.Function('w')(T, r, th)
g4 = sp.diag(-f, 1 / f, r**2 * (1 + w)**2,
             r**2 * sp.sin(th)**2 / (1 + w)**2)
sq = r**2 * sp.sin(th)
check("V1-01 q=0 time-on class: -det g == (r^2 sin)^2 exactly",
      sp.cancel(-g4.det() - sq**2) == 0)

print("   [Ricci on the q=0 time-on class ...]", flush=True)
_, _, _, Rsc = geom(g4, [T, r, th, ph])
J = Jets({f: 'f', w: 'w'}, [T, r, th], 'Trh')
L_EH = J.to_jets(sp.expand(sq * Rsc))

fj, wj = J.sym('f', ()), J.sym('w', ())
fT, fr_, fth = J.sym('f', (0,)), J.sym('f', (1,)), J.sym('f', (2,))
wT, wr, wth = J.sym('w', (0,)), J.sym('w', (1,)), J.sym('w', (2,))

# independent target objects (from their banked definitions, not their
# code): W_wave per the W4 declaration; C1 from the covariant density
# +(1/4) sqrt(-g) g^{mu nu} f_mu f_nu / f (banked positive convention,
# time-kinetic negative):
L_Wwave = (2 * r**2 * sp.sin(th) / (1 + wj)**2) * (wT**2 / fj
                                                   - fj * wr**2)
gi4 = g4.inv()
L_C1_cov = (Ra(1, 4) * sq / f) * (gi4[0, 0] * sp.diff(f, T)**2
                                  + gi4[1, 1] * sp.diff(f, r)**2
                                  + gi4[2, 2] * sp.diff(f, th)**2)
L_C1 = J.to_jets(sp.expand(L_C1_cov))
check("V1-02 my covariant C1 build reproduces the banked q=0 time-on "
      "density: (1/4) sin (r^2 f_r^2 + f_th^2/(f(1+w)^2)) "
      "- (1/4) r^2 sin f_T^2/f^2 (time-kinetic NEGATIVE)",
      sp.cancel(L_C1 - (Ra(1, 4) * sp.sin(th)
                        * (r**2 * fr_**2 + fth**2 / (fj * (1 + wj)**2))
                        - Ra(1, 4) * r**2 * sp.sin(th) * fT**2 / fj**2))
      == 0)
dLC1_dw = sp.diff(L_C1, wj)

print("   [full second-order jet EL of sqrt(-g) R, w-channel ...]",
      flush=True)
ELw_EH = J.EL2(L_EH, 'w')
ELw_Wwave = J.EL2(L_Wwave, 'w')
resid = sp.cancel(sp.together(sp.expand(
    ELw_EH - (ELw_Wwave - (2 / fj) * dLC1_dw))))
check("V1-03 THE RELATION, MY ROUTE (full second-order jet EL of the "
      "COMPLETE density sqrt(-g)R; no GG split, no Einstein tensor): "
      "E_w[sqrt(-g)R] = EL_w[W_wave] - (2/f) dL_C1/dw IDENTICALLY "
      "(symbolic) on the full q=0 time-on class", resid == 0)

print("   [GG split + symbolic div-V closure ...]", flush=True)
LGG, V = gg_split(g4, [T, r, th, ph], sq)
divV = sum(sp.diff(V[i], x) for i, x in enumerate([T, r, th, ph]))
split_resid = sp.cancel(sp.together(sp.expand(sq * Rsc - LGG - divV)))
check("V1-04 GG split identity sqrt(-g) R == LGG + div V holds "
      "SYMBOLICALLY on the class (the split itself, not assumed)",
      split_resid == 0)
divVj = J.to_jets(sp.expand(divV))
ELw_divV = sp.cancel(sp.together(sp.expand(J.EL2(divVj, 'w'))))
ELf_divV = sp.cancel(sp.together(sp.expand(J.EL2(divVj, 'f'))))
check("V1-05 div-V EL-invisibility CLOSED SYMBOLICALLY (the arm's "
      "V-1 attack item): EL_w[div V] == 0 AND EL_f[div V] == 0 "
      "identically under the full second-order EL operator (the arm "
      "had only 5 rational points, w-channel only)",
      ELw_divV == 0 and ELf_divV == 0)

# =====================================================================
print()
print("=" * 72)
print("PART 2 — A-3: SLOT LOCALIZATION + WEIGHT STRIPPING (own LGG)")
print("=" * 72)
LGGj = J.to_jets(sp.expand(LGG))
LGG_alg = LGGj.subs({wT: 0, wr: 0, wth: 0})
P_alg = sp.Poly(sp.expand(LGG_alg), fT, fr_, fth)
mons = P_alg.monoms()
check("V1-06 COMPLETENESS (never asserted by the arm): the bulk's "
      "algebraic sector is a polynomial of total degree <= 2 in the "
      "f-jets — the slot census below is COMPLETE",
      max(sum(m) for m in mons) <= 2)
wdep = {}
for mon in mons:
    c = P_alg.coeff_monomial(mon)
    dv = sp.cancel(sp.diff(c, wj))
    wdep[mon] = dv
others0 = all(v == 0 for m, v in wdep.items() if m != (0, 0, 2))
check("V1-07 LOCALIZATION: d/dw of EVERY slot except f_th^2 vanishes "
      "(incl. the linear slots the arm's census skipped); the f_th^2 "
      "slot's w-derivative is nonzero",
      others0 and wdep.get((0, 0, 2), 0) != 0)
L_C1_ang = Ra(1, 4) * sp.sin(th) * fth**2 / (fj * (1 + wj)**2)
lhs = sp.cancel(LGG_alg - LGG_alg.subs(wj, 0))
rhs = sp.cancel(-(2 / fj) * (L_C1_ang - L_C1_ang.subs(wj, 0)))
check("V1-08 WEIGHT-STRIPPING identity (exact, all w): "
      "LGG_alg(w) - LGG_alg(0) == -(2/f)[L_C1_ang(w) - L_C1_ang(0)]",
      sp.cancel(lhs - rhs) == 0)
phith = -fth / (2 * fj)
gradterm = -2 * sq * phith**2 / (r**2 * (1 + wj)**2)
check("V1-09 the -2(grad phi)^2 reading: -2 sqrt(-g) g^{thth} "
      "phi_th^2 carries the species' algebraic w-content exactly; "
      "ratio to C1's own slot = -2/f",
      sp.cancel((gradterm - gradterm.subs(wj, 0)) - lhs) == 0)

# =====================================================================
print()
print("=" * 72)
print("PART 3 — A-2: TIE DEFORMATION, COMPLETE CENSUS + INTEGER TIES")
print("=" * 72)
a_, b_ = sp.symbols('a b', real=True)
fs = sp.Function('f')(r, th)
ws = sp.Function('w')(r, th)


def tie_Ew_alg(aa, bb):
    """full E_w (Einstein variational identity, exact incl. jets) on
    the deformed static tie, then w-jets killed (algebraic channel).
    Own build."""
    gd = sp.diag(-fs**aa, fs**bb, r**2 * (1 + ws)**2,
                 r**2 * sp.sin(th)**2 / (1 + ws)**2)
    _, gi, Ric, Rs = geom(gd, [T, r, th, ph])
    sqd = fs**(sp.Rational(1, 2) * (aa + bb)) * r**2 * sp.sin(th)
    Ew = sp.S(0)
    for (i, dgi) in ((2, 2 * r**2 * (1 + ws)),
                     (3, -2 * r**2 * sp.sin(th)**2 / (1 + ws)**3)):
        Gup = sum(gi[i, k] * gi[i, l] * Ric[k, l]
                  for k in range(4) for l in range(4)) \
            - gi[i, i] * Rs / 2
        Ew += -sqd * Gup * dgi
    for d in (sp.Derivative(ws, (r, 2)), sp.Derivative(ws, (th, 2)),
              sp.Derivative(ws, r, th), sp.Derivative(ws, r),
              sp.Derivative(ws, th)):
        Ew = Ew.subs(d, 0)
    return sp.expand(sp.cancel(sp.together(Ew)))


print("   [deformed tie, symbolic (a,b) ...]", flush=True)
Ew_ab = tie_Ew_alg(a_, b_)
Jd = Jets({fs: 'f', ws: 'w'}, [r, th], 'rh')
Ew_abj = Jd.to_jets(Ew_ab)
fjd, wjd = Jd.sym('f', ()), Jd.sym('w', ())
frd, fthd = Jd.sym('f', (0,)), Jd.sym('f', (1,))
frrd, frthd, fththd = Jd.sym('f', (0, 0)), Jd.sym('f', (0, 1)), \
    Jd.sym('f', (1, 1))
# COMPLETENESS: polynomial in ALL five f-jet symbols, every monomial:
Pd = sp.Poly(sp.expand(Ew_abj), frd, fthd, frrd, frthd, fththd)
cen = {}
for mon in Pd.monoms():
    cen[mon] = sp.simplify(sp.powsimp(Pd.coeff_monomial(mon),
                                      force=True))
print("   complete monomial census (symbolic a,b):")
for mon, c in sorted(cen.items()):
    if c != 0:
        print(f"     {mon} (f_r,f_th,f_rr,f_rth,f_thth): {c}")
mon_fth2 = (0, 2, 0, 0, 0)
mon_fthth = (0, 0, 0, 0, 1)
mon_fthlin = (0, 1, 0, 0, 0)
others_dead = all(c == 0 for m, c in cen.items()
                  if m not in (mon_fth2, mon_fthth, mon_fthlin))
P_target = a_**2 / 2 - a_ + b_**2 / 2 - b_
c1 = sp.simplify(sp.powsimp(
    cen[mon_fth2] - sp.sin(th) * fjd**(a_ / 2 + b_ / 2 - 2) * P_target
    / (1 + wjd)**3, force=True))
c2 = sp.simplify(sp.powsimp(
    cen[mon_fthth] - (a_ + b_) * fjd**(a_ / 2 + b_ / 2 - 1)
    * sp.sin(th) / (1 + wjd)**3, force=True))
c3 = sp.simplify(sp.powsimp(
    cen[mon_fthlin] + (a_ + b_) * fjd**(a_ / 2 + b_ / 2 - 1)
    * sp.cos(th) / (1 + wjd)**3, force=True))   # lin = -(a+b) cos
check("V1-10 TIE CENSUS — THE ARM'S CENSUS IS INCOMPLETE (defect "
      "found): at symbolic (a,b) the algebraic w-EL has THREE slots, "
      "not two — [f_th^2] = sin f^{(a+b)/2-2} P(a,b)/(1+w)^3 and the "
      "contamination PAIR (a+b) f^{(a+b)/2-1} [sin f_thth - cos f_th]"
      "/(1+w)^3 = (a+b) f^{(a+b)/2-1} sin^2 d_th(f_th/sin)/(1+w)^3; the "
      "arm's slot list omitted the LINEAR f_th member (its census "
      "never extracted linear slots); all other monomials vanish "
      "identically",
      others_dead and c1 == 0 and c2 == 0 and c3 == 0
      and cen[mon_fthlin] != 0)
check("V1-11 the unimodular line a + b = 0: the WHOLE contamination "
      "pair (f_thth AND the missed linear f_th slot) dies "
      "IDENTICALLY (both are proportional to a + b) and P(a,-a) = "
      "a^2 — the arm's unimodular-line verdict SURVIVES its census "
      "gap; postulate point P(1,-1)=1; zero circle (a-1)^2+(b-1)^2 "
      "= 2 passes through (0,0),(2,0),(0,2),(2,2)",
      sp.simplify(cen[mon_fthth].subs(b_, -a_)) == 0
      and sp.simplify(cen[mon_fthlin].subs(b_, -a_)) == 0
      and sp.simplify(P_target.subs(b_, -a_) - a_**2) == 0
      and P_target.subs([(a_, 1), (b_, -1)]) == 1
      and all(P_target.subs([(a_, A), (b_, B)]) == 0
              for (A, B) in ((0, 0), (2, 0), (0, 2), (2, 2))))

# INDEPENDENT integer-exponent route: full density jet EL, explicit
# metrics, NO Einstein tensor, NO symbolic exponents:
print("   [integer ties, independent full-density jet-EL route ...]",
      flush=True)
ok_int = True
for (A, B) in ((2, 0), (0, 2), (0, 0), (2, -2), (1, 1), (1, -1)):
    gd = sp.diag(-fs**A, fs**B, r**2 * (1 + ws)**2,
                 r**2 * sp.sin(th)**2 / (1 + ws)**2)
    _, _, _, Rs = geom(gd, [T, r, th, ph])
    assert (A + B) % 2 == 0
    sqd = fs**((A + B) // 2) * r**2 * sp.sin(th)
    assert sp.cancel(sqd**2 + gd.det()) == 0
    Jx = Jets({fs: 'f', ws: 'w'}, [r, th], 'rh')
    Lx = Jx.to_jets(sp.expand(sp.cancel(sqd * Rs)))
    ELx = Jx.EL2(Lx, 'w')
    # algebraic channel: kill ALL w-jets present
    for (nm, mi), s in list(Jx.J.items()):
        if nm == 'w' and mi:
            ELx = ELx.subs(s, 0)
    ELx = sp.cancel(sp.together(sp.expand(ELx)))
    fj2, wj2 = Jx.sym('f', ()), Jx.sym('w', ())
    fth2, fthth2 = Jx.sym('f', (1,)), Jx.sym('f', (1, 1))
    Pv = Ra(A**2, 2) - A + Ra(B**2, 2) - B
    tgt = (sp.sin(th) * fj2**(Ra(A + B, 2) - 2) * Pv * fth2**2
           / (1 + wj2)**3
           + (A + B) * fj2**(Ra(A + B, 2) - 1)
           * (sp.sin(th) * fthth2 - sp.cos(th) * fth2)
           / (1 + wj2)**3)
    res = sp.cancel(sp.together(sp.expand(ELx - tgt)))
    okx = (res == 0)
    ok_int = ok_int and okx
    print(f"     (a,b)=({A},{B}): P = {Pv}, contamination coeff "
          f"(a+b) = {A+B}; full-density jet-EL matches "
          f"3-slot census: {okx}")
check("V1-12 INTEGER TIES, INDEPENDENT ROUTE (their V-2): the FULL "
      "3-slot census (P(a,b) f_th^2 + (a+b) d_th(sin f_th) pair) is "
      "confirmed by full-density jet EL on explicit metrics: "
      "(2,0),(0,2),(0,0) are TADPOLE-FREE (P = 0) but (2,0),(0,2) "
      "keep the (a+b) contamination pair (incl. the slot the arm "
      "missed); (2,-2) gives P = 4 (unimodular a^2 law); (1,1) "
      "P = -1; (1,-1) reproduces the species tadpole exactly — no "
      "Einstein route, no symbolic exponents", ok_int)

# =====================================================================
print()
print("=" * 72)
print("PART 4 — A-4: THE E_f MAP ON THE FULL EH DENSITY")
print("=" * 72)
# the species' w-content on the EH density itself (div V invisible by
# V1-05, so this is EL-equivalent to the arm's GG-bulk Delta):
L_EH_w0 = L_EH.subs({wT: 0, wr: 0, wth: 0, wj: 0})
Delta_EH = sp.expand(L_EH - L_EH_w0)
print("   [EL_f of the EH-density species (second-order operator) ...]",
      flush=True)
ELf_D = J.EL2(Delta_EH, 'f')
# structural triviality note (recorded, not a check): E_f[Delta]|_{w==0}
# == 0 holds for ANY density by chain-rule commutation; verify anyway:
ELf_w0 = ELf_D
for (nm, mi), s in list(J.J.items()):
    if nm == 'w':
        ELf_w0 = ELf_w0.subs(s, 0)
check("V1-13 macro gate at w == 0 (NOTE: structurally trivial for any "
      "L - L|_{w=0} density; verified anyway, full EH density): "
      "E_f[Delta] == 0 identically at w == 0",
      sp.simplify(sp.expand(ELf_w0)) == 0)
# linearized order: no w second jets feed E_f:
wsecs = [J.sym('w', mi2) for mi2 in
         ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))]
ok_lin = True
for s in wsecs:
    v = sp.diff(ELf_D, s)
    for (nm, mi), s2 in list(J.J.items()):
        if nm == 'w':
            v = v.subs(s2, 0)
    ok_lin = ok_lin and sp.cancel(sp.together(sp.expand(v))) == 0
check("V1-14 at linearized order the species feeds E_f NO w second "
      "jets (all six coefficients vanish at w = 0; full EH density, "
      "my operator) — the q=0 f-channel cannot see w_thth",
      ok_lin)
# O(w) source: shaped-only
lin_w = sp.diff(ELf_D, wj)
for (nm, mi), s2 in list(J.J.items()):
    if nm == 'w':
        lin_w = lin_w.subs(s2, 0)
lin_w = sp.cancel(sp.together(sp.expand(lin_w)))
sph_kill = [(fth, 0)] + [(J.sym('f', mi2), 0) for mi2 in
                         ((2, 2), (0, 2), (1, 2))]
check("V1-15 the O(w) f-source is NONZERO and shaped-only (vanishes "
      "when all theta-jets of f vanish)",
      lin_w != 0 and sp.cancel(sp.expand(lin_w.subs(sph_kill))) == 0)
# spherical restriction == dL_Wwave/df. EH-density EL_f may carry
# higher theta-jets of f; kill every theta-bearing f-jet:
sph_full = [(s, 0) for (nm, mi), s in list(J.J.items())
            if nm == 'f' and 2 in mi]
ELf_sph = sp.cancel(sp.together(sp.expand(ELf_D.subs(sph_full))))
tgt_sph = sp.diff(L_Wwave, fj)
check("V1-16 on spherical f the species' FULL E_f content equals "
      "dL_Wwave/df = -2 r^2 sin [w_r^2 + w_T^2/f^2]/(1+w)^2 exactly "
      "(EH density, my operator): no new spherical-f source",
      sp.cancel(sp.together(sp.expand(ELf_sph - tgt_sph))) == 0)

# =====================================================================
print()
print("=" * 72)
print("PART 5 — A-5: THE 'ANY CURVATURE-GRADE SCALAR' SENTENCE (R^2)")
print("=" * 72)
fs2 = sp.Function('f')(r, th)
ws2 = sp.Function('w')(r, th)
g_st = sp.diag(-fs2, 1 / fs2, r**2 * (1 + ws2)**2,
               r**2 * sp.sin(th)**2 / (1 + ws2)**2)
print("   [R on the static q=0 class; density sqrt(-g) R^2; EL_w ...]",
      flush=True)
_, _, _, Rst = geom(g_st, [T, r, th, ph])
J2 = Jets({fs2: 'f', ws2: 'w'}, [r, th], 'rh')
# keep the density UNEXPANDED (the squared scalar explodes under
# expand); EL2/diff work on the factored tree, and all readouts below
# are exact rational-point evaluations:
LR2 = J2.to_jets(sp.together(sp.cancel(r**2 * sp.sin(th) * Rst))**2
                 / (r**2 * sp.sin(th)))
ELw_R2 = J2.EL2(LR2, 'w')
for (nm, mi), s in list(J2.J.items()):
    if nm == 'w' and mi:
        ELw_R2 = ELw_R2.subs(s, 0)
wj2 = J2.sym('w', ())
alg_chan = ELw_R2 - ELw_R2.subs(wj2, 0)
# census: which f-jet monomials carry the w-dependence?
tp_ = sp.Symbol('t_par', real=True)
ac_t = alg_chan.subs({sp.sin(th): 2 * tp_ / (1 + tp_**2),
                      sp.cos(th): (1 - tp_**2) / (1 + tp_**2)})
subnz = {}
for s in sorted(ac_t.free_symbols, key=str):
    if s == r:
        subnz[s] = Ra(7, 3)
    elif s == tp_:
        subnz[s] = Ra(2, 5)
    elif str(s) == 'f':
        subnz[s] = Ra(5, 2)
    elif str(s) == 'w':
        subnz[s] = Ra(3, 7)
    else:
        subnz[s] = Ra(random.randint(-9, 9), random.randint(1, 7))
nonzero = (sp.cancel(ac_t.subs(subnz)) != 0)
# does it vanish on spherical f (the acceptance filter)? exact
# rational-point evaluation (4 points), theta-jets of f killed:
sphk = [(s, 0) for (nm, mi), s in list(J2.J.items())
        if nm == 'f' and 1 in mi]
asph = alg_chan.subs(sphk)
tp2 = sp.Symbol('t_par2', real=True)
asph = asph.subs({sp.sin(th): 2 * tp2 / (1 + tp2**2),
                  sp.cos(th): (1 - tp2**2) / (1 + tp2**2)})
sph_dead = True
for _ in range(4):
    sub2 = {}
    for s in sorted(asph.free_symbols, key=str):
        if s == r:
            sub2[s] = Ra(random.randint(2, 9), random.randint(1, 4))
        elif s == tp2:
            sub2[s] = Ra(random.randint(1, 7), random.randint(2, 9))
        elif str(s) == 'f':
            sub2[s] = Ra(random.randint(1, 9), random.randint(1, 4))
        elif str(s) == 'w':
            sub2[s] = Ra(random.randint(-2, 6), 7)
        else:
            sub2[s] = Ra(random.randint(-9, 9), random.randint(1, 7))
    sph_dead = sph_dead and (sp.cancel(asph.subs(sub2)) == 0)
# is it f_th-jet-localized like the EH channel? print a compact census
print("   R^2 algebraic w-channel nonzero:", nonzero,
      "| vanishes on spherical f:", sph_dead)
check("V1-17 R^2 PROBE of the doc's sentence 'any curvature-grade "
      "scalar built on the tie carries this channel': the algebraic "
      "w-channel of sqrt(-g) R^2 is NONZERO and vanishes on spherical "
      "f (channel exists for at least one non-EH curvature scalar; "
      "existence supported — the sentence's universal quantifier "
      "remains UNPROVEN, scope note in the verdict)",
      nonzero and sph_dead)

print()
print(f"TOTALS: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
for x in FAIL:
    print("FAILED:", x)
