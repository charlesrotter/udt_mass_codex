def main() -> None:
    print("boundary functional q correction")
    print("=" * 33)
    print("Earlier shorthand:")
    print("  a conjugate boundary functional can set q through dS/df=q/2")
    print()
    print("Stricter variational reading:")
    print("  dS/df cancels the C1 boundary momentum for the q supplied by")
    print("  the interior/collar solution.")
    print()
    print("It selects q only if:")
    print("  1. S_b contains an independent slope/extrinsic-curvature variable, or")
    print("  2. varying the full boundary/collar action gives a q stationarity equation.")
    print()
    print("Otherwise:")
    print("  q is inherited from the collar q-flow/self-consistency problem.")
    print()
    print("No-approximation verdict:")
    print("  Do not treat dS/df=q/2 as a derivation of q.")
    print("  It is a momentum-matching condition unless a q-variation is present.")


if __name__ == "__main__":
    main()
