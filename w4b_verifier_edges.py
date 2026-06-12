"""W4-B BLIND VERIFIER — attack A (THE FINGERPRINT) + attack C
(independent kappa_c).

Independent recomputation of both band edges (kappa_c spectral gap,
kappa_s static fold) with own machinery (w4b_verifier_lib: t-variable
FEM + own Newton fold; nothing imported from the agent's solvers), on:
  (1) the three claimed members M1/M2/M4 (validation against the
      claimed numbers kc = 0.0706/0.0256/0.0090, ks = 0.13365/0.04863/
      0.01715, ratio = 1.8999/1.9025/1.9026);
  (2) NEW members of the same recipe family never used by the agent:
      different c/c* at gamma = 1, different gamma (0.5 weaker-flow
      multiplier, 2.0, 0.25 with operationally re-bisected seal
      thresholds c*(gamma)).
  (3) per-ray ratio table (does one ray dominate both edges? how does
      the ratio vary across rays = weight shapes?).
Pre-stated reading: the fingerprint claim survives ONLY if every new
member's ratio lands in 1.900 +- 0.004 (their cross-member spread);
a drift beyond ~1% refutes member-independence (family artifact).
Log: /tmp/w4b_verifier_edges.log. New file. 2026-06-12, verifier.
"""
import sys
import time
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl


def log(*a):
    print(*a, flush=True)


t00 = time.time()
CSTAR1 = 0.141644           # claimed anchor c*_3(1.0)
CSTAR05 = 0.09087158 / 2.0  # implied c*_3(0.5) from M4 = 2.0 x

log("=" * 72)
log("PHASE 0: operational seal-threshold check (own bisection)")
log("=" * 72)
cs1 = vl.cstar_bisect(1.0, 0.10, 0.18, niter=24, rtol=1e-8)
log(f"c*(1.0) own bisection = {cs1:.6f}  (claimed anchor {CSTAR1}) "
    f"delta = {cs1 - CSTAR1:+.2e}")
cs05 = vl.cstar_bisect(0.5, 0.03, 0.07, niter=24, rtol=1e-8)
log(f"c*(0.5) own bisection = {cs05:.6f}  (implied {CSTAR05:.6f}) "
    f"delta = {cs05 - CSTAR05:+.2e}")

log("=" * 72)
log("PHASE 1: claimed members M1/M2/M4 (validation of own machinery)")
log("=" * 72)
CLAIMED = {
    "M1": (1.0, 0.18413678, 0.070346, 0.133652),
    "M2": (1.0, 0.28328735, 0.025559, 0.048626),
    "M4": (0.5, 0.09087158, 0.009011, 0.017145),
}
RES = {}
for tag, (gam, c, kc_cl, ks_cl) in CLAIMED.items():
    t0 = time.time()
    mem = vl.Member(gam, c, Nu=24, Nt=4000)
    ed = vl.member_edges(mem)
    RES[tag] = (mem, ed)
    log(f"{tag} (gamma={gam}, c={c}): t_stop={mem.t_stop:.6f}")
    log(f"   kappa_c = {ed['kc']:.6f} (claimed {kc_cl}; "
        f"rel dev {abs(ed['kc']-kc_cl)/kc_cl:.2e}) ray {ed['kray_c']} "
        f"u={mem.u[ed['kray_c']]:+.4f}")
    log(f"   kappa_s = {ed['ks']:.6f} (claimed {ks_cl}; "
        f"rel dev {abs(ed['ks']-ks_cl)/ks_cl:.2e}) ray {ed['kray_s']} "
        f"u={mem.u[ed['kray_s']]:+.4f}")
    log(f"   RATIO   = {ed['ratio']:.5f}   ({time.time()-t0:.0f}s)")

# grid convergence on M1 (Nt doubling)
mem8 = vl.Member(1.0, 0.18413678, Nu=24, Nt=8000)
ed8 = vl.member_edges(mem8, rays=[RES['M1'][1]['kray_c']])
kc4 = RES['M1'][1]['kc']
ks4 = RES['M1'][1]['ks']
log(f"M1 grid check (dominant ray only): Nt=4000 kc={kc4:.6f} "
    f"ks={ks4:.6f}; Nt=8000 kc={ed8['kc']:.6f} ks={ed8['ks']:.6f}; "
    f"rel diffs {abs(ed8['kc']-kc4)/kc4:.1e}, "
    f"{abs(ed8['ks']-ks4)/ks4:.1e}")

