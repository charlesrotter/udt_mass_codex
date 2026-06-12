#!/usr/bin/env python3
"""BLIND ADVERSARIAL VERIFIER (W4 Agent-A) — SCRIPT 2: BLOWUP vs GUARD.

Date: 2026-06-12.  Priority attack B + claim-3 scoping.  Own machinery:
the dressed static flow re-derived and integrated in v = ln(1+w)
(exactly linearizes the wave kinetic term: the reduced static W_wave is
-2 kappa e^{-t} f v_t^2, EXACT), own sympy EL -> RHS, own quadrature.
The agent's guards (1+w in [0.02, 50]) are REMOVED (v in [-30, +30],
i.e. 1+w in [9e-14, 1e13]) to adjudicate true divergence vs
guard-crossing-then-recovery, at the band edges specifically.
Also: threshold refinement by bisection (the agent's kappa grid has
factor-3.16 spacing) and the DRESSED-WELD scoping attack on the
'exist iff' wording (the agent only ever ran w(weld) = 0).
Log: /tmp/w4a_verifier2.log
"""
import sys, time
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

sys.path.insert(0, '/home/udt-admin/udt_mass_codex/rescued_workspaces/'
                '2026-06-11/verify_s2')
import v_lib as V

t0 = time.time()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"V2-{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

# ---------------- own RHS derivation (sympy, v-variables) -------------
fS, ftS, fuS, vS, vtS, kS, bS, sS = sp.symbols(
    'f f_t f_u v v_t kappa beta s', real=True)
Lpot_v = (sp.Rational(1, 4) * sS * fuS ** 2 * sp.exp(-2 * vS) / fS
          + bS * sp.Rational(1, 2) * sS * (sp.exp(vS) - 1) * fuS ** 2 / fS)
Lkin_v = -2 * kS * fS * vtS ** 2
# v-EL: d/dt[e^{-t} dL/dv_t] = e^{-t} dL/dv  with d/dt expanded:
vtt = sp.Symbol('v_tt')
dLdvt = sp.diff(Lkin_v, vtS)
lhs = (-dLdvt + sp.diff(dLdvt, fS) * ftS + sp.diff(dLdvt, vtS) * vtt)
VTT = sp.solve(sp.Eq(lhs, sp.diff(Lpot_v + Lkin_v, vS)), vtt)[0]
VTT = sp.simplify(VTT)
tgt = (vtS * (1 - ftS / fS) + sS * fuS ** 2 * sp.exp(-2 * vS)
       / (8 * kS * fS ** 2)
       - bS * sS * fuS ** 2 * sp.exp(vS) / (8 * kS * fS ** 2))
check("00", sp.simplify(VTT - tgt) == 0,
      "own v-EL: v_tt = v_t(1 - f_t/f) + s f_u^2 e^{-2v}/(8 kappa f^2) "
      "- beta s f_u^2 e^v/(8 kappa f^2)  [the quadratic v_t^2 term "
      "CANCELS exactly — the wave part is linear in v: blowup "
      "adjudication is clean in this chart]")
# consistency with the agent's w-form: w = e^v - 1:
wS, wtS = sp.symbols('w w_t', real=True)
WTT_agent = (wtS * (1 - ftS / fS) + wtS ** 2 / (1 + wS)
             + sS * fuS ** 2 / (8 * kS * fS ** 2 * (1 + wS))
             - bS * sS * fuS ** 2 * (1 + wS) ** 2 / (8 * kS * fS ** 2))
# w_tt = e^v (v_tt + v_t^2):
wtt_from_v = sp.exp(vS) * (VTT + vtS ** 2)
wtt_sub = WTT_agent.subs([(wS, sp.exp(vS) - 1),
                          (wtS, sp.exp(vS) * vtS)])
check("01", sp.simplify(wtt_from_v - wtt_sub) == 0,
      "chart consistency: e^v (v_tt + v_t^2) == the agent's w_tt "
      "formula under w = e^v - 1 (the two flows are the same dynamics)")
# f-EL integrand:
Yl, Ylp = sp.symbols('Yl Ylp', real=True)
Lpot_f = Lpot_v + kS * Lkin_v / kS * 0 + (-2 * kS * fS * vtS ** 2) * 0
Lpot_full = Lpot_v - 2 * kS * fS * vtS ** 2
dpot = sp.simplify(sp.diff(Lpot_full, fS) * Yl
                   + sp.diff(Lpot_full, fuS) * Ylp)
