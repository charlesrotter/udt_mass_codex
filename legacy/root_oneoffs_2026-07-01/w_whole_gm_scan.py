#!/usr/bin/env python3
"""
w_whole_gm_scan.py -- GENERAL-MEMBER COMPACTNESS, STEP 2 (the scan)
==================================================================
SHOOTING / NONLINEAR-EIGENVALUE solve of the closed whole-profile BVP
across general members. Determines whether the over-determined closure
(inner regularity + outer Dirichlet AND Neumann) admits a DISCRETE set
of compactness X or a CONTINUOUS band.

Frame: CRITICAL_UNIVERSE_FRAME.md. Pre-registration in
w_whole_gm_derive.py. Date 2026-06-13. Driver: GM-COMPACTNESS agent.

THE OBJECT (derived in step 1, nothing added):
  whole-profile dressed equation in the flow chart m, on a cell [0, M]:
      v_mm = Phi(m) e^{-2 v},
  with the metric's geometry fixing the weight Phi:
      LIOUVILLE member (rho=1, f~1/r):   Phi(m) = Phi0   (constant)
      EMDEN-FOWLER member (rho!=1):      Phi(m) = Lambda / m^2
  Closure conditions (all derived):
      inner regularity   v'(0) = 0     (center; mirror-fold parity)
      outer Dirichlet    v(M)  = v_*   (= the depth set by X)
      outer Neumann      v'(M) = 0      (CR-87 pair)
  PLUS the dilation/compactness map that converts the dressed depth to
  the physical compactness X (handled exactly in step 3).

WHY THE OUTER NEUMANN IS DECISIVE: a 2nd-order ODE launched with
v'(0)=0 is a 1-parameter shooting family (parameter = v(0)). Demanding
v'(M)=0 at the outer end (a SECOND zero of v') is ONE nonlinear
condition on that one parameter at fixed cell aspect -- a nonlinear
eigenvalue condition. We scan it directly and watch for isolated roots
vs a continuum.

NUMERICS: high-precision RK (mpmath) for the canonical roots; a torch
float64 GPU sweep for the dense landscape + convergence doubling. We
work in a SCALE-FIXED chart for each member to isolate the genuine
modulus (NOT the rescaling freedom, already proven free in Axis 1).
"""
import sys, time
import numpy as np
import mpmath as mp

t0 = time.time()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    PASS.append((tag, ok))
    if not ok:
        FAIL.append(tag)
    print(f"[{'PASS' if ok else 'FAIL'}] {tag}: {note}", flush=True)

mp.mp.dps = 40

# =====================================================================
print("="*72)
print("PART A -- LIOUVILLE MEMBER (rho=1, f~1/r): the flat-member check")
print("="*72)
print("""
Autonomous v_mm = Phi0 e^{-2v}. General solution (Phi0>0):
   v(m) = ln[ (sqrt(Phi0)/theta) cosh(theta (m - m0)) ].
v'(m) = theta tanh(theta(m-m0)); v'=0 ONLY at m=m0. So v'(0)=0 forces
m0=0; then v'(M)=theta tanh(theta M) = 0 forces M=0 (degenerate) OR
theta=0 (flat). => with v'(0)=0 AND v'(M)=0 the autonomous member has
NO nontrivial cell: the two Neumann nodes cannot both be interior of a
finite cosh. The closure is EMPTY on the cosh branch.
""")
# Confirm symbolically/numerically: v' = theta tanh(theta(m-m0)).
def vL(m, theta, m0, Phi0):
    return mp.log((mp.sqrt(Phi0)/theta)*mp.cosh(theta*(m-m0)))
def vLp(m, theta, m0):
    return theta*mp.tanh(theta*(m-m0))
# v'(0)=0 => m0=0; then v'(M)=0 requires tanh(theta M)=0 => M=0.
val = vLp(mp.mpf('1.0'), mp.mpf('0.7'), mp.mpf('0'))   # at m=1, m0=0
check("A1-cosh-single-node",
      abs(vLp(mp.mpf('0'), mp.mpf('0.7'), mp.mpf('0'))) < mp.mpf(10)**-30
      and abs(val) > mp.mpf('0.1'),
      "cosh branch: v'(0)=0 (m0=0) but v'(M)!=0 for M>0 -> Neumann-Neumann"
      " admits NO nontrivial cell on the autonomous member")
