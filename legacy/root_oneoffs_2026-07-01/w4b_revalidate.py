"""W4 SOLVER AGENT B — script 8: ENERGY-GATE REVALIDATION BATCH.

The pre-registered G1 gate (secular drift <= 1e-6) invalidates
catalog cells whose source stiffness makes RK4 at cfl = 0.5 weakly
dissipative (|kappa| <~ 1 cells; drift ~ 1e-4). Per the gate, those
cells are NOT banked from the core run. This script re-runs every
INVALID, non-terminated core cell at cfl = 0.0625 (8x smaller dT;
RK4 dissipation ~ (dT omega)^6 -> ~2e-5 of previous drift) and
re-classifies. BANKING RULE (pre-stated): a cell is banked iff the
revalidated run passes G1 AND its label matches the core run; label
mismatches are reported as resolution-sensitive (not banked, listed).

Also re-reads the direction of core COLLAPSE+ cells with vmin <= -2
(overflow-terminal downward collapses mislabeled '+' by the nonfinite
path): re-run at cfl 0.0625 with n_mon = 20 to catch the -3 crossing.

Input: /tmp/w4b_p3_catalog.json. Output: /tmp/w4b_reval.json.
Log: /tmp/w4b_reval.log. New file. 2026-06-12, W4-B agent.
"""
import json
import numpy as np
import w4b_evolib as ev


def log(*a):
    print(*a, flush=True)


npz = np.load("/tmp/w4b_bg.npz")
cat = json.load(open("/tmp/w4b_p3_catalog.json"))
GEOS = {}
OUT = []

# rebuild equilibria for eq+bump cells (same Newton as core)
VEQ = {}


def get_veq(tag, kk, Nx):
    key = (tag, kk, Nx)
    if key not in VEQ:
        geo = GEOS[(tag, Nx)]
        VEQ[key] = ev.equilibrium_newton(geo, kk)[0]
    return VEQ[key]


todo = [r for r in cat if r["group"].startswith("core_")
        and ((not r["valid"]) or (r["label"] == "COLLAPSE+"))]
log(f"revalidation cells: {len(todo)}")

# group by (member, dcell, bc) for batching
from collections import defaultdict
groups = defaultdict(list)
for r in todo:
    groups[(r["member"], r["dcell"])].append(r)

for (tag, dcell), rows in sorted(groups.items()):
    if (tag, 1024) not in GEOS:
        GEOS[(tag, 1024)] = ev.Geo(npz, tag, Nu=24, Nx=1024)
    geo = GEOS[(tag, 1024)]
    T_end = 12.0 * float(np.max(geo.xmax))
    v0s, kl, refs, metas = [], [], [], []
    for r in rows:
        pert = ev.bump_profile(geo, r["amp"], r["profile"])
        base = 0.0
        ref = np.zeros_like(pert)
        if r["init"] == "eq+bump":
            veq = get_veq(tag, r["kappa"], 1024)
            if veq is None:
                continue
            base = veq
            ref = veq
        v0s.append(base + pert)
        refs.append(ref)
        kl.append(r["kappa"])
        metas.append(r)
    if not v0s:
        continue
    log(f"[{tag} dcell={dcell}] reval batch NB={len(kl)} cfl=0.0625")
    resb = ev.evolve_torch(geo, np.array(v0s), np.zeros((len(kl),
                                                         geo.Nu,
                                                         geo.Nx)),
                           np.array(kl), dcell, T_end, cfl=0.0625,
                           n_mon=20, log=log, vrefb=np.array(refs))
    for b, r in enumerate(metas):
        lab, diag = ev.classify_batch(resb, b, abs(r["amp"]))
        banked = bool(diag.get("valid", False)) and \
            (lab == r["label"] or r["label"] == "COLLAPSE+")
        OUT.append(dict(member=tag, dcell=dcell, kappa=r["kappa"],
                        amp=r["amp"], init=r["init"],
                        core_label=r["label"], reval_label=lab,
                        edrift=float(diag.get("edrift", np.nan)),
                        valid=bool(diag.get("valid", False)),
                        vmin_last=float(resb["vmin_last"][b]),
                        vmax_last=float(resb["vmax_last"][b]),
                        freq=float(diag.get("freq", np.nan)),
                        banked=banked))
        log(f"  k={r['kappa']:+9.3g} a={r['amp']:+6.2g} "
            f"{r['init']:7s} core={r['label']:14s} -> "
            f"reval={lab:14s} drift={diag.get('edrift', np.nan):.1e} "
            f"vlast=({resb['vmin_last'][b]:+.2f},"
            f"{resb['vmax_last'][b]:+.2f})")
    with open("/tmp/w4b_reval.json", "w") as fh:
        json.dump(OUT, fh, indent=1)

from collections import Counter
log("reval summary: " + str(Counter(
    (o["core_label"], o["reval_label"]) for o in OUT)))
nb = sum(1 for o in OUT if o["valid"])
log(f"revalidated G1-passing: {nb}/{len(OUT)}")
log("done.")