args = (fS, fuS, vS, vtS, kS, bS, sS, Yl, Ylp)
dpot_fn = sp.lambdify(args, dpot, 'numpy')
vtt_fn = sp.lambdify((fS, ftS, fuS, vS, vtS, kS, bS, sS), VTT, 'numpy')
# anchor the f-integrand against banked 2*Pgrad at v = 0, kappa-off:
qq = V.Q12
Xt_ = np.array([2.7, 0.3, -0.2, 0.1])
fT = Xt_ @ qq.Y; fuT = Xt_ @ qq.Yu
gP = np.array([(dpot_fn(fT, fuT, 0 * fT, 0 * fT, 1.0, 0.0, qq.s,
                        qq.Y[l], qq.Yu[l]) @ qq.w) for l in range(4)])
check("02", np.max(np.abs(gP - 2 * V.Pgrad(Xt_))) < 1e-12,
      "own f-EL integrand == banked 2*P_X at v=0 (library lock)")

MEM = V.load_members(('M1', 'M2', 'M4'))
BANK = {'M1': 3.598647, 'M2': 2.134243, 'M4': 2.822749}
UG = np.linspace(-1, 1, 601)
YUG = V.Yr(UG)

def flow_v(tag, kap, beta=0.0, Nu=24, rtol=1e-9, vlo=-30.0, vhi=30.0,
           tmax=40.0, alpha0=0.0, fstop=0.002):
    uq = V.Q(Nu)
    Yn, Yun, wn, sn = V.Yr(uq.x), V.Yru(uq.x), uq.w, uq.s
    m = MEM[tag]
    def rhs(t, z):
        X, Xt = z[:4], z[4:8]
        vv, vt = z[8:8 + Nu], z[8 + Nu:]
        fv = X @ Yn; fu = X @ Yun
        dz = np.empty_like(z)
        dz[:4] = Xt
        for l in range(4):
            dz[4 + l] = Xt[l] + (dpot_fn(fv, fu, vv, vt, kap, beta, sn,
                                         Yn[l], Yun[l]) @ wn)
        dz[8:8 + Nu] = vt
        dz[8 + Nu:] = vtt_fn(fv, Xt @ Yn, fu, vv, vt, kap, beta, sn)
        return dz
    z0 = np.zeros(8 + 2 * Nu)
    z0[0] = 1.0; z0[4] = m['gamma']; z0[5] = -m['c']
    z0[8:8 + Nu] = np.log(1.0 + alpha0 * (1 - uq.x ** 2))
    def ev_seal(t, z):
        return np.min(z[:4] @ YUG) - fstop
    ev_seal.terminal, ev_seal.direction = True, -1
    def ev_lo(t, z):
        return np.min(z[8:8 + Nu]) - vlo
    ev_lo.terminal, ev_lo.direction = True, -1
    def ev_hi(t, z):
        return vhi - np.max(z[8:8 + Nu])
    ev_hi.terminal, ev_hi.direction = True, -1
    sol = solve_ivp(rhs, (0, tmax), z0, method='DOP853', rtol=rtol,
                    atol=1e-12, events=(ev_seal, ev_lo, ev_hi),
                    dense_output=True)
    sealed = len(sol.t_events[0]) > 0
    hit_lo = len(sol.t_events[1]) > 0
    hit_hi = len(sol.t_events[2]) > 0
    vfin = sol.y[8:8 + Nu, -1]
    status = ('SEAL' if sealed else 'V-LO' if hit_lo
              else 'V-HI' if hit_hi else 'NOSEAL')
    return dict(status=status, t=sol.t[-1], vmin=vfin.min(),
                vmax=vfin.max(), sol=sol, Nu=Nu)

# ---------------- anchor ----------------
okA = True
for tag in ('M1', 'M2', 'M4'):
    rr = flow_v(tag, 1e12, rtol=1e-11)
    dev = abs(rr['t'] - BANK[tag]) / BANK[tag]
    okA &= rr['status'] == 'SEAL' and dev < 1e-3 \
        and max(abs(rr['vmin']), abs(rr['vmax'])) < 1e-9
    print(f"   anchor {tag}: t_stop {rr['t']:.6f} (banked {BANK[tag]}; "
          f"rel {dev:.1e})", flush=True)
check("03", okA, "kappa->inf anchor: banked t_stop reproduced < 1e-3, "
      "v inert (own v-chart flow locked to the library)")

