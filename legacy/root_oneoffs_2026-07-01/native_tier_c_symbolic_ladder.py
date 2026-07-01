from fractions import Fraction
import math


ETA = Fraction(1, 18)
SIDE = ETA / 2
GAMMA = 3.0 * math.exp(-float(SIDE))
DEPTH_M1 = 5
DEPTH_E1 = 7


def main() -> None:
    print("Tier C symbolic ladder")
    print("=" * 22)
    print("Banked active-lane inputs:")
    print("  P_phi0: q=1/3 -> eta=1/18")
    print("  P_transfer: gamma=3 exp(-1/36)")
    print("  P_depth_M1: n_M1=5")
    print("  P_depth_E1: n_E1=7")
    print()
    print(f"gamma = {GAMMA:.12g}")
    print(f"gamma^5 = {GAMMA ** DEPTH_M1:.12g}")
    print(f"gamma^7 = {GAMMA ** DEPTH_E1:.12g}")
    print(f"gamma^2 = {GAMMA ** (DEPTH_E1 - DEPTH_M1):.12g}")
    print()
    print("Coefficient-free symbolic structure:")
    print("  M1/electron-anchor ratio = C_M1 gamma^5")
    print("  E1/electron-anchor ratio = C_E1 gamma^7")
    print("  E1/M1 ratio = (C_E1/C_M1) gamma^2")
    print()
    print("What Tier C licenses:")
    print("  the exponents 5 and 7 inside the banked graph")
    print("  the universal gamma powers inside the interface-local branch")
    print()
    print("What Tier C does not license:")
    print("  the values of C_M1 or C_E1")
    print("  identification of M1/E1 with observed particles")
    print("  dimensional masses")


if __name__ == "__main__":
    main()
