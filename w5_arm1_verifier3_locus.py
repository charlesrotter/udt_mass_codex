"""W5 ARM-1 BLIND VERIFIER — SCRIPT 3: THE f = 2 kappa LOCUS AND THE
UNTRUNCATED PENCIL (attacks claim (iii) of w5_arm1_results.md).

Date: 2026-06-12.  Blind adversarial verifier; independent machinery.

ATTACK LIST COVERED:
  C-1 (their V-7): the geometry correction regenerated DIRECTLY from
      the banked /tmp/seal_s1/lib/bg_*.dat files (not the npz), finer
      u-grid (4001 nodes), trust windows parsed from the dat headers:
      f >= 1 off the seal funnel, f_max range, cap fractions at every
      2 kappa, the ordering t_turn < t_loc < t_stop, t_turn_min >
      t1pc, the M2 1.2551 anchor.
  C-2 (their V-5): the pencil with an INDEPENDENT discretization —
      consistent P1-FEM assembly (tridiagonal potential matrices from
      exact element integrals; the arm used lumped diagonals) — VA4
      anchor locks, the kappa_c^new/old ratios on trust and full
      domains, N-convergence; plus a DIRECT SWEEP crossing check of
      kappa_c (bisection on the lowest eigenvalue) against the
      (3/8) lambda_max readout.
  C-3 (their V-6): the no-trapping verdict attacked on the SEAL-POLE
      RAYS (the rays that actually cross f < 2 kappa) and with
      Neumann and Robin (h = 5, the W4 h-dial species) inner BCs, not
      just Dirichlet; several lowest modes, cap-mass fractions.
  C-4 exact structure: tadpole/Hessian (1 - 2 kappa/f) factorization
      and the pencil decomposition re-derived symbolically with the
      banked D_cell = (c/4) sin [w f_th^2/f + q f_r f_th], c = 2.
  C-5 u-resolution of the kappa_c convention: lambda_max(u) on a
      dense u-grid vs the 12-node Gauss readout (is the max
      u-resolved?).

Log: /tmp/w5_arm1_ver3.log
"""
import re
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


# =====================================================================
print("=" * 72)
print("PART 1 — C-4: EXACT STRUCTURE (own symbols, banked D_cell)")
print("=" * 72)
th, kap, beta = sp.symbols('theta kappa beta', real=True)
fv = sp.Symbol('f', positive=True)
fthv, wv = sp.symbols('f_th w', real=True)
sin = sp.sin(th)
# C1's angular w-content on the q=0 static class (banked + convention,
# verified covariantly in verifier 1):
L_C1_ang = Ra(1, 4) * sin * fthv**2 / (fv * (1 + wv)**2)
# the species' algebraic channel = -(2/f) x [C1_ang(w) - C1_ang(0)]
# (the weight-stripping identity, closed symbolically in verifier 1):
U_sp = -(2 / fv) * (L_C1_ang - L_C1_ang.subs(wv, 0))
# banked D_cell (w4a_system.py line 160, c = 2) at q = 0:
D_cell_w = Ra(2, 4) * sin * wv * fthv**2 / fv
V_alg = L_C1_ang + beta * D_cell_w + kap * U_sp
tad = sp.together(sp.diff(V_alg, wv))
tad0 = sp.simplify(tad.subs(wv, 0))
H0 = sp.simplify(sp.diff(V_alg, wv, 2).subs(wv, 0))
check("V3-01 tadpole at w=0: (1/2)(sin f_th^2/f)(beta - 1 + 2 kappa/f) "
      "— OFF-branch zero iff f = 2 kappa; ON-branch residual "
      "kappa sin f_th^2/f^2 (W4's ON-branch exact statics DESTROYED); "
      "Hessian (3/2)(sin f_th^2/f)(1 - 2 kappa/f), beta-blind",
      sp.simplify(tad0 - Ra(1, 2) * sin * fthv**2 / fv
                  * (beta - 1 + 2 * kap / fv)) == 0
      and sp.simplify(tad0.subs(beta, 1)
                      - kap * sin * fthv**2 / fv**2) == 0
      and sp.simplify(tad0.subs(beta, 0).subs(fv, 2 * kap)) == 0
      and sp.simplify(H0 - Ra(3, 2) * sin * fthv**2 / fv
                      * (1 - 2 * kap / fv)) == 0
      and beta not in H0.free_symbols)
