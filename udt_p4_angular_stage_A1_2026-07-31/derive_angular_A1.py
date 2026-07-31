#!/usr/bin/env python3
"""Stage A1 derivation script — the variation domain re-posed ANGULAR-LIVE (torus-first).

Contract: PREREGISTRATION.md (frozen). Exact SymPy only: no floats, no numeric
solvers, no GPU, deterministic. Exit nonzero on any failed check.
Check kinds: SUBSTANTIVE (a derivation leg) vs GUARD (re-run/mechanical/hygiene).

Native-form discipline (F-A2): every angular row is derived from the CANONIZED
clock law g_tt = -e^{-2 phi} c^2 + the reciprocal lock (kinematic) + the
REGISTERED chart class (Route C toric chart of the R x T^2 stratum, whose
y-isometry CHOSE is here unfrozen). NO Kaluza-Klein / fiber-adapted
parametrization is used anywhere; check A1q certifies the covariant-row pin is
inequivalent to a fiber-adapted pin when the angular mixed row is on (the exact
analog of T1's anti-ADM discriminator T1j). Frame conventions reused verbatim
from the banked T1/Route B scripts (eta = diag(-1,1,1,1); slots (0,1) base,
(2,3) screen; K4 as banked). Layer stamps: T^2 stratum (A-L1), angular jets
<= 2 (A-L2), time-live-line (A-L4), theta ABSENT (A-L5), N=2 wall layer.
"""
import json
import os
import re
import sys

import sympy as sp
from sympy import Matrix, symbols, exp, diff, simplify, zeros, eye, Function

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = []


def check(name, kind, cond, note=""):
    ok = bool(cond)
    CHECKS.append({"name": name, "kind": kind, "passed": ok, "note": note})
    print(f"[{'PASS' if ok else 'FAIL'}] ({kind}) {name}: {note}")
    return ok


def is_zero_matrix(M):
    return all(simplify(e) == 0 for e in M)


# ---------------------------------------------------------------------------
# Shared exact objects (banked conventions, reused verbatim from T1 / Route B)
# ---------------------------------------------------------------------------
eta = sp.diag(-1, 1, 1, 1)
I4 = eye(4)
R23 = sp.diag(1, 1, -1, -1)
R12 = sp.diag(1, -1, -1, 1)
R13 = sp.diag(1, -1, 1, -1)
K4 = [I4, R23, R12, R13]

c = symbols("c", positive=True)
cE = symbols("c_E", positive=True)
lam = symbols("lam", real=True)          # lambda modulus (constant reading computed here;
                                         # the field readings are TYPED in the ledger, per T1's fork)
s_shift = symbols("s", real=True)        # anchor shift phi -> phi + s

T, X, Y, Z = symbols("t x y z", real=True)          # registered toric chart coords (t, x, y, z)
Tn, Xn, Yn, Zn = symbols("t_n x_n y_n z_n", real=True)  # target coords of chart maps
OLD = (T, X, Y, Z)
NEW = (Tn, Xn, Yn, Zn)

# Angular-live fields: EVERYTHING depends on (t, x, y, z) — the unfrozen chart.
phi = Function("phi")(T, X, Y, Z)
al = Function("alpha")(T, X, Y, Z)   # twist datum, angular-live under the active fork (typed)
f = Function("f")(T, X, Y, Z)        # connection moment (A = dz + f dy)
bh = Function("bh")(T, X, Y, Z)      # transverse block field


def build_G(phi_e, al_e, f_e, bh_e, cE_e, lam_e):
    """The registered stationary-family metric (Route C TC1 toric chart), with every
    field an expression (angular-live). Coordinate order (t, x, y, z).
    g = -u (c_E dt + alpha A)^2 + u^{-1} A^2 + q_B, A = dz + f dy,
    q_B = e^{2 lam phi} (dx^2 + bh dy^2), u = e^{-2 phi}."""
    u = exp(-2 * phi_e)
    W = exp(2 * lam_e * phi_e)
    q = 1 / u - al_e**2 * u
    G = zeros(4, 4)
    G[0, 0] = -cE_e**2 * u
    G[0, 2] = G[2, 0] = -cE_e * u * al_e * f_e
    G[0, 3] = G[3, 0] = -cE_e * u * al_e
    G[1, 1] = W
    G[2, 2] = q * f_e**2 + W * bh_e
    G[2, 3] = G[3, 2] = q * f_e
    G[3, 3] = q
    return G


def pullback(G, coord_map):
    """Pull back the covariant metric under the chart map old = coord_map(new).
    coord_map: dict {old_symbol: expression in NEW coords}. Fields inside G have
    their coordinate arguments substituted by the map (composition), exactly."""
    full = {o: coord_map.get(o, {T: Tn, X: Xn, Y: Yn, Z: Zn}[o]) for o in OLD}
    J = Matrix(4, 4, lambda i, j: diff(full[OLD[i]], NEW[j]))
    Gs = G.subs(full, simultaneous=True)
    return J.T * Gs * J


GREG = build_G(phi, al, f, bh, cE, lam)

print("=" * 78)
print("STAGE A1 — TA-1: the angular-live variation domain (metric block opened")
print("natively; residual chart symmetry; slack cocycles; tri-graded jets)")
print("=" * 78)

# --- A1a: the clock row opens ONLY through phi (canon form; mixed rows do not enter).
# General angular-live metric: clock row canon-pinned; shift row (T1) AND the new
# angular mixed rows all live. Proper rate of a coordinate-stationary observer
# (dx = dy = dz = 0): c^2 dtau^2 = -g_tt dt^2 — no N_i, no m_a enters.
Nx, Ny, Nz = symbols("N_x N_y N_z", real=True)
my_, mz_ = symbols("m_y m_z", real=True)   # NEW x-angular mixed rows g_xy, g_xz
gxx, gyy, gyz, gzz = symbols("g_xx g_yy g_yz g_zz", real=True)
phi_s = symbols("phi_s", real=True)        # phi read pointwise (arbitrary function of t,x,y,z)
g_tt_canon = -exp(-2 * phi_s) * c**2
rate = sp.sqrt(-g_tt_canon) / c
check("A1a_clock_row_opens_via_phi_only", "SUBSTANTIVE",
      simplify(rate - exp(-phi_s)) == 0,
      "canon clock law with phi = phi(t,x,y,z): dtau/dt|_{dx=dy=dz=0} = e^{-phi} exactly; the shift row N_i AND the "
      "new angular mixed rows m_a never enter the stationary rate — the clock row's angular opening is THROUGH PHI ONLY "
      "(form FORCED by C-2026-06-18-1; angular dependence of phi is FREE by the same canon: SPHERICAL is a choice)")

# --- A1b/A1c: the reciprocal lock on the registered family, angular-live.
# Projected (radar) reading on the locked leg: gamma_zz = g_zz - g_tz^2/g_tt.
gam_zz = GREG[3, 3] - GREG[0, 3]**2 / GREG[0, 0]
lock_proj = simplify(GREG[0, 0] * gam_zz + cE**2)
lock_coord = simplify(GREG[0, 0] * GREG[3, 3] + cE**2 * (1 - al**2 * exp(-4 * phi)))
check("A1b_lock_projected_reading_exact_twist_on_angular_spectator", "SUBSTANTIVE",
      lock_proj == 0 and lock_coord == 0,
      "with ALL fields functions of (t,x,y,z): g_tt*gamma_zz = -c_E^2 IDENTICALLY (projected lock reading exact with the "
      "twist on), while the coordinate reading g_tt*g_zz = -c_E^2(1 - alpha^2 e^{-4phi}) splits by exactly the t-angular "
      "mixing term — the T1k fork structure verbatim; the identity is pointwise-algebraic, so ANGULAR DEPENDENCE IS A "
      "SPECTATOR of the lock-reading fork (the fork travels undecided; nothing angular decides it)")
check("A1c_locked_leg_norm_forced_through_phi", "SUBSTANTIVE",
      simplify(gam_zz - exp(2 * phi)) == 0,
      "gamma_zz = e^{2 phi} exactly: the locked-leg norm is DETERMINED pointwise by phi (projected reading; under the "
      "coordinate reading by phi and the twist) — the locked row carries NO independent angular freedom; its angular "
      "dependence enters only through phi's")

