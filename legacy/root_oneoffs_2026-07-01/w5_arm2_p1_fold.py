#!/usr/bin/env python3
"""W5 ARM-2 — SCRIPT 4: P1' STATIC EXISTENCE / THE NEW FOLD MAP.

Date: 2026-06-12.  HYPOTHESIS-GRADE at every kappa != 0 (numerics =
telescope).  System: the untruncated species (w5_arm2_sym.py, exact);
sources carry the factor (1 - 2 kappa/f); TRUE units cc = 2 PRIMARY
(banked-unit conversions kappa_banked = kappa_true * c_member/2
printed per member; adjudication sym G1 + gates G-B).

QUESTIONS (pre-registered):
 Q1 fold per (member, branch, sign): where do all-ray static dressed
    equilibria exist?  The W4 OFF-branch Bratu fold ks_true is the
    species-OFF baseline; the untruncated source is NOT a one-lambda
    Bratu family (kappa enters through the locus too) — direct
    kappa-continuation.
 Q2 the ON branch: v = 0 is no longer static (sym C5).  Do dressed
    ON-equilibria exist, where, and how far do they sit from
    v_alg = (1/3) ln(1 - 2 kappa/f)?
 Q3 locus signature: do equilibrium profiles develop structure at
    f(t) = 2 kappa (curvature concentration)?
 Q4 domain class: full domain (W4-comparable) AND trust windows t5/t1.

PRE-STATED FAILURE/VALIDITY CRITERIA:
 - every banked edge needs Nt 4000 -> 8000 agreement <= 1e-3 rel,
   else reported NON-CONVERGED;
 - species-OFF fold must reproduce gates G-A/G-B values (internal
   re-check) else STOP;
 - Newton failures are existence verdicts ONLY when the damped Newton
   with warm-start continuation fails from BOTH directions (up- and
   down-continuation); single-path failures are retried.
HARDEST-SKEPTICISM NOTE (binding): a fold SHIFT is the hoped-for
outcome ("the locus matters"); the null (fold tracks the W4 value at
the small kappa_s where (1-2k/f) ~ 1 on the support of b) is stated
UP FRONT as the likely result for members whose ks_true * 2 << min f
on the b-support.  Compute, don't hope.

Output: /tmp/w5_arm2_p1.npz + log /tmp/w5_arm2_p1.log.
New file.  2026-06-12, W5 Arm-2 agent.
"""
import sys, time, json
import numpy as np
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl
import w5_arm2_lib as w5

t0 = time.time()
def log(*a):
    print(*a, flush=True)

MEMBERS = {"M1": (1.0, 0.18413678), "M2": (1.0, 0.28328735),
           "M4": (0.5, 0.09087158)}
TW = {"M1": (1.6383, 2.2357), "M2": (1.168, 1.5313),
      "M4": (1.7106, 2.1312)}        # (t1, t5) from banked headers

MEM = {t: vl.Member(g, c, Nu=24, Nt=4000) for t, (g, c) in
       MEMBERS.items()}
OUT = {}

log("=" * 72)
log("P1' FOLD MAP (TRUE units, cc = 2; conversions printed)")
log("=" * 72)
for tag, (gam, cm) in MEMBERS.items():
    log(f"-- {tag}: kappa_banked = kappa_true * {cm/2:.6f} "
        f"(2/c_m = {2/cm:.4f})")

