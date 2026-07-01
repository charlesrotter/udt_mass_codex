from fractions import Fraction


def fmt(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    q = Fraction(1, 3)
    boundary_momentum = -q / 2
    conjugate_derivative = -boundary_momentum
    eta = conjugate_derivative / 3
    transfer_side = eta / 2

    print("Exact C1 boundary identities")
    print("=" * 29)
    print("Metric variable:")
    print("  f = exp(-2 phi)")
    print()
    print("Exact static radial C1 density:")
    print("  sqrt(-g) e^(-2phi) g^rr phi'^2")
    print("  = r^2 e^(-4phi) phi'^2")
    print("  = (1/4) r^2 f'^2")
    print()
    print("Exact variation:")
    print("  delta S_C1 boundary = [(1/2) r^2 f' delta f]_boundary")
    print("  Pi_f = (1/2) r^2 f'")
    print()
    print("At the phi0 collar with R=1, f=1, f'=-q:")
    print("  Pi_f = -q/2")
    print("  dS_boundary/df = -Pi_f = q/2")
    print()
    print("Exact self-similar q=1/3 chain:")
    print(f"  q = {fmt(q)}")
    print(f"  Pi_f = {fmt(boundary_momentum)}")
    print(f"  -Pi_f = {fmt(conjugate_derivative)}")
    print(f"  H1/S2 projection = (-Pi_f)/3 = {fmt(eta)}")
    print(f"  one-sided transfer = eta/2 = {fmt(transfer_side)}")
    print()
    print("Exact shell jump identity for flat exterior:")
    print("  [K^a_b] = diag(q/2, 0, 0)")
    print("  [K] = q/2")
    print("  [K^a_b] - delta^a_b[K] = (0, -q/2, -q/2)")
    print()
    print("No-approximation verdict:")
    print("  These are exact identities for the stated metric ansatz and collar data.")
    print("  What remains open is not to be approximated:")
    print("    - derive the boundary functional,")
    print("    - derive the typed closure kernel,")
    print("    - derive branch coefficients.")


if __name__ == "__main__":
    main()
