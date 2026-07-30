#!/usr/bin/env python3
"""BLIND VERIFIER independent check -- P4 gradient seat (udt_p4_gradient_seat_2026-07-29).

Independent implementation: own jet formalism (different symbol layout, own total
derivative, own Euler operators) plus functions-of-x spot routes for the witnesses.
Adversarial: includes counter-computations (V-C1 nondegeneracy probe, V-C2 field-coupled
m'' probe) hunting the massive-landing leg hardest per the F-G1 duty.
Exit 0 iff all verifier checks pass (counter-probes PASS when they demonstrate the
claimed gap/scope, as labeled).
"""
import sys
import sympy as sp
from sympy import Function, symbols, Symbol, exp, sin, pi, diff, expand, simplify

FAIL = []


def V(name, ok, note=""):
    print(("[VPASS] " if ok else "[VFAIL] ") + name + (" -- " + note if note else ""))
    if not ok:
        FAIL.append(name)


# ---------- own jet layout ----------
NJ = 7
P = symbols("P0:%d" % NJ)   # depth p jets
F = symbols("Fj0:%d" % NJ)  # f jets
H = symbols("Hj0:%d" % NJ)  # h jets
L = symbols("Lj0:%d" % NJ)  # lambda jets
K = symbols("Kj0:%d" % NJ)  # k_mod jets
CH = [list(P), list(F), list(H), list(L), list(K)]
VP = symbols("vP0:5"); VF = symbols("vF0:5"); VH = symbols("vH0:5"); VL = symbols("vL0:5")
CHV = CH + [list(VP), list(VF), list(VH), list(VL)]


def mkD(chains):
    def D(e):
        out = sp.Integer(0)
        for c in chains:
            for i in range(len(c) - 1):
                d = diff(e, c[i])
                if d != 0:
                    out += d * c[i + 1]
        return out
    return D


D = mkD(CH)
DF = mkD(CH[:3])          # field chains only
DV = mkD(CHV)


def Ef(S, ch):            # field Euler row (1st order)
    return expand(diff(S, ch[0]) - D(diff(S, ch[1])))


def Em(S, ch):            # moduli Euler row (2nd order, registered m-jet alphabet)
    return expand(diff(S, ch[0]) - D(diff(S, ch[1])) + D(D(diff(S, ch[2]))))


x = Symbol("x"); ell = Symbol("ell", positive=True)
gp = Symbol("gp", nonzero=True)
gf, gh, gx = symbols("gf gh gx", real=True)
LG = gp * P[1]**2 / 2 + (gf * F[1]**2 + 2 * gx * F[1] * H[1] + gh * H[1]**2) / 2
Lfh = (gf * F[1]**2 + 2 * gx * F[1] * H[1] + gh * H[1]**2) / 2
LOCK = {c[i]: 0 for c in [list(L), list(K)] for i in range(1, NJ)}

# ===== V1: TG-1 IBP identity, arbitrary Function (own layout) =====
S = Function("S")(P[0], P[1], F[0], F[1], H[0], H[1], L[0], L[1], L[2])
dS = (diff(S, P[0]) * VP[0] + diff(S, P[1]) * VP[1] + diff(S, F[0]) * VF[0]
      + diff(S, F[1]) * VF[1] + diff(S, H[0]) * VH[0] + diff(S, H[1]) * VH[1]
      + diff(S, L[0]) * VL[0] + diff(S, L[1]) * VL[1] + diff(S, L[2]) * VL[2])
Th = (diff(S, P[1]) * VP[0] + diff(S, F[1]) * VF[0] + diff(S, H[1]) * VH[0]
      + (diff(S, L[1]) - D(diff(S, L[2]))) * VL[0] + diff(S, L[2]) * VL[1])
res = expand(dS - Ef(S, P) * VP[0] - Ef(S, F) * VF[0] - Ef(S, H) * VH[0]
             - Em(S, L) * VL[0] - DV(Th))
V("V1_ibp_rows_wall_slots", res == 0, "R_mu = full 2nd-order Euler op; N3 slots as stated")

# ===== V2: configuration-dependent weight -- general no-m-jet response =====
Sg = Function("Sg")(P[0], P[1], F[0], F[1], H[0], H[1], L[0])
ok2 = True
for ch in (P, F, H):
    dfull = Ef(Sg, ch)
    dconst = expand(diff(Sg, ch[0]) - DF(diff(Sg, ch[1])))
    ok2 &= expand(dfull - dconst + L[1] * diff(Sg, L[0], ch[1])) == 0
