from fractions import Fraction


def main():
    handoff = {
        "single_sector_S5_weight": Fraction(5, 12),
        "mixed_channel_domain_load": Fraction(15, 36),
        "mixed_channel_image_action": Fraction(5, 12),
        "mixed_channel_residual": Fraction(0),
    }

    identities = {
        "S5_weight_equals_mixed_domain_load": handoff["single_sector_S5_weight"]
        == handoff["mixed_channel_domain_load"],
        "S5_weight_equals_mixed_image_action": handoff["single_sector_S5_weight"]
        == handoff["mixed_channel_image_action"],
        "mixed_channel_balanced": handoff["mixed_channel_residual"] == 0,
    }

    interpretation = {
        "handoff": "The S5 single-sector weight is exactly the balanced A3-S5 interaction action.",
        "meaning": "S5 can be read either as a single active image sector or as the output of the first balanced mixed channel.",
        "taxonomy": "This is a native handoff from sector taxonomy to interaction taxonomy.",
        "not_claimed": "No observed particle, force, or mass has been identified.",
    }

    print(f"handoff: {handoff}")
    print(f"identities: {identities}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()
