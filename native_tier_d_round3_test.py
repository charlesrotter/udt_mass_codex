#!/usr/bin/env python3
"""Tier-D round 3: evaluate the frozen S_phi0-panel conditional readings
against the six banked lepton wall numbers.

Pre-registered via tier_d_round3_contract.md (committed fe99630 BEFORE
this script ran). Candidate set, branch assignment, and classification
rule are frozen there. Immutable once committed (repo discipline).
"""

from mpmath import mp, mpf, exp, sqrt, besseli

mp.dps = 30

ETA = mpf(1) / 18


def B_ratio(lam):
    """B(lambda) = I_{7/2}(6 sqrt lam) / I_{5/2}(6 sqrt lam)."""
    x = 6 * sqrt(mpf(lam))
    return besseli(mpf(7) / 2, x) / besseli(mpf(5) / 2, x)


# --- frozen candidates (exact forms from the contract) ---------------
B2 = B_ratio(2)
B_half = B_ratio(mpf(1) / 2)

CAND_LOCAL_M1 = {
    "M1-L1 graph: 1": mpf(1),
    "M1-L2 operator: exp(1/24)": exp(mpf(1) / 24),
}
CAND_WARPED_M1 = {
    "M1-W1 same-mode-ratio: exp(eta[B(2)-B(1/2)])": exp(ETA * (B2 - B_half)),
    "M1-W2 eigenvalue-clock: exp(eta[B(2)-B(1/2)/2])": exp(ETA * (B2 - B_half / 2)),
}
C_E1 = mpf(1)  # E1-1, both branches

# contract's quoted 12-digit values (sanity cross-check)
QUOTED = {
    "M1-L2 operator: exp(1/24)": mpf("1.042546905190"),
    "M1-W1 same-mode-ratio: exp(eta[B(2)-B(1/2)])": mpf("1.011519893216"),
    "M1-W2 eigenvalue-clock: exp(eta[B(2)-B(1/2)/2])": mpf("1.025283774326"),
}

# --- wall numbers (acceptance targets, banked rounds 1-2) ------------
WALL = {
    "local": {
        "C_M1": mpf("0.977679087638"),
        "C_E1": mpf("1.93121474779"),
        "ratio": mpf("1.97530536575"),
    },
    "warped": {
        "C_M1": mpf("0.936832609588"),
        "C_E1": mpf("1.81920864981"),
        "ratio": mpf("1.94187161205"),
    },
}

HIT, LEAD = mpf("1e-4"), mpf("1e-3")


def classify(value, target):
    dev = (value - target) / target
    a = abs(dev)
    cls = "HIT" if a <= HIT else ("LEAD" if a <= LEAD else "MISS")
    return cls, dev


def main():
    # sanity: contract-quoted digits reproduce
    for name, q in QUOTED.items():
        v = CAND_LOCAL_M1.get(name) or CAND_WARPED_M1.get(name)
        assert abs(v - q) < mpf("1e-12"), (name, v, q)
    print("sanity: contract-quoted 12-digit values reproduce: PASS")
    print(f"  B(2)   = {B2}")
    print(f"  B(1/2) = {B_half}")

    tally = {"HIT": 0, "LEAD": 0, "MISS": 0}
    n = 0
    for branch, cands in (("local", CAND_LOCAL_M1), ("warped", CAND_WARPED_M1)):
        wall = WALL[branch]
        for name, c_m1 in cands.items():
            for slot, value in (
                ("C_M1", c_m1),
                ("C_E1", C_E1),
                ("ratio", C_E1 / c_m1),
            ):
                cls, dev = classify(value, wall[slot])
                tally[cls] += 1
                n += 1
                print(
                    f"[{branch:6s}] {slot:5s} {name:48s} "
                    f"value={mp.nstr(value, 13):16s} "
                    f"target={mp.nstr(wall[slot], 13):16s} "
                    f"dev={mp.nstr(dev, 6):12s} {cls}"
                )

    print(f"\ntotal comparisons: {n} (contract: 12)")
    print(f"tally: {tally}")
    verdict = (
        "CLEAN MISS" if tally["HIT"] == 0 and tally["LEAD"] == 0 else "REVIEW"
    )
    print(f"verdict: {verdict}, {tally['MISS']}/{n} miss")


if __name__ == "__main__":
    main()
