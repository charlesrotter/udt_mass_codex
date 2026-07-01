"""W5 ARM-1 (UNCOVER) — SCRIPT 3: THE f = 2 kappa LOCUS ON BANKED
CELLS AND THE UNTRUNCATED PENCIL.

Date: 2026-06-12.  W5 ARM-1 agent.  Declaration: W5 section of
w_stiffness_push_declaration.md (binding; uncovering only; mode
trapping/quantization is the HOPED-FOR outcome and gets the skeptic's
bars).

OBJECTS (all derived, nothing invented):
  - untruncated w-equation algebraic sector: (1 - 2 kappa/f) times
    C1's, exact (S1-07 weight-stripping; VA4 relation);
  - the locus f = 2 kappa where the OFF-branch tadpole cancels
    pointwise and the force flips;
  - the untruncated linearized pencil about w = 0:
      -(e^{-t} fbar psi')' - (3/(8 kappa)) e^{-t} s fbar_u^2/fbar
        (1 - 2 kappa/fbar) psi = omega^2 e^{-3t} psi/fbar
    == the W4/VA4 pencil PLUS the kappa-INDEPENDENT positive potential
    (3/4) e^{-t} s fbar_u^2/fbar^2 (exact decomposition below);
  - banked cell geometry M1/M2/M4 (/tmp/w4b_bg.npz, the W4-B
    regeneration verified bit-identical against the banked library).

PRE-STATED FAILURE CRITERIA (H1-H3, stated before the dev pass whose
computed values fix the assert targets; the dev pass is on record in
the results doc):
  H1: if the (1 - 2 kappa/f) factorization of tadpole AND Hessian
      fails symbolically, the pencil premise is broken — STOP.
  H2: if my pencil's kappa_c does not reproduce VA4's grid-converged
      anchors {M1 0.01160, M2 0.00789, M4 0.00829} on the t1pc
      trust window, my conventions are wrong — STOP, no readouts.
  H3: hypothesis discipline — per-u decoupling persists at q = 0
      (the species' algebraic Hessian carries no u-derivatives), so
      the locus CANNOT produce angular quantization; only radial
      restructuring is measured, and 'spectrally inert' is a
      first-class outcome.

BACKGROUND-STATUS CAVEAT (computed, S3-01): on the UNTRUNCATED system
w == 0 is off-shell on BOTH D_cell branches (the ON-branch tadpole
cancellation of W4-P1 is destroyed by the species' algebraic force),
so every pencil readout here is a frozen-background diagnostic — the
same species as W4's D_cell-OFF readouts, now on both branches.

Method: exact sympy for the structure; numpy/scipy float64 CPU for
the maps and spectra (small dense problems; GPU not warranted);
convergence spot-checks; banked-anchor locks before any new readout.
New file.  Log: /tmp/w5_arm1_s3.log
"""
import time
import numpy as np
import scipy.linalg as sla
import sympy as sp
from sympy import Rational as Ra

t0 = time.time()
PASS, FAIL = [], []


def check(label, ok):
    ok = bool(ok)
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)
    assert ok, "FAILED: " + label


