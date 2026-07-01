"""Frozen lepton-ladder falsification test.

Implements EXACTLY the pre-registered contract in
`lepton_ladder_falsification_contract.md` (committed at git 26fc757 BEFORE
this script was written or run). New file only; alters nothing existing.

Frozen model (no adjustable elements):
    q = 1/3, eta = 1/18, eta/2 = 1/36, N = 3
    gamma_local  = 3 exp(-1/36)
    gamma_warped = 3 exp(-B/36), B = I_{7/2}(6 sqrt(2)) / I_{5/2}(6 sqrt(2))
    depth(M1, mu-like) = 5, depth(E1, tau-like) = 7
    M2 conditionally demoted per Pbundle0 (part of the frozen model).
    Anchor m_e applied only after dimensionless ratios.

Tests T1-T5 per the contract. Tolerances: HIT <= 1e-4 fractional,
LEAD <= 1e-3 fractional, MISS otherwise. Mandatory look-elsewhere
accounting per slot. Finite-cell diagnostics (1.1343262, 2.10394) are
context only, NOT candidates, per the contract's final paragraph.

All arithmetic in mpmath at 40 significant digits; Bessel ratios
cross-checked against scipy.special.iv where available.
"""

import mpmath as mp

mp.mp.dps = 40

# ---------------------------------------------------------------------------
# Frozen model constants
# ---------------------------------------------------------------------------

ETA = mp.mpf(1) / 18
ETA_HALF = ETA / 2  # = 1/36
N = 3

GAMMA_LOCAL = N * mp.e ** (-ETA_HALF)

ARG_B = 6 * mp.sqrt(2)
B_WARP = mp.besseli(mp.mpf(7) / 2, ARG_B) / mp.besseli(mp.mpf(5) / 2, ARG_B)
GAMMA_WARPED = N * mp.e ** (-B_WARP / 36)

DEPTH_M1 = 5  # mu-like
DEPTH_E1 = 7  # tau-like

# Targets (observed, as recorded in the repo's diagnostic lane).
MU_OVER_E = mp.mpf("206.768282988")
TAU_OVER_E = mp.mpf("3477.22828002")
TAU_OVER_MU = TAU_OVER_E / MU_OVER_E

# Published repo cross-check value for gamma_local.
GAMMA_LOCAL_PUBLISHED = mp.mpf("2.91781343135")

# Tolerances (binding).
TOL_HIT = mp.mpf("1e-4")
TOL_LEAD = mp.mpf("1e-3")

# Finite-cell diagnostics — context only, NOT candidates (contract, last
# paragraph).
FINITE_CELL_C_M1 = mp.mpf("1.1343262")
FINITE_CELL_C_E1 = mp.mpf("2.10394")

# ---------------------------------------------------------------------------
# Pre-declared candidate lists (COMPLETE; nothing added after the run)
# ---------------------------------------------------------------------------

ARG_D2 = 6 * mp.sqrt(6)
D2 = (
    mp.sqrt(6)
    * mp.besseli(mp.mpf(7) / 2, ARG_D2)
    / mp.besseli(mp.mpf(5) / 2, ARG_D2)
)

CANDIDATES_C_M1 = [
    ("1", mp.mpf(1), "bare ladder"),
    ("exp(-eta/2)", mp.e ** (-ETA_HALF), "one extra one-sided transfer action"),
    ("exp(+eta/2)", mp.e ** (+ETA_HALF), "one transfer-action credit"),
    ("exp(-eta)", mp.e ** (-ETA), "one full transfer action"),
    ("1 - eta/2 = 35/36", mp.mpf(35) / 36, "linearized one-sided transfer"),
    ("1 + eta/2 = 37/36", mp.mpf(37) / 36, "linearized credit"),
    ("W(T8) = 2/3", mp.mpf(2) / 3, "active-image action weight"),
]

CANDIDATES_C_E1 = [
    ("2", mp.mpf(2), "E1 relative-shape plane dimension"),
    ("2 exp(-eta/2)", 2 * mp.e ** (-ETA_HALF), "plane dim x one-sided transfer"),
    ("2 exp(-eta)", 2 * mp.e ** (-ETA), "plane dim x full transfer action"),
    ("2(1 - eta/2) = 35/18", mp.mpf(35) / 18, "plane dim x linearized transfer"),
    ("3/2", mp.mpf(3) / 2, "T8/A3 inverse-ish small sector ratio"),
    ("5/3", mp.mpf(5) / 3, "S5/A3 image-split ratio"),
    ("D2 (warped ell=2 DtN)", D2, "warped ell=2 DtN eigenvalue; typed-branch angular-sector candidate"),
]

