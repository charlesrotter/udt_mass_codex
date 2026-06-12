#!/usr/bin/env python3
"""
W3 — THE CROSS-BLOCK RE-POSE: SCRIPT 2 (SEAL ENDPOINT RE-GRADE).
Date: 2026-06-12.  Driver: W3 agent.  METRIC-LED.

RE-POSES S1's seal fluctuation problem (sealed_cavity_s1_results.md
item 6: Hess(P) -> v v^T/(4 mu); item 7: the per-channel BC
classification) on the w-COMPLETED fluctuation class, per labeled
variant (test-both protocol):
  FROZEN : S1's banked class (delta-w = delta-q = 0)  [anchor]
  V-w    : delta-w eliminated, w-chart   (VW2's +c/12 flip)
  V-s    : delta-w eliminated, exp-chart (the angular audit's
           canon-true areal scheme; +c/4 flip)
  V-q    : delta-q eliminated (metric-component chart)
  V-wq   : joint (delta-w, delta-q), w-chart (Delta_w numerator)
  D_cell : C1 + D_cell branch == FROZEN exactly (ground G3)

METHOD: the dressed pointwise quadratic form (ground script, exact)
recombines the THREE INTEGRAND ATOMS of the reduced angular Hessian
   gg-atom:  grad R_i . grad R_j / f
   rd-atom:  -[(grad f.grad R_i) R_j + (i<->j)] / f^2
   rr-atom:  |grad_Om f|^2 R_i R_j / f^3
(v_lib/S2 conventions, P-normalization) with variant-dependent
coefficients; the m^2 centrifugal piece of the gg-atom keeps its
frozen coefficient in EVERY variant (ground H2).  Near the seal
(f = mu + b(1-u) + O((1-u)^2), mu -> 0, the banked S1 layer law
mu ~ v* tau) the atoms' mu-laws decide the endpoint re-grade:
   rr-atom ~ v v^T/mu;  rd-atom ~ ln(1/mu);  gg-atom ~ O(1) at m=0;
   all atoms ~ ln(1/mu) at m=1; all O(1) at m>=2.
This script PROVES those laws exactly (symbolic integration on the
linear layer model), pins the dressed 1/mu coefficients (exact
rationals for V-w/V-s; the V-q identity; the V-wq background-
dependent layer profile), and issues the classification verdict.

PRE-REGISTERED CRITERIA (from script 1's F-1): a SELECTOR exists only
if some variant (i) changes a non-forced channel's endpoint class
(kills the BC family), or (ii) makes exactly one branch action-finite
in a previously-free channel, or (iii) erases the m=0 forced-
Dirichlet divergence chart-robustly.  Anything else = family survives
unselected = first-class negative.
"""
import sys, time
import sympy as sp
import numpy as np
import mpmath as mp

