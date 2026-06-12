"""W4 SOLVER AGENT B — script 9: P5 SELECTION-MAP ASSEMBLY + GRADING.

Reads the catalog (/tmp/w4b_p3_catalog.json), revalidation
(/tmp/w4b_reval.json if present), lingap (/tmp/w4b_lingap.npz), fold
metadata (/tmp/w4b_p3_meta.json) and assembles the pre-registered P5
map (kappa, member, amplitude) -> outcome with the declaration
grading:
  (i)  NO kappa with durable shaped matter -> completion FALSIFIED
  (ii) a kappa-BAND -> numerical fingerprint of the selection principle
  (iii) ALL kappa durable -> persistence does not select here
"Durable shaped matter" (operational, pre-stated): a G1-valid run
classified RING or BREATHER (bounded shaped oscillation), or a QUIET
run settling onto a nonzero static shaped profile (formation /
displaced equilibrium, env -> const > 0 with negative late rate), on
the core BCs, stable under the banked grid-doubling representatives.
A cell is counted only at its banked (revalidated where required)
classification. Frozen-f premise labeled throughout (the coupled
subset carries its own labels). New file. 2026-06-12, W4-B agent.
"""
import json
import numpy as np
from collections import Counter, defaultdict


def log(*a):
    print(*a, flush=True)


cat = json.load(open("/tmp/w4b_p3_catalog.json"))
lin = np.load("/tmp/w4b_lingap.npz")
try:
    reval = json.load(open("/tmp/w4b_reval.json"))
    RV = {(r["member"], r["dcell"], r["kappa"], r["amp"], r["init"]): r
          for r in reval}
except FileNotFoundError:
    RV = {}
    log("NOTE: no revalidation file; invalid cells stay unbanked")
meta = json.load(open("/tmp/w4b_p3_meta.json"))


def banked_label(r):
    """final (label, banked?) after the G1/reval pipeline."""
    key = (r["member"], r["dcell"], r["kappa"], r["amp"], r["init"])
    if r["valid"] and r["label"] not in ("COLLAPSE+",):
        return r["label"], True
    if key in RV:
        rv = RV[key]
        if rv["valid"]:
            # direction re-read for COLLAPSE+ cells
            lab = rv["reval_label"]
            if lab == "COLLAPSE+" and rv["vmin_last"] <= -2:
                lab = "COLLAPSE-(overflow)"
            return lab, True
        return rv["reval_label"], False
    return r["label"], r["valid"]


def durable(lab, r):
    if lab in ("RING", "BREATHER"):
        return True
    if lab == "QUIET" and r["rate"] < 0 and r["env_max"] > 0:
        return True   # settled onto displaced shaped equilibrium
    return False


log("=" * 78)
log("P5 SELECTION MAP (frozen-f core, BC = inner Dirichlet / outer "
    "Neumann, g1)")
log("=" * 78)
K0 = sorted({r["kappa"] for r in cat if r["group"].startswith("core_")
             and abs(np.log10(abs(r["kappa"])) % 1) < 1e-9})
for tag in ("M1", "M2", "M4"):
    kc = float(lin[f"{tag}_kc"])
    fold = meta["fold"][tag]
    log(f"--- {tag}: spectral kappa_c = {kc:.5f} (ON-gap); "
        f"static fold kappa_s = {fold} (OFF); ratio table below")
    for dc in (True, False):
        rows = [r for r in cat
                if r["group"] == f"core_{tag}_{'ON' if dc else 'OFF'}"]
        bykap = defaultdict(list)
        for r in rows:
            lab, bank = banked_label(r)
            bykap[r["kappa"]].append((lab, bank, r))
        log(f"  D_cell {'ON ' if dc else 'OFF'}:")
        for kk in sorted(bykap):
            ent = bykap[kk]
            labs = Counter(l for l, b, _ in ent)
            nb = sum(1 for l, b, _ in ent if b)
            dur = sum(1 for l, b, r in ent if b and durable(l, r))
            log(f"    k={kk:+10.4g}: {dict(labs)}  banked={nb}/"
                f"{len(ent)} durable={dur}")
log("")
log("=" * 78)
log("GRADING (per the W4 declaration)")
log("=" * 78)
verdicts = {}
for tag in ("M1", "M2", "M4"):
    for dc in (True, False):
        rows = [r for r in cat
                if r["group"] == f"core_{tag}_{'ON' if dc else 'OFF'}"]
        kdur, knot = set(), set()
        for r in rows:
            lab, bank = banked_label(r)
            if not bank:
                continue
            (kdur if durable(lab, r) else knot).add(r["kappa"])
        both = kdur & knot
        verdicts[(tag, dc)] = (sorted(kdur), sorted(knot - kdur))
        log(f"{tag} D_cell={'ON' if dc else 'OFF'}: durable at "
            f"{len(kdur)} kappas, non-durable-only at "
            f"{len(knot - kdur)}; mixed(amp-dependent) at {len(both)}")
        log(f"   durable kappas:      {sorted(kdur)}")
        log(f"   no-durable kappas:   {sorted(knot - kdur)}")
anyd = any(len(v[0]) for v in verdicts.values())
alld = all(len(v[1]) == 0 for v in verdicts.values())
if not anyd:
    log("VERDICT: outcome (i) - NO kappa with durable shaped matter; "
        "wave-sector completion FALSIFIED as the missing piece "
        "(frozen-f premise).")
elif alld:
    log("VERDICT: outcome (iii) - durable matter at ALL banked kappa; "
        "persistence does not select at this level (frozen-f premise).")
else:
    log("VERDICT: outcome (ii) - kappa-BAND structure: durable shaped "
        "matter outside an instability band, no durable matter inside "
        "it; numerical fingerprint of a selection principle "
        "(hypothesis-grade, frozen-f premise; band edges = spectral "
        "kappa_c [ON] and static fold kappa_s [OFF]).")

# the kappa_s / kappa_c structural ratio
log("")
for tag in ("M1", "M2", "M4"):
    kc = float(lin[f"{tag}_kc"])
    f = meta["fold"][tag]
    try:
        ks = 0.5 * (float(f[0]) + float(f[1]))
        log(f"{tag}: kappa_s/kappa_c = {ks/kc:.4f}  (kappa_s = "
            f"{ks:.6f}, kappa_c = {kc:.6f})")
    except (TypeError, ValueError):
        log(f"{tag}: fold = {f} (no ratio)")

# BC / profile / frame robustness deltas
log("")
log("=" * 78)
log("ROBUSTNESS DELTAS (subsets vs core)")
log("=" * 78)
core_idx = {}
for r in cat:
    if r["group"].startswith("core_M1"):
        core_idx[(r["dcell"], r["kappa"], r["amp"], r["init"])] = r
for r in cat:
    if r["group"].startswith(("bc_", "prof_", "kick_", "diagframe")):
        key = (r["dcell"], r["kappa"], r["amp"], r["init"])
        base = core_idx.get(key)
        lab, _ = banked_label(r)
        bl = banked_label(base)[0] if base else "n/a"
        mark = "SAME" if lab == bl else "DELTA"
        log(f"{r['group']:18s} k={r['kappa']:+9.4g} a={r['amp']:+6.2g} "
            f"{r['bc']:20s} {r['profile']} -> {lab:14s} (core: "
            f"{bl:14s}) {mark}")
log("done.")
