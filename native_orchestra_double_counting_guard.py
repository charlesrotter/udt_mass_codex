from dataclasses import dataclass


@dataclass(frozen=True)
class Guard:
    name: str
    risk: str
    guardrail: str


GUARDS = [
    Guard(
        "eta reuse",
        "using q/2, Brown-York stress, curvature jump, and eta as independent weights",
        "treat them as the same edge scalar seen through different metric identities",
    ),
    Guard(
        "interface plus DtN",
        "multiplying interface-local gamma by warped gamma for the same H1 transfer",
        "choose one transfer branch unless variables are proven distinct",
    ),
    Guard(
        "H1 count versus H1 projection",
        "using the 1/3 projection and the 3-state trace as the same operation",
        "projection makes eta; trace counts states after a transfer kernel exists",
    ),
    Guard(
        "CP1/Hopf overcount",
        "counting M1 Hopf orientation as extra nodes in addition to shared H1 frame",
        "Hopf bridge merges orientation into H1 unless residual variables are derived",
    ),
    Guard(
        "M2 omission",
        "removing M2 because E1 is the desired d=3 branch",
        "demote M2 only through primitive-bundle/energy/order rules or explicit coefficient result",
    ),
    Guard(
        "coefficient constants",
        "turning symmetry-allowed alpha, beta, alpha_2 into fitted weights",
        "derive them from S0 or leave Tier D open",
    ),
]


def main() -> None:
    print("orchestra double-counting guard")
    print("=" * 34)
    for guard in GUARDS:
        print(guard.name)
        print(f"  risk:      {guard.risk}")
        print(f"  guardrail: {guard.guardrail}")
        print()

    print("Guard verdict:")
    print("  The orchestra frame is useful only if it prevents overcounting.")
    print("  Multiple metric identities may be the same instrument, not separate")
    print("  additive contributions.")


if __name__ == "__main__":
    main()
