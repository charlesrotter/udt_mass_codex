def main() -> None:
    print("second-variation cross-term audit")
    print("=" * 35)
    print("Use the local quadratic form for angular boundary data:")
    print("  S(q,a) = A(q) + (1/2) D_l(q) sum_m a_m^2 + higher order")
    print()
    print("At the background angular amplitude a_m=0:")
    print("  dS/dq = A'(q)")
    print("  dS/da_m = D_l(q) a_m")
    print("  d2S/dq da_m = D_l'(q) a_m = 0")
    print("  d2S/da_m da_n = D_l(q) delta_mn")
    print()
    print("Exact consequence:")
    print("  The scalar q block and the angular amplitude blocks are Hessian")
    print("  block-diagonal at zero angular background amplitude.")
    print()
    print("Audit verdict:")
    print("  A q-angular Schur complement cannot generate branch coefficients")
    print("  at second order unless a nonzero background angular mode, boundary")
    print("  constraint, or explicit same-representation cross term is derived.")


if __name__ == "__main__":
    main()