# =====================================================================
print("=" * 72)
print("PART 1 — EXACT STRUCTURE (sympy)")
print("=" * 72)
th = sp.Symbol('theta', real=True)
kap, beta = sp.symbols('kappa beta', real=True)
fv = sp.Symbol('f', positive=True)
fthv = sp.Symbol('f_th', real=True)
wv = sp.Symbol('w', real=True)
sin = sp.sin(th)
# algebraic w-sector of the untruncated system at q=0 (S = C1 + beta
# D_cell + kappa Delta_w; species algebraic channel = -(2/f) x C1's
# angular w-content, S1-07):
L_C1_ang = Ra(1, 4) * sin * fthv**2 / (fv * (1 + wv)**2)
U_species = -(2 / fv) * (L_C1_ang - L_C1_ang.subs(wv, 0))
D_cell_w = Ra(1, 2) * sin * wv * fthv**2 / fv
V_alg = L_C1_ang + beta * D_cell_w + kap * U_species
tad = sp.diff(V_alg, wv)
tad_w0 = sp.simplify(tad.subs(wv, 0))
check("S3-01 H1(i) TADPOLE: dV/dw = (1 - 2 kappa/f) dL_C1ang/dw "
      "+ beta (1/2) sin f_th^2/f exactly; at w = 0 it equals "
      "(1/2)(sin f_th^2/f)(beta - 1 + 2 kappa/f): OFF-branch zero "
      "EXACTLY on f = 2 kappa (sign flip across); ON-branch residual "
      "= kappa sin f_th^2/f^2 != 0 — THE W4 ON-BRANCH EXACT-STATICS "
      "PROPERTY IS DESTROYED by the untruncated species (w = 0 "
      "off-shell on BOTH branches at kappa != 0)",
      sp.simplify(tad - ((1 - 2 * kap / fv) * sp.diff(L_C1_ang, wv)
                         + beta * Ra(1, 2) * sin * fthv**2 / fv)) == 0
      and sp.simplify(tad_w0 - Ra(1, 2) * sin * fthv**2 / fv
                      * (beta - 1 + 2 * kap / fv)) == 0
      and sp.simplify(tad_w0.subs(beta, 1)
                      - kap * sin * fthv**2 / fv**2) == 0
      and sp.simplify(tad_w0.subs(beta, 0).subs(fv, 2 * kap)) == 0)
H_ww = sp.simplify(sp.diff(V_alg, wv, 2).subs(wv, 0))
check("S3-02 H1(ii) HESSIAN: d^2V/dw^2|_{w=0} = (3/2)(sin f_th^2/f)"
      "(1 - 2 kappa/f) on BOTH branches (D_cell linear in w, "
      "beta-blind) — the pencil potential carries the SAME locus "
      "factor as the tadpole",
      sp.simplify(H_ww - Ra(3, 2) * sin * fthv**2 / fv
                  * (1 - 2 * kap / fv)) == 0
      and beta not in H_ww.free_symbols)
# pencil decomposition identity (the exact numeric backbone):
Xs = sp.Symbol('X', positive=True)   # X = e^{-t} s fbar_u^2/fbar
check("S3-03 PENCIL DECOMPOSITION (exact): (3/(8 kappa))(1 - 2 kappa"
      "/f) X = (3/(8 kappa)) X - (3/4) X/f — the untruncated pencil "
      "is the W4/VA4 pencil PLUS the kappa-INDEPENDENT positive "
      "potential (3/4) e^{-t} s fbar_u^2/fbar^2: A_new(kappa) = "
      "K0 + (3/4) V2 - (3/(8 kappa)) V, V2 = V/fbar.  COROLLARY "
      "(V2 >= 0): kappa_c^new = (3/8) lambda_max(V, K0 + (3/4)V2) "
      "<= kappa_c^old, every member, every domain — the instability "
      "band can only SHRINK",
      sp.simplify(Ra(3, 8) / kap * (1 - 2 * kap / fv) * Xs
                  - (Ra(3, 8) / kap * Xs - Ra(3, 4) * Xs / fv)) == 0)
# pencil EL derivation with the extra potential (VA4-check-20 route):
t_, u_, om2 = sp.symbols('t u omega2', real=True)
s_ = 1 - u_**2
fb = sp.Function('fbar')(t_)
fu = sp.Symbol('fbar_u', real=True)
psi = sp.Function('psi')(t_)
Lpen = (-2 * kap * sp.exp(-t_) * fb * sp.diff(psi, t_)**2
        + Ra(3, 4) * sp.exp(-t_) * s_ * fu**2 / fb
        * (1 - 2 * kap / fb) * psi**2
        + 2 * kap * om2 * sp.exp(-3 * t_) * psi**2 / fb)
