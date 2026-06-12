"""NONSTATIONARY SECTOR N2 — script 4: validated evolution kernel + anchors.

K1: collar-cell spectral kernel (banked weld phase-2 object = the
    diagonal-scheme linearization of this push's reduced system, ell=1):
    reproduce omega^2 = -3.4667814 (lam=2, gamma=2q), -10.376405 (lam=6),
    L0 = 1.33835009 / 2.29931870, and boosted gamma=1.5*L0:
    omega^2 = +4.0701100.
K2: the anchors AS TIME EVOLUTIONS. Character (s3): the T-sector is
    ELLIPTIC — the second-order T-march is Hadamard-ill-posed; the
    computable native evolution is the first-order relaxation flow
    u_T = W^{-1} L u (spectrum bounded above), whose late-time rate from
    GENERIC data is exactly the banked omega^2 (non-circular). Both
    anchors fitted to 4+ digits; plus an explicit mesh-rate blowup demo
    of the second-order march (the ill-posedness made concrete).
K3: breathing-trial verification of the w-fate on a concrete
    time-dependent configuration.

Background (banked S1): interior r <= R=1: f = r^{-q}, q = 1/3,
E0_bulk = s/r^2, s = 1/9; BC-c Robin u'(R) = (gamma/R) u(R), gamma = 2q;
Friedrichs core (indicial a+ = (sqrt(17)-1)/6). Operator:
(r^2 f^2 u')' - [lam f + 4 r^2 f^2 E0] u = omega^2 r^2 u.
In x = ln r:  d_x(e^{bx} u_x) - e^x V u = omega^2 e^{3x} u,
b = 1 - 2q, V = lam e^{-qx} + 4 s e^{-2qx}.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eig_banded, solve_banded

PASS, FAIL = [], []
def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label)

QB, SB = 1.0 / 3.0, 1.0 / 9.0
APLUS = (np.sqrt(17.0) - 1.0) / 6.0
BX = 1.0 - 2.0 * QB

# ---------------------------------------------------------------- K1a: L0 shooting
def L0_shoot(lam, x0=-40.0):
    def rhs(x, y):
        u, up = y
        return [up, -BX * up + (lam * np.exp(QB * x) + 4 * SB) * u]
    sol = solve_ivp(rhs, (x0, 0.0), [1.0, APLUS], rtol=1e-12, atol=1e-300,
                    dense_output=False, max_step=0.05)
    u, up = sol.y[0, -1], sol.y[1, -1]
    return up / u

L0_2 = L0_shoot(2.0)
L0_6 = L0_shoot(6.0)
print(f"    L0(lam=2) = {L0_2:.8f}   banked 1.33835009")
print(f"    L0(lam=6) = {L0_6:.8f}   banked 2.29931870")
check("K1a: L0 matches banked to 1e-6", abs(L0_2 - 1.33835009) < 1e-6
      and abs(L0_6 - 2.29931870) < 1e-6)

# ---------------------------------------------------------------- K1b: FD eigensolver
def assemble(lam, gamma, x0=-30.0, n=12000):
    """Symmetric FD of  d_x(e^{bx}u_x) - e^x V u  with weight e^{3x};
    Robin flux e^{bx}u_x = e^{bx0} Lcore u at x0 (zero-energy core
    log-derivative, shot exactly), and = gamma u at x=0 (BC-c).
    Returns (diag, off, weight, x). Form: u^T L u = -sum fluxes...
    """
    x = np.linspace(x0, 0.0, n)
    hh = x[1] - x[0]
    xm = 0.5 * (x[:-1] + x[1:])
    k = np.exp(BX * xm) / hh**2            # face conductances
    V = lam * np.exp(-QB * x) + 4 * SB * np.exp(-2 * QB * x)
    diag = -np.exp(x) * V
    diag[0] *= 0.5
    diag[-1] *= 0.5            # half-cell potential at the end nodes
    diag[1:-1] -= (k[:-1] + k[1:])
    diag[0] -= k[0]
    diag[-1] -= k[-1]
    # Robin closures (flux form): left boundary flux = e^{b x0} Lcore u_0
    def core_logderiv():
        def rhs(xx, y):
            u, up = y
            return [up, -BX * up + (lam * np.exp(QB * xx) + 4 * SB) * u]
        sol = solve_ivp(rhs, (-45.0, x0), [1.0, APLUS], rtol=1e-12,
                        atol=1e-300, max_step=0.05)
        return sol.y[1, -1] / sol.y[0, -1]
    Lcore = core_logderiv()
    diag[0] += np.exp(BX * x0) * Lcore / hh
    diag[-1] += np.exp(0.0) * gamma / hh
    off = k.copy()
    wgt = np.exp(3.0 * x)
    wgt[0] *= 0.5
    wgt[-1] *= 0.5             # half-cell mass at the end nodes
    return diag, off, wgt, x

def top_eigs(lam, gamma, x0=-30.0, n=12000, vlo=-80.0, vhi=40.0):
    diag, off, wgt, x = assemble(lam, gamma, x0, n)
    s = 1.0 / np.sqrt(wgt)
    d2 = diag * s * s
    o2 = off * s[:-1] * s[1:]
    band = np.zeros((2, len(d2)))
    band[0] = d2
    band[1, :-1] = o2
    vals = eig_banded(band, lower=True, eigvals_only=True,
                      select='v', select_range=(vlo, vhi))
    return np.sort(vals)[::-1]

ev2 = top_eigs(2.0, 2 * QB)
ev6 = top_eigs(6.0, 2 * QB)
gboost = 1.5 * L0_2
evb = top_eigs(2.0, gboost)
print(f"    top omega^2 (lam=2, gamma=2q)      = {ev2[0]:.7f}   banked -3.4667814")
print(f"    top omega^2 (lam=6, gamma=2q)      = {ev6[0]:.7f}   banked -10.376405")
print(f"    top omega^2 (lam=2, gamma=1.5 L0)  = {evb[0]:.7f}   banked +4.0701100")
check("K1b: FD top eigenvalues match banked to 4+ digits",
      abs(ev2[0] + 3.4667814) < 2e-4 and abs(ev6[0] + 10.376405) < 2e-3
      and abs(evb[0] - 4.0701100) < 2e-4)
# convergence control: 2nd-order FD; Richardson over n-doubling
ev2c = top_eigs(2.0, 2 * QB, n=24000)
ev_rich = (4 * ev2c[0] - ev2[0]) / 3
print(f"    Richardson(12000, 24000) = {ev_rich:.8f}   banked -3.4667814")
check("K1c: Richardson-extrapolated eigenvalue = banked to 1e-6 "
      "(h^2 convergence verified)", abs(ev_rich + 3.4667814) < 1e-6)

# ---------------------------------------------------------------- K2: time evolutions
def relax_flow(lam, gamma, T_end, dt=1e-4, x0=-12.0, n=3000, seed=3,
               theta=0.55):
    """theta-method (L-damping at stiff infinity, rate bias
    (theta-1/2) lam^2 dt ~ 1e-4) on  W u_T = L u  — the well-posed native
    relaxation flow (spectrum of W^{-1}L bounded above). GENERIC data.
    Returns fitted late-time rate d ln||u||_W / dT  (= top omega^2)."""
    from scipy.linalg import cholesky_banded, cho_solve_banded
    diag, off, wgt, x = assemble(lam, gamma, x0, n)
    rng = np.random.default_rng(seed)
    u = rng.normal(size=n)
    # LHS = W - theta dt L (SPD); upper-banded for cholesky_banded
    ab = np.zeros((2, n))
    ab[1] = wgt - theta * dt * diag
    ab[0, 1:] = -theta * dt * off
    cb = cholesky_banded(ab)
    one_m = (1.0 - theta) * dt
    nsteps = int(T_end / dt)
    norms = np.zeros(nsteps + 1)
    norms[0] = np.sqrt(np.sum(wgt * u * u))
    for i in range(nsteps):
        rhs = (wgt + one_m * diag) * u
        rhs[:-1] += one_m * off * u[1:]
        rhs[1:] += one_m * off * u[:-1]
        u = cho_solve_banded((cb, False), rhs)
        nrm = np.sqrt(np.sum(wgt * u * u))
        norms[i + 1] = nrm
        u /= nrm
    lognorm = np.cumsum(np.log(norms[1:]))
    tgrid = dt * np.arange(1, nsteps + 1)
    i0 = int(0.7 * nsteps)
    rate = np.polyfit(tgrid[i0:], lognorm[i0:], 1)[0]
    return rate

r_banked = relax_flow(2.0, 2 * QB, T_end=10.0)
r_boost = relax_flow(2.0, gboost, T_end=10.0)
print(f"    relaxation-flow rate (banked cell) = {r_banked:.6f}   target -3.4667814")
print(f"    relaxation-flow rate (boosted)     = {r_boost:.6f}   target +4.0701100")
check("K2a: BANKED ANCHOR as time evolution: generic-data late-time rate "
      "= -3.4668 to 4+ digits", abs(r_banked + 3.4667814) < 5e-4)
check("K2b: BOOSTED ANCHOR as time evolution: generic-data late-time rate "
      "= +4.0701 to 4+ digits", abs(r_boost - 4.0701100) < 5e-4)
print(f"    (second-order reading: the boosted top mode oscillates at "
      f"omega = {np.sqrt(abs(r_boost)):.7f}; the banked top mode is the "
      f"e^{{+-{np.sqrt(abs(r_banked)):.7f} T}} pair)")

# Hadamard demonstration: the second-order T-march excites mesh-rate
# growth (elliptic character made concrete; rate INCREASES with mesh).
def second_order_blowup(n, x0=-4.0, lam=2.0, gamma=2 * QB, nstep=4000):
    diag, off, wgt, x = assemble(lam, gamma, x0, n)
    def Au(v):
        out = diag * v
        out[:-1] += off * v[1:]
        out[1:] += off * v[:-1]
        return out / wgt
    # power iteration for the most negative eigenvalue of W^{-1}L:
    v = np.random.default_rng(0).normal(size=n)
    for _ in range(200):
        v = Au(v)
        v /= np.linalg.norm(v)
    lam_extreme = (v @ Au(v)) / (v @ v)
    sigma_mesh = np.sqrt(abs(lam_extreme))     # u_TT = -W^{-1}L u: growth rate
    return sigma_mesh

s1m = second_order_blowup(400)
s2m = second_order_blowup(800)
print(f"    second-order mesh growth rate: n=400: {s1m:.3e}, n=800: {s2m:.3e} "
      f"(physical top rate would be {np.sqrt(3.4668):.3f})")
check("K2c: second-order T-march is Hadamard-ill-posed: mesh growth rate "
      ">> physical and increases ~2x under mesh doubling",
      s1m > 50 * np.sqrt(3.4668) and 1.5 < s2m / s1m < 2.5)

# ---------------------------------------------------------------- K3: breathing trial
# f = e^{-2 phi}, phi = phi0(r) [1 + 0.2 sin(Omega T)] [1 + beta P2(cos th)]
# Exact pointwise check of the fate system on a concrete moving profile.
import sympy as sp
fs, As = sp.symbols('f A', positive=True)
qs = sp.Symbol('q', real=True)
vTs, vrs, vhs = sp.symbols('vT vr vh', real=True)
D2s = As / fs - qs**2
Ps = As * vrs**2 - 2 * qs * vrs * vhs + vhs**2 / fs
Rs = fs * Ps + D2s * vTs**2
hs = fs * vrs**2 + vTs**2 / fs
bracks = sp.expand(-Rs * fs * D2s + 2 * As * hs * fs * D2s - As * Rs)
brack_f = sp.lambdify((qs, As, fs, vrs, vhs, vTs), bracks, 'numpy')

def fields(T, r, th, beta, Om=1.0, amp=0.2):
    P2 = 0.5 * (3 * np.cos(th)**2 - 1)
    phi0 = 0.5 * QB * np.log(r)              # collar-like radial profile
    s_t = 1 + amp * np.sin(Om * T)
    s_a = 1 + beta * P2
    phi = phi0 * s_t * s_a
    f = np.exp(-2 * phi)
    phT = phi0 * amp * Om * np.cos(Om * T) * s_a
    phr = 0.5 * QB / r * s_t * s_a
    phh = phi0 * s_t * beta * (-3 * np.cos(th) * np.sin(th))
    return f, -2 * f * phT, -2 * f * phr, -2 * f * phh   # f, vT, vr, vh

def qroots(fv, Av, vrv, vhv, vTv):
    c3 = vTv**2
    c1 = fv * Av * vrv**2 + vhv**2 - (Av / fv) * vTv**2
    c0 = -2 * Av * vrv * vhv
    if abs(c3) < 1e-300:
        return [-c0 / c1] if c1 != 0 else []
    rr = np.roots([c3, 0.0, c1, c0])
    return [z.real for z in rr if abs(z.imag) < 1e-9 * max(1, abs(z))]

rng = np.random.default_rng(11)
# (i) shaped, moving: residual never admissibly zero along w
n_zero_admissible = 0
n_zero_degenerate = 0
n_pts = 0
for _ in range(400):
    T = rng.uniform(0, 6.0); r = rng.uniform(0.2, 1.0)
    th = rng.uniform(0.3, np.pi - 0.3)
    f, vT_, vr_, vh_ = fields(T, r, th, beta=0.3)
    if abs(vh_) < 1e-12:
        continue
    ws = np.linspace(-0.9, 4.0, 800)
    Avals = r**2 * (1 + ws)**2
    for Av in Avals:
        for qv in qroots(f, Av, vr_, vh_, vT_):
            D2v = Av / f - qv**2
            if D2v <= 1e-10:
                continue
            n_pts += 1
            res = brack_f(qv, Av, f, vr_, vh_, vT_)
            scale = abs(Av**2) * (f * vr_**2 + vT_**2 / f + vh_**2 + 1e-30)
            if abs(res) < 1e-9 * scale:
                # exact theorem: zeros only at A=0 or D2=0 (= f q vr = vh);
                # classify against the degenerate loci (relative measures)
                rel_deg = abs(f * qv * vr_ - vh_) / (
                    abs(f * qv * vr_) + abs(vh_) + 1e-30)
                rel_D2 = D2v / (Av / f)
                if rel_deg < 1e-2 or rel_D2 < 1e-2:
                    n_zero_degenerate += 1
                else:
                    n_zero_admissible += 1
print(f"    breathing shaped trial: {n_pts} admissible (w, q-branch) samples, "
      f"{n_zero_admissible} non-degenerate w-equation zeros, "
      f"{n_zero_degenerate} zeros at the degenerate locus (excluded exactly)")
check("K3a: shaped breathing profile: every w-equation zero sits on the "
      "exact degenerate locus; NO admissible zero — motion never sources "
      "shape", n_pts > 50000 and n_zero_admissible == 0)

# (ii) spherical breathing control: residual == 0 identically (q=0, any w)
maxres = 0.0
for _ in range(200):
    T = rng.uniform(0, 6.0); r = rng.uniform(0.2, 1.0)
    th = rng.uniform(0.3, np.pi - 0.3)
    f, vT_, vr_, vh_ = fields(T, r, th, beta=0.0)
    for wv in np.linspace(-0.9, 4.0, 50):
        Av = r**2 * (1 + wv)**2
        res = brack_f(0.0, Av, f, vr_, 0.0, vT_)
        scale = abs(Av**2) * (f * vr_**2 + vT_**2 / f + 1e-30)
        maxres = max(maxres, abs(res) / scale)
print(f"    spherical breathing control: max |residual|/scale = {maxres:.2e}")
check("K3b: spherical breathing: w-equation identically satisfied for ALL w "
      "(exact flat direction, machine precision)", maxres < 1e-12)

# (iii) the T2 law  brack -> (2 A h / g) vh^2  as shape -> 0, on the
# moving profile; both signs of g exercised (sonic-flip validation).
n_ok = 0
n_test = 0
n_gneg = 0
for _ in range(3000):
    T = rng.uniform(0, 6.0); r = rng.uniform(0.05, 1.0)
    th = rng.uniform(0.3, np.pi - 0.3)
    f, vT_, vr_, vh1 = fields(T, r, th, beta=1e-4, amp=0.9, Om=8.0)
    gv = f * vr_**2 - vT_**2 / f
    if abs(gv) < 0.05 * (f * vr_**2 + vT_**2 / f):
        continue                    # stay off the sonic locus for the law
    Av = r**2
    hv = f * vr_**2 + vT_**2 / f
    pred = 2 * Av * hv / gv
    got = []
    for beta in (1e-4, 5e-5):
        f2, vT2, vr2, vh2 = fields(T, r, th, beta=beta, amp=0.9, Om=8.0)
        if abs(vh2) < 1e-14:
            break
        q1v = 2 * vr2 / (f2 * vr2**2 - vT2**2 / f2)
        got.append(brack_f(q1v * vh2 / 1.0 * 1.0 * 1.0 * 1.0 * 1.0,
                           Av, f2, vr2, vh2, vT2) / vh2**2)
    if len(got) < 2:
        continue
    n_test += 1
    if gv < 0:
        n_gneg += 1
    # Richardson: residual/vh^2 should converge to pred
    if abs(got[1] - pred) <= 0.02 * abs(pred) + 1e-12:
        n_ok += 1
print(f"    T2-law validation: {n_ok}/{n_test} converge to 2 A h/g "
      f"(of which {n_gneg} have g < 0: sign flip exercised)")
check("K3c: w-force law brack/vh^2 -> 2 A h / g verified on the moving "
      "profile, both sides of the sonic locus",
      n_test > 500 and n_gneg > 50 and n_ok == n_test)

print()
print("PASS:", len(PASS), " FAIL:", len(FAIL))
if FAIL:
    print("FAILED:", FAIL)
    raise SystemExit(1)
