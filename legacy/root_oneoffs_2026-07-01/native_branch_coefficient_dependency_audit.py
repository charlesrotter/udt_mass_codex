from dataclasses import dataclass


@dataclass(frozen=True)
class CoefficientSource:
    name: str
    m1_role: str
    e1_role: str
    native_status: str
    risk: str
    required_derivation: str


SOURCES = [
    CoefficientSource(
        name="cell normalization",
        m1_role="sets anchored compact branch amplitude",
        e1_role="sets E1/M1 coefficient ratio",
        native_status="open in typed graph",
        risk="old coefficient ratio may carry legacy approximation choices",
        required_derivation="normalize finite-cell action in the same n_a/projective variables",
    ),
    CoefficientSource(
        name="shape-mode volume",
        m1_role="one compact/radial shape scalar per boundary",
        e1_role="two ordinary relative-shape scalars per boundary",
        native_status="node counts clarified; weight normalization open",
        risk="different shape volumes can move M1 and E1 in opposite directions",
        required_derivation="derive boundary measure per shape node after node-merge rules",
    ),
    CoefficientSource(
        name="compact occupation weight",
        m1_role="direct M1 selector/weight",
        e1_role="none",
        native_status="Pbundle0 still open",
        risk="can look like an M1 residual correction if fitted",
        required_derivation="find metric/interface reason for nontrivial primitive compact occupation",
    ),
    CoefficientSource(
        name="ordinary endpoint resonance normalization",
        m1_role="indirect shared frame only",
        e1_role="direct E1 selector/weight",
        native_status="p=1/3 resonance strong; normalization open",
        risk="can look like E1 boost if fitted",
        required_derivation="derive E1 finite-cell normalization from endpoint resonance and H1 shape action",
    ),
]


def main() -> None:
    print("Branch coefficient dependency audit")
    print("=" * 37)
    print("The current few-percent residuals may live in coefficient normalization,")
    print("not in eta/gamma or a new mechanism.")
    print()
    for source in SOURCES:
        print(source.name)
        print(f"  M1 role:             {source.m1_role}")
        print(f"  E1 role:             {source.e1_role}")
        print(f"  native status:       {source.native_status}")
        print(f"  risk:                {source.risk}")
        print(f"  required derivation: {source.required_derivation}")
        print()

    print("Coefficient verdict:")
    print("  - The old M1/E1 coefficient ratio should be treated as provisional.")
    print("  - Coefficients must be recomputed after the typed graph, Hopf merge,")
    print("    q-flow, and transfer normalization are fixed.")
    print("  - This is the most plausible place for opposite-sign branch movement")
    print("    without inventing a new mechanism.")


if __name__ == "__main__":
    main()
