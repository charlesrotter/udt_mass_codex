from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    name: str
    support: str
    limit: str
    status: str


CLAIMS = [
    Claim(
        name="two-sided phi bridge",
        support="phi -> -phi mirror plus phi-blind angular operator",
        limit="does not by itself define an action split",
        status="native geometric bridge",
    ),
    Claim(
        name="shared ell=1 kernel",
        support="L1=I3 on both sides of phi0",
        limit="does not decide transfer direction or trace operation",
        status="derived metric fact",
    ),
    Claim(
        name="eta/2 per side",
        support="natural if the full edge action eta is shared by two bridge sides",
        limit="requires a boundary action or amplitude structure",
        status="plausible coupling rule, not derived",
    ),
    Claim(
        name="gamma trace",
        support="exact if A_side=(eta/2)L1 and physical operation is channel trace",
        limit="trace/composition interpretation remains open",
        status="conditional identity",
    ),
]


def main() -> None:
    print("two-sided half-action status")
    print("=" * 31)
    for claim in CLAIMS:
        print(claim.name)
        print(f"  support: {claim.support}")
        print(f"  limit:   {claim.limit}")
        print(f"  status:  {claim.status}")
        print()

    print("Half-action verdict:")
    print("  The two-sided phi bridge makes eta/2 plausible and native-looking,")
    print("  but does not prove it. The exact upgrade still requires a boundary")
    print("  action or amplitude whose two sides compose to eta.")


if __name__ == "__main__":
    main()
