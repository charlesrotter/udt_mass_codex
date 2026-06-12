"""
N1 script 3: THE EXTERIOR CONTINUATION AT IMAGINARY FREQUENCY
(exclusion axis b) + the conserved-quantity axis (c).

Derivation (recorded here, used below):
 - The mode grows as exp(k T): omega^2 = -k^2 < 0, i.e. sigma = k^2 > 0.
 - The exterior medium obeys the SAME flipped time sector (MF1: the
   flip factor is pointwise, background-independent), so the exterior
   channel equation is the banked collar form continued through the
   weld with the SAME generalized eigenvalue sigma:
      -(y^2 f^2 chi')' + (lam f + 4 s_eff f^2/y^2 *y^2 ... ) chi
   with f = y^{-1/3}; in explicit self-adjoint form on y >= 1:
      -(y^{4/3} chi')' + y^{4/3} [ lam y^{-5/3} + mu2/y^2 ] chi
            = sigma y^2 chi,     mu2 = (nu^2-1)/36,
   nu = 3 (screened, licensed primary; mu2 = 2/9) or sqrt(17)
   (unscreened; mu2 = 4/9).  VALIDATION: at sigma = 0 the decaying
   solution is exactly chi = y^{-1/6} K_nu(6 sqrt(lam) y^{1/6}) and
   D := -chi_y(1)/chi(1) must reproduce the banked D_+ closed form
   (incl. the l = 0 limit (1+nu)/6, exact by indicial roots
   p = (-1 +- nu)/6).
 - INFINITE exterior, sigma > 0: the weight term dominates at large y
   (sigma y^2 vs decaying potential), Liouville-Green k(y) =
   sqrt(sigma) y^{1/3}: BOTH solutions oscillate with envelope
   y^{-5/6}; the action/B-norm integral Int y^2 chi^2 dy ~ Int y^{1/3}
   diverges => NO finite-action growing eigenmode on the unwalled
   exterior -- but sigma > 0 lies in the CONTINUOUS spectrum of the
   composite self-adjoint pencil, and under u_TT = +(A/B)u every
   positive spectral component anti-damps (cosh(sqrt(sigma)T) growth of
   the spectral measure), so the continuation does NOT quench secular
   growth; it delocalizes it.
 - FINITE exterior (the physical one: the recorded kappa -> 1 walls at
   y_w = 2.746 (M1) / 2.353 (M2) / 6.851 (M4), ensembles record;
   finite-cell canon): the composite system is again discrete. Compute
   D_wall(l, sigma; BC at wall in {Dirichlet, Neumann}) by integrating
   the exterior ODE inward, replace D_+ in M_out, and solve the
   composite fixed point  sigma = sigma_min[FEM(M_out(sigma))].
"""
import numpy as np, pickle, time
import scipy.linalg as sla
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import mpmath as mp
mp.mp.dps = 30

C = pickle.load(open('/tmp/nonstat_n1/cache.pkl', 'rb'))
meta, CF, MOUTC, LBLK, VH, WC = (C['meta'], C['CF'], C['MOUT'],
                                 C['LBLK'], C['VH'], C['WC'])
R = pickle.load(open('/tmp/seal_s2/results_main.pkl', 'rb'))
PASSN = []
def checkN(name, ok, detail=""):
    PASSN.append((name, bool(ok)))
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")

NU_S, NU_U = 3.0, float(mp.sqrt(17))
YWALL = {'M1': 2.746, 'M2': 2.353, 'M4': 6.851}

def Dplus(lam, nu):
    if lam == 0:
        return float((1 + mp.mpf(nu))/6)
    tau0 = 6*mp.sqrt(lam); nu = mp.mpf(nu)
    K = mp.besselk(nu, tau0)
    Kp = (mp.besselk(nu-1, tau0) + mp.besselk(nu+1, tau0))/(-2)
    return float((1 - 2*mp.mpf(1)/3)/2 - mp.sqrt(lam)*Kp/K)

def ext_rhs(lam, mu2, sig):
    def rhs(y, z):
        chi, dchi = z
        # (y^{4/3} chi')' = y^{4/3}[(lam y^{-5/3} + mu2/y^2) - sig y^{2/3}] chi
        return [dchi, -(4/3)*dchi/y
                + (lam*y**(-5/3) + mu2/y**2 - sig*y**(2/3))*chi]
    return rhs

