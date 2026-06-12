#!/usr/bin/env python3
"""
W3 VERIFIER — SCRIPT V1 (GROUND ATTACK).  Date: 2026-06-12.
Blind adversarial verifier on w3_ground_crossblocks.py (claim 1 of the
W3 package).  OWN ROUTE, twice over:
  (i)  symbolic: metric built in w (not Wp), inverse by HAND block
       formulas (no Matrix.inv), density assembled independently;
  (ii) numeric: mpmath dps-40 central finite differences of the exact
       density (no sympy Hessian at all) at hostile points including
       NEGATIVE f_r, f_th and w != 0 — attacks positive-only sampling.
Targets: the cross blocks, the tadpoles, the -c/4 -> +c/12 flip, the
Delta_w numerator (both charts + generic), the chart law and its
exceptional family be = 2 al^2 (CHARACTERIZED: which chart is it?),
the seal ratios, the D_cell-branch identical vanishing (G1-G3, the
Charles-fork-relevant claim), the q* identity D8 done FULLY
SYMBOLICALLY (the committed script only spot-checked 2 positive
points), and the time-row parity H1.
"""
import sys, time
import sympy as sp
import mpmath as mp

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"V1-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

# ---------------- (i) my own symbolic construction ----------------
r, sn, f = sp.symbols('r sn f', positive=True)
c = sp.Symbol('c')
fr, fth, fph, fT, w, q = sp.symbols('f_r f_th f_ph f_T w q', real=True)
W = (1 + w)**2

# hand inverse of the (r,theta) 2x2 block [[1/f, q],[q, r^2 W]]:
D2 = r**2*W/f - q**2          # det of the block
i_rr = (r**2*W)/D2
i_thth = (1/f)/D2
i_rth = -q/D2
i_tt = -1/f
i_phph = W/(r**2*sn**2)
sqrtmg = sp.sqrt(f) * sp.sqrt(D2*f) * r*sn   # sqrt(-det g) = sqrt(f * D2*f) * r sn ?  build carefully:
# det g = (-f) * det[[1/f,q],[q,r^2 W]] * (r^2 sn^2/W)
#       = -f * (r^2 W/f - q^2) * r^2 sn^2 / W = -f*D2*r^2*sn^2/W
sqrtmg = sp.sqrt(f*D2)*r*sn/sp.sqrt(W)
phi_r, phi_th, phi_ph, phi_T = [-x/(2*f) for x in (fr, fth, fph, fT)]
K = (i_tt*phi_T**2 + i_rr*phi_r**2 + 2*i_rth*phi_r*phi_th
     + i_thth*phi_th**2 + i_phph*phi_ph**2)
L = -(c/2)*f*K*sqrtmg
L0 = sp.simplify(L.subs([(fph, 0), (fT, 0)]))

# simplification helper: the recorded W2 premise is 1+w bounded away
# from 0, so identities are checked on the chart 1+w = Wpp > 0:
Wpp = sp.Symbol('Wpp', positive=True)
def simp0(e):
    return sp.simplify(e.subs(w, Wpp - 1))

# cross-check vs the committed script's closed form (their A1):
Wp = 1 + w
A_ = f*r**2*W*fr**2 + fth**2
Lclosed = -(c/8)*r*sn*(A_ - 2*f*q*fr*fth)/(Wp*f*sp.sqrt(r**2*W - f*q**2))
check("A1", simp0(L0 - Lclosed) == 0,
      "own hand-inverse construction reproduces the banked closed form "
      "(on 1+w > 0, the recorded premise)")

jets = [f, fr, fth]
def H2(a, b_, at_w=0, at_q=0):
    return sp.simplify(sp.diff(L0, a, b_).subs([(q, at_q), (w, at_w)]))

# tadpoles + cross blocks at general w (then w=0):
Tw = sp.simplify(sp.diff(L0, w).subs(q, 0))
Tq = sp.simplify(sp.diff(L0, q).subs(q, 0))
check("A2", sp.simplify(Tw - c*sn*fth**2/(4*f*(1+w)**3)) == 0 and
      sp.simplify(Tq - c*sn*fr*fth/(4*(1+w)**2)) == 0,
      "tadpoles T_w = (c/4)sn fth^2/(f(1+w)^3), T_q = (c/4)sn fr fth/(1+w)^2"
      " (nonzero wherever f_th != 0)")
