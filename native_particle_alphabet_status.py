def main():
    ledger = [
        {
            "item": "H1 carrier",
            "status": "derived pre-spectrum input",
            "content": "rank 3 harmonic angular carrier",
        },
        {
            "item": "End(H1)",
            "status": "native operator alphabet",
            "content": "dimension 9, split 1+8",
        },
        {
            "item": "T8 image",
            "status": "native active operator image",
            "content": "traceless image of commutator, split 3+5",
        },
        {
            "item": "Lambda^2 End(H1)",
            "status": "C1-weighted selector domain",
            "content": "dimension 36, uniform side weight eta/2=1/36",
        },
        {
            "item": "commutator selector",
            "status": "native functional map",
            "content": "Lambda^2 End(H1)->T8, isotropic with BBt=3P_T8",
        },
        {
            "item": "Lambda^3 End(H1)",
            "status": "native three-form domain",
            "content": "dimension 84 for Omega(A,B,C)=Tr(A[B,C])",
        },
        {
            "item": "Lambda^3 T8",
            "status": "active three-form domain",
            "content": "dimension 56, active fraction 2/3",
        },
        {
            "item": "7-family",
            "status": "native filter fingerprint",
            "content": "2/7 and 5/7 from Lambda^2 T8 image/kernel fractions",
        },
        {
            "item": "108 and 180",
            "status": "native composite fingerprints",
            "content": "3*36 and 5*36, no readout rule",
        },
        {
            "item": "63",
            "status": "weak fingerprint",
            "content": "9*7, not yet a native dimension or invariant",
        },
        {
            "item": "mass spectrum",
            "status": "open",
            "content": "requires native readout rule from operator hierarchy to observed masses",
        },
    ]

    print("particle_alphabet_status:")
    for entry in ledger:
        print(f"  - {entry}")
    print()
    print("frontier:")
    print("  derive a native readout rule; do not attach particle labels or masses before that rule exists")


if __name__ == "__main__":
    main()
