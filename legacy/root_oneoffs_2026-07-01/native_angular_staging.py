"""Angular-sector staging register for the negative-phi rebuild.

This is not a physics solver. It is a small audit artifact that keeps the
angular-sector import order explicit, so the rebuild does not accidentally pull
in Form-T-era assumptions while trying to assemble the "band".
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AngularComponent:
    name: str
    status: str
    include_now: bool
    reason: str


COMPONENTS = [
    AngularComponent(
        "round S2 eigenvalues ell(ell+1)",
        "native metric kinematics",
        True,
        "already used by scalar/angular cell operator",
    ),
    AngularComponent(
        "multiplicity 2ell+1",
        "native metric kinematics",
        True,
        "already used as degeneracy/sector label",
    ),
    AngularComponent(
        "monopole harmonics",
        "candidate compact flux sector",
        True,
        "allowed only under explicit compact-flux postulate P2",
    ),
    AngularComponent(
        "ell=1 operator algebra su(3), 8=3+5",
        "derived angular kinematics",
        True,
        "safe as representation bookkeeping; not a color force",
    ),
    AngularComponent(
        "epsilon_abc singlet",
        "derived angular kinematics",
        True,
        "safe as selection/observability rule for three ell=1 sectors",
    ),
    AngularComponent(
        "rank-2 Y2 coupling matrix",
        "solid matrix structure, origin/magnitude open",
        False,
        "premature until boundary layer and source coupling are pinned",
    ),
    AngularComponent(
        "parity blocks from full spinor angular structure",
        "spinor-dependent",
        False,
        "depends on Form-T/full-spinor structure; keep out for now",
    ),
    AngularComponent(
        "kappa channel ladder",
        "spinor/Dirac-dependent",
        False,
        "not native to scalar matter-cell scaffold",
    ),
    AngularComponent(
        "color force / confinement dynamics",
        "not metric-given",
        False,
        "explicitly not derived in rebuild",
    ),
    AngularComponent(
        "SM charge/flavor/mass labels",
        "labels/fits",
        False,
        "not part of native geometry assembly",
    ),
]


def singlet_count_for_antisymmetric_triple(dimension: int) -> int:
    """dim Lambda^3 V, with unique singlet-like epsilon only at dimension 3."""

    if dimension < 3:
        return 0
    return dimension * (dimension - 1) * (dimension - 2) // 6


def main() -> None:
    print("Angular-sector staging register")
    print()
    for component in COMPONENTS:
        flag = "INCLUDE" if component.include_now else "DEFER"
        print(f"{flag:7s} | {component.name}")
        print(f"        status: {component.status}")
        print(f"        reason: {component.reason}")
    print()
    print("antisymmetric triple count dim Lambda^3 V:")
    for dimension in range(1, 8):
        count = singlet_count_for_antisymmetric_triple(dimension)
        marker = " <-- unique epsilon case" if dimension == 3 and count == 1 else ""
        print(f"  dim={dimension}: count={count}{marker}")


if __name__ == "__main__":
    main()

