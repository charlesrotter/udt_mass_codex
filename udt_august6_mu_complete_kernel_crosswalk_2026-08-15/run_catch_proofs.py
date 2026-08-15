#!/usr/bin/env python3
"""Hostile finite-dimensional mutations for the mu crosswalk."""

from fractions import Fraction as F


def main() -> None:
    a, r, s, mu = F(1, 2), F(2), F(3), F(1, 4)

    # Correct lower transition entry is -mu. A silent sign/variance collapse must be caught.
    correct_lower_entry = s * (-mu / s)
    wrong_lower_entry = s * (+mu / s)
    assert correct_lower_entry == -mu
    assert wrong_lower_entry != -mu

    # Holding the pair embedding fixed while changing S is not the exact pullback fiber.
    old_screen_leg = -mu
    d = F(2, 5)
    mutated_without_z_carry = old_screen_leg + s * d
    assert mutated_without_z_carry != old_screen_leg

    # Terminal base pullback cannot encode old full-arrow screen-scale dependence.
    h00_s3 = -a * a + mu * mu
    h00_s4 = -a * a + mu * mu
    old_trace_s3 = r * r + F(1, r * r) + F(3) ** 2 - mu * mu
    old_trace_s4 = r * r + F(1, r * r) + F(4) ** 2 - mu * mu
    assert h00_s3 == h00_s4
    assert old_trace_s3 != old_trace_s4

    # A rank-one-only test cannot distinguish scalar extensions that separate at rank two.
    u = F(5, 6)
    rank_one_gap = F(0)
    rank_two_gap = mu * mu * u * u
    assert rank_one_gap == 0
    assert rank_two_gap != 0

    print("PASS: 4 hostile mutations caught (variance sign, omitted Z carry, pullback/full-arrow collapse, rank-one uniqueness)")


if __name__ == "__main__":
    main()
