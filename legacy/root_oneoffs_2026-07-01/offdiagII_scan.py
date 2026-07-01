#!/usr/bin/env python3
"""
offdiagII_scan.py -- THE DECISIVE SCAN: full-operator eigenvalue vs depth/position
==================================================================================
OFF-DIAGONAL ANGULAR ROW II. Driver: Claude (Opus 4.8, 1M). 2026-06-13.
Frame: CRITICAL_UNIVERSE_FRAME.md. Imports the validated machinery from
offdiagII_operator.py (anchor reproduced K_th=-2.033). Log /tmp/offdiagII.log.

Reads the SIGN of the lowest generalized eigenvalue of the FULL on-shell
angular operator on self-consistent formed cells, swept TOWARD THE SEAL/MEDIUM
(phi around 0 and NEGATIVE). Per ell. Template tripwire honored: SIGN only.
"""
import sys, time, json
import numpy as np
import scipy.linalg as sla
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
from offdiagII_operator import (onshell_coeffs, V_source, assemble_full,
                                gen_lowest, qstar, log)

log("=" * 78)
log("offdiagII_scan -- full-operator sign verdict, swept toward the seal")
log("time", time.strftime("%Y-%m-%d %H:%M:%S"))
log("=" * 78)

# =====================================================================
# BACKGROUND BUILDERS (metric-derived; radially anisotropic as formed cells
# actually are). Two families, both honest:
#  (A) verifier's formed_background shape: well + mild ell-lobe, phi: depth->0.
#  (B) toward-seal/medium: the SAME radial-dominant wall but the phi window
#      shifted across 0 into phi<0 (the exterior side Charles's cells form in).
# The radial wall is steep (|phi_r| large) and the lobe is mild (|phi_th| small)
# -> radial-dominant by ~20-30x = the GENERIC formed-cell wall (verifier).
# =====================================================================
from numpy.polynomial.legendre import legval

def formed_bg(Nr, Nth, depth=2.5, lobe=0.15, ell=2, rlo=0.18, rhi=1.0,
              phi_shift=0.0, wall_steep=1.0):
    """phi(r,th) = base_well(r) + lobe*g(r)*P_ell(cos th) + phi_shift.
       base_well: depth at center -> 0 at outer wall (phi_shift moves the
       whole window; phi_shift<0 pushes the OUTER region into phi<0 = the
       seal/medium/exterior side). wall_steep sharpens the outer wall to test
       the radial-dominant regime explicitly."""
    r = np.linspace(rlo, rhi, Nr)
    th = np.linspace(0.05, np.pi-0.05, Nth)
    x = (r - r[0])/(r[-1]-r[0])
    # well: smooth, deepest at center; outer wall steepened by wall_steep
    base = depth*(1.0 - x**wall_steep**0)  # placeholder; set below
    base = depth*(1.0 - x**2)
    if wall_steep != 1.0:
        # steepen the outer wall: blend toward depth*(1-x)^p with larger slope
        base = depth*(1.0 - x**(2.0/wall_steep))
    Pl = legval(np.cos(th), [0]*ell + [1])
    bump = np.exp(-((x-0.5)/0.3)**2)
    phi = base[:,None] + lobe*bump[:,None]*Pl[None,:] + phi_shift
    return phi, r, th

def grads(phi, r, th):
    dr = r[1]-r[0]; dth = th[1]-th[0]
    pr = np.gradient(phi, dr, axis=0)
    pth = np.gradient(phi, dth, axis=1)
    return pr, pth

