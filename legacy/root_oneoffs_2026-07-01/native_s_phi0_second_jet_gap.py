from dataclasses import dataclass


@dataclass(frozen=True)
class Unknown:
    name: str
    why_needed: str
    not_fixed_by: str


UNKNOWNS = [
    Unknown(
        "typed-node Hessian K_ab",
        "determines quadratic weights, coupled spectra, and possible coefficients",
        "q, eta, H1 projection, or lepton ratios",
    ),
    Unknown(
        "cross-coupling blocks",
        "decide whether H1 frame, M1 compact data, M2 compact data, and E1 relative shapes factorize",
        "round-S2 isotropy alone",
    ),
    Unknown(
        "M2 suppression/null direction",
        "decides whether nonprimitive compact triplet is suppressed, diagnostic, or active",
        "dimension-depth rule",
    ),
    Unknown(
        "boundary measure density",
        "turns geometric variables into invariant coefficient weights",
        "bare CP1/S2 or relative-plane volume",
    ),
]


def main() -> None:
    print("S_phi0 second-jet gap")
    print("=" * 24)
    print("The second local variation has the formal role:")
    print("  delta^2 S_phi0 = delta x^a K_ab delta x^b")
    print()
    for unknown in UNKNOWNS:
        print(unknown.name)
        print(f"  why needed:   {unknown.why_needed}")
        print(f"  not fixed by: {unknown.not_fixed_by}")
        print()

    print("Second-jet verdict:")
    print("  The missing coefficient object is the second jet of S_phi0 in typed")
    print("  boundary variables. First-variation data cannot determine it.")


if __name__ == "__main__":
    main()
