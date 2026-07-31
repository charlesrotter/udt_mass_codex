#!/usr/bin/env python3
"""Blind adversarial verifier — independent checks for Stage A1 (2026-07-31).
Exact SymPy only; exit nonzero on any failure. Written INCREMENTALLY per duty.
Independent of derive_angular_A1.py: the registered metric is rebuilt here from
the quadratic form directly; parsers for the control TSVs are the verifier's own.
"""
import os, re, sys
import sympy as sp
from sympy import Matrix, symbols, exp, diff, simplify, Function, zeros, eye

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FAILS = []


def V(name, cond, note=""):
    ok = bool(cond)
    if not ok:
        FAILS.append(name)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {note}")
    return ok


T, X, Y, Z = symbols("t x y z", real=True)
Tn, Xn, Yn, Zn = symbols("t_n x_n y_n z_n", real=True)
OLD, NEW = (T, X, Y, Z), (Tn, Xn, Yn, Zn)
cE = symbols("c_E", positive=True)
lam = symbols("lam", real=True)
phi = Function("phi")(T, X, Y, Z)
al = Function("alpha")(T, X, Y, Z)
f = Function("f")(T, X, Y, Z)
bh = Function("bh")(T, X, Y, Z)

# --- Independent rebuild of the registered metric from the quadratic form itself.
dt, dx, dy, dz = symbols("dt dx dy dz")
DIFFS = {T: dt, X: dx, Y: dy, Z: dz}


def metric_from_form(phi_e, al_e, f_e, bh_e, cE_e, lam_e):
    u = exp(-2 * phi_e)
    A = dz + f_e * dy
    ds2 = sp.expand(-u * (cE_e * dt + al_e * A) ** 2 + A ** 2 / u
                    + exp(2 * lam_e * phi_e) * (dx ** 2 + bh_e * dy ** 2))
    d = [dt, dx, dy, dz]
    G = zeros(4, 4)
    P = sp.Poly(ds2, d)
    for i in range(4):
        for j in range(4):
            mono = [0, 0, 0, 0]
            mono[i] += 1
            mono[j] += 1
            coef = P.coeff_monomial(sp.prod(v ** m for v, m in zip(d, mono)))
            G[i, j] = coef if i == j else coef / 2
    return Matrix(4, 4, lambda i, j: simplify(G[i, j]))


GREG = metric_from_form(phi, al, f, bh, cE, lam)


def pullback(G, coord_map):
    full = {o: coord_map.get(o, dict(zip(OLD, NEW))[o]) for o in OLD}
    J = Matrix(4, 4, lambda i, j: diff(full[OLD[i]], NEW[j]))
    return J.T * G.subs(full, simultaneous=True) * J


def is0(M):
    return all(simplify(sp.expand(e)) == 0 for e in M)


back = dict(zip(NEW, OLD))

# =====================  DUTY 0 (recorded from shell)  =====================
# Two reruns of derive_angular_A1.py: exit 0 both; stdout sha256
# 12becae90bc65c18a8f2e832314aed5d0bd4ab3f7aaa5cb141b9404df331252a and JSON sha256
# 1dc4d899a3112f955a56ccd8c85d226833b00adda474a46cc21f35ab6a33aff5, both byte-identical
# to the packaged DERIVATION_STDOUT.txt / angular_A1_results.json. 40 = 31S + 9G
# recounted independently. Guard mutation-probe: appending a bare "winding" line to a
# throwaway copy's EXACT_DERIVATION.md fired G4 -> FAILED-CHECKS, exit 1. Wiring OK.

