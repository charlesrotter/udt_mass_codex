"""W4 SOLVER AGENT B — script 5: P3 PERSISTENCE CATALOG (production).

FROZEN-f nonlinear evolutions of the w-channel on the banked library
backgrounds M1/M2/M4 (anchor-verified in w4b_backgrounds.py), GPU
batched (torch float64, V100), classifier and validity gates as
pre-registered in w4b_evolib.py (committed before this run).

ALL RESULTS HYPOTHESIS-GRADE (kappa != 0 underived; numerics are the
telescope, not the proof).

PRE-REGISTERED DESIGN (fixed here, before execution):
  CORE GRID: members {M1, M2, M4} x D_cell {ON, OFF} x
    kappa {+-1e-3, +-1e-2, +-1e-1, +-1, +-1e1, +-1e2, +-1e3}
    (ON adds {0.7, 0.9, 1.1, 1.3} x kappa_c(member) refinement) x
    amp {1e-4, 1e-2, 1e-1, 0.3, -0.1, -0.3} ; profile g1; BCs
    (inner Dirichlet, outer Neumann reflecting); T_end = 12 max(x_max);
    Nx = 1024 (grid-trust from w4b_gates.py T-G3); frame = primary.
  OFF INIT CLASSES: 'bump' (w = perturbation on w = 0) and 'eq+bump'
    (perturbation on the Newton static equilibrium v_eq where it
    exists) - both labeled.
  SUBSETS (M1): BC-robustness {(robin1, neumann), (dirichlet,
    dirichlet), (dirichlet, outgoing)} at kappa {0.5 kc, 2 kc, -1} x
    {ON} + kappa {+-1} x {OFF}; profiles {g2, g3} and kicked
    (vt0 != 0) at the same kappas; diagonal-frame OFF at kappa +-1.
  EQUILIBRIUM FOLD: kappa_s(member) = infimum kappa > 0 with a Newton
    static equilibrium (D_cell OFF primary), log-bisection, Nx = 1024.
  GRID DOUBLING (gate G2): >= 6 representatives spanning the observed
    labels re-run at Nx = 2048; classification must match to be banked.

PRE-STATED FAILURE/GRADING CRITERIA (P5, from the declaration):
  - NO kappa with durable shaped matter (RING/BREATHER valid runs)
    => wave-sector completion FALSIFIED as the missing piece (decisive);
  - a kappa-BAND of durable shaped matter => numerical fingerprint of
    the selection principle (derivation target);
  - durable matter at ALL kappa => persistence does not select here.
  - P3-F3: the dynamical ON-branch threshold must match the spectral
    kappa_c (w4b_gates.py) within 10%, else the band claim is NOT
    banked (reported as discrepancy).
  - Gates G1 (energy 1e-6), G2 (doubling), G3 (GPU-CPU 1e-11) binding.

Checkpoints: /tmp/w4b_p3_<group>.npz after each batch; catalog
/tmp/w4b_p3_catalog.json. Log: /tmp/w4b_p3.log (flush-per-line).
New file. 2026-06-12, W4-B agent.
"""
import json
import sys
import time
import numpy as np
import w4b_evolib as ev


def log(*a):
    print(*a, flush=True)


npz = np.load("/tmp/w4b_bg.npz")
lin = np.load("/tmp/w4b_lingap.npz")
NX = 1024
AMPS = [1e-4, 1e-2, 1e-1, 0.3, -0.1, -0.3]
K0 = [s * 10.0**e for e in range(-3, 4) for s in (+1, -1)]
BC0 = ("dirichlet", "neumann")
CAT = []
WAVE = {}

GEOS = {tag: ev.Geo(npz, tag, Nu=24, Nx=NX) for tag in ("M1", "M2", "M4")}


