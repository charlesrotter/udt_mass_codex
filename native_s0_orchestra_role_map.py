from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    name: str
    role_for_s0: str
    contributes: str
    must_not_do: str


INSTRUMENTS = [
    Instrument(
        "phi0 interface jump",
        "weight source",
        "q/2 local angular stress scale, projected to eta=q/6",
        "be counted again as a separate coefficient after eta is formed",
    ),
    Instrument(
        "ell=1 Laplacian",
        "operator shape",
        "L1=I3 on H1",
        "supply the eta clock or branch coefficients by itself",
    ),
    Instrument(
        "heat semigroup",
        "composition law",
        "exp(-t L1), trace, and gluing algebra once t is known",
        "choose t without the boundary action",
    ),
    Instrument(
        "symmetric gluing",
        "side splitter",
        "eta -> eta/2 per side if full boundary action composes symmetrically",
        "be assumed if the boundary object is bulk-DtN instead",
    ),
    Instrument(
        "proper radial/DtN operator",
        "bulk-memory alternative",
        "warped propagation kernel if transfer is through the collar",
        "be multiplied together with interface-local transfer for the same variable",
    ),
    Instrument(
        "H1 frame / CP1 bridge / E1 relative plane",
        "typed variable arena",
        "coordinates for possible S0[x] Hessian blocks",
        "create independent nodes unless the boundary graph proves independence",
    ),
    Instrument(
        "compact bundle primitivity",
        "branch selector",
        "conditional M1 activation and M2 demotion if Pbundle0 is banked",
        "supply a numeric coefficient by occupation fiat",
    ),
]


def main() -> None:
    print("S0 orchestra role map")
    print("=" * 22)
    for instrument in INSTRUMENTS:
        print(instrument.name)
        print(f"  role for S0: {instrument.role_for_s0}")
        print(f"  contributes: {instrument.contributes}")
        print(f"  must not do: {instrument.must_not_do}")
        print()

    print("Orchestra verdict:")
    print("  S0 may be a coupled composition of already-uncovered metric instruments.")
    print("  The safe rule is role composition, not additive mechanism stacking.")


if __name__ == "__main__":
    main()