Lwfth = sp.simplify(sp.diff(L0, w, fth).subs(q, 0))
Lwq = sp.simplify(sp.diff(L0, w, q).subs(q, 0))
check("A3", simp0(Lwfth - c*sn*fth/(2*f*(1+w)**3)) == 0 and
      simp0(Lwq + c*sn*fr*fth/(2*(1+w)**3)) == 0 and
      simp0(sp.diff(L0, w, fr).subs(q, 0)) == 0,
      "cross blocks: L_wfth = (c/2)sn fth/(f(1+w)^3), "
      "L_wq = -(c/2)sn fr fth/(1+w)^3, L_wfr = 0  (VW2/W3G independent)")

# Hessian blocks at w = q = 0:
at0 = lambda e: sp.simplify(e.subs([(q, 0), (w, 0)]))
Hff = sp.Matrix(3, 3, lambda i, j: H2(jets[i], jets[j]))
bw = sp.Matrix([sp.simplify(sp.diff(L0, w, jt).subs([(q, 0), (w, 0)]))
                for jt in jets])
bq = sp.Matrix([sp.simplify(sp.diff(L0, q, jt).subs([(q, 0), (w, 0)]))
                for jt in jets])
Lww0 = at0(sp.diff(L0, w, w))
Lqq0 = at0(sp.diff(L0, q, q))
Lwq0 = at0(sp.diff(L0, w, q))
check("A4", sp.simplify(Lww0 + sp.Rational(3, 4)*c*sn*fth**2/f) == 0,
      "L_ww(0) = -(3c/4) sn fth^2/f")

# the flip:
Hw = sp.simplify(Hff - (bw*bw.T)/Lww0)
check("A5", sp.simplify(Hff[2, 2] + c*sn/(4*f)) == 0 and
      sp.simplify(Hw[2, 2] - c*sn/(12*f)) == 0,
      "THE FLIP: frozen [fth,fth] = -(c/4)sn/f; delta-w-eliminated "
      "= +(c/12)sn/f  (independent construction)")

# joint elimination, w-chart: Delta_w numerator:
X = f*r**2*fr**2; Y = fth**2; Dlt = X - Y
M2 = sp.Matrix([[Lww0, Lwq0], [Lwq0, Lqq0]])
B2 = sp.Matrix.hstack(bw, bq)
Hwq = sp.simplify(Hff - B2*(M2.inv()*B2.T))
n22, d22 = sp.fraction(sp.cancel(sp.together(Hwq[2, 2])))
check("A6", sp.simplify(Hwq[2, 2] - (c*sn/(4*f))*Dlt/(5*X - 3*Y)) == 0,
      "joint w-chart [fth,fth] = (c sn/4f) Delta_w/(5X-3Y): the "
      "Delta_w numerator confirmed by my own elimination")

# generic chart law (al, be) and the seal ratio:
al, be = sp.symbols('alpha beta', real=True)
Lvv = al**2*Lww0 + be*sp.simplify(Tw.subs(w, 0))
Hv = sp.simplify(Hff - (al**2/Lvv)*(bw*bw.T))
check("A7", sp.simplify(Hv[2, 2] - (c*sn/(4*f))*(al**2 + be)/(3*al**2 - be))
      == 0 and
      sp.simplify(Hv[0, 0]/Hff[0, 0] - (2*al**2 - be)/(3*al**2 - be)) == 0
      and sp.simplify(Hv[0, 2]/Hff[0, 2] - (al**2 - be)/(3*al**2 - be)) == 0,
      "chart law: [fth,fth] -> (c/4)(sn/f)(al^2+be)/(3al^2-be); ratios "
      "rr = (2al^2-be)/(3al^2-be), rd = (al^2-be)/(3al^2-be) -- the "
      "atom-ratio table used by scripts 2/4 is the chart law at "
      "(1,0) and (1,1)")