def run_group(tag, dcell, kappas, amps, inits, bc=BC0, profile="g1",
              frame="primary", kicked=False, gname="", veq_map=None,
              Nx_override=None):
    geo = GEOS[tag] if Nx_override is None else ev.Geo(npz, tag, Nu=24,
                                                       Nx=Nx_override)
    T_end = 12.0 * float(np.max(geo.xmax))
    v0s, vt0s, kl, al, il = [], [], [], [], []
    for kk in kappas:
        for aa in amps:
            for init in inits:
                if init == "eq+bump":
                    if veq_map is None or veq_map.get(kk) is None:
                        continue
                    base = veq_map[kk]
                else:
                    base = 0.0
                pert = ev.bump_profile(geo, aa, profile)
                v0 = base + pert
                vt0 = np.zeros_like(v0)
                if kicked:
                    vt0 = ev.bump_profile(geo, abs(aa), profile) * 5.0
                v0s.append(v0)
                vt0s.append(vt0)
                kl.append(kk)
                al.append(aa)
                il.append(init)
    if not v0s:
        return
    v0b = np.array(v0s)
    vt0b = np.array(vt0s)
    vrefb = np.array([veq_map[k] if (i == "eq+bump" and veq_map)
                      else np.zeros_like(v0b[0])
                      for k, i in zip(kl, il)]) if veq_map else None
    log(f"[{gname}] batch NB={len(kl)} tag={tag} dcell={dcell} bc={bc} "
        f"profile={profile} frame={frame} kicked={kicked} "
        f"Nx={geo.Nx} T_end={T_end:.2f}")
    t0 = time.time()
    resb = ev.evolve_torch(geo, v0b, vt0b, np.array(kl), dcell, T_end,
                           frame=frame, bc=bc, log=log, vrefb=vrefb)
    log(f"[{gname}] done in {time.time() - t0:.0f}s "
        f"(nstep={resb['nstep']})")
    conserving = bc[1] != "outgoing"
    for b in range(len(kl)):
        lab, diag = ev.classify_batch(resb, b, abs(al[b]), conserving)
        row = dict(group=gname, member=tag, frame=frame,
                   dcell=bool(dcell), bc="/".join(bc), profile=profile,
                   init=il[b], kicked=bool(kicked), kappa=float(kl[b]),
                   amp=float(al[b]), Nx=int(geo.Nx), label=lab,
                   freq=float(diag.get("freq", np.nan)),
                   rate=float(diag.get("rate_final", np.nan)),
                   env_max=float(diag.get("env_max", np.nan)),
                   edrift=float(diag.get("edrift", np.nan)),
                   valid=bool(diag.get("valid", True)),
                   T_term=float(diag.get("T_term", np.nan)),
                   zc=int(diag.get("zero_crossings", -1)))
        CAT.append(row)
        key = (gname, tag, dcell, kl[b], al[b], il[b])
        if b % 7 == 0:
            WAVE[str(key)] = np.column_stack([resb["T"],
                                              resb["probe"][b]])
    np.savez(f"/tmp/w4b_p3_{gname}.npz",
             env=resb["env"], probe=resb["probe"], T=resb["T"],
             kl=np.array(kl), al=np.array(al))
    with open("/tmp/w4b_p3_catalog.json", "w") as fh:
        json.dump(CAT, fh, indent=1)


# ---------------------------------------------------------------- folds
log("=" * 72)
log("EQUILIBRIUM FOLD SEARCH (D_cell OFF primary, kappa > 0)")
log("=" * 72)
FOLD = {}
VEQ = {}
for tag in ("M1", "M2", "M4"):
    geo = GEOS[tag]
    veq_map = {}
    # existence over the core grid (warm-start continuation downward)
    vlast = None
    for kk in sorted([k for k in K0 if k > 0], reverse=True):
        veq, info = ev.equilibrium_newton(geo, kk, vinit=vlast)
        veq_map[kk] = veq
        if veq is not None:
            vlast = veq
    for kk in [k for k in K0 if k < 0]:
        veq, info = ev.equilibrium_newton(geo, kk)
        veq_map[kk] = veq
    VEQ[tag] = veq_map
    # log-bisection of the fold
    lo, hi = 1e-3, 1e3
    if veq_map[1e-3] is not None:
        FOLD[tag] = ("<=1e-3", None)
    elif veq_map[1e3] is None:
        FOLD[tag] = (">1e3", None)
    else:
        vhi = veq_map[1e3]
        for _ in range(24):
            mid = 10**(0.5 * (np.log10(lo) + np.log10(hi)))
            veq, _ = ev.equilibrium_newton(geo, mid, vinit=vhi)
            if veq is None:
                lo = mid
            else:
                hi = mid
                vhi = veq
        FOLD[tag] = (lo, hi)
    log(f"{tag}: fold kappa_s in {FOLD[tag]}; equilibria exist at "
        f"{sorted([k for k, v in veq_map.items() if v is not None])}")
    dspl = {k: float(np.min(v)) for k, v in veq_map.items()
            if v is not None}
    log(f"{tag}: equilibrium min(v_eq) per kappa: "
        + str({f'{k:g}': f'{d:.3g}' for k, d in dspl.items()}))