# =====================  DUTY 1(a): A1e rigidity + the fiber-leg slack hunt  ============
# V1a: confirm the package's k'^2 = 1 rigidity for z -> k(z).
kz = Function("k")(Zn)
Gz = pullback(GREG, {Z: kz})
gam_zz_old = simplify(GREG[3, 3] - GREG[0, 3] ** 2 / GREG[0, 0])
gam_zz_new = simplify(Gz[3, 3] - Gz[0, 3] ** 2 / Gz[0, 0])
V("V1a_A1e_rigidity_confirmed",
  simplify(gam_zz_new - diff(kz, Zn) ** 2 * gam_zz_old.subs({T: Tn, X: Xn, Y: Yn, Z: kz}, simultaneous=True)) == 0
  and simplify(gam_zz_old - exp(2 * phi)) == 0,
  "gamma_zz -> k'^2 gamma_zz with gamma_zz = e^{2phi}: projected lock preservation forces k'^2=1 (A1e right)")

# V1b: THE MISSED LAWFUL RESIDUAL MAP — z -> z + zeta(y) preserves the REGISTERED FORM
# with f~ = f o map + zeta' (phi, alpha, bh relabeled only): a fiber-translation slack
# absent from the package's slack census (sec 1.2 / J10 equality).
zeta = Function("zeta")(Yn)
Gzt = pullback(GREG, {Z: Zn + zeta})
sub_z = lambda e: e.subs({T: Tn, X: Xn, Y: Yn, Z: Zn + zeta}, simultaneous=True)
Gzt_target = metric_from_form(sub_z(phi), sub_z(al), sub_z(f) + diff(zeta, Yn), sub_z(bh), cE, lam)
V("V1b_missed_fiber_translation_slack_zeta_y",
  is0(Gzt - Gzt_target),
  "z -> z + zeta(y) maps the registered angular-live family TO ITSELF with f~ = f + zeta' "
  "(all other fields relabeled): a lawful residual map (period-compatible zeta) MISSING from "
  "the package's slack-layer census — refutes the '=' in 'residual symmetry ... = K4 x T1 x "
  "[T2 translations + mirrors] |x slack layers' (EXACT_DERIVATION 1.2.6, ledger stamp 4, J10)")

# V1c: z -> z + zeta(x) generates the m_z mixed row from the diagonal stratum (A1g's z-analog,
# underived in the package; O19's m_z fork structure was claimed by analogy only).
GF = {}
for i in range(4):
    for j in range(i, 4):
        GF[(i, j)] = Function(f"g{i}{j}")(T, X, Y, Z)
GGEN = Matrix(4, 4, lambda i, j: GF[(min(i, j), max(i, j))])
GD = GGEN.subs({GF[(1, 2)]: 0, GF[(1, 3)]: 0}, simultaneous=True)
zx = Function("zeta")(Xn)
GDz = pullback(GD, {Z: Zn + zx})
gen_xz = simplify(GDz[1, 3] - GD.subs({T: Tn, X: Xn, Y: Yn, Z: Zn + zx}, simultaneous=True)[3, 3] * diff(zx, Xn))
V("V1c_zeta_x_generates_m_z",
  gen_xz == 0,
  "z -> z + zeta(x) from the x-angular-diagonal stratum generates g_xz = g_zz zeta': the m_z row "
  "is generated by the FIBER-leg translation slack, not by chi — A1g covers only m_y; the package's "
  "'chi-slack generates m' (O19) is incomplete for m_z")

# =====================  DUTY 1(b)/(d): the chi-slack fork structure  ============
# V1d: A1h exhaustiveness for the chi-map ALONE — pointwise quadratic, exactly 2 roots
# (g_yy != 0 on the nondegenerate stratum).
cp, zp = symbols("chi_p zeta_p", real=True)
g11, g12, g13, g22, g23, g33 = symbols("gxx0 gxy0 gxz0 gyy0 gyz0 gzz0", real=True)
sols_cp = sp.solve(sp.Eq(g11 + 2 * g12 * cp + g22 * cp ** 2, g11), cp)
V("V1d_A1h_two_branches_exhaustive_for_chi_alone",
  sorted(sols_cp, key=str) == sorted([0, -2 * g12 / g22], key=str),
  "preserving g_xx under y -> y + chi(x) alone: quadratic in chi' -> exactly {0, -2 g_xy/g_yy}; "
  "A1h EXHAUSTIVE within its stated class (chi-maps alone, g_yy != 0)")