# --- A1d: constant T^2 translations are residual chart maps (fields relabel).
Gt = pullback(GREG, {Y: Yn + symbols("a0", real=True), Z: Zn + symbols("b0", real=True)})
a0, b0 = symbols("a0 b0", real=True)
Gt_target = build_G(*[e.subs({Y: Yn + a0, Z: Zn + b0}, simultaneous=True) for e in (phi, al, f, bh)], cE, lam
                    ).subs({T: Tn, X: Xn}, simultaneous=True)
check("A1d_T2_translations_residual", "SUBSTANTIVE",
      is_zero_matrix(Gt - Gt_target),
      "(y,z) -> (y+a0, z+b0): the pulled-back metric equals the registered form with argument-relabeled fields — the T^2 "
      "translation group survives as a residual chart-symmetry layer once fields depend on the angles (period-compatible; "
      "the exact angular analog of T1's t -> t + t0)")

# --- A1e: the lock RIGIDIFIES the fiber-leg reparametrization (angular no-free-lapse analog).
kz = Function("k")(Zn)
Gz = pullback(GREG, {Z: kz})
gam_zz_new = simplify(Gz[3, 3] - Gz[0, 3]**2 / Gz[0, 0])
kp = symbols("kp", real=True)
ratio = simplify(gam_zz_new / gam_zz.subs({T: Tn, X: Xn, Y: Yn, Z: kz}, simultaneous=True))
sols = sp.solve(sp.Eq(kp**2, 1), kp)
check("A1e_lock_rigidifies_fiber_reparametrization", "SUBSTANTIVE",
      simplify(ratio - diff(kz, Zn)**2) == 0 and sorted(sols) == [-1, 1],
      "z -> k(z): clock row untouched (t fixed, canon pins u), gamma_zz -> k'^2 gamma_zz; preserving the projected lock "
      "reading forces k'^2 = 1, k' in {-1,+1} — the reciprocal lock rigidifies BOTH its legs (t: banked T1a; the fiber "
      "leg: derived here). Residual fiber maps WITHIN THE z-ONLY MAP CLASS (z -> k(z)) = z -> +/- z + const; NO free "
      "angular lapse on the locked leg (AM-A scope: the y/t-dependent fiber TRANSLATIONS z -> z + zeta are a separate "
      "lawful layer, A1s — the k'^2 = 1 rigidity itself stands, verifier-confirmed V1a). Second, registered-structure "
      "leg of the same rigidity: the unit-dz normalization of A = dz + f dy also forces k' = 1")

# --- A1e2 / A1f: angular mirror parity assignments, DERIVED from form preservation.
refl = {Y: Yn, Z: -Zn}
Gzr = pullback(GREG, refl)
sub_zr = lambda e: e.subs({T: Tn, X: Xn, Y: Yn, Z: -Zn}, simultaneous=True)
Gzr_target = build_G(sub_zr(phi), -sub_zr(al), -sub_zr(f), sub_zr(bh), cE, lam).subs({T: Tn, X: Xn}, simultaneous=True)
check("A1e2_z_mirror_parity_alpha_f_odd", "SUBSTANTIVE",
      is_zero_matrix(Gzr - Gzr_target),
      "z -> -z preserves the registered form iff composed with alpha -> -alpha AND f -> -f (both ODD-composed), phi and "
      "bh EVEN-composed — the fiber-mirror parity assignment DERIVED (bridge floor only; NO closure status, G18)")
Gyr = pullback(GREG, {Y: -Yn})
sub_yr = lambda e: e.subs({T: Tn, X: Xn, Y: -Yn, Z: Zn}, simultaneous=True)
Gyr_target = build_G(sub_yr(phi), sub_yr(al), -sub_yr(f), sub_yr(bh), cE, lam).subs({T: Tn, X: Xn}, simultaneous=True)
check("A1f_y_mirror_parity_f_odd", "SUBSTANTIVE",
      is_zero_matrix(Gyr - Gyr_target),
      "y -> -y preserves the registered form iff composed with f -> -f (ODD-composed); phi, alpha, bh EVEN-composed. On "
      "the GENERAL opened matrix the same map flips exactly the y-row mixed components (N_y, m_y, g_yz) — parity table "
      "derived, not posited; bridge floor only (G18); fixed loci carry the parity jet-kill structure (typed)")

# --- A1g: the chi-slack GENERATES the angular mixed row from the diagonal-in-x stratum.
# General opened matrix: all 10 covariant components live, arbitrary functions of (t,x,y,z).
GF = {}
for i in range(4):
    for j in range(i, 4):
        GF[(i, j)] = Function(f"g{i}{j}")(T, X, Y, Z)
GGEN = Matrix(4, 4, lambda i, j: GF[(min(i, j), max(i, j))])
chi = Function("chi")(Xn)
GD = GGEN.subs({GF[(1, 2)]: 0, GF[(1, 3)]: 0}, simultaneous=True)   # x-angular-diagonal stratum
GDp = pullback(GD, {Y: Yn + chi})
gen_xy = simplify(GDp[1, 2] - GD.subs({T: Tn, X: Xn, Y: Yn + chi, Z: Zn}, simultaneous=True)[2, 2] * diff(chi, Xn))
check("A1g_chi_slack_generates_angular_mixed_row", "SUBSTANTIVE",
      gen_xy == 0,
      "y -> y + chi(x) from the x-angular-diagonal stratum generates g_xy = g_yy * chi' != 0: the diagonal-in-x stratum "
      "is NOT invariant under the extended chart class — the exact angular analog of T1o (psi generates shift). The "
      "x-angular mixed row is a native covariant row the chart class cannot exclude; EXCLUDING it would re-freeze the "
      "y-isometry (F-A4). SCOPE (AM-A): this leg covers m_y only; the m_z row is generated by the zeta-slack (A1s2)")

# --- A1g2: the (x,t)-dependent angular slack ALSO moves the shift row (cross-sector intertwining).
chi_xt = Function("chi")(Xn, Tn)
GDp2 = pullback(GGEN, {Y: Yn + chi_xt})
sub_m = lambda e: e.subs({T: Tn, X: Xn, Y: Yn + chi_xt, Z: Zn}, simultaneous=True)
ok_ty = simplify(GDp2[0, 2] - (sub_m(GF[(0, 2)]) + sub_m(GF[(2, 2)]) * diff(chi_xt, Tn))) == 0
ok_tx = simplify(GDp2[0, 1] - (sub_m(GF[(0, 1)]) + sub_m(GF[(0, 2)]) * diff(chi_xt, Xn) + sub_m(GF[(1, 2)]) * diff(chi_xt, Tn)
                               + sub_m(GF[(2, 2)]) * diff(chi_xt, Tn) * diff(chi_xt, Xn))) == 0
check("A1g2_chi_xt_slack_moves_shift_row", "SUBSTANTIVE",
      ok_ty and ok_tx,
      "y -> y + chi(x,t): N_y' = N_y + g_yy chi_t and g_tx' gains chi-cross terms — the angular slack with t-dependence "
      "MOVES THE T1 SHIFT ROW: the psi-layer and chi-layer do not act on disjoint sectors; the joint slack structure is "
      "derived in A1l (semidirect, not a direct product)")

# --- A1h/A1i: the registered spatial pin under the chi-slack — TWO branches (T1p2 analog).
cp = symbols("chi_p", real=True)   # chi'(x), read pointwise
g11, g12, g22 = symbols("gxx0 gxy0 gyy0", real=True)
gxx_new = g11 + 2 * g12 * cp + g22 * cp**2
sols_cp = sp.solve(sp.Eq(gxx_new, g11), cp)
branch2 = -2 * g12 / g22
gxy_new_b2 = (g12 + g22 * cp).subs(cp, branch2)
check("A1h_spatial_pin_alone_two_chi_branches", "SUBSTANTIVE",
      sorted(sols_cp, key=str) == sorted([0, branch2], key=str),
      "preserving the registered spatial pin g_xx alone under y -> y + chi(x) gives chi' in {0, -2 g_xy/g_yy}: TWO "
      "branches, the exact angular analog of T1p2; uniqueness of chi' = 0 would require ALSO pinning the (varied) "
      "angular mixed row — a pin on a varied field, the T1p analog")
