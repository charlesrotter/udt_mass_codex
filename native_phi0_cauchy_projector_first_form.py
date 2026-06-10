from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    print("phi0 Cauchy projector first form")
    print("=" * 34)
    q = Fraction(1, 3)
    delta_pi = q / 2
    eta = delta_pi / 3
    side_action = eta / 2
    print("Metric boundary data at phi0:")
    print("  value constraint:       f|phi0 = 1")
    print("  C1 momentum jump:       Delta Pi_f/R = q/2")
    print("  angular boundary space: H1 = ell=1(S2)")
    print("  induced measure:        round S2 measure")
    print()
    print("For q=1/3:")
    print(f"  Delta Pi_f/R = {fmt(delta_pi)}")
    print(f"  H1 projection eta = (Delta Pi/R)/3 = {fmt(eta)}")
    print(f"  projected C1 side action = eta/2 = {fmt(side_action)}")
    print()
    print("First-form projector:")
    print("  P_phi0 = P_value(f=1) * P_jump(Delta Pi=q/2) * P_H1")
    print()
    print("On an H1 identity side action:")
    print("  P_H1 exp[-(eta/2) I3] P_H1 = exp(-1/36) P_H1")
    print("  Tr_boundary[...] = exp(-1/36) Tr(P_H1)")
    print("                  = 3 exp(-1/36)")
    print()
    print("First-form verdict:")
    print("  The metric-supplied value constraint, momentum jump, H1 projector,")
    print("  and induced boundary measure compose directly into the gamma kernel")
    print("  if phi0 is treated as an internal two-sided interface.")
    print("  What remains is proving this first-form product is the exact")
    print("  Calderon projector for the UDT phi0 bridge.")


if __name__ == "__main__":
    main()