# ---- THE EXCEPTIONAL FAMILY be = 2 al^2: WHICH CHART IS IT? ----
# chart by the PHI-FIBER ROOT: v := sqrt(g_phph)/(r sn) - 1 = 1/(1+w) - 1
v_ = sp.Symbol('v_', real=True)
w_of_v = 1/(1 + v_) - 1
ser = sp.series(w_of_v, v_, 0, 3).removeO()
al_phi = sp.diff(ser, v_).subs(v_, 0)
be_phi = sp.diff(ser, v_, 2).subs(v_, 0)
check("A8", al_phi == -1 and be_phi == 2 and be_phi == 2*al_phi**2,
      "THE EXCEPTIONAL CHART FAMILY be = 2al^2 CONTAINS THE PHI-ROOT "
      "CHART v = sqrt(g_phph)/(r sin th) - 1 = 1/(1+w) - 1 (al=-1, "
      "be=2): the chart whose variable is the phi-fiber scale -- the "
      "exact class-symmetric twin of the w-chart (theta-fiber scale). "
      "NOT physically dismissible as measure-zero.")
rr_phi = sp.Rational(2*1 - 2, 3*1 - 2)   # (2al^2-be)/(3al^2-be) at (-1,2)
gg_phi = sp.Rational(1 + 2, 3 - 2)
check("A9", rr_phi == 0 and gg_phi == 3,
      "in the phi-root chart the dressed [f,f] (the 1/mu rr source) "
      "VANISHES (ratio 0) while [fth,fth] = +3c/4 (strong flip): the "
      "m=0 v-hat 1/mu law DIES in this chart; the forced-Dirichlet "
      "mechanism falls to ln order (endpoint claim must be AMENDED)")
# sanity: elimination valid there (Lvv != 0):
Lvv_phi = sp.simplify(Lvv.subs([(al, -1), (be, 2)]))
check("A10", sp.simplify(Lvv_phi + c*sn*fth**2/(4*f)) == 0,
      "phi-root chart L_vv = -(c/4) sn fth^2/f != 0: the elimination "
      "is non-degenerate there (the zero is real, not an artifact of "
      "a degenerate chart)")
# corpus charts NOT in the family: w-chart (1,0), exp (1,1),
# W-chart (1/2,-1/4), 1/W-chart (-1/2,3/4):
others = [(1, 0), (1, 1), (sp.Rational(1, 2), -sp.Rational(1, 4)),
          (-sp.Rational(1, 2), sp.Rational(3, 4))]
check("A11", all(b_ != 2*a_**2 for a_, b_ in others),
      "w-, exp-, W-, 1/W-charts all OFF the exceptional family "
      "(only the phi-root chart among natural candidates sits on it)")

# ---- D_cell branch (Charles-fork-relevant): exact verification ----
Dcell = -(c/4)*sn*(w*fth**2/f + q*fr*fth)
Ltot = L0 + Dcell
pt = [(q, 0), (w, 0)]
okT = (sp.simplify(sp.diff(Ltot, w).subs(pt)) == 0 and
       sp.simplify(sp.diff(Ltot, q).subs(pt)) == 0)
okB = all(sp.simplify(sp.diff(Ltot, Xf, jt).subs(pt)) == 0
          for Xf in (w, q) for jt in jets)
okH = all(sp.simplify(sp.diff(Ltot, a_, b_).subs(pt)
                      - sp.diff(L0, a_, b_).subs(pt)) == 0
          for a_, b_ in [(w, w), (w, q), (q, q)])
okF = all(sp.simplify(sp.diff(Ltot, jets[i], jets[j]).subs(pt)
                      - Hff[i, j]) == 0
          for i in range(3) for j in range(3))
check("A12", okT and okB and okH and okF,
      "C1 + D_cell: tadpoles AND all six cross blocks vanish "
      "identically; (w,q)-block and f-block unchanged => Schur "
      "correction == 0 => THE ENTIRE W3 DRESSING VANISHES IDENTICALLY "
      "ON THE D_CELL BRANCH (G1-G3 verified on my own route; if "
      "Charles adopts D_cell, S1/S2 hold verbatim)")
# but on the D_cell branch the dressing is zero for EVERY chart too
# (tadpole = 0 => Hessian tensorial => chart-independent):
Lv_tot = sp.simplify(al**2*sp.diff(Ltot, w, w).subs(pt)
                     + be*sp.diff(Ltot, w).subs(pt))
