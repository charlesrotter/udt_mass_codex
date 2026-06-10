from dataclasses import dataclass


@dataclass(frozen=True)
class LiftRule:
    name: str
    matrix_entry: float
    total_trace: float
    interpretation: str


def main() -> None:
    p = 1.0 / 3.0
    n = 3
    b = p / 2.0

    rules = [
        LiftRule(
            name="per-channel scalar lift",
            matrix_entry=b,
            total_trace=n * b,
            interpretation=(
                "The scalar boundary cost is charged independently to every label. "
                "This gives eta=B, not B/N."
            ),
        ),
        LiftRule(
            name="trace-preserving total-action lift",
            matrix_entry=b / n,
            total_trace=b,
            interpretation=(
                "The scalar boundary cost is one total boundary budget distributed "
                "over N symmetric labels. This gives eta=B/N."
            ),
        ),
    ]

    print("Projection normalization audit")
    print("=" * 31)
    print(f"self-similar endpoint p={p:.12g}")
    print(f"interface scalar B=p/2={b:.12g}")
    print(f"transported label count N={n}")
    print()
    print("Label symmetry only says the lifted operator is proportional to I_N.")
    print("It does not by itself fix the proportionality constant.")
    print()

    for rule in rules:
        print(rule.name)
        print(f"  action matrix entry = {rule.matrix_entry:.12g}")
        print(f"  trace action = {rule.total_trace:.12g}")
        print(f"  eta candidate = {rule.matrix_entry:.12g}")
        print(f"  interpretation: {rule.interpretation}")

    print("\nAudit verdict:")
    print("  - Identity form follows from label-blind scalar coupling.")
    print("  - eta=B/N follows only if the lift preserves the single scalar")
    print("    boundary action as a total trace, Tr S = B.")
    print("  - This is a plausible metric rule because the interface scalar is")
    print("    integrated once over the boundary, not once per label.")
    print("  - But the rule should be named Ptrace until derived from the")
    print("    boundary measure/transfer construction.")


if __name__ == "__main__":
    main()
