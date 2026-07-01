from math import comb


def exterior_dimensions(n):
    return {k: comb(n, k) for k in range(n + 1)}


def hodge_pairs(dimensions, n):
    return {k: (dimensions[k], n - k, dimensions[n - k]) for k in range(n + 1)}


def main():
    h1_dim = 3
    end_h1_dim = h1_dim * h1_dim
    dims = exterior_dimensions(end_h1_dim)
    pairs = hodge_pairs(dims, end_h1_dim)

    notable = {
        "Lambda^2 End(H1)": dims[2],
        "Lambda^3 End(H1)": dims[3],
        "Lambda^6 End(H1)": dims[6],
        "Hodge_dual_Lambda3_Lambda6_equal": dims[3] == dims[6],
        "top_form_dimension": dims[9],
    }

    interpretation = {
        "native_input": "End(H1) has dimension 9 from the H1 carrier.",
        "fingerprint": "If a native selector chooses exterior k-forms on End(H1), then 36 and 84 appear as exact binomial dimensions.",
        "missing_selector": "This script does not derive that particle sectors must use Lambda^2 or Lambda^3 End(H1).",
        "not_legacy_claim": "This is not the old Sym^3(R7) interpretation and does not use Form-T kappa or a closure orbit.",
    }

    print(f"H1_dimension: {h1_dim}")
    print(f"End(H1)_dimension: {end_h1_dim}")
    print(f"exterior_dimensions: {dims}")
    print(f"hodge_pairs: {pairs}")
    print(f"notable: {notable}")
    print(f"interpretation: {interpretation}")


if __name__ == "__main__":
    main()
