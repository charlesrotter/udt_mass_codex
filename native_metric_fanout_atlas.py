from fractions import Fraction


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return value


def main():
    q = Fraction(1, 3)
    eta = Fraction(1, 18)

    nodes = {
        "negative_phi_container": {
            "role": "mass-emergence domain",
            "native_status": "pre-spectrum container",
        },
        "phi0_boundary": {
            "role": "interface between negative-phi matter cell and positive-phi scalar background",
            "native_status": "C1 boundary with exact conjugate quantities",
        },
        "trace": {
            "dimension": 1,
            "role": "scalar identity sector",
            "native_status": "central",
        },
        "H1": {
            "dimension": 3,
            "role": "first nontrivial finite angular endpoint sector",
            "native_status": "selected by endpoint/angular admissibility",
        },
        "A3": {
            "dimension": 3,
            "weight": Fraction(1, 4),
            "role": "antisymmetric traceless sector",
            "native_status": "subsector of T8",
        },
        "S5": {
            "dimension": 5,
            "weight": Fraction(5, 12),
            "role": "symmetric traceless sector",
            "native_status": "subsector of T8",
        },
        "T8": {
            "dimension": 8,
            "weight": Fraction(2, 3),
            "role": "active traceless commutator image",
            "native_status": "A3 + S5",
        },
    }

    instruments = {
        "q": q,
        "eta": eta,
        "C1_boundary_momentum": q / 2,
        "H1_projected_unit": eta,
        "one_sided_H1_transfer": eta / 2,
        "domain_unit": Fraction(1, 36),
        "image_unit": Fraction(1, 12),
    }

    roads = {
        "container_to_boundary": {
            "from": "negative_phi_container",
            "to": "phi0_boundary",
            "operation": "finite C1 boundary/conjugate data",
            "exact_quantity": "q/2",
        },
        "boundary_to_H1": {
            "from": "phi0_boundary",
            "to": "H1",
            "operation": "round S2/H1 projection",
            "exact_quantity": "eta = (q/2)/3",
        },
        "H1_to_operator_alphabet": {
            "from": "H1",
            "to": "End(H1)",
            "operation": "endomorphism algebra",
            "exact_quantity": "9 = 1 + 3 + 5",
        },
        "alphabet_to_T8": {
            "from": "End(H1)",
            "to": "T8",
            "operation": "commutator kills trace and images traceless sector",
            "exact_quantity": "T8 = A3 + S5",
        },
        "A3S5_channel": {
            "from": "A3 wedge S5",
            "to": "S5",
            "operation": "two-form commutator channel",
            "exact_quantity": "5/12 - 5/12 = 0",
            "class": "freely balanced interaction",
        },
        "S5S5_channel": {
            "from": "S5 wedge S5",
            "to": "A3",
            "operation": "two-form commutator channel",
            "exact_quantity": "5/18 - 1/4 = eta/2",
            "class": "one-sided-transfer coupled",
        },
        "A3A3_channel": {
            "from": "A3 wedge A3",
            "to": "A3",
            "operation": "two-form commutator channel",
            "exact_quantity": "1/12 - 1/4 = -q/2",
            "class": "boundary-momentum coupled",
        },
        "trace_T8_channel": {
            "from": "trace wedge T8",
            "to": "kernel load",
            "operation": "central trace killed by commutator",
            "exact_quantity": "2/9 = q * W(T8)",
            "class": "scalar/trace bridge candidate",
        },
    }

    road_checks = {
        "eta_is_projected_boundary_momentum": eta == (q / 2) / 3,
        "one_side_is_domain_unit": eta / 2 == Fraction(1, 36),
        "image_unit_is_half_boundary_momentum": Fraction(1, 12) == (q / 2) / 2,
        "A3S5_balances": Fraction(5, 12) - Fraction(5, 12) == 0,
        "S5S5_residual_is_one_side": Fraction(5, 18) - Fraction(1, 4) == eta / 2,
        "A3A3_residual_is_minus_boundary_momentum": Fraction(1, 12) - Fraction(1, 4) == -(q / 2),
        "trace_T8_load_is_q_times_T8": Fraction(2, 9) == q * Fraction(2, 3),
    }

    open_gates = {
        "trace_kernel_role": "derive whether 2/9 is boundary normalization, scalar-background bridge, or quotient load",
        "boundary_orientation_rule": "derive the sign/orientation convention for q/2 supply in A3-A3",
        "transfer_kernel_rule": "derive when eta/2 is exported as one side of a composable boundary kernel",
        "spectrum_assignment": "defer observed-particle labels until road grammar plus radial/depth rule are native",
    }

    printable_nodes = {
        key: {k: fmt(v) for k, v in value.items()} for key, value in nodes.items()
    }
    printable_instruments = {key: fmt(value) for key, value in instruments.items()}

    verdict = {
        "fanout": "the metric supplies a typed road atlas from negative phi to boundary instruments to angular operator channels",
        "progress": "this is more constrained than a ratio ladder and less committed than a particle spectrum",
        "guard": "roads are admissibility structure; they are not destinations or observed species names",
    }

    print(f"nodes: {printable_nodes}")
    print(f"instruments: {printable_instruments}")
    print(f"roads: {roads}")
    print(f"road_checks: {road_checks}")
    print(f"open_gates: {open_gates}")
    print(f"verdict: {verdict}")


if __name__ == "__main__":
    main()
