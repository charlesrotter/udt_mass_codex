#!/usr/bin/env python3
"""W6 ARM-1 (UNCOVER) — shared builders for the unreduced coupled
fluctuation operator.  New file (repo discipline); validated patterns
are COPIED from the committed machinery (w5_arm1_verifier2_branch.py:
geom/gg_split/Jets/derad; w4a_verifier1_sym.py: covariant C1 build)
— committed files untouched.

THE SYSTEM (W6 declaration, binding; nothing invented):
  S = S_C1 + kappa * S_species + beta * S_Dcell   on the q-on,
  time-on class:
    g = [[-f,0,0,0],[0,1/f,q,0],[0,q,r^2 W,0],[0,0,0,r^2 sin^2/W]],
    W = (1+w)^2,  fields f, q, w functions of (T, r, theta),
    sqrt(-g) = r sin(th) sqrt(D)/(1+w),  D = r^2 W - f q^2.
  L_C1   = (c/2) e^{-2 phi} g^{ab} phi_a phi_b sqrt(-g),
           phi = -(1/2) ln f, c = 2 (positive banked convention ==
           corpus c = -2; convention lock V1-01 / W5S-A1).
  L_species = Delta_w = LGG - LGG|_{w-content = 0}   (the W5 species
           representative: the Gamma-Gamma bulk of sqrt(-g) R with its
           w-free part subtracted; w-row representative-unambiguous
           per VW5-1 V2-13; the subtraction is carried in the f- and
           q-rows where it is NOT EL-invisible).  At q = 0 its EL
           content equals EL[W_wave + D_alg] (gated in script A) —
           "kappa (W_wave + D_alg)" in the W6 declaration names this
           object by its q = 0 closed form.
  D_cell = (c/4) sin(th) [w f_th^2/f + q f_r f_th]   (banked
           test-both branch, w4a_system.py line 22, c = 2).

CONVENTIONS CARRIED (all banked):
  R-areal canon rho = r; polar r > 0, 1 + w > 0, signature-legal
  D > 0; same-minus time-row stack is theorem-grade (VN) with the
  Q != 0 convention — NOTE the (a,b) = (g_Tr, g_Tth) enlargement is
  OUTSIDE the declared three-field class; its fluctuation-level
  effect (the same-minus delta-f_T sector sign flip) is a labeled
  premise on time-row SIGNATURE readings only (carried in script C);
  it cannot touch the static angular-character deliverable.

OPERATOR CONVENTIONS (fixed here, used by all w6_arm1 scripts):
  Background fields X in {f, q, w}; first-jet symbols X_T, X_r, X_h
  (h = theta).  L is FIRST-ORDER in all jets (asserted in script A).
  Quadratic fluctuation form about a background:
    Q2 = (1/2) Int [ H[(X,m),(Y,n)] dX_m dY_n
                     + 2 B[X,(Y,n)] dX dY_n + C[X,Y] dX dY ]
  with H[(X,m),(Y,n)] = d2 L/d X_m d Y_n  (9x9, symmetric),
       B[X,(Y,n)]     = d2 L/d X  d Y_n   (3x9),
       C[X,Y]         = d2 L/d X  d Y     (3x3, symmetric),
  all evaluated on the background.  Fluctuation EL operator, row X:
    (O du)_X = sum_Y [ C[X,Y] dY + B[X,(Y,n)] dY_n
                       - D_m( B[Y,(X,m)] dY + H[(X,m),(Y,n)] dY_n ) ]
  PRINCIPAL SYMBOL (d_m -> i k_m):
    sigma_XY(k) = sum_{m,n} H[(X,m),(Y,n)] k_m k_n.
  Second-jet coefficient of Y_mn in row X:
    mu = nu : -H[(X,m),(Y,m)];
    mu != nu: -(H[(X,m),(Y,n)] + H[(X,n),(Y,m)]).
"""
import time
import sympy as sp
from sympy import Rational as Ra

T, th, ph = sp.symbols('T theta varphi', real=True)
r = sp.Symbol('r', positive=True)
kap, beta = sp.symbols('kappa beta', real=True)
COORDS = [T, r, th]
TAGS = 'Trh'
CC = sp.Integer(2)            # the convention constant c = +2 (banked)


