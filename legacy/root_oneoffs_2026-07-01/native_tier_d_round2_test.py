"""Tier-D round-2 vocabulary test against the six wall numbers.

Implements EXACTLY the pre-registered contract in
`tier_d_round2_contract.md` (written BEFORE this script). New file only;
alters nothing existing.

Round 2 rationale (from the contract): round 1 (26fc757) tested the
then-available native vocabulary and failed 126/126. The 2026-06-10
session derived NEW exact constants with ZERO lepton input (interface/
weld/threshold geometry). This is a NEW pre-registered round with its own
candidate list — NOT a retune of round 1 (no depth/eta/N/gamma changes;
round-1 declared rationals are an explicit exclusion set; the single D2
overlap is disclosed in the contract).

PART 1: groups A (warped DtN eigenvalues), B (interface threshold
objects), C (spectrum-stage exact rationals, generative rule) against
local/warped C_M1 (form c), C_E1 (forms c and 2c), ratio (forms c and
2c). Tolerances: HIT <= 1e-4, LEAD <= 1e-3, fractional. Mandatory
look-elsewhere per slot: uniform null AND Farey/dense-rational null
(dimension_ladder_null_audit.md methodology).

PART 2: quarantined post-hoc observation 2(1-s^2) = 160/81 vs the ratio
slot, priced with the brutal nulls. QUARANTINED LEAD-CLASS regardless of
outcome; excluded from Part 1 and its look-elsewhere counts.

All arithmetic mpmath at 40 digits; rationals exact via fractions.
No candidate added, removed, or reweighted after the run.
"""

from fractions import Fraction
from math import gcd, pi

import mpmath as mp

mp.mp.dps = 40

TOL_HIT = mp.mpf("1e-4")
TOL_LEAD = mp.mpf("1e-3")

Q_COLLAR = mp.mpf(1) / 3  # self-similar collar q = 1/3 (banked)

# ---------------------------------------------------------------------------
# The six wall numbers (archive/pre_2026-07-01/lepton_ladder_test_results.md, "Standing constraint";
# quoted at EVALUATION time per the contract's build protocol)
# ---------------------------------------------------------------------------

WALLS = {
    "local": {
        "C_M1": mp.mpf("0.977679087638"),
        "C_E1": mp.mpf("1.93121474779"),
        "ratio": mp.mpf("1.97530536575"),
    },
    "warped": {
        "C_M1": mp.mpf("0.936832609588"),
        "C_E1": mp.mpf("1.81920864981"),
        "ratio": mp.mpf("1.94187161205"),
    },
}

# Comparison forms per slot (contract Part 1): the 2 is round 1's declared
# E1 relative-shape plane dimension, carried over, not new.
SLOT_FORMS = {"C_M1": (1,), "C_E1": (1, 2), "ratio": (1, 2)}

# ---------------------------------------------------------------------------
# Group A — warped DtN eigenvalues (native_warped_dtn_hessian_spectrum
# heritage, re-derived this session)
# ---------------------------------------------------------------------------


def dtn_eigenvalue(ell):
    """D_ell = sqrt(l(l+1)) I_{7/2}(6 sqrt(l(l+1))) / I_{5/2}(6 sqrt(l(l+1)))."""
    lam = mp.mpf(ell * (ell + 1))
    x0 = 6 * mp.sqrt(lam)
    return mp.sqrt(lam) * mp.besseli(mp.mpf(7) / 2, x0) / mp.besseli(mp.mpf(5) / 2, x0)


D1 = dtn_eigenvalue(1)
D2 = dtn_eigenvalue(2)
D3 = dtn_eigenvalue(3)
B_RATIO = D1 / mp.sqrt(2)  # = I_{7/2}(6 sqrt2)/I_{5/2}(6 sqrt2)

GROUP_A = [
    ("D1", D1, None, "warped ell=1 DtN eigenvalue (H1 triplet block)"),
    ("D2", D2, None, "warped ell=2 DtN eigenvalue (round-1 overlap disclosed)"),
    ("D3", D3, None, "warped ell=3 DtN eigenvalue"),
    ("D2/D1", D2 / D1, None, "DtN spectral step ell=1 -> 2"),
    ("D1^2", D1 ** 2, None, "squared triplet eigenvalue (two-action form)"),
    ("B", B_RATIO, None, "Bessel argument ratio; warped-gamma exponent object"),
    ("exp((1-B)/36)", mp.e ** ((1 - B_RATIO) / 36), None,
     "exact warped/local gamma quotient exp(-B/36)/exp(-1/36)"),
]

