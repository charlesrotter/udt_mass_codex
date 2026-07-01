from fractions import Fraction
from math import comb, isqrt


def c1_side_action_for_n(n):
    # On the one-graph branch q=1/N:
    # eta/2 = q/(4N) = 1/(4N^2).
    return Fraction(1, 4 * n * n)


def lambda2_end_dim_for_n(n):
    return comb(n * n, 2)


def main():
    rows = []
    locks = []
    for n in range(1, 13):
        dim = lambda2_end_dim_for_n(n)
        c1_side = c1_side_action_for_n(n)
        reciprocal = None if dim == 0 else Fraction(1, dim)
        match = dim != 0 and c1_side == reciprocal
        rows.append(
            {
                "N": n,
                "dim_End": n * n,
                "dim_Lambda2_End": dim,
                "C1_side_action": c1_side,
                "1_over_dim_Lambda2_End": reciprocal,
                "match": match,
            }
        )
        if match:
            locks.append(n)

    algebraic_condition = "C(N^2,2)=4N^2 -> N^2(N^2-1)/2=4N^2 -> N^2-1=8 -> N=3"

    print(f"rows: {rows}")
    print(f"locks: {locks}")
    print(f"algebraic_condition: {algebraic_condition}")
    print(f"integer_check: {isqrt(9) == 3 and 3 * 3 == 9}")
    print(
        "interpretation: The projected C1 side action equals the reciprocal "
        "of dim Lambda^2 End(H) only on the N=3 branch. This strengthens "
        "Lambda^2 End(H1) as a selector candidate, but does not by itself "
        "prove the functional particle-sector action."
    )


if __name__ == "__main__":
    main()
