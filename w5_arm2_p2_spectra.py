#!/usr/bin/env python3
"""W5 ARM-2 — SCRIPT 5: P2' SPECTRA on the untruncated species.

Date: 2026-06-12.  HYPOTHESIS-GRADE at kappa != 0.  TRUE units cc = 2.
Operator (exact, sym E1): per-ray SL pencil about the dressed static
background vbar (the clean object; v = 0 is off-shell on BOTH branches
under untruncation — frozen readouts carried as labeled variants):
  -(p psi')' - [(1/(4 kappa))(1 - 2 kappa/f) e^{-2 vbar}
                + beta (1/(8 kappa)) e^{vbar}] b psi = omega^2 m psi.

PRE-REGISTERED QUESTIONS:
 Q1 dressed gap edges kappa_c' per (member, branch, sign, domain) and
    THE RATIO kappa_s'/kappa_c' (does ~1.90 survive untruncation?).
 Q2 locus structure (kappa in the locus regime): does the pencil
    develop turning-point structure (eigenfunctions repelled from the
    f < 2 kappa side); are there NEW discrete states localized at the
    locus (mode-count and localization-center diagnostics vs the
    species-OFF operator at identical kappa)?
 Q3 bands vs lines: per-u radial spectra; no w_u stiffness exists in
    the untruncated system either (D_alg is jet-free) — the band
    verdict can only change QUANTITATIVELY (widths); report.
 Q4 box control: t1-vs-t5 trust-cut sensitivity of omega^2_1 — W4
    recorded 31-35%; has the seal-cut dependence weakened (the locus
    wall repels modes from the seal for kappa > 0)?
 Q5 BC robustness: weld Neumann vs Dirichlet at spot kappas.

VALIDITY: GPU batched eigvalsh with diagonal-mass reduction (no
Cholesky anywhere) + CPU spot asserts (in-lib); grid doubling
Ncoarse 600 -> 1200 on representatives; pre-stated: any representative
drifting > 1e-2 rel in omega^2_1 is reported NON-CONVERGED.
SKEPTICISM (binding): trapped/locus states are the hoped-for outcome;
the null (locus invisible: potential ~ b weight support never overlaps
the locus) is checked FIRST via the overlap integral b(t)*|1-2k/f|.

Output: /tmp/w5_arm2_p2.npz; log /tmp/w5_arm2_p2.log.
New file.  2026-06-12, W5 Arm-2 agent.
"""
import sys, time
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
      "M4": (1.7106, 2.1312)}
MEM = {t: vl.Member(g, c, Nu=24, Nt=4000) for t, (g, c) in
       MEMBERS.items()}
OUT = {}

KGRID = np.array([1e-3, 1e-2, 0.05, 0.1, 0.2, 0.3, 0.5, 0.767, 1.0,
                  1.45, 2.0, 3.0, 5.0, 10.0, 100.0, 1e3])
KGRID = np.concatenate([-KGRID[::-1], KGRID])

# --------------------------------------------------------------------
log("=" * 72)
log("Q1: dressed gap edges + the ratio (full domain + t5)")
log("=" * 72)
RATIO = {}
for tag in MEMBERS:
    mem = MEM[tag]
    for domlbl, t_b in (("full", None), ("t5", TW[tag][1])):
        geo = w5.GeoW5(mem, t_b=t_b, Nt=4000, Nx=256)
        row = {}
        for dcell in (True, False):
            for spc in (False, True):
                kc, info = w5.kappa_c_member(
                    geo, dcell, cc=2.0, species=spc, dressed=True,
                    klo=1e-4, khi=50.0)
                row[(dcell, spc)] = kc
        log(f"  {tag} [{domlbl}]: dressed kappa_c'  "
            f"ON: W4 {row[(True, False)]}, W5 {row[(True, True)]};  "
            f"OFF: W4 {row[(False, False)]}, W5 {row[(False, True)]}")
        for k_, v_ in row.items():
            OUT[f"{tag}_{domlbl}_kc_dc{int(k_[0])}_sp{int(k_[1])}"] = (
                np.nan if v_ is None else v_)
        RATIO[(tag, domlbl)] = row

