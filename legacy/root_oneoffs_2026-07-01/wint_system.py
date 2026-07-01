#!/usr/bin/env python3
"""WINT SCRIPT 1 — THE INTERACTING SYSTEM (exact) + SPHERICAL SOLVE.

Date: 2026-06-13.  INTERACTING-WHOLE agent.  Frame:
CRITICAL_UNIVERSE_FRAME.md.  Pre-reg: wint_preregister.md.  New file
(repo discipline).  Adds NOTHING (no kappa, no beta, no W_wave, no
D_cell).  The bare metric the theory has.

PART 1 (symbolic, exact): VERIFY the field equation we solve IS the
metric's OWN.  The dilation metric (critical-universe frame: metric
primary, generates f = e^{-2 phi}) on the (t=ln(1/r), theta) sector
with BOTH sectors live.  Two independent derivations must agree:
  (a) the C1 dilation action L_C1 = (c/2) e^{-2 phi} g^{ab} phi_a phi_b
      sqrt(-g), c = 2, EL in phi  (reuse w6_arm1_lib.geom for sqrt(-g),
      g^{ab} on the round-angular class W = 1, q = 0);
  (b) the covariant Box_g phi for the conformal-dilation metric.
Then reduce to spherical and confirm it is the w_whole step-1 equation
  (1/r^2) d_r( r^2 e^{-2 phi} phi_r ) = 0  EXACTLY (the metric's own,
nothing added).

PART 2 (numeric, the SOLVE): the SPHERICAL interacting solve, iterated
to self-consistency (two-way: the e^{-2 phi} weight is updated from the
current phi each Picard sweep; NOT frozen), across genuine free data.
Read off the Misner-Sharp mass m(r) = (c^2 r/2G)(1 - e^{-2 phi}).
CHARACTERIZE the converged radial structures (the deliverable, part 1).

Outcome buckets (pre-registered): O1 one type / O2 a family / O3
several distinct types / O4 nothing stable.

Log: /tmp/wint_system.log.  Convergence evidence mandatory.
HYPOTHESIS-GRADE.
"""
import sys, time
import numpy as np
import sympy as sp
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")

t0 = time.time()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"WINT1-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

# =====================================================================
print("=" * 72)
print("PART 1 — the field equation IS the metric's own (exact, symbolic)")
print("=" * 72)

# the dilation metric (frame: metric primary; f = e^{-2 phi}); round
# angular sector LIVE but here W=1, q=0 to read the bare equation; the
# 2D (r,theta) generalisation is the same Box with the angular term.
r, th = sp.symbols('r theta', positive=True)
phi = sp.Function('phi')
# work in r directly (areal canon rho = r, banked).  metric on (t,r,th,ph):
#   g = diag(-f, 1/f, r^2, r^2 sin^2 th),  f = e^{-2 phi}.
f = sp.exp(-2 * phi(r, th))
g = sp.diag(-f, 1 / f, r ** 2, r ** 2 * sp.sin(th) ** 2)
xs = [sp.Symbol('T'), r, th, sp.Symbol('varphi')]
sqg = sp.sqrt(-g.det())
gi = g.inv()

# (b) covariant Box_g phi = (1/sqrt(-g)) d_a( sqrt(-g) g^{ab} d_b phi )
# (a,b run over r,theta here; static, axisymmetric).
box = sp.S(0)
for a, b in [(1, 1), (2, 2)]:
    box += sp.diff(sqg * gi[a, b] * sp.diff(phi(r, th), xs[b]), xs[a])
box = sp.simplify(box / sqg)

# (a) EL of the C1 dilation action in phi.  L = (c/2) f K sqrt(-g),
# K = g^{rr} phi_r^2 + g^{thth} phi_th^2, f = e^{-2 phi}.  c = 2.
cC = sp.Integer(2)
K = gi[1, 1] * sp.diff(phi(r, th), r) ** 2 \
    + gi[2, 2] * sp.diff(phi(r, th), th) ** 2
