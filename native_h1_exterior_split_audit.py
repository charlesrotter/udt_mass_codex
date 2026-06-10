from math import comb


def exterior_sum_dim(total_grade, dims):
    pieces = []

    def walk(index, remaining, current):
        if index == len(dims):
            if remaining == 0:
                dim = 1
                for part_grade, part_dim in zip(current, dims):
                    dim *= comb(part_dim, part_grade)
                pieces.append((tuple(current), dim))
            return
        max_grade = min(dims[index], remaining)
        for grade in range(max_grade + 1):
            walk(index + 1, remaining - grade, current + [grade])

    walk(0, total_grade, [])
    return pieces


def format_split(labels, pieces):
    out = []
    for grades, dim in pieces:
        factors = [
            f"Lambda^{grade} {label}"
            for grade, label in zip(grades, labels)
            if grade
        ]
        if not factors:
            factors = ["scalar 1"]
        out.append((" wedge ".join(factors), dim))
    return out


def main():
    trace_traceless_labels = ["trace", "T8"]
    trace_traceless_dims = [1, 8]
    tensor_labels = ["A3", "S5"]
    tensor_dims = [3, 5]

    lambda2_end = format_split(
        trace_traceless_labels, exterior_sum_dim(2, trace_traceless_dims)
    )
    lambda3_end = format_split(
        trace_traceless_labels, exterior_sum_dim(3, trace_traceless_dims)
    )
    lambda2_t8 = format_split(tensor_labels, exterior_sum_dim(2, tensor_dims))
    lambda3_t8 = format_split(tensor_labels, exterior_sum_dim(3, tensor_dims))

    hodge_complements_9d = {
        "Lambda^0": "Lambda^9",
        "Lambda^1": "Lambda^8",
        "Lambda^2": "Lambda^7",
        "Lambda^3": "Lambda^6",
        "Lambda^4": "Lambda^5",
    }

    result = {
        "native_splits": {
            "End(H1)": "1 + 8",
            "T8": "3 + 5",
        },
        "Lambda^2_End(H1)_split": lambda2_end,
        "Lambda^3_End(H1)_split": lambda3_end,
        "Lambda^2_T8_split": lambda2_t8,
        "Lambda^3_T8_split": lambda3_t8,
        "dimension_checks": {
            "Lambda^2_End(H1)": sum(dim for _, dim in lambda2_end),
            "Lambda^3_End(H1)": sum(dim for _, dim in lambda3_end),
            "Lambda^2_T8": sum(dim for _, dim in lambda2_t8),
            "Lambda^3_T8": sum(dim for _, dim in lambda3_t8),
        },
        "hodge_complements_9d": hodge_complements_9d,
        "candidate_meaning_of_7": "In the 9D operator alphabet, grade 7 is the Hodge complement of grade 2. This is a native grade relation, not yet a seven-position orbit.",
        "selector_status": "The decompositions are exact once an exterior/Hodge selector is admitted; this script does not derive that selector for particle sectors.",
    }

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
