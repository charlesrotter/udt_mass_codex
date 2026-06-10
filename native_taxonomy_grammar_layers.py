def main():
    layers = {
        "layer_0_container": {
            "object": "negative-phi mass-emergence container",
            "role": "common radial branch q=1/3 and C1 action unit 1/12",
        },
        "layer_1_alphabet": {
            "object": "End(H1)=trace+A3+S5",
            "role": "available sector letters before interactions",
        },
        "layer_2_local_channels": {
            "object": "Lambda^2 End(H1) channel blocks",
            "role": "diagnose interaction routes and local residuals",
            "use_for": "interaction taxonomy",
            "do_not_use_for": "global spectrum count without quotienting",
        },
        "layer_3_global_quotient": {
            "object": "commutator image T8",
            "role": "identify overlapping local images, especially repeated A3",
            "use_for": "active spectrum alphabet",
        },
        "layer_4_readout": {
            "object": "projector trace W(P)=Tr(P)/12",
            "role": "current scalar action readout on global image sectors",
        },
        "layer_5_excitation_candidates": {
            "object": "sector-dependent q(P), product counts, kernel energies",
            "role": "parked candidates requiring extra boundary/source rules",
        },
    }

    allowed_transitions = [
        "container -> alphabet",
        "alphabet -> local channels",
        "local channels -> global quotient",
        "global quotient -> projector readout",
    ]

    blocked_shortcuts = [
        "local channel counts -> masses",
        "domain*image product counts -> observables",
        "sector-dependent q(P) -> ground spectrum",
        "kernel dimensions -> hidden energy",
    ]

    verdict = {
        "grammar": "The metric taxonomy has layered grammar; readout must pass through global quotient before scalar weights.",
        "importance": "This prevents local interaction structure from being mistaken for global spectrum multiplicity.",
    }

    print(f"layers: {layers}")
    print(f"allowed_transitions: {allowed_transitions}")
    print(f"blocked_shortcuts: {blocked_shortcuts}")
    print(f"verdict: {verdict}")


if __name__ == "__main__":
    main()