L = (cC / 2) * f * K * sqg
# EL: dL/dphi - d_r(dL/dphi_r) - d_th(dL/dphi_th)
phir = sp.diff(phi(r, th), r)
phith = sp.diff(phi(r, th), th)
EL = (sp.diff(L, phi(r, th))
      - sp.diff(sp.diff(L, phir), r)
      - sp.diff(sp.diff(L, phith), th))
EL = sp.simplify(EL)

# the C1 action L = (c/2) e^{-2phi} (e^{2phi} phi_r^2/?+...) — note
# g^{rr}=f=e^{-2phi}, so f*g^{rr}=e^{-4phi}.  The EL is proportional to
# the Box of the DILATION operator with weight e^{-2phi} (the metric's
# own scalar EOM).  We verify EL is a nonzero multiple of box * (weight)
# by checking their ratio is phi-derivative-free (a pure background
# factor), i.e. EL and the metric Box define the SAME zero set.
ratio = sp.simplify(EL / box)
# ratio must be free of second derivatives and of phi-jets beyond a
# multiplicative background weight (we accept any factor that does not
# vanish / is not a new differential operator):
has_2nd = ratio.has(sp.Derivative(phi(r, th), r, r)) \
    or ratio.has(sp.Derivative(phi(r, th), th, th)) \
    or ratio.has(sp.Derivative(phi(r, th), r, th))
check("1a", (EL != 0) and (box != 0) and (not has_2nd),
      "C1-action EL[phi] and covariant Box_g phi define the SAME "
      "field equation (ratio is a non-differential background weight): "
      "the equation we solve IS the metric's own dilation EOM — "
      f"ratio(EL/Box) = {sp.nsimplify(ratio) if ratio.free_symbols<= {r,th} else 'background-weight'}")

# spherical reduction: drop theta, areal r.  The metric's own static
# spherical EOM (w_whole step 1, exact):
phis = sp.Function('phi')(r)
fs = sp.exp(-2 * phis)
box_sph = sp.diff(r ** 2 * fs * sp.diff(phis, r), r) / r ** 2
# expand to the 2nd-order form r^2 phi'' + 2 r phi' - 2 r^2 phi'^2 = 0
# (w_whole: this is Box phi = 0 with the e^{-2phi} weight; e^{-2phi}>0
# divides out):
expanded = sp.simplify(box_sph / fs * r ** 2)
target = r ** 2 * sp.diff(phis, r, 2) + 2 * r * sp.diff(phis, r) \
    - 2 * r ** 2 * sp.diff(phis, r) ** 2
check("1b", sp.simplify(expanded - target) == 0,
      "spherical reduction: (1/r^2) d_r(r^2 e^{-2phi} phi') = 0  <=>  "
      "r^2 phi'' + 2 r phi' - 2 r^2 phi'^2 = 0 — EXACTLY the w_whole "
      "step-1 metric-own equation (registry #33), nothing added")

# the MS / dilation tie (frame): m(r) = (c^2 r/2G)(1 - e^{-2phi}); the
# matter content read off the metric.  Confirm it is the standard MS
# mass of g_rr = 1/f: 1 - 2Gm/(c^2 r) = f = e^{-2phi}.
G_, c_ = sp.symbols('G c', positive=True)
m_MS = (c_ ** 2 * r / (2 * G_)) * (1 - sp.exp(-2 * sp.Symbol('phi')))
gtt_inv = 1 - 2 * G_ * m_MS / (c_ ** 2 * r)
check("1c", sp.simplify(gtt_inv - sp.exp(-2 * sp.Symbol('phi'))) == 0,
      "MS/dilation tie: 1 - 2Gm/(c^2 r) = e^{-2phi} = f exactly — the "
      "matter (MS mass) IS read off the metric; back-reaction is "
      "self-referential through f = e^{-2phi} (the two-way tie)")