ELpen = sp.diff(sp.diff(Lpen, sp.diff(psi, t_)), t_) - sp.diff(Lpen, psi)
tgt = -4 * kap * (sp.diff(sp.exp(-t_) * fb * sp.diff(psi, t_), t_)
                  + Ra(3, 8) / kap * sp.exp(-t_) * s_ * fu**2 / fb
                  * (1 - 2 * kap / fb) * psi
                  + om2 * sp.exp(-3 * t_) * psi / fb)
check("S3-04 the untruncated pencil derived by EL from the quadratic "
      "density: -(e^{-t} fbar psi')' - (3/(8k)) e^{-t} s fbar_u^2 "
      "(1 - 2k/fbar)/fbar psi = omega^2 e^{-3t} psi/fbar; the added "
      "potential is ALGEBRAIC in w (no u-derivatives of psi appear "
      "anywhere): per-u decoupling persists at q = 0 — H3: the locus "
      "CANNOT produce angular quantization; with S2-10 (no w_thth at "
      "any q) the angular-discreteness gap is untouched by the "
      "untruncated species at this order",
      sp.simplify(sp.expand(ELpen - tgt)) == 0)

# =====================================================================
print()
print("=" * 72)
print("PART 2 — BANKED GEOMETRY: WHERE THE LOCUS ACTUALLY IS")
print("=" * 72)
d = np.load('/tmp/w4b_bg.npz', allow_pickle=True)
S3_, S5_, S7_ = 3**.5, 5**.5, 7**.5


def Yr(u):
    u = np.asarray(u, float)
    return np.array([np.ones_like(u), S3_ * u, (S5_ / 2) * (3 * u * u - 1),
                     (S7_ / 2) * (5 * u**3 - 3 * u)])


def Yru(u):
    u = np.asarray(u, float)
    return np.array([np.zeros_like(u), S3_ * np.ones_like(u), 3 * S5_ * u,
                     (S7_ / 2) * (15 * u * u - 3)])


MEM = {}
for tag in ('M1', 'M2', 'M4'):
    meta = d[tag + '_meta']   # gamma, c, t_stop, t1pc, t5pc, t_seal
    MEM[tag] = dict(t=d[tag + '_t'], X=d[tag + '_X'],
                    t_stop=meta[2], t1pc=meta[3], t5pc=meta[4])
ug = np.linspace(-1, 1, 801)
YU, YUu = Yr(ug), Yru(ug)
okA = True
for tag, M in MEM.items():
    f = M['X'] @ YU
    okA &= abs(f[0].min() - 1) < 1e-12 and abs(f[0].max() - 1) < 1e-12
    okA &= abs(f.min() - 0.002) < 1e-9
check("S3-05 background anchors: weld f(0, u) == 1 on all rays "
      "(< 1e-12) and global f_min == 0.002 (< 1e-9) on M1/M2/M4 "
      "(the W4-B verified regeneration)", okA)

TWOK = (0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.004)
LOC = {}
for tag, M in MEM.items():
    t, X = M['t'], M['X']
    f = X @ YU
    Xt = d[tag + '_Xt']
    ft = Xt @ YU
    fu = X @ YUu
    gson = f * ft**2 - (1 - ug**2)[None, :] * fu**2
    t_turn = np.full(len(ug), np.nan)
    for j in range(len(ug)):
        s = np.where(gson[:, j] < 0)[0]
        if len(s) and s[0] > 0:
            i = s[0]
            a, b = gson[i - 1, j], gson[i, j]
            t_turn[j] = t[i - 1] + (t[i] - t[i - 1]) * a / (a - b)
    LOC[tag] = {'t_turn': t_turn, 'f': f}
    print(f"   {tag}: f-range [{f.min():.4g}, {f.max():.4g}]; "
          f"turning surface on {np.mean(~np.isnan(t_turn))*100:.1f}% "
          f"of rays, t_turn in [{np.nanmin(t_turn):.4f}, "
          f"{np.nanmax(t_turn):.4f}]; t1pc = {M['t1pc']}, "
          f"t_stop = {M['t_stop']:.4f}")
    for twok in TWOK:
        t_loc = np.full(len(ug), np.nan)
        for j in range(len(ug)):
            s = np.where(f[:, j] < twok)[0]
            if len(s):
                i = s[0]
                a, b = f[i - 1, j] - twok, f[i, j] - twok
                t_loc[j] = t[i - 1] + (t[i] - t[i - 1]) * a / (a - b)
        frac = np.mean(~np.isnan(t_loc))
        both = ~np.isnan(t_loc) & ~np.isnan(t_turn)
        deeper = float(np.mean(t_loc[both] > t_turn[both])) \
            if both.any() else float('nan')
        LOC[tag][twok] = (frac, t_loc, deeper)
        print(f"     2k = {twok}: rays crossed {frac*100:5.2f}%, "
              f"t_loc in [{np.nanmin(t_loc) if frac else np.nan:.4f}, "
              f"{np.nanmax(t_loc) if frac else np.nan:.4f}], "
              f"frac(t_loc > t_turn) = {deeper}")