# ---------------------------------------------------------------------------
# Group B — interface threshold objects (weld phases 2-3)
# ---------------------------------------------------------------------------

NU_17 = mp.sqrt(17)  # nu = sqrt(1+4q(1-q))/q at q = 1/3


def l0_threshold(lam):
    """L0(lambda) = -(1-2q)/2 + (q tau0/2) I'_nu(tau0)/I_nu(tau0), tau0=2 sqrt(lam)/q."""
    tau0 = 2 * mp.sqrt(mp.mpf(lam)) / Q_COLLAR
    iprime = (mp.besseli(NU_17 - 1, tau0) + mp.besseli(NU_17 + 1, tau0)) / 2
    return -(1 - 2 * Q_COLLAR) / 2 + (Q_COLLAR * tau0 / 2) * iprime / mp.besseli(NU_17, tau0)


L0_2 = l0_threshold(2)
L0_6 = l0_threshold(6)

GROUP_B = [
    ("L0(2)", L0_2, None, "binding threshold, lambda=2 (sqrt17 Bessel form)"),
    ("L0(2)/(4/3)", L0_2 / (mp.mpf(4) / 3), None,
     "threshold vs symmetric-pair 4q (confirmed-mirage object, mechanical)"),
    ("2q/L0(2)", 2 * Q_COLLAR / L0_2, None, "threshold deficit gamma/gamma_c"),
    ("L0(2)/(2q)", L0_2 / (2 * Q_COLLAR), None, "inverse deficit (the recorded ~2)"),
    ("L0(6)", L0_6, None, "binding threshold, lambda=6"),
    ("L0(6)/L0(2)", L0_6 / L0_2, None, "threshold spectral step"),
]

# ---------------------------------------------------------------------------
# Group C — spectrum-stage exact rationals (generative rule; contract Part 1)
# ---------------------------------------------------------------------------

LEDGER = [
    ("q", Fraction(1, 3)), ("s", Fraction(1, 9)), ("eta", Fraction(1, 18)),
    ("eta/2", Fraction(1, 36)), ("q/2", Fraction(1, 6)), ("W(A3)", Fraction(1, 4)),
    ("W(S5)", Fraction(5, 12)), ("W(T8)", Fraction(2, 3)), ("8/9", Fraction(8, 9)),
    ("2/9", Fraction(2, 9)), ("3/8", Fraction(3, 8)), ("5/8", Fraction(5, 8)),
]

ROUND1_DECLARED_RATIONALS = {
    Fraction(1), Fraction(35, 36), Fraction(37, 36), Fraction(2, 3),
    Fraction(2), Fraction(35, 18), Fraction(3, 2), Fraction(5, 3),
}


def build_group_c():
    pool = {}  # Fraction -> provenance of FIRST generation (rule order)

    def add(frac, prov):
        pool.setdefault(frac, prov)

    add(Fraction(3), "isotropy constant 3 = N (trivial, declared)")
    qshares = [Fraction(1, 9), Fraction(2, 9), Fraction(6, 9)]
    for f in qshares:
        add(f, f"quotient-completion share {f} (spectrum doc s40-42)")
    for a in qshares:
        for b in qshares:
            if a != b:
                add(a / b, f"pairwise quotient ({a})/({b}) of quotient shares")
    add(Fraction(3, 8), "commutator W-share complement 3/8")
    add(Fraction(5, 8), "commutator W-share complement 5/8")
    for name, f in LEDGER:
        add(f, f"banked ledger single {name} = {f}")
    for i in range(len(LEDGER)):
        for j in range(i, len(LEDGER)):
            (na, fa), (nb, fb) = LEDGER[i], LEDGER[j]
            add(fa * fb, f"ledger product {na}*{nb} = {fa * fb}")
    excluded = sorted(f for f in pool if f in ROUND1_DECLARED_RATIONALS)
    for f in excluded:
        del pool[f]
    group = [
        (str(f), mp.mpf(f.numerator) / f.denominator, f, prov)
        for f, prov in sorted(pool.items())
    ]
    return group, excluded


GROUP_C, GROUP_C_EXCLUDED = build_group_c()