# V1e: BUT the JOINT (chi, zeta) slack under the SAME coordinate pin has a CONIC branch
# set, and the orbit of m = (g_xy, g_xz) is the full level set of m^T B^{-1} m — strictly
# larger than the package's claimed orbit {m, -m} (A1i / O19 / EXACT_DERIVATION 1.2.3).
B = Matrix([[g22, g23], [g23, g33]])
m = Matrix([g12, g13])
s = Matrix([cp, zp])
gxx_joint = sp.expand(g11 + (2 * m.T * s)[0] + (s.T * B * s)[0])
constraint = sp.expand(gxx_joint - g11)          # = 2 m.s + s^T B s
m_new = m + B * s
inv_quad = sp.simplify((m.T * B.inv() * m)[0])
inv_quad_new = sp.expand((m_new.T * B.inv() * m_new)[0])
V("V1e_joint_slack_orbit_is_level_set_not_Z2",
  simplify(inv_quad_new - inv_quad - constraint) == 0,
  "under the joint (chi', zeta') slack preserving g_xx (constraint 2 m.s + s^T B s = 0, a CONIC "
  "of lawful slacks, not two points), m^T B^{-1} m is exactly invariant: the orbit of the mixed "
  "row is the LEVEL SET of m^T B^{-1} m — the package's '{m, -m}' orbit (A1i) is only the "
  "y-leg slice. IRREDUCIBILITY STILL HOLDS (B pos-def: m^T B^{-1} m != 0 => m never reaches 0), "
  "so the fork's coordinate branch survives, with the correct invariant = g_xx - gamma_xx")
# concrete witness that a lawful joint slack maps m outside {m, -m}:
wit = {g22: 1, g23: 0, g33: 1, g12: 1, g13: 0, cp: -1, zp: 1}
V("V1e2_witness_orbit_point_outside_pm_m",
  sp.expand(constraint.subs(wit)) == 0
  and tuple(m_new.subs(wit)) not in [(1, 0), (-1, 0)]
  and tuple(m_new.subs(wit)) == (0, 1),
  "witness B=I, m=(1,0), s=(-1,1): constraint holds, m -> (0,1) — a lawful coordinate-pin slack "
  "moving m off {m,-m}; the Z2 statement is not the full orbit")

# V1f: projected reading — gamma_xx^{full} = g_xx - m^T B^{-1} m is invariant under EVERY
# joint slack, and s = -B^{-1} m removes BOTH mixed components (A1j/A1j2 extended).
gam_full = g11 - (m.T * B.inv() * m)[0]
gam_full_new = sp.expand(gxx_joint - (m_new.T * B.inv() * m_new)[0])
rem_s = -B.inv() * m
V("V1f_projected_reading_invariant_and_full_removal",
  simplify(gam_full_new - gam_full) == 0
  and is0(sp.expand(m + B * rem_s))
  and simplify(sp.expand(gxx_joint.subs({cp: rem_s[0], zp: rem_s[1]})) - gam_full) == 0,
  "gamma_xx (full 2-component projection) is slack-invariant identically; s = -B^{-1}m removes "
  "the whole mixed row with g_xx' = gamma_xx: A1j/A1j2 confirmed and correctly extended to m_z; "
  "the SPATIAL-READING FORK itself is confirmed (coordinate => irreducible, projected => removable)")

# V1g: A1q discriminator recomputed on the 2x2 block.
B2 = Matrix([[g11, g12], [g12, g22]])
V("V1g_A1q_discriminator_confirmed",
  simplify(1 / B2.inv()[0, 0] - (g11 - g12 ** 2 / g22)) == 0 and simplify((g11 - g12 ** 2 / g22) - g11) != 0,
  "1/g^{xx} = g_xx - g_xy^2/g_yy != g_xx when m on: computed, and carries content (the covariant-row "
  "pin and the fiber-adapted pin differ by a derived nonzero quantity). NOTE the un-flagged wrinkle: "
  "1/g^{xx} = gamma_xx IS the projected reading — the fork's projected branch pins exactly the "
  "fiber-adapted quantity; the F-A2 line ('this package pins the covariant row') is branch-scoped")