def D_wall(lam, sig, yw, bc, nu=NU_S):
    mu2 = (nu**2 - 1)/36.0
    z0 = [0.0, 1.0] if bc == 'D' else [1.0, 0.0]
    sol = solve_ivp(ext_rhs(lam, mu2, sig), (yw, 1.0), z0, method='DOP853',
                    rtol=1e-11, atol=1e-13)
    chi, dchi = sol.y[0, -1], sol.y[1, -1]
    return -dchi/chi

# ---------- V1: closed-form validation at sigma = 0 ----------
print("=== V1: exterior ODE reconstruction vs banked D_+ (sigma=0) ===")
errs = []
for lam in (2.0, 6.0, 12.0):
    for nu in (NU_S, NU_U):
        # exact decaying solution as IC at large y, integrate inward
        yb = 60.0
        def chiK(y):
            return float(y**(-1/6)*mp.besselk(nu, 6*mp.sqrt(lam)*y**(1/6)))
        eps = 1e-6
        z0 = [chiK(yb), (chiK(yb+eps) - chiK(yb-eps))/(2*eps)]
        mu2 = (nu**2 - 1)/36.0
        sol = solve_ivp(ext_rhs(lam, mu2, 0.0), (yb, 1.0), z0,
                        method='DOP853', rtol=1e-12, atol=1e-300)
        Dnum = -sol.y[1, -1]/sol.y[0, -1]
        Dref = Dplus(lam, nu)
        errs.append(abs(Dnum - Dref))
        print(f"  lam={lam:4.0f} nu={nu:.3f}: D integrate-in {Dnum:.8f} "
              f"vs closed form {Dref:.8f}")
checkN("V1 exterior ODE + K_nu decaying solution reproduce the banked "
       "D_+ closed form (3 lam x 2 nu, <= 2e-6)", max(errs) < 2e-6,
       f"max {max(errs):.1e}")
# l = 0 indicial check
D0 = D_wall(0.0, 0.0, 1e6, 'D')
checkN("V2 l=0, sigma=0, far wall: D -> (1+nu)/6 (indicial root)",
       abs(D0 - (1 + NU_S)/6) < 1e-3, f"{D0:.6f} vs {(1+NU_S)/6:.6f}")

# ---------- V3: infinite exterior at sigma > 0: oscillation + envelope ---
print("\n=== V3: unwalled exterior at sigma = 7.06 (M1 rate^2): both "
      "solutions oscillate; envelope exponent; B-norm divergence ===")
sig = 7.057579
for lam in (0.0, 6.0):
    sol = solve_ivp(ext_rhs(lam, 2/9, sig), (1.0, 4000.0), [1.0, 0.0],
                    method='DOP853', rtol=1e-10, atol=1e-12,
                    dense_output=True)
    ys = np.geomspace(50, 3900, 4000)
    ch = sol.sol(ys)[0]
    # envelope exponent by log-log fit of local maxima of |chi|
    loc = [i for i in range(1, len(ys)-1)
           if abs(ch[i]) >= abs(ch[i-1]) and abs(ch[i]) >= abs(ch[i+1])]
    yy, aa = np.log(ys[loc]), np.log(np.abs(ch[loc]))
    p = np.polyfit(yy, aa, 1)[0]
    # B-norm growth: Int_1^Y y^2 chi^2 dy ~ Y^{4/3}
    Ygrid = np.array([500., 1000., 2000., 3900.])
    In = []
    for Y in Ygrid:
        yi = np.linspace(1.0, Y, 40000)
        ci = sol.sol(yi)[0]
        In.append(np.trapezoid(yi**2*ci**2, yi))
    q = np.polyfit(np.log(Ygrid), np.log(In), 1)[0]
    nzero = np.sum(np.sign(ch[1:]) != np.sign(ch[:-1]))
    print(f"  lam={lam:3.0f}: zeros on [50,3900]: {nzero}; envelope "
          f"~ y^{p:+.3f} (LG: -5/6 = -0.833); B-norm ~ Y^{q:+.3f} "
          f"(LG: +4/3)")
    if lam == 0.0:
        checkN("V3 envelope/B-norm exponents match Liouville-Green "
               "(osc. continuum; no finite-action growing mode unwalled)",
               abs(p + 5/6) < 0.05 and abs(q - 4/3) < 0.05,
               f"env {p:+.3f}, norm {q:+.3f}")