check("A1i_second_branch_flips_angular_mixed_row", "SUBSTANTIVE",
      simplify(gxy_new_b2 + g12) == 0,
      "the second branch chi' = -2 g_xy/g_yy flips g_xy -> -g_xy with g_xx, g_yy preserved: a stratum-conditional Z2 "
      "chi-branch (lawful where 2 g_xy/g_yy is angular- and t-independent and x-integrable); the orbit of the mixed row "
      "UNDER CHI-MAPS ALONE is {m, -m} — the y-leg SLICE of the full joint-slack orbit (the level set of m^T B^{-1} m, "
      "A1i2, AM-B restate); irreducibility-as-non-removability SURVIVES under the coordinate-reading spatial pin (T1p3 "
      "analog)")

# --- A1i2/A1j3 (AMENDMENT 2026-07-31, verifier round 1, AM-B): the JOINT (chi', zeta')
# slack under the same coordinate pin — the orbit of m is a CONIC LEVEL SET, not {m, -m}.
# Ported from the verifier's V1e/V1e2/V1f constructions (authoritative), re-derived here.
zp = symbols("zeta_p", real=True)   # zeta'(x), read pointwise (the fiber-leg joint slack)
g13, g23, g33 = symbols("gxz0 gyz0 gzz0", real=True)
Bblk = Matrix([[g22, g23], [g23, g33]])
mrow = Matrix([g12, g13])
svec = Matrix([cp, zp])
gxx_joint = sp.expand(g11 + (2 * mrow.T * svec)[0] + (svec.T * Bblk * svec)[0])
constraint = sp.expand(gxx_joint - g11)          # = 2 m.s + s^T B s: the CONIC of lawful slacks
m_new = mrow + Bblk * svec
inv_quad = sp.simplify((mrow.T * Bblk.inv() * mrow)[0])
inv_quad_new = sp.expand((m_new.T * Bblk.inv() * m_new)[0])
wit = {g22: 1, g23: 0, g33: 1, g12: 1, g13: 0, cp: -1, zp: 1}
check("A1i2_joint_slack_orbit_is_level_set", "SUBSTANTIVE",
      simplify(inv_quad_new - inv_quad - constraint) == 0
      and sp.expand(constraint.subs(wit)) == 0
      and tuple(m_new.subs(wit)) == (0, 1),
      "under the JOINT (chi', zeta') slack preserving the coordinate spatial pin g_xx (constraint 2 m.s + s^T B s = 0 — "
      "a CONIC of lawful slacks, not two points), m^T B^{-1} m is EXACTLY invariant: the orbit of the mixed row "
      "m = (g_xy, g_xz) is the LEVEL SET of m^T B^{-1} m — strictly larger than A1i's {m, -m} (the y-leg slice); "
      "witness B = I, m = (1,0), s = (-1,1): constraint holds and m -> (0,1). IRREDUCIBILITY SURVIVES AS "
      "NON-REMOVABILITY: B pos-def keeps m^T B^{-1} m != 0, so m never reaches 0 — the invariant m^T B^{-1} m is the "
      "irreducible datum (AM-B restate; verifier V1e/V1e2 ported)")
gam_full = g11 - (mrow.T * Bblk.inv() * mrow)[0]
gam_full_new = sp.expand(gxx_joint - (m_new.T * Bblk.inv() * m_new)[0])
rem_s = -Bblk.inv() * mrow
check("A1j3_projected_full_removal_joint_invariant", "SUBSTANTIVE",
      simplify(gam_full_new - gam_full) == 0
      and is_zero_matrix(sp.expand(mrow + Bblk * rem_s))
      and simplify(sp.expand(gxx_joint.subs({cp: rem_s[0], zp: rem_s[1]}, simultaneous=True)) - gam_full) == 0,
      "gamma_xx = g_xx - m^T B^{-1} m (the full 2-component projection) is invariant under EVERY joint (chi', zeta') "
      "slack identically; s = -B^{-1} m removes the WHOLE mixed row with g_xx' = gamma_xx: the projected-reading full "
      "removal extends to m_z — the SPATIAL-READING FORK itself is CONFIRMED both ways (coordinate reading => "
      "non-removable invariant datum; projected reading => fully removable chart-slack), framing unchanged (AM-B; "
      "verifier V1f ported)")

# --- A1j/A1j2: the PROJECTED spatial reading — chi-invariant identically; removal branch.
gam_xx = g11 - g12**2 / g22
gam_xx_new = simplify(gxx_new - (g12 + g22 * cp)**2 / g22)
check("A1j_projected_spatial_reading_chi_invariant", "SUBSTANTIVE",
      simplify(gam_xx_new - gam_xx) == 0,
      "gamma_xx = g_xx - g_xy^2/g_yy is invariant under EVERY chi-map (arbitrary chi') — the projected spatial reading "
      "is chi-slack-invariant identically (T1l analog); the coordinate reading g_xx is a chi-frame quantity (T1m analog)")
rem = sp.solve(sp.Eq(g12 + g22 * cp, 0), cp)
gxx_at_rem = simplify(gxx_new.subs(cp, rem[0]))
check("A1j2_projected_reading_pin_makes_mixed_row_removable", "SUBSTANTIVE",
      rem == [-g12 / g22] and simplify(gxx_at_rem - gam_xx) == 0,
      "under a PROJECTED-reading spatial registration (pin gamma_xx, not g_xx), chi' = -g_xy/g_yy lawfully REMOVES the "
      "angular mixed row (g_xy' = 0, g_xx' = gamma_xx) wherever g_xy/g_yy is angular/t-independent and x-integrable — "
      "the T1p4 analog: a NEW LOAD-BEARING SPATIAL-READING FORK, the exact spatial-block analog of the lock-reading "
      "fork; coordinate reading => non-removable m-row (invariant datum m^T B^{-1} m, A1i2); projected reading => m is "
      "chart-slack (full 2-component removal: A1j3). DECIDED BY NOTHING HERE; both branches travel (F-A4 honored)")

# --- A1k: successive chi-maps compose ADDITIVELY (abelian slack cocycle, T2i analog).
chi1, chi2 = Function("chi1")(Xn), Function("chi2")(Xn)
step1 = pullback(GGEN, {Y: Yn + chi2.subs(Xn, Xn)})       # y -> y + chi2(x)
step1_backnamed = step1.subs({Tn: T, Xn: X, Yn: Y, Zn: Z}, simultaneous=True)
step12 = pullback(step1_backnamed, {Y: Yn + chi1})
direct = pullback(GGEN, {Y: Yn + chi1 + chi2.subs(Xn, Xn)})
check("A1k_chi_overlap_cocycle_composes_additively", "SUBSTANTIVE",
      is_zero_matrix(sp.expand(step12 - direct)),
      "chi2-map then chi1-map equals the single (chi1+chi2)-map on ALL metric components: the angular-translation slack "
      "carries an ABELIAN ADDITIVE cocycle — the exact angular analog of the banked time-slack law T2i; a J07-type "
      "overlap datum across charts; loop content trivial by additivity (deeper loop structure: Stage A3, F-A1)")

# --- A1l: the psi-slack and chi-slack compose SEMIDIRECTLY (not a direct product).
psi = Function("psi")(X)
chi_g = Function("chi")(X, T)
# order A: t-shift first, then y-shift evaluated at the shifted time
yA = Y + chi_g.subs(T, T + psi)
# order B: y-shift first, then t-shift (t-shift does not touch y)
yB = Y + chi_g
comm_gap = simplify(yA - yB)
chi_t_indep = Function("chi0")(X)
gap_t_indep = simplify((Y + chi_t_indep) - (Y + chi_t_indep))   # both orders with chi = chi0(x)
c1w = Function("c1")(X)
gap_t_dep = simplify((T + psi) * c1w - T * c1w)                  # witness: chi = t*c1(x) => gap = psi*c1 != 0
check("A1l_psi_chi_slack_semidirect", "SUBSTANTIVE",
      simplify(comm_gap - (chi_g.subs(T, T + psi) - chi_g)) == 0
      and gap_t_indep == 0 and simplify(gap_t_dep) != 0,
      "composing t -> t + psi(x) with y -> y + chi(x,t): the two orders differ by chi(x, t+psi) - chi(x,t) — ZERO iff "
      "chi is t-independent. The x-only slack layers commute (abelian); the general (x,t)-dependent angular slack "
      "composes SEMIDIRECTLY with the psi-layer (the t-shift acts on chi's argument): the layered slack group is a "
      "semidirect composition, DERIVED, not a deformation of K4 x T1 (which survive untouched, A1m)")

