"""
depth_selector_breather.py
===========================
DEPTH-SELECTOR via the NATIVE NONLINEAR BREATHER back-reaction.

Question: does the native carrier at FINITE amplitude A, back-reacting on the
metric via the native Einstein coupling, produce an effective depth-potential
U(D) whose quantization (postulate A: oint p_D dD = (n+1/2) hbar) selects a
DISCRETE MULTI-RUNG {D_n}, giving the exponential mass ladder mass_n = cost(D_n)?

MODE: STRUCTURE-FIRST (sympy-exact where possible), then numeric-confirm.
DATA-BLIND. No git commit. Agent claude-opus-4-8[1m], 2026-06-19.

NATIVE pieces used (all banked / derived, provenance flagged inline):
  - carrier standing-wave frequency omega^2(D): from quantized_carrier doc,
    V_eff = l(l+1) + V_L, V_L = (1/2)s' - (1/4)s^2, s = 2 v0', v0 = -D f(r).
    Floor l(l+1)W_inf + power-law binding ~ -D^k. (NATIVE carrier + NATIVE charge)
  - dilation COST m(D) = (c^2 r/2G)(1 - e^{-2 v0}) ~ e^{2D} (B1, NATIVE MS, GR-form flag)
  - Einstein back-reaction: the carrier at amplitude A SOURCES the depth.
    G_{mu nu} = kappa T_{mu nu}[carrier]; the depth v0 is sourced by the carrier
    energy density. This is the NATIVE coupling (no imported potential).

POSTULATE A boundary: postulate ONLY hbar quantization + spin-1/2 + statistics.
NATIVE: carrier, charge, depth, i=area-form, the Einstein coupling, the breather
amplitude-frequency relation.
"""
import numpy as np
import sympy as sp

print("="*78)
print("DEPTH-SELECTOR BREATHER — native U(D), confinement, quantization, rungs")
print("="*78)

# -----------------------------------------------------------------------------
# PART 1 — set up the native breather energy E(A, D) symbolically.
#   The breather = the carrier standing wave at amplitude A on depth-D background,
#   back-reacting via Einstein. Its total energy has TWO native contributions:
#   (1) the carrier field energy at amplitude A and frequency omega(D);
#   (2) the gravitational dilation cost of the depth D the carrier sources.
# -----------------------------------------------------------------------------
print("\n--- PART 1: native breather energy E(A,D), the two native pieces ---")

A, D, r, f, l, kappa, xi = sp.symbols('A D r f l kappa xi', positive=True, real=True)

# (1) CARRIER FIELD ENERGY at amplitude A.
# The standing-wave Hamiltonian for u = A*U(r) e^{i omega t} (canonical, area-form
# symplectic structure) is H_field = (1/2) <pi,pi> + (1/2) <u, L_space u> with the
# native time-live operator. For a normalized mode U at amplitude A:
#   E_field(A,D) = (1/2) A^2 * omega^2(D) * N    (N = <U,M U> mode norm, D-indep proxy)
# omega^2(D) is the NATIVE carrier frequency = floor + power-law binding (quantized doc).
# We carry omega^2(D) symbolically as a power law in D (the DERIVED form from the
# quantization doc: V_L ~ D^2 from s=2v0', binding ~ D^k); floor = l(l+1) W_inf.
k_pow = sp.symbols('k_pow', positive=True)         # power index (DERIVED ~3.5-4.9, doc)
Winf, c_bind = sp.symbols('W_inf c_bind', positive=True)
omega2_D = l*(l+1)*Winf - c_bind*D**k_pow          # NATIVE carrier freq, power-law in D
E_field = sp.Rational(1,2)*A**2*omega2_D           # field energy at amplitude A

# (2) GRAVITATIONAL DILATION COST of the depth D.
# B1 Misner-Sharp dilation cost is exponential in depth: cost ~ (1 - e^{2 D f}) at core.
# At the core (f->1) the leading deep cost is ~ e^{2D}. This is the UNDIFFERENTIATED
# amplitude e^{-2 v0} = e^{+2 D f}: the gravitational energy of placing the carrier
# at depth D. NATIVE (B1), GR-form flag carried.
c_grav = sp.symbols('c_grav', positive=True)       # dimensionful prefactor (cancels in ratios)
E_grav = c_grav*(sp.exp(2*D) - 1)                  # MS dilation cost ~ e^{2D}, deep core