print("""
RESOLUTION (the banked flat-member closure was DIRICHLET-DIRICHLET, the
seal=mirror double-well, giving s tanh s = 1). With the corrected CR-87
OUTER Dirichlet+NEUMANN pair, the autonomous Liouville member has the
center as its ONLY v'=0 node, so the proper closed cell on rho=1 is the
HALF-CELL [0, M] with v'(0)=0 at the center and the OUTER pair at M.
The cosh has no second v'=0 -> the rho=1 member supplies its closure
through the Dirichlet leg alone with the inner regularity; the Neumann
leg is the SEAL parity (v'(0)=0 at the mirror center). The single
Gelfand-Bratu root s tanh s = 1 is recovered as the Dirichlet+mirror
closure (banked). We now test the GENERAL member where Dirichlet AND a
genuine interior-free Neumann coexist.""")

# =====================================================================
print()
print("="*72)
print("PART B -- EMDEN-FOWLER MEMBER (rho!=1): v_mm = Lambda m^{-2} e^{-2v}")
print("THE GENERAL NON-FLAT MEMBER. The decisive scan.")
print("="*72)
print("""
The scale-invariant Emden-Fowler equation v_mm = Lambda m^{-2} e^{-2v}.
SCALE SYMMETRY (the hostile-continuum suspect): under m -> sigma m,
v -> v + ln sigma, the equation is INVARIANT. This is the m-chart image
of the global rescaling (Axis 1, proven free). We must MOD OUT this
symmetry to isolate the genuine compactness modulus, else we will
mistake the rescaling for a physical continuum.

EXACT closed form via the scaling symmetry: substitute v = ln(m) + u(tau),
tau = ln m. Then (compute below) the equation becomes AUTONOMOUS in tau:
   u_tautau + u_tau = Lambda e^{-2u} - 1   ... (derived, not assumed)
An autonomous 2nd-order ODE in tau with a friction term. Its phase
portrait (u, u_tau) carries the closure. The compactness modulus is the
tau-LENGTH of the cell (= ln(m_outer/m_center)), which is scale-INVARIANT
(a ratio) -- exactly the dimensionless compactness, with the m-rescaling
divided out.
""")
# Derive the autonomous reduction exactly with sympy.
import sympy as sp
msym, Lam = sp.symbols('m Lambda', positive=True)
tau = sp.symbols('tau', real=True)
u = sp.Function('u')
# v = ln m + u(tau), tau = ln m  => d/dm = (1/m) d/dtau
vexpr = sp.log(msym) + u(tau)
# express derivatives wrt m via tau=ln m
ut = sp.Function('u')
# v_m = (1 + u') / m ; v_mm = (u'' - (1+u'))/m^2  (chain rule, verify)
vp_m = sp.diff(vexpr.subs(tau, sp.log(msym)), msym)
vpp_m = sp.diff(vexpr.subs(tau, sp.log(msym)), msym, 2)
# the EF equation: v_mm - Lam/m^2 e^{-2v} = 0; sub v=ln m+u
lhs = vpp_m - Lam/msym**2 * sp.exp(-2*vexpr.subs(tau, sp.log(msym)))
lhs = sp.simplify(lhs * msym**2)   # clear m^2
# substitute back tau and u' notation
lhs_tau = lhs.rewrite(sp.exp)
# Build expected autonomous form: u'' + u' - Lam e^{-2u} + 1 = 0  (times?)
uf = sp.Function('u')(tau)
expected = (sp.diff(uf, tau, 2) + sp.diff(uf, tau) - Lam*sp.exp(-2*uf) + 1)
# map lhs (in m) to tau-form: replace u(log m)->u(tau), derivatives
lhs_m = (vpp_m*msym**2 - Lam*sp.exp(-2*vexpr.subs(tau, sp.log(msym))))
# Manually verify the reduction by direct chain-rule on a test:
# v_m = (1+u_tau)/m ; v_mm = d/dm[(1+u_tau)/m] = (u_tautau/m)/m - (1+u_tau)/m^2
#      = (u_tautau - (1+u_tau))/m^2.  EF: that = Lam/m^2 e^{-2v}=Lam/m^2 e^{-2u}/m^2*m^2
# careful: e^{-2v}=e^{-2ln m -2u}=e^{-2u}/m^2 ; Lam/m^2 * e^{-2u}/m^2 = Lam e^{-2u}/m^4?
# That has an extra 1/m^2 -- so the naive v=ln m+u does NOT autonomize. Recompute:
print("  [checking the correct scaling-reduction exponent...]")
# Correct invariant: under m->sigma m, v->v+ln sigma leaves v_mm e^{2v} m^2 fixed?
#  v_mm -> v_mm/sigma^2 ; e^{-2v} -> e^{-2v}/sigma^2 ; m^{-2} -> m^{-2}/sigma^2.
#  eqn v_mm = Lam m^{-2} e^{-2v}: LHS ~1/sigma^2, RHS ~ 1/sigma^2 * 1/sigma^2?
#  RHS m^{-2}e^{-2v} -> sigma^{-2} sigma^{-2} = sigma^{-4}. MISMATCH.
# => the correct symmetry is m->sigma m, v-> v + ln sigma is NOT it.
# Find the true scaling: m->sigma m, v->v + k ln sigma.
#  v_mm -> sigma^{-2} (times e-shift) ; need v_mm = Lam m^{-2} e^{-2v} covariant:
#  v_mm: (d/dm)^2 (v+k ln sigma at m/sigma) = sigma^{-2} v_mm(m/sigma).
#  RHS: Lam (sigma m')^{-2} e^{-2(v+k ln sigma)} with m=sigma m'
#     = Lam sigma^{-2} m'^{-2} sigma^{-2k} e^{-2v}.  Match sigma powers:
#  sigma^{-2} = sigma^{-2-2k} => k=0. So v-> v (no shift), m->sigma m,
#  and we need v_mm(m) form-invariant: v(m)=g(m/sigma)??
#  Actually with k=0: LHS sigma^{-2} v_mm(m/sigma); RHS Lam sigma^{-2} m'^{-2}e^{-2v}.
#  => v_mm(m/sigma) = Lam (m/sigma)^{-2} e^{-2 v(m/sigma)} -- yes if v(m)=v(m/sigma),
#  i.e. v is SCALE-INVARIANT function: v(m)=V(no scale). The symmetry is
#  pure dilation of m with v UNCHANGED: m->sigma m, v(m)->v(m/sigma).
print("""  CORRECTED symmetry: m -> sigma m with v(m) -> v(m/sigma) (v
  unshifted). The autonomizing substitution is tau = ln m, v(m)=w(tau):
  v_m = w_tau/m, v_mm = (w_tautau - w_tau)/m^2, and Lam m^{-2}e^{-2v}
  = Lam m^{-2} e^{-2w}. The m^{-2} CANCELS:
       w_tautau - w_tau = Lam e^{-2w}.
  AUTONOMOUS in tau (a single friction sign). This is the genuine
  general-member whole-profile equation with the rescaling divided out.""")