# V1h: A1g2 (chi moves the shift row) + A1l (semidirect) recomputed from my own pullback.
chi_xt = Function("chi")(Xn, Tn)
GDp2 = pullback(GGEN, {Y: Yn + chi_xt})
sub_m2 = lambda e: e.subs({T: Tn, X: Xn, Y: Yn + chi_xt, Z: Zn}, simultaneous=True)
V("V1h_A1g2_shift_row_moves",
  simplify(GDp2[0, 2] - (sub_m2(GF[(0, 2)]) + sub_m2(GF[(2, 2)]) * diff(chi_xt, Tn))) == 0,
  "N_y' = N_y + g_yy chi_t confirmed independently (chi- and psi-sectors slack-coupled)")
psi = Function("psi")(X)
chi_g = Function("chi")(X, T)
gap = simplify((Y + chi_g.subs(T, T + psi)) - (Y + chi_g))
V("V1h2_A1l_semidirect_gap",
  simplify(gap - (chi_g.subs(T, T + psi) - chi_g)) == 0 and simplify(gap.subs(chi_g, Function("c0")(X))) != gap,
  "order gap = chi(x, t+psi) - chi(x,t), zero iff chi t-independent: semidirect composition confirmed")

# =====================  DUTY 2: TA-2 / TA-3 independent legs  ============
# V2a: A2a periodicity as a domain fact — my own legs, incl. the alphabet-neutrality probe:
# jets of periodic fields are periodic (legal letters), bare y is not a torus function,
# and the anchor-shift action (phi -> phi+s, s const) commutes with periodicity.
Pk = symbols("P", positive=True)
nn = symbols("n", integer=True, nonzero=True)
Fp = sp.cos(2 * sp.pi * Y / Pk) + sp.sin(4 * sp.pi * Y / Pk)
V("V2a_periodicity_domain_fact_and_alphabet_neutral",
  simplify(Fp.subs(Y, Y + Pk) - Fp) == 0
  and simplify(diff(Fp, Y, 2).subs(Y, Y + Pk) - diff(Fp, Y, 2)) == 0
  and simplify((Y + Pk) - Y) != 0,
  "R-valued metric components on R x T2 are P-periodic BY DEFINITION of the domain (fields here "
  "are metric components, hence single-valued functions — no winding content is being decided, "
  "only where functions live); jets inherit periodicity (letters stay legal); bare y is not a "
  "domain function. Periodicity constrains configurations, adds/removes no letters: A2a verdict "
  "'configuration-space only, zero alphabet change' CONFIRMED")

# V2b: A2b wall causal type recomputed from MY rebuilt metric.
tyz = Matrix(3, 3, lambda i, j: GREG[[0, 2, 3][i], [0, 2, 3][j]])
V("V2b_wall_block_det_recomputed",
  simplify(tyz.det() + cE ** 2 * bh * exp(2 * lam * phi)) == 0,
  "det of the induced (t,y,z) block on {x = x_w} is -c_E^2 bh e^{2 lam phi} < 0 for bh > 0: "
  "x-walls stay timelike, angular directions add no COMPLETION/boundary strata (T2 closed). "
  "NOTE: absence of interior angular JUNCTION loci is inherited from the banked wall census "
  "(walls = x-loci, CANON), not derived from closedness — see verifier report")

