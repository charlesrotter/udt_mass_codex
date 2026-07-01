from dataclasses import dataclass


@dataclass(frozen=True)
class InteriorCell:
    label: str
    tail_a: float
    q_inside: float
    radius: float = 1.0

    @property
    def f_inside(self) -> float:
        return 1.0

    @property
    def fprime_inside(self) -> float:
        return -self.q_inside / self.radius

    @property
    def exterior_tail_to_cancel(self) -> float:
        return self.tail_a

    @property
    def slope_jump_to_flat(self) -> float:
        # exterior flat f'=0
        return 0.0 - self.fprime_inside

    @property
    def delta_k_r(self) -> float:
        # Delta K R = -f'_inner R / 2 when exterior is flat.
        return self.q_inside / 2.0


def main() -> None:
    cells = [
        InteriorCell("self-similar collar", tail_a=0.10, q_inside=1.0 / 3.0),
        InteriorCell("M1-positive q diagnostic", tail_a=0.10, q_inside=0.387510439043),
        InteriorCell("E1-negative q diagnostic", tail_a=0.10, q_inside=0.264116906769),
        InteriorCell("small tail self-similar", tail_a=0.02, q_inside=1.0 / 3.0),
    ]

    print("phi0 boundary-layer requirements")
    print("=" * 34)
    print("A finite cell needs two distinct boundary jobs:")
    print("  1. cancel exterior negative-mass tail a_tail -> 0")
    print("  2. set or preserve collar slope q_phi0")
    print()
    print("At R=1 and f(R)=1:")
    print("  f'_inside=-q")
    print("  flat exterior has f'_outside=0")
    print("  slope jump to flat = q")
    print("  extrinsic scalar Delta K R = q/2")
    print()

    for cell in cells:
        print(cell.label)
        print(f"  interior tail a={cell.tail_a:.12g}")
        print(f"  q_inside={cell.q_inside:.12g}")
        print(f"  tail cancellation required={cell.exterior_tail_to_cancel:.12g}")
        print(f"  slope jump to flat={cell.slope_jump_to_flat:.12g}")
        print(f"  Delta K R={cell.delta_k_r:.12g}")
        print(f"  eta candidate=q/6={cell.q_inside / 6.0:.12g}")
        print()

    print("Boundary-layer verdict:")
    print("  - Tail cancellation and collar-slope setting are separate jobs.")
    print("  - A boundary layer that only cancels a_tail need not preserve q=1/3.")
    print("  - A boundary layer that preserves q=1/3 need not cancel a_tail unless")
    print("    its integrated source also removes the exterior monopole.")
    print("  - The hidden mechanism, if present, must couple both conditions:")
    print("      a_tail=0 and q_phi0 controlled by H1/interface data.")


if __name__ == "__main__":
    main()
