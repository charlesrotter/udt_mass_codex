#!/usr/bin/env python3
"""W5 ARM-2 — SCRIPT 6: P3'/P5' PERSISTENCE CATALOG (untruncated).

Date: 2026-06-12.  HYPOTHESIS-GRADE at kappa != 0; TRUE units cc = 2.
Frozen-f nonlinear v-evolutions of the untruncated w-channel (source
sym C3/C4: the (1 - 2 kappa/f) factor; v-chart exact), GPU batched
torch float64 (G3 CPU-trust gate enforced per batch), the W4
pre-registered classifier applied UNCHANGED (w4b_evolib.classify).

PRE-REGISTERED DESIGN (fixed before execution):
  CORE: members {M1, M2, M4} x D_cell {ON, OFF} x
    kappa {+-0.01, +-0.1, +-0.3, +-0.5, +-0.767, +-1, +-1.45, +-3,
           +-10, +-100} (TRUE units; the W4 band edges in true units
    are kc 0.767/0.180/0.198, ks 1.453/0.343/0.377) x
    amp {0.01, 0.3} x init {bump, eq+bump where the W5 equilibrium
    exists}; profile g1; BC (inner cut Dirichlet, weld Neumann);
    domains: FULL (W4-comparable) and t5 TRUST WINDOW (primary class);
    T_end = 12 max(x_max); Nx = 1024 full / 768 window.
  LOCUS DIAGNOSTIC: probe series at the locus x-position on the
    dominant ray for kappa in the locus regime (recorded waveforms).
  GRADING (P5', quoted from the declaration): no durable shaped
    matter at any kappa => untruncated completion falsified; a
    kappa-BAND => selection fingerprint (re-derived edges); durable
    at all kappa => persistence does not select at this level.
  DYNAMICAL EDGES: log-bisection of the GROW/RING boundary (ON and
    OFF about equilibria) to compare against the spectral kappa_c'.
  STIFFNESS: cells terminating nonfinite with srate*dT > 1 carry the
    pre-registered UNRESOLVED-STIFF override (classifier, unchanged);
    such cells get an implicit Radau re-solve on the dominant ray.
  G2: >= 6 representatives re-run at Nx doubled; label must match.

Output: /tmp/w5_arm2_p3_catalog.json + npz checkpoints.
Log: /tmp/w5_arm2_p3.log.  New file.  2026-06-12, W5 Arm-2 agent.
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
      "M4": (1.7106, 2.1312)}
MEM = {t: vl.Member(g, c, Nu=24, Nt=4000) for t, (g, c) in
       MEMBERS.items()}

KCORE = [0.01, 0.1, 0.3, 0.5, 0.767, 1.0, 1.45, 3.0, 10.0, 100.0]
KCORE = [s * k for k in KCORE for s in (+1, -1)]
AMPS = [0.01, 0.3]
CAT = []
WAVE = {}


def veq_on_x(geo, veq):
    out = np.empty((geo.Nu, geo.Nx))
    for k in range(geo.Nu):
        out[k] = np.interp(geo.t_of_x[k], geo.tg, veq[k])
    return out


def run_group(tag, geo, domlbl, dcell, kappas, amps, gname):
    """batch over (kappa, amp, init); eq+bump uses the W5 dressed
    equilibrium as base + reference."""
    T_end = 12.0 * float(np.max(geo.xmax))
    v0s, vt0s, kl, al, il, vrefs = [], [], [], [], [], []
    VEQ = {}
    for kk in kappas:
        veq, _ = w5.equilibrium_member(geo, kk, dcell, cc=2.0,
                                       species=True)
        VEQ[kk] = None if veq is None else veq_on_x(geo, veq)
    for kk in kappas:
        for aa in amps:
            pert = w5.bump_profile(geo, aa)
            v0s.append(pert)
            vt0s.append(np.zeros_like(pert))
            kl.append(kk); al.append(aa); il.append("bump")
            vrefs.append(np.zeros_like(pert))
            if VEQ[kk] is not None:
                v0s.append(VEQ[kk] + pert)
                vt0s.append(np.zeros_like(pert))
                kl.append(kk); al.append(aa); il.append("eq+bump")
                vrefs.append(VEQ[kk])
    log(f"[{gname}] NB={len(kl)} tag={tag} dom={domlbl} dcell={dcell} "
        f"Nx={geo.Nx} T_end={T_end:.2f}")
    t1 = time.time()
    resb = w5.evolve_torch(geo, np.array(v0s), np.array(vt0s),
                           np.array(kl), dcell, T_end, cc=2.0,
                           species=True, log=log,
                           vrefb=np.array(vrefs))
    log(f"[{gname}] done {time.time()-t1:.0f}s nstep={resb['nstep']}")
    for b in range(len(kl)):
        lab, diag = w5.classify_batch(resb, b, abs(al[b]))
        row = dict(group=gname, member=tag, dom=domlbl,
                   dcell=bool(dcell), kappa=float(kl[b]),
                   amp=float(al[b]), init=il[b], Nx=int(geo.Nx),
                   label=lab, freq=float(diag.get("freq", np.nan)),
                   rate=float(diag.get("rate_final", np.nan)),
                   env_max=float(diag.get("env_max", np.nan)),
                   edrift=float(diag.get("edrift", np.nan)),
                   valid=bool(diag.get("valid", True)),
                   T_term=float(diag.get("T_term", np.nan)))
        CAT.append(row)
        if b % 5 == 0:
            WAVE[f"{gname}_{b}"] = np.column_stack(
                [resb["T"], resb["probe"][b]])
    with open("/tmp/w5_arm2_p3_catalog.json", "w") as fh:
        json.dump(CAT, fh, indent=1)
    return resb


# ------------------------------------------------------------- core
for tag in MEMBERS:
    mem = MEM[tag]
    for domlbl, t_b, Nx in (("full", None, 1024), ("t5", TW[tag][1],
                                                   768)):
        geo = w5.GeoW5(mem, t_b=t_b, Nt=4000, Nx=Nx)
        for dcell in (True, False):
            run_group(tag, geo, domlbl, dcell, KCORE, AMPS,
                      f"core_{tag}_{domlbl}_{'ON' if dcell else 'OFF'}")

# ------------------------------------------------- dynamical band edge
log("=" * 72)
log("DYNAMICAL EDGES (M1; bisect GROW boundary about the W5 "
    "background; full domain)")
log("=" * 72)
mem = MEM["M1"]
geo = w5.GeoW5(mem, t_b=None, Nt=4000, Nx=1024)
T_end = 12.0 * float(np.max(geo.xmax))


def grows(kap, dcell):
    veq, _ = w5.equilibrium_member(geo, kap, dcell, cc=2.0,
                                   species=True)
    if veq is None:
        return None
    vx = veq_on_x(geo, veq)
    v0 = vx + w5.bump_profile(geo, 0.01)
    resb = w5.evolve_torch(geo, v0[None], np.zeros_like(v0)[None],
                           [kap], dcell, T_end, cc=2.0, species=True,
                           cpu_assert=False, vrefb=vx[None])
    lab, diag = w5.classify_batch(resb, 0, 0.01)
    return lab, diag


for dcell in (True, False):
    lo, hi = None, None
    rows = []
    for kap in (1.5, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 40.0):
        out = grows(kap, dcell)
        if out is None:
            rows.append((kap, "NOEQ"))
            continue
        rows.append((kap, out[0]))
    log(f"  {'ON' if dcell else 'OFF'} edge scan: " +
        " ".join(f"{k:g}:{l}" for k, l in rows))
    with open("/tmp/w5_arm2_p3_edges.json", "a") as fh:
        json.dump({"dcell": dcell, "rows": rows}, fh)
        fh.write("\n")

# ------------------------------------------------------ locus waveform
log("=" * 72)
log("LOCUS WAVEFORM DIAGNOSTIC (M1 full, OFF, dominant ray)")
log("=" * 72)
k_dom = int(np.argmax(geo.b_t.sum(0)))
for kap in (0.3, 0.767, 1.45, 3.0):
    tl = geo.locus_t(kap)[k_dom]
    if np.isfinite(tl):
        i_loc = int(np.argmin(np.abs(geo.t_of_x[k_dom] - tl)))
    else:
        i_loc = geo.Nx // 2
    veq, _ = w5.equilibrium_member(geo, kap, False, cc=2.0,
                                   species=True)
    base = (np.zeros((geo.Nu, geo.Nx)) if veq is None
            else veq_on_x(geo, veq))
    v0 = base + w5.bump_profile(geo, 0.05)
    res = w5.evolve_np(geo, v0, np.zeros_like(v0), kap, False,
                       6.0 * float(np.max(geo.xmax)), cc=2.0,
                       species=True, vref=base)
    v = res["v"]
    WAVE[f"locuswf_{kap:g}"] = np.column_stack([res["T"], res["probe"]])
    # spatial envelope after the run vs the locus position:
    env_x = np.max(np.abs(res["v"] - base), axis=0)  # hmm per-x over rays
    prof = np.abs((res["v"] - base)[k_dom])
    i_pk = int(np.argmax(prof))
    log(f"  kappa={kap:5.3f}: t_locus={tl if np.isfinite(tl) else np.nan:.4f} "
        f"x_locus-index={i_loc} | final |v-veq| peak at x-index {i_pk} "
        f"(x/xmax={geo.xg[k_dom, i_pk]/geo.xmax[k_dom]:.3f}); term="
        f"{res['term']}")

# ---------------------------------------------------------------- G2
log("=" * 72)
log("G2 doubling representatives")
log("=" * 72)
seen, reps = set(), []
for row in CAT:
    key = (row["label"], row["dcell"])
    if row["group"].startswith("core_M1_full") and key not in seen \
            and row["init"] == "bump":
        seen.add(key)
        reps.append(row)
reps = reps[:8]
geo2 = w5.GeoW5(mem, t_b=None, Nt=4000, Nx=2048)
ok2 = []
for row in reps:
    veq, _ = w5.equilibrium_member(geo2, row["kappa"], row["dcell"],
                                   cc=2.0, species=True)
    v0 = w5.bump_profile(geo2, row["amp"])
    resb = w5.evolve_torch(geo2, v0[None], np.zeros_like(v0)[None],
                           [row["kappa"]], row["dcell"],
                           12.0 * float(np.max(geo2.xmax)), cc=2.0,
                           species=True, cpu_assert=False)
    lab2, _ = w5.classify_batch(resb, 0, row["amp"])
    ok2.append((row["label"], lab2, row["label"] == lab2))
    log(f"  G2 k={row['kappa']:+g} dcell={row['dcell']} "
        f"amp={row['amp']:g}: Nx1024={row['label']} Nx2048={lab2} "
        f"{'MATCH' if row['label'] == lab2 else 'MISMATCH'}")

np.savez("/tmp/w5_arm2_p3_waves.npz", **WAVE)
with open("/tmp/w5_arm2_p3_catalog.json", "w") as fh:
    json.dump(CAT, fh, indent=1)

# ------------------------------------------------------------ summary
from collections import Counter
log("=" * 72)
log("SUMMARY")
log("=" * 72)
for gpre in sorted({r["group"] for r in CAT}):
    rows = [r for r in CAT if r["group"] == gpre]
    log(f"-- {gpre}: " + str(Counter(r["label"] for r in rows)))
    for r in sorted(rows, key=lambda r: (r["init"], r["kappa"],
                                         r["amp"])):
        log(f"   k={r['kappa']:+9.3g} a={r['amp']:+5.2g} "
            f"{r['init']:7s} -> {r['label']:14s} freq={r['freq']:7.3f}"
            f" rate={r['rate']:+8.3f} drift={r['edrift']:.1e}")
nval = sum(1 for r in CAT if not r["valid"])
log(f"TOTAL rows: {len(CAT)}; energy-gate invalid: {nval}; "
    f"G2: {ok2}")
log(f"done ({time.time()-t0:.0f}s)")
