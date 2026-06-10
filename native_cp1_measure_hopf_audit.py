import math


def fs_density_chi(chi: float) -> float:
    # CP1 in coordinate z = tan(chi/2) exp(i phi).
    # Fubini-Study area is proportional to sin(chi) dchi dphi.
    return math.sin(chi)


def integrate_moments(n_chi: int = 800, n_phi: int = 800) -> list[list[float]]:
    dchi = math.pi / n_chi
    dphi = 2.0 * math.pi / n_phi
    total = 0.0
    mat = [[0.0 for _ in range(3)] for _ in range(3)]
    for i in range(n_chi):
        chi = (i + 0.5) * dchi
        weight_chi = fs_density_chi(chi)
        for j in range(n_phi):
            phi = (j + 0.5) * dphi
            n = (
                math.sin(chi) * math.cos(phi),
                math.sin(chi) * math.sin(phi),
                math.cos(chi),
            )
            weight = weight_chi * dchi * dphi
            total += weight
            for a in range(3):
                for b in range(3):
                    mat[a][b] += n[a] * n[b] * weight
    return [[x / total for x in row] for row in mat]


def main() -> None:
    moment = integrate_moments()
    print("CP1/Hopf measure audit")
    print("=" * 24)
    print("CP1 with Fubini-Study measure in polar coordinate chi has area")
    print("density proportional to:")
    print("  sin(chi) dchi dphi")
    print()
    print("Under the Hopf/projective map, the bilinear unit vector is:")
    print("  n=(sin chi cos phi, sin chi sin phi, cos chi)")
    print()
    print("Numerical second moment:")
    for row in moment:
        print("  " + " ".join(f"{value: .12f}" for value in row))
    print()
    print("Analytic expectation:")
    print("  <n_a n_b>_CP1 = delta_ab / 3")
    print()
    print("Measure verdict:")
    print("  - The CP1 Fubini-Study measure pushes forward to the round S2 measure.")
    print("  - The primitive M1 Hopf bridge does not introduce a hidden anisotropic")
    print("    measure at the level of the bare projective geometry.")
    print("  - Any M1-specific measure correction must come from the boundary action")
    print("    or compact-bundle occupation weight, not from CP1 geometry alone.")


if __name__ == "__main__":
    main()