print("E_field(A,D) =", E_field, "   [NATIVE carrier freq, power-law in D]")
print("E_grav(D)    =", E_grav, "   [NATIVE B1 MS dilation cost, EXPONENTIAL in D]")

# -----------------------------------------------------------------------------
# PART 2 — the BACK-REACTION constraint: the carrier SOURCES the depth.
#   Einstein: G ~ kappa T[carrier]. The depth v0 is NOT a free parameter once the
#   carrier is present at amplitude A; the carrier energy density sources it.
#   The NATIVE constraint (Misner-Sharp / Hamiltonian constraint) ties the depth
#   to the enclosed carrier energy:  m(D) = (enclosed carrier energy).
#   I.e. the gravitational cost E_grav(D) is SET BY the carrier energy E_field(A,D).
#   This is the native amplitude<->depth relation A(D) (NOT posited).
# -----------------------------------------------------------------------------
print("\n--- PART 2: native back-reaction constraint A<->D (Einstein/MS) ---")
# Hamiltonian constraint (native MS): the dilation cost of depth D EQUALS the
# carrier energy it traps. E_grav(D) = E_field(A,D)  =>  solve A^2(D).
# This is the constraint G^t_t: m(r) = integral of carrier rho. NATIVE.
A2_of_D = sp.solve(sp.Eq(E_grav, E_field), A**2)
print("Back-reaction A^2(D) from  E_grav(D) = E_field(A,D):")
for s in A2_of_D:
    print("  A^2 =", sp.simplify(s))

# -----------------------------------------------------------------------------
# PART 3 — the EFFECTIVE DEPTH-POTENTIAL U(D).
#   With the back-reaction constraint, D is the single collective coordinate.
#   The breather energy as a function of D ALONE (amplitude slaved by Einstein)
#   is the effective depth-potential U(D). We compute it TWO ways and report both
#   (neither chosen to favor confinement):
#   (3a) ON-CONSTRAINT energy: substitute A^2(D) back -> E(D) = E_grav(D) (= E_field,
#        they're equal on-constraint). This is the BARE dilation cost ~ e^{2D}: RISING.
#   (3b) The carrier-stability / kinetic-corrected potential: the TRUE collective
#        Lagrangian for D(t). The depth oscillates; its kinetic term comes from
#        d_t of the sourced depth. U(D) is the POTENTIAL part = total energy at the
#        instantaneous turning configuration. We construct the collective-coordinate
#        Lagrangian L = (1/2) m_D(D) Ddot^2 - U(D) and read U(D).
# -----------------------------------------------------------------------------
print("\n--- PART 3: effective depth-potential U(D) ---")
# (3a) on-constraint energy
E_onconstraint = E_grav   # = E_field on the constraint surface
print("(3a) ON-CONSTRAINT total energy U(D) = E_grav(D) =", E_onconstraint,
      "  -> RISING (e^{2D}-1), monotone increasing in D")

# (3b) The full breather energy is NOT only on-constraint: as a collective coordinate
# D can be displaced off the equilibrium the amplitude prefers. The effective potential
# for the depth mode is the SUM of the two native energies at FIXED amplitude A
# (the amplitude set at the equilibrium depth D0, then D varied as the breathing mode):
# U(D; A) = E_grav(D) + E_field(A, D)   with A fixed = A(D0).
# This is the standard collective-coordinate (Bogomolny/moduli) construction:
# freeze the amplitude, let the depth breathe. The carrier energy DECREASES with D
# (binding deepens, -c_bind D^k) while the gravitational cost INCREASES (e^{2D}).
# => a COMPETITION: possible WELL.
A0sq = sp.symbols('A0sq', positive=True)   # amplitude^2 fixed at equilibrium
U_breath = E_grav + sp.Rational(1,2)*A0sq*omega2_D
U_breath = sp.expand(U_breath)
print("(3b) BREATHING potential U(D;A0) = E_grav(D) + (1/2)A0^2 omega^2(D):")
print("     U(D) =", U_breath)
dU = sp.diff(U_breath, D)
print("     dU/dD =", sp.simplify(dU))

