def main():
    candidates = {
        "projector_weight_coupling": {
            "form": "radial action/depth depends on W(P)=Tr(P)/12",
            "native_support": [
                "C1 side action",
                "commutator isotropy",
                "projector trace readout",
            ],
            "missing": "operator equation coupling radial negative-phi depth to W(P)",
            "risk": "could become a ratio fit if assigned to particles too early",
        },
        "twoform_channel_coupling": {
            "form": "radial readout depends on two-form channel image/kernel fractions",
            "native_support": [
                "2/7 and 5/7 active filter",
                "channel rules A3-A3, A3-S5, S5-S5",
            ],
            "missing": "physical meaning of kernel/image energy or source overlap",
            "risk": "tempting hadron analogy without source-overlap proof",
        },
        "threeform_support_coupling": {
            "form": "radial readout depends on Tr(A[B,C]) support",
            "native_support": [
                "84 full domain",
                "56 active domain",
                "nonzero A3^3 and A3*S5^2 support",
            ],
            "missing": "why radial depth reads a three-form scalar",
            "risk": "promoting 84 to coefficient without selection",
        },
        "product_count_coupling": {
            "form": "radial readout depends on 36*Tr(P)",
            "native_support": [
                "36 domain",
                "3+5 image split",
            ],
            "missing": "independent product trace over domain cells and image labels",
            "risk": "currently unlicensed; would recreate legacy coefficient jumps",
        },
        "kernel_energy_coupling": {
            "form": "radial readout depends on kernel dimensions or suppressed channels",
            "native_support": [
                "full kernel 28",
                "active kernel 20",
                "trace kernel 8",
                "three-form trace kernel 28",
            ],
            "missing": "native rule assigning energy/action to filtered-out modes",
            "risk": "inventing hidden-energy mechanism",
        },
    }

    verdict = {
        "best_first_test": "projector_weight_coupling",
        "reason": "It is the only candidate with a native scalar action readout already derived.",
        "second_test": "twoform_channel_coupling",
        "reason_second": "It is native but needs source-overlap/kernel interpretation.",
        "defer": ["threeform_support_coupling", "product_count_coupling", "kernel_energy_coupling"],
        "next_proof_target": "derive or reject an equation where radial negative-phi depth/action is multiplied, shifted, or constrained by W(P).",
    }

    print(f"candidates: {candidates}")
    print(f"verdict: {verdict}")


if __name__ == "__main__":
    main()
