def main():
    paths = {
        "lepton_first": {
            "requires": [
                "single active readout sector",
                "radial negative-phi depth rule",
                "electron anchor",
            ],
            "available_now": [
                "C1 action readout W(P)",
                "A3/S5/T8 projector weights",
                "electron mass anchor allowed",
            ],
            "missing": [
                "native depth ladder or radial readout coupling to W(P)",
                "generation/typing rule",
            ],
            "risk": "may regress into fitting ratios if depth rule is not derived first",
        },
        "hadron_first": {
            "requires": [
                "multi-channel operator taxonomy",
                "interaction channels",
                "kernel/image filtering",
                "possibly product/count readout",
            ],
            "available_now": [
                "A3/S5 active image",
                "two-form interaction channels",
                "three-form support",
                "legacy fingerprints 84/108/180 partly localized",
            ],
            "missing": [
                "product-trace readout for count coefficients",
                "source-overlap/domain partition rule",
                "mass readout",
            ],
            "risk": "more complex; easy to import particle labels too early",
        },
        "taxonomy_first": {
            "requires": [
                "complete native sector ledger",
                "readout mode gates",
                "radial coupling audit",
            ],
            "available_now": [
                "operator taxonomy skeleton",
                "action readout candidate",
                "product-count gate",
            ],
            "missing": [
                "radial/negative-phi coupling to sector weights",
            ],
            "risk": "slower, but minimizes imported mechanisms",
        },
    }

    verdict = {
        "recommended_next": "taxonomy_first -> radial coupling audit -> lepton/hadron branch",
        "reason": "The operator taxonomy is native, but mass readout requires showing how negative-phi radial/depth structure couples to these sector weights.",
        "avoid": "Do not assign A3/S5/T8 to observed particles before the radial coupling/readout rule exists.",
    }

    print(f"paths: {paths}")
    print(f"verdict: {verdict}")


if __name__ == "__main__":
    main()