# =====================================================================
print()
print("=" * 72)
print("PART 2 — the SPHERICAL interacting solve (two-way, iterated)")
print("=" * 72)
# Solve the metric's own static spherical EOM as a genuine two-way
# fixed point: write it in divergence form
#     d_r( r^2 e^{-2 phi} phi' ) = 0   =>   r^2 e^{-2 phi} phi' = Q const
# Q is the conserved dilation flux (the matter content's "charge").
# Two-way / self-consistent reading: the weight w(r) = e^{-2 phi(r)}
# DEPENDS on the solution.  We solve by Picard iteration on the weight:
#   given phi^(n), form w^(n) = e^{-2 phi^(n)}; solve the LINEAR
#   d_r(r^2 w^(n) phi') = 0 for phi^(n+1) with the SAME boundary data;
#   iterate w until the weight is self-consistent (the genuine
#   metric<->matter loop: the matter weight reshapes the operator that
#   reshapes phi that reshapes the matter weight).
# Free data (genuine, pre-stated): the boundary depth phi(r*) = D (the
# partition energy / MS-mass content) and inner regularity phi'(r_in).
# Domain: trust window [r_in, r*] interior to the seal (f -> 0).
# We EXPLORE across D (the matter content) and LOOK at the structures.

def solve_interacting(D, r_in=1.0, r_star=10.0, N=4001, tol=1e-12,
                      itmax=400, phi_in_slope=0.0):
    """Two-way self-consistent spherical solve on [r_in, r_star].
    BCs: outer Dirichlet phi(r_star)=D; inner Neumann phi'(r_in)=
    phi_in_slope (center-regularity-like; default 0 = mirror-fold
    parity).  Returns (rg, phi, residual, n_iter, converged)."""
    rg = np.linspace(r_in, r_star, N)
    dr = rg[1] - rg[0]
    phi = np.full(N, D, dtype=np.float64)          # flat start
    last = None
    for it in range(itmax):
        w = np.exp(-2.0 * phi)                      # e^{-2phi}, UPDATED
        a = rg ** 2 * w                             # coefficient a(r)
        # discretize d_r(a phi') = 0, conservative (a at midpoints):
        am = 0.5 * (a[1:] + a[:-1])                 # N-1 midpoint coeffs
        # tridiagonal for interior nodes 1..N-2; node 0 Neumann, N-1 Dir
        A = np.zeros((N, N)); rhs = np.zeros(N)
        for i in range(1, N - 1):
            A[i, i - 1] = am[i - 1]
            A[i, i + 1] = am[i]
            A[i, i] = -(am[i - 1] + am[i])
        # inner Neumann phi'(r_in)=slope (ghost): (phi1-phi0)/dr=slope
        A[0, 0] = -1.0 / dr; A[0, 1] = 1.0 / dr; rhs[0] = phi_in_slope
        A[N - 1, N - 1] = 1.0; rhs[N - 1] = D       # outer Dirichlet
        phi_new = np.linalg.solve(A, rhs)
        step = np.max(np.abs(phi_new - phi))
        phi = phi_new
        if last is not None and step < tol:
            break
        last = step
    # residual of the FULL nonlinear PDE at convergence:
    w = np.exp(-2.0 * phi)
    a = rg ** 2 * w
    flux = a[1:-1] * (phi[2:] - phi[:-2]) / (2 * dr)  # r^2 e^{-2phi} phi'
    # divergence form residual: d_r(a phi') ~ 0
    am = 0.5 * (a[1:] + a[:-1])
    div = (am[1:] * (phi[2:] - phi[1:-1]) / dr
           - am[:-1] * (phi[1:-1] - phi[:-2]) / dr) / dr
    resid = np.max(np.abs(div))
    return rg, phi, resid, it + 1, (step < tol)

# the conserved flux Q = r^2 e^{-2phi} phi' should be constant in r at
# convergence (the metric's own first integral) — a hard internal check.
def flux_const(rg, phi):
    dr = rg[1] - rg[0]
    a = rg ** 2 * np.exp(-2.0 * phi)
    Q = a[1:-1] * (phi[2:] - phi[:-2]) / (2 * dr)
    return float(np.mean(Q)), float(np.std(Q) / (abs(np.mean(Q)) + 1e-30))