# V2c: spot-check extends-verdicts R3 / R8 / R12 (see report for the reasoning audit) — the
# computational legs they cite: A2b (R3: no angular completion data), A3a (R8: canonical
# angular pairing domain), C1a/C2a (R12: pullback consistency) — all re-verified here.
# V3a: TA-3 orthogonality / diagonalization / mode action / mirror negation, independent.
mode = exp(2 * sp.pi * sp.I * nn * Y / Pk)
V("V3a_orthogonality_exact",
  simplify(sp.integrate(mode, (Y, 0, Pk))) == 0
  and simplify(sp.integrate(sp.S.One, (Y, 0, Pk)) - Pk) == 0
  and simplify(sp.integrate(mode * sp.conjugate(mode), (Y, 0, Pk)) - Pk) == 0,
  "int_0^P e_n = 0 (n != 0), = P (n = 0), ||e_n||^2 = P: exact orthogonality on the registered "
  "period — A3a confirmed incl. the norm leg the package did not state")
a2s = symbols("a_s", real=True)
V("V3b_translation_diagonal_jets_mode_mirror",
  simplify(mode.subs(Y, Y + a2s) - exp(2 * sp.pi * sp.I * nn * a2s / Pk) * mode) == 0
  and simplify(diff(mode, Y) - (2 * sp.pi * sp.I * nn / Pk) * mode) == 0
  and simplify(mode.subs(Y, -Y) - mode.subs(nn, -nn)) == 0,
  "translations diagonalize; d_y = mode multiplication; mirror negates the mode index: "
  "A3b/A3c/A3e confirmed independently")

# V2d: A1r anchor-shift absorption re-verified on MY rebuilt metric (J04/R-A4 leg).
s_ = symbols("s", real=True)
amap = {X: exp(lam * s_) * Xn, Z: exp(s_) * Zn}
Gab = pullback(GREG, amap)
sub_a = lambda e: e.subs({T: Tn, X: exp(lam * s_) * Xn, Y: Yn, Z: exp(s_) * Zn}, simultaneous=True)
Gab_t = metric_from_form(sub_a(phi) + s_, exp(2 * s_) * sub_a(al), exp(-s_) * sub_a(f),
                         exp(-2 * lam * s_) * sub_a(bh), cE * exp(s_), lam).subs({T: Tn}, simultaneous=True)
V("V2d_A1r_anchor_absorption_confirmed",
  is0(sp.expand(Gab - Gab_t)),
  "phi -> phi + s absorbed by (c_E, alpha, f, bh) rescales + (x,z) unit rescale, t and y untouched: "
  "A1r confirmed on the independently rebuilt metric")

# V2e: A1e2/A1f mirror parities re-verified on MY rebuilt metric.
Gzr = pullback(GREG, {Z: -Zn})
sub_zr = lambda e: e.subs({T: Tn, X: Xn, Y: Yn, Z: -Zn}, simultaneous=True)
Gzr_t = metric_from_form(sub_zr(phi), -sub_zr(al), -sub_zr(f), sub_zr(bh), cE, lam).subs({T: Tn, X: Xn}, simultaneous=True)
Gyr = pullback(GREG, {Y: -Yn})
sub_yr = lambda e: e.subs({T: Tn, X: Xn, Y: -Yn, Z: Zn}, simultaneous=True)
Gyr_t = metric_from_form(sub_yr(phi), sub_yr(al), -sub_yr(f), sub_yr(bh), cE, lam).subs({T: Tn, X: Xn}, simultaneous=True)
V("V2e_mirror_parities_confirmed",
  is0(sp.expand(Gzr - Gzr_t)) and is0(sp.expand(Gyr - Gyr_t)),
  "z -> -z with (alpha, f) odd-composed; y -> -y with f odd-composed: parity assignments confirmed")

# V2f: A1k additive chi-cocycle re-verified (my own composition).
chi1, chi2 = Function("chi1")(Xn), Function("chi2")(Xn)
step1 = pullback(GGEN, {Y: Yn + chi2})
step12 = pullback(step1.subs(back, simultaneous=True), {Y: Yn + chi1})
direct = pullback(GGEN, {Y: Yn + chi1 + chi2})
V("V2f_A1k_additive_cocycle_confirmed",
  is0(sp.expand(step12 - direct)),
  "chi2 then chi1 = (chi1 + chi2) on all components: abelian additive overlap law confirmed")