# -----------------------------------------------------------------------------
# PART 4 — DOES U(D) CONFINE? Structure of U(D).
#   U(D) = c_grav(e^{2D}-1) + (1/2)A0^2[l(l+1)W_inf - c_bind D^k]
#   Two competing terms:
#     + c_grav e^{2D}  : gravitational cost, RISING, EXPONENTIAL (dominates large D)
#     - (1/2)A0^2 c_bind D^k : carrier binding, FALLING, POWER-LAW
#   At small D the power-law fall can dominate -> U decreases; at large D the
#   exponential rise dominates -> U increases. => a MINIMUM => a WELL (confines!)
#   BUT: the well's existence and the rung count depend on whether the minimum sits
#   BELOW the tachyon cap D* (omega^2(D*) = 0), and whether multiple bound depth-modes
#   fit. We test this NUMERICALLY in Part 5-6 with native-scale (dimensionless) values
#   and an explicit anti-box-control check. Here: confirm the SHAPE analytically.
# -----------------------------------------------------------------------------
print("\n--- PART 4: confinement structure of U(D) ---")
# large-D behaviour (e^{2D} term dominates -> rising wall) — substitute k_pow=4 (mid of
# the DERIVED 3.5-4.9 range) only to display the SHAPE; the verdict is k-robust (Part 5).
U_disp = U_breath.subs({k_pow:4})
print("large-D: e^{2D} term dominates ->  U -> +inf  (RISING WALL at large D)")
print("d2U/dD2 =", sp.simplify(sp.diff(U_breath, D, 2)),
      "  (= 4 c_grav e^{2D} - power'' ; convex at large D)")
print("\nU has a stationary point where dU/dD=0:")
print("   2 c_grav e^{2D} = (1/2)A0^2 c_bind k D^{k-1}")
print("   (exp rise rate) = (power fall rate)  -> a balance depth D_min (well bottom?)")
print("\nKEY STRUCTURAL FACT (the obstruction's seed): the FALLING term is the")
print("CARRIER FREQUENCY omega^2(D), and omega^2(D)=0 at the tachyon cap D*. Past D*")
print("the carrier is unstable (no standing wave). So the 'binding' that pulls U down")
print("is ONLY available for D<D*, and at D* the falling term has bottomed out")
print("(omega^2->0). The well bottom and D* are TIED. We test if the well sits below D*.")

print("\n[Part 1-4 symbolic structure complete. Numeric confinement+rungs below.]")

# =============================================================================
# PART 5 — NUMERIC CONFINEMENT TEST of U(D), with the tachyon cap enforced.
#
#   HONEST STRUCTURAL CAVEAT (must not smuggle): the "falling" carrier term
#   -(1/2)A0^2 c_bind D^k comes from omega^2(D) = floor - c_bind D^k. That is
#   only PHYSICAL while omega^2(D) > 0 (a real standing wave). Past D* (omega^2=0)
#   the carrier is a TACHYON and (1/2)A0^2 omega^2 going negative is NOT binding
#   energy -- it is instability. So a well built by letting omega^2 go negative is
#   FAKE. We therefore build U(D) two ways:
#     (5a) NAIVE: U = E_grav + (1/2)A0^2 omega^2  (lets omega^2 go negative) -- audit.
#     (5b) PHYSICAL: U_phys(D) = E_grav(D) + (1/2)A0^2 * max(omega^2(D), 0), i.e. the
#          carrier contribution truncates at D* (beyond which there is no carrier).
#   The PHYSICAL U is the honest one. The well must come from E_grav's shape + the
#   carrier binding ONLY in D < D*.
# =============================================================================
import numpy as np
print("\n" + "="*78)
print("PART 5 — NUMERIC confinement of U(D), tachyon cap enforced")
print("="*78)

# Native dimensionless scales. CHOSE values flagged. All ratios scale-free in c_grav.
# omega^2(D) = floor - c_bind D^k. Calibrate floor & c_bind & D* from the quantization
# doc's DERIVED facts (NOT from wall numbers): floor=l(l+1)W_inf ~ 2 (l=1, W_inf~1);
# tachyon cap D* ~ 2.6 (doc Finding 2); power k ~ 4 (doc Finding 3). c_bind set so
# omega^2(D*)=0.
def make_potential(c_grav_v, A0sq_v, floor_v, Dstar_v, kpow_v):
    # c_bind from omega^2(D*)=0:  floor = c_bind D*^k
    c_bind_v = floor_v / Dstar_v**kpow_v
    def omega2(Dv):
        return floor_v - c_bind_v*np.asarray(Dv, float)**kpow_v
    def E_grav_f(Dv):
        return c_grav_v*(np.exp(2*np.asarray(Dv,float)) - 1.0)
    def U_naive(Dv):
        return E_grav_f(Dv) + 0.5*A0sq_v*omega2(Dv)
    def U_phys(Dv):
        w2 = omega2(Dv)
        return E_grav_f(Dv) + 0.5*A0sq_v*np.maximum(w2, 0.0)
    return omega2, E_grav_f, U_naive, U_phys, c_bind_v