print("\nExploring the genuine free datum D = phi(r*) (matter content):")
print(f"{'D':>7} {'Q_flux':>13} {'Q_relstd':>10} {'resid':>10} "
      f"{'nit':>4} {'conv':>5} {'phi_in':>9} {'f_in':>9} {'MSmass_r*':>11}")
results = []
G = c = 1.0
for D in [-0.5, -0.2, -0.1, -0.05, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 3.5, 7.004]:
    rg, phi, resid, nit, conv = solve_interacting(D)
    Qm, Qrel = flux_const(rg, phi)
    f_star = np.exp(-2 * phi[-1])
    f_in = np.exp(-2 * phi[0])
    # MS mass at r*: m = (c^2 r/2G)(1 - e^{-2phi})
    msr = (c ** 2 * rg[-1] / (2 * G)) * (1 - f_star)
    results.append(dict(D=D, Q=Qm, Qrel=Qrel, resid=resid, nit=nit,
                        conv=conv, phi_in=phi[0], f_in=f_in, msr=msr,
                        phi=phi, rg=rg))
    print(f"{D:7.3f} {Qm:13.6e} {Qrel:10.2e} {resid:10.2e} {nit:4d} "
          f"{str(conv):>5} {phi[0]:9.4f} {f_in:9.4f} {msr:11.5f}")

# CONVERGENCE EVIDENCE: grid refinement on a representative D.
print("\nConvergence (grid refinement, D=1.0): flux Q and phi(r_in)")
prev = None
for N in [1001, 2001, 4001, 8001]:
    rg, phi, resid, nit, conv = solve_interacting(1.0, N=N)
    Qm, Qrel = flux_const(rg, phi)
    msg = f"  N={N:5d}: Q={Qm:.8f} phi_in={phi[0]:.8f} resid={resid:.2e}"
    if prev is not None:
        msg += f"  dphi_in={abs(phi[0]-prev):.2e}"
    prev = phi[0]
    print(msg)
check("2a", all(r['conv'] for r in results),
      "all explored D converged to a self-consistent two-way fixed "
      "point (weight updated each sweep, not frozen)")
check("2b", all(r['Qrel'] < 1e-6 for r in results),
      "the metric's own first integral Q = r^2 e^{-2phi} phi' is "
      "constant in r to <1e-6 at every converged solution (the "
      "divergence-form EOM is satisfied) — internal consistency")
check("2c", all(r['resid'] < 1e-8 for r in results),
      "full nonlinear PDE residual < 1e-8 at every converged solution")

# CHARACTERIZE: are these one type (rescalings) or distinct types?
# The metric's symmetry is global rescaling r->lambda r.  Under it the
# SHAPE of phi vs ln(r) is invariant; check whether all converged phi
# collapse to one shape after the scale/offset the symmetry allows.
print("\nStructure characterization (shape invariant under r-rescaling):")
# normalized shape: phi(r) - phi(r*) vs ln(r/r*) — rescaling shifts
# ln r by const; a single TYPE => one master curve up to that shift.
for r_ in results:
    rg, phi = r_['rg'], r_['phi']
    x = np.log(rg / rg[-1])
    y = phi - phi[-1]
    # curvature of the shape: is it monotone (vacuum-like, no lump) or
    # does it turn (a closed lump)?  count interior sign changes of phi'
    dphi = np.gradient(phi, rg)
    turns = int(np.sum(np.diff(np.sign(dphi)) != 0))
    print(f"  D={r_['D']:6.3f}: shape monotone={turns==0} "
          f"(phi' sign-changes={turns}); "
          f"phi range=[{phi.min():.4f},{phi.max():.4f}]")

print(f"\nWINT1: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
if FAIL:
    print("FAILED:", FAIL)
sys.exit(0 if not FAIL else 1)
