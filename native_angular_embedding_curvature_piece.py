from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("Angular embedding-curvature piece")
    print("=" * 36)
    print("Spatial metric:")
    print("  dl^2 = f^{-1} dr^2 + r^2 dOmega^2")
    print()
    print("For the S2 collar embedded in the spatial slice:")
    print("  shape operator s^A_B = sqrt(f)/R delta^A_B")
    print("  mean curvature k = 2 sqrt(f)/R")
    print("  det(shape) = f/R^2")
    print()
    print("Ambient tangential sectional curvature:")
    print("  K_tangent = (1-f)/R^2")
    print()
    print("Gauss equation:")
    print("  K_intrinsic(S2) = K_tangent + det(shape)")
    print("                  = (1-f)/R^2 + f/R^2")
    print("                  = 1/R^2")
    print()
    print("So the intrinsic round-S2 algebra is phi-blind exactly.")
    print()
    print("But the radial evolution of the shape operator is not phi-blind:")
    print("  n(s) = sqrt(f) d/dR [sqrt(f)/R]")
    print("       = f'/(2R) - f/R^2")
    print()
    print("Riccati relation:")
    print("  K_radial-angular = -n(s) - s^2")
    print("                   = -f'/(2R)")
    print()
    print("At phi0:")
    print("  f=1")
    print("  f'=-q/R")
    print("  s=1/R, same as flat")
    print("  n(s)=-(1 + q/2)/R^2")
    print("  K_radial-angular=q/(2R^2)")
    print()
    q = Fraction(1, 3)
    print("For q=1/3:")
    print(f"  K_radial-angular/K_S2 = {fmt(q / 2)}")
    print()
    print("No-invention verdict:")
    print("  The intrinsic angular sector is preserved and phi-blind.")
    print("  The missing angular-adjacent piece is the embedding/radial-evolution")
    print("  of the S2 collar. That is where the linear q/2 unit lives.")


if __name__ == "__main__":
    main()