CANDIDATES = (
    [("A:" + n, v, fr, p) for (n, v, fr, p) in GROUP_A]
    + [("B:" + n, v, fr, p) for (n, v, fr, p) in GROUP_B]
    + [("C:" + n, v, fr, p) for (n, v, fr, p) in GROUP_C]
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def frac_dev(value, target):
    return (value - target) / target


def classify(dev):
    a = abs(dev)
    if a <= TOL_HIT:
        return "HIT"
    if a <= TOL_LEAD:
        return "LEAD"
    return "MISS"


def fmt(x, digits=12):
    return mp.nstr(mp.mpf(x), digits)


def farey_count(target, frac_window, qmax):
    """Exact count of reduced p/q, q <= qmax, with |p/q - target| <= frac_window*target."""
    t = float(target)
    w = float(frac_window * target)
    count = 0
    for q in range(1, qmax + 1):
        p_lo = int(mp.ceil((t - w) * q))
        p_hi = int(mp.floor((t + w) * q))
        for p in range(p_lo, p_hi + 1):
            if p > 0 and gcd(p, q) == 1:
                count += 1
    return count


def farey_density_expectation(target, frac_window, qmax):
    """Farey null: E[# reduced p/q, q<=Q, in window] ~ 2*w*|t|*(3/pi^2)*Q^2."""
    return 2 * frac_window * abs(target) * (mp.mpf(3) / pi ** 2) * qmax ** 2


def evaluate_slot(slot, target):
    """All comparisons for one slot: returns list of (label, value, fraction, dev, cls)."""
    rows = []
    for name, value, frac, _prov in CANDIDATES:
        for form in SLOT_FORMS[slot]:
            cmp_val = form * value
            cmp_frac = form * frac if frac is not None else None
            label = name if form == 1 else f"2*[{name}]"
            dev = frac_dev(cmp_val, target)
            rows.append((label, cmp_val, cmp_frac, dev, classify(dev)))
    return rows


def look_elsewhere_report(rows, target):
    values = [r[1] for r in rows]
    k = len(values)
    lo, hi = min(values), max(values)
    rng = hi - lo
    e_hit_u = k * 2 * TOL_HIT * abs(target) / rng
    e_lead_u = k * 2 * TOL_LEAD * abs(target) / rng
    rational_dens = [r[2].denominator for r in rows if r[2] is not None]
    qmax = max(rational_dens) if rational_dens else None
    print(f"    look-elsewhere (uniform null): K = {k}, range = "
          f"[{fmt(lo, 6)}, {fmt(hi, 6)}], width = {fmt(rng, 6)}")
    print(f"      E[accidental HITs]  = {mp.nstr(e_hit_u, 4)}   "
          f"E[accidental LEADs] = {mp.nstr(e_lead_u, 4)}")
    print("      (crude, as in round 1: range estimated from the candidates")
    print("       themselves; candidates cluster near 0-2, so this UNDERSTATES")
    print("       the accidental expectation there; order-of-magnitude only.)")
    if qmax is not None:
        e_hit_f = farey_density_expectation(target, TOL_HIT, qmax)
        e_lead_f = farey_density_expectation(target, TOL_LEAD, qmax)
        n_hit = farey_count(target, TOL_HIT, qmax)
        n_lead = farey_count(target, TOL_LEAD, qmax)
        print(f"    look-elsewhere (Farey/dense-rational null, Q = {qmax}):")
        print(f"      density E[reduced p/q in HIT window]  = {mp.nstr(e_hit_f, 4)}"
              f"   (exact enumeration: {n_hit})")
        print(f"      density E[reduced p/q in LEAD window] = {mp.nstr(e_lead_f, 4)}"
              f"   (exact enumeration: {n_lead})")
        print("      (the brutal envelope: prices the whole vocabulary CLASS")
        print("       'rationals of this complexity'. Any rational HIT here is")
        print("       worthless if this expectation is of order 1.)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=" * 72)
    print("TIER-D ROUND-2 VOCABULARY TEST")
    print("Pre-registered contract: tier_d_round2_contract.md (written BEFORE")
    print("this script; round-1 rules carry over from 26fc757).")
    print("=" * 72)
    print()

    # -- Pre-registration echo, printed FIRST --------------------------------
    print("PRE-REGISTRATION (echo)")
    print("-" * 72)
    print("  Round 2 rationale: round 1 failed 126/126; the 2026-06-10 session")
    print("  derived NEW exact constants with ZERO lepton input. New round, new")
    print("  list. NOT a retune: depths 5/7, eta, N, gamma untouched; round-1")
    print("  declared rationals excluded; D2 overlap disclosed (its round-1 MISS")
    print("  stands; retained only as part of the mechanical DtN family).")
    print()
    print("  Cross-checks against published session digits (binding):")
    checks = [
        ("D1", D1, "0.9796633"), ("D2", D2, "1.9857855"), ("D3", D3, "2.9893060"),
        ("B", B_RATIO, "0.692726581294"),
        ("L0(2)", L0_2, "1.33835009"), ("L0(6)", L0_6, "2.29931870"),
        ("L0(2)/(2q)", L0_2 / (2 * Q_COLLAR), "2.0075251"),
        ("L0(12)", l0_threshold(12), "3.28396540"),
    ]
    for name, value, published in checks:
        diff = abs(value - mp.mpf(published))
        tol = mp.mpf(10) ** (-(len(published.split(".")[1]) - 1))
        status = "ok" if diff < tol else "FAIL"
        print(f"    {name:<12} = {fmt(value, 12):<16} vs published {published:<16}"
              f" |diff| = {mp.nstr(diff, 3)}  {status}")
        assert diff < tol, f"{name} disagrees with the published repo value"
    print()
    print(f"  Group A (warped DtN, {len(GROUP_A)} candidates):")
    for n, v, _, p in GROUP_A:
        print(f"    {n:<16} = {fmt(v, 10):<14} {p}")
    print(f"  Group B (interface thresholds, {len(GROUP_B)} candidates):")
    for n, v, _, p in GROUP_B:
        print(f"    {n:<16} = {fmt(v, 10):<14} {p}")
    print(f"  Group C (exact rationals, generative rule): {len(GROUP_C)} after")
    print(f"    dedupe and exclusion of round-1 declared rationals")
    print(f"    (excluded as generated: "
          f"{', '.join(str(f) for f in GROUP_C_EXCLUDED)})")
    for n, v, fr, p in GROUP_C:
        print(f"    {str(fr):<10} = {fmt(v, 8):<12} {p}")
    print()
    n_cand = len(CANDIDATES)
    n_cmp = sum(len(SLOT_FORMS[s]) for s in SLOT_FORMS) * n_cand * 2
    print(f"  Total candidates: {n_cand}  (7 A + 6 B + {len(GROUP_C)} C)")
    print(f"  Slots/forms: C_M1 (c), C_E1 (c, 2c), ratio (c, 2c); both branches.")
    print(f"  Total classifications: {n_cmp}")
    print(f"  Tolerances: HIT <= 1e-4, LEAD <= 1e-3 (fractional; round-1 values).")
    print("  Verdict rules: round-1 T5 verbatim. Hits/leads must survive")
    print("  look-elsewhere and are NOT derivations; no banking. Targets are the")
    print("  six wall numbers (published; %-level matches uninformative).")
    print()

    # -- PART 1 evaluation ----------------------------------------------------
    print("=" * 72)
    print("PART 1 — RESULTS (evaluation against the six wall numbers)")
    print("=" * 72)
    all_rows = {}
    for branch in ("local", "warped"):
        for slot in ("C_M1", "C_E1", "ratio"):
            target = WALLS[branch][slot]
            rows = evaluate_slot(slot, target)
            all_rows[(branch, slot)] = rows
            n_hit = sum(1 for r in rows if r[4] == "HIT")
            n_lead = sum(1 for r in rows if r[4] == "LEAD")
            n_miss = sum(1 for r in rows if r[4] == "MISS")
            print()
            print(f"  Slot {slot}, branch {branch}: target = {fmt(target)}")
            print(f"    census: {len(rows)} comparisons -> "
                  f"{n_hit} HIT, {n_lead} LEAD, {n_miss} MISS")
            flagged = [r for r in rows if r[4] != "MISS"]
            for label, val, _, dev, cls in flagged:
                print(f"    {cls}: {label:<28} = {fmt(val, 10)}  "
                      f"dev = {mp.nstr(dev, 6)}")
            nearest = sorted(rows, key=lambda r: abs(r[3]))[:5]
            print("    nearest five (for calibration; MISSes have NO status):")
            for label, val, _, dev, cls in nearest:
                print(f"      {label:<28} = {fmt(val, 10)}  "
                      f"dev = {mp.nstr(dev, 6)}  {cls}")
            look_elsewhere_report(rows, target)

    # -- T4-style branch handling ---------------------------------------------
    print()
    print("BRANCH HANDLING (round-1 T4 rules, carried over)")
    print("-" * 72)
    print("  Confirmed: no branch averaging; no per-observable branch choice;")
    print("  both branches run identically and reported in full.")
    fits = {
        branch: {
            slot: [r for r in all_rows[(branch, slot)] if r[4] in ("HIT", "LEAD")]
            for slot in ("C_M1", "C_E1", "ratio")
        }
        for branch in ("local", "warped")
    }
    split = (
        (fits["local"]["C_M1"] and not fits["local"]["C_E1"]
         and fits["warped"]["C_E1"] and not fits["warped"]["C_M1"])
        or
        (fits["warped"]["C_M1"] and not fits["warped"]["C_E1"]
         and fits["local"]["C_E1"] and not fits["local"]["C_M1"])
    )
    print(f"  Cross-branch split rule triggered: {bool(split)}"
          + ("  -> MISS for BOTH branches per contract" if split else ""))
    print()

    # -- PART 1 verdict ---------------------------------------------------------
    print("PART 1 VERDICT (round-1 T5 rules)")
    print("-" * 72)
    any_hit = any(r[4] == "HIT" for rows in all_rows.values() for r in rows)
    any_lead = any(r[4] == "LEAD" for rows in all_rows.values() for r in rows)
    print(f"  HITs:  {any_hit}")
    print(f"  LEADs: {any_lead}")
    if any_hit:
        print("  At least one HIT: check its look-elsewhere expectation above.")
        print("  Even surviving, it is NOT a derivation — a sharp target only;")
        print("  the boundary-Hessian derivation of that coefficient is required")
        print("  before any grade rises. No banking.")
    elif any_lead:
        print("  LEAD(s), no HIT: recorded for the named candidate(s) ONLY, with")
        print("  look-elsewhere expectation; not banked.")
    else:
        print("  NO HIT, NO LEAD anywhere: the round-2 vocabulary (warped DtN")
        print("  family, interface thresholds, spectrum-stage rationals) joins")
        print("  round 1's on the failed side of the wall. The six numbers remain")
        print("  the standing constraint; nothing is adjusted in response.")
    print("  The REAL Tier-D target remains S_phi0[typed nodes] and its Hessian")
    print("  — this round was a vocabulary test, not the derivation.")
    print()

    # -- PART 2 — quarantine pricing -------------------------------------------
    print("=" * 72)
    print("PART 2 — QUARANTINED POST-HOC OBSERVATION (excluded from Part 1)")
    print("=" * 72)
    obs = mp.mpf(160) / 81
    print("  Observation (driver, post-hoc, CONTAMINATED BY CONSTRUCTION — it")
    print("  came from inspecting the targets): C_E1/C_M1 vs 2(1 - s^2)")
    print(f"  = 2*(80/81) = 160/81 = {fmt(obs, 14)}")
    print("  Exclusion grounds: 10/9 is not a banked share; 80/81 is not")
    print("  generatable by the Group-C rule; the form was found by target")
    print("  inspection.")
    print()
    for branch in ("local", "warped"):
        t = WALLS[branch]["ratio"]
        print(f"  vs {branch} ratio {fmt(t)}: dev = "
              f"{mp.nstr(frac_dev(obs, t), 6)}")
    t_loc = WALLS["local"]["ratio"]
    dev_obs = abs(frac_dev(obs, t_loc))
    gap_abs = abs(obs - t_loc)
    print(f"  Observed window (local branch): |dev| = {mp.nstr(dev_obs, 6)}"
          f"  (inside the HIT tolerance — hence the quarantine matters)")
    print()

    probs = []

    print("  (a) Brutal null 1 — all reduced rationals p/q, q <= 81:")
    for wname, w in (("observed-dev", dev_obs), ("HIT", TOL_HIT)):
        e = farey_density_expectation(t_loc, w, 81)
        n = farey_count(t_loc, w, 81)
        print(f"      window {wname:<13} density E = {mp.nstr(e, 4)}   "
              f"exact count = {n}")
        if wname == "observed-dev":
            probs.append(("rationals q<=81 within observed dev", e))
    print("      (chance that SOME q<=81 rational lands as close as 160/81 did")
    print("       is the observed-dev expectation above.)")
    print()

    print("  (b) Brutal null 2 — post-hoc form families:")
    # F1: 2(1 - 1/n)
    f1 = [(n, 2 * (1 - mp.mpf(1) / n)) for n in range(2, 10001)]
    f1_obs = sum(1 for _, v in f1 if abs(frac_dev(v, t_loc)) <= dev_obs)
    f1_hit = sum(1 for _, v in f1 if abs(frac_dev(v, t_loc)) <= TOL_HIT)
    n1 = min(f1, key=lambda nv: abs(nv[1] - t_loc))[0]
    spacing1 = 2 * (mp.mpf(1) / (n1 - 1) - mp.mpf(1) / n1)
    p1 = 2 * gap_abs / spacing1
    print(f"      F1 = 2(1-1/n), n<=10000: in observed window {f1_obs}, in HIT")
    print(f"        window {f1_hit}; nearest n = {n1} (2(1-1/81) = 160/81, the")
    print(f"        SAME value); local spacing {mp.nstr(spacing1, 4)},")
    print(f"        local-spacing chance p = {mp.nstr(p1, 4)}")
    probs.append(("F1 local-spacing", p1))
    # F2: 2(1 - 1/n^2)
    f2 = [(n, 2 * (1 - mp.mpf(1) / n ** 2)) for n in range(2, 1001)]
    f2_obs = sum(1 for _, v in f2 if abs(frac_dev(v, t_loc)) <= dev_obs)
    f2_hit = sum(1 for _, v in f2 if abs(frac_dev(v, t_loc)) <= TOL_HIT)
    n2 = min(f2, key=lambda nv: abs(nv[1] - t_loc))[0]
    spacing2 = 2 * (mp.mpf(1) / (n2 - 1) ** 2 - mp.mpf(1) / n2 ** 2)
    p2 = 2 * gap_abs / spacing2
    print(f"      F2 = 2(1-1/n^2), n<=1000: in observed window {f2_obs}, in HIT")
    print(f"        window {f2_hit}; nearest n = {n2} (2(1-1/81) AGAIN — naming")
    print(f"        multiplicity); local spacing {mp.nstr(spacing2, 4)},")
    print(f"        local-spacing chance p = {mp.nstr(p2, 4)}")
    probs.append(("F2 local-spacing", p2))
    # F3: 2(1-1/m)(1-1/n)
    f3_obs = 0
    f3_hit = 0
    for m in range(2, 201):
        am = 1 - mp.mpf(1) / m
        for n in range(m, 201):
            v = 2 * am * (1 - mp.mpf(1) / n)
            d = abs(frac_dev(v, t_loc))
            if d <= dev_obs:
                f3_obs += 1
            if d <= TOL_HIT:
                f3_hit += 1
    p3 = min(mp.mpf(1), f3_hit * dev_obs / TOL_HIT)  # density-scaled expected
    print(f"      F3 = 2(1-1/m)(1-1/n), 2<=m<=n<=200: in observed window "
          f"{f3_obs},")
    print(f"        in HIT window {f3_hit} — the product family alone supplies")
    print(f"        ~{f3_hit} HIT-level namings of this target: naming is CHEAP.")
    print(f"        density-scaled chance of an observed-dev-close member for a")
    print(f"        random target: p = min(1, {f3_hit}*dev_obs/tol_HIT) = "
          f"{mp.nstr(p3, 4)}")
    print(f"        (direct count in the observed window is {f3_obs} — the")
    print(f"        match is GUARANTEED under this form class)")
    probs.append(("F3 product-family density", p3))
    print()
    print("      Naming multiplicity note: 160/81 is reachable as 2(1-1/81),")
    print("      2(1-1/9^2), AND a q<=81 rational — three namings of one value.")
    print("      Multiplicity is evidence the naming is cheap, not that the")
    print("      value is special.")
    print()

    p_headline = max(probs, key=lambda kv: kv[1])
    print("  (c) Honest conclusion:")
    print(f"      observation recorded, p ~ {mp.nstr(p_headline[1], 2)} "
          f"(most brutal null: {p_headline[0]};")
    print(f"      all computed: "
          + ", ".join(f"{k} = {mp.nstr(v, 2)}" for k, v in probs) + "),")
    print("      status: QUARANTINED LEAD-CLASS — usable only if a derivation")
    print("      produces the form 2(1-s^2) independently.")
    print()

    # -- Repo check / closing verdict ------------------------------------------
    print("=" * 72)
    print("REPO CHECK / CLOSING")
    print("-" * 72)
    print("  Contract compliance: list built structurally before evaluation;")
    print("  no candidate added/removed/reweighted after seeing results; both")
    print("  branches reported in full; look-elsewhere printed per slot; the")
    print("  Part-2 observation never entered Part 1 or its counts.")
    print("  Forbidden henceforth: re-running with a modified list; promoting")
    print("  the quarantined observation without an independent derivation of")
    print("  2(1-s^2); treating any Part-1 MISS proximity as a lead.")
    print("  Next real work: the boundary functional S_phi0[typed nodes] and")
    print("  its Hessian (STATE.md item 0).")


if __name__ == "__main__":
    main()