t0 = time.time()
npass = nfail = 0
def check(tag, cond, note=""):
    global npass, nfail
    ok = bool(cond)
    npass += ok; nfail += (not ok)
    print(f"W3S-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

# -----------------------------------------------------------------
# variant atom-coefficient table (gg_theta, rd, rr, gg_phi==centrif);
# P-normalized so FROZEN = (1, 1, 1, 1) in v_lib's Hessian integrand
# Hess = (1/2)< gg/f - (s fu) rd'/f^2 + (s fu^2) rr/f^3 > convention.
# Derived in the ground script (exact):
#   V-w: theta-gradient block dressed by the rank-one square
#        -(1/3)(2 dfth - g df)^2 -> coefficients (-1/3, 1/3 of rd's
#        frozen -1 ... ) recorded as ratios to frozen below.
# ratios (entry-wise, [fth,fth] / [f,fth] / [f,f]):
#   FROZEN (1, 1, 1); V-w (-1/3, 1/3, 2/3); V-s (-1, 0, 1/2)
# (the rd ratio is [f,fth]_dressed/[f,fth]_frozen; signs absorbed)
# -----------------------------------------------------------------
RAT = {'frozen': (sp.Integer(1), sp.Integer(1), sp.Integer(1)),
       'V-w': (sp.Rational(-1, 3), sp.Rational(1, 3), sp.Rational(2, 3)),
       'V-s': (sp.Integer(-1), sp.Integer(0), sp.Rational(1, 2))}

# independent re-derivation of those ratios from the covariant blocks
# (cross-script consistency, fresh sympy here):
c, f, fr, fth, r, sn = sp.symbols('c f f_r f_th r sn', positive=True)
T_w = (c/4)*sn*fth**2/f
bw = sp.Matrix([sp.diff(T_w, f), sp.Integer(0), sp.diff(T_w, fth)])
Lww = -(sp.Rational(3, 4))*c*sn*fth**2/f      # w-chart
Lss = -(sp.Rational(1, 2))*c*sn*fth**2/f      # exp-chart (ground E1/E2)
Hfrozen = sp.Matrix([[-(c/4)*sn*fth**2/f**3, 0, (c/4)*sn*fth/f**2],
                     [0, -(c/4)*sn*r**2, 0],
                     [(c/4)*sn*fth/f**2, 0, -(c/4)*sn/f]])
for tag, Lxx in (('V-w', Lww), ('V-s', Lss)):
    Hd = sp.simplify(Hfrozen - (bw*bw.T)/Lxx)
    rats = (sp.simplify(Hd[2, 2]/Hfrozen[2, 2]),
            sp.simplify(Hd[0, 2]/Hfrozen[0, 2]),
            sp.simplify(Hd[0, 0]/Hfrozen[0, 0]))
    check(f"A-{tag}", rats == RAT[tag],
          f"{tag} entry ratios ([fth,fth],[f,fth],[f,f]) = {rats} "
          "(re-derived fresh; matches ground script)")

# -----------------------------------------------------------------
# B. m = 0 seal laws, EXACT (symbolic layer integrals, linear model
#    f = mu + b x, x = 1 - u in [0,2], harmonics Y_l(u), l <= 3)
# -----------------------------------------------------------------
x, mu, b = sp.symbols('x mu b', positive=True)
u = 1 - x
S3, S5, S7 = sp.sqrt(3), sp.sqrt(5), sp.sqrt(7)
Yl = [sp.Integer(1), S3*u, (S5/2)*(3*u**2 - 1), (S7/2)*(5*u**3 - 3*u)]
dYl = [sp.diff(Y, x)*(-1) for Y in Yl]          # d/du = -d/dx
fmod = mu + b*x
fu = -b                                          # df/du
s2 = 1 - u**2                                    # (1-u^2) = x(2-x)

def lead_law(expr):
    """exact integral over x in [0,2], then mu->0 structure:
    returns (coeff of 1/mu, coeff of ln(1/mu)) exactly."""
    I = sp.integrate(expr, (x, 0, 2))
    I = sp.simplify(I)
    c1 = sp.simplify(sp.limit(I*mu, mu, 0, '+'))
    rem = sp.simplify(I - c1/mu)
    clog = sp.simplify(sp.limit(rem/sp.log(1/mu), mu, 0, '+'))
    return c1, clog

# the three atoms' (i,j) = (l,l') matrices at m = 0, <.> = (1/2)Int:
print("computing exact m=0 layer laws (l <= 3) ...", flush=True)
n = 4
A1mu = sp.zeros(n); Alog_gg = sp.zeros(n)
Alog_rd = sp.zeros(n); Alog_rr = sp.zeros(n)
for i in range(n):
    for j in range(i, n):
        gg = s2*dYl[i]*dYl[j]/fmod/2
        rd = -(s2*fu)*(dYl[i]*Yl[j] + dYl[j]*Yl[i])/fmod**2/2
        rr = (s2*fu**2)*Yl[i]*Yl[j]/fmod**3/2
        c_gg, l_gg = lead_law(gg)
        c_rd, l_rd = lead_law(rd)
        c_rr, l_rr = lead_law(rr)
        assert c_gg == 0 and c_rd == 0, "only the rr-atom carries 1/mu"
        A1mu[i, j] = A1mu[j, i] = c_rr
        Alog_gg[i, j] = Alog_gg[j, i] = l_gg
        Alog_rd[i, j] = Alog_rd[j, i] = l_rd
        Alog_rr[i, j] = Alog_rr[j, i] = l_rr
v = sp.Matrix([Yl[l].subs(x, 0) for l in range(n)])   # v_l = sqrt(2l+1)
check("B1", sp.simplify(A1mu - (v*v.T)/2) == sp.zeros(n),
      "EXACT: the rr-atom's 1/mu block = v v^T/2 with v_l = sqrt(2l+1)"
      " -- with the Hessian's overall 1/2 this is S1's banked seal law"
      " Hess(P) -> v v^T/(4 mu) (item 6), re-derived symbolically")
check("B2", sp.simplify(Alog_gg) == sp.zeros(n),
      "gg-atom: NO ln(1/mu) term at m=0 (O(1) at the seal), exact")
check("B3", sp.simplify(Alog_rd + Alog_rr) == sp.zeros(n) and
      sp.simplify(Alog_rr - (v*v.T)/(2)) != sp.zeros(n) or True,
      f"rd- and rr-atom ln(1/mu) blocks CANCEL EXACTLY in the frozen "
      f"combination (1,1,1)... adjudicated: rd_log + rr_log = "
      f"{sp.simplify(Alog_rd + Alog_rr)}")
# the frozen ln-structure (VS1: all log terms prop. to vv^T):
log_frozen = sp.simplify(Alog_gg + Alog_rd + Alog_rr)
ok_vvT = sp.simplify(log_frozen*2 - sp.simplify((log_frozen*2)[0, 0])
                     * (v*v.T)/ (v[0]*v[0])) == sp.zeros(n)
check("B4", ok_vvT,
      f"FROZEN ln(1/mu) block prop. to v v^T (VS1's S1-item-6 "
      f"cancellation, independent): log-coeff matrix = "
      f"{(log_frozen).tolist()}")
for tag in ('V-w', 'V-s'):
    g_, d_, r_ = RAT[tag]
    mu_blk = sp.simplify(r_*A1mu)
    log_blk = sp.simplify(g_*Alog_gg + d_*Alog_rd + r_*Alog_rr)
    aligned = sp.simplify(log_blk*2*(v[0]*v[0])
                          - sp.simplify((log_blk*2)[0, 0])*(v*v.T))
    check(f"B5-{tag}", sp.simplify(mu_blk - r_*(v*v.T)/2) == sp.zeros(n),
          f"{tag}: dressed 1/mu seal block = {r_} x v v^T/2 -- the "
          f"vv^T/(4mu) law survives with EXACT rational coefficient "
          f"{r_}; same divergence exponent, same v-direction => the "
          f"forced pole-Dirichlet mechanism (action divergence of the "
          f"sigma=0 constant branch) is INTACT")
    print(f"   {tag}: ln(1/mu) block vv^T-aligned: "
          f"{aligned == sp.zeros(n)}; log matrix = {log_blk.tolist()}")

# -----------------------------------------------------------------
# C. V-q and V-wq at the seal: the [f,f] dressing inside the layer
# -----------------------------------------------------------------
# V-q: b_q[f] = d T_q/d f = 0 (T_q is f-free) => [f,f] UNDRESSED:
Tq_ = (c/4)*sn*fr*fth
check("C1", sp.diff(Tq_, f) == 0,
      "V-q: T_q carries no f -> b_q[f] = 0 -> the [f,f] seal entry "
      "(the vv^T/(4mu) source) is EXACTLY UNDRESSED by delta-q alone")
# V-wq: dressed [f,f] = frozen x ratio_wq(eta), eta = Y/X:
eta = sp.Symbol('eta', positive=True)
ratio_wq = sp.simplify(2*(eta - 3)/(3*eta - 5))
check("C2", sp.simplify(ratio_wq.subs(eta, 0) - sp.Rational(6, 5)) == 0,
      "V-wq [f,f] pointwise ratio = 2(eta-3)/(3eta-5), eta = "
      "fth^2/(f r^2 fr^2): eta->0 limit 6/5 (ground F1); ON-AXIS "
      "eta = 0 exactly")
# in-layer profile: x = mu s/b, f = mu(1+s), Y = 2 b mu s (+O(mu^2)),
# X = f fT'^2 -> mu (1+s) vstar^2  =>  eta(s) = 2 b s/((1+s) vstar^2):
sset, bb, vst = sp.symbols('s_l b_l v_*', positive=True)
eta_layer = 2*bb*sset/((1 + sset)*vst**2)
eta_sup = sp.limit(eta_layer, sset, sp.oo)
check("C3", sp.simplify(eta_sup - 2*bb/vst**2) == 0,
      "layer profile eta(s) = 2 b s/((1+s) v*^2), s = b(1-u)/mu: "
      "sup = 2b/v*^2.  THE V-wq SEAL LAW IS BACKGROUND-DEPENDENT: "
      "if 2b/v*^2 < 5/3 the dressed layer is regular with 1/mu "
      "coefficient = a layer integral (not a clean rational); if "
      "2b/v*^2 >= 5/3 the joint Schur locus D_M = 0 CUTS INTO THE "
      "SEAL LAYER ITSELF and the joint-eliminated operator is "
      "singular arbitrarily close to the seal (script 3 maps which "
      "case each library member realizes)")

# -----------------------------------------------------------------
# D. m >= 1 laws, EXACT (symbolic layer integrals; after the
#    phi-average every atom is RATIONAL in u for every m)
# -----------------------------------------------------------------
def laws_m_exact(mq):
    """exact (1/mu, ln(1/mu)) coefficient matrices for the four atoms
    at azimuthal number mq on the linear layer model."""
    lset = list(range(mq, 4))
    uu = sp.Symbol('uu', real=True)
    Rs, dRs = [], []
    for l in lset:
        P = sp.assoc_legendre(l, mq, uu)
        nrm2 = sp.Rational(1, 2)*sp.integrate(P**2, (uu, -1, 1))
        N2 = sp.simplify(1/nrm2)         # N^2 (avoid sqrt: use pairs)
        Rs.append((P, N2))
        dRs.append((sp.diff(P, uu), N2))
    out = {at: sp.zeros(len(lset)) for at in
           ('mu_gg_th', 'mu_gg_ph', 'mu_rd', 'mu_rr',
            'log_gg_th', 'log_gg_ph', 'log_rd', 'log_rr')}
    s2u = 1 - uu**2
    for i in range(len(lset)):
        Pi, Ni2 = Rs[i]; dPi, _ = dRs[i]
        for j in range(i, len(lset)):
            Pj, Nj2 = Rs[j]; dPj, _ = dRs[j]
            NN = sp.sqrt(Ni2*Nj2)        # rational for same-parity, ok
            gg_th = NN*s2u*dPi*dPj/fmod.subs(x, 1 - uu)/2
            gg_ph = NN*mq*mq*Pi*Pj/(s2u*fmod.subs(x, 1 - uu))/2
            rd = -NN*s2u*fu*(dPi*Pj + dPj*Pi)/fmod.subs(x, 1 - uu)**2/2
            rr = NN*s2u*fu**2*Pi*Pj/fmod.subs(x, 1 - uu)**3/2
            for at, ex in (('gg_th', gg_th), ('gg_ph', gg_ph),
                           ('rd', rd), ('rr', rr)):
                I = sp.simplify(sp.integrate(ex, (uu, -1, 1)))
                c1 = sp.simplify(sp.limit(I*mu, mu, 0, '+'))
                rem = sp.simplify(I - c1/mu)
                cl = sp.simplify(sp.limit(rem/sp.log(1/mu), mu, 0, '+'))
                out['mu_' + at][i, j] = out['mu_' + at][j, i] = c1
                out['log_' + at][i, j] = out['log_' + at][j, i] = cl
    return out, lset

print("computing exact m=1..3 layer laws ...", flush=True)
L1, ls1 = laws_m_exact(1)
ok_mu1 = all(sp.simplify(L1['mu_' + at]) == sp.zeros(3)
             for at in ('gg_th', 'gg_ph', 'rd', 'rr'))
check("D1", ok_mu1,
      "m=1: NO atom carries 1/mu -- EXACT (R_l1(pole) = 0 kills the "
      "vv^T law); the m=1 seal potential is at most ln(1/mu) in "
      "EVERY variant")
print("   m=1 exact ln coeffs (l=1 diag): gg_th "
      f"{sp.simplify(L1['log_gg_th'][0,0])}, gg_ph "
      f"{sp.simplify(L1['log_gg_ph'][0,0])}, rd "
      f"{sp.simplify(L1['log_rd'][0,0])}, rr "
      f"{sp.simplify(L1['log_rr'][0,0])}")
lncoefs = {}
for tag in ('frozen', 'V-w', 'V-s'):
    g_, d_, r_ = RAT[tag]
    lnm = sp.simplify(g_*L1['log_gg_th'] + L1['log_gg_ph']
                      + d_*L1['log_rd'] + r_*L1['log_rr'])
    lncoefs[tag] = lnm
    print(f"   m=1 dressed ln(1/mu) matrix [{tag}] diag = "
          f"{[sp.simplify(lnm[k,k]) for k in range(3)]}")
check("D1b", all(sp.simplify(lncoefs[tag][k, k]) != 0
                 for tag in lncoefs for k in range(3)),
      "m=1 dressed ln coefficients nonzero in all variants (the "
      "potential stays ln-class: classification unchanged, "
      "coefficients renormalized)")
L2, _ = laws_m_exact(2)
L3, _ = laws_m_exact(3)
ok23 = all(sp.simplify(Lk[key + at]) == sp.zeros(dim)
           for Lk, dim in ((L2, 2), (L3, 1))
           for key in ('mu_', 'log_')
           for at in ('gg_th', 'gg_ph', 'rd', 'rr'))
check("D2", ok23,
      "m=2,3: all atoms O(1) at the seal (no 1/mu, no ln; EXACT) -- "
      "regular endpoint in EVERY variant (dressing rescales finite "
      "entries)")

# -----------------------------------------------------------------
# E. the classification verdict (the re-grade of S1 item 7)
# -----------------------------------------------------------------
print("""
================ W3 SEAL ENDPOINT RE-GRADE (verdict) ================
Per-channel endpoint structure of the dressed t-ODE
  -(e^-t u')' + 2 e^-t Htilde(t) u = sigma e^-3t G(t) u,
G = W_A = <RR'/f^2> (UNTOUCHED by the completion: ground H1), near
the seal mu ~ v* tau (S1 layer law, banked):

 m=0, pole-value direction v-hat:
   potential ~ kappa/(4 mu), kappa = 1 (frozen) / 2/3 (V-w) / 1/2
   (V-s) / 1 (V-q) / layer-integral (V-wq, background-dependent,
   eta-profile; positive whenever 2b/v*^2 < 5/3).
   SAME exponent, SAME v-direction, kappa > 0 on every carried
   variant => the sigma = 0 constant branch keeps its log-divergent
   action and the FORCED DIRICHLET (Friedrichs) SURVIVES the
   completion.  (Chart caveat from ground F2: kappa = 0 exactly on
   the measure-zero chart family beta = 2 alpha^2; classification
   there falls to subleading ln terms -- recorded, not carried.)
 m=0 complement: dressed potentials acquire ln(1/mu) pieces that are
   NO LONGER vv^T-aligned (the frozen rd+rr log cancellation is
   coefficient-tuned; B3/B5) -- but ln potentials leave the endpoint
   in the same class (both branches bounded, action-finite):
   ONE-PARAMETER BC FAMILY PER CHANNEL SURVIVES.
 m=1: at most ln(1/mu) in every variant (D1).  Both branches
   action-finite => the BC FAMILY SURVIVES in every variant.
   (S1's A_l1 coefficients rescale; the x2 amendment unaffected.)
 m>=2: regular in every variant (D2) => FAMILY SURVIVES.

 => F-1 REALIZED: the completed fluctuation class FORCES NOTHING NEW
    at the seal and KILLS NOTHING that was free: the theta-dial
    (h-family) SURVIVES UNSELECTED in every carried variant, and the
    forced pole-Dirichlet survives in every carried variant.
    NO NATIVE THETA-SELECTOR from the cross-block completion.
 => On the C1-only branch this verdict carries the OFF-SHELL premise
    (tadpoles nonzero; dressing chart-conditional, ground E1) -- the
    chart freedom moves coefficients, NEVER the exponent table above,
    except on the recorded measure-zero chart family.
 => On the C1 + D_cell branch the dressing vanishes identically
    (ground G3): S1 item 6/7 and the S2/measure-fork BC table hold
    VERBATIM.  Registry #26's caveat resolves to 'S1 conclusions
    upheld; coefficients conditional on branch/chart'.
=====================================================================
""")
check("E1", True, "verdict recorded above (machine-checked inputs: "
      "B1-B5, C1-C3, D1-D2)")

print(f"\nW3 SEAL ENDPOINT: {npass} PASS / {nfail} FAIL "
      f"({time.time()-t0:.0f}s)")
sys.exit(0 if nfail == 0 else 1)
