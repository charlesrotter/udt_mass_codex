from dataclasses import dataclass
from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class SourceClass:
    name: str
    source_content: str
    q_behavior: str
    verdict: str


SOURCE_CLASSES = [
    SourceClass(
        name="no angular source",
        source_content="s(t)=0",
        q_behavior="q=0 is the regular/nontrivial-free branch",
        verdict="scalar background, not mass-cell endpoint",
    ),
    SourceClass(
        name="constant H1 collar source",
        source_content="s(t)=1/9",
        q_behavior="q=1/3 fixed branch; q=2/3 companion rejected by finite C1 action",
        verdict="single graph, delta_h=0",
    ),
    SourceClass(
        name="self-coupled H1 source",
        source_content="s(q)=q/3",
        q_behavior="fixed branches q=0 and q=1/3; on nontrivial branch s=1/9",
        verdict="single graph if the product rule is native",
    ),
    SourceClass(
        name="running collar source",
        source_content="s(t) arbitrary or branch-dependent",
        q_behavior="q runs; endpoint exponent p and phi0 slope q can split",
        verdict="split graph / independent h direction",
    ),
]


def main() -> None:
    print("first-jet source inventory")
    print("=" * 27)
    print("Exact q-flow for the collar:")
    print("  dq/dt = q^2 - q + 2s(t)")
    print()
    print("Collar factorization:")
    print("  f(r) = (R/r)^p h(r)")
    print("  q_phi0 = p + delta_h")
    print()
    print("Thus an independent h direction is not free.")
    print("It is equivalent to nonzero integrated q-flow:")
    print("  delta_h = integral [q^2 - q + 2s(t)] dt")
    print()
    for source_class in SOURCE_CLASSES:
        print(source_class.name)
        print(f"  source content: {source_class.source_content}")
        print(f"  q behavior:     {source_class.q_behavior}")
        print(f"  verdict:        {source_class.verdict}")
        print()

    q = Fraction(1, 3)
    print("Nontrivial fixed branch:")
    print(f"  q = {fmt(q)}")
    print(f"  s = q(1-q)/2 = {fmt(q * (1 - q) / 2)}")
    print(f"  eta = q/6 = {fmt(q / 6)}")
    print()
    print("Ponder verdict:")
    print("  The neutral bridge does not need a rule forbidding arbitrary h.")
    print("  It needs a metric source inventory. If the elementary bridge contains")
    print("  only the invariant H1 source and no running collar source, the first")
    print("  jet collapses to the q=1/3 graph. If the metric supplies running")
    print("  source content, p and q may split.")


if __name__ == "__main__":
    main()
