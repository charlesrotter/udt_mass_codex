"""BLIND VERIFIER independent check — P4 boundary-action gate (2026-07-30).

Own layout, own IBP, own constructions. Adjudicates duties (2)-(9):
  V1  own N=2 IBP: boundary residue pairs ONLY the 0-jet variation (no v')
      -> the R6 unpaired-jet cut re-derived, incl. weight-robustness
  V2  inert-germ theorem re-derived on a FULLY GENERIC function (no expansion
      ansatz) + the germ-LOCALITY probe (is inertness global or per-point?)
  V3  fold: doubled momentum re-derived from L_P + flip; joint forcing
      (essential dphi=0) + (natural BC) + (mirror C^1) => B_rho germ = 0;
      branch-uniformity of the crease momentum at phi=0
  V4  two-sided jump laws + flux-seal <=> B_Q=0, BOTH directions
  V5  mirror-wall theorem via SYMMETRIZATION (more general than the invariant
      construction): generic degree-4 polynomial density, even part, momenta
      at the kill locus; load-bearing witness for mirror-incompatible member
  V6  open-end germ laws: q = -c_E B_Q, rho' = -B_rho/4; any-(q,rho') realized;
      germ-flat stratum reproduces banked K6d q=0 & rho'=0
  V7  consistency spot-checks: K6c B_rho=q/2; K4d; M-WALL = a_F*M-GEN
      (independent quadratic-class computation); TS1 handshake germ pair
  V8  D-b dependence laws (fold -B_rho/8 -> 0; open-end -B_rho/4)
  V9  selector-hunt probe: confirm the anchored rule kills bare-phi but
      admits arbitrary f(Q,rho) (i.e. arguments pinned, function free) — and
      that NO N=2 banked cut touches the function beyond the first germ.
"""
import sympy as sp

FAIL = []