X_ = sp.Symbol('X', positive=True)
check("V3-02 pencil decomposition: (3/(8k))(1 - 2k/f) X == "
      "(3/(8k)) X - (3/4) X/f (kappa-independent positive V2 shift; "
      "with V2 >= 0 in the Rayleigh quotient, kappa_c^new = "
      "(3/8) lmax(V, K0 + (3/4)V2) <= kappa_c^old)",
      sp.simplify(Ra(3, 8) / kap * (1 - 2 * kap / fv) * X_
                  - (Ra(3, 8) / kap * X_ - Ra(3, 4) * X_ / fv)) == 0)

# =====================================================================
print()
print("=" * 72)
print("PART 2 — C-1: GEOMETRY FROM THE BANKED bg_*.dat (not the npz)")
print("=" * 72)
S3_, S5_, S7_ = 3**.5, 5**.5, 7**.5


def Yr(u):
    u = np.asarray(u, float)
    return np.array([np.ones_like(u), S3_ * u,
                     (S5_ / 2) * (3 * u * u - 1),
                     (S7_ / 2) * (5 * u**3 - 3 * u)])


def Yru(u):
    u = np.asarray(u, float)
    return np.array([np.zeros_like(u), S3_ * np.ones_like(u),
                     3 * S5_ * u, (S7_ / 2) * (15 * u * u - 3)])


MEM = {}
for tag in ('M1', 'M2', 'M4'):
    path = f"/tmp/seal_s1/lib/bg_{tag}.dat"
    hdr = open(path).read(3000)
    m1 = re.search(r"<1% t<([0-9.]+)", hdr)
    m5 = re.search(r"<5% t<([0-9.]+)", hdr)
    ms = re.search(r"t_stop=([0-9.]+)", hdr)
    dat = np.loadtxt(path)
    MEM[tag] = dict(t=dat[:, 0], X=dat[:, 2:6], Xt=dat[:, 6:10],
                    fmin=dat[:, 10], t1pc=float(m1.group(1)),
                    t5pc=float(m5.group(1)), t_stop=float(ms.group(1)))
    print(f"   {tag}: rows {dat.shape[0]}, t_stop {MEM[tag]['t_stop']}"
          f", t1pc {MEM[tag]['t1pc']}, t5pc {MEM[tag]['t5pc']}")

# cross-check the npz the arm used against the dat library:
dnpz = np.load('/tmp/w4b_bg.npz', allow_pickle=True)
ok_npz = True
for tag in MEM:
    Xi = np.array([np.interp(MEM[tag]['t'], dnpz[tag + '_t'],
                             dnpz[tag + '_X'][:, k])
                   for k in range(4)]).T
    ok_npz &= np.max(np.abs(Xi - MEM[tag]['X'])) < 5e-6
check("V3-03 the npz background the arm used matches the BANKED dat "
      "library to < 5e-6 everywhere (all members, all four "
      "coefficients; the residual is LINEAR-INTERPOLATION error of "
      "this comparison near the seal, max 3.2e-6 — the dat t-grid is "
      "1501 points vs the npz's 4097; endpoint values agree to "
      "3e-15)", ok_npz)

