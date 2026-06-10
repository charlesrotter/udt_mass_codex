from dataclasses import dataclass


@dataclass(frozen=True)
class CoefficientGate:
    name: str
    exact_status: str
    cannot_do: str
    required_next: str


GATES = [
    CoefficientGate(
        "finite-cell normalization",
        "open after Dirac/Form-T removal",
        "reuse legacy M1/E1 coefficient ratios as derived",
        "renormalize cells in the post-P_phi0 variables",
    ),
    CoefficientGate(
        "M1 compact occupation",
        "primitive compact bundle remains conditional",
        "tune M1 by an occupation weight fitted to masses",
        "derive or explicitly bank compact primitive occupation",
    ),
    CoefficientGate(
        "E1 relative-shape measure",
        "bare relative plane is exactly isotropic",
        "extract an E1 boost from measure anisotropy",
        "derive boundary-action weighting if E1 gets a coefficient shift",
    ),
    CoefficientGate(
        "CP1/Hopf M1 measure",
        "Fubini-Study measure pushes to round S2 second moment",
        "extract an M1 correction from bare CP1 anisotropy",
        "derive compact-bundle or boundary-action weighting if M1 shifts",
    ),
    CoefficientGate(
        "electron anchor",
        "allowed only after dimensionless coefficients are fixed",
        "choose gates by matching electron/muon/tau values",
        "use masses as downstream checks",
    ),
]


def main() -> None:
    print("branch-coefficient active-lane gate")
    print("=" * 36)
    for gate in GATES:
        print(gate.name)
        print(f"  exact status:  {gate.exact_status}")
        print(f"  cannot do:     {gate.cannot_do}")
        print(f"  required next: {gate.required_next}")
        print()

    print("Coefficient verdict:")
    print("  Branch coefficients are not available yet in the active lane.")
    print("  They are the next real calculation after transfer branch and typed")
    print("  graph status are fixed. Until then, mass comparisons remain diagnostic.")


if __name__ == "__main__":
    main()
