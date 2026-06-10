from dataclasses import dataclass


@dataclass(frozen=True)
class EdgeObject:
    name: str
    phi0_form: str
    independent_shape: str
    consequence: str


OBJECTS = [
    EdgeObject(
        name="intrinsic S2 metric",
        phi0_form="gamma_AB = R^2 omega_AB",
        independent_shape="isotropic; no traceless angular part",
        consequence="preserves phi-blind round-S2 representation arena",
    ),
    EdgeObject(
        name="S2 shape operator",
        phi0_form="s^A_B = (1/R) delta^A_B",
        independent_shape="isotropic; same value as flat at f=1",
        consequence="does not create branch depth by itself",
    ),
    EdgeObject(
        name="normal derivative of shape",
        phi0_form="n(s)^A_B = -(1+q/2) delta^A_B / R^2",
        independent_shape="isotropic scalar q correction",
        consequence="carries edge momentum but no traceless angular split",
    ),
    EdgeObject(
        name="radial-angular sectional curvature",
        phi0_form="K_rad = q/(2R^2)",
        independent_shape="single scalar shared by both radial-angular planes",
        consequence="supplies eta source unit q/2 before projection",
    ),
    EdgeObject(
        name="C1 boundary momentum",
        phi0_form="Pi_f = -qR/2",
        independent_shape="single scalar conjugate momentum",
        consequence="native Neumann edge datum",
    ),
]


def main() -> None:
    print("phi0 edge invariant rank audit")
    print("=" * 35)
    for obj in OBJECTS:
        print(obj.name)
        print(f"  phi0 form:          {obj.phi0_form}")
        print(f"  independent shape:  {obj.independent_shape}")
        print(f"  consequence:        {obj.consequence}")
        print()

    print("Rank verdict:")
    print("  The spherical phi0 edge supplies scalar/isotropic invariants plus the")
    print("  H1/S2 orientation arena. It does not by itself contain native 5- or")
    print("  7-node typed depth. Those counts require an additional edge graph or")
    print("  bundle structure beyond the scalar spherical metric edge.")


if __name__ == "__main__":
    main()
