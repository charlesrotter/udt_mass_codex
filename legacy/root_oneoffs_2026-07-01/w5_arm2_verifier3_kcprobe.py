"""W5 ARM-2 VERIFIER #3 — kc' CONVENTION PROBE.

Finding under investigation: the ON-branch dressed background is
NON-UNIQUE below the claimed kc'.  Cold Newton (init v=0) converges to
an equilibrium with w2min < 0; warm continuation from large kappa
tracks a DIFFERENT equilibrium with w2min > 0.  The claimed kc' is
therefore suspected to be the COLD-START convention edge, while the
stable-branch (warm) convention gives a smaller kc' and different
ratios.

This script: (a) recomputes kc' under the COLD convention (equilibria
re-solved from v=0 at every bisection point — the claimant's
kappa_c_member does exactly this: its cache is dead code) for the
claimed members M1/M2/M4 and the fresh members F1/F2/F3 on full + t5;
(b) probes the warm/stable branch at its own edge (existence vs
stability); (c) tabulates ratios under BOTH conventions.

Imports only w4b_verifier_lib + my own verifier module.  VB5,
2026-06-12.
"""
import sys
import numpy as np

sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl
import w5_arm2_verifier3_fresh as V

LOG = open("/tmp/w5_arm2_verifier3_fresh.log", "a")


def log(*a):
    msg = " ".join(str(x) for x in a)
    print(msg, flush=True)
    LOG.write(msg + "\n")
    LOG.flush()


def w2min_cold(geo, kappa):
    """claimant-convention: equilibria from v=0, no warm start."""
    w2s = []
    for k in range(geo.Nu):
        v = V.newton_ray(geo, k, kappa, dcell=True)
        if v is None:
            return None
        w2s.append(V.pencil_lowest(geo, k, kappa, True, vbar=v))
    return min(w2s)


def kc_cold(geo, klo=1e-4, khi=50.0, nbis=34):
    wlo = w2min_cold(geo, klo)
    whi = w2min_cold(geo, khi)
    if not ((wlo is None or wlo < 0) and (whi is not None and whi >= 0)):
        return None
    lo, hi = klo, khi
    for _ in range(nbis):
        mid = np.sqrt(lo * hi)
        wm = w2min_cold(geo, mid)
        if wm is None or wm < 0:
            lo = mid
        else:
            hi = mid
    return float(np.sqrt(lo * hi))


def stable_branch_at_edge(geo, kc_warm):
    """probe the warm/stable branch just below the warm edge: does the
    equilibrium still EXIST (stability edge) or vanish (fold)?"""
    for fac, lab in ((1.001, "just above"), (0.999, "just below"),
                     (0.97, "3% below")):
        kap = kc_warm * fac
        vw = None
        ok = True
        for kk in np.geomspace(1.0, kap, 30):
            vw = V.newton_ray(geo, 16, kk, dcell=True, vinit=vw)
            if vw is None:
                ok = False
                break
        # full member warm check
        wm, _ = V.w2min_dressed(geo, kap)
        log(f"    {lab} warm edge (kappa={kap:.6f}): ray16 warm "
            f"branch {'EXISTS' if ok else 'GONE'}; member warm "
            f"w2min={'None' if wm is None else f'{wm:.5f}'}")


MEMBERS = [
    ("M1", 1.0, 0.18413678, 2.2357, (0.678857, 0.041396)),
    ("M2", 1.0, 0.28328735, 1.5313, (0.161096, 0.024358)),
    ("M4", 0.5, 0.09087158, 2.1312, (0.177554, 0.024529)),
]


def main(fresh):
    log("=" * 72)
    log("[T-PROBE] kc' CONVENTION PROBE (cold-start vs stable-branch)")

    log("\n A) cold-convention kc' on claimed members (vs claim):")
    for name, g, c, t5, (ckfull, ckt5) in MEMBERS:
        sol = vl.flow(g, c)
        for win, tb, ck in (("full", None, ckfull), ("t5", t5, ckt5)):
            geo = V.Geo(sol, t_b=tb)
            kc = kc_cold(geo)
            ksw = {"M1": (0.915696, 0.076078), "M2": (0.255321, 0.044942),
                   "M4": (0.282425, 0.045333)}[name][0 if win == "full"
                                                     else 1]
            dev = abs(kc - ck) / ck
            log(f"  {name}/{win}: kc_cold={kc:.6f} (claim {ck}) "
            f"rel dev {dev:.2e} -> {'MATCH' if dev <= 1e-2 else 'NO'}; "
                f"ratio_cold={ksw / kc:.4f}")

    log("\n B) stable-branch probe at the warm edge (M1/t5, warm "
        "kc'=0.038225):")
    sol = vl.flow(1.0, 0.18413678)
    geo = V.Geo(sol, t_b=2.2357)
    stable_branch_at_edge(geo, 0.038225)

    log("\n C) cold-convention kc' on FRESH members:")
    for name, g, c, t5 in fresh:
        sol = vl.flow(g, c)
        for win, tb in (("full", None), ("t5", t5)):
            geo = V.Geo(sol, t_b=tb)
            kc = kc_cold(geo)
            ks, kray, _ = V.ks_member(geo)
            log(f"  {name}/{win}: ks={ks:.6f} kc_cold={kc:.6f} "
                f"ratio_cold={ks / kc:.4f}")


if __name__ == "__main__":
    # fresh members: (name, gamma, c, t5) — c from the main run's
    # cstar bisects, t5 from the main run's trust cuts (read its log).
    fresh = [tuple(x) for x in eval(sys.argv[1])]
    main(fresh)