# All 49 pairwise quotients, computed mechanically, no hand-picking.
CANDIDATES_RATIO = [
    (f"[{en}] / [{mn}]", ev / mv, f"quotient of declared candidates")
    for (en, ev, _) in CANDIDATES_C_E1
    for (mn, mv, _) in CANDIDATES_C_M1
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def frac_dev(value, target):
    """Signed fractional deviation (value - target) / target."""
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


def look_elsewhere(candidates, required):
    """Crude uniform-null look-elsewhere accounting for one slot.

    K candidates spread over the candidate-value range [min, max].
    Under a uniform null in which each candidate value is an independent
    uniform draw over that range, the chance one candidate falls within the
    fractional tolerance window of the required value is
    (2 * tol * |required|) / range, so the expected accidental count is
    E = K * 2 * tol * |required| / range.

    CRUDENESS (stated, per the contract): this is an order-of-magnitude
    estimate only. The range is itself estimated from the candidates
    (partly circular), the candidates are NOT uniform draws (they cluster:
    several are within O(eta) of each other, raising the local density near
    1 and 2 well above uniform), and K is small. Treat E as a floor on the
    accidental expectation near clustered values, not a precise null.
    """
    values = [v for (_, v, *_) in candidates]
    k = len(values)
    lo, hi = min(values), max(values)
    rng = hi - lo
    e_hit = k * 2 * TOL_HIT * abs(required) / rng
    e_lead = k * 2 * TOL_LEAD * abs(required) / rng
    return k, lo, hi, rng, e_hit, e_lead


def print_candidate_table(slot_name, candidates, required, branch_name):
    print(f"  Slot {slot_name}, branch {branch_name}:")
    print(f"    required value: {fmt(required)}")
    print(f"    {'candidate':<42} {'value':>16} {'signed frac dev':>16}  class")
    results = []
    for entry in candidates:
        name, value = entry[0], entry[1]
        dev = frac_dev(value, required)
        cls = classify(dev)
        results.append((name, value, dev, cls))
        print(f"    {name:<42} {fmt(value, 10):>16} {mp.nstr(dev, 6):>16}  {cls}")
    k, lo, hi, rng, e_hit, e_lead = look_elsewhere(candidates, required)
    print(f"    look-elsewhere: K = {k}, candidate range = "
          f"[{fmt(lo, 8)}, {fmt(hi, 8)}], width = {fmt(rng, 8)}")
    print(f"      expected accidental HITs  (uniform null, crude): "
          f"{mp.nstr(e_hit, 4)}")
    print(f"      expected accidental LEADs (uniform null, crude): "
          f"{mp.nstr(e_lead, 4)}")
    print("      (crude: range estimated from the candidates themselves;")
    print("       candidates cluster, so the uniform null UNDERSTATES the")
    print("       accidental expectation near the clusters; order-of-")
    print("       magnitude only.)")
    print()
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 72)
    print("FROZEN LEPTON LADDER TEST")
    print("Pre-registered contract: lepton_ladder_falsification_contract.md")
    print("(committed at git 26fc757 BEFORE this run)")
    print("=" * 72)
    print()

    # -- Frozen model echo + precision cross-checks --------------------------
    print("FROZEN MODEL (echo)")
    print("-" * 72)
    print(f"  eta = 1/18, eta/2 = 1/36, N = 3, depths (M1, E1) = (5, 7)")
    print(f"  gamma_local  = 3 exp(-1/36)      = {fmt(GAMMA_LOCAL, 15)}")
    print(f"    repo cross-check 2.91781343135 : "
          f"|diff| = {mp.nstr(abs(GAMMA_LOCAL - GAMMA_LOCAL_PUBLISHED), 3)}")
    assert abs(GAMMA_LOCAL - GAMMA_LOCAL_PUBLISHED) < mp.mpf("5e-12"), (
        "gamma_local disagrees with the published repo value"
    )
    print(f"  B = I_(7/2)(6 sqrt 2)/I_(5/2)(6 sqrt 2) = {fmt(B_WARP, 15)}")
    try:
        from scipy.special import iv
        b_scipy = iv(3.5, float(ARG_B)) / iv(2.5, float(ARG_B))
        print(f"    scipy cross-check               = {b_scipy:.15g}  "
              f"(|diff| = {abs(float(B_WARP) - b_scipy):.2e})")
        assert abs(float(B_WARP) - b_scipy) < 1e-12
    except ImportError:
        print("    (scipy unavailable; mpmath value used alone)")
    print(f"  gamma_warped = 3 exp(-B/36)      = {fmt(GAMMA_WARPED, 15)}")
    print(f"  D2 = sqrt(6) I_(7/2)(6 sqrt 6)/I_(5/2)(6 sqrt 6) = {fmt(D2, 15)}")
    try:
        from scipy.special import iv
        d2_scipy = (6 ** 0.5) * iv(3.5, float(ARG_D2)) / iv(2.5, float(ARG_D2))
        print(f"    scipy cross-check               = {d2_scipy:.15g}  "
              f"(|diff| = {abs(float(D2) - d2_scipy):.2e})")
        assert abs(float(D2) - d2_scipy) < 1e-12
    except ImportError:
        pass
    print(f"  M2 stance: conditionally demoted per Pbundle0 (frozen; part of")
    print(f"             the falsification surface, not adjustable).")
    print()
    print("  Targets (observed, repo diagnostic lane):")
    print(f"    m_mu/m_e   = {fmt(MU_OVER_E)}")
    print(f"    m_tau/m_e  = {fmt(TAU_OVER_E)}")
    print(f"    m_tau/m_mu = {fmt(TAU_OVER_MU)}")
    print("  Caveat (noted, not corrected for): measured ratios include EM")
    print("  self-energy; the geometric model targets the full physical ratio.")
    print()

    branches = [
        ("local", GAMMA_LOCAL),
        ("warped", GAMMA_WARPED),
    ]

    # -- T1 -------------------------------------------------------------------
    print("T1 — PURE EQUAL-COEFFICIENT LADDER (baseline pressure; no pass")
    print("     threshold). Signed fractional deviation = (pred - obs)/obs.")
    print("-" * 72)
    for bname, g in branches:
        g5, g7, g2 = g**5, g**7, g**2
        print(f"  Branch {bname}: gamma = {fmt(g, 15)}")
        print(f"    gamma^5 = {fmt(g5)}   vs m_mu/m_e   = {fmt(MU_OVER_E)}"
              f"   dev = {mp.nstr(frac_dev(g5, MU_OVER_E), 6)}")
        print(f"    gamma^7 = {fmt(g7)}   vs m_tau/m_e  = {fmt(TAU_OVER_E)}"
              f"   dev = {mp.nstr(frac_dev(g7, TAU_OVER_E), 6)}")
        print(f"    gamma^2 = {fmt(g2)}   vs m_tau/m_mu = {fmt(TAU_OVER_MU)}"
              f"   dev = {mp.nstr(frac_dev(g2, TAU_OVER_MU), 6)}")
        print()

    # -- T2 -------------------------------------------------------------------
    print("T2 — REQUIRED-COEFFICIENT EXTRACTION  *** DIAGNOSTIC ONLY ***")
    print("     These are NOT evidence and must not be promoted.")
    print("-" * 72)
    required = {}
    for bname, g in branches:
        c_m1_req = MU_OVER_E / g**5
        c_e1_req = TAU_OVER_E / g**7
        ratio_req = c_e1_req / c_m1_req
        required[bname] = (c_m1_req, c_e1_req, ratio_req)
        print(f"  Branch {bname}:")
        print(f"    C_M1_req       = (m_mu/m_e)/gamma^5  = {fmt(c_m1_req)}")
        print(f"    C_E1_req       = (m_tau/m_e)/gamma^7 = {fmt(c_e1_req)}")
        print(f"    C_E1_req/C_M1_req                    = {fmt(ratio_req)}")
        print()

    # -- T3 -------------------------------------------------------------------
    print("T3 — PRE-DECLARED NATIVE CANDIDATE MATCH")
    print(f"     Tolerances: HIT |dev| <= 1e-4, LEAD |dev| <= 1e-3, else MISS.")
    print("     Known-limitation disclosure applies: the required values were")
    print("     already published (~0.9777 / ~1.9312 / ~1.9753), so %-level")
    print("     matches are UNINFORMATIVE by pre-registration.")
    print("-" * 72)
    t3_results = {}
    for bname, _ in branches:
        c_m1_req, c_e1_req, ratio_req = required[bname]
        t3_results[(bname, "C_M1")] = print_candidate_table(
            "C_M1 (7 candidates)", CANDIDATES_C_M1, c_m1_req, bname)
        t3_results[(bname, "C_E1")] = print_candidate_table(
            "C_E1 (7 candidates)", CANDIDATES_C_E1, c_e1_req, bname)
        t3_results[(bname, "ratio")] = print_candidate_table(
            "C_E1/C_M1 (49 mechanical pairwise quotients)",
            CANDIDATES_RATIO, ratio_req, bname)

    # -- T4 -------------------------------------------------------------------
    print("T4 — BRANCH HANDLING (pre-registered rule)")
    print("-" * 72)
    print("  Confirmed: NO averaging of branches was performed anywhere above.")
    print("  Confirmed: NO per-observable branch choice was made; both branches")
    print("  were run identically through T1-T3 and both are reported in full.")
    fits = {}
    for bname, _ in branches:
        fits[bname] = {
            slot: [r for r in t3_results[(bname, slot)] if r[3] in ("HIT", "LEAD")]
            for slot in ("C_M1", "C_E1", "ratio")
        }
    cross_branch_split = (
        (fits["local"]["C_M1"] and not fits["local"]["C_E1"]
         and fits["warped"]["C_E1"] and not fits["warped"]["C_M1"])
        or
        (fits["warped"]["C_M1"] and not fits["warped"]["C_E1"]
         and fits["local"]["C_E1"] and not fits["local"]["C_M1"])
    )
    for bname in ("local", "warped"):
        summary = ", ".join(
            f"{slot}: {len(fits[bname][slot])} hit/lead"
            for slot in ("C_M1", "C_E1", "ratio")
        )
        print(f"  Branch {bname} hit/lead census — {summary}")
    if cross_branch_split:
        print("  RULE TRIGGERED: one branch fits one lepton and the other branch")
        print("  the other — per the contract this is a MISS for BOTH branches")
        print("  (branch selection must come from a derivation, not the fit).")
    else:
        print("  Cross-branch split rule (one branch per lepton): NOT triggered.")
    print()

    # -- Context: finite-cell diagnostics (NOT candidates) --------------------
    print("CONTEXT ONLY — FINITE-CELL DIAGNOSTICS (NOT CANDIDATES)")
    print("  Per the contract's final paragraph these are unexplained numerics;")
    print("  they may only be compared as additional context, clearly labeled.")
    print("  They do NOT enter T3 classification or look-elsewhere counts.")
    print("-" * 72)
    for bname, _ in branches:
        c_m1_req, c_e1_req, _ = required[bname]
        print(f"  Branch {bname}:")
        print(f"    finite-cell C_M1 = 1.1343262 vs required {fmt(c_m1_req, 10)}"
              f"  -> dev = {mp.nstr(frac_dev(FINITE_CELL_C_M1, c_m1_req), 6)}")
        print(f"    finite-cell C_E1 = 2.10394   vs required {fmt(c_e1_req, 10)}"
              f"  -> dev = {mp.nstr(frac_dev(FINITE_CELL_C_E1, c_e1_req), 6)}")
    print()

    # -- T5 -------------------------------------------------------------------
    print("T5 — VERDICT (per the contract's verdict rules)")
    print("-" * 72)
    any_hit = any(
        r[3] == "HIT" for results in t3_results.values() for r in results
    )
    any_lead = any(
        r[3] == "LEAD" for results in t3_results.values() for r in results
    )
    t1_percent_or_worse = all(
        abs(frac_dev(g**d, t)) >= mp.mpf("0.01")
        for _, g in branches
        for d, t in ((5, MU_OVER_E), (7, TAU_OVER_E), (2, TAU_OVER_MU))
    )
    print(f"  T1 deviations at percent level or worse (all branches/slots): "
          f"{t1_percent_or_worse}")
    print(f"  T3 HITs:  {any_hit}")
    print(f"  T3 LEADs: {any_lead}")
    print()
    if any_hit:
        print("  VERDICT: T3 produced at least one HIT. Per the contract this is")
        print("  still NOT a derivation — record as a sharp target and require the")
        print("  variational derivation of that specific coefficient before any")
        print("  grade rises. Each HIT is reported above WITH its look-elsewhere")
        print("  expectation; check that expectation before treating the HIT as")
        print("  surviving.")
    elif any_lead:
        print("  VERDICT: T3 produced LEAD(s) but no HIT. Per the contract:")
        print("  record as a lead for the named candidate(s) ONLY, with rationale,")
        print("  for future derivation work. DO NOT BANK. Each LEAD is reported")
        print("  above WITH its look-elsewhere expectation.")
        if t1_percent_or_worse:
            print("  T1 baseline remains percent-level-or-worse: the bare frozen")
            print("  ladder is under FALSIFICATION PRESSURE independent of leads.")
    else:
        print("  VERDICT: FALSIFICATION PRESSURE on the frozen [depths 5/7 +")
        print("  gamma] model. T1 deviations are at the percent level or worse")
        print("  and T3 produced no HIT (and no LEAD). The required-coefficient")
        print("  pressure numbers (T2) become the STANDING CONSTRAINT that any")
        print("  future derivation of the branch coefficients must hit:")
        for bname, _ in branches:
            c_m1_req, c_e1_req, ratio_req = required[bname]
            print(f"    {bname:>6}: C_M1 = {fmt(c_m1_req)}, "
                  f"C_E1 = {fmt(c_e1_req)}, ratio = {fmt(ratio_req)}")
        print("  No element of the frozen model (depths 5/7, eta, N, gamma form,")
        print("  candidate lists, M2 stance) may be adjusted in response.")


if __name__ == "__main__":
    main()