# --------------------------------------------------------------------
log("=" * 72)
log("Q2: locus structure (M1; full domain; OFF branch; kappa > 0)")
log("=" * 72)
mem = MEM["M1"]
geo = w5.GeoW5(mem, t_b=None, Nt=4000, Nx=256)
k_dom = int(np.argmax(geo.b_t.sum(0)))
k_seal = int(np.argmin(geo.f_t.min(0)))
log(f"  dominant-b ray k={k_dom} u={mem.u[k_dom]:+.4f}, f range "
    f"({geo.f_t[:, k_dom].min():.4g}, {geo.f_t[:, k_dom].max():.4g}); "
    f"seal-adjacent ray k={k_seal} u={mem.u[k_seal]:+.4f}, f range "
    f"({geo.f_t[:, k_seal].min():.4g}, {geo.f_t[:, k_seal].max():.4g})")
h = geo.tg[1] - geo.tg[0]
for kray, raylbl in ((k_dom, "dom"), (k_seal, "seal")):
    for kap in (0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.767, 1.0, 1.45, 2.0,
                3.0):
        tl = geo.locus_t(kap)
        # null check first: b-weight overlap with the flipped region
        b = geo.b_t[:, kray]
        f = geo.f_t[:, kray]
        wflip = float(np.sum(b[f < 2 * kap]) / max(np.sum(b), 1e-300))
        # dressed backgrounds (OFF) where they exist — EACH system
        # about ITS OWN equilibrium (comparability fix, on record):
        veq, fails = w5.equilibrium_member(geo, kap, dcell=False,
                                           cc=2.0, species=True)
        veq4, _ = w5.equilibrium_member(geo, kap, dcell=False,
                                        cc=2.0, species=False)
        vb = None if veq is None else veq[kray]
        vb4 = None if veq4 is None else veq4[kray]
        w2_5, V5, tk = w5.pencil_ray(geo, kray, kap, False, 2.0, True,
                                     vbar=vb, nev=6)
        w2_4, V4, _ = w5.pencil_ray(geo, kray, kap, False, 2.0, False,
                                    vbar=vb4, nev=6)
        def locdiag(V):
            ps = V[:, 0] ** 2
            ps = ps / np.sum(ps)
            cm = float(np.sum(tk * ps))
            wd = float(np.sqrt(np.sum((tk - cm) ** 2 * ps)))
            return cm, wd
        cm5, wd5 = locdiag(V5)
        cm4, wd4 = locdiag(V4)
        nneg5 = int(np.sum(w2_5 < 0))
        nneg4 = int(np.sum(w2_4 < 0))
        tloc = tl[kray]
        log(f"  [{raylbl}] kappa={kap:5.3f}: t_locus="
            f"{tloc if np.isfinite(tloc) else np.nan:6.4f}  b-wt "
            f"flipped={wflip:5.1%} | "
            f"W5[{'dressed' if vb is not None else 'FROZEN '}] "
            f"w2_1..3={np.array2string(w2_5[:3], precision=3)} "
            f"nneg={nneg5} cm/wd={cm5:.3f}/{wd5:.3f} | W4 w2_1..3="
            f"{np.array2string(w2_4[:3], precision=3)} nneg={nneg4} "
            f"cm/wd={cm4:.3f}/{wd4:.3f}")
        OUT[f"locus_{raylbl}_{kap:.3f}_w2_W5"] = w2_5
        OUT[f"locus_{raylbl}_{kap:.3f}_w2_W4"] = w2_4
        OUT[f"locus_{raylbl}_{kap:.3f}_mode1_W5"] = V5[:, 0]
OUT["locus_tk"] = tk
OUT["locus_fdom"] = geo.f_t[:-1, k_dom]
OUT["locus_fseal"] = geo.f_t[:-1, k_seal]

# --------------------------------------------------------------------
log("=" * 72)
log("Q3: band structure across rays (GPU batch; M1; dressed where "
    "available, frozen elsewhere — labels per row)")
log("=" * 72)
VB = {}
VB4 = {}
for kap in KGRID:
    veq, _ = w5.equilibrium_member(geo, kap, dcell=False, cc=2.0,
                                   species=True)
    VB[kap] = veq
    veq4, _ = w5.equilibrium_member(geo, kap, dcell=False, cc=2.0,
                                    species=False)
    VB4[kap] = veq4
ndress = sum(1 for v in VB.values() if v is not None)
log(f"  dressed OFF equilibria exist at {ndress}/{len(KGRID)} kappas "
    f"(W5); {sum(1 for v in VB4.values() if v is not None)} (W4)")
w2g = w5.pencil_member_gpu(geo, KGRID, dcell=False, cc=2.0,
                           species=True, vbars=VB, nev=4, Ncoarse=600)
w2g4 = w5.pencil_member_gpu(geo, KGRID, dcell=False, cc=2.0,
                            species=False, vbars=VB4, nev=4,
                            Ncoarse=600)