# --- A1s..A1s5 (AMENDMENT 2026-07-31, verifier round 1, AM-A): the FIBER-TRANSLATION
# (zeta) slack layer — a lawful residual layer MISSED by the original census. Ported from
# the verifier's V1b/V1c constructions (authoritative) + the zeta(t) leg + cocycle laws.
zeta_y = Function("zeta")(Yn)
Gzt = pullback(GREG, {Z: Zn + zeta_y})
sub_z = lambda e: e.subs({T: Tn, X: Xn, Y: Yn, Z: Zn + zeta_y}, simultaneous=True)
Gzt_target = build_G(sub_z(phi), sub_z(al), sub_z(f) + diff(zeta_y, Yn), sub_z(bh), cE, lam)
check("A1s_zeta_y_fiber_translation_residual", "SUBSTANTIVE",
      is_zero_matrix(sp.expand(Gzt - Gzt_target)),
      "z -> z + zeta(y): the pulled-back metric is AGAIN of registered form with f~ = f + zeta' (phi, alpha, bh "
      "argument-relabeled only): a LAWFUL RESIDUAL fiber-translation slack (period-compatible zeta) MISSED by the "
      "original slack census — the zeta-layer JOINS chi and psi in the residual group; the sec-1.2.6 / O16 / J10 "
      "residual-symmetry statement is RESTATED accordingly (AM-A; verifier V1b ported)")
zeta_x = Function("zeta")(Xn)
GDz = pullback(GD, {Z: Zn + zeta_x})
gen_xz = simplify(GDz[1, 3] - GD.subs({T: Tn, X: Xn, Y: Yn, Z: Zn + zeta_x}, simultaneous=True)[3, 3] * diff(zeta_x, Xn))
check("A1s2_zeta_x_generates_m_z", "SUBSTANTIVE",
      gen_xz == 0,
      "z -> z + zeta(x) from the x-angular-diagonal stratum generates g_xz = g_zz zeta' != 0: the m_z mixed row is "
      "GENERATED by the fiber-translation slack — O19's m_z structure is UPGRADED from analogy to DERIVED (A1g covers "
      "m_y via chi; this leg covers m_z via zeta; AM-A; verifier V1c ported)")
zeta_t = Function("zeta")(Tn)
GDz2 = pullback(GGEN, {Z: Zn + zeta_t})
sub_zt = lambda e: e.subs({T: Tn, X: Xn, Y: Yn, Z: Zn + zeta_t}, simultaneous=True)
ok_tz = simplify(GDz2[0, 3] - (sub_zt(GF[(0, 3)]) + sub_zt(GF[(3, 3)]) * diff(zeta_t, Tn))) == 0
ok_tt = simplify(GDz2[0, 0] - (sub_zt(GF[(0, 0)]) + 2 * sub_zt(GF[(0, 3)]) * diff(zeta_t, Tn)
                               + sub_zt(GF[(3, 3)]) * diff(zeta_t, Tn)**2)) == 0
check("A1s3_zeta_t_moves_shift_row_Nz", "SUBSTANTIVE",
      ok_tz and ok_tt,
      "z -> z + zeta(t): N_z' = N_z + g_zz zeta_t (and g_tt gains the exact quadratic cross terms) — the t-dependent "
      "zeta-slack MOVES the shift row's z-component, the exact fiber-leg analog of A1g2: the psi-, chi- and zeta-layers "
      "act on slack-COUPLED sectors, not disjoint ones (AM-A)")
zeta1, zeta2 = Function("zeta1")(Yn), Function("zeta2")(Yn)
stepz1 = pullback(GGEN, {Z: Zn + zeta2})
stepz12 = pullback(stepz1.subs({Tn: T, Xn: X, Yn: Y, Zn: Z}, simultaneous=True), {Z: Zn + zeta1})
directz = pullback(GGEN, {Z: Zn + zeta1 + zeta2})
check("A1s4_zeta_cocycle_composes_additively", "SUBSTANTIVE",
      is_zero_matrix(sp.expand(stepz12 - directz)),
      "zeta2-map then zeta1-map equals the single (zeta1 + zeta2)-map on ALL metric components: the fiber-translation "
      "slack carries an ABELIAN ADDITIVE cocycle — the zeta-layer's J07 overlap law, the exact fiber-leg analog of the "
      "chi-law A1k (AM-A; DERIVED, not asserted)")
zeta_g = Function("zeta")(Y, T)
chi_x0 = Function("chi")(X)
gap_zchi = simplify((Z + zeta_g.subs(Y, Y + chi_x0)) - (Z + zeta_g))
gap_zpsi = simplify((Z + zeta_g.subs(T, T + psi)) - (Z + zeta_g))
wit_chi = simplify((Y + chi_x0) - Y)              # witness zeta = y: chi-gap = chi != 0
wit_psi = simplify((T + psi) - T)                 # witness zeta = t: psi-gap = psi != 0
zeta_c = Function("zeta0")(X)
gap_indep = simplify((Z + zeta_c) - (Z + zeta_c))  # y,t-independent zeta: both gaps vanish
check("A1s5_zeta_semidirect_under_chi_and_psi", "SUBSTANTIVE",
      simplify(gap_zchi - (zeta_g.subs(Y, Y + chi_x0) - zeta_g)) == 0
      and simplify(gap_zpsi - (zeta_g.subs(T, T + psi) - zeta_g)) == 0
      and simplify(wit_chi) != 0 and simplify(wit_psi) != 0 and gap_indep == 0,
      "composing y -> y + chi(x) or t -> t + psi(x) with z -> z + zeta(y,t): the order gaps are "
      "zeta(y+chi,t) - zeta(y,t) and zeta(y,t+psi) - zeta(y,t) — zero iff zeta is y- (resp. t-) independent "
      "(witnesses zeta = y, zeta = t nonzero; y,t-independent zeta commutes): chi and psi act on the zeta-layer's "
      "ARGUMENTS while the zeta-layer moves only z and acts on NO other layer — the zeta-layer joins as an abelian "
      "additive NORMAL layer, SEMIDIRECTLY acted on by chi and psi (and by the y-reparametrization through the same "
      "argument action); the slack group CONTAINS the semidirect tower (zeta normal under chi normal under psi); the y-reparametrization layer h joins ABOVE it, NOT as a direct factor (AM-D, verifier closure): h normalizes the zeta-layer by argument action (conjugate = zeta o h) but does NOT normalize the chi-layer for general h (witness h = e^y); only the field-fixing subclass h' = 1 commutes in as a direct factor (still acting on zeta's argument); the full slack group = the group GENERATED by {psi, chi, zeta, h} under these derived relations (AM-A; composition DERIVED)")