# ------------------------------------------------------------------
# geometry engines (copied patterns: w5_arm1_verifier2_branch.py)
# ------------------------------------------------------------------
def geom(g, xs):
    """Christoffel (index dict), inverse, Ricci, Ricci scalar."""
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
                Gam[(c, a, b)] = Gam[(c, b, a)] = sp.together(e)
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
            Ric[a, b] = Ric[b, a] = sp.together(e)
    Rs = sum(gi[a, b] * Ric[a, b] for a in range(n) for b in range(n))
    return Gam, gi, Ric, Rs


def gg_split(g, xs, sq):
    """Gamma-Gamma split: sqrt(-g) R = LGG + sum_a D_a V^a."""
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
                Gam[(c, a, b)] = Gam[(c, b, a)] = sp.together(e)
    V = [sq * sum(gi[a, b] * Gam[(c, a, b)] - gi[c, b] * Gam[(a, a, b)]
                  for a in range(n) for b in range(n))
         for c in range(n)]
    LGG = sq * sum(gi[a, b] * (Gam[(c, a, d)] * Gam[(d, b, c)]
                               - Gam[(c, a, b)] * Gam[(d, d, c)])
                   for a in range(n) for b in range(n)
                   for c in range(n) for d in range(n))
    return LGG, V


class Jets:
    """jet-symbol conversion + total derivative + 2nd-order EL
    (copied pattern: w5_arm1_verifier2_branch.py)."""

    def __init__(self, fields, coords, tags):
        self.fields, self.coords, self.tags = fields, coords, tags
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


def derad(expr, base_target, root_sub):
    """replace Pow(b, p/2) by (s*root_sub)**p whenever b ==
    s^2 * base_target (copied: w5_arm1_verifier2_branch.py)."""
    def pred(e):
        return (e.is_Pow and getattr(e.exp, 'is_Rational', False)
                and e.exp.q == 2)

    def rep(e):
        ratio = sp.cancel(sp.together(e.base / base_target))
        rt = sp.sqrt(sp.factor(ratio))
        if not any(pred(p) for p in rt.atoms(sp.Pow)):
            return (rt * root_sub) ** (2 * e.exp)
        return e
    return expr.replace(pred, rep)


# ------------------------------------------------------------------
# the W6 density builders
# ------------------------------------------------------------------
def build_fields():
    f = sp.Function('f')(T, r, th)
    q = sp.Function('q')(T, r, th)
    w = sp.Function('w')(T, r, th)
    return f, q, w


def build_metric(f, q, w):
    W = (1 + w) ** 2
    g4 = sp.Matrix([[-f, 0, 0, 0],
                    [0, 1 / f, q, 0],
                    [0, q, r ** 2 * W, 0],
                    [0, 0, 0, r ** 2 * sp.sin(th) ** 2 / W]])
    D = r ** 2 * W - f * q ** 2
    sq = r * sp.sin(th) * sp.sqrt(D) / (1 + w)
    return g4, D, sq


def build_LC1(f, q, w, g4, sq):
    """covariant C1, positive banked convention c = +2 (lock V1-01):
    L_C1 = (c/2) f K sqrt(-g), K = g^{ab} phi_a phi_b, phi=-(1/2)ln f,
    a,b over (T, r, th) (g^{T i} = 0 on this class)."""
    gi = g4.inv()
    phiT = -sp.diff(f, T) / (2 * f)
    phir = -sp.diff(f, r) / (2 * f)
    phith = -sp.diff(f, th) / (2 * f)
    K = (gi[0, 0] * phiT ** 2 + gi[1, 1] * phir ** 2
         + 2 * gi[1, 2] * phir * phith + gi[2, 2] * phith ** 2)
    return (CC / 2) * f * K * sq


def build_Dcell(f, q, w):
    """banked test-both branch (w4a_system.py line 22), c = 2."""
    return (CC / 4) * sp.sin(th) * (w * sp.diff(f, th) ** 2 / f
                                    + q * sp.diff(f, r)
                                    * sp.diff(f, th))