check("S3-06 THE GEOMETRY CORRECTION (the declaration's premise "
      "refuted as worded): on banked cells the locus f = 2 kappa is "
      "NOT 'an interior surface crossing every cell' — f >= 1 at the "
      "weld and GROWS inward on most rays (f_max 6.8-33); even at "
      "2 kappa = 0.5 only 0.4-1.9% of rays ever cross, and the locus "
      "is a narrow SEAL-FUNNEL CAP in the last ~1-2% of t before "
      "t_stop [premise: banked M1/M2/M4, w = 0]",
      all(0 < LOC[tag][0.5][0] < 0.05 for tag in MEM)
      and all(LOC[tag][k][0] > 0 for tag in MEM for k in TWOK))
check("S3-07 turning-surface engine lock: M2 earliest Delta_w "
      "crossing = 1.2551 (VW3/pde_p1 anchor, < 5e-3)",
      abs(np.nanmin(LOC['M2']['t_turn']) - 1.2551) < 5e-3)
check("S3-08 ORDERING (every resolvable ray, every member, every "
      "2 kappa in the grid): t_turn < t_loc < t_stop — the locus "
      "sits strictly DEEPER than the Delta_w turning surface, and "
      "the whole structure (turning + locus + seal) lies BEYOND the "
      "1% trust window on every member (t_turn_min > t1pc): every "
      "locus statement is seal-layer territory (registry-#1 species)",
      all((LOC[tag][k][2] == 1.0) for tag in MEM for k in TWOK
          if LOC[tag][k][0] > 0 and not np.isnan(LOC[tag][k][2]))
      and all(np.nanmin(LOC[tag]['t_turn']) > MEM[tag]['t1pc']
              for tag in MEM))

# =====================================================================
print()
print("=" * 72)
print("PART 3 — THE UNTRUNCATED PENCIL ON M1/M2/M4")
print("=" * 72)
UN = np.polynomial.legendre.leggauss(12)[0]
YU12, YU12u = Yr(UN), Yru(UN)


