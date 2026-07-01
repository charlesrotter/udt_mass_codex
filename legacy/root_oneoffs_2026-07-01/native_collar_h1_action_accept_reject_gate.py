from dataclasses import dataclass


@dataclass(frozen=True)
class Gate:
    name: str
    requirement: str
    rejects: str


GATES = [
    Gate(
        "collar support",
        "the object must live on S2 x I, not only on the phi0 endpoint",
        "pure boundary counterterms and value-only shell actions",
    ),
    Gate(
        "native H1 carrier",
        "the H1 triplet must enter through round-S2 geometry, transported H1 data, or an exact edge mode",
        "a hand-added three-state multiplier",
    ),
    Gate(
        "q source without substitution trick",
        "variation must supply the same effect as dV/df=(q/3)f without replacing q by -r f'/f inside an ordinary potential",
        "the naive q f^2/6 term that collapses to fixed s=1/6",
    ),
    Gate(
        "curvature-share origin",
        "the q dependence should trace to an exact collar identity such as R3/R2=q, m_MS'=q/2, or C1 momentum q/2",
        "an arbitrary coefficient selected only because it gives q=1/3",
    ),
    Gate(
        "no double counting",
        "the collar action must reduce consistently to the interface-local eta carrier or to the warped DtN branch, not both at once",
        "using interface action and bulk propagation as independent factors for the same degree of freedom",
    ),
    Gate(
        "exactness",
        "all identities used in the closure must be exact in f, q, and the angular projector",
        "linearized or small-q arguments promoted to conclusions",
    ),
]


def main() -> None:
    print("collar H1 action accept/reject gate")
    print("=" * 39)
    for gate in GATES:
        print(gate.name)
        print(f"  requirement: {gate.requirement}")
        print(f"  rejects:     {gate.rejects}")
        print()

    print("Gate verdict:")
    print("  A candidate that fails any one of these gates is not a derivation of")
    print("  s(q)=q/3. It may remain a conditional postulate, but not a native")
    print("  metric-uncovered result.")


if __name__ == "__main__":
    main()
