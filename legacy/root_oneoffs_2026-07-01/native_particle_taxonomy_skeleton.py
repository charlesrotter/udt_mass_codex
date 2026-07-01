from fractions import Fraction


def fmt(value):
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"
    return str(value)


def main():
    image_unit = Fraction(1, 12)

    primary_sectors = {
        "trace": {
            "dimension": 1,
            "role": "value/normalization scalar",
            "commutator_status": "central; not in active T8 image",
            "readout_weight": None,
        },
        "A3": {
            "dimension": 3,
            "role": "antisymmetric/rotation-like traceless image",
            "commutator_status": "active",
            "readout_weight": 3 * image_unit,
        },
        "S5": {
            "dimension": 5,
            "role": "symmetric-traceless/shape-like traceless image",
            "commutator_status": "active",
            "readout_weight": 5 * image_unit,
        },
        "T8": {
            "dimension": 8,
            "role": "full active traceless image",
            "commutator_status": "active",
            "readout_weight": 8 * image_unit,
        },
    }

    twoform_channels = {
        "trace_wedge_T8": {
            "domain": 8,
            "image": 0,
            "kernel": 8,
            "rule": "central silent channel",
        },
        "A3_wedge_A3": {
            "domain": 3,
            "image": 3,
            "kernel": 0,
            "rule": "self-interaction returns A3",
        },
        "A3_wedge_S5": {
            "domain": 15,
            "image": 5,
            "kernel": 10,
            "rule": "mixed interaction returns S5",
        },
        "S5_wedge_S5": {
            "domain": 10,
            "image": 3,
            "kernel": 7,
            "rule": "shape-shape interaction returns A3",
        },
    }

    threeform_support = {
        "trace_wedge_Lambda2_T8": {
            "domain": 28,
            "support": 0,
            "status": "trace kernel",
        },
        "Lambda3_A3": {
            "domain": 1,
            "support": "nonzero",
            "status": "orientation-like A3 triple support",
        },
        "Lambda2_A3_wedge_S5": {
            "domain": 15,
            "support": 0,
            "status": "filtered out",
        },
        "A3_wedge_Lambda2_S5": {
            "domain": 30,
            "support": "nonzero",
            "status": "mixed A3/S5 support",
        },
        "Lambda3_S5": {
            "domain": 10,
            "support": 0,
            "status": "pure S5 triple filtered out",
        },
    }

    taxonomy = {
        "container": "negative-phi mass-emergence container with H1 angular carrier",
        "alphabet": "End(H1)=trace + A3 + S5 = 1+3+5",
        "active_image": "T8=A3+S5",
        "readout_candidate": "W(P)=Tr(P)/12 on active T8 projectors",
        "primary_sectors": {
            name: {
                **data,
                "readout_weight": fmt(data["readout_weight"])
                if data["readout_weight"] is not None
                else None,
            }
            for name, data in primary_sectors.items()
        },
        "twoform_channels": twoform_channels,
        "threeform_support": threeform_support,
        "taxonomy_verdict": {
            "derived": "metric/operator taxonomy before particle labels",
            "not_derived": "mapping to electron/muon/pion/proton or mass values",
            "next": "derive whether radial negative-phi readout couples to A3, S5, T8, two-form channels, or three-form support",
        },
    }

    print("taxonomy:")
    for key, value in taxonomy.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
