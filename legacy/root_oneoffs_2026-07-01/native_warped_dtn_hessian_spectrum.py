import mpmath as mp


mp.mp.dps = 50


def dtn_eigenvalue(ell: int, q: mp.mpf = mp.mpf(1) / 3) -> mp.mpf:
    if ell == 0:
        return mp.mpf("0")
    lam = mp.mpf(ell * (ell + 1))
    beta = q / 2
    nu = abs((1 - 2 / q) / 2)
    x0 = mp.sqrt(lam) / beta
    return beta * x0 * mp.besseli(nu + 1, x0) / mp.besseli(nu, x0)


def main() -> None:
    print("warped DtN Hessian spectrum")
    print("=" * 30)
    print("Self-similar collar q=1/3.")
    print("Finite angular mode branch:")
    print("  D_ell = sqrt(ell(ell+1)) I_{7/2}(6 sqrt(ell(ell+1)))")
    print("          / I_{5/2}(6 sqrt(ell(ell+1)))")
    print("for ell >= 1, and D_0=0.")
    print()
    print("ell  degeneracy  exact role                         D_ell")
    for ell in range(0, 6):
        degeneracy = 2 * ell + 1
        role = "scalar zero mode" if ell == 0 else ("H1 triplet" if ell == 1 else "higher shape block")
        dtn = dtn_eigenvalue(ell)
        print(f"{ell:>3}  {degeneracy:>10}  {role:<34} {mp.nstr(dtn, 18)}")
    print()
    print("Hessian verdict:")
    print("  If the phi0 action is the on-shell warped-collar action, the")
    print("  angular second variation is diagonal in ell,m with eigenvalues")
    print("  D_ell, up to the fixed quadratic-action normalization.")
    print("  The ell=1 block is exactly proportional to I3 by degeneracy.")
    print("  It is not equal to the intrinsic boundary L1=I3 kernel unless")
    print("  the Bessel ratio factor is removed by a separate boundary-action rule.")


if __name__ == "__main__":
    main()
