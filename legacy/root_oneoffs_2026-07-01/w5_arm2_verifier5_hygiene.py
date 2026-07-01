#!/usr/bin/env python3
"""W5 Arm-2 verifier-5 hygiene audit of /tmp/w5_arm2_p3_catalog.json.

Adversarial verifier pass (read-only on existing artifacts).
Tasks (per brief):
  2a. row count, valid==False count, cross-tab invalid by label/group,
      whether headline claims rest on invalid rows.
  2b. M1-full band check vs TRUE-unit edges (ON 0.679 dressed kc',
      OFF fold ks=0.916 claimed; banked TRUE map gives kc=0.767,
      ks=1.453 -- both checked).
  2c. GROW outliers vs Radau stiff log.
  2d. k=+0.01 rows (G2 doubling mismatch cells): labels + dependence.
  3.  kappa grid + domain/member/dcell coverage; duplicates; NaN freq
      on RING rows; classifier-consistency oddities.
"""
import json
import math
from collections import Counter, defaultdict

CAT = "/tmp/w5_arm2_p3_catalog.json"
rows = json.load(open(CAT))


def sec(t):
    print("\n" + "=" * 72 + "\n" + t + "\n" + "=" * 72)


# ------------------------------------------------------------------ 2a
sec("2a. ROW COUNT / VALIDITY CROSS-TAB")
print(f"rows total: {len(rows)} (claimed 934)")
inv = [r for r in rows if r["valid"] is False]
print(f"valid==False rows: {len(inv)} (claimed 301)")
print("\ninvalid by label:")
for k, v in sorted(Counter(r["label"] for r in inv).items()):
    print(f"  {k:18s} {v}")
print("\nALL rows by label:")
for k, v in sorted(Counter(r["label"] for r in rows).items()):
    print(f"  {k:18s} {v}")
print("\nvalid==False / total by label:")
tot = Counter(r["label"] for r in rows)
bad = Counter(r["label"] for r in inv)
for k in sorted(tot):
    print(f"  {k:18s} {bad.get(k,0):4d} / {tot[k]:4d}")
print("\ninvalid by group (top 40):")
for k, v in Counter(r["group"] for r in inv).most_common(40):
    print(f"  {k:40s} {v}")
print("\nRING rows that are invalid:")
for r in inv:
    if r["label"] == "RING":
        print("  ", r)
ring_inv = sum(1 for r in inv if r["label"] == "RING")
quiet_inv = sum(1 for r in inv if r["label"] == "QUIET")
br_inv = sum(1 for r in inv if r["label"] == "BREATHER")
print(f"\nsummary: invalid RING={ring_inv}, QUIET={quiet_inv}, "
      f"BREATHER={br_inv} (these are the labels headline ringing claims "
      "rest on)")

# ------------------------------------------------------------------ 2b
sec("2b. M1 FULL-DOMAIN BAND CHECK (TRUE units)")
EDGE = {("M1", True): 0.679,    # dressed kappa_c' ON (claimed)
        ("M1", False): 0.916}   # OFF fold ks (claimed)
m1 = [r for r in rows if r["member"] == "M1" and r["dom"] == "full"]
print(f"M1 full rows: {len(m1)}")
print("\nAll M1-full rows (sorted by dcell, init, kappa):")
hdr = f"{'dcell':5s} {'init':8s} {'kappa':>8s} {'Nx':>5s} {'label':18s} " \
      f"{'freq':>9s} {'valid':5s} {'group'}"
print(hdr)
for r in sorted(m1, key=lambda r: (not r["dcell"], r["init"], r["kappa"],
                                   r["Nx"])):
    f = r["freq"]
    fs = f"{f:9.4f}" if isinstance(f, float) and math.isfinite(f) else \
        "      nan"
    print(f"{str(r['dcell']):5s} {r['init']:8s} {r['kappa']:8.3f} "
          f"{r['Nx']:5d} {r['label']:18s} {fs} {str(r['valid']):5s} "
          f"{r['group']}")