# ---------------------------------------------------------------- core
for tag in ("M1", "M2", "M4"):
    kc = float(lin[f"{tag}_kc"])
    kON = K0 + [f * kc for f in (0.7, 0.9, 1.1, 1.3)]
    run_group(tag, True, kON, AMPS, ["bump"], gname=f"core_{tag}_ON")
    run_group(tag, False, K0, AMPS, ["bump", "eq+bump"],
              gname=f"core_{tag}_OFF", veq_map=VEQ[tag])

# ---------------------------------------------------------------- subsets
kcM1 = float(lin["M1_kc"])
for bc in (("robin1", "neumann"), ("dirichlet", "dirichlet"),
           ("dirichlet", "outgoing")):
    nm = f"bc_{bc[0][:3]}_{bc[1][:3]}"
    run_group("M1", True, [0.5 * kcM1, 2 * kcM1, -1.0], [1e-2],
              ["bump"], bc=bc, gname=nm + "_ON")
    run_group("M1", False, [1.0, -1.0], [1e-2], ["bump"], bc=bc,
              gname=nm + "_OFF", veq_map=VEQ["M1"])
for prof in ("g2", "g3"):
    run_group("M1", True, [0.5 * kcM1, 2 * kcM1, -1.0], [1e-2, 0.3],
              ["bump"], profile=prof, gname=f"prof_{prof}_ON")
run_group("M1", True, [2 * kcM1, -1.0], [1e-2], ["bump"], kicked=True,
          gname="kick_ON")
run_group("M1", False, [1.0, -1.0], [1e-2], ["bump"], frame="diagonal",
          gname="diagframe_OFF")

# ---------------------------------------------------------------- G2
log("=" * 72)
log("G2 GRID-DOUBLING REPRESENTATIVES (Nx = 2048)")
log("=" * 72)
seen, reps = set(), []
for row in CAT:
    if row["group"].startswith("core_M1") and row["label"] not in seen \
            and row["init"] == "bump":
        seen.add(row["label"])
        reps.append(row)
reps = reps[:8]
g2ok = []
for row in reps:
    run_group("M1", row["dcell"], [row["kappa"]], [row["amp"]],
              ["bump"], gname=f"g2_{row['label'][:6]}_{len(g2ok)}",
              Nx_override=2048)
    lab2 = CAT[-1]["label"]
    g2ok.append((row["label"], lab2, row["label"] == lab2))
    log(f"G2 rep kappa={row['kappa']:g} amp={row['amp']:g} "
        f"dcell={row['dcell']}: Nx1024={row['label']} Nx2048={lab2} "
        f"{'MATCH' if row['label'] == lab2 else 'MISMATCH'}")

with open("/tmp/w4b_p3_catalog.json", "w") as fh:
    json.dump(CAT, fh, indent=1)
np.savez("/tmp/w4b_p3_waveforms.npz",
         **{k: v for k, v in WAVE.items()})
with open("/tmp/w4b_p3_meta.json", "w") as fh:
    json.dump(dict(fold={k: list(map(str, v)) for k, v in FOLD.items()},
                   g2=[list(map(str, g)) for g in g2ok]), fh, indent=1)

# ---------------------------------------------------------------- summary
log("=" * 72)
log("P3/P5 SUMMARY TABLES")
log("=" * 72)
from collections import Counter
for gpre in ("core_M1_ON", "core_M1_OFF", "core_M2_ON", "core_M2_OFF",
             "core_M4_ON", "core_M4_OFF"):
    rows = [r for r in CAT if r["group"] == gpre]
    log(f"-- {gpre}: " + str(Counter(r["label"] for r in rows)))
    for r in sorted(rows, key=lambda r: (r["init"], r["kappa"],
                                         r["amp"])):
        log(f"   k={r['kappa']:+9.3g} a={r['amp']:+6.2g} "
            f"{r['init']:7s} -> {r['label']:14s} freq={r['freq']:7.3f} "
            f"rate={r['rate']:+8.3f} env={r['env_max']:8.3g} "
            f"drift={r['edrift']:.1e} valid={r['valid']}")
nval = sum(1 for r in CAT if not r["valid"])
log(f"TOTAL rows: {len(CAT)}; energy-gate invalid: {nval}")
log(f"G2 doubling: {g2ok}")
log("done.")
