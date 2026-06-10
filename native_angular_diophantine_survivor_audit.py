from math import comb


def lambda3_count(n: int) -> int:
    if n < 3:
        return 0
    return comb(n, 3)


def diophantine_identity_holds(j2p1: int, ell: int, k_abs: int) -> bool:
    # Legacy identity:
    # (2j+1)^2 (2ell+1)(2K+1) = C(2ell+2K+1, 2ell+1)
    left = (j2p1 * j2p1) * (2 * ell + 1) * (2 * k_abs + 1)
    right = comb(2 * ell + 2 * k_abs + 1, 2 * ell + 1)
    return left == right


def main() -> None:
    print("angular Diophantine survivor audit")
    print("=" * 36)
    print("Metric-native angular dimensions on S2:")
    print("  N_ell = 2ell + 1")
    print()
    for ell in range(5):
        n = 2 * ell + 1
        role = "scalar/background" if ell == 0 else "nonconstant angular"
        print(
            f"  ell={ell}: N={n}, role={role}, "
            f"Lambda^3 count={lambda3_count(n)}"
        )
    print()
    print("Immediate survivor facts:")
    print("  ell=0 has N=1 and is the scalar/radial tail channel.")
    print("  Tail cancellation kills that as the macro-visible matter imprint.")
    print("  ell=1 has N=3 and is the first nonconstant angular channel.")
    print("  N=3 is the first dimension with a unique Lambda^3 object.")
    print("  N>3 has multiple Lambda^3 objects, not a unique triplet.")
    print()
    print("Legacy Diophantine identity check, with 2j+1=2:")
    print("  (2j+1)^2(2ell+1)(2K+1) = C(2ell+2K+1, 2ell+1)")
    for ell in range(0, 5):
        hits = []
        for k_abs in range(1, 12):
            if diophantine_identity_holds(2, ell, k_abs):
                hits.append(k_abs)
        hit_text = ", ".join(str(hit) for hit in hits) if hits else "none"
        print(f"  ell={ell}: K hits={hit_text}")
    print()
    print("Survivor verdict:")
    print("  The Form-T-specific parts of the old triple remain quarantined.")
    print("  But its angular arithmetic points to the same native S2 fact:")
    print("    after scalar-tail cancellation, the first nonconstant angular")
    print("    bridge has dimension N=3, and N=3 is uniquely epsilon-eligible.")
    print()
    print("Connection to current q problem:")
    print("  This can pin the angular dimension N=3 without importing spinors.")
    print("  q=1/3 is then supported if the phi=0 bridge uses the dimension rule")
    print("    p = 1/N")
    print("  or if the self-similar C1 condition independently gives")
    print("    1 - 2p = p.")
    print("  The remaining proof is the metric rule connecting the transported")
    print("  angular dimension N=3 to the endpoint/first-jet exponent.")


if __name__ == "__main__":
    main()