print("\nBand-pattern adjudication (eq+bump + bump inits, kappa>0):")
print("claimed: COLLAPSE/GROW inside (0, edge); RING/QUIET outside")
viol = []
for r in m1:
    k = r["kappa"]
    edge = EDGE[("M1", r["dcell"])]
    lab = r["label"]
    if k <= 0:
        continue
    inside = 0 < k < edge
    bad_inside = inside and lab in ("RING", "QUIET", "BREATHER",
                                    "DISPERSE")
    bad_outside = (not inside) and lab in ("COLLAPSE+", "COLLAPSE-",
                                           "GROW")
    tag = ""
    if bad_inside:
        tag = "VIOLATION? non-collapse INSIDE band"
    if bad_outside:
        tag = "VIOLATION? collapse OUTSIDE band"
    if lab == "UNRESOLVED-STIFF":
        tag = "(non-verdict)"
    if tag:
        viol.append((r, tag))
        print(f"  dcell={r['dcell']} init={r['init']:8s} k={k:+.3f} "
              f"edge={edge} Nx={r['Nx']} -> {lab:18s} {tag}")
print(f"\nflagged rows: {len(viol)} "
      "(UNRESOLVED-STIFF non-verdicts listed for completeness)")

print("\nSpotlight: OFF (dcell=False) k=+0.767 rows "
      "(0.767 < claimed fold 0.916 -- sub-fold):")
for r in m1:
    if not r["dcell"] and abs(r["kappa"] - 0.767) < 1e-3:
        print("  ", {k: r[k] for k in ("init", "Nx", "label", "freq",
                                       "valid", "group")})

print("\nSpotlight: ON (dcell=True) k=+1 rows (BREATHER question):")
for r in m1:
    if r["dcell"] and abs(r["kappa"] - 1.0) < 1e-9:
        print("  ", {k: r[k] for k in ("init", "Nx", "label", "freq",
                                       "rate", "valid", "group")})
print("ALL BREATHER rows in catalog:")
for r in rows:
    if r["label"] == "BREATHER":
        print("  ", {k: r[k] for k in ("group", "member", "dom", "dcell",
                                       "kappa", "init", "Nx", "valid",
                                       "rate")})

# also: kappa<0 claim "rings/quiet at all |kappa|" -- any collapse/grow
# at kappa<0 anywhere?
print("\nkappa<0 rows whose label is NOT RING/QUIET/DISPERSE/BREATHER:")
n = 0
for r in rows:
    if r["kappa"] < 0 and r["label"] not in ("RING", "QUIET", "DISPERSE",
                                             "BREATHER"):
        n += 1
        print("  ", {k: r[k] for k in ("group", "member", "dom", "dcell",
                                       "kappa", "init", "Nx", "label",
                                       "valid")})
print(f"count: {n}")

# ------------------------------------------------------------------ 2c
sec("2c. GROW OUTLIERS")
grows = [r for r in rows if r["label"] == "GROW"]
print(f"GROW rows: {len(grows)}")
for r in grows:
    print(json.dumps(r))
print("\n(compare manually vs /tmp/w5_arm2_stiff.log Radau verdicts; "
      "stiff kappas TRUE {+-0.01,+-0.1})")

# ------------------------------------------------------------------ 2d
sec("2d. k=+0.01 ROWS (G2 mismatch cells)")
for r in rows:
    if abs(r["kappa"] - 0.01) < 1e-12:
        print("  ", {k: r[k] for k in ("group", "member", "dom", "dcell",
                                       "init", "Nx", "label", "valid",
                                       "T_term")})

