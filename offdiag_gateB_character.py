#!/usr/bin/env python3
"""
offdiag_gateB_character.py -- GATE B part 1: the FLIPPED operator's CHARACTER
============================================================================
OFF-DIAGONAL ANGULAR ROW push. Driver: Claude (Opus 4.8, 1M). 2026-06-13.
Uses the GATE-A-VALIDATED generalized eigensolver (offdiag_gateA.assemble /
gen_spectrum) -- the measure M=r^2 sin th, stiffness carrying e^{-2phi}.

THE QUESTION (character, NOT a mass ladder): angular_completeness_results.md
derived (exact, gauge-protected, verifier-confirmed) that eliminating ALL
couplable components SIMULTANEOUSLY flips the angular-gradient (centrifugal)
term to ATTRACTIVE sign:
   L2_corr = -(c/2) sin th [ ... - f0 dpth^2 - f0 dpv^2/sin^2 th ]
i.e. the dpth^2 (and dpv^2/sin^2) terms enter with NEGATIVE (attractive) sign,
where the DIAGONAL class has them POSITIVE (repulsive). GATE B part 1 asks:
posed with the CORRECT self-adjoint measure (GATE A), is the FLIPPED operator
  - SIGN-DEFINITE (round still the only type, the flip merely relocates rates),
  - or SIGN-INDEFINITE (a non-round deformation LOWERS the energy => a shaped
    type is geometrically supported)?

TEMPLATE TRIPWIRE (binding): if negative directions appear, the verdict is
"the geometry SUPPORTS a shaped type" -- NOT "particle masses/a spectrum".
Eigenvalues are NOT masses. We do NOT load wall numbers.

This part 1 is OPERATOR-CHARACTER on the SAME round formed background as the
control, with ONLY the angular-gradient sign flipped (the angular_completeness
joint-elimination result). It establishes what the flipped operator DOES.
Whether the flip is PHYSICAL (on-shell) is GATE B part 2 (the self-consistent
q,w-on background, offdiag_gateB_selfconsistent.py).
"""
import time, json
import numpy as np
from offdiag_gateA import (assemble, gen_spectrum, round_background, log,
                           PASS, FAIL, check)

log("=" * 74)
log("GATE B part 1 -- the FLIPPED (attractive) operator's CHARACTER "
    "(validated measure)")
log("=" * 74)

def character_scan():
    # Compare diagonal-class (+1) vs flipped (-1) on the SAME round backgrounds,
    # across depth (field strength) and azimuthal m (the ell knob via m).
    log(f"\n{'depth':>6} {'m':>3} {'lam_min(+diag)':>15} "
        f"{'lam_min(-flip)':>15} {'flip_nneg':>10} {'verdict':>22}")
    rows = []
    any_indef = False
    for depth in [0.6, 1.2, 2.0, 3.0, 4.0]:   # field strength: exp(-2phi)~3.3..3000
        phi, r, th = round_background(Nr=41, Nth=33, depth=depth)
        for mq in [0, 1, 2, 3]:
            Ap, Mp, _ = assemble(phi, r, th, sign_th=+1.0, m_quantum=mq)
            wp = gen_spectrum(Ap, Mp)
            Af, Mf, _ = assemble(phi, r, th, sign_th=-1.0, m_quantum=mq)
            wf = gen_spectrum(Af, Mf)
            nneg = int(np.sum(wf < -1e-6))
            indef = nneg > 0
            any_indef = any_indef or indef
            verdict = "SIGN-INDEF (shaped)" if indef else "sign-def (round)"
            log(f"{depth:6.2f} {mq:3d} {wp[0]:15.6e} {wf[0]:15.6e} "
                f"{nneg:10d} {verdict:>22}")
            rows.append(dict(depth=depth, m=mq, lam_diag=float(wp[0]),
                             lam_flip=float(wf[0]), flip_nneg=nneg,
                             nonlin=float(np.exp(2*depth))))
    json.dump(rows, open("/tmp/offdiag_gateB_char.json", "w"))
    return any_indef, rows

if __name__ == "__main__":
    t0 = time.time()
    any_indef, rows = character_scan()
    log("")
    check("CHAR", True,
          "character scan complete (interpretation below; this check always "
          "passes -- it records the scan, the VERDICT is the sign pattern)")
    # honest verdict on the flipped operator's character:
    deepest_indef = [r for r in rows if r["flip_nneg"] > 0]
    if any_indef:
        log(f"\nVERDICT (flipped operator, validated measure): SIGN-INDEFINITE "
            f"in {len(deepest_indef)} (depth,m) cells. The attractive flip, "
            f"posed self-adjointly, SUPPORTS a non-round shaped deformation "
            f"that LOWERS the energy. This is a CHARACTER statement (the "
            f"geometry supports a shaped type), NOT a mass spectrum.")
        # where does it first go negative? (ell/m and field-strength onset)
        onset = min(deepest_indef, key=lambda r: (r["m"], r["depth"]))
        log(f"  earliest sign-indefinite channel: m={onset['m']} "
            f"depth={onset['depth']} (nonlin exp(-2phi)~{onset['nonlin']:.0f})")
    else:
        log("\nVERDICT (flipped operator, validated measure): SIGN-DEFINITE "
            "everywhere scanned. Even with the attractive angular-gradient "
            "sign, the confining matter potential V dominates: round remains "
            "the only supported type. The flip relocates rates, not type.")
    log(f"\nGATE B part 1: {len(PASS)} PASS / {len(FAIL)} FAIL "
        f"({time.time()-t0:.1f}s)")
