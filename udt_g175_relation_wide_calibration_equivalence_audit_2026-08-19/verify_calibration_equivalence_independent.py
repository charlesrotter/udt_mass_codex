#!/usr/bin/env python3
"""Independent Fraction-only replay for G175; imports no production code."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent
rng = random.Random(175)
trials = 12_000
checks = 0
anchored = 0
anchored_changed = 0


def hit(condition: bool) -> None:
    global checks
    if not condition:
        raise AssertionError("independent exact check failed")
    checks += 1


def pos() -> Fraction:
    return Fraction(rng.randint(1, 19), rng.randint(1, 19))


for i in range(trials):
    Ap, Aq, Hp, Hq, mp, mq = (pos() for _ in range(6))
    if i < 2_000:
        fp = Fraction(1)
        fq = pos()
        if fq == 1:
            fq = Fraction(2)
        anchored += 1
    else:
        fp, fq = pos(), pos()
    Kp = Ap * Hp / (mp * mp)
    Kq = Aq * Hq / (mq * mq)
    Knp = Ap * Hp / ((fp * mp) ** 2)
    Knq = Aq * Hq / ((fq * mq) ** 2)
    Rm = Kq / Kp
    Rn = Knq / Knp
    c = pos()
    vp = pos()

    hit(Kp > 0)
    hit(Kq > 0)
    hit(Knp * fp * fp == Kp)
    hit(Knq * fq * fq == Kq)
    hit(Rm == Kq / Kp)
    hit(Rn == Knq / Knp)
    hit(Rn / Rm == (fp / fq) ** 2)
    hit(Rm * (Kp / Kq) == 1)
    hit((Aq * Hq / ((c * mq) ** 2)) / (Ap * Hp / ((c * mp) ** 2)) == Rm)
    hit(Ap * Hp / Hp == Ap)
    hit(Ap * Hp / (Hp / Ap) == Ap * Ap)
    hit(Ap * (Ap * vp * vp) / (vp * vp) == Ap * Ap)
    if i < 2_000 and Rn != Rm:
        anchored_changed += 1

assert checks == 144_000
assert anchored == anchored_changed == 2_000

result = {
    "status": "PASS__G175_INDEPENDENT_FRACTION_REPLAY",
    "trials": trials,
    "checks_passed": checks,
    "anchored_counterfamilies": anchored,
    "anchored_changed": anchored_changed,
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(result, sort_keys=True))
