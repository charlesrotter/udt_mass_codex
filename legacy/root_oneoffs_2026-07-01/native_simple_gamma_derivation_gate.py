from dataclasses import dataclass


@dataclass(frozen=True)
class Gate:
    name: str
    status: str
    consequence: str


GATES = [
    Gate(
        "phi0 scalar edge unit",
        "banked as P_phi0; exact consequences follow",
        "q=1/3, q/2=1/6, eta=q/6=1/18",
    ),
    Gate(
        "H1/S2 isotropic projection",
        "derived from round S2 second moment",
        "<n_a n_b>=delta_ab/3",
    ),
    Gate(
        "ell=1 angular identity",
        "derived from intrinsic S2 Laplacian",
        "L1=(-R^2 Delta_S2)/2=I_3 on ell=1",
    ),
    Gate(
        "constant-mode blindness",
        "physically motivated selector; not yet forced",
        "removes alpha<a,a> and leaves Laplacian branch",
    ),
    Gate(
        "scalar-to-angular S0 coupling",
        "open",
        "needed to form A_full=eta L1 or A_side=(eta/2)L1",
    ),
    Gate(
        "one-sided composable split",
        "conditional gluing identity",
        "side kernel carries half of full shared boundary action",
    ),
    Gate(
        "trace over ell=1 triplet",
        "conditional transfer interpretation",
        "Tr exp[-(eta/2)I_3]=3 exp(-eta/2)",
    ),
]


def main() -> None:
    print("simple gamma derivation gate")
    print("=" * 30)
    for gate in GATES:
        print(gate.name)
        print(f"  status:      {gate.status}")
        print(f"  consequence: {gate.consequence}")
        print()

    print("No-approximation verdict:")
    print("  The simple gamma path is now a gated derivation, not a free fit.")
    print("  The central missing gate is scalar-to-angular S0 coupling at phi0.")


if __name__ == "__main__":
    main()