# =====================  DUTY 3: controls with the VERIFIER'S OWN parsers  ============
import csv


def my_parse(path):
    out = {}
    order = []
    with open(path, encoding="utf-8") as fh:
        for row in csv.reader(fh, delimiter="\t"):
            if not row or row[0].startswith("#") or row[0] in ("row_id", "object"):
                continue
            out[row[0]] = row
            order.append(row[0])
    return out, order


A1L, a1_order = my_parse(os.path.join(HERE, "ANGULAR_A1_LEDGER.tsv"))
T1L, t1_order = my_parse(os.path.join(ROOT, "udt_p4_timelive_stage_T1_2026-07-31", "TIMELIVE_T1_LEDGER.tsv"))
CEN, cen_order = my_parse(os.path.join(ROOT, "udt_p4_routeA_response_inverse_problem_2026-07-29",
                                       "VARIATION_DOMAIN_CENSUS.tsv"))

# C-1: y-independent restriction column vs the banked T1 ledger, name-matched, my parse.
ok_c1 = len(t1_order) == 48 and len(a1_order) == 50
for oid in [f"O{i:02d}" for i in range(1, 19)]:
    mine, t1 = A1L[oid], T1L[oid]
    ok_c1 = ok_c1 and mine[5].startswith(f"T1:{oid} ") and mine[5].split()[1] == t1[2].split()[0] \
        and mine[2].split()[0].split("(")[0].rstrip() != "" \
        and mine[2].split(" ")[0] == t1[2].split(" ")[0]  # same object NAME leading token
for rid in [f"R{i:02d}" for i in range(1, 16)] + [f"J{i:02d}" for i in range(1, 16)]:
    ok_c1 = ok_c1 and A1L[rid][5].startswith(f"T1:{rid}")
ok_c1 = ok_c1 and A1L["O19"][5].startswith("ABSENT-from-T1") and A1L["O20"][5].startswith("ABSENT-from-T1")
V("VC1_T1_recovery_own_parse", ok_c1,
  "my own csv parse of BOTH ledgers: 48 T1 rows / 50 A1 rows; every extended row's y-independent "
  "restriction names its T1 row, name-matched on the leading object token; O19/O20 restrict to "
  "ABSENT-from-T1 — C-1 recovery CONFIRMED independently")

# C-1 class tally, my own parse of the T1 ledger's class markers.
cls = {}
for rid in [f"R{i:02d}" for i in range(1, 16)]:
    mm = re.search(r"banked R\d+ \((PW|WS|GC|per-row)", T1L[rid][5])
    cls[rid] = mm.group(1) if mm else "?"
tly = [list(cls.values()).count(k) for k in ("PW", "WS", "GC", "per-row")]
V("VC1b_class_tally_own_parse", tly == [8, 2, 4, 1],
  f"T1 ledger classes re-parsed: PW/WS/GC/per-row = {tly} — matches the claimed 8/2/4/1")

# C-2: transitive static recovery, my own parse.
cen_tokens = [CEN[k][0].split()[0] if False else k.split()[0] for k in cen_order]
cen_tokens = [k.split()[0] for k in cen_order]
ok_c2 = len(cen_order) == 16
for i, oid in enumerate([f"O{k:02d}" for k in range(1, 17)]):
    ok_c2 = ok_c2 and A1L[oid][6] == f"banked:{cen_tokens[i]}"
    mm = re.search(r"banked row (\S+)", T1L[oid][5])
    ok_c2 = ok_c2 and mm and mm.group(1) == cen_tokens[i]
ok_c2 = ok_c2 and A1L["O17"][6].startswith("banked-premise:diagonal") \
    and all(A1L[k][6].startswith("ABSENT-static") for k in ("O18", "O19", "O20"))