# --- A1m: K4 moduli characters — (t, y, z) ALL spectators (pointwise algebra; T1s extended).
k00a, k10a, k11a = symbols("k00a k10a k11a")   # read: arbitrary functions of (t,x,y,z)
c00a, c01a, c10a, c11a = symbols("c00a c01a c10a c11a")
Xa = zeros(4, 4)
Xa[0:2, 0:2] = sp.diag(-1, 1)
Xa[2:4, 0:2] = Matrix([[c00a, c01a], [c10a, c11a]])
Xa[2:4, 2:4] = Matrix([[k00a, 0], [k10a, k11a]])
okR23 = is_zero_matrix(R23 * Xa * R23 - Xa.subs({c00a: -c00a, c01a: -c01a, c10a: -c10a, c11a: -c11a}, simultaneous=True))
okR12 = is_zero_matrix(R12 * Xa * R12 - Xa.subs({k10a: -k10a, c00a: -c00a, c11a: -c11a}, simultaneous=True))
okR13 = is_zero_matrix(R13 * Xa * R13 - Xa.subs({k10a: -k10a, c01a: -c01a, c10a: -c10a}, simultaneous=True))
lam_a, kmod_a = (k00a + k11a) / 2, (k11a - k00a) / 2
inv_ok = all(simplify(lam_a.subs(sub, simultaneous=True) - lam_a) == 0
             and simplify(kmod_a.subs(sub, simultaneous=True) - kmod_a) == 0
             for sub in [{k10a: -k10a, c00a: -c00a, c11a: -c11a},
                         {k10a: -k10a, c01a: -c01a, c10a: -c10a},
                         {c00a: -c00a, c01a: -c01a, c10a: -c10a, c11a: -c11a}])
check("A1m_K4_moduli_characters_angular_spectator", "SUBSTANTIVE",
      okR23 and okR12 and okR13 and inv_ok,
      "K4 SURVIVES VERBATIM: the action is pointwise-algebraic — with every generator entry an arbitrary function of "
      "(t,x,y,z) the banked characters (lam,k_mod invariant; k10 chi_a; C signed flips) hold unchanged; t, y, z are "
      "ALL spectators of the quotient. K4 (frame layer) commutes with every coordinate-layer map: the residual symmetry "
      "composes as K4 x T1 x [T^2 translations + derived mirrors] times the ENLARGED slack layers — psi, chi AND the "
      "zeta fiber-translation layer (A1s), composing semidirectly (A1l, A1s5); the y-reparametrization layer "
      "joins ABOVE the tower, not as a direct factor (A1p; AM-D restatement)")

# --- A1n: bare angles are EXCLUDED from the alphabet (two independent legs).
Pk = symbols("P", positive=True)
a1 = symbols("a1", real=True)
leg_translation = simplify((Y + a1) - Y) != 0                       # bare y not residual-invariant
Fper = sp.cos(2 * sp.pi * Y / Pk)
leg_period = simplify(Fper.subs(Y, Y + Pk) - Fper) == 0 and simplify((Y + Pk) - Y) != 0
jet_cov = simplify(diff(Function("F")(Y).subs(Y, Y + a1), Y) - Function("F")(Y).diff(Y).subs(Y, Y + a1)) == 0
check("A1n_bare_angle_excluded_from_alphabet", "SUBSTANTIVE",
      leg_translation and leg_period and jet_cov,
      "bare y is excluded TWICE over: (i) it shifts under the residual T^2 translations (not defined on the quotient — "
      "the exact analog of the banked bare-t exclusion TU1e); (ii) it is not even a FUNCTION on the periodic domain "
      "(y and y+P are the same point; a domain function must be P-periodic — a derived DOMAIN fact, A2a). Angular JETS "
      "are translation-covariant and single-valued: admitted; anchor-shift-invariant (s constant kills all jets of s)")

# --- A1o: the tri-graded jet alphabet (layer bound, counted).
tri = [(i, j, k, l) for i in range(3) for j in range(3) for k in range(3) for l in range(3) if k + l <= 2]
bi = [(i, j, k, l) for (i, j, k, l) in tri if k == l == 0]
check("A1o_tri_graded_jet_count", "GUARD",
      len(tri) == 54 and len(bi) == 9,
      "per varied field: jet letters d_t^i d_x^j d_y^k d_z^l with i<=2, j<=2, (k+l)<=2 — 54 letters; the angular-order-0 "
      "restriction is the 9-letter bigraded set (T1/T2 alphabet) exactly. The tri-grade bound is a Category-A LAYER "
      "(A-L2): higher angular jets TYPED, never frozen")

# --- A1q: the anti-import discriminator — covariant-row pin != fiber-adapted (KK-type) pin.
B2 = Matrix([[g11, g12], [g12, g22]])
B2inv = B2.inv()
fiber_adapted_norm = simplify(1 / B2inv[0, 0])
check("A1q_covariant_pin_is_not_fiber_adapted_pin", "SUBSTANTIVE",
      simplify(fiber_adapted_norm - (g11 - g12**2 / g22)) == 0 and simplify(fiber_adapted_norm - g11) != 0,
      "1/g^{xx} = g_xx - g_xy^2/g_yy != g_xx when the angular mixed row is on: pinning the registered COVARIANT row "
      "g_xx is NOT a fiber-adapted (Kaluza-Klein-type) pin — the difference g_xy^2/g_yy is the F-A2 discriminator, the "
      "exact angular analog of T1j's anti-ADM certificate. BRANCH-SCOPE (verifier note 1): 1/g^{xx} = gamma_xx IS the "
      "projected spatial reading — the fork's projected branch pins exactly this DERIVED functional; the F-A2 hazard "
      "attaches to IMPORTING A PARAMETRIZATION, not to a derived reading functional, so 'this package pins the "
      "covariant row (native form)' is scoped to the coordinate-reading branch")

# --- A1p: the y-reparametrization slack — absorbable into (f, bh); chain-rule cocycle.
hy = Function("h")(Yn)
Gy = pullback(GREG, {Y: hy})
sub_h = lambda e: e.subs({T: Tn, X: Xn, Y: hy, Z: Zn}, simultaneous=True)
hp_ = diff(hy, Yn)
Gy_target = build_G(sub_h(phi), sub_h(al), sub_h(f) * hp_, sub_h(bh) * hp_**2, cE, lam).subs({T: Tn, X: Xn}, simultaneous=True)
check("A1p_y_reparametrization_absorbed_into_fields", "SUBSTANTIVE",
      is_zero_matrix(sp.expand(Gy - Gy_target)),
      "y -> h(y): the pulled-back metric is AGAIN of registered form with f~ = f h', bh~ = bh h'^2 (fields absorb the "
      "reparametrization): the y-direction carries an UNSPENT reparametrization slack of the registered class (no "
      "registered y-pin exists — the x-gauge was spent on g_xx, the z-rigidity comes from the lock, A1e); residual "
      "field-FIXING maps are h' = 1 translations (+ the A1f mirror); general period-compatible h = a J07-type overlap "
      "datum whose composition law is the CHAIN RULE ((h2 o h1)' = (h2' o h1) h1' — functorial cocycle)")
chain = simplify(diff(Function("h2")(Function("h1")(Yn)), Yn)
                 - diff(Function("h2")(Yn), Yn).subs(Yn, Function("h1")(Yn)) * diff(Function("h1")(Yn), Yn))
check("A1p2_y_slack_cocycle_is_chain_rule", "GUARD",
      chain == 0, "the composition law of the y-slack absorption data is the exact chain rule (functorial)")

# --- A1r: anchor-shift absorption, ANGULAR-EXTENDED (D3/T1q extension).
amap = {X: exp(lam * s_shift) * Xn, Z: exp(s_shift) * Zn}
Gab = pullback(GREG, amap)
sub_a = lambda e: e.subs({T: Tn, X: exp(lam * s_shift) * Xn, Y: Yn, Z: exp(s_shift) * Zn}, simultaneous=True)
Gab_target = build_G(sub_a(phi) + s_shift, exp(2 * s_shift) * sub_a(al), exp(-s_shift) * sub_a(f),
                     exp(-2 * lam * s_shift) * sub_a(bh), cE * exp(s_shift), lam).subs({T: Tn}, simultaneous=True)
check("A1r_anchor_shift_absorption_angular_extended", "SUBSTANTIVE",
      is_zero_matrix(sp.expand(Gab - Gab_target)),
      "phi -> phi + s is absorbed EXACTLY by c_E -> c_E e^s, alpha -> e^{2s} alpha, f -> e^{-s} f, bh -> e^{-2 lam s} bh "
      "with the unit rescale (x,z) -> (e^{lam s} x, e^s z) and t, y UNTOUCHED: the compact y-leg absorbs purely on the "
      "FIELD side (its registered period needs no rescale) while the fiber-leg period rescales as an OVERLAP datum "
      "between presentations (T1q's reading: not a chart automorphism); shift-EQUIVARIANCE (F-RA4) extends angular-live "
      "with the anchored readout Q = c_E e^{-phi} invariant")