# baseline native-scale parameters (CHOSE, flagged; ratios independent of c_grav)
c_grav_v = 1.0     # gravitational cost prefactor (sets the unit; cancels in ratios) CHOSE
floor_v  = 2.0     # l(l+1)W_inf, l=1, W_inf=1   (NATIVE: banked charge floor)
Dstar_v  = 2.6     # tachyon cap (NATIVE: quantization doc D*~2.4-3.4) CHOSE within range
kpow_v   = 4.0     # depth power (NATIVE: doc 3.5-4.9) CHOSE within range
# A0sq sets the carrier's weight vs gravity. CHOSE; scanned in Part 6.
for A0sq_v in [1.0, 5.0, 20.0, 100.0]:
    omega2, E_grav_f, U_naive, U_phys, c_bind_v = make_potential(
        c_grav_v, A0sq_v, floor_v, Dstar_v, kpow_v)
    Dg = np.linspace(0.01, Dstar_v, 4000)
    Uphys = U_phys(Dg); Unaive = U_naive(Dg)
    # find interior minima of U_phys on (0, D*)
    dmin_idx = 1 + np.where((Uphys[1:-1] < Uphys[:-2]) & (Uphys[1:-1] < Uphys[2:]))[0]
    has_well = len(dmin_idx) > 0
    # U at 0, at D*, and min
    U0 = U_phys(1e-6); UDs = U_phys(Dstar_v)
    Umin = Uphys.min(); Dmin = Dg[Uphys.argmin()]
    print(f"\nA0^2={A0sq_v:6.1f}: U(0)={U0:.4f}  U_min={Umin:.4f}@D={Dmin:.3f}  U(D*)={UDs:.4f}")
    print(f"   interior minimum on (0,D*)? {has_well}  (well depth U(D*)-U_min={UDs-Umin:.4f})")
    print(f"   c_bind={c_bind_v:.4f}  omega^2(0)={omega2(0.0):.3f}  omega^2(D*)={omega2(Dstar_v):.2e}")


# =============================================================================
# PART 6 — does ANY native assembly of the two pieces CONFINE? + quantization.
#
# Part 5 verdict (physical, cap enforced): U_phys(D) = E_grav(D) + (1/2)A0^2 max(w2,0)
# is MONOTONE RISING on (0,D*). E_grav ~ e^{2D} rises; the carrier term DROPS by a
# BOUNDED amount (floor->0, finite) so it can never out-pull the exponential.
# => the well bottom sits at D->0; there is a RIGHT WALL (e^{2D}) but NO LEFT WALL.
# This is a HALF-WELL (confining on one side only) -> at most a SINGLE bound depth
# mode against the r->0/D->0 boundary, NOT a multi-rung tower.
#
# But honesty demands: test whether a DIFFERENT native assembly confines. Three
# native candidates for the "other wall" (must be NATIVE, not posited):
#   (i)   the on-constraint A^2(D) diverges at D* (denominator omega^2->0): an
#         INFINITE-cost barrier at D* (right wall) -- but still no LEFT wall.
#   (ii)  a small-D barrier from the charge floor / regularity at the core (D->0
#         means no dilation -> no charge -> the l(l+1) centrifugal core barrier).
#   (iii) the carrier KINETIC mass m_D(D) for the breathing depth mode (the
#         conjugate momentum), which sets the quantization spacing.
# Test (i)+(ii) as the two walls; quantize between them if a well closes.
# =============================================================================
print("\n" + "="*78)
print("PART 6 — confinement audit + depth quantization attempt")
print("="*78)

A0sq_v = 5.0
omega2, E_grav_f, U_naive, U_phys, c_bind_v = make_potential(
    c_grav_v, A0sq_v, floor_v, Dstar_v, kpow_v)

