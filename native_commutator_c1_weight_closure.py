from fractions import Fraction


def main():
    domain_dim = 36
    h1_dim = 3
    image_dim = 8

    c1_side_domain_weight = Fraction(1, domain_dim)
    commutator_isotropy_factor = Fraction(3)
    output_weight_per_t8_direction = c1_side_domain_weight * commutator_isotropy_factor

    q = Fraction(1, 3)
    c1_unprojected_action = q * q / (4 * (1 - 2 * q))
    c1_h1_projected_action = c1_unprojected_action / h1_dim
    image_total_weight = image_dim * output_weight_per_t8_direction
    threeform_active_fraction = Fraction(56, 84)
    threeform_trace_kernel_fraction = Fraction(28, 84)

    checks = {
        "domain_weight_eta_half": c1_side_domain_weight,
        "commutator_BBt_factor": commutator_isotropy_factor,
        "output_weight_per_T8_direction": output_weight_per_t8_direction,
        "C1_unprojected_action": c1_unprojected_action,
        "C1_H1_projected_action": c1_h1_projected_action,
        "output_equals_unprojected_C1_action": output_weight_per_t8_direction
        == c1_unprojected_action,
        "domain_weight_equals_projected_C1_action": c1_side_domain_weight
        == c1_h1_projected_action,
        "image_total_weight": image_total_weight,
        "threeform_active_fraction": threeform_active_fraction,
        "threeform_trace_kernel_fraction": threeform_trace_kernel_fraction,
        "image_total_weight_equals_threeform_active_fraction": image_total_weight
        == threeform_active_fraction,
    }

    interpretation = {
        "closure": "Uniform C1 side weight 1/36 on Lambda^2 End(H1), pushed through the commutator isotropy BBt=3P_T8, gives 1/12 on each T8 image direction.",
        "C1_match": "1/12 is exactly the unprojected self-similar C1 action S_C1/R at q=1/3.",
        "projection_pair": "The same C1 action appears as 1/36 when H1-projected and as 1/12 after commutator projection onto T8.",
        "twoform_threeform_link": "The total T8 image weight is 2/3, matching the active Lambda^3 T8 fraction inside Lambda^3 End(H1).",
        "not_mass": "This is a normalization closure for the operator selector, not a mass spectrum.",
    }

    print(f"checks: {checks}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()
