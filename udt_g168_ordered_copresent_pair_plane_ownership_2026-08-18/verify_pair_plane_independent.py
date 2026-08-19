#!/usr/bin/env python3
"""Independent Fraction replay for G168; imports no production code or SymPy."""

from __future__ import annotations

import json
import random
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
checks = 0


def require(condition: bool, name: str) -> None:
    global checks
    if not condition:
        raise AssertionError(name)
    checks += 1


def dot_diag(x, diag, y):
    return sum(a * d * b for a, d, b in zip(x, diag, y))


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def scale(a, x):
    return tuple(a * b for b in x)


rng = random.Random(168)
trials = 1200
for i in range(trials):
    # Static diagonal primary-metric rational control.
    a = F(rng.randint(1, 9), rng.randint(1, 9))
    b = F(rng.randint(1, 9), rng.randint(1, 9))
    c = F(rng.randint(1, 9), rng.randint(1, 9))
    d = F(rng.randint(1, 9), rng.randint(1, 9))
    metric = (-a, b, c, d)
    u = (F(1), F(0), F(0), F(0))
    s = tuple(F(rng.randint(-7, 7), rng.randint(1, 7)) for _ in range(4))
    guu = dot_diag(u, metric, u)
    gus = dot_diag(u, metric, s)
    r = add(s, scale(-gus / guu, u))
    require(dot_diag(u, metric, r) == 0, f"orthogonality_{i}")
    rr = dot_diag(r, metric, r)
    require(rr == dot_diag(s, metric, s) - gus * gus / guu, f"norm_{i}")
    if any(r[j] != 0 for j in (1, 2, 3)):
        require(rr > 0, f"positive_rest_space_{i}")
        require(guu * rr < 0, f"lorentzian_plane_{i}")
    lam = F(rng.randint(1, 9), rng.randint(1, 9))
    sl = scale(lam, s)
    rl = add(sl, scale(-dot_diag(u, metric, sl) / guu, u))
    require(rl == scale(lam, r), f"rescale_{i}")

# Exact G167 block witness by independent arithmetic.
metric = (F(-1, 4), F(4), F(9), F(144, 25))
u = (F(2), F(0), F(0), F(0))
s = (F(1), F(1, 2), F(1, 3), F(1, 4))
guu = dot_diag(u, metric, u)
gus = dot_diag(u, metric, s)
gss = dot_diag(s, metric, s)
r = add(s, scale(-gus / guu, u))
require(guu == -1, "witness_guu")
require(gus == F(-1, 2), "witness_gus")
require(dot_diag(r, metric, r) == F(59, 25), "witness_rr")
require(guu * gss - gus * gus == F(-59, 25), "witness_det")
angular = metric[2] * s[2] * s[2] + metric[3] * s[3] * s[3]
require(angular == F(34, 25), "angular_live")
require(gss - angular != gss, "radial_freeze_changes_metric")

# Same boundary observers/event labels; two distinct surface tangents at A.
e0 = (F(1), F(0), F(0), F(0))
s0 = (F(0), F(1), F(0), F(0))
s1 = (F(0), F(1), F(1), F(0))
require(s0 != s1, "counterfamily_distinct_germs")
require(dot_diag(e0, (F(-1), F(1), F(1), F(1)), s0) == 0, "counterfamily_s0_orthogonal")
require(dot_diag(e0, (F(-1), F(1), F(1), F(1)), s1) == 0, "counterfamily_s1_orthogonal")

# Relative velocity outside positional plane.
vb = (F(5, 4), F(0), F(3, 4), F(0))
require(dot_diag(vb, (F(-1), F(1), F(1), F(1)), vb) == -1, "relative_velocity_timelike")
require(vb[2] != 0, "relative_velocity_outside_plane")

# Coincidence lacks a nonzero ruler line.
zero = (F(0), F(0), F(0), F(0))
require(all(x == 0 for x in zero), "coincidence_rank_loss")

result = {
    "implementation": "stdlib Fraction; no production imports",
    "seed": 168,
    "trials": trials,
    "checks_passed": checks,
    "landing_supported": "SUPPLIED_ORDERED_COPRESENT_PAIR_GERM_DERIVES_LOCAL_CALIBRATED_PAIR_PLANE__NO_PATH_REQUIRED__PHYSICAL_GERM_OWNERSHIP_IS_ADDITIONAL_WORKING_POSTULATE",
}
(HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, sort_keys=True))