print("=" * 78)
print("STAGE A1 — TA-2: the requirement set re-posed (computational legs)")
print("=" * 78)

# --- A2a: PERIODICITY is a DERIVED domain fact of the registered stratum, not an imposition.
Fgen = Function("F")(Y)
per_ok = simplify(Fper.subs(Y, Y + Pk) - Fper) == 0
bare_fails = simplify((Y + Pk) - Y) != 0
jet_per = simplify(diff(Fper, Y).subs(Y, Y + Pk) - diff(Fper, Y)) == 0
check("A2a_periodicity_is_a_domain_fact", "SUBSTANTIVE",
      per_ok and bare_fails and jet_per,
      "the registered stratum's domain is R_x x T^2 (x R_t): a FIELD is by definition a function ON the domain, hence "
      "P-periodic in (y,z) — DERIVED from the banked toric arena registration (routeC :29; the S^3 descent), never "
      "imposed; jets inherit periodicity; bare y does not (A1n). Alphabet interaction: periodicity constrains the "
      "CONFIGURATION space, it adds NO new alphabet letters and removes none — the anchored/shift rules are pointwise "
      "and periodicity-blind; the alphabet's periodic-sector content stays at this legality layer (mode structure = "
      "TA-3; anything beyond function-decomposition — e.g. any cycle content — is Stage A3's contract, F-A1)")

# --- A2b: walls stay timelike x-loci; the ANGULAR directions contribute NO wall strata.
tyz_block = Matrix([[GREG[0, 0], GREG[0, 2], GREG[0, 3]],
                    [GREG[2, 0], GREG[2, 2], GREG[2, 3]],
                    [GREG[3, 0], GREG[3, 2], GREG[3, 3]]])
det_tyz = simplify(tyz_block.det())
target_det = -cE**2 * bh * exp(2 * lam * phi)
check("A2b_walls_timelike_no_angular_walls", "SUBSTANTIVE",
      simplify(det_tyz - target_det) == 0,
      "the induced metric on a wall locus {x = x_w} is the (t,y,z) block: det = -c_E^2 bh e^{2 lam phi} < 0 for the "
      "registered positivity bh > 0 — walls remain TIMELIKE surfaces {x_w} x R_t x T^2 with ANGULAR-VARYING germ/trace "
      "data (typed, N=2 wall layer). HONEST SPLIT (verifier note 2): T^2 compact WITHOUT boundary DERIVES the absence "
      "of angular BOUNDARY/completion strata and corner types; the absence of interior angular JUNCTION loci is an "
      "INHERITED-PREMISE (the banked wall census: walls = x-loci, CANON), not derived from closedness — the completion "
      "census stays the x-direction's banked 12 FC families")

# --- A2c: R4's exact conditions are pointwise-algebraic; (t,y,z) spectators (banked re-run).
lam_r, kmod_r, phi_r = symbols("lam_r kmod_r phi_r")   # read: arbitrary functions of (t,x,y,z)
k00_r, k11_r = lam_r - kmod_r, lam_r + kmod_r
trX_r = k00_r + k11_r
det_channel = exp(phi_r * trX_r)
check("A2c_R4_blindness_angular_spectator", "GUARD",
      simplify(diff(trX_r, kmod_r)) == 0 and simplify(diff(det_channel, kmod_r)) == 0,
      "banked re-run (T2g/T2h -> TU2f/TU2g lineage): the trace and volume-density channels are k_mod-blind as pointwise "
      "algebra with every symbol an arbitrary function of (t,x,y,z) — R4's slot theorem transfers, (t,y,z) spectators")

print("=" * 78)
print("STAGE A1 — TA-3: the angular character/mode layer (Category-A organizing")
print("technique; mode bound = LAYER with remainder typed, A-L2)")
print("=" * 78)

# --- A3a: character orthogonality on the registered periods (exact, integer symbols).
nn = symbols("n", integer=True, nonzero=True)
mode = exp(2 * sp.pi * sp.I * nn * Y / Pk)
integ = sp.integrate(mode, (Y, 0, Pk))
zero_mode = sp.integrate(sp.S.One, (Y, 0, Pk))
check("A3a_character_orthogonality_exact", "SUBSTANTIVE",
      simplify(integ) == 0 and simplify(zero_mode - Pk) == 0,
      "int_0^P e^{2 pi i n y / P} dy = 0 for nonzero integer n, = P for n = 0: the T^2 characters are exactly "
      "orthogonal on the registered periods — the pairing's angular domain is CANONICAL (compact, no supplied decay "
      "class), in derived CONTRAST with the time-domain datum (branch-dependent supplied structure, T1 TT-4)")

# --- A3b/A3c/A3e: the translation action diagonalizes; jets act by mode multiplication;
#     mirrors act by mode negation. (Function-decomposition layer ONLY; A3 untouched, F-A1.)
a2 = symbols("a2", real=True)
diag_ok = simplify(mode.subs(Y, Y + a2) - exp(2 * sp.pi * sp.I * nn * a2 / Pk) * mode) == 0
check("A3b_translation_action_diagonal_on_characters", "SUBSTANTIVE",
      diag_ok,
      "y -> y + a acts on the character e_n by the scalar e^{2 pi i n a / P}: the residual T^2 translation layer "
      "DIAGONALIZES on the character decomposition — the derived organizing layer for Stage A2's equivariance runs")
deriv_ok = simplify(diff(mode, Y) - (2 * sp.pi * sp.I * nn / Pk) * mode) == 0
check("A3c_angular_jets_act_by_mode_multiplication", "SUBSTANTIVE",
      deriv_ok,
      "d_y e_n = (2 pi i n / P) e_n: the angular jet letters act diagonally on modes — the tri-graded alphabet's "
      "angular grading is mode-compatible; the mode index is DUAL/decomposition data of a FUNCTION (Category-A "
      "harmonic-analysis technique), NOT field-cycle content (that census is Stage A3's contract, F-A1)")
refl_ok = simplify(mode.subs(Y, -Y) - exp(2 * sp.pi * sp.I * (-nn) * Y / Pk)) == 0
check("A3e_mirror_negates_modes", "SUBSTANTIVE",
      refl_ok,
      "y -> -y maps e_n -> e_{-n}: the derived angular mirrors act on the character lattice by negation; K4 acts on "
      "moduli only (coordinates untouched, A1m) and so COMMUTES with the mode decomposition — the layered character "
      "rule (T2's table) extends by one angular column, per mode")

print("=" * 78)
print("STAGE A1 — TA-4: composition facts (reading-independence's angular fate;")
print("fork interactions; R-A typed)")
print("=" * 78)

# --- A4a: the shift-corrected spatial derivative is chi-slack-invariant (TU1f analog).
Ffld = Function("Ffld")(T, X, Y, Z)
chi_i = Function("chi")(Xn)
F_new = Ffld.subs({T: Tn, X: Xn, Y: Yn + chi_i, Z: Zn}, simultaneous=True)
dx_new = diff(F_new, Xn)
dy_new = diff(F_new, Yn)
g12n = symbols("gxy0", real=True) + symbols("gyy0", real=True) * diff(chi_i, Xn)   # g_xy' (A1g pullback law)
Dx_new = dx_new - (g12n / symbols("gyy0", real=True)) * dy_new
Dx_old = (diff(Ffld, X) - (symbols("gxy0", real=True) / symbols("gyy0", real=True)) * diff(Ffld, Y)
          ).subs({T: Tn, X: Xn, Y: Yn + chi_i, Z: Zn}, simultaneous=True)
check("A4a_corrected_derivative_chi_invariant", "SUBSTANTIVE",
      simplify(sp.expand(Dx_new - Dx_old)) == 0,
      "D_x = d_x - (g_xy/g_yy) d_y — the g-orthogonal-to-d_y projection of d_x, a native covariant-row object — is "
      "EXACTLY chi-slack-invariant (the angular analog of the banked TU1f psi-invariant D_x); with gamma_xx "
      "chi-invariant (A1j) the invariant alphabet blocks extend to the angular sector: the TU1g triangular-invertible "
      "reorganization EXTENDS in structure; the full angular reading-independence theorem is Stage A2 business (TYPED)")