log("=" * 72)
log("PHASE 2: NEW members (the fingerprint on unseen family points)")
log("=" * 72)
# thresholds for new gammas (own operational bisection)
cs2 = None
cs025 = None
try:
    # bracket scan for gamma = 2.0
    lo, hi = 0.05, 0.10
    while not vl.sealed(2.0, hi, rtol=1e-8) and hi < 3.0:
        lo = hi
        hi *= 1.6
    while vl.sealed(2.0, lo, rtol=1e-8) and lo > 1e-3:
        hi = lo
        lo /= 1.6
    cs2 = vl.cstar_bisect(2.0, lo, hi, niter=24, rtol=1e-8)
    log(f"c*(2.0) own bisection = {cs2:.6f}")
except Exception as ex:
    log(f"c*(2.0) bisection failed: {ex}")
try:
    lo, hi = 0.02, 0.08
    while not vl.sealed(0.25, hi, rtol=1e-8) and hi < 3.0:
        lo = hi
        hi *= 1.6
    while vl.sealed(0.25, lo, rtol=1e-8) and lo > 1e-3:
        hi = lo
        lo /= 1.6
    cs025 = vl.cstar_bisect(0.25, lo, hi, niter=24, rtol=1e-8)
    log(f"c*(0.25) own bisection = {cs025:.6f}")
except Exception as ex:
    log(f"c*(0.25) bisection failed: {ex}")

NEW = [("V1_g1.0_1.5x", 1.0, 1.5 * cs1),
       ("V2_g1.0_3.0x", 1.0, 3.0 * cs1),
       ("V3_g0.5_1.3x", 0.5, 1.3 * cs05),
       ("V4_g0.5_4.0x", 0.5, 4.0 * cs05)]
if cs2 is not None:
    NEW += [("V5_g2.0_1.3x", 2.0, 1.3 * cs2),
            ("V6_g2.0_2.0x", 2.0, 2.0 * cs2)]
if cs025 is not None:
    NEW += [("V7_g0.25_2.0x", 0.25, 2.0 * cs025)]

table = []
for tag, gam, c in NEW:
    t0 = time.time()
    try:
        mem = vl.Member(gam, c, Nu=24, Nt=4000)
    except AssertionError:
        log(f"{tag} (gamma={gam}, c={c:.6f}): DOES NOT SEAL — skipped")
        continue
    ed = vl.member_edges(mem)
    same_ray = ed['kray_c'] == ed['kray_s']
    log(f"{tag} (gamma={gam}, c={c:.6f}): t_stop={mem.t_stop:.4f} "
        f"kc={ed['kc']:.6f} (ray {ed['kray_c']}) ks={ed['ks']:.6f} "
        f"(ray {ed['kray_s']}) same_ray={same_ray} "
        f"RATIO={ed['ratio']:.5f}  ({time.time()-t0:.0f}s)")
    table.append((tag, gam, c, ed['kc'], ed['ks'], ed['ratio']))

log("=" * 72)
log("PHASE 3: per-ray ratio structure (M1 + one new member)")
log("=" * 72)
for tag in ("M1",):
    mem, ed = RES[tag]
    log(f"-- {tag} per-ray table (u, kappa_c, kappa_s, ratio):")
    for k in sorted(ed['kc_all']):
        kc = ed['kc_all'][k]
        ks = ed['ks_all'][k]
        log(f"   ray {k:2d} u={mem.u[k]:+.4f}  kc={kc:.6g}  "
            f"ks={ks:.6g}  ratio={ks/kc:.5f}")

log("=" * 72)
log("SUMMARY: member -> ratio  (claimed members + new members)")
log("=" * 72)
for tag, (mem, ed) in RES.items():
    log(f"  {tag:14s} gamma={mem.gamma:4.2f} c={mem.c:.6f} "
        f"ratio={ed['ratio']:.5f}")
for tag, gam, c, kc, ks, ratio in table:
    log(f"  {tag:14s} gamma={gam:4.2f} c={c:.6f} ratio={ratio:.5f}")
log(f"flat-case (constant-weight) analytic ratio = "
    f"2 pi^2 / (3 * 3.513830719) = {2*np.pi**2/(3*3.513830719):.5f}")
log(f"total {time.time()-t00:.0f}s")