# CANDIDATE (i): on-constraint cost  A^2(D) = 2 E_grav / omega^2(D). Diverges at D*.
def A2_onc(Dv):
    w2 = omega2(Dv)
    return np.where(w2>1e-12, 2*E_grav_f(Dv)/np.maximum(w2,1e-12), np.inf)
# The on-constraint ENERGY is just E_grav (monotone). The DIVERGENCE of A^2 at D*
# means: to source depth->D*, the carrier amplitude -> infinity. So the carrier
# CANNOT reach D*; there is a dynamical right wall BELOW D* where A^2 blows up the
# energy. This is a RIGHT wall, consistent with Part 5. Still one-sided.

# CANDIDATE (ii): small-D core barrier. As D->0, v0->0, dilation vanishes; the
# l(l+1) centrifugal floor is a CONSTANT pedestal (doc: flat, NOT an r^-2 wall in D).
# So there is NO rising barrier as D->0. The charge floor does not supply a left wall.
print("\nLeft-wall test (small D): the l(l+1) floor is a flat pedestal (doc Finding,")
print("W/M=1 => constant, NOT a 1/D^2 barrier). => NO native left wall at small D.")
print("Right-wall test (D->D*): on-constraint A^2(D) -> inf (omega^2->0).")
A2_near = A2_onc(np.array([2.0, 2.4, 2.55, 2.59, 2.599]))
print("  A^2(D) approaching D*=2.6:", np.array2string(A2_near, precision=2))
print("  => RIGHT wall at D* (carrier amplitude diverges). LEFT side OPEN.")

# CONFINEMENT VERDICT: U_phys(D) on (0,D*) is monotone rising + a right wall at D*.
Dg = np.linspace(0.005, Dstar_v-1e-3, 5000)
Uv = U_phys(Dg)
monotone = np.all(np.diff(Uv) > -1e-9)
print(f"\nU_phys(D) monotone-rising on (0,D*)? {monotone}")
print("=> HALF-WELL: bounded on the right (D*), OPEN on the left (D->0).")
print("=> a single boundary-bound depth state at most. NOT a multi-rung well.")

# QUANTIZATION ATTEMPT (postulate A): oint p_D dD = (n+1/2) hbar.
# For a bound depth tower we need TWO turning points D-(E), D+(E) with U(D)=E between.
# With a monotone-rising U + a hard right wall at D*, the "turning points" are the
# core boundary (D~0) and the wall (D*). This is an INFINITE-square-well-like problem
# in D, NOT a smooth confining U. Its levels are box-like: spacing set by the WIDTH
# (0, D*), i.e. by D* -- which is the TACHYON CAP, a fixed value, NOT hbar+backreaction
# producing a smooth ladder. Count how many levels fit.
# Effective 1D Schrodinger in D: -(hbar^2/2 m_D) d^2/dD^2 psi + U_phys(D) psi = E psi,
# hard walls at D=0 and D=D*. m_D = depth-mode kinetic mass (CHOSE unit; sets scale).
import numpy as np
hbar = 1.0; m_D = 1.0   # CHOSE units (postulate A hbar; m_D mode mass)
N = 2000
Dgrid = np.linspace(1e-3, Dstar_v, N+2)[1:-1]  # interior, hard walls at ends
h = Dgrid[1]-Dgrid[0]
Upot = U_phys(Dgrid)
# tridiagonal -hbar^2/2m d2/dD2 + U
main = hbar**2/(m_D*h**2) + Upot
off  = -hbar**2/(2*m_D*h**2)*np.ones(N-1)
import torch
dev = 'cuda' if torch.cuda.is_available() else 'cpu'
Tm = (torch.diag(torch.tensor(main)) + torch.diag(torch.tensor(off),1)
      + torch.diag(torch.tensor(off),-1)).to(torch.float64).to(dev)
