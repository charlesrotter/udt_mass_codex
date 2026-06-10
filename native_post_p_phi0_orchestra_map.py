from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    name: str
    role: str
    current_status: str
    next_test: str


INSTRUMENTS = [
    Instrument(
        name="P_phi0 edge closure",
        role="fixes -Pi_f/R=1/6, hence q=1/3 and eta=1/18",
        current_status="banked minimal postulate",
        next_test="optional search for exact H1/S2 edge kernel",
    ),
    Instrument(
        name="H1/S2 projection",
        role="projects q/2 to eta=q/6 via <n_a n_b>=delta_ab/3",
        current_status="derived geometry",
        next_test="none for eta; only check independence in transfer graph",
    ),
    Instrument(
        name="finite C1 action filter",
        role="rejects q=2/3 branch once s=1/9 is present",
        current_status="derived filter",
        next_test="ensure no branch-specific source running reintroduces delta_h",
    ),
    Instrument(
        name="transfer multiplier gamma",
        role="converts eta into per-node multiplicative ladder gamma=3 exp(-eta/2)",
        current_status="candidate transfer rule",
        next_test="derive channel multiplicity and one-sided exponential from boundary action",
    ),
    Instrument(
        name="typed node depth",
        role="assigns M1 depth 5 and E1 depth 7 in current diagnostic",
        current_status="candidate graph rule",
        next_test="derive node independence and prevent double counting shared H1 frame nodes",
    ),
    Instrument(
        name="branch coefficients",
        role="supply M1/E1 finite-cell coefficient ratio",
        current_status="diagnostic coefficient data",
        next_test="derive from native edge spectrum or remove from predictive chain",
    ),
    Instrument(
        name="electron anchor",
        role="sets absolute mass scale",
        current_status="allowed single dimensionful anchor",
        next_test="none; keep it as scale only",
    ),
]


def main() -> None:
    print("post-P_phi0 orchestra map")
    print("=" * 27)
    for instrument in INSTRUMENTS:
        print(instrument.name)
        print(f"  role:          {instrument.role}")
        print(f"  status:        {instrument.current_status}")
        print(f"  next test:     {instrument.next_test}")
        print()

    print("Work verdict:")
    print("  Do not spend the next pass re-deriving eta.")
    print("  With P_phi0 banked, the next load-bearing work is transfer gamma,")
    print("  typed node depth, and branch coefficients.")


if __name__ == "__main__":
    main()