w = sp.Function('w')
v_of_m = w(sp.log(msym))
vmm = sp.diff(v_of_m, msym, 2)
EF_resid = sp.simplify((vmm - Lam/msym**2*sp.exp(-2*v_of_m))*msym**2)
# should equal w'' - w' - Lam e^{-2w} (in tau args)
wt = w(tau)
target = sp.diff(wt, tau, 2) - sp.diff(wt, tau) - Lam*sp.exp(-2*wt)
# map EF_resid (function of log m) to tau:
EF_in_tau = EF_resid.subs(sp.log(msym), tau)
check("B1-autonomous-reduction",
      sp.simplify(EF_in_tau - target) == 0,
      "EF member reduces EXACTLY to autonomous w_tautau - w_tau = "
      "Lambda e^{-2w} in tau=ln m (m^{-2} cancels; rescaling divided out)")

print("""
NOW the closure in tau-coordinates (tau = ln m, the scale-invariant
chart). The cell spans tau in [tau_c, tau_*] (center to boundary); the
COMPACTNESS modulus is the tau-LENGTH  L = tau_* - tau_c  (scale-free).
Closure (mapped through tau=ln m, m=e^tau):
   v'(0_r-end)=0 etc.  In tau:
     inner regularity  v'(0)=0  ->  w_tau = 0 at the center tau_c
     outer Neumann     v'(M)=0  ->  w_tau = 0 at the boundary tau_*
   (Dirichlet sets the depth, i.e. fixes w at tau_*, converted to X
    in step 3; it does NOT constrain L by itself.)
So the DECISIVE closure for the modulus L is:
   w_tau(tau_c) = 0  AND  w_tau(tau_*) = 0   on   w'' - w' = Lam e^{-2w}.
TWO Neumann nodes of an AUTONOMOUS-with-friction ODE. Friction breaks
the cosh degeneracy of the rho=1 member: the trajectory between two
w_tau=0 nodes is a genuine nonlinear eigenvalue condition on L.
""")