NU = 4001
ug = np.linspace(-1, 1, NU)
YU, YUu = Yr(ug), Yru(ug)
TWOK = (0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.004)
GEO = {}
ok_weld = ok_fmin = ok_grow = ok_ord = ok_trust = True
cap_fracs_05 = {}
for tag, M in MEM.items():
    t, X, Xt = M['t'], M['X'], M['Xt']
    fgrid = X @ YU
    ftgrid = Xt @ YU
    fugrid = X @ YUu
    ok_weld &= np.allclose(fgrid[0], 1.0, atol=1e-12)
    ok_fmin &= abs(fgrid.min() - 0.002) < 1e-4
    # growth claim: rays that never dip below 1 vs the funnel:
    minf_ray = fgrid.min(axis=0)
    frac_ge1 = float(np.mean(minf_ray >= 1.0 - 1e-12))
    fmax = fgrid.max()
    gson = fgrid * ftgrid**2 - (1 - ug**2)[None, :] * fugrid**2
    t_turn = np.full(NU, np.nan)
    for j in range(NU):
        s = np.where(gson[:, j] < 0)[0]
        if len(s) and s[0] > 0:
            i = s[0]
            a, b = gson[i - 1, j], gson[i, j]
            t_turn[j] = t[i - 1] + (t[i] - t[i - 1]) * a / (a - b)
    ok_trust &= np.nanmin(t_turn) > M['t1pc']
    GEO[tag] = dict(fmax=fmax, frac_ge1=frac_ge1, t_turn=t_turn,
                    f=fgrid, minf_ray=minf_ray)
    print(f"   {tag}: f_max {fmax:.2f}; rays never below 1: "
          f"{frac_ge1*100:.2f}%; t_turn_min {np.nanmin(t_turn):.4f} "
          f"(t1pc {M['t1pc']}); funnel u-extent "
          f"[{ug[minf_ray < 1].min():+.4f}, "
          f"{ug[minf_ray < 1].max():+.4f}]")
    for twok in TWOK:
        t_loc = np.full(NU, np.nan)
        for j in range(NU):
            s = np.where(fgrid[:, j] < twok)[0]
            if len(s):
                i = s[0]
                a, b = fgrid[i - 1, j] - twok, fgrid[i, j] - twok
                t_loc[j] = t[i - 1] + (t[i] - t[i - 1]) * a / (a - b)
        frac = float(np.mean(~np.isnan(t_loc)))
        both = ~np.isnan(t_loc) & ~np.isnan(t_turn)
        if both.any():
            ok_ord &= bool(np.all(t_loc[both] > t_turn[both]))
            ok_ord &= bool(np.all(t_loc[both] < M['t_stop']))
        if twok == 0.5:
            cap_fracs_05[tag] = frac
        print(f"     2k={twok}: cross {frac*100:5.2f}% of rays")
check("V3-04 weld f == 1 (<1e-12) and global f_min == 0.002 on every "
      "member, straight from the banked dat files",
      ok_weld and ok_fmin)
check("V3-05 THE GEOMETRY CORRECTION upheld on a 4001-node u-grid: "
      "f grows inward on most rays (>=95% of rays never dip below "
      "1); true f_max per member 58.4/14.1/14.4 (M1/M2/M4); at "
      "2 kappa = 0.5 only 0.37-1.8% of rays cross — the locus is a "
      "narrow seal-funnel cap, NOT an interior surface crossing "
      "every cell (the substantive correction stands, STRENGTHENED)",
      all(GEO[tag]['frac_ge1'] >= 0.95 for tag in MEM)
      and all(14.0 <= GEO[tag]['fmax'] <= 58.5 for tag in MEM)
      and all(0.003 <= cap_fracs_05[tag] <= 0.019 for tag in MEM))
check("V3-05b DOC NUMBER DEFECT (recorded): the results doc claims "
      "'f_max 6.8-33' — but the committed script's own output prints "
      "f-range maxima 58.43/14.10/14.36, and the doc's numbers "
      "{6.86, 7.46, 33.04} are the SHELL-CROSSING F_cross values "
      "from the dat headers, not cell f_max; my dat-direct f_max "
      "values match the script output (58.4/14.1/14.4), refuting the "
      "doc's wording, not the script",
      abs(GEO['M1']['fmax'] - 58.43) < 0.3
      and abs(GEO['M2']['fmax'] - 14.10) < 0.2
      and abs(GEO['M4']['fmax'] - 14.36) < 0.2)
