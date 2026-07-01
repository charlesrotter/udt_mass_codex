import math


def main() -> None:
    n = 3
    p = 1.0 / 3.0
    boundary_scalar = p / 2.0
    s2_projection = 1.0 / 3.0
    eta = boundary_scalar * s2_projection
    side_action = eta / 2.0
    gamma = n * math.exp(-side_action)

    print("Current eta/gamma chain")
    print("=" * 25)
    print("Metric-derived or metric-forced pieces:")
    print(f"  endpoint self-similarity p = {p:.12g}")
    print(f"  phi=0 interface scalar B=p/2 = {boundary_scalar:.12g}")
    print(f"  round S2 isotropic second moment = {s2_projection:.12g}")
    print(f"  eta = B/3 = {eta:.12g}")
    print()
    print("Composable transfer piece:")
    print(f"  one-sided boundary action eta/2 = {side_action:.12g}")
    print(f"  gamma = N exp(-eta/2) = {gamma:.12g}")
    print()
    print("Conditions still required:")
    print("  1. Boundary closure observable is the H1/projective unit vector n_a.")
    print("  2. Closure constraints are represented by symmetric composable kernels.")
    print("  3. Closure nodes are physical and independent in the factor graph.")
    print()
    print("Status:")
    print("  eta is now metric-derived under condition 1.")
    print("  gamma is now transfer-derived under conditions 1 and 2.")
    print("  the hierarchy still depends on condition 3.")


if __name__ == "__main__":
    main()
