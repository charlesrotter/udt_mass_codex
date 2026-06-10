from fractions import Fraction


def main():
    roles = {
        "S5_wedge_S5_residual": {
            "value": Fraction(1, 36),
            "matches": "eta/2",
            "boundary_role": "one-sided projected C1 action",
            "interpretation": "side-action residual",
            "status": "native quantity already derived",
        },
        "A3_wedge_A3_residual": {
            "value": Fraction(-1, 6),
            "matches": "-q/2",
            "boundary_role": "negative of unprojected boundary momentum",
            "interpretation": "momentum/source deficit",
            "status": "native quantity already derived, sign requires orientation/source convention",
        },
    }

    possible_accounting = {
        "S5S5": {
            "needed": "one side-action unit eta/2",
            "candidate_source": "symmetric interface side action or residual boundary layer",
            "not_yet": "physical source assignment",
        },
        "A3A3": {
            "needed": "boundary momentum q/2 with opposite sign",
            "candidate_source": "C1 momentum jump/source orientation",
            "not_yet": "source supply rule",
        },
    }

    verdict = {
        "pure_residuals_are_native": True,
        "pure_residuals_are_explained_as_particles": False,
        "next": "derive source/boundary accounting rules for side-action and momentum residuals before using pure channels in spectrum construction",
    }

    print(f"roles: {roles}")
    print(f"possible_accounting: {possible_accounting}")
    print(f"verdict: {verdict}")


if __name__ == "__main__":
    main()