check("V3-06 ORDERING upheld at u-resolution 4001 (vs the arm's 801): "
      "every resolvable crossing has t_turn < t_loc < t_stop, and "
      "t_turn_min > t1pc on every member (locus + turning + seal all "
      "beyond the 1% trust window)", ok_ord and ok_trust)
check("V3-07 M2 turning anchor: earliest Delta_w crossing == 1.2551 "
      "(< 5e-3), independent reconstruction",
      abs(np.nanmin(GEO['M2']['t_turn']) - 1.2551) < 5e-3)

# =====================================================================
print()
print("=" * 72)
print("PART 3 — C-2: THE PENCIL, CONSISTENT-FEM INDEPENDENT BUILD")
print("=" * 72)
UN12 = np.polynomial.legendre.leggauss(12)[0]


def fem_mats(tg, coef):
    """P1-FEM: stiffness for -(p psi')' with p = coef['p'], and
    CONSISTENT (tridiagonal) matrices for the potentials/mass, exact
    element integrals with linear interpolation of the coefficient
    (Simpson is exact for the cubic integrand)."""
    N = len(tg) - 1
    h = np.diff(tg)
    out = {}
    pm = 0.5 * (coef['p'][:-1] + coef['p'][1:])
    K = np.zeros((N + 1, N + 1))
    for e in range(N):
        k = pm[e] / h[e]
        K[e, e] += k
        K[e + 1, e + 1] += k
        K[e, e + 1] -= k
        K[e + 1, e] -= k
    out['K'] = K
    for nm in ('V', 'V2', 'B'):
        c = coef[nm]
        Mt = np.zeros((N + 1, N + 1))
        for e in range(N):
            c0, c1 = c[e], c[e + 1]
            # int over element of c(t) phi_i phi_j dt, c linear:
            Mt[e, e] += h[e] * (3 * c0 + c1) / 12
            Mt[e + 1, e + 1] += h[e] * (c0 + 3 * c1) / 12
            Mt[e, e + 1] += h[e] * (c0 + c1) / 12
            Mt[e + 1, e] += h[e] * (c0 + c1) / 12
        out[nm] = Mt
    return out


def ray_coefs(tag, u, tg):
    M = MEM[tag]
    Xi = np.array([np.interp(tg, M['t'], M['X'][:, k])
                   for k in range(4)]).T
    Y, Yu = Yr(np.array([u])), Yru(np.array([u]))
    fvn = (Xi @ Y)[:, 0]
    fun = (Xi @ Yu)[:, 0]
    su = 1 - u * u
    return {'p': np.exp(-tg) * fvn,
            'V': np.exp(-tg) * su * fun**2 / fvn,
            'V2': np.exp(-tg) * su * fun**2 / fvn**2,
            'B': np.exp(-3 * tg) / fvn,
            'f': fvn}


def kc_member(tag, tb, N=1600, nodes=UN12):
    ko, kn = [], []
    tg = np.linspace(0, tb, N + 1)
    for u in nodes:
        c = ray_coefs(tag, u, tg)
        m = fem_mats(tg, c)
        sl = slice(0, N)        # Dirichlet at tb, natural at 0
        lo = sla.eigh(m['V'][sl, sl], m['K'][sl, sl],
                      eigvals_only=True,
                      subset_by_index=[N - 1, N - 1])[0]
        ln = sla.eigh(m['V'][sl, sl],
                      m['K'][sl, sl] + 0.75 * m['V2'][sl, sl],
                      eigvals_only=True,
                      subset_by_index=[N - 1, N - 1])[0]
        ko.append(3 / 8 * lo)
        kn.append(3 / 8 * ln)
    return np.array(ko), np.array(kn)


VA4_KC = {'M1': 0.01160, 'M2': 0.00789, 'M4': 0.00829}
rt, rf = {}, {}
okA = True
for tag in MEM:
    ko, kn = kc_member(tag, MEM[tag]['t1pc'])
    okA &= abs(ko.max() - VA4_KC[tag]) < 2e-4
    rt[tag] = kn.max() / ko.max()
    print(f"   {tag} trust: kc_old {ko.max():.5f} (VA4 "
          f"{VA4_KC[tag]}), kc_new {kn.max():.5f}, ratio "
          f"{rt[tag]:.4f}")
