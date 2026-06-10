from fractions import Fraction


def main():
    branches = {
        "single_sector_action": {
            "objects": ["A3", "S5", "T8"],
            "readout": {
                "A3": Fraction(1, 4),
                "S5": Fraction(5, 12),
                "T8": Fraction(2, 3),
            },
            "radial_status": "common q=1/3 branch",
            "residual": "none inside the readout; no interaction channel used",
            "status": "simplest taxonomy branch",
            "missing": "map to observed species or generation/depth rule",
        },
        "balanced_twoform_channel": {
            "objects": ["A3 wedge S5 -> S5"],
            "domain_load": Fraction(5, 12),
            "image_action": Fraction(5, 12),
            "residual": Fraction(0),
            "status": "first balanced interaction branch",
            "missing": "source-overlap/physical interpretation",
        },
        "pure_A3_channel": {
            "objects": ["A3 wedge A3 -> A3"],
            "domain_load": Fraction(1, 12),
            "image_action": Fraction(1, 4),
            "residual": Fraction(-1, 6),
            "status": "requires q/2 accounting",
            "missing": "boundary momentum/source supply interpretation",
        },
        "pure_S5_channel": {
            "objects": ["S5 wedge S5 -> A3"],
            "domain_load": Fraction(5, 18),
            "image_action": Fraction(1, 4),
            "residual": Fraction(1, 36),
            "status": "requires eta/2 accounting",
            "missing": "side-action/source residual interpretation",
        },
        "threeform_support": {
            "objects": ["Lambda3 A3", "A3 wedge Lambda2 S5"],
            "full_domain": 84,
            "active_domain": 56,
            "status": "native higher-order support",
            "missing": "why radial readout should use three-form scalar",
        },
    }

    recommended_order = [
        "single_sector_action",
        "balanced_twoform_channel",
        "pure_S5_channel",
        "pure_A3_channel",
        "threeform_support",
    ]

    verdict = {
        "first_test": "single_sector_action",
        "reason": "It needs only the derived common radial branch and projector trace readout.",
        "first_interaction_test": "balanced_twoform_channel",
        "reason_interaction": "A3 wedge S5 balances exactly without residual source accounting.",
        "defer": ["pure_A3_channel", "pure_S5_channel", "threeform_support"],
        "guardrail": "Do not attach lepton/hadron names until a species/readout map is derived.",
    }

    print(f"branches: {branches}")
    print(f"recommended_order: {recommended_order}")
    print(f"verdict: {verdict}")


if __name__ == "__main__":
    main()