# =====================================================================
print("="*72)
print("PART C -- THE NEUMANN-NEUMANN EIGENVALUE SCAN (mpmath RK, hi-prec)")
print("="*72)
# Autonomous system: w' = p ; p' = p + Lam e^{-2w}.  (w''=w'+Lam e^{-2w})
# Start at a w_tau=0 node: p(tau_c)=0, w(tau_c)=w0. Integrate forward;
# find the NEXT tau where p=0 again -> that gap is L(w0; Lam). The
# closure admits a cell for each (w0) giving a second node. Question:
# is L pinned (discrete) or does a continuum of (w0, L) close?
def rhs(taux, y, Lam):
    wv, pv = y
    return [pv, pv + Lam*mp.exp(-2*wv)]

def integrate_to_next_node(w0, Lam, dtau=mp.mpf('0.002'), taumax=mp.mpf('60')):
    # RK4 in mpmath from a node p=0; return tau of next p=0 (sign change of p)
    wv = mp.mpf(w0); pv = mp.mpf('0'); taux = mp.mpf('0')
    # nudge off the node in the direction the dynamics pushes:
    # at p=0: p' = Lam e^{-2w0} > 0 -> p increases (w grows). To find the
    # NEXT node we must see p return to 0, which needs p to turn around.
    # p' = p + Lam e^{-2w}; with p>0,w growing, Lam e^{-2w} shrinks but
    # the +p term GROWS p (anti-friction). Check if a turnaround exists.
    prev_p = pv
    steps = int(taumax/dtau)
    for i in range(steps):
        k1 = rhs(taux, [wv, pv], Lam)
        k2 = rhs(taux+dtau/2, [wv+dtau/2*k1[0], pv+dtau/2*k1[1]], Lam)
        k3 = rhs(taux+dtau/2, [wv+dtau/2*k2[0], pv+dtau/2*k2[1]], Lam)
        k4 = rhs(taux+dtau, [wv+dtau*k3[0], pv+dtau*k3[1]], Lam)
        wv += dtau/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        pv += dtau/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        taux += dtau
        if i > 0 and prev_p < 0 and pv >= 0:
            return taux  # crossed back to a node
        if i > 0 and prev_p > 0 and pv <= 0:
            return taux
        prev_p = pv
        if wv > 50 or wv < -50:
            return None
    return None

print("""
Integrate w'' - w' = Lam e^{-2w} from a node (p=w_tau=0, w=w0) and look
for the NEXT node p=0 (the outer Neumann). The ANTI-friction sign (+w')
is the metric's own: p' = p + Lam e^{-2w}. At a node p=0, p'=Lam e^{-2w}
>0, so p grows; the +p term then amplifies p (no restoring) -> p does
NOT return to zero. We verify there is NO second interior node:
""")
for Lam in [mp.mpf('1.0'), mp.mpf('0.3'), mp.mpf('3.0')]:
    for w0 in [mp.mpf('0.0'), mp.mpf('0.5'), mp.mpf('-0.5')]:
        L = integrate_to_next_node(w0, Lam)
        print(f"   Lam={float(Lam):+.2f} w0={float(w0):+.2f} -> next node L = {L}")
check("C1-antifriction-no-second-node",
      integrate_to_next_node(mp.mpf('0'), mp.mpf('1.0')) is None,
      "anti-friction (+w') EF member: from a Neumann node p escapes "
      "monotonically -> NO second Neumann node -> Neumann-Neumann "
      "closure EMPTY on the anti-friction branch (like the cosh: the "
      "single-node structure)")

print("""
The OTHER chart (rho>1 vs rho<1) flips the friction sign: dm = dt/p with
the opposite scaling gives w'' + w' = Lam e^{-2w} (TRUE friction). That
member CAN have two nodes (damped). Scan it: this is the genuine general
non-flat member that supports a closed Neumann-Neumann cell.
""")
def rhs2(taux, y, Lam):
    wv, pv = y
    return [pv, -pv + Lam*mp.exp(-2*wv)]   # w'' = -w' + Lam e^{-2w}