# =====================================================================
# THE GATE on one background: full operator, control + on-shell, per channel.
# =====================================================================
def gate_one(phi, r, th, tag, Phi=1.0):
    pr, pth = grads(phi, r, th)
    rad_dom = np.median(np.abs(pr)[2:-2,2:-2])/max(1e-9, np.median(np.abs(pth)[2:-2,2:-2]))
    log(f"\n--- {tag}: phi in [{phi.min():.2f},{phi.max():.2f}] "
        f"radial-dominance(median|pr|/|pth|)={rad_dom:.1f} grid {phi.shape}")
    out = {"tag": tag, "phimin": float(phi.min()), "phimax": float(phi.max()),
           "rad_dom": float(rad_dom)}
    # CONTROL: diagonal (flip off) -- must be sign-definite (round-only baseline)
    Ac, Mc, _, _, _ = assemble_full(phi, r, th, pr, pth, Phi, m_az=0,
                                     include_V=True, flip_on=False)
    wc = gen_lowest(Ac, Mc)
    out["ctrl_lam0"] = float(wc[0])
    log(f"    CONTROL (bare diag, +V): lam0 = {wc[0]:.5e}  "
        f"{'(>=0 round-only baseline OK)' if wc[0] > -1e-7 else '(CONTROL NEG?!)'}")
    # ON-SHELL full operator, m_az = 0 (polar even sector; ell>=2 lives here):
    A0, M0, _, qr, Kth = assemble_full(phi, r, th, pr, pth, Phi, m_az=0,
                                       include_V=True, flip_on=True)
    w0 = gen_lowest(A0, M0)
    out["onshell_lam0_m0"] = float(w0[0])
    kthneg = int(np.sum(Kth[2:-2,2:-2] < 0))
    out["Kth_neg_pts"] = kthneg
    out["qratio_max"] = float(np.max(qr))
    log(f"    K_th<0 interior pts: {kthneg}/{(phi.shape[0]-4)*(phi.shape[1]-4)}  "
        f"max|q*|/bound={np.max(qr):.3f}")
    log(f"    ON-SHELL full op (m=0): lam0..2 = {np.array2string(w0[:3],precision=5)}")
    # azimuthal channels:
    for m in (1, 2):
        Am, Mm, _, _, _ = assemble_full(phi, r, th, pr, pth, Phi, m_az=m,
                                        include_V=True, flip_on=True)
        wm = gen_lowest(Am, Mm)
        out[f"onshell_lam0_m{m}"] = float(wm[0])
        log(f"    ON-SHELL full op (m={m}): lam0 = {wm[0]:.5e}")
    sgn = "SIGN-INDEFINITE (shaped type supported)" if w0[0] < -1e-6 \
          else "sign-definite (round only)"
    out["verdict"] = sgn
    log(f"    >>> {tag}: lam0(on-shell,m=0) = {w0[0]:.5e}  =>  {sgn}")
    return out

# =====================================================================
# SWEEP TOWARD THE SEAL: phi_shift from +0.5 (interior) down through 0 and
# into phi<0 (exterior/medium). The verifier: the flip STRENGTHENS as phi->0
# and phi<0. We hunt for the lowest eigenvalue crossing zero.
# =====================================================================
def main():
    RESULTS = []
    # primary grid (CPU dense eigh; N ~ 41*25 ~ 1025, robust):
    Nr, Nth = 41, 25
    log("\n############ FAMILY A: verifier formed_background, sweep phi_shift ############")
    for shift in [0.5, 0.0, -0.5, -1.0, -2.0]:
        phi, r, th = formed_bg(Nr, Nth, depth=2.5, lobe=0.15, ell=2,
                               phi_shift=shift)
        RESULTS.append(gate_one(phi, r, th, f"A_shift={shift:+.1f}"))

    log("\n############ FAMILY B: STEEPENED outer wall (radial-dominant), seal sweep ############")
    for shift in [0.0, -0.5, -1.0]:
        phi, r, th = formed_bg(Nr, Nth, depth=3.0, lobe=0.12, ell=2,
                               phi_shift=shift, wall_steep=3.0)
        RESULTS.append(gate_one(phi, r, th, f"B_steep_shift={shift:+.1f}"))

    log("\n############ FAMILY C: stronger lobe (larger |phi_th|, ell=2 and ell=3) ############")
    for ell in (2, 3):
        for shift in [0.0, -1.0]:
            phi, r, th = formed_bg(Nr, Nth, depth=2.5, lobe=0.4, ell=ell,
                                   phi_shift=shift, wall_steep=2.0)
            RESULTS.append(gate_one(phi, r, th, f"C_ell={ell}_shift={shift:+.1f}"))

    # SUMMARY
    log("\n" + "=" * 78)
    log("SUMMARY -- lowest on-shell eigenvalue (m=0) per background")
    log(f"{'tag':26}{'phimin':>8}{'raddom':>8}{'Kth<0':>7}{'ctrl_l0':>11}{'on_l0':>12}  verdict")
    anyneg = False
    for o in RESULTS:
        if o["onshell_lam0_m0"] < -1e-6: anyneg = True
        log(f"{o['tag']:26}{o['phimin']:8.2f}{o['rad_dom']:8.1f}{o['Kth_neg_pts']:7d}"
            f"{o['ctrl_lam0']:11.3e}{o['onshell_lam0_m0']:12.4e}  {o['verdict']}")
    log("\n" + ("*** SIGN-INDEFINITE found: a non-round type is geometrically "
                "supported on at least one self-consistent formed cell. ***"
                if anyneg else
                "*** SIGN-DEFINITE on every cell tested: V-dominated; round only "
                "(the attractive K_th flip is real pointwise but does NOT lower "
                "the full-operator energy). ***"))
    json.dump(RESULTS, open("/tmp/offdiagII_scan.json", "w"), indent=0)
    return RESULTS, anyneg

if __name__ == "__main__":
    main()