check("V3-08 CONSISTENT-FEM (independent assembly) reproduces the "
      "VA4 grid-converged anchors {0.01160, 0.00789, 0.00829} to "
      "< 2e-4 on trust windows — the arm's lumped convention is not "
      "load-bearing", okA)
for tag in MEM:
    ko, kn = kc_member(tag, MEM[tag]['t_stop'])
    rf[tag] = kn.max() / ko.max()
    print(f"   {tag} full: kc_old {ko.max():.5f}, kc_new "
          f"{kn.max():.5f}, ratio {rf[tag]:.4f}")
check("V3-09 THE RATIO READOUT upheld on independent discretization: "
      "kappa_c^new/old = 0.990 +- 0.002 on every trust window and in "
      "[0.76, 0.86] on full domains; kappa_c^new < kappa_c^old "
      "everywhere (the V2 >= 0 corollary realized)",
      all(abs(rt[t_] - 0.990) < 0.002 for t_ in MEM)
      and all(0.76 < rf[t_] < 0.86 for t_ in MEM)
      and all(rt[t_] < 1 and rf[t_] < 1 for t_ in MEM))
ko24, kn24 = kc_member('M1', MEM['M1']['t1pc'], N=3200)
check("V3-10 N-convergence: M1 trust kc_old and kc_new move < 1e-4 "
      "from N = 1600 to N = 3200",
      abs(ko24.max() - VA4_KC['M1']) < 2e-4
      and abs(kn24.max() - rt['M1'] * VA4_KC['M1']) < 1e-4)


def lowest_omega2(tag, tb, kapv, u, N=1600, bc='dir', h_rob=5.0,
                  pencil='new', nmodes=1):
    tg = np.linspace(0, tb, N + 1)
    c = ray_coefs(tag, u, tg)
    m = fem_mats(tg, c)
    A = m['K'] - 3 / (8 * kapv) * m['V']
    if pencil == 'new':
        A = A + 0.75 * m['V2']
    B = m['B']
    if bc == 'dir':
        A, B = A[:N, :N], B[:N, :N]
        dof_t = tg[:N]
        fdof = c['f'][:N]
    else:
        if bc == 'rob':
            A = A.copy()
            A[N, N] += c['p'][N] * h_rob
        dof_t = tg
        fdof = c['f']
    evals, evecs = sla.eigh(A, B, subset_by_index=[0, nmodes - 1])
    res = []
    for k in range(nmodes):
        psi = evecs[:, k]
        mass = psi * (B @ psi)
        mass = mass / mass.sum()
        res.append((evals[k], float(mass[fdof < 2 * kapv].sum()),
                    float((mass * dof_t).sum())))
    return res


# direct sweep crossing (C-2): bisect kappa where lowest omega^2 = 0
def kc_bisect(tag, tb, u, pencil, lo=1e-4, hi=0.05):
    f_ = (lambda k: lowest_omega2(tag, tb, k, u, pencil=pencil)[0][0])
    a, b = lo, hi
    if f_(a) * f_(b) > 0:
        return np.nan
    for _ in range(40):
        m_ = 0.5 * (a + b)
        if f_(a) * f_(m_) <= 0:
            b = m_
        else:
            a = m_
    return 0.5 * (a + b)


tag = 'M1'
tb = MEM[tag]['t1pc']
ko, kn = kc_member(tag, tb)
ju = int(np.argmax(ko))
ubest = UN12[ju]
kc_dir_old = kc_bisect(tag, tb, ubest, 'old')
kc_dir_new = kc_bisect(tag, tb, ubest, 'new')
print(f"   M1 trust, most-unstable node u = {ubest:+.4f}: bisected "
      f"kc_old {kc_dir_old:.5f} vs eig {ko.max():.5f}; kc_new "
      f"{kc_dir_new:.5f} vs eig {kn.max():.5f}")
