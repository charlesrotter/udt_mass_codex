from fractions import Fraction


def main():
    a3_rank = 3
    c1_image_unit = Fraction(1, 12)
    a3_weight = a3_rank * c1_image_unit

    report = {
        "native_quantity": "W(A3)=Tr(P_A3)/12",
        "value": a3_weight,
        "equals_one_quarter": a3_weight == Fraction(1, 4),
        "inputs": [
            "T8=A3+S5",
            "Tr(P_A3)=3",
            "C1/commutator image unit=1/12",
        ],
        "legacy_reinterpretation": {
            "old_form": "source(kappa=-1) ~= 1/4",
            "new_status": "candidate native projector weight",
            "quarantine": "do not restore kappa or Form-T source interpretation",
        },
        "not_claimed": [
            "A3 is a particle",
            "1/4 is a mass coefficient",
            "old Dirac source derivation is recovered",
        ],
    }

    print(f"report: {report}")


if __name__ == "__main__":
    main()
