import math


def integrate_s2_moments(n_theta: int = 400, n_phi: int = 800) -> list[list[float]]:
    # Midpoint quadrature on the unit sphere, normalized by 4*pi.
    moment = [[0.0 for _ in range(3)] for _ in range(3)]
    dtheta = math.pi / n_theta
    dphi = 2.0 * math.pi / n_phi
    total_area = 0.0

    for i in range(n_theta):
        theta = (i + 0.5) * dtheta
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        for j in range(n_phi):
            phi = (j + 0.5) * dphi
            vector = (
                sin_theta * math.cos(phi),
                sin_theta * math.sin(phi),
                cos_theta,
            )
            weight = sin_theta * dtheta * dphi
            total_area += weight
            for a in range(3):
                for b in range(3):
                    moment[a][b] += vector[a] * vector[b] * weight

    return [[entry / total_area for entry in row] for row in moment]


def main() -> None:
    b = 1.0 / 6.0
    moment = integrate_s2_moments()

    print("S2 isotropic projection audit")
    print("=" * 31)
    print("For the round metric two-sphere, let n_a be the unit coordinate vector.")
    print("The isotropic projection is the normalized second moment:")
    print("  <n_a n_b> = integral n_a n_b dOmega / integral dOmega")
    print()
    print("Numerical moment matrix:")
    for row in moment:
        print("  " + " ".join(f"{value: .12f}" for value in row))
    print()
    print("Analytic result:")
    print("  <n_a n_b> = delta_ab / 3")
    print()
    print("Applying scalar boundary budget B=1/6:")
    print(f"  B/3 = {b / 3.0:.12g}")
    print("  B <n_a n_b> = (1/18) delta_ab")
    print()
    print("Projection verdict:")
    print("  - The round S2 metric itself supplies the trace-preserving equal split.")
    print("  - This derives the identity lift S_label=(B/3) I_3 if the boundary")
    print("    scalar couples through the isotropic H1/projective unit vector.")
    print("  - For p=1/3, B=1/6, so eta=1/18 follows from the S2 average.")
    print("  - Remaining condition: the closure observable must be the H1/projective")
    print("    unit vector n_a, not an anisotropic selected component.")


if __name__ == "__main__":
    main()