aF = Function("aF")(L[0])
W = exp(aF * P[0])
Sq = W * LG
ok2 &= expand((Ef(Sq, P) - (expand(diff(Sq, P[0]) - DF(diff(Sq, P[1])))))
              + W * diff(aF, L[0]) * L[1] * P[0] * gp * P[1]) == 0
ok2 &= expand(Em(Sq, L) - diff(aF, L[0]) * P[0] * Sq) == 0 and Em(Sq, K) == 0
V("V2_weight_single_new_term", bool(ok2),
  "general rule: E_full - E_const = -lam' d2S/(dlam du'); anchored member = the stated "
  "term; lam-row algebraic a_F' p0 W Ltil; k_mod row vacuous")

# ===== V3: lock-reduction, EXTENDED quadratic set (incl. km2/l2-km cross terms) =====
args = (P[1], F[0], F[1], H[0], H[1], L[0], K[0])
cs = [Function("q%d" % i)(*args) for i in range(9)]
Sext = W * (cs[0] * L[1]**2 + cs[1] * L[1] * L[2] + cs[2] * L[2]**2
            + cs[3] * K[1]**2 + cs[4] * K[1] * K[2] + cs[5] * K[2]**2
            + cs[6] * L[1] * K[1] + cs[7] * L[1] * K[2] + cs[8] * L[2] * K[1])
ok3 = all(expand(r.subs(LOCK)) == 0 for r in
          [Em(Sext, L), Em(Sext, K), Ef(Sext, P), Ef(Sext, F), Ef(Sext, H)])
V("V3_lock_reduction_extended_set", bool(ok3),
  "verifier's LARGER quadratic set (all lam/k_mod jet quadratics) also vanishes at lock")

# ===== V4: the landing -- affine forced + exact split + NONDEGENERACY PROBE =====
S40 = LG                                    # W == 1 at the lam = 0 landing
r4 = [expand(Ef(S40, ch).subs(LOCK)) for ch in (P, F, H)]
sol = sp.solve([sp.Eq(r, 0) for r in r4], [P[2], F[2], H[2]], dict=True)
ok4 = sol == [{P[2]: 0, F[2]: 0, H[2]: 0}]
lrow = expand(Em(exp(2 * L[0] * P[0]) * LG, L).subs(LOCK).subs(L[0], 0))
ok4 &= expand(lrow - 2 * P[0] * LG) == 0
a0, a1 = symbols("a0 a1", real=True)
pol = sp.Poly(2 * (a0 + a1 * x) * LG.subs(P[1], a1), x)
ok4 &= (pol.degree() == 1
        and expand(pol.all_coeffs()[0] - 2 * a1 * LG.subs(P[1], a1)) == 0
        and expand(pol.all_coeffs()[1] - 2 * a0 * LG.subs(P[1], a1)) == 0)
V("V4_landing_affine_and_split", bool(ok4), "affine atlas unique (GENERIC solve); "
  "lam-row 2 p0 LtG; poly split {LtG=0} U {p==0}")
# COUNTER-PROBE: at Delta_G = gf*gh - gx^2 = 0 the affine forcing FAILS (kernel dir)
r_deg = [r.subs({gf: 1, gh: 1, gx: 1}) for r in r4[1:]]
kernel_sol = (expand(r_deg[0].subs({F[2]: 1, H[2]: -1})) == 0
              and expand(r_deg[1].subs({F[2]: 1, H[2]: -1})) == 0)
V("VC1_degenerate_G_probe", kernel_sol,
  "COUNTER-COMPUTATION: gf=gh=gx=1 (Delta_G=0): f''=1, h''=-1 solves the f/h rows -- "
  "affine atlas NOT forced at degenerate (f,h) block; landing claims need the "
  "nondegeneracy (Delta_G != 0 / W3-exclusion) stamp explicit")

# ===== V5: lock emergence, lam as arbitrary Function of x (functions route) =====
xf = Symbol("x")
lam = Function("lam")(xf)
f0c, f1c, h0c, h1c = symbols("f0c f1c h0c h1c", real=True)
ffun = f0c + f1c * xf
hfun = h0c + h1c * xf
eps = Symbol("eps")
pp = eps * Function("vp")(xf)
Wp = exp(2 * lam * pp)
LGp = gp * diff(pp, xf)**2 / 2 + (gf * diff(ffun, xf)**2
      + 2 * gx * diff(ffun, xf) * diff(hfun, xf) + gh * diff(hfun, xf)**2) / 2