def next_node2(w0, Lam, dtau=mp.mpf('0.002'), taumax=mp.mpf('80'), p0sign=1):
    wv=mp.mpf(w0); pv=mp.mpf('0'); taux=mp.mpf('0'); prev=pv
    # at node p=0, p'=Lam e^{-2w0}>0 -> w grows; friction -p damps;
    steps=int(taumax/dtau)
    for i in range(steps):
        k1=rhs2(taux,[wv,pv],Lam)
        k2=rhs2(taux+dtau/2,[wv+dtau/2*k1[0],pv+dtau/2*k1[1]],Lam)
        k3=rhs2(taux+dtau/2,[wv+dtau/2*k2[0],pv+dtau/2*k2[1]],Lam)
        k4=rhs2(taux+dtau,[wv+dtau*k3[0],pv+dtau*k3[1]],Lam)
        wv+=dtau/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0])
        pv+=dtau/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        taux+=dtau
        if i>2 and prev>0 and pv<=0:
            return taux,wv
        prev=pv
        if wv>60 or wv<-60: return None
    return None
print("   FRICTION branch w'' + w' = Lam e^{-2w} (the other general member):")
for Lam in [mp.mpf('1.0'), mp.mpf('0.3'), mp.mpf('3.0'), mp.mpf('0.1')]:
    rows=[]
    for w0 in [mp.mpf('0.0'), mp.mpf('0.5'), mp.mpf('1.0'), mp.mpf('-0.5')]:
        res=next_node2(w0,Lam)
        rows.append((float(w0), None if res is None else float(res[0])))
    print(f"   Lam={float(Lam):+.2f}: (w0, L_to_next_node) = {rows}")

check("C2-friction-monotone-source-empty",
      all(next_node2(w0, mp.mpf('1.0')) is None
          for w0 in [mp.mpf('0'), mp.mpf('0.5'), mp.mpf('1.0')]),
      "BOTH friction signs: a MONOTONE (single-exponential e^{-2w}) "
      "source has NO sign change, so p=w_tau cannot return to 0 -> "
      "the OFF/vacuum member admits NO Neumann-Neumann cell. A closed "
      "two-turning-point cell REQUIRES a restoring term (the ON / "
      "two-exponential source). This is the metric telling us the "
      "closed cell is the ON member, not the OFF vacuum.")

# =====================================================================
print()
print("="*72)
print("PART D -- THE ON (TWO-EXPONENTIAL) MEMBER: the genuine closed cell")
print("v_mm = Phi (e^{-2v} - e^{v})  (w_alg PART E, exact elliptic)")
print("="*72)
print("""
w_alg PART E: the ON-branch whole-profile statics on the member is the
EXACT elliptic equation v_mm = Phi(e^{-2v} - e^{v}) with first integral
   (1/2) v_m^2 + (Phi/2) e^{-2v} + Phi e^{v} = E   (E3, banked).
This source CHANGES SIGN at e^{-2v}=e^{v} (v=0): a genuine restoring
well. It has TWO turning points (v_m=0) for E in a window -> a bounded
oscillation between v_min and v_max. THOSE TWO turning points are the
inner-regularity node and the outer-Neumann node. The cell is the
half-period (or full period) between them. The COMPACTNESS modulus is
the m-length between the two v_m=0 nodes -- and for an autonomous
1st-integral system that length is FIXED by the energy E (quadrature),
giving L(E). So the closure is a CURVE L(E): a continuum unless a
FURTHER condition pins E.

THE FURTHER CONDITION (Dirichlet, the depth): outer Dirichlet fixes
v(M)=v_* (the depth set by the compactness X). Combined with the two
turning-point Neumann nodes, this is the over-determination: v_min and
v_max are functions of E; demanding the OUTER node sit at the prescribed
depth v_* selects E. Two turning points + a prescribed endpoint value =
the +1 condition. We scan whether this admits discrete E (discrete X)
or a continuum.
""")
def Vpot(vv, Phi):
    # potential s.t. v_m^2/2 = E - U,  U = (Phi/2)e^{-2v} + Phi e^{v}
    return Phi/2*mp.exp(-2*vv) + Phi*mp.exp(vv)
def Umin(Phi):
    # U'(v)= -Phi e^{-2v} + Phi e^{v}=0 -> e^{3v}=1 -> v=0; U(0)=3Phi/2
    return mp.mpf('1.5')*Phi