ev = torch.linalg.eigvalsh(Tm).cpu().numpy()[:10]
# physical (standing-wave) depth levels need E within [U_min, U(D*)] = bound in the half-well
Umin = Upot.min(); Uwall = U_phys(Dstar_v)
bound = ev[(ev>Umin-1e-6)&(ev<Uwall)]
print(f"\nDepth-quantization (postulate A, hard walls 0..D*={Dstar_v}, m_D={m_D},hbar={hbar}):")
print("  lowest depth-levels E_n:", np.array2string(ev[:6], precision=4))
print(f"  U_min={Umin:.3f}  U(D*)={Uwall:.3f}  bound levels below the wall: {len(bound)}")
print("  *** these levels are BOX-LIKE: set by the WIDTH (0,D*)=tachyon cap + m_D,")
print("      NOT by a smooth native confining U. The 'spacing' is D*-controlled. ***")


# =============================================================================
# PART 7 — ANTI-BOX-CONTROL audit of the depth-levels + the mass ladder.
#   The Part-6 "10 levels" are suspicious: a hard-walled box of width D* gives
#   E_n ~ (hbar^2/2 m_D)(n pi/D*)^2 -- box-controlled (depends on D* and m_D).
#   TEST: vary D* (the cap) and m_D; do the level count / spacing track them?
#   If yes => BOX-CONTROLLED (the same trap, now in the depth direction).
#   Then: even if we ACCEPT the levels, is mass_n = cost(D_n) ~ e^{2 D_n} EXPONENTIAL?
#   D_n = the classical turning point / mean depth of level n.
# =============================================================================
print("\n" + "="*78)
print("PART 7 — anti-box-control audit + mass ladder")
print("="*78)

def count_depth_levels(Dstar, m_Dv, A0sq_v=5.0, Nn=1500):
    om2,Eg,Un,Up,cb = make_potential(c_grav_v, A0sq_v, floor_v, Dstar, kpow_v)
    Dg = np.linspace(1e-3, Dstar, Nn+2)[1:-1]; hh=Dg[1]-Dg[0]
    Up_v = Up(Dg)
    mn = hbar**2/(m_Dv*hh**2) + Up_v
    of = -hbar**2/(2*m_Dv*hh**2)*np.ones(Nn-1)
    Tm = (np.diag(mn)+np.diag(of,1)+np.diag(of,-1))
    e = np.linalg.eigvalsh(Tm)
    Uwall = Up(Dstar)
    return e[e<Uwall], e

print("\n(a) Does the depth-level COUNT/spacing track D* and m_D? (box-control test)")
print(f"{'D*':>6} {'m_D':>6} {'#levels<wall':>12} {'E_1':>9} {'E_2-E_1':>9}")
for Dstar in [2.0, 2.6, 3.2]:
    for m_Dv in [1.0, 4.0, 16.0]:
        b,e = count_depth_levels(Dstar, m_Dv)
        sp01 = e[1]-e[0]
        print(f"{Dstar:6.1f} {m_Dv:6.1f} {len(b):12d} {e[0]:9.3f} {sp01:9.4f}")

print("\n  READ: if #levels and spacing change with D* and m_D, the tower is BOX-LIKE")
print("  (width=D*=tachyon cap; m_D=chosen mode mass) -- NOT a smooth native U ladder.")

# (b) the mass ladder: mass_n = cost(D_n). Use D_n = mean depth of level n
# (classical turning point in the half-well). For the hard-wall box, level n peaks
# near D ~ (n+1) D*/(Nlevels+1) roughly; we take D_n = sqrt(<D^2>) proxy via the
# WKB turning point U(D_n)=E_n. mass_n = e^{2 D_n}-1 (B1 cost).
print("\n(b) mass ladder mass_n = cost(D_n) = e^{2 D_n}-1, D_n = WKB turning pt U(D_n)=E_n")
om2,Eg,Un,Up,cb = make_potential(c_grav_v, 5.0, floor_v, Dstar_v, kpow_v)
b,e = count_depth_levels(Dstar_v, 1.0)
Dscan = np.linspace(1e-3, Dstar_v, 20000)
Uscan = Up(Dscan)
Dn=[]
for En in e[:6]:
    idx = np.argmin(np.abs(Uscan-En))
    Dn.append(Dscan[idx])
Dn=np.array(Dn)
mass_n = np.exp(2*Dn)-1
print("  level n:    ", list(range(len(Dn))))
print("  D_n:        ", np.array2string(Dn, precision=3))
print("  mass_n:     ", np.array2string(mass_n, precision=3))
with np.errstate(divide='ignore'):
    ratios = mass_n[1:]/np.maximum(mass_n[:-1],1e-12)