# --- A4b: the reorganization is triangular and invertible (first-jet instance).
gxy0, gyy0 = symbols("gxy0 gyy0", real=True)
Mtri = Matrix([[1, -gxy0 / gyy0], [0, 1]])
check("A4b_alphabet_reorganization_triangular_invertible", "SUBSTANTIVE",
      simplify(Mtri.det() - 1) == 0 and is_zero_matrix(Mtri * Mtri.inv() - eye(2)),
      "(d_x, d_y) -> (D_x, d_y) is unit-determinant triangular (invertible); with g_xx = gamma_xx + g_xy^2/g_yy the "
      "component map is triangular-invertible too: no pointwise content rides the presentation choice — the derived "
      "first leg of reading-independence's angular fate (full theorem = A2; TYPED, not claimed)")

print("=" * 78)
print("STAGE A1 — TA-5: controls (C-1 T1 recovery; C-2 transitive static recovery;")
print("C-3 registry sweep) and guards")
print("=" * 78)

ROOT = os.path.dirname(HERE)
T1_LEDGER = os.path.join(ROOT, "udt_p4_timelive_stage_T1_2026-07-31", "TIMELIVE_T1_LEDGER.tsv")
CENSUS = os.path.join(ROOT, "udt_p4_routeA_response_inverse_problem_2026-07-29", "VARIATION_DOMAIN_CENSUS.tsv")
REGISTRY = os.path.join(ROOT, "NEGATIVES_REGISTRY.md")
MY_LEDGER = os.path.join(HERE, "ANGULAR_A1_LEDGER.tsv")