def build_all_jets():
    """returns (Jets instance, jet density dict) with everything in
    first-jet symbols: L_C1, LGG, LGG0 (w-content stripped), Delta_w,
    D_cell, L_total(kappa, beta)."""
    f, q, w = build_fields()
    g4, D, sq = build_metric(f, q, w)
    LC1 = build_LC1(f, q, w, g4, sq)
    LGG, V = gg_split(g4, [T, r, th, ph], sq)
    Dc = build_Dcell(f, q, w)
    J = Jets({f: 'f', q: 'q', w: 'w'}, COORDS, TAGS)
    LC1_j = J.to_jets(LC1)
    LGG_j = J.to_jets(LGG)
    Dc_j = J.to_jets(Dc)
    wsub = {J.sym('w', ()): 0, J.sym('w', (0,)): 0,
            J.sym('w', (1,)): 0, J.sym('w', (2,)): 0}
    LGG0_j = LGG_j.subs(wsub)
    Dw_j = LGG_j - LGG0_j
    Ltot = LC1_j + kap * Dw_j + beta * Dc_j
    dens = {'LC1': LC1_j, 'LGG': LGG_j, 'LGG0': LGG0_j, 'Dw': Dw_j,
            'Dcell': Dc_j, 'L': Ltot}
    return J, dens, (f, q, w, g4, D, sq, V)


FIELDS = ('f', 'q', 'w')


def jet_syms(J):
    """convenience: dict name -> 0-jet, and (name, i) -> 1-jet."""
    u = {nm: J.sym(nm, ()) for nm in FIELDS}
    j1 = {(nm, i): J.sym(nm, (i,)) for nm in FIELDS for i in range(3)}
    return u, j1


def blocks(J, L):
    """H (9x9 as dict), B (3x9 dict), C (3x3 dict) of a first-jet
    density L, exact (cancel/together applied)."""
    u, j1 = jet_syms(J)
    H, B, C = {}, {}, {}
    keys = [(nm, i) for nm in FIELDS for i in range(3)]
    for a, ka in enumerate(keys):
        for kb in keys[a:]:
            e = sp.diff(sp.diff(L, j1[ka]), j1[kb])
            e = sp.cancel(sp.together(e))
            H[(ka, kb)] = H[(kb, ka)] = e
    for nm in FIELDS:
        for kb in keys:
            e = sp.cancel(sp.together(sp.diff(sp.diff(L, u[nm]),
                                              j1[kb])))
            B[(nm, kb)] = e
    for a, na in enumerate(FIELDS):
        for nb in FIELDS[a:]:
            e = sp.cancel(sp.together(sp.diff(sp.diff(L, u[na]),
                                              u[nb])))
            C[(na, nb)] = C[(nb, na)] = e
    return H, B, C


def save_blocks(path, J, H, B, C, extra=None):
    """checkpoint: srepr dump (rerun-safe; loaders re-verify)."""
    with open(path, 'w') as fh:
        for (ka, kb), v in H.items():
            fh.write(f"H|{ka[0]},{ka[1]}|{kb[0]},{kb[1]}|"
                     f"{sp.srepr(v)}\n")
        for (nm, kb), v in B.items():
            fh.write(f"B|{nm}|{kb[0]},{kb[1]}|{sp.srepr(v)}\n")
        for (na, nb), v in C.items():
            fh.write(f"C|{na}|{nb}|{sp.srepr(v)}\n")
        for k, v in (extra or {}).items():
            fh.write(f"X|{k}|{sp.srepr(v)}\n")


def load_blocks(path):
    H, B, C, X = {}, {}, {}, {}
    with open(path) as fh:
        for line in fh:
            parts = line.rstrip('\n').split('|')
            if parts[0] == 'H':
                a = (parts[1].split(',')[0], int(parts[1].split(',')[1]))
                b = (parts[2].split(',')[0], int(parts[2].split(',')[1]))
                H[(a, b)] = sp.sympify(parts[3])
            elif parts[0] == 'B':
                b = (parts[2].split(',')[0], int(parts[2].split(',')[1]))
                B[(parts[1], b)] = sp.sympify(parts[3])
            elif parts[0] == 'C':
                C[(parts[1], parts[2])] = sp.sympify(parts[3])
            else:
                X[parts[1]] = sp.sympify(parts[2])
    return H, B, C, X


# ------------------------------------------------------------------
# exact rational background points
# ------------------------------------------------------------------
def tan_half(expr, tp):
    return expr.subs({sp.sin(th): 2 * tp / (1 + tp ** 2),
                      sp.cos(th): (1 - tp ** 2) / (1 + tp ** 2)})


def qstar_expr(fv, frv, fthv, wv):
    """C1's algebraic q-stationarity branch (V2-06): q* =
    2 r^2 W f_r f_th / (f r^2 W f_r^2 + f_th^2), W = (1+w)^2."""
    Wv = (1 + wv) ** 2
    return 2 * r ** 2 * Wv * frv * fthv / (fv * r ** 2 * Wv
                                           * frv ** 2 + fthv ** 2)
