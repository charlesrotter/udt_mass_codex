from dataclasses import dataclass


@dataclass(frozen=True)
class LegacyInput:
    name: str
    old_role: str
    rejection_reason: str
    replacement_requirement: str


LEGACY_INPUTS = [
    LegacyInput(
        "old finite-cell eigenfrequencies",
        "supplied provisional M1/M2/E1 coefficient ratios",
        "computed in the pre-active-lane scaffold with legacy eta/profile choices",
        "recompute from post-P_phi0 variables under one shared boundary convention",
    ),
    LegacyInput(
        "eta=0.03 runs",
        "exploratory mass-sector diagnostics",
        "active lane uses eta=1/18 exactly after banked P_phi0",
        "use eta=1/18 or keep the result outside Tier D",
    ),
    LegacyInput(
        "softened profile parameters",
        "regularized singular endpoint for numerical exploration",
        "profile choices are not a native coefficient functional",
        "derive profile, prove profile-independence, or state profile dependence",
    ),
    LegacyInput(
        "observed lepton residuals",
        "identified possible correction directions",
        "mass data cannot choose coefficients in the active lane",
        "use only after dimensionless coefficients are fixed",
    ),
]


def main() -> None:
    print("Tier D legacy coefficient rejection")
    print("=" * 37)
    for item in LEGACY_INPUTS:
        print(item.name)
        print(f"  old role:                {item.old_role}")
        print(f"  rejection reason:        {item.rejection_reason}")
        print(f"  replacement requirement: {item.replacement_requirement}")
        print()

    print("Rejection verdict:")
    print("  The old M1/M2/E1 coefficient ratios may remain diagnostics.")
    print("  They are not Tier D inputs in the post-Dirac active lane.")


if __name__ == "__main__":
    main()