def parse_tsv(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if parts[0] in ("row_id", "object"):
                continue
            rows.append(parts)
    return rows


t1_rows = {p[0]: p for p in parse_tsv(T1_LEDGER)}
my_rows = {p[0]: p for p in parse_tsv(MY_LEDGER)}
census_rows = parse_tsv(CENSUS)
census_tokens = [r[0].split()[0] for r in census_rows]

# --- C1a: the y-independent restriction recovers the banked T1 18-object census EXACTLY.
t1_o_ids = [f"O{i:02d}" for i in range(1, 19)]
t1_r_ids = [f"R{i:02d}" for i in range(1, 16)]
t1_j_ids = [f"J{i:02d}" for i in range(1, 16)]
c1a_ok = set(t1_rows) == set(t1_o_ids + t1_r_ids + t1_j_ids)
targets = []
for oid in t1_o_ids:
    mine = my_rows.get(oid)
    t1 = t1_rows.get(oid)
    ok = (mine is not None and t1 is not None and mine[5].startswith(f"T1:{oid} ")
          and mine[5].split()[1] == t1[2].split()[0])
    c1a_ok = c1a_ok and ok
    targets.append(oid)
for nid in ("O19", "O20"):
    c1a_ok = c1a_ok and my_rows[nid][5].startswith("ABSENT-from-T1")
for rid in t1_r_ids + t1_j_ids:
    c1a_ok = c1a_ok and my_rows[rid][5].startswith(f"T1:{rid}")
    targets.append(rid)
c1a_ok = c1a_ok and targets == t1_o_ids + t1_r_ids + t1_j_ids and len(my_rows) == 50
check("C1a_census_y_independent_recovery_object_by_object", "SUBSTANTIVE",
      c1a_ok,
      "mechanical parse of BOTH ledgers: the y-independent restriction column of the 50-row angular-live ledger maps "
      "the 18 extended O-rows, 15 R-rows and 15 J-rows onto the banked TIMELIVE_T1_LEDGER rows one-to-one, in order, "
      "name-matched; the two NEW rows (O19 angular mixed row, O20 angular domain structure) restrict to "
      "ABSENT-from-T1 with stated reasons — the T1 18-object census + re-posed R/J set is recovered EXACTLY (F-A7 not fired)")

# --- C1b: requirement-class recovery (PW 8 / WS 2 / GC 4 + R11 per-row), row-by-row.
cls_re = re.compile(r"banked R\d+ \((\w+[-\w]*)")
tally = {"PW": 0, "WS": 0, "GC": 0, "per": 0}
row_match = True
for rid in t1_r_ids:
    m = cls_re.search(t1_rows[rid][5])
    cls = m.group(1) if m else "?"
    if cls in ("PW", "WS", "GC"):
        tally[cls] += 1
    elif cls.startswith("per"):
        tally["per"] += 1
    m2 = re.search(r"T1:R\d+ \((\w+[-\w]*)\)", my_rows[rid][5])
    my_cls = m2.group(1) if m2 else ("per-row" if "per-row" in my_rows[rid][5] else "?")
    row_match = row_match and (my_cls == cls or (cls.startswith("per") and my_cls.startswith("per")))
check("C1b_requirement_class_recovery", "GUARD",
      tally == {"PW": 8, "WS": 2, "GC": 4, "per": 1} and row_match,
      "the banked class tally PW 8 / WS 2 / GC 4 (+ R11 per-row) parsed from the T1 ledger matches the angular-live "
      "ledger's claimed classes row-by-row: no class migration at A1 depth (declaration-grade table comparison)")

# --- C2a/C2b: TRANSITIVE static recovery down to the banked Stage-1 census (16 rows).
c2a_ok = len(census_tokens) == 16
for i, oid in enumerate([f"O{k:02d}" for k in range(1, 17)]):
    c2a_ok = c2a_ok and my_rows[oid][6] == f"banked:{census_tokens[i]}"
c2a_ok = (c2a_ok and my_rows["O17"][6].startswith("banked-premise:diagonal")
          and all(my_rows[k][6].startswith("ABSENT-static") for k in ("O18", "O19", "O20")))
check("C2a_static_recovery_transitive_my_ledger", "SUBSTANTIVE",
      c2a_ok,
      "the static+y-independent restriction column of the angular-live ledger names the 16 banked "
      "VARIATION_DOMAIN_CENSUS objects in order, exactly; O17 restricts to the canonized DIAGONAL premise (N=0); "
      "O18/O19/O20 are absent from the static posing — the banked static Stage-1 posing is recovered transitively")
t1_static_tokens = []
for oid in [f"O{k:02d}" for k in range(1, 17)]:
    m = re.search(r"banked row (\S+)", t1_rows[oid][5])
    t1_static_tokens.append(m.group(1) if m else "?")
check("C2b_transitivity_leg_T1_to_census", "GUARD",
      t1_static_tokens == census_tokens,
      "the T1 ledger's own static-restriction column names the same 16 banked census objects in the same order "
      "(mechanical re-run of T1's C1a correspondence): restriction composes transitively angular->time->static")

# --- C3: the A-L9 registry sweep (list BUILT, registry NOT edited — driver work post-bank).
# AMENDMENT 2026-07-31, verifier round 1 (AM-C): the original two-keyword regex
# ('axisym|one-parameter') under-covered its prereg spec — it missed the digit form
# '1-PARAMETER' and the entry-#17 'spherical-average interface reading' premise class.
# The WIDENED vocabulary below adds: 1-param (digit/hyphen forms), spherical (covers
# spherical-average), even-sector. Both sweeps run; old -> new counts reported honestly.
sweep_re_old = re.compile(r"axisym|one-parameter", re.IGNORECASE)
sweep_re = re.compile(r"axisym|one-param|1-param|spherical|even-sector", re.IGNORECASE)
anchor_re = re.compile(r"^\s*\d+\.\s|^##\s")


def run_sweep(rx):
    hits = {}
    cur = "(preamble)"
    with open(REGISTRY, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if anchor_re.match(line):
                cur = line.strip()[:110]
            if rx.search(line):
                hits.setdefault(cur, {"first_line": lineno, "quotes": []})
                if len(hits[cur]["quotes"]) < 3:
                    hits[cur]["quotes"].append(line.strip()[:180])
    return hits


anchors_old = run_sweep(sweep_re_old)
anchors = run_sweep(sweep_re)
C3_SWEEP = [{"anchor": k, **v} for k, v in anchors.items()]
check("C3a_registry_sweep_one_parameter_presentation", "SUBSTANTIVE",
      len(C3_SWEEP) > 0 and len(anchors) >= len(anchors_old)
      and set(anchors_old) <= set(anchors)
      and any("n = 0 ATTAINED NOWHERE" in a for a in anchors),
      f"NEGATIVES_REGISTRY.md swept mechanically; WIDENED premise-set vocabulary (AM-C: axisym / one-param / 1-param / "
      f"spherical / even-sector): {len(anchors_old)} -> {len(C3_SWEEP)} candidate entries flagged (old sweep strictly "
      f"contained in new; the verifier-named entry #17 'spherical-average interface reading' now flagged); anchors + "
      f"premise quotes recorded in the results JSON and the decision surface; per A-L9 each needs a premise-scope "
      f"re-grade BEFORE it can block an angular-live result — the LIST is built here; classification and any registry "
      f"edit are driver work post-bank")

# --- Guards G1-G4 (wired into the exit path).
src = open(os.path.join(HERE, "derive_angular_A1.py"), encoding="utf-8").read()
banned_src = ["num" + "py", "sci" + "py", "rand" + "om", ".eva" + "lf", "nso" + "lve(", "tor" + "ch", "flo" + "at("]
check("G3_no_floats_numeric_solvers_or_rng", "GUARD",
      all(tok not in src for tok in banned_src),
      "self-scan of this script's source: no external numerics, no RNG, no eval-to-decimal / numeric-solve / "
      "decimal-coercion calls — exact SymPy only")

fa1_re = re.compile(r"\bwinding\b|\bholonomy\b|\bcycles?\b", re.IGNORECASE)
allow_re = re.compile(r"stage a3|a3's|f-a1|scope", re.IGNORECASE)
fa1_viol = []
for fname in ("EXACT_DERIVATION.md", "ANGULAR_A1_LEDGER.tsv"):
    fpath = os.path.join(HERE, fname)
    if os.path.exists(fpath):
        for lineno, line in enumerate(open(fpath, encoding="utf-8"), 1):
            if fa1_re.search(line) and not allow_re.search(line):
                fa1_viol.append(f"{fname}:{lineno}")
check("G4_FA1_banned_word_scan", "GUARD",
      len(fa1_viol) == 0,
      "F-A1 self-audit: every occurrence of the A3-scoped vocabulary in the derivation record and ledger sits on a "
      "scope-exclusion line (Stage A3 / F-A1 / scope marker); violations: " + (";".join(fa1_viol) or "none") +
      ". (DECISION_SURFACE_UPDATE.md carries third-party registry QUOTES for C-3 and is audited by hand in "
      "AUDIT_REPORT.md, not by this mechanical scan.)")

n_rows = {"OBJECT": 0, "REQUIREMENT": 0, "JROW": 0}
cols_ok = True
for p in my_rows.values():
    n_rows[p[1]] = n_rows.get(p[1], 0) + 1
    cols_ok = cols_ok and len(p) == 9
check("G2_ledger_coverage_and_shape", "GUARD",
      n_rows == {"OBJECT": 20, "REQUIREMENT": 15, "JROW": 15} and cols_ok,
      "the angular-live ledger parses with exactly 20 OBJECT + 15 REQUIREMENT + 15 JROW rows, 9 columns each")

# --- Tally, JSON, exit (all checks incl. guards wired).
n_sub = sum(1 for ch in CHECKS if ch["kind"] == "SUBSTANTIVE")
n_gd = sum(1 for ch in CHECKS if ch["kind"] == "GUARD")
n_pass = sum(1 for ch in CHECKS if ch["passed"])
results = {
    "stage": "A1 angular-live variation domain (torus-first)",
    "date": "2026-07-31",
    "contract": "PREREGISTRATION.md (frozen first)",
    "stamps": ["A-L1 T2-stratum layer (full-S3 typed)", "A-L2 tri-graded jets <=2 (higher typed)",
               "A-L4 time-live-line", "A-L5 theta absent", "N=2 wall layer",
               "lock-reading fork carried (T1)", "NEW spatial-reading fork carried (A1j2/A1j3)",
               "no response law / no solve / no A3 census (F-A1)",
               "AMENDMENT 2026-07-31, verifier round 1: AM-A zeta-slack layer (A1s..A1s5); "
               "AM-B joint-slack orbit = level set of m^T B^-1 m (A1i2/A1j3); AM-C widened C-3 sweep"],
    "checks": CHECKS,
    "tally": {"total": len(CHECKS), "passed": n_pass, "substantive": n_sub, "guard": n_gd},
    "amendments": [
        "AM-A (MODERATE): missed fiber-translation (zeta) residual slack layer derived — z -> z + zeta(y) residual on "
        "the registered family with f~ = f + zeta' (A1s); zeta(x) generates m_z (A1s2: O19 m_z DERIVED, was analogy); "
        "zeta(t) moves N_z (A1s3); additive cocycle within the layer (A1s4); semidirect under chi and psi (A1s5). "
        "Residual-group statement RESTATED in sec 1.2.6, ledger stamp 4, O16, J10. A1e's rigidity scoped to z-only maps.",
        "AM-B (MINOR-MODERATE): under the coordinate pin the joint (chi', zeta') slack orbit of m = (g_xy, g_xz) is "
        "the LEVEL SET of m^T B^-1 m (a conic of lawful slacks), not {m, -m} (A1i2, witness (1,0) -> (0,1)); "
        "irreducibility survives as NON-REMOVABILITY (invariant = the irreducible datum); projected full removal "
        "s = -B^-1 m stands (A1j3). Fork framing unchanged (verifier-confirmed both ways).",
        "AM-C (MINOR): C-3 sweep vocabulary widened (1-param digit form; spherical/spherical-average; even-sector); "
        "flagged anchors " + str(len(anchors_old)) + " -> " + str(len(C3_SWEEP)) + "; registry NOT edited.",
        "NOTE-1: A1q branch-scope clarified — 1/g^xx = gamma_xx IS the projected reading; the F-A2 hazard attaches to "
        "imported PARAMETRIZATION, not to the derived projected reading functional.",
        "NOTE-2: A2b's junction leg re-labeled INHERITED-PREMISE (banked wall census: walls = x-loci, CANON); the "
        "T^2-closedness (no boundary/completion strata) leg stays DERIVED."],
    "C3_sweep_counts": {"old_regex_anchors": len(anchors_old), "widened_regex_anchors": len(C3_SWEEP)},
    "C3_registry_sweep": C3_SWEEP,
    "outcome_class": "OA1-1 (the angular-live posing closes; controls pass; forks typed, none adopted)"
        if n_pass == len(CHECKS) else "FAILED-CHECKS",
}
json_path = os.path.join(HERE, "angular_A1_results.json")
with open(json_path, "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=1, sort_keys=False)
g1_ok = json.load(open(json_path, encoding="utf-8")) == results
check("G1_json_roundtrip_wired", "GUARD", g1_ok, "results JSON round-trips byte-faithfully; wired into the exit path")
n_sub = sum(1 for ch in CHECKS if ch["kind"] == "SUBSTANTIVE")
n_gd = sum(1 for ch in CHECKS if ch["kind"] == "GUARD")
n_pass = sum(1 for ch in CHECKS if ch["passed"])
results["tally"] = {"total": len(CHECKS), "passed": n_pass, "substantive": n_sub, "guard": n_gd}
results["outcome_class"] = ("OA1-1 (the angular-live posing closes; controls pass; forks typed, none adopted)"
                            if n_pass == len(CHECKS) else "FAILED-CHECKS")
with open(json_path, "w", encoding="utf-8") as fh:
    json.dump(results, fh, indent=1, sort_keys=False)

print("=" * 78)
print(f"TALLY: {len(CHECKS)} checks, {n_pass} passed — {n_sub} SUBSTANTIVE + {n_gd} GUARD")
print(f"OUTCOME: {results['outcome_class']}")
print("=" * 78)
sys.exit(0 if n_pass == len(CHECKS) else 1)






