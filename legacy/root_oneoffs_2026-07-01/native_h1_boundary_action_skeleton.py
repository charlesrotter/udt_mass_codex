from dataclasses import dataclass


@dataclass(frozen=True)
class Term:
    name: str
    form: str
    status: str
    role: str
    forbidden_upgrade: str


TERMS = [
    Term(
        name="unit-vector constraint",
        form="n_a n_a = 1",
        status="metric/projective native",
        role="defines the H1/projective boundary observable on S2 or CP1",
        forbidden_upgrade="do not add extra internal components beyond H1 without metric source",
    ),
    Term(
        name="isotropic second moment",
        form="<n_a n_b> = delta_ab / 3",
        status="round-S2 metric native",
        role="projects scalar boundary budget into eta delta_ab",
        forbidden_upgrade="do not choose an anisotropic direction to tune branch corrections",
    ),
    Term(
        name="interface scalar coupling",
        form="B <n_a n_b>, B=p/2",
        status="native if closure observable is n_a",
        role="gives eta=1/18 at p=1/3",
        forbidden_upgrade="do not apply B separately per component unless boundary measure says so",
    ),
    Term(
        name="one-sided transfer split",
        form="S_side = eta / 2",
        status="composition native for symmetric transfer kernels",
        role="prevents double-counting under gluing",
        forbidden_upgrade="do not use half-weight if the object is not a composable boundary side",
    ),
    Term(
        name="shape closure projectors",
        form="P_i = |i><i| on H1 labels",
        status="conditional",
        role="turns scalar closure equations into independent gamma traces",
        forbidden_upgrade="do not count multiple projectors without distinct boundary equations",
    ),
    Term(
        name="anisotropic branch potential",
        form="V_ab n_a n_b with V not proportional to delta_ab",
        status="not metric-derived yet",
        role="could create branch corrections only if derived",
        forbidden_upgrade="do not introduce to fit mu/tau residuals",
    ),
]


def main() -> None:
    print("H1/projective boundary-action skeleton")
    print("=" * 40)
    print("Goal: write only the boundary terms currently supported by the metric")
    print("and identify which terms would be imports.")
    print()
    for term in TERMS:
        print(term.name)
        print(f"  form:   {term.form}")
        print(f"  status: {term.status}")
        print(f"  role:   {term.role}")
        print(f"  guard:  {term.forbidden_upgrade}")
    print()
    print("Skeleton verdict:")
    print("  The native minimal boundary action in n_a is isotropic.")
    print("  It can supply eta and gamma-side weights.")
    print("  It does not by itself supply branch-specific residual corrections.")
    print("  The remaining hierarchy question is how many distinct shape/projector")
    print("  closure equations the metric boundary variation actually creates.")


if __name__ == "__main__":
    main()