# ------------------------------------------------------------------ 3
sec("3. GRID / COVERAGE / DEFECT SWEEP")
kp = sorted({abs(r["kappa"]) for r in rows})
print("distinct |kappa|:", kp)
want = [0.01, 0.1, 0.3, 0.5, 0.767, 1.0, 1.45, 3.0, 10.0, 100.0]
print("claimed grid    :", want)
extra = [k for k in kp if not any(abs(k - w) < 5e-4 for w in want)]
missing = [w for w in want if not any(abs(k - w) < 5e-4 for k in kp)]
print("off-grid values :", extra)
print("missing values  :", missing)
signs = Counter("+" if r["kappa"] > 0 else "-" for r in rows)
print("sign split:", dict(signs))
print("\ncoverage (member, dom, dcell) -> row count:")
cov = Counter((r["member"], r["dom"], r["dcell"]) for r in rows)
for k in sorted(cov):
    print(f"  {k}: {cov[k]}")
print("\ndistinct doms:", sorted({r["dom"] for r in rows}),
      " members:", sorted({r["member"] for r in rows}),
      " inits:", sorted({r["init"] for r in rows}),
      " Nx:", sorted({r["Nx"] for r in rows}),
      " amps:", sorted({r["amp"] for r in rows}))

# duplicates on the full key
key = lambda r: (r["group"], r["member"], r["dom"], r["dcell"],
                 r["kappa"], r["amp"], r["init"], r["Nx"])
dups = [k for k, v in Counter(map(key, rows)).items() if v > 1]
print(f"\nduplicate (group,member,dom,dcell,kappa,amp,init,Nx) keys: "
      f"{len(dups)}")
for d in dups[:20]:
    print("  ", d)
# duplicates ignoring group (same physical cell catalogued twice under
# different group names is expected for doubling/repro groups; report)
key2 = lambda r: (r["member"], r["dom"], r["dcell"], r["kappa"],
                  r["amp"], r["init"], r["Nx"])
d2 = {k: v for k, v in Counter(map(key2, rows)).items() if v > 1}
print(f"physical-cell keys appearing >1x (across groups): {len(d2)}")

# NaN freq on RING rows
nf = [r for r in rows if r["label"] == "RING" and not
      (isinstance(r["freq"], float) and math.isfinite(r["freq"]))]
print(f"\nRING rows with non-finite freq: {len(nf)}")
for r in nf[:10]:
    print("  ", r)

# classifier-consistency oddities
odd = []
for r in rows:
    lab, tt = r["label"], r["T_term"]
    tt_fin = isinstance(tt, float) and math.isfinite(tt)
    if lab in ("COLLAPSE+", "COLLAPSE-", "UNRESOLVED-STIFF") and not \
            tt_fin:
        odd.append(("terminal label w/o T_term", r))
    if lab in ("RING", "QUIET", "GROW", "BREATHER", "DISPERSE") and \
            tt_fin:
        odd.append(("non-terminal label WITH T_term", r))
    ed = r["edrift"]
    ed_fin = isinstance(ed, float) and math.isfinite(ed)
    if r["valid"] is False and ed_fin and ed <= 1e-6:
        odd.append(("valid=False but edrift<=1e-6", r))
    if r["valid"] is True and ed_fin and ed > 1e-6:
        odd.append(("valid=True but edrift>1e-6", r))
print(f"\nclassifier-consistency oddities: {len(odd)}")
for t, r in odd[:20]:
    print("  ", t, "->", {k: r[k] for k in ("group", "kappa", "dcell",
                                            "init", "Nx", "label",
                                            "edrift", "valid",
                                            "T_term")})

# invalid rows: edrift distribution (how bad is the worst drift?)
eds = sorted((r["edrift"] for r in inv if isinstance(r["edrift"], float)
              and math.isfinite(r["edrift"])), reverse=True)
print(f"\ninvalid-row edrift: n={len(eds)}, "
      f"max={eds[0] if eds else None}, "
      f"median={eds[len(eds)//2] if eds else None}, "
      f"min={eds[-1] if eds else None}")
# valid RING rows: worst edrift
edr = sorted((r["edrift"] for r in rows if r["label"] == "RING" and
              r["valid"] and isinstance(r["edrift"], float) and
              math.isfinite(r["edrift"])), reverse=True)
print(f"valid RING edrift: n={len(edr)}, max={edr[0] if edr else None}")
print("\nDONE")