Sp = Wp * LGp
prow_fn = diff(Sp, eps).subs(eps, 0)  # first variation in p about p == 0
Lfh_c = (gf * f1c**2 + 2 * gx * f1c * h1c + gh * h1c**2) / 2
V("V5_lock_emergence_functions_route",
  simplify(prow_fn - 2 * lam * Function("vp")(xf) * Lfh_c) == 0,
  "on p==0, f/h affine, lam(x) ARBITRARY Function: delta_p S = 2 lam(x) Ltil_fh vp(x) "
  "exactly (no boundary piece: dS/dp1 prop p1 = 0) => lam(x) == 0 forced wherever "
  "Ltil_fh != 0 -- emergence confirmed on the general field, functions-of-x route")

# ===== V6: massive locked witness -- all five rows + energy (own layout) =====
kap = Symbol("kappa", real=True)
km = kap * sin(pi * xf / ell)
S4 = exp(2 * L[0] * P[0]) * LG
subw = {}
for ch, base in [(P, sp.Integer(0)), (F, ffun), (H, hfun), (L, sp.Integer(0)),
                 (K, km)]:
    for i in range(NJ):
        subw[ch[i]] = diff(base, xf, i) if i else base
rows5 = [Ef(S4, P), Ef(S4, F), Ef(S4, H), Em(S4, L), Em(S4, K)]
ok6 = all(simplify(r.subs(subw, simultaneous=True)) == 0 for r in rows5)
E6 = (P[1] * diff(S4, P[1]) + F[1] * diff(S4, F[1]) + H[1] * diff(S4, H[1]) - S4)
ok6 &= simplify(E6.subs(subw, simultaneous=True) - Lfh_c) == 0
V("V6_massive_witness_all_rows_energy", bool(ok6),
  "p==0/affine/lam==0/k_mod=kappa sin: all five rows 0; E = Ltil_fh(f1,h1) generically "
  "nonzero, symbolic")

# ===== V7: parity solves (lock-at-zero; affine kills; witness oddness) =====
c = Symbol("c")
ok7 = sp.solve(sp.Eq(c, -c), c) == [0]
fA, fB = symbols("fA fB")
ok7 &= sp.solve([sp.Eq(fA + fB * ell, 0), sp.Eq(fA - fB * ell, 0)], [fA, fB],
                dict=True) == [{fA: 0, fB: 0}]
sw = Symbol("s", real=True)
ok7 &= (simplify(km.subs(xf, ell + sw) + km.subs(xf, ell - sw)) == 0
        and simplify(km.subs(xf, -ell + sw) + km.subs(xf, -ell - sw)) == 0)
V("V7_parity_solves", bool(ok7),
  "odd wall value = 0; both-wall-odd affine killed; sin witness exactly odd about BOTH "
  "walls (consistent w/ Route-P 'forced ODD about the wall' + CANON fold-at-seal)")

# ===== V8: linear-jet layer, both witnesses + the m'' COUNTER-PROBE =====
Bo = F[0]
Ba = H[1] * F[0] - F[1] * H[0]
So = exp(2 * L[0] * P[0]) * (LG + Bo * L[1])
Sa = exp(2 * L[0] * P[0]) * (LG + Ba * L[1])
ok8 = simplify(Em(So, L).subs(subw, simultaneous=True) + f1c) == 0
ok8 &= all(simplify(r.subs(subw, simultaneous=True)) == 0 for r in
           [Ef(Sa, P), Ef(Sa, F), Ef(Sa, H), Em(Sa, L), Em(Sa, K)])
V("V8_linear_jet_witnesses", bool(ok8),
  "B=f0 obstructs (locked row -f1); B=h1 f0 - f1 h0 admits (all rows 0 on the same "
  "massive witness); both pass Route-D exclusions: local jet arguments, no bare p0, "
  "no nonlocal/absolute-point entries; f0/h0 are banked Slice-2b response arguments")
# COUNTER-PROBE: field-coupled m'' content C = f0^2/2 -- the stated B-only condition
# is vacuously satisfied (B = 0) yet the massive class is CUT:
Sc = exp(2 * L[0] * P[0]) * (LG + (F[0]**2 / 2) * L[2])
lrow_c = simplify(Em(Sc, L).subs(subw, simultaneous=True))
V("VC2_mpp_field_coupled_probe", simplify(lrow_c - f1c**2) == 0,
  "COUNTER-COMPUTATION: S = W(LtG + (f0^2/2) m'') has locked lam-row = f1^2 != 0 on "
  "the massive witness while the package's stated 'EXACT GENERAL CONDITION' (B-terms "
  "only) is vacuously satisfied -- the condition as PHRASED is complete only for "
  "m'-linear content; m'' field-coupled content adds Dx^2(W_F C)|lock (present in "
  "G2b's closed form, typed in G2j, but absent from the 2.3/JR5/DSU(b) formula)")

