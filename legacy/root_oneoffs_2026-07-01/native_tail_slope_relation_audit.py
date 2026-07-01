from dataclasses import dataclass


@dataclass(frozen=True)
class ExteriorState:
    label: str
    a_tail: float
    radius: float = 1.0

    @property
    def f(self) -> float:
        return 1.0 + self.a_tail / self.radius

    @property
    def fprime(self) -> float:
        return -self.a_tail / (self.radius * self.radius)

    @property
    def q(self) -> float:
        return -self.radius * self.fprime / self.f


def main() -> None:
    states = [
        ExteriorState("flat exterior", 0.0),
        ExteriorState("small negative-mass tail", 0.02),
        ExteriorState("moderate negative-mass tail", 0.10),
        ExteriorState("large negative-mass tail", 1.0),
    ]

    print("Tail/slope relation audit")
    print("=" * 26)
    print("Exterior vacuum branch near R=1:")
    print("  f_out = 1 + a/r")
    print("  q_out = -R f'_out/f_out = a/(R+a)")
    print()
    for state in states:
        print(state.label)
        print(f"  a_tail={state.a_tail:.12g}")
        print(f"  f(R)={state.f:.12g}")
        print(f"  f'(R)={state.fprime:.12g}")
        print(f"  q_out={state.q:.12g}")
        print()

    print("If the boundary is normalized to f(R)=1 and exterior flat:")
    print("  a_tail=0")
    print("  q_out=0")
    print()
    print("Audit verdict:")
    print("  - In a vacuum exterior, tail amplitude and exterior slope are linked.")
    print("  - But a finite matter cell wants f(R)=1, a_tail=0 outside, and nonzero")
    print("    interior q to retain eta.")
    print("  - Therefore nonzero eta requires a genuine shell/boundary-layer slope jump.")
    print("  - The boundary layer cannot be replaced by smooth matching to flat exterior.")


if __name__ == "__main__":
    main()
