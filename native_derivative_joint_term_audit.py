from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    sees_slope: str
    varies_derivative: str
    can_enforce_delta_h_zero: str
    status: str


CANDIDATES = [
    Candidate(
        name="C1 first-order boundary variation",
        sees_slope="yes, through Pi_f=(1/2)R^2 f'",
        varies_derivative="no, boundary term is Pi_f delta f",
        can_enforce_delta_h_zero="no",
        status="supplies q/2 unit but not p=q",
    ),
    Candidate(
        name="boundary functional B(f)",
        sees_slope="only if slope is inserted as a parameter",
        varies_derivative="no",
        can_enforce_delta_h_zero="no",
        status="can cancel momentum but cannot stationarize h'(R)",
    ),
    Candidate(
        name="standard EH+GHY Dirichlet completion",
        sees_slope="raw EH sees f', GHY cancels f' in the action value",
        varies_derivative="no under Dirichlet metric data",
        can_enforce_delta_h_zero="no",
        status="rejected as eta/q selector",
    ),
    Candidate(
        name="Brown-York angular stress",
        sees_slope="yes, angular stress unit is q/2 at f=1",
        varies_derivative="not by itself; it is a response tensor",
        can_enforce_delta_h_zero="no",
        status="good atlas diagnostic, not a UDT stationarity equation",
    ),
    Candidate(
        name="Israel shell jump",
        sees_slope="yes, trace-reversed angular jump has q/2",
        varies_derivative="bookkeeping, not an action by itself",
        can_enforce_delta_h_zero="no",
        status="exact interface accounting, not selection",
    ),
    Candidate(
        name="native derivative/joint functional B(f,q,H1)",
        sees_slope="yes by construction",
        varies_derivative="yes, if q or extrinsic curvature is boundary data",
        can_enforce_delta_h_zero="yes, if stationarity gives q=p",
        status="needed object; not yet derived",
    ),
]


def main() -> None:
    print("derivative-sensitive joint-term audit")
    print("=" * 39)
    for candidate in CANDIDATES:
        print(candidate.name)
        print(f"  sees slope:                {candidate.sees_slope}")
        print(f"  varies derivative data:    {candidate.varies_derivative}")
        print(f"  can enforce delta_h=0:     {candidate.can_enforce_delta_h_zero}")
        print(f"  status:                    {candidate.status}")
        print()

    print("Necessary form of a closing joint term:")
    print("  B_joint must depend on Cauchy data, not only value data:")
    print("    B_joint = B(F, Q, angular data)")
    print("  where:")
    print("    F = f(R)")
    print("    Q = -R f'(R)/f(R)")
    print()
    print("Required stationarity conditions:")
    print("  value/momentum closure:")
    print("    partial B / partial F |F=1 = Q/2")
    print("  graph uniqueness:")
    print("    partial B / partial Q enforces Q=p")
    print()
    print("Audit verdict:")
    print("  The GR corpus points at the correct derivative-sensitive kind")
    print("  of object, but the currently known GR candidates do not close")
    print("  p=q after positional-dilation refactor. A UDT-native B(F,Q,H1)")
    print("  or an exact one-graph Calderon projector is still required.")


if __name__ == "__main__":
    main()