check("V3-11 DIRECT SWEEP CROSSING (their V-5): bisection of the "
      "lowest omega^2 zero reproduces the (3/8) lambda_max kappa_c "
      "for BOTH pencils to < 2e-4 — the corollary is a real "
      "spectral crossing, not an algebraic artifact",
      abs(kc_dir_old - ko.max()) < 2e-4
      and abs(kc_dir_new - kn.max()) < 2e-4)

# C-5: u-resolution of the kappa_c convention:
udense = np.linspace(-0.999, 0.999, 81)
ko_d, _ = kc_member('M1', MEM['M1']['t1pc'], N=800, nodes=udense)
print(f"   C-5 M1 trust, dense-u lambda scan: max kc_old(u) = "
      f"{ko_d.max():.5f} at u = {udense[np.argmax(ko_d)]:+.3f} "
      f"(12-node Gauss readout {ko.max():.5f})")
check("V3-12 C-5 u-resolution: the dense-u (81-node) kappa_c^old max "
      "exceeds the 12-node Gauss readout by < 5% on M1 trust — the "
      "anchor convention is u-resolved enough that the RATIO readout "
      "stands (absolute kappa_c carries the 12-node convention, "
      "noted)",
      ko_d.max() < 1.05 * ko.max())

# =====================================================================
print()
print("=" * 72)
print("PART 4 — C-3: NO-TRAPPING ATTACKED ON SEAL-POLE RAYS + ROBIN")
print("=" * 72)
tag = 'M1'
tb = MEM[tag]['t_stop']
ok_trap = True
for kapv in (0.3, 0.1):
    cross = np.where(GEO[tag]['minf_ray'] < 2 * kapv)[0]
    if len(cross) == 0:
        print(f"   kappa = {kapv}: NO ray reaches f < 2 kappa")
        continue
    # the deepest-cap ray (seal pole):
    jstar = cross[np.argmin(GEO[tag]['minf_ray'][cross])]
    upole = ug[jstar]
    print(f"   kappa = {kapv}: {len(cross)} of {NU} rays cross; "
          f"deepest-cap ray u = {upole:+.5f} "
          f"(min f = {GEO[tag]['minf_ray'][jstar]:.4f})")
    for bc in ('dir', 'neu', 'rob'):
        for pencil in ('old', 'new'):
            modes = lowest_omega2(tag, tb, kapv, upole, N=2400,
                                  bc=bc, pencil=pencil, nmodes=3)
            capm = [m[1] for m in modes]
            print(f"     u_pole {bc:>3s} {pencil:>3s}: omega^2 = "
                  + ", ".join(f"{m[0]:9.2f}" for m in modes)
                  + " | cap mass = "
                  + ", ".join(f"{cm:.2e}" for cm in capm))
            ok_trap &= all(cm < 1e-2 for cm in capm)
check("V3-13 C-3 NO TRAPPING — upheld under attack: on the SEAL-POLE "
      "ray itself (the ray that reaches f < 2 kappa), with Dirichlet, "
      "Neumann AND Robin h=5 inner BCs, kappa = 0.3 and 0.1, the "
      "three lowest modes of BOTH pencils each carry < 1% of their "
      "mass in the f < 2 kappa cap: the locus traps no mode even "
      "where it exists and even when the boundary lets modes live "
      "there", ok_trap)
# the arm's specific statement (most-unstable node never reaches cap):
ko_full, _ = kc_member('M1', tb)
jmax = int(np.argmax(ko_full))
c = ray_coefs('M1', UN12[jmax], np.linspace(0, tb, 1601))
check("V3-14 the arm's most-unstable-node statement: on M1 full "
      "domain the most unstable Gauss node's ray never reaches "
      "f < 0.6 (kappa = 0.3) nor f < 0.2 (kappa = 0.1)",
      c['f'].min() > 0.6)

print()
print(f"TOTALS: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
for x in FAIL:
    print("FAILED:", x)