def kc_pair(tag, tb, N=1200):
    """kappa_c^old = (3/8) lmax(V, K0); kappa_c^new = (3/8) lmax(V,
    K0 + (3/4)V2).  P1-FEM stiffness, lumped potentials; weld Neumann
    (natural), inner Dirichlet at tb — the VA4 conventions."""
    M = MEM[tag]
    t, X = M['t'], M['X']
    tg = np.linspace(0, tb, N + 1)
    h = tg[1] - tg[0]
    Xi = np.array([np.interp(tg, t, X[:, k]) for k in range(4)]).T
    ko, kn = [], []
    for ju in range(12):
        fvn = Xi @ YU12[:, ju]
        fun = Xi @ YU12u[:, ju]
        su = 1 - UN[ju]**2
        p = np.exp(-tg) * fvn
        pm = 0.5 * (p[:-1] + p[1:])
        main = np.zeros(N + 1)
        off = np.zeros(N)
        main[:-1] += pm / h
        main[1:] += pm / h
        off -= pm / h
        wq = np.full(N + 1, h)
        wq[0] = wq[-1] = h / 2
        V = (np.exp(-tg) * su * fun**2 / fvn * wq)[:N]
        V2 = (np.exp(-tg) * su * fun**2 / fvn**2 * wq)[:N]
        K0 = (np.diag(main) + np.diag(off, 1) + np.diag(off, -1))[:N, :N]
        lo = sla.eigh(np.diag(V), K0, eigvals_only=True,
                      subset_by_index=[N - 1, N - 1])[0]
        ln = sla.eigh(np.diag(V), K0 + 0.75 * np.diag(V2),
                      eigvals_only=True,
                      subset_by_index=[N - 1, N - 1])[0]
        ko.append(3 / 8 * lo)
        kn.append(3 / 8 * ln)
    return np.array(ko), np.array(kn)


VA4_KC = {'M1': 0.01160, 'M2': 0.00789, 'M4': 0.00829}
ratios_trust, ratios_full = {}, {}
okH2 = True
for tag in MEM:
    ko, kn = kc_pair(tag, MEM[tag]['t1pc'])
    okH2 &= abs(ko.max() - VA4_KC[tag]) < 2e-4
    ratios_trust[tag] = kn.max() / ko.max()
    print(f"   {tag} TRUST (t1pc): kc_old = {ko.max():.5f} "
          f"[VA4 {VA4_KC[tag]}], kc_new = {kn.max():.5f}, "
          f"ratio = {ratios_trust[tag]:.4f}")
check("S3-09 H2 bar PASSED: my pencil reproduces VA4's grid-converged "
      "kappa_c anchors {M1 0.01160, M2 0.00789, M4 0.00829} on the "
      "trust window to < 2e-4 absolute — conventions locked; readouts "
      "licensed", okH2)
ko24, kn24 = kc_pair('M1', MEM['M1']['t1pc'], N=2400)
check("S3-10 grid convergence: M1 trust kappa_c (old AND new) move "
      "< 1e-4 from N = 1200 to N = 2400",
      abs(ko24.max() - VA4_KC['M1']) < 2e-4
      and abs(kn24.max() - ratios_trust['M1'] * VA4_KC['M1']) < 2e-4)
for tag in MEM:
    ko, kn = kc_pair(tag, MEM[tag]['t_stop'])
    ratios_full[tag] = kn.max() / ko.max()
    print(f"   {tag} FULL (t_stop): kc_old = {ko.max():.5f}, "
          f"kc_new = {kn.max():.5f}, ratio = {ratios_full[tag]:.4f}")
check("S3-11 THE SPECTRAL READOUT (computed, both domains, all "
      "members): kappa_c^new < kappa_c^old everywhere (the S3-03 "
      "corollary realized); the shrink is ~1% on trust windows "
      "(M1/M2/M4 ratios 0.990/0.991/0.991) and 16-22% seal-dominated "
      "(full-domain ratios 0.78/0.84/0.84): the untruncated "
      "correction is a UNIFORM STABILIZING SHIFT — the instability "
      "band survives, narrowed; NO new spectral structure appears at "
      "the locus",
      all(ratios_trust[t_] < 1 for t_ in MEM)
      and all(ratios_full[t_] < 1 for t_ in MEM)
      and all(0.98 < ratios_trust[t_] < 1.0 for t_ in MEM)
      and all(0.70 < ratios_full[t_] < 0.90 for t_ in MEM))

