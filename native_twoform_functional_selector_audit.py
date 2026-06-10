def main():
    routes = [
        {
            "route": "dimension ladder",
            "native_inputs": [
                "H1 dimension 3",
                "End(H1) dimension 9",
                "projected C1 side action eta/2=1/36",
            ],
            "reaches_twoform": True,
            "reaches_Lambda2_EndH1_functionally": False,
            "status": "strong dimensional selector candidate",
            "gap": "shows eta/2 equals 1/dim Lambda^2 End(H1), but not that the C1 functional acts on Lambda^2 End(H1)",
        },
        {
            "route": "C1 boundary symplectic form",
            "native_inputs": [
                "C1 boundary variation delta S = Pi delta f",
                "canonical boundary two-form delta Pi wedge delta f",
            ],
            "reaches_twoform": True,
            "reaches_Lambda2_EndH1_functionally": False,
            "status": "native two-form, wrong arena so far",
            "gap": "acts on boundary phase-space pairs, not yet on unordered pairs of End(H1) operator directions",
        },
        {
            "route": "H1 harmonic area carrier",
            "native_inputs": [
                "Lambda^3 H1 -> dOmega_S2",
                "orientation/top-form structure on the rank-3 carrier",
            ],
            "reaches_twoform": False,
            "reaches_Lambda2_EndH1_functionally": False,
            "status": "licenses exterior algebra on H1, not the End(H1) two-form sector",
            "gap": "does not select Lambda^2 End(H1) or Lambda^3 End(H1)",
        },
        {
            "route": "angular connection/curvature",
            "native_inputs": [
                "round S2 angular geometry",
                "H1 vector carrier",
                "curvature is naturally a two-form",
            ],
            "reaches_twoform": True,
            "reaches_Lambda2_EndH1_functionally": False,
            "status": "promising route, not computed here",
            "gap": "native S2 connection acts first on antisymmetric H1 rotations; must show whether full End(H1) pair space is involved",
        },
        {
            "route": "metric perturbation scalar/vector/tensor split",
            "native_inputs": [
                "End(H1)=1+8",
                "8=3+5",
                "legacy scalar/vector/tensor sectors as candidate survivors",
            ],
            "reaches_twoform": False,
            "reaches_Lambda2_EndH1_functionally": False,
            "status": "orchestra component candidate",
            "gap": "gives operator-sector ingredients, not an exterior-sector selector by itself",
        },
    ]

    closed = [
        route for route in routes if route["reaches_Lambda2_EndH1_functionally"]
    ]
    partial = [route for route in routes if route["reaches_twoform"]]

    print(f"routes: {routes}")
    print(f"partial_twoform_routes: {[route['route'] for route in partial]}")
    print(f"closed_functional_routes: {[route['route'] for route in closed]}")
    print("verdict: no route currently proves a functional Lambda^2 End(H1) particle-sector selector")
    print(
        "next_target: derive an End(H1)-valued boundary field or curvature/source-overlap "
        "operator whose natural action is an alternating two-form over the operator alphabet"
    )


if __name__ == "__main__":
    main()
