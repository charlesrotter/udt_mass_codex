import sympy as sp


def main() -> None:
    theta, phi = sp.symbols("theta phi", real=True)

    n = sp.Matrix(
        [
            sp.sin(theta) * sp.cos(phi),
            sp.sin(theta) * sp.sin(phi),
            sp.cos(theta),
        ]
    )
    n_theta = n.diff(theta)
    n_phi = n.diff(phi)

    g_tt = sp.simplify(n_theta.dot(n_theta))
    g_tp = sp.simplify(n_theta.dot(n_phi))
    g_pp = sp.simplify(n_phi.dot(n_phi))

    eps = sp.LeviCivita
    area_pullback = sp.Integer(0)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                area_pullback += eps(i, j, k) * n[i] * n_theta[j] * n_phi[k]
    area_pullback = sp.simplify(area_pullback)

    print("H1 area-form projector bridge")
    print("=" * 31)
    print("Use the ell=1 coordinate harmonics on the unit S2:")
    print("  n = (sin(theta)cos(phi), sin(theta)sin(phi), cos(theta))")
    print()
    print("Round metric recovered from H1 embedding:")
    print(f"  d_theta n . d_theta n = {g_tt}")
    print(f"  d_theta n . d_phi n   = {g_tp}")
    print(f"  d_phi n . d_phi n     = {g_pp}")
    print()
    print("Canonical H1 epsilon/area identity:")
    print("  eps_ijk n_i d_theta n_j d_phi n_k =")
    print(f"    {area_pullback}")
    print("  which is exactly the S2 area density.")
    print()
    print("Isotropic H1 second moment:")
    print("  <n_i n_j>_S2 = delta_ij / 3")
    print()
    print("Trace-normalized scalar action on H1:")
    print("  scalar B acting as B I_3 has per-label share B/3")
    print()
    print("Collar transgression candidate:")
    print("  d ln f wedge omega_H1 = -q d ln r wedge dOmega")
    print("  normalized H1 share = q/3")
    print()
    print("No-overclaim verdict:")
    print("  H1 supplies a canonical rank-one scalar angular carrier:")
    print("    Lambda^3 H1 -> S2 area form.")
    print("  This justifies the angular 1/3 without choosing a projector by hand.")
    print("  But d ln f wedge omega_H1 is boundary/transgression-like.")
    print("  By itself it supports a Cauchy/interface action more directly than")
    print("  an ordinary bulk potential source.")
    print()
    print("Updated proof target:")
    print("  derive whether the phi0 Calderon/Cauchy boundary action uses this")
    print("  H1 area-form carrier to impose the rank-one source share q/3.")


if __name__ == "__main__":
    main()