# ---------- composite FEM with sigma-dependent M_out ----------
def fem_min(tag, mm, Mout, N=220, nev=3):
    cf = CF[(tag, mm)]; d = cf['d']
    tb = meta[tag]['t1pc']
    tg, Hg, Gg = cf['t'], cf['H'], cf['GA']
    s = np.linspace(0.0, tb, N + 1)
    ndof = (N + 1)*d
    K = np.zeros((ndof, ndof)); B = np.zeros((ndof, ndof))
    I = np.eye(d)
    for e in range(N):
        he = s[e+1] - s[e]; tm = 0.5*(s[e] + s[e+1])
        j = max(min(np.searchsorted(tg, tm) - 1, len(tg) - 2), 0)
        w = (tm - tg[j])/(tg[j+1] - tg[j])
        Hm = (1-w)*Hg[j] + w*Hg[j+1]; Gm = (1-w)*Gg[j] + w*Gg[j+1]
        pm = np.exp(-tm); qm = 2*np.exp(-tm)*Hm; wm = np.exp(-3*tm)*Gm
        i0 = e*d
        K[i0:i0+d, i0:i0+d] += pm/he*I + qm*he/3
        K[i0+d:i0+2*d, i0+d:i0+2*d] += pm/he*I + qm*he/3
        K[i0:i0+d, i0+d:i0+2*d] += -pm/he*I + qm*he/6
        K[i0+d:i0+2*d, i0:i0+d] += -pm/he*I + qm*he/6
        B[i0:i0+d, i0:i0+d] += wm*he/3
        B[i0+d:i0+2*d, i0+d:i0+2*d] += wm*he/3
        B[i0:i0+d, i0+d:i0+2*d] += wm*he/6
        B[i0+d:i0+2*d, i0:i0+d] += wm*he/6
    K[:d, :d] += Mout
    last = N*d; drop = []
    Tm = np.eye(ndof)
    if mm == 0:
        R4 = np.column_stack([VH, WC])
        Tm[last:last+d, last:last+d] = R4
        K = Tm.T @ K @ Tm; B = Tm.T @ B @ Tm
        drop = [last]
    keep = np.setdiff1d(np.arange(ndof), drop)
    K = 0.5*(K + K.T)
    w = sla.eigh(K[np.ix_(keep, keep)], B[np.ix_(keep, keep)],
                 eigvals_only=True, subset_by_index=[0, nev-1])
    return w

def mout_sig(tag, mm, sig, yw, bc, nu=NU_S):
    m = meta[tag]; ls = LBLK[mm]
    # recover the member/block Gaunt C from the cached static M_out
    Msc = MOUTC[tag][mm]['scr']
    Dst = [Dplus(l*(l+1), NU_S) for l in ls]
    Cg = (np.diag([m['gamma'] + d for d in Dst]) - Msc)/m['c']
    Dw = [D_wall(l*(l+1), sig, yw, bc, nu) for l in ls]
    M = np.diag([m['gamma'] + d for d in Dw]) - m['c']*Cg
    return 0.5*(M + M.T)

# sanity: static walled D vs banked bracket
print("\n=== T8: walled STATIC D (sigma=0) vs banked infinite-exterior "
      "D_+ (screened) ===")
for tag in ('M1', 'M2', 'M4'):
    yw = YWALL[tag]
    row = []
    for l in range(4):
        lam = l*(l+1)
        row.append((Dplus(lam, NU_S), D_wall(lam, 0.0, yw, 'D'),
                    D_wall(lam, 0.0, yw, 'N')))
    print(f"  {tag} (y_w={yw}): " + " | ".join(
        f"l={l}: inf {a:.3f} wallD {b:.3f} wallN {c:.3f}"
        for l, (a, b, c) in enumerate(row)))