print("  mass_n/m_{n-1}:", np.array2string(ratios, precision=3))
print("  *** D_n CAPPED at D* (all turning points <= D*=2.6); mass_n cannot exceed")
print("      cost(D*)=exp(2 D*)-1 = %.1f. The ladder TOPS OUT at the tachyon cap. ***"
      % (np.exp(2*Dstar_v)-1))

# =============================================================================
# PART 8 — CONSTRUCTION-ROBUSTNESS: is the "no smooth confining U" verdict an
# artifact of the frozen-amplitude (3b) choice? Test the alternative natural
# collective-coordinate constructions and confirm NONE confines into a smooth
# multi-rung well below D*.
#   (8a) ON-CONSTRAINT: U(D)=E_grav(D)=c_grav(e^{2D}-1). MONOTONE RISING. No well.
#   (8b) MINIMIZED-amplitude (BPS-like): at each D minimize E over A -> A=0 trivial
#        if omega^2>0 (carrier wants to vanish) -> U=E_grav, monotone. No well.
#   (8c) FIXED carrier energy E_c (a charge-fixed sector, A^2 omega^2 = const): then
#        E_grav(D) + E_c = monotone. No well.
#   (8d) FROZEN amplitude (Part 3b/5): half-well, monotone rising to D*. No interior min.
# In ALL natural constructions U(D) has NO interior minimum below D* -> NO smooth
# confining well -> the only "confinement" is the hard tachyon WALL at D* + the core
# boundary at D->0 = a BOX of width D*. Confirm:
# =============================================================================
print("\n" + "="*78)
print("PART 8 — construction-robustness of the no-smooth-well verdict")
print("="*78)
Dg = np.linspace(0.005, Dstar_v-1e-3, 3000)
constructions = {
  "8a on-constraint  U=E_grav":        E_grav_f(Dg),
  "8b min-amplitude  U=E_grav (A->0)": E_grav_f(Dg),
  "8c fixed-Ec       U=E_grav+Ec":     E_grav_f(Dg)+10.0,
  "8d frozen-A (3b)  U=E_grav+A0w2/2": U_phys(Dg),
}
for name,Uv in constructions.items():
    interior_min = np.any((Uv[1:-1]<Uv[:-2])&(Uv[1:-1]<Uv[2:]))
    mono = np.all(np.diff(Uv)>-1e-9)
    print(f"  {name:36s}: interior-min={interior_min}  monotone-rising={mono}")
print("\nVERDICT (construction-robust): NO native construction gives a smooth interior")
print("minimum below D*. U(D) rises monotonically; the ONLY confinement is the box")
print("[D->0 core, D*->tachyon wall]. The depth tower is therefore BOX-CONTROLLED")
print("(width=D*=tachyon cap), NOT a smooth-U hbar-quantized multi-rung native ladder.")

print("\n" + "="*78)
print("SUMMARY OF VERDICTS")
print("="*78)
print("""
1. U(D) NATIVE? YES -- assembled from B1 dilation cost (e^{2D}, native) + the native
   carrier frequency omega^2(D) (power-law, native). No imported potential.
2. Does U(D) CONFINE into a smooth well? NO. Construction-robust: U(D) is monotone
   RISING on (0,D*); the gravitational e^{2D} always out-pulls the BOUNDED carrier
   binding (floor->0 over a finite drop). HALF-WELL: right wall at D*, open left.
3. Quantize the depth: the only 'levels' are HARD-BOX levels of width D*=tachyon cap.
   Their count/spacing track D* and m_D (box-controlled, the SAME trap in the depth
   direction). NOT set by hbar acting on a smooth native U.
4. The mass ladder mass_n=cost(D_n): SUB-exponential (ratios DECREASE 2.4->1.3->1,
   not constant), and TOPS OUT at cost(D*) -- bounded, finite, capped. NOT a clean
   exponential scale-free multi-rung ladder.
OBSTRUCTION: the depth-selector does NOT close. The carrier binding that would form
the left wall of a confining depth-well is the SAME power-law omega^2(D) that hits
the tachyon cap D* -- so it cannot both (i) deepen enough to confine and (ii) keep
omega^2>0. The exponential gravitational cost has no native counter-term to make a
SMOOTH well; only the tachyon WALL bounds it, and that wall is the old D* box trap
relocated to the depth axis.
""")