for i, kap in enumerate(KGRID):
    b1 = w2g[i, :, 0]
    b2 = w2g[i, :, 1]
    lab = "DRESSED" if VB[kap] is not None else "FROZEN"
    lab4 = "DRESSED" if VB4[kap] is not None else "FROZEN"
    log(f"  kappa={kap:+9.3g} W5[{lab:7s}]: band1 [{b1.min():9.3f},"
        f"{b1.max():9.3f}] gap-to-2 {b2.min()-b1.max():9.3f}  | "
        f"W4[{lab4:7s}] band1 [{w2g4[i, :, 0].min():9.3f},"
        f"{w2g4[i, :, 0].max():9.3f}]")
OUT["bands_W5"] = w2g
OUT["bands_W4"] = w2g4
OUT["bands_K"] = KGRID
# convergence representatives (dressed rows only — the frozen
# sub-fold rows carry ~1e6-scale eigenvalues whose conditioning is
# outside the doubling question; amended after first run, on record):
KREP = [-1.0, 1.0, 3.0]
irep = [int(np.argmin(np.abs(KGRID - kk))) for kk in KREP]
w2h = w5.pencil_member_gpu(geo, np.array(KREP), dcell=False, cc=2.0,
                           species=True,
                           vbars={kk: VB[KGRID[i]] for kk, i in
                                  zip(KREP, irep)},
                           nev=4, Ncoarse=1200)
dr = np.max(np.abs(w2h[:, :, 0] - w2g[irep, :, 0])
            / np.maximum(np.abs(w2h[:, :, 0]), 1e-9))
log(f"  grid doubling Ncoarse 600->1200 on kappa={KREP}: max rel "
    f"drift omega^2_1 = {dr:.2e} "
    f"[{'CONVERGED' if dr <= 1e-2 else 'NON-CONVERGED'}]")

# --------------------------------------------------------------------
log("=" * 72)
log("Q4: box control — t1 vs t5 trust-cut sensitivity (M1, OFF)")
log("=" * 72)
geo1 = w5.GeoW5(mem, t_b=TW["M1"][0], Nt=4000, Nx=256)
geo5 = w5.GeoW5(mem, t_b=TW["M1"][1], Nt=4000, Nx=256)
for kap in (0.5, 1.0, 2.0, 5.0, -1.0, -5.0):
    rows = []
    for spc in (True, False):
        v1, _ = w5.equilibrium_member(geo1, kap, False, 2.0, spc)
        v5_, _ = w5.equilibrium_member(geo5, kap, False, 2.0, spc)
        k1 = int(np.argmax(geo1.b_t.sum(0)))
        w21 = w5.pencil_ray(geo1, k1, kap, False, 2.0, spc,
                            vbar=None if v1 is None else v1[k1],
                            nev=1)[0][0]
        w25 = w5.pencil_ray(geo5, k1, kap, False, 2.0, spc,
                            vbar=None if v5_ is None else v5_[k1],
                            nev=1)[0][0]
        sh = abs(w21 - w25) / max(abs(w21), 1e-12)
        rows.append((spc, w21, w25, sh))
    log(f"  kappa={kap:+6.3g}: W5 w2_1(t1)={rows[0][1]:9.4f} "
        f"w2_1(t5)={rows[0][2]:9.4f} shift={rows[0][3]:6.1%}   | "
        f"W4 shift={rows[1][3]:6.1%}")

# --------------------------------------------------------------------
log("=" * 72)
log("Q5: BC robustness (weld N vs D; M1 full, OFF, dressed)")
log("=" * 72)
for kap in (0.5, 2.0, -1.0):
    veq, _ = w5.equilibrium_member(geo, kap, False, 2.0, True)
    vbk = None if veq is None else veq[k_dom]
    wN = w5.pencil_ray(geo, k_dom, kap, False, 2.0, True, vbar=vbk,
                       nev=2, bc_weld='N')[0]
    wD = w5.pencil_ray(geo, k_dom, kap, False, 2.0, True, vbar=vbk,
                       nev=2, bc_weld='D')[0]
    log(f"  kappa={kap:+5.2f}: weld-N w2_1,2={wN}  weld-D w2_1,2={wD}")

np.savez("/tmp/w5_arm2_p2.npz", **{k: np.asarray(v)
                                   for k, v in OUT.items()})
log(f"\ndone ({time.time()-t0:.0f}s); banked to /tmp/w5_arm2_p2.npz")