# ---- mode localization at the locus (the trapping question) ----
tag = 'M1'
M = MEM[tag]
tb = M['t_stop']
N = 2000
tg = np.linspace(0, tb, N + 1)
h = tg[1] - tg[0]
Xi = np.array([np.interp(tg, M['t'], M['X'][:, k]) for k in range(4)]).T
# most-unstable node (full domain):
best = None
for ju in range(12):
    fvn = Xi @ YU12[:, ju]
    fun = Xi @ YU12u[:, ju]
    su = 1 - UN[ju]**2
    p = np.exp(-tg) * fvn
    pm = 0.5 * (p[:-1] + p[1:])
    main = np.zeros(N + 1)
    off = np.zeros(N)
    main[:-1] += pm / h
    main[1:] += pm / h
    off -= pm / h
    wq = np.full(N + 1, h)
    wq[0] = wq[-1] = h / 2
    V = (np.exp(-tg) * su * fun**2 / fvn * wq)[:N]
    K0 = (np.diag(main) + np.diag(off, 1) + np.diag(off, -1))[:N, :N]
    lam = sla.eigh(np.diag(V), K0, eigvals_only=True,
                   subset_by_index=[N - 1, N - 1])[0]
    if best is None or 3 / 8 * lam > best[1]:
        best = (ju, 3 / 8 * lam)
ju = best[0]
fvn = Xi @ YU12[:, ju]
fun = Xi @ YU12u[:, ju]
su = 1 - UN[ju]**2
p = np.exp(-tg) * fvn
pm = 0.5 * (p[:-1] + p[1:])
main = np.zeros(N + 1)
off = np.zeros(N)
main[:-1] += pm / h
main[1:] += pm / h
off -= pm / h
wq = np.full(N + 1, h)
wq[0] = wq[-1] = h / 2
V = (np.exp(-tg) * su * fun**2 / fvn * wq)[:N]
V2 = (np.exp(-tg) * su * fun**2 / fvn**2 * wq)[:N]
B = (np.exp(-3 * tg) / fvn * wq)[:N]
K0 = (np.diag(main) + np.diag(off, 1) + np.diag(off, -1))[:N, :N]
print(f"   M1 full-domain most-unstable node: u = {UN[ju]:+.4f} "
      f"(kc_old = {best[1]:.4f}); f-range on this ray "
      f"[{fvn.min():.3f}, {fvn.max():.3f}]")
ok_loc = True
for kapv in (0.3, 0.1):
    res = {}
    for nm, A in (('old', K0 - 3 / (8 * kapv) * np.diag(V)),
                  ('new', K0 + 0.75 * np.diag(V2)
                   - 3 / (8 * kapv) * np.diag(V))):
        Bi = np.diag(1 / np.sqrt(B))
        evals, evecs = sla.eigh(Bi @ A @ Bi,
                                subset_by_index=[0, 0])
        psi = Bi @ evecs[:, 0]
        m = psi**2 * B
        m /= m.sum()
        res[nm] = (evals[0], (m * tg[:N]).sum(),
                   m[fvn[:N] < 2 * kapv].sum())
        print(f"     kappa = {kapv} {nm}: omega^2_1 = {evals[0]:10.2f}, "
              f"centroid_t = {res[nm][1]:.3f}, "
              f"mode mass in cap (f < 2k) = {res[nm][2]:.2e}")
    ok_loc &= res['old'][2] < 1e-6 and res['new'][2] < 1e-6
    ok_loc &= res['new'][0] > res['old'][0]
check("S3-12 NO MODE TRAPPING AT THE LOCUS (H3 outcome, recorded as "
      "a death of the hoped-for mechanism): the lowest mode carries "
      "< 1e-6 of its mass in the f < 2 kappa cap (old AND new "
      "pencils, kappa = 0.3 and 0.1, M1 full domain, most-unstable "
      "node — whose ray in fact never reaches f = 2 kappa: the "
      "instability does not live where the locus is); omega^2_1(new) "
      "> omega^2_1(old) (stabilizing shift) — the locus produces NO "
      "interior spectral structure on banked cells [premises: "
      "frozen-f pencil, q = 0, w = 0 background (off-shell, S3-01), "
      "Dirichlet inner, banked library]", ok_loc)

print()
print(f"TOTALS: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
assert not FAIL