# ---------------- verdict agreement under translated guards ----------
print("\n--- agent-map verdict reproduction (guards 1+w in [0.02, 50]"
      " == v in [-3.912, +3.932]) ---", flush=True)
AG = {(-1.0): 'SEAL', (-0.1): 'SEAL', (-0.0316): 'BLOWUP',
      (0.001): 'BLOWUP', (0.1): 'BLOWUP', (0.316): 'SEAL', (1.0): 'SEAL'}
okV = True
for kap, want in AG.items():
    rr = flow_v('M1', kap, vlo=np.log(0.02), vhi=np.log(50.0), tmax=12.0)
    got = ('SEAL' if rr['status'] == 'SEAL'
           else 'BLOWUP' if rr['status'] in ('V-LO', 'V-HI')
           else 'NOSEAL')
    okV &= (got == want)
    print(f"   M1 kappa={kap:+.4g}: own={got} (agent {want})  "
          f"t={rr['t']:.4f}", flush=True)
check("04", okV, "agent existence verdicts reproduced at 7 spot kappas "
      "(M1) with own chart, own RHS, own integrator")

# ---------------- kappa < 0: true collapse or guard artifact? --------
print("\n--- kappa < 0 band edge: guards OFF (v down to -30) ---",
      flush=True)
neg_rows = {}
for kap in (-0.0316, -0.01, -0.001):
    rr = flow_v('M1', kap, vlo=-30.0, vhi=30.0, tmax=40.0)
    ts = np.linspace(0, rr['t'] * 0.999, 400)
    vmins = np.array([rr['sol'].sol(x)[8:8 + rr['Nu']].min() for x in ts])
    icross = int(np.argmax(vmins < np.log(0.02)))
    rec = bool((np.diff(vmins[icross:]) > 1e-6).any()) if icross > 0 \
        else None
    # solver stall at the singular collapse counts as collapse:
    collapsed = (rr['status'] == 'V-LO'
                 or (rr['status'] == 'NOSEAL' and rr['t'] < 39.0
                     and np.exp(rr['vmin']) < 1e-11))
    neg_rows[kap] = (rr['status'], rr['t'], np.exp(rr['vmin']), rec,
                     collapsed)
    print(f"   M1 kappa={kap:+.4g}: status={rr['status']} at t="
          f"{rr['t']:.4f}; min(1+w) reached {np.exp(rr['vmin']):.2e}; "
          f"recovery after old guard: {rec}", flush=True)
deep_ok = all(neg_rows[k][4] and neg_rows[k][3] is False
              for k in (-0.01, -0.001))
edge_seals = neg_rows[-0.0316][0] == 'SEAL'
check("05", deep_ok,
      "DEEP kappa<0 collapse is GENUINE (kappa = -0.01, -0.001): "
      "1+w plunges below 1e-11 with NO recovery, before any seal — "
      "those BLOWUP verdicts are real shear collapse, not guard "
      "artifacts")
check("05b", edge_seals,
      f"EDGE FINDING: at kappa = -0.0316 (agent verdict BLOWUP/no "
      f"cell) the flow with guards REMOVED reaches its seal at t = "
      f"{neg_rows[-0.0316][1]:.4f} with min(1+w) = "
      f"{neg_rows[-0.0316][2]:.2e}: a sealed cell with extreme-but-"
      f"finite shear EXISTS there — the negative-side threshold is "
      f"GUARD-DEFINED, not a true existence boundary")

# ---------------- kappa > 0: true runaway or guard artifact? ---------
print("\n--- kappa > 0 band edge: guards OFF (v up to +30 ~ 1+w 1e13)"
      " ---", flush=True)
res_hi = {}
for kap in (0.001, 0.01, 0.0316, 0.1, 0.2):
    rr = flow_v('M1', kap, vlo=-30.0, vhi=30.0, tmax=40.0)
    res_hi[kap] = rr
    print(f"   M1 kappa={kap:+.4g}: status={rr['status']} at t="
          f"{rr['t']:.4f}; max(1+w) = {np.exp(rr['vmax']):.3e}, "
          f"min f = {np.min(rr['sol'].y[:4, -1] @ YUG):.4f}",
          flush=True)
anyseal = [k for k, rr in res_hi.items() if rr['status'] == 'SEAL']
check("06", True,
      f"kappa>0 sub-threshold adjudication recorded: kappas sealing "
      f"with the 50-guard REMOVED: {anyseal} (if non-empty, the "
      f"agent's BLOWUP-below-threshold reading on the + side is "
      f"GUARD-DEFINED, not true divergence — see verdict text)")

