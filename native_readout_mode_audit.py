from fractions import Fraction


def main():
    projectors = {
        "A3": 3,
        "S5": 5,
        "T8": 8,
    }
    c1_image_unit = Fraction(1, 12)
    c1_domain_dim = 36

    rows = {}
    for name, rank in projectors.items():
        rows[name] = {
            "rank_readout": rank,
            "C1_weight_readout": rank * c1_image_unit,
            "domain_composite_count": rank * c1_domain_dim,
            "inverse_weight": Fraction(1, rank * c1_image_unit),
        }

    modes = {
        "C1_weight": {
            "formula": "W(P)=Tr(P)/12",
            "native_status": "best current scalar action readout candidate",
            "outputs": {name: rows[name]["C1_weight_readout"] for name in rows},
            "caution": "dimensionless action weight, not mass by itself",
        },
        "rank": {
            "formula": "D(P)=Tr(P)",
            "native_status": "projector dimension ledger",
            "outputs": {name: rows[name]["rank_readout"] for name in rows},
            "caution": "counts active image directions; not an action or mass by itself",
        },
        "domain_composite_count": {
            "formula": "C(P)=dim Lambda^2 End(H1) * Tr(P)",
            "native_status": "composite fingerprint",
            "outputs": {name: rows[name]["domain_composite_count"] for name in rows},
            "caution": "produces 108 and 180, but no native mass readout rule selects this mode yet",
        },
        "inverse_weight": {
            "formula": "1/W(P)",
            "native_status": "not selected",
            "outputs": {name: rows[name]["inverse_weight"] for name in rows},
            "caution": "do not use without a variational or spectral reason for inversion",
        },
    }

    verdict = {
        "selected_candidate": "C1_weight only",
        "fingerprints_only": ["rank", "domain_composite_count"],
        "rejected_for_now": ["inverse_weight"],
        "mass_readout": "open; no native rule maps any mode to masses yet",
    }

    print(f"rows: {rows}")
    print(f"modes: {modes}")
    print(f"verdict: {verdict}")


if __name__ == "__main__":
    main()
