def main():
    gates = {
        "single_internal_trace": {
            "status": "supported",
            "metric_source": "phi0 internal gluing plus induced S2 measure",
            "operation": "Tr over internal H1 or image label",
        },
        "product_trace": {
            "status": "conditional",
            "metric_source": "tensor-product trace over independent local transfer slots",
            "operation": "Tr(K1 tensor K2)=Tr(K1)Tr(K2)",
            "gate": "derive independent slots",
        },
        "commutator_selector": {
            "status": "derived as operator map",
            "metric_source": "native End(H1) composition and C1 weighting",
            "operation": "Lambda^2 End(H1)->T8",
            "effect": "couples and quotients the domain into an image/kernel split",
        },
        "domain_times_image_count": {
            "status": "not licensed",
            "operation": "dim Lambda^2 End(H1) * Tr(P)",
            "problem": "would require the two-form domain and image label to be independent trace slots",
        },
    }

    consequences = {
        "allowed_now": [
            "commutator action readout W(P)=Tr(P)/12",
            "single internal trace over canonical image projector",
        ],
        "not_allowed_yet": [
            "108=36*3 as an observable coefficient",
            "180=36*5 as an observable coefficient",
            "any mass formula using domain*image count",
        ],
        "proof_to_upgrade": "construct a boundary/source-overlap model where Lambda^2 End(H1) cells and image-sector labels are independent internal transfer slots rather than commutator-coupled variables",
    }

    print(f"gates: {gates}")
    print(f"consequences: {consequences}")


if __name__ == "__main__":
    main()