for tag in MEMBERS:
    mem = MEM[tag]
    cm = MEMBERS[tag][1]
    for domlbl, t_b in (("full", None), ("t5", TW[tag][1]),
                        ("t1", TW[tag][0])):
        geo = w5.GeoW5(mem, t_b=t_b, Nt=4000, Nx=256)
        frng = (geo.f_t.min(), geo.f_t.max())
        log(f"\n== {tag} [{domlbl}] t_b={geo.t_b:.4f}  f range "
            f"({frng[0]:.4g}, {frng[1]:.4g}); locus interior for "
            f"kappa_true in ({frng[0]/2:.4g}, {frng[1]/2:.4g})")
        for dcell, sgn in ((False, +1), (False, -1), (True, +1),
                           (True, -1)):
            lbl = f"{'ON' if dcell else 'OFF'} sign={sgn:+d}"
            # species OFF baseline (W4 truncation) and species ON:
            res = {}
            for spc in (False, True):
                ks, vinfo = w5.kappa_s_member(
                    geo, dcell, cc=2.0, species=spc, sign=sgn,
                    klo=1e-4, khi=400.0)
                res[spc] = ks
            ksOFF, ksON = res[False], res[True]
            OUT[f"{tag}_{domlbl}_{lbl}_ksW4"] = (
                np.nan if ksOFF is None else ksOFF)
            OUT[f"{tag}_{domlbl}_{lbl}_ksW5"] = (
                np.nan if ksON is None else ksON)
            def fmt(x):
                return ("none@klo" if x is None else
                        ("no-fold<400" if np.isinf(x) else f"{x:.6f}"))
            log(f"  {lbl:12s}: fold kappa_s  W4-trunc = {fmt(ksOFF)}"
                f"   UNTRUNCATED = {fmt(ksON)}")
    # convergence check on the headline (full-domain OFF +) fold
    geoA = w5.GeoW5(mem, t_b=None, Nt=4000, Nx=256)
    geoB = w5.GeoW5(mem, t_b=None, Nt=8000, Nx=256)
    kA, _ = w5.kappa_s_member(geoA, False, cc=2.0, species=True,
                              sign=+1, klo=1e-4, khi=400.0)
    kB, _ = w5.kappa_s_member(geoB, False, cc=2.0, species=True,
                              sign=+1, klo=1e-4, khi=400.0)
    if kA is not None and kB is not None and np.isfinite(kA) \
            and np.isfinite(kB):
        log(f"  convergence (OFF,+,full): Nt4000 {kA:.6f}  Nt8000 "
            f"{kB:.6f}  rel {abs(kA-kB)/kB:.1e} "
            f"[{'CONVERGED' if abs(kA-kB)/kB <= 1e-3 else 'NON-CONVERGED'}]")
    else:
        log(f"  convergence (OFF,+,full): Nt4000 {kA}  Nt8000 {kB} "
            "(non-finite branch: fold-absence verdicts compared)")

# --------------------------------------------------------------------
log("\n" + "=" * 72)
log("Q2/Q3: ON-branch dressing + locus structure (M1 full domain)")
log("=" * 72)
mem = MEM["M1"]
geo = w5.GeoW5(mem, t_b=None, Nt=4000, Nx=256)
for kap in (0.05, 0.2, 0.5, 1.0, 2.0, -0.5, -2.0):
    veq, fails = w5.equilibrium_member(geo, kap, dcell=True, cc=2.0,
                                       species=True)
    if veq is None:
        log(f"  ON kappa={kap:+.3g}: NO all-ray equilibrium "
            f"(fail rays {fails})")
        continue
    tl = geo.locus_t(kap)
    k_dom = int(np.argmax(geo.b_t.sum(0)))
    v_d = veq[k_dom]
    # locus curvature diagnostic on the dominant ray:
    h = geo.tg[1] - geo.tg[0]
    curv = np.abs(np.gradient(np.gradient(v_d, h), h))
    i_loc = (np.nan if not np.isfinite(tl[k_dom])
             else int(round(tl[k_dom] / h)))
    # algebraic equilibrium where defined:
    fac = 1 - 2 * kap / geo.f_t[:, k_dom]
    valg = np.where(fac > 0, np.log(np.maximum(fac, 1e-300)) / 3,
                    np.nan)
    dev_alg = (np.nan if np.all(~np.isfinite(valg)) else
               float(np.nanmax(np.abs(v_d - valg))))
    cm_curv = float(np.sum(geo.tg * curv) / max(np.sum(curv), 1e-300))
    log(f"  ON kappa={kap:+.3g}: min v_eq={veq.min():+.4f} max="
        f"{veq.max():+.4f}; dominant-ray t_locus="
        f"{tl[k_dom] if np.isfinite(tl[k_dom]) else np.nan:.4f}; "
        f"curvature center-of-mass t={cm_curv:.4f}; "
        f"max|v_eq - v_alg|={dev_alg:.4f}")
    OUT[f"M1_ONeq_{kap:+.3g}"] = veq[k_dom]
for kap in (0.05, 0.2, 0.5, 1.0, 2.0, -0.5, -2.0):
    veq, fails = w5.equilibrium_member(geo, kap, dcell=False, cc=2.0,
                                       species=True)
    st = ("none (rays %s)" % fails[:4] if veq is None else
          f"min={veq.min():+.4f} max={veq.max():+.4f}")
    if veq is not None:
        OUT[f"M1_OFFeq_{kap:+.3g}"] = veq[int(np.argmax(geo.b_t.sum(0)))]
    log(f"  OFF kappa={kap:+.3g}: equilibrium {st}")
OUT["M1_tg"] = geo.tg
OUT["M1_fdom"] = geo.f_t[:, int(np.argmax(geo.b_t.sum(0)))]

np.savez("/tmp/w5_arm2_p1.npz", **{k: np.asarray(v)
                                   for k, v in OUT.items()})
log(f"\ndone ({time.time()-t0:.0f}s); banked to /tmp/w5_arm2_p1.npz")