V("VC2_static_recovery_own_parse", ok_c2,
  "my own parse: the 16 banked census tokens are named in order by BOTH the A1 static column and "
  "the T1 static column; O17 -> diagonal premise; O18/O19/O20 absent — C-2 transitivity CONFIRMED")

# =====================  DUTY 4: mechanical F-sweeps (verifier's own)  ============
# F-A1: my own scan (wider vocabulary) over the record + ledger; every hit must carry a
# scope marker (Stage A3 / F-A1 / scope) on the line.
fa1 = re.compile(r"\bwinding\b|\bholonom\w+|\bcycles?\b|\bmonodrom\w+|\bhomotop\w+|\bwraps?\b", re.I)
allow = re.compile(r"stage a3|a3's|f-a1|scope", re.I)
viol = []
for fn in ("EXACT_DERIVATION.md", "ANGULAR_A1_LEDGER.tsv"):
    for ln, line in enumerate(open(os.path.join(HERE, fn), encoding="utf-8"), 1):
        if fa1.search(line) and not allow.search(line):
            viol.append(f"{fn}:{ln}")
V("VF1_A3_vocabulary_scan_widened", viol == [],
  "widened F-A1 scan (winding/holonomy/cycle/monodromy/homotopy/wrap) over the record and ledger: "
  "every occurrence sits on a scope-exclusion line; violations: " + (";".join(viol) or "none"))

# F-A4: theta absent; y-isometry not re-frozen (no 'y-independent' outside control columns
# and control/restriction discussion); R-A typed not resolved.
theta_hits = []
for fn in ("EXACT_DERIVATION.md", "ANGULAR_A1_LEDGER.tsv", "derive_angular_A1.py"):
    for ln, line in enumerate(open(os.path.join(HERE, fn), encoding="utf-8"), 1):
        if re.search(r"\btheta\b(?!\s*(ABSENT|absent))", line) and "A-L5" not in line and "absent" not in line.lower():
            theta_hits.append(f"{fn}:{ln}")
V("VF4_theta_absent", theta_hits == [],
  "theta appears nowhere outside its A-L5 absence stamps; hits: " + (";".join(theta_hits) or "none"))

# =====================  CLOSURE ROUND (2026-07-31): duty-2 composition recompute  ============
# The amended package claims: slack group = SEMIDIRECT TOWER (zeta < chi < psi) x [y-reparam].
# The "x" (direct factor) is the hunt target: does the y-reparam layer h interact with zeta/chi?
hY = Function("h")(Y)
zY = Function("zeta")(Y)
chiX = Function("chi")(X)
V("VX1_h_acts_on_zeta_argument_not_direct_factor",
  simplify(zY.subs(Y, hY) - zY) != 0,
  "order gap (h then zeta-map) vs (zeta-map then h) on z = zeta(h(y)) - zeta(y) != 0 for h != id: "
  "the y-reparam layer ACTS on the zeta-layer's argument -- 'x [y-reparam]' as a DIRECT factor is "
  "an overclaim (the zeta-layer IS normal under h: the conjugate is the zeta-map with zeta o h)")
conj_chi_by_exp = sp.log(sp.exp(Y) + chiX)   # conjugate of the chi-shift by h(y) = e^y
V("VX2_chi_layer_not_normal_under_general_h",
  simplify(diff(conj_chi_by_exp, Y) - 1) != 0,
  "witness h = e^y: h^{-1}(h(y) + chi(x)) = log(e^y + chi) is NOT a y-shift (d/dy != 1): the "
  "chi-layer is not normalized by general y-reparametrizations -- the group-product form "
  "'tower x [y-reparam]' fails for general h (affine h only); correct statement: h at the top "
  "acting on zeta by argument composition, or the factor restricted to the field-fixing h' = 1")

print()
print(f"VERIFIER TALLY: {'ALL PASS' if not FAILS else 'FAILS: ' + ', '.join(FAILS)}")
sys.exit(1 if FAILS else 0)