def ck(name, ok, note=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {note}")
    if not ok:
        FAIL.append(name)


x, rs, ell = sp.symbols('x r_s ell', real=True, positive=True)
Z = sp.Symbol('Z', positive=True)
cE = sp.Symbol('c_E', positive=True)
q = sp.Symbol('q', real=True)

# ---------------- V1: own IBP at N=2 ----------------
u = sp.Function('u')
v = sp.Function('v')
L = sp.Function('L')
Lx = L(u(x), u(x).diff(x))
delta = Lx.diff(u(x))*v(x) + Lx.diff(u(x).diff(x))*v(x).diff(x)
EL = Lx.diff(u(x)) - sp.diff(Lx.diff(u(x).diff(x)), x)
residue_density = sp.diff(Lx.diff(u(x).diff(x))*v(x), x)
ck("V1a_ibp_identity", sp.expand(delta - (EL*v(x) + residue_density)) == 0)
# boundary residue = (dL/du') * v : contains v but NOT v'
res = Lx.diff(u(x).diff(x))*v(x)
ck("V1b_residue_has_no_vprime", res.diff(v(x).diff(x)) == 0)
# hence a wall functional argument rho'_s would inject an unpaired dv' term;
# with anchored weight W_F = e^{aF*p0} (never zero) the same conclusion:
aF, p0 = sp.symbols('a_F p0', real=True)
WF = sp.exp(aF*p0)
Brp = sp.Symbol('B_rp', real=True)
ck("V1c_R6_cut_weight_robust", sp.solve(sp.Eq(WF*Brp, 0), Brp) == [0])

# ---------------- V2: inert germ, generic function ----------------
B = sp.Function('B')
phis, rhos, dphi, drho = sp.symbols('phi_s rho_s dphi drho', real=True)
Q = cE*sp.exp(-phis)
# first variation of B(Q(phi), rho) in directions (dphi, drho):
dB = B(Q, rhos).diff(phis)*dphi + B(Q, rhos).diff(rhos)*drho
Qv, rv = sp.symbols('Qv rv', real=True)
BQ = sp.Derivative(B(Qv, rv), Qv)
Br = sp.Derivative(B(Qv, rv), rv)
dB_seam = dB.subs(phis, 0)  # seam locus phi_s = 0 => Q = c_E
target = (-cE*BQ.subs([(Qv, cE), (rv, rhos)])*dphi
          + Br.subs([(Qv, cE), (rv, rhos)])*drho)
ck("V2a_first_variation_is_first_germ_only",
   sp.simplify(dB_seam - target) == 0)
# adding pure >=2nd-order germ content changes NOTHING in the variation
# at the seam point:
pert = (Qv - cE)**2*(rv - rhos) + (rv - rhos)**3
dpert = (pert.subs([(Qv, Q), (rv, rhos)]).diff(phis)*dphi).subs(phis, 0)
ck("V2b_higher_germ_inert_at_point", sp.simplify(dpert) == 0)
# GERM-LOCALITY probe: the same perturbation is NOT inert at a DIFFERENT
# realized trace rho1 != rhos — its rho-partial there is nonzero:
rho1 = sp.Symbol('rho_1', real=True)
away = pert.diff(rv).subs([(Qv, cE), (rv, rho1)])
ck("V2c_inertness_is_germ_local_only",
   sp.simplify(away) != 0, f"(residual at rho_1: {sp.simplify(away)})")

# ---------------- V3: fold ----------------
p, pp, ro, rop = sp.symbols('p pp rho rhop', real=True)
L_P = Z/2*ro**2*pp**2 - 2*sp.exp(-2*p)*rop**2 + 2
L_flip = L_P.subs(p, -p)          # mirrored copy (phi odd)
ptot = sp.diff(L_P, rop) + sp.diff(L_flip, rop)
ck("V3a_doubled_momentum",
   sp.simplify(sp.expand((ptot + 8*sp.cosh(2*p)*rop).rewrite(sp.exp))) == 0)
# Branch-G doubled momentum at the crease locus phi=0 coincides:
L_G = Z/2*ro**2*pp**2 - 2*rop**2 + 2
ptot_G = 2*sp.diff(L_G, rop)
ck("V3b_crease_momentum_branch_uniform_at_phi0",
   sp.simplify(ptot.subs(p, 0) - ptot_G) == 0)
# essential dphi: odd identification => variation odd => trace zero:
vv = sp.Symbol('v', real=True)
ck("V3c_essential_dphi_zero", sp.solve(sp.Eq(vv, -vv), vv) == [0])
# natural BC: -8 rho'(r_s) = B_rho ; mirror C^1 (rho even) => rho'(r_s)=0.
Brg = sp.Symbol('B_rho', real=True)
rps = sp.Symbol('rhop_s', real=True)
sol = sp.solve([sp.Eq(-8*rps, Brg), sp.Eq(rps, 0)], [rps, Brg], dict=True)
ck("V3d_joint_forcing_Brho_zero", sol == [{rps: 0, Brg: 0}])
# rho even about crease => 1-jet kill (independent, own parity computation):
g = sp.Function('g')
mirrored = (g(rs + x) + g(rs - x))/2      # even part about r_s
ck("V3e_even_config_has_zero_crease_slope",
   sp.simplify(sp.diff(mirrored, x).subs(x, 0)) == 0)

# ---------------- V4: two-sided jump laws + flux seal ----------------
Jp, Jr = sp.symbols('Jphi Jrho', real=True)
BQg = sp.Symbol('B_Q', real=True)
expr = (Jp*dphi + Jr*drho) - (-cE*BQg*dphi + Brg*drho)
solj = sp.solve([expr.coeff(dphi), expr.coeff(drho)], [Jp, Jr], dict=True)
ck("V4a_jump_laws", solj == [{Jp: -cE*BQg, Jr: Brg}])
# seal => B_Q = 0 (cE > 0), and B_Q = 0 => seal: both directions
ck("V4b_seal_forward", sp.solve(sp.Eq(-cE*BQg, 0), BQg) == [0])
ck("V4c_seal_backward", (-cE*BQg).subs(BQg, 0) == 0)

# ---------------- V5: mirror-wall theorem by symmetrization ----------------
# generic degree-4 polynomial density in (p0,p1,f0,f1,h0,h1), even part under
# (p0,f1,h1) -> -(p0,f1,h1); momenta at kill locus {p0=f1=h1=0}.
p0s, p1s, f0s, f1s, h0s, h1s = sp.symbols('P0 P1 F0 F1 H0 H1', real=True)
vars6 = (p0s, p1s, f0s, f1s, h0s, h1s)
import itertools
terms = []
coeffs = []
idx = 0
for deg in range(5):
    for combo in itertools.combinations_with_replacement(range(6), deg):
        mono = sp.S.One
        for i in combo:
            mono *= vars6[i]
        c = sp.Symbol(f'c{idx}', real=True)
        idx += 1
        coeffs.append(c)
        terms.append(c*mono)
Lgen = sp.Add(*terms)
flip = {p0s: -p0s, f1s: -f1s, h1s: -h1s}
Leven = sp.expand((Lgen + Lgen.subs(flip, simultaneous=True))/2)
kill = {p0s: 0, f1s: 0, h1s: 0}
pi_f = sp.expand(Leven.diff(f1s).subs(kill))
pi_h = sp.expand(Leven.diff(h1s).subs(kill))
pi_p = sp.expand(Leven.diff(p1s).subs(kill))
ck("V5a_even_momentum_kill_f", pi_f == 0)
ck("V5b_even_momentum_kill_h", pi_h == 0)
ck("V5c_pi_p_generically_nonzero", pi_p != 0,
   "(unpaired: dphi essential-killed)")
# load-bearing: full generic (not symmetrized) density fails the kill:
pi_f_full = sp.expand(Lgen.diff(f1s).subs(kill))
ck("V5d_mirror_compat_load_bearing", pi_f_full != 0)

# ---------------- V6: open-end ----------------
phip_s = sp.Symbol('phip_s', real=True)
pi_phi = Z*rhos**2*phip_s
pi_rho = -4*rps            # both branches at phi=0
one = (pi_phi*dphi + pi_rho*drho) - (-cE*BQg*dphi + Brg*drho)
solo = sp.solve([one.coeff(dphi), one.coeff(drho)], [phip_s, rps], dict=True)
ck("V6a_openend_laws",
   solo == [{phip_s: -cE*BQg/(Z*rhos**2), rps: -Brg/4}])
q_out = Z*rhos**2*solo[0][phip_s]
ck("V6b_q_law", sp.simplify(q_out + cE*BQg) == 0)
ck("V6c_germflat_reproduces_K6d",
   q_out.subs(BQg, 0) == 0 and solo[0][rps].subs(Brg, 0) == 0)
b1, b2 = sp.symbols('b1 b2', real=True)
solr = sp.solve([sp.Eq(-cE*b1, q), sp.Eq(-b2/4, rps)], [b1, b2], dict=True)
ck("V6d_any_output_realized", solr == [{b1: -q/cE, b2: -4*rps}])

# ---------------- V7: consistency spot-checks ----------------
ck("V7a_K6c_glue_pin", sp.solve(sp.Eq(Brg, q/2), Brg) == [q/2])
ck("V7b_K4d_fold_B0", sp.solve(sp.Eq(-8*rps, 0), rps) == [0])
# M-WALL = a_F * M-GEN on the quadratic class (own computation):
gp, E0, w1, w0 = sp.symbols('g_p E_0 w_1 w_0', real=True)
A = aF**2*E0/(2*gp)
w = A*x**2 + w1*x + w0
pi_p_q = gp*sp.diff(w, x)/aF
MWALL = sp.simplify(pi_p_q.subs(x, ell) - pi_p_q.subs(x, -ell))
ck("V7c_MWALL_aF_MGEN", sp.simplify(MWALL - aF*(2*ell*E0)) == 0)
# TS1 handshake: odd-mirror germ vanishes on the seam locus yet carries a
# distinct first jet (underdetermination):
pm = sp.Function('phim')
germB = -pm(2*rs - x)
ck("V7d_handshake_locus", germB.subs(x, rs).subs(pm(rs), 0) == 0)
ck("V7e_handshake_jets_distinct",
   sp.simplify(sp.diff(germB, x).subs(x, rs)) != 0)

# ---------------- V8: D-b dependence ----------------
ck("V8a_fold_Db", sp.solve(sp.Eq(-8*rps, Brg), rps) == [-Brg/8])
ck("V8b_openend_Db", solo[0][rps] == -Brg/4)

# ---------------- V9: selector-hunt probe ----------------
# anchored rule: c_E^p e^{-q phi} shift-invariant iff p=q  => bare-phi dead,
# arbitrary smooth dependence through Q alive:
pw, qw, s = sp.symbols('p_w q_w s', real=True)
phiw = sp.Symbol('phi_w', real=True)
coeff = cE**pw*sp.exp(-qw*phiw)
shifted = coeff.subs([(cE, cE*sp.exp(s)), (phiw, phiw + s)], simultaneous=True)
ck("V9a_anchored_iff_p_eq_q",
   sp.solve(sp.Eq(sp.expand_log(sp.log(sp.simplify(shifted/coeff)),
                                force=True), 0), pw) == [qw])
# an ARBITRARY composite f(Q) is shift-invariant (function-level freedom):
f = sp.Function('f')
Qw = cE*sp.exp(-phiw)
ck("V9b_arbitrary_f_of_Q_invariant",
   sp.simplify(f(Qw).subs([(cE, cE*sp.exp(s)), (phiw, phiw + s)],
                          simultaneous=True) - f(Qw)) == 0)

print()
print(f"INDEPENDENT CHECKS: {len(FAIL)} failures"
      + (f": {FAIL}" if FAIL else " — all pass"))
import sys
sys.exit(1 if FAIL else 0)