# For E>Umin there are two turning points v_min<0<v_max with U=E.
def turning_points(E, Phi):
    Um = Umin(Phi)
    if E <= Um: return None
    # solve U(v)=E for the two roots around 0
    f = lambda vv: Vpot(vv, Phi) - E
    try:
        vlo = mp.findroot(f, mp.mpf('-1.0'))
        vhi = mp.findroot(f, mp.mpf('1.0'))
    except Exception:
        return None
    if vlo < 0 < vhi:
        return vlo, vhi
    return None
def half_period(E, Phi, n=4000):
    tp = turning_points(E, Phi)
    if tp is None: return None
    vlo, vhi = tp
    # L = integral_{vlo}^{vhi} dv / sqrt(2(E-U))  (half period; one node->other)
    def integ(vv):
        val = 2*(E - Vpot(vv, Phi))
        if val <= 0: val = mp.mpf('1e-40')
        return 1/mp.sqrt(val)
    # endpoint singularities ~ inverse sqrt: use mp.quad with the turning pts
    return mp.quad(integ, [vlo, vhi])

print("   ON member: two turning points (Neumann nodes) and the m-length")
print("   L(E) between them (the half-period = the closed cell width):")
Phi = mp.mpf('1.0')
Um = Umin(Phi)
print(f"   U_min = {float(Um):.6f} at v=0 (the well bottom)")
Es = [Um*mp.mpf(f) for f in ['1.01','1.05','1.2','1.5','2.0','3.0','5.0']]
Ls = []
for E in Es:
    L = half_period(E, Phi)
    tp = turning_points(E, Phi)
    Ls.append((float(E), None if L is None else float(L),
               None if tp is None else (float(tp[0]), float(tp[1]))))
    print(f"   E={float(E):.4f}  L={None if L is None else float(L):.6f}"
          f"  (v_min,v_max)={None if tp is None else (float(tp[0]),float(tp[1]))}")

# Is L(E) a CONTINUOUS function of E (=> a curve, continuum of cells)?
goodLs = [l for _,l,_ in Ls if l is not None]
mono = all(goodLs[i] != goodLs[i+1] for i in range(len(goodLs)-1))
check("D1-on-member-Lcurve",
      len(goodLs) >= 5 and mono,
      "ON member: the closed-cell width L(E) is a SMOOTH NONCONSTANT "
      "function of the energy E (a CURVE), NOT a discrete set. Each E "
      "in the window gives a valid two-turning-point (Neumann-Neumann) "
      "cell of a DIFFERENT width L. => a CONTINUUM of admissible cells "
      "parameterized by E.")

print("""
THE DECISIVE QUESTION: does the OUTER DIRICHLET (depth v_* = -1/2 ln(1-X)
mapped to the dressed variable) pin E to a DISCRETE set, or does the
(E, depth) map stay a continuous curve? The two turning points are
v_min(E), v_max(E); the boundary depth v_* must equal one of them (the
outer node sits at the boundary). Since v_max(E) is a CONTINUOUS
INVERTIBLE function of E (U is monotone above the well on each side),
ANY prescribed depth v_* in the range selects EXACTLY ONE E -- but a
CONTINUUM of v_* (hence X) are all admissible, each with its own E and
its own L. So the Dirichlet leg RELATES (E <-> depth <-> X) but does
NOT pin X to discrete values.
""")
vmax_of_E = []
for E in Es:
    tp = turning_points(E, Phi)
    if tp: vmax_of_E.append((float(E), float(tp[1])))
inv_cont = all(vmax_of_E[i][1] < vmax_of_E[i+1][1] for i in range(len(vmax_of_E)-1))
check("D2-depth-E-monotone-continuum",
      inv_cont and len(vmax_of_E) >= 5,
      "v_max(E) is STRICTLY MONOTONE in E -> the depth<->E map is a "
      "CONTINUOUS BIJECTION: a prescribed Dirichlet depth selects one E "
      "but a CONTINUUM of depths (X) are admissible. The closure is a "
      "CURVE, not a discrete set, on the ON member.")

print()
print(f"SCAN PART A-D done ({time.time()-t0:.0f}s)")
n=sum(1 for _,ok in PASS if ok)
print(f"CHECKS: {n}/{len(PASS)} PASS  FAIL={FAIL}")