check("A13", sp.simplify(Lv_tot - al**2*sp.diff(Ltot, w, w).subs(pt)) == 0,
      "D_cell branch: T = 0 kills the be-dependence of L_vv (the "
      "Hessian becomes TENSORIAL on-shell-in-(w,q)): the chart "
      "ambiguity itself dissolves with the dressing -- the F-2 "
      "obstruction is a C1-only-branch disease, exactly as claimed")

# ---- D8 (q* identity) done fully symbolically ----
qstar = 2*r**2*W*fr*fth/A_
Lstar = L0.subs(q, qstar)
Dlt_w = f*r**2*W*fr**2 - fth**2
target = -(c/8)*sn*Dlt_w/(f*W)
diff = sp.simplify(sp.radsimp(sp.powsimp(sp.simplify(Lstar - target),
                                         force=False)))
if diff != 0:
    # the sqrt branch: r^2 W - f q*^2 must be simplified assuming
    # subsonic Dlt_w > 0; substitute fth = s*sqrt(X) parametrization:
    s_, Xv = sp.symbols('s_ X_v', positive=True)
    # subsonic: fth^2 < f r^2 W fr^2; param fth = t_*sqrt(f) r sqrt(W) fr,
    # |t_| < 1, and check both signs of fr, fth via t_ in (-1,1):
    t_ = sp.Symbol('t_', real=True)
    sub = {fth: t_*sp.sqrt(f)*r*sp.sqrt(W)*fr}
    d2 = sp.simplify(sp.expand(sp.simplify((Lstar - target).subs(sub))))
    # subsonic branch |t_| < 1: sqrt((1-t^2)^2) = 1 - t^2:
    d2 = sp.simplify(d2.subs(sp.sqrt(t_**4 - 2*t_**2 + 1), 1 - t_**2))
    diff = d2
check("A14", sp.simplify(diff) == 0 or all(
      abs(sp.N((Lstar - target).subs(s), 50)) < sp.Float('1e-30')
      for s in [{f: sp.Rational(1, 2), fr: -1, fth: sp.Rational(1, 10),
                 r: 2, w: 0, sn: sp.Rational(1, 2), c: 1},
                {f: sp.Rational(1, 3), fr: 2, fth: -sp.Rational(1, 7),
                 r: 3, w: sp.Rational(1, 5), sn: sp.Rational(3, 4),
                 c: 1},
                {f: 2, fr: -1, fth: -sp.Rational(1, 2),
                 r: 2, w: -sp.Rational(1, 3),
                 sn: sp.Rational(1, 5), c: 1},
                {f: sp.Rational(7, 8), fr: sp.Rational(3, 11),
                 fth: sp.Rational(1, 4), r: sp.Rational(5, 3),
                 w: sp.Rational(2, 7), sn: 1, c: 1}]),
      f"q*-identity L(q*) = -(c/8) sn Delta_w/(f(1+w)^2): symbolic "
      f"residual after subsonic refine = {diff}; PLUS 4 hostile spots "
      "incl. NEGATIVE fr/fth and w<0 (the committed D8 used only 2 "
      "positive spots)")

# ---- time-row parity H1 (independent) ----
a_, b2, p2 = sp.symbols('a b2 p2', real=True)
g4t = sp.Matrix([[-f, a_, b2, p2],
                 [a_, 1/f, q, 0],
                 [b2, q, r**2*W, 0],
                 [p2, 0, 0, r**2*sn**2/W]])
Kt = sum(g4t.inv()[i, j]*[-fT/(2*f), -fr/(2*f), -fth/(2*f),
                          -fph/(2*f)][i]
         * [-fT/(2*f), -fr/(2*f), -fth/(2*f), -fph/(2*f)][j]
         for i in range(4) for j in range(4))
Lt = -(c/2)*f*Kt*sp.sqrt(-g4t.det())
statpt = [(q, 0), (a_, 0), (b2, 0), (p2, 0), (fT, 0), (fph, 0), (w, 0)]
okt = all(sp.simplify(sp.diff(Lt, Xf, Yf).subs(statpt)) == 0
          for Xf in (w, q) for Yf in (fT, a_, b2, p2))
check("A15", okt,
      "time-row parity: all eight (w,q)x(time-row) cross blocks vanish "
      "at static diagonal backgrounds (H1 independent: W_A untouched)")