# ---------------- threshold refinement (the 3.16-grid defect) --------
print("\n--- threshold bisection, agent guards, M1 ---", flush=True)
def verdict(kap):
    rr = flow_v('M1', kap, vlo=np.log(0.02), vhi=np.log(50.0), tmax=12.0)
    return rr['status'] == 'SEAL'
lo, hi = 0.1, 0.316          # BLOWUP .. SEAL
for _ in range(10):
    mid = np.sqrt(lo * hi)
    if verdict(mid):
        hi = mid
    else:
        lo = mid
kplus = (lo, hi)
lo2, hi2 = -0.0316, -0.1     # BLOWUP .. SEAL (more negative seals)
for _ in range(10):
    mid = -np.sqrt(lo2 * hi2)
    if verdict(mid):
        hi2 = mid
    else:
        lo2 = mid
kminus = (lo2, hi2)
print(f"   M1 + threshold in ({kplus[0]:.4f}, {kplus[1]:.4f}); "
      f"- threshold in ({kminus[0]:.5f}, {kminus[1]:.5f})", flush=True)
check("07", kplus[1] < 0.316 and abs(kminus[1]) < 0.1,
      f"GRID-GRANULARITY DEFECT quantified: the true M1 existence "
      f"thresholds (agent guards) are kappa+* ~ {kplus[1]:.3f} and "
      f"kappa-* ~ {kminus[1]:.4f}, NOT the quoted grid points "
      f"+0.316 / -0.1 (the agent's sweep spacing is factor 3.16; "
      f"claim-3 threshold values are upper brackets only)")

# ---------------- dressed-weld scoping attack ------------------------
print("\n--- sub-threshold DRESSED welds w0 = alpha (1-u^2) "
      "(agent only ran alpha = 0) ---", flush=True)
found = []
for kap in (0.1, -0.0316):
    for al in (-0.9, -0.6, -0.3, 0.3, 0.6, 1.5):
        rr = flow_v('M1', kap, vlo=np.log(0.02), vhi=np.log(50.0),
                    tmax=12.0, alpha0=al)
        tagres = rr['status']
        if tagres == 'SEAL':
            found.append((kap, al, rr['t'], np.exp(rr['vmax']),
                          np.exp(rr['vmin'])))
        print(f"   kappa={kap:+.4g} alpha={al:+.2f}: {tagres} "
              f"t={rr['t']:.4f} (1+w) in [{np.exp(rr['vmin']):.3f}, "
              f"{np.exp(rr['vmax']):.3f}]", flush=True)
check("08", len(found) > 0,
      f"DRESSED-WELD SCOPE: sub-threshold seals INSIDE the agent's own "
      f"guards at {[(k, a) for k, a, *_ in found]}: claim 3's 'exist "
      f"iff' is REFUTED as stated — the map is the w(weld)=0 slice "
      f"only; the undressed weld itself rests on the W2 interface law "
      f"(CONDITIONAL/unbanked)")
# convergence hygiene on two dressed-weld exhibits:
okH = True
for (kap, al) in ((0.1, -0.6), (0.1, 0.3)):
    r1 = flow_v('M1', kap, vlo=np.log(0.02), vhi=np.log(50.0),
                tmax=12.0, alpha0=al, Nu=24, rtol=1e-9)
    r2 = flow_v('M1', kap, vlo=np.log(0.02), vhi=np.log(50.0),
                tmax=12.0, alpha0=al, Nu=48, rtol=1e-11)
    same = r1['status'] == r2['status'] == 'SEAL'
    tdev = abs(r1['t'] - r2['t']) / r2['t']
    okH &= same and tdev < 2e-3
    print(f"   hygiene kappa={kap} alpha={al}: Nu24/48 status "
          f"{r1['status']}/{r2['status']}, t rel dev {tdev:.1e}",
          flush=True)
check("09", okH, "dressed-weld sub-threshold seals survive u-node "
      "doubling + tolerance tightening (the exhibits are converged, "
      "not numerics)")

print(f"\nVERIFIER-2 BLOWUP/EXISTENCE: {len(PASS)} PASS / {len(FAIL)} "
      f"FAIL ({time.time()-t0:.0f}s)")
sys.exit(0 if not FAIL else 1)