# ===== V9: Ostrogradsky first integral (own layout, arbitrary Function) =====
Eo = expand(P[1] * diff(S, P[1]) + F[1] * diff(S, F[1]) + H[1] * diff(S, H[1])
            + L[1] * (diff(S, L[1]) - D(diff(S, L[2]))) + L[2] * diff(S, L[2]) - S)
belt = expand(D(Eo) + P[1] * Ef(S, P) + F[1] * Ef(S, F) + H[1] * Ef(S, H)
              + L[1] * Em(S, L))
V("V9_ostrogradsky_first_integral", belt == 0,
  "Dx(E_ext) = -sum u' E_a - m' R_m identically (M-GEN available on the jet alphabet)")

# ===== V10: jet-quadratic forcing + tuned branch =====
cq = Symbol("cq", nonzero=True)
Sjq = exp(2 * L[0] * P[0]) * (LG + cq * L[1]**2 / 2)
p00 = Symbol("p00", real=True)
subc = {}
for ch, base in [(P, p00), (F, f0c), (H, h0c)]:
    for i in range(NJ):
        subc[ch[i]] = base if i == 0 else sp.Integer(0)
lamF = Function("lm")(xf)
for i in range(NJ):
    subc[L[i]] = diff(lamF, xf, i) if i else lamF
    subc[K[i]] = sp.Integer(0)
prow_jq = simplify(Ef(Sjq, P).subs(subc, simultaneous=True)
                   / (cq * exp(2 * lamF * p00)))
ok10 = simplify(prow_jq - lamF * diff(lamF, xf)**2) == 0
beta = Symbol("beta", real=True)
subt = dict(subw)
subt[L[0]] = beta * xf
subt[L[1]] = beta
for i in range(2, NJ):
    subt[L[i]] = sp.Integer(0)
prow_t = simplify(Ef(Sjq, P).subs(subt, simultaneous=True))
lrow_t = simplify(Em(Sjq, L).subs(subt, simultaneous=True))
Ejq = (P[1] * diff(Sjq, P[1]) + F[1] * diff(Sjq, F[1]) + H[1] * diff(Sjq, H[1])
       + L[1] * diff(Sjq, L[1]) - Sjq)
Et = simplify(Ejq.subs(subt, simultaneous=True))
ok10 &= simplify(prow_t - 2 * beta * xf * (Lfh_c + cq * beta**2 / 2)) == 0
ok10 &= lrow_t == 0 and simplify(Et - (Lfh_c + cq * beta**2 / 2)) == 0
V("V10_jet_quadratic_and_tuned", bool(ok10),
  "p-row factor lam lam'^2 (lock forced on constant-field bg, w/ continuity); tuned "
  "branch admitted iff Ltil_fh = -c beta^2/2 with E_ext = 0 exactly; parity kills beta")

# ===== V11: P1-triad locked leg -- p-row escape kill + on-shell E = W Ltil =====
Stri = exp(P[0]) * LG
prow_tri = expand(Ef(Stri, P).subs(LOCK).subs(
    {P[0]: 0, P[1]: 0, P[2]: 0, F[2]: 0, H[2]: 0}))
Etri = expand(P[1] * diff(Stri, P[1]) + F[1] * diff(Stri, F[1])
              + H[1] * diff(Stri, H[1]) - Stri)
V("V11_triad_prow_kill_and_E_density",
  expand(prow_tri - Lfh) == 0 and expand(Etri - Stri) == 0,
  "at p==0 affine the p-row = a_F Ltil_fh = Ltil_fh => E0 = 0 (escape killed); "
  "E-density = W Ltil on the quadratic class, so the locked lam-row a_F' p0 W Ltil = "
  "2 p0 E-density -- the '2 E0 p0(x) = 0' reading confirmed independently")

# ===== V12: masses on the landing class + M-WALL divergence-law consistency =====
from sympy import integrate
MG = 2 * ell * Lfh_c
V("V12_masses_landing",
  integrate(sp.Integer(1), (xf, -ell, ell)) == 2 * ell
  and simplify(integrate(Lfh_c, (xf, -ell, ell)) - MG) == 0,
  "V = 2 ell; M-DENS-proper = M-DENS-coord = M-GEN = 2 ell E0; M-WALL = a_F * M-GEN = "
  "0 at a_F = 0 (banked divergence law, consistent) and [pi_p] = 0 at p1 == 0")

print()
if FAIL:
    print("VERIFIER RESULT: %d FAILURES: %s" % (len(FAIL), FAIL))
    sys.exit(1)
print("VERIFIER RESULT: all independent checks + counter-probes as labeled PASS")
sys.exit(0)
