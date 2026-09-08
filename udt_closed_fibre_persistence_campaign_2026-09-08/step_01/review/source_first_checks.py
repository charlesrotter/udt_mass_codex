"""Independent exact finite support for SOURCE_FIRST_ARGUMENT, no author imports."""
import fractions
import json
import math
import platform
import sys

F = fractions.Fraction
checks = []

def check(name, actual, expected):
    row = {"name": name, "actual": str(actual), "expected": str(expected),
           "passed": actual == expected}
    checks.append(row)
    if actual != expected:
        raise AssertionError(row)

def rotation_order(turns):
    """Exact rational circle rotation; determine order by actual iterates."""
    turns = F(turns)
    for n in range(1, turns.denominator + 1):
        if (n * turns).denominator == 1:
            return n
    raise AssertionError("no rational return")

cases = []
for p in range(1, 10):
    for q in range(1, 10):
        if math.gcd(p, q) != 1:
            continue
        slope = F(p, q)
        # Enumerate simultaneous angular returns, independently of order formula.
        periods = [n for n in range(1, q + 1)
                   if (n * slope).denominator == 1]
        check(f"interior_return_{p}_{q}", periods, [q])
        axis0, axis1 = rotation_order(slope), rotation_order(1 / slope)
        check(f"axis0_order_{p}_{q}", axis0, q)
        check(f"axis1_order_{p}_{q}", axis1, p)
        check(f"both_axes_trivial_{p}_{q}", axis0 == axis1 == 1, p == q == 1)
        # At s=1 a central traversal has time 2pi/slope, NOT 2pi.
        check(f"axis1_time_{p}_{q}", F(1, 1) / slope, F(q, p))
        cases.append({"p": p, "q": q, "slope": str(slope),
                      "interior_period_in_2pi": q,
                      "axis0_holonomy_order": axis0,
                      "axis1_holonomy_order": axis1})

# Cartesian tangent/nonzero checks at rational points on S3. X=(iz1, i*r*z2).
for x1, y1, x2, y2 in [(F(1),F(0),F(0),F(0)),
                       (F(0),F(0),F(1),F(0)),
                       (F(3,5),F(0),F(4,5),F(0)),
                       (F(1,2),F(1,2),F(1,2),F(1,2))]:
    s = x2*x2 + y2*y2
    for r in (F(1), F(2,3), F(7,5)):
        pos = (x1,y1,x2,y2)
        vel = (-y1,x1,-r*y2,r*x2)
        tag = f"{pos}_{r}"
        check("tangency_" + tag, sum(x*v for x,v in zip(pos,vel)), F(0))
        check("s_conserved_" + tag, 2*x2*vel[2]+2*y2*vel[3], F(0))
        norm = sum(v*v for v in vel)
        check("norm_formula_" + tag, norm, (1-s)+r*r*s)
        check("nonzero_" + tag, norm > 0, True)

# Nonreduced rational input must still reduce before assigning exceptional orders.
check("reduce_6_4_axis0", rotation_order(F(6,4)), 2)
check("reduce_6_4_axis1", rotation_order(1/F(6,4)), 3)
check("rescale_speed_same_3_2", F(15,10), F(3,2))
check("invert_leaf_orientation_order", rotation_order(-F(3,2)), 2)

# Concrete proposed false criteria, evaluated against return-map witnesses.
# These are actual finite defect catches, not evidence about all smooth fields.
catches = []
for label, proposed_regular, p, q in [
    ("rational_implies_regular", True, 3, 2),
    ("one_trivial_axis_suffices", True, 2, 1),
    ("other_trivial_axis_suffices", True, 1, 2),
    ("near_one_implies_regular", True, 101, 100),
]:
    observed = (rotation_order(F(p,q)) == 1 and rotation_order(F(q,p)) == 1)
    caught = proposed_regular != observed
    check(label, caught, True)
    catches.append({"mutation": label, "proposed_regular": proposed_regular,
                    "actual_axis_orders": [rotation_order(F(p,q)),rotation_order(F(q,p))],
                    "caught": caught})

print(json.dumps({"scope": "finite exact rational/Cartesian checks; proof owns real/smooth quantifiers",
                  "python": sys.version, "platform": platform.platform(),
                  "cases": cases, "checks": checks, "defect_catches": catches,
                  "all_passed": all(x["passed"] for x in checks)}, indent=2))
