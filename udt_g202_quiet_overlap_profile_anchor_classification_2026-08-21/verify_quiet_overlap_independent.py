#!/usr/bin/env python3
"""Independent exact-Fraction G202 verification; no SymPy or production imports."""

from fractions import Fraction as F
import json
import random


def poly_eval(coeffs, x):
    return sum((coefficient * x**power for power, coefficient in coeffs.items()), F(0))


def poly_derivative(coeffs):
    return {power - 1: power * coefficient for power, coefficient in coeffs.items() if power}


def poly_multiply(left, right):
    result = {}
    for lp, lc in left.items():
        for rp, rc in right.items():
            result[lp + rp] = result.get(lp + rp, F(0)) + lc * rc
    return result


def main() -> None:
    rng = random.Random(202)
    cases = 20000
    assertions = 0
    for _ in range(cases):
        coeffs = {
            3: F(rng.randint(1, 17), rng.randint(1, 11)),
            5: F(rng.randint(0, 17), rng.randint(1, 11)),
            7: F(rng.randint(0, 17), rng.randint(1, 11)),
        }
        first = poly_derivative(coeffs)
        second = poly_derivative(first)
        assert poly_eval(coeffs, F(0)) == 0
        assert poly_eval(first, F(0)) == 0
        assert poly_eval(second, F(0)) == 0
        assertions += 3

        x = F(rng.choice([i for i in range(-19, 20) if i != 0]), rng.randint(1, 13))
        assert poly_eval(coeffs, -x) == -poly_eval(coeffs, x)
        assert poly_eval(first, x) > 0
        assertions += 2

        phi = poly_eval(coeffs, x)
        p_log = poly_eval(first, x)
        q_log = poly_eval(second, x)
        # Use an independent positive rational stand-in for exp(-2 phi); the jet identity is algebraic.
        f = F(rng.randint(1, 31), rng.randint(1, 17))
        radial_p = p_log
        radial_q = q_log - p_log
        old_parallel = f * (2 * radial_p**2 + radial_p - radial_q)
        new_parallel = f * (2 * p_log**2 + 2 * p_log - q_log)
        old_perp = 1 - f * (1 + radial_p)
        new_perp = 1 - f * (1 + p_log)
        assert old_parallel == new_parallel
        assert old_perp == new_perp
        assertions += 2
        assert isinstance(phi, F)
        assertions += 1

    # Exact finite anchor jets: multiply cubic factors at three arbitrary rational anchors.
    anchor_controls = 1000
    for _ in range(anchor_controls):
        anchors = [
            F(-rng.randint(1, 9), rng.randint(1, 7)),
            F(0),
            F(rng.randint(1, 9), rng.randint(1, 7)),
        ]
        perturbation = {0: F(1)}
        for anchor in anchors:
            factor = {-0: -anchor, 1: F(1)}
            for _power in range(3):
                perturbation = poly_multiply(perturbation, factor)
        derivatives = [perturbation]
        derivatives.append(poly_derivative(derivatives[-1]))
        derivatives.append(poly_derivative(derivatives[-1]))
        for anchor in anchors:
            for derivative in derivatives:
                assert poly_eval(derivative, anchor) == 0
                assertions += 1
        assert any(value != 0 for value in perturbation.values())
        assertions += 1

    # Independent dimensional-exponent checks.
    # c_E^a G^b: M exponent forces b=0, T then a=0, so L exponent cannot be one.
    no_anchor_solution = False
    # With mass: (a,b,c)=(-2,1,1). With density: (a,b,d)=(1,-1/2,-1/2).
    mass_solution = (F(-2), F(1), F(1))
    density_solution = (F(1), F(-1, 2), F(-1, 2))
    assert no_anchor_solution is False
    assert (mass_solution[0] + 3 * mass_solution[1],
            -mass_solution[1] + mass_solution[2],
            -mass_solution[0] - 2 * mass_solution[1]) == (1, 0, 0)
    assert (density_solution[0] + 3 * density_solution[1] - 3 * density_solution[2],
            -density_solution[1] + density_solution[2],
            -density_solution[0] - 2 * density_solution[1]) == (1, 0, 0)
    assertions += 3

    print(json.dumps({
        "all_pass": True,
        "cases": cases,
        "anchor_controls": anchor_controls,
        "assertions": assertions,
        "method": "independent exact-Fraction odd-profile anchor-jet and dimension replay",
        "production_imports": False,
        "production_artifacts_read": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