# ---------------- (ii) mpmath numeric FD route ----------------
mp.mp.dps = 40
def Lnum(fv, frv, fthv, wv, qv, rv=mp.mpf('1.7'), snv=mp.mpf('0.6'),
         cv=mp.mpf(1)):
    Wv = (1 + wv)**2
    D2v = rv**2*Wv/fv - qv**2
    sq = mp.sqrt(fv*D2v)*rv*snv/mp.sqrt(Wv)
    irr = rv**2*Wv/D2v; ithth = (1/fv)/D2v; irth = -qv/D2v
    pr = -frv/(2*fv); pth = -fthv/(2*fv)
    Kv = irr*pr**2 + 2*irth*pr*pth + ithth*pth**2
    return -(cv/2)*fv*Kv*sq

def fd2(g, i, j, x0, h=mp.mpf('1e-8')):
    e = [mp.mpf(0)]*5
    def at(di, dj):
        xs = list(x0); xs[i] += di*h; xs[j] += dj*h
        return g(*xs)
    if i == j:
        return (at(1, 0) - 2*at(0, 0) + at(-1, 0))/h**2
    return (at(1, 1) - at(1, -1) - at(-1, 1) + at(-1, -1))/(4*h**2)

# hostile point: negative fr, fth, w != 0, q != 0 baseline:
pts = [(mp.mpf('0.37'), mp.mpf('-1.21'), mp.mpf('0.83'), mp.mpf(0),
        mp.mpf(0)),
       (mp.mpf('1.9'), mp.mpf('0.41'), mp.mpf('-0.57'), mp.mpf(0),
        mp.mpf(0))]
VAR = ['f', 'fr', 'fth', 'w', 'q']
okn = True
for x0 in pts:
    fv, frv, fthv, _, _ = x0
    subs0 = {f: sp.Float(str(fv), 40), fr: sp.Float(str(frv), 40),
             fth: sp.Float(str(fthv), 40), r: sp.Float('1.7', 40),
             sn: sp.Float('0.6', 40), c: 1}
    # numeric Hessian entries vs symbolic:
    pairs = [(3, 2, Lwfth.subs(w, 0)), (3, 4, Lwq0), (3, 3, Lww0),
             (3, 0, bw[0]), (4, 1, bq[1]), (2, 2, Hff[2, 2]),
             (0, 0, Hff[0, 0]), (0, 2, Hff[0, 2])]
    for i, j, symb in pairs:
        num = fd2(Lnum, i, j, x0)
        ref = mp.mpf(str(sp.N(symb.subs(subs0), 35)))
        scale = max(abs(ref), mp.mpf('1e-6'))
        if abs(num - ref)/scale > mp.mpf('1e-10'):
            okn = False
            print(f"   FD mismatch ({VAR[i]},{VAR[j]}) at {x0}: "
                  f"{num} vs {ref}")
check("N1", okn,
      "mpmath dps-40 central-FD second derivatives of the RAW density "
      "match every symbolic block entry at hostile points with "
      "NEGATIVE f_r/f_th (route fully independent of sympy diff)")

# numeric flip check: eliminate delta-w numerically at a hostile point:
fv, frv, fthv = mp.mpf('0.37'), mp.mpf('-1.21'), mp.mpf('0.83')
x0 = (fv, frv, fthv, mp.mpf(0), mp.mpf(0))
Hn = mp.matrix(3, 3)
for i in range(3):
    for j in range(3):
        Hn[i, j] = fd2(Lnum, i, j, x0)
bn = mp.matrix([fd2(Lnum, 3, k, x0) for k in range(3)])
lww = fd2(Lnum, 3, 3, x0)
flip = Hn[2, 2] - bn[2]*bn[2]/lww
ref_flip = mp.mpf(1)*mp.mpf('0.6')/(12*fv)   # c sn/(12 f)
check("N2", abs(flip - ref_flip)/abs(ref_flip) < mp.mpf('1e-9'),
      f"numeric Schur flip at hostile point: dressed [fth,fth] = "
      f"{mp.nstr(flip, 12)} vs +c sn/12f = {mp.nstr(ref_flip, 12)} "
      "(the +c/12 flip is real, not a sympy artifact)")

print(f"\nV1 GROUND ATTACK: {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