# ---------- T9: composite fixed points sigma = sigma_min(M_out(sigma)) --
print("\n=== T9: composite (cell + walled exterior) growing modes ===")
t0 = time.time()
COMP = {}
for tag in ('M1', 'M2', 'M4'):
    yw = YWALL[tag]
    for mm in range(4):
        ref = R[(tag, mm, 'ladder')][0]
        for bc in ('D', 'N'):
            def g(sig):
                Mo = mout_sig(tag, mm, sig, yw, bc)
                return fem_min(tag, mm, Mo, nev=1)[0] - sig
            # scan for ALL fixed points of the LOWEST interior branch
            sgrid = np.geomspace(0.02, 3.0*ref, 40)
            gv = np.array([g(s_) for s_ in sgrid])
            roots = []
            for i in range(len(sgrid)-1):
                a, b = gv[i], gv[i+1]
                if np.isfinite(a) and np.isfinite(b) and a*b < 0 \
                   and abs(a) < 5*ref and abs(b) < 5*ref:
                    try:
                        roots.append(brentq(g, sgrid[i], sgrid[i+1],
                                            xtol=1e-6))
                    except Exception:
                        pass
            COMP[(tag, mm, bc)] = roots
            rt = " ".join(f"{r:.4f}" for r in roots[:6])
            print(f"  {tag} m={mm} wall-{bc}: fixed points sigma = [{rt}]"
                  f"  (static-D_+ ref {ref:.4f})")
print(f"  wall {time.time()-t0:.0f}s")

surv = all(len(COMP[(tag, mm, bc)]) > 0
           for tag in ('M1', 'M2', 'M4') for mm in range(4)
           for bc in ('D', 'N'))
checkN("T9 growth SURVIVES exterior matching: every member/block/wall-BC "
       "has at least one self-consistent growing composite mode", surv)
lo = {(tag, mm): min(min(COMP[(tag, mm, 'D')] or [np.inf]),
                     min(COMP[(tag, mm, 'N')] or [np.inf]))
      for tag in ('M1', 'M2', 'M4') for mm in range(4)}
print("\n  lowest composite rate vs static-D_+ rate:")
for tag in ('M1', 'M2', 'M4'):
    for mm in range(4):
        ref = R[(tag, mm, 'ladder')][0]
        print(f"   {tag} m={mm}: k_comp(lowest) = {np.sqrt(lo[(tag,mm)]):.4f}"
              f" vs k_ref = {np.sqrt(ref):.4f}")

# ---------- T10: conserved-quantity axis ----------
print("\n=== T10: conserved quantities ===")
print(" (i) Hamiltonian: H2[mode] = E2 - K2 = (sigma - k^2)<u,Bu>/4 = 0")
print("     exactly on every growing mode (k^2 = sigma): growth is")
print("     energetically FREE under L2 = -(c/2)[T+U]; energy")
print("     conservation cannot quench it. (analytic; zero by")
print("     construction of the mode pair)")
print(" (ii) weld flux / Q = 2 p_F: the no-flux (pure-Neumann) spectra")
MODES, NOFLUX = C['MODES'], C['NOFLUX']
for tag in ('M1', 'M2', 'M4'):
    sig_nf = NOFLUX[tag]['sig'][0]
    sig_rf = R[(tag, 0, 'ladder')][0]
    u = MODES[(tag, 0)]['modes'][0]; s = MODES[(tag, 0)]['sgrid']
    du0 = (u[1] - u[0])/(s[1] - s[0])
    print(f"   {tag}: reference mode u(0) = {np.round(u[0],3)}, "
          f"u'(0) = {np.round(du0,3)} (monopole flux NONZERO); "
          f"no-flux sigma {sig_nf:.4f} vs ref {sig_rf:.4f} "
          f"(rate slowdown x{np.sqrt(sig_rf/sig_nf):.2f})")
checkN("T10 flux constraint SLOWS but does not freeze the m=0 scaling "
       "sector (no-flux sigma_min > 0 in all members)",
       all(NOFLUX[t]['sig'][0] > 1e-3 for t in ('M1', 'M2', 'M4')))
n = sum(1 for _, ok in PASSN if ok)
print(f"\nN1-EXTERIOR PASS {n}/{len(PASSN)}")
